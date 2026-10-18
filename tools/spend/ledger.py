"""Code-free spend ledger: one event per line, rebuilt from data the repo already has.

    python tools/spend/ledger.py                  # rebuild research/audits/spend_ledger.jsonl
    python tools/spend/ledger.py --root DIR --out FILE

Sources and the kinds they give:
  experiment_run        research/experiment_run_history.json (one timestamp per run, no duration)
  theorem_commit        git log of theorems/ (one line per theorem file per commit)
  registry_commit       git history of research/registry/negative_results.json (count and new ids)
  registry_uncommitted  ids in the working-tree registry that no commit has yet, dated by file mtime
  report_write          mtimes of the REPORT json files that theorem modules name

The rebuild replaces only these kinds. Lines of any other kind (timed_run from timed.py,
token_day from tokens.py) are kept as they are. Git is only read, never written.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.spend.common import LEDGER, NEGATIVES, REGISTRY_DIR, git, read_json, replace_kinds, to_utc_iso  # noqa: E402

HISTORY = "research/experiment_run_history.json"
NEGATIVES_PATH = f"{REGISTRY_DIR.as_posix()}/{NEGATIVES}"
DERIVED_KINDS = ("experiment_run", "theorem_commit", "registry_commit", "registry_uncommitted", "report_write")
REPORT_CONSTANT = re.compile(r"^REPORT[A-Z0-9_]*\s*(?::[^=\n]*)?=(?!=)")
JSON_LITERAL = re.compile(r"[\"'](research/[^\"'\n]+?\.json)[\"']")


def experiment_run_events(history: list[dict]) -> list[dict]:
    events = []
    for row in history:
        if not isinstance(row, dict) or not row.get("recorded_at"):
            continue
        written = (row.get("metrics") or {}).get("negative_results_written")
        events.append({
            "kind": "experiment_run",
            "timestamp": to_utc_iso(row["recorded_at"]),
            "run_id": row.get("run_id"),
            "experiment_id": row.get("experiment_id"),
            "candidate_id": row.get("candidate_id"),
            "status": row.get("status"),
            "falsifier_count": row.get("falsifier_count"),
            "negatives_written": written if isinstance(written, int) else None,
            "source": HISTORY,
        })
    return events


def parse_theorem_log(text: str) -> list[dict]:
    """Parse `git log --format='C %H %cI' --name-status --no-renames -- theorems/`."""
    events = []
    sha = when = None
    for line in text.splitlines():
        if line.startswith("C "):
            _, sha, when = line.split(" ", 2)
            continue
        if "\t" not in line or sha is None:
            continue
        status, path = line.split("\t", 1)
        if not (path.startswith("theorems/") and path.endswith(".py")):
            continue
        events.append({
            "kind": "theorem_commit",
            "timestamp": to_utc_iso(when),
            "sha": sha[:12],
            "path": path,
            "change": status[:1],
            "source": "git",
        })
    return events


def theorem_commit_events(root: Path) -> list[dict]:
    text = git(root, "log", "--format=C %H %cI", "--name-status", "--no-renames", "--", "theorems/")
    return parse_theorem_log(text) if text else []


def registry_history(root: Path) -> list[tuple[str, str, list]]:
    """(sha, commit time, records) for every commit that touched the negatives registry, oldest first."""
    log = git(root, "log", "--reverse", "--format=%H %cI", "--", NEGATIVES_PATH)
    history = []
    for line in (log or "").splitlines():
        sha, when = line.split(" ", 1)
        blob = git(root, "show", f"{sha}:{NEGATIVES_PATH}")
        try:
            records = json.loads(blob) if blob else None
        except ValueError:
            records = None
        if isinstance(records, list):
            history.append((sha, when, records))
    return history


def _ids(records: list) -> set[str]:
    return {row["id"] for row in records if isinstance(row, dict) and row.get("id")}


def registry_commit_events(history: list[tuple[str, str, list]], current_ids: set[str], current_mtime: float) -> list[dict]:
    """Negatives per commit; `negatives_new_retained` counts ids first seen there and still in the registry."""
    events = []
    seen: set[str] = set()
    previous = 0
    for sha, when, records in history:
        ids = _ids(records)
        new = ids - seen
        seen |= ids
        events.append({
            "kind": "registry_commit",
            "timestamp": to_utc_iso(when),
            "sha": sha[:12],
            "negatives": len(ids),
            "negatives_delta": len(ids) - previous,
            "negatives_new": len(new),
            "negatives_new_retained": len(new & current_ids),
            "source": "git",
        })
        previous = len(ids)
    uncommitted = current_ids - seen
    if uncommitted:
        events.append({
            "kind": "registry_uncommitted",
            "timestamp": to_utc_iso(current_mtime),
            "negatives": len(current_ids),
            "negatives_new_retained": len(uncommitted),
            "source": f"mtime {NEGATIVES_PATH}",
        })
    return events


def _registry_events(root: Path) -> list[dict]:
    path = root / NEGATIVES_PATH
    if not path.exists():
        return []
    current = read_json(path)
    current_ids = _ids(current if isinstance(current, list) else [])
    return registry_commit_events(registry_history(root), current_ids, path.stat().st_mtime)


def report_paths(root: Path) -> dict[str, str]:
    """Map each research/*.json named by a module-level REPORT* constant to the theorem file naming it."""
    found: dict[str, str] = {}
    for module in sorted((root / "theorems").rglob("*.py")):
        try:
            lines = module.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for index, line in enumerate(lines):
            if not REPORT_CONSTANT.match(line):
                continue
            chunk, depth = [], 0
            for follow in lines[index:index + 6]:
                chunk.append(follow)
                depth += follow.count("(") - follow.count(")")
                if depth <= 0:
                    break
            match = JSON_LITERAL.search("\n".join(chunk))
            if match:
                found.setdefault(match.group(1), module.relative_to(root).as_posix())
    return found


def report_write_events(root: Path) -> list[dict]:
    events = []
    for rel, theorem in sorted(report_paths(root).items()):
        path = root / rel
        if path.is_file():
            events.append({
                "kind": "report_write",
                "timestamp": to_utc_iso(path.stat().st_mtime),
                "path": rel,
                "theorem": theorem,
                "source": "mtime",
            })
    return events


def build_events(root: Path) -> list[dict]:
    history_path = root / HISTORY
    history = read_json(history_path) if history_path.exists() else []
    return [
        *experiment_run_events(history if isinstance(history, list) else []),
        *theorem_commit_events(root),
        *_registry_events(root),
        *report_write_events(root),
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--out", type=Path, help=f"Ledger path (default: ROOT/{LEDGER}).")
    args = parser.parse_args(argv)

    out = args.out or args.root / LEDGER
    events = build_events(args.root)
    kept = replace_kinds(out, DERIVED_KINDS, events)
    print(json.dumps({"ledger": str(out), "kept_lines": kept, "derived": dict(Counter(e["kind"] for e in events))}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
