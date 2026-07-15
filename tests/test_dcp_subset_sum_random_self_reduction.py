import os
import tempfile
import unittest
from pathlib import Path

from dcp_subset_sum_random_self_reduction import (
    certify_self_reduction,
    certify_signed_embedding_isometry,
    inverse_transform_instance,
    run_random_self_reduction_audit,
    transform_instance,
    transform_witness,
    write_random_self_reduction_audit,
)
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
    validate_registry,
)


class DCPSubsetSumRandomSelfReductionTests(unittest.TestCase):
    def test_signed_odd_unit_map_preserves_and_inverts_witness(self):
        n_bits = 8
        labels = [3, 17, 44, 91, 127, 201]
        witness = [1, 0, 1, 1, 0, 1]
        mask = [0, 1, 1, 0, 1, 0]
        target = sum(a * x for a, x in zip(labels, witness)) % (1 << n_bits)
        transformed_labels, transformed_target = transform_instance(
            n_bits, labels, target, mask, odd_unit=173
        )
        transformed_witness = transform_witness(witness, mask)

        self.assertEqual(
            sum(a * x for a, x in zip(transformed_labels, transformed_witness))
            % (1 << n_bits),
            transformed_target,
        )
        recovered_labels, recovered_target = inverse_transform_instance(
            n_bits, transformed_labels, transformed_target, mask, odd_unit=173
        )
        self.assertEqual(recovered_labels, labels)
        self.assertEqual(recovered_target, target)
        self.assertEqual(transform_witness(transformed_witness, mask), witness)

    def test_certificate_preserves_every_target_multiplicity(self):
        certificate = certify_self_reduction(
            n_bits=6,
            labels=[3, 7, 12, 21, 34, 55, 61, 9],
            mask=[1, 0, 1, 0, 0, 1, 0, 1],
            odd_unit=37,
            witness=[1, 1, 0, 1, 0, 0, 1, 0],
        )

        self.assertTrue(certificate.forward_witness_verified)
        self.assertTrue(certificate.inverse_witness_verified)
        self.assertTrue(certificate.all_target_multiplicities_preserved)
        self.assertTrue(certificate.all_target_multiplicities_exhaustively_checked)
        self.assertTrue(certificate.legal_conditioned_source_preserved)
        self.assertTrue(certificate.shared_seed_interface_compatible)

    def test_sign_subgroup_is_exact_embedding_isometry(self):
        certificate = certify_signed_embedding_isometry(
            n_bits=8,
            labels=[3, 17, 44, 91, 127, 201],
            target=73,
            mask=[0, 1, 1, 0, 1, 0],
        )

        self.assertTrue(certificate.exact_basis_identity_verified)
        self.assertTrue(certificate.row_map_unimodular)
        self.assertTrue(certificate.coordinate_map_orthogonal)
        self.assertTrue(certificate.embedding_lattice_isometry_proved)
        self.assertIn("Odd-unit", certificate.implication)

    def test_audit_uses_uniform_targets_and_does_not_promote_finite_rescues(self):
        report = run_random_self_reduction_audit(
            n_values=[6, 8],
            register_offsets=[2],
            attempt_multiplier=1,
            trials_per_row=1,
        )

        self.assertTrue(all(item.target_sampled_independently_uniform for item in report.trials))
        self.assertTrue(all(item.all_returned_witnesses_valid for item in report.trials))
        self.assertEqual(
            report.headline_metrics["polynomial_attempt_budget_row_count"],
            report.headline_metrics["trial_count"],
        )
        self.assertEqual(len(report.scaling_rows), 2)
        self.assertTrue(
            all(
                row.unconditional_success_lower_bounds_legal_coverage
                for row in report.scaling_rows
            )
        )
        self.assertEqual(
            report.headline_metrics["proved_uniform_inverse_polynomial_legal_coverage_count"],
            0,
        )
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_large_n_path_avoids_exponential_legality_table(self):
        report = run_random_self_reduction_audit(
            n_values=[21],
            register_offsets=[2],
            attempt_multiplier=1,
            trials_per_row=1,
            exact_legality_max_bits=8,
        )

        self.assertFalse(report.trials[0].target_legality_exactly_known)
        self.assertIsNone(report.trials[0].target_legal)
        self.assertEqual(report.headline_metrics["tail_trial_count"], 1)
        self.assertEqual(report.headline_metrics["exact_legality_trial_count"], 0)
        self.assertEqual(len(report.scaling_rows), 1)

    def test_class_selective_sweep_skips_isometric_controls(self):
        report = run_random_self_reduction_audit(
            n_values=[8],
            register_offsets=[2],
            attempt_multiplier=1,
            trials_per_row=1,
            enabled_classes=["odd-unit"],
        )

        trial = report.trials[0]
        self.assertFalse(trial.sign_only_executed)
        self.assertTrue(trial.odd_unit_executed)
        self.assertFalse(trial.signed_odd_unit_executed)
        self.assertEqual(trial.sign_only_attempts_used, 0)
        self.assertEqual(trial.signed_odd_unit_attempts_used, 0)

    def test_writer_registers_result_and_both_negative_boundaries(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_random_self_reduction_audit(
                    n_values=[6],
                    register_offsets=[2],
                    attempt_multiplier=1,
                    trials_per_row=1,
                )
                results = load_experiment_results()
                negatives = {item["id"] for item in load_negative_results()}
                validation = validate_registry()
                artifact_exists = Path(
                    "research/reductions/dcp_subset_sum_random_self_reduction.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(payload["headline_metrics"]["source_contract_satisfying_row_count"], 0)
        self.assertTrue(
            any(
                item["experiment_id"]
                == "EXP-DHS-DCP-SUBSET-SUM-RANDOM-SELF-REDUCTION"
                for item in results
            )
        )
        self.assertIn("NEG-DCP-SIGNED-COORDINATE-SELF-REDUCTION-ISOMETRIC", negatives)
        self.assertIn(
            "NEG-DCP-ODD-UNIT-LLL-FINITE-RANDOMIZATION-WITHOUT-COVERAGE",
            negatives,
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
