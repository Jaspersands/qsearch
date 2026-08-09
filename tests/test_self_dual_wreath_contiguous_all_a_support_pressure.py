import itertools
import math

import pytest

from self_dual_wreath_contiguous_all_a_support_pressure import (
    audit_contiguous_all_a_support_pressure,
    audit_finite_contiguous_all_a_control,
    outer_conjugacy_fiber_certificate,
    run_contiguous_all_a_support_pressure,
)


def test_outer_equation_has_exact_conjugacy_normal_form_for_every_base_through_width_five():
    for width in range(1, 6):
        for base in itertools.product((0, 1), repeat=width):
            certificate = outer_conjugacy_fiber_certificate(base)
            assert certificate.exact_conjugacy_normal_form_verified
            assert certificate.uniform_finite_group_outer_bound == "|G|*k(G)"


def test_nonzero_base_and_nonlinear_support_are_certified():
    same = ((0, 0, 0, 0), (1, 1, 0, 0), (1, 1, 1, 1))
    different = ((1, 0, 1, 0), (0, 1, 1, 1), (1, 1, 0, 1))
    control = audit_contiguous_all_a_support_pressure(
        "NONZERO-NONLINEAR",
        same,
        different,
    )
    assert control.different_base_assignment != (0, 0, 0, 0)
    assert (0, 0, 0, 0) in control.rerooted_different_support
    assert control.same_fiber_induction_verified
    assert control.different_fiber_rerooting_verified
    assert control.different_fiber_induction_verified
    assert control.outer_conjugacy_bound_verified
    assert control.crossing_pressure_upper_bound <= -1
    assert control.exact_all_support_pressure_theorem_verified


def test_larger_fiber_pays_average_support_entropy():
    cube = tuple(itertools.product((0, 1), repeat=5))
    control = audit_contiguous_all_a_support_pressure(
        "ASYMMETRIC",
        ((1, 1, 1, 1, 1),),
        cube,
    )
    assert control.dominant_fiber == "different-common-value-fiber"
    assert control.dominant_fiber_entropy_bits == 5
    assert control.support_entropy_exponent == 2.5
    assert control.frame_solution_exponent_upper_bound == 0
    assert control.crossing_pressure_upper_bound == pytest.approx(-3.5)


def test_exact_S3_full_counts_obey_bound_for_every_width_two_support_pair():
    cube = tuple(itertools.product((0, 1), repeat=2))
    supports = tuple(
        tuple(row for index, row in enumerate(cube) if mask >> index & 1)
        for mask in range(1, 1 << len(cube))
    )
    for same in supports:
        for different in supports:
            control = audit_finite_contiguous_all_a_control(
                "EXHAUSTIVE-S3-WIDTH-TWO",
                same,
                different,
            )
            assert control.exact_count_below_theorem_bound
            assert math.isfinite(control.theorem_solution_count_upper_bound)


def test_report_proves_scalar_pressure_but_blocks_component_claims():
    report = run_contiguous_all_a_support_pressure()
    metrics = report.headline_metrics
    assert metrics["checked_arbitrary_support_pair_count_through_width_three"] == 65259
    assert metrics["arbitrary_support_pair_control_failure_count"] == 0
    assert metrics["finite_S3_control_failure_count"] == 0
    assert metrics[
        "growing_width_arbitrary_support_scalar_pressure_theorem_count"
    ] == 1
    assert report.claim_gate["arbitrary_supports_certified"]
    assert report.claim_gate["nonzero_different_bases_certified"]
    assert report.claim_gate["growing_width_scalar_pressure_proved"]
    assert not report.claim_gate["mixed_target_character_control_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
