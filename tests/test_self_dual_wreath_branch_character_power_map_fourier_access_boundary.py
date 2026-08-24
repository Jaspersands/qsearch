import itertools
import json
import math

import numpy as np

from self_dual_wreath_branch_character_power_map_fourier_access_boundary import (
    audit_cyclic_power_map_fourier,
    cyclic_multiplier_monomial,
    cyclic_power_map_isometry,
    power_map_access_scaling,
    power_tuple,
    run_power_map_fourier_access_boundary,
    transformed_cyclic_power_map,
    write_power_map_fourier_access_boundary_report,
)


def test_paired_power_map_is_injective_for_arbitrary_exponents() -> None:
    for order in range(2, 10):
        for parameters in ((0,), (1,), (2,), (-3,), (2, -1)):
            isometry = cyclic_power_map_isometry(order, parameters)
            assert np.linalg.norm(
                isometry.conj().T @ isometry - np.eye(order),
                ord=2,
            ) < 1e-12
            exponents = power_tuple(parameters)
            assert all(
                exponents[index] + exponents[index + 1] == 1
                for index in range(0, len(exponents), 2)
            )


def test_qft_conjugated_power_map_remains_an_isometry() -> None:
    for order, parameters in ((5, (2,)), (3, (2, 1)), (4, (-1,))):
        transformed = transformed_cyclic_power_map(order, parameters)
        assert np.linalg.norm(
            transformed.conj().T @ transformed - np.eye(order),
            ord=2,
        ) < 1e-10


def test_every_cyclic_fourier_block_has_the_exact_dimension_factor() -> None:
    for order in (3, 4, 5):
        parameters = (2,)
        exponents = power_tuple(parameters)
        for outputs in itertools.product(range(order), repeat=len(exponents)):
            input_character = sum(
                character * exponent
                for character, exponent in zip(outputs, exponents)
            ) % order
            control = audit_cyclic_power_map_fourier(
                "block",
                order,
                parameters,
                input_character,
                outputs,
            )
            assert control.selection_rule_satisfied
            assert control.exact_power_map_fourier_normalization_verified
            assert math.isclose(control.predicted_block_normalization, order)


def test_selection_rule_zero_blocks_are_exactly_zero() -> None:
    control = audit_cyclic_power_map_fourier(
        "zero",
        5,
        (2,),
        3,
        (1, 1),
    )
    assert not control.selection_rule_satisfied
    assert abs(complex(*control.direct_multiplier_monomial)) < 1e-10
    assert abs(complex(*control.transformed_fourier_block)) < 1e-10
    assert control.exact_power_map_fourier_normalization_verified


def test_direct_monomial_matches_explicit_frequency_conservation() -> None:
    order = 7
    parameters = (3, -2)
    exponents = power_tuple(parameters)
    outputs = (1, 2, 3, 4)
    frequency = sum(
        character * exponent
        for character, exponent in zip(outputs, exponents)
    ) % order
    nonzero = cyclic_multiplier_monomial(
        order,
        parameters,
        frequency,
        outputs,
    )
    zero = cyclic_multiplier_monomial(
        order,
        parameters,
        (frequency + 1) % order,
        outputs,
    )
    assert math.isclose(abs(nonzero), math.sqrt(order), rel_tol=1e-10)
    assert abs(zero) < 1e-10


def test_natural_scaling_makes_termwise_extraction_superpolynomial() -> None:
    rows = [power_map_access_scaling(n) for n in (8, 16, 32, 64)]
    assert all(row.termwise_power_map_block_extraction_superpolynomial for row in rows)
    assert all(not row.coherent_full_quadrant_sum_compiled for row in rows)
    assert all(
        right.termwise_block_normalization_log2_lower_bound
        > left.termwise_block_normalization_log2_lower_bound
        for left, right in zip(rows, rows[1:])
    )


def test_report_rejects_termwise_but_keeps_whole_sum_open() -> None:
    report = run_power_map_fourier_access_boundary()
    assert report.theorem.theorem_verified
    assert all(row.selection_rule_satisfied for row in report.nonzero_controls)
    assert all(not row.selection_rule_satisfied for row in report.zero_controls)
    assert report.claim_gate["paired_power_map_injective_isometry_proved"]
    assert report.claim_gate["power_map_fourier_block_identity_proved"]
    assert report.claim_gate[
        "termwise_power_map_compiler_superpolynomial_proved"
    ]
    assert not report.claim_gate["coherent_full_quadrant_sum_factorized"]
    assert not report.claim_gate["direct_equivariant_multiplier_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_writer_emits_live_artifact(tmp_path) -> None:
    path = tmp_path / "power-map-fourier-access.json"
    payload = write_power_map_fourier_access_boundary_report(path)
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert loaded["status"] == payload["status"]
    assert loaded["headline_metrics"][
        "termwise_power_map_normalization_no_go_count"
    ] == 1
