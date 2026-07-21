import math
import os
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

from coset_typical_irrep_transfer_audit import (
    audit_typical_irrep_transfer,
    bounded_tail_count,
    bounded_tail_weak_probability_upper_bound,
    build_typical_irrep_transfer_report,
    write_typical_irrep_transfer_report,
)
from dequantization_checks import findings_from_coset_typical_irrep_transfer
from experiment_runner import run_experiment, supported_experiment_ids
from research_registry import (
    initialize_seed_registry,
    load_negative_results,
    validate_registry,
)


class TypicalIrrepTransferAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = build_typical_irrep_transfer_report()

    def test_fixed_bounded_tail_union_has_factorial_probability_bound(self) -> None:
        self.assertEqual(bounded_tail_count(4), 12)
        for n in (8, 12, 20, 32):
            expected = Fraction(24 * n**8, math.factorial(n))
            self.assertEqual(
                bounded_tail_weak_probability_upper_bound(n, 4), expected
            )
        self.assertGreater(
            bounded_tail_weak_probability_upper_bound(20, 4),
            bounded_tail_weak_probability_upper_bound(32, 4),
        )
        self.assertEqual(
            self.report.headline_metrics[
                "bounded_tail_natural_access_no_go_theorem_count"
            ],
            1,
        )

    def test_exact_typical_profiles_verify_kronecker_dimension_identity(self) -> None:
        self.assertEqual(len(self.report.records), 7)
        self.assertTrue(
            all(
                record.exact_weighted_dimension_identity_verified
                for record in self.report.records
            )
        )
        n20 = audit_typical_irrep_transfer(20)
        self.assertEqual(n20.source_partition, (7, 5, 3, 2, 2, 1))
        self.assertEqual(n20.source_dimension, 249420600)
        self.assertEqual(n20.kronecker_target_support_count, 626)
        self.assertEqual(n20.partition_count, 627)
        self.assertEqual(n20.maximum_kronecker_multiplicity, 6408361)
        self.assertEqual(n20.targets_for_ninety_percent_coupling_mass, 148)

    def test_bounded_tail_coupling_mass_collapses_on_finite_controls(self) -> None:
        by_n = {record.n: record for record in self.report.records}
        self.assertGreater(by_n[8].bounded_tail_coupling_mass, 0.5)
        self.assertLess(by_n[12].bounded_tail_coupling_mass, 0.006)
        self.assertLess(by_n[16].bounded_tail_coupling_mass, 4e-6)
        self.assertLess(by_n[20].bounded_tail_coupling_mass, 3e-10)
        self.assertGreater(by_n[20].coupling_target_entropy_bits, 7.2)
        self.assertGreater(by_n[20].source_tail_size, 4)

    def test_claim_gate_requires_uniform_typical_label_circuits(self) -> None:
        gate = self.report.claim_gate
        self.assertFalse(gate["bounded_tail_stable_route_naturally_accessible"])
        self.assertTrue(gate["typical_label_adaptation_required"])
        self.assertFalse(gate["finite_typical_profiles_are_complexity_theorems"])
        self.assertFalse(gate["uniform_typical_label_multiplicity_transform_proved"])
        self.assertFalse(gate["speedup_claim_allowed"])
        self.assertEqual(
            self.report.required_typical_label_interface[
                "current_proved_operation_count"
            ],
            0,
        )

    def test_writer_runner_registry_and_dequantization_record_transfer_debt(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_typical_irrep_transfer_report(
                    n_values=(8, 10, 12)
                )
                runner = run_experiment("EXP-COSET-TYPICAL-IRREP-TRANSFER-AUDIT")
                findings = findings_from_coset_typical_irrep_transfer()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/representation/coset_typical_irrep_transfer_audit.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(runner.status, "completed")
        self.assertIn(
            "EXP-COSET-TYPICAL-IRREP-TRANSFER-AUDIT",
            supported_experiment_ids(),
        )
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].severity, "critical")
        self.assertIn("BOUNDED-TAIL", findings[0].id)
        self.assertIn(
            "NEG-COSET-FIXED-BOUNDED-TAIL-FOURIER-ROUTE",
            {item["id"] for item in negatives},
        )
        self.assertEqual(
            payload["headline_metrics"][
                "uniform_typical_label_commutant_gap_theorem_count"
            ],
            0,
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
