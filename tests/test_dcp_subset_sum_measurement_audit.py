import os
import tempfile
import unittest
from pathlib import Path

import numpy as np

from dcp_subset_sum_measurement_audit import (
    analyze_prefix_residue_ranks,
    certify_residue_bond_dimension,
    explicit_qft_output_distribution,
    run_subset_sum_measurement_audit,
    write_subset_sum_measurement_audit,
)
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class DCPSubsetSumMeasurementAuditTests(unittest.TestCase):
    def test_compute_sum_qft_is_exactly_uniform_for_every_hidden_reflection(self):
        for hidden in (0, 1, 5, 11):
            distribution = explicit_qft_output_distribution(4, [1, 3, 7], hidden)
            self.assertLess(float(np.max(np.abs(distribution - 1.0 / 16.0))), 1e-12)

    def test_prefix_rank_tracks_distinct_reachable_residues(self):
        instance = analyze_prefix_residue_ranks(6, [1, 2, 4, 8, 16, 31])

        self.assertEqual(instance.prefix_distinct_counts[0], 1)
        self.assertGreaterEqual(instance.maximum_prefix_distinct_count, instance.middle_prefix_distinct_count)
        self.assertFalse(instance.sum_measurement_depends_on_hidden_reflection)
        self.assertFalse(instance.compute_qft_retaining_input_depends_on_hidden_reflection)

    def test_asymptotic_certificate_has_exponential_bond_and_small_collision_bound(self):
        certificate = certify_residue_bond_dimension(256)

        self.assertGreater(certificate.certified_bond_dimension_if_collision_free, 256**4)
        self.assertLess(certificate.collision_union_bound, 1.0 / 256.0)
        self.assertTrue(certificate.polynomial_bond_dimension_ruled_out_with_high_probability)

    def test_report_keeps_approximate_and_compressed_measurements_open(self):
        report = run_subset_sum_measurement_audit(n_values=[6, 8], trials_per_size=1)

        self.assertEqual(report.headline_metrics["qft_uniformity_failure_count"], 0)
        self.assertEqual(report.headline_metrics["compute_qft_signal_instance_count"], 0)
        self.assertEqual(report.headline_metrics["proved_polynomial_collective_measurement_count"], 0)
        self.assertEqual(report.headline_metrics["approximate_fiber_bond_density_one_no_go_theorem_count"], 1)
        self.assertEqual(report.headline_metrics["polynomial_layout_dictionary_no_go_theorem_count"], 1)
        self.assertTrue(report.claim_gate["approximate_fiber_state_fixed_layout_density_one_ruled_out"])
        self.assertFalse(report.claim_gate["approximate_hashed_network_ruled_out"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_registers_two_restricted_negatives(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_subset_sum_measurement_audit(n_values=[6, 8], trials_per_size=1)
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/phase_workbench/dcp_subset_sum_measurement_audit.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        negative_ids = {item["id"] for item in negatives}
        self.assertTrue(artifact_exists)
        self.assertTrue(any(item["experiment_id"] == "EXP-DHS-DCP-SUBSET-SUM-MEASUREMENT-AUDIT" for item in results))
        self.assertIn("NEG-DCP-COMPUTE-SUBSET-SUM-QFT-NO-INTERFERENCE", negative_ids)
        self.assertIn("NEG-DCP-EXACT-RESIDUE-MPS-EXPONENTIAL-BOND", negative_ids)
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
