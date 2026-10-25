# 01 Register and lexicon

The most frequent defect of academic translations into Chinese is not a wrong word. It is a
correct, faithful sentence that no Chinese academic would write, because it keeps the syntax of
the source language. This file lists the patterns to avoid and what to write instead.

Reference figures come from a measured corpus of Chinese academic prose in economics: two
master's theses and six journal articles, about 149,000 characters of running text. "Corpus = 0"
means the form never appears there. Recalibrate with a corpus of your own field when you can
(`scripts/verify_zh.py --calibrate`).

## 1. Calques and their replacements

Each pattern reproduces a source-language structure with Chinese words. All of them have zero or
near-zero frequency in the reference corpus.

| Avoid | Typical source | Write instead |
|---|---|---|
| 加以 + verb (对其加以检验) | "is examined", "se somete a prueba" | 对其进行检验, or the bare verb: 在产品层面应用 |
| 与……相联系 | "is associated with" | 正相关 / 负相关; for a coefficient, 显著为正 / 显著为负 |
| 之所以……是因为 | "the reason why… is that" | 源于, 由于, 原因在于, or restructure the sentence |
| 正因如此 | "precisely because of this" | 鉴于此, 据此, 这也是……的原因 |
| 使得可以 / 使……得以 | "makes it possible to" | 使……能够, 有助于 |
| ……是直接的 | "the implication is direct" | 由此可以直接得出…… |
| 据以 / ……的那个 | "the one on which… is based" | 作为……的依据, ……时所参照的 |
| 不在于……而在于 | "the point is not X but Y" | 并非……，而是…… |
| 其目的是双重的 / 是双重的 | "its purpose is twofold" | 有两重目的, 包含两重含义, 体现在两个方面 |
| 使这一成为可能 | "makes this possible" | 使这一点成为可能 (这一 needs a noun) |
| 支配(着) + variable | "governs", "dominates", "drives" | 决定了, 影响 |
| 读作 / 读法 | "should be read as", "two readings" | 理解为, 两种解释, 目视考察 |
| 相容 | "compatible with" | 与……一致, 并不冲突 (keep fixed collocations such as 互不相容) |
| 反对意见 (methodological) | "objection" | 局限 |
| 证据是混合的 | "mixed evidence" | 证据不一 |
| 可辩护的 | "defensible (choice, date)" | 具有合理依据的 |
| 形式检验 | "formal test" | 正式检验 |
| 量级 (outside 数量级) | "magnitude" | 幅度, 规模, 大小 |
| 先例 | "precedent" (for a method) | 借鉴, 参照, 范例 |
| 专业化于 | "to specialise in" | 专门生产, 专门从事 |
| 政策处方 | "policy prescription" | 政策方案 |
| 合而为一 | "to conflate" | 混为一谈 |
| 进行了建模 | "modelled" | 构建了模型 |
| 第一是 / 第二项 / 第三项 | "the first is…" | 第一，……；第二，…… |
| 何况, 况且 | "all the more since" | 此外, 而且 |
| 名目, 值得做的是, 所能支撑, 要紧的是, 呈现在……面前, 在那里 | literal renderings | rewrite with a plain academic verb |
| 所生产之物 | "what is produced" | 所生产的产品 (no archaic forms) |
| 不必然 | "not necessarily" | 不一定 |
| 顾及 | "to take into account" | 考虑 |
| 差距是数量级上的 | "the gap is an order of magnitude" | 差距十分悬殊 |
| 还有待完成 at the end of a long subject | "X remains to be built" | 还需要构建X |
| 自[协定]以来 | "since the agreement" | 自[协定]生效以来 (an agreement is not a point in time) |

How to apply it:
- A calque is not fixed by search and replace. Many sentences have to be rebuilt.
- When you replace a form, check the meaning against the source.

## 2. Pronouns and anaphora

- **它 / 它们 as subject is a calque** of the implicit subject of Romance languages and of
  English "it". In the reference corpus 它 occurs about 1.7 times per 10,000 characters. Write the
  noun, 其, 该 + noun, or chain the clauses by topic with the subject omitted.
- **Never replace 它 mechanically with 其 or 该变量.** Fix pronouns section by section, and check
  the referent against the source each time. Bulk replacements have attached pronouns to the
  wrong noun.
- **Every backward reference needs an explicit, near antecedent:** 这一问题, 该机制,
  这种不对称性, 效应, 幅度. Chinese tolerates distant anaphora less than Spanish or English.
  A native reviewer will ask 指的是什么 / 是什么机制; name the referent instead.
  - Example: 同意建立该机制 → 同意建立[组织全称].
- **效应, 影响 and 作用 always say on what:** 对劳动生产率的效应, not a bare 效应.
- **An elliptic source sentence** ("It is not.", "No lo es.") becomes a full sentence with its
  subject. Keep the number of sentences.
  - Example: 上一节把样本作为一个整体进行描述。然而，样本实际上并不是同质的。

## 3. Register

- **Self-reference:**
  - The author is 本文 or 本研究. Never 我们, 笔者 or 作者 in the body; 作者 only in a source
    line (资料来源：作者整理).
  - Do not repeat 本文 as the subject of consecutive sentences, especially in the 摘要. Vary with
    thematic subjects: 研究样本为……, 估计方法为……
