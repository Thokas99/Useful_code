# Quarto HTML scientific-report template

A reusable template for professional, self-contained scientific HTML reports produced from Quarto and R/knitr.

The defaults prioritize:

- a clean light/dark HTML report;
- a navigable, numbered document structure;
- collapsed but recoverable analysis code;
- high-resolution figures;
- semantic figure/table cross-references;
- reproducibility and cautious scientific interpretation;
- a single portable HTML output with embedded render dependencies.

> **Important:** `embed-resources: true` embeds the resources required to render the document (figures, CSS, JavaScript, etc.). It does **not** automatically turn arbitrary linked files such as `.csv`, `.xlsx`, or `.rds` files into downloadable content inside the HTML. A pattern for embedding small supplementary files is provided later in this template.

---

## 1. Copy-ready YAML

Use this as the default front matter for a standalone scientific report.

```yaml
---
title: "Report title"
subtitle: "Short descriptive subtitle"
lang: en

# Optional document metadata.
# author: "Author Name"
# date: today
# date-format: "DD MMMM YYYY"
# keywords:
#   - transcriptomics
#   - biomarker validation
#   - external validation

format:
  html:
    # ── Theme ────────────────────────────────────────────────────────────────
    theme:
      light: cosmo
      dark: darkly
    respect-user-color-scheme: true

    # ── Navigation ───────────────────────────────────────────────────────────
    toc: true
    toc-title: "Contents"
    toc-depth: 4
    toc-location: right
    toc-expand: 2

    number-sections: true
    number-depth: 3
    smooth-scroll: true
    anchor-sections: true

    # ── Code display ─────────────────────────────────────────────────────────
    code-fold: true
    code-summary: "Show analysis code"
    code-copy: true
    code-overflow: wrap
    code-line-numbers: false

    # Optional for R/knitr reports when downlit is installed.
    # code-link: true

    # ── Figures ──────────────────────────────────────────────────────────────
    # Default figure size and resolution: 16 × 12 inches at 300 dpi.
    fig-width: 16
    fig-height: 12
    fig-dpi: 300
    fig-format: png
    fig-align: center
    fig-responsive: true
    fig-cap-location: bottom

    # ── Tables ───────────────────────────────────────────────────────────────
    tbl-cap-location: top
    df-print: paged

    # ── Cross-reference / hover behavior ─────────────────────────────────────
    crossrefs-hover: true
    footnotes-hover: true
    citations-hover: true

    # ── Standalone HTML ──────────────────────────────────────────────────────
    # Embed figures, CSS, JavaScript, and other render resources.
    embed-resources: true

    # MathJax/KaTeX are not embedded by embed-resources alone.
    # Enable this when the report contains mathematical notation.
    self-contained-math: true

    # ── Page layout ──────────────────────────────────────────────────────────
    page-layout: article
    grid:
      sidebar-width: 250px
      body-width: 1050px
      margin-width: 300px
      gutter-width: 1.5rem

    # ── Links ────────────────────────────────────────────────────────────────
    link-external-newwindow: true
    link-external-icon: true

# ── Figure inspection ────────────────────────────────────────────────────────
lightbox:
  match: auto
  effect: fade
  desc-position: bottom
  loop: false

# ── Execution ────────────────────────────────────────────────────────────────
execute:
  echo: true
  warning: false
  message: false
  error: false

# ── knitr defaults ───────────────────────────────────────────────────────────
# Keep only engine-specific display options here. Figure size/resolution is
# defined above with Quarto's document-level figure options.
knitr:
  opts_chunk:
    fig.align: center
    out.width: "100%"
    collapse: true
    comment: "#>"

# ── Cross-reference terminology ──────────────────────────────────────────────
crossref:
  fig-title: "Figure"
  tbl-title: "Table"
  sec-prefix: "Section"
  fig-prefix: "Figure"
  tbl-prefix: "Table"
  ref-hyperlink: true

# ── Bibliography: enable only when the file actually exists ─────────────────
# bibliography: references.bib
# citeproc: true
# link-citations: true
---
```

### Why bibliography support is commented out

Do not keep:

```yaml
bibliography: references.bib
```

unless `references.bib` actually exists at a path Quarto can resolve. Otherwise, the entire render can fail after all computational cells have completed.

---

## 2. Figure-resolution presets

### High-resolution report preset

The default configuration above uses:

```yaml
fig-width: 16
fig-height: 12
fig-dpi: 300
fig-format: png
```

This produces raster figures up to approximately **4800 × 3600 pixels** before HTML scaling, which is a strong default for scientific HTML reports while keeping file size manageable.

