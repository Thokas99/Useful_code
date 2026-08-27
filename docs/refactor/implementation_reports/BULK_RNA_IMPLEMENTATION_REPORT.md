# Bulk RNA-seq implementation report

## Scope

This report documents the canonical bulk RNA-seq templates in
`templates/bulk_rna/`. The library preserves compact, reusable workflows from
the current source notebooks and separates count modeling, QC, enrichment, and
sample-level scoring.

The templates are a personal analytical cookbook. They are not a replacement
for current edgeR, tximport, clusterProfiler, singscore, GSVA, or Bioconductor
documentation.

All six templates are currently `draft`. Source-backed code has not yet been
executed in its canonical form on representative project data. The DE template
is intentionally an API/tutorial reminder and has no complete source workflow
to validate against.

## Canonical templates

| Template | Class | Status | Canonical source |
|---|---|---|---|
| `tximport_edger.qmd` | SOURCE-BACKED WORKFLOW | draft | `examples/bulk_rna/mgi_organoids/simple_QC_MGI_organoids.qmd` |
| `qc_normalization_edger.qmd` | SOURCE-BACKED WORKFLOW | draft | `examples/bulk_rna/mgi_organoids/simple_QC_MGI_organoids.qmd` |
| `differential_expression_edger.qmd` | API / TUTORIAL REMINDER | draft | No complete reusable source implementation found |
| `gsea.qmd` | SOURCE-BACKED WORKFLOW | draft | `examples/bulk_rna/mgi_organoids/GSEA_of_DEGs.qmd` |
| `singscore.qmd` | SOURCE-BACKED WORKFLOW | draft | `examples/bulk_rna/mgi_organoids/HALLMARK_50.qmd` |
| `gsva.qmd` | SOURCE-BACKED WORKFLOW | draft | `examples/multiomics/cptac_luad/00_CPTAC_LUAD_scoring` |

## Canonical bulk RNA contracts

### Count-model route

```text
tximport object
      ↓
tximport_edger.qmd
      ↓
DGEList
      ↓
qc_normalization_edger.qmd
      ↓
filtered + normalized DGEList
      ↓
differential_expression_edger.qmd
      ↓
gene-level statistical results
      ↓
gsea.qmd
```

`tximport_edger.qmd` expects a gene-level tximport object and aligned sample
metadata. It produces an edgeR `DGEList` with raw count-scale values. The QC
template filters that object, calculates library-composition normalization
factors, and produces logCPM for diagnostics while retaining filtered raw
counts. The DE reminder then uses the DGEList with an explicit design and
contrast.

### Sample-scoring route

```text
normalized expression matrix
      ├── singscore.qmd
      └── gsva.qmd
```

Singscore and GSVA consume declared normalized expression matrices. They are
optional sample-level scoring branches and do not require differential
expression results.

### Persistence

```text
R analytical objects -> qs2
tables               -> TSV
```

The useful count-model handoffs are persisted as qs2. Human-readable count,
QC, ranking, enrichment, score, and coverage outputs are TSV. Trivial
intermediate matrices are not serialized automatically.

## Source inspection summary

The current source material supports the following decisions:

- `simple_QC_MGI_organoids.qmd` contains a tximport branch using
  `DGEListFromTximport()`, explicit gene annotation alignment, a >1 CPM in at
  least five samples filter, `TMMwsp`, and logCPM with `prior.count = 1`;
- the same source contains a raw count route that collapses duplicate gene
  symbols, removes all-zero rows, computes library/detection metrics, checks
  distributions and sample correlation, runs PCA, and reviews clustering and
  outlier evidence;
- the source contains both >1 CPM and >5 CPM filtering paths, so the canonical
  QC template exposes the threshold rather than claiming one project rule is
  universal;
- `rnaseq_normalization_cheatsheet.md` distinguishes raw counts, CPM, TMM/TMMwsp,
  and logCPM, and explicitly warns that TMMwsp is composition normalization,
  not batch correction;
- `GSEA_of_DEGs.qmd` prepares a signed `sign(logFC) * sqrt(F)` ranking, maps
  SYMBOL/ENSEMBL identifiers to Entrez IDs, resolves duplicate mapped IDs, and
  runs GO BP and KEGG GSEA with clusterProfiler;
