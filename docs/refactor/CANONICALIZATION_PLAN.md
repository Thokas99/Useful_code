# Scientific canonicalization plan

Audit date: 2026-08-26

This is a second-level scientific comparison of the existing notebooks. It is a planning document only. No source file, directory, archive, or notebook was moved, renamed, deleted, rewritten, or converted.

The ranking below is based on implemented scientific content, diagnostics, explicitness, reproducibility, and generalizability. It is not based on filename order, notebook length, or the apparent cleanliness of notebook_templates.

## Scope and ranking rules

The repository contains:

- 18 scaffolded notebooks under code_MAP/notebook_templates;
- complete or nearly complete project workflows under code_MAP/code_MAP;
- live and cleaned MOFA workflows under code_MOFA;
- a complete TRENTO modeling notebook and a separate TRENTO reporting notebook;
- a proteomics/network analysis inside Task for 2nd interview.zip;
- historical copies in Archive.zip.

The current template scaffold is useful for identifying stages and output contracts, but it is not automatically the preferred source. In several families, a project notebook contains the real implementation while the current template is only an importer, summary, or method stub.

Classification used in the tables:

- CANONICAL BACKBONE: the implementation to refactor first.
- MERGE SOURCE: unique useful code to incorporate into the backbone.
- ALTERNATIVE METHOD: scientifically distinct and retained separately.
- EXAMPLE / PROVENANCE: useful biological or project context, not generic core.
- DEPRECATED: do not promote without replacing the obsolete component.
- REDUNDANT: functionality fully represented elsewhere, but only after the indicated merge succeeds.

Confidence describes confidence in the proposed ranking, not whether the future template has already been validated.

## 1. Single-cell core

### 1.1 Seurat object creation

| Method | Candidate source files | Canonical backbone | Merge sources | Unique functionality to preserve | Functionality to remove | Deprecated components | Scientifically distinct alternatives | Proposed canonical template name | Confidence | Validation required |
|---|---|---|---|---|---|---|---|---|---|---|
| Minimal RNA object creation | code_MAP/notebook_templates/scRNA/01_create_seurat_object.qmd | CANONICAL BACKBONE. Focused stage with count matrix, metadata validation, mitochondrial percentage, and qs2 save. | code_MAP/00_MAP_qc_integration.qmd; code_MAP/00_MAP_RNA_qc_integration.qmd; code_MAP/GSE171145.qmd for raw-input and metadata patterns. | Explicit cell-ID checks, metadata alignment, min.cells and min.features settings, object contract. | Project paths, fixed sample names, and unrelated downstream QC. | None established. | Per-sample raw 10x assembly in the MAP notebooks; barcode remapping in GSE171145. | single_cell/create_seurat_object.qmd | High | Test matrix orientation, duplicate cell IDs, missing metadata, empty cells, qs2 round trip, and Seurat version behavior. |
| Per-sample assembly and merge | code_MAP/00_MAP_RNA_qc_integration.qmd; code_MAP/00_MAP_qc_integration.qmd; code_MAP/GSE171145.qmd | MERGE SOURCE, not a separate generic backbone. The project notebooks contain more complete sample-wise assembly than the scaffold. | scRNA/01 for a minimal final object contract; 01_MAP_metadata_bridge.qmd for sample metadata checks. | Per-sample QC-before-merge pattern, sample labels, barcode/sample provenance, merge diagnostics. | Cohort-specific paths, Azimuth/CopyKAT, and project-specific sample lists. | None. | Single combined matrix input is simpler and remains the default. | Optional single_cell/create_seurat_object_per_sample.qmd | Medium | Verify whether QC must precede merge, whether barcode uniqueness is guaranteed, and whether the future template accepts raw 10x directories. |
| ATAC assay construction | code_MAP/notebook_templates/scATAC/01_create_signac_object.qmd; code_MAP/notebook_templates/multiome/01_create_multiome_object.qmd | CANONICAL BACKBONE for the focused Signac/multiome stages, with the paired-assay template kept separate. | code_MAP/00_MAP_ATAC_qc_integration.qmd; code_MAP/001_RNA_ATAC_LT.qmd for fragment and GeneActivity contracts. | Fragment path, separator, genome, cell-ID intersection, ChromatinAssay, and initial Signac QC. | Placeholder genome and project-specific paths. | None established. | Multiome paired RNA+ATAC object construction is distinct from standalone scATAC. | scatac/create_signac_object.qmd and multiome/create_object.qmd | High | Test fragments, genome assembly, cell-ID coverage, peak naming, assay names, and object reload. |

### 1.2 QC and doublet handling

| Method | Candidate source files | Canonical backbone | Merge sources | Unique functionality to preserve | Functionality to remove | Deprecated components | Scientifically distinct alternatives | Proposed canonical template name | Confidence | Validation required |
|---|---|---|---|---|---|---|---|---|---|---|
| Basic scRNA QC thresholds | code_MAP/notebook_templates/scRNA/02_quality_control.qmd | MERGE SOURCE. It is readable and exposes thresholds, but it currently saves object rather than filtered. | code_MAP/00_MAP_RNA_qc_integration.qmd; code_MAP/00_MAP_qc_integration.qmd for diagnostic plots and per-sample QC. | Explicit nFeature and mitochondrial thresholds, QC flag, metadata export, before/after summaries. | The save-target mismatch, unused options, and generic claims that imply universal thresholds. | None. | MAD-derived thresholds in project notebooks; these should remain an alternative policy. | single_cell/quality_control_fixed_thresholds.qmd | Medium | Confirm filtered-object persistence, threshold semantics, NA handling, per-sample summaries, and doublet ordering. |
| QC with project-level MAD thresholds | code_MAP/00_MAP_qc_integration.qmd; code_MAP/00_MAP_RNA_qc_integration.qmd | MERGE SOURCE for an optional robust-QC stage. The MAP RNA workflow has the strongest diagnostic context, while the other notebook has explicit MAD logic. | scRNA/02 for minimal output and QC flag contract. | Per-sample distributions, MAD cutoffs, correlation/PCA diagnostics, and explicit QC plots. | Project-specific sample names, hard-coded paths, downstream C1 interpretation. | None, but check any old Seurat accessors during extraction. | Fixed thresholds are easier to copy and should remain a distinct baseline. | single_cell/quality_control_mad.qmd | Medium | Resolve k=3 versus active mad_multiplier=5, define direction per metric, test small groups, and document undefined thresholds. |
| Doublet detection | code_MAP/00_MAP_qc_integration.qmd; code_MAP/00_MAP_RNA_qc_integration.qmd; code_MAP/GSE171145.qmd | CANONICAL BACKBONE should be a separate method-specific stage derived from the most complete scDblFinder usage in the project workflows. | scRNA/02 for QC flag/persistence conventions; project metadata bridge for sample labels. | Explicit doublet calls, per-sample execution, doublet rate summaries, and exclusion accounting. | CopyKAT/Azimuth and biological interpretation from the surrounding projects. | None established. | DoubletFinder-like legacy approaches are not documented as a supported implementation here; do not add them without source evidence. | single_cell/doublet_detection_scdblfinder.qmd | Medium | Confirm package/API version, whether calls are per sample or after merge, expected assay/input, and interaction with QC thresholds. |
| scATAC QC | code_MAP/code_MAP/00_MAP_ATAC_qc_integration.qmd | CANONICAL BACKBONE for scATAC QC because it has fragment-aware diagnostics, per-sample plots, and explicit thresholds. | notebook_templates/scATAC/02_quality_control_integration.qmd for compact TF-IDF/LSI/clustering stage; scATAC/01 for object contract. | TSS enrichment, nucleosome signal, fragments/passed filters, fraction in peaks, blacklist ratio, per-sample QC tables. | Project-specific five-sample paths, inactive later integration scaffolding, and fixed thresholds as universal defaults. | None established. | Minimal template thresholds are a separate lightweight approach, not a replacement. | scatac/quality_control.qmd | High | Confirm Signac version, fragment metric definitions, threshold provenance, per-sample versus merged filtering, and output object. |

### 1.3 Normalization, reduction, clustering, and UMAP

| Method | Candidate source files | Canonical backbone | Merge sources | Unique functionality to preserve | Functionality to remove | Deprecated components | Scientifically distinct alternatives | Proposed canonical template name | Confidence | Validation required |
|---|---|---|---|---|---|---|---|---|---|---|
| Log-normalization plus PCA/neighbors/clustering/UMAP | code_MAP/notebook_templates/scRNA/03_normalization_integration_clustering.qmd; code_MAP/00_MAP_RNA_qc_integration.qmd | CANONICAL BACKBONE should start from scRNA/03 because the stage is focused and visible, after removing the false integration claim. | MAP RNA workflow for explicit seeds, dimensional diagnostics, and export; scRNA/02 for filtered-object input. | NormalizeData, variable features, ScaleData, PCA, neighbor graph, resolution, UMAP, and visible dimensions. | Unused batch_column and any automatic integration implied by the name. | None established. | SCTransform is scientifically distinct, not a drop-in API update. | single_cell/normalization_reduction_clustering_log.qmd | High | Test assay/layer behavior, variable-feature selection, dimensions, resolution, seed, and object persistence. |
| SCTransform processing | code_MAP/00_MAP_qc_integration.qmd | ALTERNATIVE METHOD and strong source for a separate SCTransform template. | MAP RNA QC for per-sample preprocessing and project diagnostics. | Per-sample SCTransform, SCT assay use, PCA, and explicit assay choice. | Harmony, LISI, and C1 biological outputs from the example. | None established. | Log-normalized workflow remains the simpler baseline. | single_cell/normalization_reduction_clustering_sct.qmd | High | Validate Seurat v5 assay/layer behavior, regression variables, per-sample versus merged SCT, and memory use. |
| LSI reduction and clustering | code_MAP/notebook_templates/scATAC/02_quality_control_integration.qmd; code_MAP/code_MAP/00_MAP_ATAC_qc_integration.qmd | CANONICAL BACKBONE is scATAC/02 for the compact TF-IDF, top-feature, SVD, graph, cluster, and UMAP stage, with project QC merged first. | MAP ATAC for strict QC diagnostics, consensus peak context, and export. | RunTFIDF, FindTopFeatures, RunSVD, exclusion of LSI dimension 1 where justified, graph construction, clustering, UMAP. | The word integration when no integration is called, and inactive downstream branches. | None established. | ATAC batch integration is separate. | scatac/lsi_reduction_clustering.qmd | High | Confirm Signac dimensions, TF-IDF defaults, LSI dimension exclusion, graph names, resolution, and object reload. |
| Multiome WNN | code_MAP/notebook_templates/multiome/02_qc_integration_wnn.qmd; code_MAP/code_MAP/00_MAP_qc_integration.qmd if the mapped multiome branch is retained | CANONICAL BACKBONE is multiome/02 for WNN because it explicitly runs RNA PCA and ATAC LSI then FindMultiModalNeighbors. | multiome/01 for paired-assay input; MAP workflows for modality-specific QC. | Separate modality reductions, dims.list, weighted nearest neighbors, weighted UMAP, wsnn clustering. | Batch-integration wording and any assumption that WNN removes batch effects. | None established. | Harmony/RPCA batch correction is distinct and may precede or accompany WNN only by explicit choice. | multiome/wnn.qmd | High | Test matched cells, modality-specific reductions, dimensions, graph names, and whether WNN is used for clustering or visualization only. |