### Publication-export preset

When a specific figure needs a higher-resolution raster export, override it locally:

```yaml
fig-width: 16
fig-height: 12
fig-dpi: 600
fig-format: png
```

Use 600 dpi selectively for figures intended for manuscript export rather than as the default for every HTML figure.

### Override only when a figure genuinely needs a different aspect ratio

Do not redefine `fig-width` and `fig-height` on every chunk. That defeats the purpose of a consistent global report layout.

Use local overrides only when necessary:

````markdown
```{r}
#| label: fig-wide-heatmap
#| fig-cap: "Expression heatmap in the validation cohort."
#| fig-width: 16
#| fig-height: 8
#| fig-alt: "Heatmap of standardized expression values across validation samples."

# Plot code.
```
````

---

## 3. Recommended scientific-report structure

```markdown
This report evaluates [one-sentence biological or analytical question].

::: {.callout-note}
## Analysis scope

State explicitly whether this is exploratory analysis, internal validation,
external validation, or application of a previously locked model.
:::

## Objective and report scope

State:

- the biological/clinical question;
- cohort and sample type;
- outcome being predicted or compared;
- whether preprocessing and model parameters are locked;
- what is outside the scope of this report.

## Cohort and data

### Cohort definition

Describe inclusion/exclusion criteria, sample count, outcome classes, and relevant
clinical variables.

### Data preprocessing

Describe filtering, normalization/transformation, feature matching, missing-data
handling, and any batch-related decisions.

### Quality control

Show only QC outputs that influence interpretation or sample inclusion.

## Analytical methods

### Model or statistical procedure

State:

- model/statistical method;
- predictors/features;
- outcome;
- positive/event class;
- decision threshold, if applicable;
- whether tuning or feature selection occurred in this cohort.

### Validation design

Distinguish clearly between:

- model development;
- internal validation;
- held-out testing;
- external validation;
- post hoc exploratory comparison.

### Performance metrics

Separate:

- discrimination metrics;
- threshold-dependent classification metrics;
- probability/calibration metrics.

## Results

### Cohort overview

Present the denominator first: total samples, evaluable samples, class balance,
and any exclusions.

### Primary analysis

Lead with the primary result, then provide the supporting figure/table.

### Secondary or comparative analysis

State exactly how models or groups differ. Do not imply superiority from a small
numerical difference without uncertainty estimates or paired inference.

## Sensitivity analyses

Include only analyses that test robustness to a meaningful analytical choice.

## Discussion

Interpret the result in the context of the validation design and cohort.

## Limitations

State limitations directly: sample size, class imbalance, missing data, absence
of calibration assessment, missing confidence intervals, cohort shift, or
preprocessing differences where applicable.

## Conclusion

Answer the original question in a few sentences without introducing new results.

## Reproducibility {.appendix}

Include session information and, when appropriate, input/output file inventories.
```

---

## 4. Chunk conventions

### Analysis / preparation chunk

Use semantic labels even for non-figure chunks.

````markdown
```{r}
#| label: prepare-validation-data
#| echo: false
#| message: false
#| warning: false

# Existing analysis code.
```
````

Prefer labels that describe the action rather than generic names such as `chunk-1`.

Good:

```text
prepare-validation-data
derive-response-outcome
apply-locked-model
calculate-performance-metrics
```

Avoid:

```text
analysis1
plot2
new_chunk
test
```

---

## 5. Figure pattern

Every figure that is discussed in the prose should have:

1. a unique `fig-` label;
2. a caption;
3. useful alternative text;
4. a prose interpretation outside the caption.

````markdown
```{r}
#| label: fig-validation-roc
#| echo: false
#| message: false
#| warning: false
#| fig-cap: "ROC curve for the locked model in the external validation cohort."
#| fig-alt: "Receiver operating characteristic curve showing sensitivity against false-positive rate across classification thresholds."

# Existing plotting code.
```
````

Reference it as:

```markdown
The model's discrimination across probability thresholds is shown in
@fig-validation-roc.
```

Do **not** write:

```markdown
Figure @fig-validation-roc ...
```

because `@fig-validation-roc` already renders the figure prefix and number.

### Figure-caption rule

A good caption answers:

- **what** is shown;
- **where/in which cohort**;
- **which model/group**;
- **which threshold/baseline**, if the figure depends on one.

Keep interpretation in the surrounding Results prose.

---

## 6. Multi-panel figures

For grouped outputs, use a single parent figure where this improves comparison.

