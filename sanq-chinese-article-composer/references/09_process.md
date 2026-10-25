# 09 Process, triage and report

## 1. Priority when two sources collide

1. **Explicit instruction of the user or of whoever evaluates the text** (supervisor, editor).
   Between two contradictory instructions from the same person in different rounds, the most
   recent prevails.
2. **The institution's or journal's formal norm.**
3. **A native speaker with academic training**, for naturalness, collocation and register.
4. **A measured corpus of the subfield**, for frequencies, formulas and attested terminology.
5. **Automatic reviewers** (other models). Their proposals are accepted only if they do not clash
   with 1 to 4 and do not change meaning.

## 2. Steps

### Step 0. Optional: calibrate on a corpus of the field
- Gather two theses of the same programme (or of the same supervisor) and about six articles
  from the subfield, as plain text.
- Run:
  ```
  python scripts/verify_zh.py --calibrate corpus/*.txt -o config.json
  ```
  It measures sentence and paragraph lengths, connective density, enumerators and other rates
  with **the same lists and extraction the verifier uses**, and writes them as thresholds.
- Normalise spaces when the corpus was converted from PDF: conversions insert spaces inside
  Chinese words and break literal counts. The script does it.
- Measure only running prose: no tables of contents, tables, captions, references or English
  abstracts.
- Corpus files are for measurement. Do not quote long passages of third-party documents in the
  translation or in published material.

### Step 1. Glossary first
See `05_terms_glossaries.md`. Freeze it before translating.

### Step 2. Fix the master files
- One source master in plain text or Markdown (the source of truth) and one Chinese master in
  Markdown.
- A `.docx` is generated from the Chinese master, never edited by hand, so that a correction
  never lives in only one place.
- A model document (approved earlier) gives styles, tables and order of pieces, **not prose**:
  a format model can be a poor model of language.

### Step 3. Read before translating
- Read the whole source, the glossary and any supervisor's model rewrites (修改范例).
- **From model rewrites, copy the manner, not the content.** Do not import figures without a
  source, nor artefacts of the example.
- What the supervisor wrote and the user adopted is copied literally.
- Each supervisor's correction applies to the whole text, not only to the spot marked
  (全文类似的问题请自行修改).

### Step 4. Pieces that do not exist in the source
- Cover, 目录 (generated), glossary appendix, 摘要/Abstract if a model already has approved ones.
- Compare them against the source summary instead of redoing them from scratch.

### Step 5. Translate one section at a time
During translation it is forbidden to:
- summarise;
- omit, especially caveats;
- merge or split paragraphs;
- add transitions, clarifications or metatext;
- invent citations or figures;
- interpret results.

Mark untranslated parts with 【待翻译】, so that the verifier knows the counts are not
interpretable yet.

### Step 6. Verifier on that section before moving on
Zero FAILs before the next section: a loose register in one chapter spreads to the others.

### Step 7. Close each section
- Re-measure its connective density and recount its paragraphs against the source.
- If density drops or the count moves, a correction removed tissue: revise or undo, and note it.

### Step 8. Prose review against the corpus, one section per pass
- Large chapters (about 15,000 characters) are split by second-level sections. A pass over the
  whole document produces three or four examples per chapter and closes the matter falsely.
- Order of search:
  1. source-language form with Chinese words;
  2. internal inconsistency;
  3. divergence from the glossary;
  4. a tic introduced by corrections;
  5. sentences and paragraphs out of range.
- **No objection without evidence:** the measured figure, or a literal corpus sentence that makes
  the same rhetorical move. Without that it is a preference and is not formulated.
- Format of each objection:
  ```
  [N] <section>: <one line: what fails>
      Translation: «…»
      Source:      «…»
      Evidence:    «…» [corpus document]  or  <measured figure>
      Proposal:    «…»
  ```

### Step 9. Optional: native-judgement pass
- Complementary: an academic native reader, paragraph by paragraph, with the format
  原文 / 修改 / 理由 and priority 【高】【中】【低】.
- It touches no figures, years, authors, section numbers, variables, tables, equations or
  citations.
- It ends with a re-read for the coherence of its own corrections.

### Step 10. Triage of suggestions
Use the table in section 4 and the anti-rules (`08`):
- Apply accepted changes **by short sections, never as a whole-document sweep**. One bulk
  rewrite of eighty passages once slipped in five sentence merges that nobody saw.
- Undo any change that leaves a passage logically lame, however grammatical.

### Step 11. Whole-document pass
Consistency and glossary by counting (`05`, 5).

### Step 12. Assembly and delivery
- Run the verifier on the whole document.
- Generate and update the 目录.
- Deliver the report of section 5.
- Review each WARN; justify the ones you leave.

### Step 13. Catalogue of errors
- Record every real error with its correct form next to it (content, terminology, format,
  register), so that the next translation does not repeat it.
- If two translations of the same text are made, both must resolve the same catalogue items in
  the same way.

## 3. Comparing two translations

Apply the same procedure to both. Then:
- make a paragraph-by-paragraph table **only of the passages where they differ**;
- add a third column saying which one is closer to the corpus **and by which measurement**;
- where both depart from the corpus, say so and propose a third wording;
- never declare a winner on overall impression.

## 4. Triage table

| # | Origin (reviewer, model, web) | Passage | Suggestion | Decision | Reason |
|---|---|---|---|---|---|
| 1 | native reviewer | «……» | «……» | accepted | fixed collocation 发挥作用 |
| 2 | model X | «……» | «……» | rejected | turns association into causation (anti-rule 1) |
| 3 | native reviewer | «……» | «……» | diagnosis accepted, third form adopted: «……» | proposal loses the meaning |

## 5. Decision report (template)

```
# Translation report: <document>, <sections>

## 1. Scope
Source: <file, language>. Profile: <thesis/article/report>. Norm: <institution profile or "unknown: items to check">.

## 2. Verifier output
<pasted as is>

## 3. Paragraph correspondence
| Section | Source paragraphs | Chinese paragraphs | Note |

## 4. Glossary
- New terms adopted: <term → 中文, reference, evidence>
- Terms pending human check [待人工核对]: <list, with the candidates found>
- Deviations from the user's glossary, with justification: <list or "none">

## 5. Sentences split
<source sentence → Chinese sentences>

## 6. Doubtful passages
<source next to translation, what is doubtful, how it was resolved provisionally>

## 7. Triage of external suggestions
<table of section 4>

## 8. Issues in the source (for the author, not fixed)
<clumsy or contradictory passages, figures that look wrong>
```

## 6. Unit size

| Section size | How to review it |
|---|---|
| About 5,000 to 9,000 Chinese characters | One pass |
| About 15,000 | Split by second-level sections |

Coherence and glossary checks are the exception: they run once over the whole document, at the
end.
