# verify_zh.py

A mechanical verifier for academic translations into Chinese. It needs Python 3.8 or newer and
uses only the standard library.

```
python verify_zh.py TRANSLATION [--source SOURCE] [--glossary GLOSSARY.csv]
                    [--profile thesis|article|report] [--config CONFIG.json]
                    [--source-decimal auto|comma|point] [--json]
python verify_zh.py --calibrate CORPUS_FILE [CORPUS_FILE ...] -o CONFIG.json
```

- **Inputs:**
  - `TRANSLATION` and `SOURCE` may be `.md`, `.txt` or `.docx`. In Markdown, paragraphs are
    blocks separated by a blank line, headings start with `#`, and tables are lines starting with
    `|`.
  - Blocks after a references heading (参考文献, References, Bibliografía…) are excluded from the
    prose checks.
- **Output levels:**
  - `FAIL` must be fixed (exit code 1);
  - `WARN` is fixed or justified in the report;
  - `REVIEW` lists passages a human should read;
  - `INFO` gives measurements.
- **Short texts:** rates are reported but not judged below `min_chars_for_rates`, because rates
  on a few hundred characters are noise.

## Checks

| Code | Check | Level | Needs |
|---|---|---|---|
| A1 | Every figure of the source is in the translation. Decimal comma or point detected or set; thousands separators removed; accepts 亿/万 rewrites | FAIL | `--source` |
| A2 | Every cited author surname, from «Author (year)» or «(Author, year)», appears | WARN | `--source` |
| A3 | Prose paragraph count, source vs translation | FAIL beyond tolerance | `--source` |
| A4 | Per-paragraph length ratio against the median ratio, when counts match | WARN | `--source` |
| A5 | Number of table and figure captions | WARN | `--source` |
| B1 | Section announcements (本节将, 本章主要, 下面将, 接下来将, 下文将) | FAIL | |
| B2 | Calques of source syntax (list in `CALQUES`; extend with `calques` in the config) | FAIL or WARN per item | |
| B3 | Rate of 它/它们 | WARN | |
| B4 | 值得注意的是 and similar phrases above ceiling | WARN | |
| B5 | 百分之 | FAIL | |
| B6 | Significance phrase written in several forms | WARN | |
| B7 | Causal wording (因果效应, 导致, 促进了, 使……提高…) | REVIEW | |
| B8 | Sentence length: share above `long_sentence_chars`, each one above `max_sentence_chars` | WARN | |
| B9 | Paragraph length: share above `long_paragraph_chars`, monoliths | WARN | |
| B10 | The same closing or transition formula used as a refrain | WARN | |
| B11 | Enumerator rate | WARN | |
| B12 | Connective density and number of distinct forms (list `CONNECTIVES`) | WARN | |
| B13 | Consecutive sentences both opened by 本文 | WARN | |
| B14 | Bold in body paragraphs (the 关键词 line is exempt) | WARN | |
| C1 | Foreign scripts: Cyrillic, Arabic, Hangul, Kana (Greek is allowed for notation) | FAIL | |
| C2 | Lower-case Latin word glued to a Chinese character. Allowed: `latin_whitelist`, symbols defined as （symbol）, all-caps acronyms | WARN | |
| C3 | Straight quotation marks | WARN | |
| C4 | Half-width punctuation next to Chinese characters | WARN | |
| C5 | Thousands separators, decimal commas | WARN | |
| C6 | Year ranges in two forms | WARN | |
| C7 | 【待翻译】 markers | WARN | |
| C8 | Visible backticks, LaTeX remnants (`.docx` only) | FAIL | |
| D0–D4 | Glossary: terms present in the source but not in the translation; pending `[待人工核对]`; entries without reference or evidence; two forms of one term | WARN | `--glossary` |
| E1 | 表/图 numbering consecutive per chapter (or global) | FAIL for thesis, WARN otherwise | |
| E2 | Caption title length, 。 in title, «被解释变量：» in title | WARN | |
| E3 | References to tables or figures that have no caption | WARN | |
| E4 | 资料来源： line after each table or figure | WARN | thesis, report |
| E5 | Chapter headings in two numbering styles (第N章 and N.) | WARN | thesis |
| E6 | Regression table without 常数项, or controls summarised as 是 | WARN | thesis |
| E7 | Numbered headings without a heading style | FAIL | thesis, `.docx` |
| E8 | 目录 missing or not updated | WARN | thesis, `.docx` |
| E9 | Tables without borders or style; every header shaded | FAIL / WARN | `.docx` |
| E10 | Fonts outside `allowed_fonts` | WARN | `.docx` |
| E11 | Body paragraph starting with 图/表N-M centred or not indented | WARN | `.docx` |

## Thresholds and where they come from

Defaults are in `DEFAULTS` at the top of the script. Override any of them with a JSON file passed
with `--config`.

