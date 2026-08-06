import math

import numpy as np
import pytest

from self_dual_wreath_pgm_success_theorem import (
    audit_holder_control,
    exact_projector_frame_second_moment_coefficient,
    pgm_success_lower_bound,
    pgm_success_scaling_record,
    run_pgm_success_theorem,
)


def test_exact_projector_moment_and_success_formula() -> None:
    hidden_count = math.factorial(8)
    copies = math.ceil(math.log2(hidden_count))
    coefficient = exact_projector_frame_second_moment_coefficient(
        hidden_count,
        copies,
    )

    assert coefficient == pytest.approx(
        (1 + (hidden_count - 1) / 2**copies) / hidden_count
    )
    assert pgm_success_lower_bound(hidden_count, copies) == pytest.approx(
        1 / (hidden_count * coefficient)
    )


def test_information_threshold_and_copy_slack_bounds() -> None:
    threshold = pgm_success_scaling_record(512, extra_copies=0)
    two_extra = pgm_success_scaling_record(512, extra_copies=2)

    assert threshold.pgm_success_lower_bound > 0.5
    assert not threshold.bounded_error_one_third_certified
    assert two_extra.pgm_success_lower_bound >= 0.8
    assert two_extra.bounded_error_one_third_certified
    assert not two_extra.polynomial_pgm_implementation_proved


def test_holder_control_is_exact_for_flat_spectrum() -> None:
    matrix = np.diag([0.25, 0.25, 0.25, 0.25, 0.0])
    control = audit_holder_control("flat", matrix)

    assert control.inequality_verified
    assert control.holder_residual_margin == pytest.approx(0.0, abs=1e-12)
    assert control.holder_lower_bound == pytest.approx(4.0)


def test_holder_control_is_valid_for_nonuniform_spectrum() -> None:
    control = audit_holder_control(
        "nonuniform",
        np.diag([0.7, 0.2, 0.1]),
    )

    assert control.inequality_verified
    assert control.holder_residual_margin > 0


def test_report_closes_success_but_not_implementation() -> None:
    report = run_pgm_success_theorem()

    assert report.headline_metrics["holder_control_failure_count"] == 0
    assert report.headline_metrics["physical_branch_bound_failure_count"] == 0
    assert report.headline_metrics["minimum_threshold_pgm_success_lower_bound"] > 0.5
    assert report.headline_metrics["minimum_two_extra_copy_success_lower_bound"] >= 0.8
    assert report.claim_gate["information_theoretic_pgm_success_proved"]
    assert report.claim_gate["bounded_error_with_constant_extra_copies_proved"]
    assert not report.claim_gate["conditional_branch_uniform_success_proved"]
    assert not report.claim_gate["polynomial_coherent_pgm_implementation_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