### 1.4 Harmony and RPCA integration

| Method | Candidate source files | Canonical backbone | Merge sources | Unique functionality to preserve | Functionality to remove | Deprecated components | Scientifically distinct alternatives | Proposed canonical template name | Confidence | Validation required |
|---|---|---|---|---|---|---|---|---|---|---|
| Harmony on SCTransform | code_MAP/00_MAP_qc_integration.qmd | CANONICAL BACKBONE for a Harmony/SCT example because it has a complete route, explicit seed, LISI diagnostics, and downstream graph construction. | code_MAP/00_MAP_RNA_qc_integration.qmd for comparison of log-normalized Harmony; scRNA/03 for a clean pre-integration stage. | HarmonyIntegration/RunHarmony settings, batch variable, LISI before/after diagnostics, graph and UMAP use. | Optional RPCA branch, project C1 labels, and project-specific QC. | None established; validate current Harmony/Seurat API. | Log-normalized Harmony is scientifically distinct. | single_cell/batch_integration_harmony_sct.qmd | High | Compare pre/post integration metrics, preserve biological structure, validate assay/layer API, batch variable, seed, and overcorrection risk. |
| Harmony on log-normalized RNA | code_MAP/00_MAP_RNA_qc_integration.qmd | ALTERNATIVE METHOD. It is a complete project implementation but uses a different normalization/assay contract. | scRNA/03 for visible log normalization; MAP QC for diagnostics. | Explicit log-normalized assay, Harmony reduction, annotation-compatible output. | Azimuth, CopyKAT, CNV, and project interpretation. | None established. | SCTransform/Harmony must remain separate. | single_cell/batch_integration_harmony_log.qmd | Medium | Validate normalization scale, assay used by Harmony, batch variable, and biological preservation. |
| RPCA integration | code_MAP/00_MAP_qc_integration.qmd optional IntegrateLayers branch; code_MAP/001_RNA_ATAC_LT.qmd uses RPCA for transfer anchors | ALTERNATIVE METHOD, not yet a strong canonical backbone. The optional integration branch is not demonstrated as the preferred executed result; the label-transfer use of RPCA is a different operation. | scRNA/03 for pre-integration; MAP RNA/RPCA code only after extracting a verified integration branch. | RPCA reduction/anchors, explicit integration dimensions, and distinction between integration and transfer. | “Try” branches left executable alongside Harmony; project-specific labels. | None established. | Harmony is the current better-supported backbone in this repository. | single_cell/batch_integration_rpca.qmd | Low to medium | Render the isolated branch, verify Seurat version/API, compare against Harmony, and establish intended use for small versus large datasets. |
| Seurat v5 IntegrateLayers | code_MAP/00_MAP_qc_integration.qmd optional branch | DEPRECATED AS A CANONICAL SOURCE only in the sense of being unverified here, not because the API is deprecated. Keep as source evidence, not active default. | None until runtime-tested. | Current Seurat v5 layer-aware integration syntax if it works. | Unexecuted exploratory branch. | No package deprecation established; status is unvalidated, not obsolete. | Harmony and RPCA. | Not a separate template until validated | Low | Direct render and output comparison required before promotion. |

### 1.5 Annotation and label transfer

| Method | Candidate source files | Canonical backbone | Merge sources | Unique functionality to preserve | Functionality to remove | Deprecated components | Scientifically distinct alternatives | Proposed canonical template name | Confidence | Validation required |
|---|---|---|---|---|---|---|---|---|---|---|
| Anchor-based RNA-to-ATAC label transfer | code_MAP/001_RNA_ATAC_LT.qmd | CANONICAL BACKBONE for a focused label-transfer template because it actually computes GeneActivity, anchors, TransferData predictions, and exports results. | multiome/01 for paired assay/object contract; multiome/03 for linked RNA/ATAC context. | GeneActivity assay, RPCA anchors, transfer predictions, score/max-score handling, RNA-to-ATAC direction. | GSE274934 paths and project labels. | None established. | Azimuth and SingleR are not interchangeable. | multiome/rna_to_atac_label_transfer.qmd | High | Validate reference/query direction, assay/layer inputs, gene activity settings, prediction coverage, and held-out/reference controls. |
| Azimuth reference annotation | code_MAP/00_MAP_RNA_qc_integration.qmd; code_MAP/GSE171145.qmd | ALTERNATIVE METHOD and example source. | MAP QC and object assembly for input contract. | Reference selection, mapping diagnostics, and annotation confidence. | Cohort-specific reference and downstream CopyKAT interpretation. | None established. | Anchor transfer and SingleR. | single_cell/annotation_azimuth.qmd | Medium | Confirm reference version, species/tissue match, assay normalization, and label confidence. |
| SingleR annotation | code_MAP/00_MAP_qc_integration.qmd | ALTERNATIVE METHOD and example source. | scRNA object/QC and per-sample metadata. | Reference-based annotation, per-cell labels, and marker/reference diagnostics if present. | Project-specific labels and LISI/C1 outputs. | None established. | Azimuth and anchor transfer. | single_cell/annotation_singler.qmd | Medium | Confirm reference dataset/version, normalized input, labels, and reproducibility across package versions. |

## 2. Cell-state analysis

### 2.1 AddModuleScore and predefined gene-module scoring

| Method | Candidate source files | Canonical backbone | Merge sources | Unique functionality to preserve | Functionality to remove | Deprecated components | Scientifically distinct alternatives | Proposed canonical template name | Confidence | Validation required |
|---|---|---|---|---|---|---|---|---|---|---|
| Seurat AddModuleScore | code_MAP/notebook_templates/scRNA/04_signature_scoring.qmd; code_MAP/notebook_templates/scRNA/08_coexpression_modules.qmd; code_MAP/notebook_templates/multiome/04_regulatory_programs.qmd | CANONICAL BACKBONE is scRNA/04 because it is the clearest focused implementation. | scRNA/08 and multiome/04 for multiple modules/programs, coverage checks, and assay-specific storage. | Signature TSV input, gene intersection, coverage reporting, score attachment, export, and explicit grouping. | Claims of coexpression, regulatory inference, or pathway inference when only AddModuleScore is used. | None established. | UCell, singscore, GSVA, decoupler, and scCellFie are distinct. | single_cell/signature_scoring_addmodulescore.qmd | High | Test feature coverage, duplicate genes, assay selection, control-feature behavior, and score reproducibility. |
| Predefined module score import/attachment | code_MAP/notebook_templates/scRNA/08_coexpression_modules.qmd; code_MAP/notebook_templates/multiome/04_regulatory_programs.qmd | MERGE SOURCE only for a named gene-module scoring stage. | scRNA/04 for the generic input/export contract. | Multiple modules, program labels, module-to-gene parsing, and score summaries. | “Coexpression” and “regulatory program” claims. | None. | Actual hdWGCNA and decoupler activity. | single_cell/gene_module_scoring.qmd | High | Verify module format, missing genes, minimum coverage, assay, and metadata naming. |

### 2.2 UCell

| Method | Candidate source files | Canonical backbone | Merge sources | Unique functionality to preserve | Functionality to remove | Deprecated components | Scientifically distinct alternatives | Proposed canonical template name | Confidence | Validation required |
|---|---|---|---|---|---|---|---|---|---|---|
| UCell single-cell signature scoring | code_MAP/01_MAP_c1_scoring.qmd; code_MAP/02_MAP_c1_scoring.qmd; code_MAP/09_MAP_C1_Core_refined_signature.qmd | CANONICAL BACKBONE should be derived from 01_MAP_c1_scoring.qmd because it contains the most complete explicit UCell up/down workflow and coverage checks. | 02_MAP_c1_scoring for simpler score transformations; 09 for score validation and evidence reporting. | UP/DOWN scoring, direction-aware score formula, raw versus transformed score, signature coverage, sample/cluster summaries. | C1 names, kNN smoothing, project-specific evidence union, and unrelated state analyses in the generic template. | None established. | AddModuleScore, singscore, and GSVA must remain distinct. | single_cell/signature_scoring_ucell_up_down.qmd | Medium to high | Generalize signature schema, test absent/partial signatures, check assay/layer choice, evaluate smoothing as optional, and compare known controls. |

### 2.3 CytoTRACE2

| Method | Candidate source files | Canonical backbone | Merge sources | Unique functionality to preserve | Functionality to remove | Deprecated components | Scientifically distinct alternatives | Proposed canonical template name | Confidence | Validation required |
|---|---|---|---|---|---|---|---|---|---|---|
| CytoTRACE2 potency/state scoring | code_MAP/01_MAP_c1_scoring.qmd; code_MAP/code_MAP/07_MAP_velocity_scvelo_cellrank.qmd contains downstream CytoTRACE2 visualization/metadata use | CANONICAL BACKBONE should be extracted from the actual CytoTRACE2 computation in 01_MAP_c1_scoring.qmd, not from the current template scaffold. It is a required candidate for the future library. | 07_MAP_velocity_scvelo_cellrank.qmd for AnnData metadata alignment and joint visualization; 09_MAP_C1_Core_refined_signature.qmd for cautious state interpretation. | Explicit CytoTRACE2 run, input expression contract, potency output, cell-ID alignment, and comparison to state/signature scores. | C1-specific interpretation, velocity plots, and project-specific thresholds. | None established; package version and API need pinning. | UCell, cell-cycle, SCEVAN/CopyKAT, and velocity answer different questions. | single_cell/cell_state_cytotrace2.qmd | Medium | Identify the exact CytoTRACE2 API and input scale, test sparse/dense matrices, confirm species/gene identifiers, seed behavior, runtime, and interpretation of potency versus differentiation. |

### 2.4 Cell cycle and CNV/state analysis

