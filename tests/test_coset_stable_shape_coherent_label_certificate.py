import os
import tempfile
import unittest
from pathlib import Path

from coset_stable_shape_coherent_label_certificate import (
    build_stable_shape_coherent_label_certificate,
    write_stable_shape_coherent_label_certificate,
)
from dequantization_checks import write_dequantization_report
from experiment_runner import run_experiment, supported_experiment_ids
from proof_tracker import build_proof_status_report
from research_registry import (
    initialize_seed_registry,
    load_negative_results,
    validate_registry,
)


class StableShapeCoherentLabelCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = build_stable_shape_coherent_label_certificate()

    def test_common_block_encoding_covers_all_nontrivial_shapes(self) -> None:
        self.assertTrue(self.report.theorem["proved"])
        self.assertTrue(self.report.common_block_encoding_certificate["proved"])
        self.assertEqual(len(self.report.shape_records), 7)
        self.assertEqual(
            {record.multiplicity_dimension for record in self.report.shape_records},
            {2, 3, 4},
        )
        self.assertTrue(
            all(
                record.common_ordered_triple_block_encoding_applies
                and record.coherent_phase_estimation_label_proved
                for record in self.report.shape_records
            )
        )

    def test_local_label_theorem_does_not_claim_routing_or_associator(self) -> None:
        metrics = self.report.headline_metrics
        self.assertEqual(metrics["new_coherent_shape_label_count"], 6)
        self.assertEqual(metrics["all_nontrivial_stable_shape_coherent_label_count"], 7)
        self.assertEqual(metrics["channel_routing_circuit_count"], 0)
        self.assertEqual(metrics["coupling_tree_transition_circuit_count"], 0)
        self.assertEqual(metrics["complete_racah_associator_count"], 0)
        self.assertEqual(metrics["hidden_involution_decoder_count"], 0)
        self.assertFalse(self.report.claim_gate["channel_routing_proved"])
        self.assertFalse(self.report.claim_gate["speedup_claim_allowed"])

    def test_writer_runner_and_ledgers_preserve_local_label_boundary(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                source_dir = Path("research/representation")
                source_dir.mkdir(parents=True, exist_ok=True)
                for source in (
                    "coset_stable_shape_family_certificate.json",
                    "coset_stable_shape_quadratic_gap_certificate.json",
                    "coset_stable_shape_cubic_gap_certificate.json",
                    "coset_stable_coherent_label_certificate.json",
                ):
                    original = Path(old_cwd) / "research/representation" / source
                    (source_dir / source).write_text(original.read_text())
                payload = write_stable_shape_coherent_label_certificate()
                runner = run_experiment(
                    "EXP-COSET-STABLE-SHAPE-COHERENT-LABEL-CERTIFICATE"
                )
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/representation/"
                    "coset_stable_shape_coherent_label_certificate.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(runner.status, "completed")
        self.assertIn(
            "EXP-COSET-STABLE-SHAPE-COHERENT-LABEL-CERTIFICATE",
            supported_experiment_ids(),
        )
        self.assertIn(
            "NEG-COSET-SEVEN-COHERENT-SHAPE-LABELS-AS-COMPLETE-RACAH-DECODER",
            {item["id"] for item in negatives},
        )
        self.assertIn(
            "DEQ-COSET-ALL-SHAPE-LOCAL-LABELS-STILL-ASSUME-ROUTING-AND-LACK-TRANSITION",
            {item["id"] for item in dequantization["findings"]},
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-COSET-STABLE-RACAH-ALL-SEVEN-SHAPE-LOCAL-LABELS"
            ]["status"],
            "proved-all-seven-shape-local-coherent-labels-routing-open",
        )
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-COSET-STABLE-RACAH-UNIFORM-SHAPE-LABEL"
            ]["status"],
            "proved-all-seven-nontrivial-shape-local-coherent-labels",
        )
        self.assertEqual(payload["headline_metrics"]["complete_racah_associator_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
