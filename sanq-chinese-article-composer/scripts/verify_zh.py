# -*- coding: utf-8 -*-
"""Mechanical verifier for academic translations into Chinese.

It is not a reviewer: it opens the files and measures. A translation can be perfectly faithful
(every paragraph, every figure) and still be rejected for its Chinese, so it measures three
things: fidelity to the source, register against reference rates of Chinese academic prose,
and format.

Usage:
    python verify_zh.py TRANSLATION [--source SOURCE] [--glossary GLOSSARY.csv]
                        [--profile thesis|article|report] [--config CONFIG.json] [--json]
    python verify_zh.py --calibrate CORPUS_FILE [CORPUS_FILE ...] -o CONFIG.json

TRANSLATION and SOURCE may be .md, .txt or .docx. Only the Python standard library is used.

Levels:
    FAIL    must be fixed before delivery (exit code 1)
    WARN    must be looked at; fix it or justify it in the report
    REVIEW  passages a human should read (e.g. causal wording); never blocks
    INFO    measurements

Every threshold is in DEFAULTS below, documented in README.md, and can be overridden with
--config. The defaults were measured on Chinese running prose in economics (two master's
theses and six journal articles, about 149,000 characters). For another field, recalibrate
with --calibrate on a corpus of that field: the same lists and the same extraction are then
used on both sides, which is the only way a comparison is valid.
"""
import argparse
import csv
import json
import math
import os
import re
import statistics
import sys
import zipfile
from collections import Counter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# ----------------------------------------------------------------- thresholds

DEFAULTS = {
    # length (characters without whitespace; sentences split at 。！？；)
    'long_sentence_chars': 90,          # corpus p90 = 87
    'max_sentence_chars': 140,          # corpus p99 = 140
    'long_sentence_share_max': 0.10,    # WARN if more than this share exceeds long_sentence_chars
    'long_paragraph_chars': 340,        # corpus p90 = 337
    'long_paragraph_share_max': 0.10,
    'monolith_paragraph_chars': 1000,   # no paragraph of this size exists in the corpus
    # rates per 10,000 Chinese characters of running prose
    'min_chars_for_rates': 3000,        # below this, rates are reported but not judged
    'connective_density_min': 92.0,     # two reference theses: 92.4 and 96.0 with CONNECTIVES
    'connective_forms_min': 48,         # 53 and 48 distinct forms
    'min_chars_for_forms': 20000,       # variety grows with length; judged only on long texts
    'enumerator_rate_min': 6.0,         # corpus 16.0 (theses 12.0 and 19.1)
    'min_chars_for_enumerators': 10000,
    'ta_rate_max': 5.0,                 # 它/它们; corpus 1.7
    'metatext_per_chars': 20000,        # one 值得注意的是-type phrase per 20,000 characters
    'repeat_formula_min': 6,            # same closing/transition formula this many times
    'consecutive_benwen_max': 2,        # pairs of consecutive sentences both opened by 本文
    # fidelity
    'paragraph_tolerance_abs': 2,
    'paragraph_tolerance_rel': 0.015,
    'ratio_low': 0.70,                  # paragraph length ratio vs median ratio: omission?
    'ratio_high': 1.50,                 # addition?
    'number_min_int_digits': 3,         # integers with fewer digits are not checked
    # format
    'caption_title_max_chars': 45,
    'allowed_fonts': ['SimSun', 'SimHei', 'Times New Roman', 'Cambria Math', '宋体', '黑体',
                      '方正小标宋简体', '楷体', 'KaiTi', '仿宋', 'FangSong'],
    'latin_whitelist': [],              # variable names allowed glued to Chinese characters
    'calques': {},                      # extra calques: {"regex": ["warn"|"fail", "suggestion"]}
    # How the field states statistical significance:
    #   economics  在N%水平上显著 / 显著为正 (one form, checked for mixing)
    #   medicine   差异有统计学意义 (P<0.05); 显著性差异 / 差异显著 are flagged, as journal
    #              author guidelines (稿约) ask
    #   none       no check
    'significance_style': 'economics',
}

# Connective list used for density. Thresholds above were measured with THIS list.
CONNECTIVES = sorted(set("""
首先 其次 再次 最后 第一 第二 第三 第四 第五 一方面 另一方面 其一 其二 其三
因此 因而 从而 由此 故 所以 这意味着 这表明 这说明 可见 究其原因 原因在于 之所以
然而 但是 不过 相反 与之相反 尽管 虽然 反之 相比之下 与此不同
此外 同时 并且 而且 进一步 更进一步 不仅 而是 与此同时 相应地 正因如此 也就是说
综上 综上所述 总体而言 总的来看 总之 由此可见 据此 基于此 归纳起来 换言之 具体而言
在一定程度上 总体上 大体上 有待 并不必然 未必 就本文而言 对此 在于
结果表明 结果显示 研究表明 研究发现 实证结果表明 回归结果显示 这一结果 上述结果
""".split()))

ENUMERATORS = r'首先|其次|再次|最后|第[一二三四五](?:，|、|环节|方面|条|点)'
ANNOUNCEMENTS = r'本[节章](?:将|主要|旨在)|下面[^，。]{0,4}将|接下来[^，。]{0,4}将|下文将'
METATEXT = r'值得注意的是|需要(?:指出|说明|强调)的是'
REPEATED = r'基于[^，。]{0,10}，本文提出|综上所述|由此可见|这意味着|值得注意的是'

