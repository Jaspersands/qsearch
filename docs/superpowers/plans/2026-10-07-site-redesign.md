# Q-Search Website Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the six-page "academic monograph" site with a four-page, white, plainly written site whose every number and chart comes from the research registries.

**Architecture:** Static HTML pages at the repo root, one hand-written stylesheet, and small vanilla ES modules under `site/js/`. Pure logic (formatting, filtering, chart SVG, grouping) lives in `site/js/lib/` and is unit-tested with `node --test`. A deterministic Python script (`tools/build_site_data.py`) derives small JSON files into `site/data/`. A static checker (`tools/check_site.py`) and a local Playwright smoke script (`tools/site_smoke.py`) verify the result.

**Tech Stack:** HTML, CSS, vanilla JavaScript ES modules, Python 3 (stdlib only for the build/check scripts), unittest/pytest, `node:test`, Playwright (local only), GitHub Pages, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-10-07-site-redesign-design.md`

## Global Constraints

- Local Python: `/opt/anaconda3/bin/python3` (3.13, has pytest and Playwright). Code must also run on Python 3.9+ (`from __future__ import annotations`) and on CI's 3.13. The build and check scripts use the standard library only.
- Local Node: `/Users/jaspersands/.nvm/versions/node/v24.18.0/bin/node`. The default `node` in some shells is v14, which has no `node:test`. CI uses Node 22.
- The repo path contains spaces: always quote it (`cd "/Users/jaspersands/Desktop/quantum algorithm search"`).
- Work on branch `site-redesign`. Commit after every task. Commit messages end with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- No framework, no bundler, no npm dependencies. KaTeX is not used (no page shows typeset math after the simulated widgets are removed).
- GitHub base URL: `https://github.com/Jaspersands/qsearch` (file links use `/blob/main/<path>`, folders `/tree/main/<path>`).
- Anti-slop rules (hard constraints, from the spec):
  1. No eyebrow labels above headings. No all-caps monospace micro-labels.
  2. No grids of identical icon/number/title/tag cards.
  3. No pills or badges except the single status marker (rule 8).
  4. No shadows, gradients, glows, pulses, holographic effects, drop caps, or fake terminal chrome.
  5. Rounded containers only where a control needs one (inputs, buttons). Structure comes from type, whitespace, and hairline rules.
  6. Copy is plain and first-person plural. Banned words: monograph, protocol APG, rigorous, first-class, certified, peer-verifiable, deterministic audit, executive abstract, laboratory.
  7. Every number on the page comes from data, carries a date, and links to its source file.
  8. Status vocabulary is exactly three terms — **open**, **ruled out**, **active** — rendered as a small colored dot plus plain text, identical on every page.
- Copy mechanics: sentence case for headings, buttons, and labels; no exclamation marks; no "successfully", "simply", "just", "leverage", "seamless".
- Tokens: page `#ffffff`, text `#111111`, secondary `#555555`, muted `#767676`, hairline `#e6e6e6`, accent `#c2410c` (status and verdict only). Fonts: Schibsted Grotesk (headings and UI), Source Serif 4 (long prose), JetBrains Mono (paths and commands only).
- Track tone mapping: snapshot `tone: "active"` → **active**; anything else → **open**. Negative results are **ruled out**; proof debts and frontiers are **open**.
- No metric value is written into HTML. Every count is filled from JSON at runtime.

## File Structure

| File | Responsibility |
| --- | --- |
| `tools/build_site_data.py` (create) | Derive `site/data/activity.json`, `negatives.json`, `changelog.json` from registries and git history |
| `tests/test_build_site_data.py` (create) | Unit tests for the build script |
| `tools/check_site.py` (create) | Static checks: referenced repo files exist, internal links resolve, no hardcoded metric values |
| `tests/test_check_site.py` (create) | Unit tests for the checker |
| `tools/site_smoke.py` (create) | Local Playwright run: overflow, console errors, leftover "Loading", redirects, screenshots |
| `site/package.json` (create) | Marks `site/` JavaScript as ES modules for Node |
| `site/js/lib/format.js` (create) | Escaping, number/date formatting, repo URLs, status markers, BibTeX |
| `site/js/lib/negatives.js` (create) | Search and tag filtering for negative results, hash parsing |
| `site/js/lib/debts.js` (create) | Grouping proof debts by type |
| `site/js/lib/chart.js` (create) | Activity chart as an SVG string |
| `tests/js/*.test.mjs` (create) | `node:test` tests for the four lib modules |
| `site/js/common.js` (create) | Fetch helper, load-error message, copy buttons, footer date |
| `site/js/home.js`, `site/js/open-problems.js`, `site/js/negative-results.js` (create) | Page renderers |
| `site/styles.css` (rewrite) | The whole visual system |
| `index.html` (rewrite), `open-problems.html`, `negative-results.html` (rewrite), `how-it-works.html` (create) | The four pages |
| `methodology.html`, `repomap.html`, `frontier.html`, `proof-debt.html` (replace) | Redirect stubs |
| `site/progress.js` (delete) | Old monolithic script |
| `site/data/activity.json`, `negatives.json`, `changelog.json` (generated, committed) | Site data |
| `.github/workflows/validate.yml`, `_config.yml` (modify) | CI checks, Pages include list |

---

### Task 1: Site data builder — activity and negatives

**Files:**
- Create: `tools/build_site_data.py`
- Create: `tests/test_build_site_data.py`
- Create (generated): `site/data/activity.json`, `site/data/negatives.json`

**Interfaces:**
- Produces (Python, module `tools.build_site_data`):
  - `week_start(timestamp: str) -> str` — Monday of the timestamp's date, `YYYY-MM-DD`.
  - `weekly_runs(runs: list[dict]) -> dict` — `{"total_runs": int, "weeks": [{"week": "YYYY-MM-DD", "runs": int}, ...]}`, consecutive weeks, gaps filled with 0.
  - `repo_path(value, root: Path) -> str | None` — the value if it names an existing file in the repo, else `None`.
  - `slim_negatives(records: list[dict], root: Path, min_tag_count: int = 20) -> dict` — `{"count": int, "tags": [{"id", "label", "count"}], "records": [{"id", "claim", "reason", "lesson", "tags", "source", "source_path", "derivation_path", "artifact_path", "review_status"}]}`.
  - `write_json(path: Path, payload, *, compact: bool = False) -> None`
  - `main(argv: list[str] | None = None) -> int` with `--root PATH`.
- Produces (data files consumed by Tasks 6 and 8): `site/data/activity.json`, `site/data/negatives.json` with the shapes above.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_build_site_data.py`:

```python
import json
import tempfile
import unittest
from pathlib import Path

from tools.build_site_data import main, repo_path, slim_negatives, week_start, weekly_runs


def negative(record_id, tags, source="EXP-X", evidence=None):
    return {
        "id": record_id,
        "applies_to": tags,
        "claim": f"claim {record_id}",
        "reason_invalid": f"reason {record_id}",
        "lesson": f"lesson {record_id}",
        "source": source,
        "evidence": evidence or {},
    }


class WeeklyRunsTests(unittest.TestCase):
    def test_week_start_is_monday(self) -> None:
        self.assertEqual(week_start("2026-09-23T04:10:00+00:00"), "2026-09-21")
        self.assertEqual(week_start("2026-09-21T00:00:00Z"), "2026-09-21")

    def test_weekly_runs_counts_and_fills_gaps(self) -> None:
        runs = [
            {"recorded_at": "2026-07-07T10:00:00+00:00"},
            {"recorded_at": "2026-07-08T10:00:00+00:00"},
            {"recorded_at": "2026-07-22T10:00:00+00:00"},
            {"status": "no timestamp"},
        ]
        self.assertEqual(
            weekly_runs(runs),
            {
                "total_runs": 3,
                "weeks": [
                    {"week": "2026-07-06", "runs": 2},
                    {"week": "2026-07-13", "runs": 0},
                    {"week": "2026-07-20", "runs": 1},
                ],
            },
        )

    def test_weekly_runs_empty(self) -> None:
        self.assertEqual(weekly_runs([]), {"total_runs": 0, "weeks": []})


class NegativesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "research").mkdir()
        (self.root / "research" / "note.md").write_text("x")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_repo_path_only_returns_existing_files(self) -> None:
        self.assertEqual(repo_path("research/note.md", self.root), "research/note.md")
        self.assertIsNone(repo_path("research/missing.md", self.root))
        self.assertIsNone(repo_path("EXP-COSET-BINARY", self.root))
        self.assertIsNone(repo_path(None, self.root))

    def test_slim_negatives_keeps_display_fields_sorted_by_id(self) -> None:
        records = [
            negative(
                "B-ID",
                ["DHS-GOWERS-SIEVE"],
                source="research/note.md",
                evidence={
                    "derivation": "research/note.md",
                    "artifact": "research/gone.json",
                    "status": "derived-review-pending",
                },
            ),
            negative("A-ID", ["DHS-GOWERS-SIEVE", "PO-MEASUREMENT", "free text scope"]),
        ]
        payload = slim_negatives(records, self.root, min_tag_count=1)
        self.assertEqual(payload["count"], 2)
        self.assertEqual([r["id"] for r in payload["records"]], ["A-ID", "B-ID"])
        self.assertEqual(
            payload["records"][1],
            {
                "id": "B-ID",
                "claim": "claim B-ID",
                "reason": "reason B-ID",
                "lesson": "lesson B-ID",
                "tags": ["DHS-GOWERS-SIEVE"],
                "source": "research/note.md",
                "source_path": "research/note.md",
                "derivation_path": "research/note.md",
                "artifact_path": None,
                "review_status": "derived-review-pending",
            },
        )

    def test_filter_tags_skip_policy_tags_free_text_and_rare_tags(self) -> None:
        records = [
            negative("A", ["DHS-GOWERS-SIEVE", "PO-MEASUREMENT", "NO-TOY-ORACLE", "free text"]),
            negative("B", ["DHS-GOWERS-SIEVE", "RARE-TAG"]),
        ]
        payload = slim_negatives(records, self.root, min_tag_count=2)
        self.assertEqual(
            payload["tags"], [{"id": "DHS-GOWERS-SIEVE", "label": "Dihedral sieve", "count": 2}]
        )
        self.assertEqual(payload["records"][0]["tags"], ["DHS-GOWERS-SIEVE"])
        self.assertEqual(payload["records"][1]["tags"], ["DHS-GOWERS-SIEVE", "RARE-TAG"])


class MainTests(unittest.TestCase):
    def test_main_writes_activity_and_negatives(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "research" / "registry").mkdir(parents=True)
            (root / "research" / "experiment_run_history.json").write_text(
                json.dumps([{"recorded_at": "2026-07-07T10:00:00+00:00"}])
            )
            (root / "research" / "registry" / "negative_results.json").write_text(
                json.dumps([negative("A", ["DHS-GOWERS-SIEVE"])])
            )
            self.assertEqual(main(["--root", str(root)]), 0)
            activity = json.loads((root / "site" / "data" / "activity.json").read_text())
            self.assertEqual(activity["total_runs"], 1)
            negatives = json.loads((root / "site" / "data" / "negatives.json").read_text())
            self.assertEqual(negatives["count"], 1)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `cd "/Users/jaspersands/Desktop/quantum algorithm search" && /opt/anaconda3/bin/python3 -m pytest tests/test_build_site_data.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'tools.build_site_data'`.

- [ ] **Step 3: Write the implementation**

Create `tools/build_site_data.py`:

```python
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
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `cd "/Users/jaspersands/Desktop/quantum algorithm search" && /opt/anaconda3/bin/python3 -m pytest tests/test_build_site_data.py -q`
Expected: `7 passed`.

- [ ] **Step 5: Generate the real data and sanity-check it**

Run:
```bash
cd "/Users/jaspersands/Desktop/quantum algorithm search" && /opt/anaconda3/bin/python3 tools/build_site_data.py && ls -la site/data && /opt/anaconda3/bin/python3 -c "
import json
a=json.load(open('site/data/activity.json')); n=json.load(open('site/data/negatives.json'))
print('runs', a['total_runs'], 'weeks', len(a['weeks']), a['weeks'][0], a['weeks'][-1])
print('negatives', n['count'], n['tags'])"
```
Expected: `runs` equals the length of `research/experiment_run_history.json` (574 at time of writing), weeks start `2026-07-06`; `negatives` equals the registry length (934 at time of writing); tags list contains `CODE-COSET-COLLECTIVE`, `DHS-GOWERS-SIEVE`, `HYP-LIT-HIDDEN-SHIFT-SIEVE`, `HYP-LIT-COSET-OBSERVABLES`. `negatives.json` should be clearly smaller than `research/registry/negative_results.json` (2.3 MB). Run the script a second time and confirm `git diff --stat site/data` shows no change (determinism).

- [ ] **Step 6: Commit**

```bash
cd "/Users/jaspersands/Desktop/quantum algorithm search" && git add tools/build_site_data.py tests/test_build_site_data.py site/data/activity.json site/data/negatives.json && git commit -m "Add site data builder for weekly activity and slim negative results

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 2: Site data builder — changelog from git history

**Files:**
- Modify: `tools/build_site_data.py`
- Modify: `tests/test_build_site_data.py`
- Create (generated): `site/data/changelog.json`

**Interfaces:**
- Consumes: `write_json`, `read_json`, `main` from Task 1.
- Produces (Python):
  - `snapshot_versions(root: Path) -> list[dict]` — `[{"commit": "8-char sha", "date": "YYYY-MM-DD", "snapshot": dict}, ...]`, oldest first.
  - `latest_per_date(versions) -> list[dict]` — last version of each date, sorted by date.
  - `track_states(snapshot) -> dict[str, str]` — `{short_title: status}`.
  - `describe_changes(previous: dict | None, current: dict) -> list[str]`
  - `build_changelog(versions) -> dict` — `{"points": [{"date", "negative_results", "experiments"}], "entries": [{"date", "commit", "verdict", "changes": [str]}]}`; points oldest first, entries newest first.
  - `main` gains `--skip-changelog`.
- Produces (data file consumed by Task 6): `site/data/changelog.json`.

- [ ] **Step 1: Write the failing tests**

In `tests/test_build_site_data.py`, change the import line to:

```python
from tools.build_site_data import (
    build_changelog,
    describe_changes,
    main,
    repo_path,
    slim_negatives,
    snapshot_versions,
    week_start,
    weekly_runs,
)
```

Add `import os` and `import subprocess` to the imports at the top. In `MainTests.test_main_writes_activity_and_negatives`, change the call to `main(["--root", str(root), "--skip-changelog"])` and add after the negatives assertion:

```python
            self.assertFalse((root / "site" / "data" / "changelog.json").exists())
```

Append these test classes above the `if __name__ == "__main__":` line:

