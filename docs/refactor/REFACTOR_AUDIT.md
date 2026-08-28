# Useful_code refactor audit

Audit date: 2026-08-26

Scope: static, recursive audit of the repository excluding ordinary Git internals. No source file was modified, moved, renamed, deleted, or rewritten for this audit. The only intended new file is this report.

## 1. Executive summary

Useful_code is currently a code map rather than a curated template library. It combines 18 recently scaffolded Quarto templates, a larger set of project-specific MAP and TCGA/MOFA analyses, bulk RNA-seq and pathway notebooks, a TRENTO machine-learning analysis, an interview proteomics analysis stored in a zip archive, documentation, logs, and historical copies.

The repository contains useful reusable material, but the current template directories overstate their completeness. Several files are structurally similar without being scientifically equivalent, and several names claim an operation that the code does not perform:

- scRNA trajectory, pathway activity, coexpression, and metabolic templates mostly summarize or import precomputed results.
- scRNA and scATAC files named integration do not perform batch integration.
- the multiome WNN file performs multimodal neighbor construction, not batch correction.
- the multiome regulatory-program file performs RNA gene-set scoring, not a complete regulatory-program inference.
- the velocity file computes scVelo velocity and a CellRank velocity kernel, but no fate estimator, terminal-state analysis, or fate probabilities.
- the scRNA QC template filters an object but saves the unfiltered object.
- the MOFA structure is cleaner than the project notebooks but is still a 1,162-line project-shaped workflow with fixed TCGA assumptions, hidden scientific normalization, and mixed generic and C1-specific interpretation.

The best future library is therefore not the current 18-template mirror. It should contain a small number of visible, method-specific analytical stages, with alternate scientific approaches retained as separate templates or examples. Project notebooks should become examples, and historical copies should be archived before any conservative deletion.

Highest-confidence immediate canonical candidates:

- bulk RNA-seq QC and normalization, derived from simple_QC_MGI_organoids.qmd after resolving the count/filtering contract;
- scRNA object creation, QC, basic normalization/reduction/clustering, signature scoring, and marker analysis;
- Signac object creation, scATAC QC/LSI/clustering, and motif enrichment;
- multiome object creation, WNN, and RNA/ATAC linkage;
- minimal group-association statistics.

Candidates requiring substantial generalization before promotion:

- batch integration, because Harmony, RPCA, SCTransform, log-normalized Harmony, and WNN represent different scientific choices;
- annotation and label transfer;
- true trajectory/tradeSeq;
- true coexpression/hdWGCNA;
- true scCellFie metabolic activity;
- decoupler regulatory scoring;
- generic MOFA;
- machine-learning classification.

No active spatial-analysis implementation was found. No complete bulk RNA-seq differential-expression notebook was found; GSEA_of_DEGs.qmd consumes an existing DEG result rather than producing it.

## 2. Current repository structure

The repository contains approximately 75 non-Git files:

- CODE_MAP: 63 files, approximately 15.7 MB; this is the main scientific collection.
- .claude: six GitNexus instruction files.
- former compact references: retained only as historical audit context.
- root: README, license, agent instructions, Claude instructions, and a macOS metadata file.

The indexed GitNexus snapshot reports 64 files, 171 symbols, and zero execution flows, while the recursive filesystem inventory contains approximately 75 files. The index is therefore incomplete or stale for process-level auditing. Static source inspection was used for the conclusions below; notebooks were not rendered or executed.

Current tree, excluding ordinary Git internals:

    .claude/skills/gitnexus/
    AGENTS.md
    CLAUDE.md
    CODE_MAP/
      alevin_fry/
      code_MAP/
      code_MOFA/
      quarto_config_tmplate.md
      Task for 2nd interview.zip
      TRENTO_gtExtras_tables.qmd
      TRENTO_models_miRNA_vs_PD_L1.qmd
    LICENSE
    README.md

Within code_MAP, the current organization is:

    code_MAP/
      00_CPTAC_LUAD_scoring
      00_MAP_*.qmd
      001_RNA_ATAC_LT.qmd
      002_ATAC_MOTIF.qmd
      01_MAP_*.qmd
      02_MAP_c1_scoring.qmd
      03_MAP_state_markers_statistics_export.qmd
      04_MAP_*.qmd
      05_MAP_regulatory_programs.qmd
      06_MAP_coexpression_modules.qmd
      07_MAP_velocity_scvelo_cellrank.qmd
      08_MAP_metabolic_activity_scCellFie.qmd
      09_MAP_C1_Core_refined_signature.qmd
      10_MAP_extensive_statistics.qmd
      GSE171145.qmd
      GSEA_of_DEGs.qmd
      HALLMARK_50.qmd
      notebook_templates/
      Archive.zip

The numbering is project chronology, not a reusable-library taxonomy. In particular, files numbered 00 to 10 are not interchangeable stages and do not form a single portable workflow.

## 3. File inventory

Status labels mean:

- TEMPLATE: suitable starting point after targeted cleanup.
- EXAMPLE: scientifically useful but tied to a cohort, project, or story.
- HELPER: mechanical code that may be shared without hiding scientific choices.
- CHEATSHEET: explanatory guidance rather than executable analysis.
- ARCHIVE: retain for provenance but keep outside the active surface.
- DELETE_CANDIDATE: safe only after confirming no provenance or user value.
- REVIEW: insufficient evidence to choose safely.

### 3.1 Repository and governance files

| Source | Purpose and assessment | Eventual status |
|---|---|---|
| README.md | Two-line repository description; does not describe the analyses or future library contract. | REVIEW; update later |
| LICENSE | Repository license. | PRESERVE |
| AGENTS.md | Project-specific operating instructions, including GitNexus requirements. | PRESERVE as project metadata |
| CLAUDE.md | Same class of agent/project instructions as AGENTS.md. | PRESERVE as project metadata |
| .claude/skills/gitnexus/gitnexus-cli/SKILL.md | GitNexus CLI operating guidance. | PRESERVE as project metadata |
| .claude/skills/gitnexus/gitnexus-debugging/SKILL.md | GitNexus debugging guidance. | PRESERVE as project metadata |
| .claude/skills/gitnexus/gitnexus-exploring/SKILL.md | GitNexus code-exploration guidance. | PRESERVE as project metadata |
| .claude/skills/gitnexus/gitnexus-guide/SKILL.md | GitNexus tool/resource reference. | PRESERVE as project metadata |
| .claude/skills/gitnexus/gitnexus-impact-analysis/SKILL.md | GitNexus impact-analysis guidance. | PRESERVE as project metadata |
| .claude/skills/gitnexus/gitnexus-refactoring/SKILL.md | GitNexus refactoring guidance. | PRESERVE as project metadata |
| .DS_Store | macOS Finder metadata; no scientific or governance value. | DELETE_CANDIDATE |
| CODE_MAP/.DS_Store | macOS Finder metadata; no scientific or governance value. | DELETE_CANDIDATE |

### 3.2 Documentation and reference material

| Source | Purpose, language, modality/task, reuse, and overlap | Eventual status |
|---|---|---|
| Former Quarto reference | Markdown guidance for Quarto HTML report structure, captions, cross-references, metrics, and handoff; no longer kept in an active cheatsheet directory. | RETIRED |
| CODE_MAP/quarto_config_tmplate.md | Markdown copy-ready Quarto YAML/report guidance. It overlapped the former Quarto reference; the filename contains a typo. | RETIRED / compare with `miscellaneous/quarto/` |
| Former RNA-seq normalization reference | Markdown scientific guidance on raw counts, filtering, edgeR TMM, log2CPM, limma-voom, and DESeq2 distinctions; no longer kept in an active cheatsheet directory. | RETIRED |
| CODE_MAP/notebook_templates/README.md | Markdown instructions for copying 18 Quarto templates, user input blocks, qs2/h5ad persistence, and TSV outputs. | ARCHIVE or replace with library README |
| CODE_MAP/notebook_templates/NOTEBOOK_INVENTORY.md | Markdown map of source notebooks to 18 templates. It omits bulk RNA and TRENTO despite those files being present, and describes some source/template relationships too generously. | ARCHIVE or replace |
| CODE_MAP/notebook_templates/PONYTAIL_AUDIT.md | Markdown audit limited to notebook_templates. It correctly identifies repetitive wrappers but is not a repository-wide audit and treats several stubs/importers as complete methods. | ARCHIVE |
| CODE_MAP/code_MOFA/MOFA_TEMPLATE_CLEAN/README.md | Markdown description of the MOFA notebook-first structure and output contract. Useful, but the contract disagrees with parts of the helper implementation. | REVIEW; retain as design note until corrected |
| CODE_MAP/code_MOFA/MOFA_TEMPLATE_CLEAN/archive_notes/MOFA_code_inventory.md | Markdown mapping from live TCGA/MOFA notebooks to the clean version and a list of deliberately excluded project-specific material. | ARCHIVE or retain as provenance note |

