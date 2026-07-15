import os
import tempfile
import unittest
from pathlib import Path

from dcp_subset_sum_lattice_search import (
    modular_subset_sum_embedding,
    run_lattice_solver_trial,
    run_subset_sum_lattice_search,
    solve_with_lll_embedding,
    solve_with_lll_embedding_diagnostics,
    write_subset_sum_lattice_search,
)
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class DCPSubsetSumLatticeSearchTests(unittest.TestCase):
    def test_embedding_has_polynomial_dimension_and_bit_length(self):
        basis = modular_subset_sum_embedding([3, 17, 29, 41], 11, 256, 4)

        self.assertEqual(basis.shape, (6, 6))
        self.assertLessEqual(max(abs(int(value)).bit_length() for value in basis), 13)

    def test_solver_returns_only_exact_valid_witnesses(self):
        labels = [3, 17, 29, 41, 73, 101, 127, 191, 5, 11, 19, 23]
        target = sum(labels[index] for index in (0, 3, 5, 8)) % 256
        witness, _, _ = solve_with_lll_embedding(8, labels, target, combination_arity=2)

        self.assertIsNotNone(witness)
        self.assertEqual(sum(label * bit for label, bit in zip(labels, witness)) % 256, target)

    def test_diagnostics_preserve_solver_and_expose_reduced_geometry(self):
        labels = [3, 17, 29, 41, 73, 101, 127, 191, 5, 11, 19, 23]
        target = sum(labels[index] for index in (0, 3, 5, 8)) % 256
        witness, checked, maximum_bits = solve_with_lll_embedding(
            8, labels, target, combination_arity=2
        )
        diagnostics = solve_with_lll_embedding_diagnostics(
            8, labels, target, combination_arity=2
        )

        self.assertEqual(diagnostics.witness, witness)
        self.assertEqual(diagnostics.candidate_vectors_checked, checked)
        self.assertEqual(diagnostics.maximum_entry_bit_length, maximum_bits)
        self.assertEqual(diagnostics.ideal_witness_norm_squared, len(labels) + 1)
        self.assertGreater(diagnostics.minimum_reduced_row_norm_squared, 0)
        self.assertGreaterEqual(diagnostics.minimum_reduced_to_ideal_norm_ratio, 0.0)

    def test_trial_never_marks_finite_success_as_source_contract(self):
        trial = run_lattice_solver_trial(8, 4, 4, 0.75, 2, seed=3)

        self.assertTrue(trial.target_legal_exactly_known)
        self.assertEqual(trial.solved, trial.returned_witness_valid)

    def test_search_tracks_tail_collapse_and_proof_debt(self):
        report = run_subset_sum_lattice_search(
            n_values=[12, 16, 20, 24, 28],
            register_offsets=[4],
            embedding_scales=[4],
            lll_deltas=[0.75],
            combination_arities=[1],
            trials_per_row=4,
            seed=10,
        )

        self.assertEqual(report.headline_metrics["invalid_witness_count"], 0)
        self.assertEqual(report.headline_metrics["source_contract_satisfying_row_count"], 0)
        self.assertFalse(report.claim_gate["uniform_inverse_polynomial_coverage_proved"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_registers_restricted_lattice_negative(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_subset_sum_lattice_search(
                    n_values=[8, 12],
                    register_offsets=[4],
                    embedding_scales=[4],
                    lll_deltas=[0.75],
                    combination_arities=[1],
                    trials_per_row=2,
                )
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path("research/classical_baselines/dcp_subset_sum_lattice_search.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertTrue(any(item["experiment_id"] == "EXP-DHS-DCP-SUBSET-SUM-LATTICE-SEARCH" for item in results))
        self.assertIn("NEG-DCP-TESTED-LLL-DENSITY-ONE-PARTIAL-SOLVERS", {item["id"] for item in negatives})
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
