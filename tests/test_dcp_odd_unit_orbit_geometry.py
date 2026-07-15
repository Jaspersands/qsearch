import os
import tempfile
import unittest
from pathlib import Path

from dcp_odd_unit_orbit_geometry import (
    certify_odd_unit_orbit_invariants,
    learn_heldout_feature_rules,
    run_odd_unit_orbit_geometry_audit,
    two_adic_valuation,
    write_odd_unit_orbit_geometry_audit,
)
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
    validate_registry,
)


class DCPOddUnitOrbitGeometryTests(unittest.TestCase):
    def test_two_adic_valuation_handles_zero_and_units(self):
        self.assertEqual(two_adic_valuation(0, 8), 8)
        self.assertEqual(two_adic_valuation(3, 8), 0)
        self.assertEqual(two_adic_valuation(40, 8), 3)

    def test_odd_units_preserve_full_two_adic_signature(self):
        certificate = certify_odd_unit_orbit_invariants(
            n_bits=8,
            labels=[3, 12, 17, 44, 91, 128],
            target=40,
            units=[3, 5, 173, 255],
        )

        self.assertTrue(certificate.label_two_adic_signature_preserved)
        self.assertTrue(certificate.target_two_adic_valuation_preserved)
        self.assertTrue(certificate.pairwise_difference_two_adic_signature_preserved)
        self.assertTrue(certificate.orbit_exponential_in_n)
        self.assertEqual(certificate.exact_orbit_size_if_odd_label, 128)

    def test_audit_uses_heldout_rules_without_promoting_them_to_proofs(self):
        report = run_odd_unit_orbit_geometry_audit(
            n_values=[8, 10],
            register_offset=2,
            base_instances_per_size=2,
            units_multiplier=1,
        )

        self.assertTrue(all(row.target_sampled_independently_uniform for row in report.records))
        self.assertEqual(report.headline_metrics["invalid_witness_count"], 0)
        self.assertGreater(report.headline_metrics["feature_rule_count"], 0)
        self.assertEqual(len(report.scaling_rows), 2)
        self.assertLessEqual(
            report.headline_metrics["maximum_n_with_heldout_positive_pre_reduction_rule"],
            10,
        )
        self.assertEqual(
            report.headline_metrics["proved_inverse_polynomial_easy_orbit_measure_count"], 0
        )
        self.assertTrue(all(rule.holdout_row_count > 0 for rule in report.feature_rules))
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_rule_learner_marks_post_reduction_features_diagnostic_only(self):
        report = run_odd_unit_orbit_geometry_audit(
            n_values=[8],
            register_offset=2,
            base_instances_per_size=2,
            units_multiplier=1,
        )
        rules = learn_heldout_feature_rules(report.records)

        self.assertTrue(any(rule.feature_stage == "post-reduction" for rule in rules))
        self.assertTrue(
            all(
                not rule.proof_relevant_pre_reduction_rule
                for rule in rules
                if rule.feature_stage == "post-reduction"
            )
        )

    def test_writer_registers_result_and_feature_enrichment_boundary(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_odd_unit_orbit_geometry_audit(
                    n_values=[8],
                    register_offset=2,
                    base_instances_per_size=2,
                    units_multiplier=1,
                )
                results = load_experiment_results()
                negatives = {item["id"] for item in load_negative_results()}
                validation = validate_registry()
                artifact_exists = Path(
                    "research/classical_baselines/dcp_odd_unit_orbit_geometry.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(payload["headline_metrics"]["proved_polynomial_partial_subset_sum_solver_count"], 0)
        self.assertTrue(
            any(item["experiment_id"] == "EXP-DHS-DCP-ODD-UNIT-ORBIT-GEOMETRY" for item in results)
        )
        self.assertIn("NEG-DCP-ODD-UNIT-FINITE-FEATURE-ENRICHMENT-NOT-COVERAGE", negatives)
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
