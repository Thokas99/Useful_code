# Single-cell method templates

This directory is a personal analytical cookbook: reusable workflows that
have been used in practice, plus short API reminders for useful methods without
a complete source workflow in this repository. It is not a replacement for
package documentation. All 16 templates are currently `draft` because the
canonical forms have not been runtime-validated on representative objects.

## Core Seurat path

`create_object.qmd` creates one RNA Seurat object from a feature-by-cell count
matrix and aligned metadata, checking identifiers before applying
`min.cells = 3`, `min.features = 200`, and a configurable mitochondrial
pattern. `qc.qmd` applies visible fixed thresholds, reports pooled and
per-sample distributions, and saves the filtered object. Inspecting QC per
sample is a workflow preference, not a universal threshold rule.

`doublets_scdblfinder.qmd` converts Seurat to SingleCellExperiment, calls
scDblFinder by an explicit capture/library column, and retains calls unless
`remove_doublets` is changed. `normalization_log.qmd` ends with
`NormalizeData -> FindVariableFeatures -> ScaleData -> RunPCA`.
`normalization_sct.qmd` ends with `SCTransform -> RunPCA` and exposes
regression variables. `harmony.qmd` consumes a PCA-ready object and performs
the optional post-Harmony graph, clustering, UMAP, and LISI diagnostics.

## Scoring and markers

`ucell.qmd` reads a signature TSV with `signature`, `gene`, and `direction`
columns. It preserves UP and DOWN UCell components, makes the raw directional
difference primary, and keeps dataset-relative z-scoring optional.
`cytotrace2.qmd` passes a raw count layer to CytoTRACE2 with explicit species,
resource, and cell-ID decisions, then attaches score and potency outputs.
`markers_cell_level.qmd` is a focused Seurat `FindMarkers()` comparison. It is
cell-level exploratory analysis and is not a substitute for sample-aware or
pseudobulk inference when samples are the biological replicates.

## Trajectory and dynamics

`slingshot.qmd` is an API / TUTORIAL REMINDER: it shows the minimal current
reduced-dimension and cluster-label call, pseudotime, and curve weights. It
has no complete source implementation here. `tradeseq.qmd` is the separate
SOURCE-BACKED WORKFLOW: it consumes explicit pseudotime and lineage weights,
fits `fitGAM()`, and distinguishes association testing from start-versus-end
testing without imposing a universal feature cap.

`scvelo.qmd` requires aligned kinetic `spliced` and `unspliced` layers, makes
the neighbor representation explicit, and writes velocity-aware h5ad output.
An integrated expression matrix must not silently replace those kinetic
layers. `cellrank.qmd` consumes that velocity-aware h5ad, combines velocity
and connectivity kernels, and exposes Schur/state, initial/terminal, solver,
and fate-driver decisions.

## Activity and networks

`decoupler.qmd` uses the Python decoupler ULM route with a long network TSV
containing `source`, `target`, and `weight`. `hdwgcna.qmd` performs the actual
co-expression workflow: variable features, user-controlled metacell grouping,
soft-power diagnostics, network construction, eigengenes, connectivity, and
hub ranking. It is not predefined gene-set scoring.

`sccellfie.qmd` runs the actual scCellFie computation, retains organism,
counts, batch, neighbor, threshold, smoothing, alpha, and chunk decisions,
and summarizes metabolic-task estimates by group. These are activity
estimates, not direct flux measurements. Its documented package summary
writer emits CSV files; this is the one package-output exception to the
otherwise TSV table convention.

## Persistence and use

- R analytical objects: `qs2` via visible `qs2::qs_save()` and `qs2::qs_read()`
  calls, using `.qs2` paths.
- Python AnnData objects: `.h5ad`.
- Tables: `.tsv`, except the documented scCellFie report-writer output.

Preserve the object handoffs, record package versions and input provenance,
and consult the current official documentation before adapting any template to
a new package release or biological question.