| Method | Candidate source files | Canonical backbone | Merge sources | Unique functionality to preserve | Functionality to remove | Deprecated components | Scientifically distinct alternatives | Proposed canonical template name | Confidence | Validation required |
|---|---|---|---|---|---|---|---|---|---|---|
| Cell-cycle scoring | code_MAP/01_MAP_c1_scoring.qmd; code_MAP/00_MAP_RNA_qc_integration.qmd where cell-cycle variables are used in processing | MERGE SOURCE; no focused notebook exists. The most explicit scoring block appears in 01_MAP_c1_scoring.qmd. | scRNA object/QC and signature input contracts. | S and G2M scores, phase calls, optional regression decision, and reporting. | C1 biological narrative and project-only plots. | None established. | Cell cycle is a state covariate, not a general signature score or batch variable by default. | single_cell/cell_cycle_scoring.qmd | Medium | Confirm gene lists, assay/scale, whether regression is used, and whether phase is descriptive or a modeling covariate. |
| SCEVAN CNV/state analysis | code_MAP/01_MAP_c1_scoring.qmd; code_MAP/00_MAP_RNA_qc_integration.qmd may contain related CNV context | ALTERNATIVE METHOD / EXAMPLE. SCEVAN is a distinct CNV/state method and is not a generic cell-state score. | object/QC and annotation contracts; 09 for state interpretation only. | SCEVAN calls, malignant/CNV state output, and comparison with epithelial state. | Project-specific C1 labels and downstream evidence aggregation. | None established; verify current package support. | CopyKAT in GSE171145 and MAP RNA is a scientifically distinct CNV approach. | single_cell/cnv_scevan.qmd only if needed | Low to medium | Verify exact SCEVAN input, reference/normal-cell assumptions, genome/gene ordering, output interpretation, and reproducibility. |
| CopyKAT CNV analysis | code_MAP/00_MAP_RNA_qc_integration.qmd; code_MAP/GSE171145.qmd | ALTERNATIVE METHOD / EXAMPLE. It is complete in project workflows but should not be merged with SCEVAN. | per-sample QC, sample labels, and object persistence. | Per-sample CopyKAT settings, epithelial masking, aneuploid/diploid labels, and QC. | Cohort-specific malignant-cell interpretation. | None established; old but valid project method pending version check. | SCEVAN. | single_cell/cnv_copykat.qmd only if both methods are intentionally supported | Medium | Confirm CopyKAT version, reference cells, chromosome parameters, cell-number limits, and biological validation. |

## 3. Trajectory and dynamics

### 3.1 Slingshot, tradeSeq, and pseudotime

| Method | Candidate source files | Canonical backbone | Merge sources | Unique functionality to preserve | Functionality to remove | Deprecated components | Scientifically distinct alternatives | Proposed canonical template name | Confidence | Validation required |
|---|---|---|---|---|---|---|---|---|---|---|
| Slingshot trajectory inference | code_MAP/04_MAP_c1_gene_programs_tradeSeq.qmd | CANONICAL BACKBONE. This is the repository's strongest source for a real trajectory workflow and must outrank the minimal scaffold. | scRNA/06 for input/output conventions and descriptive pseudotime summaries. | Reduced-dimension input, cluster labels, lineage selection, pseudotime, lineage diagnostics, and explicit C1-derived ordering where scientifically justified. | C1-specific lineage names and project-only gene lists in the generic version. | None established. | Other trajectory methods are not represented and should not be silently added. | single_cell/trajectory_slingshot.qmd | High | Reproduce lineage construction, assess sensitivity to clusters/reduction, inspect disconnected paths, define root/terminal assumptions, and validate pseudotime stability. |
| tradeSeq GAM testing | code_MAP/04_MAP_c1_gene_programs_tradeSeq.qmd | CANONICAL BACKBONE. The notebook actually fits tradeSeq GAMs and runs association tests. | scRNA/06 for a compact pseudotime summary; 03_MAP_state_markers_statistics_export.qmd for export/enrichment conventions. | fitGAM, association tests, FDR, lineage/pseudotime plotting, Spearman evidence, and gene-set enrichment. | Fixed C1 score, one project lineage, and evidence-union narrative from the generic core. | None established; validate tradeSeq and Slingshot versions. | Descriptive pseudotime summaries do not replace tradeSeq. | single_cell/trajectory_tradeseq.qmd | High | Check counts versus normalized input, knots, ncores, cell-number limits, lineage weights, model diagnostics, multiple testing, and reproducibility. |
| Descriptive pseudotime summaries | code_MAP/notebook_templates/scRNA/06_trajectory_gene_programs.qmd | ALTERNATIVE METHOD, not a trajectory-inference backbone. | 04_MAP_c1_gene_programs_tradeSeq.qmd for pseudotime fields and gene-summary ideas. | Feature binning, grouped means, selected-feature visualization, and an explicit requirement that pseudotime already exists. | The terms trajectory and tradeSeq when no inference/model is run. | None. | Slingshot and tradeSeq. | single_cell/pseudotime_feature_summary.qmd | High | Test pseudotime ordering, missing values, bin counts, duplicate cells, and whether summaries are appropriate for branches. |

### 3.2 scVelo and CellRank

| Method | Candidate source files | Canonical backbone | Merge sources | Unique functionality to preserve | Functionality to remove | Deprecated components | Scientifically distinct alternatives | Proposed canonical template name | Confidence | Validation required |
|---|---|---|---|---|---|---|---|---|---|---|
| scVelo preprocessing and dynamical velocity | code_MAP/code_MAP/07_MAP_velocity_scvelo_cellrank.qmd; code_MAP/notebook_templates/scRNA/09_velocity_scvelo_cellrank.qmd; CODE_MAP/alevin_fry/scripts/run_simpleaf_velocity.sh | CANONICAL BACKBONE is project 07 because it rebuilds spliced/unspliced layers, aligns velocity data, uses dynamical mode, computes latent time/pseudotime/confidence, and runs diagnostics. | scRNA/09 for a minimal compact flow; alevin_fry script for upstream quantification provenance. | Spliced/unspliced reconstruction, barcode fixes, dynamical model, moments, velocity graph, latent time, confidence, PAGA, and export back to Seurat. | MAP-specific sample maps, fixed paths, C1 plots, and downstream story interpretation. | None established; pin scVelo and AnnData versions. | Slingshot/tradeSeq are not substitutes for RNA velocity. | single_cell/velocity_scvelo.qmd | High | Validate layer construction, gene/cell alignment, loom/h5ad contract, model mode, neighbor settings, diagnostics, and resource requirements. |
| Minimal scVelo diagnostic | code_MAP/notebook_templates/scRNA/09_velocity_scvelo_cellrank.qmd | MERGE SOURCE for a lightweight optional diagnostic, not the primary complete workflow. | Project 07 for layer alignment and output checks. | Minimal moments, velocity, graph, pseudotime, and kernel setup. | Claim of complete CellRank analysis; unused seed and incomplete fate outputs. | None established. | Full project velocity workflow. | single_cell/velocity_scvelo_minimal.qmd | Medium | Verify that the minimal input contains valid spliced/unspliced layers and document what cannot be inferred from the output. |
| CellRank transition kernel | code_MAP/code_MAP/07_MAP_velocity_scvelo_cellrank.qmd; code_MAP/notebook_templates/scRNA/09_velocity_scvelo_cellrank.qmd | CANONICAL BACKBONE should be extracted from project 07, but only as a separate CellRank stage after scVelo. | Minimal template for kernel setup; project exports for metadata. | VelocityKernel, transition matrix, macrostates, fate probabilities, terminal states, and driver analysis where actually present in project 07. | Treating a transition matrix alone as fate inference; project-specific C1 interpretation. | None established; validate CellRank2 API and estimator choices. | scVelo-only diagnostic. | single_cell/cellrank_fate_inference.qmd | Medium to high | Confirm kernel assumptions, estimator, terminal-state selection, fate probabilities, driver statistics, and reproducibility under current CellRank2. |

## 4. Regulatory and pathway activity

### 4.1 decoupler, decoupleR, TF activity, and pathway activity

| Method | Candidate source files | Canonical backbone | Merge sources | Unique functionality to preserve | Functionality to remove | Deprecated components | Scientifically distinct alternatives | Proposed canonical template name | Confidence | Validation required |
|---|---|---|---|---|---|---|---|---|---|---|
| Python decoupler ULM bridge | code_MAP/04_MAP_decoupler_bridge.qmd | CANONICAL BACKBONE. It is the actual cross-language implementation and is the target direction for future regulatory activity. | code_MAP/05_MAP_regulatory_programs.qmd for downstream score interpretation; scRNA/07 only for score-table attachment conventions. | Stable R-to-AnnData payload, Python decoupler ULM for TF/pathway networks, score-table export, R assay restoration, and ID validation. | GSE274934 paths, C1-specific naming, and broad regulatory interpretation inside the bridge. | R decoupleR code should not be copied into the target implementation. | GSVA, singscore, and AddModuleScore are different score families. | single_cell/regulatory_activity_decoupler_python.qmd | High | Pin Python decoupler/API, network source/version, input scale, matrix orientation, cell IDs, ULM parameters, and R/Python round trip. |
| R decoupleR ULM | code_MAP/GSE171145.qmd uses library(decoupleR), get_collectri, and run_ulm; code_MAP/09_MAP_C1_Core_refined_signature.qmd consumes decoupleR-derived output | DEPRECATED. Retain as source/provenance only; do not promote as the target implementation. | Preserve downstream metadata/interpretation ideas only after replacing the scoring engine with Python decoupler. | Collectri network selection and ULM conceptual parameters may inform the Python target. | R package calls, project-specific SCT matrix assumptions, and unvalidated output equivalence. | DEPRECATED PACKAGE: R decoupleR per the task instruction. DEPRECATED APIs: R get_collectri/run_ulm usage in these notebooks for future canonical work. | Python decoupler ULM is the target; not necessarily numerically identical. | Not a canonical template; replace with regulatory_activity_decoupler_python.qmd | High for deprecation classification | Verify Python replacement against a small controlled matrix and document any score-scale or network differences. |
| R decoupleR MLM | code_MOFA/01_TCGA_LUAD_scoring_tf.qmd uses decoupleR::get_collectri and decoupleR::run_mlm | DEPRECATED. Keep the TCGA notebook as project provenance, not as a source for a new R implementation. | MOFA input/export only if needed; Python decoupler bridge for replacement. | MLM conceptual setup, minsize, and TF network provenance. | TCGA-specific RNA matrix and R package calls. | DEPRECATED PACKAGE/API as above. | Python decoupler ULM or another explicitly chosen Python method; ULM versus MLM is also a scientific method choice. | No direct canonical template; evaluate a named decoupler method first | High | Compare ULM versus MLM assumptions and outputs; do not claim equivalence from a language migration. |
| Imported activity scores | code_MAP/notebook_templates/scRNA/07_pathway_activity_decoupler.qmd | ALTERNATIVE SUPPORTING STAGE, not an activity-computation backbone. | Python bridge outputs and multiome assay-storage blocks. | Cell-ID validation, metadata attachment, and downstream reuse of precomputed scores. | “Pathway activity with Decoupler” when no decoupler call occurs. | None in the importer itself; its name should not imply the deprecated R package. | Actual Python decoupler computation. | single_cell/import_activity_scores.qmd | High | Test complete versus partial cell coverage, duplicate score columns, score orientation, and provenance metadata. |
| TF activity interpretation | code_MAP/05_MAP_regulatory_programs.qmd; code_MAP/09_MAP_C1_Core_refined_signature.qmd | MERGE SOURCE after Python decoupler scores are produced; not a computation backbone. | code_MAP/04_MAP_decoupler_bridge.qmd for score storage and network provenance. | Correlation with state scores, TF ranking, driver tables, and cautious interpretation. | Project-specific C1 evidence claims and all fixed output paths. | Any R decoupleR-derived input must be replaced or explicitly labeled legacy. | TF activity versus gene-set score versus motif activity. | single_cell/regulatory_activity_interpretation.qmd | Medium | Validate score provenance, multiple testing, correlation assumptions, and independence of interpretation from the training/definition data. |
| Generic pathway activity | code_MAP/04_MAP_decoupler_bridge.qmd; code_MAP/00_CPTAC_LUAD_scoring; code_MAP/HALLMARK_50.qmd | No single universal backbone. Python decoupler is the target for network-based activity; GSVA and singscore remain separate methods. | Activity importer and project summaries. | Named network, score matrix, pathway coverage, and grouping summaries. | One generic “pathway activity” abstraction covering all methods. | R decoupleR portions are deprecated for new work. | GSVA, singscore, GSEA, AddModuleScore, and scCellFie. | separate templates by method: regulatory_activity_decoupler_python.qmd, pathway_scoring_gsva.qmd, pathway_scoring_singscore.qmd | High | Validate pathway database/version, gene overlap, score scale, normalization, and method-specific interpretation. |

