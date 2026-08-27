# Biomarker ML implementation report

## Scope

This report documents the canonical biomarker machine-learning templates in
`templates/machine_learning/`. They preserve a real sample-level binary
classification workflow from the source notebooks while removing cohort names,
fixed paths, identifiers, biological labels, and study-specific conclusions.

The templates are a personal analytical cookbook, not a replacement for
tidymodels, brglm2, important, filtro, yardstick, or other package
documentation.

Both canonical templates are currently `draft`. They have been parsed and
smoke-tested with small synthetic inputs, but they have not been executed on a
representative real dataset in their canonical form.

## Canonical templates

| Template | Class | Status | Purpose |
|---|---|---|---|
| `biomarker_binary_classification_brglm2.qmd` | SOURCE-BACKED WORKFLOW | draft | Fit, tune, evaluate, and persist the primary classifier plus an optional reduced stable-feature model. |
| `biomarker_model_reporting.qmd` | SOURCE-BACKED WORKFLOW | draft | Read frozen TSV outputs and create presentation tables and figures without refitting. |

The canonical implementation uses the source-backed bias-reduced logistic
regression route. It does not provide a general decoupler, pathway, or generic
feature-scoring pipeline.

## Canonical biomarker model contract

The expected input is one row per biological sample or other declared
experimental unit, with a binary outcome and a feature matrix whose predictors
are measured for the same samples.

```text
sample-level biomarker data
        ↓
locked train/test split
        ↓
training-only preprocessing
        ↓
supervised feature selection inside resampling
        ↓
stratified Monte Carlo CV
        ↓
bias-reduced logistic regression
        ↓
training-only threshold selection
        ↓
frozen final workflow
        ↓
held-out evaluation
        ↓
feature stability
        ↓
optional reduced stable panel
```

The primary template accepts a wide feature table, a split/outcome table, and
a user-supplied feature/signature table. It validates unique sample IDs,
sample alignment, disjoint train/test membership, both outcome classes in
each split, and the requested feature count.

The source-backed modeling choices retained in the canonical template are:

- class-frequency-derived importance weights, with the weight exponent exposed
  as `class_weight_alpha`;
- a training-only recipe using zero-variance removal, supervised predictor
  desirability selection, and normalization;
- stratified Monte Carlo resampling, with the source-backed default of 200
  resamples and the resampling proportion exposed;
- bias-reduced binomial regression through the current brglm2 engine route;
- probability-threshold tuning against training resamples, with the threshold
  grid and balanced-accuracy selection visible;
- held-out predictions and metrics that include ROC-AUC, PR-AUC, balanced
  accuracy, sensitivity, specificity, precision, negative predictive value,
  and the Youden index where defined;
- per-resample selected-feature records and a stability summary;
- an optional reduced model trained from the stable primary-model features.

The reduced stable-feature model is a secondary sensitivity analysis. It does
not replace the primary model or turn stability into a claim of biological
feature importance.

## Leakage safeguards

The canonical workflow keeps the supplied train/test assignment locked. Test
samples are not used for recipe estimation, supervised feature selection,
threshold selection, or model tuning. Feature selection is part of the
resampled training workflow rather than a one-time operation on all samples.

The optional metadata join in the model summary occurs after fitting and is
for reporting only. It is not a predictor-processing step.

The source workflow operates at the sample level. If patients, donors, or
other experimental units contribute multiple rows, the split and resampling
strategy must be changed to keep those units together. Thousands of feature
rows or technical measurements must not be treated as independent biological
replicates.

## Persistence contract

The canonical persistence policy is:

```text
fitted R workflow/model -> qs2
predictions             -> TSV
metrics                 -> TSV
feature stability       -> TSV
reporting inputs        -> frozen TSV outputs
```

The primary model bundle and optional reduced-panel bundle are written with
`qs2::qs_save()`. Human-readable class-balance, tuning, prediction, metric,
confusion-matrix, ROC/PR-curve, and feature-stability outputs are written as
TSV files.

