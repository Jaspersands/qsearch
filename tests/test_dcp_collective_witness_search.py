import os
import tempfile
import unittest
from pathlib import Path

from dcp_collective_witness_search import (
    certify_locality_barrier,
    run_collective_witness_search,
    signed_relation_search,
    write_collective_witness_search,
)
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class DCPCollectiveWitnessSearchTests(unittest.TestCase):
    def test_exact_signed_relation_is_found(self):
        trial = signed_relation_search([1, 1, 7], n_bits=8, maximum_weight=2)

        self.assertGreater(trial.relation_count, 0)
        self.assertEqual(trial.minimum_relation_weight, 2)
        self.assertIsNotNone(trial.first_witness)
        self.assertEqual(trial.first_witness.residue, 0)

    def test_relation_free_labels_do_not_create_pauli_signal(self):
        trial = signed_relation_search([1, 2, 4], n_bits=8, maximum_weight=3)

        self.assertEqual(trial.relation_count, 0)
        self.assertEqual(trial.minimum_relation_weight, 0)
        self.assertIsNone(trial.first_witness)

    def test_logarithmic_locality_is_negligible_for_polynomial_label_pool(self):
        certificate = certify_locality_barrier(128)

        self.assertTrue(certificate.negligible_below_inverse_polynomial)
        self.assertLess(certificate.log2_relation_union_bound, -10.0)
        self.assertGreater(certificate.first_weight_not_ruled_out_by_union_bound, certificate.tested_locality)
        self.assertGreater(certificate.all_good_probability_at_f1_rate_at_threshold, 0.0)

    def test_report_does_not_promote_finite_relations(self):
        report = run_collective_witness_search(n_values=[12], trials_per_row=2, seed=3)

        self.assertEqual(report.headline_metrics["polynomial_time_robust_witness_count"], 0)
        self.assertEqual(report.headline_metrics["proved_full_decoder_count"], 0)
        self.assertFalse(report.claim_gate["logarithmic_locality_asymptotically_viable"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_registers_bounded_locality_negative(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_collective_witness_search(n_values=[12], trials_per_row=2, seed=3)
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path("research/phase_workbench/dcp_collective_witness_search.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertTrue(any(item["experiment_id"] == "EXP-DHS-DCP-COLLECTIVE-WITNESS-SEARCH" for item in results))
        self.assertIn(
            "NEG-DCP-BOUNDED-LOCALITY-PAULI-WITNESSES-NEGLIGIBLE",
            {item["id"] for item in negatives},
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
