# Repository architecture

Useful code has one active library and several deliberately separate support
areas:

```text
templates/   active reusable analytical templates
examples/    real project workflows and provenance
miscellaneous/ reusable scientific-workflow resources that are not analytical method templates
docs/        architecture and refactor documentation
archive/     superseded scaffolds and historical material
website/     searchable catalog and notebook downloads
```

The active library contains seven Quarto guides across six analysis areas.
The root README and [`templates/README.md`](../templates/README.md) describe
the current guides; `website/` publishes their catalog and downloadable copies.

## Canonical conventions

- R analytical objects → `qs2`
- Python AnnData → `.h5ad`
- MOFA2 trained models → native HDF5
- human-readable tables → TSV

Scientific choices remain visible in canonical notebooks: filtering,
normalization, integration, model design, feature selection, and interpretation
are not hidden in a shared helper library. Helpers are intentionally minimal.

`SOURCE-BACKED WORKFLOW` templates preserve substantial implementations from
the source repository. `API / TUTORIAL REMINDER` templates are short reminders
that point upstream rather than reproducing package manuals. Project-specific
biology, labels, paths, and study conclusions remain in `examples/` or
`archive/`.

`miscellaneous/` contains reusable prompts and reporting resources that support
scientific workflows but do not define analytical methods. A separate
cheatsheet collection is not currently maintained.

The website is a Jekyll catalog. It indexes the guide sources and builds a ZIP
for each method family; it does not run the bioinformatics analyses.
