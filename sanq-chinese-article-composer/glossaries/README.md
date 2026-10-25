# Glossaries

| File | What it is |
|---|---|
| `glossary_template.csv` | Empty format to copy: one row per term, with reference and evidence |
| `economics_international_trade.csv` | Example glossary of generic terms in economics and international trade (English, Spanish, Chinese) |

## Columns

| Column | Meaning |
|---|---|
| `term_en`, `term_es` | Source terms (any column whose name starts with `term`; add `term_fr`, `term_de`…) |
| `chinese` | Adopted Chinese form |
| `reference` | Where the form comes from |
| `evidence` | What was seen, and when |
| `note` | Variants, context of use, `[待人工核对]` if pending human check |

Spanish headers are accepted too: `origen`, `chino`, `fuente`, `evidencia`, `nota`.

## Provenance of the example glossary

The example was distilled from a 436-term glossary built while translating an economics thesis.
Only generic terms are kept; terms fixed for that particular thesis are left out.

Reference codes:

| Code | Meaning |
|---|---|
| `corpus` | Attested in a measured corpus of eight Chinese economics documents (two master's theses, six journal articles, about 149,000 characters). Counts are occurrences in that corpus. |
| `corpus glossary` | Usage note of the glossary built on that corpus |
| `supervised draft` | Count in a Chinese thesis draft read by a supervisor, used to decide between two attested variants |
| `native reviewer` | Correction by a native academic reader |

**These terms were not re-checked one by one on 术语在线 for this release.** That site needs a
browser (see `references/05_terms_glossaries.md`). Before adopting the glossary in a new project,
check the terms the project depends on, and update `reference` and `evidence`.

The example is a starting point. Under the skill's priority rules, the user's own terms and
glossary prevail over it.
