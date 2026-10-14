# Repository architecture

The repository separates reusable guides, project examples, support material,
and historical records:

```text
templates/   active reusable analytical templates
examples/    real project workflows and provenance
functions/   small reusable R and Python helpers
miscellaneous/ reusable scientific-workflow resources that are not analytical method templates
docs/        architecture and refactor documentation
archive/     superseded scaffolds and historical material
scripts/     repository checks
website/     searchable catalog and notebook downloads
```

The active library has eight Quarto guides across six analysis areas. The root
and [template README](../templates/README.md) index them; `website/` publishes
the catalog and notebook downloads.

## Canonical conventions

- R analytical objects → `qs2`
- Python AnnData → `.h5ad`
- MOFA2 trained models → native HDF5
- human-readable tables → TSV

Keep scientific choices visible in the notebooks: filtering, normalization,
integration, model design, feature selection, and interpretation stay beside
the analysis that uses them.

`SOURCE-BACKED WORKFLOW` templates adapt substantial source implementations.
`API / TUTORIAL REMINDER` templates summarize a package workflow and link to
its documentation. Keep project-specific labels, paths, and conclusions in
`examples/`; preserve superseded material in `archive/`.

`miscellaneous/` contains reporting resources, not analysis methods.

The Jekyll site catalogs guides and builds family downloads. It does not run
the bioinformatics analyses.