`biomarker_model_reporting.qmd` consumes frozen TSV outputs. It does not refit
the model, select features, tune thresholds, or re-evaluate performance.
HTML tables, a probability plot, and a selected-feature heatmap are reporting
artifacts; the TSV files remain the numerical handoff.

## Source provenance

Primary source:

- `CODE_MAP/TRENTO_models_miRNA_vs_PD_L1.qmd`

Merge source:

- `CODE_MAP/TRENTO_gtExtras_tables.qmd`

The source notebooks are provenance/examples and remain unchanged. The
canonical templates do not claim that the source labels, cohort, feature names,
or biological interpretation are transferable.

## Per-template implementation records

### `biomarker_binary_classification_brglm2.qmd`

**Template class:** SOURCE-BACKED WORKFLOW
**Status:** draft
**Canonical source:** `CODE_MAP/TRENTO_models_miRNA_vs_PD_L1.qmd`
**Merge sources:** the source notebook's reduced stable-feature section; frozen
table/plot contracts from `CODE_MAP/TRENTO_gtExtras_tables.qmd`.

**SOURCE-DERIVED blocks**

- wide expression-table preparation and sample-level train/test separation;
- training-derived class weighting;
- supervised predictor desirability filtering inside the tidymodels recipe;
- stratified Monte Carlo cross-validation;
- brglm2 bias-reduced logistic regression;
- probability-threshold tuning and held-out predictions;
- ROC/PR, threshold metrics, confusion matrices, and feature stability;
- the optional reduced model based on stable primary-model features.

**API-DERIVED blocks**

- current package-compatible use of typed `hardhat::importance_weights()`;
- current `filtro`/`important` score-object and
  `step_predictor_desirability()` syntax;
- current `qs2::qs_save()` persistence syntax.

These API-derived details were used to keep the source-backed workflow
compatible with the installed/current package interfaces. They are not claims
that the source notebook used the same version of every package.

**MERGED blocks**

- generic file and column contracts replacing project paths and fixed labels;
- explicit validation of sample and feature alignment;
- TSV output contracts for predictions, metrics, curves, confusion matrices,
  tuning, and stability;
- optional dynamic metadata reporting inputs;
- qs2 migration from the source notebook's RDS model persistence;
- expanded compact held-out diagnostics and reduced-panel outputs.

**PROJECT-SPECIFIC AND OMITTED blocks**

- TRENTO, miRNA, PD-L1, and cohort-specific names;
- fixed sample identifiers, project paths, and output directories;
- the fixed feature/signature contents, retained only as a user-supplied input;
- project-specific biological labels, conclusions, and presentation prose;
- study-specific metadata interpretation and any claim of clinical validity.

**Scientific decisions retained:** split definition, outcome direction,
feature-selection size, class-weight exponent, resampling count/proportion,
threshold grid, stability cutoff, reduced-panel size, and whether to run the
reduced model.

**Practical notes retained:** select features inside resampling; preserve the
primary model's component outputs; keep the held-out test set frozen; inspect
class balance and threshold metrics; and treat reduced stable panels as
sensitivity analyses.

**Input contract:** wide feature expression table with feature rows and sample
columns; split/outcome table with unique sample IDs and binary labels; optional
feature/signature table; optional metadata table used only after fitting.

**Output contract:** qs2 model bundles plus TSV class-balance, tuning,
prediction, metric, confusion, curve, feature-stability, and reduced-panel
tables.

**Object persistence:** fitted R workflow/model bundles use qs2; tables use TSV.

**API changes relative to source:** RDS persistence was replaced with qs2;
source-specific column/path names were parameterized; current typed case-weight
and predictor-desirability syntax was used; output extraction was made explicit.

### `biomarker_model_reporting.qmd`

