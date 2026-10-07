import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

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
            self.assertEqual(main(["--root", str(root), "--skip-changelog"]), 0)
            activity = json.loads((root / "site" / "data" / "activity.json").read_text())
            self.assertEqual(activity["total_runs"], 1)
            negatives = json.loads((root / "site" / "data" / "negatives.json").read_text())
            self.assertEqual(negatives["count"], 1)
            self.assertFalse((root / "site" / "data" / "changelog.json").exists())


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

            dated = dict(snapshot(negatives=3), updated_at="2026-07-20")
            path.write_text(json.dumps(dated))
            self.git(root, "commit", "-q", "-am", "three", when="2026-07-21T12:00:00+00:00")
            self.assertEqual(snapshot_versions(root)[-1]["date"], "2026-07-20")

            (root / "research" / "experiment_run_history.json").write_text("[]")
            (root / "research" / "registry").mkdir()
            (root / "research" / "registry" / "negative_results.json").write_text("[]")
            self.assertEqual(main(["--root", str(root)]), 0)
            changelog = json.loads((root / "site" / "data" / "changelog.json").read_text())
            self.assertEqual(len(changelog["points"]), 3)


if __name__ == "__main__":
    unittest.main()
