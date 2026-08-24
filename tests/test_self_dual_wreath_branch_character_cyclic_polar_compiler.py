import cmath
import math
import tempfile
import unittest
from pathlib import Path

import numpy as np

from self_dual_wreath_branch_character_cyclic_polar_compiler import (
    _cyclic_phase,
    audit_local_cyclic_polar,
    audit_tensor_character_polar,
    cyclic_polar_cocycle_countercontrol,
    cyclic_polar_scaling_record,
    permutation_order,
    run_branch_character_cyclic_polar_compiler,
    write_branch_character_cyclic_polar_report,
)


class BranchCharacterCyclicPolarCompilerTests(unittest.TestCase):
    def test_cyclic_phase_matches_scalar_polar(self) -> None:
        for order in range(1, 9):
            omega = cmath.exp(2j * math.pi / order)
            for phase in range(order):
                eigenvalue = omega**phase
                for sign in (1, -1):
                    scalar = (1 + sign * eigenvalue) / 2
                    expected = scalar / abs(scalar) if abs(scalar) > 1e-10 else 0j
                    self.assertAlmostEqual(
                        abs(_cyclic_phase(phase, order, sign) - expected),
                        0.0,
                        places=9,
                    )

    def test_permutation_order(self) -> None:
        self.assertEqual(permutation_order((0, 1, 2)), 1)
        self.assertEqual(permutation_order((1, 0, 2)), 2)
        self.assertEqual(permutation_order((1, 2, 0)), 3)
        self.assertEqual(permutation_order((1, 2, 3, 0)), 4)

    def test_local_known_relative_polar_handles_kernel_and_full_rank(self) -> None:
        transposition = audit_local_cyclic_polar(
            "TRANSPOSE-KERNEL",
            (3,),
            (2, 1),
            (1, 0, 2),
            1,
        )
        cycle = audit_local_cyclic_polar(
            "THREE-CYCLE-FULL",
            (3,),
            (2, 1),
            (1, 2, 0),
            1,
        )
        self.assertTrue(transposition.exact_known_relative_cyclic_polar_verified)
        self.assertEqual(transposition.active_singular_value_count, 1)
        self.assertTrue(cycle.exact_known_relative_cyclic_polar_verified)
        self.assertEqual(cycle.active_singular_value_count, 2)
        self.assertFalse(cycle.inverse_singular_value_amplification_used)

    def test_tensor_character_polar_factorizes(self) -> None:
        labels = (
            ((3,), (2, 1)),
            ((3,), (1, 1, 1)),
            ((2, 1), (1, 1, 1)),
        )
        controls = [
            audit_tensor_character_polar(
                f"CHAR-{character}",
                labels,
                (1, 2, 0),
                character,
            )
            for character in range(8)
        ]
        self.assertTrue(
            all(row.exact_tensor_polar_factorization_verified for row in controls)
        )
        self.assertLess(
            max(row.direct_to_tensor_cyclic_polar_residual for row in controls),
            1e-8,
        )

    def test_natural_full_rank_cocycle_defect_is_two(self) -> None:
        control = cyclic_polar_cocycle_countercontrol()
        self.assertTrue(control.exact_norm_two_cocycle_failure_verified)
        self.assertEqual(control.generator_order, 3)
        self.assertEqual(control.generator_polar_rank, 2)
        self.assertEqual(control.squared_generator_polar_rank, 2)
        self.assertAlmostEqual(control.cocycle_operator_norm_defect, 2.0, places=9)
        self.assertFalse(control.observed_time_only_phase_stripping_possible)

    def test_scaling_preserves_claim_boundaries(self) -> None:
        row = cyclic_polar_scaling_record(128)
        self.assertTrue(row.known_relative_tensor_character_polar_polynomial)
        self.assertFalse(row.hidden_relative_element_available_to_decoder)
        self.assertFalse(row.polar_field_cocycle_proved)
        self.assertFalse(row.joint_multiplicity_inverse_compiled)
        self.assertLessEqual(
            row.permutation_order_register_qubit_upper_bound,
            math.ceil(math.lgamma(129) / math.log(2)),
        )

    def test_report_and_artifact_keep_algorithm_gate_false(self) -> None:
        report = run_branch_character_cyclic_polar_compiler()
        self.assertEqual(report.status, "known-relative-character-polar-compiled-covariant-assembly-open")
        self.assertEqual(
            report.headline_metrics["finite_local_control_failure_count"],
            0,
        )
        self.assertEqual(
            report.headline_metrics["finite_tensor_control_failure_count"],
            0,
        )
        self.assertTrue(
            report.claim_gate["known_relative_tensor_character_polar_polynomial"]
        )
        self.assertFalse(report.claim_gate["polar_field_is_cocycle"])
        self.assertFalse(report.claim_gate["complete_orientation_polar_compiled"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "report.json"
            payload = write_branch_character_cyclic_polar_report(path)
            self.assertTrue(path.exists())
            self.assertEqual(payload["status"], report.status)


if __name__ == "__main__":
    unittest.main()
