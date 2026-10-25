# 07 Format by document profile

Three profiles. Rules 1 to 6 of `SKILL.md` and files `01` to `06` apply to all of them; this file
adds what is specific.

| Profile | Activates |
|---|---|
| `thesis` | Chinese thesis structure, heading numbering, front matter, three-line tables, 注：/资料来源：, numbered equations, GB/T 7714 |
| `article` | Abstract and keywords, journal sections, tables and figures with source lines; **the target journal's 投稿须知 overrides everything** |
| `report` | Hierarchy of headings of Chinese reports, tables and figures with sources; no thesis front matter |

**Never assume an institution's norm.** Ask the user for it, or load an institution profile. An
example is in `profiles/swufe_example.md`; copy it for another university or journal. When the
norm is unknown, use the general conventions below and list in the report what must be checked
against the norm.

---

## 1. Profile `thesis`

### 1.1 Pieces and order

Typical order of a Chinese master's thesis (confirm with the institution):

1. 封面 / 扉页: classification number, security level, U.D.C., titles in Chinese and English,
   author, student number, programme, supervisor, date. The cover of a draft thesis says
   研究生学位论文, not 开题报告.
2. 原创性及知识产权声明.
3. 摘要 + 关键词.
4. Abstract + Keywords.
5. 目录.
6. Chapters.
7. 参考文献.
8. 附录, if needed (e.g. 附录 术语表).
9. 致谢.

Rules for these pieces:
- 关键词： and Keywords: are in bold, without indentation. Keywords are separated by ；.
- Pages before chapter 1 are numbered in Roman numerals; Arabic numbering starts at 1 with
  chapter 1. The cover and the 目录 itself are not listed in the 目录.
- Some programmes put the Abstract before the 摘要, or a glossary before the abstracts. Follow the
  model document the supervisor approved.

### 1.2 Skeleton and proportions

A frequent six-chapter skeleton:

| Chapter | Typical titles |
|---|---|
| 1 | 绪论 / 引言 |
| 2 | 文献综述 / 相关概念及文献综述 |
| 3 | 理论基础与研究假设 |
| 4 | 研究设计 / 现状分析 |
| 5 | 实证分析 / 回归结果及机制检验 |
| 6 | 结论与政策建议 |

- The empirical chapter takes roughly 40 to 45% of the body.
- Chapter 3 is often 3.1 理论基础, with one subsection per named theory (……理论), followed by
  3.2 研究假设.
- Each theory ends with its implication for the empirical design.

### 1.3 Headings

- **Numbering:**
  - many Chinese university norms use **「1.绪论」, 1.1, 1.1.1**, then （一）（二）（三） on its
    own line;
  - others use 第一章 / 第1章.
  - **Follow the institution's annex or the supervisor's model.**
  - In the prose, chapters are named with Chinese numerals: 第四章.
- **Headings are short noun phrases.** Remove explanatory subtitles after a colon at levels 2
  and 3:
  - 5.3.1 效应的轨迹：事件研究 → 5.3.1 事件研究;
  - 3.1.2 技术的国际扩散及其指标 → 3.1.2 技术扩散与吸收能力理论.
  - A chapter title may keep a colon. A （一） label may name the axis of comparison
    (（一）与A的比较：开放型 vs 内向型).
- **Page layout:** each chapter starts on a new page with a centred title; 摘 要, 参考文献 and
  致谢 are centred too.
- **In Word:**
  - Every heading uses a real heading style (Heading 1/2/3), including unnumbered pieces and
    unnumbered subheadings that must appear in the 目录. Bold text is not a heading: it does not
    enter the table of contents.
  - The 目录 is generated from the styles and updated (F9) before delivery. Check by eye that
    every chapter is listed.
  - Headings are black. Inherited Word styles are blue by default and must be overridden.

### 1.4 Typography in Word (when the norm says nothing else)

- Body text, tables and references:
  - Latin script: Times New Roman (`w:ascii` / `w:hAnsi`);
  - Chinese: 宋体 SimSun (`w:eastAsia`).
- Headings: Times New Roman + 黑体 SimHei.
- Declare the two fonts separately: SimSun for everything sets Latin text with full-width-looking
  glyphs.
- Equations: Cambria Math.
- Variable names in the body font, not monospace.
- No colours or tracked changes in the delivered file.

### 1.5 Tables

- **Title above the table:** 表N-M␣title.
  - Numbered by chapter and consecutive (表5-1, 表5-2…). Renumber after moving or splitting
    tables.
  - The title is a short noun phrase (≤ 45 characters is a good limit), without 。, and without
    「被解释变量：」, sample or period. These go in the header row or the note.
  - 表5-4 事件研究，分样本，2010至2019年 → 表5-4 事件研究估计结果.
- **Three-line table (三线表):** top rule, rule under the header, bottom rule.
  - No vertical lines, no shading of the header.
  - Table centred, body in a smaller size than the text.
  - Same rows and columns as the source; double headers keep both lines.
- **Under the table:**
  - 注：…… with the asterisk convention and the type of standard errors. Number it 1. 2. 3. (or
    ①②③) only when the note covers three or more distinct aspects. Join sentences on the same
    aspect with a comma; separate aspects with a semicolon; put the significance convention last.
  - 资料来源：…… on its own line, e.g. 资料来源：作者根据……数据整理/计算。