```python
def snapshot(verdict="No breakthrough yet", tracks=None, negatives=10, experiments=5):
    return {
        "verdict": {"title": verdict, "detail": "d"},
        "tracks": tracks if tracks is not None else [{"short_title": "DHSP", "status": "Blocked"}],
        "metrics": {"negative_results": negatives, "experiments": experiments},
    }


class ChangelogTests(unittest.TestCase):
    def test_first_snapshot(self) -> None:
        self.assertEqual(describe_changes(None, snapshot()), ["First public snapshot."])

    def test_no_change_gives_no_entries(self) -> None:
        self.assertEqual(describe_changes(snapshot(), snapshot()), [])

    def test_verdict_track_and_negative_changes(self) -> None:
        before = snapshot(tracks=[{"short_title": "DHSP", "status": "Blocked"}, {"short_title": "Old", "status": "x"}])
        after = snapshot(
            verdict="Speedup found",
            tracks=[{"short_title": "DHSP", "status": "Readout checked"}, {"short_title": "Codes", "status": "Closed"}],
            negatives=13,
        )
        self.assertEqual(
            describe_changes(before, after),
            [
                'Verdict changed from "No breakthrough yet" to "Speedup found".',
                "DHSP: Readout checked (was: Blocked).",
                "Codes track added: Closed.",
                "Old track removed.",
                "3 more ideas ruled out (13 in total).",
            ],
        )

    def test_single_new_negative_is_singular(self) -> None:
        self.assertEqual(
            describe_changes(snapshot(negatives=10), snapshot(negatives=11)),
            ["1 more idea ruled out (11 in total)."],
        )

    def test_build_changelog_keeps_last_version_per_date(self) -> None:
        versions = [
            {"commit": "aaaaaaaa", "date": "2026-07-17", "snapshot": snapshot(negatives=10)},
            {"commit": "bbbbbbbb", "date": "2026-07-17", "snapshot": snapshot(negatives=12)},
            {"commit": "cccccccc", "date": "2026-07-20", "snapshot": snapshot(negatives=15)},
        ]
        changelog = build_changelog(versions)
        self.assertEqual(
            changelog["points"],
            [
                {"date": "2026-07-17", "negative_results": 12, "experiments": 5},
                {"date": "2026-07-20", "negative_results": 15, "experiments": 5},
            ],
        )
        self.assertEqual([e["date"] for e in changelog["entries"]], ["2026-07-20", "2026-07-17"])
        self.assertEqual(changelog["entries"][0]["changes"], ["3 more ideas ruled out (15 in total)."])
        self.assertEqual(changelog["entries"][1]["commit"], "bbbbbbbb")


class SnapshotVersionsTests(unittest.TestCase):
    def git(self, root: Path, *args: str, when: str = "2026-07-17T12:00:00+00:00") -> None:
        env = dict(os.environ, GIT_AUTHOR_DATE=when, GIT_COMMITTER_DATE=when)
        subprocess.run(
            ["git", "-c", "user.name=Test", "-c", "user.email=test@example.com", "-c", "commit.gpgsign=false", *args],
            cwd=root, check=True, capture_output=True, env=env,
        )

    def test_reads_every_committed_version_oldest_first(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "research" / "progress_snapshot.json"
            path.parent.mkdir()
            self.git(root, "init", "-q")
            path.write_text(json.dumps(snapshot(negatives=1)))
            self.git(root, "add", ".")
            self.git(root, "commit", "-q", "-m", "one", when="2026-07-17T12:00:00+00:00")
            path.write_text(json.dumps(snapshot(negatives=2)))
            self.git(root, "commit", "-q", "-am", "two", when="2026-07-19T12:00:00+00:00")
            versions = snapshot_versions(root)
            self.assertEqual([v["date"] for v in versions], ["2026-07-17", "2026-07-19"])
            self.assertEqual([v["snapshot"]["metrics"]["negative_results"] for v in versions], [1, 2])
            self.assertEqual(len(versions[0]["commit"]), 8)

            (root / "research" / "experiment_run_history.json").write_text("[]")
            (root / "research" / "registry").mkdir()
            (root / "research" / "registry" / "negative_results.json").write_text("[]")
            self.assertEqual(main(["--root", str(root)]), 0)
            changelog = json.loads((root / "site" / "data" / "changelog.json").read_text())
            self.assertEqual(len(changelog["points"]), 2)
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `cd "/Users/jaspersands/Desktop/quantum algorithm search" && /opt/anaconda3/bin/python3 -m pytest tests/test_build_site_data.py -q`
Expected: FAIL — `ImportError: cannot import name 'build_changelog'`.

- [ ] **Step 3: Write the implementation**

In `tools/build_site_data.py`, add `import subprocess` to the imports, add `SNAPSHOT_PATH = "research/progress_snapshot.json"` below `ROOT`, and add these functions above `write_json`:

```python
def _git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=root, check=True, capture_output=True, text=True
    ).stdout.strip()


def snapshot_versions(root: Path) -> list[dict[str, Any]]:
    """Every committed version of the progress snapshot, oldest first."""
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
        versions.append({"commit": commit[:8], "date": day, "snapshot": snapshot})
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
```

In `main`, add the flag after the `--root` argument:

```python
    parser.add_argument(
        "--skip-changelog",
        action="store_true",
        help="Leave changelog.json alone (it needs full git history, which CI does not have).",
    )
```

and add before `return 0`:

```python
    if not args.skip_changelog:
        write_json(out / "changelog.json", build_changelog(snapshot_versions(root)))
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `cd "/Users/jaspersands/Desktop/quantum algorithm search" && /opt/anaconda3/bin/python3 -m pytest tests/test_build_site_data.py -q`
Expected: `13 passed`.

- [ ] **Step 5: Generate the real changelog and check it**

Run:
```bash
cd "/Users/jaspersands/Desktop/quantum algorithm search" && /opt/anaconda3/bin/python3 tools/build_site_data.py && /opt/anaconda3/bin/python3 -c "
import json
c=json.load(open('site/data/changelog.json'))
print(len(c['points']), 'points', c['points'][0], c['points'][-1])
for e in c['entries'][:4]: print(e['date'], e['changes'])
print('oldest:', c['entries'][-1])"
```
Expected: about 20 points starting `2026-07-17`; newest entries mention negative-result growth and any DHSP status change; oldest entry's changes are `["First public snapshot."]`. `git diff --stat site/data/activity.json site/data/negatives.json` shows no change.

- [ ] **Step 6: Commit**

```bash
cd "/Users/jaspersands/Desktop/quantum algorithm search" && git add tools/build_site_data.py tests/test_build_site_data.py site/data/changelog.json && git commit -m "Build a public changelog from the progress snapshot's git history

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 3: Verification tools — static checker and smoke script

**Files:**
- Create: `tools/check_site.py`
- Create: `tests/test_check_site.py`
- Create: `tools/site_smoke.py`

**Interfaces:**
- Produces (Python, module `tools.check_site`):
  - `site_files(root: Path) -> list[Path]` — root `*.html` plus `site/js/**/*.js`.
  - `missing_references(root: Path) -> list[str]` — problems for repo paths that don't exist and `href="x.html"` links that don't resolve.
  - `hardcoded_metrics(root: Path) -> list[str]` — problems for snapshot metric values ≥ 100 written literally in HTML.
  - `main(argv: list[str] | None = None) -> int` with `--root`; prints problems, returns 1 if any.
- Produces (CLI): `tools/site_smoke.py [--pages a.html,b.html] [--widths 1440,390] [--out DIR] [--no-redirects]` — exit 1 on any problem. Used for verification in Tasks 5–9.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_check_site.py`:

```python
import json
import tempfile
import unittest
from pathlib import Path

from tools.check_site import hardcoded_metrics, main, missing_references


class CheckSiteTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "research").mkdir()
        (self.root / "research" / "progress_snapshot.json").write_text(
            json.dumps({"metrics": {"experiments": 796, "negative_results": 1326, "proof_debts": 24}})
        )
        (self.root / "tests").mkdir()
        (self.root / "tests" / "test_real.py").write_text("")
        (self.root / "other.html").write_text("<p>ok</p>")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write_page(self, html: str) -> None:
        (self.root / "index.html").write_text(html)

    def test_existing_references_and_links_pass(self) -> None:
        self.write_page(
            '<code>tests/test_real.py</code> '
            '<a href="https://github.com/x/blob/main/research/progress_snapshot.json">s</a> '
            '<a href="other.html#top">o</a> <a href="https://example.com/page.html">e</a>'
        )
        self.assertEqual(missing_references(self.root), [])

    def test_missing_reference_is_reported(self) -> None:
        self.write_page('<a href="https://github.com/x/blob/main/tests/test_gone.py">t</a>')
        self.assertEqual(
            missing_references(self.root), ["index.html: references missing file tests/test_gone.py"]
        )

    def test_broken_internal_link_is_reported(self) -> None:
        self.write_page('<a href="missing.html">m</a>')
        self.assertEqual(missing_references(self.root), ["index.html: links to missing page missing.html"])

    def test_js_files_are_scanned(self) -> None:
        self.write_page("<p></p>")
        (self.root / "site" / "js").mkdir(parents=True)
        (self.root / "site" / "js" / "page.js").write_text('const DATA = "site/data/gone.json";')
        self.assertEqual(
            missing_references(self.root), ["site/js/page.js: references missing file site/data/gone.json"]
        )

    def test_hardcoded_metric_values_are_reported(self) -> None:
        self.write_page("<p>796 experiments, 1,326 negatives, 24 debts, 2026-07-96, 17960</p>")
        self.assertEqual(
            hardcoded_metrics(self.root),
            [
                "index.html: hardcodes the current metric value 796",
                "index.html: hardcodes the current metric value 1,326",
            ],
        )

    def test_main_returns_nonzero_on_problems(self) -> None:
        self.write_page('<a href="missing.html">m</a>')
        self.assertEqual(main(["--root", str(self.root)]), 1)
        self.write_page("<p>fine</p>")
        self.assertEqual(main(["--root", str(self.root)]), 0)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `cd "/Users/jaspersands/Desktop/quantum algorithm search" && /opt/anaconda3/bin/python3 -m pytest tests/test_check_site.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'tools.check_site'`.

- [ ] **Step 3: Write the implementation**

Create `tools/check_site.py`:

```python
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
```

Note on the test expectations: in `test_hardcoded_metric_values_are_reported`, `24` is below the floor, `2026-07-96` and `17960` are not standalone values, so only `796` and `1,326` are reported. The ordering is by metric value, then by form.

- [ ] **Step 4: Run the tests to verify they pass**

Run: `cd "/Users/jaspersands/Desktop/quantum algorithm search" && /opt/anaconda3/bin/python3 -m pytest tests/test_check_site.py -q`
Expected: `6 passed`.

- [ ] **Step 5: Run the checker against the current (old) site**

Run: `cd "/Users/jaspersands/Desktop/quantum algorithm search" && /opt/anaconda3/bin/python3 tools/check_site.py; echo "exit=$?"`
Expected: `exit=1`, listing at least `index.html: references missing file tests/test_dhs_sieve.py`, `tests/test_code_syzygy.py`, `tests/test_fourier_decay.py`, `tests/test_commutant.py`, `tests/test_commutant_splitting.py`. This confirms the checker catches the real problems the redesign removes. Do not fix the old pages; they are replaced in later tasks.

- [ ] **Step 6: Write the smoke script**

Create `tools/site_smoke.py`:

```python
"""Load the public pages in headless Chromium and check layout, errors, and redirects.

Local helper (needs Playwright, not used in CI):
    python tools/site_smoke.py --out /tmp/site-shots
"""

from __future__ import annotations

import argparse
import functools
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
PAGES = ["index.html", "open-problems.html", "negative-results.html", "how-it-works.html"]
REDIRECTS = {
    "methodology.html": "how-it-works.html",
    "repomap.html": "how-it-works.html",
    "frontier.html": "open-problems.html",
    "proof-debt.html": "open-problems.html",
}


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args: object) -> None:
        pass


def serve(root: Path) -> ThreadingHTTPServer:
    handler = functools.partial(QuietHandler, directory=str(root))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def check_page(browser, base: str, name: str, width: int, out: Path | None) -> list[str]:
    page = browser.new_page(viewport={"width": width, "height": 900})
    errors: list[str] = []
    page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
    page.on("pageerror", lambda exc: errors.append(str(exc)))
    page.goto(f"{base}/{name}", wait_until="networkidle")
    page.wait_for_timeout(400)
    problems = [f"{name} @{width}px: console error: {error}" for error in errors]
    if page.evaluate("document.documentElement.scrollWidth > window.innerWidth + 1"):
        problems.append(f"{name} @{width}px: horizontal overflow")
    if "Loading" in page.inner_text("body"):
        problems.append(f"{name} @{width}px: still shows a loading message")
    if out is not None:
        page.screenshot(path=str(out / f"{Path(name).stem}-{width}.png"), full_page=True)
    page.close()
    return problems


def check_redirect(browser, base: str, source: str, target: str) -> list[str]:
    page = browser.new_page()
    page.goto(f"{base}/{source}")
    try:
        page.wait_for_url(f"**/{target}*", timeout=5000)
        problems: list[str] = []
    except Exception:
        problems = [f"{source}: did not redirect to {target} (ended at {page.url})"]
    page.close()
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--pages", default=",".join(PAGES))
    parser.add_argument("--widths", default="1440,390")
    parser.add_argument("--out", type=Path, default=None, help="Directory for full-page screenshots.")
    parser.add_argument("--no-redirects", action="store_true")
    args = parser.parse_args(argv)
    if args.out is not None:
        args.out.mkdir(parents=True, exist_ok=True)

    server = serve(ROOT)
    base = f"http://127.0.0.1:{server.server_address[1]}"
    problems: list[str] = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        for name in [p for p in args.pages.split(",") if p]:
            for width in [int(w) for w in args.widths.split(",")]:
                problems += check_page(browser, base, name, width, args.out)
        if not args.no_redirects:
            for source, target in REDIRECTS.items():
                problems += check_redirect(browser, base, source, target)
        browser.close()
    server.shutdown()

    for problem in problems:
        print(problem)
    print("Smoke checks passed." if not problems else f"{len(problems)} problem(s).")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 7: Run the smoke script against the old homepage**

Run: `cd "/Users/jaspersands/Desktop/quantum algorithm search" && /opt/anaconda3/bin/python3 tools/site_smoke.py --pages index.html --no-redirects; echo "exit=$?"`
Expected: `exit=1` with `index.html @390px: horizontal overflow` (the old Falsifier cards overflow on phones). This proves the script detects the problem. If Chromium is missing, run `/opt/anaconda3/bin/python3 -m playwright install chromium` first.

- [ ] **Step 8: Commit**

