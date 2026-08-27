# Repository architecture

Useful code has one active library and several deliberately separate support
areas:

```text
templates/   active reusable analytical templates
examples/    real project workflows and provenance
cheatsheets/ compact conceptual and reference material
docs/        architecture and refactor documentation
archive/     superseded scaffolds and historical material
```

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

The structure is suitable for later documentation, but no website or Quarto
website configuration is part of this repository state.
