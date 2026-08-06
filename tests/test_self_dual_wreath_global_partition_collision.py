from self_dual_wreath_character_moments import unequal_pair_descriptor
from self_dual_wreath_global_partition_collision import (
    exact_all_distinct_probability,
    global_collision_record,
    known_repeated_source_counterexample,
    run_global_partition_collision,
    source_partitions_globally_distinct,
)


def test_exact_weighted_occupancy_probability() -> None:
    assert exact_all_distinct_probability(2, 1) == 1
    assert exact_all_distinct_probability(2, 2) == 0.5
    assert exact_all_distinct_probability(2, 3) == 0


def test_union_bound_is_a_valid_lower_bound_on_all_distinct_probability() -> None:
    for n in (8, 12, 16):
        record = global_collision_record(n)
        assert 0 <= record.exact_all_distinct_probability <= 1
        assert (
            record.exact_all_distinct_probability + 1e-12
            >= record.all_distinct_probability_lower_bound
        )


def test_global_distinctness_checks_cross_label_partition_reuse() -> None:
    distinct = (
        unequal_pair_descriptor((4,), (3, 1)),
        unequal_pair_descriptor((2, 2), (2, 1, 1)),
    )
    repeated = (
        unequal_pair_descriptor((4,), (3, 1)),
        unequal_pair_descriptor((4,), (2, 2)),
    )
    assert source_partitions_globally_distinct(distinct)
    assert not source_partitions_globally_distinct(repeated)


def test_known_half_norm_counterexample_is_excluded() -> None:
    record = known_repeated_source_counterexample()
    assert record.maximum_frame_eigenvalue == 0.5
    assert not record.globally_distinct
    assert record.excluded_by_global_distinct_event


def test_report_retargets_without_unlocking_speedup() -> None:
    report = run_global_partition_collision()
    assert report.claim_gate[
        "asymptotic_global_all_distinct_dominance_proved"
    ]
    assert report.claim_gate[
        "known_repeated_source_half_norm_counterexample_excluded"
    ]
    assert not report.claim_gate["collision_free_tuple_norm_bound_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