```bash
cd "/Users/jaspersands/Desktop/quantum algorithm search" && git add tools/check_site.py tests/test_check_site.py tools/site_smoke.py && git commit -m "Add static site checker and local Playwright smoke script

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 4: Front-end logic modules with Node tests

**Files:**
- Create: `site/package.json`
- Create: `site/js/lib/format.js`, `site/js/lib/negatives.js`, `site/js/lib/debts.js`, `site/js/lib/chart.js`
- Create: `tests/js/format.test.mjs`, `tests/js/negatives.test.mjs`, `tests/js/debts.test.mjs`, `tests/js/chart.test.mjs`

**Interfaces:**
- Produces (ES module exports):
  - `format.js`: `REPO_URL: string`, `escapeHtml(value) -> string`, `formatNumber(value) -> string` (en-US grouping), `formatDate(isoDate) -> string` ("Sep 23, 2026"), `repoUrl(path) -> string`, `statusMarker(kind: "open"|"ruled-out"|"active") -> string` (HTML), `trackStatusKind(tone) -> "active"|"open"`, `humanizeId(id) -> string`, `bibtexEntry(snapshot) -> string`.
  - `negatives.js`: `matchesQuery(record, query) -> boolean`, `filterRecords(records, {query, tag}) -> record[]`, `recordIdFromHash(hash) -> string`.
  - `debts.js`: `groupDebts(debts) -> [{type, resolution: string|null, debts: debt[]}]` (groups ordered by highest priority; debts by priority desc then candidate id; `resolution` is `null` when the group's debts disagree).
  - `chart.js`: `niceMax(value) -> number`, `activityChart({weeks, points, width?, height?}) -> string` (SVG markup with classes `chart-bar`, `chart-line`, `chart-grid`, `chart-axis`, `chart-label`, `chart-label-strong`; `""` when `weeks` is empty).

- [ ] **Step 1: Write the failing tests**

Create `site/package.json`:

```json
{
  "private": true,
  "type": "module"
}
```

Create `tests/js/format.test.mjs`:

```js
import test from "node:test";
import assert from "node:assert/strict";
import {
  REPO_URL, bibtexEntry, escapeHtml, formatDate, formatNumber, humanizeId,
  repoUrl, statusMarker, trackStatusKind,
} from "../../site/js/lib/format.js";

test("escapeHtml escapes markup characters", () => {
  assert.equal(escapeHtml(`<a href="x">&'`), "&lt;a href=&quot;x&quot;&gt;&amp;&#39;");
  assert.equal(escapeHtml(null), "");
});

test("formatNumber groups thousands", () => {
  assert.equal(formatNumber(1326), "1,326");
  assert.equal(formatNumber(24), "24");
});

test("formatDate reads date-only and full timestamps the same", () => {
  assert.equal(formatDate("2026-09-23"), "Sep 23, 2026");
  assert.equal(formatDate("2026-09-23T04:10:00+00:00"), "Sep 23, 2026");
});

test("repoUrl encodes each path segment", () => {
  assert.equal(repoUrl("research/a b.json"), `${REPO_URL}/blob/main/research/a%20b.json`);
});

test("status markers use the three-word vocabulary", () => {
  assert.equal(statusMarker("ruled-out"), '<span class="status status-ruled-out">ruled out</span>');
  assert.equal(statusMarker("open"), '<span class="status status-open">open</span>');
  assert.equal(statusMarker("active"), '<span class="status status-active">active</span>');
  assert.equal(trackStatusKind("active"), "active");
  assert.equal(trackStatusKind("blocked"), "open");
});

test("humanizeId turns registry ids into sentence case", () => {
  assert.equal(humanizeId("code-equivalence-hard-family-search"), "Code equivalence hard family search");
});

test("bibtexEntry fills date and count from the snapshot", () => {
  const entry = bibtexEntry({ updated_at: "2026-09-23", metrics: { negative_results: 1934 } });
  assert.ok(entry.startsWith("@misc{sands2026qsearch,"));
  assert.ok(entry.includes("Snapshot of 2026-09-23; 1,934 negative results recorded"));
  assert.ok(entry.endsWith("}"));
});
```

Create `tests/js/negatives.test.mjs`:

```js
import test from "node:test";
import assert from "node:assert/strict";
import { filterRecords, matchesQuery, recordIdFromHash } from "../../site/js/lib/negatives.js";

const records = [
  { id: "GOPPA-SYZYGY", claim: "Goppa syzygies resist attacks", reason: "Hull projector", lesson: "", source: "x.py", tags: ["CODE-COSET-COLLECTIVE"] },
  { id: "SIEVE-DEPTH", claim: "Fixed depth lists work", reason: "Collapse at scale", lesson: "Use growing depth", source: "y.py", tags: ["DHS-GOWERS-SIEVE"] },
];

test("matchesQuery searches id, claim, reason, lesson, and source case-insensitively", () => {
  assert.equal(matchesQuery(records[0], "goppa"), true);
  assert.equal(matchesQuery(records[0], "HULL"), true);
  assert.equal(matchesQuery(records[1], "growing"), true);
  assert.equal(matchesQuery(records[1], "y.py"), true);
  assert.equal(matchesQuery(records[1], "goppa"), false);
  assert.equal(matchesQuery(records[1], "   "), true);
});

test("filterRecords combines tag and query", () => {
  assert.deepEqual(filterRecords(records, {}).map((r) => r.id), ["GOPPA-SYZYGY", "SIEVE-DEPTH"]);
  assert.deepEqual(filterRecords(records, { tag: "DHS-GOWERS-SIEVE" }).map((r) => r.id), ["SIEVE-DEPTH"]);
  assert.deepEqual(filterRecords(records, { tag: "DHS-GOWERS-SIEVE", query: "goppa" }), []);
});

test("recordIdFromHash decodes the fragment", () => {
  assert.equal(recordIdFromHash("#SIEVE-DEPTH"), "SIEVE-DEPTH");
  assert.equal(recordIdFromHash("#A%20B"), "A B");
  assert.equal(recordIdFromHash(""), "");
  assert.equal(recordIdFromHash("#%E0%A4%A"), "%E0%A4%A");
});
```

Create `tests/js/debts.test.mjs`:

```js
import test from "node:test";
import assert from "node:assert/strict";
import { groupDebts } from "../../site/js/lib/debts.js";

const debt = (candidate_id, debt_type, priority_score, required_resolution = `fix ${debt_type}`) =>
  ({ candidate_id, debt_type, priority_score, required_resolution });

test("groups by type, highest-priority group first, rows sorted", () => {
  const groups = groupDebts([
    debt("B", "reduction-route", 98),
    debt("C", "dequantization", 100),
    debt("A", "dequantization", 100),
    debt("A", "reduction-route", 99),
  ]);
  assert.deepEqual(groups.map((g) => g.type), ["dequantization", "reduction-route"]);
  assert.deepEqual(groups[0].debts.map((d) => d.candidate_id), ["A", "C"]);
  assert.deepEqual(groups[1].debts.map((d) => d.candidate_id), ["A", "B"]);
  assert.equal(groups[0].resolution, "fix dequantization");
});

test("resolution is null when a group's debts disagree", () => {
  const [group] = groupDebts([debt("A", "falsifier", 90, "one"), debt("B", "falsifier", 90, "two")]);
  assert.equal(group.resolution, null);
});

test("empty input gives no groups", () => {
  assert.deepEqual(groupDebts([]), []);
});
```

Create `tests/js/chart.test.mjs`:

```js
import test from "node:test";
import assert from "node:assert/strict";
import { activityChart, niceMax } from "../../site/js/lib/chart.js";

test("niceMax rounds up to 1, 2, 2.5, or 5 times a power of ten", () => {
  assert.equal(niceMax(0), 1);
  assert.equal(niceMax(7), 10);
  assert.equal(niceMax(43), 50);
  assert.equal(niceMax(120), 200);
  assert.equal(niceMax(240), 250);
});

test("activityChart draws one bar per week, the line, and month ticks", () => {
  const weeks = [
    { week: "2026-07-06", runs: 4 },
    { week: "2026-07-13", runs: 0 },
    { week: "2026-07-20", runs: 9 },
    { week: "2026-07-27", runs: 2 },
    { week: "2026-08-03", runs: 5 },
  ];
  const points = [
    { date: "2026-07-17", negative_results: 464 },
    { date: "2026-08-05", negative_results: 520 },
  ];
  const svg = activityChart({ weeks, points });
  assert.ok(svg.startsWith("<svg"));
  assert.equal((svg.match(/class="chart-bar"/g) || []).length, 5);
  assert.match(svg, /<path class="chart-line" d="M[\d.]+,[\d.]+ L[\d.]+,[\d.]+"/);
  assert.ok(svg.includes(">Aug<"));
  assert.ok(svg.includes(">520<"));
  assert.ok(svg.includes('aria-label="Experiment runs per week from Jul 6, 2026: 20 runs in total. Ideas ruled out grew to 520."'));
});

test("activityChart returns an empty string without weeks", () => {
  assert.equal(activityChart({ weeks: [], points: [] }), "");
});
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `cd "/Users/jaspersands/Desktop/quantum algorithm search" && /Users/jaspersands/.nvm/versions/node/v24.18.0/bin/node --test tests/js/*.test.mjs`
Expected: FAIL — `Cannot find module .../site/js/lib/format.js`.

- [ ] **Step 3: Write the implementations**

Create `site/js/lib/format.js`:

```js
export const REPO_URL = "https://github.com/Jaspersands/qsearch";

const ESCAPES = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };

export function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (ch) => ESCAPES[ch]);
}

export function formatNumber(value) {
  return Number(value).toLocaleString("en-US");
}

export function formatDate(isoDate) {
  const [year, month, day] = String(isoDate).slice(0, 10).split("-").map(Number);
  return new Date(Date.UTC(year, month - 1, day)).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
    timeZone: "UTC",
  });
}

export function repoUrl(path) {
  return `${REPO_URL}/blob/main/${String(path).split("/").map(encodeURIComponent).join("/")}`;
}

const STATUS_LABELS = { open: "open", "ruled-out": "ruled out", active: "active" };

export function statusMarker(kind) {
  return `<span class="status status-${kind}">${STATUS_LABELS[kind]}</span>`;
}

export function trackStatusKind(tone) {
  return tone === "active" ? "active" : "open";
}

export function humanizeId(id) {
  const words = String(id).replace(/[-_]+/g, " ").trim().toLowerCase();
  return words.charAt(0).toUpperCase() + words.slice(1);
}

export function bibtexEntry(snapshot) {
  return [
    "@misc{sands2026qsearch,",
    "  author       = {Sands, Jasper},",
    "  title        = {Q-Search: an open search for structural quantum speedups},",
    "  year         = {2026},",
    "  howpublished = {\\url{https://qsearch.jaspersands.com}},",
    `  note         = {Snapshot of ${snapshot.updated_at}; ${formatNumber(snapshot.metrics.negative_results)} negative results recorded}`,
    "}",
  ].join("\n");
}
```

Create `site/js/lib/negatives.js`:

```js
const SEARCH_FIELDS = ["id", "claim", "reason", "lesson", "source"];

export function matchesQuery(record, query) {
  const needle = String(query ?? "").trim().toLowerCase();
  if (!needle) return true;
  return SEARCH_FIELDS.some((field) => String(record[field] ?? "").toLowerCase().includes(needle));
}

export function filterRecords(records, { query = "", tag = "" } = {}) {
  return records.filter((record) => (!tag || record.tags.includes(tag)) && matchesQuery(record, query));
}

export function recordIdFromHash(hash) {
  const raw = String(hash ?? "").replace(/^#/, "");
  if (!raw) return "";
  try {
    return decodeURIComponent(raw);
  } catch {
    return raw;
  }
}
```

Create `site/js/lib/debts.js`:

```js
function byPriorityThenCandidate(a, b) {
  return b.priority_score - a.priority_score || a.candidate_id.localeCompare(b.candidate_id);
}

export function groupDebts(debts) {
  const groups = new Map();
  for (const debt of debts) {
    if (!groups.has(debt.debt_type)) {
      groups.set(debt.debt_type, { type: debt.debt_type, resolution: debt.required_resolution, debts: [] });
    }
    const group = groups.get(debt.debt_type);
    if (group.resolution !== debt.required_resolution) group.resolution = null;
    group.debts.push(debt);
  }
  const topPriority = (group) => Math.max(...group.debts.map((debt) => debt.priority_score));
  return [...groups.values()]
    .map((group) => ({ ...group, debts: [...group.debts].sort(byPriorityThenCandidate) }))
    .sort((a, b) => topPriority(b) - topPriority(a) || a.type.localeCompare(b.type));
}
```

Create `site/js/lib/chart.js`:

