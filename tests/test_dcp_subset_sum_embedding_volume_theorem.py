import math
import os
import tempfile
import unittest
from pathlib import Path

from dcp_subset_sum_carry_slice_lattice import carry_sliced_embedding
from dcp_subset_sum_embedding_volume_theorem import (
    carry_sliced_covolume_squared,
    run_embedding_volume_theorem,
    standard_embedding_covolume,
    write_embedding_volume_theorem,
)
from dcp_subset_sum_lattice_search import modular_subset_sum_embedding
from dcp_subset_sum_solver_synthesis import build_solver_primitives
from dequantization_checks import write_dequantization_report
from experiment_runner import supported_experiment_ids
from proof_tracker import build_proof_status_report
from query_model_ledger import build_query_model_ledger
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
    validate_registry,
)


class DCPSubsetSumEmbeddingVolumeTheoremTests(unittest.TestCase):
    def test_standard_covolume_matches_exact_embedding_determinant(self):
        n_bits = 6
        labels = [1, 7, 12, 19, 31]
        scale = 3
        basis = modular_subset_sum_embedding(labels, 5, 1 << n_bits, scale)
        self.assertEqual(
            abs(int(basis.det())),
            standard_embedding_covolume(n_bits, len(labels), scale),
        )

    def test_carry_sliced_covolume_matches_exact_gram_determinant(self):
        n_bits = 6
        low_bits = 2
        low_labels = [1, 2, 3, 1, 0]
        planted = [1, 0, 1, 1, 0]
        low_sum = sum(label * bit for label, bit in zip(low_labels, planted))
        target = low_sum % (1 << low_bits)
        carry = low_sum // (1 << low_bits)
        embedding_scale = 3
        low_scale = 5
        basis = carry_sliced_embedding(
            low_labels,
            target,
            n_bits,
            low_bits,
            carry,
            embedding_scale,
            low_scale,
        )
        self.assertEqual(
            int((basis * basis.T).det()),
            carry_sliced_covolume_squared(
                n_bits,
                low_bits,
                low_labels,
                low_sum,
                embedding_scale,
                low_scale,
            ),
        )

    def test_volume_limits_close_only_volume_based_gap(self):
        report = run_embedding_volume_theorem(n_values=[16, 64, 256])
        certificate = report.theorem_certificate
        self.assertTrue(certificate.cauchy_binet_proved)
        self.assertEqual(certificate.standard_determinant_root_limit, 4.0)
        self.assertEqual(certificate.carry_sliced_determinant_root_limit, 4.0)
        self.assertAlmostEqual(
            certificate.planted_witness_to_gaussian_scale_limit,
            math.sqrt(2 * math.pi * math.e) / 4,
        )
        self.assertFalse(report.claim_gate["standard_volume_only_gap_exists"])
        self.assertFalse(report.claim_gate["logarithmic_slice_volume_only_gap_exists"])
        self.assertFalse(report.claim_gate["local_reduced_basis_gap_proved"])
        self.assertEqual(
            report.headline_metrics["volume_only_asymptotic_separation_ruled_out_count"],
            2,
        )

    def test_registry_proof_query_dequantization_and_synthesis_integration(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_embedding_volume_theorem(n_values=[16, 32, 64])
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                query = build_query_model_ledger()
                primitives = {item.primitive_id: item for item in build_solver_primitives()}
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/classical_baselines/dcp_subset_sum_embedding_volume_theorem.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertTrue(
            any(item["id"] == "DEQ-DCP-SUBSET-SUM-EMBEDDING-VOLUME-ONLY-GAP" for item in dequantization["findings"])
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas["LEMMA-DHS-GOWERS-SIEVE-DCP-EMBEDDING-VOLUME-ONLY-GAP-OBSTRUCTION"]["status"],
            "proved-exact-standard-and-sliced-covolume-limits",
        )
        query_record = next(
            item for item in query["records"] if item["candidate_id"] == "DHS-GOWERS-SIEVE"
        )
        self.assertTrue(any("Embedding volume theorem" in item for item in query_record["blocking_evidence"]))
        self.assertIn("subset-sum-embedding-volume-obstruction", primitives)
        self.assertTrue(
            any(item["artifacts"].get("dcp_subset_sum_embedding_volume_theorem") for item in results)
        )
        self.assertTrue(
            any(item["id"] == "NEG-DCP-SUBSET-SUM-VOLUME-ONLY-LATTICE-GAP" for item in negatives)
        )
        self.assertEqual(
            payload["headline_metrics"]["volume_only_asymptotic_separation_ruled_out_count"],
            2,
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_experiment_is_registered_and_supported(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)
        self.assertIn(
            "EXP-DHS-DCP-SUBSET-SUM-EMBEDDING-VOLUME-THEOREM",
            supported_experiment_ids(),
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
