#' Center and scale a numeric vector with base R's `scale()`.
#'
#' @param x Numeric values.
#' @return A numeric vector with mean zero and unit sample standard deviation.
#'   Missing or constant values can produce `NA` or `NaN`.
zscore <- function(x) {
  if (!is.numeric(x)) {
    stop("x must be numeric.", call. = FALSE)
  }

  as.numeric(scale(x))
}
