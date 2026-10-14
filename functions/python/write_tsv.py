"""Write a pandas-style table as TSV without row names."""

from pathlib import Path
from typing import Any, Union


def write_tsv(table: Any, path: Union[str, Path]) -> None:
    """Write ``table`` to ``path`` with tab separators and no index.

    ``table`` must provide ``to_csv``. Parent directories are created.
    """

    if not hasattr(table, "to_csv"):
        raise TypeError("table must provide a to_csv method")

    output_path = Path(path)
    if output_path.exists() and output_path.is_dir():
        raise IsADirectoryError(output_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(output_path, sep="\t", index=False)
