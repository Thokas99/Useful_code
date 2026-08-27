# Multiome implementation report

## Scope

This checkpoint adds four canonical paired RNA/ATAC templates under
`templates/multiome/`. They preserve the repository's real object creation,
WNN, peak–gene linkage, and RNA-to-ATAC transfer patterns while removing
project paths, sample names, fixed state labels, and biological conclusions.
Original source notebooks remain unchanged.

All four templates are `SOURCE-BACKED WORKFLOW` and remain `draft`: the source
implementations were not executed in these generalized canonical forms.

## Canonical multiome object contract

```text
matched RNA counts + ATAC peak counts + metadata + fragments + build annotation
    ↓
create_object.qmd
    ↓ paired Seurat object with RNA and ATAC assays; qs2
wnn.qmd
    ↓ RNA PCA + ATAC LSI + weighted neighbors + WNN UMAP/clusters; qs2
    ├── rna_atac_linkage.qmd
    │       ↓ LinkPeaks links + optional CoveragePlot; qs2 + TSV
    └── rna_to_atac_label_transfer.qmd
            ↓ GeneActivity query + directional predictions; qs2 + TSV
```

The RNA and ATAC assays must have identical retained cell IDs. The ATAC assay
requires indexed fragments, compatible peak coordinates, annotation, and an
explicit genome build. WNN uses separate RNA PCA and ATAC LSI reductions; it is
not batch correction. LinkPeaks is statistical peak–gene evidence, not causal
enhancer proof. Label transfer is directional RNA reference → ATAC query, and
GeneActivity is an accessibility-derived proxy rather than measured RNA.

R analytical objects use qs2; tables use TSV.

## Provenance and template records

### `templates/multiome/create_object.qmd`

- **Class/status:** SOURCE-BACKED WORKFLOW; draft.
- **Canonical source:** `CODE_MAP/code_MAP/notebook_templates/multiome/01_create_multiome_object.qmd`.
- **Merge sources:** Seurat multimodal object examples, `CODE_MAP/code_MAP/00_MAP_ATAC_qc_integration.qmd`, and current Signac object APIs.
- **SOURCE-DERIVED:** RNA/ATAC assay construction, `CreateChromatinAssay`, fragments, metadata, genome, and initial checks.
- **API-DERIVED:** explicit `CreateFragmentObject`, current assay/object namespaces, and current qs2 format.
- **MERGED:** paired matrix alignment and dropped-cell reporting added to the source scaffold.
- **PROJECT-SPECIFIC AND OMITTED:** MAP/GSE identifiers, sample loops, downstream QC, and fixed biological labels.
- **Scientific decisions retained:** assay names, feature orientation, peak separator, genome/build, fragments, annotation, exact cell matching, and the decision to defer cell filtering to QC.
- **Practical notes retained:** unmatched modality barcodes are reported and intersected, never silently unioned.
- **RNA contract:** qs2 gene-by-cell matrix.
- **ATAC contract:** qs2 peak-by-cell matrix, indexed fragments, and compatible annotation/build.
- **Output contract:** paired Seurat object with RNA and ATAC assays and identical cell names.
- **Persistence:** object qs2; alignment/summary TSV.
- **API changes:** direct current ChromatinAssay insertion is retained; no extra assay wrapper is introduced.
- **Validation performed:** source tracing, current API signature inspection, and static parsing.
- **Validation still required:** representative paired object creation with real fragments and build-compatible annotations.
- **Unresolved decisions:** whether future inputs should support 10x HDF5 directly; not expanded here.

### `templates/multiome/wnn.qmd`

- **Class/status:** SOURCE-BACKED WORKFLOW; draft.
- **Canonical source:** `CODE_MAP/code_MAP/notebook_templates/multiome/02_qc_integration_wnn.qmd`.
- **Merge sources:** current Seurat `FindMultiModalNeighbors`/WNN API and scATAC LSI source.
- **SOURCE-DERIVED:** RNA normalization/PCA, ATAC TF-IDF/SVD, WNN graph construction, UMAP, and graph clustering.
- **API-DERIVED:** explicit current WNN graph/reduction names, k, dimensions, resolution, and seed.
- **MERGED:** source WNN flow without duplicating modality QC, plus an explicit non-batch-correction warning.
- **PROJECT-SPECIFIC AND OMITTED:** sample/group names, project plots, and fixed output directories.
- **Scientific decisions retained:** assay roles, separate reductions, dimensions, k, graph names, resolution, and seed.
- **Practical notes retained:** inspect LSI1/depth before changing ATAC dimensions.
- **Input contract:** paired Seurat object from create_object with RNA and ATAC assays.
- **Output contract:** RNA PCA, ATAC LSI, weighted neighbors, WNN UMAP, and WNN graph-based clusters.
- **Persistence:** object qs2; metadata/cluster TSV.
- **API changes:** no Harmony/RPCA integration added; current `FindMultiModalNeighbors` names verified locally.
- **Validation performed:** source/API inspection and static parsing.
- **Validation still required:** representative execution with adequate paired cells and review of modality weights/batch structure.
- **Unresolved decisions:** reduction dimensions and resolution remain dataset-specific.