# Calques of source-language syntax, zero or near zero in the reference corpus.
# (regex, level, suggestion)
CALQUES = [
    (r'其目的是双重的|是双重的', 'fail', '有两重目的 / 包含两重含义 / 体现在两个方面'),
    (r'使这一成为可能', 'fail', '使这一点成为可能'),
    (r'以[正负]号进入', 'fail', '显著为正 / 显著为负'),
    (r'使得可以', 'fail', '使……能够 / 有助于'),
    (r'据作者所知', 'fail', '就现有文献而言'),
    (r'(?<![增参施附追添更])加以(?![及下上外内后前来往])', 'warn', '对……进行…… / bare verb'),
    (r'相联系', 'warn', '正相关 / 负相关 / 显著为正'),
    (r'标准误为', 'warn', '系数为X（标准误：Y）'),
    (r'之所以', 'warn', '源于 / 由于 / 原因在于, or restructure'),
    (r'正因如此', 'warn', '鉴于此 / 据此'),
    (r'是直接的', 'warn', '由此可以直接得出……'),
    (r'(?<![依根])据以(?![往上下前来])', 'warn', '作为……的依据'),
    (r'不在于[^。]{0,40}而在于', 'warn', '并非……，而是……'),
    (r'(?<!可)支配着?(?!收入|权)', 'warn', '决定了 / 影响 (for variables)'),
    (r'读作|读法', 'warn', '理解为 / 解释'),
    (r'第一是|第[二三四]项', 'warn', '第一，……；第二，……'),
    (r'何况|况且', 'warn', '此外 / 而且'),
    (r'名目(?!利率|汇率|GDP|工资|价格|收入)|值得做的是|所能支撑|要紧的是|呈现在[^。]{0,10}面前', 'warn', 'plain academic verb'),
    (r'形式检验', 'warn', '正式检验'),
    (r'专业化于', 'warn', '专门生产 / 专门从事'),
    (r'政策处方', 'warn', '政策方案'),
    (r'不必然', 'warn', '不一定'),
    (r'之物', 'warn', '……的产品 / modern form'),
    (r'笔者', 'warn', '本文 / 本研究'),
    (r'我们', 'warn', '本文 / 本研究 (impersonal register)'),
    (r'填补[^。]{0,6}空白', 'warn', '研究切入点 (master level)'),
]

CAUSAL = (r'因果效应|因果关系|导致|促进了|带来了|引起了?|造成了?|推动了|'
          r'使得?[^，。；]{0,14}(?:提高|提升|增加|下降|降低|上升|改善)')

HAN = re.compile(r'[一-鿿]')
CAPTION = re.compile(r'^(?:表|图)\s?\d+(?:[-.－]\d+)?\s')
NOTE = re.compile(r'^(?:注[：:]|资料来源[：:]|数据来源[：:]|续表|Notes?[:.]|Sources?[:.]|Nota[:.]|Fuente[s]?[:.])')
SRC_CAPTION = re.compile(r'^\**\s*(?:Table|Figure|Fig\.|Tabla|Cuadro|Figura|Gráfico|Tableau)\s+\d+', re.I)


def han_count(s):
    return len(HAN.findall(s))


def nospace(s):
    return re.sub(r'\s+', '', s)


# ----------------------------------------------------------------- loading

class Block:
    __slots__ = ('text', 'kind', 'level', 'xml')

    def __init__(self, text, kind, level=0, xml=''):
        self.text, self.kind, self.level, self.xml = text, kind, level, xml


def classify(text):
    t = text.strip()
    if CAPTION.match(t) or SRC_CAPTION.match(t):
        return 'caption'
    if NOTE.match(t):
        return 'note'
    if re.fullmatch(r'（[一二三四五六七八九十]+）[^。]{0,40}', t):
        return 'label'
    return 'prose'


def load_markdown(path):
    raw = open(path, encoding='utf-8-sig').read()
    raw = re.sub(r'```.*?```', '', raw, flags=re.S)
    blocks = []
    for chunk in re.split(r'\n\s*\n', raw):
        lines = [l for l in chunk.split('\n') if l.strip()]
        if not lines:
            continue
        if all(l.lstrip().startswith('|') for l in lines):
            blocks.append(Block('\t'.join(lines), 'table'))
            continue
        # a chunk may start with a heading line followed by text
        rest = []
        for l in lines:
            m = re.match(r'^(#{1,6})\s+(.*)', l)
            if m or l.lstrip().startswith('|'):
                if rest:
                    blocks.append(_text_block(_join(rest)))
                    rest = []
                blocks.append(Block(m.group(2).strip(), 'heading', len(m.group(1))) if m
                              else Block(l, 'table'))
            else:
                rest.append(l.strip().lstrip('>').strip())
        if rest:
            blocks.append(_text_block(_join(rest)))
    # merge consecutive table lines into one table block
    merged = []
    for b in blocks:
        if b.kind == 'table' and merged and merged[-1].kind == 'table':
            merged[-1].text += '\t' + b.text
        else:
            merged.append(b)
    return merged, ''


def _join(lines):
    # Chinese lines wrapped in the file are joined without a space; other scripts with one
    return ''.join(lines) if HAN.search(''.join(lines)) else ' '.join(lines)


def _text_block(t):
    return Block(t, classify(t))


def _docx_text(xml):
    x = re.sub(r'<w:tab/>', '\t', xml)
    x = re.sub(r'</w:(tc|p)>', '\t', x)
    x = re.sub(r'<[^>]+>', '', x)
    for a, b in (('&lt;', '<'), ('&gt;', '>'), ('&quot;', '"'), ('&apos;', "'"), ('&amp;', '&')):
        x = x.replace(a, b)
    return x.strip('\t').strip()


