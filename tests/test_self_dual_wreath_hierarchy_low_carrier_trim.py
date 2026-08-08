import math
from fractions import Fraction

from representation_obstruction import hook_length_dimension, integer_partitions
from self_dual_wreath_hierarchy_low_carrier_trim import (
    audit_exact_low_carrier_mass,
    canonical_carrier_cutoff,
    hierarchy_low_carrier_trim_scaling_record,
    low_carrier_power_sums,
    run_hierarchy_low_carrier_trim,
)


def test_canonical_cutoff_obeys_quarter_factorial_bound() -> None:
    for n in (8, 12, 20, 32, 48):
        order = math.factorial(n)
        partition_count = len(tuple(integer_partitions(n)))
        cutoff = canonical_carrier_cutoff(n)
        assert cutoff >= 1
        if math.isqrt(math.isqrt(order)) >= partition_count:
            assert cutoff * partition_count <= order ** 0.25


def test_exact_nonantipodal_low_carrier_fourth_power_law() -> None:
    for n, target, cutoff, random_count in (
        (3, (2, 1), 1, 1),
        (3, (2, 1), 2, 1),
        (4, (3, 1), 2, 2),
        (4, (2, 2), 3, 2),
    ):
        record = audit_exact_low_carrier_mass(
            n,
            target,
            cutoff,
            random_count,
        )
        _, _, low_z4 = low_carrier_power_sums(n, cutoff)
        assert Fraction(
            record.observed_nonantipodal_low_carrier_relative_rank
        ) == Fraction(low_z4, math.factorial(n) ** 3)
        assert record.exact_nonantipodal_low_carrier_law_verified


def test_root_antipodal_low_carrier_law_tracks_target_dimension() -> None:
    for target, cutoff in (((4,), 1), ((3, 1), 2), ((3, 1), 3)):
        record = audit_exact_low_carrier_mass(4, target, cutoff, 2)
        dimension = hook_length_dimension(target)
        predicted = Fraction(
            dimension**2 if dimension <= cutoff else 0,
            math.factorial(4) ** 2,
        )
        assert Fraction(
            record.observed_root_antipodal_low_carrier_relative_rank
        ) == predicted
        assert record.exact_root_antipodal_low_carrier_law_verified


def test_scaling_matches_exact_rank_budget_and_beats_polynomial_pair_scale() -> None:
    record = hierarchy_low_carrier_trim_scaling_record(48)
    assert record.carrier_dimension_cutoff_log2 > 30
    assert record.low_carrier_count > 100
    assert record.conditioned_all_target_trim_rank_log2 < -15
    assert record.residual_pair_correlation_log2 < -30
    assert record.finite_simultaneous_trim_certified
    assert record.asymptotic_vanishing_rank_and_pair_correlation_proved
    assert not record.high_carrier_frame_edge_proved


def test_report_keeps_high_carrier_and_speedup_gates_closed() -> None:
    report = run_hierarchy_low_carrier_trim()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics["first_finite_conditioned_trim_n"] == 44
    assert report.claim_gate["all_hierarchy_low_carrier_rank_budget_proved"]
    assert report.claim_gate["quarter_factorial_cutoff_tradeoff_proved"]
    assert report.claim_gate["residual_pair_correlation_vanishes"]
    assert not report.claim_gate["arbitrary_source_coupling_covered"]
    assert not report.claim_gate["high_carrier_signed_incidence_controlled"]
    assert not report.claim_gate["collision_free_noncommon_frame_edge_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
