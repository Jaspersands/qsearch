import os
import tempfile
import unittest
from pathlib import Path

import sympy as sp

from coset_stable_shape_router_certificate import (
    build_stable_shape_router_certificate,
    stable_shape_central_eigenvalues,
    write_stable_shape_router_certificate,
)
from experiment_runner import run_experiment, supported_experiment_ids
from research_registry import (
    initialize_seed_registry,
    load_negative_results,
    validate_registry,
)


class StableShapeRouterCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = build_stable_shape_router_certificate()

    def test_content_formulas_match_collision_endpoints(self) -> None:
        n = sp.symbols("n", integer=True, positive=True)
        transposition, three_cycle = stable_shape_central_eigenvalues((2, 1))
        self.assertEqual(transposition, n**2 / 2 - 7 * n / 2 + 3)
        self.assertEqual(three_cycle, n**3 / 3 - 4 * n**2 + 38 * n / 3 - 9)
        signatures_n8 = {record.n8_signature for record in self.report.shape_records}
        signatures_n9 = {record.n9_signature for record in self.report.shape_records}
        signatures_n12 = {record.n12_signature for record in self.report.shape_records}
        self.assertEqual(len(signatures_n8), 9)
        self.assertEqual(len(signatures_n9), 9)
        self.assertEqual(len(signatures_n12), 9)

    def test_all_symbolic_pair_collisions_are_below_stable_range(self) -> None:
        self.assertEqual(len(self.report.pair_collision_records), 36)
        self.assertFalse(
            any(
                record.collision_in_stable_range
                for record in self.report.pair_collision_records
            )
        )
        self.assertEqual(
            self.report.headline_metrics[
                "maximum_simultaneous_integer_collision_point"
            ],
            6,
        )
        self.assertEqual(
            self.report.headline_metrics["stable_range_shape_pair_collision_count"],
            0,
        )

    def test_router_is_coherent_but_not_a_compressed_clebsch_transform(self) -> None:
        self.assertTrue(self.report.theorem["proved"])
        self.assertTrue(
            self.report.claim_gate[
                "coherent_encoded_intermediate_shape_router_proved"
            ]
        )
        self.assertFalse(
            self.report.claim_gate["compressed_clebsch_isometry_proved"]
        )
        self.assertFalse(
            self.report.claim_gate["complete_encoded_left_tree_basis_proved"]
        )
        self.assertEqual(
            self.report.headline_metrics["coupling_tree_transition_circuit_count"],
            0,
        )

    def test_writer_runner_and_registry_preserve_scope(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_stable_shape_router_certificate()
                runner = run_experiment(
                    "EXP-COSET-STABLE-SHAPE-ROUTER-CERTIFICATE"
                )
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/representation/"
                    "coset_stable_shape_router_certificate.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(runner.status, "completed")
        self.assertIn(
            "EXP-COSET-STABLE-SHAPE-ROUTER-CERTIFICATE",
            supported_experiment_ids(),
        )
        self.assertIn(
            "NEG-COSET-TRANSPOSITION-SIGNATURE-ALONE-AS-STABLE-SHAPE-ROUTER",
            {item["id"] for item in negatives},
        )
        self.assertEqual(
            payload["headline_metrics"][
                "coherent_intermediate_shape_router_count"
            ],
            1,
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