### 3.3 Reusable-template candidates

All 18 files below are Quarto/R or Quarto/Python templates of approximately 165 to 189 lines. They repeat the same report wrapper, input/config blocks, validation, summary, analysis, QC, visualization, persistence, and export sections. Their scientific bodies are not exact duplicates.

| Source | Purpose and scientific implementation | Reuse / status |
|---|---|---|
| code_MAP/notebook_templates/scRNA/01_create_seurat_object.qmd | R/Seurat; count matrix plus metadata to Seurat object; min.cells 3, min.features 200, mitochondrial percentage; qs2 persistence. Assumes the first metadata column is the cell identifier. | TEMPLATE candidate |
| code_MAP/notebook_templates/scRNA/02_quality_control.qmd | R/Seurat; computes or reuses mitochondrial percentage, applies feature/mitochondrial thresholds, exports filtered metadata and plots. Final save writes object rather than filtered, so the persisted result contradicts the analysis. | TEMPLATE after fix |
| code_MAP/notebook_templates/scRNA/03_normalization_integration_clustering.qmd | R/Seurat; NormalizeData, 3,000 variable features, ScaleData, PCA, neighbors, clusters, UMAP. No integration despite the filename and unused batch_column. | TEMPLATE after rename |
| code_MAP/notebook_templates/scRNA/04_signature_scoring.qmd | R/Seurat; reads one signature table and applies AddModuleScore. Generic enough for a visible gene-set scoring stage, but not a universal scoring implementation. | TEMPLATE candidate |
| code_MAP/notebook_templates/scRNA/05_marker_identification_and_export.qmd | R/Seurat; FindMarkers for two identities with logFC/min.pct thresholds, dot plot, TSV export. It is group-vs-group marker/DE, not all-cluster marker discovery. | TEMPLATE candidate |
| code_MAP/notebook_templates/scRNA/06_trajectory_gene_programs.qmd | R/Seurat; assumes pseudotime already exists, bins it, and summarizes selected features. It does not infer trajectories or fit tradeSeq. | Rename to pseudotime summary; TEMPLATE only after clarification |
| code_MAP/notebook_templates/scRNA/07_pathway_activity_decoupler.qmd | R/Seurat; reads activity.tsv and attaches precomputed scores to metadata. It does not run decoupleR/decoupler or pathway scoring. | Rename to activity-score import; TEMPLATE candidate |
| code_MAP/notebook_templates/scRNA/08_coexpression_modules.qmd | R/Seurat; reads predefined module genes and uses AddModuleScore. It does not calculate coexpression or WGCNA/hdWGCNA modules. | Rename to gene-module scoring; TEMPLATE candidate |
| code_MAP/notebook_templates/scRNA/09_velocity_scvelo_cellrank.qmd | Python/AnnData; scVelo filtering, moments, velocity, velocity graph, velocity pseudotime, and a CellRank VelocityKernel transition matrix. It has no fate estimator, terminal states, or fate probabilities. | Minimal velocity TEMPLATE after rename; CellRank proper separate |
| code_MAP/notebook_templates/scRNA/10_metabolic_activity.qmd | Python/AnnData; reads precomputed metabolic_activity.tsv, attaches scores, summarizes, plots, and saves h5ad. It does not run scCellFie. | Rename to score import; actual metabolic template requires another source |
| code_MAP/notebook_templates/scATAC/01_create_signac_object.qmd | R/Signac; peak matrix, fragments, metadata, ChromatinAssay, NucleosomeSignal, TSSEnrichment. Genome and input conventions are placeholders. | TEMPLATE candidate |
| code_MAP/notebook_templates/scATAC/02_quality_control_integration.qmd | R/Signac; QC flags, TF-IDF, top features, LSI, neighbors, clusters, UMAP. No batch integration. | TEMPLATE after rename |
| code_MAP/notebook_templates/scATAC/03_motif_enrichment.qmd | R/Signac; imports a PFM database, AddMotifs, FindMarkers, FindMotifs, motif plot. It does not run chromVAR despite the description suggesting chromVAR-style activity. | TEMPLATE after method naming cleanup |
| code_MAP/notebook_templates/multiome/01_create_multiome_object.qmd | R/Seurat/Signac; paired RNA and ATAC matrices, fragments, shared cell IDs, two assays, basic ATAC QC. Genome is a placeholder. | TEMPLATE candidate |
| code_MAP/notebook_templates/multiome/02_qc_integration_wnn.qmd | R/Seurat/Signac; RNA PCA plus ATAC LSI followed by FindMultiModalNeighbors, weighted UMAP, and wsnn clustering. WNN is not batch integration. | TEMPLATE after rename |
| code_MAP/notebook_templates/multiome/03_rna_atac_linkage.qmd | R/Signac; LinkPeaks and CoveragePlot with configurable distance and group. This is a genuine linkage stage. | TEMPLATE candidate |
| code_MAP/notebook_templates/multiome/04_regulatory_programs.qmd | R/Seurat; reads predefined programs and scores RNA genes with AddModuleScore. It does not combine motif activity, links, and expression as described. | Rename to program scoring; TEMPLATE candidate |
| code_MAP/notebook_templates/general_statistics/01_group_summary_and_association_tests.qmd | R; accepts Seurat or data.frame, summarizes groups, uses Wilcoxon for numeric and chi-square for categorical variables, combines BH-adjusted p values, and makes boxplots. Minimal candidate, but lacks effect sizes and explicit assumption/zero-cell handling. | TEMPLATE candidate |

### 3.4 Project-specific computational-biology notebooks