- `HALLMARK_50.qmd` checks gene-set coverage and scores per-sample signatures
  with `rankGenes()` and `simpleScore()`; a misleading source heading says
  “ssGSEA” while the active code uses singscore, so the canonical name follows
  the code;
- `00_CPTAC_LUAD_scoring` uses `GSVA::gsvaParam()` with `kcdf = "Gaussian"`
  on a transformed expression matrix, then extracts sample-level scores.

## Per-template implementation records

### `tximport_edger.qmd`

**Template class:** SOURCE-BACKED WORKFLOW
**Status:** draft
**Canonical source:** `examples/bulk_rna/mgi_organoids/simple_QC_MGI_organoids.qmd`
**Merge sources:** `cheatsheets/rnaseq_normalization_cheatsheet.md` and current
tximport/edgeR object documentation.

**SOURCE-DERIVED blocks**

- load a tximport result and inspect its gene-level count matrix;
- use `edgeR::DGEListFromTximport()`;
- align metadata to count-matrix sample columns;
- retain explicit gene identifiers and library-size inspection.

**API-DERIVED blocks**

- current qs2 input/output syntax;
- current `DGEListFromTximport()` argument names;
- conservative version-suffix cleanup and current matrix checks.

**MERGED blocks**

- optional annotation attachment;
- explicit duplicate-ID stop after cleanup instead of silent collapse;
- non-conflicting metadata attached to `DGEList$samples`;
- output of a small library-size TSV.

**PROJECT-SPECIFIC AND OMITTED blocks**

- Salmon paths, raw-count filenames, Excel metadata, UDB parsing, lane labels,
  MGI identifiers, and project output directories;
- support for every quantifier and every input file layout;
- downstream filtering, normalization, QC plots, and differential testing.

**Scientific decisions retained:** feature-ID cleanup, duplicate-ID behavior,
metadata/sample alignment, optional annotation, and whether all-zero genes are
removed at import or deferred to QC.

**Practical notes retained:** feature-by-sample orientation, exact sample-name
matching, explicit dimensions, and stopping when identifier cleanup creates
duplicates.

**Input contract:** one qs2-persisted gene-level tximport object with `counts`
and sample columns; metadata TSV with unique `sample_id`; optional annotation
TSV with unique `gene_id`.

**Output contract:** edgeR `DGEList` with raw count-scale data, aligned sample
metadata, optional gene annotation, and a library-size TSV.

**Persistence:** input and output analytical objects use qs2; summary tables
use TSV.

**API changes:** source RDS input is represented as qs2 in the canonical
workflow; the source's extra raw-count input path is not combined with the
tximport path.

**Validation performed:** source inspection, static contract review, and a
temporary synthetic tximport-like render that passed object construction,
sample alignment, and output creation.

**Validation still required:** representative tximport object execution,
metadata alignment, annotation attachment, and qs2 round trip.

**Unresolved decisions:** whether a particular tximport object has appropriate
gene-level identifiers and whether duplicate IDs should be resolved upstream
or by a declared aggregation policy.

### `qc_normalization_edger.qmd`

**Template class:** SOURCE-BACKED WORKFLOW
**Status:** draft
**Canonical source:** `examples/bulk_rna/mgi_organoids/simple_QC_MGI_organoids.qmd`
**Merge sources:** `cheatsheets/rnaseq_normalization_cheatsheet.md` and source
QC/object-flow notes in the project-example README under
`examples/single_cell/map/README.md`.

**SOURCE-DERIVED blocks**

- library-size and detected-gene summaries;
- CPM and logCPM representations;
- sample-level logCPM distributions;
- Spearman sample correlation;
- PCA and sample clustering diagnostics;
- before/after feature accounting;
- TMMwsp library-composition normalization and `prior.count = 1` logCPM.

**API-DERIVED blocks**

- direct current `stats::prcomp()` implementation for a compact PCA diagnostic;
- current qs2 persistence syntax and explicit TSV extraction;
- optional generic PCA color-column handling.

**MERGED blocks**

- a visible >1 CPM in at least five samples baseline;
- source-backed explanation of the competing >5 CPM branch without silently
  canonizing it;
- multi-diagnostic outlier review without automatic sample deletion;
- normalized DGEList and transformed-expression table handoffs.

**PROJECT-SPECIFIC AND OMITTED blocks**

