import pytest

from self_dual_wreath_adaptive_syndrome_trim_transfer import (
    audit_adaptive_syndrome_trim_transfer,
    entropy_continuity_bound_bits,
    run_adaptive_syndrome_trim_transfer,
)


def test_denominator_free_l1_identity_and_cauchy_bound_through_S5():
    rows = [
        audit_adaptive_syndrome_trim_transfer(n, threshold)
        for n, threshold in ((2, 0), (3, 1), (4, 1), (4, 2), (5, 1), (5, 4))
    ]
    assert all(row.exact_denominator_free_trim_transfer_verified for row in rows)
    assert all(
        row.exact_retained_expected_conditional_tv
        == pytest.approx(row.denominator_free_retained_l1_expression, abs=2e-8)
        for row in rows
    )
    assert all(
        row.exact_retained_expected_conditional_tv
        <= row.retained_tv_cauchy_upper_bound + 2e-8
        for row in rows
    )


def test_adaptive_energy_is_full_minus_base_for_second_moment_and_chi_square():
    rows = [
        audit_adaptive_syndrome_trim_transfer(n, threshold)
        for n, threshold in ((2, 0), (3, 0), (3, 1), (4, 1), (5, 1), (5, 4))
    ]
    for row in rows:
        assert row.second_moment_excess == pytest.approx(
            row.retained_parity_coset_energy,
            abs=2e-8,
        )
        assert row.chi_square_excess == pytest.approx(
            row.retained_parity_coset_energy,
            abs=2e-8,
        )
        assert row.maximum_transfer_identity_residual < 2e-8


def test_dimension_tail_and_entropy_continuity_control_total_information():
    for n, threshold in ((3, 1), (4, 1), (4, 2), (5, 1), (5, 4)):
        row = audit_adaptive_syndrome_trim_transfer(n, threshold)
        assert row.removed_physical_mass <= row.removed_physical_mass_union_bound + 2e-8
        assert row.exact_expected_conditional_tv <= (
            row.removed_physical_mass + row.retained_tv_cauchy_upper_bound + 2e-8
        )
        assert row.exact_expected_conditional_kl_bits <= (
            entropy_continuity_bound_bits(row.exact_expected_conditional_tv) + 2e-8
        )


def test_nontrivial_trim_strictly_reduces_finite_adaptive_energy():
    full = audit_adaptive_syndrome_trim_transfer(5, 0)
    trimmed = audit_adaptive_syndrome_trim_transfer(5, 1)
    assert 0 < trimmed.retained_parity_coset_energy < full.retained_parity_coset_energy
    assert 0 < trimmed.exact_retained_expected_conditional_tv


def test_report_keeps_all_asymptotic_and_algorithmic_gates_false():
    report = run_adaptive_syndrome_trim_transfer()
    assert report.headline_metrics["denominator_free_trim_transfer_theorem_count"] == 1
    assert report.claim_gate["adaptive_denominator_eliminated_proved"]
    assert report.claim_gate["adaptive_energy_is_projected_excess_proved"]
    assert not report.claim_gate["canonical_face_twist_energy_vanishes_proved"]
    assert not report.claim_gate["canonical_opposite_twist_energy_vanishes_proved"]
    assert not report.claim_gate["canonical_adaptive_syndrome_decouples_proved"]
    assert not report.claim_gate["canonical_adaptive_syndrome_survives_proved"]
    assert not report.claim_gate["classical_separation_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