### 4.2 GSVA and enrichment distinction

| Method | Candidate source files | Canonical backbone | Merge sources | Unique functionality to preserve | Functionality to remove | Deprecated components | Scientifically distinct alternatives | Proposed canonical template name | Confidence | Validation required |
|---|---|---|---|---|---|---|---|---|---|---|
| GSVA/ssGSEA-style per-sample scoring | code_MAP/00_CPTAC_LUAD_scoring | CANONICAL BACKBONE for GSVA because it actually compares singscore and GSVA on an expression matrix. | code_MAP/HALLMARK_50.qmd for Hallmark coverage and reporting; rnaseq normalization guidance. | Matrix transformation, gene-set coverage, per-sample scores, and method comparison. | CPTAC identifiers, fixed score names, and downstream project models. | None established, but GSVA API is version-sensitive. | singscore, GSEA, decoupler, and AddModuleScore. | bulk_rna/pathway_scoring_gsva.qmd | Medium | Pin GSVA version/API, verify input scale and orientation, inspect gene-set overlap, and compare score stability. |
| Ranked GSEA | code_MAP/GSEA_of_DEGs.qmd | ALTERNATIVE METHOD and canonical source for a GSEA template. It is not interchangeable with GSVA or per-cell scoring. | 03_MAP_state_markers_statistics_export.qmd for enrichment/export conventions. | Ranking score, GO/KEGG gene-set enrichment, simplify, term similarity, and visualization. | OVC-specific contrast and fixed file paths. | None established. | GSVA and singscore. | bulk_rna/gsea_ranked_degs.qmd | High | Validate ranking statistic, universe/background, gene IDs, duplicate genes, minGSSize, multiple testing, and interpretation. |

## 5. Coexpression and gene modules

| Method | Candidate source files | Canonical backbone | Merge sources | Unique functionality to preserve | Functionality to remove | Deprecated components | Scientifically distinct alternatives | Proposed canonical template name | Confidence | Validation required |
|---|---|---|---|---|---|---|---|---|---|---|
| hdWGCNA network/module inference | code_MAP/06_MAP_coexpression_modules.qmd | CANONICAL BACKBONE. This is the only genuine coexpression/network implementation in the repository. | code_MAP/09_MAP_C1_Core_refined_signature.qmd for hub-gene evidence; scRNA/08 only for downstream module-score presentation. | Metacells, soft-threshold selection, network construction, module eigengenes, connectivity, hub genes, module scores, and enrichment. | C1-specific module names, fixed sample structure, and large interpretation story in the generic core. | None established; dependency/API version must be checked. | Predefined AddModuleScore module scoring is not coexpression. | single_cell/coexpression_hdWGCNA.qmd | High | Validate metacell construction, sample independence, soft-threshold diagnostics, network type, module reproducibility, hub criteria, and memory use. |
| Predefined gene-module scoring | code_MAP/notebook_templates/scRNA/08_coexpression_modules.qmd; code_MAP/notebook_templates/multiome/04_regulatory_programs.qmd | ALTERNATIVE METHOD. It should remain a lightweight gene-module scoring template and should not be merged into hdWGCNA. | scRNA/04 for AddModuleScore input/coverage; MAP 06 only for downstream comparison. | Simple module file, coverage, score attachment, and UMAP summary. | Coexpression/network terminology and inferred-module claims. | None. | hdWGCNA. | single_cell/gene_module_scoring.qmd | High | Validate module coverage and make the distinction from inferred modules explicit in title and documentation. |

## 6. Metabolic analysis

| Method | Candidate source files | Canonical backbone | Merge sources | Unique functionality to preserve | Functionality to remove | Deprecated components | Scientifically distinct alternatives | Proposed canonical template name | Confidence | Validation required |
|---|---|---|---|---|---|---|---|---|---|---|
| scCellFie metabolic activity computation | code_MAP/08_MAP_metabolic_activity_scCellFie.qmd | CANONICAL BACKBONE. It actually imports sccellfie, runs the pipeline, saves enriched AnnData, and generates grouped reports. | scRNA/10_metabolic_activity.qmd for compact score attachment and visualization patterns; project velocity notebook for AnnData input contract. | Explicit scCellFie run, batch key, threshold key, metabolic-task output, cluster summaries, and cautious non-flux interpretation. | MAP-specific integrated object path, C1 state narrative, and fixed report names. | None established; verify current sccellfie API. | Imported metabolic scores are a separate interoperability stage. | single_cell/metabolic_activity_sccellfie.qmd | High | Validate input layers, gene identifiers, batch handling, threshold semantics, task database/version, output object, and biological interpretation. |
| Imported metabolic scores | code_MAP/notebook_templates/scRNA/10_metabolic_activity.qmd | ALTERNATIVE SUPPORTING STAGE, not the computational backbone. | scCellFie output table/object from the real implementation. | Reindexing by cell IDs, score attachment, UMAP, and summaries. | Claim that the notebook performs metabolic analysis or scCellFie. | None. | Actual scCellFie computation. | single_cell/import_metabolic_scores.qmd | High | Validate complete ID coverage, score orientation, and provenance of the upstream computation. |

## 7. scATAC-seq

### 7.1 Signac object, QC, TF-IDF, LSI, and clustering

| Method | Candidate source files | Canonical backbone | Merge sources | Unique functionality to preserve | Functionality to remove | Deprecated components | Scientifically distinct alternatives | Proposed canonical template name | Confidence | Validation required |
|---|---|---|---|---|---|---|---|---|---|---|
| Signac object creation | code_MAP/notebook_templates/scATAC/01_create_signac_object.qmd; code_MAP/code_MAP/00_MAP_ATAC_qc_integration.qmd | CANONICAL BACKBONE starts from the focused template, strengthened with project fragment checks. | MAP ATAC for fragment-aware QC and explicit file contracts. | CreateChromatinAssay, fragments, genome, metadata alignment, NucleosomeSignal, TSSEnrichment. | Placeholder genome, project paths, and assumptions about peak separators. | None established. | Multiome object creation is distinct. | scatac/create_signac_object.qmd | High | Test genome assembly, fragment index, peak naming, cell IDs, and assay/layer APIs. |
| Fragment-aware scATAC QC | code_MAP/code_MAP/00_MAP_ATAC_qc_integration.qmd | CANONICAL BACKBONE, as above. | scATAC/02 for downstream reduction; scATAC/01 for initial object. | Per-sample thresholds for peak counts, passed filters, fraction reads in peaks, blacklist, nucleosome, TSS, QC CSVs and plots. | Fixed five-sample policy and later inactive integration/label-transfer blocks. | None established. | Minimal threshold scaffold. | scatac/quality_control.qmd | High | Validate every metric, thresholds, per-sample filtering order, and whether thresholds are data-driven or fixed. |
| TF-IDF/LSI/clustering | code_MAP/notebook_templates/scATAC/02_quality_control_integration.qmd; code_MAP/code_MAP/00_MAP_ATAC_qc_integration.qmd | CANONICAL BACKBONE is the focused TF-IDF/LSI stage, with MAP QC merged before it. | MAP ATAC for diagnostics and consensus peak context. | TF-IDF, top features, SVD, LSI dimensions, neighbors, clusters, UMAP. | “Integration” wording where no batch integration is present. | None established. | Separate scATAC batch integration. | scatac/lsi_reduction_clustering.qmd | High | Test Signac version, dimensions, graph names, clustering algorithm/resolution, and peak matrix scale. |

### 7.2 Motif enrichment, chromVAR, and label transfer

