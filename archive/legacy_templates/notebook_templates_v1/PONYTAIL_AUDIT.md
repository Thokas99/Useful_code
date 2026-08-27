# Ponytail Audit

Scope: `notebook_templates/` only.

## Result

The templates stay intentionally boring: standalone Quarto notebooks, no shared helper layer, no sourced scripts, no extra categories, and no new dependencies beyond the workflow packages already represented by the source notebooks.

## Checks

- Eighteen source notebooks are represented in `NOTEBOOK_INVENTORY.md`.
- Eighteen reusable `.qmd` templates are present.
- Every template keeps one editable `# USER INPUT:` section.
- Every template has the same required section headers from purpose through output summary.
- Every executable code block has a stable Quarto chunk label plus `echo`, `warning`, and `message` options.
- Every non-config code block has a short orienting comment.
- R object persistence uses `qs2::qs_read()` and `qs2::qs_save()`.
- Python object persistence uses `sc.read_h5ad()` and `adata.write_h5ad()`.
- Tabular output is TSV-only: `readr::write_tsv()` in R and pandas `to_csv(..., sep="\t")` to `.tsv` paths in Python.
- No shared helper files, cross-template imports, `source()` calls, legacy R object persistence calls, `.RData`, `.csv` paths, or local absolute paths are used.

## Ponytail Notes

Skipped a shared helper package and one-template-per-source expansion. The current topic templates cover the real workflows with less code and fewer moving parts.

