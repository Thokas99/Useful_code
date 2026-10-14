# Shared helpers

These small helpers support notebooks that benefit from a common operation.
The analytical workflows remain readable and runnable on their own.

| Language | Helper | Example |
|---|---|---|
| R | [`zscore()`](R/zscore.R) | `zscore(values)` |
| Python | [`write_tsv()`](python/write_tsv.py) | `write_tsv(table, "output/table.tsv")` |

```r
source("functions/R/zscore.R")
zscore(values)
```

```python
from functions.python.write_tsv import write_tsv

write_tsv(table, "output/table.tsv")
```
