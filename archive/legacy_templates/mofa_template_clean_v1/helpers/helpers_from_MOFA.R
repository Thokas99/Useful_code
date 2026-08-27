# Shared helpers copied from the live MOFA notebooks.
# Keep model choices inline in notebooks; only repetitive mechanical code lives here.

# Download helpers

tcga_sample_barcode <- function(x) {
  substr(x, 1, 16)
}

collapse_duplicate_samples_mean <- function(df, feature_col) {
  df |>
    pivot_longer(
      cols = -all_of(feature_col),
      names_to = "sample",
      values_to = "value"
    ) |>
    mutate(sample = tcga_sample_barcode(sample)) |>
    group_by(.data[[feature_col]], sample) |>
    summarise(value = mean(value, na.rm = TRUE), .groups = "drop") |>
    pivot_wider(
      names_from = sample,
      values_from = value
    )
}

collapse_duplicate_samples_sum <- function(df, feature_col) {
  df |>
    pivot_longer(
      cols = -all_of(feature_col),
      names_to = "sample",
      values_to = "value"
    ) |>
    mutate(sample = tcga_sample_barcode(sample)) |>
    group_by(.data[[feature_col]], sample) |>
    summarise(value = sum(value, na.rm = TRUE), .groups = "drop") |>
    pivot_wider(
      names_from = sample,
      values_from = value,
      values_fill = 0
    )
}

collapse_duplicate_samples_max <- function(df, feature_col) {
  df |>
    pivot_longer(
      cols = -all_of(feature_col),
      names_to = "sample",
      values_to = "value"
    ) |>
    mutate(sample = tcga_sample_barcode(sample)) |>
    group_by(.data[[feature_col]], sample) |>
    summarise(value = max(value, na.rm = TRUE), .groups = "drop") |>
    pivot_wider(
      names_from = sample,
      values_from = value,
      values_fill = 0
    )
}

write_output_manifest <- function() {
  output_files <- list.files(
    table_dir,
    pattern = "\\.csv$",
    full.names = TRUE,
    recursive = FALSE
  )

  manifest <- tibble::tibble(
    file = output_files,
    basename = basename(output_files),
    size_bytes = file.info(output_files)$size,
    modified_time = as.character(file.info(output_files)$mtime)
  )

  data.table::fwrite(
    manifest,
    file.path(metadata_dir, "TCGA_LUAD_download_output_manifest.csv")
  )

  manifest
}

# Shared scoring and MOFA helpers

compute_cpm <- function(count_mat) {
  dge <- edgeR::DGEList(counts = count_mat)
  keep <- rowSums(edgeR::cpm(dge) > 1) >= 5
  dge <- dge[keep, , keep.lib.sizes = FALSE]
  dge <- edgeR::normLibSizes(dge, method = "TMMwsp")
  edgeR::cpm(dge,  prior.count = 1)
}

compute_logcpm <- function(count_mat) {
  dge <- edgeR::DGEList(counts = count_mat)
  keep <- rowSums(edgeR::cpm(dge) > 1) >= 5
  dge <- dge[keep, , keep.lib.sizes = FALSE]
  dge <- edgeR::normLibSizes(dge, method = "TMMwsp")
  edgeR::cpm(dge, log = TRUE, prior.count = 1)
}

class_from_z <- function(x) {
  case_when(
    x > 1 ~ "C1-like",
    x > 0 & x <= 1 ~ "C1-intermediate",
    x >= -1 & x <= 0 ~ "Not-C1-intermediate",
    x < -1 ~ "Not-C1-like",
    TRUE ~ NA_character_
  )
}

save_plot_png <- function(plot, filename, width = 10, height = 6) {
  ggplot2::ggsave(
    filename = file.path(FIG_DIR, filename),
    plot = plot,
    width = width,
    height = height,
    units = "in",
    dpi = FIG_DPI,
    bg = "white"
  )
}

keep_most_variable_dt <- function(mat, top_n = 5000, min_non_na_frac = 0.8) {
  mat <- as.matrix(mat)
  storage.mode(mat) <- "numeric"

  keep <- matrixStats::rowMeans2(!is.na(mat)) >= min_non_na_frac
  mat <- mat[keep, , drop = FALSE]

  vars <- matrixStats::rowVars(mat, na.rm = TRUE)

  var_dt <- data.table::data.table(
    feature = rownames(mat),
    variance = vars
  ) |>
    dplyr::filter(is.finite(variance)) |>
    dplyr::arrange(dplyr::desc(variance))

  keep_features <- var_dt |>
    dplyr::slice_head(n = min(top_n, nrow(var_dt))) |>
    dplyr::pull(feature)

  mat[keep_features, , drop = FALSE]
}

to_numeric_matrix <- function(x) {
  x <- as.matrix(x)
  storage.mode(x) <- "numeric"
  x
}

