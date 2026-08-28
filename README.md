# Useful code

A personal collection of bioinformatics notebooks in R, Python, and Quarto.
Most started in real projects and were later cleaned up so I could find and
reuse the useful parts.

[![Bioinformatics](https://img.shields.io/badge/domain-bioinformatics-1f6feb)](https://github.com/Thokas99/Useful_code)
[![R](https://img.shields.io/badge/R-276DC3?logo=r&logoColor=white)](https://www.r-project.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Quarto](https://img.shields.io/badge/Quarto-39729E?logo=quarto&logoColor=white)](https://quarto.org/)
[![GitHub Pages](https://img.shields.io/badge/site-GitHub%20Pages-222222?logo=github)](https://thokas99.github.io/Useful_code/)
[![Jekyll / Just the Docs](https://img.shields.io/badge/site-Jekyll%20%2F%20Just%20the%20Docs-cc0000)](https://just-the-docs.github.io/just-the-docs/)
[![MIT License](https://img.shields.io/badge/license-MIT-2ea44f)](LICENSE)

> [!CAUTION]
> **Personal research code.** These notebooks are maintained as a personal
> analytical cookbook and are provided as-is. They may contain assumptions,
> thresholds, package APIs, or methodological choices that were appropriate for
> the source project but are not automatically appropriate for another dataset.
>
> Review the notebook, verify current upstream documentation, adapt parameters
> to your study design, and independently validate the workflow and outputs
> before relying on them. These scripts are not intended for clinical,
> diagnostic, or other high-stakes decision-making.

[Browse the website](https://thokas99.github.io/Useful_code/) ·
[Browse templates](templates/README.md) ·
[Examples](examples/README.md) ·
[Miscellaneous](miscellaneous/README.md)

## What is here

Useful code keeps readable analytical workflows together with the parameters,
diagnostics, and implementation details that make them useful when reopened.
The website groups the notebooks by analysis area and links back to the files.
The generated registry in `CODE_MAP/method_registry.tsv` makes the active
notebook collection searchable by script.

## Browse the methods

| Family | Scope | Notebooks | Link |
|---|---|---:|---|
| Single-cell RNA | Seurat preprocessing, scoring, trajectories, dynamics, and networks | 16 | [Open family](https://thokas99.github.io/Useful_code/methods/single-cell/) |
| Bulk RNA | tximport/edgeR, quality control, enrichment, and sample-level scoring | 6 | [Open family](https://thokas99.github.io/Useful_code/methods/bulk-rna/) |
| scATAC | Signac object construction, quality control, LSI, and motif analysis | 5 | [Open family](https://thokas99.github.io/Useful_code/methods/scatac/) |
| Multiome | Paired RNA/ATAC WNN, linkage, and label transfer | 4 | [Open family](https://thokas99.github.io/Useful_code/methods/multiome/) |
| Multi-omics / MOFA | MOFA2 view preparation, fitting, diagnostics, and interpretation | 4 | [Open family](https://thokas99.github.io/Useful_code/methods/mofa/) |
| Biomarker machine learning | Sample-level biomarker classification and frozen reporting | 2 | [Open family](https://thokas99.github.io/Useful_code/methods/biomarker-ml/) |

The collection currently contains **37 notebooks**: **34 source-backed
workflows** and **3 API / tutorial reminders**.

## How to use these scripts safely

Before reusing a notebook:

1. Read its Purpose, Inputs, Outputs, Parameters, and Status sections.
2. Check package and API behavior against current upstream documentation.
3. Review thresholds, transformations, genome builds, factor levels, and
   positive/event classes.
4. Adapt paths and other dataset-specific assumptions.
5. Validate the outputs on your own data and study design.

## Repository checks and registry

GitHub Actions runs lightweight checks on pushes and pull requests: YAML and
Quarto front matter, Markdown links, Python and R syntax, reusable-template
paths, large files, registry consistency, and the website build. It does not
run the bioinformatics analyses.

Regenerate the notebook registry after changing the active catalog with:

```bash
python3 scripts/build_method_registry.py
```

Use `--check` in CI or before committing to confirm that the tracked TSV is
current.

## Repository structure

    functions/        small reusable R and Python implementation primitives
    templates/       reusable notebooks
    examples/        project-specific analyses and context
    miscellaneous/   reporting prompts and reusable documentation material
    scripts/          repository maintenance and registry checks
    CODE_MAP/         searchable repository metadata
    website/         Jekyll catalog website
    docs/            architecture and refactor documentation
    archive/         superseded historical material

## Template classes and status

`SOURCE-BACKED WORKFLOW` means that a substantial implementation exists in the
repository sources. `API / TUTORIAL REMINDER` means that the notebook is a
concise reminder based on a package interface where no complete source workflow
was found.

Each notebook also states a validation status such as `draft`, `validated`, or
`blocked`. A source-backed workflow is not automatically scientifically
validated everywhere, and `draft` does not mean broken; the status describes
what was established for the source project.

## Conventions

- R analytical objects use `.qs2`.
- Python AnnData objects use `.h5ad`.
- Human-readable tables use TSV.
- Trained MOFA2 models use native HDF5 as an intentional exception.
- Advanced package behavior should be checked against official documentation.

## Examples and additional resources

- [Examples](examples/README.md) retain concrete project workflows and
  context; generalized versions belong under `templates/`.
- [Miscellaneous](miscellaneous/README.md) collects reporting and documentation
  resources.

## License

Released under the [MIT License](LICENSE).
