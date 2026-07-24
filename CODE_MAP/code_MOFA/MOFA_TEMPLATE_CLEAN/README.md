# MOFA_TEMPLATE_CLEAN

This folder is the distilled notebook-first MOFA template built from the live notebooks in `code_MOFA/`.

## Notebook order

1. `00_project_setup.qmd`
2. `01_multiomics_input_prep.qmd`
3. `02_signature_scoring.qmd`
4. `03_mofa_model.qmd`
   This includes factor heatmaps, per-view top-weight heatmaps, and the group-wise median or mutation-frequency difference exports that sit at the center of the analysis.

## Shared conventions

- Read matched matrices from `input/tables/` and save model artifacts under `output/`.
- Keep assay-specific cleanup, score definitions, and biological interpretation inline in notebooks.
- Source only repetitive mechanical helpers from `helpers/helpers_from_MOFA.R`.

## Object contracts

- `input/tables/PROJECT_ID_matched_multiomics_manifest.tsv`
- `output/tables/PROJECT_ID_scored_metadata.tsv`
- `output/objects/PROJECT_ID_mofa_input.qs2`
- `output/objects/PROJECT_ID_mofa_model.hdf5`
- `output/tables/PROJECT_ID_mofa_factors.tsv`
- `output/tables/PROJECT_ID_factor_score_associations.tsv`
- `output/tables/mofa_group_summaries/`
- `output/figures/mofa_heatmaps/`

## Environment assumptions

- The prep and scoring notebooks are R-first.
- The modeling notebook depends on `MOFA2` and the usual matrix and plotting stack.
- Add external download or GDC-authenticated steps explicitly in `01_multiomics_input_prep.qmd`, not in hidden scripts.

## Archive notes

Use `archive_notes/MOFA_code_inventory.md` for the source-to-template mapping and for TCGA-LUAD-specific decisions that should not leak into the reusable surface.