````markdown
```{r}
#| label: fig-model-comparison
#| fig-cap: "Comparison of discrimination for the two prespecified models in the validation cohort."
#| fig-subcap:
#|   - "Full model."
#|   - "Reduced model."
#| layout-ncol: 2
#| echo: false

plot_full
plot_reduced
```
````

Reference the complete comparison with:

```markdown
@fig-model-comparison
```

Use multi-panel figures when panels answer the same question. Do not group unrelated
plots merely to reduce page length.

---

## 7. Table pattern

````markdown
```{r}
#| label: tbl-validation-performance
#| echo: false
#| message: false
#| warning: false
#| tbl-cap: "Performance of the locked model in the external validation cohort."

# Existing table-producing code.
```
````

Reference it as:

```markdown
The complete performance summary is reported in @tbl-validation-performance.
```

### Table design rules

- Put table captions above tables.
- Round displayed values consistently, but do not alter underlying objects.
- Include units in column names where relevant.
- Prefer explicit labels such as `Sensitivity` over cryptic abbreviations when space permits.
- State the positive/event class in either the table or nearby prose.
- Do not hide the denominator or number of evaluable samples.

---

## 8. Cross-reference rules

Quarto figure cross-references require a `fig-` label, and table cross-references
require a `tbl-` label.

Correct:

```yaml
#| label: fig-full-roc
#| fig-cap: "ROC curve for the full model."
```

```yaml
#| label: tbl-performance
#| tbl-cap: "Validation performance metrics."
```

Then:

```markdown
@fig-full-roc
@tbl-performance
```

A chunk label alone is not sufficient for a useful figure/table reference: provide the
corresponding caption as well.

Before delivery, render and search the console output for:

```text
Unable to resolve crossref
```

Treat every unresolved cross-reference as a report defect.

---

## 9. Metric language for model-validation reports

### Discrimination

- **ROC-AUC** summarizes ranking discrimination across thresholds.
- **PR-AUC** summarizes precision versus recall for the positive/event class.
- PR-AUC should be interpreted relative to event prevalence.

### Classification at a fixed threshold

These metrics describe performance at the selected classification threshold:

- accuracy;
- balanced accuracy;
- sensitivity/recall;
- specificity;
- precision/PPV;
- NPV;
- F1 score;
- Cohen's kappa;
- MCC;
- confusion-matrix counts.

Always state the positive/event class and the threshold used.

### Probability quality

- **Brier score** summarizes squared probability error; lower values are better.
- It reflects probability quality and is sensitive to calibration, but it is not a
  substitute for a calibration plot or calibration slope/intercept.

### Model comparison

Avoid:

> Model A performs better than Model B.

when the only evidence is a small difference in point estimates from the same small
validation cohort.

Prefer:

> Model A had a numerically higher ROC-AUC in this cohort; uncertainty around the
> difference was not estimated.

---

## 10. Results-writing pattern

For every major result:

1. **Question:** what is being evaluated?
2. **Result:** what was observed?
3. **Evidence:** which figure/table supports it?
4. **Scope:** what should not be inferred?

Example structure:

```markdown
The locked classifier separated responders from non-responders with moderate
discrimination in the external cohort (@fig-validation-roc). Performance at the
prespecified classification threshold is summarized in
@tbl-validation-performance. Because the validation cohort is limited in size,
small differences between candidate models should be treated as descriptive
rather than definitive.
```

Do not mechanically repeat every number from a table in the prose.

---

## 11. Callouts

Use callouts sparingly for information readers should not miss.

### Analysis scope

```markdown
::: {.callout-note}
## Analysis scope

This cohort is used only for external application of the locked model.
No feature selection, threshold optimization, or model refitting is performed.
:::
```

### Important limitation

```markdown
::: {.callout-warning}
## Interpretation

Performance estimates are based on a limited validation cohort and should be
interpreted with corresponding uncertainty.
:::
```

Avoid turning ordinary results into callouts.

---

## 12. Model-comparison tabs

Tabs are useful for secondary detail:

```markdown
::: {.panel-tabset}

### Full model

Content for the full model.

### Reduced model

Content for the reduced model.

:::
```

Do not hide the primary result or primary conclusion inside a tab. A reader should
understand the main finding without opening interactive elements.

---

## 13. Reproducibility appendix

Add a reproducibility section at the end of the report.

````markdown
## Reproducibility {.appendix}

### R session

```{r}
#| label: session-information
#| echo: false
#| results: markup

sessionInfo()
```
````

For analyses that contain stochastic steps, set and report a reproducible seed where
scientifically appropriate. Do not add a seed merely to make a fundamentally
non-deterministic external process look deterministic.

