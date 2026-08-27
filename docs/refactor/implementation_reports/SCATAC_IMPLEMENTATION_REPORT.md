# scATAC implementation report

## Scope

This checkpoint adds a shallow canonical scATAC library under
`templates/scatac/`. It preserves the real fragment-aware QC, TF-IDF/LSI, and
JASPAR/Signac motif-enrichment patterns while removing MAP sample names,
project paths, cluster labels, and biological conclusions. Original source
notebooks remain unchanged.

All five templates are currently `draft`: the source implementations were not
executed in these new canonical forms, and the chromVAR page is intentionally
an API/tutorial reminder.

## Canonical scATAC object contract

```text
peak-by-cell counts + metadata + indexed fragments + compatible annotation
    ↓
create_object.qmd
    ↓  Seurat object with ATAC ChromatinAssay; qs2
qc.qmd
    ↓  filtered object with fragment-aware QC metadata; qs2
lsi_clustering.qmd
    ↓  TF-IDF, LSI, neighbors, clusters, ATAC UMAP; qs2
    ├── motif_enrichment_findmotifs.qmd
    │       ↓ motif-enabled assay + FindMotifs TSV; qs2 + TSV
    └── chromvar.qmd
            ↓ direct chromVAR deviation-score TSV reminder
```

The ATAC assay expects peak features in rows and cells in columns. Cell IDs are
intersected deliberately between matrices and metadata; dropped IDs are
reported. Fragments must be bgzip/tabix indexed and contain the retained
barcodes. `genome_build`, peak coordinates, annotations, sequence genome, and
motif resources must be mutually compatible. R objects use qs2 and tabular
outputs use TSV.

## Provenance and template records

### `templates/scatac/create_object.qmd`

- **Class/status:** SOURCE-BACKED WORKFLOW; draft.
- **Canonical source:** `examples/single_cell/map/00_MAP_ATAC_qc_integration.qmd`.
- **Merge sources:** `archive/legacy_templates/notebook_templates_v1/scATAC/01_create_signac_object.qmd` and Seurat/Signac object-contract documentation.
- **SOURCE-DERIVED:** peak matrix orientation, `CreateChromatinAssay`, `CreateSeuratObject`, `sep = c(":", "-")`, `hg38` example, fragments, annotation, `min.cells`, and cell-level object checks.
- **API-DERIVED:** explicit `CreateFragmentObject` construction and current qs2/API spelling where the source passed the fragment path directly.
- **MERGED:** source object construction plus explicit barcode intersection/alignment reporting.
- **PROJECT-SPECIFIC AND OMITTED:** Cell Ranger sample loops, MAP/GSE identifiers, downstream QC, Harmony, Azimuth, CopyKAT, and project paths.
- **Scientific decisions retained:** matrix orientation, valid genome/build choice, peak separators, fragment validation, cell matching, and feature/cell minimums.
- **Practical notes retained:** do not silently repair barcode mismatches; preserve an alignment table.
- **Input contract:** qs2 matrix, metadata TSV with `cell_id`, indexed fragments, qs2 gene annotation.
- **Output contract:** Seurat object with one ATAC `ChromatinAssay`, aligned metadata, fragments, annotation, and a creation summary.
- **Persistence:** object qs2; alignment/summary TSV.
- **API changes:** fragment-object construction made explicit; no source notebook changed.
- **Validation performed:** R package/API signature inspection and static parsing.
- **Validation still required:** representative fragment-backed object creation and qs2 round trip with a compatible genome/annotation.
- **Unresolved decisions:** whether future users will supply sparse matrices, HDF5 matrices, or Cell Ranger metrics directly; not expanded here.

### `templates/scatac/qc.qmd`

- **Class/status:** SOURCE-BACKED WORKFLOW; draft.
- **Canonical source:** `examples/single_cell/map/00_MAP_ATAC_qc_integration.qmd`.
- **Merge sources:** `archive/legacy_templates/notebook_templates_v1/scATAC/02_quality_control_integration.qmd`.
- **SOURCE-DERIVED:** passed filters, peak-region fragments, FRiP, blacklist ratio, peak counts, nucleosome signal, TSS enrichment, per-sample QC, explicit failure logic, plots, and before/after counts.
- **API-DERIVED:** current direct `NucleosomeSignal`/`TSSEnrichment` calls and explicit metric alignment.
- **MERGED:** Cell Ranger-style metrics plus Signac metrics in one compact canonical object flow.
- **PROJECT-SPECIFIC AND OMITTED:** AL05/AL08/AL10/AL11/AL12 loops, MAP outputs, fixed project directories, and study conclusions.
- **Scientific decisions retained:** all thresholds are visible; default values mirror the active source but are labeled non-universal; sample-wise inspection is retained.
- **Practical notes retained:** inspect several metrics together, inspect per sample, investigate outliers, and consider doublets alongside QC.
- **Input contract:** created Seurat object, metrics TSV with required fragment columns, and a valid fragment index.
- **Output contract:** filtered Seurat object only, QC metadata, per-cell/per-sample tables, and a QC distribution PDF.
- **Persistence:** filtered object qs2; summaries TSV.
- **API changes:** no MAD multiplier canonized; direct current Signac calls replace the source `ATACqc`/fragtk helper for the baseline notebook.
- **Validation performed:** source tracing, API signature inspection, and static parsing.
- **Validation still required:** representative fragment-aware QC execution, especially `TSSEnrichment`, and confirmation of metric names on the intended Signac version.
- **Unresolved decisions:** exact sample-specific or MAD thresholds; source contained project-specific values and competing distribution policies.

