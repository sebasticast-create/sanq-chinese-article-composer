# 03 Connectors and cohesion

**The connection of ideas outranks register, terminology and format.** A correction must never
remove a connective without putting another in its place, unless the sentence already says it.
If a passage ends grammatically flawless but logically lame, undo the correction and note it.

## 1. Reference rates

Per 10,000 Chinese characters of running prose. Measured on a corpus of economics theses and
articles, excluding tables of contents, tables, captions and references. These are defaults:
recalibrate on your field.

| Family | Rate | Most used forms (rate) |
|---|---|---|
| Enumerators | 36.8 | 第三 8.5; 一方面 4.2; 第一 4.1; 首先 4.0; 第二 4.0; 其次 3.1; 最后 2.0; 另一方面 2.0 |
| Addition | 26.4 | 还 6.4; 进一步 6.0; 同时 5.4; 不仅 3.2; 此外 2.2 |
| Cause and consequence | 20.7 | 因此 9.3; 从而 6.7; 由此 1.9; 原因在于 0.7 |
| Significance | 16.3 | 显著 15.0; 不显著 1.3 |
| Hedging | 11.8 | 可能 10.9; 有待 0.5 |
| Contrast | 8.7 | 但是 2.1; 然而 1.9; 尽管 1.5; 虽然 1.5 |
| Empirical result | 7.6 | 结果显示 2.0; 结果表明 1.4; 研究发现 1.2; 研究表明 1.1 |
| Hypothesis | 4.8 | 假设 3.0; 成立 1.1; 得到验证 0.4 |
| Synthesis | 2.6 | 综上 0.8; 综上所述 0.6; 据此 0.5; 由此可见 0.3 |
| Announcing metatext | 0.7 | 值得注意的是 0.3; 需要说明的是 0.3; 下文将 0.07 |

**Overall connective density.** The verifier measures density with a fixed list of about 90
forms (`scripts/verify_zh.py`, `CONNECTIVES`).
- Two reference master's theses measured with that list: 92.4 and 96.0 per 10,000, with 53 and
  48 distinct forms.
- Default WARN thresholds: below 92 per 10,000, or fewer than 48 distinct forms, on texts long
  enough to measure (≥ 3,000 Chinese characters).
- **A comparison is valid only if both sides are measured with the same list and the same text
  extraction.** A broader list gives higher numbers (about 133 to 158 per 10,000 on the same
  corpus); never compare a figure measured one way with a threshold measured another.

## 2. Enumeration

- **Enumerating a lot is the norm, not an excess.** The strict pattern (首先/其次/再次/最后 +
  第一/第二… followed by ，、环节 方面 条 点) runs at about 16 per 10,000. The two reference
  theses are at 12 and 19, and articles range from 7 to 31.
- **Do not reduce enumerators.** Structure is carried by enumerating, not by announcing.
- Use 第一，第二，第三，, never 第一是 / 第二项.
- For mechanisms: 该理论的核心贡献在于揭示了两个机制：第一，……；第二，……

## 3. One aspect, two sides: 一方面……另一方面

Use it for two parallel facets inside the same paragraph, not scattered across paragraphs.
> 本节通过相关系数矩阵，一方面初步判断变量之间的相关程度，另一方面判断是否存在多重共线性。

## 4. 进一步

进一步 marks the move to a finer level of the same analysis, and replaces "in more detail" and
"more thoroughly". It is usually under-used in translations: 6.4 per 10,000 in the corpus.

## 5. Closing a block

- 综上 / 综上所述 / 据此 / 基于此 go at the start of the sentence, **followed by the
  consequence**, never by a mere summary of what was said.
- Prefer 综上 to close a theory block. 总之 exists but is less frequent in the genre.
  > 综上，本文对两个维度分别赋予0.5的权重，构建综合指标。

## 6. Cohesion formulas of the genre

| Function | Formula |
|---|---|
| Close a line of literature | 这一支文献的共同结论是：…… / 对本文而言，这意味着…… |
| Theory → case | 结合[研究对象]语境，……的传导链条可分解为两个环节：第一环节，……；第二环节，…… |
| Theory → hypothesis | 基于上述理论逻辑，本文提出Hn： / 基于以上分析，本文提出以下假设： |
| Link to the previous chapter (backward, free) | 通过第二章的文献综述与第三章的理论分析，本章首先…… |
| Forward reference (task only) | ……将在第五章进行检验 (never anticipate the sign or size of a result) |
| End of a results block, substantive transition | 以下基准回归将进一步以系数形式量化上述效应的平均幅度。 |
| Two comparisons | 上述两个比较表明：…… |
| Subgroup summary | 小结：将三组结果比较观察，本文发现：…… (findings only, no disclaimer) |

**Do not use the same formula as a refrain.** If 「基于……，本文提出」, 综上所述 or 由此可见 appears
six times or more, vary it: the reference theses alternate 综上所述 and 基于以上分析, or use
neither.

## 7. Announcing metatext: ceiling

- **No section announcements:** 本节将, 本章主要, 本章旨在, 下面将, 接下来将. The reference
  theses have zero in about 83,000 characters each. Enter the subject directly.
- **Ceiling for 值得注意的是, 需要指出的是, 需要说明的是 and 需要强调的是:** about one per
  20,000 characters.
- Legitimate use: justify a debatable choice in one sentence and point to its test.
  > 需要说明的是，等权重设定虽具有简明直观的优势，但其主观性可能影响指标测度的稳健性。

## 8. Do not sweep

When a connector is frequent because the source argues that way (因为, 因此, 由此, 而非), it is
not a tic. Rewriting it would rebuild the argumentative surface of the text. If it must change, it
changes in the source first.

Calques that are swept (加以, 相联系, 使得可以, 之所以) are verbal constructions inside a clause,
not connectives. Removing them must not lower connective density. If it does, a correction
removed argumentative tissue.

## 9. Under-used forms worth considering

Where the source allows it: 进一步, 从而, 有助于, 结果表明, 回归结果, 这说明, 一方面……另一方面.
