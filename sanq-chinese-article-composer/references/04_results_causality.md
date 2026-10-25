# 04 Results and causality

## 1. Association is not causation

**Rule:** the study's own results are reported with associative vocabulary unless the source
makes a causal claim and the design supports it. A randomised controlled trial, for example,
supports the causal wording its authors use (……可归因于治疗); an observational panel usually does
not. The translator changes **only how a result is
stated, never the result**: figures, significance and conclusions stay identical.

**Vocabulary that does not imply causation in Chinese** (legitimate also for nulls):
- 效应, 影响, 作用;
- 相关联, 正相关 / 负相关, 显著为正 / 显著为负;
- 并无显著关联, 并无系统差异, 不显著, 在统计上无法区分;
- 与[处理]相关的差异, [处理]对应的……高出N个百分点.

**Words to avoid when the treatment, policy or membership is the subject of the study's own
estimate:** 使, 促进, 导致, 带来, 推动, 引起, 造成, 提升了, 提高了, 产生了, 因果效应, 政策效应.
Rewriting a cautious source sentence with them because it "sounds more natural" is the most
common way reviewers and other models damage a translation.

**Scope.** The rule covers the study's own results only. Do not touch causal language in:
- theory and literature review (what other authors claim);
- hypotheses (hypothesised links);
- conditionals;
- technical method terms (固定效应, 处理组平均处理效应);
- sentences that already limit causality ("the design does not allow a causal reading").

**Typical transformations (source → decided form):**

| Source says | Chinese |
|---|---|
| "X raises Y" (estimated) | X对应的Y更高 / X与更高的Y相关联 |
| "X did not raise Y" | X与Y的提高并无显著关联 / 处理组与对照组并无系统差异 |
| "the true effect" | 该组的估计系数 |
| "the effect is 3.2 points" | 与[处理]相关的差异为3.2个百分点 (keep 得到验证 if the source says "confirmed") |
| "the channel that worked" | 获得实证支持的渠道 |
| "a strong positive effect" | 显著为正且稳健的系数 |
| "causal inference with panel data" (method name) | 面板数据双重差分法 / 反事实评估方法 |
| "open the causal black box" | 考察机制 |

**Limitations** are concentrated in one place (e.g. 研究局限与展望), numbered (第一，……的局限性。),
each ending in 未来研究可……. A serious limitation is admitted in one line, without apologies.
> 本文的发现应被理解为稳健的相关关系，而非严格的因果论断。

## 2. Reporting a coefficient

**These are the conventions of economics and empirical social science.** Other fields report
differently:
- clinical medicine writes 差异有统计学意义（P<0.05） rather than 显著, and gives 95%CI or
  均数±标准差;
- some fields never report coefficients at all.

Learn the field's convention first (`10_field_discovery.md`, 6). When it differs from what
follows, the field wins.

In economics:

Three moves:
1. **Figure:** coefficient, standard error and significance.
2. **Reading:** what the sign means in the language of the hypothesis.
3. **Verdict:** whether the hypothesis is supported.

Template:
> 变量（符号）系数为X（标准误：Y），在N%水平上显著，表明……；其可能的原因在于……

**Rules:**
- **Significance and sign:** 显著为正 / 显著为负, never 以正号进入且显著 (zero in the corpus,
  about 40 uses of 显著为正/负).
- **Standard error** in parentheses right after the coefficient: （标准误：0.017）. It is not
  discussed in prose.
- **Significance phrase:** choose one form and do not mix. The corpus prefers 在N%水平上显著
  over 在N%的水平上显著 by about 3 to 1. Consistency is what matters.
- **Introducing a result:** 结果显示, 结果表明, 回归结果显示, 实证结果表明.
- **Never leave a coefficient alone:** it carries its reading.
- **Signs are always translated into the language of the hypothesis:** 系数为负，表明……越倾向于……
- **Economic magnitude, with the right unit:**
  - 个单位;
  - 个百分点 for a share expressed as a fraction (a coefficient of 0.032 on a 0–1 share is
    3.2个百分点);
  - 个标准差 for standardised variables.
  - Write it in associative wording: [处理]对应的……高出3.2个百分点, not ……使……提高3.2个百分点,
    unless the design is causal and the source says so.
