# Useful code

A curated personal bioinformatics cookbook of 37 reusable R, Python, and
Quarto workflows derived from real analytical projects.

**Browse the catalog:** [open the website](https://thokas99.github.io/Useful_code/)
· [browse the templates](templates/README.md) · [view the repository on GitHub](https://github.com/Thokas99/Useful_code)

The website is an index, not a second copy of the science: each catalog entry
links to the canonical notebook in this repository, where the code, parameters,
provenance, and current status remain the source of truth.

## What this repository contains

The repository preserves small, understandable workflows together with the
scientific decisions, diagnostics, implementation details, and provenance that
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
miscellaneous/ reusable scientific documentation and reporting resources
docs/        architecture and refactor documentation
archive/     superseded scaffolds and historical archives
```

General documentation and reporting resources are collected under
[`miscellaneous/`](miscellaneous/README.md).

## How to use the templates

1. Choose a method family from the [website catalog](https://thokas99.github.io/Useful_code/)
   or [`templates/`](templates/README.md).
2. Read the notebook's purpose, inputs, outputs, parameters, and status before
   adapting it.
3. Recheck package behavior and assumptions against the relevant upstream
   documentation and your own data.

The notebooks are intentionally readable starting points. They are not
guarantees of validation for every dataset or analysis design.

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

Individual templates remain at their stated validation status. No claim is made
that every workflow has been executed end to end on a representative dataset.

## License

See [`LICENSE`](LICENSE).