**Template class:** SOURCE-BACKED WORKFLOW
**Status:** draft
**Canonical source:** `CODE_MAP/TRENTO_gtExtras_tables.qmd`
**Merge sources:** frozen prediction and selected-feature outputs from
`biomarker_binary_classification_brglm2.qmd`.

**SOURCE-DERIVED blocks**

- compact `gt`/`gtExtras` audit and presentation tables;
- model probability visualization;
- selected-feature expression heatmap reporting.

**API-DERIVED blocks**

- current package calls for dynamic `gt`/`gtExtras` tables and
  `ComplexHeatmap`/`circlize` visualization;
- generic extraction of model-output columns rather than fixed source names.

**MERGED blocks**

- frozen-output input checks;
- dynamic feature-column and metadata handling;
- explicit distinction between numerical TSV inputs and HTML/PNG presentation
  artifacts;
- visualization-only row-wise feature z-scoring with zero-variance safeguards.

**PROJECT-SPECIFIC AND OMITTED blocks**

- fixed TRENTO/PD-L1 labels and clinical interpretation;
- fixed sample names, state labels, annotations, paths, and feature names;
- project-specific heatmap ordering and biological conclusions;
- any model refit, feature selection, threshold tuning, or performance claim.

**Scientific decisions retained:** which frozen model outputs are displayed,
which metadata columns are available, feature display labels, sample ordering,
and whether selected-feature values are shown as a visualization.

**Practical notes retained:** reporting is downstream of a frozen model;
heatmap scaling is for visualization only; and the complete/essential tables
keep the underlying TSV outputs auditable.

**Input contract:** frozen TSV files produced by the primary model template,
including predictions, observed classes, selected-feature values, and optional
metadata columns.

**Output contract:** compact HTML tables, a model-probability PNG, and a
selected-feature heatmap PNG.

**Object persistence:** no analytical model is persisted or refit; frozen
numerical inputs are TSV.

**API changes relative to source:** fixed project columns were replaced by
validated dynamic columns; source-specific output names and annotations were
removed; the companion consumes canonical frozen outputs only.

## Validation performed

Static checks passed for both canonical QMDs:

- balanced Quarto fences;
- exactly one visible `draft` status per notebook;
- R code blocks extracted and parsed successfully;
- no absolute private paths, credentials, secrets, project identifiers, RDS
  persistence, or deprecated R decoupleR code;
- required model/reporting tokens and output contracts present.

Code-path smoke tests passed with temporary synthetic fixtures outside the
repository:

- primary model route rendered successfully with a reduced resampling count;
- optional reduced-panel route rendered successfully with a reduced
  resampling count and permissive test stability cutoff;
- reporting companion rendered successfully from generic frozen TSV fixtures.

These renders established that the documented code paths and object/output
contracts execute. They did not establish scientific performance, feature
stability, calibration, or biological validity.

## Validation still required

Before either notebook is promoted to `validated`, execute the canonical forms
with representative data and the intended package environment. Confirm:

- expression, split, outcome, signature, and metadata alignment;
- the intended biological unit and grouped split/resampling policy;
- training-only selection, weighting, normalization, and threshold behavior;
- successful qs2 round trips and complete TSV outputs;
- held-out evaluation with an independent validation strategy where possible;
- stability interpretation under the actual sample size and class balance;
- reporting output against the exact frozen files produced by the model route.

## Unresolved decisions

- Whether the supplied split is sufficiently independent for the biological
  question, especially when samples share patients, donors, or batches.
- The final feature/signature definition, feature count, stability cutoff, and
  reduced-panel size for a particular study.
- Whether balanced accuracy is the correct threshold-selection objective for a
  given class-imbalance and decision-cost setting.
- Whether the held-out test set is large enough for stable ROC/PR and threshold
  estimates.
- External validation, calibration, and prospective utility remain untested.
- Package APIs and defaults should be rechecked before real use, particularly
  for supervised recipe steps, brglm2 engines, and reporting packages.
