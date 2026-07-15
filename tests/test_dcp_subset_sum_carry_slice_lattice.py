import os
import tempfile
import unittest
from pathlib import Path

from dcp_subset_sum_carry_slice_lattice import (
    constrained_low_bits,
    decode_carry_sliced_vector,
    reachable_carries,
    run_carry_slice_lattice_search,
    solve_with_carry_sliced_lll,
    write_carry_slice_lattice_search,
)
from research_registry import initialize_seed_registry, load_negative_results


class DCPSubsetSumCarrySliceLatticeTests(unittest.TestCase):
    def test_reachable_carries_are_polynomially_bounded_and_exact(self):
        labels = [3, 5, 6, 7]
        carries = reachable_carries(labels, target=5, low_bits=3)
        self.assertEqual(carries, [0, 1, 2])
        self.assertLessEqual(len(carries), len(labels))

    def test_decoder_enforces_original_equation_and_carry(self):
        n_bits = 6
        low_bits = 2
        labels = [3, 5, 11, 17]
        witness = [1, 0, 1, 0]
        target = sum(label * bit for label, bit in zip(labels, witness)) % (1 << n_bits)
        low_modulus = 1 << low_bits
        low_sum = sum((label % low_modulus) * bit for label, bit in zip(labels, witness))
        carry = (low_sum - target % low_modulus) // low_modulus
        vector = [2 * bit - 1 for bit in witness] + [0, 0, -1]
        self.assertEqual(
            decode_carry_sliced_vector(vector, labels, target, n_bits, low_bits, carry),
            witness,
        )
        self.assertIsNone(
            decode_carry_sliced_vector(vector, labels, target, n_bits, low_bits, carry + 1)
        )

    def test_solver_never_returns_an_invalid_witness(self):
        n_bits = 7
        labels = [5, 11, 17, 23, 31, 37, 43, 51, 59]
        target = 42
        witness, _, _, carry_count, _ = solve_with_carry_sliced_lll(
            n_bits,
            labels,
            target,
            constrained_low_bits(n_bits, 1),
            combination_arity=2,
        )
        self.assertLessEqual(carry_count, len(labels))
        if witness is not None:
            self.assertEqual(sum(a * x for a, x in zip(labels, witness)) % (1 << n_bits), target)

    def test_report_keeps_finite_solver_improvements_proof_gated(self):
        report = run_carry_slice_lattice_search(
            n_values=[8],
            register_offsets=[2],
            lll_deltas=[0.75],
            trials_per_row=1,
        )
        self.assertEqual(report.headline_metrics["invalid_witness_count"], 0)
        self.assertEqual(report.headline_metrics["polynomial_carry_enumeration_certificate_count"], 1)
        self.assertFalse(report.claim_gate["finite_improvement_is_coverage_theorem"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_records_artifact_and_negative_result(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_carry_slice_lattice_search(
                    n_values=[8],
                    register_offsets=[2],
                    lll_deltas=[0.75],
                    trials_per_row=1,
                )
                artifact_exists = Path(
                    "research/classical_baselines/dcp_subset_sum_carry_slice_lattice.json"
                ).exists()
                negatives = load_negative_results()
            finally:
                os.chdir(old_cwd)
        self.assertTrue(artifact_exists)
        self.assertEqual(payload["headline_metrics"]["source_contract_satisfying_row_count"], 0)
        self.assertTrue(
            any(
                item["id"] == "NEG-DCP-CARRY-SLICED-LLL-FINITE-WITHOUT-COVERAGE-THEOREM"
                for item in negatives
            )
        )


if __name__ == "__main__":
    unittest.main()
