# Bulk RNA-seq templates

This folder contains compact, source-backed reminders for count-based bulk
RNA-seq import, QC, normalization, differential expression, ranked enrichment,
and sample-level gene-set scoring.

## Suggested order

```text
tximport_edger.qmd
        ↓
qc_normalization_edger.qmd
        ↓
differential_expression_edger.qmd
        ↓
gsea.qmd

normalized expression matrix
        ├── singscore.qmd
        └── gsva.qmd
```

The scoring branches are optional and do not require differential expression.

## Template classes and status

`SOURCE-BACKED WORKFLOW` preserves a substantial implementation from the
source notebooks. `API / TUTORIAL REMINDER` is intentionally shorter when no
complete reusable implementation was found. Every template currently has
status `draft`: syntax and small code-path checks are not scientific
validation.

## Persistence

- R analytical objects: qs2;
- human-readable matrices and result tables: TSV.

The templates are a personal analytical cookbook. They preserve method-specific
reasoning but do not replace the current tximport, edgeR, clusterProfiler,
singscore, GSVA, or Bioconductor documentation.

## What each method means

- `tximport_edger`: construct a gene-level edgeR count-model object;
- `qc_normalization_edger`: filter, normalize library composition, and inspect
  sample quality;
- `differential_expression_edger`: fit an edgeR count model for a declared
  design and contrast;
- `gsea`: test a ranked gene-level statistic against gene sets;
- `singscore`: score a directional signature per sample using within-sample
  ranks;
- `gsva`: estimate per-sample gene-set activity from an expression matrix.

These are separate analytical questions and should not be collapsed into one
generic “RNA-seq analysis” workflow.
