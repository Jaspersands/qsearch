import os
import tempfile
import unittest
from pathlib import Path

import sympy as sp

from coset_stable_first_stage_label_certificate import (
    build_stable_first_stage_label_certificate,
    exact_wn_second_power_trace,
    write_stable_first_stage_label_certificate,
)
from experiment_runner import run_experiment, supported_experiment_ids
from research_registry import (
    initialize_seed_registry,
    load_negative_results,
    validate_registry,
)


class StableFirstStageLabelCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = build_stable_first_stage_label_certificate()

    def test_exact_W_target_moments_and_discriminant(self) -> None:
        certificate = self.report.equality_pattern_certificate
        self.assertEqual(
            certificate["first_power_trace"],
            "2*n**3 - 19*n**2 + 51*n - 36",
        )
        self.assertEqual(
            certificate["second_power_trace"],
            "2*n**6 - 38*n**5 + 283*n**4 - 1048*n**3 + 2021*n**2 - 1904*n + 688",
        )
        self.assertEqual(
            certificate["discriminant"],
            "n**4 - 14*n**3 + 73*n**2 - 136*n + 80",
        )
        self.assertEqual(
            certificate["shifted_discriminant_coefficients"],
            [1, 10, 37, 92, 164],
        )
        self.assertTrue(certificate["positive_for_every_n_at_least_6"])

    def test_every_pre_stable_endpoint_is_exact(self) -> None:
        self.assertEqual([record.n for record in self.report.endpoint_records], list(range(6, 12)))
        self.assertTrue(all(record.verified for record in self.report.endpoint_records))
        n = sp.symbols("n", integer=True, positive=True)
        formula = (
            2 * n**6
            - 38 * n**5
            + 283 * n**4
            - 1048 * n**3
            + 2021 * n**2
            - 1904 * n
            + 688
        )
        for endpoint_n in range(6, 12):
            self.assertEqual(
                exact_wn_second_power_trace(endpoint_n),
                int(formula.subs(n, endpoint_n)),
            )

    def test_all_nontrivial_first_stage_blocks_have_coherent_labels(self) -> None:
        self.assertTrue(self.report.theorem["proved"])
        self.assertEqual(
            {record.target_tail for record in self.report.target_records},
            {(2,), (2, 1)},
        )
        self.assertTrue(
            all(
                record.coherent_phase_estimation_label_proved
                for record in self.report.target_records
            )
        )
        metrics = self.report.headline_metrics
        self.assertEqual(metrics["all_nontrivial_first_stage_gap_theorem_count"], 2)
        self.assertEqual(
            metrics["all_stable_first_stage_multiplicity_resolved_shape_count"], 9
        )
        self.assertEqual(metrics["intermediate_shape_label_transform_count"], 0)
        self.assertEqual(metrics["coupling_tree_transition_circuit_count"], 0)
        self.assertFalse(self.report.claim_gate["encoded_channel_router_proved"])

    def test_writer_runner_and_registry_preserve_scope(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_stable_first_stage_label_certificate()
                runner = run_experiment(
                    "EXP-COSET-STABLE-FIRST-STAGE-LABEL-CERTIFICATE"
                )
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/representation/"
                    "coset_stable_first_stage_label_certificate.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(runner.status, "completed")
        self.assertIn(
            "EXP-COSET-STABLE-FIRST-STAGE-LABEL-CERTIFICATE",
            supported_experiment_ids(),
        )
        self.assertIn(
            "NEG-COSET-SECOND-STAGE-LABELS-AS-COMPLETE-LEFT-TREE-BASIS",
            {item["id"] for item in negatives},
        )
        self.assertEqual(
            payload["headline_metrics"][
                "all_stable_first_stage_multiplicity_resolved_shape_count"
            ],
            9,
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
