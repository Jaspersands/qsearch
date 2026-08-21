import pytest

from coset_hidden_involution_occupied_matrix_rank import (
    audit_occupied_rank_kernel,
    build_occupied_matrix_rank_report,
    occupied_rank_scaling_record,
)


@pytest.mark.parametrize("copy_count", (1, 2))
def test_finite_source_kernel_is_bounded_by_centered_moment(copy_count: int) -> None:
    row = audit_occupied_rank_kernel(3, 1, copy_count)
    assert row.kernel_dimension >= 0
    assert row.exact_kernel_fraction <= row.theorem_kernel_fraction_upper_bound + 1e-12
    assert row.kernel_fraction_bound_verified


def test_natural_blocks_have_constant_mass_and_huge_occupied_rank() -> None:
    rows = [occupied_rank_scaling_record(value) for value in (4, 6, 8, 12, 16, 32)]
    assert all(row.constant_alternative_mass_in_huge_occupied_rank_blocks for row in rows)
    assert all(row.huge_occupied_rank_alternative_mass_lower_bound >= 0.85 for row in rows)
    assert all(row.source_kernel_fraction_upper_bound <= 1 / 64 for row in rows)
    assert all(
        row.occupied_rank_threshold_log2 == pytest.approx(
            row.multiplicity_threshold_log2 - 1
        )
        for row in rows
    )


def test_report_resolves_rank_but_not_basis_or_transform() -> None:
    report = build_occupied_matrix_rank_report()
    assert report.headline_metrics["finite_kernel_control_failure_count"] == 0
    assert report.headline_metrics["minimum_huge_occupied_rank_alternative_mass_lower_bound"] >= 0.85
    assert report.claim_gate["global_source_kernel_fraction_small"] is True
    assert report.claim_gate["half_rank_deficient_blocks_negligible"] is True
    assert report.claim_gate["constant_alternative_mass_in_huge_occupied_rank_blocks"] is True
    assert report.claim_gate["occupied_cosine_sine_rank_lower_bound_proved"] is True
    assert report.claim_gate["succinct_occupied_block_basis_constructed"] is False
    assert report.claim_gate["matrix_cosine_sine_transform_compiled"] is False
    assert report.claim_gate["binary_hidden_involution_detector_constructed"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False
