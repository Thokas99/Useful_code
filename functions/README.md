# Shared functions

`functions/` contains small, standalone implementation primitives that are
useful across more than one notebook. The analytical notebooks remain
self-contained where sourcing a repository-relative file would make copying
them harder.

R:

```r
source("functions/R/zscore.R")
zscore(values)
```

Python:

```python
from functions.python.write_tsv import write_tsv

write_tsv(table, "output/table.tsv")
```

These helpers do not replace the notebook workflows or package documentation.