```js
import { escapeHtml, formatDate, formatNumber } from "./format.js";

const DAY_MS = 86400000;
const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

function dayValue(isoDate) {
  const [year, month, day] = String(isoDate).slice(0, 10).split("-").map(Number);
  return Date.UTC(year, month - 1, day);
}

export function niceMax(value) {
  if (!(value > 0)) return 1;
  const magnitude = 10 ** Math.floor(Math.log10(value));
  for (const step of [1, 2, 2.5, 5, 10]) {
    if (step * magnitude >= value) return step * magnitude;
  }
  return 10 * magnitude;
}

export function activityChart({ weeks, points = [], width = 720, height = 240 }) {
  if (!weeks || weeks.length === 0) return "";
  const pad = { top: 20, right: 56, bottom: 28, left: 36 };
  const plotWidth = width - pad.left - pad.right;
  const plotHeight = height - pad.top - pad.bottom;
  const baseline = pad.top + plotHeight;
  const start = dayValue(weeks[0].week);
  const end = Math.max(
    dayValue(weeks[weeks.length - 1].week) + 7 * DAY_MS,
    ...points.map((point) => dayValue(point.date)),
  );
  const x = (time) => pad.left + ((time - start) / (end - start)) * plotWidth;
  const visible = points.filter((point) => dayValue(point.date) >= start);
  const runMax = niceMax(Math.max(...weeks.map((week) => week.runs)));
  const lineMax = niceMax(Math.max(1, ...visible.map((point) => point.negative_results)));
  const yRuns = (value) => baseline - (value / runMax) * plotHeight;
  const yLine = (value) => baseline - (value / lineMax) * plotHeight;
  const barWidth = Math.max(1, x(start + 7 * DAY_MS) - x(start) - 3);
  const parts = [];

  const first = new Date(start);
  let tick = Date.UTC(first.getUTCFullYear(), first.getUTCMonth() + 1, 1);
  while (tick < end) {
    const tickDate = new Date(tick);
    const tx = x(tick).toFixed(1);
    parts.push(`<line class="chart-grid" x1="${tx}" x2="${tx}" y1="${pad.top}" y2="${baseline}"/>`);
    parts.push(`<text class="chart-label" x="${(x(tick) + 4).toFixed(1)}" y="${baseline + 18}">${MONTHS[tickDate.getUTCMonth()]}</text>`);
    tick = Date.UTC(tickDate.getUTCFullYear(), tickDate.getUTCMonth() + 1, 1);
  }

  for (const week of weeks) {
    const top = yRuns(week.runs);
    parts.push(
      `<rect class="chart-bar" x="${(x(dayValue(week.week)) + 1.5).toFixed(1)}" y="${top.toFixed(1)}" ` +
        `width="${barWidth.toFixed(1)}" height="${(baseline - top).toFixed(1)}">` +
        `<title>Week of ${escapeHtml(formatDate(week.week))}: ${formatNumber(week.runs)} runs</title></rect>`,
    );
  }

  if (visible.length) {
    const path = visible
      .map((point, index) => `${index === 0 ? "M" : "L"}${x(dayValue(point.date)).toFixed(1)},${yLine(point.negative_results).toFixed(1)}`)
      .join(" ");
    parts.push(`<path class="chart-line" d="${path}"/>`);
    const last = visible[visible.length - 1];
    parts.push(
      `<text class="chart-label chart-label-strong" x="${(x(dayValue(last.date)) + 6).toFixed(1)}" ` +
        `y="${(yLine(last.negative_results) + 4).toFixed(1)}">${formatNumber(last.negative_results)}</text>`,
    );
  }

  parts.push(`<line class="chart-axis" x1="${pad.left}" x2="${pad.left + plotWidth}" y1="${baseline}" y2="${baseline}"/>`);
  parts.push(`<text class="chart-label" x="${pad.left - 6}" y="${baseline}" text-anchor="end">0</text>`);
  parts.push(`<text class="chart-label" x="${pad.left - 6}" y="${pad.top + 4}" text-anchor="end">${formatNumber(runMax)}</text>`);

  const total = weeks.reduce((sum, week) => sum + week.runs, 0);
  let label = `Experiment runs per week from ${formatDate(weeks[0].week)}: ${formatNumber(total)} runs in total.`;
  if (visible.length) label += ` Ideas ruled out grew to ${formatNumber(visible[visible.length - 1].negative_results)}.`;
  return `<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="${escapeHtml(label)}">${parts.join("")}</svg>`;
}
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `cd "/Users/jaspersands/Desktop/quantum algorithm search" && /Users/jaspersands/.nvm/versions/node/v24.18.0/bin/node --test tests/js/*.test.mjs`
Expected: all tests pass (`# fail 0`).

- [ ] **Step 5: Commit**

```bash
cd "/Users/jaspersands/Desktop/quantum algorithm search" && git add site/package.json site/js/lib tests/js && git commit -m "Add tested front-end modules for formatting, filtering, grouping, and the activity chart

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 5: Visual system, shared shell, and the How it works page

**Files:**
- Rewrite: `site/styles.css` (replace the whole file)
- Create: `site/js/common.js`
- Create: `how-it-works.html`

**Interfaces:**
- Consumes: `REPO_URL`, `escapeHtml`, `formatDate` from `site/js/lib/format.js`.
- Produces (`site/js/common.js` exports): `SNAPSHOT_PATH = "research/progress_snapshot.json"`, `loadJson(path) -> Promise<any>`, `showLoadError(container, path)`, `setText(id, value)`, `bindCopyButtons(root = document)` (wires `button[data-copy="<element id>"]`), `initFooter(snapshotPromise?)` (fills every `[data-updated]`).
- Produces (CSS classes used by every page): `wrap`, `with-notes`, `note`, `prose`, `page-head`, `intro`, `section`, `section-head`, `verdict`, `verdict-label`, `figures`, `figure-value`, `figure-label`, `status`, `status-open|ruled-out|active`, `rows`, `row`, `row-title`, `row-summary`, `row-next`, `row-body`, `facts`, `mono`, `small`, `sub`, `milestones`, `changelog`, `command`, `copy`, `chart`, `legend`, `legend-bar`, `legend-line`, `table`, `id`, `filters`, `chip`, `count`, `search`, `result-count`, `button`, `field`, `debt-group`, `terms`, `loop`, `loop-return`, `load-error`, `muted`, `num`, `visually-hidden`, `site-header`, `site-footer`.
- Produces: the shared header and footer markup below, copied verbatim into every page (only `aria-current` moves).

Shared header (set `aria-current="page"` on the current page's link):

```html
  <header class="site-header">
    <div class="wrap header-inner">
      <a class="wordmark" href="index.html">Q-Search</a>
      <nav aria-label="Site">
        <a href="index.html">Home</a>
        <a href="open-problems.html">Open problems</a>
        <a href="negative-results.html">Negative results</a>
        <a href="how-it-works.html">How it works</a>
      </nav>
      <a class="header-github" href="https://github.com/Jaspersands/qsearch">GitHub</a>
    </div>
  </header>
```

Shared footer:

```html
  <footer class="site-footer">
    <div class="wrap footer-inner">
      <p>Q-Search is an open research project by Jasper Sands. Data updated <time data-updated>recently</time>.</p>
      <p><a href="https://github.com/Jaspersands/qsearch">Source on GitHub</a> · <a href="index.html#cite">Cite</a></p>
    </div>
  </footer>
```

Shared `<head>` block (change `<title>` and `description` per page):

```html
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Schibsted+Grotesk:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap">
  <link rel="stylesheet" href="site/styles.css">
```

- [ ] **Step 1: Replace the stylesheet**

Overwrite `site/styles.css` with:

```css
:root {
  --bg: #ffffff;
  --text: #111111;
  --text-2: #555555;
  --text-3: #767676;
  --rule: #e6e6e6;
  --rule-strong: #111111;
  --fill: #f5f5f4;
  --bar: #d6d3d1;
  --accent: #c2410c;
  --sans: "Schibsted Grotesk", "Helvetica Neue", Arial, sans-serif;
  --serif: "Source Serif 4", Georgia, serif;
  --mono: "JetBrains Mono", ui-monospace, Menlo, monospace;
  --measure: 40rem;
  --wide: 70rem;
}

*, *::before, *::after { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body { margin: 0; background: var(--bg); color: var(--text); font: 17px/1.6 var(--sans); }
svg { display: block; max-width: 100%; }
a { color: inherit; text-decoration: underline; text-decoration-color: #bdbdbd; text-decoration-thickness: 1px; text-underline-offset: 0.18em; }
a:hover { text-decoration-color: currentColor; }
:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
h1, h2, h3, h4 { margin: 0; font-family: var(--sans); font-weight: 600; line-height: 1.15; letter-spacing: -0.015em; }
h1 { font-size: clamp(2rem, 4.6vw, 3.25rem); letter-spacing: -0.03em; max-width: 20ch; }
h2 { font-size: 1.6rem; }
h3 { font-size: 1.1rem; letter-spacing: -0.005em; }
h4 { font-size: 0.95rem; }
p { margin: 0 0 1em; }
code, pre { font-family: var(--mono); font-size: 0.84em; }
ul, ol { margin: 0 0 1em; padding-left: 1.2em; }

.wrap { max-width: var(--wide); margin: 0 auto; padding: 0 24px; }
.prose { font-family: var(--serif); font-size: 1.125rem; line-height: 1.65; max-width: var(--measure); }
.muted { color: var(--text-2); }
.num { font-variant-numeric: tabular-nums; }
.mono { font-family: var(--mono); font-size: 0.8rem; overflow-wrap: anywhere; }
.small { font-size: 0.88rem; line-height: 1.55; color: var(--text-2); }
.visually-hidden { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
.load-error { color: var(--text-2); font-size: 0.95rem; }

/* Header and footer */
.site-header { border-bottom: 1px solid var(--rule); }
.header-inner { display: flex; align-items: baseline; gap: 12px 36px; padding-top: 18px; padding-bottom: 16px; }
.wordmark { font-weight: 700; font-size: 1.05rem; letter-spacing: -0.01em; text-decoration: none; }
.site-header nav { display: flex; flex-wrap: wrap; gap: 4px 22px; font-size: 0.95rem; }
.site-header nav a, .header-github { color: var(--text-2); text-decoration: none; }
.site-header nav a:hover, .header-github:hover { color: var(--text); }
.site-header nav a[aria-current="page"] { color: var(--text); text-decoration: underline; text-decoration-color: var(--accent); text-decoration-thickness: 2px; text-underline-offset: 0.45em; }
.header-github { margin-left: auto; font-size: 0.95rem; }
.site-footer { border-top: 1px solid var(--rule); padding: 32px 0 48px; font-size: 0.9rem; color: var(--text-2); }
.footer-inner { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 8px 24px; }
.footer-inner p { margin: 0; }

/* Page structure */
.intro { padding-top: 72px; padding-bottom: 56px; }
.intro h1 { margin-bottom: 24px; }
.page-head { padding-top: 64px; padding-bottom: 24px; }
.page-head h1 { margin-bottom: 20px; }
.section { padding: 64px 0; border-top: 1px solid var(--rule); }
.section-head { max-width: var(--measure); margin-bottom: 28px; }
.section-head h2 { margin-bottom: 10px; }
.section-head p { color: var(--text-2); margin: 0; }

/* Margin notes */
.with-notes { display: grid; grid-template-columns: minmax(0, 1fr); gap: 16px; }
.note { font-size: 0.85rem; line-height: 1.5; color: var(--text-2); border-top: 1px solid var(--rule); padding-top: 10px; }
.note p { margin: 0 0 0.6em; }
@media (min-width: 900px) {
  .with-notes { grid-template-columns: minmax(0, 46rem) minmax(0, 15rem); column-gap: 56px; }
  .note { border-top: 0; padding-top: 0.4em; }
}

/* Intro figures and verdict */
.verdict { display: flex; flex-wrap: wrap; gap: 4px 12px; align-items: baseline; margin: 28px 0 0; max-width: var(--measure); }
.verdict-label { color: var(--accent); font-weight: 600; }
.figures { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 24px; margin-top: 36px; padding-top: 20px; border-top: 1px solid var(--rule-strong); max-width: 46rem; }
.figure-value { display: block; font-size: clamp(1.9rem, 4vw, 2.75rem); font-weight: 600; letter-spacing: -0.03em; line-height: 1; font-variant-numeric: tabular-nums; }
.figure-label { display: block; margin-top: 8px; font-size: 0.9rem; color: var(--text-2); }

/* Status marker: the only badge-like element on the site */
.status { display: inline-flex; align-items: center; gap: 6px; font-size: 0.85rem; color: var(--text-2); white-space: nowrap; }
.status::before { content: ""; flex: none; width: 7px; height: 7px; border-radius: 50%; }
.status-active { color: var(--text); }
.status-active::before { background: var(--text); }
.status-open::before { border: 1.5px solid var(--text-2); }
.status-ruled-out { color: var(--accent); }
.status-ruled-out::before { background: var(--accent); }