| Method | Candidate source files | Canonical backbone | Merge sources | Unique functionality to preserve | Functionality to remove | Deprecated components | Scientifically distinct alternatives | Proposed canonical template name | Confidence | Validation required |
|---|---|---|---|---|---|---|---|---|---|---|
| Signac FindMotifs enrichment | code_MAP/002_ATAC_MOTIF.qmd; code_MAP/notebook_templates/scATAC/03_motif_enrichment.qmd | CANONICAL BACKBONE is 002_ATAC_MOTIF.qmd because it uses an explicit hg38/JASPAR2024/TFBSTools configuration and performs DA-peak-driven motif enrichment. | scATAC/03 for user-config/output structure; MAP ATAC for peak universe and QC. | PFM/database provenance, DA peak thresholds, FindMotifs, MotifPlot, and explicit peak universe. | GSE274934 paths and fixed threshold values as universal defaults. | None established. | chromVAR activity is distinct. | scatac/motif_enrichment_findmotifs.qmd | High | Validate genome/PFM matching, peak naming, background peaks, DA test, multiple testing, database version, and motif interpretation. |
| chromVAR motif activity | No confirmed RunChromVAR implementation found in the audited notebooks | NO BACKBONE. Do not claim a chromVAR template from scATAC/03. | None; 002 motif/database setup may inform a future source. | None currently established. | “ChromVAR-style” language in the scaffold. | No deprecated package identified; this is an absent implementation, not a deprecated one. | FindMotifs enrichment. | Add only after a real chromVAR implementation is available | None | Require a complete tested notebook with motif deviations, bias correction, and object storage. |
| RNA-to-ATAC label transfer | code_MAP/001_RNA_ATAC_LT.qmd | CANONICAL BACKBONE for the cross-modality transfer stage, classified under multiome rather than generic motif analysis. | multiome/01 and scATAC object/QC. | GeneActivity, anchor transfer, prediction scores, and validation checks. | Project cohort paths and biological label claims. | None established. | Azimuth/SingleR annotation and motif enrichment. | multiome/rna_to_atac_label_transfer.qmd | High | Confirm reference/query roles, shared features, GeneActivity settings, and label-transfer controls. |

## 8. Multiome

| Method | Candidate source files | Canonical backbone | Merge sources | Unique functionality to preserve | Functionality to remove | Deprecated components | Scientifically distinct alternatives | Proposed canonical template name | Confidence | Validation required |
|---|---|---|---|---|---|---|---|---|---|---|
| Paired RNA+ATAC object creation | code_MAP/notebook_templates/multiome/01_create_multiome_object.qmd | CANONICAL BACKBONE. It is a focused paired-assay construction stage with shared cell-ID validation. | scATAC/01; MAP ATAC and 001_RNA_ATAC_LT for fragment/GeneActivity conventions. | RNA/ATAC matrix alignment, ChromatinAssay, fragments, metadata, and initial modality QC. | Placeholder genome and project paths. | None established. | Separate standalone RNA or ATAC objects. | multiome/create_object.qmd | High | Test cell-ID intersection, assay names, matrix orientation, genome, fragments, and object reload. |
| WNN | code_MAP/notebook_templates/multiome/02_qc_integration_wnn.qmd | CANONICAL BACKBONE. It directly implements multimodal neighbor construction. | multiome/01 for object; scATAC/02 and scRNA/03 for modality-specific preprocessing. | RNA PCA, ATAC LSI, dims.list, weighted.nn, wsnn, UMAP, and clusters. | Batch-integration title and any claim that WNN corrects batch effects. | None established. | Harmony/RPCA integration. | multiome/wnn.qmd | High | Validate reductions, modality weighting, graph names, dimensions, and sensitivity to modality quality. |
| RNA/ATAC linkage | code_MAP/notebook_templates/multiome/03_rna_atac_linkage.qmd | CANONICAL BACKBONE. LinkPeaks is a genuine standalone stage. | 001_RNA_ATAC_LT.qmd for RNA/ATAC alignment concepts; multiome/01 for object contract. | LinkPeaks, distance, expression/peak assays, Links export, and CoveragePlot. | Generic placeholder genome and project-specific feature assumptions. | None established. | Label transfer is distinct from cis-linkage. | multiome/rna_atac_linkage.qmd | High | Validate assay/layer choices, distance, covariates, cell number, peak/gene identifiers, and link reproducibility. |
| Regulatory analysis on multiome | code_MAP/notebook_templates/multiome/04_regulatory_programs.qmd; code_MAP/04_MAP_decoupler_bridge.qmd; code_MAP/05_MAP_regulatory_programs.qmd | CANONICAL BACKBONE should be a composition of separate stages: Python decoupler for activity, LinkPeaks for cis-links, and explicit RNA module scoring if desired. No one current file is a complete generic regulatory analysis. | multiome/04 for simple RNA program scores; decoupler bridge for TF/pathway activity; multiome/03 for links; MAP 05 for interpretation. | Separate assay provenance, linked peaks, TF/pathway activity, and program summaries. | Claim that multiome/04 combines all regulatory evidence; project C1 story. | R decoupleR sections remain legacy. | RNA-only program scoring and motif enrichment. | multiome/regulatory_analysis_composed.qmd, or separate stages | Medium | Define whether “regulatory program” means score, motif, linkage, or integrated evidence; validate all assay and network contracts. |

## 9. Bulk RNA-seq

### 9.1 tximport, edgeR QC/normalization, and differential expression

| Method | Candidate source files | Canonical backbone | Merge sources | Unique functionality to preserve | Functionality to remove | Deprecated components | Scientifically distinct alternatives | Proposed canonical template name | Confidence | Validation required |
|---|---|---|---|---|---|---|---|---|---|---|
| tximport-to-edgeR input | code_MAP/simple_QC_MGI_organoids.qmd | CANONICAL BACKBONE for bulk input/QC because it uses DGEListFromTximport and makes count/object handling visible. | rnaseq_normalization_cheatsheet.md for input distinctions; MOFA helper for TMMwsp details only after making them visible. | tximport provenance, DGEListFromTximport, gene cleanup, all-zero filtering, sample metadata checks. | MGI/IEO paths, organoid-specific labels, and unrelated plots. | None established. | Raw count matrix input is a separate simpler contract. | bulk_rna/tximport_edgeR_input.qmd | High | Verify tximport object structure, effective lengths, gene duplication policy, metadata alignment, and count scale. |
| edgeR QC/normalization | code_MAP/simple_QC_MGI_organoids.qmd; CODE_MAP/rnaseq_normalization_cheatsheet.md | CANONICAL BACKBONE is simple_QC_MGI_organoids.qmd, with the cheatsheet as documentation. | Project QC plots, correlation/PCA/PAM diagnostics; explicitly expose helper logic from MOFA only as code, not as a hidden function. | DGEList, TMMwsp, CPM/logCPM, library size, detected genes, MAD/outlier flags, correlation, PCA, clustering. | Project file paths, duplicate report prose, and inconsistent filters. | None established. | DESeq2/limma-voom are not present as complete workflows; do not invent a merged choice. | bulk_rna/qc_normalization_edgeR.qmd | High | Resolve >1 versus >5 CPM paths, number of samples, filter direction, normalization order, outlier policy, and output scale. |
| Bulk differential expression | No complete generic bulk DE notebook identified. GSEA_of_DEGs.qmd consumes DEG results; edgeR glmQLFit appears in other project contexts but not as a complete source here. | NO BACKBONE. Do not create or infer a canonical DE template from GSEA. | rnaseq_normalization_cheatsheet.md; GSEA_of_DEGs only for downstream result contract. | None sufficient for a complete reusable implementation. | Do not treat GSEA input as a DE implementation. | None established. | edgeR, limma-voom, and DESeq2 would be scientifically distinct choices. | Reserve bulk_rna/differential_expression/ until a complete source is selected | None | Require design, replication, dispersion, contrasts, filtering, batch/covariate policy, and result diagnostics. |

### 9.2 GSEA, singscore, and GSVA

| Method | Candidate source files | Canonical backbone | Merge sources | Unique functionality to preserve | Functionality to remove | Deprecated components | Scientifically distinct alternatives | Proposed canonical template name | Confidence | Validation required |
|---|---|---|---|---|---|---|---|---|---|---|
| Ranked GO/KEGG GSEA | code_MAP/GSEA_of_DEGs.qmd | CANONICAL BACKBONE for a ranked enrichment template. | code_MAP/03_MAP_state_markers_statistics_export.qmd for marker/enrichment table conventions. | Ranking statistic, gseGO, gseKEGG, simplify, term similarity, and plots. | OVC-specific contrast and files. | None established. | Per-sample GSVA/singscore. | bulk_rna/gsea_ranked_results.qmd | High | Validate rank construction, gene universe, identifier mapping, ties, background, cutoffs, and multiple testing. |
| Hallmark singscore | code_MAP/HALLMARK_50.qmd | CANONICAL BACKBONE for a Hallmark-focused singscore stage because it builds/validates MSigDB signatures and scores samples. | code_MAP/00_CPTAC_LUAD_scoring for matrix cleaning and alternative score comparison. | Hallmark retrieval, gene coverage, rankGenes/simpleScore, score summaries, group comparisons, and plots. | MGI organoid labels and fixed collection-specific story. | None established; pin msigdbr/singscore versions. | GSVA and GSEA. | bulk_rna/pathway_scoring_singscore.qmd | High | Verify MSigDB collection/version, gene IDs, rank direction, missingness, score scale, and group-test design. |
| GSVA | code_MAP/00_CPTAC_LUAD_scoring.qmd or extensionless Quarto file | CANONICAL BACKBONE for a GSVA stage because it actually uses GSVA alongside singscore on an expression matrix. | HALLMARK_50 for signature coverage/reporting; normalization cheatsheet for input scale. | Gene-set scoring, matrix orientation, score comparison, and sample-level export. | CPTAC-specific identifiers and multi-score project story. | None established, but GSVA API is version-sensitive. | singscore, GSEA, decoupler, AddModuleScore. | bulk_rna/pathway_scoring_gsva.qmd | Medium | Pin GSVA version/API, test current call signature, validate input scale/orientation and gene-set overlap. |

## 10. Multiomics and MOFA

### 10.1 View preparation and sample matching

| Method | Candidate source files | Canonical backbone | Merge sources | Unique functionality to preserve | Functionality to remove | Deprecated components | Scientifically distinct alternatives | Proposed canonical template name | Confidence | Validation required |
|---|---|---|---|---|---|---|---|---|---|---|
| Matched-view preparation | code_MOFA/MOFA_TEMPLATE_CLEAN/01_multiomics_input_prep.qmd; code_MOFA/00_TCGA_LUAD_multiomics_download.qmd | CANONICAL BACKBONE starts from clean 01 because it isolates matching and export better than the live downloader, but it is not generic yet. | Live TCGA download for provenance; helper barcode/collapse logic only if explicitly scoped. | View-specific input files, sample-ID normalization, intersection reporting, matched tables, and missingness diagnostics. | Fixed TCGA five-view list, 16-character barcode assumption, GDC acquisition, and C1 names. | None established. | Arbitrary named views versus fixed assay contracts is a design choice. | multiomics/match_samples.qmd | Medium | Test ID normalization, duplicate samples, empty intersections, view orientation, missingness, and arbitrary view names. |
| TCGA acquisition | code_MOFA/00_TCGA_LUAD_multiomics_download.qmd | EXAMPLE / PROVENANCE, not a generic input template. | Clean 01 only for matched output contract. | TCGAbiolinks queries, primary-tumor filters, and data provenance. | Fixed TCGA project and download paths. | None established; pin GDC/TCGAbiolinks APIs. | User-supplied local views. | examples/multiomics/tcga_luad_download.qmd | High | Re-run only with current GDC/TCGAbiolinks and record data release/version. |

