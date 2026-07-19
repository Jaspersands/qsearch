import os
import tempfile
import unittest
from pathlib import Path

from coset_stable_encoded_tree_certificate import (
    build_stable_encoded_tree_certificate,
    finite_encoded_operator_commutation_audit,
    write_stable_encoded_tree_certificate,
)
from experiment_runner import run_experiment, supported_experiment_ids
from research_registry import (
    initialize_seed_registry,
    load_negative_results,
    validate_registry,
)


class StableEncodedTreeCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = build_stable_encoded_tree_certificate()

    def test_observable_layers_commute_in_finite_operator_control(self) -> None:
        audit = finite_encoded_operator_commutation_audit()
        self.assertEqual(audit.pairwise_commutator_count, 6)
        self.assertLess(audit.maximum_normalized_commutator_residual, 1e-12)
        self.assertTrue(audit.numerical_identity_check_passed)
        self.assertEqual(audit.second_stage_orbit_term_count, 60)

    def test_joint_labels_exactly_exhaust_final_multiplicity(self) -> None:
        self.assertTrue(self.report.theorem["proved"])
        self.assertEqual(len(self.report.branch_records), 9)
        self.assertTrue(
            all(
                record.complete_joint_branch_label_proved
                for record in self.report.branch_records
            )
        )
        self.assertEqual(
            sum(
                record.first_stage_multiplicity
                * record.second_stage_multiplicity
                for record in self.report.branch_records
            ),
            25,
        )
        self.assertEqual(
            self.report.headline_metrics["joint_multiplicity_label_count"], 25
        )
        self.assertEqual(
            self.report.headline_metrics["final_multiplicity_dimension"], 25
        )

    def test_encoded_transition_is_not_promoted_to_compressed_associator(self) -> None:
        gate = self.report.claim_gate
        self.assertTrue(gate["complete_encoded_left_tree_joint_labels_proved"])
        self.assertTrue(gate["complete_encoded_right_tree_joint_labels_proved"])
        self.assertTrue(
            gate["encoded_coupling_tree_transition_label_isometry_proved"]
        )
        self.assertFalse(gate["compressed_internal_kronecker_transform_proved"])
        self.assertFalse(gate["compressed_racah_associator_proved"])
        self.assertFalse(gate["state_dependent_transition_filter_proved"])
        self.assertFalse(gate["hidden_involution_decoder_proved"])
        self.assertFalse(gate["speedup_claim_allowed"])

    def test_writer_runner_and_registry_preserve_scope(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_stable_encoded_tree_certificate()
                runner = run_experiment(
                    "EXP-COSET-STABLE-ENCODED-TREE-CERTIFICATE"
                )
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/representation/"
                    "coset_stable_encoded_tree_certificate.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(runner.status, "completed")
        self.assertIn(
            "EXP-COSET-STABLE-ENCODED-TREE-CERTIFICATE",
            supported_experiment_ids(),
        )
        self.assertIn(
            "NEG-COSET-ENCODED-TREE-LABELS-AS-COMPLETE-HSP-DECODER",
            {item["id"] for item in negatives},
        )
        self.assertEqual(
            payload["headline_metrics"][
                "encoded_coupling_tree_transition_isometry_count"
            ],
            1,
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