def load_docx(path):
    z = zipfile.ZipFile(path)
    xml = z.read('word/document.xml').decode('utf-8')
    heading_ids, toc_ids = {}, set()
    if 'word/styles.xml' in z.namelist():
        st = z.read('word/styles.xml').decode('utf-8')
        for m in re.finditer(r'<w:style\b[^>]*w:styleId="([^"]+)"[^>]*>(.*?)</w:style>', st, re.S):
            name = re.search(r'<w:name w:val="([^"]+)"', m.group(2))
            name = name.group(1) if name else ''
            h = re.match(r'(?i)(?:heading|标题)\s*(\d)', name)
            if h:
                heading_ids[m.group(1)] = int(h.group(1))
            elif re.match(r'(?i)toc\s*\d', name):
                toc_ids.add(m.group(1))
    body = re.search(r'<w:body>(.*)</w:body>', xml, re.S)
    body = body.group(1) if body else xml
    blocks = []
    for m in re.finditer(r'<w:tbl>.*?</w:tbl>|<w:p\b.*?</w:p>', body, re.S):
        bx = m.group(0)
        if bx.startswith('<w:tbl'):
            blocks.append(Block(_docx_text(bx), 'table', xml=bx))
            continue
        txt = _docx_text(bx)
        if not txt:
            continue
        sid = re.search(r'<w:pStyle w:val="([^"]+)"', bx)
        sid = sid.group(1) if sid else ''
        lvl = heading_ids.get(sid) or (int(sid[-1]) if re.fullmatch(r'(?i)heading\d', sid) else 0)
        if sid in toc_ids or re.search(r'(?i)^TOC\d', sid) or 'PAGEREF' in txt:
            blocks.append(Block(txt, 'toc', xml=bx))
        elif lvl:
            blocks.append(Block(txt, 'heading', lvl, xml=bx))
        else:
            b = _text_block(txt)
            b.xml = bx
            blocks.append(b)
    return blocks, xml


REFS_HEAD = re.compile(r'^(参考文献|References|Bibliograf[ií]a|Bibliography|Referencias)\s*$', re.I)


def mark_references(blocks):
    """Reference lists follow their own style (GB/T 7714 uses half-width punctuation) and are
    not translated prose: blocks after a references heading are set apart until the next
    heading of the same or a higher level."""
    level = None
    for b in blocks:
        if b.kind == 'heading':
            if REFS_HEAD.match(b.text.strip()):
                level = b.level or 1
                continue
            if level is not None and (b.level or 1) <= level:
                level = None
        elif level is not None:
            b.kind = 'ref'
        elif REFS_HEAD.match(b.text.strip()):    # unstyled references heading
            level = 1
    return blocks


def load(path):
    if not os.path.exists(path):
        sys.exit(f'file not found: {path}')
    blocks, xml = load_docx(path) if path.lower().endswith('.docx') else load_markdown(path)
    return mark_references(blocks), xml


def prose(blocks, chinese=True):
    out = [b.text for b in blocks if b.kind == 'prose']
    if chinese:
        out = [p for p in out if han_count(p) >= 12]
    return out


def sentences(paragraphs):
    out = []
    for p in paragraphs:
        out += [s for s in re.split(r'[。！？；]', p) if han_count(s) >= 2]
    return out


def pct(values, q):
    if not values:
        return 0
    v = sorted(values)
    k = (len(v) - 1) * q
    f, c = math.floor(k), math.ceil(k)
    return v[f] if f == c else v[f] + (v[c] - v[f]) * (k - f)


# ----------------------------------------------------------------- report

class Report:
    def __init__(self):
        self.items = []

    def add(self, level, code, msg):
        self.items.append((level, code, msg))

    def has_fail(self):
        return any(l == 'FAIL' for l, _, _ in self.items)


def snippet(text, m, width=18):
    a, b = max(0, m.start() - width), min(len(text), m.end() + width)
    return text[a:b].replace('\t', ' ').replace('\n', ' ')


# ----------------------------------------------------------------- A. fidelity

def _decimal_style(text):
    comma = len(re.findall(r'\d,\d{1,2}(?!\d)|\d,\d{4,}', text))
    point = len(re.findall(r'\d\.\d{1,2}(?!\d)|\d\.\d{4,}', text))
    return 'comma' if comma > point else 'point'


def _norm_number(tok, style):
    dec, thou = (',', '.') if style == 'comma' else ('.', ',')
    if tok.count(dec) > 1:               # 5.3.1-like section numbers in a point document
        return tok
    if thou in tok:
        groups = tok.split(dec)[0].split(thou)
        if all(len(g) == 3 for g in groups[1:]):
            tok = tok.replace(thou, '')
        else:
            return tok                   # not a thousands pattern (e.g. a section number)
    return tok.replace(dec, '.')


