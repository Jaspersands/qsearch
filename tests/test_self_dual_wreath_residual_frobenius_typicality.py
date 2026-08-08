from fractions import Fraction

import numpy as np

from self_dual_wreath_residual_frobenius_typicality import (
    audit_frobenius_spectral_trim,
    audit_occupancy_energy,
    expected_star_overlap_energy_by_occupancy,
    residual_frobenius_scaling_record,
    run_residual_frobenius_typicality,
)


def test_every_occupancy_stratum_obeys_the_universal_energy_bound() -> None:
    for mask in range(16):
        occupancy = tuple(bool(mask & (1 << index)) for index in range(4))
        record = audit_occupancy_energy(7, (4, 2, 1), occupancy)

        assert record.universal_bound_respected
        if record.arm_class_missing:
            assert record.residual_vanishes_when_arm_class_missing


def test_full_and_target_only_strata_saturate_before_common_removal() -> None:
    order = __import__("math").factorial(7)
    bound = Fraction(4, order**5)
    target_only_residual, target_only_common = (
        expected_star_overlap_energy_by_occupancy(
            7, (4, 2, 1), (False, True, True, True)
        )
    )
    full_residual, full_common = expected_star_overlap_energy_by_occupancy(
        7, (4, 2, 1), (True, True, True, True)
    )

    assert target_only_residual == bound
    assert target_only_common == 0
    assert full_residual + full_common == bound


def test_two_operator_frobenius_trim_bound() -> None:
    metric = np.diag([0.0] * 18 + [0.6, -0.7])
    graded = np.diag([0.0] * 17 + [0.5, -0.8, 0.9])

    record = audit_frobenius_spectral_trim(metric, graded, 0.25)

    assert record.frobenius_markov_bound_respected
    assert record.metric_removed_dimension == 2
    assert record.graded_removed_dimension == 3
    assert record.joint_retained_dimension_lower_bound == 15
    assert record.metric_retained_norm <= 0.25
    assert record.graded_retained_norm <= 0.25


def test_natural_frobenius_trim_turns_on_after_pair_rank_concentration() -> None:
    early = residual_frobenius_scaling_record(32)
    late = residual_frobenius_scaling_record(48)

    assert not early.finite_vanishing_fraction_trim_certified
    assert late.finite_vanishing_fraction_trim_certified
    assert late.metric_and_graded_removed_fraction_upper_bound < 1e-20
    assert late.combined_structural_failure_probability_upper_bound < 1e-20


def test_report_keeps_physical_graded_trim_and_pgm_transfer_open() -> None:
    report = run_residual_frobenius_typicality()

    assert report.claim_gate[
        "universal_residual_star_frobenius_bound_proved"
    ]
    assert report.claim_gate[
        "natural_relation_frobenius_density_vanishes_proved"
    ]
    assert report.claim_gate[
        "vanishing_coefficient_fraction_spectral_trim_exists"
    ]
    assert not report.claim_gate["grading_compatible_trim_proved"]
    assert not report.claim_gate[
        "coefficient_trace_equals_pgm_state_trace_proved"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]
