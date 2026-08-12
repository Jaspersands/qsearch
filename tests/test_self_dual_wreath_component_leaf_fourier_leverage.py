import numpy as np
import pytest

from self_dual_wreath_component_leaf_fourier_leverage import (
    STRONG_POINTWISE_DIAGONAL_BUDGET,
    _coarse_pvm,
    _uniform_povm,
    audit_leaf_fourier_profile,
    fourier_degree_scaling_record,
    leaf_fourier_leverage_theorem,
    run_component_leaf_fourier_leverage,
    sparse_fourier_certificate,
    walsh_fourier_coefficients,
)


def test_uniform_povm_has_one_walsh_mode_and_exact_cap() -> None:
    row = audit_leaf_fourier_profile(
        "UNIFORM",
        "uniform",
        _uniform_povm(5, 3),
    )
    assert row.all_certificates_verified
    assert row.numerical_fourier_support_size == 1
    assert row.numerical_fourier_degree == 0
    assert row.exact_support_certificate.effect_operator_cap == pytest.approx(1 / 32)
    assert row.actual_normalized_diagonal_fourth_moment == pytest.approx(1 / 32**3)
    assert row.finite_control_closes_diagonal_budget


def test_sparse_coarse_pvm_saturates_support_certificate() -> None:
    row = audit_leaf_fourier_profile(
        "COARSE",
        "coarse-pvm",
        _coarse_pvm(7, 2),
    )
    assert row.all_certificates_verified
    assert row.numerical_fourier_support_size == 4
    assert row.numerical_fourier_degree == 2
    assert row.exact_support_certificate.effect_operator_cap == pytest.approx(1 / 32)
    assert row.actual_maximum_effect_eigenvalue == pytest.approx(1 / 32)
    assert row.actual_normalized_diagonal_fourth_moment == pytest.approx(1 / 32**3)
    assert row.finite_control_closes_diagonal_budget


def test_full_pvm_is_sharp_full_support_obstruction() -> None:
    row = audit_leaf_fourier_profile(
        "FULL-PVM",
        "full-pvm",
        _coarse_pvm(3, 3),
    )
    assert row.all_certificates_verified
    assert row.numerical_fourier_support_size == 8
    assert row.numerical_fourier_degree == 3
    assert row.actual_maximum_effect_eigenvalue == pytest.approx(1.0)
    assert row.actual_normalized_diagonal_fourth_moment == pytest.approx(1.0)
    assert row.exact_support_certificate.normalized_diagonal_fourth_moment_bound == pytest.approx(1.0)
    assert not row.finite_control_closes_diagonal_budget


def test_uniform_sparse_truncation_certificate_handles_nonzero_tail() -> None:
    coarse = []
    for point in range(8):
        effect = np.zeros((8, 8), dtype=complex)
        block = slice(0, 4) if point & 1 == 0 else slice(4, 8)
        effect[block, block] = np.eye(4) / 4
        coarse.append(effect)
    coarse = tuple(coarse)
    full = _coarse_pvm(3, 3)
    epsilon = 0.05
    effects = tuple(
        (1.0 - epsilon) * left + epsilon * right
        for left, right in zip(coarse, full, strict=True)
    )
    coefficients = walsh_fourier_coefficients(effects)
    active = tuple(
        mask for mask, coefficient in enumerate(coefficients)
        if mask in (0, 1)
    )
    certificate = sparse_fourier_certificate(
        effects,
        active,
        certificate_id="APPROXIMATE-TWO-MODE",
    )
    actual = max(np.linalg.eigvalsh(effect)[-1] for effect in effects)
    assert certificate.omitted_uniform_operator_residual > 0
    assert certificate.theorem_bound_verified
    assert actual <= certificate.effect_operator_cap + 1e-10


def test_degree_scaling_closes_below_half_but_not_automatically_at_small_m() -> None:
    small = fourier_degree_scaling_record(8)
    large = fourier_degree_scaling_record(32)
    assert not (
        small.quarter_degree_diagonal_bound
        <= STRONG_POINTWISE_DIAGONAL_BUDGET
    )
    assert (
        large.quarter_degree_diagonal_bound
        <= STRONG_POINTWISE_DIAGONAL_BUDGET
    )
    assert large.maximum_degree_closing_uniform_cap > (
        large.maximum_degree_closing_budget
    )
    assert large.maximum_degree_closing_budget < 16
    assert large.fixed_gap_below_half_degree_is_asymptotically_sufficient


def test_invalid_povm_and_missing_constant_mode_are_rejected() -> None:
    with pytest.raises(ValueError, match="power of two"):
        walsh_fourier_coefficients((np.eye(2),) * 3)
    with pytest.raises(ValueError, match="constant mode"):
        sparse_fourier_certificate(
            _uniform_povm(2, 2),
            (1,),
            certificate_id="NO-CONSTANT",
        )


def test_report_preserves_natural_diagonal_and_speedup_gates() -> None:
    report = run_component_leaf_fourier_leverage()
    assert report.headline_metrics["leaf_fourier_leverage_theorem_count"] == 1
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics[
        "natural_finite_controls_closing_diagonal_budget"
    ] == 0
    assert report.claim_gate[
        "positive_povm_sparse_fourier_leverage_theorem_proved"
    ]
    assert not report.claim_gate["natural_leaf_fourier_sparsity_proved"]
    assert not report.claim_gate["natural_diagonal_leakage_controlled"]
    assert not report.claim_gate["natural_component_M4_positive"]
    assert not report.claim_gate["speedup_claim_allowed"]
    assert report.natural_finite_controls[0].numerical_fourier_support_size == 4
    assert report.natural_finite_controls[1].numerical_fourier_support_size == 4


def test_theorem_rejects_naive_matrix_hypercontractive_shortcut() -> None:
    theorem = leaf_fourier_leverage_theorem()
    assert theorem.theorem_verified
    assert theorem.arbitrary_positive_povm
    assert theorem.exact_or_uniform_approximation_required
    assert "rejected" in theorem.matrix_hypercontractive_shortcut
