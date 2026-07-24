# Notebook Inventory

Eighteen current Quarto notebooks were represented in these templates.

| Source notebook | Reusable template coverage |
|---|---|
| `00_MAP_RNA_qc_integration.qmd` | `scRNA/01_create_seurat_object.qmd`, `scRNA/02_quality_control.qmd`, `scRNA/03_normalization_integration_clustering.qmd` |
| `GSE171145.qmd` | `scRNA/01_create_seurat_object.qmd`, `scRNA/02_quality_control.qmd`, `scRNA/03_normalization_integration_clustering.qmd` |
| `00_MAP_ATAC_qc_integration.qmd` | `scATAC/01_create_signac_object.qmd`, `scATAC/02_quality_control_integration.qmd` |
| `00_MAP_qc_integration.qmd` | `multiome/01_create_multiome_object.qmd`, `multiome/02_qc_integration_wnn.qmd` |
| `001_RNA_ATAC_LT.qmd` | `multiome/03_rna_atac_linkage.qmd` |
| `002_ATAC_MOTIF.qmd` | `scATAC/03_motif_enrichment.qmd` |
| `01_MAP_metadata_bridge.qmd` | Validation, metadata checks, and join guards inside object-loading and QC templates |
| `01_MAP_c1_scoring.qmd` | `scRNA/04_signature_scoring.qmd` |
| `02_MAP_c1_scoring.qmd` | `scRNA/04_signature_scoring.qmd` |
| `09_MAP_C1_Core_refined_signature.qmd` | `scRNA/04_signature_scoring.qmd` |
| `03_MAP_state_markers_statistics_export.qmd` | `scRNA/05_marker_identification_and_export.qmd`, `general_statistics/01_group_summary_and_association_tests.qmd` |
| `04_MAP_c1_gene_programs_tradeSeq.qmd` | `scRNA/06_trajectory_gene_programs.qmd` |
| `04_MAP_decoupler_bridge.qmd` | `scRNA/07_pathway_activity_decoupler.qmd` |
| `05_MAP_regulatory_programs.qmd` | `multiome/04_regulatory_programs.qmd` |
| `06_MAP_coexpression_modules.qmd` | `scRNA/08_coexpression_modules.qmd` |
| `07_MAP_velocity_scvelo_cellrank.qmd` | `scRNA/09_velocity_scvelo_cellrank.qmd` |
| `08_MAP_metabolic_activity_scCellFie.qmd` | `scRNA/10_metabolic_activity.qmd` |
| `10_MAP_extensive_statistics.qmd` | `general_statistics/01_group_summary_and_association_tests.qmd` |

No separate `bulk_RNA/`, `miRNA/`, or `machine_learning/` category was added because the current notebook set supports single-cell RNA, ATAC, multiome, Python AnnData bridge workflows, and general statistics.

All templates are standalone. There are no shared helper scripts, legacy R object persistence calls, or workspace-image dependencies.
