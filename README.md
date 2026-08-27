# Useful code

Useful code is a curated personal bioinformatics cookbook of reusable R,
Python, and Quarto templates derived from real analytical workflows.

## What this repository is

The repository preserves small, understandable workflows together with the
scientific decisions, diagnostics, implementation tricks, and provenance that
make them useful when reopened later. It is not an R/Python package, a
production clinical pipeline, or a replacement for upstream documentation.

## Template library

The active, generalized templates are under [`templates/`](templates/README.md).

| Family | Purpose | Canonical folder |
|---|---|---|
| Single-cell RNA | Seurat preprocessing, scoring, trajectories, dynamics, networks | [`templates/single_cell/`](templates/single_cell/README.md) |
| Bulk RNA | tximport/edgeR, QC, enrichment, and sample-level scoring | [`templates/bulk_rna/`](templates/bulk_rna/README.md) |
| scATAC | Signac object construction, QC, LSI, and motif analysis | [`templates/scatac/`](templates/scatac/README.md) |
| Multiome | Paired RNA/ATAC WNN, linkage, and label transfer | [`templates/multiome/`](templates/multiome/README.md) |
| Multi-omics / MOFA | MOFA2 view preparation, fitting, diagnostics, and interpretation | [`templates/multiomics/mofa/`](templates/multiomics/mofa/README.md) |
| Biomarker machine learning | Sample-level biomarker classification and frozen reporting | [`templates/machine_learning/biomarkers/`](templates/machine_learning/biomarkers/README.md) |

## Repository structure

```text
templates/   active canonical workflows
examples/    real project analyses and provenance
cheatsheets/ compact reference material
docs/        architecture and refactor documentation
archive/     superseded scaffolds and historical archives
```

## Template philosophy

Canonical notebooks keep meaningful parameters and scientific operations
visible. `SOURCE-BACKED WORKFLOW` means a substantial implementation exists in
the repository history. `API / TUTORIAL REMINDER` means the notebook is a
concise reminder based on current package interfaces. Each notebook states
whether it is `validated`, `draft`, or `blocked`; parsing alone does not make a
workflow validated.

## Conventions

- R analytical objects use `qs2`.
- Python AnnData objects use `.h5ad`.
- Human-readable tables use TSV.
- Trained MOFA2 models use native HDF5 as an intentional exception.
- Advanced package behavior should be checked against official documentation.

## Examples and provenance

The [`examples/`](examples/README.md) tree retains concrete project workflows,
including their project-specific labels and assumptions. Those files are
provenance and worked examples; the reusable generalized versions are under
`templates/`.

## Status

The library is actively organized for later documentation, but individual
templates remain at their stated validation status. No claim is made that every
workflow has been executed end to end on a representative dataset.

## License

See [`LICENSE`](LICENSE).