### `templates/multiome/rna_atac_linkage.qmd`

- **Class/status:** SOURCE-BACKED WORKFLOW; draft.
- **Canonical source:** `CODE_MAP/code_MAP/notebook_templates/multiome/03_rna_atac_linkage.qmd`.
- **Merge sources:** current Signac `LinkPeaks`, `Links`, and `CoveragePlot` API inspection.
- **SOURCE-DERIVED:** LinkPeaks call, explicit RNA/ATAC assays, distance parameter, links extraction, CoveragePlot pattern, and TSV export.
- **API-DERIVED:** explicit gene coordinate object and current namespace-qualified accessors.
- **MERGED:** source linkage flow plus explicit build/distance/model contract and optional region plotting.
- **PROJECT-SPECIFIC AND OMITTED:** fixed genes, project state labels, and hard-coded biological regions.
- **Scientific decisions retained:** gene coordinates, assay roles, distance, minimum cells, correlation method, and optional gene subset.
- **Practical notes retained:** peak–gene links are statistical evidence and depend on coordinate compatibility.
- **Input contract:** WNN-capable paired object, qs2 gene-coordinate `GRanges`, normalized RNA data, and ATAC counts/fragments.
- **Output contract:** object with Signac links plus link TSV and optional CoveragePlot.
- **Persistence:** updated object qs2; links TSV.
- **API changes:** current `Links(object[[atac_assay]])` and `LinkPeaks` argument names verified locally.
- **Validation performed:** source/API inspection and static parsing.
- **Validation still required:** representative LinkPeaks run with suitable gene coordinates and expression normalization.
- **Unresolved decisions:** distance, score/p-value interpretation, and gene universe should follow the study design.

### `templates/multiome/rna_to_atac_label_transfer.qmd`

- **Class/status:** SOURCE-BACKED WORKFLOW; draft.
- **Canonical source:** `CODE_MAP/code_MAP/001_RNA_ATAC_LT.qmd`.
- **Merge sources:** `CODE_MAP/code_MAP/notebook_templates/multiome/01_create_multiome_object.qmd` and current Seurat/Signac APIs.
- **SOURCE-DERIVED:** GeneActivity, query ACTIVITY assay, normalization/scaling, RPCA anchors, LSI-weighted TransferData, metadata attachment, and qs2 save.
- **API-DERIVED:** current `CreateAssay5Object`, explicit feature overlap, prediction TSV export, and current Seurat transfer signatures.
- **MERGED:** real label-transfer flow plus directional input contracts and retained confidence output.
- **PROJECT-SPECIFIC AND OMITTED:** GSE274934 objects, `predicted.ann_finest_level`, fixed state names, and project plots.
- **Scientific decisions retained:** reference/query roles, GeneActivity feature set, RPCA transfer, anchor dimensions, weight reduction/dimensions, and label column.
- **Practical notes retained:** confidence diagnostics are retained without inventing an acceptance cutoff; GeneActivity is not RNA.
- **Input contract:** RNA reference with a label column and variable features; ATAC query with fragments and LSI reduction.
- **Output contract:** annotated ATAC query with prediction metadata and a full prediction table.
- **Persistence:** annotated query qs2; prediction TSV.
- **API changes:** source `CreateAssayObject` replaced by current `SeuratObject::CreateAssay5Object`; current transfer signatures verified.
- **Validation performed:** source/API inspection and static parsing.
- **Validation still required:** representative GeneActivity, RPCA-anchor, transfer, and cell-ID/prediction alignment execution.
- **Unresolved decisions:** label ontology, reference compatibility, and confidence review thresholds remain study-specific.

## Validation summary

- Quarto fences and extracted R blocks were statically checked after creation.
- Local package/API signatures were inspected for Seurat 5.5.1, Signac 1.17.1,
  SeuratObject, and qs2.
- No representative paired fragment/genome fixture was available; no
  biologically invalid synthetic multiome execution was claimed.
- All templates remain draft. Syntax/API checks are not analytical validation.