/* Expandable rows: tracks, frontiers, negative results */
.rows { border-top: 1px solid var(--rule-strong); }
.row { border-bottom: 1px solid var(--rule); }
.row > summary { list-style: none; cursor: pointer; display: grid; grid-template-columns: minmax(0, 13rem) minmax(0, 1fr) auto; gap: 6px 32px; align-items: baseline; padding: 18px 0; }
.row > summary::-webkit-details-marker { display: none; }
.row > summary:hover .row-title { text-decoration: underline; text-decoration-color: #bdbdbd; text-underline-offset: 0.18em; }
.row-title { font-weight: 600; }
.row-title.mono { font-weight: 500; }
.row-next { display: block; margin-top: 4px; font-size: 0.92rem; color: var(--text-2); }
.row-body { max-width: var(--measure); padding-bottom: 24px; }
.row-body > *:last-child { margin-bottom: 0; }
.row-body h4 { margin: 16px 0 6px; }
@media (min-width: 760px) { .row-body { margin-left: calc(13rem + 32px); } }
@media (max-width: 759px) {
  .row > summary { grid-template-columns: minmax(0, 1fr) auto; }
  .row > summary .row-summary { grid-column: 1 / -1; }
}
.facts { display: grid; grid-template-columns: max-content minmax(0, 1fr); gap: 8px 20px; margin: 0 0 12px; font-size: 0.95rem; }
.facts dt { color: var(--text-2); }
.facts dd { margin: 0; overflow-wrap: anywhere; }
@media (max-width: 600px) { .facts { grid-template-columns: minmax(0, 1fr); gap: 2px; } .facts dd { margin-bottom: 8px; } }
details.sub { margin: 10px 0; }
details.sub > summary { cursor: pointer; font-size: 0.9rem; color: var(--text-2); }
details.sub[open] > summary { margin-bottom: 6px; }

/* Lists */
.milestones { list-style: none; padding: 0; margin: 0; max-width: var(--measure); }
.milestones li { padding: 18px 0; border-top: 1px solid var(--rule); }
.milestones h3 { margin-bottom: 6px; }
.milestones p { margin: 0; color: var(--text-2); }
.changelog { list-style: none; padding: 0; margin: 0; max-width: 52rem; }
.changelog > li { display: grid; grid-template-columns: 7.5rem minmax(0, 1fr); gap: 4px 24px; padding: 14px 0; border-top: 1px solid var(--rule); }
.changelog time { color: var(--text-2); font-variant-numeric: tabular-nums; }
.changelog ul { margin: 0; padding-left: 1.1em; }
@media (max-width: 600px) { .changelog > li { grid-template-columns: minmax(0, 1fr); } }

/* Commands and copy buttons */
.command { display: flex; align-items: flex-start; gap: 12px; border: 1px solid var(--rule); padding: 12px 14px; margin: 0 0 10px; max-width: 46rem; }
.command pre { flex: 1; min-width: 0; margin: 0; white-space: pre-wrap; overflow-wrap: anywhere; }
button.copy { font: 500 0.8rem var(--sans); background: none; border: 1px solid var(--rule); color: var(--text-2); padding: 3px 10px; border-radius: 3px; cursor: pointer; }
button.copy:hover { border-color: var(--text); color: var(--text); }
button.button { font: 600 0.95rem var(--sans); background: var(--bg); color: var(--text); border: 1px solid var(--text); padding: 8px 16px; border-radius: 3px; cursor: pointer; margin-top: 20px; }
button.button:hover { background: var(--fill); }

/* Chart */
.chart { margin: 0; max-width: 56rem; }
.chart svg { width: 100%; height: auto; }
.chart-bar { fill: var(--bar); }
.chart-line { fill: none; stroke: var(--accent); stroke-width: 2; }
.chart-grid { stroke: var(--rule); stroke-width: 1; }
.chart-axis { stroke: var(--rule-strong); stroke-width: 1; }
.chart-label { font: 12px var(--sans); fill: var(--text-2); }
.chart-label-strong { fill: var(--accent); font-weight: 600; }
.legend { display: flex; flex-wrap: wrap; gap: 6px 20px; margin: 12px 0 0; font-size: 0.85rem; color: var(--text-2); }
.legend-bar::before { content: ""; display: inline-block; width: 10px; height: 10px; background: var(--bar); margin-right: 6px; vertical-align: -1px; }
.legend-line::before { content: ""; display: inline-block; width: 14px; height: 2px; background: var(--accent); margin-right: 6px; vertical-align: 3px; }

/* Tables */
.table { width: 100%; border-collapse: collapse; font-size: 0.95rem; }
.table th { text-align: left; font-weight: 600; font-size: 0.85rem; color: var(--text-2); padding: 0 16px 10px 0; border-bottom: 1px solid var(--rule-strong); }
.table td { padding: 12px 16px 12px 0; border-bottom: 1px solid var(--rule); vertical-align: top; }
.table .id { font-family: var(--mono); font-size: 0.8rem; overflow-wrap: anywhere; }
@media (max-width: 700px) {
  .table thead { display: none; }
  .table tr { display: block; padding: 12px 0; border-bottom: 1px solid var(--rule); }
  .table td { display: block; border: 0; padding: 2px 0; }
  .table td[data-label]::before { content: attr(data-label) ": "; color: var(--text-2); font-family: var(--sans); }
}

/* Filters and search */
.search { width: 100%; max-width: var(--measure); font: 1rem var(--sans); color: var(--text); background: var(--bg); padding: 10px 12px; border: 1px solid #bdbdbd; border-radius: 3px; }
.search:focus { outline: 2px solid var(--accent); outline-offset: 1px; border-color: var(--text); }
.filters { display: flex; flex-wrap: wrap; gap: 8px; margin: 16px 0 8px; }
.chip { font: 0.9rem var(--sans); color: var(--text-2); background: var(--bg); border: 1px solid var(--rule); padding: 4px 12px; border-radius: 3px; cursor: pointer; }
.chip:hover { border-color: var(--text-2); }
.chip[aria-pressed="true"] { color: var(--text); border-color: var(--text); background: var(--fill); }
.chip .count { color: var(--text-3); margin-left: 6px; font-variant-numeric: tabular-nums; }
.result-count { font-size: 0.9rem; color: var(--text-2); margin: 12px 0; }
.field { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 12px; margin-bottom: 8px; font-size: 0.95rem; }
.field select { font: inherit; color: var(--text); background: var(--bg); padding: 6px 8px; border: 1px solid #bdbdbd; border-radius: 3px; max-width: 100%; }
.debt-group { margin-top: 40px; }
.debt-group h3 { margin-bottom: 6px; }
.debt-group > p { max-width: var(--measure); }

/* How it works */
.loop { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); border-top: 1px solid var(--rule-strong); counter-reset: loop; }
.loop li { counter-increment: loop; padding: 16px 24px 4px 0; }
.loop li + li { padding-left: 24px; border-left: 1px solid var(--rule); }
.loop h3 { margin-bottom: 8px; }
.loop h3::before { content: counter(loop) "\2002"; color: var(--accent); font-variant-numeric: tabular-nums; }
.loop p { margin: 0; color: var(--text-2); font-size: 0.95rem; }
.loop-return { margin-top: 20px; color: var(--text-2); max-width: var(--measure); }
@media (max-width: 760px) {
  .loop { grid-template-columns: minmax(0, 1fr); }
  .loop li + li { border-left: 0; padding-left: 0; border-top: 1px solid var(--rule); }
}
.terms { display: grid; grid-template-columns: minmax(0, 12rem) minmax(0, 1fr); gap: 14px 32px; margin: 0; max-width: 52rem; }
.terms dt { font-weight: 600; }
.terms dd { margin: 0; color: var(--text-2); }
@media (max-width: 600px) { .terms { grid-template-columns: minmax(0, 1fr); gap: 2px; } .terms dd { margin-bottom: 12px; } }

/* Small screens */
@media (max-width: 640px) {
  body { font-size: 16px; }
  .wrap { padding: 0 16px; }
  .header-inner { flex-direction: column; gap: 8px; }
  .header-github { display: none; }
  .intro { padding-top: 40px; padding-bottom: 40px; }
  .page-head { padding-top: 40px; }
  .section { padding: 44px 0; }
  .figures { gap: 12px; }
}
```

- [ ] **Step 2: Write the shared module**

Create `site/js/common.js`:

```js
import { REPO_URL, escapeHtml, formatDate } from "./lib/format.js";

export const SNAPSHOT_PATH = "research/progress_snapshot.json";

export async function loadJson(path) {
  const response = await fetch(path, { cache: "no-cache" });
  if (!response.ok) throw new Error(`${path}: HTTP ${response.status}`);
  return response.json();
}

export function showLoadError(container, path) {
  if (!container) return;
  container.innerHTML =
    `<p class="load-error">This part of the page couldn't load <code>${escapeHtml(path)}</code>. ` +
    `<a href="${REPO_URL}/blob/main/${escapeHtml(path)}">Read the file on GitHub</a>.</p>`;
}

export function setText(id, value) {
  const node = document.getElementById(id);
  if (node) node.textContent = value;
}

export function bindCopyButtons(root = document) {
  for (const button of root.querySelectorAll("button[data-copy]")) {
    button.addEventListener("click", async () => {
      const source = document.getElementById(button.dataset.copy);
      if (!source) return;
      try {
        await navigator.clipboard.writeText(source.textContent.trim());
        button.textContent = "Copied";
      } catch {
        button.textContent = "Copy failed";
      }
      setTimeout(() => {
        button.textContent = "Copy";
      }, 1600);
    });
  }
}

export function initFooter(snapshotPromise = loadJson(SNAPSHOT_PATH)) {
  snapshotPromise
    .then((snapshot) => {
      for (const node of document.querySelectorAll("[data-updated]")) {
        node.textContent = formatDate(snapshot.updated_at);
        node.setAttribute("datetime", snapshot.updated_at);
      }
    })
    .catch(() => {});
}
```

- [ ] **Step 3: Write the How it works page**

Create `how-it-works.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>How it works · Q-Search</title>
  <meta name="description" content="How Q-Search proposes quantum algorithms, attacks them classically, records what fails, and decides what can be claimed.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Schibsted+Grotesk:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap">
  <link rel="stylesheet" href="site/styles.css">
  <script type="module">
    import { initFooter } from "./site/js/common.js";
    initFooter();
  </script>
</head>
<body>
  <header class="site-header">
    <div class="wrap header-inner">
      <a class="wordmark" href="index.html">Q-Search</a>
      <nav aria-label="Site">
        <a href="index.html">Home</a>
        <a href="open-problems.html">Open problems</a>
        <a href="negative-results.html">Negative results</a>
        <a href="how-it-works.html" aria-current="page">How it works</a>
      </nav>
      <a class="header-github" href="https://github.com/Jaspersands/qsearch">GitHub</a>
    </div>
  </header>

  <main>
    <div class="wrap page-head">
      <h1>How it works</h1>
      <div class="prose">
        <p>Most proposals for new quantum algorithms fall apart for one of two reasons: a classical algorithm turns out to do the same job, or the idea only works on small examples. Q-Search is set up to find out which, as early as possible, and to write the answer down.</p>
      </div>
    </div>

    <section class="section" id="loop">
      <div class="wrap">
        <div class="section-head">
          <h2>The loop</h2>
          <p>Every idea goes through the same four steps.</p>
        </div>
        <ol class="loop">
          <li>
            <h3>Propose</h3>
            <p>Write down a candidate quantum procedure for one specific problem, including the exact measurement it would make.</p>
          </li>
          <li>
            <h3>Attack classically</h3>
            <p>Try to get the same answer with classical methods: information-set decoding, lattice reduction, Weisfeiler–Leman refinement, Fourier methods. If one works, the quantum idea offers no speedup.</p>
          </li>
          <li>
            <h3>Record</h3>
            <p>Every idea that fails goes into the negative-results registry with the reason and the lesson, so it isn't tried again.</p>
          </li>
          <li>
            <h3>Proof gate</h3>
            <p>An idea that survives still can't be called a speedup until its missing proofs, its proof debts, are written and checked.</p>
          </li>
        </ol>
        <p class="loop-return">Ideas that survive the gate at small sizes go back to step 2 at larger sizes. So far, none has made it through.</p>
      </div>
    </section>

    <section class="section" id="terms">
      <div class="wrap">
        <div class="section-head">
          <h2>Terms used on this site</h2>
        </div>
        <dl class="terms">
          <dt>Hidden subgroup problem</dt>
          <dd>A family of problems where a function hides a subgroup and you have to find it. Shor's factoring algorithm solves the abelian case. The dihedral and symmetric-group cases are open.</dd>
          <dt>Code equivalence</dt>
          <dd>Deciding whether two error-correcting codes are the same up to reordering their coordinates. Some post-quantum cryptography depends on this being hard.</dd>
          <dt>Dequantization</dt>
          <dd>Showing that a classical algorithm can do what a proposed quantum one does, about as fast. A dequantized idea offers no speedup.</dd>
          <dt>Negative result</dt>
          <dd>A recorded failure: the claim that was tested, why it's false or blocked, and what to do differently next time.</dd>
          <dt>Proof debt</dt>
          <dd>A proof that has to exist before a claim can be made. For example, that a reduction really preserves the original problem, or that no known classical method already works.</dd>
          <dt>Kill criterion</dt>
          <dd>A condition, decided in advance, that ends a line of research if it's met.</dd>
        </dl>
      </div>
    </section>

    <section class="section" id="repository">
      <div class="wrap">
        <div class="section-head">
          <h2>What's in the repository</h2>
          <p>Everything on this site is generated from these folders.</p>
        </div>
        <table class="table">
          <thead><tr><th>Path</th><th>What it holds</th></tr></thead>
          <tbody>
            <tr><td class="id" data-label="Path"><a href="https://github.com/Jaspersands/qsearch/blob/main/qsearch.py">qsearch.py</a></td><td data-label="Holds">The command-line entry point for every registered workflow.</td></tr>
            <tr><td class="id" data-label="Path"><a href="https://github.com/Jaspersands/qsearch/tree/main/core">core/</a></td><td data-label="Holds">The framework: research registry, experiment runner, proof gate, and the classical-attack scanner.</td></tr>
            <tr><td class="id" data-label="Path"><a href="https://github.com/Jaspersands/qsearch/tree/main/theorems">theorems/</a></td><td data-label="Holds">One module per verification workbench: dihedral and phase-state problems (<code>dcp_*</code>), coset states (<code>coset_*</code>, <code>cfi_*</code>), wreath products (<code>self_dual_wreath_*</code>), and code equivalence (<code>code_*</code>, <code>goppa_*</code>, <code>bch_*</code>).</td></tr>
            <tr><td class="id" data-label="Path"><a href="https://github.com/Jaspersands/qsearch/tree/main/research/registry">research/registry/</a></td><td data-label="Holds">The canonical registries: candidates, experiments, results, negative results, and dequantization checks.</td></tr>
            <tr><td class="id" data-label="Path"><a href="https://github.com/Jaspersands/qsearch/tree/main/research">research/</a></td><td data-label="Holds">Generated outputs for each area, the written derivations (<code>*.md</code>), the frontier map, and the proof-debt report.</td></tr>
            <tr><td class="id" data-label="Path"><a href="https://github.com/Jaspersands/qsearch/tree/main/tests">tests/</a></td><td data-label="Holds">Unit, integration, and registry tests.</td></tr>
            <tr><td class="id" data-label="Path"><a href="https://github.com/Jaspersands/qsearch/tree/main/tools">tools/</a></td><td data-label="Holds">Scripts that build and check this website's data.</td></tr>
            <tr><td class="id" data-label="Path"><a href="https://github.com/Jaspersands/qsearch/tree/main/site">site/</a></td><td data-label="Holds">This website's styles, scripts, and data files.</td></tr>
          </tbody>
        </table>
      </div>
    </section>

    <section class="section" id="commands">
      <div class="wrap with-notes">
        <div>
          <div class="section-head">
            <h2>Main commands</h2>
            <p>Run these from the repository root.</p>
          </div>
          <div class="command"><pre id="cmd-validate">python qsearch.py validate</pre><button class="copy" type="button" data-copy="cmd-validate">Copy</button></div>
          <div class="command"><pre id="cmd-run-next">python qsearch.py run-next</pre><button class="copy" type="button" data-copy="cmd-run-next">Copy</button></div>
          <div class="command"><pre id="cmd-build">python tools/build_progress_snapshot.py
python tools/build_site_data.py</pre><button class="copy" type="button" data-copy="cmd-build">Copy</button></div>
          <div class="command"><pre id="cmd-tests">python -m pytest tests/</pre><button class="copy" type="button" data-copy="cmd-tests">Copy</button></div>
        </div>
        <aside class="note">
          <p><code>validate</code> checks every candidate and experiment against its proof obligations. GitHub Actions runs it on every push.</p>
          <p><code>run-next</code> runs the highest-priority registered experiment.</p>
          <p>The two build scripts regenerate the files this website reads.</p>
        </aside>
      </div>
    </section>

    <section class="section" id="limits">
      <div class="wrap">
        <div class="section-head">
          <h2>Limits</h2>
        </div>
        <ul class="prose">
          <li>Numerical checks are not formal proofs. Many derivations in the registry are marked review-pending: written down and checked by scripts, but not yet independently reviewed.</li>
          <li>Results at small sizes don't establish how an idea scales. The proof gate exists because small cases often look better than large ones.</li>
          <li>Research runs in interactive sessions directed by Jasper Sands, using AI coding agents. GitHub Actions validates every push. Nothing runs on its own between sessions.</li>
          <li>No speedup is claimed. The site will only say otherwise once every proof debt for that claim is closed.</li>
        </ul>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="wrap footer-inner">
      <p>Q-Search is an open research project by Jasper Sands. Data updated <time data-updated>recently</time>.</p>
      <p><a href="https://github.com/Jaspersands/qsearch">Source on GitHub</a> · <a href="index.html#cite">Cite</a></p>
    </div>
  </footer>
  <script type="module">
    import { bindCopyButtons } from "./site/js/common.js";
    bindCopyButtons();
  </script>
</body>
</html>
```

- [ ] **Step 4: Check syntax, references, and the rendered page**

Run:
```bash
cd "/Users/jaspersands/Desktop/quantum algorithm search" && /Users/jaspersands/.nvm/versions/node/v24.18.0/bin/node --check site/js/common.js && /opt/anaconda3/bin/python3 tools/check_site.py | grep -vE "^(index|methodology|frontier|negative-results|proof-debt|repomap)\.html"; /opt/anaconda3/bin/python3 tools/site_smoke.py --pages how-it-works.html --no-redirects --out /private/tmp/claude-501/-Users-jaspersands-Desktop-quantum-algorithm-search/bd8c9228-91bd-497e-a749-a904429b7c83/scratchpad/shots-new
```
Expected: the only remaining lines are `how-it-works.html: links to missing page open-problems.html` (created in Task 7) — nothing about `site/js`. Old pages still report problems; they are replaced later. Smoke: `Smoke checks passed.` Open `how-it-works-1440.png` and `how-it-works-390.png` with the Read tool and check against the anti-slop rules: no eyebrows, no shadows, no pills, the loop reads as a ruled sequence, the table stacks on mobile, no horizontal scroll.

- [ ] **Step 5: Commit**

```bash
cd "/Users/jaspersands/Desktop/quantum algorithm search" && git add site/styles.css site/js/common.js how-it-works.html && git commit -m "Rewrite the visual system and add the How it works page

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 6: Home page

**Files:**
- Rewrite: `index.html` (replace the whole file)
- Create: `site/js/home.js`
- Delete: `site/progress.js`

**Interfaces:**
- Consumes: `loadJson`, `showLoadError`, `setText`, `bindCopyButtons`, `initFooter`, `SNAPSHOT_PATH` from `site/js/common.js`; `escapeHtml`, `formatDate`, `formatNumber`, `statusMarker`, `trackStatusKind`, `bibtexEntry` from `format.js`; `activityChart` from `chart.js`; `site/data/activity.json` (Task 1), `site/data/changelog.json` (Task 2), `research/progress_snapshot.json` (existing: `verdict.{title,detail}`, `updated_at`, `metrics.{negative_results,experiments,proof_debts}`, `tracks[].{title,short_title,status,summary,evidence,next,tone}`, `milestones[].{title,detail}`, `execution_model`).

- [ ] **Step 1: Write the page**

Overwrite `index.html` with:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Q-Search · looking for quantum speedups</title>
  <meta name="description" content="An open research project looking for quantum algorithms that beat classical ones on hard algebraic problems, with a public record of every idea that failed.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Schibsted+Grotesk:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap">
  <link rel="stylesheet" href="site/styles.css">
  <script type="module" src="site/js/home.js"></script>
</head>
<body>
  <header class="site-header">
    <div class="wrap header-inner">
      <a class="wordmark" href="index.html">Q-Search</a>
      <nav aria-label="Site">
        <a href="index.html" aria-current="page">Home</a>
        <a href="open-problems.html">Open problems</a>
        <a href="negative-results.html">Negative results</a>
        <a href="how-it-works.html">How it works</a>
      </nav>
      <a class="header-github" href="https://github.com/Jaspersands/qsearch">GitHub</a>
    </div>
  </header>

  <main>
    <section class="wrap intro with-notes">
      <div>
        <h1>Looking for quantum speedups, and keeping every idea that fails.</h1>
        <div class="prose">
          <p>Quantum computers are known to beat classical ones on a few problems, like factoring. Q-Search asks whether the same kind of speedup exists for harder relatives of those problems: the dihedral hidden subgroup problem, hidden subgroups of symmetric groups, and deciding whether two error-correcting codes are the same up to relabeling.</p>
          <p>Each idea gets attacked with the best classical methods we can find. Almost all of them fail. We keep every failure on record, with the reason, so the same idea doesn't get tried twice.</p>
        </div>
        <p class="verdict" id="verdict"><span class="verdict-label" id="verdict-title">Current verdict</span> <span class="muted" id="verdict-detail">Reading the latest snapshot.</span></p>
        <div class="figures">
          <div><span class="figure-value" id="fig-negatives">–</span><span class="figure-label">ideas ruled out</span></div>
          <div><span class="figure-value" id="fig-experiments">–</span><span class="figure-label">experiments run</span></div>
          <div><span class="figure-value" id="fig-debts">–</span><span class="figure-label">open proof debts</span></div>
        </div>
      </div>
      <aside class="note">
        <p>As of <span id="snapshot-date">the latest snapshot</span>.</p>
        <p>Counts come from <a href="https://github.com/Jaspersands/qsearch/blob/main/research/progress_snapshot.json"><code>progress_snapshot.json</code></a>, which <a href="https://github.com/Jaspersands/qsearch/blob/main/tools/build_progress_snapshot.py"><code>build_progress_snapshot.py</code></a> builds from the registries.</p>
        <p>No speedup is claimed anywhere on this site.</p>
      </aside>
    </section>

    <section class="section" id="tracks">
      <div class="wrap">
        <div class="section-head">
          <h2>Where things stand</h2>
          <p>Three lines of attack. Each row shows the current state and the next step. Open a row for the evidence.</p>
        </div>
        <div class="rows" id="track-rows"></div>
      </div>
    </section>

    <section class="section" id="activity">
      <div class="wrap">
        <div class="section-head">
          <h2>Activity</h2>
          <p>Experiment runs per week, and the running total of ideas ruled out.</p>
        </div>
        <figure class="chart" id="activity-chart"></figure>
        <p class="legend"><span class="legend-bar">Runs per week</span><span class="legend-line">Ideas ruled out, running total</span></p>
        <p class="small">Runs come from <a href="https://github.com/Jaspersands/qsearch/blob/main/research/experiment_run_history.json"><code>experiment_run_history.json</code></a>. The total comes from each committed version of the snapshot.</p>
      </div>
    </section>

    <section class="section" id="results">
      <div class="wrap">
        <div class="section-head">
          <h2>Results so far</h2>
          <p>The strongest things established so far. Most are limits: proofs that a route can't work.</p>
        </div>
        <ol class="milestones" id="milestones"></ol>
      </div>
    </section>

    <section class="section" id="changes">
      <div class="wrap">
        <div class="section-head">
          <h2>What changed</h2>
          <p>How the verdict, the three tracks, and the count of ruled-out ideas have moved, newest first.</p>
        </div>
        <ol class="changelog" id="changelog"></ol>
        <button class="button" type="button" id="changelog-more" hidden>Show all changes</button>
      </div>
    </section>

    <section class="section" id="reproduce">
      <div class="wrap with-notes">
        <div>
          <div class="section-head">
            <h2>Check it yourself</h2>
            <p>Everything here is generated from files in the repository. To rebuild and validate the registries on your machine:</p>
          </div>
          <div class="command"><pre id="cmd-setup">git clone https://github.com/Jaspersands/qsearch.git
cd qsearch
python -m pip install -r requirements.txt</pre><button class="copy" type="button" data-copy="cmd-setup">Copy</button></div>
          <div class="command"><pre id="cmd-validate">python qsearch.py validate</pre><button class="copy" type="button" data-copy="cmd-validate">Copy</button></div>
          <div class="command"><pre id="cmd-tests">python -m pytest tests/test_classical_baseline_suite.py</pre><button class="copy" type="button" data-copy="cmd-tests">Copy</button></div>
        </div>
        <aside class="note">
          <p><code>validate</code> checks every candidate and experiment against its proof obligations. GitHub Actions runs the same check on every push.</p>
          <p>The test file runs the classical baseline attacks on small instances. More commands are on <a href="how-it-works.html#commands">How it works</a>.</p>
        </aside>
      </div>
    </section>

    <section class="section" id="cite">
      <div class="wrap">
        <div class="section-head">
          <h2>Cite</h2>
          <p>If you use the negative results or the attack code, please cite the project.</p>
        </div>
        <div class="command"><pre id="bibtex">@misc{sands2026qsearch,
  author       = {Sands, Jasper},
  title        = {Q-Search: an open search for structural quantum speedups},
  year         = {2026},
  howpublished = {\url{https://qsearch.jaspersands.com}}
}</pre><button class="copy" type="button" data-copy="bibtex">Copy</button></div>
      </div>
    </section>

    <section class="section" id="about">
      <div class="wrap">
        <div class="section-head">
          <h2>About</h2>
        </div>
        <div class="prose">
          <p id="execution-model">Research runs in interactive sessions. A GitHub workflow validates every pushed snapshot.</p>
          <p>Q-Search is built and directed by Jasper Sands. The code, the data, and every negative result are public on <a href="https://github.com/Jaspersands/qsearch">GitHub</a>.</p>
        </div>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="wrap footer-inner">
      <p>Q-Search is an open research project by Jasper Sands. Data updated <time data-updated>recently</time>.</p>
      <p><a href="https://github.com/Jaspersands/qsearch">Source on GitHub</a> · <a href="index.html#cite">Cite</a></p>
    </div>
  </footer>
</body>
</html>
```

- [ ] **Step 2: Write the page script**

Create `site/js/home.js`:

```js
import { SNAPSHOT_PATH, bindCopyButtons, initFooter, loadJson, setText, showLoadError } from "./common.js";
import { bibtexEntry, escapeHtml, formatDate, formatNumber, statusMarker, trackStatusKind } from "./lib/format.js";
import { activityChart } from "./lib/chart.js";

const ACTIVITY_PATH = "site/data/activity.json";
const CHANGELOG_PATH = "site/data/changelog.json";
const CHANGELOG_PREVIEW = 6;

function renderIntro(snapshot) {
  setText("verdict-title", `${snapshot.verdict.title}.`);
  setText("verdict-detail", snapshot.verdict.detail);
  setText("snapshot-date", formatDate(snapshot.updated_at));
  setText("fig-negatives", formatNumber(snapshot.metrics.negative_results));
  setText("fig-experiments", formatNumber(snapshot.metrics.experiments));
  setText("fig-debts", formatNumber(snapshot.metrics.proof_debts));
}

function trackRow(track) {
  return `<details class="row">
    <summary>
      <span class="row-title">${escapeHtml(track.title)}</span>
      <span class="row-summary">${escapeHtml(track.status)}<span class="row-next">Next: ${escapeHtml(track.next)}</span></span>
      ${statusMarker(trackStatusKind(track.tone))}
    </summary>
    <div class="row-body">
      <p>${escapeHtml(track.summary)}</p>
      <dl class="facts"><dt>Evidence</dt><dd>${escapeHtml(track.evidence)}</dd></dl>
    </div>
  </details>`;
}

function renderMilestones(milestones) {
  document.getElementById("milestones").innerHTML = milestones
    .map((item) => `<li><h3>${escapeHtml(item.title)}</h3><p>${escapeHtml(item.detail)}</p></li>`)
    .join("");
}

function changelogItem(entry) {
  const changes = entry.changes.map((change) => `<li>${escapeHtml(change)}</li>`).join("");
  return `<li><time datetime="${escapeHtml(entry.date)}">${escapeHtml(formatDate(entry.date))}</time><ul>${changes}</ul></li>`;
}

function renderChangelog(changelog) {
  const list = document.getElementById("changelog");
  const button = document.getElementById("changelog-more");
  const entries = changelog.entries;
  const draw = (all) => {
    list.innerHTML = entries.slice(0, all ? entries.length : CHANGELOG_PREVIEW).map(changelogItem).join("");
  };
  draw(false);
  if (entries.length > CHANGELOG_PREVIEW) {
    button.textContent = `Show all ${formatNumber(entries.length)} changes`;
    button.hidden = false;
    button.addEventListener("click", () => {
      draw(true);
      button.hidden = true;
    });
  }
}

function main() {
  bindCopyButtons();
  const snapshotPromise = loadJson(SNAPSHOT_PATH);
  initFooter(snapshotPromise);

  snapshotPromise
    .then((snapshot) => {
      renderIntro(snapshot);
      document.getElementById("track-rows").innerHTML = snapshot.tracks.map(trackRow).join("");
      renderMilestones(snapshot.milestones);
      setText("bibtex", bibtexEntry(snapshot));
      setText("execution-model", snapshot.execution_model);
    })
    .catch(() => {
      setText("verdict-detail", "The latest snapshot couldn't load.");
      showLoadError(document.getElementById("track-rows"), SNAPSHOT_PATH);
      showLoadError(document.getElementById("milestones"), SNAPSHOT_PATH);
    });

  const changelogPromise = loadJson(CHANGELOG_PATH);
  Promise.all([loadJson(ACTIVITY_PATH), changelogPromise])
    .then(([activity, changelog]) => {
      document.getElementById("activity-chart").innerHTML = activityChart({
        weeks: activity.weeks,
        points: changelog.points,
      });
    })
    .catch(() => showLoadError(document.getElementById("activity-chart"), ACTIVITY_PATH));
  changelogPromise
    .then(renderChangelog)
    .catch(() => showLoadError(document.getElementById("changelog"), CHANGELOG_PATH));
}

main();
```

- [ ] **Step 3: Delete the old script**

Run: `cd "/Users/jaspersands/Desktop/quantum algorithm search" && git rm -q site/progress.js`

- [ ] **Step 4: Verify**

Run:
```bash
cd "/Users/jaspersands/Desktop/quantum algorithm search" && /Users/jaspersands/.nvm/versions/node/v24.18.0/bin/node --check site/js/home.js && /opt/anaconda3/bin/python3 tools/check_site.py | grep "^index.html"; /opt/anaconda3/bin/python3 tools/site_smoke.py --pages index.html --no-redirects --out /private/tmp/claude-501/-Users-jaspersands-Desktop-quantum-algorithm-search/bd8c9228-91bd-497e-a749-a904429b7c83/scratchpad/shots-new
```
Expected: the only `index.html` checker line is `index.html: links to missing page open-problems.html` (created in Task 7); no missing files and no hardcoded metrics. Smoke: `Smoke checks passed.` Read `index-1440.png` and `index-390.png`: verdict in accent color with the date in the margin note; three figures filled with real numbers; three track rows with status markers (Cosets = active, DHSP and Codes = open); chart with bars and an accent line ending in the current negative count; milestones; six changelog entries with a "Show all" button; no horizontal scroll at 390 px. Also open the page in the browser pane, click a track row and the "Show all" button, and confirm they work.

- [ ] **Step 5: Commit**

```bash
cd "/Users/jaspersands/Desktop/quantum algorithm search" && git add index.html site/js/home.js && git commit -m "Rebuild the home page on registry data and remove the simulated widgets

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 7: Open problems page

**Files:**
- Create: `open-problems.html`
- Create: `site/js/open-problems.js`

**Interfaces:**
- Consumes: `loadJson`, `showLoadError`, `setText`, `initFooter` from `common.js`; `escapeHtml`, `formatDate`, `formatNumber`, `humanizeId`, `statusMarker` from `format.js`; `groupDebts` from `debts.js`; `research/frontier_map.json` (`created_at`, `frontiers[].{frontier_id, priority_score, status, why_it_matters, next_experiment, required_new_capability: string[], kill_criteria: string[], evidence: string}`); `research/proof_debt_report.json` (`proof_debts[].{id, candidate_id, debt_type, claim_blocked, priority_score, required_resolution, evidence}`).

- [ ] **Step 1: Write the page**

Create `open-problems.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Open problems · Q-Search</title>
  <meta name="description" content="The research frontiers Q-Search is working on now, and the proofs still missing before any idea could be called a speedup.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Schibsted+Grotesk:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap">
  <link rel="stylesheet" href="site/styles.css">
  <script type="module" src="site/js/open-problems.js"></script>
</head>
<body>
  <header class="site-header">
    <div class="wrap header-inner">
      <a class="wordmark" href="index.html">Q-Search</a>
      <nav aria-label="Site">
        <a href="index.html">Home</a>
        <a href="open-problems.html" aria-current="page">Open problems</a>
        <a href="negative-results.html">Negative results</a>
        <a href="how-it-works.html">How it works</a>
      </nav>
      <a class="header-github" href="https://github.com/Jaspersands/qsearch">GitHub</a>
    </div>
  </header>

  <main>
    <div class="wrap page-head">
      <h1>Open problems</h1>
      <div class="prose">
        <p>What we're working on now, ranked by priority, and the proofs still missing before any idea here could be called a speedup.</p>
      </div>
    </div>

    <section class="section" id="frontiers">
      <div class="wrap with-notes">
        <div>
          <div class="section-head">
            <h2>Research frontiers</h2>
            <p>Each frontier is a line of work with a next experiment and a list of conditions that would end it. Open one for details.</p>
          </div>
        </div>
        <aside class="note">
          <p>Ranked on <span id="frontier-date">the date in the file</span> from the current blockers.</p>
          <p>Source: <a href="https://github.com/Jaspersands/qsearch/blob/main/research/frontier_map.json"><code>frontier_map.json</code></a>.</p>
        </aside>
      </div>
      <div class="wrap">
        <div class="rows" id="frontier-rows"></div>
      </div>
    </section>

    <section class="section" id="proof-debts">
      <div class="wrap with-notes">
        <div>
          <div class="section-head">
            <h2>Proof debts</h2>
            <p>A proof debt is a proof that has to exist before a claim can be made. There are <span id="debt-count">several</span> open, grouped by what kind of proof is missing.</p>
          </div>
          <div class="field">
            <label for="debt-candidate">Candidate</label>
            <select id="debt-candidate"><option value="">All candidates</option></select>
          </div>
        </div>
        <aside class="note">
          <p>Source: <a href="https://github.com/Jaspersands/qsearch/blob/main/research/proof_debt_report.json"><code>proof_debt_report.json</code></a>.</p>
        </aside>
      </div>
      <div class="wrap" id="debt-groups"></div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="wrap footer-inner">
      <p>Q-Search is an open research project by Jasper Sands. Data updated <time data-updated>recently</time>.</p>
      <p><a href="https://github.com/Jaspersands/qsearch">Source on GitHub</a> · <a href="index.html#cite">Cite</a></p>
    </div>
  </footer>
</body>
</html>
```

- [ ] **Step 2: Write the page script**

Create `site/js/open-problems.js`:

```js
import { initFooter, loadJson, setText, showLoadError } from "./common.js";
import { escapeHtml, formatDate, formatNumber, humanizeId, statusMarker } from "./lib/format.js";
import { groupDebts } from "./lib/debts.js";

const FRONTIERS_PATH = "research/frontier_map.json";
const DEBTS_PATH = "research/proof_debt_report.json";
const DEBT_TYPES = {
  dequantization: ["Dequantization", "A classical method may already match the idea."],
  "reduction-route": ["Reduction route", "The link between the idea and the real problem isn't proved yet."],
  falsifier: ["Falsifiers", "A known test already rejects the idea in its current form."],
};

function asList(value) {
  if (Array.isArray(value)) return value;
  return value ? [value] : [];
}

function listItems(values) {
  return values.map((value) => `<li>${escapeHtml(value)}</li>`).join("");
}

function frontierRow(frontier) {
  const needs = asList(frontier.required_new_capability);
  const kills = asList(frontier.kill_criteria);
  return `<details class="row" id="${escapeHtml(frontier.frontier_id)}">
    <summary>
      <span class="row-title">${escapeHtml(humanizeId(frontier.frontier_id))}</span>
      <span class="row-summary">${escapeHtml(frontier.why_it_matters)}</span>
      ${statusMarker("open")}
    </summary>
    <div class="row-body">
      <dl class="facts">
        <dt>Priority</dt><dd class="num">${formatNumber(frontier.priority_score)}</dd>
        <dt>State</dt><dd><code>${escapeHtml(frontier.status)}</code></dd>
        <dt>Next experiment</dt><dd>${escapeHtml(frontier.next_experiment)}</dd>
      </dl>
      ${needs.length ? `<h4>What it needs</h4><ul>${listItems(needs)}</ul>` : ""}
      ${kills.length ? `<details class="sub"><summary>Kill criteria (${kills.length})</summary><ul>${listItems(kills)}</ul></details>` : ""}
      <details class="sub"><summary>Evidence so far</summary><p class="small">${escapeHtml(asList(frontier.evidence).join(" "))}</p></details>
    </div>
  </details>`;
}

function debtRow(debt, sharedResolution) {
  const ownResolution = sharedResolution ? "" : `<p class="small">To close: ${escapeHtml(debt.required_resolution)}</p>`;
  return `<tr>
    <td class="id" data-label="Candidate">${escapeHtml(debt.candidate_id)}</td>
    <td data-label="Blocks"><code>${escapeHtml(debt.claim_blocked)}</code></td>
    <td class="num" data-label="Priority">${formatNumber(debt.priority_score)}</td>
    <td data-label="Evidence"><details class="sub"><summary>Show</summary><p class="small">${escapeHtml(debt.evidence)}</p></details>${ownResolution}</td>
  </tr>`;
}

function debtGroup(group) {
  const [label, explanation] = DEBT_TYPES[group.type] || [humanizeId(group.type), ""];
  const shared = group.resolution ? ` To close: ${escapeHtml(group.resolution)}` : "";
  return `<section class="debt-group">
    <h3>${escapeHtml(label)} <span class="muted num">${formatNumber(group.debts.length)}</span></h3>
    <p class="muted">${escapeHtml(explanation)}${shared}</p>
    <table class="table">
      <thead><tr><th>Candidate</th><th>Blocks</th><th>Priority</th><th>Evidence</th></tr></thead>
      <tbody>${group.debts.map((debt) => debtRow(debt, group.resolution)).join("")}</tbody>
    </table>
  </section>`;
}

function renderFrontiers(data) {
  const frontiers = [...data.frontiers].sort((a, b) => b.priority_score - a.priority_score);
  setText("frontier-date", formatDate(data.created_at));
  document.getElementById("frontier-rows").innerHTML = frontiers.map(frontierRow).join("");
}

function renderDebts(report) {
  const debts = report.proof_debts;
  const select = document.getElementById("debt-candidate");
  const container = document.getElementById("debt-groups");
  setText("debt-count", formatNumber(debts.length));
  const candidates = [...new Set(debts.map((debt) => debt.candidate_id))].sort();
  select.insertAdjacentHTML(
    "beforeend",
    candidates.map((id) => `<option value="${escapeHtml(id)}">${escapeHtml(id)}</option>`).join(""),
  );
  const render = () => {
    const shown = select.value ? debts.filter((debt) => debt.candidate_id === select.value) : debts;
    container.innerHTML = groupDebts(shown).map(debtGroup).join("");
  };
  select.addEventListener("change", render);
  render();
}

function main() {
  initFooter();
  loadJson(FRONTIERS_PATH)
    .then(renderFrontiers)
    .catch(() => showLoadError(document.getElementById("frontier-rows"), FRONTIERS_PATH));
  loadJson(DEBTS_PATH)
    .then(renderDebts)
    .catch(() => showLoadError(document.getElementById("debt-groups"), DEBTS_PATH));
}

main();
```

- [ ] **Step 3: Verify**

Run:
```bash
cd "/Users/jaspersands/Desktop/quantum algorithm search" && /Users/jaspersands/.nvm/versions/node/v24.18.0/bin/node --check site/js/open-problems.js && /opt/anaconda3/bin/python3 tools/check_site.py | grep "open-problems"; /opt/anaconda3/bin/python3 tools/site_smoke.py --pages open-problems.html --no-redirects --out /private/tmp/claude-501/-Users-jaspersands-Desktop-quantum-algorithm-search/bd8c9228-91bd-497e-a749-a904429b7c83/scratchpad/shots-new
```
Expected: no `open-problems` lines (the old `negative-results.html` still exists until Task 8 rewrites it). Smoke passes. Read both screenshots: five frontier rows ordered 158, 110, 94, 82, 70 (values at time of writing); three debt groups of eight with the shared "To close" sentence once per group, not per row; at 390 px the debt table stacks into labelled rows with no horizontal scroll. In the browser pane, pick a candidate in the select and confirm the groups filter.

- [ ] **Step 4: Commit**

```bash
cd "/Users/jaspersands/Desktop/quantum algorithm search" && git add open-problems.html site/js/open-problems.js && git commit -m "Add Open problems page merging frontiers and proof debts

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 8: Negative results page

**Files:**
- Rewrite: `negative-results.html` (replace the whole file)
- Create: `site/js/negative-results.js`

**Interfaces:**
- Consumes: `loadJson`, `showLoadError`, `setText`, `initFooter` from `common.js`; `escapeHtml`, `formatNumber`, `repoUrl` from `format.js`; `filterRecords`, `recordIdFromHash` from `negatives.js`; `site/data/negatives.json` (Task 1 shape).

- [ ] **Step 1: Write the page**

Overwrite `negative-results.html` with:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Negative results · Q-Search</title>
  <meta name="description" content="Every idea Q-Search has ruled out, with the reason it failed and what it taught us. Searchable, with a link for each result.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Schibsted+Grotesk:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap">
  <link rel="stylesheet" href="site/styles.css">
  <script type="module" src="site/js/negative-results.js"></script>
</head>
<body>
  <header class="site-header">
    <div class="wrap header-inner">
      <a class="wordmark" href="index.html">Q-Search</a>
      <nav aria-label="Site">
        <a href="index.html">Home</a>
        <a href="open-problems.html">Open problems</a>
        <a href="negative-results.html" aria-current="page">Negative results</a>
        <a href="how-it-works.html">How it works</a>
      </nav>
      <a class="header-github" href="https://github.com/Jaspersands/qsearch">GitHub</a>
    </div>
  </header>

  <main>
    <div class="wrap page-head with-notes">
      <div>
        <h1>Negative results</h1>
        <div class="prose">
          <p>Every idea we've ruled out, with the reason it failed and what it taught us. There are <span id="nr-total">hundreds of</span> records. Each one has its own link, so you can point someone at a single dead end.</p>
        </div>
      </div>
      <aside class="note">
        <p>Source: <a href="https://github.com/Jaspersands/qsearch/blob/main/research/registry/negative_results.json"><code>negative_results.json</code></a>, the full registry. This page reads a smaller copy built by <a href="https://github.com/Jaspersands/qsearch/blob/main/tools/build_site_data.py"><code>build_site_data.py</code></a>.</p>
      </aside>
    </div>

    <section class="wrap" id="registry">
      <label class="visually-hidden" for="nr-search">Search negative results</label>
      <input class="search" id="nr-search" type="search" placeholder="Try “Goppa”, “sieve”, or “decoder”" autocomplete="off">
      <div class="filters" id="nr-tags" role="group" aria-label="Filter by line of research"></div>
      <p class="result-count" id="nr-count" aria-live="polite"></p>
      <div class="rows" id="nr-rows"></div>
      <button class="button" type="button" id="nr-more" hidden>Show more</button>
    </section>
  </main>

  <footer class="site-footer">
    <div class="wrap footer-inner">
      <p>Q-Search is an open research project by Jasper Sands. Data updated <time data-updated>recently</time>.</p>
      <p><a href="https://github.com/Jaspersands/qsearch">Source on GitHub</a> · <a href="index.html#cite">Cite</a></p>
    </div>
  </footer>
</body>
</html>
```

- [ ] **Step 2: Write the page script**

Create `site/js/negative-results.js`:

```js
import { initFooter, loadJson, setText, showLoadError } from "./common.js";
import { escapeHtml, formatNumber, repoUrl } from "./lib/format.js";
import { filterRecords, recordIdFromHash } from "./lib/negatives.js";

const DATA_PATH = "site/data/negatives.json";
const PAGE_SIZE = 40;

const state = { records: [], query: "", tag: "", shown: PAGE_SIZE };
const rowsEl = document.getElementById("nr-rows");
const tagsEl = document.getElementById("nr-tags");
const searchEl = document.getElementById("nr-search");
const moreEl = document.getElementById("nr-more");

function fileLink(path) {
  return `<a href="${repoUrl(path)}"><code>${escapeHtml(path)}</code></a>`;
}

function recordRow(record) {
  const facts = [
    ["Why it failed", escapeHtml(record.reason)],
    ["Lesson", escapeHtml(record.lesson)],
    ["Source", record.source_path ? fileLink(record.source_path) : `<code>${escapeHtml(record.source)}</code>`],
    ["Derivation", record.derivation_path ? fileLink(record.derivation_path) : ""],
    ["Data", record.artifact_path ? fileLink(record.artifact_path) : ""],
    ["Review", escapeHtml(record.review_status)],
  ];
  const list = facts
    .filter(([, value]) => value)
    .map(([label, value]) => `<dt>${label}</dt><dd>${value}</dd>`)
    .join("");
  return `<details class="row" id="${escapeHtml(record.id)}" data-id="${escapeHtml(record.id)}">
    <summary>
      <span class="row-title mono">${escapeHtml(record.id)}</span>
      <span class="row-summary">${escapeHtml(record.claim)}</span>
    </summary>
    <div class="row-body">
      <dl class="facts">${list}</dl>
      <p class="small"><a href="#${encodeURIComponent(record.id)}">Link to this result</a></p>
    </div>
  </details>`;
}

function render() {
  const matches = filterRecords(state.records, state);
  const visible = matches.slice(0, state.shown);
  rowsEl.innerHTML = visible.map(recordRow).join("");
  const filtered = matches.length !== state.records.length;
  setText(
    "nr-count",
    `Showing ${formatNumber(visible.length)} of ${formatNumber(matches.length)}` +
      (filtered ? ` matching results (${formatNumber(state.records.length)} in total)` : " results"),
  );
  moreEl.hidden = visible.length >= matches.length;
}

function setTag(tag) {
  state.tag = tag;
  for (const chip of tagsEl.querySelectorAll("button[data-tag]")) {
    chip.setAttribute("aria-pressed", String(chip.dataset.tag === tag));
  }
}

function renderTags(tags) {
  const chip = (id, label, count) =>
    `<button type="button" class="chip" data-tag="${escapeHtml(id)}" aria-pressed="${id === state.tag}">` +
    `${escapeHtml(label)}<span class="count">${formatNumber(count)}</span></button>`;
  tagsEl.innerHTML = [chip("", "All", state.records.length), ...tags.map((t) => chip(t.id, t.label, t.count))].join("");
  tagsEl.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-tag]");
    if (!button) return;
    setTag(button.dataset.tag);
    state.shown = PAGE_SIZE;
    render();
  });
}

function openFromHash() {
  const id = recordIdFromHash(location.hash);
  const index = state.records.findIndex((record) => record.id === id);
  if (index === -1) return;
  state.query = "";
  searchEl.value = "";
  setTag("");
  state.shown = Math.max(state.shown, Math.ceil((index + 1) / PAGE_SIZE) * PAGE_SIZE);
  render();
  const row = document.getElementById(id);
  if (row) {
    row.open = true;
    row.scrollIntoView({ block: "start" });
  }
}

function wireControls() {
  let timer;
  searchEl.addEventListener("input", () => {
    clearTimeout(timer);
    timer = setTimeout(() => {
      state.query = searchEl.value;
      state.shown = PAGE_SIZE;
      render();
    }, 120);
  });
  moreEl.addEventListener("click", () => {
    state.shown += PAGE_SIZE;
    render();
  });
  rowsEl.addEventListener(
    "toggle",
    (event) => {
      const row = event.target;
      if (row.matches("details.row") && row.open) {
        history.replaceState(null, "", `#${encodeURIComponent(row.dataset.id)}`);
      }
    },
    true,
  );
  window.addEventListener("hashchange", openFromHash);
}