### 10.2 MOFA fitting

| Method | Candidate source files | Canonical backbone | Merge sources | Unique functionality to preserve | Functionality to remove | Deprecated components | Scientifically distinct alternatives | Proposed canonical template name | Confidence | Validation required |
|---|---|---|---|---|---|---|---|---|---|---|
| Core MOFA model fitting | code_MOFA/MOFA_TEMPLATE_CLEAN/03_mofa_model.qmd; code_MOFA/03_MOFA.qmd | CANONICAL BACKBONE is clean 03 for structure, not for its current full contents. Split its load, model construction, prepare_mofa, run_mofa, factor export, and output contract into a smaller core. | Live 03_MOFA for view preparation, model settings, and exports that are absent or more complete; clean helper matrix coercion only if made explicit. | Named view matrices, feature filtering, num_factors, model/training options, MOFA2 fit, HDF5/qs2 persistence, factor and weight tables. | C1 focus columns, group heatmaps, mutation summaries, and all optional interpretation from the core. | None established; pin MOFA2 and HDF5 behavior. | Alternative factor models are not represented. | multiomics/mofa_fit.qmd | High | Validate view orientation, missing values, feature filtering, factor number, convergence, seeds, HDF5 output, and reload. |
| Model diagnostics | code_MOFA/03_MOFA.qmd; code_MOFA/MOFA_TEMPLATE_CLEAN/03_mofa_model.qmd | MERGE SOURCE only. No isolated diagnostics notebook exists; extract diagnostics from both sources into a separate stage. | Core fit output; factor/weight exports. | Training/convergence information, variance explained by view/factor, factor weights, factor distributions, and model reload checks. | Group-specific C1 interpretation and publication heatmaps. | None established. | Diagnostic choices depend on model options and view preprocessing. | multiomics/mofa_diagnostics.qmd | Medium | Define minimum diagnostic set, check convergence and variance explained, and test failure behavior for degenerate views. |

### 10.3 Interpretation

| Method | Candidate source files | Canonical backbone | Merge sources | Unique functionality to preserve | Functionality to remove | Deprecated components | Scientifically distinct alternatives | Proposed canonical template name | Confidence | Validation required |
|---|---|---|---|---|---|---|---|---|---|---|
| Factor associations and view/feature interpretation | code_MOFA/MOFA_TEMPLATE_CLEAN/03_mofa_model.qmd; code_MOFA/03_MOFA.qmd | CANONICAL BACKBONE should be a new optional interpretation stage derived from clean 03 after core extraction. | Live 03 for project interpretation patterns; clean metadata/scored tables for generic association contract. | Factor-score associations, top features/weights, view summaries, selected heatmaps, and explicit group comparisons. | C1-specific focus_score_column/focus_group_column as mandatory inputs, mutation frequency story, and fixed heatmap panels. | None established. | Generic factor interpretation versus project-specific biological narrative. | multiomics/mofa_interpretation.qmd | Medium | Validate factor selection, association tests, multiple testing, heatmap scaling, and separation from model training data. |
| C1 signature scoring before MOFA | code_MOFA/MOFA_TEMPLATE_CLEAN/02_signature_scoring.qmd; code_MOFA/01_TCGA_LUAD_scoring_tf.qmd | EXAMPLE / MERGE SOURCE, not core MOFA. | bulk normalization guidance; UCell/singscore/GSVA alternatives where relevant. | Score table, metadata alignment, and downstream grouping contract. | Hidden compute_logcpm and class_from_z helper calls; fixed C1 labels. | None package-deprecated; hidden science is the main issue. | Other signature scoring methods. | separate multiomics/pre_mofa_signature_score.qmd only if needed | Medium | Expose filtering/normalization, define score method, test missing signatures and class cutoffs, and ensure no leakage into model evaluation. |

## 11. Biomarker machine learning

The two TRENTO notebooks are source material for the supported canonical library, not merely archive examples. Their biological labels and paths must eventually be generalized, but they should not be rewritten during this planning task.

### 11.1 Binary classification model

| Method | Candidate source files | Canonical backbone | Merge sources | Unique functionality to preserve | Functionality to remove | Deprecated components | Scientifically distinct alternatives | Proposed canonical template name | Confidence | Validation required |
|---|---|---|---|---|---|---|---|---|---|---|
| Small-cohort biomarker binary classification | CODE_MAP/TRENTO_models_miRNA_vs_PD_L1.qmd | CANONICAL BACKBONE. This is the strongest complete implementation in the repository for the requested supported biomarker workflow. | TRENTO_gtExtras_tables.qmd for output/reporting contracts; existing top-4 stable-panel section for reduced-model analysis. | Explicit train/test split, training-only recipe, supervised top-10 selection inside resampling, class weights, 200 stratified Monte Carlo resamples, brglm2 bias-reduced logistic regression, threshold tuning, held-out predictions, ROC-AUC, PR-AUC, balanced accuracy, sensitivity, specificity, precision, confusion matrix, feature stability, and top-4 stable panel. | TRENTO/miRNA/PD-L1 names, fixed input paths, fixed union signature, project-specific class labels, and report prose. | None established for brglm2/tidymodels, but pin versions and validate tailor/tidymodels APIs. | Other models, nested CV, elastic net, random forest, and external validation are not represented and should not be added by silent generalization. | machine_learning/biomarker_binary_classification_brglm2.qmd | High | Verify that every preprocessing step is learned within resampling, confirm threshold tuning cannot see test labels, test class-weight semantics, define precision/NPV/F1 behavior when undefined, reproduce held-out metrics, and verify feature-stability calculations. |
| Reduced stable-biomarker panel | CODE_MAP/TRENTO_models_miRNA_vs_PD_L1.qmd top-4 section | MERGE SOURCE into the canonical modeling template as an explicitly secondary sensitivity analysis. | Feature-stability table and held-out prediction outputs from the same notebook. | Stable-panel selection, unchanged held-out test set, same model/resampling/threshold rules, and compact ROC/PR/confusion outputs. | Treating the reduced model as the primary model or choosing a panel using test data. | None established. | Stability cutoffs and panel size are scientific sensitivity choices. | machine_learning/biomarker_reduced_stable_panel.qmd or section in primary template | High | Check panel selection uses training-derived stability only, compare performance uncertainty, and document multiplicity/model-selection optimism. |

### 11.2 Model reporting and interpretation

| Method | Candidate source files | Canonical backbone | Merge sources | Unique functionality to preserve | Functionality to remove | Deprecated components | Scientifically distinct alternatives | Proposed canonical template name | Confidence | Validation required |
|---|---|---|---|---|---|---|---|---|---|---|
| Biomarker model reporting | CODE_MAP/TRENTO_gtExtras_tables.qmd | CANONICAL BACKBONE for a companion reporting template. It is not a modeling method. | TRENTO_models_miRNA_vs_PD_L1.qmd for prediction, selected-feature, threshold, split, and stability outputs. | Prediction tables, selected-biomarker values, probability visualization, gt/gtExtras tables, biomarker heatmap, train/test annotation, and threshold display. | Model fitting, resampling, feature selection, and claims that tables independently validate the model. | None established; pin gt/gtExtras APIs. | Base plotting/table output is a lighter presentation alternative. | machine_learning/biomarker_model_reporting.qmd | High | Validate that reporting reads frozen outputs, preserves train/test annotations, does not refit, and handles missing metrics/undefined precision safely. |

## 12. Supporting statistics, visualization, import/export, and persistence

| Method | Candidate source files | Canonical backbone | Merge sources | Unique functionality to preserve | Functionality to remove | Deprecated components | Scientifically distinct alternatives | Proposed canonical template name | Confidence | Validation required |
|---|---|---|---|---|---|---|---|---|---|---|
| Group summaries and association tests | code_MAP/notebook_templates/general_statistics/01_group_summary_and_association_tests.qmd; code_MAP/03_MAP_state_markers_statistics_export.qmd | CANONICAL BACKBONE is the focused general-statistics template. | MAP statistics for effect-size, correlation, and export ideas, but not its biological story. | Counts, missingness, Wilcoxon, chi-square, BH adjustment, and compact plots. | Unused assay_name and assumptions that two-group tests cover all study designs. | None established. | Paired, repeated-measures, covariate-adjusted, survival, and mixed models are not represented. | statistics/group_association_tests.qmd | Medium to high | Add effect sizes/confidence intervals, define zero-cell and NA handling, test categorical expected counts, and document unsupported designs. |
| Quarto report guidance | cheatsheets/quarto_guide.md; CODE_MAP/quarto_config_tmplate.md | CANONICAL BACKBONE should be one consolidated cheatsheet, not a code template. | Unique sections from both guides. | YAML, captions, cross-references, metrics, and handoff guidance. | Duplicate guides and the misspelled filename. | None. | Notebook analysis templates are distinct. | cheatsheets/quarto_report_guide.md | High | Compare unique prose before consolidation; no runtime validation needed beyond a small example render later. |
| Generic plotting/output mechanics | Repeated in all 18 templates and project notebooks | HELPER SOURCE, not an analytical template. | Per-template explicit paths and dimensions. | Directory creation, plot saving with explicit arguments, TSV writing, and compact table formatting. | Hidden global directories, implicit output names, and helpers that perform analysis. | None. | Direct code remains preferable when used only once. | helpers/R/io_plot_helpers.R and helpers/python/io_helpers.py only if repetition remains | Medium | Check paths, overwrite policy, file formats, and that helpers receive all state explicitly. |
| Object import/export | qs2 in templates; qs, qsave/qread, saveRDS, and h5ad in project notebooks | No single canonical object format has enough evidence. Document a small policy rather than wrapping every format. | Existing input/output contracts from focused templates and MOFA/TRENTO workflows. | Explicit R/Python boundaries, stable TSV outputs, and object round trips. | Silent format conversions and helper functions that conceal assays or preprocessing. | None established. | qs2, qs, saveRDS, and h5ad are ecosystem-specific alternatives. | cheatsheets/object_persistence_contract.md | Medium | Round-trip representative Seurat, Signac, AnnData, and MOFA objects; record package/session versions. |

