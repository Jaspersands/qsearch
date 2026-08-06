import itertools
import os
import random
import tempfile
import unittest
from unittest.mock import patch

import numpy as np

from code_equivalence_workbench import enumerate_codewords
from code_frontier_triage import build_code_frontier_triage
from dequantization_checks import write_dequantization_report
from experiment_runner import run_experiment, supported_experiment_ids
from proof_tracker import write_proof_status_report
from query_model_ledger import write_query_model_ledger
from research_frontier_map import write_frontier_map
from research_registry import initialize_seed_registry, validate_registry
from self_dual_code_boundary_search import (
    SelfDualSearchSpec,
    generate_self_dual_instances,
    write_self_dual_code_boundary,
)
from self_dual_global_orbit_audit import (
    GlobalOrbitAuditSpec,
    basis_normalized_column_key,
    construction_a_lattice_record,
    gf2_inverse,
    run_self_dual_global_orbit_audit,
    write_self_dual_global_orbit_audit,
)


class SelfDualGlobalOrbitAuditTests(unittest.TestCase):
    def test_gf2_inverse_and_normalized_key_invariance(self):
        instance = generate_self_dual_instances(
            SelfDualSearchSpec("orbit-control", 8, 1, 64, 1, seed=91)
        )[0]
        generator = np.asarray(instance.generator, dtype=np.uint8)
        basis = next(
            coordinates
            for coordinates in itertools.combinations(range(generator.shape[1]), generator.shape[0])
            if basis_normalized_column_key(generator, coordinates) is not None
        )
        matrix = generator[:, basis]
        inverse = gf2_inverse(matrix)
        self.assertIsNotNone(inverse)
        self.assertTrue(np.array_equal((inverse @ matrix) & 1, np.eye(len(matrix), dtype=np.uint8)))

        transformed = generator.copy()
        transformed[[0, 3]] = transformed[[3, 0]]
        transformed[4] ^= transformed[1]
        permutation = list(range(generator.shape[1]))
        random.Random(92).shuffle(permutation)
        transformed = transformed[:, permutation]
        inverse_permutation = [0] * len(permutation)
        for new_coordinate, old_coordinate in enumerate(permutation):
            inverse_permutation[old_coordinate] = new_coordinate
        mapped_basis = tuple(inverse_permutation[coordinate] for coordinate in basis)
        self.assertEqual(
            basis_normalized_column_key(generator, basis),
            basis_normalized_column_key(transformed, mapped_basis),
        )

    def test_construction_a_root_formula_matches_exact_weight_counts(self):
        instance = generate_self_dual_instances(
            SelfDualSearchSpec("lattice-control", 6, 1, 48, 1, seed=93)
        )[0]
        record = construction_a_lattice_record("lattice-control", instance.__dict__)
        words = enumerate_codewords(np.asarray(instance.generator, dtype=np.uint8))
        weights = words.sum(axis=1)
        weight_two = int(np.count_nonzero(weights == 2))
        weight_four = int(np.count_nonzero(weights == 4))
        self.assertEqual(record.weight_two_codeword_count, weight_two)
        self.assertEqual(record.weight_four_codeword_count, weight_four)
        self.assertEqual(record.norm_two_vector_count, 2 * record.length + 16 * weight_four)
        self.assertTrue(record.unimodular_certificate_passed)
        self.assertEqual(record.scaled_lattice_covolume, 1.0)

    def test_report_never_turns_sample_misses_or_orbit_growth_into_lower_bounds(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_self_dual_code_boundary(
                    specs=(SelfDualSearchSpec("global-k16", 16, 3, 128, 2, seed=94),)
                )
                report = run_self_dual_global_orbit_audit(
                    spec=GlobalOrbitAuditSpec(
                        sampled_information_sets=64,
                        exact_subset_cap=100,
                        maximum_pair_audits_per_family=2,
                    )
                )
            finally:
                os.chdir(old_cwd)
        self.assertFalse(report.claim_gate["sampled_key_miss_is_nonequivalence_evidence"])
        self.assertFalse(report.claim_gate["information_set_growth_is_general_classical_lower_bound"])
        self.assertFalse(report.claim_gate["construction_a_reverse_frame_preservation_proved"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])
        self.assertEqual(report.headline_metrics["proved_polynomial_global_canonicalization_count"], 0)

    def test_writer_registry_triage_and_ledgers_preserve_global_debt(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_self_dual_code_boundary(
                    specs=(SelfDualSearchSpec("global-k16", 16, 3, 128, 1, seed=95),)
                )
                write_self_dual_global_orbit_audit(
                    spec=GlobalOrbitAuditSpec(
                        sampled_information_sets=48,
                        exact_subset_cap=100,
                        maximum_pair_audits_per_family=1,
                    )
                )
                validation = validate_registry()
                triage = build_code_frontier_triage()
                dequantization = write_dequantization_report()
                proofs = write_proof_status_report()
                queries = write_query_model_ledger()
                frontier = write_frontier_map()
            finally:
                os.chdir(old_cwd)
        self.assertTrue(validation["valid"], validation["issues"])
        row = next(item for item in triage.records if item.row_id == "self-dual-family-global-k16")
        self.assertEqual(row.final_status, "proof-debt-not-positive-evidence")
        finding_ids = {item["id"] for item in dequantization["findings"]}
        self.assertIn("DEQ-SELF-DUAL-GLOBAL-INFORMATION-SET-ORBIT-DEBT", finding_ids)
        self.assertIn("DEQ-SELF-DUAL-CONSTRUCTION-A-REVERSE-REDUCTION-DEBT", finding_ids)
        lemma_ids = {item["id"] for item in proofs["proof_debt"]["lemmas"]}
        self.assertIn("LEMMA-CODE-COSET-COLLECTIVE-SELF-DUAL-POLYNOMIAL-GLOBAL-CANONICALIZATION", lemma_ids)
        self.assertIn("LEMMA-CODE-COSET-COLLECTIVE-SELF-DUAL-CONSTRUCTION-A-IFF-REDUCTION", lemma_ids)
        query = next(item for item in queries["records"] if item["candidate_id"] == "CODE-COSET-COLLECTIVE")
        self.assertTrue(any("global-orbit audit" in item.lower() for item in query["blocking_evidence"]))
        code_frontier = next(
            item for item in frontier["frontiers"] if item["frontier_id"] == "code-equivalence-hard-family-search"
        )
        self.assertIn("Self-dual global orbit", code_frontier["evidence"])

    def test_experiment_runner_dispatches_global_orbit_audit(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                with patch(
                    "experiment_runner.write_self_dual_global_orbit_audit",
                    return_value={"status": "test-complete", "summary": "global orbit dispatch"},
                ) as writer, patch("experiment_runner.append_run_history"), patch(
                    "experiment_runner.write_experiment_trends"
                ):
                    result = run_experiment("EXP-CODE-SELF-DUAL-GLOBAL-ORBIT-AUDIT")
            finally:
                os.chdir(old_cwd)
        self.assertIn("EXP-CODE-SELF-DUAL-GLOBAL-ORBIT-AUDIT", supported_experiment_ids())
        self.assertEqual(result.status, "completed")
        writer.assert_called_once()


if __name__ == "__main__":
    unittest.main()
