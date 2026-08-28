---
layout: default
title: About
nav_order: 6
---

Useful code is a personal bioinformatics cookbook of reusable R, Python, and
Quarto workflows derived from real analytical work.

Browse the [live catalog](https://thokas99.github.io/Useful_code/) for method
families and direct notebook links. The [GitHub repository](https://github.com/Thokas99/Useful_code)
is the source of truth for the code, parameters, provenance, and notebook
status.

## Personal research code

These notebooks are maintained as a personal analytical cookbook and are
provided as-is. They may contain project-specific assumptions, thresholds,
package APIs, or methodological choices that are not automatically appropriate
for another dataset or study design.

Review each notebook, verify current upstream documentation, adapt the
parameters and paths, and independently validate the workflow and outputs
before relying on them. The scripts are not intended for clinical, diagnostic,
or other high-stakes decision-making. No warranty is provided beyond the terms
of the repository's MIT License.

## Templates and examples

`templates/` contains the active generalized notebooks. `examples/` contains
project-specific analyses and provenance. The catalog links to those source
files on GitHub; it does not mirror or execute them.

## Template labels

- `SOURCE-BACKED WORKFLOW` means a substantial implementation was available in
  the repository sources.
- `API / TUTORIAL REMINDER` means a concise reminder based on a current package
  interface where no complete source workflow was found.
- `draft`, `validated`, and `blocked` describe strict notebook validation
  status. `SOURCE-BACKED` does not mean scientifically validated everywhere,
  and `draft` does not mean broken.

## Conventions

R analytical objects use `.qs2`, Python AnnData uses `.h5ad`, human-readable
tables use TSV, and MOFA2 models use native HDF5 as an intentional exception.
The repository and its notebooks remain the source of truth.

## License

See the [repository README](https://github.com/Thokas99/Useful_code/blob/main/README.md),
[archive](https://github.com/Thokas99/Useful_code/tree/main/archive), and
[LICENSE](https://github.com/Thokas99/Useful_code/blob/main/LICENSE) on GitHub.
