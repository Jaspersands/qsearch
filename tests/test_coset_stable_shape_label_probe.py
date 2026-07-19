import os
import tempfile
import unittest
from pathlib import Path

from coset_stable_shape_family_certificate import STABLE_TAILS
from coset_stable_shape_label_probe import (
    audit_stable_shape_label,
    build_stable_shape_label_report,
    write_stable_shape_label_report,
)
from dequantization_checks import write_dequantization_report
from experiment_runner import run_experiment, supported_experiment_ids
from proof_tracker import build_proof_status_report
from research_registry import (
    initialize_seed_registry,
    load_negative_results,
    validate_registry,
)


class StableShapeLabelProbeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = build_stable_shape_label_report((8,))

    def test_uniform_orbit_operator_splits_every_nontrivial_n8_shape(self) -> None:
        records = {
            record.intermediate_tail: record for record in self.report.records
        }
        self.assertEqual(set(records), set(STABLE_TAILS))
        nontrivial = [
            record for record in records.values()
            if record.second_stage_multiplicity > 1
        ]
        self.assertEqual(len(nontrivial), 7)
        self.assertTrue(
            all(record.nontrivial_multiplicity_fully_split for record in nontrivial)
        )
        self.assertTrue(
            all(record.orbit_generator_id == "ORB-TC-INTERSECTION-2" for record in nontrivial)
        )
        self.assertEqual(
            self.report.headline_metrics["unproved_shape_finite_target_count"],
            6,
        )

    def test_extraction_and_integer_reconstruction_are_numerically_controlled(self) -> None:
        for record in self.report.records:
            self.assertEqual(record.orbit_term_count, 8 * 7 * 6)
            self.assertEqual(record.orbit_term_count, record.orbit_term_count_formula)
            self.assertLess(record.target_eigenspace_relative_residual, 1e-9)
            self.assertLess(record.target_basis_orthogonality_residual, 1e-9)
            self.assertTrue(record.exact_integer_polynomial_candidate)
            self.assertLess(
                record.integer_polynomial_relative_reconstruction_residual,
                1e-10,
            )
        stable = audit_stable_shape_label(8, (2, 1))
        self.assertEqual(stable.second_stage_multiplicity, 4)
        self.assertTrue(stable.coherent_normalized_gap_already_proved)

    def test_finite_targets_do_not_cross_exact_or_speedup_claim_gates(self) -> None:
        metrics = self.report.headline_metrics
        self.assertEqual(metrics["new_exact_all_n_characteristic_polynomial_count"], 0)
        self.assertEqual(metrics["new_normalized_gap_theorem_count"], 0)
        self.assertEqual(metrics["new_coherent_shape_label_count"], 0)
        self.assertFalse(self.report.claim_gate["all_n_characteristic_polynomials_proved"])
        self.assertFalse(self.report.claim_gate["coherent_lcu_implementations_proved"])
        self.assertFalse(self.report.claim_gate["speedup_claim_allowed"])

    def test_writer_runner_and_ledgers_record_the_six_open_proof_targets(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_stable_shape_label_report(n_values=(8,))
                runner = run_experiment("EXP-COSET-STABLE-SHAPE-LABEL-PROBE")
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/representation/coset_stable_shape_label_probe.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(runner.status, "completed")
        self.assertIn(
            "EXP-COSET-STABLE-SHAPE-LABEL-PROBE",
            supported_experiment_ids(),
        )
        self.assertIn(
            "NEG-COSET-FINITE-NINE-SHAPE-SPECTRA-AS-COMPLETE-RACAH-LABELS",
            {item["id"] for item in negatives},
        )
        self.assertIn(
            "DEQ-COSET-SIX-FINITE-SHAPE-LABEL-TARGETS-LACK-ALL-N-PROOFS",
            {item["id"] for item in dequantization["findings"]},
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-COSET-STABLE-RACAH-UNIFORM-SHAPE-LABEL"
            ]["status"],
            "blocked-six-finite-spectral-targets-found-exact-gaps-and-circuits-open",
        )
        self.assertEqual(payload["headline_metrics"]["unproved_shape_finite_target_count"], 6)
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
