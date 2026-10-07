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
