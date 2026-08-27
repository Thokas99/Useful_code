# MOFA Code Inventory

This note records how the live MOFA notebooks were distilled into `MOFA_TEMPLATE_CLEAN/`.

## Notebook mapping

| Source notebook | Distilled destination | Role in clean template | Notes |
| --- | --- | --- | --- |
| `00_TCGA_LUAD_multiomics_download.qmd` | `01_multiomics_input_prep.qmd` | matched multi-omics preparation | keep download and sample harmonization visible |
| `01_TCGA_LUAD_scoring_tf.qmd` | `02_signature_scoring.qmd` | score construction and metadata layer | generalize notebook name, keep score story inline |
| `03_MOFA.qmd` | `03_mofa_model.qmd` | MOFA model build and export | keep factor heatmaps, view heatmaps, and median or frequency summaries in the main notebook |

## Helper extraction

| Helper | Source | Final use | Essential |
| --- | --- | --- | --- |
| `tcga_sample_barcode` | `00_TCGA_LUAD_multiomics_download.qmd` | `01` | yes |
| `collapse_duplicate_samples_mean`, `collapse_duplicate_samples_sum`, `collapse_duplicate_samples_max` | `00_TCGA_LUAD_multiomics_download.qmd` | `01` | optional |
| `compute_cpm`, `compute_logcpm` | `01_TCGA_LUAD_scoring_tf.qmd` and `03_MOFA.qmd` | `02`, `03` | yes |
| `class_from_z` | `01_TCGA_LUAD_scoring_tf.qmd` | `02` | yes |
| `save_plot_png`, `keep_most_variable_dt`, `to_numeric_matrix` | `03_MOFA.qmd` | `03` | yes |

## Dataset-specific material kept out of the reusable surface

- TCGA-LUAD-specific cohort names and titles
- fixed C1-Core labels and signature panels
- exact GDC query settings, manifests, and tumor-only filters
- specific mutation panels, pathway shortlists, and factor interpretation labels
- preselected top features or story-driven plots tied to one project
