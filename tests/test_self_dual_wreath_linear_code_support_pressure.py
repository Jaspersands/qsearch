import itertools

import pytest

from self_dual_wreath_linear_code_support_pressure import (
    audit_linear_code_pressure,
    binary_linear_subspaces,
    code_dimension,
    gf2_rref_basis,
    is_binary_linear_subspace,
    run_linear_code_support_pressure,
)
from self_dual_wreath_marked_relation_topology import (
    marked_support_presentation,
    presentation_solution_count,
)


def _parity_code(width: int):
    return tuple(
        row
        for row in itertools.product((0, 1), repeat=width)
        if sum(row) % 2 == 0
    )


def test_rref_basis_words_have_distinct_unique_pivots():
    code = _parity_code(5)
    basis = gf2_rref_basis(code)
    pivots = tuple(row.index(1) for row in basis)
    assert code_dimension(code) == 4
    assert len(set(pivots)) == 4
    assert all(
        row[pivot] == int(row_index == pivot_index)
        for row_index, row in enumerate(basis)
        for pivot_index, pivot in enumerate(pivots)
    )
    assert all(row in code for row in basis)


def test_non_linear_support_is_not_promoted_to_code_theorem():
    support = ((0, 0, 0), (1, 0, 0), (0, 1, 0))
    assert not is_binary_linear_subspace(support)
    with pytest.raises(ValueError, match="linear subspace"):
        audit_linear_code_pressure("NONLINEAR", support, support)


def test_affine_translate_without_zero_is_outside_the_proof_mechanism():
    affine_line = ((1, 0), (1, 1))
    assert not is_binary_linear_subspace(affine_line)
    with pytest.raises(ValueError, match="linear subspace"):
        audit_linear_code_pressure("AFFINE-TRANSLATE", affine_line, affine_line)


def test_every_binary_subspace_through_dimension_four_is_certified():
    assert [len(binary_linear_subspaces(width)) for width in range(1, 5)] == [
        2,
        5,
        16,
        67,
    ]
    for width in range(1, 5):
        for code in binary_linear_subspaces(width):
            assert is_binary_linear_subspace(code)
            assert len(code) == 2 ** code_dimension(code)


def test_parity_support_full_presentations_obey_the_exact_finite_bound():
    parity2 = _parity_code(2)
    parity3 = _parity_code(3)
    relations2 = marked_support_presentation("EAAFEF", parity2, parity2)
    relations3 = marked_support_presentation("EAAAFEF", parity3, parity3)
    assert presentation_solution_count(3, range(1, 7), relations2) == 108
    assert presentation_solution_count(3, range(1, 8), relations3) == 72


def test_linear_code_pressure_is_uniform_in_degree_and_dimension():
    for width in range(2, 9):
        parity = _parity_code(width)
        full = tuple(itertools.product((0, 1), repeat=width))
        equal = audit_linear_code_pressure("PARITY", parity, parity)
        unequal = audit_linear_code_pressure("UNEQUAL", full, ((0,) * width,))
        assert equal.crossing_pressure_upper_bound == pytest.approx(-1)
        assert unequal.crossing_pressure_upper_bound == pytest.approx(
            -1 - width / 2
        )
        assert equal.exact_finite_group_upper_bound_verified
        assert unequal.exact_finite_group_upper_bound_verified


def test_report_proves_only_the_linear_code_family():
    report = run_linear_code_support_pressure()
    metrics = report.headline_metrics
    assert metrics["checked_linear_code_pair_count"] == 4774
    assert metrics["linear_code_pair_certificate_failure_count"] == 0
    assert metrics["finite_S3_control_failure_count"] == 0
    assert metrics["growing_degree_linear_code_pressure_theorem_count"] == 1
    assert report.claim_gate["linear_code_growing_degree_crossing_pressure_proved"]
    assert not report.claim_gate["affine_coset_pressure_proved"]
    assert not report.claim_gate["arbitrary_support_pressure_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
