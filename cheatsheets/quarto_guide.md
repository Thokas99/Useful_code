Quarto HTML scientific-report template

Copy the YAML below into the front matter of a .qmd report and adapt the title, subtitle, and section content. Keep only options that suit the project.

Copy-ready YAML

---
title: "Report title"
subtitle: "Short descriptive subtitle"

format:
  html:
    # Built-in light and dark Bootstrap themes.
    theme:
      light: cosmo
      dark: darkly
    respect-user-color-scheme: true

    # Navigation and section numbering.
    toc: true
    toc-title: "Contents"
    toc-depth: 4
    toc-location: right
    number-sections: true
    number-depth: 3
    smooth-scroll: true
    anchor-sections: true

    # Reader-friendly code display.
    code-fold: true
    code-summary: "Show analysis code"
    code-copy: true
    code-overflow: wrap

    # Figure and page layout.
    fig-responsive: true
    embed-resources: true
    page-layout: article
    grid:
      sidebar-width: 250px
      body-width: 1050px
      margin-width: 300px
      gutter-width: 1.5rem

    # Open external links in a new tab.
    link-external-newwindow: true

# Click figures to inspect them at full size.
lightbox:
  match: auto
  effect: fade
  desc-position: bottom
  loop: false

# Quiet, reproducible report output.
execute:
  echo: true
  warning: false
  message: false
  error: false

# Sensible defaults for knitr figures and code blocks.
knitr:
  opts_chunk:
    fig.align: center
    fig.width: 16
    fig.height: 12
    dpi: 300
    out.width: "100%"
    collapse: true
    comment: "#>"
---

Recommended report structure

This report answers [one-sentence biological question].

## Objective and report scope

State the question, cohort, and what the report does not do.

## Analytical Methods

- **Data and preprocessing.** Files, filtering, transformation, and sample matching.
- **Model.** Model type, outcome, predictors, positive/event class, and threshold.
- **Validation.** Training versus validation strategy; state clearly if the model is only applied here.
- **Metrics.** Discrimination, threshold-dependent classification, and probability/calibration measures.

## Cohort preparation

One short paragraph before the data-preparation chunks.

### Software setup

One sentence before the package chunk.

### Data and outcome preparation

One sentence before the import/preprocessing chunk.

### Expression or feature quality check

One sentence before the exploratory figure.

## Model application

### Predicted probabilities and classes

Explain what is produced and how the class call is made.

### Threshold-dependent classification

Introduce the confusion matrix and report what the errors mean.

### ROC discrimination

Explain ROC-AUC as ranking discrimination across thresholds.

### Precision-recall discrimination

Explain PR-AUC as responder-focused performance and show the prevalence baseline.

## Comparative evaluation

State exactly how models differ and interpret differences cautiously.

## Conclusion and limitations

Summarize the observed result, cohort size, class balance, threshold, and uncertainty limits.

Chunk-option patterns

Hide implementation-heavy code while keeping the report readable:

```{r}
#| label: data-preparation
#| echo: false
#| message: false
#| warning: false
```

For a figure, use a semantic label beginning with fig- and add a caption:

```{r}
#| label: fig-roc
#| echo: false
#| message: false
#| warning: false
#| fig-width: 7
#| fig-height: 6
#| fig-cap: "ROC curve for the validated model."

# Existing analysis code goes here unchanged.
```

For a table, use a semantic label beginning with tbl-:

```{r}
#| label: tbl-performance
#| echo: false
#| message: false
#| warning: false
#| tbl-cap: "Model performance in the validation cohort."

# Existing table-producing code goes here unchanged.
```

When code should remain available to readers, leave echo: true and let the global code-fold: true keep it collapsed by default.

Captions and cross-references

Use labels and refer to outputs in the prose:

Figure @fig-roc shows discrimination across probability thresholds.

Table @tbl-performance reports the complete metric set.

Good captions say what is shown, in which cohort, and under which important threshold or baseline. Keep plot titles short; put interpretation in the surrounding prose.

Metric language

Discrimination: ROC-AUC summarizes sensitivity versus false-positive rate across thresholds. PR-AUC summarizes precision versus recall for the positive/event class and should be read against event prevalence.
Classification at one threshold: Accuracy, balanced accuracy, sensitivity/recall, specificity, precision, NPV, F1, kappa, MCC, and the confusion matrix describe the selected classification threshold. A confusion matrix contains TP, TN, FP, and FN.
Probability quality: Brier score measures squared probability error and is sensitive to calibration; lower values are better.
Do not call a model superior from a small numerical difference alone, especially when models are evaluated on the same small validation cohort.

Human-writing rules

Lead each section with what is being done and why.
Use one short paragraph before a major code block; never put a heading directly before code.
Use bullets when several items need to be defined together.
Interpret figures and tables in one or two sentences; do not repeat every number in the caption and prose.
Use consistent terms: miRNA, RNA-seq, responder, non-responder, predicted probability, classification threshold, ROC-AUC, and PR-AUC.
State uncertainty and scope plainly: cohort size, class balance, external validation, missing training details, and lack of confidence intervals when applicable.
Avoid claims not supported by the notebook. Do not invent a train/test split, clinical meaning, or biological mechanism.
Handoff prompt for the next AI agent

Refactor this Quarto notebook into a concise scientific HTML report.

Preserve all analytical code and results exactly:
- do not change statistical methods, formulas, thresholds, filtering, preprocessing,
  splits, object names, numerical results, plotted data, or output paths;
- only change prose, headings, comments, Quarto options, captions, layout, and
  presentation, except for a strictly necessary rendering fix.

Use the attached Quarto YAML template as the design baseline. Read the full notebook
before editing. Add short methods prose, explain the model and validation design,
define the positive/event class, and distinguish discrimination, threshold-dependent
classification, and probability/calibration metrics. Use bullets when several items
must be explained. Add semantic `fig-` and `tbl-` labels, meaningful captions, and
cross-references. Keep interpretations cautious and grounded in the actual outputs.

Render the notebook after editing. Check that the HTML renders, cross-references,
figures, tables, code folding, light/dark themes, and lightbox behavior work. Report
which source files changed and whether the numerical outputs were preserved.

Final checklist

 Read the complete .qmd before editing.
 Confirm the biological question, cohort, outcome, predictors, model, and validation strategy.
 Keep analysis code and results unchanged.
 Add short prose before major sections and one concise interpretation after major outputs.
 Use semantic chunk labels, captions, and cross-references.
 Keep warnings/messages quiet where they add no value.
 Render the report and check for unresolved references or errors.
 Verify the regenerated figures/tables against the pre-edit outputs.
 State any unavailable interactive browser or theme-toggle check honestly.
