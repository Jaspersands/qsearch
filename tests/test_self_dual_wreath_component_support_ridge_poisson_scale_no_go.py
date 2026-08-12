from fractions import Fraction

import pytest

from self_dual_wreath_component_support_ridge_poisson_scale_no_go import (
    _projection_controls,
    audit_poisson_scale_mixture,
    geometric_length_mass,
    geometric_length_tail,
    run_component_support_ridge_poisson_scale_no_go,
    squared_constant_mass_length_lower_bound,
    squared_length_mass,
    squared_length_tail,
    support_ridge_poisson_scale_no_go_theorem,
    support_ridge_poisson_scale_record,
    support_ridge_tail_lower_bound,
)


def test_geometric_and_squared_length_laws_normalize_exactly() -> None:
    delta = Fraction(1, 3)
    truncation = 25
    geometric_mass = sum(
        geometric_length_mass(delta, length)
        for length in range(truncation + 1)
    )
    squared_mass = sum(
        squared_length_mass(delta, length)
        for length in range(truncation + 1)
    )
    assert geometric_mass + geometric_length_tail(delta, truncation) == 1
    assert squared_mass + squared_length_tail(delta, truncation) == 1


def test_positive_complement_word_mixtures_equal_both_resolvents() -> None:
    row = audit_poisson_scale_mixture(
        "MIXTURE",
        _projection_controls(301, 7, 4),
        Fraction(1, 3),
        18,
    )
    assert row.exact_positive_mixture_verified
    assert row.geometric_residual_bounded_by_tail
    assert row.squared_residual_bounded_by_tail
    assert row.geometric_resolvent_residual <= row.geometric_tail + 1e-10
    assert row.squared_resolvent_residual <= row.negative_binomial_tail + 1e-10


def test_constant_squared_mixture_mass_requires_inverse_delta_length() -> None:
    for denominator in (8, 16, 32, 64):
        delta = Fraction(1, denominator)
        length = squared_constant_mass_length_lower_bound(delta)
        assert length >= denominator // 2
        if length:
            previous_upper = delta**2 * length * (length + 1) / 2
            assert previous_upper < Fraction(1, 2)


def test_coarse_physical_ridge_has_constant_tail_lower_bound() -> None:
    bound = support_ridge_tail_lower_bound(
        support_rank_density=0.25,
        frame_trace_density=4.0,
        physical_ridge_parameter=10**8,
    )
    assert bound == pytest.approx(0.25 - 8e-8)


def test_final_root_scaling_exposes_factorial_length_and_coarse_tail() -> None:
    row = support_ridge_poisson_scale_record(64)
    assert 2 <= row.child_leaf_aspect < 4
    assert row.log2_geometric_mean_length_at_physical_eta > 250
    assert row.constant_mass_squared_length_log2_lower_bound > 250
    assert row.coarse_normalized_tail_lower_bound > 0.249
    assert not row.positive_poisson_words_polynomial_at_physical_scale
    assert not row.coarse_normalized_ridge_transfers_support


def test_report_falsifies_only_positive_uniform_leaf_poisson_route() -> None:
    report = run_component_support_ridge_poisson_scale_no_go()
    assert report.headline_metrics[
        "poisson_parameter_scale_no_go_theorem_count"
    ] == 1
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["positive_poisson_leaf_words_valid_at_physical_scale"]
    assert not report.claim_gate[
        "positive_poisson_leaf_words_polynomial_length_at_physical_scale"
    ]
    assert not report.claim_gate[
        "polynomial_normalized_parameter_approximates_support"
    ]
    assert not report.claim_gate["signed_polynomial_or_rational_route_ruled_out"]
    assert not report.claim_gate["aggregate_frame_route_ruled_out"]
    assert not report.claim_gate["natural_support_ridge_tail_small"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_theorem_scope_preserves_signed_and_aggregate_routes() -> None:
    theorem = support_ridge_poisson_scale_no_go_theorem()
    assert theorem.theorem_verified
    assert theorem.positive_uniform_leaf_poisson_route_only
    assert not theorem.signed_or_aggregate_approximations_ruled_out
    assert "eta/q" in theorem.parameter_rescaling
