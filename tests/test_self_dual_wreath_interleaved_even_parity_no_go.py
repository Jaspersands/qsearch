from functools import lru_cache

import math

import pytest

from self_dual_wreath_interleaved_even_parity_no_go import (
    audit_even_parity_presentation,
    audit_symmetric_involution_bound,
    elementary_involution_upper_bound,
    even_parity_all_depth_certificate,
    even_parity_support,
    interleaved_even_parity_pattern,
    involution_count_symmetric_group,
    run_interleaved_even_parity_no_go,
)


@lru_cache(maxsize=1)
def _report():
    return run_interleaved_even_parity_no_go()


@pytest.mark.parametrize("width", range(3, 11))
def test_weight_two_rows_force_the_fixed_commuting_involution_group(width):
    control = audit_even_parity_presentation(width)
    assert control.pattern == "EFE" + "A" * (width - 2) + "BFB"
    assert control.different_support_size == 1 << (width - 1)
    assert control.same_support_size == (1 << (width - 1)) - 1
    assert control.minimum_same_weight == 2
    assert control.every_weight_two_row_present
    assert len(control.selected_frame_pair_relations) == math.comb(width, 2)
    assert control.frame_relations_force_common_involution
    assert control.abstract_relations == ("z^2", "[e,f]", "[f,z]")
    assert control.target_identity_verified
    assert control.exact_control_verified


@pytest.mark.parametrize("width", range(3, 11))
def test_involution_bound_restores_uniform_half_exponent_margin(width):
    control = audit_even_parity_presentation(width)
    expected_generic = -0.5 * math.log2(
        1.0 - 2.0 ** (-(width - 1))
    )
    expected_improved = 0.5 + expected_generic
    assert control.generic_scalar_pressure_margin == pytest.approx(expected_generic)
    assert control.involution_improved_scalar_pressure_margin == pytest.approx(
        expected_improved
    )
    assert control.involution_improved_scalar_pressure_margin > 0.5


def test_even_parity_support_and_pattern_are_exact_infinite_families():
    for width in range(2, 9):
        support = even_parity_support(width)
        assert len(support) == 1 << (width - 1)
        assert all(sum(row) % 2 == 0 for row in support)
        pattern = interleaved_even_parity_pattern(width)
        assert len(pattern) == width + 4
        assert pattern.count("E") == pattern.count("F") == 2
        assert pattern.count("B") == 2


@pytest.mark.parametrize(
    ("degree", "expected"),
    ((2, 2), (3, 4), (4, 10), (5, 26), (6, 76)),
)
def test_symmetric_group_involution_formula(degree, expected):
    assert involution_count_symmetric_group(degree) == expected
    assert expected <= elementary_involution_upper_bound(degree)


@pytest.mark.parametrize("degree", range(2, 7))
def test_exact_finite_H_counts_obey_class_involution_bound(degree):
    control = audit_symmetric_involution_bound(degree)
    assert control.involution_count == involution_count_symmetric_group(degree)
    assert control.exact_H_homomorphism_count <= control.class_involution_upper_bound
    assert control.homomorphism_bound_verified
    assert control.finite_log_group_exponent > 1.0


def test_all_depth_certificate_uses_all_n_count_not_finite_extrapolation():
    theorem = even_parity_all_depth_certificate()
    assert theorem.arbitrary_frame_width
    assert theorem.exact_target_identity
    assert theorem.universal_family_no_go_verified
    assert theorem.solution_exponent_upper_bound == "3/2+o(1)"
    assert theorem.uniform_pressure_margin_lower_bound == 0.5
    assert "I(S_n)" in theorem.involution_asymptotic_bound


def test_report_falsifies_linear_family_without_claiming_nonlinear_closure():
    report = _report()
    assert report.headline_metrics[
        "all_depth_even_parity_involution_no_go_theorem_count"
    ] == 1
    assert report.headline_metrics["presentation_control_failure_count"] == 0
    assert report.headline_metrics["finite_involution_bound_failure_count"] == 0
    assert report.headline_metrics["improved_solution_exponent_upper_bound"] == 1.5
    assert report.claim_gate["even_parity_group_presentation_classified"]
    assert report.claim_gate["even_parity_target_identity_proved"]
    assert report.claim_gate["uniform_involution_loss_proved"]
    assert not report.claim_gate["even_parity_near_threshold_escape_survives"]
    assert not report.claim_gate["all_nonlinear_near_threshold_supports_controlled"]
    assert not report.claim_gate["speedup_claim_allowed"]
