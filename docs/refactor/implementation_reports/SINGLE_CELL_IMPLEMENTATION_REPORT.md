# Single-cell canonical template refinement report

Implementation date: 2026-08-27

Scope: `templates/single_cell/` and this report only. Original source
notebooks were not moved, renamed, deleted, or rewritten. No other analytical
family was modified.

## Refinement summary

The single-cell library now contains all 16 requested templates. Every
template is intentionally `draft`: no compatible source object, network,
resource folder, or complete method-specific runtime environment was available
for execution in the canonical form. Static parsing and contract checks are
reported below; parsing is not treated as scientific validation.

The 16 templates contain 1,989 lines in total. They are deliberately direct:
no scientific operation was moved into a helper, and no shared helper system
was introduced.

| Template | Class | Status | Lines | Primary provenance |
|---|---|---|---:|---|
| `create_object.qmd` | SOURCE-BACKED WORKFLOW | draft | 108 | Seurat object scaffold, merged with source input checks |
| `qc.qmd` | SOURCE-BACKED WORKFLOW | draft | 149 | QC scaffold, merged with source QC diagnostics |
| `doublets_scdblfinder.qmd` | SOURCE-BACKED WORKFLOW | draft | 98 | Source scDblFinder blocks |
| `normalization_log.qmd` | SOURCE-BACKED WORKFLOW | draft | 101 | Seurat normalization scaffold and source PCA route |
| `normalization_sct.qmd` | SOURCE-BACKED WORKFLOW | draft | 90 | Source SCTransform route |
| `harmony.qmd` | SOURCE-BACKED WORKFLOW | draft | 134 | Source log-normalized RunHarmony route |
| `ucell.qmd` | SOURCE-BACKED WORKFLOW | draft | 140 | Direction-aware UCell scoring |
| `cytotrace2.qmd` | SOURCE-BACKED WORKFLOW | draft | 109 | Actual CytoTRACE2 call |
| `markers_cell_level.qmd` | SOURCE-BACKED WORKFLOW | draft | 104 | Focused FindMarkers scaffold |
| `slingshot.qmd` | API / TUTORIAL REMINDER | draft | 121 | Current official Slingshot API; no source workflow existed |
| `tradeseq.qmd` | SOURCE-BACKED WORKFLOW | draft | 137 | Actual fitGAM/startVsEndTest workflow |
| `scvelo.qmd` | SOURCE-BACKED WORKFLOW | draft | 147 | Complete source scVelo workflow, current API-checked |
| `cellrank.qmd` | SOURCE-BACKED WORKFLOW | draft | 171 | Complete source CellRank2 workflow, current API-checked |
| `decoupler.qmd` | SOURCE-BACKED WORKFLOW | draft | 119 | Active Python decoupler bridge |
| `hdwgcna.qmd` | SOURCE-BACKED WORKFLOW | draft | 146 | Actual hdWGCNA network workflow |
| `sccellfie.qmd` | SOURCE-BACKED WORKFLOW | draft | 115 | Actual scCellFie computation |

Status inventory: `validated` — none; `draft` — all 16 templates; `blocked` —
none. The API/tutorial reminder is draft by design, not blocked.

Filename changes: the canonical `markers.qmd` was renamed to
`markers_cell_level.qmd`; no original source notebook was renamed. No other
canonical filename changes were made.

## Provenance classes

The following labels are used consistently in each record:

- **SOURCE-DERIVED**: executable logic directly represented in a real source
  notebook.
- **API-DERIVED**: a block written from current package documentation because
  no complete repository implementation existed for that method.
- **MERGED**: a source-backed backbone combined with a useful, non-project-
  specific block from another source or a current API adjustment.
- **PROJECT-SPECIFIC AND OMITTED**: source material intentionally excluded
  because it encodes one cohort, biological label, fixed gene list, or
  interpretation.

## Current documentation checks

Current official documentation was checked on 2026-08-27 only for minimal API
names, input/output objects, and obvious deprecations. It was not copied into
the templates and does not replace version-specific package documentation.

