# Translation report: "Minimum wages and youth employment" (test paragraph, English → Chinese)

## 1. Scope
- **Source:** `source.md`, English, 1 paragraph, 6 sentences.
- **Discipline:** labour economics.
- **Profile:** `article`.
- **Norm:** none given.
- **Note:** the paragraph was written for this test. Its study, figures and county panel are
  invented; only the citation of Card and Krueger (1994) refers to a real, published study.

## 2. Verifier output
See `verifier_output.txt`: NO FAILS, 1 warning (D2, a term pending human check), 1 REVIEW (B7).

## 3. Paragraph correspondence
| Section | Source paragraphs | Chinese paragraphs |
|---|---|---|
| Body | 1 | 1 |

Sentences: 6 in the source, 6 in the translation.

## 4. Glossary
- **Adopted, with evidence** (`glossary.csv`):
  - 最低工资 (《最低工资规定》);
  - 工资总额 (国家统计局 indicator);
  - 检验功效 (a Chinese supervisor's wording);
  - 双重差分法, 标准误, 个百分点, 处理组, 对照组, 平行趋势假设 (corpus).
- **Pending human check [待人工核对]:** youth employment → 青年就业. The only Chinese study found
  is Taiwanese and writes 青少年就业. Check usage in mainland journals (CNKI: 最低工资 青年就业 /
  青少年就业).

## 5. Sentences split
None.

## 6. Decisions
- "is consistent with parallel trends" → 与平行趋势假设一致, not 平行趋势成立: a non-rejected test
  does not prove the assumption (`04`, 5).
- "although the test has low power" → 但检验功效较低, kept as a caveat inside the sentence.
- "is not statistically significant at the 10% level" → 在10%水平上并不显著, without softening
  (not 较弱) and without hardening.
- "1.4 percentage points" → 1.4个百分点. "2.4 billion dollars" → 24亿美元 (2.4 × 10 = 24 亿).
- "Card and Krueger (1994)" → Card 和 Krueger（1994）, names in Latin script, year in full-width
  parentheses.
- Standard error in the corpus pattern: 估计系数为0.014（标准误：0.009）.

## 7. Triage of external suggestions
None received.

## 8. Issues in the source (for the author)
- **REVIEW B7: «该政策使年度工资总额增加约24亿美元».** It is causal because the source is causal
  ("The policy raised…"). It is kept, because the translator does not change the strength of a
  claim. The author should check that this is an accounting figure and not an estimated effect;
  if it is estimated, the associative wording of the rest of the paragraph would be more
  consistent.
