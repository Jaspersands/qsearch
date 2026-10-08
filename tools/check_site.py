"""Static checks for the public website.

Every repository path the site mentions must exist, every internal page link must
resolve, and no current metric value may be written into HTML (counts are filled
from JSON at runtime).

Run from the repository root:
    python tools/check_site.py
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO_PATH = re.compile(
    r"(?<![\w.-])((?:core|docs|research|site|tests|theorems|tools)/[\w./-]+\.(?:css|html|js|json|md|py)"
    r"|qsearch\.py)(?![\w/-])"
)
INTERNAL_LINK = re.compile(r'href="([\w./-]+\.html)(?:#[^"]*)?"')
METRIC_FLOOR = 100


def site_files(root: Path) -> list[Path]:
    files = sorted(root.glob("*.html"))
    scripts = root / "site" / "js"
    if scripts.is_dir():
        files += sorted(scripts.rglob("*.js"))
    return files


def missing_references(root: Path) -> list[str]:
    problems = []
    for path in site_files(root):
        name = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        for reference in sorted(set(REPO_PATH.findall(text))):
            if not (root / reference).is_file():
                problems.append(f"{name}: references missing file {reference}")
        if path.suffix == ".html":
            for link in sorted(set(INTERNAL_LINK.findall(text))):
                if not (root / link).is_file():
                    problems.append(f"{name}: links to missing page {link}")
    return problems


def hardcoded_metrics(root: Path) -> list[str]:
    snapshot = json.loads((root / "research" / "progress_snapshot.json").read_text(encoding="utf-8"))
    values = sorted(
        value
        for value in snapshot.get("metrics", {}).values()
        if isinstance(value, int) and value >= METRIC_FLOOR
    )
    problems = []
    for path in sorted(root.glob("*.html")):
        text = path.read_text(encoding="utf-8")
        for value in values:
            for form in dict.fromkeys([str(value), f"{value:,}"]):
                if re.search(rf"(?<![\w.,-]){re.escape(form)}(?![\w.,-])", text):
                    problems.append(f"{path.name}: hardcodes the current metric value {form}")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository root.")
    args = parser.parse_args(argv)
    problems = missing_references(args.root) + hardcoded_metrics(args.root)
    for problem in problems:
        print(problem)
    if not problems:
        print("Site checks passed.")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
