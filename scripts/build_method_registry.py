#!/usr/bin/env python3
"""Generate the machine-readable registry for active template notebooks."""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
METHODS_FILE = ROOT / "website" / "_data" / "methods.yml"
DEFAULT_OUTPUT = ROOT / "CODE_MAP" / "method_registry.tsv"
FENCE = chr(96) * 3
HEADER = [
    "method",
    "category",
    "language",
    "main_packages",
    "input",
    "output",
    "status",
    "tags",
    "path",
]

STANDARD_PYTHON_MODULES = {
    "collections",
    "itertools",
    "json",
    "pathlib",
    "re",
    "sys",
    "typing",
}

TAG_TERMS = {
    "atac": "atac",
    "biomarker": "biomarker",
    "cellrank": "cellrank",
    "chromvar": "chromvar",
    "clustering": "clustering",
    "decoupler": "decoupler",
    "doublet": "doublets",
    "edger": "edger",
    "gsea": "gsea",
    "gsva": "gsva",
    "harmony": "harmony",
    "marker": "markers",
    "metabolic": "metabolic",
    "mofa": "mofa",
    "motif": "motifs",
    "multiome": "multiome",
    "normalization": "normalization",
    "pathway": "pathway",
    "qc": "qc",
    "rna": "rna",
    "scatac": "scatac",
    "scrna": "scrna",
    "scvelo": "scvelo",
    "signature": "signatures",
    "trajectory": "trajectory",
    "ucell": "ucell",
    "velocity": "velocity",
    "wnn": "wnn",
}


