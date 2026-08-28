#!/usr/bin/env Rscript

files <- system2("git", "ls-files", stdout = TRUE)
errors <- character()
r_files <- 0L
r_chunks <- 0L

parse_r <- function(code, label) {
  tryCatch(
    {
      parse(text = code, keep.source = FALSE)
      TRUE
    },
    error = function(error) {
      errors <<- c(errors, sprintf("%s: %s", label, conditionMessage(error)))
      FALSE
    }
  )
}

for (path in files[grepl("\\.[Rr]$", files)]) {
  parse_r(paste(readLines(path, warn = FALSE), collapse = "\n"), path)
  r_files <- r_files + 1L
}

for (path in files[grepl("\\.qmd$", files)]) {
  lines <- readLines(path, warn = FALSE)
  inside <- FALSE
  body <- character()
  start <- 0L
  for (i in seq_along(lines)) {
    line <- lines[[i]]
    if (!inside && grepl("^```\\{r\\b", line)) {
      inside <- TRUE
      body <- character()
      start <- i
    } else if (inside && trimws(line) == "```") {
      parse_r(paste(body, collapse = "\n"), sprintf("%s:%d", path, start))
      r_chunks <- r_chunks + 1L
      inside <- FALSE
    } else if (inside) {
      body <- c(body, line)
    }
  }
}

if (length(errors)) {
  cat(paste0("ERROR: ", errors, collapse = "\n"), "\n", file = stderr())
  quit(status = 1)
}

cat(sprintf("R syntax checks passed: %d files and %d Quarto chunks parsed\n", r_files, r_chunks))
