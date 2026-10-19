"""Spend report: negatives per day, runs per day and cost per retained negative, from the ledger.

    python tools/spend/report.py
    python tools/spend/report.py --root DIR --ledger FILE

Outputs research/audits/SPEND_REPORT.md and research/audits/spend_summary.json. The
summary's shape is fixed because the cockpit reads it:

    {"generated_on": "YYYY-MM-DD",
     "days": [{"date", "runs", "wall_seconds", "cpu_seconds", "negatives_added", "tokens"}]}

Days are UTC calendar days, and generated_on is the UTC date too. runs counts experiment
runs (the run history); commands timed with timed.py are counted apart, as timed commands,
because any command can be timed. wall_seconds and cpu_seconds come from timed commands
only: a day without one has wall_seconds 0.0 and cpu_seconds null. tokens is null on days
with no token record.
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


def _uncached(event: dict) -> int:
    return int(event.get("input_tokens") or 0) - int(event.get("cached_input_tokens") or 0) + int(event.get("output_tokens") or 0)


def utc_today() -> str:
    return dt.datetime.now(dt.timezone.utc).date().isoformat()


def daily_rows(events: list[dict]) -> list[dict]:
    days: dict[str, dict] = defaultdict(lambda: {
        "experiment_runs": 0, "timed_runs": 0, "wall": 0.0, "cpu": None,
        "negatives": 0, "theorems": 0, "tokens": None, "uncached": None, "written": 0,
    })
    for event in events:
        kind = event.get("kind")
        if kind not in ACTIVITY_KINDS:
            continue
        day = days[event.get("date") or day_of(event["timestamp"])]
        if kind == "experiment_run":
            day["experiment_runs"] += 1
            day["written"] += event.get("negatives_written") or 0
        elif kind == "timed_run":
            day["timed_runs"] += 1
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
            "runs": day["experiment_runs"],
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
    """Totals and ratios for the headline.

    tokens_per_negative divides every Codex token in the ledger by every retained negative dated
    from the first to the last day with a token record, days without a token record included.
    timed_registry_growth is the raw change in the negatives registry's record count while timed
    commands ran, from any writer; it is not a count of retained negatives.
    """
    token_rows = [row for row in rows if row["tokens"] is not None]
    first_token_day = token_rows[0]["date"] if token_rows else None
    last_token_day = token_rows[-1]["date"] if token_rows else None
    token_negatives = sum(row["negatives_added"] for row in rows
                          if token_rows and first_token_day <= row["date"] <= last_token_day)
    tokens = sum(row["tokens"] for row in token_rows)
    uncached = sum(row["tokens_uncached"] or 0 for row in token_rows)
    timed = [event for event in events if event.get("kind") == "timed_run"]
    growth = sum(event.get("negatives_added") or 0 for event in timed)
    wall = sum(float(event.get("wall_seconds") or 0.0) for event in timed)
    cpu = sum(float(event.get("cpu_seconds") or 0.0) for event in timed)
    runs = sum(row["runs"] for row in rows)
    negatives = sum(row["negatives_added"] for row in rows)
    return {
        "runs": runs,
        "experiment_runs": runs,
        "negatives": negatives,
        "runs_per_negative": _ratio(runs, negatives),
        "negatives_written_by_runs": sum(row["negatives_written"] for row in rows),
        "token_days": len(token_rows),
        "first_token_day": first_token_day,
        "last_token_day": last_token_day,
        "tokens": tokens,
        "tokens_uncached": uncached,
        "token_negatives": token_negatives,
        "tokens_per_negative": _ratio(tokens, token_negatives),
        "uncached_tokens_per_negative": _ratio(uncached, token_negatives),
        "timed_runs": len(timed),
        "timed_wall_seconds": wall,
        "timed_cpu_seconds": cpu,
        "timed_registry_growth": growth,
        "timed_wall_per_registry_record": _ratio(wall, growth),
        "timed_cpu_per_registry_record": _ratio(cpu, growth),
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
        "n/a: the negatives registry did not grow during any timed command"
        if cost["timed_wall_per_registry_record"] is None
        else f"{_num(cost['timed_wall_per_registry_record'], 1)} s wall, "
             f"{_num(cost['timed_cpu_per_registry_record'], 1)} s CPU per record"
    )
    window = (f"all {cost['token_negatives']:,} retained negatives dated {cost['first_token_day']} to "
              f"{cost['last_token_day']}" if cost["token_days"] else "no token records")
    if cost["token_days"] and cost["token_negatives"] != cost["negatives"]:
        window = window.replace("all ", "", 1)
    lines = [
        "# Spend Report",
        "",
        f"Generated {generated_on} (UTC) by `tools/spend/report.py` from `{LEDGER.as_posix()}`; do not edit by hand.",
        "Days are UTC calendar days. See `tools/spend/README.md` for what each source can and cannot tell you.",
        "",
        "## Headline",
        "",
        "| Measure | Value |",
        "|---|---|",
        f"| Days with recorded activity | {len(rows)} ({span}) |",
        f"| Experiment runs | {cost['experiment_runs']:,} |",
        f"| Timed commands | {cost['timed_runs']:,} ({_num(cost['timed_wall_seconds'], 1)} s wall, "
        f"{_num(cost['timed_cpu_seconds'], 1)} s CPU) |",
        f"| Retained negatives added | {cost['negatives']:,} on {len(active)} days"
        + (f" (most: {busiest['negatives_added']:,} on {busiest['date']})" if busiest else "") + " |",
        f"| Experiment runs per retained negative | {_num(cost['runs_per_negative'], 2)} |",
        f"| Codex tokens | {cost['tokens']:,} on {cost['token_days']} days"
        + (f" ({cost['first_token_day']} to {cost['last_token_day']})" if cost["token_days"] else "") + " |",
        f"| Codex tokens per retained negative | {_num(cost['tokens_per_negative'])} (Codex only; {window}) |",
        f"| Uncached Codex tokens per retained negative | {_num(cost['uncached_tokens_per_negative'])} |",
        f"| Timed seconds per negatives-registry record added during timed commands | {timed_note} |",
        "",
        "## What the numbers mean",
        "",
        "- **Experiment runs** are the runs in `research/experiment_run_history.json`. The history has one",
        "  timestamp per run and no durations.",
        "- **Timed commands** are commands run through `tools/spend/timed.py`. Any command can be timed (for",
        "  example `qsearch.py validate`), so they are counted apart from experiment runs; an experiment run",
        "  made through the wrapper is in both counts.",
        "- **Retained negatives** are records still in `research/registry/negative_results.json`, dated by the",
        "  first commit that contains them. That is the commit day, not the day the work was done. Ids not yet",
        "  committed are dated by the registry file's mtime.",
        "- **Back-fills.** The first commit of a file holds everything made before it, so the busiest days",
        "  are partly history. " + " ".join(note for note in backfills(events) if note),
        f"- The run history's own `negative_results_written` metric sums to {cost['negatives_written_by_runs']:,}."
        " Only some runs set it, so it undercounts.",
        "- **Wall and CPU seconds** come only from commands run through `tools/spend/timed.py`. Days before the",
        "  wrapper was used show 0.0 wall seconds and no CPU time: unmeasured, not free.",
        "- **Timed seconds per negatives-registry record** divides timed seconds by the raw change in the",
        "  record count of `research/registry/negative_results.json` while timed commands ran. Any writer counts,",
        "  other agents included, and a record added then can be removed later, so it is not a cost per",
        "  retained negative.",
        "- **Codex tokens** come from Codex session logs whose working directory is this repo, summed per day.",
        "  A forked session's copy of its parent's history is counted once, under the parent. The total",
        "  includes cached input tokens, which dominate; the uncached figure is input minus cached input plus",
        "  output.",
        "- **Codex tokens per retained negative** divides every Codex token in the ledger by every retained",
        "  negative dated from the first to the last day with a Codex token record, days without a token record",
        "  included. It is Codex only: the Gemini agents' tokens are missing, because their logs hold no labelled",
        "  token counts, and nothing here measures how large the missing part is.",
        "",
        "## Per day",
        "",
        "| Date | Experiment runs | Timed commands | Retained negatives | Theorem files added | Wall s | CPU s | Codex tokens |",
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
    today = utc_today()
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