function main() {
  initFooter();
  loadJson(DATA_PATH)
    .then((data) => {
      state.records = data.records;
      setText("nr-total", formatNumber(data.count));
      renderTags(data.tags);
      wireControls();
      render();
      openFromHash();
    })
    .catch(() => showLoadError(rowsEl, DATA_PATH));
}

main();
```

- [ ] **Step 3: Verify**

Run:
```bash
cd "/Users/jaspersands/Desktop/quantum algorithm search" && /Users/jaspersands/.nvm/versions/node/v24.18.0/bin/node --check site/js/negative-results.js && /opt/anaconda3/bin/python3 tools/check_site.py | grep -E "^(index|open-problems|negative-results|how-it-works)\.html|^site/"; /opt/anaconda3/bin/python3 tools/site_smoke.py --pages negative-results.html,index.html,open-problems.html,how-it-works.html --no-redirects --out /private/tmp/claude-501/-Users-jaspersands-Desktop-quantum-algorithm-search/bd8c9228-91bd-497e-a749-a904429b7c83/scratchpad/shots-new
```
Expected: no checker lines for the four new pages or `site/`. Smoke passes for all four pages. Read `negative-results-1440.png` and `-390.png`: search box, five chips (All plus four tracks, each with a count), "Showing 40 of N results", 40 one-line rows with mono IDs, a "Show more" button; long IDs wrap without overflow at 390 px. In the browser pane: type "goppa" (count drops), click "Dihedral sieve" (filters), open a row (URL hash updates), then load `negative-results.html#AFFINE-GEOMETRY-CODE-SEARCH-AG2_F2_K3` in a fresh tab and confirm that row opens and scrolls into view.