- **Master's level, neither humble nor grandiose:**
  - 填补空白 → 研究切入点 / 本文的研究方向;
  - 据作者所知 → 就现有文献而言;
  - 未曾考虑 → 少有考虑 (soften absolute claims about the literature).
- **No "AI style" and no pedagogical self-explanation.** Avoid paragraphs that explain the logic
  of the text itself in a self-conscious enumerative tone ("X is…, Y is not…, even if…"). Use the
  genre's moulds instead (`02_syntax.md`, `03_connectors.md`).
- **No metatext:**
  - no sentences saying what a section does or does not do;
  - no warnings about how not to read a figure;
  - no "this will be explained in chapter X";
  - no production notes ("text in the figure is in Chinese").
  - A supervisor will delete them all as 不属于文章内容.
- **No conversational or moral turns** ("to be honest", "we should declare rather than hide").
  State a weakness in the present tense, without moral adjectives, and point to the test that
  deals with it.
- **No vague jargon.** If a result is weak: the coefficient does not reach significance, or only
  in one column. Nothing more.
- **No work log inside the text:** no protocols, earlier decisions, corrections or "provisional,
  to be completed".
- **Policy recommendations open with a programmatic verb** (建立, 完善, 推动, 合理看待), never
  with a colloquial imperative (不要指望……).
- **No bold in running text.** Emphasis is carried by position in the paragraph and by
  connectors. Ignore the bold of the source.
- **Deliberate repetition is part of the genre.** Central ideas are stated in the abstract, the
  body and the conclusions with the same terminology. No ornamental synonyms.

## 4. Collocations

Use the fixed collocation; do not translate noun + verb word by word.

| Avoid | Write |
|---|---|
| 保护主义压力上升 | 保护主义抬头 |
| 协定产生效应 | 协定发挥作用 |
| 首要决定 (two qualifiers) | 首要因素 |
| 联合促进 | 联合推动 |
| 进口商与出口商 | 进出口商 |
| ……等区域进程 (for entities) | ……等区域组织 (name the category of the entity) |
| 是否使其出口…… (what has a composition is the product) | 出口产品 |

A combination that "can be understood" but that nobody writes is a defect. When in doubt, check
attestation (`05_terms_glossaries.md`).

## 5. Preferred academic vocabulary

From model rewrites by Chinese supervisors:

- **Attributing ideas to authors:** 认为, 指出, 论证, 证实, 进一步证实, 进一步表明, 强调, 提出,
  开创性地提出, 区分, 揭示, 解释, 系统梳理, 确立了……的联系, 将这一逻辑引入/延伸至……
- **Presenting data, tables and figures:** 呈现, 展示, 报告, 印证, 列出, 补充了这一图景.
- **Abstract nouns:** 核心贡献, 传导链条, 环节, 路径, 取向, 语境, 情境, 逻辑延伸, 理论根源,
  前提条件, 异质性, 结构性差异, 宏观背景.
- **Precision adverbs:** 严格（取决于/调节）, 显著, 根本性（差异）, 截然不同, 高度（依赖）.
- **Fixed formulas:** 并非自动实现, 并不等同于, 性质截然不同, 相容而非互斥, 无法直接区分.
- **Choose the reporting verb by function**, not always 记录 for "documents / records":
  - an author documents a finding → 发现, 揭示;
  - a datum records something → 体现;
  - "which chapter 4 documents" → 如第四章所示.

## 6. Absences are as diagnostic as excesses

Forms that the corpus uses and that a translation often lacks:

| Form | Corpus per 10,000 characters | Function |
|---|---|---|
| 结果显示 / 结果表明 | 3.8 | Introduce a result |
| 进一步 | 6.4 | Move to a finer level of the same analysis ("in more detail") |
| 从而 | 6.9 | Consequence inside the sentence |
| 有助于 | 3.2 | "allows", "contributes to" |
| 一方面……另一方面 | 4.5 / 2.2 | Two sides of one question in one paragraph |
| 显著为正 / 显著为负 | 2.7 | Significance and sign |
| 这说明 / 可能的原因 | 0.5 / 0.5 | Reading and explanation |
| 得到验证 | 0.4 | Hypothesis verdict |

## 7. Measure before you replace

**Before proposing a replacement form, count how often it already appears in the document.**
If its rate already exceeds the corpus rate, choose another form. Otherwise you trade one tic for
another.
- Real case: 换言之 was proposed to replace 这意味着 while 换言之 was already at 3.6 times its
  corpus rate.
- Replacements that are often already overused: 视为, 其, 描述, 指出, 预期.

**The converse also holds.** A form that is frequent because the source argues that way (因为
for a text that says "because" on every page) is not a translator's tic. Leave it; changing it
would rewrite the argument.

## 8. Quotation marks for coined concepts

Use “ ” for:
- coined terms;
- names of initiatives;
- the author's own labels;
- a technical term the first time it is introduced or defined;
- conceptual oppositions (外部知识的“可获得性”与“可利用性”).

Do not use them for citations or for ordinary proper names. A few well-placed occurrences, not a
sweep: in the reference theses, about 13 per 10,000 characters.
