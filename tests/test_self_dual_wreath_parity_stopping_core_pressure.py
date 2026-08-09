import itertools
import math
from functools import lru_cache

import pytest

from self_dual_wreath_parity_stopping_core_pressure import (
    audit_parity_stopping_core,
    even_parity_code,
    hypercube_independent_set_rigidity_control,
    involution_count,
    parity_class,
    parity_stopping_core_supports,
    run_parity_stopping_core_pressure,
)


@lru_cache(maxsize=1)
def _report():
    return run_parity_stopping_core_pressure()


@pytest.mark.parametrize("width", range(2, 7))
def test_even_parity_support_is_a_nonpeelable_power_boundary_family(width):
    pattern, same, different, removed = parity_stopping_core_supports(width)
    code = even_parity_code(width)
    assert pattern == "E" + "BABA" + "A" * width + "FEF"
    assert removed in code
    assert len(code) == 2 ** (width - 1)
    assert len(same) == 2 ** (width - 1) - 1
    assert len(different) == 2 ** (width - 1)
    assert all(
        sum(a != b for a, b in zip(left, right)) != 1
        for left, right in itertools.combinations(code, 2)
    )


@pytest.mark.parametrize("width", range(2, 7))
def test_exact_controls_preserve_finite_signal_but_restore_pressure_gap(width):
    control = next(row for row in _report().finite_controls if row.core_width == width)
    assert control.support_difference_peeling_stalls_on_full_core
    assert control.remaining_generator_count == 6
    assert control.generic_integer_certificate_margin > 0
    assert control.reducer_pressure_margin >= control.involution_pressure_margin
    assert control.involution_pressure_margin >= 0.5
    assert control.exact_S3_sign_character_average == 1.0
    assert control.exact_S3_standard_normalized_character_average == 0.5
    assert control.finite_nontrivial_target_signal_survives
    if width >= 3:
        expected = 0.5 + 0.5 * math.log2(
            2 ** (width - 1) / (2 ** (width - 1) - 1)
        )
        assert control.even_code_contains_required_weight_two_rows
        assert control.exact_involution_forcing_subpresentation_verified
        assert control.residual_involution_relation_present
        assert control.involution_pressure_margin == pytest.approx(expected)
    assert control.exact_control_verified


def test_involution_counts_include_identity_and_have_half_exponent_limit():
    assert involution_count(3) == 4
    assert involution_count(4) == 10
    scaling = _report().involution_scaling
    assert scaling[-1].symmetric_group_degree == 80
    assert scaling[-1].log_group_exponent > 0.5
    assert scaling[-1].log_group_exponent < scaling[0].log_group_exponent


@pytest.mark.parametrize("width", range(1, 5))
def test_maximum_hypercube_independent_sets_are_exactly_parity_classes(width):
    control = hypercube_independent_set_rigidity_control(width)
    assert len(parity_class(width, 0)) == 2 ** (width - 1)
    assert len(parity_class(width, 1)) == 2 ** (width - 1)
    assert control.independent_maximum_set_count == 2
    assert control.every_maximum_independent_set_is_a_parity_class


def test_report_rejects_the_family_without_erasing_the_finite_target_signal():
    report = _report()
    assert report.headline_metrics[
        "all_depth_parity_stopping_core_no_go_theorem_count"
    ] == 1
    assert report.headline_metrics["control_failure_count"] == 0
    assert report.headline_metrics[
        "stored_extremal_parity_coset_control_count"
    ] == 8
    assert report.headline_metrics[
        "maximum_independent_set_rigidity_failure_count"
    ] == 0
    assert all(
        row.exact_control_verified
        for row in report.extremal_parity_coset_controls
    )
    assert report.headline_metrics[
        "minimum_stored_involution_pressure_margin"
    ] > 0.5
    assert report.claim_gate["nonpeelable_power_boundary_family_constructed"]
    assert report.claim_gate["finite_S3_target_signal_survives"]
    assert not report.claim_gate[
        "parity_stopping_core_actual_pressure_survives"
    ]
    assert report.claim_gate["parity_stopping_core_uniformly_subleading"]
    assert report.claim_gate[
        "all_single_fiber_maximum_density_stopping_cores_controlled"
    ]
    assert not report.claim_gate["all_nonlinear_stopping_cores_controlled"]
    assert not report.claim_gate["speedup_claim_allowed"]
