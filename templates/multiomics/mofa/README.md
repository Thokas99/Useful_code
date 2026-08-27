# Canonical MOFA2 templates

This folder keeps a compact, reusable MOFA2 workflow for multi-omics factor
analysis. It is a cookbook: modality-specific preparation, likelihood choices,
factor selection and interpretation remain visible, and the pages do not
replace the current MOFA2 documentation.

All four pages are `SOURCE-BACKED WORKFLOW` templates and currently `draft`.

## Workflow

```text
modality-appropriate feature x sample matrices
          |
          v
prepare_views.qmd
          |
          +-- prepared named view list (.qs2) + TSV manifests
          v
fit.qmd
          |
          +-- native trained MOFA2 model (.hdf5) + option TSVs
          v
diagnostics.qmd
          |
          +-- variance, factor and technical-diagnostic TSVs/figures
          v
interpretation.qmd
          |
          +-- factor scores, feature weights and optional associations (TSV)
```

## Template classes and status

- `SOURCE-BACKED WORKFLOW`: substantial implementation exists in the source
  notebooks.
- `validated`, `draft`, `blocked`: the status is stated on every page. These
  pages remain `draft` until the canonical object contract is run on a
  representative dataset.

## Persistence

The prepared named list of R matrices and supporting R objects uses `.qs2`.
The trained MOFA2 model uses the native `.hdf5` file written by
`MOFA2::run_mofa()`; this is an intentional MOFA-specific exception to the
repository-wide R-object rule. Human-readable manifests, options, scores,
weights and associations use TSV.

## Scientific reminders

MOFA2 is unsupervised. Fit it from the omics views, then associate factors with
metadata after training. View transformations, missingness, feature selection,
likelihoods, view scaling and the number of factors are modality/model
decisions, not generic boilerplate. The baseline here matches samples present
in every selected view without automatic imputation; deliberately incomplete
designs require an explicit alternative.

Consult the current MOFA2 tutorials and documentation for incomplete views,
likelihood assumptions, advanced training, MEFISTO, single-cell MOFA and
version-specific options.
