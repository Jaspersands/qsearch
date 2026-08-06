import math
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from dequantization_checks import write_dequantization_report
from experiment_runner import (
    run_experiment,
    select_next_experiment,
    supported_experiment_ids,
)
from proof_tracker import write_proof_status_report
from query_model_ledger import write_query_model_ledger
from research_frontier_map import write_frontier_map
from research_registry import initialize_seed_registry, validate_registry
from self_dual_wreath_carrier_orbit_growth import (
    simultaneous_conjugacy_orbit_count,
)
from self_dual_wreath_harmonic_carrier_schema import (
    audit_harmonic_carrier_scaling,
    conjugation_multiplicity,
    harmonic_multiplicity_blocks,
    run_self_dual_wreath_harmonic_carrier_schema,
    write_self_dual_wreath_harmonic_carrier_schema,
)


class SelfDualWreathHarmonicCarrierSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = run_self_dual_wreath_harmonic_carrier_schema()

    def test_conjugation_multiplicities_match_small_exact_control(self):
        self.assertEqual(conjugation_multiplicity((3,)), 3)
        self.assertEqual(conjugation_multiplicity((2, 1)), 1)
        self.assertEqual(conjugation_multiplicity((1, 1, 1)), 1)

    def test_kronecker_blocks_reproduce_burnside_pair_orbits(self):
        for n in range(2, 11):
            blocks = harmonic_multiplicity_blocks(n)
            self.assertEqual(
                sum(
                    block.invariant_matrix_coordinate_count
                    for block in blocks
                ),
                simultaneous_conjugacy_orbit_count(n, 2),
            )
            scaling, _ = audit_harmonic_carrier_scaling(n, exact=True)
            self.assertTrue(
                scaling.harmonic_burnside_identity_verified
            )

    def test_compact_addresses_do_not_hide_dense_block_lower_bound(self):
        scaling, blocks = audit_harmonic_carrier_scaling(12, exact=True)
        maximum = max(
            block.conjugation_multiplicity for block in blocks
        )
        self.assertEqual(maximum, 7507)
        lower = int(
            scaling.factorial_average_block_coordinate_lower_bound_decimal
        )
        self.assertGreaterEqual(lower, math.factorial(12) // 77)
        self.assertTrue(scaling.compact_coordinate_address)
        self.assertFalse(scaling.polynomial_dense_block_dimension_proved)
        self.assertFalse(scaling.internal_kronecker_basis_transform_proved)

    def test_tail_theorem_blocks_dense_harmonic_enumeration(self):
        scaling, blocks = audit_harmonic_carrier_scaling(64, exact=False)
        self.assertEqual(blocks, [])
        self.assertGreater(
            scaling.log2_certified_maximum_block_coordinate_lower_bound,
            275,
        )
        self.assertGreater(
            scaling.log2_certified_maximum_multiplicity_lower_bound,
            137,
        )
        self.assertFalse(scaling.polynomial_outer_block_count)
        self.assertFalse(scaling.sparse_carrier_product_rules_proved)

    def test_report_separates_schema_from_transform(self):
        metrics = self.report.headline_metrics
        self.assertEqual(
            metrics["harmonic_burnside_identity_verification_count"],
            11,
        )
        self.assertEqual(
            metrics["compact_harmonic_coordinate_schema_count"],
            17,
        )
        self.assertEqual(
            metrics["uniform_coherent_harmonic_transform_count"],
            0,
        )
        self.assertTrue(
            self.report.claim_gate[
                "depth_three_harmonic_burnside_identity_verified"
            ]
        )
        self.assertFalse(
            self.report.claim_gate[
                "efficient_sn_qft_alone_resolves_carrier_blocks"
            ]
        )
        self.assertFalse(self.report.claim_gate["speedup_claim_allowed"])

    def test_writer_updates_ledgers_and_frontier(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_self_dual_wreath_harmonic_carrier_schema()
                validation = validate_registry()
                dequantization = write_dequantization_report()
                proofs = write_proof_status_report()
                queries = write_query_model_ledger()
                frontier = write_frontier_map()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(validation["valid"], validation["issues"])
        finding_ids = {item["id"] for item in dequantization["findings"]}
        self.assertIn(
            "DEQ-SELF-DUAL-WREATH-HARMONIC-LABELS-NOT-TRANSFORM",
            finding_ids,
        )
        self.assertIn(
            "DEQ-SELF-DUAL-WREATH-DENSE-MULTIPLICITY-BLOCK",
            finding_ids,
        )
        lemmas = {
            item["id"]: item
            for item in proofs["proof_debt"]["lemmas"]
        }
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-SELF-DUAL-WREATH-HARMONIC-CARRIER-SCHEMA"
            ]["status"],
            "proved-harmonic-carrier-schema",
        )
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-SELF-DUAL-WREATH-SPARSE-HARMONIC-CARRIER-TRANSFORM"
            ]["status"],
            "blocked-dense-multiplicity-blocks-no-sparse-transform",
        )
        query = next(
            item
            for item in queries["records"]
            if item["candidate_id"] == "CODE-COSET-COLLECTIVE"
        )
        self.assertTrue(
            any(
                "harmonic carrier schema verifies" in item.lower()
                for item in query["blocking_evidence"]
            )
        )
        code_frontier = next(
            item
            for item in frontier["frontiers"]
            if item["frontier_id"] == "code-equivalence-hard-family-search"
        )
        self.assertEqual(
            code_frontier["status"],
            "self-dual-wreath-sparse-harmonic-carrier-transform",
        )

    def test_runner_dispatches_and_prioritizes_harmonic_schema(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                Path("research").mkdir(exist_ok=True)
                Path("research/frontier_map.json").write_text(
                    """{
  "top_frontier": "code-equivalence-hard-family-search",
  "frontiers": [{
    "frontier_id": "code-equivalence-hard-family-search",
    "status": "self-dual-wreath-compressed-harmonic-carrier-transform"
  }]
}"""
                )
                Path("research/blocker_taxonomy.json").write_text(
                    '{"top_actionable_blocker_class": "code-equivalence-invariant-collapse"}'
                )
                selection = select_next_experiment()
                with patch(
                    "experiment_runner.write_self_dual_wreath_harmonic_carrier_schema",
                    return_value={
                        "status": "test-complete",
                        "summary": "wreath harmonic carrier dispatch",
                    },
                ) as writer, patch(
                    "experiment_runner.append_run_history"
                ), patch(
                    "experiment_runner.write_experiment_trends"
                ):
                    result = run_experiment(
                        "EXP-CODE-SELF-DUAL-WREATH-HARMONIC-CARRIER-SCHEMA"
                    )
            finally:
                os.chdir(old_cwd)

        self.assertIn(
            "EXP-CODE-SELF-DUAL-WREATH-HARMONIC-CARRIER-SCHEMA",
            supported_experiment_ids(),
        )
        self.assertEqual(
            selection.experiment_id,
            "EXP-CODE-SELF-DUAL-WREATH-HARMONIC-CARRIER-SCHEMA",
        )
        self.assertEqual(result.status, "completed")
        writer.assert_called_once()


if __name__ == "__main__":
    unittest.main()
