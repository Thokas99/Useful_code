#!/usr/bin/env python3
"""Run lightweight structural checks for the repository."""

from __future__ import annotations

import argparse
import ast
import csv
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
ABSOLUTE_PATH = re.compile(r"(?<![A-Za-z0-9])/(?:Users|home|Volumes|mnt|tmp|var|opt)/")
WINDOWS_PATH = re.compile(r"\b[A-Za-z]:[\\/]")
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)\s]+)")
HREF = re.compile(r"\bhref=[\"']([^\"']+)[\"']", re.IGNORECASE)


def tracked_files() -> list[Path]:
    output = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT)
    return [ROOT / name for name in output.decode().split("\0") if name]


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def check_python(paths: list[Path]) -> list[str]:
    errors = []
    parsed_files = 0
    parsed_blocks = 0
    for path in paths:
        name = relative(path)
        if path.suffix == ".py":
            try:
                ast.parse(path.read_text(), filename=name)
                parsed_files += 1
            except SyntaxError as error:
                errors.append(f"Python syntax: {name}:{error.lineno}: {error.msg}")
        if path.suffix != ".qmd":
            continue
        lines = path.read_text().splitlines()
        inside = False
        body: list[str] = []
        start = 0
        for line_number, line in enumerate(lines, 1):
            if not inside and re.match(r"^```\{python\b", line):
                inside = True
                body = []
                start = line_number
            elif inside and line.strip() == "```":
                try:
                    ast.parse("\n".join(body), filename=f"{name}:{start}")
                    parsed_blocks += 1
                except SyntaxError as error:
                    errors.append(f"Python chunk: {name}:{start + (error.lineno or 1)}: {error.msg}")
                inside = False
            elif inside:
                body.append(line)
    print(f"Python checks: {parsed_files} files and {parsed_blocks} Quarto chunks parsed")
    return errors


def check_template_paths(paths: list[Path]) -> list[str]:
    errors = []
    for path in paths:
        if "templates" not in path.parts or path.suffix != ".qmd":
            continue
        text = path.read_text()
        if ABSOLUTE_PATH.search(text) or WINDOWS_PATH.search(text):
            errors.append(f"Absolute path in reusable template: {relative(path)}")
    print("Reusable-template absolute-path check complete")
    return errors


def check_quarto_fences(paths: list[Path]) -> list[str]:
    errors = []
    checked = 0
    for path in paths:
        if path.suffix != ".qmd":
            continue
        checked += 1
        fences = sum(line.startswith("```") for line in path.read_text().splitlines())
        if fences % 2:
            errors.append(f"Unbalanced code fence: {relative(path)}")
    print(f"Quarto fence check: {checked} documents checked")
    return errors


def check_large_files(paths: list[Path]) -> list[str]:
    errors = []
    for path in paths:
        size = path.stat().st_size
        parts = {part.lower() for part in path.parts}
        limit = 5 * 1024 * 1024 if parts & {"data", "output", "results"} else 25 * 1024 * 1024
        if size >= limit:
            errors.append(f"Large tracked file ({size} bytes): {relative(path)}")
    print("Tracked-file size check complete")
    return errors


def target_exists(base: Path, target: str) -> bool:
    parsed = urlsplit(unquote(target))
    if parsed.scheme or parsed.netloc or not parsed.path:
        return True
    if target.startswith("/"):
        return True
    candidate = (base / parsed.path).resolve()
    if candidate.is_file():
        return True
    if candidate.is_dir():
        return True
    return False


def check_markdown_links(paths: list[Path]) -> list[str]:
    errors = []
    checked = 0
    for path in paths:
        if path.suffix not in {".md", ".qmd"}:
            continue
        for target in LINK.findall(path.read_text()):
            if target.startswith(("http://", "https://", "mailto:", "#", "{{", "{%")):
                continue
            if target.startswith("<"):
                target = target[1:].split(">", 1)[0]
            checked += 1
            if not target_exists(path.parent, target):
                errors.append(f"Broken Markdown link: {relative(path)} -> {target}")
    print(f"Markdown link check: {checked} local links checked")
    return errors


def site_target_exists(site_root: Path, source_html: Path, target: str) -> bool:
    parsed = urlsplit(unquote(target))
    if parsed.scheme or parsed.netloc or not parsed.path:
        return True
    path = parsed.path
    base = "/Useful_code/"
    if path.startswith(base):
        path = path[len(base) :]
    elif path.startswith("/"):
        path = path.lstrip("/")
    candidate = (site_root / path).resolve()
    if candidate.is_file():
        return True
    if candidate.is_dir() and (candidate / "index.html").is_file():
        return True
    if not candidate.suffix and (candidate.with_suffix(".html")).is_file():
        return True
    if not parsed.path.startswith("/") and (source_html.parent / parsed.path).resolve().is_file():
        return True
    return False


def check_site(site_root: Path) -> list[str]:
    errors = []
    checked = 0
    for path in site_root.rglob("*.html"):
        for target in HREF.findall(path.read_text(errors="replace")):
            if target.startswith(("http://", "https://", "mailto:", "#", "javascript:", "{{", "{%")):
                continue
            checked += 1
            if not site_target_exists(site_root, path, target):
                errors.append(f"Broken built-site link: {relative(path)} -> {target}")
    print(f"Built-site link check: {checked} local links checked")
    return errors


def load_registry(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    errors = []
    if not path.is_file():
        return [], [f"Missing method registry: {relative(path)}"]
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    required = {"method", "category", "language", "main_packages", "input", "output", "status", "tags", "path"}
    if set(rows[0]) != required if rows else True:
        errors.append("Method registry has an unexpected header")
    paths = [row.get("path", "") for row in rows]
    if len(paths) != len(set(paths)):
        errors.append("Method registry contains duplicate paths")
    for item in paths:
        if not item.startswith("templates/") or not (ROOT / item).is_file():
            errors.append(f"Registry path is missing or outside templates/: {item}")
    print(f"Method registry check: {len(rows)} rows")
    return rows, errors


def check_catalog_consistency(registry_rows: list[dict[str, str]]) -> list[str]:
    command = [
        "ruby",
        "-ryaml",
        "-rjson",
        "-e",
        'puts JSON.generate(YAML.load_file(ARGV.fetch(0)))',
        "website/_data/methods.yml",
    ]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        return [f"Catalog YAML could not be read: {result.stderr.strip()}"]
    import json

    methods = json.loads(result.stdout)
    catalog_paths = [notebook["path"] for family in methods.values() for notebook in family["notebooks"]]
    registry_paths = [row["path"] for row in registry_rows]
    errors = []
    if catalog_paths != registry_paths:
        errors.append("Method registry paths do not match website/_data/methods.yml")
    print(f"Catalog consistency check: {len(catalog_paths)} catalog notebooks")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", type=Path, help="also check links in a built Jekyll site")
    args = parser.parse_args()
    paths = tracked_files()
    errors: list[str] = []
    errors += check_python(paths)
    errors += check_template_paths(paths)
    errors += check_quarto_fences(paths)
    errors += check_large_files(paths)
    errors += check_markdown_links(paths)
    rows, registry_errors = load_registry(ROOT / "CODE_MAP" / "method_registry.tsv")
    errors += registry_errors
    errors += check_catalog_consistency(rows)
    if args.site:
        errors += check_site((ROOT / args.site).resolve())
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1
    print("Repository checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
