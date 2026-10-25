# 02 Syntax and paragraph structure

## 1. Length, measured

Reference values, from Chinese running prose in economics (two theses and six articles):

| Unit | Mean | Median | p90 | p99 |
|---|---|---|---|---|
| Sentence (characters, split at 。！？；) | 47 | 41 | 87 | 140 |
| Paragraph (characters) | 146 | n/a | 337 | n/a |
| Sentences per paragraph | 3.0 | n/a | n/a | n/a |

How to read them:
- **More than 90 characters without punctuation** puts a sentence in the longest 10% of the
  corpus: consider splitting it.
- **More than 140** is outside the 99th percentile: split it.
- **A paragraph of more than 340 characters** is outside what the corpus does, and **one of more
  than 1,000** does not exist in it. A one-sentence monolith paragraph is a sign of calque: the
  source chains with subordinate clauses what Chinese separates into sentences.
- The thresholds are configurable in the verifier.
- A supervisor's rule of thumb on the source side: split sentences of more than 35 to 40 words
  into two or three.

## 2. What may and may not change

- **Splitting a long sentence into two or three is the only licence against literalness**, and
  it is a licence of punctuation only.
- **One source paragraph = one target paragraph.** Never merge or split paragraphs. Recount
  after every revision pass: merges introduced by "style improvements" are the most common hidden
  damage.
- **Do not merge sentences** to improve flow.
- **Before splitting, look at the source.** If the source is itself one endless sentence, the
  problem may be there: flag it for the author instead of rewriting on your own.

## 3. Sentence-level patterns

| Problem | Before | After |
|---|---|---|
| Elided head noun in a parallel structure (the source says "and that of exports") | 城市人口增长率呈上升趋势，而农村…… | ……，而农村人口增长率…… |
| 的-chains and nominalisations | 把劳动力流动性的不足…… | 缺少劳动力流动性…… |
| | X的保留是…… | 对X需要作……上的限定 |
| Long clause embedded in 与……相关 | 处理组与就业率高出3.2个百分点相关，且在1%水平上显著 | 处理组对应的就业率高出3.2个百分点，在1%水平上显著 |
| Dangling predicate after a very long subject | 构建一项覆盖全部地区的、连续的度量仍有待完成 | 还需要构建一项覆盖全部地区的、连续的度量 |
| Event without its verb | 自改革以来 / 自协定以来 | 自改革实施以来 / 自协定生效以来 |
| "More X, not less" | 变得更加集中，而不是更少 | 集中度进一步提高，而非下降 |
| | A变得更集中，而B变得更少 | A的集中度上升，而B的集中度下降 |
| "What matters is whether" | ……是是否…… | ……在于是否…… |
| Focalised source structure ("The link… is provided by literature Y") | ……之间的联系，由Y文献提供 | Y文献揭示了……之间的联系 |
| "Does not exhaust the description of a…" | ……并未穷尽对一个……的描述 | rewrite; no indefinite 一个 calqued from "un/a" |
| "In exchange", "all the more since" | 作为交换…… | 但……, 此外……, 而且…… |

**Word order:** Chinese puts the temporal and locative frame, and the conditions, before the verb.
Reorder sentences that keep the source order.

**Elliptic or ultra-short source sentences** ("It is not.") become complete sentences with an
explicit subject and complement, keeping the sentence count.

## 4. Contrast and precision constructions

Prefer these constructions for nuance; they recur in supervisors' model rewrites.

| Construction | Example |
|---|---|
| 并非……而是…… | 溢出效应并非自动实现，而是受到接收方吸收能力的严格调节 |
| 不仅是……更是…… | 这不仅是计量方法的选择，更是理论在实证层面的逻辑延伸 |
| 既……也…… / 既未……也未…… | 两组的轨迹既未在政策实施前出现分化，也未在实施后呈现持续扩大的差距 |
| 如果说……那么…… | 如果说与A的比较揭示了取向差异，那么与B的比较则揭示了路径差异 |
| A而非B / 相容而非互斥 | 源于共同的外部冲击而非处理效应的消退 |
| 前者……后者…… | 前者以观测值定年，后者以滤波后的长期成分定年 |
| 即使……仅……即足以…… | 即使数量完全不变，仅相对价格的变动即足以使占比发生显著变化 |

## 5. Paragraph architecture

### 5.1 General unit

Claim → theoretical justification → supporting citation with author and year → evidence or
example → implication. The last sentence links back to the research question. **The development
comes first and the conclusion after, never the reverse.**

### 5.2 Theory paragraph: three moves

1. **Theory as subject:** X理论认为，……（作者，年份）。后续研究进一步证实，……。这意味着，……
2. **Mechanism:** 为解释这一差异，[作者]提出了……的概念，将其定义为……。该理论的核心贡献在于揭示了两个机制：第一，……；第二，……
3. **Implication for the study:** 综上，……。这一理论直接决定了本文的实证策略：……

Do not open a theory section with metatext ("The second premise concerns…") or with loose
aphorisms without a theoretical subject. Open with the name of the theory.

### 5.3 Literature review: "one author, one contribution"

- Each author takes one short clause with one contribution verb.
- Clauses are chained with ；and with 进一步 / 则.
- The line closes with the common conclusion and its implication.
- Never narrate each author's model in detail.

Before (narrative, calqued):
> 第二条渠道是知识溢出。奠基性的参考文献是A（1995），他们把以下思想形式化：一个地区的生产率不仅取决于本地的研发存量，也取决于外部的研发存量；他们发现……

After:
> 第二条渠道是知识溢出。A（1995）确立了区域间研发溢出与生产率的联系；B和C（2009）进一步表明溢出强度受接收地区制度特征调节；D（2022）则将这一逻辑引入城市层面。这一支文献的共同结论是：溢出并非自动发生，而取决于接收方事先积累的知识。对本文而言，这意味着样本地区在吸收能力上的差异，可能使同一政策产生不同效应。

### 5.4 Literature review closing (研究评述)

Three fixed axes, each ending in a gap:
- 从研究视角来看: which relation has not been studied;
- 从研究方法来看: measurement or design weaknesses;
- 从研究情境来看: settings not yet covered.

The gaps must be exactly the contributions claimed in chapter 1, and each must be picked up by
the theory or the hypotheses. A gap left without a hypothesis is a 断裂 that supervisors notice.

### 5.5 Robustness checks: purpose first

为 + purpose，本文 + procedure。
> 为确保研究结论不依赖于特定的权重设定，本文在稳健性检验中采用熵权法重新测度核心变量。

### 5.6 Descriptive or contextual paragraph

1. General thesis.
2. Basis ("这一判断源自一个基本事实：……").
3. The figure, with numerical milestones.
4. Reconciliation of sources if they differ ("两种分期方法相容而非互斥").
5. Link to the design and its limit ("然而，需要指出的是，……仅提供了……的宏观背景").

In a descriptive chapter, describe trends, structure and differences ("what is"), not causes
("why"). Causal explanations belong to the theory or empirical chapters.

## 6. Internal enumeration

- Parallel points inside a paragraph: 第一，……；第二，…… separated by semicolons.
- Links of a mechanism: 第一环节，……；第二环节，……
- Also （1）（2）（3） or 其一 / 其二.
- Comparative subsections carry a label on its own line: （一）……（二）……
- **Enumerating a lot is the norm of the genre.** The connectors file gives the rates.

## 7. Paragraph opening

- Every body paragraph is indented two characters (段前空两格), including a paragraph that
  starts with 表X-Y or 图X-Y when it is prose and not a caption.
- An introductory paragraph under a chapter title is copied if the source has one. Never invent
  one, and never delete an existing one.
