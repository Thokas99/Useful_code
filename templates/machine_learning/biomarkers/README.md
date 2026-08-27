# Biomarker classification templates

## Suggested order

```text
binary_classification_brglm2.qmd
        ↓ frozen qs2/TSV outputs
model_reporting.qmd
```

The classifier preserves the source-backed bias-reduced logistic-regression
workflow, including resampling-time feature selection, threshold tuning,
held-out evaluation, and feature stability. The reporting notebook reads
frozen outputs and does not refit the model.

Both pages are `SOURCE-BACKED WORKFLOW` and `draft`. R model bundles use qs2;
predictions, metrics, stability tables, and reporting inputs use TSV.
