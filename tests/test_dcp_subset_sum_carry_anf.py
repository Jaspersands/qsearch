import os
import tempfile
import unittest
from pathlib import Path

from dcp_subset_sum_carry_anf import (
    analyze_carry_anf_trial,
    anf_profile,
    run_subset_sum_carry_anf_audit,
    write_subset_sum_carry_anf_audit,
)
from research_registry import initialize_seed_registry, load_negative_results


class DCPSubsetSumCarryANFTests(unittest.TestCase):
    def test_anf_profile_recovers_parity_degree_and_sparsity(self):
        truth = [mask.bit_count() & 1 for mask in range(8)]
        degree, monomial_count, top_count = anf_profile(truth, 3)
        self.assertEqual(degree, 1)
        self.assertEqual(monomial_count, 3)
        self.assertEqual(top_count, 3)

    def test_first_subset_sum_output_bit_is_affine(self):
        rows, summary = analyze_carry_anf_trial(6, 2, 0, seed=7)
        self.assertEqual(rows[0].exact_anf_degree, 1)
        self.assertEqual(summary.register_count, 8)
        self.assertFalse(summary.polynomial_witness_solver_constructed)

    def test_full_domain_audit_remains_claim_gated(self):
        report = run_subset_sum_carry_anf_audit(
            n_values=[6, 8], register_offsets=[2], trials_per_row=1
        )
        self.assertGreater(report.headline_metrics["carry_row_count"], 0)
        self.assertEqual(report.headline_metrics["source_contract_satisfying_row_count"], 0)
        self.assertFalse(report.claim_gate["high_anf_degree_implies_subset_sum_hardness"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_records_negative_result(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_subset_sum_carry_anf_audit(
                    n_values=[6], register_offsets=[2], trials_per_row=1
                )
                artifact_exists = Path(
                    "research/classical_baselines/dcp_subset_sum_carry_anf.json"
                ).exists()
                negatives = load_negative_results()
            finally:
                os.chdir(old_cwd)
        self.assertTrue(artifact_exists)
        self.assertEqual(payload["headline_metrics"]["proved_polynomial_algebraic_witness_solver_count"], 0)
        self.assertTrue(
            any(item["id"] == "NEG-DCP-FINITE-FULL-DOMAIN-CARRY-ANF-WITHOUT-SOLVER" for item in negatives)
        )


if __name__ == "__main__":
    unittest.main()
