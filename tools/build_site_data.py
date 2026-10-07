"""Build the small data files the public website reads from site/data/.

Run from the repository root:
    python tools/build_site_data.py
"""

from __future__ import annotations

import argparse
import json
import subprocess
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_PATH = "research/progress_snapshot.json"
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


def _git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=root, check=True, capture_output=True, text=True
    ).stdout.strip()


def snapshot_versions(root: Path) -> list[dict[str, Any]]:
    """Every committed version of the progress snapshot, oldest first, dated by updated_at when present."""
    log = _git(root, "log", "--format=%H %cs", "--", SNAPSHOT_PATH)
    versions = []
    for line in reversed(log.splitlines()):
        commit, day = line.split()
        shown = subprocess.run(
            ["git", "show", f"{commit}:{SNAPSHOT_PATH}"],
            cwd=root, capture_output=True, text=True,
        )
        if shown.returncode != 0:
            continue
        try:
            snapshot = json.loads(shown.stdout)
        except json.JSONDecodeError:
            continue
        # Prefer the snapshot's own data date so the site shows one date per snapshot.
        updated = snapshot.get("updated_at")
        version_date = updated[:10] if isinstance(updated, str) and len(updated) >= 10 else day
        versions.append({"commit": commit[:8], "date": version_date, "snapshot": snapshot})
    return versions


def latest_per_date(versions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_date: dict[str, dict[str, Any]] = {}
    for version in versions:
        by_date[version["date"]] = version
    return [by_date[day] for day in sorted(by_date)]


def track_states(snapshot: dict[str, Any]) -> dict[str, str]:
    return {
        (track.get("short_title") or track.get("title", "")): track.get("status", "")
        for track in snapshot.get("tracks", [])
    }


def describe_changes(previous: dict[str, Any] | None, current: dict[str, Any]) -> list[str]:
    """Plain-language list of what changed between two snapshots."""
    if previous is None:
        return ["First public snapshot."]
    changes = []
    old_verdict = previous.get("verdict", {}).get("title", "")
    new_verdict = current.get("verdict", {}).get("title", "")
    if old_verdict != new_verdict:
        changes.append(f'Verdict changed from "{old_verdict}" to "{new_verdict}".')
    old_tracks, new_tracks = track_states(previous), track_states(current)
    for name, status in new_tracks.items():
        if name not in old_tracks:
            changes.append(f"{name} track added: {status}.")
        elif old_tracks[name] != status:
            changes.append(f"{name}: {status} (was: {old_tracks[name]}).")
    for name in old_tracks:
        if name not in new_tracks:
            changes.append(f"{name} track removed.")
    old_count = previous.get("metrics", {}).get("negative_results", 0)
    new_count = current.get("metrics", {}).get("negative_results", 0)
    if new_count > old_count:
        delta = new_count - old_count
        noun = "idea" if delta == 1 else "ideas"
        changes.append(f"{delta:,} more {noun} ruled out ({new_count:,} in total).")
    return changes


def build_changelog(versions: list[dict[str, Any]]) -> dict[str, Any]:
    points, entries = [], []
    previous = None
    for version in latest_per_date(versions):
        current = version["snapshot"]
        metrics = current.get("metrics", {})
        points.append(
            {
                "date": version["date"],
                "negative_results": metrics.get("negative_results", 0),
                "experiments": metrics.get("experiments", 0),
            }
        )
        changes = describe_changes(previous, current)
        if changes:
            entries.append(
                {
                    "date": version["date"],
                    "commit": version["commit"],
                    "verdict": current.get("verdict", {}).get("title", ""),
                    "changes": changes,
                }
            )
        previous = current
    entries.reverse()
    return {"points": points, "entries": entries}


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
    parser.add_argument(
        "--skip-changelog",
        action="store_true",
        help="Leave changelog.json alone (it needs full git history, which CI does not have).",
    )
    args = parser.parse_args(argv)
    root = args.root
    out = root / "site" / "data"

    runs = read_json(root / "research" / "experiment_run_history.json")
    write_json(out / "activity.json", weekly_runs(runs))

    negatives = read_json(root / "research" / "registry" / "negative_results.json")
    write_json(out / "negatives.json", slim_negatives(negatives, root), compact=True)
    if not args.skip_changelog:
        write_json(out / "changelog.json", build_changelog(snapshot_versions(root)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
