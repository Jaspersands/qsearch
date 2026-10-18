"""Spend report: negatives per day, runs per day and cost per retained negative, from the ledger.

    python tools/spend/report.py
    python tools/spend/report.py --root DIR --ledger FILE

Outputs research/audits/SPEND_REPORT.md and research/audits/spend_summary.json. The
summary's shape is fixed because the cockpit reads it:

    {"generated_on": "YYYY-MM-DD",
     "days": [{"date", "runs", "wall_seconds", "cpu_seconds", "negatives_added", "tokens"}]}

Days are UTC calendar days. wall_seconds and cpu_seconds come from timed runs only: a day
without one has wall_seconds 0.0 and cpu_seconds null. tokens is null on days with no
token record.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.spend.common import LEDGER, day_of, read_ledger  # noqa: E402

ACTIVITY_KINDS = {"experiment_run", "timed_run", "theorem_commit", "registry_commit", "registry_uncommitted", "token_day"}
SUMMARY_FIELDS = ("date", "runs", "wall_seconds", "cpu_seconds", "negatives_added", "tokens")
CLUSTER_SHARE = 0.5


def _matched_timed_runs(events: list[dict]) -> set[int]:
    """Timed runs whose window contains an experiment_run: the same run, counted once."""
    runs = sorted(e["timestamp"] for e in events if e.get("kind") == "experiment_run")
    matched = set()
    for index, event in enumerate(events):
        if event.get("kind") != "timed_run":
            continue
        start, end = event["timestamp"], event.get("ended_at") or event["timestamp"]
        if any(start <= stamp <= end for stamp in runs):
            matched.add(index)
    return matched


def _uncached(event: dict) -> int:
    return int(event.get("input_tokens") or 0) - int(event.get("cached_input_tokens") or 0) + int(event.get("output_tokens") or 0)


def daily_rows(events: list[dict]) -> list[dict]:
    matched = _matched_timed_runs(events)
    days: dict[str, dict] = defaultdict(lambda: {
        "experiment_runs": 0, "timed_runs": 0, "matched": 0, "wall": 0.0, "cpu": None,
        "negatives": 0, "theorems": 0, "tokens": None, "uncached": None, "written": 0,
    })
    for index, event in enumerate(events):
        kind = event.get("kind")
        if kind not in ACTIVITY_KINDS:
            continue
        day = days[event.get("date") or day_of(event["timestamp"])]
        if kind == "experiment_run":
            day["experiment_runs"] += 1
            day["written"] += event.get("negatives_written") or 0
        elif kind == "timed_run":
            day["timed_runs"] += 1
            day["matched"] += index in matched
            day["wall"] += float(event.get("wall_seconds") or 0.0)
            if event.get("cpu_seconds") is not None:
                day["cpu"] = (day["cpu"] or 0.0) + float(event["cpu_seconds"])
        elif kind in {"registry_commit", "registry_uncommitted"}:
            day["negatives"] += int(event.get("negatives_new_retained") or 0)
        elif kind == "theorem_commit":
            day["theorems"] += event.get("change") == "A"
        elif kind == "token_day":
            day["tokens"] = (day["tokens"] or 0) + int(event.get("total_tokens") or 0)
            day["uncached"] = (day["uncached"] or 0) + _uncached(event)
    rows = []
    for date in sorted(days):
        day = days[date]
        rows.append({
            "date": date,
            "runs": day["experiment_runs"] + day["timed_runs"] - day["matched"],
            "experiment_runs": day["experiment_runs"],
            "timed_runs": day["timed_runs"],
            "wall_seconds": round(day["wall"], 3),
            "cpu_seconds": None if day["cpu"] is None else round(day["cpu"], 3),
            "negatives_added": day["negatives"],
            "theorems_added": day["theorems"],
            "tokens": day["tokens"],
            "tokens_uncached": day["uncached"],
            "negatives_written": day["written"],
        })
    return rows


def summarize(rows: list[dict], generated_on: str) -> dict:
    return {"generated_on": generated_on, "days": [{field: row[field] for field in SUMMARY_FIELDS} for row in rows]}


def _ratio(part: float, whole: float) -> float | None:
    return part / whole if whole else None


def costs(rows: list[dict], events: list[dict]) -> dict:
    token_rows = [row for row in rows if row["tokens"] is not None]
    token_negatives = sum(row["negatives_added"] for row in token_rows)
    tokens = sum(row["tokens"] for row in token_rows)
    uncached = sum(row["tokens_uncached"] or 0 for row in token_rows)
    timed = [event for event in events if event.get("kind") == "timed_run"]
    timed_negatives = sum(event.get("negatives_added") or 0 for event in timed)
    wall = sum(float(event.get("wall_seconds") or 0.0) for event in timed)
    cpu = sum(float(event.get("cpu_seconds") or 0.0) for event in timed)
    runs = sum(row["runs"] for row in rows)
    negatives = sum(row["negatives_added"] for row in rows)
    return {
        "runs": runs,
        "negatives": negatives,
        "runs_per_negative": _ratio(runs, negatives),
        "negatives_written_by_runs": sum(row["negatives_written"] for row in rows),
        "token_days": len(token_rows),
        "first_token_day": token_rows[0]["date"] if token_rows else None,
        "last_token_day": token_rows[-1]["date"] if token_rows else None,
        "tokens": tokens,
        "tokens_uncached": uncached,
        "token_negatives": token_negatives,
        "tokens_per_negative": _ratio(tokens, token_negatives),
        "uncached_tokens_per_negative": _ratio(uncached, token_negatives),
        "timed_runs": len(timed),
        "timed_wall_seconds": wall,
        "timed_cpu_seconds": cpu,
        "timed_negatives": timed_negatives,
        "timed_wall_per_negative": _ratio(wall, timed_negatives),
        "timed_cpu_per_negative": _ratio(cpu, timed_negatives),
    }


def mtime_check(events: list[dict]) -> dict:
    """Share of report-file mtimes in the busiest hour; a large share means checkout time, not write time."""
    hours = Counter(event["timestamp"][:13] for event in events if event.get("kind") == "report_write")
    total = sum(hours.values())
    if not total:
        return {"files": 0, "modal_hour": None, "modal_share": None, "clustered": False}
    hour, count = hours.most_common(1)[0]
    share = round(count / total, 4)
    return {"files": total, "modal_hour": hour, "modal_share": share, "clustered": share >= CLUSTER_SHARE}


def backfills(events: list[dict]) -> tuple[str, str]:
    """The first registry commit and the first theorem commit hold everything made before them."""
    commits = sorted((e for e in events if e.get("kind") == "registry_commit"), key=lambda e: e["timestamp"])
    theorems = [e for e in events if e.get("kind") == "theorem_commit" and e.get("change") == "A"]
    registry_note = theorem_note = ""
    if commits:
        first = commits[0]
        registry_note = (f"The first registry commit ({day_of(first['timestamp'])}) holds "
                         f"{first['negatives_new_retained']:,} retained negatives made at any point up to then.")
    if theorems:
        first_sha = min(theorems, key=lambda e: e["timestamp"]).get("sha")
        first_day = day_of(min(e["timestamp"] for e in theorems))
        added = sum(1 for e in theorems if e.get("sha") == first_sha)
        theorem_note = f"The first theorem commit ({first_day}) adds {added:,} theorem files at once."
    return registry_note, theorem_note


def _num(value: float | int | None, digits: int = 0) -> str:
    if value is None:
        return "-"
    return f"{value:,.{digits}f}"


def render(rows: list[dict], events: list[dict], generated_on: str) -> str:
    cost = costs(rows, events)
    active = [row for row in rows if row["negatives_added"]]
    busiest = max(active, key=lambda row: row["negatives_added"]) if active else None
    span = f"{rows[0]['date']} to {rows[-1]['date']}" if rows else "none"
    timed_note = (
        "n/a: no timed run has added a negative yet"
        if cost["timed_wall_per_negative"] is None
        else f"{_num(cost['timed_wall_per_negative'], 1)} s wall, {_num(cost['timed_cpu_per_negative'], 1)} s CPU"
    )
    lines = [
        "# Spend Report",
        "",
        f"Generated {generated_on} by `tools/spend/report.py` from `{LEDGER.as_posix()}`; do not edit by hand.",
        "Days are UTC calendar days. See `tools/spend/README.md` for what each source can and cannot tell you.",
        "",
        "## Headline",
        "",
        "| Measure | Value |",
        "|---|---|",
        f"| Days with recorded activity | {len(rows)} ({span}) |",
        f"| Runs | {cost['runs']:,} |",
        f"| Retained negatives added | {cost['negatives']:,} on {len(active)} days"
        + (f" (most: {busiest['negatives_added']:,} on {busiest['date']})" if busiest else "") + " |",
        f"| Runs per retained negative | {_num(cost['runs_per_negative'], 2)} |",
        f"| Codex tokens | {cost['tokens']:,} on {cost['token_days']} days"
        + (f" ({cost['first_token_day']} to {cost['last_token_day']})" if cost["token_days"] else "") + " |",
        f"| Codex tokens per retained negative | {_num(cost['tokens_per_negative'])} "
        f"({cost['token_negatives']:,} negatives on days with token records) |",
        f"| Uncached Codex tokens per retained negative | {_num(cost['uncached_tokens_per_negative'])} |",
        f"| Timed runs | {cost['timed_runs']} ({_num(cost['timed_wall_seconds'], 1)} s wall, "
        f"{_num(cost['timed_cpu_seconds'], 1)} s CPU) |",
        f"| Measured time per retained negative | {timed_note} |",
        "",
        "## What the numbers mean",
        "",
        "- **Runs** are the experiment runs in `research/experiment_run_history.json`, plus timed runs that did not",
        "  log an experiment run inside their own time window. The history has one timestamp per run and no",
        "  durations.",
        "- **Retained negatives** are records still in `research/registry/negative_results.json`, dated by the",
        "  first commit that contains them. That is the commit day, not the day the work was done. Ids not yet",
        "  committed are dated by the registry file's mtime.",
        "- **Back-fills.** The first commit of a file holds everything made before it, so the busiest days",
        "  are partly history. " + " ".join(note for note in backfills(events) if note),
        f"- The run history's own `negative_results_written` metric sums to {cost['negatives_written_by_runs']:,}."
        " Only some runs set it, so it undercounts.",
        "- **Wall and CPU seconds** come only from runs made through `tools/spend/timed.py`. Days before the",
        "  wrapper was used show 0.0 wall seconds and no CPU time: unmeasured, not free.",
        "- **Codex tokens** come from Codex session logs whose working directory is this repo, summed per day.",
        "  The total includes cached input tokens, which dominate; the uncached figure is input minus cached",
        "  input plus output. The Gemini agents are not counted because their logs hold no labelled token",
        "  counts, so tokens per negative is a lower bound for the whole loop.",
        "",
        "## Per day",
        "",
        "| Date | Runs | Timed runs | Retained negatives | Theorem files added | Wall s | CPU s | Codex tokens |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        wall = _num(row["wall_seconds"], 1) if row["timed_runs"] else "-"
        lines.append(
            f"| {row['date']} | {row['runs']} | {row['timed_runs']} | {row['negatives_added']} | {row['theorems_added']} "
            f"| {wall} | {_num(row['cpu_seconds'], 1)} | {_num(row['tokens'])} |"
        )
    check = mtime_check(events)
    lines += ["", "## Report-file mtimes", ""]
    if not check["files"]:
        lines.append("No report files were found.")
    elif check["clustered"]:
        lines.append(
            f"{check['files']:,} report files; {100 * check['modal_share']:.0f}% have an mtime in the hour starting "
            f"{check['modal_hour']}:00 UTC. A fresh checkout or worktree sets mtimes like this, so here they are "
            "checkout times, not write times. They are kept in the ledger but not used above."
        )
    else:
        lines.append(
            f"{check['files']:,} report files; the busiest hour holds {100 * check['modal_share']:.0f}% of mtimes. "
            "An mtime is the last write, not the first, and is not used above."
        )
    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--ledger", type=Path, help=f"Ledger path (default: ROOT/{LEDGER}).")
    args = parser.parse_args(argv)

    events = read_ledger(args.ledger or args.root / LEDGER)
    rows = daily_rows(events)
    today = dt.date.today().isoformat()
    audits = args.root / "research" / "audits"
    audits.mkdir(parents=True, exist_ok=True)
    (audits / "spend_summary.json").write_text(json.dumps(summarize(rows, today), indent=1) + "\n", encoding="utf-8")
    (audits / "SPEND_REPORT.md").write_text(render(rows, events, today), encoding="utf-8")
    cost = costs(rows, events)
    print(json.dumps({key: cost[key] for key in ("runs", "negatives", "runs_per_negative", "tokens", "tokens_per_negative",
                                                  "timed_runs")}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