- [ ] **Step 4: Commit**

```bash
cd "/Users/jaspersands/Desktop/quantum algorithm search" && git add negative-results.html site/js/negative-results.js && git commit -m "Rebuild Negative results as a searchable list with per-result links

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 9: Redirects, CI, and final verification

**Files:**
- Replace: `methodology.html`, `repomap.html`, `frontier.html`, `proof-debt.html`
- Modify: `.github/workflows/validate.yml`
- Modify: `_config.yml`

**Interfaces:**
- Consumes: everything above. `tools/site_smoke.py` checks the redirect map `methodology.html → how-it-works.html`, `repomap.html → how-it-works.html`, `frontier.html → open-problems.html`, `proof-debt.html → open-problems.html`.

- [ ] **Step 1: Replace the four old pages with redirect stubs**

Run:
```bash
cd "/Users/jaspersands/Desktop/quantum algorithm search" && while read -r old new label; do
cat > "$old" <<EOF
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Moved to ${label//_/ } · Q-Search</title>
  <link rel="canonical" href="${new}">
  <meta http-equiv="refresh" content="0; url=${new}">
  <script>location.replace("${new}" + location.hash);</script>
</head>
<body>
  <p>This page moved to <a href="${new}">${label//_/ }</a>.</p>
</body>
</html>
EOF
done <<'LIST'
methodology.html how-it-works.html How_it_works
repomap.html how-it-works.html How_it_works
frontier.html open-problems.html Open_problems
proof-debt.html open-problems.html Open_problems
LIST
cat frontier.html
```
Expected: `frontier.html` contains `url=open-problems.html` and the text "This page moved to Open problems".

- [ ] **Step 2: Update the Pages include list**

Overwrite `_config.yml` with:

```yaml
exclude:
  - core/
  - theorems/
  - tests/
  - tools/
  - .agents/
  - .gemini/
  - ag-remote/
  - "*.py"
include:
  - index.html
  - open-problems.html
  - negative-results.html
  - how-it-works.html
  - methodology.html
  - repomap.html
  - frontier.html
  - proof-debt.html
  - site/
  - research/
```

(The site is served with `.nojekyll`, so Jekyll doesn't read this file today; the list is kept accurate so enabling Jekyll later wouldn't hide `research/` JSON the pages fetch.)

- [ ] **Step 3: Update CI**

In `.github/workflows/validate.yml`, replace the final step

```yaml
      - name: Check website JavaScript
        run: node --check site/progress.js
```

with:

```yaml
      - uses: actions/setup-node@v4
        with:
          node-version: "22"
      - name: Check website JavaScript
        run: |
          for file in site/js/*.js site/js/lib/*.js; do node --check "$file"; done
          node --test tests/js/*.test.mjs
      - name: Verify website data and references
        run: |
          python -m pip install pytest
          python -m pytest tests/test_build_site_data.py tests/test_check_site.py -q
          python tools/build_site_data.py --skip-changelog
          git diff --exit-code site/data/activity.json site/data/negatives.json
          python -c "import json; json.load(open('site/data/changelog.json'))"
          python tools/check_site.py
```

Note: `tests/test_build_site_data.py::SnapshotVersionsTests` creates its own temporary git repository, so it works on CI's shallow checkout.

- [ ] **Step 4: Run every check locally**

Run:
```bash
cd "/Users/jaspersands/Desktop/quantum algorithm search" && \
/opt/anaconda3/bin/python3 -m pytest tests/test_build_site_data.py tests/test_check_site.py -q && \
/Users/jaspersands/.nvm/versions/node/v24.18.0/bin/node --test tests/js/*.test.mjs && \
for f in site/js/*.js site/js/lib/*.js; do /Users/jaspersands/.nvm/versions/node/v24.18.0/bin/node --check "$f" || exit 1; done && \
/opt/anaconda3/bin/python3 tools/build_site_data.py --skip-changelog && git diff --exit-code site/data/activity.json site/data/negatives.json && \
/opt/anaconda3/bin/python3 tools/check_site.py && \
/opt/anaconda3/bin/python3 tools/site_smoke.py --out /private/tmp/claude-501/-Users-jaspersands-Desktop-quantum-algorithm-search/bd8c9228-91bd-497e-a749-a904429b7c83/scratchpad/shots-final
```
Expected: pytest `19 passed`; node tests `# fail 0`; no diff; `Site checks passed.`; `Smoke checks passed.` (8 page renders plus 4 redirects). If `git diff` shows changes because the registries moved since Task 1, rebuild with `/opt/anaconda3/bin/python3 tools/build_site_data.py` and commit the regenerated data in this task.

- [ ] **Step 5: Final review against the spec**

Read all eight screenshots in `shots-final/`. For each page confirm, and fix anything that fails before committing:
- No eyebrow labels, all-caps mono labels, shadows, gradients, drop caps, terminal chrome, or pill badges (only the dot-plus-word status marker and the square-cornered filter chips).
- Every visible number is real and has a date or source nearby.
- No banned words: run `grep -inE "monograph|protocol apg|rigorous|first-class|certified|peer-verifiable|deterministic audit|executive abstract|laboratory" *.html site/js/*.js site/js/lib/*.js` and expect no output.
- Mobile (390 px): header fits on two lines at most, figures fit, rows and tables stack, nothing scrolls sideways.

- [ ] **Step 6: Commit**

```bash
cd "/Users/jaspersands/Desktop/quantum algorithm search" && git add methodology.html repomap.html frontier.html proof-debt.html _config.yml .github/workflows/validate.yml site/data && git commit -m "Redirect old pages, update Pages config, and check the site in CI

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

## Spec coverage

| Spec requirement | Task |
| --- | --- |
| Anti-slop rules, tokens, typefaces, margin notes | 5 (CSS), applied in 5–8, reviewed in 9 |
| Status vocabulary (open / ruled out / active) | 4 (`statusMarker`), 5 (CSS), 6–8 |
| Home: intro, tracks, activity, results, changelog, reproduce/cite, about | 6 |
| Open problems: ranked frontiers, grouped proof debts, candidate filter | 7 |
| Negative results: search, tag chips, expandable rows, permalinks, paging | 8 |
| How it works: loop, terms, repo map, commands, limits | 5 |
| Redirects for old URLs | 9 |
| `tools/build_site_data.py` with activity, changelog, negatives, `--skip-changelog` | 1, 2 |
| No hardcoded counts; all referenced paths exist | 3 (checker), 6–9 |
| Load-failure message instead of permanent loading | 5 (`showLoadError`), 6–8, smoke "Loading" check |
| Playwright screenshots at 1440 and 390, overflow, console errors, redirects | 3 (tool), 5–9 |
| CI: node checks, data diff, changelog parse, checker | 9 |
| Simulated widgets removed | 6 (`site/progress.js` deleted, index rewritten) |

---

## Addendum: circuit identity and negative-results map (spec revision b)

Same global constraints as above, with one override: the negative-results map may use per-track colors (`#3b6ea5` codes and cosets, `#c2410c` dihedral sieve, `#6b8e23` hidden-shift literature, `#8e5ea2` coset-observables literature, `#9ca3af` other). Each task follows red → green → verify → commit.

### Task 10: Circuit plan and SVG module

**Files:** create `site/js/lib/circuit.js`, `tests/js/circuit.test.mjs`.

**Interfaces (exports):**
- `STAGES = ["hypothesis", "structure", "classical attack", "proof gate", "separation"]`
- `wirePlan(tracks) -> [{label, active, solidTo, endsAt}]` — `label = short_title || title`; stage clamped to 0–3. Non-active: `solidTo = endsAt = min(stage + 1, 3)`. Active: `solidTo = stage`, `endsAt = null`.
- `aliveAt(wire, gate) -> boolean` — `wire.active || gate <= wire.endsAt`.
- `wireExtents(plan, gateYs, width) -> [{x, end}]` — x evenly spaced with 22 px margins; `end` = meter top (`gateYs[endsAt] + 30`) for ended wires, `gateYs[4]` for active ones.
- `circuitSvg({plan, gateYs, height, width}) -> string` — vertical circuit: labels at top, solid wires, `wire-live` overlay lines (`data-wire=i`, initially zero length), dashed continuation (`wire-dash`) for active wires, one `gate` box per stage spanning only alive wires (stage names; single letters H S A P when `width < 100`; last gate always "?"), one `meter` per ended wire, one `circuit-dot` on the first active wire.
- `circuitStrip({plan, width, height = 64}) -> string` — horizontal version for page headers: wire labels at left, gates as evenly spaced faint ticks with stage names (class `strip-stage`), meters where wires end, dashed continuation and a "?" box for active wires.

**Tests first:** snapshot-shaped tracks (Codes stage 1 blocked, DHSP stage 2 blocked, Cosets stage 3 active) give `solidTo/endsAt` = 2/2, 3/3, 3/null; a blocked stage-3 track caps at 3; `aliveAt` truth table; `circuitSvg` has 5 gate boxes, 2 meters, 1 dashed line, 1 dot, gate 3 box spans only wires 0 and 2 (check its x and width against `wireExtents`), short labels at width 60; `circuitStrip` has 2 meters and 1 "?" box.

### Task 11: Circuit on the home page, strip on other pages

**Files:** modify `index.html`, `site/js/home.js`, `site/js/common.js`, `site/styles.css`, `open-problems.html`, `negative-results.html`, `how-it-works.html`, `site/js/open-problems.js`, `site/js/negative-results.js`.

- Home: add `class="has-circuit"` to `<body>` and an absolutely positioned `<svg class="circuit-svg" id="circuit">` inside `<main>` (`main` gets `position: relative`). `.has-circuit main .wrap` gets extra left padding equal to the gutter (150 px; 60 px below 760 px). Gate y positions: the intro `h1` and the `h2` of `#tracks`, `#activity`, `#results` (offset relative to `main`, +18 px), separation = `main.offsetHeight - 48`. The SVG's left edge aligns with the first `.wrap`'s content box. Redraw on a debounced `ResizeObserver` of `main` (content height changes as data loads). Scroll handler sets each `wire-live` `y2` to `min(end, scrollProgressY)` and moves the dot along the active wire; skipped entirely under `prefers-reduced-motion`.
- "ideas ruled out" figure becomes a link to `negative-results.html#map` (no underline; underline on the label on hover).
- `common.js` gains `initCircuitStrip(snapshotPromise)`: fills `#circuit-strip` (a `<div>` under the header) with `circuitStrip` at the container's width, redrawn on resize. Open problems, Negative results, and How it works share one snapshot promise between the footer and the strip.
- Verify: smoke at 1440/390 (no overflow, no errors), screenshots reviewed; wires end at Activity (Codes) and Results (DHSP); Cosets dashed to the "?" gate above the footer.

### Task 12: Negative-results map builder

**Files:** create `tools/build_negative_map.py`, `tests/test_build_negative_map.py`; generate `site/data/negative_map.json`.

- `build_map(records, seed=7, regions=9) -> {"points": [{id, x, y}], "regions": [{x, y, label, count}]}`: TF-IDF (id words + claim + reason, English stop words, `min_df=min(3, n)`, `max_df=0.4` only when n ≥ 50) → `TruncatedSVD(min(40, features - 1))` → row-normalise → `TSNE(perplexity=min(30, max(5, (n - 1) // 3)), init="pca", metric="cosine", random_state=seed)` → scale to [0, 1] → `KMeans(min(regions, n))` → label each region with the highest-mean claim bigram not in a generic-phrase list and not already used. Coordinates rounded to 4 places.
- `main(argv)` with `--root`; writes compact JSON. Imports scikit-learn lazily so `py_compile` in CI needs no extra dependency.
- Tests (skipped when scikit-learn is missing): 60 synthetic records in two vocabularies → 60 points in [0, 1]; with `regions=2`, 2 distinct non-empty labels; the two topics' centroids are more than 0.2 apart.

### Task 13: Map on the Negative results page

**Files:** create `site/js/lib/map.js`, `tests/js/map.test.mjs`; modify `negative-results.html`, `site/js/negative-results.js`, `site/styles.css`, `.github/workflows/validate.yml`.

- `map.js` exports `TRACK_COLORS`, `trackOf(tags)` (priority: the two literature tags, then dihedral sieve, then codes and cosets, else `OTHER`), `projectPoints(points, width, height, pad) -> [[x, y]]`, `nearestIndex(screen, mx, my, include, maxDist = 10) -> index | -1`. Tests cover each.
- Page: `<section id="map">` with a canvas (560 px tall desktop, 380 px mobile), region labels, hover tooltip (id + claim), and a note "N records aren't on the map yet" when coordinates are missing. Filter chips gain a color swatch (they double as the legend) and a "Grey: other" note. Points not in the current matches are drawn at 12% opacity. Clicking a point: if the record is in the current matches, page the list to it, open it, scroll to it, and update the hash; otherwise fall back to the existing hash behaviour (clear filters). If `negative_map.json` fails to load, the map section is hidden and the list works as before.
- CI: parse-check `site/data/negative_map.json`.
- Final verification: all Python and Node tests, `check_site.py`, smoke at both widths with redirects, screenshot review against the spec, then the full-suite comparison with `main` before offering to land the branch.
