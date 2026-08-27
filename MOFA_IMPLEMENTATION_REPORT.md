# MOFA implementation report

## Scope

This report documents the canonical MOFA2 family under
`templates/multiomics/mofa/`. It is a focused analytical cookbook, not a
replacement for MOFA2 documentation. The family separates view preparation,
model fitting, model diagnostics and factor interpretation.

All four canonical notebooks are currently `draft` and are explicitly
classified as `SOURCE-BACKED WORKFLOW`. They have not been promoted to
`validated` from parsing, package inspection or synthetic execution alone.

## Canonical MOFA workflow contract

```text
modality-appropriate feature x sample matrices
          |
          v
prepare_views.qmd
          |
          +-- matched/prepared named view list (.qs2)
          +-- sample and feature manifests (TSV)
          v
fit.qmd
          |
          +-- trained MOFA2 model (.hdf5)
          +-- model/training options (TSV)
          v
diagnostics.qmd
          |
          +-- variance, factor and technical diagnostics (TSV + figures)
          v
interpretation.qmd
          |
          +-- factor scores, feature weights and optional associations (TSV)
```

The input matrices have features in rows and samples in columns. They must be
numeric, named, non-empty and already prepared at a modality-appropriate scale.
The canonical baseline retains samples present in every selected view and keeps
one common sample order. It accounts for dropped samples in TSV manifests and
does not automatically impute missing values or replace `NA` with zero.

MOFA fitting is unsupervised. Outcomes, clinical groups and signature scores
are not inputs to `fit.qmd`; they can be joined after fitting for explicitly
post hoc interpretation or technical diagnostics.

## Native persistence exception

The repository-wide policy is R analytical objects in `qs2` and human-readable
tables in TSV. MOFA2 has a native trained-model artifact, so this family uses:

```text
prepared views/supporting R objects -> .qs2
trained MOFA2 model                  -> native .hdf5
manifests/options/scores/weights     -> .tsv
```

The `.hdf5` file written by `MOFA2::run_mofa(..., outfile = ...)` is the
canonical trained model. The downstream notebooks use `MOFA2::load_model()`;
the trained model is not redundantly serialized as `.qs2`.

## Source provenance

Primary source notebooks inspected:

- `CODE_MAP/code_MOFA/MOFA_TEMPLATE_CLEAN/01_multiomics_input_prep.qmd`
- `CODE_MAP/code_MOFA/MOFA_TEMPLATE_CLEAN/03_mofa_model.qmd`
- `CODE_MAP/code_MOFA/03_MOFA.qmd`

Additional provenance inspected:

- `CODE_MAP/code_MOFA/MOFA_TEMPLATE_CLEAN/00_project_setup.qmd`
- `CODE_MAP/code_MOFA/MOFA_TEMPLATE_CLEAN/02_signature_scoring.qmd`
- `CODE_MAP/code_MOFA/00_TCGA_LUAD_multiomics_download.qmd`
- `CODE_MAP/code_MOFA/01_TCGA_LUAD_scoring_tf.qmd`
- `CODE_MAP/code_MOFA/MOFA_TEMPLATE_CLEAN/helpers/helpers_from_MOFA.R`
- `CODE_MAP/code_MOFA/MOFA_TEMPLATE_CLEAN/README.md`

Current API checks used the installed MOFA2 1.22.0 package and the official
MOFA2 documentation for the current `prepare_mofa()`, `run_mofa()`,
`load_model()`, variance and extraction accessors. The verified current calls
include `run_mofa(..., outfile = ..., save_data = ..., use_basilisk = ...)`,
`get_variance_explained(..., as.data.frame = TRUE)`,
`get_factors(..., as.data.frame = TRUE)` and
`get_weights(..., as.data.frame = TRUE)`.

## Per-template implementation records

### `templates/multiomics/mofa/prepare_views.qmd`

- **Template class:** `SOURCE-BACKED WORKFLOW`
- **Status:** `draft`
- **Canonical source:** `MOFA_TEMPLATE_CLEAN/01_multiomics_input_prep.qmd`
- **Merge sources:** view construction and filtering in `03_MOFA.qmd` and
  `MOFA_TEMPLATE_CLEAN/03_mofa_model.qmd`; matrix-validation safeguards from
  the original workflow.
- **SOURCE-DERIVED:** named view-list preparation; feature-by-sample matrix
  contract; strict intersection of samples across views; removal of
  non-variable features; qs2 persistence; sample-order checks.
