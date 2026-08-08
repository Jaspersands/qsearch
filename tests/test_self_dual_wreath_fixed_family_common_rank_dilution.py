import math
from fractions import Fraction

from self_dual_wreath_fixed_family_common_rank_dilution import (
    _membership_pattern_counts,
    audit_pair_expectation,
    canonical_full_pattern_orientations,
    expected_relative_common_rank,
    fixed_family_dilution_scaling_record,
    full_pattern_family_parameters,
    run_fixed_family_common_rank_dilution,
)


def test_canonical_family_realizes_every_nonzero_pattern_equally() -> None:
    for family_size in (2, 3, 4):
        repetitions = 3
        orientations = canonical_full_pattern_orientations(
            family_size, repetitions
        )
        source_pairs = repetitions * (1 << (family_size - 1))
        counts = _membership_pattern_counts(orientations, source_pairs)
        assert counts[0] == repetitions
        assert all(
            counts[pattern] == repetitions
            for pattern in range(1, 1 << family_size)
        )


def test_exact_expected_rank_formula() -> None:
    order = math.factorial(5)
    assert expected_relative_common_rank(order, 2) == Fraction(2, order**3)
    assert expected_relative_common_rank(order, 3) == Fraction(16, order**7)
    assert expected_relative_common_rank(order, 4) == Fraction(1 << 11, order**15)
    assert full_pattern_family_parameters(4) == (15, 4, 11)


def test_complete_s5_pair_plancherel_expectation_control() -> None:
    record = audit_pair_expectation()
    assert record.target_count == 7
    assert record.source_tuple_count_per_target == 7**4
    assert record.predicted_expected_relative_common_rank == "1/864000"
    assert record.maximum_exact_expectation_residual == "0"
    assert record.exact_plancherel_expectation_verified


def test_fixed_family_scalar_mass_decays_doubly_in_family_patterns() -> None:
    records = [fixed_family_dilution_scaling_record(48, size) for size in (2, 3, 4)]
    assert all(record.asymptotic_relative_rank_concentration for record in records)
    assert all(record.global_distinct_transfer_valid for record in records)
    assert all(
        not record.full_node_bad_spectral_projection_dilution_proved
        for record in records
    )
    assert records[2].expected_relative_common_rank_log2 < records[1].expected_relative_common_rank_log2
    assert records[1].expected_relative_common_rank_log2 < records[0].expected_relative_common_rank_log2


def test_report_keeps_full_node_edge_and_speedup_gates_closed() -> None:
    report = run_fixed_family_common_rank_dilution()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["fixed_family_common_support_probability_one_proved"]
    assert report.claim_gate["fixed_family_relative_rank_dilution_proved"]
    assert not report.claim_gate["support_only_higher_order_incidence_sufficient_for_edge"]
    assert not report.claim_gate["full_node_bad_projection_central_support_controlled"]
    assert not report.claim_gate["speedup_claim_allowed"]
