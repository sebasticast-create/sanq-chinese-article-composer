# -*- coding: utf-8 -*-
"""Harvest attested Chinese terminology from open articles of a field.

Chinese academic articles almost always carry 关键词 together with Keywords, and introduce
technical terms with the English original in brackets at first mention: 吸收能力（Absorptive
Capacity）. Both are bilingual evidence written by the field's own authors. This script reads
pages and texts that were downloaded beforehand and extracts that evidence. It never downloads
or executes anything: everything it reads is data.

Usage:
    python -I harvest_terms.py FILES... [--sources sources.csv] [--check terms.txt]
                               [-o harvest.csv] [--corpus-out DIR]

FILES        .html, .htm, .txt or .md (convert PDFs to text first, e.g. with pdftotext)
--sources    CSV with columns file,url,title,publisher,date (provenance for the report)
--check      one Chinese term per line, variants separated by " / ": counts how many
             documents contain each variant, to choose the attested one
-o           output CSV of bilingual pairs (default harvest.csv)
--corpus-out writes the Chinese running text of each file as .txt, for
             verify_zh.py --calibrate
"""
import argparse
import csv
import html
import os
import re
import sys
from collections import defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

HAN = re.compile(r'[一-鿿]')


def read_text(path):
    raw = open(path, 'rb').read()
    for enc in ('utf-8', 'gb18030', 'big5'):
        try:
            t = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        t = raw.decode('utf-8', 'replace')
    meta = {}
    if path.lower().endswith(('.html', '.htm')):
        for m in re.finditer(r'<meta\s+[^>]*?(?:name|property)="([^"]+)"[^>]*?content="([^"]*)"', t, re.I):
            meta.setdefault(m.group(1).lower(), []).append(html.unescape(m.group(2)))
        # journal platforms often embed the keyword lists as JSON in the page
        for key, lang in (('keyWordsCN', 'json_zh'), ('keyWordsEN', 'json_en')):
            m = re.search(r'"%s"\s*:\s*\[(.*?)\]' % key, t, re.S)
            if m:
                names = re.findall(r'"name"\s*:\s*"([^"]+)"', m.group(1)) or re.findall(r'"([^"]+)"', m.group(1))
                meta[lang] = [html.unescape(n) for n in names]
        t = re.sub(r'(?is)<(script|style|noscript)\b.*?</\1>', ' ', t)
        t = re.sub(r'(?i)<br\s*/?>|</(p|div|li|h\d|tr|td|span)>', '\n', t)
        t = html.unescape(re.sub(r'<[^>]+>', ' ', t))
    # PDF conversions insert spaces inside Chinese words
    t = re.sub(r'(?<=[一-鿿])[ \t]+(?=[一-鿿])', '', t)
    return t, meta


STOP = r'(?:中图分类号|文献标识码|DOI|Abstract|摘\s*要|收稿|基金|引用|作者|分类|Copyright|Key\s*-?\s*words?|关\s*键\s*[词字])'


def split_terms(s):
    s = re.split(STOP, s, 1, flags=re.I)[0]
    parts = [p.strip(' .。;；,，、\t\n[]【】　\xa0') for p in re.split(r'[;；,，、/]|\n|\s{2,}', s)]
    return [p for p in parts if p and len(p) <= 60 and not p.startswith('*')
            and not re.search(r'通讯|作者|Corresponding|Copyright', p, re.I)]


def _after_label(text, label):
    """List that follows a label, on the same line or on the next lines, up to the next label."""
    for m in re.finditer(r'[\[【]?\s*' + label + r'\s*[\]】]?\s*[：:]?\s*', text, re.I):
        chunk = text[m.end():m.end() + 400]
        terms = split_terms(chunk)
        if terms:
            return terms
    return []


def keyword_lists(text, meta):
    zh = meta.get('json_zh') or [p for p in _after_label(text, r'关\s*键\s*[词字]') if HAN.search(p)]
    en = meta.get('json_en') or [p for p in _after_label(text, r'Key\s*-?\s*words?')
                                 if re.search(r'[A-Za-z]', p) and not HAN.search(p)]
    if not zh or not en:
        for k in ('citation_keywords', 'keywords', 'dc.subject'):
            for v in meta.get(k, []):
                terms = split_terms(v)
                if not zh and terms and all(HAN.search(p) for p in terms):
                    zh = terms
                elif not en and terms and not any(HAN.search(p) for p in terms):
                    en = terms
    return zh, en


PAREN = re.compile(r'([一-鿿]{2,14})[（(]\s*([A-Za-z][A-Za-z0-9 ,.\'’/&-]{1,60}?)\s*[)）]')