- **MERGED:** source matching/manifests combined with explicit per-view
  feature-selection parameters, all-missing/duplicate checks and missing-value
  accounting.
- **API-DERIVED:** none for the main analytical transformation. The current
  `qs2::qs_read()`/`qs2::qs_save()` calls are package-verified persistence calls.
- **PROJECT-SPECIFIC AND OMITTED:** fixed five-view input files, project paths,
  sample-barcode truncation, duplicate sample collapsing, download logic,
  clinical data, fixed mutation rules and downstream signature scoring.
- **Scientific decisions retained:** strict complete-sample intersection as the
  baseline; feature filtering by within-view variance; optional per-view top-N
  selection; matrix orientation; duplicate-feature policy; internal `NA`
  preservation.
- **Practical notes retained:** modality-specific transformations must be
  visible; count-derived RNA/miRNA may use an explicit logCPM preparation, but
  non-count views must not inherit it; missing whole views and internal missing
  entries are distinct; no automatic imputation.
- **Genome/build contract:** not applicable.
- **Fragment contract:** not applicable.
- **Input contract:** a named `.qs2` list of numeric, non-empty matrices with
  unique feature and sample names. Sample IDs are supplied by the user and are
  not silently truncated or renamed.
- **Output contract:** a named list of numeric feature×sample matrices with one
  common sample order; view, sample-overlap and feature manifests.
- **Persistence:** prepared list `.qs2`; manifests `.tsv`.
- **API changes:** current source used helper-based table loading and barcode
  normalization; the canonical version deliberately consumes a generic named
  list and performs visible checks inline. No unsupported MOFA API was added.
- **Validation performed:** R/static checks and object-contract review are
  recorded after implementation; source files were inspected and left intact.
- **Validation still required:** representative matrices from at least two
  modalities; modality-specific transformations; deliberate internal missing
  values; sample-drop accounting; qs2 round trip.
- **Unresolved decisions:** whether a future workflow should support incomplete
  views directly; per-view likelihood and transformation choices; the feature
  count appropriate for each modality.

### `templates/multiomics/mofa/fit.qmd`

- **Template class:** `SOURCE-BACKED WORKFLOW`
- **Status:** `draft`
- **Canonical sources:** `MOFA_TEMPLATE_CLEAN/03_mofa_model.qmd` and
  `03_MOFA.qmd`.
- **Merge sources:** prepared-view contract from
  `MOFA_TEMPLATE_CLEAN/01_multiomics_input_prep.qmd`.
- **SOURCE-DERIVED:** `create_mofa()`; default data/model/training options;
  explicit factor count; view scaling choice; ARD/sparsity settings; seed,
  convergence mode, iteration limit, factor-dropping threshold and
  `run_mofa()` training flow.
- **MERGED:** the source placed the output path in training options and called
  `run_mofa()` without an explicit output argument. The canonical notebook uses
  the current verified `run_mofa(outfile = ...)` contract while preserving the
  source training choices. It also requires a named likelihood for every view
  instead of allowing an accidental default for a binary view.
- **API-DERIVED:** current option/accessor argument verification for
  `prepare_mofa()` and `run_mofa()`; no new model method was invented.
- **PROJECT-SPECIFIC AND OMITTED:** fixed modality names, fixed clinical/C1
  score inputs, project groups, project output paths and interpretation plots.
- **Scientific decisions retained:** number of factors is explicit; likelihoods
  are view-specific and explicit; view scaling, float precision, ARD/sparsity,
  seed, convergence and factor dropping remain visible; phenotype is excluded
  from fitting.
- **Practical notes retained:** MOFA2 invokes the Python `mofapy2` backend;
  `use_basilisk` is visible and no local executable path is hard-coded; default
  MOFA2 likelihoods are printed only as a reminder before the required explicit
  declaration.
- **Genome/build contract:** not applicable.
- **Fragment contract:** not applicable.
- **Input contract:** prepared `.qs2` named views, common sample order, valid
  feature names, understood missingness and at least two views.
- **Output contract:** trained MOFA2 object written as native HDF5 plus concise
  model/training option TSVs.
- **Persistence:** prepared views `.qs2`; trained model `.hdf5`; option tables
  `.tsv`.
- **API changes:** current MOFA2 1.22.0 confirms `prepare_mofa(object =,
  data_options =, model_options =, training_options =)` and
  `run_mofa(object =, outfile =, save_data =, use_basilisk =)`. The explicit
  outfile call is a current-API merge with the source workflow.
- **Validation performed:** installed package/version and formal argument
  checks; R/static checks; synthetic fit checks only if reported below.