def load_methods() -> dict:
    """Load the existing catalog YAML without adding a Python dependency."""

    result = subprocess.run(
        [
            "ruby",
            "-ryaml",
            "-rjson",
            "-e",
            'puts JSON.generate(YAML.load_file(ARGV.fetch(0)))',
            str(METHODS_FILE),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "Ruby could not parse methods.yml")
    return json.loads(result.stdout)


def code_blocks(text: str) -> list[tuple[str, str]]:
    """Return language and body for R/Python fenced blocks."""

    blocks = []
    inside = False
    language = ""
    body: list[str] = []
    for line in text.splitlines():
        if line.startswith(FENCE):
            if inside:
                blocks.append((language, "\n".join(body)))
                inside = False
                body = []
            else:
                match = re.match(r"^```\{(r|python)\b", line)
                if match:
                    inside = True
                    language = match.group(1)
                    body = []
        elif inside:
            body.append(line)
    return blocks


def section_summary(text: str, term: str) -> str:
    """Extract the first prose summary under an input/output heading."""

    heading = re.compile(r"^#{2,6}\s+(.+?)\s*$")
    capture = False
    prose: list[str] = []
    for line in text.splitlines():
        match = heading.match(line)
        if match:
            if capture:
                break
            capture = term in match.group(1).lower()
            continue
        if not capture:
            continue
        if line.startswith(FENCE) or line.startswith(":::"):
            break
        if line.strip():
            prose.append(line.strip().lstrip("> "))
        elif prose:
            break
    return re.sub(r"\s+", " ", " ".join(prose)).strip()


def section_code(text: str, term: str) -> str:
    """Return code blocks under the first heading matching ``term``."""

    heading = re.compile(r"^#{2,6}\s+(.+?)\s*$")
    capture = False
    lines: list[str] = []
    for line in text.splitlines():
        match = heading.match(line)
        if match:
            if capture:
                break
            capture = term in match.group(1).lower()
            continue
        if capture:
            lines.append(line)
    return "\n".join(lines)


def configured_paths(text: str, kind: str) -> str:
    """Extract named path-like values without guessing undocumented outputs."""

    code = "\n".join(body for _, body in code_blocks(text))
    assignment = re.compile(
        r"^\s*([A-Za-z][A-Za-z0-9_.]*)\s*(?:<-|=)\s*(?:Path\()?[\"']([^\"']+)[\"']",
        re.MULTILINE,
    )
    values = []
    for name, value in assignment.findall(code):
        lower = name.lower()
        if kind == "input":
            is_input = any(term in lower for term in ("input", "count", "matrix", "metadata", "reference"))
            is_output = lower.startswith("output") or "output" in lower
            if not is_input and not ("path" in lower or "file" in lower):
                continue
            if is_output:
                continue
        else:
            is_output = lower.startswith("output") or any(
                term in lower for term in ("result", "report", "summary", "figure", "plot", "export")
            )
            if not is_output:
                continue
        item = f"{name}={value}"
        if item not in values:
            values.append(item)
    return "; ".join(values)


def registry_value(text: str, term: str) -> str:
    """Prefer authored prose, then expose explicitly configured path values."""

    prose = section_summary(text, term)
    if prose:
        return prose
    if term == "input":
        return configured_paths(section_code(text, term), "input")
    return configured_paths(text, "output")


def package_names(text: str, language: str) -> str:
    code = "\n".join(body for lang, body in code_blocks(text) if lang == language)
    if language == "r":
        names = set(re.findall(r"(?<![A-Za-z0-9_.])([A-Za-z][A-Za-z0-9_.]*)::", code))
        names.update(re.findall(r"^\s*library\(\s*['\"]?([A-Za-z][A-Za-z0-9_.]*)", code, re.MULTILINE))
    else:
        names = set()
        names.update(re.findall(r"^\s*import\s+([A-Za-z][A-Za-z0-9_]*)", code, re.MULTILINE))
        names.update(re.findall(r"^\s*from\s+([A-Za-z][A-Za-z0-9_]*)\s+import", code, re.MULTILINE))
        names.difference_update(STANDARD_PYTHON_MODULES)
    return ";".join(sorted(names))


def tags(family_slug: str, notebook: dict, language: str) -> str:
    text = " ".join(str(notebook.get(key, "")) for key in ("title", "description")).lower()
    values = [family_slug, language]
    for term, tag in TAG_TERMS.items():
        if term in text and tag not in values:
            values.append(tag)
    return ";".join(values)


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip().replace("\t", " ")


def render_registry(methods: dict) -> str:
    rows = []
    seen_paths = set()
    for family in methods.values():
        family_slug = clean(family["slug"])
        for notebook in family["notebooks"]:
            relative_path = clean(notebook["path"])
            if relative_path in seen_paths:
                raise ValueError(f"Duplicate registry path: {relative_path}")
            seen_paths.add(relative_path)
            source = ROOT / relative_path
            if not source.is_file():
                raise FileNotFoundError(relative_path)
            text = source.read_text()
            languages = [lang for lang, _ in code_blocks(text)]
            language = "python" if "python" in languages else "r"
            rows.append(
                [
                    clean(notebook["title"]),
                    clean(family["title"]),
                    language,
                    package_names(text, language),
                    registry_value(text, "input"),
                    registry_value(text, "output"),
                    clean(notebook["status"]),
                    tags(family_slug, notebook, language),
                    relative_path,
                ]
            )

    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer, delimiter="\t", lineterminator="\n")
    writer.writerow(HEADER)
    writer.writerows(rows)
    return buffer.getvalue()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if the committed TSV is stale")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    try:
        content = render_registry(load_methods())
    except (FileNotFoundError, RuntimeError, ValueError, json.JSONDecodeError) as error:
        print(f"method registry failed: {error}", file=sys.stderr)
        return 1

    output = args.output if args.output.is_absolute() else ROOT / args.output
    if args.check:
        if not output.is_file() or output.read_text() != content:
            print(f"{output} is stale; run python3 scripts/build_method_registry.py", file=sys.stderr)
            return 1
        print(f"Registry is current: {output}")
        return 0

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content)
    print(f"Wrote {len(content.splitlines()) - 1} notebook rows to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