- MGI, organoid, TME, IEO grade, lane, mapping-rate, and fixed sample labels;
- Excel metadata cleanup and project-specific consensus outlier labels;
- fixed MAD constants and project-specific biological interpretation;
- large plot panels and PAM/ARI agreement analyses.

**Scientific decisions retained:** CPM threshold, minimum number of samples,
normalization method, logCPM prior, PCA scaling, and optional metadata overlay.

**Practical notes retained:** inspect library size, detection, distributions,
correlation, PCA, and clustering together; an outlier flag is a reason to
investigate; TMMwsp is not batch correction; and logCPM does not replace raw
counts for edgeR likelihood modeling.

**Input contract:** qs2-persisted edgeR `DGEList` with raw counts and sample
IDs in column names, normally from `tximport_edger.qmd`.

**Output contract:** filtered/normalized DGEList, gene filter accounting,
sample QC summary, outlier-review table, correlation/PCA tables, filtered CPM,
and filtered logCPM TSVs.

**Persistence:** normalized DGEList uses qs2; QC matrices and summaries use
TSV.

**API changes:** source FactoMineR PCA and project plotting were reduced to
current base-R PCA/clustering diagnostics; the source's MAD framework remains
documented as an omitted project-specific policy rather than a hidden default.

**Validation performed:** source inspection, static contract review, and a
temporary synthetic render that passed filtering, TMMwsp normalization, QC
tables, PCA/correlation diagnostics, and qs2 output creation.

**Validation still required:** run with representative counts, confirm the
chosen filter for the study design, inspect all diagnostics, and verify a qs2
round trip before using the object for DE.

**Unresolved decisions:** >1 versus >5 CPM, CPM filtering versus
`edgeR::filterByExpr()`, and any study-specific sample exclusion policy.

### `differential_expression_edger.qmd`

**Template class:** API / TUTORIAL REMINDER
**Status:** draft
**Canonical source:** none; no complete reusable source DE workflow was found.

**API-DERIVED blocks**

- current edgeR quasi-likelihood sequence:
  `estimateDisp()` → `glmQLFit()` → `glmQLFTest()` → `topTags()`;
- current `model.matrix()` and contrast-vector object contract;
- compact TSV result extraction.

**SOURCE-DERIVED blocks:** none. `GSEA_of_DEGs.qmd` consumes DE results but does
not fit the DE model.

**MERGED blocks:** generic input/output paths and the handoff from the
filtered/normalized DGEList.

**PROJECT-SPECIFIC AND OMITTED blocks:** all cohort designs, fixed contrasts,
sample names, biological labels, significance conclusions, and large
downstream reporting sections.

**Scientific decisions retained:** design formula, covariates, biological
replication, contrast direction, filtering handoff, and reporting thresholds.

**Input contract:** filtered edgeR `DGEList` with raw counts and normalization
factors plus metadata aligned to its sample columns.

**Output contract:** gene-level edgeR quasi-likelihood result TSV with an
explicit reporting flag.

**Persistence:** fitted objects are not serialized by default; result tables
use TSV.

**Validation performed:** current edgeR API inspection, R syntax parsing, and a
temporary replicated-count smoke render that passed design construction,
dispersion estimation, QL fitting, contrast testing, and result extraction.

**Validation still required:** execute with replicated counts and a real study
design; verify dispersion, design rank, contrast signs, and result extraction.

**Unresolved decisions:** every study-specific design, blocking structure,
contrast, replication unit, and reporting threshold.

### `gsea.qmd`

**Template class:** SOURCE-BACKED WORKFLOW
**Status:** draft
**Canonical source:** `examples/bulk_rna/mgi_organoids/GSEA_of_DEGs.qmd`
**Merge sources:** current clusterProfiler documentation and the normalization
cheat sheet's distinction between statistics and transformed expression.

**SOURCE-DERIVED blocks**

- consume a gene-level result/ranking table rather than rerun DE;
- derive or accept a signed ranking statistic;
- map SYMBOL/ENSEMBL identifiers to Entrez IDs;
- remove missing IDs and resolve duplicate mapped IDs;
- run GO BP and KEGG GSEA with explicit gene-set limits and BH adjustment;
- simplify redundant GO terms and export result tables.

**API-DERIVED blocks**

- current clusterProfiler `gseGO()` and `gseKEGG()` calls;
- explicit KEGG key type and current result extraction.