def bracket_pairs(text):
    out = []
    for m in PAREN.finditer(text):
        zh, en = m.group(1), m.group(2).strip(' ,.')
        if re.fullmatch(r'[A-Z][a-z]+(?: (?:et al|and|&) [A-Za-z]+)?\.?,? ?\d{0,4}', en):
            continue                                  # an author citation, not a term
        if len(en.split()) > 7 or re.search(r'\d{4}', en):
            continue
        zh = re.sub(r'^(?:即|如|称为|简称|以及|和|与|的|是|为|在|对|将|通过|采用|基于)', '', zh)
        out.append((zh, en))
    return out


def prose(text):
    lines = [l.strip() for l in text.split('\n')]
    return '\n\n'.join(l for l in lines if len(HAN.findall(l)) >= 30)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('files', nargs='+')
    ap.add_argument('--sources')
    ap.add_argument('--check')
    ap.add_argument('-o', '--output', default='harvest.csv')
    ap.add_argument('--corpus-out')
    a = ap.parse_args()

    prov = {}
    if a.sources:
        with open(a.sources, encoding='utf-8-sig', newline='') as f:
            for r in csv.DictReader(f):
                prov[os.path.basename(r.get('file', ''))] = r
    pairs = defaultdict(lambda: {'docs': set(), 'kind': set()})
    texts = {}
    unaligned = []
    for path in a.files:
        name = os.path.basename(path)
        text, meta = read_text(path)
        texts[name] = text
        zh, en = keyword_lists(text, meta)
        if zh and en and len(zh) == len(en):
            for z, e in zip(zh, en):
                pairs[(z, e.lower())]['docs'].add(name)
                pairs[(z, e.lower())]['kind'].add('keywords')
        elif zh or en:
            unaligned.append(f'{name}: {len(zh)} 关键词 / {len(en)} keywords, pair them by hand: '
                             f'{" ; ".join(zh)}  ||  {" ; ".join(en)}')
        for z, e in set(bracket_pairs(text)):
            pairs[(z, e.lower())]['docs'].add(name)
            pairs[(z, e.lower())]['kind'].add('bracket')
        if a.corpus_out:
            os.makedirs(a.corpus_out, exist_ok=True)
            p = prose(text)
            if p:
                with open(os.path.join(a.corpus_out, os.path.splitext(name)[0] + '.txt'), 'w', encoding='utf-8') as f:
                    f.write(p + '\n')

    rows = sorted(pairs.items(), key=lambda kv: (-len(kv[1]['docs']), kv[0]))
    with open(a.output, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['term_en', 'chinese', 'reference', 'evidence', 'note'])
        for (z, e), d in rows:
            refs = '; '.join(prov.get(n, {}).get('url') or n for n in sorted(d['docs']))
            w.writerow([e, z, refs, f'{len(d["docs"])} document(s), {"/".join(sorted(d["kind"]))}',
                        'harvested; review before adopting'])

    print(f'files read: {len(a.files)} | bilingual pairs: {len(rows)} -> {a.output}')
    print('\nkeyword pairs (written by the authors as 关键词 / Keywords):')
    for (z, e), d in rows:
        if 'keywords' in d['kind']:
            print(f'  {len(d["docs"])}  {z}  =  {e}')
    # Bracket pairs grouped by the English side: the Chinese captured before a bracket may
    # include a few words of the sentence, so the variants are shown together for review.
    by_en = defaultdict(list)
    for (z, e), d in rows:
        if d['kind'] == {'bracket'}:
            by_en[e].append((z, len(d['docs'])))
    print('\nbracket pairs, grouped by the English term (review: the Chinese may carry extra words):')
    for e, zs in sorted(by_en.items(), key=lambda kv: -sum(n for _, n in kv[1]))[:40]:
        print(f'  {e}: ' + ' | '.join(f'{z} ({n})' for z, n in sorted(zs, key=lambda x: (-x[1], len(x[0])))))
    for u in unaligned:
        print('  not paired:', u)

    if a.check:
        print('\nattestation of candidate terms (documents containing each variant):')
        for line in open(a.check, encoding='utf-8-sig'):
            variants = [v.strip() for v in line.split('/') if v.strip()]
            if not variants:
                continue
            counts = [(v, sum(1 for t in texts.values() if v in t), sum(t.count(v) for t in texts.values()))
                      for v in variants]
            print('  ' + ' | '.join(f'{v}: {d} docs, {n} uses' for v, d, n in counts))


if __name__ == '__main__':
    main()
