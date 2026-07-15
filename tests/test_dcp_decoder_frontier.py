import os
import tempfile
import unittest
from pathlib import Path

from dcp_decoder_frontier import build_decoder_frontier, write_decoder_frontier
from research_registry import initialize_seed_registry, load_experiment_results, validate_registry


class DCPDecoderFrontierTests(unittest.TestCase):
    def test_frontier_rejects_access_invalid_and_dominated_methods(self):
        report = build_decoder_frontier()
        rows = {row.method_id: row for row in report.rows}

        self.assertFalse(rows["chosen-label-phase-estimation"].access_legal_for_regev_dcp)
        self.assertFalse(rows["grover-likelihood-search"].access_legal_for_regev_dcp)
        self.assertIn("kuperberg-generic-sieve", rows["local-quadrature-full-fft"].dominated_by)
        self.assertIn("2^(Theta(n))", rows["local-quadrature-full-fft"].time_class)
        self.assertFalse(rows["structured-query-sparse-fft"].access_legal_for_regev_dcp)
        self.assertTrue(rows["iid-exact-linear-hash-buckets"].access_legal_for_regev_dcp)
        self.assertTrue(rows["iid-biased-linear-margin-buckets"].access_legal_for_regev_dcp)
        self.assertIn("2^Theta(n)", rows["iid-biased-linear-margin-buckets"].state_sample_class)
        self.assertTrue(rows["iid-disjoint-multirecord-product-kernels"].access_legal_for_regev_dcp)
        self.assertIn("4^r", rows["iid-disjoint-multirecord-product-kernels"].time_class)
        self.assertTrue(rows["iid-explicit-overlapping-product-ustatistics"].access_legal_for_regev_dcp)
        self.assertIn("2^Omega(n)", rows["iid-explicit-overlapping-product-ustatistics"].time_class)
        self.assertTrue(rows["iid-rank-one-elementary-symmetric-contraction"].access_legal_for_regev_dcp)
        self.assertIn("Omega(r^2 N/B)", rows["iid-rank-one-elementary-symmetric-contraction"].state_sample_class)
        self.assertTrue(rows["iid-tested-polynomial-rank-contractions"].access_legal_for_regev_dcp)
        self.assertIn("sample-superpolynomial", rows["iid-tested-polynomial-rank-contractions"].blocking_reason)
        self.assertTrue(rows["collective-compute-subset-sum-qft"].access_legal_for_regev_dcp)
        self.assertIn("exactly uniform", rows["collective-compute-subset-sum-qft"].blocking_reason)
        self.assertIn("2^Omega(n)", rows["collective-exact-residue-mps"].memory_class)
        self.assertIn(
            "2^(Omega(n))",
            rows["collective-approximate-fiber-tensor-layout-dictionary"].memory_class,
        )
        self.assertIn(
            "label-adaptive",
            rows["collective-approximate-fiber-tensor-layout-dictionary"].blocking_reason,
        )
        self.assertIn("exponential postselection", rows["collective-hashed-hadamard-fiber-erasure"].time_class)
        self.assertIn("polynomial-trace", rows["collective-public-low-trace-reference-projection"].blocking_reason)
        self.assertIn("remain open", rows["collective-public-low-trace-reference-projection"].blocking_reason)
        self.assertIn("information complexity", rows["collective-clean-covariant-pgm"].blocking_reason)
        self.assertIn("unknown", rows["collective-clean-covariant-pgm"].time_class)
        self.assertIn("information robustness proofs", rows["collective-clean-covariant-pgm"].exact_f1_robustness)
        self.assertIn("partial deterministic solver", rows["regev-partial-average-subset-sum-route"].blocking_reason)
        self.assertEqual(rows["regev-partial-average-subset-sum-route"].dominated_by, [])
        self.assertIn(
            "interface obstruction is resolved",
            rows["shared-seed-randomized-partial-solver-interface"].blocking_reason,
        )
        self.assertIn(
            "orthogonal which-path workspaces",
            rows["general-quantum-relation-partial-solver-interface"].blocking_reason,
        )
        self.assertIn(
            "paired-workspace fidelity",
            rows["general-quantum-relation-partial-solver-interface"].blocking_reason,
        )
        self.assertIn(
            "legitimate non-sign-isometric",
            rows["odd-unit-randomized-lll-partial-subset-sum"].blocking_reason,
        )
        self.assertIn(
            "easy-orbit measure and LLL theorem",
            rows["odd-unit-randomized-lll-partial-subset-sum"].blocking_reason,
        )
        self.assertIn(
            "Blind orbit sampling is cut",
            rows["odd-unit-randomized-lll-partial-subset-sum"].blocking_reason,
        )
        self.assertIn("collapses in the tail", rows["deterministic-modular-lll-partial-subset-sum"].blocking_reason)
        self.assertIn("polynomial", rows["deterministic-modular-lll-partial-subset-sum"].time_class)
        self.assertIn("exponential enumeration", rows["two-adic-carry-lifting-partial-subset-sum"].blocking_reason)
        self.assertIn("no polynomial", rows["two-adic-carry-lifting-partial-subset-sum"].time_class)
        self.assertIn("remain exponential", rows["known-subset-sum-resource-frontier"].blocking_reason)
        self.assertIn("0.218", rows["known-subset-sum-resource-frontier"].time_class)
        self.assertIn("not bounded degree", rows["bounded-degree-two-adic-carry-reconstruction"].blocking_reason)
        self.assertIn("exact polynomial low-bit representation is proved", rows["logarithmic-low-bit-bdd-preconditioner"].blocking_reason)
        self.assertIn("poly(n)", rows["logarithmic-low-bit-bdd-preconditioner"].time_class)
        self.assertIn("explicit-list shortcut", rows["conditioned-high-bit-quotient-implicit-decoder"].blocking_reason)
        self.assertIn("2^Theta(n)", rows["conditioned-high-bit-quotient-implicit-decoder"].time_class)
        self.assertIn("does not improve paired tail", rows["carry-sliced-quotient-lattice"].blocking_reason)
        self.assertIn("poly(n)", rows["carry-sliced-quotient-lattice"].time_class)
        self.assertIn("size-biased", rows["source-target-high-representation-partial-solver"].blocking_reason)
        self.assertIn("2^Theta(n)", rows["source-target-high-representation-partial-solver"].time_class)
        self.assertIn("2^(Theta(n))", rows["exact-likelihood-interval-branch-bound"].time_class)

    def test_polynomial_target_remains_open_and_exact_f1_gated(self):
        report = build_decoder_frontier()
        rows = {row.method_id: row for row in report.rows}

        self.assertTrue(rows["target-polynomial-dcp-decoder"].access_legal_for_regev_dcp)
        self.assertEqual(rows["target-polynomial-dcp-decoder"].exact_f1_robustness, "required")
        self.assertEqual(report.headline_metrics["proved_polynomial_exact_f1_decoder_count"], 0)
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_registers_frontier_result(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_decoder_frontier()
                results = load_experiment_results()
                validation = validate_registry()
                artifact_exists = Path("research/phase_workbench/dcp_decoder_frontier.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertTrue(any(item["experiment_id"] == "EXP-DHS-DCP-DECODER-FRONTIER" for item in results))
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
