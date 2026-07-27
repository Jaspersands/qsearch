import json
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch

import numpy as np

from coset_typical_modular_yjm_contraction import (
    build_modular_yjm_contraction_report,
    write_modular_yjm_contraction_report,
)
from symmetric_modular_yjm_contraction import (
    characteristic_polynomial_mod,
    characteristic_polynomial_square_free_mod,
    matrix_power_traces_mod,
    modular_inverse,
    modular_projected_fiber_parallel,
    modular_yjm_separator_block,
    rational_seminormal_generators,
    seminormal_gram_weights,
)


PRIME = 1009


def fraction_mod(value: Fraction) -> int:
    return value.numerator * modular_inverse(value.denominator, PRIME) % PRIME


def dense_generator(generator) -> np.ndarray:
    dimension = len(generator.diagonal)
    matrix = np.zeros((dimension, dimension), dtype=np.int64)
    for column in range(dimension):
        matrix[column, column] = generator.diagonal[column]
        matrix[generator.partner[column], column] += (
            generator.outgoing_off_diagonal[column]
        )
    return matrix % PRIME


class ModularYJMContractionTests(unittest.TestCase):
    def test_rational_seminormal_generators_preserve_coxeter_and_gram(self) -> None:
        generators = tuple(
            dense_generator(generator)
            for generator in rational_seminormal_generators((3, 1, 1), PRIME)
        )
        identity = np.eye(generators[0].shape[0], dtype=np.int64)
        weights = seminormal_gram_weights((3, 1, 1), prime=PRIME)
        gram = np.diag(weights)
        for generator in generators:
            self.assertTrue(
                np.array_equal(generator @ generator % PRIME, identity)
            )
            self.assertTrue(
                np.array_equal(
                    (generator.T @ gram - gram @ generator) % PRIME,
                    np.zeros_like(generator),
                )
            )
        for index in range(len(generators) - 1):
            left = (
                generators[index]
                @ generators[index + 1]
                @ generators[index]
            ) % PRIME
            right = (
                generators[index + 1]
                @ generators[index]
                @ generators[index + 1]
            ) % PRIME
            self.assertTrue(np.array_equal(left, right))

    def test_n5_modular_block_matches_exact_rational_traces(self) -> None:
        block, metrics = modular_yjm_separator_block(
            (3, 1, 1),
            (3, 2),
            2,
            prime=PRIME,
        )
        expected = tuple(
            fraction_mod(value)
            for value in (Fraction(1, 30), Fraction(1, 36))
        )
        self.assertEqual(
            matrix_power_traces_mod(block, 2, prime=PRIME),
            expected,
        )
        self.assertEqual(metrics.projected_rank, 2)
        self.assertEqual(metrics.tableau_fiber_count, 5)
        self.assertFalse(metrics.pair_group_states_materialized)
        self.assertEqual(
            characteristic_polynomial_mod(block, prime=PRIME),
            (
                1,
                fraction_mod(Fraction(-1, 30)),
                fraction_mod(Fraction(-1, 75)),
            ),
        )

    def test_n6_independent_control_matches_exact_rational_traces(self) -> None:
        block, metrics = modular_yjm_separator_block(
            (4, 2),
            (4, 2),
            2,
            prime=PRIME,
        )
        self.assertEqual(
            matrix_power_traces_mod(block, 2, prime=PRIME),
            tuple(
                fraction_mod(value)
                for value in (Fraction(4, 45), Fraction(19, 1350))
            ),
        )
        self.assertEqual(metrics.distinct_nonzero_penalty_count, 35)

    def test_parallel_projector_and_square_free_good_reduction(self) -> None:
        fiber, _, trials, seeds = modular_projected_fiber_parallel(
            (3, 1, 1),
            (3, 2),
            2,
            prime=PRIME,
            workers=2,
            maximum_trials=2,
        )
        self.assertEqual(len(fiber), 2)
        self.assertEqual(trials, 2)
        self.assertEqual(seeds, (0, 1))
        self.assertTrue(
            characteristic_polynomial_square_free_mod(
                (
                    1,
                    fraction_mod(Fraction(-1, 30)),
                    fraction_mod(Fraction(-1, 75)),
                ),
                prime=PRIME,
            )
        )
        self.assertFalse(
            characteristic_polynomial_square_free_mod(
                (1, PRIME - 2, 1),
                prime=PRIME,
            )
        )

    def test_report_removes_factorial_states_without_promoting_scaling(self) -> None:
        report = build_modular_yjm_contraction_report()
        metrics = report.headline_metrics
        self.assertEqual(metrics["exact_modular_power_trace_count"], 4)
        self.assertEqual(metrics["exact_modular_trace_disagreement_count"], 0)
        self.assertEqual(metrics["n10_tensor_dimension"], 589824)
        self.assertGreater(
            metrics["n10_pair_group_to_tensor_dimension_reduction_factor"],
            20_000_000,
        )
        self.assertEqual(metrics["n10_projector_polynomial_degree"], 281)
        self.assertEqual(metrics["compiled_modular_projector_kernel_count"], 0)
        self.assertEqual(
            metrics["exact_n10_multiplicity6_square_free_certificate_count"],
            1,
        )
        self.assertEqual(metrics["n10_direct_exact_square_free_target_count"], 6)
        self.assertEqual(metrics["n10_exact_square_free_target_count"], 10)
        self.assertEqual(
            metrics["n10_inferred_by_conjugate_sign_duality_count"],
            4,
        )
        self.assertEqual(metrics["n10_maximum_exact_certified_multiplicity"], 15)
        self.assertEqual(
            metrics["exact_conjugate_sign_duality_theorem_count"],
            1,
        )
        self.assertEqual(
            metrics["conjugate_sign_duality_validation_pair_count"],
            1,
        )
        self.assertTrue(
            report.claim_gate[
                "n10_multiplicity6_exactly_certified_square_free"
            ]
        )
        self.assertFalse(report.claim_gate["state_dimension_scales_polynomially"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])
        by_target = {
            tuple(record["target_partition"]): record
            for record in report.n10_prime_certificates
        }
        primary_polynomial = by_target[(5, 5)][
            "characteristic_polynomial_mod_prime"
        ]
        self.assertEqual(
            by_target[(2, 2, 2, 2, 2)][
                "characteristic_polynomial_mod_prime"
            ],
            [
                coefficient if index % 2 == 0 else (-coefficient) % PRIME
                for index, coefficient in enumerate(primary_polynomial)
            ],
        )
        self.assertTrue(
            by_target[(8, 2)][
                "rational_characteristic_polynomial_square_free_consequence"
            ]
        )
        self.assertTrue(
            by_target[(6, 4)][
                "rational_characteristic_polynomial_square_free_consequence"
            ]
        )
        self.assertTrue(
            by_target[(7, 3)][
                "rational_characteristic_polynomial_square_free_consequence"
            ]
        )

    def test_write_records_python_kernel_negative_result(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "modular.json"
            negative = Path(directory) / "negative.json"
            results = Path(directory) / "results.json"
            negative.write_text("[]")
            results.write_text("[]")
            with (
                patch("research_registry.NEGATIVE_RESULTS_PATH", negative),
                patch("research_registry.EXPERIMENT_RESULTS_PATH", results),
            ):
                payload = write_modular_yjm_contraction_report(
                    output_path=output,
                )
            self.assertEqual(
                json.loads(negative.read_text())[0]["id"],
                "NEG-COSET-TYPICAL-PURE-PYTHON-MODULAR-YJM-N10-KERNEL",
            )
            self.assertEqual(
                json.loads(results.read_text())[0]["experiment_id"],
                "EXP-COSET-TYPICAL-MODULAR-YJM-CONTRACTION",
            )
            self.assertFalse(payload["claim_gate"]["speedup_claim_allowed"])


if __name__ == "__main__":
    unittest.main()