| Source | Purpose, language, modality, task, and scientific distinctions | Eventual status |
|---|---|---|
| code_MAP/00_MAP_qc_integration.qmd | R/Seurat; four raw 10x scRNA samples, per-sample QC/doublet filtering, SCTransform, Harmony, LISI, clustering, UMAP/TSNE, SingleR. Contains an optional RPCA integration branch and an active Harmony branch. Uses project paths and samples. | EXAMPLE; archive original |
| code_MAP/00_MAP_RNA_qc_integration.qmd | R/Seurat; five scRNA samples with QC, Azimuth, CopyKAT, epithelial masking, doublet handling, log-normalized Harmony, annotation, and exports. Scientifically distinct from the SCTransform/Harmony notebook. | EXAMPLE |
| code_MAP/00_MAP_ATAC_qc_integration.qmd | R/Signac; five project scATAC samples, fragment-level QC, strict thresholds, per-sample plots/CSV, filtered objects, and later consensus/integration scaffolding. It is a project QC example, not the generic template. | EXAMPLE |
| code_MAP/001_RNA_ATAC_LT.qmd | R/Seurat/Signac; GSE274934 RNA-to-ATAC label transfer using GeneActivity, RPCA anchors, and TransferData. Good source for an annotation/label-transfer example. | EXAMPLE; possible future TEMPLATE source |
| code_MAP/002_ATAC_MOTIF.qmd | R/Signac; GSE274934 hg38 motif analysis using JASPAR2024/TFBSTools, DA peaks, FindMotifs, and MotifPlot. More concrete than the generic motif scaffold. | EXAMPLE; possible future TEMPLATE source |
| code_MAP/00_CPTAC_LUAD_scoring | R/Quarto without an extension; CPTAC LUAD bulk-like expression scoring. Converts FPKM/RPKM to TPM, log-transforms, and applies both singscore and GSVA plus project-specific scores. | EXAMPLE |
| code_MAP/simple_QC_MGI_organoids.qmd | R; tximport-derived bulk RNA-seq counts, DGEListFromTximport, duplicate-gene cleanup, TMMwsp CPM/logCPM, library/QC/outlier/correlation/PCA/clustering/PAM analysis. It has two CPM filtering paths (>5 and >1) and no DE stage. | EXAMPLE; strongest bulk QC/TEMPLATE source |
| code_MAP/GSE171145.qmd | R/Seurat; external LUAD cohort, raw counts/barcode maps, CopyKAT per sample, scDblFinder, Harmony, Azimuth, QC and scoring. Cohort-specific and too large for a template. | EXAMPLE |
| code_MAP/GSEA_of_DEGs.qmd | R/clusterProfiler; OVC High_TME versus Low_TME ranked DEG enrichment with GO and KEGG GSEA, simplify, term similarity, and plots. It assumes DEGs already exist. | EXAMPLE; possible GSEA template source |
| code_MAP/HALLMARK_50.qmd | R/singscore; Hallmark-50 scoring from logCPM with summaries/plots. This is distinct from GSEA, GSVA, UCell, and decoupler activity. | EXAMPLE; possible bulk scoring template source |
| code_MAP/01_MAP_metadata_bridge.qmd | R/Seurat; project metadata/sample-ID bridge and validation. Useful evidence for metadata checks, but not a general analysis stage. | EXAMPLE or helper requirements source |
| code_MAP/01_MAP_c1_scoring.qmd | R/Seurat; complex C1 plasticity scoring with UCell up/down signatures, raw and kNN-smoothed scores, CytoTRACE2, SCEVAN, cell cycle, and project plots/statistics. | EXAMPLE |
| code_MAP/02_MAP_c1_scoring.qmd | R/Seurat; earlier/simpler C1 scoring from existing UCell up/down fields, transformed score variants, CytoTRACE2 comparison, and statistics. It overlaps 01 but is not identical. | ARCHIVE or EXAMPLE pending provenance |
| code_MAP/03_MAP_state_markers_statistics_export.qmd | R/Seurat plus Python export; all-cluster markers, gProfiler/ORA, GO/KEGG GSEA, nonparametric/linear statistics, optional velocity/CellRank metadata, and h5ad export. Large project reporting stage. | EXAMPLE |
| code_MAP/04_MAP_c1_gene_programs_tradeSeq.qmd | R/Seurat/slingshot/tradeSeq; C1-score-derived lineage/pseudotime, fitGAM, association tests, Spearman evidence, concordance, and enrichment. This is the repository's genuine trajectory/tradeSeq source. | EXAMPLE; future TEMPLATE source after generalization |
| code_MAP/04_MAP_decoupler_bridge.qmd | R plus Python/AnnData; exports Seurat RNA to h5ad, runs decoupler ULM TF/pathway scoring, imports score tables, and stores regulatory assays. This is a real cross-language regulatory bridge. | EXAMPLE; future bridge TEMPLATE source |
| code_MAP/05_MAP_regulatory_programs.qmd | R/Seurat; TF activity, pathway/Hallmark, surface/secreted markers, correlations, and metabolic links from a regulatory-ready object. Project-specific interpretive notebook. | EXAMPLE |
| code_MAP/06_MAP_coexpression_modules.qmd | R/Seurat/hdWGCNA; metacells, soft threshold, network/modules, eigengenes, connectivity, hubs, module scores, and enrichment. This is the genuine coexpression implementation. | EXAMPLE; future TEMPLATE source |
| code_MAP/07_MAP_velocity_scvelo_cellrank.qmd | R plus Python/AnnData; project bridge and scVelo/CellRank workflow with barcode fixes and many diagnostic plots. More complete than the current minimal template but project-bound. | EXAMPLE; future velocity TEMPLATE source |
| code_MAP/08_MAP_metabolic_activity_scCellFie.qmd | Python/AnnData; actual scCellFie metabolic activity and cluster marker/task analysis, including marker-task export. | EXAMPLE; future metabolic TEMPLATE source |
| code_MAP/09_MAP_C1_Core_refined_signature.qmd | R/Seurat; refined C1-Core UCell up/down signature, z-score, evidence union from tradeSeq, Spearman genes, TF activity, hdWGCNA hubs, and kinetic evidence, with group/cluster statistics. Project-specific biological refinement, not a generic scorer. | EXAMPLE |
| code_MAP/10_MAP_extensive_statistics.qmd | R/Quarto; mostly a plan/reader guide for post-hoc C1-EpiCore robustness, permutation, correlations, and cross-modal comparisons. Little executable analysis. | ARCHIVE or REVIEW |
| TRENTO_models_miRNA_vs_PD_L1.qmd | R/tidymodels; held-out miRNA binary classification, feature selection, normalization, 200-times Monte Carlo CV, bias-reduced logistic regression, threshold tuning, and metrics. Strong analysis example but fixed split and PD-L1 project contract. | EXAMPLE; future ML TEMPLATE source |
| TRENTO_gtExtras_tables.qmd | R/gt/gtExtras; publication/report tables, probabilities, and miRNA heatmap from TRENTO outputs. Presentation layer, not a general modeling stage. | EXAMPLE |

### 3.5 MOFA files

| Source | Purpose and assessment | Eventual status |
|---|---|---|
| code_MOFA/00_TCGA_LUAD_multiomics_download.qmd | R/TCGAbiolinks; TCGA GDC acquisition of RNA, miRNA, methylation, RPPA, and mutation for primary LUAD. Fixed data source and cohort. | EXAMPLE; archive |
| code_MOFA/01_TCGA_LUAD_scoring_tf.qmd | R; TCGA RNA harmonization, edgeR processing, ConsensusTME/EpiDISH/GSVA/METAFlux/SecAct and TF/pathway scores. Very large project scoring notebook. | EXAMPLE; archive |
| code_MOFA/03_MOFA.qmd | R/MOFA2; live project multi-view factor modeling, factor summaries, heatmaps, and interpretation. | EXAMPLE; source for core MOFA template |
| code_MOFA/MOFA_TEMPLATE_CLEAN/00_project_setup.qmd | R/Quarto; project paths, identifiers, resource settings, and output directories. It is configuration/bootstrap rather than an analytical stage. | Merge into README/config guidance later |
| code_MOFA/MOFA_TEMPLATE_CLEAN/01_multiomics_input_prep.qmd | R; fixed five-view TCGA-like input matching by 16-character barcode and matched-table export. | TEMPLATE candidate only after generalization |
| code_MOFA/MOFA_TEMPLATE_CLEAN/02_signature_scoring.qmd | R; reads matched RNA and signature CSV, calls hidden CPM/logCPM normalization, computes mean score, z classes, and writes metadata. C1-specific and hides scientific choices in a helper. | Split; example or future scoring TEMPLATE |
| code_MOFA/MOFA_TEMPLATE_CLEAN/03_mofa_model.qmd | R/MOFA2; loads views, retains variable features, trains model, exports factors and extensive C1/group/heatmap interpretation. At 1,162 lines it is not minimal. | Split into core TEMPLATE and optional example |
| code_MOFA/MOFA_TEMPLATE_CLEAN/helpers/helpers_from_MOFA.R | R helper file; barcode trimming, duplicate collapse, CPM/logCPM, class_from_z, plot saving, variable selection, matrix coercion, and manifest writing. It mixes mechanical, scientific, and project-specific functions and uses global directories. | REVIEW; trim before HELPER promotion |

### 3.6 Scripts, logs, and compressed archives

| Source | Purpose and assessment | Eventual status |
|---|---|---|
| CODE_MAP/alevin_fry/scripts/run_simpleaf_velocity.sh | Shell; attempts simpleaf velocity quantification. Likely reusable only after documenting reference/index/input contracts. | EXAMPLE or ARCHIVE |
| CODE_MAP/alevin_fry/scripts/quant.log | Log from a quantification attempt. | ARCHIVE; delete only after provenance review |
| CODE_MAP/alevin_fry/scripts/run.log | Four-line failed run log reporting a missing index. | ARCHIVE or DELETE_CANDIDATE after review |
| CODE_MAP/code_MAP/Archive.zip | Historical archive containing older MAP notebooks and macOS metadata. It contains exact duplicates of current velocity and metabolic notebooks and near-duplicates of several others. | ARCHIVE; later deduplicate |
| CODE_MAP/Task for 2nd interview.zip | Compressed interview analysis with clinical breast-cancer proteomics, CORUM data, PPI/network analysis, PCA, modules, enrichment, results, and images. It contains unique scientific work but is not a template. | ARCHIVE or EXAMPLE after unpack/review |

The interview archive contains at least CORUM_data.txt, proteomics_data.txt, DDLS_PhD_Round2_Task_v2.md, analysis_ppi_network_patched.qmd, result TSVs, PNGs, and archive metadata. The analysis is a legitimate network/proteomics example, but its data and results should not be promoted into the reusable surface without a deliberate privacy, licensing, and data-size review.

## 4. Analytical workflow inventory

