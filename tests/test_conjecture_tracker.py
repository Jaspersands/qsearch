import os
import tempfile
import unittest

from conjecture_tracker import build_conjectures, write_conjecture_report
from dequantization_checks import write_dequantization_report
from experiment_runner import run_experiment
from research_registry import initialize_seed_registry, load_conjectures, validate_registry


class ConjectureTrackerTests(unittest.TestCase):
    def test_conjectures_include_reduction_links_and_blockers(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                run_experiment("EXP-DHS-PHASE-SIEVE")
                write_dequantization_report()
                report = write_conjecture_report()
                conjectures = load_conjectures()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertGreaterEqual(report["conjecture_count"], 2)
        hidden = [item for item in conjectures if item["candidate_id"] == "DHS-GOWERS-SIEVE"][0]
        self.assertTrue(any("dihedral-hsp" in link for link in hidden["reduction_links"]))
        self.assertTrue(hidden["blocking_evidence"])
        self.assertTrue(validation["valid"])

    def test_conjectures_can_be_built_without_results(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                conjectures = build_conjectures()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(all(item["status"] == "falsified-or-blocked" for item in conjectures))
        self.assertTrue(all(any("REDUCTION-ROUTE" in blocker["finding_id"] for blocker in item["blocking_evidence"]) for item in conjectures))


if __name__ == "__main__":
    unittest.main()
