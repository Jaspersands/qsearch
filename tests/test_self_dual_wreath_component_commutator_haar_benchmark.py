from fractions import Fraction

import pytest

from self_dual_wreath_component_commutator_haar_benchmark import (
    audit_haar_commutator_formula,
    haar_commutator_asymptotic_record,
    haar_normalized_commutator_trace,
    haar_ordered_pair_moment_gap,
    run_component_commutator_haar_benchmark,
    unitary_weingarten_s4,
)


def test_s4_weingarten_values_match_known_identity_and_transposition() -> None:
    identity = (0, 1, 2, 3)
    transposition = (1, 0, 2, 3)
    dimension = 8

    identity_value = unitary_weingarten_s4(identity, dimension)
    transposition_value = unitary_weingarten_s4(transposition, dimension)
    assert identity_value > 0
    assert transposition_value < 0


@pytest.mark.parametrize(
    ("ambient", "fiber", "block", "expected"),
    [
        (8, 4, 2, Fraction(1, 21)),
        (12, 6, 3, Fraction(27, 572)),
        (20, 10, 2, Fraction(12, 133)),
        (30, 12, 3, Fraction(34749, 503440)),
    ],
)
def test_exact_weingarten_enumeration_matches_closed_formula(
    ambient: int,
    fiber: int,
    block: int,
    expected: Fraction,
) -> None:
    row = audit_haar_commutator_formula(
        "CONTROL",
        ambient,
        fiber,
        block,
    )

    assert row.exact_weingarten_formula_verified is True
    assert Fraction(row.formula_residual) == 0
    assert Fraction(row.exact_normalized_commutator_trace_formula) == expected
    assert Fraction(row.enumerated_normalized_commutator_trace) == expected


def test_pair_gap_and_ordered_pair_count_reconstruct_total() -> None:
    ambient, fiber, block = 20, 10, 2
    outcomes = ambient // block
    pair_gap = haar_ordered_pair_moment_gap(ambient, fiber, block)
    total = outcomes * (outcomes - 1) * pair_gap / fiber

    assert total == haar_normalized_commutator_trace(ambient, fiber, block)


def test_formula_has_exact_commuting_boundaries() -> None:
    one_dimensional = audit_haar_commutator_formula("R1", 8, 1, 2)
    two_outcome = audit_haar_commutator_formula("Q2", 8, 4, 4)

    assert one_dimensional.one_dimensional_boundary is True
    assert Fraction(one_dimensional.exact_normalized_commutator_trace_formula) == 0
    assert two_outcome.two_outcome_boundary is True
    assert Fraction(two_outcome.exact_normalized_commutator_trace_formula) == 0


def test_sparse_block_asymptotic_gap_remains_positive() -> None:
    alpha = 19 / 520
    row = haar_commutator_asymptotic_record(alpha, 0.0)

    assert row.asymptotic_normalized_commutator_trace == pytest.approx(
        alpha**2 * (1 - alpha)
    )
    assert row.sparse_block_limit == pytest.approx(alpha**2 * (1 - alpha))
    assert row.positive_surrogate_signal is True
    assert row.natural_frame_transfer_proved is False


def test_positive_block_aspect_has_expected_suppression() -> None:
    alpha = 0.25
    sparse = haar_commutator_asymptotic_record(alpha, 0.0)
    dense = haar_commutator_asymptotic_record(alpha, 0.1)

    assert dense.asymptotic_normalized_commutator_trace == pytest.approx(
        sparse.sparse_block_limit * 0.9 * 0.8
    )
    assert dense.asymptotic_normalized_commutator_trace < sparse.sparse_block_limit


def test_report_keeps_haar_to_natural_gate_closed() -> None:
    report = run_component_commutator_haar_benchmark()

    assert report.status == (
        "exact-positive-haar-commutator-benchmark-natural-transfer-open"
    )
    assert report.headline_metrics[
        "exact_complex_haar_commutator_formula_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "sparse_block_positive_haar_limit_theorem_count"
    ] == 1
    assert report.headline_metrics["exact_control_failure_count"] == 0
    assert report.headline_metrics["natural_aspect_sparse_haar_normalized_gap"] == pytest.approx(
        (19 / 520) ** 2 * (1 - 19 / 520)
    )
    assert report.claim_gate["haar_jacobi_model_is_natural_wreath_theorem"] is False
    assert report.claim_gate["natural_compressed_component_M4_positive"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False
