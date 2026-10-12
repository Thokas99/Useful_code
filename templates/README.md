# Analysis guidebook

The active library is seven Quarto guides. Each guide keeps one main analysis
object and puts related steps in order. The original project notebooks under
`../code_MAP/` are preserved unchanged; these guides are the reusable starting
points.

## Guide map

```mermaid
flowchart LR
  RNA1[RNA counts] --> RSC[Single-cell RNA in R<br/>Seurat]
  RNA2[Processed AnnData] --> PSC[Single-cell RNA in Python<br/>scVelo and CellRank]
  BULK[Bulk gene counts] --> BR[Bulk RNA<br/>edgeR and scoring]
  PEAK[ATAC peaks and fragments] --> AT[scATAC<br/>Signac]
  PAIR[Paired RNA and ATAC] --> MO[Multiome<br/>WNN and linkage]
  VIEWS[Matched omics views] --> MF[MOFA2<br/>factors and weights]
  SAMPLES[Sample expression and labels] --> BM[Biomarker model<br/>held-out evaluation]
```

| Guide | Main object | Analyses in one notebook |
|---|---|---|
| [Single-cell RNA in R](single_cell/guide_r.qmd) | `object` (Seurat) | QC, doublets, normalization, clustering, markers, scoring, trajectories, hdWGCNA |
| [Single-cell RNA in Python](single_cell/guide_python.qmd) | `adata` (AnnData) | scVelo, CellRank, decoupler, scCellFie |
| [Bulk RNA-seq](bulk_rna/guide.qmd) | `dge` (edgeR) | tximport, QC, differential expression, GSEA, singscore, GSVA |
| [scATAC-seq](scatac/guide.qmd) | `object` (Signac) | fragment QC, LSI, peaks, motif enrichment, chromVAR |
| [Multiome](multiome/guide.qmd) | `object` (Seurat) | paired QC, WNN, peak-gene links, label transfer |
| [Multi-omics with MOFA2](multiomics/mofa/guide.qmd) | `mofa` | matched views, fitting, factor diagnostics, weights |
| [Sample-level biomarkers](machine_learning/biomarkers/guide.qmd) | `model` | training-only preprocessing, bias-reduced classification, held-out reporting |

## Use

Run the code cells from top to bottom after changing the input paths and the
scientific choices for the study. Optional cells are marked in the guide.
The guides are drafts and have not been rendered or run on representative data.
Check the current package documentation, study design, and assumptions before
using results.

R objects use `.qs2`; AnnData objects use `.h5ad`; tables use TSV. MOFA2 models
use their native HDF5 format.