## 13. Deprecation and API status

The following distinctions are important:

- DEPRECATED PACKAGE/API: do not promote into new canonical code.
- OLD BUT VALID APPROACH: retain as an example when scientifically useful, after version validation.
- SCIENTIFICALLY DISTINCT APPROACH: preserve separately even when a newer or more convenient method exists.
- UNVALIDATED: do not call deprecated; it simply needs runtime evidence.

| Component | Source evidence | Classification | Canonicalization treatment |
|---|---|---|---|
| R decoupleR package | code_MAP/GSE171145.qmd: library(decoupleR), get_collectri, run_ulm; code_MOFA/01_TCGA_LUAD_scoring_tf.qmd: decoupleR::get_collectri and decoupleR::run_mlm | DEPRECATED PACKAGE and DEPRECATED R APIs per the task instruction | Keep source notebooks as provenance/examples. Do not copy R calls into templates. Use Python decoupler as the target, then validate method/network equivalence rather than assuming it. |
| decoupleR-derived downstream files | code_MAP/09_MAP_C1_Core_refined_signature.qmd references decoupleR-derived TF activity tables | LEGACY PROVENANCE, not necessarily executable deprecated code | Preserve the interpretation only with explicit provenance and regenerate from the supported Python workflow if needed. |
| Python decoupler | code_MAP/04_MAP_decoupler_bridge.qmd imports decoupler and runs ULM | TARGET CURRENT IMPLEMENTATION, subject to version pinning | Use as canonical regulatory activity backbone. Keep R only for input/output bridge if that remains the chosen boundary. |
| Seurat IntegrateLayers/RPCA branch | code_MAP/00_MAP_qc_integration.qmd | UNVALIDATED API branch, not automatically deprecated | Render/test before promotion; do not leave experimental branches in a canonical notebook. |
| Seurat/Harmony workflows | MAP notebooks | OLD BUT VALID / CURRENT DEPENDENCY TO VERIFY | Preserve Harmony as a distinct integration method if diagnostics support it; pin package versions. |
| CopyKAT and SCEVAN | MAP/GSE and C1 notebooks | OLD BUT VALID PROJECT APPROACHES, scientifically distinct | Preserve as separate CNV examples. Promote only if current runtime and biological reference assumptions are documented. |
| scVelo and CellRank2 | project 07 and template 09 | CURRENT/ACTIVE APPROACHES TO VERIFY | Separate velocity diagnostics from CellRank fate inference; pin versions and test AnnData layers. |
| tradeSeq/Slingshot | code_MAP/04_MAP_c1_gene_programs_tradeSeq.qmd | CURRENT/VALID SCIENTIFIC APPROACH TO VERIFY | Use as the primary trajectory source; retain true model diagnostics. |
| hdWGCNA | code_MAP/06_MAP_coexpression_modules.qmd | CURRENT/VALID HEAVY APPROACH TO VERIFY | Keep separate from simple module scoring and document dependency cost. |
| scCellFie | code_MAP/08_MAP_metabolic_activity_scCellFie.qmd | CURRENT/VALID APPROACH TO VERIFY | Prefer the actual computation over imported-score scaffolding. |
| GSVA/singscore | code_MAP/00_CPTAC_LUAD_scoring and HALLMARK_50.qmd | SCIENTIFICALLY DISTINCT METHODS; APIs version-sensitive | Maintain separate named templates and pin versions. |
| brglm2/tidymodels | TRENTO model | CURRENT/VALID METHOD TO VERIFY | Promote the modeling logic, preserve leakage controls, and pin the complete R dependency set. |
| gt/gtExtras | TRENTO reporting | CURRENT/VALID REPORTING DEPENDENCY | Promote as a reporting companion only; it does not define the model. |

No current source establishes a deprecated chromVAR implementation. The issue with the current motif scaffold is that it claims chromVAR-style activity while no RunChromVAR call was found.

## 14. Proposed final method hierarchy

The future library should have a shallow hierarchy with explicit method names:

1. Core input and object stages
   - bulk tximport/edgeR input
   - scRNA Seurat object
   - Signac object
   - multiome object
   - multiomics matched views

2. Core per-modality analytical stages
   - scRNA QC
   - doublet detection
   - log normalization/PCA/neighbors/clustering/UMAP
   - SCTransform alternative
   - scATAC QC/TF-IDF/LSI/clustering
   - bulk edgeR QC/normalization

3. Explicit optional method stages
   - Harmony SCT
   - Harmony log-normalized
   - RPCA
   - Azimuth
   - SingleR/anchor label transfer
   - WNN
   - RNA/ATAC linkage
   - AddModuleScore
   - UCell
   - CytoTRACE2
   - cell cycle
   - Slingshot
   - tradeSeq
   - scVelo
   - CellRank
   - Python decoupler
   - GSVA
   - singscore
   - hdWGCNA
   - scCellFie
   - MOFA fit/diagnostics/interpretation
   - biomarker classification/reporting

4. Interpretation and reporting
   - marker analysis
   - GSEA
   - group statistics
   - score/report tables
   - model reporting

5. Examples and provenance
   - MAP, TCGA/MOFA, C1, TRENTO, and interview-specific notebooks.

The hierarchy should not force every optional method into every workflow. A template should represent one meaningful stage and its required scientific choices.

## 15. Proposed canonical template list

### High-confidence first wave

- templates/bulk_rna/tximport_edgeR_input.qmd
- templates/bulk_rna/qc_normalization_edgeR.qmd
- templates/bulk_rna/gsea_ranked_results.qmd
- templates/bulk_rna/pathway_scoring_singscore.qmd
- templates/bulk_rna/pathway_scoring_gsva.qmd
- templates/single_cell/create_seurat_object.qmd
- templates/single_cell/quality_control_fixed_thresholds.qmd
- templates/single_cell/normalization_reduction_clustering_log.qmd
- templates/single_cell/signature_scoring_addmodulescore.qmd
- templates/single_cell/signature_scoring_ucell_up_down.qmd
- templates/single_cell/marker_analysis_group_comparison.qmd
- templates/single_cell/pseudotime_feature_summary.qmd
- templates/scatac/create_signac_object.qmd
- templates/scatac/quality_control.qmd
- templates/scatac/lsi_reduction_clustering.qmd
- templates/scatac/motif_enrichment_findmotifs.qmd
- templates/multiome/create_object.qmd
- templates/multiome/wnn.qmd
- templates/multiome/rna_atac_linkage.qmd
- templates/multiome/rna_to_atac_label_transfer.qmd
- templates/statistics/group_association_tests.qmd
- templates/machine_learning/biomarker_binary_classification_brglm2.qmd
- templates/machine_learning/biomarker_model_reporting.qmd

### Second wave after source extraction and validation

- templates/single_cell/doublet_detection_scdblfinder.qmd
- templates/single_cell/normalization_reduction_clustering_sct.qmd
- templates/single_cell/batch_integration_harmony_sct.qmd
- templates/single_cell/batch_integration_harmony_log.qmd
- templates/single_cell/batch_integration_rpca.qmd
- templates/single_cell/annotation_azimuth.qmd
- templates/single_cell/annotation_singler.qmd
- templates/single_cell/cell_cycle_scoring.qmd
- templates/single_cell/cell_state_cytotrace2.qmd
- templates/single_cell/trajectory_slingshot.qmd
- templates/single_cell/trajectory_tradeseq.qmd
- templates/single_cell/velocity_scvelo.qmd
- templates/single_cell/cellrank_fate_inference.qmd
- templates/single_cell/regulatory_activity_decoupler_python.qmd
- templates/single_cell/regulatory_activity_interpretation.qmd
- templates/single_cell/coexpression_hdWGCNA.qmd
- templates/single_cell/metabolic_activity_sccellfie.qmd
- templates/multiome/regulatory_analysis_composed.qmd, or separate method stages
- templates/multiomics/match_samples.qmd
- templates/multiomics/mofa_fit.qmd
- templates/multiomics/mofa_diagnostics.qmd
- templates/multiomics/mofa_interpretation.qmd
- templates/machine_learning/biomarker_reduced_stable_panel.qmd

Do not add a bulk differential-expression template until a complete tested source is selected. Do not add spatial templates without a real spatial implementation.

## 16. Source to canonical-template merge graph

The graph below identifies source roles. It is not a filesystem move plan.

    notebook_templates/scRNA/01_create_seurat_object
      -> single_cell/create_seurat_object
      <- MAP QC/RNA and GSE171145 raw import and metadata checks

    notebook_templates/scRNA/02_quality_control
      -> single_cell/quality_control_fixed_thresholds
      <- MAP RNA and MAP QC diagnostic plots
      <- review/fix filtered-object save target

    notebook_templates/scRNA/03_normalization_integration_clustering
      -> single_cell/normalization_reduction_clustering_log
      <- MAP RNA seeds and diagnostics
      || MAP QC SCTransform branch -> single_cell/normalization_reduction_clustering_sct

    MAP 00_MAP_qc_integration SCTransform + Harmony
      -> single_cell/batch_integration_harmony_sct
      <- LISI diagnostics and explicit batch settings

    MAP 00_MAP_RNA log-normalized Harmony
      -> single_cell/batch_integration_harmony_log
      <- visible log-normalization stage

    MAP optional RPCA IntegrateLayers
      -> single_cell/batch_integration_rpca only after runtime validation

    MAP 001_RNA_ATAC_LT
      -> multiome/rna_to_atac_label_transfer
      <- multiome/create_object and GeneActivity/ID checks

    notebook_templates/scRNA/04_signature_scoring
      -> single_cell/signature_scoring_addmodulescore

    MAP 01_MAP_c1_scoring
      -> single_cell/signature_scoring_ucell_up_down
      -> single_cell/cell_state_cytotrace2
      -> cell_cycle_scoring
      <- MAP 02 simplified score transformations

    MAP 04_MAP_c1_gene_programs_tradeSeq
      -> single_cell/trajectory_slingshot
      -> single_cell/trajectory_tradeseq
      <- notebook_templates/scRNA/06 descriptive pseudotime summaries

    MAP 07_MAP_velocity_scvelo_cellrank
      -> single_cell/velocity_scvelo
      -> single_cell/cellrank_fate_inference
      <- notebook_templates/scRNA/09 minimal diagnostics
      <- alevin_fry velocity quantification script as provenance

    MAP 04_MAP_decoupler_bridge
      -> single_cell/regulatory_activity_decoupler_python
      <- MAP 05 interpretation and score storage
      <- replace R decoupleR blocks from GSE171145 and TCGA scoring

    MAP 06_MAP_coexpression_modules
      -> single_cell/coexpression_hdWGCNA
      || notebook_templates/scRNA/08 -> single_cell/gene_module_scoring

    MAP 08_MAP_metabolic_activity_scCellFie
      -> single_cell/metabolic_activity_sccellfie
      || notebook_templates/scRNA/10 -> single_cell/import_metabolic_scores

    MAP 00_MAP_ATAC_qc_integration
      -> scatac/quality_control
      <- notebook_templates/scATAC/01 and 02 object/reduction contracts

    MAP 002_ATAC_MOTIF
      -> scatac/motif_enrichment_findmotifs
      <- notebook_templates/scATAC/03 user-input/output structure

    simple_QC_MGI_organoids
      -> bulk_rna/tximport_edgeR_input
      -> bulk_rna/qc_normalization_edgeR
      <- rnaseq_normalization_cheatsheet

    GSEA_of_DEGs
      -> bulk_rna/gsea_ranked_results

    HALLMARK_50
      -> bulk_rna/pathway_scoring_singscore

    CPTAC LUAD scoring
      -> bulk_rna/pathway_scoring_gsva
      <- HALLMARK_50 coverage/reporting blocks

    MOFA_TEMPLATE_CLEAN/01_multiomics_input_prep
      -> multiomics/match_samples
      <- TCGA acquisition only as provenance

    MOFA_TEMPLATE_CLEAN/03_mofa_model
      -> multiomics/mofa_fit
      -> multiomics/mofa_diagnostics
      -> multiomics/mofa_interpretation
      <- live 03_MOFA model/output blocks

    TRENTO_models_miRNA_vs_PD_L1
      -> machine_learning/biomarker_binary_classification_brglm2
      -> machine_learning/biomarker_reduced_stable_panel

    TRENTO_gtExtras_tables
      -> machine_learning/biomarker_model_reporting

