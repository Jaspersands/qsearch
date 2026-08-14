import math

import pytest

from coset_hidden_involution_fourier_coefficient_normalization_no_go import (
    audit_fourier_coefficient_normalization,
    build_fourier_coefficient_normalization_report,
    fourier_coefficient_scaling_record,
    write_fourier_coefficient_normalization_report,
)


@pytest.mark.parametrize("copy_count", (1, 2, 3))
def test_regular_fourier_coefficient_formula_holds_in_every_s3_sector(copy_count):
    control = audit_fourier_coefficient_normalization(copy_count)
    assert control.exact_all_sector_formula_verified
    assert control.sector_source_dimension_sum == control.regular_source_dimension
    assert control.maximum_fourier_block_formula_residual < 1e-8
    assert control.maximum_singular_value_scaling_residual < 1e-8
    assert {row.irrep_name for row in control.sectors} == {
        "trivial",
        "sign",
        "standard",
    }
    assert all(row.exact_fourier_coefficient_formula_verified for row in control.sectors)


def test_fourier_scalar_matches_schur_orthogonality():
    control = audit_fourier_coefficient_normalization(2)
    for row in control.sectors:
        assert row.fourier_scalar_amplification == pytest.approx(
            math.sqrt(control.group_order / row.carrier_dimension)
        )
        assert row.generic_raw_coefficient_polar_degree_lower_scale == pytest.approx(
            row.fourier_scalar_amplification
        )
        assert row.scaled_row_maximum_singular_value == pytest.approx(
            row.raw_coefficient_maximum_singular_value
            * row.fourier_scalar_amplification
        )


def test_every_sector_has_universal_quarter_root_generic_cost():
    control = audit_fourier_coefficient_normalization(2)
    universal = control.group_order ** 0.25
    assert all(
        row.generic_raw_coefficient_polar_degree_lower_scale >= universal - 1e-10
        for row in control.sectors
    )


def test_scaling_matches_branch_erasure_factorial_order():
    rows = [fourier_coefficient_scaling_record(m) for m in (3, 4, 8, 16, 32, 64)]
    assert all(row.same_factorial_leading_exponent for row in rows)
    assert all(not row.sector_normalized_direct_access_compiled for row in rows)
    assert all(row.lower_bound_to_branch_erasure_log2_ratio > 0 for row in rows)
    assert rows[-1].raw_coefficient_qsvt_degree_lower_log2 > 100
    with pytest.raises(ValueError, match="at least three"):
        fourier_coefficient_scaling_record(2)


def test_report_closes_raw_coefficient_qsvt_only(tmp_path):
    report = build_fourier_coefficient_normalization_report(
        finite_copy_counts=(1, 2),
        scaling_half_degrees=(3, 4, 8, 16),
    )
    assert report.theorem.theorem_verified
    assert report.theorem.regular_fourier_block_formula_proved
    assert report.theorem.every_sector_quarter_root_obstruction_proved
    assert not report.theorem.sector_normalized_direct_access_compiled
    assert not report.theorem.structured_row_polar_compiled
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_fourier_coefficient_normalization_report(
        tmp_path / "fourier-coefficient.json",
        finite_copy_counts=(1,),
        scaling_half_degrees=(3, 4, 8),
    )
    assert payload["status"] == (
        "raw-fourier-normalization-closed-direct-sector-polar-open"
    )
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0