| Family | Implementations found | Scientific alternatives or gaps | Recommended library treatment |
|---|---|---|---|
| Bulk RNA-seq import/QC | simple_QC_MGI_organoids.qmd and the former RNA-seq reference | tximport/DGEListFromTximport, raw count cleanup, TMMwsp, CPM/logCPM, MAD/PCA/correlation; project paths and filter thresholds | One visible bulk QC/normalization template; retain threshold choices in notebook |
| Bulk differential expression | No complete active implementation | GSEA notebook consumes DEGs; edgeR methods appear in other projects but not a general bulk DE stage | Do not invent a template yet; add only when an actual DE analysis is generalized |
| Bulk pathway/GSEA | GSEA_of_DEGs.qmd | Ranked GO/KEGG GSEA differs from per-sample Hallmark scoring | Separate GSEA template and signature-scoring example |
| Bulk signature scoring | HALLMARK_50.qmd, 00_CPTAC_LUAD_scoring | singscore, GSVA, and project-specific score methods are not interchangeable | Preserve methods as separate examples or explicitly named alternatives |
| Seurat object creation | scRNA template 01, project MAP/RNA/GSE171145 files | Raw count contracts and metadata conventions differ | One minimal RNA object template; examples for Azimuth/CopyKAT workflows |
| scRNA QC | scRNA template 02, MAP RNA and GSE171145 notebooks | Fixed thresholds versus MAD-derived thresholds; doublet and CNV tools add distinct decisions | One simple QC template; project QC remains examples |
| scRNA normalization | NormalizeData in template 03 and some projects; SCTransform in MAP QC | Log normalization and SCTransform are scientifically different | Keep visible as separate named approaches if both are needed |
| scRNA dimensionality reduction/clustering | template 03 and multiple project files | PCA/UMAP/neighbors/resolution differ; clustering is sensitive to assay and integration choices | One basic stage plus optional integration stage |
| Batch integration | Harmony, RPCA, SCTransform integration, and log-normalized Harmony in project files | These are not API variants of one identical method | Separate Harmony and RPCA templates only if both recur; never hide inside clustering |
| scRNA annotation | SingleR, Azimuth, label transfer in project files | Reference choice and transfer assumptions are biological decisions | Future annotation/label-transfer template; current files are examples |
| Marker discovery | template 05, 03_MAP_state_markers_statistics_export | FindMarkers versus FindAllMarkers; statistical grouping and thresholds differ | Separate group comparison from all-cluster marker template if both are retained |
| Gene/signature scoring | AddModuleScore templates, UCell C1 notebooks, singscore, GSVA | Different normalization, null/reference behavior, and interpretation | Name each method explicitly; do not merge into one opaque scorer |
| Pathway activity | decoupler bridge, GSVA, singscore, precomputed activity import | Inference, per-cell scoring, and score attachment are different operations | Separate score computation templates from score-import helper/stage |
| Trajectory/pseudotime | real Slingshot/tradeSeq notebook; current binned pseudotime template | Pseudotime inference, tradeSeq GAM testing, and descriptive binning are distinct | Three names if needed: inference, tradeSeq testing, pseudotime summary |
| RNA velocity | project scVelo/CellRank and minimal Python template | Filtering/moments/velocity model choices; AnnData bridge required | One scVelo diagnostic template and a separate CellRank fate template |
| CellRank | VelocityKernel transition matrix in template/project | No terminal-state estimator or fate probabilities in current scaffold | Do not call current file a complete CellRank template |
| Coexpression | true hdWGCNA project notebook; module-score scaffold | Network inference versus predefined gene-set score | Promote hdWGCNA only after generalization; rename scaffold |
| Regulatory programs | decoupler bridge, large regulatory notebook, simple AddModuleScore scaffold | TF activity, pathway activity, linked peaks, and RNA gene scores are distinct | Keep bridge and interpretation separate |
| Metabolic analysis | real scCellFie project notebook; score-import scaffold | Computation versus imported score attachment | Future scCellFie template from real source; rename importer |
| scATAC object/QC | Signac templates and MAP/GSE project notebooks | Fragment QC, TSS/nucleosome/blacklist thresholds, consensus peaks differ | One minimal object template and one visible QC/LSI stage; examples for strict project QC |
| scATAC motif | generic PFM/FindMotifs template and JASPAR2024 project notebook | PFM database, genome, peak universe, DA threshold, chromVAR versus motif enrichment | Keep FindMotifs and chromVAR as distinct methods |
| Multiome object/WNN | multiome templates and project bridge | RNA/ATAC assay construction, WNN, and batch correction are separate | Keep object creation, WNN, batch integration, and linkage separate |
| RNA/ATAC linkage | multiome LinkPeaks template | Distance, expression/peak assay and genome assumptions | Genuine standalone template candidate |
| MOFA/multiomics | live TCGA notebooks and clean MOFA directory | View matching, feature filtering, missingness, factor number, training, and interpretation are separate | Split input matching, model fit, and optional interpretation |
| Statistics | general statistics template and project statistics | Wilcoxon/chi-square are minimal tests; effect sizes, covariates, repeated measures, and survival are absent | Keep minimal group-association stage; add methods only when justified |
| Visualization/reporting | Quarto guides, gtExtras, plotting code throughout notebooks | Report formatting is not an analytical template | Keep as compact references/examples; generic plot saving may be a helper |
| Machine learning | TRENTO notebook | Fixed train/test split, supervised feature selection, bias-reduced logistic regression, repeated Monte Carlo CV | Example now; future template only after a clear generic contract |
| Data import/export | qs/qs2, saveRDS, h5ad, TSV/CSV, GDC/TCGAbiolinks, tximport | Persistence formats and naming are inconsistent | Document a small supported contract; generic wrappers only if repetition justifies them |
| Object persistence | qs2 in templates; qs, qsave/qread, saveRDS, h5ad in projects | Format choice is partly ecosystem-specific; no version/session records found | Keep format visible in templates; optional small I/O helpers |

## 5. Duplicate and overlap analysis

### 5.1 Template scaffolding duplication

The 18 notebook templates share a repeated report shell: purpose, package loading, user configuration, input loading, validation, input summary, main analysis, QC, visualization, object saving, result export, and final summary. Pairwise comparison found no exact duplicate template, but the highest normalized overlaps are:

- multiome/01_create_multiome_object versus scATAC/01_create_signac_object: 41 common normalized lines, similarity approximately 0.62;
- scATAC/02_quality_control_integration versus scRNA/03_normalization_integration_clustering: 38 common lines, approximately 0.53;
- multiome/02_qc_integration_wnn versus scATAC/02_quality_control_integration: 39 common lines, approximately 0.53;
- scATAC/03_motif_enrichment versus scRNA/05_marker_identification_and_export: 37 common lines, approximately 0.50.

These overlaps are mostly wrapper mechanics and validation, not evidence that the scientific methods should be merged. The wrappers are a reasonable helper opportunity, but each scientific operation should remain visible.

### 5.2 Scientific overlaps that must remain distinct

Normalization:

- edgeR TMMwsp CPM/logCPM for bulk counts;
- Seurat NormalizeData/log normalization;
- Seurat SCTransform;
- FPKM/RPKM-to-TPM conversion in the CPTAC notebook.

These cannot be collapsed into a generic normalize function without hiding scale, input, and downstream assumptions.

Integration:

- Harmony on SCTransform data;
- Harmony on log-normalized data;
- RPCA integration;
- optional Seurat IntegrateLayers;
- WNN for combining RNA and ATAC neighborhoods.

WNN is not a replacement for batch correction. Harmony and RPCA are alternative integration decisions, not merely implementation versions.

Scoring:

- AddModuleScore for predefined gene modules;
- UCell up/down score construction;
- singscore;
- GSVA;
- decoupler ULM activity;
- scCellFie metabolic activity.

These differ in input transformation, null model, feature-set interpretation, and dependency requirements. The canonical library should prefer explicit method names over one “score signature” abstraction.

Trajectory and dynamics:

- the current template only summarizes an existing pseudotime;
- the MAP tradeSeq notebook fits GAMs along a lineage;
- scVelo estimates RNA velocity;
- CellRank uses transition kernels and, in a complete workflow, fate estimators.

These answer different questions and should not be one template.

Coexpression and gene modules:

- the current module template scores predefined genes;
- MAP 06 infers networks and modules with hdWGCNA.

The latter is computationally and scientifically heavier, but it is the actual coexpression implementation.

### 5.3 Historical archive duplicates

Archive.zip contains:

- an exact duplicate of the current 07_MAP_velocity_scvelo_cellrank.qmd;
- an exact duplicate of the current 08_MAP_metabolic_activity_scCellFie.qmd;
- near-duplicates of current ATAC QC, RNA QC, C1 scoring, and regulatory notebooks.

Keep the zip intact until provenance is checked. After that, one preserved historical copy is enough; exact embedded duplicates are delete candidates.

### 5.4 Documentation duplication

The former Quarto reference and `CODE_MAP/quarto_config_tmplate.md` had approximately 0.76 sequence similarity and described overlapping Quarto report conventions. The former reference material is now retired; current guidance is maintained under `miscellaneous/quarto/`.

### 5.5 C1 scoring evolution

