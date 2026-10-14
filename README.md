# Useful code

A collection of bioinformatics guides and project examples in R, Python, and
Quarto. Guides provide compact starting points; examples retain project
context.

[![R](https://img.shields.io/badge/R-276DC3?logo=r&logoColor=white)](https://www.r-project.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Quarto](https://img.shields.io/badge/Quarto-39729E?logo=quarto&logoColor=white)](https://quarto.org/)
[![MIT License](https://img.shields.io/badge/license-MIT-2ea44f)](LICENSE)

> [!CAUTION]
> These workflows are not validated for your study. Review their inputs,
> assumptions, software versions, and outputs before reuse. They are not for
> clinical or diagnostic decisions.

[Methods catalog](https://thokas99.github.io/Useful_code/) ·
[Templates](templates/README.md) · [Examples](examples/README.md) ·
[Other resources](miscellaneous/README.md)

## Methods

| Area | Guides | Focus |
|---|---:|---|
| [Single-cell](https://thokas99.github.io/Useful_code/methods/single-cell/) | 3 | Seurat, AnnData velocity and activity, pyUCell signatures |
| [Bulk RNA](https://thokas99.github.io/Useful_code/methods/bulk-rna/) | 1 | tximport, edgeR, enrichment, and sample scoring |
| [scATAC](https://thokas99.github.io/Useful_code/methods/scatac/) | 1 | Signac QC, peak testing, motifs, and chromVAR |
| [Multiome](https://thokas99.github.io/Useful_code/methods/multiome/) | 1 | Paired RNA/ATAC QC, WNN, linkage, and label transfer |
| [MOFA2](https://thokas99.github.io/Useful_code/methods/mofa/) | 1 | Matched views, factors, and diagnostics |
| [Biomarker ML](https://thokas99.github.io/Useful_code/methods/biomarker-ml/) | 1 | Patient-grouped held-out evaluation |

The [template guide](templates/README.md) lists all eight workflows. The
[examples](examples/README.md) preserve project-specific context and methods.

## Reuse a workflow

1. Confirm that the input, identifiers, and study design match the guide.
2. Check package versions and current upstream documentation.
3. Set paths and scientific choices for your data.
4. Review diagnostics and validate outputs before interpretation.

> **Guide status:** `draft` means the workflow has not been checked on
> representative data. It does not certify or invalidate a scientific method.

## Repository map

| Path | Contents |
|---|---|
| `templates/` | Reusable analysis guides |
| `examples/` | Project-specific workflows and provenance |
| `functions/` | Small shared R and Python helpers |
| `miscellaneous/` | Reporting and documentation resources |
| `scripts/` | Repository checks |
| `website/` | Searchable catalog and downloads |
| `archive/` | Superseded material and historical records |

GitHub Actions checks document structure, paths, and syntax. It does not run
the bioinformatics analyses.

## File conventions

- Seurat objects: `.qs2`
- AnnData objects: `.h5ad`
- Tables: TSV
- MOFA2 models: native HDF5

## License

Released under the [MIT License](LICENSE).
