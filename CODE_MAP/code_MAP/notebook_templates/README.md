# Reusable Notebook Templates

This directory contains copy-and-configure Quarto templates distilled from the current repository notebooks.

Use them as starting points, not as imported modules. Each template is self-contained and keeps editable paths, columns, assays, thresholds, and output names in a single `# USER INPUT:` section.

## Layout

- `scRNA/`: Seurat RNA workflows.
- `scATAC/`: Signac ATAC workflows.
- `multiome/`: paired RNA/ATAC and WNN-style workflows.
- `general_statistics/`: group summaries and association tests.

R templates use `qs2::qs_read()` and `qs2::qs_save()`. Python templates use AnnData `.h5ad` files.