01_MAP_c1_scoring.qmd and 02_MAP_c1_scoring.qmd share a title and project concept but differ substantially in scope and likely represent evolution rather than simple duplication. 01 includes more QC/annotation/statistical context; 02 is a simpler score derivation from existing UCell columns. 09_MAP_C1_Core_refined_signature.qmd is a later biological refinement that combines multiple evidence sources. Do not merge or delete these by line similarity alone.

## 6. Scientific inconsistencies discovered

These are static findings requiring review before promotion. They are not fixed in this audit.

1. scRNA QC output mismatch. scRNA/02_quality_control.qmd creates filtered and exports filtered metadata, but its final save writes object. The saved qs2 object is therefore apparently unfiltered.
2. Misnamed scRNA integration. scRNA/03_normalization_integration_clustering.qmd has no integration call. batch_column is unused. Rename or add a separately justified integration stage later.
3. Misnamed scATAC integration. scATAC/02_quality_control_integration.qmd performs QC, TF-IDF, LSI, neighbors, clustering, and UMAP but no batch correction.
4. WNN terminology. multiome/02_qc_integration_wnn.qmd performs RNA/ATAC WNN construction. It should not be presented as batch integration.
5. Trajectory overclaim. scRNA/06 assumes pseudotime and bins features; it does not infer a trajectory or run tradeSeq.
6. Pathway activity overclaim. scRNA/07 attaches a precomputed activity table; it does not call decoupler or calculate pathway scores.
7. Coexpression overclaim. scRNA/08 scores predefined modules with AddModuleScore; it does not infer coexpression modules.
8. Velocity/CellRank incompleteness. scRNA/09 computes scVelo quantities and a VelocityKernel transition matrix but no CellRank terminal states or fate probabilities.
9. Metabolic overclaim. scRNA/10 attaches precomputed metabolic scores; it does not run scCellFie.
10. Motif overclaim. scATAC/03 does AddMotifs and FindMotifs but no RunChromVAR. genome=NULL also leaves an important genome/sequence assumption implicit.
11. Regulatory-program overclaim. multiome/04 only scores RNA programs; it does not combine motif activity, peak links, and expression summaries.
12. MOFA helper hides science. compute_cpm and compute_logcpm contain filtering and TMMwsp normalization. These are analytical decisions that should remain visible in a template.
13. MOFA helper contains domain logic. class_from_z encodes C1-specific class cutoffs and should not be a generic helper.
14. MOFA helper uses hidden global state. save_plot_png depends on global FIG_DIR and FIG_DPI; write_output_manifest depends on metadata_dir and table_dir.
15. MOFA helper contract mismatch. write_output_manifest writes CSV and uses global paths, while the clean README describes TSV output and explicit output directories.
16. MOFA helper shadowing. 01_multiomics_input_prep.qmd defines its own write_output_manifest after sourcing the helper, making the shared function ineffective or ambiguous.
17. MOFA is not yet minimal. 03_mofa_model.qmd is approximately 1,162 lines and includes core fitting plus many optional C1/group/heatmap interpretations. These should be separate stages.
18. Bulk filtering inconsistency. simple_QC_MGI_organoids.qmd contains both >1 CPM and >5 CPM filtering paths; the active path appears to use >5 in compute_cpm, but this must be made explicit.
19. MAP QC branch ambiguity. 00_MAP_qc_integration.qmd contains an optional RPCA IntegrateLayers branch while the active path uses SCTransform plus Harmony. The notebook says Harmony is preferred, but both methods remain in the executable document.
20. MAP QC threshold comment mismatch. The QC helper defaults to k=3 while the active configuration uses mad_multiplier=5, and a comment describes 3 as the correct baseline. This needs a deliberate scientific choice.
21. MAP static syntax issue. 00_MAP_qc_integration.qmd contains a RunTSNE call with a double comma in its argument list. It should not be used as a canonical source without a syntax/runtime check.
22. Metadata assumptions are hidden. Several templates assume exact column names, first-column cell IDs, complete row alignment, or project-specific assay names.
23. Output contracts are inconsistent. Templates use qs2 and h5ad, while project files use qs, qsave/qread, saveRDS, CSV, and TSV. The library needs a small documented contract rather than invisible conversion.
24. Reproducibility records are incomplete. No lockfile, renv record, conda environment, Python requirements file, session information, or stable source-data manifest was found in the audited tree.
25. Static versus runtime status is not separated. This report did not render or execute notebooks; API compatibility, syntax, memory use, and output correctness still require targeted validation.

## 7. Misleading filenames or organization

| Current name or organization | Problem | Better future name |
|---|---|---|
| code_MAP | A personal project prefix, not a reusable analytical category. | examples/single_cell or examples/multiome after classification |
| 00_MAP_qc_integration.qmd | “Integration” includes multiple branches and project-specific processing. | example_map_sctransform_harmony.qmd |
| 00_MAP_RNA_qc_integration.qmd | Mixes QC, Azimuth, CopyKAT, and Harmony. | example_map_qc_cnv_annotation.qmd |
| 00_MAP_ATAC_qc_integration.qmd | Project QC and later integration scaffolding are bundled. | example_map_scatac_qc.qmd |
| scRNA/03_normalization_integration_clustering.qmd | No integration is performed. | normalization_reduction_clustering.qmd |
| scATAC/02_quality_control_integration.qmd | No integration is performed. | quality_control_lsi_clustering.qmd |
| multiome/02_qc_integration_wnn.qmd | WNN is not batch integration. | wnn_neighbors_clustering.qmd |
| scRNA/06_trajectory_gene_programs.qmd | Assumes pseudotime and summarizes features. | pseudotime_gene_program_summary.qmd |
| scRNA/07_pathway_activity_decoupler.qmd | Imports activity scores and does not run decoupler. | import_activity_scores.qmd |
| scRNA/08_coexpression_modules.qmd | Scores predefined modules rather than inferring coexpression. | gene_module_scoring.qmd |
| scRNA/09_velocity_scvelo_cellrank.qmd | Partial CellRank kernel stage, not a complete fate analysis. | scvelo_velocity_diagnostic.qmd |
| scRNA/10_metabolic_activity.qmd | Imports precomputed scores, not metabolic computation. | import_metabolic_scores.qmd |
| multiome/04_regulatory_programs.qmd | Scores RNA programs only. | rna_program_scoring.qmd |
| code_MOFA/MOFA_TEMPLATE_CLEAN | “Clean” suggests generality that fixed TCGA/C1 assumptions do not support. | split into multiomics stages after cleanup |
| code_MAP/01_MAP_c1_scoring.qmd and 02_MAP_c1_scoring.qmd | Same title/number family for different implementations. | names based on scoring method and provenance |
| CODE_MAP/quarto_config_tmplate.md | Typo and placement made it easy to miss the duplicate guide. | Retired; see `miscellaneous/quarto/` for current guidance. |
| notebook_templates | Contains importers, summaries, and method stubs presented alongside real stages. | templates after method-specific renaming |

## 8. Candidate canonical templates

The following is a proposed shortlist, not a decision to create files now.

### High-confidence candidates

| Future template | Source basis | Why it is a good candidate | Required caveat |
|---|---|---|---|
| templates/bulk_rna/qc_normalization.qmd | simple_QC_MGI_organoids.qmd plus the former RNA-seq reference | Only substantial bulk RNA QC/normalization implementation; uses tximport and edgeR visibly. | Resolve >1 versus >5 CPM and define count/input contract |
| templates/single_cell/create_seurat_object.qmd | notebook_templates/scRNA/01 | Minimal, readable, meaningful stage. | Define matrix orientation and cell-ID metadata contract |
| templates/single_cell/quality_control.qmd | notebook_templates/scRNA/02 | Simple explicit thresholds and QC export. | Save filtered object and expose threshold policy |
| templates/single_cell/normalization_reduction_clustering.qmd | notebook_templates/scRNA/03 | Readable basic Seurat workflow. | Remove “integration” from name; keep normalization choice explicit |
| templates/single_cell/signature_scoring_addmodulescore.qmd | notebook_templates/scRNA/04 | Minimal visible gene-set scoring stage. | Keep UCell, singscore, GSVA, and decoupler separate |
| templates/single_cell/marker_analysis_group_comparison.qmd | notebook_templates/scRNA/05 | A complete small FindMarkers stage with exports. | State whether group-vs-group is the intended contract |
| templates/scatac/create_signac_object.qmd | notebook_templates/scATAC/01 | Clear Signac object-construction stage. | Require genome, fragments, separator, and assay contracts |
| templates/scatac/quality_control_lsi_clustering.qmd | notebook_templates/scATAC/02 | Complete minimal QC-to-LSI/clustering stage. | Do not call it integration; define dimensions and thresholds |
| templates/scatac/motif_enrichment_findmotifs.qmd | notebook_templates/scATAC/03 plus 002_ATAC_MOTIF.qmd | Represents an actual method distinct from chromVAR. | Make genome/PFM/peak universe explicit |
| templates/multiome/create_object.qmd | notebook_templates/multiome/01 | Meaningful paired-assay construction stage. | Validate shared cell IDs and genome |
| templates/multiome/wnn.qmd | notebook_templates/multiome/02 | A genuine multimodal neighbor stage. | Separate from batch integration |
| templates/multiome/rna_atac_linkage.qmd | notebook_templates/multiome/03 | Genuine LinkPeaks stage with useful visualization. | Expose distance, assay, and genome choices |
| templates/statistics/group_association_tests.qmd | notebook_templates/general_statistics/01 | Small, readable baseline for simple group tests. | Add effect sizes and explicit unsupported designs later |