- **p-values:** （p=0.032）; several values: （p值分别为0.041和0.008）; p<0.001.
  - "four of them below 0.1%" refers to p-values: 其中四个在0.1%水平上显著.
- **"Marginally significant":**
  - in the abstract or for non-specialists, state the level: 仅在10%水平上显著;
  - in the body, 边缘显著 is acceptable if used uniformly.

## 3. Tables and figures in the text

- The number is the subject, followed by a presentation verb, and the finding is attached:
  - 表5-3报告了……的估计结果，……
  - ……，结果如表5-3所示。
  - 图4-2呈现了……的走势。
- The prose walks the table column by column: 列（1）……；列（2）加入控制变量后，系数保持稳定。
- Introduce each table or figure in the text before it appears.

## 4. Hypotheses

- **Wording:** one sentence, comparative and directional, after the argument, never before it.
- **Hierarchy:** state it when there is one (主假设 / 机制假设).
- **A hypothesis travels:** stated in the theory chapter, tested with a table, recalled in the
  conclusions, always with the same wording. No table without a hypothesis behind it, no
  hypothesis without a table.
- **Expected heterogeneity goes into the hypotheses ex ante** (H1a……), not as an ex post
  observation.
- **Verdicts:**
  - 假设H2得到验证 / 未得到验证 / 未得到支持 / 被拒绝.
  - The **hypothesis** is rejected, not the **channel**. For a channel: 该渠道并未实现, or
    ……并不显著.
  - In mediation analysis the mediator is not randomly assigned: a link 得到验证 or receives
    partial support. The reservation is a limit of the design:
    > 由于……，……不足以证明……，只能说明……

## 5. Nulls, assumptions and fragile results

- **A test that does not reject an assumption does not prove it.**
  - 差异趋势不显著不等于平行趋势成立.
  - Say 平行趋势假设未被拒绝 or 未发现处理前存在显著分化, and admit low power when the sample is
    small.
  - Tone down 有力支持, 精确吻合 and 几乎不可能由偶然因素产生 unless the source says exactly that.
- **"No effect" ≠ "no change".**
  > 事件研究所显示的“无效应”并不意味着处理组的结构没有发生变化，而是说明这些变动与对照组的同期变动在统计上无法区分。
- **Fragility is stated honestly.** If a result does not survive an alternative specification,
  the translation says so as the source does, without softening or hardening it.
- **Hedging goes inside the sentence:** 可能, 主要, 相对, 无法直接区分, 仅提供了……的背景. Never in
  separate warning paragraphs or captions.
  > 该占比的下降可能反映生产结构的实质性转型，也可能仅仅源于价格下跌导致的分母收缩，两种机制在占比数据中无法直接区分。

## 6. Do not interpret

- If the source says "does not reach significance", the translation says 未达到显著水平, not
  "is weak" (较弱) or "tends to be positive" (倾向于为正).
- Do not add a reading the source does not give.
- Phrases of a supervisor's model text that the user adopted are kept literally, even if they are
  stronger than you would write. If they clash with a later instruction from the same supervisor
  (e.g. "avoid overclaiming"), the later instruction prevails: flag the clash to the user rather
  than rewriting silently.

## 7. Method section openings

Open a method's results section by saying:
- what it estimates compared with the baseline model;
- which features it lets the reader see;
- why the pre-treatment coefficients test the assumption;
- which is the base period;
- how the interval is read.

> 与基准回归仅报告一个平均系数不同，事件研究法逐年估计处理组与对照组之间的差异，使读者能够观察两个关键特征：效应在何时出现以及效应如何随时间演变。所有系数均以政策实施前一年为基准期；图中竖线表示95%置信区间，若竖线不跨越零线，则该年度两组差异在5%水平上显著。
