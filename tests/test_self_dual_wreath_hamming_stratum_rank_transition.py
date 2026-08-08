import math

from self_dual_wreath_hamming_stratum_rank_transition import (
    class_variance_upper_bound,
    hamming_stratum_scaling_record,
    run_hamming_stratum_rank_transition,
)
from self_dual_wreath_plancherel_kronecker_positivity import (
    reciprocal_nonidentity_class_sum,
)


def test_hamming_three_variance_is_the_ordinary_kronecker_bound() -> None:
    for n in range(3, 10):
        assert class_variance_upper_bound(n, 3) == (
            reciprocal_nonidentity_class_sum(n)
        )


def test_expected_bad_fraction_bound_improves_with_hamming_distance() -> None:
    for n in (10, 20, 30, 40, 50):
        records = [hamming_stratum_scaling_record(n, h) for h in (3, 4, 5)]
        assert records[2].expected_bad_pair_fraction_upper_bound < records[1].expected_bad_pair_fraction_upper_bound
        assert records[1].expected_bad_pair_fraction_upper_bound < records[0].expected_bad_pair_fraction_upper_bound
        assert all(record.asymptotic_live_pair_fraction == "1-o(1)" for record in records)
        assert all(not record.simultaneous_every_pair_control_proved for record in records)


def test_good_pair_rank_window_matches_six_factor_union_argument() -> None:
    record = hamming_stratum_scaling_record(30, 3, 0.2)
    assert math.isclose(
        record.normalized_pair_rank_lower_bound_on_good_pairs,
        2 * 0.8**3,
    )
    assert math.isclose(
        record.normalized_pair_rank_upper_bound_on_good_pairs,
        2 * 1.2**3,
    )
    assert math.isclose(
        record.bad_fraction_exceeds_threshold_probability_upper_bound_before_conditioning,
        math.sqrt(record.expected_bad_pair_fraction_upper_bound),
    )


def test_report_keeps_incidence_central_support_and_speedup_gates_closed() -> None:
    report = run_hamming_stratum_rank_transition()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate[
        "sharp_hamming_one_two_vs_three_support_transition_proved"
    ]
    assert report.claim_gate[
        "fixed_hamming_at_least_three_live_pair_density_one_proved"
    ]
    assert not report.claim_gate[
        "simultaneous_every_fixed_hamming_pair_controlled"
    ]
    assert not report.claim_gate["coherent_pair_core_incidence_controlled"]
    assert not report.claim_gate[
        "full_node_bad_projection_central_support_controlled"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]
