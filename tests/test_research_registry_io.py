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

    def test_non_overwrite_initialization_refreshes_seed_definitions(self):
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
                phase["protocol"] = "stale deterministic subtraction"
                save_experiments(experiments)

                initialize_seed_registry(overwrite=False)
                refreshed_hidden = next(item for item in load_candidates() if item["id"] == "DHS-GOWERS-SIEVE")
                refreshed_phase = next(item for item in load_experiments() if item["id"] == "EXP-DHS-PHASE-SIEVE")
            finally:
                os.chdir(old_cwd)

        self.assertEqual(refreshed_hidden["title"], "State-sample-native generic DCP sieve and decoder")
        self.assertIn("EXP-LOCAL-EXTRA", refreshed_hidden["experiment_ids"])
        self.assertIn("dcp_sample_workbench.py", refreshed_phase["protocol"])


if __name__ == "__main__":
    unittest.main()