### Candidates only after generalization

| Future template | Source basis | Reason it is not ready |
|---|---|---|
| templates/single_cell/batch_integration_harmony.qmd | MAP Harmony notebooks | Multiple assays/normalizations and project-specific QC; method choice must be isolated |
| templates/single_cell/batch_integration_rpca.qmd | MAP optional RPCA and label-transfer notebook | Needs a clean, tested contract and must remain distinct from Harmony |
| templates/single_cell/annotation_label_transfer.qmd | 001_RNA_ATAC_LT.qmd, Azimuth, SingleR sections | Reference object, labels, assay, and mapping assumptions are not generic |
| templates/single_cell/trajectory_tradeseq.qmd | 04_MAP_c1_gene_programs_tradeSeq.qmd | Real method, but lineage and pseudotime are tied to C1 biology |
| templates/single_cell/velocity_scvelo.qmd | project 07 plus current template 09 | Need a clean R/AnnData boundary and explicit velocity-model choices |
| templates/single_cell/cellrank_fate.qmd | project 07 | Current code lacks a complete fate-estimation stage |
| templates/single_cell/coexpression_hdWGCNA.qmd | 06_MAP_coexpression_modules.qmd | Heavy dependencies and metacell/network choices require a narrowly documented contract |
| templates/single_cell/metabolic_activity_sccellfie.qmd | 08_MAP_metabolic_activity_scCellFie.qmd | Python/data/task inputs need generalization |
| templates/multiomics/match_samples.qmd | MOFA clean 01 | Fixed five TCGA views and 16-character barcodes are not general |
| templates/multiomics/mofa_fit.qmd | MOFA clean 03 | Must split core factor fitting from project interpretation |
| templates/multiomics/mofa_interpretation.qmd | MOFA clean 03 | Optional C1/group/heatmap outputs should not be forced into core |
| templates/machine_learning/binary_classification.qmd | TRENTO model | Feature selection, split, CV, class weighting, and model family are project choices |
| templates/proteomics_network/network_analysis.qmd | Task for 2nd interview.zip | Unique source exists, but data/result separation and generality are unreviewed |

There is not enough source evidence for templates/spatial. Keep the category out of the active tree until a real spatial workflow exists.

## 9. Candidate helpers

Helpers should be mechanical and boring. They should reduce repeated plumbing without hiding analytical decisions.

### Good R helper candidates

- Create declared output directories and return their paths.
- Check required columns, unique identifiers, non-empty intersections, and metadata/object row alignment.
- Save a plot to a supplied path with explicit width, height, units, and DPI; do not depend on FIG_DIR or FIG_DPI globals.
- Read/write a declared object format when the format is already part of the template contract.
- Write a TSV with a declared path and stable column handling.
- Check matrix orientation and duplicate identifiers, returning a clear diagnostic.

### Good Python helper candidates

- Create output directories using pathlib.
- Check AnnData observation identifiers against imported score tables.
- Save figures and AnnData objects to supplied paths.
- Validate required obs/var columns and complete ID coverage.

### Helpers that should not be generic

- compute_cpm and compute_logcpm: filtering and TMMwsp normalization are scientific decisions.
- class_from_z: C1-specific class definitions.
- tcga_sample_barcode: useful only in a clearly named TCGA preprocessing context, not a universal sample-ID helper.
- collapse_duplicate_samples_mean/sum/max: may be a scoped TCGA/data-cleaning helper, but the aggregation choice must remain visible.
- scVelo filtering, moments, velocity, CellRank, scCellFie, WGCNA/hdWGCNA, decoupler, MOFA fitting, normalization, integration, clustering, marker testing, and signature scoring.

The current helpers_from_MOFA.R should not be promoted unchanged. It mixes the two categories, relies on globals, and hides an analysis step.

## 10. Candidate examples

Examples should demonstrate real scientific choices and complete project context while being clearly labeled as non-canonical.

### Single-cell and multiome examples

- code_MAP/00_MAP_qc_integration.qmd: SCTransform plus Harmony, MAD QC, doublet handling, LISI, and the competing RPCA branch.
- code_MAP/00_MAP_RNA_qc_integration.qmd: log-normalized Harmony, Azimuth, CopyKAT, and cohort-specific QC.
- code_MAP/00_MAP_ATAC_qc_integration.qmd: strict fragment/TSS/nucleosome/blacklist QC and project consensus-peak scaffolding.
- code_MAP/001_RNA_ATAC_LT.qmd: RNA-to-ATAC label transfer.
- code_MAP/002_ATAC_MOTIF.qmd: JASPAR2024 motif enrichment.
- code_MAP/GSE171145.qmd: external LUAD processing, CopyKAT, and Azimuth.
- code_MAP/03_MAP_state_markers_statistics_export.qmd: integrated project marker/statistics/export reporting.

### C1, pathway, regulatory, and dynamics examples

- code_MAP/01_MAP_c1_scoring.qmd, 02_MAP_c1_scoring.qmd, and 09_MAP_C1_Core_refined_signature.qmd: evolving C1 score implementations; preserve provenance.
- code_MAP/04_MAP_c1_gene_programs_tradeSeq.qmd: genuine tradeSeq workflow.
- code_MAP/04_MAP_decoupler_bridge.qmd: genuine R/Python decoupler bridge.
- code_MAP/05_MAP_regulatory_programs.qmd: project regulatory interpretation.
- code_MAP/06_MAP_coexpression_modules.qmd: genuine hdWGCNA coexpression analysis.
- code_MAP/07_MAP_velocity_scvelo_cellrank.qmd: project velocity/dynamics workflow.
- code_MAP/08_MAP_metabolic_activity_scCellFie.qmd: actual scCellFie workflow.

### Bulk, multiomics, and machine learning examples

- code_MAP/00_CPTAC_LUAD_scoring: bulk-like CPTAC score comparison using singscore and GSVA.
- code_MAP/simple_QC_MGI_organoids.qmd: bulk RNA QC/normalization source.
- code_MAP/GSEA_of_DEGs.qmd: ranked GO/KEGG enrichment.
- code_MAP/HALLMARK_50.qmd: per-sample Hallmark scoring with singscore.
- code_MOFA/00_TCGA_LUAD_multiomics_download.qmd, 01_TCGA_LUAD_scoring_tf.qmd, and 03_MOFA.qmd: live TCGA/MOFA project.
- TRENTO_models_miRNA_vs_PD_L1.qmd and TRENTO_gtExtras_tables.qmd: model and report examples.
- Task for 2nd interview.zip: proteomics/PPI/network example only after data separation and review.

## 11. Candidate reference material

The audit proposed a small reference layer, but no active cheatsheet collection is retained:

- one canonical Quarto report guide, selected from the former reference material and `CODE_MAP/quarto_config_tmplate.md`;
- the former RNA-seq normalization reference as a starting normalization reference, reconciled with the final bulk template;
- a future short “method choice” guide covering TMM/logCPM versus SCTransform, Harmony versus RPCA, WNN versus batch integration, GSEA versus per-cell scoring, and UCell/AddModuleScore/singscore/GSVA/decoupler distinctions;
- a future input/output contract guide covering cell IDs, metadata alignment, assay names, matrix orientation, qs2/h5ad, TSV, and provenance records.

The current Quarto documents are guidance, not visualization templates or infrastructure. The proposed visualization directory should therefore not be populated automatically.

## 12. Archive candidates

Archive before deleting when provenance may matter:

