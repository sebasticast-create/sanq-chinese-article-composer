# Translation report: "Acupuntura en el insomnio por deficiencia del corazón y del bazo" (test paragraph, Spanish → Chinese)

## 1. Scope
- **Source:** `source.md`, Spanish, 1 paragraph, 5 sentences.
- **Discipline:** traditional Chinese medicine → acupuncture → randomised controlled trial.
- **Profile:** `article`.
- **Norm:** none given.
- **Note:** the paragraph was written for this test. Its trial and figures are invented.

## 2. Field discovery (`references/10_field_discovery.md`)

**Field profile.**
- Central terms: the TCM syndrome, the acupoints, the sham control, the sleep scale, the
  interval and P value, blinding.
- Concepts of Chinese origin to back-translate: «deficiencia del corazón y del bazo», Shenmen,
  Sanyinjiao, Baihui.

**Sources.**
- Searches: web search with Chinese terms (针刺 心脾两虚 失眠 随机对照 关键词…).
- Downloaded into a separate folder: 10 open documents (8 abstract pages, 2 full-text PDFs).
  - The pages come from journal platforms: tiprpress.com, 国家科技期刊平台 opaj.napstic.cn and
    search.napstic.cn.
  - The PDFs come from the open-access publisher Hans (CC BY).
  - There is also the Chinese Cochrane summary.
  - List in `discovery/sources.csv`.
- One page returned 403 and was discarded.
- Not used: CNKI search (captcha).
- Two terms absent from the harvest were checked by web search:
  - 假针刺 and 盲法, attested in 《中国针灸》 and in a review in 世界科学技术-中医药现代化;
  - the field's statistical reporting, from Chinese medical journals' author guidelines.

**Harvest** (`discovery/harvest_output.txt`, `discovery/harvest.csv`):
- 40 bilingual pairs, among them 25 关键词/Keywords pairs written by the authors.
- Attestation counts for the candidate variants (`discovery/candidates.txt`).

**Conventions adopted.**
- **Significance:** medical journals write 差异有统计学意义（P<0.05）, not 显著 or 显著性差异. Their
  author guidelines say so. Verifier config: `significance_style: medicine` (`config.json`).
- **Interval and P value:** 95%CI with the interval as 3.1～6.1; the P value is copied as in the
  source.
- **Counts and duration:** 120例患者 (例 for patients); 治疗4周 (duration in Arabic digits, as
  the harvested abstracts write 疗程均为4周).
- **Causal wording:** «can be attributed to the treatment» is kept causal (该差异可归因于治疗).
  The design is randomised and the source states it. Association rule, scope (`04`, 1).

**Calibration.**
- Run on the harvested text, but the corpus has fewer than 20,000 characters (abstracts). The
  script warned that the thresholds are unreliable.
- Defaults kept; only `significance_style` set.

## 3. Verifier output
See `verifier_output.txt`: NO FAILS, 1 warning (D2: three terms pending human check).

## 4. Paragraph correspondence
1 source paragraph, 1 Chinese paragraph; 5 sentences each.

## 5. Glossary
See `glossary.csv`.

**Decided by attestation in the field.**
- 心脾两虚证: 8 of 10 documents; 关键词/Keywords pairs in 3.
- 失眠, rather than the classical 不寐: 10 documents against 2.
- 针刺, not 针灸, which pairs with "acupuncture and moxibustion".
- 匹兹堡睡眠质量指数 (2 documents), not 匹茨堡 (1).
- 评分, not 得分.

**Back-translated.**
- 心脾两虚证, not 心和脾的缺乏综合征.
- 神门（HT7）, 三阴交（SP6）, 百会（GV20).

**Pending [待人工核对].**
- 针刺组 (only 治疗组 found).
- 主穴 (not in the harvest).
- The spelled-out form of 95%CI (置信区间 / 可信区间).

## 6. Sentences split
None.

## 7. Triage of external suggestions
None received.

## 8. Issues in the source (for the author)
- «Este ensayo clínico aleatorizado asignó…» does not say how many patients were in each group.
  Not added.
