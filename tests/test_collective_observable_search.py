import os
import tempfile
import unittest
from pathlib import Path

from collective_observable_search import (
    audit_collective_observables,
    run_collective_observable_search,
    write_collective_observable_search,
)
from dequantization_checks import write_dequantization_report
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class CollectiveObservableSearchTests(unittest.TestCase):
    def test_control_pair_collapses_to_classical_shadow(self):
        audit = audit_collective_observables("cycle-vs-chorded-cycle")
        shadowed = [item for item in audit.observable_records if item.status == "classical-shadow-collapse"]

        self.assertEqual(audit.boundary_status, "classical-shadow-collapse")
        self.assertTrue(shadowed)
        self.assertTrue(all(item.classical_shadow for item in shadowed))
        self.assertFalse(any(item.status == "nonclassical-candidate-needs-proof" for item in audit.observable_records))

    def test_shrikhande_four_register_signal_is_classical_shadow(self):
        audit = audit_collective_observables("shrikhande-vs-rook")
        four_register = next(item for item in audit.observable_records if item.id.endswith("four-register-wl-boundary"))

        self.assertTrue(four_register.evaluated)
        self.assertEqual(four_register.status, "classical-shadow-collapse")
        self.assertEqual(four_register.classical_shadow, "4-WL tuple refinement")

    def test_cfi_k5_skips_high_register_without_positive_claim(self):
        audit = audit_collective_observables("cfi-k5-parity-twist")
        skipped = [item for item in audit.observable_records if item.status == "skipped-scaling-cap"]

        self.assertEqual(audit.boundary_status, "boundary-no-current-observable")
        self.assertTrue(skipped)
        self.assertFalse(any(item.distinguishes for item in audit.observable_records if item.evaluated))

    def test_report_metrics_separate_shadow_and_boundary_cases(self):
        report = run_collective_observable_search(pair_ids=["cycle-vs-chorded-cycle", "cfi-k4-parity-twist"])

        self.assertGreater(report.headline_metrics["classical_shadow_collapse_count"], 0)
        self.assertEqual(report.headline_metrics["boundary_pair_count"], 1)
        self.assertEqual(report.headline_metrics["nonclassical_candidate_count"], 0)
        self.assertEqual(report.status, "blocked-needs-new-collective-observable")

    def test_write_report_updates_registry_negative_results_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_collective_observable_search(pair_ids=["cycle-vs-chorded-cycle", "cfi-k4-parity-twist"])
                artifact_exists = Path("research/coset_workbench/collective_observable_search.json").exists()
                results = load_experiment_results()
                negatives = load_negative_results()
                deq = write_dequantization_report()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(payload["headline_metrics"]["boundary_pair_count"], 1)
        self.assertTrue(any(result["artifacts"].get("collective_observable_search") for result in results))
        self.assertTrue(any(item["id"].startswith("COSET-OBSERVABLE-SHADOW-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "collective_observable_search" for item in deq["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
