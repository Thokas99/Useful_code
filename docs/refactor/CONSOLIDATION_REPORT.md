# Final consolidation report

## Before

The repository combined an almost empty root landing page, active canonical
templates, project notebooks under `CODE_MAP/code_MAP/`, MOFA sources and an
intermediate clean scaffold under `CODE_MAP/code_MOFA/`, old notebook
scaffolds, development reports, archives, and local context
files. The canonical families were already established, but their navigation
and provenance boundaries were not.

## Final architecture

```text
Useful_code/
├── README.md
├── LICENSE
├── templates/
│   ├── README.md
│   ├── single_cell/
│   ├── bulk_rna/
│   ├── scatac/
│   ├── multiome/
│   ├── multiomics/mofa/
│   └── machine_learning/biomarkers/
├── examples/
│   ├── single_cell/
│   ├── bulk_rna/
│   ├── biomarker_ml/
│   └── multiomics/
├── docs/
│   ├── ARCHITECTURE.md
│   └── refactor/
└── archive/
    ├── legacy_templates/
    └── raw_archives/
```

`CODE_MAP/` remains only for intentionally untouched legacy metadata and local
untracked material described below; active canonical navigation no longer
depends on it.

## Moves

| Old path or group | New path | Classification | Reason |
|---|---|---|---|
| Root implementation reports | `docs/refactor/implementation_reports/` | REFACTOR DOCUMENTATION | Keep development provenance out of the repository front door. |
| `CANONICALIZATION_PLAN.md`, `REFACTOR_AUDIT.md` | `docs/refactor/` | REFACTOR DOCUMENTATION | Preserve the historical audit and plan. |
| `templates/machine_learning/biomarker_*.qmd` | `templates/machine_learning/biomarkers/` | ACTIVE CANONICAL | Normalize the family path without changing analytical code. |
| `CODE_MAP/code_MAP/` MAP QMDs | `examples/single_cell/map/` | PROJECT EXAMPLE | Preserve the coupled MAP source workflow and provenance. |
| `GSE171145.qmd` | `examples/single_cell/gse171145.qmd` | PROJECT EXAMPLE | Preserve the external cohort workflow separately. |
| MGI QMDs | `examples/bulk_rna/mgi_organoids/` | PROJECT EXAMPLE | Keep bulk-RNA source workflows together. |
| `00_CPTAC_LUAD_scoring` | `examples/multiomics/cptac_luad/` | PROJECT EXAMPLE | Preserve its project-specific multi-omics scoring context. |
| TCGA/MOFA QMDs | `examples/multiomics/tcga_mofa/` | PROJECT EXAMPLE | Separate real project workflows from the canonical MOFA family. |
| `CODE_MAP/TRENTO_*.qmd` | `examples/biomarker_ml/trento/` | PROJECT EXAMPLE | Preserve the original ML and reporting provenance; no private paths or credentials were detected. |
| `CODE_MAP/code_MAP/notebook_templates/` | `archive/legacy_templates/notebook_templates_v1/` | LEGACY TEMPLATE / SUPERSEDED | Retain the old scaffold without presenting it as active. |
| `CODE_MAP/code_MOFA/MOFA_TEMPLATE_CLEAN/` | `archive/legacy_templates/mofa_template_clean_v1/` | LEGACY TEMPLATE / SUPERSEDED | Retain the project-shaped MOFA scaffold beside the split canonical family. |
| `CODE_MAP/code_MAP/Archive.zip`, interview ZIP | `archive/raw_archives/` | ARCHIVE | Preserve historical archives without unpacking or duplication. |
| Former compact reference material | Retired | REFERENCE | No active cheatsheet collection is maintained. |

The implementation reports record current example/archive paths and retain
former source names where needed for historical interpretation.

## Canonical template inventory

There are 37 canonical QMDs:

| Family | Templates | Source-backed | API/tutorial reminder | Validated | Draft | Blocked |
|---|---:|---:|---:|---:|---:|---:|
| Single-cell RNA | 16 | 15 | 1 | 0 | 16 | 0 |
| Bulk RNA-seq | 6 | 5 | 1 | 0 | 6 | 0 |
| scATAC-seq | 5 | 4 | 1 | 0 | 5 | 0 |
| Multiome | 4 | 4 | 0 | 0 | 4 | 0 |
| Multi-omics / MOFA | 4 | 4 | 0 | 0 | 4 | 0 |
| Biomarker ML | 2 | 2 | 0 | 0 | 2 | 0 |
| **Total** | **37** | **34** | **3** | **0** | **37** | **0** |

The source/API class and strict status are stated inside every canonical QMD.
No status was upgraded merely because a file parses or a small smoke test
exists.

