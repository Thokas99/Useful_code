# Legacy reusable notebook templates

> Superseded intermediate scaffold. The active canonical library is under
> [`../../../templates/`](../../../templates); this directory is retained for
> history and provenance only.

**Status:** Reusable computational template library; not a study-results workflow.

## Purpose and status

This directory contains self-contained Quarto templates distilled from the source notebooks. They are configurable starting points, not imported modules and not the provenance of any one reported MAP, MGI, TRENTO, or TCGA result. Each template exposes paths, columns, assays, thresholds, and output names in a user-configuration section. A template can therefore be copied into a project and parameterized without changing the underlying analysis code, but the copied configuration must be preserved with the resulting analysis.

The R templates generally use `qs2::qs_read()` and `qs2::qs_save()` for serialized objects and TSV files for tabular outputs. The velocity and metabolic templates use AnnData `.h5ad` files and Python packages. Most templates validate paths and required columns, but they are not all rendered against representative data in this repository; “source-backed” means that the method is present in code, not that a current end-to-end execution has been verified.

## Template families

- `scRNA/`, `scATAC/`, `multiome/`, and `general_statistics/` contain the
  former scaffold components and their original QMDs.

## Shared implementation contract

The templates read an explicit input object, validate dimensions and identifiers where implemented, perform the configured transformation or test, write tables/figures, and save a downstream object. Defaults are template defaults and must not be reported as study-specific values. For example, the generic scRNA clustering template uses 3,000 variable features, 30 PCs, and resolution 0.5, whereas the principal MAP notebook uses 3,500 variable features, Harmony dimensions 1–41, and a final resolution of 0.2. The generic scATAC template uses TSS ≥2 and nucleosome signal ≤4, whereas the MAP ATAC notebook has its own QC and resolution diagnostics.

## Reproducibility requirements

To use a template reproducibly, record the copied notebook, all user-configuration values, input checksums or object-generation scripts, package versions, random seeds, and output paths. Keep upstream object contracts explicit: a filtered Seurat object is required by normalization templates, an h5ad with the expected RNA/velocity layers is required by scVelo, and activity-attachment templates require a cell-aligned TSV. The template code does not supply missing biological metadata, gene annotations, motif databases, or transcript-to-gene mappings.

## Method reconstruction

Select a template family, copy the relevant notebook, populate its user configuration, restore the stated object/input contract, and execute only the dependent templates in sequence. Preserve the resulting configuration, input checks, software versions, and output object. Do not combine defaults from separate families with study-specific parameters without documenting the combined method.
