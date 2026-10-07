"""Build the small data files the public website reads from site/data/.

Run from the repository root:
    python tools/build_site_data.py
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TAG_MIN_COUNT = 20
POLICY_PREFIXES = ("PO-", "NO-")
TAG_LABELS = {
    "CODE-COSET-COLLECTIVE": "Codes and cosets",
    "DHS-GOWERS-SIEVE": "Dihedral sieve",
    "HYP-LIT-HIDDEN-SHIFT-SIEVE": "Hidden shift, from the literature",
    "HYP-LIT-COSET-OBSERVABLES": "Coset observables, from the literature",
}


def week_start(timestamp: str) -> str:
    """Return the Monday of the timestamp's date as YYYY-MM-DD."""
    day = datetime.fromisoformat(timestamp.replace("Z", "+00:00")).date()
    return (day - timedelta(days=day.weekday())).isoformat()


def weekly_runs(runs: list[dict[str, Any]]) -> dict[str, Any]:
    """Count experiment runs per ISO week, filling empty weeks with zero."""
    counts = Counter(week_start(run["recorded_at"]) for run in runs if run.get("recorded_at"))
    if not counts:
        return {"total_runs": 0, "weeks": []}
    cursor = date.fromisoformat(min(counts))
    last = date.fromisoformat(max(counts))
    weeks = []
    while cursor <= last:
        key = cursor.isoformat()
        weeks.append({"week": key, "runs": counts.get(key, 0)})
        cursor += timedelta(days=7)
    return {"total_runs": sum(counts.values()), "weeks": weeks}


def repo_path(value: Any, root: Path) -> str | None:
    """Return value when it names an existing file in the repository."""
    if not isinstance(value, str) or not value:
        return None
    looks_like_path = "/" in value or value.endswith((".py", ".json", ".md"))
    return value if looks_like_path and (root / value).is_file() else None


def is_filter_tag(tag: Any) -> bool:
    """Candidate-style IDs (DHS-GOWERS-SIEVE) qualify; policy tags and free text do not."""
    return (
        isinstance(tag, str)
        and tag == tag.upper()
        and " " not in tag
        and any(ch.isalpha() for ch in tag)
        and not tag.startswith(POLICY_PREFIXES)
    )


def slim_negatives(
    records: list[dict[str, Any]], root: Path, min_tag_count: int = TAG_MIN_COUNT
) -> dict[str, Any]:
    """Reduce the negative-result registry to the fields the website shows."""
    tag_counts = Counter(
        tag for record in records for tag in record.get("applies_to", []) if is_filter_tag(tag)
    )
    tags = [
        {"id": tag, "label": TAG_LABELS.get(tag, tag), "count": count}
        for tag, count in sorted(tag_counts.items(), key=lambda item: (-item[1], item[0]))
        if count >= min_tag_count
    ]
    slim = []
    for record in sorted(records, key=lambda item: item["id"]):
        evidence = record.get("evidence") if isinstance(record.get("evidence"), dict) else {}
        slim.append(
            {
                "id": record["id"],
                "claim": record.get("claim", ""),
                "reason": record.get("reason_invalid", ""),
                "lesson": record.get("lesson", ""),
                "tags": [tag for tag in record.get("applies_to", []) if is_filter_tag(tag)],
                "source": record.get("source", ""),
                "source_path": repo_path(record.get("source"), root),
                "derivation_path": repo_path(evidence.get("derivation"), root),
                "artifact_path": repo_path(evidence.get("artifact"), root),
                "review_status": evidence.get("status", ""),
            }
        )
    return {"count": len(slim), "tags": tags, "records": slim}


def write_json(path: Path, payload: Any, *, compact: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if compact:
        text = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    else:
        text = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
    path.write_text(text + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository root.")
    args = parser.parse_args(argv)
    root = args.root
    out = root / "site" / "data"

    runs = read_json(root / "research" / "experiment_run_history.json")
    write_json(out / "activity.json", weekly_runs(runs))

    negatives = read_json(root / "research" / "registry" / "negative_results.json")
    write_json(out / "negatives.json", slim_negatives(negatives, root), compact=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