- **Validation still required:** a representative multi-view fit with an
  appropriate Python backend; likelihood review for binary/count views; model
  convergence and option reproducibility.
- **Unresolved decisions:** factor count; view scaling; Gaussian versus other
  likelihoods for each supplied view; use of basilisk versus a configured
  reticulate environment; whether to enable ARD factor pruning.

### `templates/multiomics/mofa/diagnostics.qmd`

- **Template class:** `SOURCE-BACKED WORKFLOW`
- **Status:** `draft`
- **Canonical sources:** `MOFA_TEMPLATE_CLEAN/03_mofa_model.qmd` and
  diagnostic sections of `03_MOFA.qmd`.
- **Merge sources:** source factor extraction and Spearman factor-correlation
  plot; current MOFA2 variance accessor contract.
- **SOURCE-DERIVED:** loading the native model; variance-explained review;
  factor-score distributions; factor correlations; high-weight sanity checks;
  technical-variable association as a pre-interpretation diagnostic.
- **MERGED:** source diagnostics were separated from biological interpretation,
  exported as TSV, and generalized to optional numeric technical metadata.
- **API-DERIVED:** use of current `get_variance_explained(...,
  as.data.frame = TRUE)` and current tidy factor/weight accessors where the
  source used matrix accessors or cached objects.
- **PROJECT-SPECIFIC AND OMITTED:** fixed clinical score correlations, group
  labels, leading-factor assumptions, fixed sample identifiers and project
  plots.
- **Scientific decisions retained:** variance is examined per view and factor;
  factors are checked for redundancy and technical association; high variance
  is not treated as biological importance; weight signs are retained.
- **Practical notes retained:** technical association is an investigation flag,
  not a relabeling rule; factor numbers, signs and order are model-specific;
  multiple technical factor-variable tests receive BH correction.
- **Genome/build contract:** not applicable.
- **Fragment contract:** not applicable.
- **Input contract:** native MOFA2 `.hdf5`; optional metadata TSV with unique
  sample IDs and explicitly named numeric technical columns.
- **Output contract:** variance-explained TSVs, factor-score and correlation
  TSVs, a compact top-weight TSV, optional technical-association TSV and
  diagnostic figures.
- **Persistence:** input model `.hdf5`; outputs `.tsv` and rendered figures.
- **API changes:** current `load_model()`, `get_variance_explained()` and
  `plot_variance_explained()` contracts were verified; the source's
  `calculate_variance_explained()` behavior is not forced on non-Gaussian views
  when cached variance is available.
- **Validation performed:** API formal-argument checks, R/static checks and
  no-refit object-flow review.
- **Validation still required:** representative native HDF5 model; variance
  accessors for mixed likelihoods; technical-metadata alignment; useful figure
  rendering.
- **Unresolved decisions:** how many weights to display; whether to add
  categorical technical diagnostics; how to compare factors across fits.

### `templates/multiomics/mofa/interpretation.qmd`

- **Template class:** `SOURCE-BACKED WORKFLOW`
- **Status:** `draft`
- **Canonical sources:** `MOFA_TEMPLATE_CLEAN/03_mofa_model.qmd` and
  interpretation sections of `03_MOFA.qmd`.
- **Merge sources:** source factor/weight extraction and group summaries; the
  current tidy accessor API.
- **SOURCE-DERIVED:** native model loading; factor-score and feature-weight
  extraction; absolute-weight ranking with signed values; factor heatmap;
  continuous association and group-summary concepts.
- **MERGED:** source-specific score/group logic was generalized to optional
  continuous metadata and optional multi-group categorical summaries with
  explicit factor selection and BH correction.
- **API-DERIVED:** current `get_factors(..., as.data.frame = TRUE)` and
  `get_weights(..., as.data.frame = TRUE, scale = FALSE)` output contracts were
  used for the tidy tables.
- **PROJECT-SPECIFIC AND OMITTED:** fixed score/class columns, fixed high/low
  groups, outcome-selected lead factors, mutation-specific plots, cohort
  interpretation and duplicated signature-scoring/enrichment workflows.
- **Scientific decisions retained:** factors are selected explicitly after
  diagnostics; positive and negative weights are retained; top features are
  ranked by absolute weight; continuous associations use Spearman correlation;
  categorical summaries do not assume two groups; one sample is one replicate.
- **Practical notes retained:** phenotype-based factor selection is post hoc;
  factors are not stable biological identities across fits; weights and
  associations are not causal evidence; factor sign/order is not treated as
  transferable.
