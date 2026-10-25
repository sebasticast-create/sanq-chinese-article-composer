# 08 Anti-rules: suggestions to reject

Reviewers (human or automatic) and other models will propose changes. Most improve the text;
some damage it in predictable ways. Reject the following, and write the reason in the triage
table (`09_process.md`).

| # | Reject | Why |
|---|---|---|
| 1 | **Turning associative wording into causal wording** (并未伴随……的差异 → 并未带来……; 与……相关 → 使……显著提升; 评估……的政策效应), however natural it sounds | The study claims an association. Filter every suggestion for 使, 促进, 导致, 推动, 引起, 造成, 产生了, 提升了, 提高了, 带来, 政策效应, 因果效应 |
| 2 | **Reintroducing 它**, or changing 其 → 它 | 它 as subject is a calque (`01`, 2) |
| 3 | **Replacing 它 with an already overused form** (其, 该变量, 视为, 描述, 指出, 预期) | Trading one tic for another (`01`, 7) |
| 4 | **Wholesale rewrites of a paragraph** | Take only the local fix of a calque, written in your own words, never the whole paragraph. Rewrites add or change content (a new claim, a new technical term) |
| 5 | **Replacing a fixed project term with a synonym** | Terms fixed by the user or the glossary stay. Neither 渠道 → 机制 nor 渠道 → 方法 when the source distinguishes them, nor 观察 → 实现 when a variable measures a channel |
| 6 | **Retouching the supervisor's literal text**, even where it clashes with the corpus | The supervisor's adopted wording is kept literally. Flag a real clash to the user; do not fix it silently |
| 7 | **Deleting content to lighten the style**: a sentence that makes a claim, a technical term, a prefix that changes meaning (超国家机构 → 国家机构) | Fidelity. Style is not a reason to lose content |
| 8 | **Proposals that change the meaning** ("two problems" → "the current situation") | Same |
| 9 | **Replacing a precise technical term with a colloquial phrase** (识别上的考虑 → 需要考虑的地方) | Register and precision |
| 10 | **Adding numerical precision or vagueness** that the source lacks (三百 → 三百余) | Fidelity of figures |
| 11 | **Sweeping a frequent connector** whose frequency mirrors the source (因为, 因此, 由此, 而非) | It is how the source argues (`03`, 8) |
| 12 | **Merging sentences or paragraphs; adding announcements or introductory paragraphs** | Paragraph correspondence; no metatext |
| 13 | **笔者** as self-reference | Use 本文 / 本研究 |
| 14 | **Unifying a term without checking the glossary and attestation**, or adopting a reviewer's form without evidence | Unifying toward the minority form has to be reverted later |
| 15 | **Touching figures, years, authors, section numbers, tables, equations or citations** | Out of the scope of language revision |
| 16 | **Declaring a supervisor's sentence wrong** without first checking it against the text and the record of decisions | It may already have been discussed and adopted |

## Accept the diagnosis, not necessarily the proposal

A native reviewer is often right that something is wrong and wrong about the fix.
- Real case: «差距是数量级上的» (calque of "an order of magnitude"). The reviewer proposed
  体现在数量上, which loses the meaning. The adopted form, 差距十分悬殊, accepts the diagnosis and
  finds a third wording.
- A reviewer's own proposal can be ungrammatical. Check it as carefully as the original.

## A suggestion is accepted only if

- it does not clash with the user's instructions, the institution's norm, the native reviewer's
  accepted judgements or the corpus evidence, in that order of priority;
- it does not change meaning, figures or the strength of a claim;
- its replacement form is not already overused in the document;
- it leaves the passage at least as well connected as before.