Also consider recording:

- input filenames;
- model artifact filenames;
- package versions;
- analysis date;
- output filenames;
- Git commit hash when the project is under version control.

---

## 14. Optional bibliography block

Enable only when a bibliography exists.

```yaml
bibliography: references.bib
citeproc: true
link-citations: true
```

Then cite references with standard Quarto/Pandoc citation syntax:

```markdown
Previous work has shown ... [@citation-key].
```

Do not include an empty or nonexistent bibliography path in a reusable template.

---

## 15. Embedding small supplementary files inside the HTML

`embed-resources: true` handles resources needed to render the report, but an ordinary
link to a local `.csv`, `.xlsx`, `.tsv`, or `.rds` file remains a file link.

For **small** supplementary files that must travel inside the single HTML document,
an explicit `data:` URI can be created.

Example in R:

````markdown
```{r}
#| label: embed-small-supplement
#| echo: false
#| results: asis

embed_download <- function(path,
                           label = basename(path),
                           mime = "application/octet-stream") {
  stopifnot(file.exists(path))

  if (!requireNamespace("base64enc", quietly = TRUE)) {
    stop("Package 'base64enc' is required to embed supplementary files.")
  }

  if (!requireNamespace("htmltools", quietly = TRUE)) {
    stop("Package 'htmltools' is required to embed supplementary files.")
  }

  encoded <- base64enc::base64encode(path)
  safe_label <- htmltools::htmlEscape(label)
  safe_name <- htmltools::htmlEscape(basename(path), attribute = TRUE)

  cat(
    sprintf(
      '<a download="%s" href="data:%s;base64,%s">%s</a>',
      safe_name,
      mime,
      encoded,
      safe_label
    )
  )
}

# Example:
# embed_download(
#   "supplementary_metrics.tsv",
#   label = "Download supplementary metrics",
#   mime = "text/tab-separated-values"
# )
```
````

Use this only for relatively small files. Large embedded attachments can make the HTML
unnecessarily large and slow to open.

For tables that readers only need to inspect, prefer rendering the table directly in
the report rather than embedding a separate downloadable file.

---

## 16. Human-writing rules

- Lead each major section with **what is being done and why**.
- Do not place a heading directly above a code block without explanatory prose.
- Keep Methods descriptive and Results interpretive.
- Separate observation from interpretation.
- Define the positive/event class once and use the same terminology throughout.
- Use consistent scientific notation and terminology.
- Report denominators, not only percentages.
- State cohort size and class balance before discussing performance.
- Distinguish external validation from model development.
- Distinguish discrimination from fixed-threshold classification.
- Do not use causal language for observational associations.
- Do not invent biological explanations that were not tested.
- Do not claim model superiority from tiny point-estimate differences alone.
- Do not describe a model as "validated" if the cohort was used to tune features,
  thresholds, hyperparameters, or preprocessing decisions.
- Put interpretation in prose, not inside oversized plot titles.
- Prefer one or two focused sentences after each major output.
- Remove redundant code comments that merely restate the code.

---

## 17. Naming conventions

Use stable, semantic identifiers.

### Figures

```text
fig-cohort-overview
fig-expression-qc
fig-full-model-roc
fig-full-model-pr
fig-full-model-confusion
fig-model-comparison
```

### Tables

```text
tbl-cohort-characteristics
tbl-full-model-predictions
tbl-performance-summary
tbl-model-comparison
```

### Non-output chunks

```text
setup-packages
read-input-data
prepare-outcome
construct-predictor-matrix
apply-locked-model
calculate-metrics
```

Do not rename analytical R objects solely for cosmetic reasons during a presentation
refactor unless explicitly requested.

---

## 18. Render command

For paths containing spaces, quote the complete path:

```bash
quarto render "/path/with spaces/report.qmd" --to html
```

A successful report build should end with the generated `.html` path and no unresolved
cross-reference warnings.

---

## 19. Render QA

After rendering, verify all of the following.

### Structural QA

- [ ] HTML renders without errors.
- [ ] No `Unable to resolve crossref` warnings.
- [ ] Table of contents matches the actual report hierarchy.
- [ ] Section numbering is sensible.
- [ ] Light and dark themes both remain readable.
- [ ] Code folding and code copy work.
- [ ] Lightbox opens figures correctly.
- [ ] External links behave as expected.

### Scientific QA

