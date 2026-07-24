# RNA-seq Normalization Cheat Sheet

> CPM · FPKM · TPM · TMM/TMMwsp · logCPM · negative values — for a wet-lab audience

---

## 1. Starting point: raw counts

$$y_{gi}$$

| Symbol   | Meaning                                     |
| -------- | ------------------------------------------- |
| $g$      | gene / miRNA / transcript                   |
| $i$      | sample                                      |
| $y_{gi}$ | reads assigned to feature $g$ in sample $i$ |

Raw counts are **not comparable across samples** — one sample may simply have more total reads.

---

## 2. Library size

$$L_i = \sum_g y_{gi}$$

The total mapped reads per sample. The root cause of why normalization is needed.

---

## 3. CPM — Counts Per Million

$$\text{CPM}_{gi} = \frac{y_{gi}}{L_i} \times 10^6$$

> "Out of one million reads in this sample, how many came from this gene?"

**Example:** 500 counts, library size = 10 M → CPM = 50

|    CPM | Interpretation |
| -----: | -------------- |
|      0 | not detected   |
|    < 1 | very low       |
|    1–5 | low            |
| 10–100 | moderate       |
|  > 100 | high           |

Best for: gene-level / miRNA-level expression matrices. For miRNA-seq, length correction is usually not the main concern, so CPM/logCPM is standard.

---

## 4. FPKM / RPKM

$$\text{FPKM}_{gi} = \frac{y_{gi} \times 10^9}{L_i \times \ell_g}$$

where $\ell_g$ = feature length in bp.

Corrects for: sequencing depth + gene length (longer genes accumulate more reads regardless of biology).

**Limitation:** FPKM values are hard to compare between samples — the total distribution shifts with transcript composition. Now largely superseded by TPM.

---

## 5. TPM — Transcripts Per Million

**Step 1 — length-correct:**
$$r_{gi} = \frac{y_{gi}}{\ell_g}$$

**Step 2 — scale to 1 million:**
$$\text{TPM}_{gi} = \frac{r_{gi}}{\sum_g r_{gi}} \times 10^6$$

Every sample sums to exactly 1 M, making between-sample comparison cleaner than FPKM.

> "Out of one million normalized transcript molecules, how many are from this gene?"

---

## 6. Method comparison

| Measure    | Depth? | Length? | Composition bias? | Typical use                      |
| ---------- | :----: | :-----: | :---------------: | -------------------------------- |
| Raw counts |   ✗    |    ✗    |         ✗         | DESeq2/edgeR model input         |
| CPM        |   ✓    |    ✗    |         ✗         | gene/miRNA expression            |
| FPKM       |   ✓    |    ✓    |       weak        | older RNA-seq reporting          |
| TPM        |   ✓    |    ✓    |      partial      | transcript abundance             |
| TMM-CPM    |   ✓    |    ✗    |         ✓         | normalized gene/miRNA expression |
| TMMwsp-CPM |   ✓    |    ✗    |         ✓         | sparse RNA/miRNA data            |
| logCPM     |   ✓    |    ✗    |  ✓ (if TMM used)  | modeling, correlations, heatmaps |

**Practical rule:**

- Transcript/gene abundance → **TPM**
- Differential expression → **raw counts + DESeq2/edgeR/limma-voom**
- Normalized matrices, plots, correlations, biomarker modeling → **logCPM**

---

## 7. TMM normalization

**TMM = Trimmed Mean of M-values** (edgeR)

Corrects for composition bias. Assumes most genes are not truly DE, then estimates a per-sample scaling factor $f_i$:

$$L_i^* = L_i \times f_i \qquad \text{(effective library size)}$$

$$\text{CPM}_{gi}^{\text{TMM}} = \frac{y_{gi}}{L_i^*} \times 10^6$$

```r
dge <- edgeR::DGEList(counts = count_mat)
dge <- edgeR::normLibSizes(dge, method = "TMM")
logcpm <- edgeR::cpm(dge, log = TRUE, prior.count = 1)
```

---

## 8. TMMwsp normalization

**TMMwsp = TMM with singleton pairing**

Standard TMM needs features expressed in _both_ samples to compare. When data are sparse (many zeros), fewer features qualify. TMMwsp uses singleton positive counts to recover information.

Use for: miRNA-seq · low-input RNA-seq · small panels · sparse matrices.

```r
dge <- edgeR::DGEList(counts = count_mat)
dge <- edgeR::normLibSizes(dge, method = "TMMwsp")
logcpm <- edgeR::cpm(dge, log = TRUE, prior.count = 1)
```

---

## 9. logCPM

$$\log_2(\text{CPM}_{gi})$$

Raw CPM is right-skewed. Log scale makes fold-changes symmetric and variances more stable.

