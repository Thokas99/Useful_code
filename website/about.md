---
layout: default
title: About
nav_order: 6
---

Useful code collects R, Python, and Quarto workflows drawn from bioinformatics
projects. Browse the [methods catalog](https://thokas99.github.io/Useful_code/)
or open the [GitHub repository](https://github.com/Thokas99/Useful_code).

> [!CAUTION]
> Examples are provided as-is. Check each workflow's inputs, assumptions,
> package versions, and design before reuse. Outputs need independent review;
> this repository does not establish clinical or diagnostic performance.

## Guide labels

| Label | Meaning |
|---|---|
| `SOURCE-BACKED WORKFLOW` | A substantial implementation was available in the repository sources. |
| `API / TUTORIAL REMINDER` | A concise workflow summary links to package documentation. |
| `Static checks` | CI checks document structure, paths, front matter, and code syntax; it does not run the analysis. |
| `draft` | The guide has not been run on representative data. |

A source-backed workflow can still need adaptation and validation.

## File conventions

Seurat objects use `.qs2`, AnnData objects use `.h5ad`, tables use TSV, and
MOFA2 models use native HDF5.

## License

See the [MIT License](https://github.com/Thokas99/Useful_code/blob/main/LICENSE).