**MERGED blocks:** generic ranking-column parameters, optional GO/KEGG branches,
and compact TSV outputs without project-specific plot networks.

**PROJECT-SPECIFIC AND OMITTED blocks:** High/Low TME labels, OVC/IEO names,
fixed input paths, human-only biological conclusions, project figure panels,
and source-specific evidence-union prose.

**Scientific decisions retained:** ranking statistic, identifier type,
annotation database, organism code, directionality, gene-set size limits,
multiple-testing correction, and GO simplification cutoff.

**Practical notes retained:** use the full ranked result table; do not confuse
GSEA with differential expression; and keep GO and KEGG results separate.

**Input contract:** TSV with one gene identifier and one signed statistic per
row. The canonical default maps to Entrez IDs for GO/KEGG.

**Output contract:** ranked gene list, GO results, optional simplified GO
results, and optional KEGG results as TSV.

**Persistence:** ranking and result tables use TSV; no trivial enrichment
intermediate is serialized.

**API changes:** source-specific names were parameterized; current key types and
clusterProfiler calls were checked; source plots were reduced to the result
tables needed for downstream interpretation.

**Validation performed:** source inspection, current API inspection, R syntax
parsing, and a temporary synthetic GO-only smoke render with valid SYMBOL
mapping. KEGG was disabled in that temporary copy to avoid an external KEGG
request.

**Validation still required:** run with a representative DE result, confirm
identifier mapping and KEGG availability, and review the ranking direction.

**Unresolved decisions:** species/database choice, statistic definition, and
whether GO simplification is appropriate for the intended report.

### `singscore.qmd`

**Template class:** SOURCE-BACKED WORKFLOW
**Status:** draft
**Canonical source:** `examples/bulk_rna/mgi_organoids/HALLMARK_50.qmd`
**Merge sources:** `examples/multiomics/cptac_luad/00_CPTAC_LUAD_scoring` and current
singscore documentation.

**SOURCE-DERIVED blocks**

- gene-set loading and gene coverage checks;
- `singscore::rankGenes()` followed by `singscore::simpleScore()`;
- sample-level score-table extraction;
- direction-aware up/down signature handling from the CPTAC scoring workflow.

**API-DERIVED blocks:** current namespaced singscore calls and explicit score
component extraction.

**MERGED blocks:** generic signature input, coverage threshold, no mandatory
Hallmark collection, and compact TSV outputs.

**PROJECT-SPECIFIC AND OMITTED blocks:** Hallmark-only assumptions, TME
addition, IEO grade, fixed sample ordering, fixed colors, project heatmaps,
and group-specific statistical tests.

**Scientific decisions retained:** expression scale, up/down direction, gene
coverage, tie behavior from rankGenes, and whether score centering is used.

**Practical notes retained:** preserve `TotalScore`, `UpScore`, `DownScore`,
and dispersion columns; inspect coverage before interpretation; and do not
interpret a sample score as a GSEA p-value.

**Input contract:** finite gene-by-sample expression matrix TSV and a signature
TSV with `gene_id` and `direction` columns.

**Output contract:** per-sample score table and direction-specific coverage TSV.

**Persistence:** score and coverage tables use TSV; no additional analytical
object is serialized.

**API changes:** fixed Hallmark/C1 names were removed; source score
standardization was not made primary; generic up/down components are retained.

**Validation performed:** source inspection, current API inspection, R syntax
parsing, and a temporary synthetic score render that passed coverage checks,
rank generation, directional scoring, and TSV output.

**Validation still required:** run with representative normalized expression,
verify gene-ID matching, coverage, and score orientation.

**Unresolved decisions:** expression scale, minimum coverage, signature
definition, and whether any downstream group comparison is scientifically
appropriate.

### `gsva.qmd`

**Template class:** SOURCE-BACKED WORKFLOW
**Status:** draft
**Canonical source:** `examples/multiomics/cptac_luad/00_CPTAC_LUAD_scoring`
**Merge sources:** `examples/bulk_rna/mgi_organoids/HALLMARK_50.qmd` coverage and reporting
patterns, plus current GSVA documentation.

**SOURCE-DERIVED blocks**

- expression matrix orientation and sample-level score extraction;
- `GSVA::gsvaParam()` with a Gaussian kernel on transformed expression;
- `GSVA::gsva()` and gene-set score-table output.