- **Every table has its own title and number.** A block of results without a title (e.g.
  sub-samples printed one after another) is either split into numbered tables or turned into
  grouped columns.
- **Regression tables, uniform across the thesis:**
  - variables by their short name;
  - coefficient with asterisks, standard error in parentheses below;
  - **all controls listed one by one**, not "控制变量：是";
  - 常数项 when the estimator returns one (do not write 常数项被固定效应吸收 if a constant can be
    reported);
  - closing rows 观测值, number of units if relevant, one row per set of fixed effects with 是/否;
  - the same closing rows in every table;
  - note such as 注：***、**、*分别表示在1%、5%、10%的水平上显著，括号内为聚类稳健标准误。
- **Repeated categories in a column** (phase, variable type) go in a vertically merged cell.
- **Descriptive tables list only the variables that enter the models.**
- **Variable definition table, four columns:** 变量类型 / 变量名称 / 变量符号 / 变量测度. It is the
  single reference for names throughout the thesis.
- **Long tables** continue with 续表 and the same number.

### 1.6 Figures

- **Under the figure, on separate lines:**
  1. 图N-M␣short title;
  2. 注：…… (abbreviations, reference lines, shading, base of an index);
  3. 资料来源：……
- No explanations in the title. No production notes ("labels are in Chinese", "descriptive
  figure, no causal claim").
- The conceptual explanation of a diagram goes in the body, not in the caption.
- **Caption vs prose:**
  - a caption has a space after the number: 图4-3 出口结构;
  - a body paragraph that starts by naming the figure has no space, is indented and not centred:
    图4-3显示……
- Figure labels use the same terms as the section titles. Chinese fonts in figures: e.g. Noto
  Sans CJK SC / Source Han Sans SC.

### 1.7 Equations

- Numbered: (1), (2)…
- In Word: native equations (OMML), never visible LaTeX or images.
- Right after each equation, a 其中， paragraph defines every symbol with exactly the notation of
  the equation, with real subscripts and superscripts, separated by semicolons:
  > 其中，Y_it 为地区 i 在年份 t 的被解释变量；μ_i 为地区固定效应；λ_t 为年份固定效应；ε_it 为随机误差项。
- The expected sign of the coefficient of interest is stated before the results.
- Each variable has one short name in formulas, text and tables.

### 1.8 References

- **GB/T 7714** (the current edition, GB/T 7714-2015, unless the institution says otherwise),
  numbered [1]…[n].
- Order (Chinese sources first, or a single sequence by order of citation) follows the norm.
- **Never add a bibliographic detail that is not in the source:** no invented pages, issue
  numbers, DOIs or publishers.
- If the source bibliography is in another style, either keep it as is and translate only the
  heading (参考文献), or convert it to GB/T 7714 with the data available, flagging missing fields.
  Do not translate titles of foreign works.
- Separate entries that a conversion merged.

### 1.9 Structural conventions of the genre

- **Chapter 1:** the roadmap goes chapter by chapter, describing tasks, never results.
- **Chapter 2:** ends in 研究评述 (see `02`, 5.4). Its gaps are picked up by the hypotheses.
- **Literature on mechanisms** sits in the review. The hypothesis section uses it; it does not
  repeat it.
- **A descriptive chapter** describes; it neither attributes causes nor tests mechanisms. Its
  chronology table lists events without evaluation, and the chapter closes with 本章小结 listing
  the descriptive findings.
- **Empirical chapter order:**
  1. design (identification and model, variables, sample and data sources);
  2. descriptive statistics and correlation / VIF;
  3. baseline results, then event study and parallel trends (with p-values and the joint test of
     pre-period coefficients);
  4. mechanisms;
  5. robustness (alternative dependent variable, estimator, sample, window, stepwise controls,
     comparison group, placebo, leave-one-out);
  6. heterogeneity.
- **Each content appears once.** Overlapping sections are merged where they belong.
- **致谢** is the only personal, literary piece.

---

## 2. Profile `article`

- **Follow the target journal's 投稿须知 (author guidelines)** for everything below: they vary.
  Do not invent requirements; list the ones you could not verify.
- **Usual pieces:**
  - 题目;
  - 摘要, often structured or with the moves 目的/方法/结果/结论, in one paragraph;
  - 关键词, separated by ；;
  - 中图分类号 and 文献标识码 when the journal asks;
  - sections (一、引言 / 1 引言, following the journal);
  - 参考文献;
  - often an English title and abstract.
- Tables and figures: as in the thesis profile, unless the journal differs (numbering is usually
  global, 表1, 表2, not by chapter).
- No thesis front matter, no 本章小结, no chapter roadmap.
- Literature review shorter; same "one author, one contribution" form.

## 3. Profile `report`

- **Heading hierarchy** of Chinese reports and official documents: 一、 → （一） → 1. → （1）.
  This is the hierarchy set by GB/T 9704 for official documents; confirm whether the client wants
  it or a decimal numbering.
- Executive summary first when the source has one.
- Tables and figures with title, 注： and 资料来源：.
- Policy recommendations open with programmatic verbs (`01`).
- Same rules on association, numbers and terminology.
