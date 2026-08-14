import math

import pytest

from coset_hyperoctahedral_cg_kronecker_reduction import (
    audit_inflated_kronecker_reduction,
    build_hyperoctahedral_cg_kronecker_report,
    hyperoctahedral_cg_scaling_record,
    inflated_wreath_tensor_coefficient,
    kronecker_coefficient,
    write_hyperoctahedral_cg_kronecker_report,
)


@pytest.mark.parametrize("half_degree", (2, 3, 4, 5, 6))
def test_inflated_wreath_tensor_coefficients_equal_kronecker(half_degree):
    control = audit_inflated_kronecker_reduction(half_degree)
    assert control.exact_inflation_reduction_verified
    assert control.coefficient_mismatch_count == 0
    assert control.sum_inflated_irrep_dimension_squares == math.factorial(
        half_degree
    )
    assert control.trivial_color_regular_plancherel_mass == pytest.approx(
        2.0 ** (-half_degree)
    )
    assert control.even_parity_conditioned_trivial_color_mass == pytest.approx(
        2.0 ** (1 - half_degree)
    )


def test_known_small_kronecker_coefficient_is_preserved():
    left = (2, 1)
    right = (2, 1)
    assert kronecker_coefficient(left, right, (3,)) == 1
    assert kronecker_coefficient(left, right, (2, 1)) == 1
    assert kronecker_coefficient(left, right, (1, 1, 1)) == 1
    assert inflated_wreath_tensor_coefficient(left, right, (2, 1)) == 1

    with pytest.raises(ValueError, match="common size"):
        kronecker_coefficient((2,), (1,), (2,))
    with pytest.raises(ValueError, match="common size"):
        inflated_wreath_tensor_coefficient((2,), (1,), (2,))


def test_regular_hard_sector_mass_is_small_so_natural_mass_remains_open():
    rows = [
        hyperoctahedral_cg_scaling_record(m)
        for m in (4, 8, 16, 32, 64, 128)
    ]
    assert all(row.generic_wreath_cg_contains_symmetric_kronecker for row in rows)
    assert all(not row.efficient_wreath_qft_implies_efficient_wreath_cg for row in rows)
    assert all(not row.natural_source_trivial_color_mass_lower_bound_proved for row in rows)
    assert all(not row.source_specific_matrix_hecke_bypass_ruled_out for row in rows)
    assert rows[-1].even_parity_conditioned_trivial_color_mass < 1e-30

    with pytest.raises(ValueError, match="positive"):
        hyperoctahedral_cg_scaling_record(0)
    with pytest.raises(ValueError, match="positive"):
        audit_inflated_kronecker_reduction(0)


def test_report_scopes_generic_reduction_away_from_natural_lower_bound(tmp_path):
    report = build_hyperoctahedral_cg_kronecker_report(
        finite_half_degrees=(2, 3, 4),
        scaling_half_degrees=(4, 8, 16, 32),
    )
    assert report.theorem.theorem_verified
    assert report.theorem.inflated_tensor_identity_proved
    assert report.theorem.generic_wreath_cg_contains_internal_symmetric_kronecker
    assert not report.theorem.efficient_qft_sufficient_for_cg
    assert not report.theorem.natural_source_hard_sector_mass_proved
    assert not report.theorem.source_specific_fusion_compiler_ruled_out
    assert not report.theorem.quantum_complexity_lower_bound_proved
    assert report.claim_gate[
        "generic_hyperoctahedral_cg_contains_symmetric_kronecker"
    ]
    assert not report.claim_gate["natural_source_kronecker_hard_mass_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_hyperoctahedral_cg_kronecker_report(
        tmp_path / "wreath-cg.json",
        finite_half_degrees=(2, 3),
        scaling_half_degrees=(4, 8),
    )
    assert payload["status"] == (
        "generic-wreath-cg-contains-kronecker-natural-mass-open"
    )
    assert payload["headline_metrics"][
        "natural_source_hard_sector_mass_theorem_count"
    ] == 0
