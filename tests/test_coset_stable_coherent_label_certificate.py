import os
import tempfile
import unittest
from pathlib import Path

from coset_recoupling_capability_ledger import CAPABILITIES
from coset_stable_coherent_label_certificate import (
    GAP_CONSTANT_DENOMINATOR,
    build_stable_coherent_label_certificate,
    canonical_oriented_cycle,
    ordered_triple_bijection_verified,
    ordered_triple_terms,
    support_term_signature,
    write_stable_coherent_label_certificate,
)
from coset_stable_root_separation_certificate import NORMALIZED_GAP_EXPONENT
from dequantization_checks import write_dequantization_report
from experiment_runner import run_experiment, supported_experiment_ids
from proof_tracker import build_proof_status_report
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
    validate_registry,
)


class StableCoherentLabelCertificateTests(unittest.TestCase):
    def test_ordered_triples_are_exactly_three_by_two_orbit_terms(self) -> None:
        for n in range(3, 10):
            terms = ordered_triple_terms(n)
            self.assertEqual(len(terms), n * (n - 1) * (n - 2))
            self.assertTrue(ordered_triple_bijection_verified(n))

        support_terms = {
            support_term_signature(term)
            for term in ordered_triple_terms(3)
        }
        self.assertEqual(len(support_terms), 6)
        self.assertEqual(len({item[0] for item in support_terms}), 3)
        self.assertEqual(len({item[1] for item in support_terms}), 2)
        self.assertEqual(canonical_oriented_cycle((1, 2, 0)), (0, 1, 2))
        self.assertEqual(canonical_oriented_cycle((2, 1, 0)), (0, 2, 1))

    def test_certificate_proves_only_the_declared_stable_label(self) -> None:
        report = build_stable_coherent_label_certificate()
        self.assertTrue(report.theorem["proved"])
        self.assertEqual(
            report.headline_metrics[
                "uniform_polynomial_stable_multiplicity_label_transform_count"
            ],
            1,
        )
        self.assertEqual(
            report.headline_metrics["normalized_gap_inverse_polynomial_exponent"],
            NORMALIZED_GAP_EXPONENT,
        )
        self.assertEqual(
            report.phase_estimation_certificate["precision"],
            f"less than 1/(3*{GAP_CONSTANT_DENOMINATOR}*n^{NORMALIZED_GAP_EXPONENT})",
        )
        for metric in (
            "unrestricted_internal_kronecker_transform_count",
            "overlapping_racah_associator_count",
            "all_sector_uniform_transform_count",
            "hidden_involution_decoder_count",
        ):
            self.assertEqual(report.headline_metrics[metric], 0)
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_capability_ledger_records_scoped_not_unrestricted_progress(self) -> None:
        capability = next(
            item
            for item in CAPABILITIES
            if item.id == "CAP-GAPPED-KRONECKER-MULTIPLICITY-TRANSFORM"
        )
        self.assertTrue(capability.uniform_polynomial_gate_complexity_proved)
        self.assertEqual(capability.availability, "proved-one-stable-channel-only")
        self.assertIn("one declared multiplicity-four channel", capability.scope_limit)
        self.assertFalse(capability.handles_overlapping_k_copy_associators)
        self.assertFalse(capability.supplies_hidden_involution_decoder)

    def test_writer_runner_and_ledgers_preserve_scope_boundary(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_stable_coherent_label_certificate()
                runner = run_experiment(
                    "EXP-COSET-STABLE-COHERENT-LABEL-CERTIFICATE"
                )
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/representation/"
                    "coset_stable_coherent_label_certificate.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(runner.status, "completed")
        self.assertIn(
            "EXP-COSET-STABLE-COHERENT-LABEL-CERTIFICATE",
            supported_experiment_ids(),
        )
        self.assertTrue(
            any(
                item["artifacts"].get("coset_stable_coherent_label_certificate")
                for item in results
            )
        )
        self.assertIn(
            "NEG-COSET-STABLE-COHERENT-LABEL-AS-RACAH-DECODER",
            {item["id"] for item in negatives},
        )
        self.assertIn(
            "DEQ-COSET-ONE-STABLE-COHERENT-LABEL-NOT-RACAH-DECODER",
            {item["id"] for item in dequantization["findings"]},
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-COSET-STABLE-RACAH-COHERENT-LABEL"
            ]["status"],
            "proved-one-stable-channel-coherent-multiplicity-label",
        )
        self.assertFalse(payload["claim_gate"]["speedup_claim_allowed"])
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
