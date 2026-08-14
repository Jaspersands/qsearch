import math

from self_dual_wreath_racah_entropic_delocalization_certificate import (
    audit_global_entropic_tail_certificate,
    audit_operator_relative_overlap_bound,
    entropic_tail_upper_bits,
    run_racah_entropic_delocalization_certificate,
    synthetic_entropic_scaling_control,
    write_racah_entropic_delocalization_report,
)


def test_entropy_tail_bound_handles_zero_and_positive_bad_mass() -> None:
    assert entropic_tail_upper_bits(10, 2.0, 0.0) == 1.0
    expected = 1.0 + 0.1 * math.log2(1000.0)
    assert math.isclose(
        entropic_tail_upper_bits(10, 2.0, 0.1), expected, rel_tol=1e-14
    )


def test_exact_finite_racah_information_obeys_average_tail_certificate() -> None:
    for n, threshold in ((3, 1.0), (4, 1.0), (5, 1.0), (5, 2.0), (5, 4.0)):
        row = audit_global_entropic_tail_certificate(n, threshold)
        assert row.certificate_violation_bits < 2e-9
        assert row.average_tail_certificate_upper_bits >= (
            row.physical_average_recoupling_mutual_information_bits - 2e-9
        )
        assert row.exact_entropic_tail_certificate_verified


def test_operator_norm_bound_controls_relative_block_overlap() -> None:
    row = audit_operator_relative_overlap_bound(20, 4, 5, 0.25, 1.0)

    assert row.exact_relative_block_overlap == 1.0
    assert row.operator_relative_overlap_upper == 1.0
    assert row.operator_bound_violation == 0.0
    assert row.exact_operator_certificate_verified


def test_synthetic_tail_schedule_is_sublogarithmic() -> None:
    rows = [synthetic_entropic_scaling_control(n) for n in (20, 100, 1_000, 10_000)]

    assert all(row.sufficient_asymptotic_conditions_satisfied for row in rows)
    assert not any(row.natural_racah_conditions_proved for row in rows)
    assert rows[-1].information_upper_over_log2_n < rows[0].information_upper_over_log2_n


def test_report_keeps_both_natural_tail_rates_open(tmp_path) -> None:
    report = run_racah_entropic_delocalization_certificate()

    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["tail_tolerant_racah_mi_certificate_proved"]
    assert report.claim_gate[
        "operator_norm_to_relative_overlap_bound_proved"
    ]
    assert not report.claim_gate["uniform_racah_collision_bound_required"]
    assert not report.claim_gate[
        "natural_subpolynomial_good_block_overlap_proved"
    ]
    assert not report.claim_gate["natural_bad_block_mass_rate_proved"]
    assert not report.claim_gate["physical_rank_profile_mixes_proved"]
    assert not report.claim_gate["algorithm_claim_allowed"]
    assert not report.claim_gate["speedup_claim_allowed"]

    path = tmp_path / "racah-entropic-tail.json"
    payload = write_racah_entropic_delocalization_report(path)
    assert path.exists()
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0
