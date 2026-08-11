import math

import pytest

from coset_measurement_copy_width_whitening_tradeoff import (
    arbitrary_measurement_success_upper_bound,
    audit_finite_measurement_dimension_control,
    build_coset_measurement_copy_width_whitening_report,
    minimum_copies_for_target_success,
    success_whitening_scaling_record,
    target_forced_multiplicity_rank_lower_bound,
    write_coset_measurement_copy_width_whitening_report,
)


def test_arbitrary_measurement_dimension_bound_sets_exact_copy_threshold():
    hidden_count = 105
    target = 1 / 8
    copies = minimum_copies_for_target_success(hidden_count, target)
    assert copies == math.ceil(math.log2(hidden_count * target))
    assert arbitrary_measurement_success_upper_bound(
        hidden_count, copies - 1
    ) < target
    assert arbitrary_measurement_success_upper_bound(
        hidden_count, copies
    ) >= target


def test_exact_s3_pgm_obeys_support_and_ambient_dimension_bounds():
    for copy_count in (1, 2):
        row = audit_finite_measurement_dimension_control(3, copy_count)
        assert row.theorem_control_passed
        assert row.maximum_pairwise_projector_overlap_residual < 1e-9
        assert row.pgm_completeness_residual < 1e-8
        assert row.pgm_success_probability <= (
            row.support_dimension_success_upper_bound + 1e-9
        )
        assert row.support_dimension_success_upper_bound <= (
            row.ambient_dimension_success_upper_bound + 1e-9
        )


def test_inverse_polynomial_success_window_retains_rank_lower_bound():
    n = 32
    target = n**-2
    row = success_whitening_scaling_record(
        n,
        success_requirement_id="inverse-quadratic",
        target_success_probability=target,
        polynomial_exponent=2,
    )
    assert row.inverse_polynomial_success_regime
    assert row.copy_deficit_from_pgm_width <= 2 * math.ceil(math.log2(n)) + 1
    assert row.success_upper_bound_one_copy_below_minimum < target
    assert row.success_upper_bound_at_minimum >= target
    assert row.exact_multiplicity_rank_lower_bound_at_minimum >= (
        row.target_only_multiplicity_rank_lower_bound
    )
    assert row.rank_sandwich_consistent


def test_target_forced_lower_bound_rejects_invalid_success():
    with pytest.raises(ValueError, match="target success"):
        target_forced_multiplicity_rank_lower_bound(8, 105, 0.0)
    with pytest.raises(ValueError, match="target success"):
        minimum_copies_for_target_success(105, 1.1)


def test_report_closes_copy_escape_but_not_fused_measurements(tmp_path):
    report = build_coset_measurement_copy_width_whitening_report()
    assert report.theorem.theorem_verified
    assert report.theorem.arbitrary_povm_exact_identification_bound_proved
    assert report.theorem.inverse_polynomial_copy_window_proved
    assert report.theorem.exp_sqrt_standalone_whitening_in_success_window_proved
    assert not report.theorem.alternative_collective_measurement_ruled_out
    assert not report.theorem.fused_polar_isometry_ruled_out
    assert not report.theorem.decision_problem_lower_bound_proved
    assert not report.theorem.general_quantum_circuit_lower_bound_proved
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_coset_measurement_copy_width_whitening_report(
        tmp_path / "report.json"
    )
    assert payload["status"] == (
        "exact-identification-copy-window-proved-"
        "standalone-whitening-closed-fused-measurement-open"
    )