## 17. Notebooks that become redundant only after successful merge

These are not deletion decisions. They become redundant only if the proposed canonical output is rendered, tested, and shown to preserve the source functionality.

| Notebook or file | Why it may become redundant | Preconditions |
|---|---|---|
| notebook_templates/scRNA/03_normalization_integration_clustering.qmd | Its baseline logic is represented by a correctly named normalization/reduction/clustering template. | Remove false integration claim and validate output equivalence. |
| notebook_templates/scRNA/06_trajectory_gene_programs.qmd | Its descriptive binning block can be retained in pseudotime_feature_summary or merged into the tradeSeq reporting stage. | Preserve the distinction between summary and inference. |
| notebook_templates/scRNA/07_pathway_activity_decoupler.qmd | Its score-import mechanics can be retained in a shared importer or decoupler output stage. | Keep a separate importer if precomputed scores remain common. |
| notebook_templates/scRNA/08_coexpression_modules.qmd | Its AddModuleScore logic is represented by gene_module_scoring, not hdWGCNA. | Rename and retain if lightweight module scoring is wanted. |
| notebook_templates/scRNA/09_velocity_scvelo_cellrank.qmd | Its minimal flow is subsumed by the validated scVelo template. | Preserve minimal template if a low-resource diagnostic is useful. |
| notebook_templates/scRNA/10_metabolic_activity.qmd | Its importer is subsumed by a named score-import stage. | Do not delete if imported scores are a supported input. |
| notebook_templates/scATAC/02_quality_control_integration.qmd | Its LSI/clustering block is subsumed by the canonical ATAC QC/LSI stage. | Preserve user-visible dimensions and thresholds. |
| notebook_templates/scATAC/03_motif_enrichment.qmd | Its generic wrapper is subsumed by a parameterized FindMotifs template. | Preserve PFM/database contract. |
| notebook_templates/multiome/02_qc_integration_wnn.qmd | Its WNN implementation is subsumed by multiome/wnn. | Keep WNN separate from batch integration. |
| notebook_templates/multiome/04_regulatory_programs.qmd | Its simple RNA scoring is subsumed by gene/module scoring or a named regulatory scoring stage. | Do not claim it implements integrated regulatory analysis. |
| MOFA_TEMPLATE_CLEAN/03_mofa_model.qmd | The giant notebook is replaced by fit, diagnostics, and interpretation stages. | Validate all exported factors/weights/plots before retiring it. |
| MOFA_TEMPLATE_CLEAN/helpers/helpers_from_MOFA.R | Functions that remain mechanical may move to helpers; scientific functions must remain visible or scoped. | Remove globals and hidden normalization first. |
| cheatsheets/quarto_guide.md or CODE_MAP/quarto_config_tmplate.md | One guide can replace the other. | Compare unique sections manually. |
| Archive.zip exact velocity/metabolic members | Exact duplicates of current files. | Preserve one historical archive and confirm provenance value. |

## 18. Notebooks that must remain examples

These contain biological interpretation, cohort-specific references, or combined pipelines that should not be forced into generic templates:

- code_MAP/00_MAP_qc_integration.qmd;
- code_MAP/00_MAP_RNA_qc_integration.qmd;
- code_MAP/00_MAP_ATAC_qc_integration.qmd;
- code_MAP/001_RNA_ATAC_LT.qmd after any focused extraction;
- code_MAP/002_ATAC_MOTIF.qmd after motif extraction;
- code_MAP/GSE171145.qmd;
- code_MAP/00_CPTAC_LUAD_scoring;
- code_MAP/03_MAP_state_markers_statistics_export.qmd;
- code_MAP/05_MAP_regulatory_programs.qmd;
- code_MAP/09_MAP_C1_Core_refined_signature.qmd;
- code_MOFA/00_TCGA_LUAD_multiomics_download.qmd;
- code_MOFA/01_TCGA_LUAD_scoring_tf.qmd;
- code_MOFA/03_MOFA.qmd;
- CODE_MAP/TRENTO_models_miRNA_vs_PD_L1.qmd after a generic modeling template is derived;
- CODE_MAP/TRENTO_gtExtras_tables.qmd after a generic reporting template is derived;
- Task for 2nd interview.zip, if the proteomics/network work is curated.

The original examples should remain scientifically recognizable. Generalization should add a clearly separate template, not erase the project narrative.

## 19. Notebooks that must remain provenance/archive

- code_MAP/02_MAP_c1_scoring.qmd until its relationship to 01 and 09 is documented;
- code_MAP/10_MAP_extensive_statistics.qmd because it records intended analyses even though it is mostly a plan;
- code_MAP/Archive.zip until historical duplicates and version relationships are recorded;
- Task for 2nd interview.zip until data licensing, privacy, and redistribution decisions are made;
- alevin_fry/scripts/quant.log and run.log if they document a failed or incomplete velocity input attempt;
- code_MAP/notebook_templates/README.md, NOTEBOOK_INVENTORY.md, and PONYTAIL_AUDIT.md once a replacement library contract exists;
- MOFA_TEMPLATE_CLEAN README and inventory notes until the split MOFA plan is validated;
- all unpromoted project notebooks that contain unique parameter choices, intermediate results, or biological conclusions.

## 20. Unresolved scientific decisions

1. Should the first bulk canonical workflow use the active >5 CPM filter or the alternate >1 CPM filter in simple_QC_MGI_organoids.qmd?
2. Is edgeR TMMwsp the supported bulk normalization, or should the library support separate edgeR/limma-voom and DESeq2 templates?
3. Should log normalization or SCTransform be the primary scRNA baseline? The repository supports both as scientifically meaningful choices.
4. Are both Harmony SCT and Harmony log-normalized worth maintaining, or should one be an example only?
5. Is RPCA integration sufficiently validated to become a supported template, or should its optional project branch remain provenance?
6. Should annotation support Azimuth, SingleR, and anchor transfer as three templates, or should the initial library select one reference-based method?
7. Is CytoTRACE2 intended as a supported independent cell-state template? It is a strong candidate, but its current code is embedded in a C1 project workflow rather than a standalone notebook.
8. Should cell-cycle scoring be descriptive only, or should regression be a supported optional modeling decision?
9. Which CNV method, if any, should be supported: SCEVAN, CopyKAT, or examples only?
10. Should the trajectory library support Slingshot plus tradeSeq as a two-stage pair, or keep pseudotime inference and gene-association testing in one template?
11. Is a complete CellRank fate-analysis template required, or is scVelo sufficient for the first dynamics release?
12. Which Python decoupler method and network source should be canonical: ULM with CollecTRI, another network, or separate TF/pathway configurations?
13. Should pathway activity support decoupler, GSVA, singscore, and imported-score stages, or should only method families with repeated reuse be promoted?
14. Is hdWGCNA important enough to support its heavier dependencies in the curated library?
15. Should scCellFie be supported as a full Python template, or as an example plus imported-score stage?
16. What does “regulatory program” mean in the supported library: RNA gene-set score, TF activity, motif activity, RNA/ATAC linkage, or an explicit composition of these?
17. Should MOFA accept arbitrary named views or retain a documented minimum view schema?
18. Which MOFA outputs are core: factors and weights only, or diagnostics and interpretation tables as well?
19. For the TRENTO canonical model, should the primary model retain top-10 supervised selection and the top-4 panel as a separate sensitivity section?
20. How should undefined precision, NPV, F1, sensitivity, or specificity be represented: NA, an explicit undefined state, or a documented zero convention?
21. Should model reporting be a separate Quarto template with frozen-input contracts, or a small companion section in the modeling notebook?
22. Are there independent validation cohorts for the biomarker workflow, or should the library explicitly stop at held-out internal evaluation?
23. Should the proteomics/network interview analysis be curated as an example, kept only as raw archive, or excluded for licensing/data-size reasons?
24. Which R object format should canonical templates support: qs2, qs, or saveRDS?
25. What package/version and session-provenance record is required before a source is promoted from example to canonical backbone?

## 21. Recommended next action

Do not migrate files yet. First make a small validation matrix for the proposed backbones:

- one representative scRNA object/QC/reduction path;
- one Harmony and one RPCA comparison;
- one CytoTRACE2 run;
- one Slingshot/tradeSeq run from 04_MAP_c1_gene_programs_tradeSeq.qmd;
- one Python decoupler run replacing an R decoupleR run;
- one scVelo/CellRank layer-alignment run;
- one hdWGCNA and one scCellFie run;
- one Signac motif run with explicit genome/PFM provenance;
- one MOFA fit with separated diagnostics;
- one TRENTO model/report round trip with frozen held-out evaluation.

Only after those checks should the repository choose exact canonical filenames and perform the structural migration.
