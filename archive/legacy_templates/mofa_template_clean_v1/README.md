# Legacy MOFA scaffold

This project-shaped template is retained for provenance. Use the active
[MOFA2 guide](../../../templates/multiomics/mofa/guide.qmd) for new analyses.

The notebooks prepare matched assay views, score a configured signature, fit a
MOFA2 model, and export factors, weights, and summaries. They contain no cohort
data. Replace the project identifiers and input contracts before use; preserve
the chosen transformations, likelihoods, feature filters, package versions,
and model settings with the output.

The scaffold's ten-factor defaults differ from the project-specific TCGA model.
See [the source inventory](archive_notes/MOFA_code_inventory.md) for the
historical mapping and project decisions.