| Key | Default | Origin |
|---|---|---|
| `long_sentence_chars` | 90 | Corpus p90 = 87 characters (sentences split at 。！？；) |
| `max_sentence_chars` | 140 | Corpus p99 = 140 |
| `long_sentence_share_max` | 0.10 | About 10% of corpus sentences exceed p90 by definition |
| `long_paragraph_chars` | 340 | Corpus p90 = 337 |
| `long_paragraph_share_max` | 0.10 | Same logic |
| `monolith_paragraph_chars` | 1000 | No paragraph of this size in the corpus |
| `min_chars_for_rates` | 3000 | Below this, rates are not judged |
| `connective_density_min` | 92.0 | Two reference master's theses: 92.4 and 96.0 per 10,000 with `CONNECTIVES` |
| `connective_forms_min` | 48 | The same theses: 53 and 48 distinct forms |
| `min_chars_for_forms` | 20000 | Variety grows with length |
| `enumerator_rate_min` | 6.0 | Corpus 16.0 per 10,000 (theses 12.0 and 19.1); WARN only far below |
| `min_chars_for_enumerators` | 10000 | |
| `ta_rate_max` | 5.0 | Corpus 1.7 per 10,000 for 它/它们; translations full of calques run far higher |
| `metatext_per_chars` | 20000 | Reference theses: about one 值得注意的是-type phrase per 20,000 characters; WARN above twice the ceiling |
| `repeat_formula_min` | 6 | A formula used six times or more (or twice per 20,000 characters on long texts) |
| `consecutive_benwen_max` | 2 | |
| `paragraph_tolerance_abs` / `_rel` | 2 / 0.015 | A whole thesis (about 400 paragraphs) was accepted with a gap of ±6 |
| `ratio_low` / `ratio_high` | 0.70 / 1.50 | A paragraph at 0.74 × the median ratio had lost three sentences |
| `number_min_int_digits` | 3 | Smaller integers are often written as Chinese numerals for structural counts |
| `caption_title_max_chars` | 45 | Supervisor's format comments |
| `allowed_fonts` | SimSun, SimHei, Times New Roman, Cambria Math, 宋体, 黑体, 方正小标宋简体, 楷体/KaiTi, 仿宋/FangSong | Common Chinese thesis norms |
| `latin_whitelist` | [] | Add the project's variable names |
| `calques` | {} | `{"regex": ["warn", "suggestion"]}` to add project calques |
| `significance_style` | `economics` | `economics`: checks that 在N%水平上显著 is written in one form. `medicine`: flags 显著性差异 / 差异显著, which medical journals' author guidelines ask to write as 差异有统计学意义. `none`: no check |

**The corpus.** Two Chinese master's theses in economics and six journal articles of
the same subfield, about 149,000 characters of running prose.

**How the defaults were measured.** The length and rate figures come from the original
measurement of that corpus. The connective thresholds were measured with the same `CONNECTIVES`
list as this script.

**Measured with this script.** `--calibrate` on the two theses reproduces the distinct-form counts
exactly (53 and 48). It gives somewhat higher densities (96.2 and 106.1) because it leaves
captions and notes out of the denominator. The defaults are therefore slightly lenient, which is
the safe side for a WARN.

## Calibrating on your own field

```
python verify_zh.py --calibrate corpus/*.txt -o config.json
python verify_zh.py translation.md --config config.json ...
```

The corpus files should be **clean running prose**:
- no table of contents, tables, captions, references or English abstract;
- spaces inserted inside Chinese words by PDF conversion are removed automatically.

Derived thresholds:

| Key | How it is derived |
|---|---|
| `long_sentence_chars` | p90 of sentence length |
| `max_sentence_chars` | p99 of sentence length |
| `long_paragraph_chars` | p90 of paragraph length |
| `connective_density_min` | The lowest per-file density among files of at least 20,000 characters, or 0.85 × the pooled density if none is that long |
| `connective_forms_min` | The lowest distinct-form count among those files |
| `enumerator_rate_min` | 0.4 × the pooled enumerator rate |
| `ta_rate_max` | 3 × the pooled 它 rate, at least 3 |

The per-file figures are written under `_calibration` for the record.

If the corpus has fewer than 20,000 Chinese characters of running prose, the script warns that
the thresholds are unreliable. Abstracts alone are too short and carry few connectives.

**Copyright of the corpus.** The corpus is only measured: the output contains numbers, not text.
Do not redistribute third-party theses or articles.

# harvest_terms.py

Extracts attested Chinese terminology from open articles of the field that were downloaded
beforehand. It is the tool of `references/10_field_discovery.md`. It uses only the standard
library, downloads nothing and executes nothing it reads. Run it with `python -I`, from outside
the download folder.

```
python -I harvest_terms.py FILES... [--sources sources.csv] [--check candidates.txt]
                           [-o harvest.csv] [--corpus-out DIR]
```

| Option | What it does |
|---|---|
| `FILES` | `.html`, `.htm`, `.txt` or `.md`. Convert PDFs first (`pdftotext -enc UTF-8`). UTF-8, GB18030 and Big5 are detected |
| `--sources` | CSV `file,url,title,publisher,date`. The URL replaces the file name in the `reference` column |
| `--check` | One concept per line, variants separated by ` / `. Prints, for each variant, the documents that contain it and the total uses |
| `-o` | Output CSV in the glossary format (`term_en,chinese,reference,evidence,note`), every row marked `harvested; review before adopting` |
| `--corpus-out` | Writes each file's Chinese running text to a `.txt`, for `verify_zh.py --calibrate` |

What it extracts:
- **关键词 / Keywords pairs.**
  - They are read from the page text (with or without a colon, on the same or the next lines,
    separated by ；, ，, 、 or /), from `citation_keywords` meta tags, or from the JSON keyword
    lists that journal platforms embed in the page.
  - Lists of equal length are paired by position. Otherwise both lists are printed, to pair by
    hand.
- **First-mention brackets** 中文术语（English Term）, grouped by the English term so that the
  variants are visible. Author citations such as （Smith, 2010） are skipped.

Known limits:
- Pairing by position fails when the authors list the keywords in a different order; review
  every pair.
- The Chinese side of a bracket pair may include a few words of the sentence; trim it.
- Pages that build their content with JavaScript give little text. Use their PDF or another
  page of the same article.
