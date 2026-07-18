import os
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

import numpy as np

from coset_stable_subspace_transition_probe import (
    audit_stable_subspace_transition,
    invariant_tensor_basis,
    stable_transition_overlap,
    write_stable_subspace_transition_report,
)
from dequantization_checks import write_dequantization_report
from experiment_runner import run_experiment, supported_experiment_ids
from proof_tracker import build_proof_status_report
from representation_obstruction import hook_length_dimension
from research_registry import (
    initialize_seed_registry,
    load_negative_results,
    validate_registry,
)


class StableSubspaceTransitionProbeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.record = audit_stable_subspace_transition(7)

    def test_stable_intertwiner_dimensions_and_residuals(self) -> None:
        self.assertEqual(self.record.first_stage_multiplicity, 2)
        self.assertEqual(self.record.second_stage_multiplicity, 4)
        self.assertEqual(self.record.stable_branch_dimension, 8)
        self.assertEqual(self.record.overlap_rank, 8)
        self.assertGreater(self.record.first_invariant_laplacian_gap, 0.1)
        self.assertGreater(self.record.second_invariant_laplacian_gap, 0.1)
        self.assertLess(self.record.maximum_invariant_residual, 1e-9)
        self.assertLess(self.record.maximum_embedding_isometry_residual, 1e-9)

    def test_n7_projector_overlap_proves_large_finite_leakage(self) -> None:
        expected = Fraction(907, 324)
        self.assertAlmostEqual(
            self.record.projector_overlap_trace,
            expected.numerator / expected.denominator,
            places=10,
        )
        self.assertEqual(
            self.record.projector_overlap_rational_candidate, "907/324"
        )
        self.assertLess(self.record.maximally_mixed_branch_retention, 0.36)
        self.assertGreater(self.record.maximally_mixed_branch_leakage, 0.64)
        self.assertFalse(self.record.stable_branch_closed_under_recoupling)
        self.assertTrue(self.record.finite_numerical_probe_only)

    def test_overlap_singular_values_are_multiplicity_gauge_invariant(self) -> None:
        source = (5, 2)
        stable = (4, 2, 1)
        stable_dimension = hook_length_dimension(stable)
        first, _, _ = invariant_tensor_basis((source, source, stable), 2)
        second, _, _ = invariant_tensor_basis((stable, source, stable), 4)
        first = first * np.sqrt(stable_dimension)
        second = second * np.sqrt(stable_dimension)
        reference = np.linalg.svd(
            stable_transition_overlap(first, second), compute_uv=False
        )
        first_rotation, _ = np.linalg.qr(
            np.asarray([[1.0, 2.0], [3.0, 5.0]])
        )
        second_rotation, _ = np.linalg.qr(
            np.asarray(
                [
                    [1.0, 2.0, 3.0, 5.0],
                    [2.0, 3.0, 5.0, 7.0],
                    [3.0, 5.0, 7.0, 11.0],
                    [5.0, 7.0, 11.0, 13.0],
                ]
            )
        )
        rotated_first = np.einsum("ab,biju->aiju", first_rotation, first)
        rotated_second = np.einsum("ab,buit->auit", second_rotation, second)
        rotated = np.linalg.svd(
            stable_transition_overlap(rotated_first, rotated_second),
            compute_uv=False,
        )
        self.assertTrue(np.allclose(reference, rotated, atol=1e-10))

    def test_writer_runner_and_ledgers_record_leakage_boundary(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_stable_subspace_transition_report(n_values=(7,))
                runner = run_experiment(
                    "EXP-COSET-STABLE-SUBSPACE-TRANSITION-PROBE"
                )
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/representation/"
                    "coset_stable_subspace_transition_probe.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(runner.status, "completed")
        self.assertIn(
            "EXP-COSET-STABLE-SUBSPACE-TRANSITION-PROBE",
            supported_experiment_ids(),
        )
        self.assertIn(
            "NEG-COSET-STABLE-CHANNEL-AS-CLOSED-RACAH-SUBSPACE",
            {item["id"] for item in negatives},
        )
        self.assertIn(
            "DEQ-COSET-STABLE-BRANCH-LEAKS-BEFORE-DECODER",
            {item["id"] for item in dequantization["findings"]},
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-COSET-STABLE-RACAH-SUBSPACE-CLOSURE"
            ]["status"],
            "refuted-finite-stable-branch-leakage-observed",
        )
        self.assertEqual(payload["headline_metrics"]["closed_stable_associator_count"], 0)
        self.assertFalse(payload["claim_gate"]["speedup_claim_allowed"])
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
