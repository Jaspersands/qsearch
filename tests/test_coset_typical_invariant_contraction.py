import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np

from coset_multiplicity_commutant_search import _orbit_sum
from coset_typical_invariant_contraction import (
    audit_invariant_contraction_block,
    build_invariant_contraction_report,
    numerical_invariant_basis,
    restricted_separator_matrix,
    write_invariant_contraction_report,
)
from symmetric_yjm_multiplicity_contraction import yjm_separator_block


class InvariantContractionTests(unittest.TestCase):
    def test_small_kronecker_block_has_low_residuals(self) -> None:
        record = audit_invariant_contraction_block(
            (3, 2),
            2,
            source_partition=(3, 1, 1),
            arpack_subspace_dimension=8,
        )
        self.assertEqual(record.invariant_vector_dimension, 180)
        self.assertLess(record.maximum_invariant_residual, 1e-8)
        self.assertLess(record.restricted_symmetry_residual, 1e-10)
        self.assertFalse(record.explicit_group_rows_materialized)
        self.assertFalse(record.orbit_terms_materialized)

    def test_representatives_equal_explicit_orbit_averages_on_invariants(
        self,
    ) -> None:
        source = (3, 1, 1)
        target = (3, 2)
        basis, _, _, _ = numerical_invariant_basis(
            (target, source, source),
            2,
            arpack_subspace_dimension=8,
        )
        representative, _ = restricted_separator_matrix(basis, source)
        tt_sum, tt_count, *_ = _orbit_sum(
            source,
            source,
            "ORB-TT-INTERSECTION-1",
            1,
        )
        tc_sum, tc_count, *_ = _orbit_sum(
            source,
            source,
            "ORB-TC-INTERSECTION-1",
            1,
        )
        full = tt_sum / tt_count + tc_sum / tc_count
        flattened = basis.reshape(2, basis.shape[1], -1)
        transformed = np.einsum(
            "ij,mtj->mti",
            full,
            flattened,
            optimize=True,
        )
        explicit = np.einsum(
            "mti,nti->mn",
            flattened,
            transformed,
            optimize=True,
        )
        self.assertTrue(np.allclose(representative, explicit, atol=1e-10))

    def test_yjm_fiber_matches_direct_invariant_spectrum(self) -> None:
        source = (3, 1, 1)
        target = (3, 2)
        direct = audit_invariant_contraction_block(
            target,
            2,
            source_partition=source,
            arpack_subspace_dimension=8,
        )
        yjm, metrics = yjm_separator_block(
            source,
            target,
            2,
            arpack_subspace_dimension=8,
        )
        self.assertTrue(
            np.allclose(
                np.linalg.eigvalsh(yjm),
                direct.separator_eigenvalues,
                atol=1e-10,
            )
        )
        self.assertEqual(metrics.vector_dimension_reduction_factor, 5)
        self.assertEqual(metrics.tableau_fiber_count, 5)
        self.assertLess(metrics.maximum_penalty_residual, 1e-10)
        self.assertLess(metrics.maximum_tableau_propagation_residual, 1e-10)

    def test_stored_control_reproduces_exact_traces(self) -> None:
        report = build_invariant_contraction_report()
        metrics = report.headline_metrics
        self.assertLess(metrics["maximum_exact_control_trace_residual"], 1e-10)
        self.assertEqual(metrics["factorial_group_row_storage_removed_count"], 1)
        self.assertEqual(metrics["exact_multiplicity6_certificate_count"], 0)
        self.assertEqual(
            metrics["polynomial_invariant_contraction_theorem_count"],
            0,
        )
        self.assertGreater(
            metrics["n10_multiplicity6_declared_budget_gap_lower_bound"],
            0,
        )
        self.assertGreater(
            metrics["n10_multiplicity6_declared_budget_margin_ratio"],
            1,
        )
        self.assertEqual(
            metrics["machine_verified_roundoff_certificate_count"],
            0,
        )
        self.assertFalse(
            report.claim_gate["declared_error_budget_is_machine_verified"]
        )
        self.assertFalse(report.claim_gate["interval_arithmetic_verified"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_write_records_result_without_promoting_numerics(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "invariant.json"
            negative = Path(directory) / "negative.json"
            results = Path(directory) / "results.json"
            negative.write_text("[]")
            results.write_text("[]")
            with (
                patch("research_registry.NEGATIVE_RESULTS_PATH", negative),
                patch("research_registry.EXPERIMENT_RESULTS_PATH", results),
            ):
                payload = write_invariant_contraction_report(
                    output_path=output,
                )
            self.assertFalse(payload["claim_gate"]["multiplicity6_exactly_certified"])
            self.assertEqual(
                {
                    row["id"] for row in json.loads(negative.read_text())
                },
                {
                    "NEG-COSET-TYPICAL-DIRECT-COXETER-MULTIPLICITY6-SCALING",
                    "NEG-COSET-TYPICAL-EXPLICIT-S10-ROWS-ARE-NOT-A-FINITE-BLOCK-REQUIREMENT",
                },
            )
            self.assertEqual(
                json.loads(results.read_text())[0]["experiment_id"],
                "EXP-COSET-TYPICAL-INVARIANT-CONTRACTION",
            )


if __name__ == "__main__":
    unittest.main()