def fidelity(src_blocks, tgt_blocks, cfg, rep, decimal='auto'):
    src_text = '\n'.join(b.text for b in src_blocks)
    tgt_text = '\n'.join(b.text for b in tgt_blocks).replace('−', '-')
    style = _decimal_style(src_text) if decimal == 'auto' else decimal
    rep.add('INFO', 'A0', f'source decimal separator: {style}')

    nums = set()
    for tok in re.findall(r'\d+(?:[.,]\d+)*', src_text):
        n = _norm_number(tok, style)
        intpart = n.split('.')[0]
        if '.' in n or len(intpart) >= cfg['number_min_int_digits']:
            nums.add(n)
    tgt_nodot = tgt_text.replace('.', '')

    def present(n):
        if re.search(r'(?<![\d.])' + re.escape(n) + r'(?![\d])', tgt_text):
            return True
        if n.count('.') > 1 and n.replace('.', '') in tgt_nodot:
            return True
        try:
            v = float(n)
        except ValueError:
            return False
        # magnitudes rewritten with 亿 / 万: millions, billions, raw units
        cands = [(v / 100, '亿'), (v * 10, '亿'), (v / 1e8, '亿'), (v * 100, '万'), (v / 1e4, '万')]
        for x, unit in cands:
            if x <= 0:
                continue
            for form in {f'{x:.6f}'.rstrip('0').rstrip('.'), f'{x:g}'}:
                if re.search(re.escape(form) + r'\s*' + unit, tgt_text):
                    return True
        return False

    missing = sorted(n for n in nums if not present(n))
    rep.add('INFO', 'A1', f'figures checked: {len(nums)}')
    if missing:
        rep.add('FAIL', 'A1', f'{len(missing)} figures of the source are not in the translation: '
                + ', '.join(missing[:15]))

    cites = set(re.findall(r'([A-ZÀ-Ý][A-Za-zÀ-ÿ\'’-]+)(?:\s+et\s+al\.?)?\s*\((\d{4})[a-z]?\)', src_text))
    cites |= set(re.findall(r'\(([A-ZÀ-Ý][A-Za-zÀ-ÿ\'’-]+)[^()]{0,40}?,\s*(\d{4})[a-z]?', src_text))
    lost = sorted(f'{a} ({y})' for a, y in cites if a not in tgt_text)
    rep.add('INFO', 'A2', f'author citations checked: {len(cites)}')
    if lost:
        rep.add('WARN', 'A2', f'{len(lost)} cited authors without trace in the translation: '
                + ', '.join(lost[:10]))

    sp = [b.text for b in src_blocks if b.kind == 'prose' and len(nospace(b.text)) >= 20]
    tp = [b.text for b in tgt_blocks if b.kind == 'prose' and len(nospace(b.text)) >= 12]
    tol = max(cfg['paragraph_tolerance_abs'], round(cfg['paragraph_tolerance_rel'] * len(sp)))
    rep.add('INFO', 'A3', f'prose paragraphs: source {len(sp)}, translation {len(tp)} '
            f'(tolerance ±{tol})')
    if abs(len(sp) - len(tp)) > tol:
        rep.add('FAIL', 'A3', f'paragraph count differs by {len(tp) - len(sp):+d}: paragraphs were '
                'merged, split, added or lost')
    elif len(sp) == len(tp) and len(sp) >= 3:
        ratios = [len(nospace(t)) / max(1, len(nospace(s))) for s, t in zip(sp, tp)]
        med = statistics.median(ratios)
        rep.add('INFO', 'A4', f'median length ratio translation/source: {med:.3f}')
        odd = [(i + 1, r) for i, r in enumerate(ratios)
               if r < med * cfg['ratio_low'] or r > med * cfg['ratio_high']]
        if odd:
            rep.add('WARN', 'A4', 'paragraphs whose length ratio departs from the median '
                    '(possible omission or addition): '
                    + ', '.join(f'§{i} ({r / med:.2f}× median)' for i, r in odd[:10]))

    s_cap = len({re.match(r'\D*(\d+(?:[-.]\d+)?)', SRC_CAPTION.match(b.text.strip()).group(0)).group(1)
                 for b in src_blocks if b.kind == 'caption' and SRC_CAPTION.match(b.text.strip())})
    t_cap = len({b.text.split()[0] for b in tgt_blocks if b.kind == 'caption'})
    if s_cap:
        rep.add('INFO', 'A5', f'captions: source {s_cap}, translation {t_cap}')
        if t_cap < s_cap:
            rep.add('WARN', 'A5', f'fewer table/figure captions in the translation ({t_cap}) than '
                    f'in the source ({s_cap})')


# ----------------------------------------------------------------- B. register

