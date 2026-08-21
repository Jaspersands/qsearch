import math

from self_dual_wreath_point_copy_threshold import (
    annealed_point_signal_bounds,
    audit_point_threshold_finite_control,
    build_point_copy_threshold_report,
    direct_word_density_control,
    exact_maximum_nonidentity_class_reciprocal,
    maximum_nonidentity_class_reciprocal,
    point_threshold_scaling_record,
    write_point_copy_threshold_report,
)


def test_smallest_nonidentity_class_is_transposition_scale():
    for n in range(5, 13):
        assert math.isclose(
            exact_maximum_nonidentity_class_reciprocal(n),
            maximum_nonidentity_class_reciprocal(n),
            rel_tol=0.0,
            abs_tol=1e-15,
        )


def test_commutator_and_product_of_conjugates_have_same_direct_law():
    for n in (3, 4, 5):
        row = direct_word_density_control(n)
        assert row.direct_word_laws_identical
        assert row.maximum_class_count_mismatch == 0
        assert row.commutator_class_counts == row.conjugate_product_class_counts


def test_exact_finite_point_signals_lie_inside_theorem_bounds():
    for n in (5, 6):
        for multiplier in (1.0, 1.5, 2.0):
            row = audit_point_threshold_finite_control(n, multiplier)
            assert row.exact_signal_inside_certified_interval
            assert row.lower_bound_residual >= -1e-10
            assert row.upper_bound_residual >= -1e-10


def test_subcritical_point_povm_bound_collapses_with_rank():
    rows = [point_threshold_scaling_record(n, 1.0) for n in (16, 32, 64, 128)]
    assert all(row.subcritical_point_decoder_excess_superpolynomial for row in rows)
    assert all(
        right.signal_upper_bound_log2 < left.signal_upper_bound_log2
        for left, right in zip(rows, rows[1:])
    )
    assert rows[-1].arbitrary_point_povm_excess_log2_upper_bound < -300.0


def test_factor_two_copy_width_has_positive_normalized_energy_lower_bound():
    for n in (16, 32, 64, 128):
        row = point_threshold_scaling_record(n, 2.0)
        bounds = annealed_point_signal_bounds(n, row.copy_count)
        assert row.critical_normalized_energy_lower_bound
        assert bounds.signal_lower_bound >= 0.5 * (n - 1)
        assert not row.critical_harmonic_measurement_compiled


def test_report_closes_subcritical_point_route_without_promoting_critical_energy(tmp_path):
    report = build_point_copy_threshold_report()
    assert report.theorem.theorem_verified
    assert report.theorem.subcritical_arbitrary_point_povm_no_go_proved
    assert report.theorem.critical_normalized_energy_phase_transition_proved
    assert not report.theorem.critical_operational_point_advantage_proved
    assert not report.theorem.critical_harmonic_naimark_compiled
    assert not report.claim_gate["point_decoder_at_information_threshold_viable"]
    assert not report.claim_gate["critical_energy_is_operational_advantage"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_point_copy_threshold_report(tmp_path / "threshold.json")
    assert payload["status"] == (
        "point-copy-threshold-two-proved-critical-harmonic-measurement-open"
    )
    assert not payload["claim_gate"]["speedup_claim_allowed"]
