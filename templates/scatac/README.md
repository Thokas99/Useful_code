# Canonical scATAC-seq templates

These compact templates preserve reusable Signac workflows from the project
notebooks. They are a personal cookbook, not replacements for Signac,
Seurat, Bioconductor, or genome-resource documentation.

## Suggested flow

```text
create_object
    ↓
qc
    ↓
lsi_clustering
    ├── motif_enrichment_findmotifs
    └── chromvar
```

`FindMotifs` tests motif enrichment in a selected foreground peak set against
an explicit background. chromVAR estimates cell-level motif deviation scores;
it is a different analysis and is intentionally only a short API reminder
here.

## Class and status legend

- `SOURCE-BACKED WORKFLOW`: substantial implementation exists in the source
  notebooks.
- `API / TUTORIAL REMINDER`: concise code derived from the current API because
  no complete source implementation was found.
- `draft`: the canonical form still needs representative execution.

## Persistence

R analytical objects use `qs2`; human-readable tables use TSV. Fragment files,
genome builds, annotations, and motif databases remain external inputs and
must be recorded with the analysis.