def register(blocks, cfg, rep):
    paras = prose(blocks)
    text = '\n'.join(paras)
    flat = nospace(text)
    n = han_count(flat) or 1
    rate = lambda c: c * 10000 / n
    judged = n >= cfg['min_chars_for_rates']
    rep.add('INFO', 'B0', f'Chinese characters of running prose: {n}'
            + ('' if judged else f' (below {cfg["min_chars_for_rates"]}: rates reported, not judged)'))

    for m in re.finditer(ANNOUNCEMENTS, flat):
        rep.add('FAIL', 'B1', f'section announcement: «{snippet(flat, m)}»; enter the subject directly')

    calques = list(CALQUES) + [(k, v[0], v[1]) for k, v in cfg['calques'].items()]
    for pat, level, sug in calques:
        hits = list(re.finditer(pat, flat))
        if hits:
            ex = ' | '.join(snippet(flat, h, 10) for h in hits[:3])
            rep.add(level.upper(), 'B2', f'calque «{hits[0].group(0)}» ×{len(hits)} → {sug}: {ex}')

    ta = len(re.findall(r'它们?', flat))
    rep.add('INFO', 'B3', f'它/它们: {ta} ({rate(ta):.1f} per 10,000; corpus 1.7)')
    if judged and rate(ta) > cfg['ta_rate_max']:
        rep.add('WARN', 'B3', f'它 as subject is frequent ({rate(ta):.1f} per 10,000): use the noun, '
                '其 or 该 + noun, checking each referent')

    meta = len(re.findall(METATEXT, flat))
    ceiling = max(1, n // cfg['metatext_per_chars'])
    rep.add('INFO', 'B4', f'值得注意的是 and similar: {meta} (ceiling {ceiling})')
    if meta > 2 * ceiling:
        rep.add('WARN', 'B4', f'{meta} phrases of the 值得注意的是 type; about {ceiling} would be usual')

    if '百分之' in flat:
        rep.add('FAIL', 'B5', f'百分之 ×{flat.count("百分之")}: write digits + %')

    forms = Counter()
    for p in paras:
        if NOTE.match(p):
            continue
        for m in re.finditer(r'在\s?\d+(?:\.\d+)?%\s?(的水平上|水平上|的水平下|统计水平上|的显著性水平上)显著', p):
            forms[m.group(1)] += 1
    style = cfg['significance_style']
    if style == 'medicine':
        for m in re.finditer(r'显著性差异|具有显著性|差异显著|显著性意义', flat):
            rep.add('WARN', 'B6', f'«{m.group(0)}»: medical journals write 差异有统计学意义 (P<0.05): '
                    f'«{snippet(flat, m, 12)}»')
    elif style == 'economics' and len(forms) > 1:
        rep.add('WARN', 'B6', 'significance phrase written in several forms: '
                + ', '.join(f'在N%{k}显著 ×{v}' for k, v in forms.most_common())
                + '; choose one (the corpus prefers 在N%水平上显著)')

    causal = list(re.finditer(CAUSAL, flat))
    if causal:
        rep.add('REVIEW', 'B7', f'{len(causal)} passages with causal wording; check that none states '
                'the study\'s own associative result causally: '
                + ' | '.join(snippet(flat, m, 12) for m in causal[:8]))

    sents = sentences(paras)
    lens = [len(nospace(s)) for s in sents]
    long_ = [l for l in lens if l > cfg['long_sentence_chars']]
    very = [s for s in sents if len(nospace(s)) > cfg['max_sentence_chars']]
    if lens:
        rep.add('INFO', 'B8', f'sentences: {len(lens)}, mean {statistics.mean(lens):.0f}, median '
                f'{statistics.median(lens):.0f}, p90 {pct(lens, .9):.0f} characters '
                f'(corpus 47 / 41 / 87); over {cfg["long_sentence_chars"]}: {len(long_)}')
        if len(long_) / len(lens) > cfg['long_sentence_share_max'] and len(lens) >= 10:
            rep.add('WARN', 'B8', f'{len(long_) / len(lens):.0%} of sentences exceed '
                    f'{cfg["long_sentence_chars"]} characters; split the long ones')
        for s in very[:5]:
            rep.add('WARN', 'B8', f'sentence of {len(nospace(s))} characters: «{nospace(s)[:40]}…»')

    plens = [len(nospace(p)) for p in paras]
    if plens:
        lp = [l for l in plens if l > cfg['long_paragraph_chars']]
        rep.add('INFO', 'B9', f'paragraphs: {len(plens)}, mean {statistics.mean(plens):.0f} characters '
                f'(corpus 146); over {cfg["long_paragraph_chars"]}: {len(lp)}')
        if len(plens) >= 10 and len(lp) / len(plens) > cfg['long_paragraph_share_max']:
            rep.add('WARN', 'B9', f'{len(lp) / len(plens):.0%} of paragraphs exceed '
                    f'{cfg["long_paragraph_chars"]} characters')
        mono = [p for p in paras if len(nospace(p)) > cfg['monolith_paragraph_chars']]
        if mono:
            rep.add('WARN', 'B9', f'{len(mono)} paragraphs over {cfg["monolith_paragraph_chars"]} '
                    'characters; check that source paragraphs were not merged')

    limit = max(cfg['repeat_formula_min'], 2 * math.ceil(n / 20000))
    for f, c in Counter(re.findall(REPEATED, flat)).items():
        if c >= limit:
            rep.add('WARN', 'B10', f'«{f}» ×{c}: a refrain; vary the connector')

    enum = len(re.findall(ENUMERATORS, flat))
    rep.add('INFO', 'B11', f'enumerators: {enum} ({rate(enum):.1f} per 10,000; corpus 16.0)')
    if n >= cfg['min_chars_for_enumerators'] and rate(enum) < cfg['enumerator_rate_min']:
        rep.add('WARN', 'B11', f'few enumerators ({rate(enum):.1f} per 10,000); the genre enumerates')

    uses = {c: flat.count(c) for c in CONNECTIVES}
    total, distinct = sum(uses.values()), sum(1 for v in uses.values() if v)
    rep.add('INFO', 'B12', f'connectives: {total} = {rate(total):.1f} per 10,000, {distinct} distinct '
            f'forms (reference theses: 92.4 / 53 and 96.0 / 48)')
    if judged and rate(total) < cfg['connective_density_min']:
        rep.add('WARN', 'B12', f'connective density {rate(total):.1f} below {cfg["connective_density_min"]}: '
                'check that corrections did not remove argumentative links')
    if n >= cfg['min_chars_for_forms'] and distinct < cfg['connective_forms_min']:
        rep.add('WARN', 'B12', f'only {distinct} distinct connective forms: a replacement may have '
                'become a tic')

    pairs = 0
    for p in paras:
        ss = [s.strip() for s in re.split(r'[。！？]', p) if s.strip()]
        pairs += sum(1 for a, b in zip(ss, ss[1:]) if a.startswith('本文') and b.startswith('本文'))
    if pairs > cfg['consecutive_benwen_max']:
        rep.add('WARN', 'B13', f'{pairs} pairs of consecutive sentences opened by 本文; vary the subject')

    bold = sum(1 for b in blocks if b.kind == 'prose' and
               not re.match(r'^(关键词|Keywords?|Key words)\s*[：:]', b.text.strip(), re.I) and
               (re.search(r'\*\*[^*]+\*\*', b.text) or re.search(r'<w:b/>|<w:b w:val="(1|true)"/>', b.xml)))
    if bold:
        rep.add('WARN', 'B14', f'{bold} body paragraphs with bold; Chinese academic prose carries '
                'emphasis without bold')


# ----------------------------------------------------------------- C. typography

def typography(blocks, cfg, rep, is_docx):
    text = '\n'.join(b.text for b in blocks if b.kind not in ('toc',))
    body = '\n'.join(b.text for b in blocks if b.kind in ('prose', 'caption', 'note', 'heading', 'label'))

    for name, rng in (('Cyrillic', r'[Ѐ-ӿ]'), ('Arabic', r'[؀-ۿ]'),
                      ('Hangul', r'[가-힯]'), ('Kana', r'[぀-ヿ]')):
        found = re.findall(rng + '+', text)
        if found:
            rep.add('FAIL', 'C1', f'{name} script inside the Chinese text: ' + ', '.join(sorted(set(found))[:6]))

    white = {w.lower() for w in cfg['latin_whitelist']}
    white |= {w.lower() for w in re.findall(r'（([A-Za-z][A-Za-z0-9_]*)）', text)}
    glued = set()
    for m in re.finditer(r'[一-鿿]([A-Za-z]*[a-z][A-Za-z]{2,})|([A-Za-z]*[a-z][A-Za-z]{2,})[一-鿿]', body):
        w = (m.group(1) or m.group(2))
        if w.lower() not in white:
            glued.add(snippet(body, m, 3))
    if glued:
        rep.add('WARN', 'C2', f'{len(glued)} Latin words glued to Chinese characters (a foreign word in '
                'a Chinese sentence, or a missing space): ' + ' | '.join(sorted(glued)[:8]))

    straight = len(re.findall(r'(?<![A-Za-z])[\'"](?![A-Za-z])|(?<=[一-鿿])[\'"]|[\'"](?=[一-鿿])', body))
    if straight:
        rep.add('WARN', 'C3', f'{straight} straight quotation marks; use “ ” (or 「 」)')

    ascii_p = re.findall(r'[一-鿿][,;:?!()]|[,;:?!()][一-鿿]|[一-鿿]\.(?=\s|$)', body)
    if ascii_p:
        rep.add('WARN', 'C4', f'{len(ascii_p)} half-width punctuation marks next to Chinese characters: '
                + ' '.join(sorted(set(ascii_p))[:10]))

    thou = re.findall(r'(?<![\d.])\d{1,3}(?:,\d{3})+(?![\d])', body)
    if thou:
        rep.add('WARN', 'C5', f'thousands separators in figures: {", ".join(thou[:6])}; write 3120, '
                'or use 万/亿')
    dcomma = re.findall(r'(?<![\d,])\d+,\d{1,2}(?![\d,])', body)
    if dcomma:
        rep.add('WARN', 'C5', f'possible decimal commas: {", ".join(dcomma[:6])}; Chinese uses the point')

    hy = len(re.findall(r'\b(?:19|20)\d{2}-(?:19|20)\d{2}\b', body))
    dash = len(re.findall(r'(?:19|20)\d{2}\s*(?:—|–|至|到)\s*(?:19|20)\d{2}', body))
    if hy and dash:
        rep.add('WARN', 'C6', f'year ranges in two forms: hyphen ×{hy}, dash/至 ×{dash}; unify')

    pend = sum(1 for b in blocks if '【待翻译】' in b.text)
    if pend:
        rep.add('WARN', 'C7', f'{pend} blocks marked 【待翻译】: counts are not interpretable yet')

    if is_docx:
        if '`' in text:
            rep.add('FAIL', 'C8', f'{text.count("`")} visible backticks (Markdown markup printed)')
        if re.search(r'\\frac|\\sum|\\beta|\\alpha|\$\$', text):
            rep.add('FAIL', 'C8', 'LaTeX remnants: insert equations as native Word equations')


# ----------------------------------------------------------------- D. glossary

def read_glossary(path):
    alias = {'origen': 'term', 'chino': 'chinese', 'fuente': 'reference', 'evidencia': 'evidence',
             'nota': 'note', 'source': 'term', 'zh': 'chinese', '中文': 'chinese'}
    rows = []
    with open(path, encoding='utf-8-sig', newline='') as f:
        for r in csv.DictReader(f):
            row = {}
            for k, v in r.items():
                if k is None:
                    continue
                k2 = alias.get(k.strip().lower(), k.strip().lower())
                row[k2] = (v or '').strip()
            if row.get('chinese'):
                rows.append(row)
    return rows


def glossary(path, src_blocks, tgt_blocks, rep):
    rows = read_glossary(path)
    tgt = '\n'.join(b.text for b in tgt_blocks)
    src = '\n'.join(b.text for b in src_blocks).lower() if src_blocks else ''
    used, diverge, pending, undocumented = 0, [], [], []
    for r in rows:
        variants = [v.strip() for v in re.split(r'\s*/\s*|／', re.sub(r'[（(][^）)]*[）)]', '', r['chinese'])) if v.strip()]
        terms = [t.strip() for k, v in r.items() if k.startswith('term') and v
                 for t in re.sub(r'\([^)]*\)', '', v).split(';') if t.strip()]
        if '待人工核对' in r.get('note', '') or '待人工核对' in r['chinese']:
            pending.append(f'{terms[0] if terms else "?"} → {r["chinese"]}')
        if not r.get('reference') or not r.get('evidence'):
            undocumented.append(r['chinese'])
        if any(v in tgt for v in variants):
            used += 1
        elif src and any(re.search(r'(?<![a-záéíóúñ])' + re.escape(t.lower()) + r'(?![a-záéíóúñ])', src)
                         for t in terms):
            diverge.append(f'«{terms[0]}» → {r["chinese"]}')
        if sum(1 for v in variants if v in tgt) > 1:
            rep.add('WARN', 'D4', f'two forms of the same glossary term in the translation: {r["chinese"]}')
    rep.add('INFO', 'D0', f'glossary: {len(rows)} entries, {used} used in the translation')
    if diverge:
        rep.add('WARN', 'D1', f'{len(diverge)} glossary terms present in the source but not in the '
                'translation (translated another way?): ' + ' | '.join(diverge[:10]))
    if pending:
        rep.add('WARN', 'D2', f'{len(pending)} terms pending human check [待人工核对]: ' + ' | '.join(pending[:10]))
    if undocumented:
        rep.add('WARN', 'D3', f'{len(undocumented)} entries without reference or evidence: '
                + ', '.join(undocumented[:10]))


# ----------------------------------------------------------------- E. format by profile

def fmt(blocks, xml, cfg, rep, profile, is_docx):
    caps = [b.text.strip() for b in blocks if b.kind == 'caption' and CAPTION.match(b.text.strip())]
    labels = [re.match(r'^([表图])\s?(\d+(?:[-.－]\d+)?)', c) for c in caps]
    seq = {}
    for m in labels:
        kind, num = m.group(1), re.sub(r'[.－]', '-', m.group(2))
        chap, k = (num.split('-') + [''])[:2] if '-' in num else ('', num)
        seq.setdefault((kind, chap), []).append(int(k))
    for (kind, chap), ks in seq.items():
        if ks != list(range(1, len(ks) + 1)):
            rep.add('WARN' if profile == 'article' else 'FAIL', 'E1',
                    f'{kind}{chap + "-" if chap else ""}N numbering not consecutive: {ks}')
    for c in caps:
        title = re.sub(r'^([表图])\s?\S+\s*', '', c)
        if len(title) > cfg['caption_title_max_chars']:
            rep.add('WARN', 'E2', f'long caption title ({len(title)}): «{c[:30]}…»')
        if '。' in c:
            rep.add('WARN', 'E2', f'caption title with 。 (a long note in the title?): «{c[:30]}»')
        if re.search(r'被解释变量\s*[：:]', c):
            rep.add('WARN', 'E2', f'«被解释变量：» in the title; put it in the header row: «{c[:30]}»')
    names = {re.sub(r'\s', '', c.split()[0]) for c in caps}
    all_text = '\n'.join(b.text for b in blocks if b.kind in ('prose', 'note', 'label'))
    ref_pat = r'(?<![代发外])[表图]\d+-\d+' if profile == 'thesis' else r'(?<![代发外])[表图]\s?\d+(?:-\d+)?'
    for ref in sorted(set(re.findall(ref_pat, all_text))):
        if caps and re.sub(r'\s', '', ref) not in names:
            rep.add('WARN', 'E3', f'reference to {ref}, which has no caption')

    if profile in ('thesis', 'report'):
        idx = [i for i, b in enumerate(blocks) if b.kind == 'caption' and CAPTION.match(b.text.strip())]
        for j, i in enumerate(idx):
            end = idx[j + 1] if j + 1 < len(idx) else len(blocks)
            seg = blocks[i + 1:end]
            stop = next((k for k, b in enumerate(seg) if b.kind == 'heading'), len(seg))
            if not any(b.kind == 'note' and re.search(r'(资料来源|数据来源)[：:]', b.text)
                       for b in seg[:stop]):
                rep.add('WARN', 'E4', f'no 资料来源： line after «{blocks[i].text.strip()[:24]}»')

    if profile == 'thesis':
        heads = [b.text.strip() for b in blocks if b.kind == 'heading']
        styles = Counter('第N章' if re.match(r'^第[一二三四五六七八九十\d]+章', h) else
                         'N.title' if re.match(r'^\d+\.(?!\d)\s?\S', h) else None for h in heads)
        styles.pop(None, None)
        if len(styles) > 1:
            rep.add('WARN', 'E5', f'chapter headings in two numbering styles: {dict(styles)}; follow the norm')
        for i, b in enumerate(blocks):
            if b.kind == 'caption' and b.text.startswith('表'):
                tbl = next((x for x in blocks[i + 1:i + 3] if x.kind == 'table'), None)
                if tbl and '观测值' in tbl.text and '常数项' not in tbl.text and re.search(r'固定效应|控制变量', tbl.text):
                    rep.add('WARN', 'E6', f'regression table without 常数项 row: «{b.text[:24]}» '
                            '(fine only if the estimator returns none)')
                if tbl and re.search(r'控制变量\s*[|\t]\s*(是|控制|Yes)', tbl.text):
                    rep.add('WARN', 'E6', f'controls summarised as 是 in «{b.text[:24]}»; list them one by one')

    if is_docx:
        unstyled = [b.text[:40] for b in blocks if b.kind in ('prose', 'label') and
                    re.match(r'^(第[一二三四五六七八九十\d]+章|\d+(\.\d+){1,2}\s?\S|\d+\.\s?[一-鿿])', b.text)
                    and len(b.text) <= 60 and '。' not in b.text]
        if unstyled and profile == 'thesis':
            rep.add('FAIL', 'E7', f'{len(unstyled)} numbered headings without a heading style (they will '
                    'not enter the 目录): ' + ' | '.join(unstyled[:6]))
        toc = [b for b in blocks if b.kind == 'toc']
        has_field = 'TOC \\' in xml
        if profile == 'thesis':
            if has_field and not toc:
                rep.add('WARN', 'E8', 'the 目录 field is inserted but empty: update it in Word (F9)')
            elif not has_field and not toc:
                rep.add('WARN', 'E8', 'no 目录 in the document')
        tables = [b for b in blocks if b.kind == 'table']
        nob = sum(1 for t in tables if '<w:tblBorders' not in t.xml and not re.search(r'<w:tblStyle w:val=', t.xml))
        if nob:
            rep.add('FAIL', 'E9', f'{nob} tables without borders or table style')
        shaded = sum(1 for t in tables if re.search(r'w:fill="(?!auto)[0-9A-Fa-f]{6}"',
                                                     (re.findall(r'<w:tr\b.*?</w:tr>', t.xml, re.S) or [''])[0]))
        if tables and shaded == len(tables):
            rep.add('WARN', 'E9', 'every table has a shaded header; three-line tables are not shaded')
        fonts = Counter(re.findall(r'w:(?:ascii|eastAsia)="([^"]+)"', xml))
        odd = {f: c for f, c in fonts.items() if f not in cfg['allowed_fonts']}
        if odd:
            rep.add('WARN', 'E10', 'fonts outside the allowed list: ' + ', '.join(f'{f} ({c})' for f, c in odd.items()))
        bad = 0
        for b in blocks:
            if b.kind == 'prose' and re.match(r'^[图表]\d+-\d+[^\s\d]', b.text):
                if 'w:firstLine' not in b.xml or '<w:jc w:val="center"/>' in b.xml:
                    bad += 1
        if bad:
            rep.add('WARN', 'E11', f'{bad} body paragraphs starting with 图/表N-M are centred or not '
                    'indented (treated as captions?)')


# ----------------------------------------------------------------- calibration

def calibrate(files, out):
    per, all_p = [], []
    for f in files:
        blocks, _ = load(f)
        paras = [re.sub(r'(?<=[一-鿿])\s+(?=[一-鿿])', '', p) for p in prose(blocks)]
        flat = nospace('\n'.join(paras))
        n = han_count(flat) or 1
        uses = {c: flat.count(c) for c in CONNECTIVES}
        per.append({'file': os.path.basename(f), 'chinese_chars': n,
                    'connective_density': sum(uses.values()) * 10000 / n,
                    'connective_forms': sum(1 for v in uses.values() if v),
                    'enumerator_rate': len(re.findall(ENUMERATORS, flat)) * 10000 / n,
                    'ta_rate': len(re.findall(r'它们?', flat)) * 10000 / n})
        all_p += paras
    sl = [len(nospace(s)) for s in sentences(all_p)]
    pl = [len(nospace(p)) for p in all_p]
    flat = nospace('\n'.join(all_p))
    n = han_count(flat) or 1
    big = [p for p in per if p['chinese_chars'] >= 20000]
    pooled_density = sum(flat.count(c) for c in CONNECTIVES) * 10000 / n
    cfg = {
        'long_sentence_chars': round(pct(sl, .9)),
        'max_sentence_chars': round(pct(sl, .99)),
        'long_paragraph_chars': round(pct(pl, .9)),
        'connective_density_min': round(min(p['connective_density'] for p in big), 1) if big
        else round(pooled_density * 0.85, 1),
        'connective_forms_min': min(p['connective_forms'] for p in big) if big else DEFAULTS['connective_forms_min'],
        'enumerator_rate_min': round(0.4 * len(re.findall(ENUMERATORS, flat)) * 10000 / n, 1),
        'ta_rate_max': round(max(3.0, 3 * len(re.findall(r'它们?', flat)) * 10000 / n), 1),
        '_calibration': {
            'files': per, 'pooled_chinese_chars': n,
            'sentence_mean': round(statistics.mean(sl), 1) if sl else None,
            'sentence_median': statistics.median(sl) if sl else None,
            'paragraph_mean': round(statistics.mean(pl), 1) if pl else None,
            'pooled_connective_density': round(pooled_density, 1),
            'note': 'thresholds derived as documented in scripts/README.md',
        },
    }
    if n < 20000:
        cfg['_calibration']['warning'] = (
            f'only {n} Chinese characters of running prose: thresholds are unreliable. Add full '
            'texts (introductions, discussions), not only abstracts, which carry few connectives.')
    with open(out, 'w', encoding='utf-8') as fh:
        json.dump(cfg, fh, ensure_ascii=False, indent=2)
    print(json.dumps(cfg, ensure_ascii=False, indent=2))
    if n < 20000:
        print('\nWARNING: ' + cfg['_calibration']['warning'])


# ----------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('translation', nargs='?')
    ap.add_argument('--source')
    ap.add_argument('--glossary')
    ap.add_argument('--profile', choices=['thesis', 'article', 'report'], default='article')
    ap.add_argument('--config')
    ap.add_argument('--source-decimal', choices=['auto', 'comma', 'point'], default='auto')
    ap.add_argument('--json', action='store_true', help='print the report as JSON')
    ap.add_argument('--calibrate', nargs='+', metavar='CORPUS_FILE')
    ap.add_argument('-o', '--output', default='config.json')
    a = ap.parse_args()

    if a.calibrate:
        calibrate(a.calibrate, a.output)
        return
    if not a.translation:
        ap.error('give the translation file, or --calibrate')

    cfg = dict(DEFAULTS)
    if a.config:
        user = json.load(open(a.config, encoding='utf-8'))
        cfg.update({k: v for k, v in user.items() if not k.startswith('_')})

    tgt, xml = load(a.translation)
    src = load(a.source)[0] if a.source else []
    is_docx = a.translation.lower().endswith('.docx')
    rep = Report()
    if src:
        fidelity(src, tgt, cfg, rep, a.source_decimal)
    register(tgt, cfg, rep)
    typography(tgt, cfg, rep, is_docx)
    if a.glossary:
        glossary(a.glossary, src, tgt, rep)
    fmt(tgt, xml, cfg, rep, a.profile, is_docx)

    if a.json:
        print(json.dumps([{'level': l, 'code': c, 'message': m} for l, c, m in rep.items],
                         ensure_ascii=False, indent=2))
    else:
        print(f'=== {os.path.basename(a.translation)}'
              + (f' against {os.path.basename(a.source)}' if a.source else '')
              + f' | profile: {a.profile} ===\n')
        for level in ('INFO', 'REVIEW', 'WARN', 'FAIL'):
            for l, c, m in rep.items:
                if l == level:
                    print(f'  {l:<6} {c:<4} {m}')
        nf = sum(1 for l, _, _ in rep.items if l == 'FAIL')
        nw = sum(1 for l, _, _ in rep.items if l == 'WARN')
        print('\n' + ('NO FAILS' if not nf else f'{nf} FAILS') + f', {nw} warnings')
    sys.exit(1 if rep.has_fail() else 0)


if __name__ == '__main__':
    main()
