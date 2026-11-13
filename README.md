# SanQ Chinese Article Composer

**English** · [Español](#español)

Created by **SanQ**.

A Claude skill that translates and revises academic texts (theses, journal articles, research
reports) from any language into academic Chinese, written in the register of Chinese theses and
journal papers.

## What it does

- **Workflow.** It identifies the discipline and the document profile, builds a terminology
  glossary before translating, translates section by section, checks each section against core
  rules, runs a verifier, and delivers a report of its decisions.
- **Register, not only fidelity.** It targets the most common defect of academic translations
  into Chinese: correct Chinese words in the syntax of the source language. Its rules come from
  real corrections by Chinese supervisors and native reviewers. Its reference rates come from a
  measured corpus of Chinese academic prose.
- **It learns your field first.**
  - It reads your text and identifies the field, the method and the central terms.
  - It searches open Chinese sources of that field: journals of professional associations and
    universities, national open-access platforms, open-access publishers, journals' author
    guidelines.
  - From those sources it harvests the authors' own 关键词/Keywords pairs and first-mention
    brackets 中文（English）, with `scripts/harvest_terms.py`.
  - It adopts the field's conventions, for example how medicine reports significance as against
    economics.
  - Chinese concepts written in pinyin or as calques (Qi, acupoint names, hukou…) are
    back-translated to their canonical form.
- **Discipline glossaries.**
  - Terms are also checked in 术语在线 (termonline.cn), UNTERM, the IMF TermBase and CNKI usage.
  - Each term is recorded with its source and evidence.
  - Untested terms are marked for human review, never invented.
- **Document profiles.** `thesis`, `article` and `report`. Chinese thesis format applies only to
  `thesis`: chapter headings, front matter, three-line tables, 注：/资料来源：, numbered equations,
  GB/T 7714. University norms are asked for or loaded as optional profiles, never assumed.
- **Golden rules.**
  - Association is never turned into causation.
  - No bibliographic data or figures are invented.
  - Text written by a human reviewer is kept literally.
  - Every external suggestion is triaged with a written reason.
- **Verifier** (`scripts/verify_zh.py`, standard-library Python).
  - It checks fidelity (figures, citations, paragraph count), register (calques, connectives,
    sentence length, metatext), typography and format.
  - Thresholds are configurable and documented.
  - It can be recalibrated on a corpus of your own field.

## Installation

**Claude Code**
- Copy the `sanq-chinese-article-composer` folder into `~/.claude/skills/` (all your projects) or into
  `.claude/skills/` inside a project.
- Restart Claude Code if the `skills` folder did not exist before.

```
git clone https://github.com/sebasticast-create/sanq-chinese-article-composer.git
cp -r sanq-chinese-article-composer/sanq-chinese-article-composer ~/.claude/skills/
```

Or install it as a plugin, inside Claude Code:

```
/plugin marketplace add sebasticast-create/sanq-chinese-article-composer
/plugin install sanq-chinese-article-composer@sanq
```

**claude.ai** (paid plans with code execution enabled)
1. Make a ZIP that contains the `sanq-chinese-article-composer` folder itself, not its loose files.
2. Open Settings → Capabilities (named Features in some versions) → Skills → Upload skill.
3. Enable the skill.

## Example

> Translate `chapter2.md` into academic Chinese for a master's thesis in economics. Use my
> glossary `terms.csv`. The university norm is attached.

Claude will:
1. ask for the document profile if it is unclear;
2. extend your glossary with sourced terms;
3. translate section by section;
4. run `verify_zh.py`;
5. return the translation with its verifier output and a decision report.

Short input and output examples are in [`examples/`](examples/):
- an English economics paragraph;
- a Spanish urban-ecology paragraph;
- a Spanish traditional Chinese medicine paragraph, with the full field discovery (open
  sources, harvested terms, attestation counts).

Each example comes with its source, translation, glossary, verifier output and report.

Running the verifier yourself:

```
python sanq-chinese-article-composer/scripts/verify_zh.py translation.md --source source.md \
       --glossary glossary.csv --profile article
```

## Limitations

- **The default figures come from economics.** They were measured on two master's theses and six
  journal articles.
  - Field discovery adapts terms and conventions to other fields.
  - Recalibrating the thresholds needs at least about 20,000 characters of running text from
    the field; abstracts alone are not enough.
- **Some sources cannot be read automatically.** CNKI search asks for a captcha, and some sites
  block scripts. The skill uses open sources that respond and lists the ones it tried.
- **Some terminology sources need a browser.** 术语在线, UNTERM and the CNKI 翻译助手 render their
  results with JavaScript; 术语在线's API requires login. Without a browser tool, Claude marks
  those checks as pending and asks you to confirm.
- **The verifier is mechanical.** It does not judge meaning or naturalness, and short texts are
  measured but not judged on rates. A native academic reader remains necessary.
- **Profiles are examples.** The institution profile included is an example, recorded by a
  student, and not an official document. Journal requirements vary; the skill does not invent
  them.
- **The example glossary has not been re-verified.** Its generic economics and trade terms were
  not re-checked term by term on 术语在线 for this release.

## License

MIT © 2026 SanQ. See [LICENSE](LICENSE). You may use, modify and share this skill freely; the license asks you to keep the copyright notice, which credits SanQ.

---

## Español

Creada por **SanQ**.

Una skill de Claude que traduce y revisa textos académicos (tesis, artículos, informes de
investigación) de cualquier idioma al chino académico, con el registro de las tesis y los
artículos chinos.

### Qué hace

- **Flujo de trabajo.** Identifica la disciplina y el tipo de documento, construye un glosario
  antes de traducir, traduce por secciones, comprueba cada sección contra las reglas núcleo,
  pasa un verificador y entrega un informe de decisiones.
- **Registro, no solo fidelidad.** Ataca el defecto más común de las traducciones académicas al
  chino: palabras chinas correctas con la sintaxis del idioma de origen. Sus reglas salen de
  correcciones reales de tutores chinos y de revisores nativos. Sus cifras de referencia salen
  de un corpus medido de prosa académica china.
- **Primero aprende la disciplina.**
  - Lee el texto e identifica la disciplina, el método y los términos centrales.
  - Busca fuentes chinas abiertas de esa disciplina: revistas de asociaciones profesionales y
    de universidades, plataformas nacionales de acceso abierto, editoriales de acceso abierto,
    normas para autores de las revistas.
  - De esas fuentes extrae los pares 关键词/Keywords de los propios autores y los paréntesis de
    primera mención 中文（English）, con `scripts/harvest_terms.py`.
  - Adopta las convenciones del campo, por ejemplo cómo informa la significación la medicina
    frente a la economía.
  - Los conceptos chinos escritos en pinyin o calcados (Qi, nombres de puntos de acupuntura,
    hukou…) se devuelven a su forma canónica.
- **Glosarios por disciplina.**
  - Comprueba además los términos en 术语在线 (termonline.cn), UNTERM, el IMF TermBase y en el
    uso atestiguado en CNKI.
  - Registra cada término con fuente y evidencia.
  - Si no hay evidencia, marca el término para revisión humana y no lo inventa.
- **Perfiles de documento.** `thesis`, `article` y `report`. El formato de tesis china solo se
  activa con `thesis`: títulos, parte inicial, tablas de tres líneas, 注：/资料来源：, ecuaciones
  numeradas, GB/T 7714. La norma de una universidad se pregunta o se carga como perfil opcional,
  nunca se asume.
- **Reglas de oro.**
  - Asociación no es causalidad.
  - No se inventan datos bibliográficos ni cifras.
  - El texto de un revisor humano se conserva literal.
  - Cada sugerencia externa se acepta o se rechaza con un motivo escrito.
- **Verificador** (`scripts/verify_zh.py`, Python sin dependencias).
  - Comprueba fidelidad (cifras, citas, número de párrafos), registro (calcos, conectores,
    longitud de oración, metatexto), tipografía y formato.
  - Los umbrales son configurables y están documentados.
  - Se puede recalibrar con un corpus de la propia disciplina.

### Instalación

**Claude Code**
- Copie la carpeta `sanq-chinese-article-composer` en `~/.claude/skills/` (para todos sus proyectos) o
  en `.claude/skills/` dentro de un proyecto.
- Reinicie Claude Code si la carpeta `skills` no existía.

```
git clone https://github.com/sebasticast-create/sanq-chinese-article-composer.git
cp -r sanq-chinese-article-composer/sanq-chinese-article-composer ~/.claude/skills/
```

O instálela como plugin, dentro de Claude Code:

```
/plugin marketplace add sebasticast-create/sanq-chinese-article-composer
/plugin install sanq-chinese-article-composer@sanq
```

**claude.ai** (planes de pago, con ejecución de código activada)
1. Haga un ZIP que contenga la carpeta `sanq-chinese-article-composer`, no sus archivos sueltos.
2. Abra Configuración → Capacidades (en algunas versiones, Funciones) → Skills → Subir skill.
3. Active la skill.

### Ejemplo de uso

> Traduce `capitulo2.md` al chino académico para una tesis de máster en economía. Usa mi
> glosario `terminos.csv`. Adjunto la norma de la universidad.

Claude:
1. pide el tipo de documento si no está claro;
2. amplía el glosario con términos documentados;
3. traduce por secciones;
4. pasa `verify_zh.py`;
5. devuelve la traducción con la salida del verificador y un informe de decisiones.

En [`examples/`](examples/) hay ejemplos breves de entrada y salida:
- un párrafo de economía en inglés;
- un párrafo de ecología urbana en español;
- un párrafo de medicina china en español, con el descubrimiento completo de la disciplina
  (fuentes abiertas, términos extraídos, recuentos de atestiguación).

Cada uno trae su original, su traducción, su glosario, la salida del verificador y el informe.

### Limitaciones

- **Las cifras por defecto vienen de la economía.** Se midieron sobre dos tesis de máster y seis
  artículos.
  - El descubrimiento de la disciplina adapta los términos y las convenciones a otros campos.
  - Recalibrar los umbrales exige unos 20.000 caracteres de texto corrido del campo; los
    resúmenes solos no bastan.
- **Algunas fuentes no se pueden leer de forma automática.** La búsqueda de CNKI pide captcha y
  algunos sitios bloquean los scripts. La skill usa las fuentes abiertas que responden y dice
  cuáles probó.
- **Algunas fuentes de terminología necesitan un navegador.** 术语在线, UNTERM y el CNKI 翻译助手
  muestran sus resultados con JavaScript, y la API de 术语在线 pide iniciar sesión. Sin un navegador,
  Claude deja esas comprobaciones como pendientes y pide confirmación.
- **El verificador es mecánico.** No juzga el sentido ni la naturalidad, y en textos cortos mide
  las tasas pero no las juzga. Hace falta un lector académico nativo.
- **Los perfiles son ejemplos.** El perfil de institución incluido lo registró un estudiante y no
  es un documento oficial. Las normas de las revistas varían, y la skill no las inventa.
- **El glosario de ejemplo no se ha vuelto a verificar.** Sus términos genéricos de economía y
  comercio no se han comprobado uno a uno en 术语在线 para esta versión.

### Licencia

MIT © 2026 SanQ. Véase [LICENSE](LICENSE). Puede usar, modificar y compartir esta skill libremente; la licencia pide conservar el aviso de copyright, que da el crédito a SanQ.