**API-DERIVED blocks:** current parameter-object construction, current output
accessor handling, and explicit kernel/minimum-size parameters.

**MERGED blocks:** generic gene-set TSV input, coverage diagnostics, filtering
of gene sets below the declared mapped size, and compact TSV handoffs.

**PROJECT-SPECIFIC AND OMITTED blocks:** CPTAC, LUAD, C1 signatures, fixed
sample names, RPKM-to-TPM conversion, consensus scoring, fixed biological
classes, and project-specific PCA/correlation plots.

**Scientific decisions retained:** expression scale, gene-set coverage,
minimum/maximum mapped set size, GSVA method, and kernel choice.

**Practical notes retained:** rows are genes and columns are samples; Gaussian
kernel input should be continuous normalized expression; and GSVA is distinct
from singscore and ranked-list GSEA.

**Input contract:** finite gene-by-sample normalized expression matrix TSV and
a gene-set TSV with set and gene identifiers.

**Output contract:** gene-set-by-sample score matrix and gene-set coverage TSV.

**Persistence:** score and coverage tables use TSV; the score matrix is the
useful analytical handoff and is not duplicated as a qs2 object.

**API changes:** source fixed signatures and transformed-input preparation were
removed; current `gsvaParam()`/`gsva()` syntax was verified for the installed
GSVA API; output handling supports the current matrix or SummarizedExperiment
return contract.

**Validation performed:** source inspection, current API inspection, R syntax
parsing, and a temporary synthetic GSVA render that passed coverage checks,
parameter-object construction, score extraction, and TSV output.

**Validation still required:** run with representative normalized expression,
confirm the intended kernel/input scale, and verify gene-set coverage and score
orientation.

**Unresolved decisions:** expression transformation, kernel, set-size limits,
and whether GSVA or singscore is the better score for a particular question.

## Official-documentation checks

Current package APIs were checked before drafting the templates. The compact
checks covered:

- tximport fields and `edgeR::DGEListFromTximport()`;
- edgeR quasi-likelihood functions and filtering/normalization entry points;
- clusterProfiler `gseGO()`/`gseKEGG()` and result extraction;
- GSVA parameter objects, `kcdf`, and return types;
- singscore `rankGenes()`/`simpleScore()` and directional outputs;
- installed `qs2::qs_save()`/`qs2::qs_read()` signatures.

Future users should consult the current official documentation for complex
designs, organism-specific annotation, gene-set databases, kernel assumptions,
and version-specific behavior.

## Validation performed

Static checks passed for all six canonical QMDs:

- balanced Quarto fences;
- exactly one visible `draft` status per notebook;
- 26 extracted R blocks parsed successfully;
- all declared parameters were referenced;
- no absolute private paths, project identifiers, RDS/qs persistence, or CSV
  output violations were found;
- input/output contracts and method-specific warnings were present.

`quarto check` passed with exit status 0. Temporary synthetic code-path smoke
tests also passed for tximport, QC/normalization, the edgeR QL reminder,
singscore, GSVA, and GO-only GSEA. The GSEA smoke copy disabled KEGG solely to
avoid an external KEGG request. An explicit qs2 save/read round trip for an
edgeR DGEList passed.

These checks establish syntax, package-call paths, object alignment, and output
contracts. They do not establish biological significance, QC thresholds,
normalization adequacy, differential-expression validity, enrichment meaning,
or score validity. Synthetic fixtures must not be reported as scientific
results.

## Validation still required

Before promotion to `validated`, run representative count, metadata, DE-result,
normalized-expression, and gene-set inputs through the canonical templates.
Check object persistence, sample/feature alignment, design and contrast signs,
filtering choices, score orientation, identifier coverage, and the scientific
interpretation of every output.

## Unresolved scientific issues

- The appropriate filtering rule is study- and design-dependent; the source
  contains both >1 and >5 CPM branches.
- Sample exclusion requires investigation in the context of replication and
  design; no automatic QC deletion policy is canonicalized.
- `filterByExpr()` versus an explicit CPM rule remains a user decision.
- edgeR design, blocking, contrast, and replication choices cannot be generic.
- GSEA ranking statistics, identifier mapping, organism databases, and GO/KEGG
  redundancy choices remain study-specific.
- Singscore and GSVA require declared input scale and coverage decisions.
- All templates remain draft until representative execution establishes their
  object contracts in the intended environments.
