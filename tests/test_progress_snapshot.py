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
        self.assertIn("Spectral packing", snapshot["overview"])
        self.assertIn("unknown centralizer", snapshot["tracks"][2]["summary"])
        self.assertIn("No efficient high-coverage", snapshot["tracks"][0]["summary"])
        self.assertIn("exponential references", snapshot["tracks"][0]["evidence"])
        self.assertIn("logical target effect", snapshot["next_actions"][0]["title"])
        self.assertLessEqual(len(snapshot["active_conjecture"]["facts"]), 6)
        self.assertNotIn("Attack the all-n separator", str(snapshot))


if __name__ == "__main__":
    unittest.main()


def test_missing_pairing_artifact_does_not_claim_controls_checked(monkeypatch):
    import tools.build_progress_snapshot as snapshot
    real_read = snapshot.read_json
    def without_pairing(path, fallback):
        return {} if path.name == "dcp_coherent_matching_interface.json" else real_read(path, fallback)
    monkeypatch.setattr(snapshot, "read_json", without_pairing)
    assert "not run or failing" in snapshot.build_snapshot()["tracks"][0]["status"]