### `templates/scatac/lsi_clustering.qmd`

- **Class/status:** SOURCE-BACKED WORKFLOW; draft.
- **Canonical source:** `examples/single_cell/map/00_MAP_ATAC_qc_integration.qmd` LSI section.
- **Merge sources:** `archive/legacy_templates/notebook_templates_v1/scATAC/02_quality_control_integration.qmd`.
- **SOURCE-DERIVED:** TF-IDF → `FindTopFeatures` → `RunSVD` → LSI UMAP/neighbors/clustering and `q5` feature cutoff.
- **API-DERIVED:** explicit graph naming, current `DepthCor`, neighbor, cluster, and UMAP argument spelling.
- **MERGED:** source LSI path with a visible dimension vector and depth-correlation diagnostic.
- **PROJECT-SPECIFIC AND OMITTED:** GSE274934 names, Harmony, resolution scans, silhouette-specific project analysis, and study interpretation.
- **Scientific decisions retained:** top-feature cutoff, SVD dimensions, neighbor k, clustering resolution, UMAP seed, and dimension selection.
- **Practical notes retained:** inspect LSI1 against depth/QC; do not call TF-IDF/LSI integration or discard LSI1 automatically.
- **Input contract:** filtered ATAC Seurat object with valid ChromatinAssay.
- **Output contract:** object with TF-IDF data, LSI, ATAC neighbors, clusters, and ATAC UMAP.
- **Persistence:** object qs2; embeddings/cluster tables TSV.
- **API changes:** graph names and explicit seed added for a reusable handoff.
- **Validation performed:** API signature inspection and static parsing.
- **Validation still required:** representative execution and review of dimension/depth diagnostics.
- **Unresolved decisions:** final dimensions and clustering resolution are dataset-specific.

### `templates/scatac/motif_enrichment_findmotifs.qmd`

- **Class/status:** SOURCE-BACKED WORKFLOW; draft.
- **Canonical source:** `examples/single_cell/map/002_ATAC_MOTIF.qmd`.
- **Merge sources:** `archive/legacy_templates/notebook_templates_v1/scATAC/03_motif_enrichment.qmd` and current Signac/JASPAR API checks.
- **SOURCE-DERIVED:** JASPAR2024, TFBSTools PFM retrieval, CORE vertebrate/human selection, hg38 BSgenome, `AddMotifs`, `FindMotifs`, and `MotifPlot`.
- **API-DERIVED:** explicit foreground/background TSV contract and current namespace-qualified calls.
- **MERGED:** real motif setup plus explicit external peak-set definitions and TSV export.
- **PROJECT-SPECIFIC AND OMITTED:** AT1/AT2 labels, MAP/GSE identifiers, selected TEAD4/APOBEC interpretation, and project-specific peak filters.
- **Scientific decisions retained:** database/version, taxon, build, foreground, background, adjustment method, and motif plotting count.
- **Practical notes retained:** build compatibility and distinction between enrichment and cell-level motif deviation.
- **Input contract:** motif-ready-compatible Seurat object, foreground/background peak TSVs, and compatible hg38/JASPAR resources.
- **Output contract:** motif-enabled object, enrichment table, and minimal motif plot.
- **Persistence:** object qs2; results TSV.
- **API changes:** current JASPAR2024 constructor/TFBSTools call retained; explicit DB disconnect added.
- **Validation performed:** source/API inspection and static parsing.
- **Validation still required:** real motif matching against compatible peak ranges and a representative `FindMotifs` run.
- **Unresolved decisions:** foreground selection and background universe are intentionally left to the upstream study design.

### `templates/scatac/chromvar.qmd`

- **Class/status:** API / TUTORIAL REMINDER; draft.
- **Canonical source:** none; no complete `RunChromVAR` implementation was found in the source repository.
- **Merge sources:** current Signac/chromVAR documentation and local API inspection.
- **SOURCE-DERIVED:** none.
- **API-DERIVED:** direct `chromVAR::computeDeviations`, `deviationScores`, and Signac motif-data access; the installed Signac 1.17.1 namespace does not export `RunChromVAR`.
- **MERGED:** none.
- **PROJECT-SPECIFIC AND OMITTED:** all project motif/state interpretations and any full regulatory program workflow.
- **Scientific decisions retained:** motif-enabled input, counts layer, annotation orientation, genome/background compatibility, and score interpretation.
- **Practical notes retained:** motif deviation is not proof of binding or causal regulation.
- **Input contract:** qs2 Seurat object with motif-enabled ATAC assay.
- **Output contract:** chromVAR deviation-score TSV; no canonical object rewrite is attempted.
- **Persistence:** TSV scores; input object remains qs2.
- **API changes:** used direct chromVAR API because the expected Signac wrapper is not exported in the verified local version.
- **Validation performed:** local package export/signature inspection, official chromVAR API lookup, and static parsing.
- **Validation still required:** run on a representative motif-enabled object and confirm the current Signac motif-data orientation.
- **Unresolved decisions:** current wrapper/storage conventions may vary by Signac version; consult official docs before real use.

## Validation summary

- Quarto fences and R blocks were statically checked after creation.
- Local package versions/API signatures were inspected: Seurat 5.5.1, Signac
  1.17.1, chromVAR 1.34.1, JASPAR2024 0.99.7, TFBSTools 1.50.0,
  BSgenome.Hsapiens.UCSC.hg38 1.4.5, and qs2 0.3.1.
- No representative fragment/genome fixture was available; no biologically
  invalid synthetic fragment execution was claimed.
- All templates remain draft. Syntax/API checks are not analytical validation.
