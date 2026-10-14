# Analysis guides

Eight reusable Quarto guides cover six analysis areas. Each follows one main
object from input checks through analysis and export. Project-specific
workflows remain under [`../examples/`](../examples/).

| Guide | Main object | Scope |
|---|---|---|
| [Single-cell RNA in R](single_cell/guide_r.qmd) | Seurat | QC, clustering, MAST markers, pseudobulk, signatures, trajectories, modules |
| [Single-cell RNA in Python](single_cell/guide_python.qmd) | AnnData | scVelo, CellRank, decoupler, optional scCellFie |
| [Gene signatures in Python](single_cell/guide_pyucell.qmd) | AnnData | pyUCell scores, gene coverage, plots, and exports |
| [Bulk RNA-seq](bulk_rna/guide.qmd) | edgeR DGEList | Differential expression, enrichment, and sample scores |
| [scATAC-seq](scatac/guide.qmd) | Signac | Fragment QC, LSI, peak tests, motifs, chromVAR |
| [Multiome](multiome/guide.qmd) | Seurat | Paired RNA/ATAC QC, WNN, linkage, label transfer |
| [Multi-omics with MOFA2](multiomics/mofa/guide.qmd) | MOFA2 | Matched views, fitting, factors, and diagnostics |
| [Sample-level biomarkers](machine_learning/biomarkers/guide.qmd) | Tidymodels workflow | Patient split, classification, held-out metrics |

## Use

Read the input contract and draft note first. Then update paths, labels,
thresholds, covariates, and model choices for the study. Run cells in order and
keep the configuration, software versions, and outputs with the analysis.

> **Status:** Every guide is a starting point. A draft has not been run on
> representative data; a source-backed method is not a universal validation.