- **Genome/build contract:** not applicable.
- **Fragment contract:** not applicable.
- **Input contract:** native MOFA2 `.hdf5`; optional metadata TSV with unique
  sample IDs; explicit factor, view and metadata-column selections.
- **Output contract:** tidy `sample_id/factor/value` scores; tidy
  `view/feature/factor/weight/abs_weight` weights; top-weight TSV; optional
  continuous/categorical association and group-summary TSVs; factor heatmap.
- **Persistence:** input model `.hdf5`; all tabular outputs `.tsv`.
- **API changes:** current accessors replace the source's direct matrix-only
  extraction where useful; no refit or alternative model format was added.
- **Validation performed:** current accessor signatures, R/static checks and
  explicit no-refit review.
- **Validation still required:** representative model extraction; metadata
  joins; multiple-testing behavior; readable heatmap/top-weight output.
- **Unresolved decisions:** which factors to interpret; metadata variables;
  ordering/annotation of heatmaps; categorical test choice for a future study.

## Project-specific cleanup

The source notebooks contain a fixed set of cancer-study views, sample-barcode
truncation/collapse, a binary mutation transformation, a fixed top-feature
count, fixed outcome/group labels and score-driven interpretation. Those are
retained only as provenance in the original source files and are not used as
canonical defaults. The canonical notebooks do not contain project paths,
fixed study identifiers, fixed biological groups, or score construction.

The project setup and signature-scoring source pages were not promoted to
canonical MOFA templates. Signature methods remain in their dedicated
single-cell/bulk/scoring families.

## API and package record

- MOFA2: installed 1.22.0; current calls verified against the official MOFA2
  documentation.
- qs2: installed 0.3.1; used for prepared/supporting R objects.
- reticulate: installed 1.46.0; no local Python path is hard-coded.
- basilisk: installed 1.24.0; `use_basilisk` remains an explicit fitting choice.
- Officially checked functions: `create_mofa`,
  `get_default_data_options`, `get_default_model_options`,
  `get_default_training_options`, `prepare_mofa`, `run_mofa`, `load_model`,
  `get_variance_explained`, `calculate_variance_explained`,
  `plot_variance_explained`, `get_factors` and `get_weights`.

No MEFISTO, MOFAcell, Python mofax or MuData template was added.

## Validation performed

The canonical branch was created from the pushed `canonical/multiome` head and
the original MOFA source files were inspected without modification. Static
validation includes balanced Quarto fences, extracted R parsing, path/project
identifier scans, persistence scans, API-name scans and contract review. The
`prepare_views.qmd` was executed against temporary two-view synthetic matrices;
sample matching, manifests, feature filtering and the qs2 round trip passed.
The fitting configuration through `prepare_mofa()` also passed with explicit
named Gaussian likelihoods. A temporary two-view synthetic model then passed
the complete `create_mofa()` -> `prepare_mofa()` -> `run_mofa()` -> native HDF5
save/load -> factor/weight/variance extraction path using the supported basilisk
backend. This is a code-path smoke test only: the synthetic model is not a
scientific validation dataset and the four notebooks remain `draft`.

## Validation still required

- Execute `prepare_views.qmd` on representative compatible views from at least
  two modalities.
- Run a native MOFA2 fit through a compatible `mofapy2` backend and confirm the
  HDF5 round trip.
- Confirm mixed-likelihood behavior, especially binary and count-derived views.
- Verify variance, factor and weight extraction on the saved model.
- Review technical metadata joins, post hoc multiple-testing output and
  interpretation figures.
- Confirm that the chosen transformations, feature filters and factor count
  are scientifically appropriate for each new study.

## Unresolved scientific decisions

The family intentionally leaves these decisions visible for each analysis:

- modality-specific transformation and likelihood;
- complete-sample matching versus an explicitly designed incomplete-view fit;
- internal missing-value handling;
- per-view feature filtering and view scaling;
- number of factors and factor-pruning settings;
- MOFA2 Python backend/environment;
- factors and metadata variables selected for post hoc interpretation.

## Filename and source record

No canonical filename was renamed in this mission. The new files are:

- `templates/multiomics/mofa/README.md`
- `templates/multiomics/mofa/prepare_views.qmd`
- `templates/multiomics/mofa/fit.qmd`
- `templates/multiomics/mofa/diagnostics.qmd`
- `templates/multiomics/mofa/interpretation.qmd`
- `MOFA_IMPLEMENTATION_REPORT.md`

The original MOFA notebooks and helper files remain unchanged.