- [Seurat reference and v5 essential commands](https://satijalab.org/seurat/reference/index.html)
  and [qs2](https://qsbase.r-universe.dev/qs2/) support the visible R object
  access and `qs2::qs_save()`/`qs2::qs_read()` contract.
- [Slingshot manual](https://bioconductor.org/packages/release/bioc/manuals/slingshot/man/slingshot.pdf)
  supports the reduced-dimension, cluster-label, start/end, pseudotime, and
  curve-weight reminder.
- [CytoTRACE2 usage](https://github.com/digitalcytometry/cytotrace2#extended-usage-details)
  supports the current matrix orientation, species, `ncores`, seed, and score
  column names.
- [scVelo getting started](https://scvelo.readthedocs.io/en/stable/) supports
  the current preprocessing, dynamical recovery, `recover_latent_time()`,
  velocity, graph, pseudotime, and confidence calls.
- [CellRank GPCCA](https://cellrank.readthedocs.io/en/stable/api/_autosummary/estimators/cellrank.estimators.GPCCA.html)
  and [CellRank tutorials](https://cellrank.readthedocs.io/en/stable/notebooks/tutorials/estimators/600_initial_terminal.html)
  support `compute_schur()`, `compute_macrostates()`, state selection, fate
  probabilities, and lineage drivers. The older `GPCCA.fit()` path is
  deprecated in CellRank 2.1.
- [decoupler ULM](https://decoupler.readthedocs.io/en/latest/api/generated/decoupler.mt.ulm.html)
  supports the Python `dc.mt.ulm()` and `dc.pp.get_obsm()` calls.
- [scCellFie API](https://sccellfie.readthedocs.io/en/latest/api/index.html)
  supports the pipeline, grouped report, and package summary writer. That
  writer emits CSV report files; this is the one documented CSV exception to
  the canonical TSV table convention.

## Per-template implementation records

### `create_object.qmd`

- **Template class / status:** SOURCE-BACKED WORKFLOW; `draft`.
- **Canonical source:** `archive/legacy_templates/notebook_templates_v1/scRNA/01_create_seurat_object.qmd`.
- **Merge sources:** `examples/single_cell/map/00_MAP_qc_integration.qmd`,
  `examples/single_cell/map/00_MAP_RNA_qc_integration.qmd`, and
  `examples/single_cell/gse171145.qmd` for matrix/metadata alignment and
  identifier safeguards.
- **SOURCE-DERIVED blocks:** `CreateSeuratObject()` and
  `PercentageFeatureSet()` object construction.
- **API-DERIVED blocks:** none; `qs2` persistence follows the repository
  persistence contract.
- **MERGED blocks:** duplicate checks, exact cell-name matching, and explicit
  feature-by-cell orientation.
- **PROJECT-SPECIFIC AND OMITTED:** sample loops, cohort paths, fixed labels,
  Azimuth, CopyKAT, and downstream QC/integration.
- **Project-specific material removed:** MAP/C1 identifiers, fixed samples,
  biological labels, and downstream analysis.
- **Scientific decisions retained:** `min.cells = 3`, `min.features = 200`,
  assay, mitochondrial pattern, matrix orientation, and metadata alignment.
- **Practical notes retained:** feature-by-cell orientation and exact
  metadata/cell-name matching are stated visibly.
- **APIs/packages:** Seurat, readr, qs2.
- **API changes:** raw counts and the output object use `.qs2`; the source
  scaffold's analytical contract is otherwise unchanged.
- **Persistence:** input count matrix and output Seurat object use `qs2`; the
  metadata export is TSV.
- **Input contract:** one feature-by-cell count matrix in `counts.qs2` and one
  metadata TSV with one row per cell and a unique cell-ID column.
- **Output contract:** a Seurat object with aligned metadata, raw assay counts,
  `nFeature`, `nCount`, and mitochondrial percentage; metadata TSV.
- **Validation performed:** R parsing, fence balance, path/identifier scans;
  no object construction was executed.
- **Validation still required:** test a sparse matrix, duplicate identifiers,
  metadata ordering, and organism-specific mitochondrial names.
- **Unresolved decisions:** whether a future companion should support 10x
  directories; the accepted gene-identifier convention.
- **Source blocks intentionally not merged:** Azimuth, CopyKAT, sample-specific
  import loops, and downstream QC.

### `qc.qmd`

- **Template class / status:** SOURCE-BACKED WORKFLOW; `draft`.
- **Canonical sources:** `archive/legacy_templates/notebook_templates_v1/scRNA/02_quality_control.qmd`,
  `examples/single_cell/map/00_MAP_RNA_qc_integration.qmd`, and
  `examples/single_cell/map/00_MAP_qc_integration.qmd`.
- **SOURCE-DERIVED blocks:** feature/count/mitochondrial metrics, transparent
  pass flag, before/after accounting, VlnPlot diagnostics, and filtered-object
  save.
- **API-DERIVED blocks:** none.
- **MERGED blocks:** per-sample summaries and plots are combined with the fixed
  threshold baseline.
- **PROJECT-SPECIFIC AND OMITTED:** fixed sample names, MAP paths, CNV,
  annotation, LISI, and biological state interpretation.
- **Project-specific material removed:** cohort names and hard-coded biological
  conclusions.
- **Scientific decisions retained:** `nFeature`, `nCount`, mitochondrial
  fraction, explicit thresholds, missing-value handling, sample column, and
  review of before/after cell counts.
- **Practical notes retained:** inspecting distributions per sample, treating
  thresholds as transparent but non-universal, and considering several QC
  metrics with doublet results and biological context.
- **APIs/packages:** Seurat, ggplot2, readr, dplyr, qs2.
- **API changes:** the canonical output is the filtered object in `.qs2`.
  The exact MAD multiplier is not silently selected.
- **Persistence:** input and filtered Seurat objects use `qs2`; QC metadata is
  TSV; plots are PNG.
- **Input contract:** Seurat object containing the selected assay and its
  feature/count columns; a sample column is used when present.
- **Output contract:** filtered Seurat object, per-cell pass metadata, pooled
  and sample-aware QC plots where sample metadata exists.
- **Validation performed:** R parsing, fence balance, and static scans; no
  filtering was executed.
- **Validation still required:** inspect behavior on multiple samples and
  confirm thresholds before promotion.
- **Unresolved decisions:** whether a separate MAD template is warranted and
  whether filtering precedes or follows doublet calling.
- **Source blocks intentionally not merged:** ambiguous `k = 3` versus `k = 5`
  MAD policies, complex project-specific QC, CopyKAT/Azimuth, and integration.

### `doublets_scdblfinder.qmd`

- **Template class / status:** SOURCE-BACKED WORKFLOW; `draft`.
- **Canonical sources:** scDblFinder blocks in
  `examples/single_cell/map/00_MAP_RNA_qc_integration.qmd` and
  `examples/single_cell/gse171145.qmd`.
- **SOURCE-DERIVED blocks:** Seurat-to-SingleCellExperiment conversion,
  sample-aware `scDblFinder()`, class/score attachment, and per-sample counts.
- **API-DERIVED blocks:** none.
- **MERGED blocks:** explicit retention/removal policy and TSV call export.
- **PROJECT-SPECIFIC AND OMITTED:** CopyKAT, Azimuth, SCEVAN, LISI, fixed
  sample names, and biological doublet interpretation.
- **Project-specific material removed:** fixed cohorts and epithelial/C1
  conclusions.
- **Scientific decisions retained:** assay, sample/library column,
  `remove_doublets = FALSE`, doublet class, and score.
- **Practical notes retained:** calls should be conditioned on independent
  capture/loading experiments, not unrelated libraries silently pooled as one
  capture.
- **APIs/packages:** Seurat, SingleCellExperiment, scDblFinder, qs2, readr.
- **API changes:** analytical object persistence is `.qs2`.
- **Persistence:** input/output Seurat objects use `qs2`; calls are TSV.
- **Input contract:** QC-stage Seurat object with a capture/library metadata
  column.
- **Output contract:** Seurat object with `scDblFinder.class` and
  `scDblFinder.score`, optionally filtered, plus calls TSV.
- **Validation performed:** R parsing and static checks; no call was executed.
- **Validation still required:** verify current scDblFinder sample semantics,
  behavior on merged libraries, and the correct ordering for the study.
- **Unresolved decisions:** whether calls should precede or follow merging and
  whether filtering belongs in QC or this stage.
- **Source blocks intentionally not merged:** CNV, annotation, and project
  interpretation.

### `normalization_log.qmd`

- **Template class / status:** SOURCE-BACKED WORKFLOW; `draft`.
- **Canonical sources:** `archive/legacy_templates/notebook_templates_v1/scRNA/03_normalization_integration_clustering.qmd`
  plus the standard log-normalization/PCA route in the MAP workflows.
- **SOURCE-DERIVED blocks:** `NormalizeData`, `FindVariableFeatures`,
  `ScaleData`, and variable-feature diagnostics.
- **API-DERIVED blocks:** current `RunPCA` placement and named reduction
  contract.
- **MERGED blocks:** `NormalizeData -> FindVariableFeatures -> ScaleData ->
  RunPCA` as one PCA-ready stage.
- **PROJECT-SPECIFIC AND OMITTED:** batch labels, Harmony, RPCA, neighbors,
  clustering, UMAP, and biological interpretation.
- **Project-specific material removed:** fixed sample names and integration
  claims.
- **Scientific decisions retained:** assay, scale factor, feature-selection
  method/count, regression variables, and PC count.
- **Practical notes retained:** log normalization and SCTransform remain
  visibly distinct preprocessing choices.
- **APIs/packages:** Seurat, qs2, ggplot2.
- **API changes:** added explicit PCA so the output contract is genuinely
  downstream-ready; removed the old optional scaling branch because this stage
  must produce the scaled data required by its PCA contract.
- **Persistence:** input/output Seurat objects use `qs2`; variable-feature plot
  is PNG.
- **Input contract:** filtered Seurat object with the selected raw assay.
- **Output contract:** normalized assay, variable features, scaled data, and a
  named PCA reduction.
- **Validation performed:** R parsing and static checks; no object was run.
- **Validation still required:** execute PCA with and without regression
  covariates and confirm the intended assay state.
- **Unresolved decisions:** the default covariates to regress, if any.
- **Source blocks intentionally not merged:** integration, clustering, UMAP,
  and RPCA.

### `normalization_sct.qmd`

- **Template class / status:** SOURCE-BACKED WORKFLOW; `draft`.
- **Canonical source:** SCTransform route in
  `examples/single_cell/map/00_MAP_qc_integration.qmd`.
- **SOURCE-DERIVED blocks:** `SCTransform`, explicit regression variables,
  variable-feature retention, and SCT feature diagnostics.
- **API-DERIVED blocks:** current `RunPCA` placement on the SCT assay.
- **MERGED blocks:** source SCTransform call plus the PCA-ready output
  contract.
- **PROJECT-SPECIFIC AND OMITTED:** fixed samples, C1 labels, LISI,
  integration, clustering, and project interpretation.
- **Project-specific material removed:** cohort paths and biological labels.
- **Scientific decisions retained:** assay, `vars.to.regress`, variable-feature
  count, `return.only.var.genes`, and PC count.
- **Practical notes retained:** SCTransform is a scientifically distinct
  preprocessing choice, not merely faster log normalization.
- **APIs/packages:** Seurat, qs2, ggplot2.
- **API changes:** added explicit PCA and made the SCT assay/reduction contract
  visible; no universal regression formula was imposed.
- **Persistence:** input/output Seurat objects use `qs2`; plot is PNG.
- **Input contract:** filtered Seurat object with the selected raw assay and
  any metadata covariates named in `vars_to_regress`.
- **Output contract:** SCT assay, SCT variable features, and named PCA
  reduction.
- **Validation performed:** R parsing and static checks; no fit was run.
- **Validation still required:** test current Seurat/SCT behavior and assay
  selection with representative covariates.
- **Unresolved decisions:** which covariates are scientifically justified in a
  given study.
- **Source blocks intentionally not merged:** Harmony, RPCA, and clustering.

### `harmony.qmd`

- **Template class / status:** SOURCE-BACKED WORKFLOW; `draft`.
- **Canonical source:** active log-normalized `RunHarmony` route in
  `examples/single_cell/map/00_MAP_RNA_qc_integration.qmd`.
- **Merge sources:** LISI diagnostics from
  `examples/single_cell/map/00_MAP_qc_integration.qmd`.
- **SOURCE-DERIVED blocks:** PCA-based `RunHarmony`, post-Harmony neighbors,
  clustering, UMAP, and batch diagnostics.
- **API-DERIVED blocks:** current package call syntax was checked against the
  available API documentation, including the explicit PCA-based call and
  current LISI input shape; execution remains required.
- **MERGED blocks:** LISI summary/plot and the explicit PCA-ready input
  contract.
- **PROJECT-SPECIFIC AND OMITTED:** C1 interpretation, project labels, RPCA,
  SCT `IntegrateLayers` route, and project plotting.
- **Project-specific material removed:** fixed batch names and biological
  labels.
- **Scientific decisions retained:** batch column, input reduction, PC count,
  iterations, convergence plot, clustering resolution, and seed.
- **Practical notes retained:** integration must be justified and checked for
  overcorrection rather than applied automatically.
- **APIs/packages:** Seurat, harmony, lisi, qs2, readr, ggplot2.
- **API changes:** canonical persistence is `.qs2`; the template has one
  log-normalized Harmony route rather than duplicating the SCT route.
- **Persistence:** input/output Seurat objects use `qs2`; LISI is TSV and PNG.
- **Input contract:** merged Seurat object with selected assay normalized,
  scaled, and a PCA reduction containing at least `n_pcs` dimensions.
- **Output contract:** Seurat object with Harmony reduction and post-Harmony
  graph/UMAP, plus LISI table.
- **Validation performed:** R parsing and static checks; Harmony/LISI were not
  executed.
- **Validation still required:** current Harmony arguments, LISI orientation,
  and biological preservation/overcorrection diagnostics.
- **Unresolved decisions:** when to prefer the scientifically distinct SCT
  integration route.
- **Source blocks intentionally not merged:** RPCA and the SCT/Harmony branch.

### `ucell.qmd`

- **Template class / status:** SOURCE-BACKED WORKFLOW; `draft`.
- **Canonical source:** `examples/single_cell/map/01_MAP_c1_scoring.qmd`.
- **Merge sources:** `examples/single_cell/map/02_MAP_c1_scoring.qmd` and
  `examples/single_cell/map/09_MAP_C1_Core_refined_signature.qmd` for signature
  coverage and direction handling.
- **SOURCE-DERIVED blocks:** `AddModuleScore_UCell`, UP/DOWN components,
  coverage checks, and metadata attachment.
- **API-DERIVED blocks:** generic TSV signature schema.
- **MERGED blocks:** coverage, directional component scores, raw signed score,
  compact diagnostics, and optional cohort-relative composite.
- **PROJECT-SPECIFIC AND OMITTED:** C1 genes/thresholds, biological labels,
  CytoTRACE2, SCEVAN, correlations, and project evidence narrative.
- **Project-specific material removed:** C1 names and fixed gene lists.
- **Scientific decisions retained:** direction, minimum coverage, raw component
  preservation, and explicit score construction.
- **Practical notes retained:** raw UP and DOWN scores remain available before
  any transformation.
- **APIs/packages:** Seurat, UCell, qs2, readr, dplyr, ggplot2.
- **API changes:** the raw UP-minus-DOWN score is primary; dataset-relative
  z-scoring is optional and disabled by default.
- **Persistence:** input/output Seurat objects use `qs2`; coverage is TSV and
  diagnostics are PNG.
- **Input contract:** Seurat object plus TSV with `signature`, `gene`, and
  `direction` (`UP`/`DOWN`) columns.
- **Output contract:** Seurat metadata with component and directional scores,
  coverage TSV, and score diagnostic plot.
- **Validation performed:** R parsing and static checks; no score was computed.
- **Validation still required:** current UCell output column names, all-UP
  signatures, coverage policy, and optional z-score behavior.
- **Unresolved decisions:** whether smoothing belongs in a later explicit stage.
- **Source blocks intentionally not merged:** kNN smoothing and all biological
  state thresholds.

### `cytotrace2.qmd`

- **Template class / status:** SOURCE-BACKED WORKFLOW; `draft`.
- **Canonical source:** actual CytoTRACE2 call in
  `examples/single_cell/map/01_MAP_c1_scoring.qmd`.
- **Merge sources:** raw-count and alignment details from
  `examples/single_cell/map/02_MAP_c1_scoring.qmd`.
- **SOURCE-DERIVED blocks:** raw-count call, score/potency extraction, and
  cell-ID alignment.
- **API-DERIVED blocks:** validation note for the current CytoTRACE2 version,
  package resources, raw-matrix input, and returned score columns.
- **MERGED blocks:** generic species parameter, Seurat metadata attachment,
  TSV output, and reduction diagnostic.
- **PROJECT-SPECIFIC AND OMITTED:** C1 correlations, SCEVAN crosstabs, ARI,
  fixed labels, and project interpretation.
- **Project-specific material removed:** C1 and state-analysis narrative.
- **Scientific decisions retained:** raw counts, species, seed, cores, score,
  potency, and cell-ID alignment.
- **Practical notes retained:** normalized/scaled values must not be substituted
  for the raw-count input contract without checking the package.
- **APIs/packages:** Seurat, CytoTRACE2, qs2, readr, ggplot2.
- **API changes:** canonical object persistence is `.qs2`; species is exposed
  rather than made a hidden human-only assumption.
- **Persistence:** input/output Seurat objects use `qs2`; scores are TSV.
- **Input contract:** Seurat object with raw count layer and unique cell names.
- **Output contract:** object metadata with score and potency plus score TSV.
- **Validation performed:** R parsing and static checks; no CytoTRACE2 run.
- **Validation still required:** current API, species resources, count
  orientation, returned names, and resource/parallel behavior.
- **Unresolved decisions:** accepted gene identifiers and potency semantics by
  species.
- **Source blocks intentionally not merged:** C1/SCEVAN comparisons and state
  interpretation.

### `markers_cell_level.qmd`

- **Template class / status:** SOURCE-BACKED WORKFLOW; `draft`.
- **Canonical source:** focused marker scaffold
  `archive/legacy_templates/notebook_templates_v1/scRNA/05_marker_identification_and_export.qmd`.
- **Merge sources:** marker/export conventions in
  `examples/single_cell/map/03_MAP_state_markers_statistics_export.qmd`.
- **SOURCE-DERIVED blocks:** two-group `FindMarkers`, group-size accounting,
  compact DotPlot, and TSV export.
- **API-DERIVED blocks:** none.
- **MERGED blocks:** explicit test, detection, logFC, and positive-only choices.
- **PROJECT-SPECIFIC AND OMITTED:** fixed groups, project marker names,
  enrichment, and biological conclusions.
- **Project-specific material removed:** cohort names, gene lists, and pathway
  story.
- **Scientific decisions retained:** group labels, assay, test, `min.pct`,
  logFC threshold, and positive-only option.
- **Practical notes retained:** this is a cell-level exploratory comparison.
- **APIs/packages:** Seurat, qs2, readr, ggplot2.
- **API changes:** canonical input uses `.qs2`; the canonical filename is now
  `markers_cell_level.qmd`.
- **Persistence:** input Seurat object uses `qs2`; markers are TSV and plot is
  PNG.
- **Input contract:** clustered Seurat object with an explicit comparison
  column and two group labels.
- **Output contract:** marker table and compact diagnostic plot.
- **Validation performed:** R parsing and static checks; no marker test ran.
- **Validation still required:** current test defaults and interpretation with
  replicated samples.
- **Unresolved decisions:** whether a separate all-cluster marker stage is
  needed later.
- **Source blocks intentionally not merged:** pseudobulk/design-based DE,
  enrichment, and all-cluster loops.
- **Scientific warning retained:** cell-level `FindMarkers()` is not a
  substitute for sample-aware or pseudobulk inference when patients/samples
  are the biological replicates.

### `slingshot.qmd`

- **Template class / status:** API / TUTORIAL REMINDER; `draft`.
- **Canonical source:** none. The cited
  `examples/single_cell/map/04_MAP_c1_gene_programs_tradeSeq.qmd` contains no
  `slingshot()` call; it uses a continuous C1-derived score for one-lineage
  tradeSeq pseudotime.
- **Merge sources:** descriptive pseudotime scaffold only for the downstream
  handoff concept; no source Slingshot implementation was merged.
- **SOURCE-DERIVED blocks:** none.
- **API-DERIVED blocks:** current minimal `SingleCellExperiment` conversion,
  reduced-dimension assignment, `slingshot()`, `slingPseudotime()`, and
  `slingCurveWeights()` calls.
- **MERGED blocks:** none; the notebook is intentionally short.
- **PROJECT-SPECIFIC AND OMITTED:** all C1 scoring, sample names, fixed roots,
  biological endpoints, and interpretation.
- **Project-specific material removed:** no source implementation was copied.
- **Scientific decisions retained:** reduction, cluster labels, start cluster,
  terminal clusters, branching plausibility, and curve diagnostics are visible
  user decisions.
- **Practical notes retained:** pseudotime and curve weights can feed tradeSeq;
  trajectory inference and gene-level testing remain separate stages.
- **APIs/packages:** slingshot, SingleCellExperiment, Seurat, qs2, readr.
- **API changes:** all analytical code is API-derived from the current official
  Slingshot API; no claim of repository execution is made.
- **Persistence:** SCE output uses `qs2`; pseudotime and weights are TSV.
- **Input contract:** clustered Seurat object with a named reduced dimension
  and cluster column.
- **Output contract:** Slingshot SCE, pseudotime matrix, lineage/curve weights,
  and a minimal trajectory plot.
- **Validation performed:** R parsing, fence balance, and source absence check;
  no trajectory was executed.
- **Validation still required:** current Bioconductor release, SCE reduction
  naming, root/terminal behavior, and a representative curve fit. Consult the
  official package documentation and vignette before real use.
- **Unresolved decisions:** reduction choice, cluster resolution, and
  biologically defensible root/end constraints.
- **Source blocks intentionally not merged:** the project tradeSeq fit and
  descriptive pseudotime binning remain separate.

### `tradeseq.qmd`

- **Template class / status:** SOURCE-BACKED WORKFLOW; `draft`.
- **Canonical source:** actual `fitGAM()` and `startVsEndTest()` workflow in
  `examples/single_cell/map/04_MAP_c1_gene_programs_tradeSeq.qmd`.
- **Merge sources:** pseudotime input/output contract from
  `archive/legacy_templates/notebook_templates_v1/scRNA/06_trajectory_gene_programs.qmd`.
- **SOURCE-DERIVED blocks:** raw counts, one-lineage pseudotime/weights,
  expression filter, negative-binomial GAM, parallel backend, endpoint test,
  and BH correction.
- **API-DERIVED blocks:** optional `associationTest()` branch and generic
  feature-set contract.
- **MERGED blocks:** source-backed GAM with `feature_set <- NULL`, explicit
  test choice, and no universal top-2,500 cap.
- **PROJECT-SPECIFIC AND OMITTED:** C1 score creation, fixed feature lists,
  correlations, evidence unions, enrichment, and project plots.
- **Project-specific material removed:** C1 object/path and downstream story.
- **Scientific decisions retained:** count layer, minimum expressed cells,
  pseudotime/weights, knots, family, workers, and test question.
- **Practical notes retained:** endpoint testing and association along
  pseudotime are different questions.
- **APIs/packages:** Seurat, tradeSeq, BiocParallel, Matrix, qs2, readr.
- **API changes:** `feature_set = NULL` uses all genes passing the declared
  filter; the source's fixed top-2,500 variable-gene restriction is not made
  universal. Output fit uses `.qs2`.
- **Persistence:** input Seurat object and GAM fit use `qs2`; gene results are
  TSV.
- **Input contract:** Seurat object with raw counts and explicit pseudotime and
  cell-weight metadata columns aligned to count columns.
- **Output contract:** tradeSeq GAM fit and gene-level result table.
- **Validation performed:** R parsing and static checks; no GAM was fitted.
- **Validation still required:** current `fitGAM` test signatures, multi-lineage
  extension, count filtering, and platform-specific parallel backend.
- **Unresolved decisions:** whether a future canonical stage should support
  multiple lineages by default.
- **Source blocks intentionally not merged:** Slingshot inference, descriptive
  pseudotime binning, correlation, and GO/KEGG enrichment.
- **Source discrepancy:** the source title implies a Slingshot relationship,
  but the executable code does not run Slingshot.

### `scvelo.qmd`

- **Template class / status:** SOURCE-BACKED WORKFLOW; `draft`.
- **Canonical source:** complete velocity section in
  `examples/single_cell/map/07_MAP_velocity_scvelo_cellrank.qmd`.
- **Merge sources:** minimal velocity scaffold in
  `archive/legacy_templates/notebook_templates_v1/scRNA/09_velocity_scvelo_cellrank.qmd`
  and a concise upstream provenance note.
- **SOURCE-DERIVED blocks:** spliced/unspliced preprocessing, filtering,
  normalization, neighbors, moments, dynamical recovery, velocity, graph,
  pseudotime, latent time, confidence, and stream diagnostic.
- **API-DERIVED blocks:** current scVelo/Scanpy layer and representation
  checks. The current `recover_latent_time()` name and the `moments()` call
  without a representation argument were checked against current docs.
- **MERGED blocks:** explicit kinetic-layer contract, optional representation,
  h5ad persistence, and generic metadata.
- **PROJECT-SPECIFIC AND OMITTED:** barcode reconstruction, fixed Harmony
  objects, C1 labels, and project Seurat export.
- **Project-specific material removed:** cohort paths and biological labels.
- **Scientific decisions retained:** layers, filtering, top genes, neighbors,
  representation, velocity mode, jobs, and seed.
- **Practical notes retained:** integrated representation choice is separate
  from kinetic layers; dynamical velocity is distinct from stochastic or
  deterministic modes.
- **APIs/packages:** AnnData, Scanpy, scVelo, pathlib, pandas, matplotlib.
- **API changes:** custom source layer names are copied to explicit standard
  `spliced`/`unspliced` layers; the older latent-time call was replaced by
  `recover_latent_time()`, and the moments call now relies on the explicit
  neighbor graph rather than passing a representation argument. No integrated
  matrix is accepted as a kinetic layer by implication.
- **Persistence:** input/output analytical AnnData uses h5ad; metadata is TSV.
- **Input contract:** cells as observations, genes as variables, unique IDs,
  explicit aligned spliced/unspliced layers, and a representation choice.
- **Output contract:** velocity-aware h5ad with velocity graph/pseudotime,
  latent time, confidence, and metadata.
- **Validation performed:** Python AST parsing and static checks; no AnnData
  workflow executed.
- **Validation still required:** layer alignment, current dynamical API, graph
  construction, and whether the chosen representation is scientifically
  defensible.
- **Unresolved decisions:** whether neighbors should use PCA or an explicitly
  integrated representation for a particular study.
- **Source blocks intentionally not merged:** upstream simpleaf/alevin-fry
  reconstruction and project-specific barcode repair.

### `cellrank.qmd`

- **Template class / status:** SOURCE-BACKED WORKFLOW; `draft`.
- **Canonical source:** complete CellRank2 workflow in
  `examples/single_cell/map/07_MAP_velocity_scvelo_cellrank.qmd`.
- **Merge sources:** no separate scientific source; current CellRank API
  documentation was used to check the modular kernels/GPCCA structure.
- **SOURCE-DERIVED blocks:** velocity/connectivity kernels, weighted kernel
  combination, GPCCA, Schur decomposition, state prediction, fate
  probabilities, lineage drivers, and diagnostics.
- **API-DERIVED blocks:** current `compute_schur()` plus
  `compute_macrostates()` in place of deprecated `GPCCA.fit()`, explicit
  manual state-column policies, current setter/predictor branches, and the
  DataFrame return from `compute_lineage_drivers()`.
- **MERGED blocks:** h5ad input/output contract, exposed kernel weights,
  state-selection policies, and tabular fate/driver outputs.
- **PROJECT-SPECIFIC AND OMITTED:** C1 quantile roots, fixed biological state
  names, project barcode logic, and interpretation.
- **Project-specific material removed:** hard-coded initial cells and terminal
  labels.
- **Scientific decisions retained:** velocity/connectivity weights, number of
  states, cluster key, estimator method, initial/terminal policy, overlap, and
  fate solver settings.
- **Practical notes retained:** a velocity kernel alone is not fate inference;
  state selection requires model and biological review.
- **APIs/packages:** AnnData, CellRank, numpy, pandas, matplotlib, pathlib.
- **API changes:** removed the hard-coded project root rule; replaced the
  deprecated `GPCCA.fit()` call with `compute_schur()` and
  `compute_macrostates()`, and added current `predict_*`/`set_*` policy
  branches and explicit state columns.
- **Persistence:** input/output analytical AnnData uses h5ad; fate and driver
  tables are TSV.
- **Input contract:** scVelo h5ad with `Ms` and `velocity` layers, velocity
  graph, connectivity graph, embedding, and cluster column.
- **Output contract:** velocity/connectivity-informed fate probabilities,
  lineage drivers, annotated h5ad, and TSV tables.
- **Validation performed:** Python AST parsing and static checks; no CellRank
  run was possible.
- **Validation still required:** current `set_*` state formats, GPCCA state
  fitting, fate solver settings, and manual state-column behavior.
- **Unresolved decisions:** whether automatic or manually curated states should
  be the default for a particular biological system.
- **Source blocks intentionally not merged:** project-specific C1 state
  definition and biological state naming.

### `decoupler.qmd`

- **Template class / status:** SOURCE-BACKED WORKFLOW; `draft`.
- **Canonical source:** active Python bridge in
  `examples/single_cell/map/04_MAP_decoupler_bridge.qmd`.
- **Merge sources:** no deprecated R workflow was merged; current Python API
  documentation was used to check `dc.mt.ulm` and output accessors.
- **SOURCE-DERIVED blocks:** AnnData construction contract, long-format prior
  network, ULM, score/padj extraction, and network provenance.
- **API-DERIVED blocks:** current Python namespace/accessor checks.
- **MERGED blocks:** explicit source/target/weight requirement, cell-ID
  validation, and generic input/output paths.
- **PROJECT-SPECIFIC AND OMITTED:** fixed collecTRI/PROGENy biological story,
  project assay restoration, and R bridge code.
- **Project-specific material removed:** MAP/C1 network interpretation and
  fixed labels.
- **Scientific decisions retained:** cells-as-observations orientation, input
  layer, ULM method, minimum targets, network provenance, and score/padj
  storage.
- **Practical notes retained:** ULM is explicit and not silently substituted by
  MLM or GSVA.
- **APIs/packages:** AnnData, decoupler, pandas, pathlib.
- **API changes:** Python decoupler is the only promoted implementation;
  network weight is required, and deprecated R calls are omitted from the
  canonical notebook.
- **Persistence:** input/output AnnData uses h5ad; activities/padj are TSV.
- **Input contract:** cells x genes AnnData and long network TSV with
  `source`, `target`, and `weight` columns.
- **Output contract:** h5ad with decoupler results and TSV score/padj matrices.
- **Validation performed:** Python AST parsing and static deprecated-API scan;
  no network or AnnData was executed.
- **Validation still required:** current ULM namespace, `get_obsm` output
  orientation, target filtering, and network provenance.
- **Unresolved decisions:** which network and activity method are appropriate
  for a given biological question.
- **Source blocks intentionally not merged:** deprecated R `get_collectri`,
  `run_ulm`, and `run_mlm` workflows.

### `hdwgcna.qmd`

- **Template class / status:** SOURCE-BACKED WORKFLOW; `draft`.
- **Canonical source:** `examples/single_cell/map/06_MAP_coexpression_modules.qmd`.
- **Merge sources:** none required; old predefined module scoring is not a
  coexpression source.
- **SOURCE-DERIVED blocks:** variable features, metacells, metacell
  normalization, expression setup, soft-power testing, network construction,
  eigengenes, connectivity, grey-module exclusion, hub ranking, and plots.
- **API-DERIVED blocks:** generalized group-column contract and current API
  syntax checks.
- **MERGED blocks:** source cluster-focused grouping generalized visibly to
  user-controlled sample/cluster grouping.
- **PROJECT-SPECIFIC AND OMITTED:** fixed clusters, module names, enrichment,
  and biological module interpretation.
- **Project-specific material removed:** C1 and project-specific labels.
- **Scientific decisions retained:** assay/layer, variable features, metacell
  grouping, `k`, shared cells, network type, soft power, eigengene grouping,
  and hub ranking.
- **Practical notes retained:** grouping determines which cells can be
  aggregated; sample-plus-cluster grouping is a deliberate generalization of
  the source's cluster-focused policy.
- **APIs/packages:** Seurat, hdWGCNA, qs2, patchwork, ggplot2, readr.
- **API changes:** analytical persistence is `.qs2`; group columns are exposed
  rather than silently fixed to one project policy.
- **Persistence:** input/output Seurat objects use `qs2`; module/power/hub
  tables are TSV and diagnostics are PNG.
- **Input contract:** processed Seurat object with expression assay/layer,
  reduction, and declared grouping columns.
- **Output contract:** network-enriched Seurat object, module table, hub table,
  power table, and diagnostic plots.
- **Validation performed:** R parsing and static checks; no network was built.
- **Validation still required:** current hdWGCNA output columns, metacell
  grouping behavior, soft-power choice, and object size/resources.
- **Unresolved decisions:** the default grouping policy for replicated studies.
- **Source blocks intentionally not merged:** predefined AddModuleScore-style
  modules, enrichment, and project interpretation.

### `sccellfie.qmd`

- **Template class / status:** SOURCE-BACKED WORKFLOW; `draft`.
- **Canonical source:** actual pipeline in
  `examples/single_cell/map/08_MAP_metabolic_activity_scCellFie.qmd`.
- **Merge sources:** old metabolic-score importer was inspected but not used as
  the computational backbone.
- **SOURCE-DERIVED blocks:** scCellFie pipeline call, organism, count/batch/
  neighbor/threshold settings, smoothing, alpha, chunk size, report, and save.
- **API-DERIVED blocks:** current public pipeline/report call names and the
  `tissue_col` report argument were checked against the package API.
- **MERGED blocks:** generic AnnData contract and grouped report output.
- **PROJECT-SPECIFIC AND OMITTED:** MAP task lists, hand-picked plots, state
  narrative, marker-task comparisons, differential tests, and GAM analysis.
- **Project-specific material removed:** fixed task interpretation and labels.
- **Scientific decisions retained:** organism, count key, batch key, neighbor
  key/count, threshold key, smoothing, alpha, chunk size, and report grouping.
- **Practical notes retained:** outputs are metabolic-task estimates, not direct
  flux measurements.
- **APIs/packages:** AnnData, scCellFie, pathlib.
- **API changes:** canonical computation uses the real pipeline rather than
  imported precomputed scores; output is h5ad. The package summary writer's
  CSV output is retained as a documented package-output exception.
- **Persistence:** input/output analytical AnnData uses h5ad; report artifacts
  use the package's report writer, which emits its documented CSV summaries.
- **Input contract:** AnnData with count, batch, group, and neighbor metadata
  matching the named parameters.
- **Output contract:** enriched h5ad and grouped scCellFie report/summary.
- **Validation performed:** Python AST parsing and static checks; no resource
  folder or AnnData workflow was available.
- **Validation still required:** current scCellFie API, resource/data-folder
  behavior, threshold key, neighbor graph, and report generation.
- **Unresolved decisions:** whether a future template should expose a custom
  scCellFie data folder rather than the current `None` default.
- **Source blocks intentionally not merged:** imported metabolic scores and all
  project downstream testing.

## Canonical object contracts

### Core Seurat path

```text
create_object
    -> qc
    -> doublets_scdblfinder
    -> normalization_log OR normalization_sct
    -> harmony (optional)
    -> downstream single-cell methods
```

- `create_object` expects a feature-by-cell raw count matrix and exact cell-ID
  matching metadata; its Seurat object boundary is `.qs2`.
- `qc` expects the selected assay and writes the filtered Seurat object, not the
  pre-filter object. The sample column is strongly preferred for diagnostics.
- `doublets_scdblfinder` expects a capture/library-aware metadata column and
  preserves calls unless `remove_doublets` is explicitly changed.
- The log route outputs normalized data, variable features, scaled data, and a
  named PCA reduction. The SCT route outputs an SCT assay and named PCA
  reduction. Neither performs integration or clustering.
- `harmony` consumes a PCA-ready object, applies one explicit batch variable to
  PCA coordinates, and then constructs post-Harmony neighbors/clusters/UMAP.

### Trajectory path

```text
normalized / reduced object
    -> slingshot
    -> pseudotime + lineage weights
    -> tradeseq
```

`slingshot` is an API/tutorial reminder and remains `draft`; it is not a
source-backed project workflow. `tradeseq` is source-backed and consumes an
explicit pseudotime/weight contract. Slingshot inference and tradeSeq GAM
testing are intentionally separate.

### Dynamics path

```text
AnnData with kinetic spliced/unspliced layers
    -> scVelo
    -> velocity-aware AnnData
    -> CellRank
```

scVelo requires explicit kinetic layers; its moments stage adds `Ms`/`Mu`, and
CellRank consumes velocity-aware AnnData with the `Ms` and `velocity` layers.
CellRank then performs kernel/state/fate analysis. Integrated representations
may be used for neighbors or visualization only as an explicit choice, never
as a silent replacement for kinetic layers.

### Persistence contract

```text
R analytical objects     -> qs2 (.qs2)
Python AnnData objects   -> h5ad
tabular outputs          -> TSV
```

No persistence helper was added. The read/save call remains visible in each
template.

## Source-to-canonical merge graph

```text
01_create_seurat_object.qmd --------------------> create_object.qmd
02_quality_control.qmd + MAP QC -----------------> qc.qmd
MAP scDblFinder blocks --------------------------> doublets_scdblfinder.qmd
03_normalization_integration_clustering.qmd -----> normalization_log.qmd
MAP SCTransform route ---------------------------> normalization_sct.qmd
MAP active RunHarmony route + LISI --------------> harmony.qmd
01_MAP_c1_scoring + 02_MAP_c1_scoring -----------> ucell.qmd
01_MAP_c1_scoring CytoTRACE2 --------------------> cytotrace2.qmd
05_marker_identification_and_export.qmd ---------> markers_cell_level.qmd
current official Slingshot API ------------------> slingshot.qmd
04_MAP_c1_gene_programs_tradeSeq.qmd ------------> tradeseq.qmd
07_MAP_velocity_scvelo_cellrank.qmd -------------> scvelo.qmd
07_MAP_velocity_scvelo_cellrank.qmd -------------> cellrank.qmd
04_MAP_decoupler_bridge.qmd ---------------------> decoupler.qmd
06_MAP_coexpression_modules.qmd -----------------> hdwgcna.qmd
08_MAP_metabolic_activity_scCellFie.qmd ---------> sccellfie.qmd
```

The Slingshot edge is API-derived, not source-derived. The tradeSeq edge is
not evidence that the source ran Slingshot.

## Notebooks that become redundant only after successful merge

No original notebook is deleted. After execution and output comparison, the
following old scaffolds may become redundant as active template copies:

- `archive/legacy_templates/notebook_templates_v1/scRNA/01_create_seurat_object.qmd`
- `02_quality_control.qmd`
- `03_normalization_integration_clustering.qmd` (split across stages)
- `09_velocity_scvelo_cellrank.qmd` (split across scVelo and CellRank)
- the old `markers.qmd` canonical filename, now replaced by
  `markers_cell_level.qmd`.

The old `04_signature_scoring.qmd`, `06_trajectory_gene_programs.qmd`,
`07_pathway_activity_decoupler.qmd`, `08_coexpression_modules.qmd`, and
`10_metabolic_activity.qmd` remain scientifically distinct reminders or
importer stages and should not be called redundant merely because a new
workflow exists.

## Notebooks that must remain examples

The MAP project notebooks remain examples of complete biological analyses and
practical implementation choices, especially:

- `examples/single_cell/map/00_MAP_RNA_qc_integration.qmd` and
  `examples/single_cell/map/00_MAP_qc_integration.qmd` for richer QC/integration context;
- `01_MAP_c1_scoring.qmd` and related C1 scoring notebooks for project
  interpretation and signature decisions;
- `04_MAP_c1_gene_programs_tradeSeq.qmd` for the original one-lineage score
  interpretation;
- `07_MAP_velocity_scvelo_cellrank.qmd` for project-level velocity/fate
  interpretation;
- `06_MAP_coexpression_modules.qmd` and
  `08_MAP_metabolic_activity_scCellFie.qmd` for project-specific downstream
  interpretation.

## Notebooks that must remain provenance/archive

The following source material should remain available for provenance even when
the canonical templates pass validation:

- deprecated R `decoupleR` workflows, because they explain historical results
  but should not be promoted;
- project-specific barcode reconstruction and assay-restoration code;
- source notebooks containing fixed biological state thresholds, hand-picked
  gene lists, enrichment conclusions, or cohort-specific plots;
- the old metabolic-score importer and predefined-module scoring scaffold,
  because importing precomputed values and computing activity/network modules
  are distinct operations.

## Source/template discrepancies discovered

- The old QC scaffold exported filtered metadata but saved the unfiltered
  object. The canonical QC template saves `object_qc` explicitly.
- The file and surrounding language associated with Slingshot in the tradeSeq
  project notebook do not contain a Slingshot call; the source uses a
  continuous C1-derived one-lineage pseudotime.
- The source tradeSeq workflow limits itself to the first 2,500 variable genes.
  That is preserved as historical provenance, not as a universal canonical
  restriction.
- The old coexpression scaffold uses predefined module scoring and is not a
  substitute for the actual hdWGCNA network workflow.
- The old metabolic template imports scores; the actual scCellFie computation
  is in a different project notebook and is the canonical source here.
- The source CellRank workflow uses a C1-derived root rule. The canonical
  template removes it and exposes automatic or explicit state policies.
- The source velocity workflow uses Harmony coordinates for moments. The
  canonical template keeps the representation choice visible and warns that
  integrated expression is not a kinetic layer.
- `markers.qmd` was renamed to `markers_cell_level.qmd`; the original source
  notebooks were not renamed.

## Static and runtime checks

Static checks performed after refinement on 2026-08-27:

- all 16 templates have balanced Quarto fences;
- all R code blocks parse with `Rscript`;
- all Python code blocks parse with Python `ast.parse`;
- no canonical template contains an absolute user/shared-volume path;
- no canonical template contains the whole-word identifiers MAP, C1, TRENTO,
  TCGA, GSE274934, PD-L1, fixed project paths, or fixed project sample names
  (the substring `MAP` in `UMAP` is not treated as an identifier);
- no canonical template uses `readRDS()`, `saveRDS()`, `.rds`, or deprecated R
  `decoupleR` calls;
- R analytical object paths use `.qs2`, Python analytical objects use `.h5ad`,
  and tabular outputs use `.tsv` except for the documented scCellFie package
  summary writer, which emits CSV reports;
- all 16 templates explicitly state one template class and exactly one visible
  status, and all are `draft`;
- the renamed marker file exists and the old canonical `markers.qmd` file does
  not remain;
- no scientific logic was moved into helpers.

Method runtime checks were not performed. Required source objects, AnnData
files, network/resource folders, and method-specific Python packages were
unavailable; Quarto also reported that Jupyter is not installed. A temporary
`qs2::qs_save()`/`qs2::qs_read()` round-trip smoke test passed, but that does
not validate any analytical template. No template is therefore `validated`.

## Unresolved scientific issues

- QC threshold policy remains study-specific; the repository does not justify
  one MAD multiplier.
- Doublet detection must be aligned to the actual capture/library design.
- Log normalization and SCTransform remain scientifically distinct choices;
  Harmony is initially canonicalized only for the log-normalized PCA route.
- UCell coverage cutoffs and the interpretation of all-UP signatures need a
  project decision; z-scored composites remain dataset-relative.
- CytoTRACE2 package version, species resource, and identifier contract need a
  runtime check.
- Slingshot root/end constraints and reduction choice require biological
  justification; its notebook is intentionally only a reminder.
- tradeSeq multi-lineage support and the preferred primary test require a
  future decision.
- scVelo representation choice must be checked against the kinetic data
  generation process.
- CellRank automatic versus manually supplied state definitions require
  biological review and current API execution.
- decoupler network choice and ULM interpretation are question-dependent.
- hdWGCNA metacell grouping and soft-power selection need execution on a
  sufficiently sized replicated object.
- scCellFie resource/data-folder and neighbor/threshold behavior need runtime
  confirmation.
