# Prompt: document a computational analysis

Use this prompt to write a concise, source-backed README for an analysis folder.

> **Purpose:** Help a researcher understand what the workflow does, what it needs,
> what it produces, and what conclusions its design can support.

## Instructions

Inspect the notebook or scripts, configuration, and existing documentation before
writing. Follow the workflow itself; do not infer methods from filenames or outputs.

Describe only facts supported by the repository. Mark missing details as **not
specified**. Keep measured results separate from interpretation, and identify the
experimental unit, comparison, covariates, validation design, and important
limitations when they affect inference.

Prefer a short guide with these sections when they fit:

1. **Purpose** — the question and analysis scope.
2. **Inputs and unit of analysis** — file/object, sample or cell unit, metadata,
   identifiers, and required layers.
3. **Workflow** — the essential transformations, model, contrast, and diagnostics.
4. **Outputs** — saved objects and tables, with a short description.
5. **Interpretation and limits** — what the design estimates and what it cannot
   establish.
6. **Reproducibility** — software versions, reference data, and execution notes
   only when recorded.

Use a table for inputs or outputs when it makes them easier to compare. Add a
Mermaid diagram only when the workflow has branches or dependencies that prose
does not show clearly. Link to the canonical notebook and relevant upstream
documentation.

## Scientific writing rules

- State the model formula, contrast direction, biological replicate, and
  covariates when available.
- Distinguish cell-level exploratory tests from sample-level inference; do not
  treat cells from one sample as independent biological replicates.
- Separate training, tuning, held-out evaluation, and external validation.
- Report the denominator and analysis unit alongside summaries or metrics.
- Do not call a score a direct measurement, an association a cause, or a
  non-significant result evidence of equivalence.
- Preserve uncertainty and concrete limitations. Do not claim that a workflow
  was run, validated, or reproduced unless the repository shows that evidence.
- Do not invent sample counts, thresholds, software versions, results, citations,
  or biological conclusions.

Keep code, parameters, and outputs unchanged. Edit documentation only unless the
request explicitly includes implementation work.