- all project-specific MAP notebooks not promoted to a general template;
- the original TCGA download, scoring, and MOFA notebooks;
- the current MOFA clean structure and inventory notes until the replacement is validated;
- older C1 scoring variants;
- 10_MAP_extensive_statistics.qmd because it records planned analyses even though it is mostly non-executable;
- Archive.zip as a historical snapshot;
- Task for 2nd interview.zip and its data/results;
- alevin_fry logs and script if the velocity reference/index attempt is part of provenance;
- the current notebook_templates README, inventory, and ponytail audit after their claims are superseded;
- the duplicate Quarto guide, if not selected as canonical;
- exact duplicate archive members after a retained historical copy is confirmed.

Archive layout should distinguish raw historical snapshots from curated examples. Do not leave archives adjacent to active templates where users can mistake them for supported code.

## 13. Delete candidates

Deletion should be conservative. Current candidates are limited to:

- root .DS_Store;
- CODE_MAP/.DS_Store;
- macOS metadata members inside a repacked archive;
- exact duplicate copies of current velocity and metabolic notebooks inside Archive.zip, after the archive's provenance value is preserved elsewhere;
- the non-selected duplicate Quarto guide, but only after unique guidance is manually compared;
- run.log, only if the failed missing-index attempt has no provenance value;
- other generated logs only after confirming they are not needed to reconstruct a result.

No scientific Quarto notebook should be deleted merely because it is long, project-specific, old, or similar to another notebook. The two C1 scoring notebooks, MAP branches, MOFA live/clean versions, and interview archive all require manual review before deletion.

## 14. Proposed final directory tree

The user's proposed top-level tree is broadly appropriate, but it needs method-specific stages and a possible network/proteomics category. A conservative future tree is:

    README.md
    LICENSE
    templates/
      bulk_rna/
        qc_normalization/
        differential_expression/          # add only after a real DE stage is generalized
        gsea/
        pathway_scoring/
      single_cell/
        create_seurat_object/
        quality_control/
        normalization_reduction_clustering/
        batch_integration/
        annotation_label_transfer/
        marker_analysis/
        signature_scoring/
        pseudotime_feature_summary/
        trajectory_tradeseq/
        velocity/
        cellrank_fate/
        pathway_activity/
        coexpression_hdWGCNA/
        metabolic_activity/
      scatac/
        create_signac_object/
        quality_control/
        lsi_reduction_clustering/
        batch_integration/
        motif_enrichment/
      multiome/
        create_object/
        wnn/
        batch_integration/
        rna_atac_linkage/
        regulatory_program_scoring/
      multiomics/
        match_samples/
        mofa_input/
        mofa_fit/
        mofa_interpretation/
      statistics/
        group_association_tests/
        correlation_effect_sizes/
      machine_learning/
        binary_classification/
      proteomics_network/                 # create only if interview analysis is worth curating
        network_analysis/
    helpers/
      R/
      python/
    examples/
      bulk_rna/
      single_cell/
      scatac/
      multiome/
      multiomics/
      proteomics_network/
    archive/
      legacy_map/
      legacy_mofa/
      legacy_templates/
      raw_archives/

Two adjustments are important:

1. spatial should not be created as an active category without source code.
2. visualization is better represented by compact references and example report outputs than by an analysis-template directory, unless reusable plotting code later accumulates.

## 15. Source-file to proposed-destination mapping

This mapping is intentionally a plan. It does not authorize the moves.

