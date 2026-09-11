import os
import tempfile
import threading
import time
import unittest
from pathlib import Path

from research_registry import (
    _read_json,
    _write_json,
    initialize_seed_registry,
    load_candidates,
    load_experiments,
    save_candidates,
    save_experiments,
)


class ResearchRegistryIOTests(unittest.TestCase):
    def test_write_json_is_atomic_and_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "registry.json"
            _write_json(path, [{"id": "a", "value": 1}])

            self.assertEqual(_read_json(path, []), [{"id": "a", "value": 1}])
            self.assertFalse(list(Path(tmp).glob(".registry.json.*.tmp")))

    def test_read_json_retries_transient_empty_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "registry.json"
            path.write_text("")

            def repair_file() -> None:
                time.sleep(0.03)
                _write_json(path, [{"id": "repaired"}])

            thread = threading.Thread(target=repair_file)
            thread.start()
            try:
                self.assertEqual(_read_json(path, [], retries=10, delay_seconds=0.01), [{"id": "repaired"}])
            finally:
                thread.join()

    def test_non_overwrite_refreshes_candidates_but_preserves_experiment_records(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                candidates = load_candidates()
                hidden = next(item for item in candidates if item["id"] == "DHS-GOWERS-SIEVE")
                hidden["title"] = "stale evaluator-era title"
                hidden["experiment_ids"].append("EXP-LOCAL-EXTRA")
                save_candidates(candidates)
                experiments = load_experiments()
                phase = next(item for item in experiments if item["id"] == "EXP-DHS-PHASE-SIEVE")
                phase["protocol"] = "reviewed current experiment protocol"
                phase["status"] = "blocked-after-falsifier"
                phase["metrics"] = ["new-structural-measurement"]
                save_experiments(experiments)

                initialize_seed_registry(overwrite=False)
                refreshed_hidden = next(item for item in load_candidates() if item["id"] == "DHS-GOWERS-SIEVE")
                refreshed_phase = next(item for item in load_experiments() if item["id"] == "EXP-DHS-PHASE-SIEVE")
            finally:
                os.chdir(old_cwd)

        self.assertEqual(refreshed_hidden["title"], "State-sample-native generic DCP sieve and decoder")
        self.assertIn("EXP-LOCAL-EXTRA", refreshed_hidden["experiment_ids"])
        self.assertEqual(refreshed_phase["protocol"], "reviewed current experiment protocol")
        self.assertEqual(refreshed_phase["status"], "blocked-after-falsifier")
        self.assertEqual(refreshed_phase["metrics"], ["new-structural-measurement"])

    def test_missing_seed_experiment_is_inserted_without_rewriting_existing_records(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiments = load_experiments()
                removed = experiments.pop()
                experiments[0]["protocol"] = "preserved local research record"
                save_experiments(experiments)
                initialize_seed_registry(overwrite=False)
                restored = {record["id"]: record for record in load_experiments()}
                initialize_seed_registry(overwrite=False)
                self.assertEqual(restored, {record["id"]: record for record in load_experiments()})
                self.assertEqual(restored[removed["id"]], removed)
                self.assertEqual(restored[experiments[0]["id"]]["protocol"], "preserved local research record")
            finally:
                os.chdir(old_cwd)


if __name__ == "__main__":
    unittest.main()
