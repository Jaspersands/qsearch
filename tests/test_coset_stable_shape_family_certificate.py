import os
import tempfile
import unittest
from pathlib import Path

import sympy as sp

from coset_stable_shape_family_certificate import (
    STABLE_TAILS,
    X,
    build_stable_shape_family_certificate,
    factorial_cycle_moment,
    reconstruct_character_polynomial,
    write_stable_shape_family_certificate,
)
from dequantization_checks import write_dequantization_report
from experiment_runner import run_experiment, supported_experiment_ids
from proof_tracker import build_proof_status_report
from research_registry import (
    initialize_seed_registry,
    load_negative_results,
    validate_registry,
)


class StableShapeFamilyCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = build_stable_shape_family_certificate()

    def test_exact_character_polynomials_have_full_rank_witnesses(self) -> None:
        w, w_certificate = reconstruct_character_polynomial((2,))
        xi, xi_certificate = reconstruct_character_polynomial((2, 1))
        self.assertEqual(
            sp.expand(w - (X[0] ** 2 - 3 * X[0] + 2 * X[1]) / 2),
            0,
        )
        self.assertEqual(
            sp.expand(
                xi
                - (X[0] ** 3 - 6 * X[0] ** 2 + 8 * X[0] - 3 * X[2])
                / 3
            ),
            0,
        )
        self.assertEqual(
            w_certificate["basis_dimension"], w_certificate["witness_rank"]
        )
        self.assertEqual(
            xi_certificate["basis_dimension"], xi_certificate["witness_rank"]
        )
        self.assertGreater(w_certificate["verification_row_count"], 20)
        self.assertGreater(xi_certificate["verification_row_count"], 20)

    def test_factorial_moments_prove_all_n_multiplicity_pairs(self) -> None:
        records = {record.tail: record for record in self.report.shape_records}
        expected = {
            (1,): (1, 1),
            (2,): (2, 2),
            (1, 1): (1, 2),
            (3,): (1, 2),
            (2, 1): (2, 4),
            (1, 1, 1): (1, 2),
            (4,): (1, 1),
            (3, 1): (1, 3),
            (2, 2): (1, 2),
        }
        self.assertEqual(set(records), set(STABLE_TAILS))
        self.assertEqual(
            {
                tail: (
                    record.first_stage_multiplicity,
                    record.second_stage_multiplicity,
                )
                for tail, record in records.items()
            },
            expected,
        )
        source, _ = reconstruct_character_polynomial((2,))
        final, _ = reconstruct_character_polynomial((2, 1))
        self.assertEqual(factorial_cycle_moment(source**2 * final), 2)
        self.assertEqual(factorial_cycle_moment(final * source * final), 4)

    def test_theorem_closes_n8_endpoint_but_not_coherent_labels(self) -> None:
        metrics = self.report.headline_metrics
        self.assertTrue(self.report.theorem["proved"])
        self.assertEqual(metrics["stable_intermediate_shape_count"], 9)
        self.assertEqual(metrics["n8_endpoint_verified_shape_count"], 9)
        self.assertEqual(metrics["stable_final_total_multiplicity"], 25)
        self.assertEqual(metrics["direct_triple_character_moment_multiplicity"], 25)
        self.assertEqual(metrics["all_n_sector_exhaustion_theorem_count"], 1)
        self.assertTrue(
            self.report.endpoint_certificate["selected_shapes_exhaust_all_channels"]
        )
        self.assertEqual(metrics["nontrivial_second_stage_shape_count"], 7)
        self.assertEqual(metrics["coherent_gapped_second_stage_shape_count"], 1)
        self.assertEqual(metrics["unresolved_coherent_second_stage_shape_count"], 6)
        self.assertFalse(self.report.claim_gate["speedup_claim_allowed"])

    def test_writer_runner_and_ledgers_preserve_shape_vs_circuit_boundary(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_stable_shape_family_certificate()
                runner = run_experiment(
                    "EXP-COSET-STABLE-SHAPE-FAMILY-CERTIFICATE"
                )
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/representation/"
                    "coset_stable_shape_family_certificate.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(runner.status, "completed")
        self.assertIn(
            "EXP-COSET-STABLE-SHAPE-FAMILY-CERTIFICATE",
            supported_experiment_ids(),
        )
        self.assertIn(
            "NEG-COSET-NINE-STABLE-SHAPES-AS-COHERENT-RACAH-TRANSFORM",
            {item["id"] for item in negatives},
        )
        self.assertIn(
            "DEQ-COSET-NINE-STABLE-SHAPES-STILL-LACK-SIX-GAPPED-LABELS",
            {item["id"] for item in dequantization["findings"]},
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-COSET-STABLE-RACAH-NINE-SHAPE-FAMILY"
            ]["status"],
            "proved-exact-nine-shape-stable-sector-family",
        )
        self.assertEqual(payload["headline_metrics"]["coherent_all_sector_transform_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
