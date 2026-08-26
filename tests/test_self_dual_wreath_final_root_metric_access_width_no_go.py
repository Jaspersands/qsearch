from __future__ import annotations

import math

import numpy as np
import pytest

from self_dual_wreath_final_root_metric_access_width_no_go import (
    PARENT_WINDOW_LOWER,
    PARENT_WINDOW_UPPER,
    _rotated_effect_pair,
    audit_metric_access_width,
    bernstein_sign_degree_lower_bound,
    natural_metric_access_width_scaling_record,
    run_final_root_metric_access_width_no_go,
    write_final_root_metric_access_width_no_go_report,
)


def test_bernstein_sign_degree_lower_bound_scales_inverse_signal() -> None:
    coarse = bernstein_sign_degree_lower_bound(1 / 8, 0.1)
    fine = bernstein_sign_degree_lower_bound(1 / 32, 0.1)

    assert fine > 3.9 * coarse
    assert fine > 28
    with pytest.raises(ValueError):
        bernstein_sign_degree_lower_bound(0)
    with pytest.raises(ValueError):
        bernstein_sign_degree_lower_bound(0.5, 1.0)


@pytest.mark.parametrize(
    "control_id,left,right,q",
    [
        (
            "flat",
            0.5 * np.eye(2),
            0.5 * np.eye(2),
            32,
        ),
        (
            "diagonal",
            np.diag([0.25, 0.75]),
            np.diag([0.75, 0.25]),
            64,
        ),
        (
            "rotated",
            *_rotated_effect_pair(),
            64,
        ),
    ],
)
def test_exact_metric_signal_and_endpoint_polar_factorization(
    control_id: str,
    left: np.ndarray,
    right: np.ndarray,
    q: int,
) -> None:
    row = audit_metric_access_width(control_id, left, right, q)

    assert row.exact_metric_access_factorization_verified
    assert row.square_root_width_charge_verified
    assert row.signal_gram_residual < 1e-10
    assert row.endpoint_polar_residual < 1e-10
    assert row.endpoint_effect_residual < 1e-10
    assert row.native_success_identity_residual < 1e-12
    assert row.signal_maximum_singular_value == pytest.approx(
        math.sqrt(row.parent_maximum_eigenvalue / row.parent_orientation_width)
    )


def test_noncommuting_metrics_preserve_exact_access_factorization() -> None:
    left = np.array([[2.0, 0.4], [0.4, 1.0]], dtype=complex)
    right = np.array([[1.0, -0.2j], [0.2j, 2.5]], dtype=complex)
    row = audit_metric_access_width("noncommuting", left, right, 64)

    assert row.exact_metric_access_factorization_verified
    assert row.square_root_width_charge_verified
    assert row.bernstein_qsvt_degree_lower_bound > 4


@pytest.mark.parametrize("n", [16, 24, 32, 40, 48])
def test_natural_scaling_has_factorial_width_and_superpolynomial_cost(n: int) -> None:
    row = natural_metric_access_width_scaling_record(n)

    q = int(row.child_orientation_width_decimal)
    w = int(row.parent_orientation_width_decimal)
    assert w == 2 * q
    assert 2 <= row.child_aspect < 4
    assert row.retained_signal_minimum_singular_value == pytest.approx(
        math.sqrt(PARENT_WINDOW_LOWER / w)
    )
    assert row.retained_signal_maximum_singular_value == pytest.approx(
        math.sqrt(PARENT_WINDOW_UPPER / w)
    )
    assert row.raw_metric_access_superpolynomial
    assert row.matrix_endpoint_bulk_well_conditioned
    assert not row.representation_specific_metric_oracle_ruled_out


def test_invalid_metric_controls_are_rejected() -> None:
    with pytest.raises(ValueError):
        audit_metric_access_width("bad-width", np.eye(2), np.eye(2), 1)
    with pytest.raises(ValueError):
        audit_metric_access_width(
            "singular-child",
            np.diag([1.0, 0.0]),
            np.eye(2),
            16,
        )
    with pytest.raises(ValueError):
        natural_metric_access_width_scaling_record(2)


def test_report_falsifies_canonical_raw_access_but_not_direct_metric_oracle() -> None:
    report = run_final_root_metric_access_width_no_go()

    assert report.theorem.theorem_verified
    assert report.headline_metrics["exact_control_failure_count"] == 0
    assert report.claim_gate[
        "child_polar_recovers_metric_sqrt_at_raw_normalization"
    ]
    assert report.claim_gate[
        "exact_final_root_endpoint_is_polar_of_binary_metric_signal"
    ]
    assert report.claim_gate["generic_qsvt_polar_requires_sqrt_width_degree"]
    assert report.claim_gate[
        "native_raw_metric_selection_probability_is_inverse_width"
    ]
    assert not report.claim_gate["canonical_raw_child_metric_access_is_polynomial"]
    assert not report.claim_gate[
        "representation_specific_metric_magnitude_oracle_proved"
    ]
    assert not report.claim_gate["arbitrary_hierarchical_global_polar_ruled_out"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_writer_emits_artifact_without_registry_mutation(tmp_path) -> None:
    path = tmp_path / "metric-access-width.json"
    payload = write_final_root_metric_access_width_no_go_report(
        path,
        write_registry=False,
    )

    assert path.exists()
    assert payload["theorem"]["theorem_verified"]
    assert payload["headline_metrics"]["exact_control_failure_count"] == 0
