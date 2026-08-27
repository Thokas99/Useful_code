# Canonical paired RNA/ATAC templates

These templates preserve reusable paired-modality Seurat/Signac workflows. They
are a personal cookbook, not replacements for Seurat, Signac, or genome-resource
documentation.

## Suggested flow

```text
create_object
    ↓
wnn
    ├── rna_atac_linkage
    └── rna_to_atac_label_transfer
```

The object-creation page deliberately intersects RNA and ATAC cell IDs and
reports mismatches. Use the single-cell and scATAC templates for modality QC
and preprocessing before this handoff when needed.

- **WNN:** combines RNA and ATAC representations for cell neighborhoods; it is
  not batch correction.
- **RNA–ATAC linkage:** estimates statistical peak–gene links from paired
  expression and accessibility.
- **Label transfer:** transfers labels directionally from an RNA reference to
  an ATAC query using GeneActivity in gene space.

## Class and status legend

All four pages are `SOURCE-BACKED WORKFLOW` templates and currently `draft`.
Their source implementations were not executed in the new canonical forms.

## Persistence

R analytical objects use `qs2`; predictions, links, alignment records, and
other human-readable results use TSV. Genome builds, annotations, and fragment
files remain external inputs that must be recorded.