|   CPM | log₂CPM |
| ----: | ------: |
| 0.125 |      −3 |
|  0.25 |      −2 |
|   0.5 |      −1 |
|     1 |       0 |
|     2 |       1 |
|     4 |       2 |
|     8 |       3 |
|    16 |       4 |

### ⚠️ Negative logCPM ≠ negative expression

$$\log_2(\text{CPM}) < 0 \iff 0 < \text{CPM} < 1$$

Negative logCPM means: **detected at less than 1 count per million** — not absent, not an error.

---

## 10. `prior.count = 1` — what it actually does

`edgeR::cpm(dge, log = TRUE, prior.count = 1)` adds a small pseudocount **on the count scale** (adjusted per library size) before logging, to avoid $\log_2(0) = -\infty$.

This is **not** the same as `log2(cpm + 1)`. The prior is size-adjusted:

$$\log_2\!\left(\frac{y_{gi} + p_i}{L_i^* + P_i} \times 10^6\right)$$

Values can still be negative after adding the prior if the adjusted CPM remains below 1. That is expected.

---

## 11. Why negative values survive filtering

A typical filter:

```r
keep <- rowSums(edgeR::cpm(dge) > 1) >= 3
```

Keeps features with CPM > 1 in **at least 3 samples** — not in _all_ samples. Samples below the threshold are still retained with their (negative) logCPM values.

| Sample | CPM |       log₂CPM |
| ------ | --: | ------------: |
| S1     | 4.2 |          2.07 |
| S2     | 2.1 |          1.07 |
| S3     | 1.3 |          0.38 |
| S4     | 0.7 |         −0.51 |
| S5     | 0.2 |         −2.32 |
| S6     | 0.0 | prior handles |

Feature passes filter (3 samples > 1 CPM) but S4–S6 legitimately have negative logCPM.

---

## 12. Do not clip negative logCPM for statistics

Clipping $x \leftarrow \max(x, 0)$ forces all values below 1 CPM to the same number:

|  CPM | log₂CPM | clipped |
| ---: | ------: | ------: |
|  1.0 |       0 |       0 |
|  0.5 |      −1 |   **0** |
| 0.25 |      −2 |   **0** |
| 0.01 |   −6.64 |   **0** |

0.5 CPM ≠ 0.01 CPM — but clipping makes them identical. This distorts correlations, regression, LASSO, PCA, and any biomarker ranking.

### Clipping is only acceptable for visualization

```r
# heatmap color scale only — never for statistics
logcpm_plot <- logcpm
logcpm_plot[logcpm_plot < -2] <- -2
logcpm_plot[logcpm_plot > 8]  <-  8

# or z-score with capped colors
z <- t(scale(t(logcpm)))
z[z < -2] <- -2
z[z > 2]  <-  2
```

---

## 13. Recommended workflow (miRNA/biomarker)

```r
compute_logcpm <- function(count_mat) {
  dge <- edgeR::DGEList(counts = count_mat)
  dge <- edgeR::normLibSizes(dge, method = "TMMwsp")   # composition correction
  keep <- rowSums(edgeR::cpm(dge) > 1) >= 3            # filter low features
  dge  <- dge[keep, , keep.lib.sizes = FALSE]
  edgeR::cpm(dge, log = TRUE, prior.count = 1)          # logCPM; negatives are fine
}
```

```
raw counts
  → TMMwsp normalization
  → CPM-based feature filtering
  → logCPM (prior.count = 1)
  → keep negative values
  → use for correlation / GLM / LASSO / heatmaps / biomarker plots
```

---

## 14. One-slide summary for the PI

| Step            | Formula                                                 | Purpose                                    |
| --------------- | ------------------------------------------------------- | ------------------------------------------ |
| Raw counts      | $y_{gi}$                                                | Starting point; not comparable             |
| CPM             | $\frac{y_{gi}}{L_i} \times 10^6$                        | Correct for sequencing depth               |
| TMM/TMMwsp-CPM  | $\frac{y_{gi}}{L_i \times f_i} \times 10^6$             | Also correct for composition bias          |
| logCPM          | $\log_2(\text{CPM}^{\text{norm}})$                      | Stabilize variance, symmetric fold-changes |
| Negative logCPM | $\log_2(\text{CPM}) < 0 \Leftrightarrow \text{CPM} < 1$ | Very low abundance — not an error          |
| Clipping        | $\max(x, 0)$                                            | **Do not use for statistics**              |

---

## 15. Wet-lab elevator pitch

> Raw counts depend on sequencing depth, so we normalize to counts per million. We then apply TMMwsp to correct for differences in RNA composition between samples — especially important because miRNA data are often sparse. Finally, we take log₂ CPM to make expression differences proportional and suitable for statistics. Negative logCPM values are not negative expression; they mean the feature is present below 1 count per million in that sample. We filter weak features before analysis, but we never clip the remaining values — clipping would force all low-expression differences to look identical and distort every downstream model.
