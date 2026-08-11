from fractions import Fraction
from functools import lru_cache

import numpy as np
import pytest

from self_dual_wreath_poisson_ridge_word_mixture import (
    audit_fixed_length_complement_words,
    audit_ridge_mixture,
    minimum_truncation_length,
    negative_binomial_length_mass,
    negative_binomial_log_tail,
    negative_binomial_tail,
    normalized_frame,
    poisson_ridge_word_mixture_theorem,
    ridge_pressure_scaling_record,
    run_poisson_ridge_word_mixture,
)


@lru_cache(maxsize=1)
def _report():
    return run_poisson_ridge_word_mixture()


@pytest.fixture(scope="module")
def projections():
    first = np.diag([1.0, 1.0, 0.0, 0.0])
    second = np.diag([0.0, 1.0, 1.0, 0.0])
    vector = np.asarray([1.0, 0.0, 0.0, 1.0]) / np.sqrt(2.0)
    third = np.outer(vector, vector)
    return first, second, third


@pytest.mark.parametrize("length", range(6))
def test_fixed_length_iid_complement_words_factorize(projections, length):
    control = audit_fixed_length_complement_words(
        f"length-{length}",
        projections,
        length,
    )
    assert control.average_word_residual <= 1e-12
    assert control.exact_fixed_length_factorization_verified


@pytest.mark.parametrize("eta", (Fraction(1, 2), Fraction(1, 5), Fraction(1, 10)))
def test_negative_binomial_length_law_normalizes_and_has_exact_tail(eta):
    cutoff = 2000
    mass = sum(
        (negative_binomial_length_mass(eta, length) for length in range(cutoff + 1)),
        start=Fraction(0),
    )
    assert 1 - mass == negative_binomial_tail(eta, cutoff)
    assert negative_binomial_tail(eta, cutoff) < Fraction(1, 10**20)


@pytest.mark.parametrize(
    ("eta", "length"),
    ((Fraction(1, 2), 20), (Fraction(1, 5), 50), (Fraction(1, 10), 100)),
)
def test_truncated_word_mixture_converges_to_normalized_ridge(
    projections,
    eta,
    length,
):
    control = audit_ridge_mixture(
        "ridge",
        projections,
        eta,
        length,
    )
    assert control.tail_formula_residual <= 1e-14
    assert control.truncated_mixture_operator_residual <= (
        control.exact_negative_binomial_tail + 1e-12
    )
    assert control.residual_bounded_by_tail
    assert control.negative_binomial_mean == pytest.approx(2 / float(eta))
    assert control.exact_mixture_verified


def test_minimum_truncation_is_polynomial_for_inverse_polynomial_eta():
    for n in (10, 20, 40):
        eta = Fraction(1, n**2)
        target = Fraction(1, n**8)
        length = minimum_truncation_length(eta, target)
        assert negative_binomial_tail(eta, length) <= target
        if length:
            assert negative_binomial_tail(eta, length - 1) > target
        assert length < 40 * n**2 * max(1, int(np.log(n)))


def test_log_tail_tracks_exact_tail_and_certifies_large_scaling():
    eta = Fraction(1, 10)
    for length in (0, 1, 10, 100):
        exact = float(negative_binomial_tail(eta, length))
        assert negative_binomial_log_tail(eta, length) == pytest.approx(
            np.log(exact), abs=1e-12
        )

    large_eta = Fraction(1, 1024**2)
    target = Fraction(1, 1024**10)
    length = minimum_truncation_length(large_eta, target)
    assert negative_binomial_log_tail(large_eta, length) <= np.log(float(target))
    assert negative_binomial_log_tail(large_eta, length - 1) > np.log(
        float(target)
    )


def test_normalized_frame_has_spectrum_in_unit_interval(projections):
    frame = normalized_frame(projections)
    eigenvalues = np.linalg.eigvalsh(frame)
    assert eigenvalues[0] >= -1e-12
    assert eigenvalues[-1] <= 1 + 1e-12


def test_fixed_ridge_prefactor_cannot_erase_factorial_crossing_loss():
    moderate = ridge_pressure_scaling_record(
        50,
        ridge_inverse_polynomial_degree=2,
        fixed_ridge_factor_count=4,
    )
    large = ridge_pressure_scaling_record(
        512,
        ridge_inverse_polynomial_degree=2,
        fixed_ridge_factor_count=4,
    )
    assert moderate.factorial_crossing_loss_survives
    assert large.factorial_crossing_loss_survives
    assert large.log2_crossing_bound_after_ridge_prefactor < (
        moderate.log2_crossing_bound_after_ridge_prefactor
    )
    assert large.polynomial_word_length


def test_theorem_closes_word_coefficients_not_common_metric():
    theorem = poisson_ridge_word_mixture_theorem()
    assert theorem.arbitrary_leaf_count
    assert theorem.arbitrary_word_length
    assert theorem.inverse_polynomial_ridge_has_polynomial_truncation
    assert theorem.green_word_coefficient_burden_resolved
    assert theorem.theorem_verified
    assert not theorem.common_metric_normalization_resolved
    assert not theorem.positive_component_M4_proved


def test_report_moves_M4_boundary_to_common_metric_and_noncrossing_mass():
    report = _report()
    assert report.headline_metrics[
        "poisson_ridge_word_mixture_theorem_count"
    ] == 1
    assert report.headline_metrics["fixed_length_control_failure_count"] == 0
    assert report.headline_metrics["ridge_mixture_control_failure_count"] == 0
    assert report.headline_metrics[
        "green_word_coefficient_burden_remaining_count"
    ] == 0
    assert report.claim_gate["green_word_coefficient_burden_controlled"]
    assert report.claim_gate[
        "all_width_crossing_pressure_survives_ridge_mixture"
    ]
    assert not report.claim_gate["common_metric_normalization_controlled"]
    assert not report.claim_gate["ridge_to_green_average_error_controlled"]
    assert not report.claim_gate["noncrossing_ridge_moment_lower_bounded"]
    assert not report.claim_gate["natural_component_M4_positive"]
    assert not report.claim_gate["speedup_claim_allowed"]