| Current source | Proposed destination or treatment | Status |
|---|---|---|
| README.md | README.md, rewritten later to describe the curated library | REVIEW |
| LICENSE | LICENSE | PRESERVE |
| AGENTS.md, CLAUDE.md, .claude/skills/gitnexus/*.md | remain as project metadata | PRESERVE |
| Former Quarto reference | Retired; current report guidance is under `miscellaneous/quarto/` | REFERENCE |
| CODE_MAP/quarto_config_tmplate.md | merge unique guidance into the canonical Quarto guide, then archive/delete candidate | REVIEW |
| Former RNA-seq normalization reference | Retired | REFERENCE |
| code_MAP/notebook_templates/README.md | archive/legacy_templates/README.md or replace with new library README | ARCHIVE |
| code_MAP/notebook_templates/NOTEBOOK_INVENTORY.md | archive/legacy_templates/NOTEBOOK_INVENTORY.md | ARCHIVE |
| code_MAP/notebook_templates/PONYTAIL_AUDIT.md | archive/legacy_templates/PONYTAIL_AUDIT.md | ARCHIVE |
| notebook_templates/scRNA/01_create_seurat_object.qmd | templates/single_cell/create_seurat_object/ | TEMPLATE |
| notebook_templates/scRNA/02_quality_control.qmd | templates/single_cell/quality_control/ | TEMPLATE after save fix |
| notebook_templates/scRNA/03_normalization_integration_clustering.qmd | templates/single_cell/normalization_reduction_clustering/ | TEMPLATE after rename |
| notebook_templates/scRNA/04_signature_scoring.qmd | templates/single_cell/signature_scoring/ | TEMPLATE |
| notebook_templates/scRNA/05_marker_identification_and_export.qmd | templates/single_cell/marker_analysis/ | TEMPLATE |
| notebook_templates/scRNA/06_trajectory_gene_programs.qmd | templates/single_cell/pseudotime_feature_summary/ | TEMPLATE only after rename |
| notebook_templates/scRNA/07_pathway_activity_decoupler.qmd | templates/single_cell/pathway_activity/import_activity_scores/ | TEMPLATE only after rename |
| notebook_templates/scRNA/08_coexpression_modules.qmd | templates/single_cell/signature_scoring/gene_module_scoring/ | TEMPLATE only after rename |
| notebook_templates/scRNA/09_velocity_scvelo_cellrank.qmd | templates/single_cell/velocity/ | TEMPLATE after rename and completeness decision |
| notebook_templates/scRNA/10_metabolic_activity.qmd | templates/single_cell/metabolic_activity/import_scores/ or archive | REVIEW |
| notebook_templates/scATAC/01_create_signac_object.qmd | templates/scatac/create_signac_object/ | TEMPLATE |
| notebook_templates/scATAC/02_quality_control_integration.qmd | templates/scatac/quality_control/ | TEMPLATE after rename |
| notebook_templates/scATAC/03_motif_enrichment.qmd | templates/scatac/motif_enrichment/ | TEMPLATE after method cleanup |
| notebook_templates/multiome/01_create_multiome_object.qmd | templates/multiome/create_object/ | TEMPLATE |
| notebook_templates/multiome/02_qc_integration_wnn.qmd | templates/multiome/wnn/ | TEMPLATE after rename |
| notebook_templates/multiome/03_rna_atac_linkage.qmd | templates/multiome/rna_atac_linkage/ | TEMPLATE |
| notebook_templates/multiome/04_regulatory_programs.qmd | templates/multiome/regulatory_program_scoring/ | TEMPLATE after rename |
| notebook_templates/general_statistics/01_group_summary_and_association_tests.qmd | templates/statistics/group_association_tests/ | TEMPLATE after statistical review |
| code_MAP/simple_QC_MGI_organoids.qmd | examples/bulk_rna/ and source for templates/bulk_rna/qc_normalization/ | EXAMPLE |
| code_MAP/GSEA_of_DEGs.qmd | examples/bulk_rna/ and possible templates/bulk_rna/gsea/ | EXAMPLE |
| code_MAP/HALLMARK_50.qmd | examples/bulk_rna/pathway_scoring/ | EXAMPLE |
| code_MAP/00_CPTAC_LUAD_scoring | examples/bulk_rna/ | EXAMPLE |
| code_MAP/00_MAP_qc_integration.qmd | examples/single_cell/ | EXAMPLE |
| code_MAP/00_MAP_RNA_qc_integration.qmd | examples/single_cell/ | EXAMPLE |
| code_MAP/00_MAP_ATAC_qc_integration.qmd | examples/scatac/ | EXAMPLE |
| code_MAP/001_RNA_ATAC_LT.qmd | examples/multiome/ or examples/single_cell/annotation_label_transfer/ | EXAMPLE |
| code_MAP/002_ATAC_MOTIF.qmd | examples/scatac/motif_enrichment/ | EXAMPLE |
| code_MAP/GSE171145.qmd | examples/single_cell/ | EXAMPLE |
| code_MAP/01_MAP_metadata_bridge.qmd | examples/multiome/ or archive/legacy_map/ | EXAMPLE/ARCHIVE |
| code_MAP/01_MAP_c1_scoring.qmd | examples/single_cell/c1_scoring/ | EXAMPLE |
| code_MAP/02_MAP_c1_scoring.qmd | archive/legacy_map/c1_scoring/ or examples/single_cell/c1_scoring/ | REVIEW |
| code_MAP/03_MAP_state_markers_statistics_export.qmd | examples/single_cell/ | EXAMPLE |
| code_MAP/04_MAP_c1_gene_programs_tradeSeq.qmd | examples/single_cell/trajectory_tradeseq/ | EXAMPLE and future source |
| code_MAP/04_MAP_decoupler_bridge.qmd | examples/multiomics/ or examples/single_cell/regulatory/ | EXAMPLE and future source |
| code_MAP/05_MAP_regulatory_programs.qmd | examples/multiomics/regulatory_programs/ | EXAMPLE |
| code_MAP/06_MAP_coexpression_modules.qmd | examples/single_cell/coexpression_hdWGCNA/ | EXAMPLE and future source |
| code_MAP/07_MAP_velocity_scvelo_cellrank.qmd | examples/single_cell/velocity/ | EXAMPLE and future source |
| code_MAP/08_MAP_metabolic_activity_scCellFie.qmd | examples/single_cell/metabolic_activity/ | EXAMPLE and future source |
| code_MAP/09_MAP_C1_Core_refined_signature.qmd | examples/single_cell/c1_scoring/ | EXAMPLE |
| code_MAP/10_MAP_extensive_statistics.qmd | archive/legacy_map/ | ARCHIVE |
| code_MOFA/00_TCGA_LUAD_multiomics_download.qmd | examples/multiomics/ | EXAMPLE |
| code_MOFA/01_TCGA_LUAD_scoring_tf.qmd | examples/multiomics/ | EXAMPLE |
| code_MOFA/03_MOFA.qmd | examples/multiomics/ | EXAMPLE |
| MOFA_TEMPLATE_CLEAN/00_project_setup.qmd | archive/legacy_mofa/ or future documentation | ARCHIVE |
| MOFA_TEMPLATE_CLEAN/01_multiomics_input_prep.qmd | source for templates/multiomics/match_samples/ after generalization | REVIEW |
| MOFA_TEMPLATE_CLEAN/02_signature_scoring.qmd | example or separate scoring template after exposing normalization | REVIEW |
| MOFA_TEMPLATE_CLEAN/03_mofa_model.qmd | split source for templates/multiomics/mofa_fit/ and mofa_interpretation/ | REVIEW |
| MOFA_TEMPLATE_CLEAN/helpers/helpers_from_MOFA.R | trim into helpers/R only after removing scientific/global functions; otherwise archive | REVIEW |
| MOFA_TEMPLATE_CLEAN/README.md and archive_notes/MOFA_code_inventory.md | archive/legacy_mofa/ | ARCHIVE |
| TRENTO_models_miRNA_vs_PD_L1.qmd | examples/machine_learning/ | EXAMPLE |
| TRENTO_gtExtras_tables.qmd | examples/machine_learning/reporting/ | EXAMPLE |
| alevin_fry/scripts/run_simpleaf_velocity.sh | examples/single_cell/velocity/ or archive/raw_archives/ | REVIEW |
| alevin_fry/*.log | archive/raw_archives/ or delete after provenance review | ARCHIVE/DELETE_CANDIDATE |
| code_MAP/Archive.zip | archive/raw_archives/ | ARCHIVE |
| Task for 2nd interview.zip | archive/raw_archives/ or unpacked examples/proteomics_network/ after review | ARCHIVE/REVIEW |
| .DS_Store files | remove after confirming they are only Finder metadata | DELETE_CANDIDATE |

## 16. Recommended migration order

1. Freeze the audit snapshot. Record the current Git status, file hashes if provenance matters, and the current archive contents.
2. Decide the supported library contract: R/Python versions, Quarto expectation, object formats, TSV/CSV policy, identifier rules, and whether each template is a standalone notebook.
3. Validate the current 18 templates statically and with minimal test renders where dependencies permit. Fix naming and output-contract defects before moving files.
4. Correct only the high-confidence template defects: save the filtered scRNA object, remove misleading integration labels, make genome/ID/assay requirements explicit, and separate score importers from score calculators.
5. Promote the smallest high-confidence set first: bulk QC/normalization, scRNA core stages, Signac core stages, multiome object/WNN/linkage, and group statistics.
6. Extract only mechanical helpers that are repeated and have explicit arguments. Keep normalization, testing, integration, scoring, dynamics, and MOFA fitting in notebooks.
7. Convert project notebooks to examples without rewriting their scientific results. Preserve alternate Harmony/RPCA/SCTransform, scoring, trajectory, velocity, coexpression, and metabolic approaches.
8. Generalize one complex family at a time: true tradeSeq, annotation/label transfer, hdWGCNA, scVelo/CellRank, scCellFie, decoupler, and MOFA.
9. Move historical and superseded material to clearly labeled archives only after downstream references and provenance are checked.
10. Compare the new tree against this mapping, run targeted renders/tests, inspect output objects and tables, then consider conservative cleanup of duplicate guides, Finder metadata, and exact archive copies.

## 17. Risks and items requiring manual review

- Changing count filtering or normalization changes the biological input and invalidates downstream comparisons.
- Moving notebooks without their input/output directories may make paths look portable while silently breaking the workflow.
- The same biological label, especially C1, is used across scoring, trajectory, regulatory, and MOFA notebooks but does not make those notebooks generic.
- Harmony, RPCA, SCTransform, log normalization, and WNN should not be selected by repository frequency alone.
- Project-specific reference objects for Azimuth, SingleR, CopyKAT, JASPAR, decoupler, and scCellFie may be unavailable or version-sensitive.
- The template placeholders are not sufficient input contracts. Matrix orientation, cell IDs, genome assembly, fragments, assay names, feature identifiers, and missing-value policy need explicit documentation.
- The interview zip contains large data and results that may have licensing, privacy, or redistribution constraints.
- Archive.zip may be the only record of intermediate code versions. Preserve it until the historical relationship is documented.
- The GitNexus index is incomplete relative to the filesystem and has zero process flows, so it cannot establish full execution reachability or safe deletion.
- No notebook was rendered or executed in this audit. Syntax, package API compatibility, memory requirements, and actual saved-object contents remain unverified.
- If source objects are not available, a later template can become a plausible-looking but scientifically untested rewrite. Preserve the original example beside any generalized version.
- The final tree could become over-segmented if every method gets a directory. Keep one template per meaningful stage and combine only operations with the same required scientific choices.
- Reusing a helper for generic save/load can accidentally conceal assay selection, filtering, or normalization. Keep those choices in the visible notebook.

## 18. Questions where the available code does not justify choosing one method

1. Should bulk RNA-seq normalization use the active >5 CPM filter in simple_QC_MGI_organoids.qmd, the other >1 CPM path, or a user-configured rule? The repository does not establish a universal threshold.
2. Is TMMwsp the intended canonical bulk method, or should the library retain separate edgeR/limma-voom and DESeq2 guidance? The former reference describes distinctions but no complete DE template chooses one.
3. Should the single-cell baseline use Seurat log normalization or SCTransform? Both are used for different project reasons.
4. Should batch integration have separate Harmony and RPCA templates, or only one supported method with the other retained as an example?
5. Is annotation expected to be reference-based with Azimuth/SingleR, anchor-based label transfer, or intentionally outside the first library release?
6. Should signature scoring promote AddModuleScore, UCell, singscore, GSVA, or decoupler first? The available code demonstrates all as scientifically distinct approaches.
7. Is a “pathway activity” template expected to compute scores, import scores, or do both in sequentially named stages?
8. Is the intended trajectory library Slingshot plus tradeSeq, another trajectory method, or only a pseudotime summary stage?
9. Is CellRank required as a complete fate-inference workflow, or is a scVelo diagnostic sufficient for the initial library?
10. Is coexpression important enough to support the heavier hdWGCNA dependency set, or should the project notebook remain only an example?
11. Should scCellFie become a supported Python template, or is metabolic score import sufficient for practical reuse?
12. What is the intended generic MOFA input contract: arbitrary named views, a fixed assay set, or a minimum of two matched numeric matrices?
13. Which MOFA interpretation outputs are core: factor values/weights only, or group associations and heatmaps as well?
14. Should a machine-learning template support only the TRENTO bias-reduced logistic workflow, or multiple model families and resampling schemes?
15. Is the interview proteomics/PPI analysis part of the personal reusable library, or should it remain a provenance archive outside the curated collection?
16. Should spatial analysis and visualization have reserved directories now, or should empty categories be avoided until real source implementations exist?
17. Which object persistence format should be recommended for R templates: qs2, qs, or saveRDS? The current repository demonstrates all three without a documented policy.
18. What minimum package/version and session-provenance record is required before a notebook can be called canonical?

These questions should be answered from intended reuse and validated scientific practice, not from filename order or the apparent cleanliness of an existing directory.