## Examples and provenance

Moved project material includes the MAP single-cell/ATAC/multiome downstream
workflows, the GSE171145 cohort workflow, MGI organoid bulk-RNA sources,
TRENTO biomarker notebooks, TCGA/MOFA sources, and CPTAC-LUAD scoring. The
notebooks were moved rather than copied so Git history retains one source of
truth. They may still require their original external input/output layout.

The tracked `CODE_MAP/alevin_fry/` directory was not moved: its README and
shell wrapper document private absolute storage paths and project-specific
quantification inputs. It remains available in place for deliberate local
reconstruction and is not promoted as a public canonical workflow.

## Legacy and archive

The old scRNA/scATAC/multiome/general-statistics scaffold and the old clean
MOFA scaffold are under `archive/legacy_templates/`. Their README files now
state that they are superseded, while retaining the useful historical content
from the pre-existing local modifications.

The two ZIP archives are under `archive/raw_archives/` and were not unpacked.
No raw omics matrix, fragment file, model output, or generated website was
added.

## Dirty and untracked material

| Item | Decision | Reason |
|---|---|---|
| `README.md` | Integrated | Rewritten as the concise repository landing page; project detail moved to example/navigation documentation. |
| `CODE_MAP/code_MAP/notebook_templates/README.md` | Archived | Its useful historical contract is retained in the moved legacy README with a superseded notice. |
| `CODE_MAP/code_MOFA/MOFA_TEMPLATE_CLEAN/README.md` | Archived | Its useful scaffold explanation is retained in the moved legacy README with a superseded notice. |
| TRENTO source notebooks | Integrated | Safe example provenance after security/path scan; inputs and outputs remain external. |
| `.claude/` | Keep local / do not commit | Coding-agent context files. |
| `AGENTS.md`, `CLAUDE.md` | Keep local / do not commit | Local coding-agent instructions. |
| `CODE_MAP/README.md`, `CODE_MAP/code_MAP/README.md`, `CODE_MAP/code_MOFA/README.md` | Leave untouched | Pre-existing untracked source-map documents; not needed after new canonical navigation. |
| `CODE_MAP/alevin_fry/README.md` | Leave untouched | Documents private-path infrastructure; moving it would promote private local assumptions. |
| untracked old family READMEs under `CODE_MAP/code_MAP/notebook_templates/` | Leave untouched | Local context files adjacent to archived tracked scaffolds; not required by active navigation. |
| `CODE_MAP/quarto_config_tmplate.md` and duplicate Quarto template documents | Leave local / superseded | Overlapping untracked reference material; current Quarto report guidance is maintained under `miscellaneous/quarto/`. |
| `.DS_Store` files | Leave untouched | Existing tracked metadata was not part of this non-destructive consolidation. |

## Deletions

None. Existing content was moved, retained, or left untouched; no destructive
cleanup was performed.

## Validation

Completed on the consolidation worktree:

- `git diff --check`: passed for the staged documentation checkpoint;
- 37 canonical QMDs checked, with 94 R blocks and 16 Python blocks parsed;
- Quarto fences were balanced;
- R parsing and Python AST parsing passed;
- 124 Markdown/QMD files were checked for relative links; no broken links were
  found after repairing archived README links;
- canonical templates had no absolute local paths, stale `CODE_MAP` template
  paths, or old ML filenames;
- canonical QMDs contained no TCGA/LUAD/C1/project identifiers;
- `quarto check`: passed with Quarto 1.10.18, R 4.6.1, and Python 3.14.7;
- no website configuration or deployment files were created.

These are structural/static checks. Analytical templates remain `draft` unless
representative runtime validation existed before consolidation. The one
canonical ML input path retaining `.csv` is an input-contract detail inherited
from the prior canonical workflow, not a tabular output or persistence change.

## Website readiness

The repository is structurally ready for a later documentation layer: active
templates have predictable paths, examples and archives have explicit roles,
reports are grouped under `docs/`, and the root README points to the canonical
library. This mission did not create website files, Quarto website
configuration, or deployment workflows.

## Miscellaneous resources

Two reusable non-analytical resources were incorporated after the main
consolidation:

- a scientific Methods documentation prompt;
- a Quarto scientific-report template.

They were placed under `/miscellaneous` rather than `/templates` because they
support documentation and reporting workflows rather than defining analytical
methods.

## Remaining uncertainty

The private-path `alevin_fry` infrastructure and several pre-existing
untracked source-map/reference documents remain under `CODE_MAP/` locally. They
were deliberately not guessed into the public architecture. A later cleanup
can decide their fate after private-path review and dependency reconstruction.
