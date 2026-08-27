# Canonical template library

This is the active reusable analytical library. It contains compact
source-backed workflows and concise API/tutorial reminders derived from real
bioinformatics work. Project-specific analyses are preserved separately under
[`../examples/`](../examples/README.md).

## Families

| Family | Folder | Contents |
|---|---|---|
| Single-cell RNA | [`single_cell/`](single_cell/README.md) | Seurat, QC, normalization, scoring, trajectories, dynamics, networks |
| Bulk RNA-seq | [`bulk_rna/`](bulk_rna/README.md) | tximport/edgeR, QC, DE reminder, GSEA, singscore, GSVA |
| scATAC-seq | [`scatac/`](scatac/README.md) | Signac construction, fragment-aware QC, LSI, motifs, chromVAR reminder |
| Multiome | [`multiome/`](multiome/README.md) | Paired RNA/ATAC WNN, peak-gene linkage, label transfer |
| Multi-omics / MOFA | [`multiomics/mofa/`](multiomics/mofa/README.md) | View preparation, MOFA2 fitting, diagnostics, interpretation |
| Biomarker machine learning | [`machine_learning/biomarkers/`](machine_learning/biomarkers/README.md) | Bias-reduced sample-level classification and frozen reporting |

## Legend

- `SOURCE-BACKED WORKFLOW`: substantial implementation was available in the
  repository sources.
- `API / TUTORIAL REMINDER`: minimal current API reminder where no complete
  source workflow was available.
- `validated`, `draft`, `blocked`: strict notebook validation status. Most
  templates are intentionally `draft` until representative execution.

## Persistence

R analytical objects use `.qs2` through visible `qs2` calls, Python AnnData
uses `.h5ad`, and tabular outputs use `.tsv`. MOFA2 trained models use native
`.hdf5` as the documented model-format exception.

Use a template by reading its input/output contract, setting only the exposed
scientific decisions, and checking the current official package documentation
before adapting version-sensitive code.