- [ ] Cohort denominator and class balance are stated.
- [ ] Positive/event class is explicit.
- [ ] Model-development and validation data are clearly separated.
- [ ] Preprocessing applied to validation data is described accurately.
- [ ] Decision threshold is stated where threshold-dependent metrics are reported.
- [ ] ROC-AUC and PR-AUC are not confused with fixed-threshold classification metrics.
- [ ] Brier score is not described as a complete calibration analysis.
- [ ] Model comparisons are appropriately cautious.
- [ ] Limitations match the actual analysis.

### Figure/table QA

- [ ] Every referenced figure has a `fig-` label and `fig-cap`.
- [ ] Every referenced table has a `tbl-` label and `tbl-cap`.
- [ ] Important figures have meaningful `fig-alt` text.
- [ ] Captions identify cohort/model/threshold where needed.
- [ ] Displayed rounding does not change underlying results.
- [ ] Plot text remains legible in both light and dark themes.
- [ ] The final HTML file size is reasonable for the intended delivery method.

### Reproducibility QA

- [ ] Input files can be identified.
- [ ] Model artifacts can be identified.
- [ ] Package/session information is recorded.
- [ ] Randomness is controlled where appropriate.
- [ ] Absolute machine-specific paths are either intentional or clearly documented.
- [ ] Numerical outputs were not altered during presentation refactoring.

---

## 20. Handoff prompt for Codex / another coding agent

```text
Refactor the Quarto notebook in this project into a professional, self-contained
scientific HTML report.

FIRST:
- read the complete .qmd file before making edits;
- identify the biological/analytical question, cohort, outcome, predictors/features,
  model/statistical method, positive/event class, classification threshold,
  validation design, and all primary outputs;
- identify all existing figure/table references and any render warnings.

HARD CONSTRAINT — preserve the analysis:
- do not change statistical methods;
- do not change formulas;
- do not change filtering or preprocessing logic;
- do not change normalization/transformation logic;
- do not change train/test/external-validation membership;
- do not change model parameters or thresholds;
- do not change feature sets;
- do not rename analytical objects unless a rendering fix strictly requires it;
- do not change plotted data;
- do not change numerical results;
- do not change output paths unless explicitly requested.

You MAY improve:
- YAML / Quarto options;
- section hierarchy;
- prose;
- code comments;
- captions;
- semantic chunk labels;
- cross-references;
- callouts;
- table presentation;
- figure presentation;
- accessibility text;
- reproducibility/session-information sections.

Use the attached scientific-report template as the design baseline.

REPORT REQUIREMENTS:
1. Produce one self-contained HTML report with `embed-resources: true`.
2. Use the configured light/dark themes.
3. Keep analysis code available but folded by default.
4. Use semantic `fig-` and `tbl-` labels.
5. Give every referenced figure/table a meaningful caption.
6. Add useful `fig-alt` text to important figures.
7. Cross-reference figures and tables from the prose.
8. Explain the validation design precisely.
9. Define the positive/event class and classification threshold.
10. Distinguish:
    - discrimination;
    - threshold-dependent classification;
    - probability/calibration metrics.
11. Keep conclusions proportional to cohort size and uncertainty.
12. Do not invent biological mechanisms, clinical implications, or training details.
13. Add a short reproducibility appendix with `sessionInfo()` unless the notebook
    already contains an equivalent section.
14. Do not enable a bibliography path unless the bibliography file exists.

FIGURES:
- default to 16 × 12 inches at 300 dpi unless the notebook explicitly requires a
  different aspect ratio or higher-resolution export for a specific figure;
- do not locally override figure dimensions without a clear layout reason;
- keep HTML display responsive;
- verify labels, legends, and annotations remain legible.

RENDER AND VALIDATE:
- render the complete notebook after editing;
- fix presentation-layer render problems without changing the scientific analysis;
- check for unresolved cross-references;
- check tables, figures, light/dark themes, code folding, and lightbox behavior;
- compare key numerical outputs before and after the refactor;
- report the final HTML path;
- report source files changed;
- report any render warnings that remain;
- state explicitly whether the analytical results were preserved.
```

---

## 21. Minimal final checklist

Before sharing the report:

- [ ] Render succeeds.
- [ ] No unresolved cross-references.
- [ ] No missing bibliography/resource files.
- [ ] Scientific question and validation design are explicit.
- [ ] Positive/event class and threshold are explicit.
- [ ] Figures/tables are captioned and referenced.
- [ ] Important figures include alt text.
- [ ] Conclusions reflect uncertainty and sample size.
- [ ] Session information is present.
- [ ] Analytical code and numerical results are unchanged.
- [ ] Self-contained HTML opens without project-side resource folders.
- [ ] Final HTML size is acceptable.
