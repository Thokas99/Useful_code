#' Standardize a numeric vector using base R's scale behavior.
#'
#' @param x A numeric vector.
#' @return A numeric vector with the scaled values.
zscore <- function(x) {
  if (!is.numeric(x)) {
    stop("x must be numeric.", call. = FALSE)
  }

  as.numeric(scale(x))
}
