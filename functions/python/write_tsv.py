"""Small helper for writing dataframe-like objects as TSV files."""

from pathlib import Path
from typing import Any, Union


def write_tsv(table: Any, path: Union[str, Path]) -> None:
    """Write a dataframe-like object as a headered TSV.

    The object must provide a pandas-compatible ``to_csv`` method. Parent
    directories are created, but table contents and output names stay with the
    caller.
    """

    if not hasattr(table, "to_csv"):
        raise TypeError("table must provide a to_csv method")

    output_path = Path(path)
    if output_path.exists() and output_path.is_dir():
        raise IsADirectoryError(output_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(output_path, sep="\t", index=False)
