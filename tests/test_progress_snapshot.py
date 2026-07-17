import unittest

from tools.build_progress_snapshot import build_snapshot, latest_artifact_date


class ProgressSnapshotTests(unittest.TestCase):
    def test_latest_artifact_date_is_data_driven(self) -> None:
        self.assertEqual(
            latest_artifact_date(
                {"created_at": "2025-01-01T12:00:00+00:00"},
                [{"updated_at": "2025-02-03T04:05:06Z"}],
            ),
            "2025-02-03",
        )

    def test_snapshot_is_curated_and_research_gated(self) -> None:
        snapshot = build_snapshot()

        self.assertEqual(len(snapshot["tracks"]), 3)
        self.assertLessEqual(len(snapshot["milestones"]), 5)
        self.assertEqual(len(snapshot["next_actions"]), 3)
        self.assertIn("No breakthrough", snapshot["verdict"]["title"])
        self.assertGreater(snapshot["metrics"]["blocking_findings"], 0)
        self.assertIn("interactively", snapshot["execution_model"])


if __name__ == "__main__":
    unittest.main()
