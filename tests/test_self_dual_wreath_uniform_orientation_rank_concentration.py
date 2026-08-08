from fractions import Fraction

from self_dual_wreath_uniform_orientation_rank_concentration import (
    audit_orientation_rank_identity,
    audit_second_moment,
    normalized_target_multiplicity_relative_variance,
    relative_variance_class_bound,
    run_uniform_orientation_rank_concentration,
    uniform_rank_concentration_record,
)


def test_exact_second_moment_matches_direct_plancherel_tuples() -> None:
    for target in ((3,), (2, 1), (1, 1, 1)):
        record = audit_second_moment(
            3, 3, target, direct_check=True
        )

        assert record.direct_formula_match
        assert record.bound_respected


def test_relative_variance_obeys_the_class_size_bound() -> None:
    relative = normalized_target_multiplicity_relative_variance(
        7, 5, (4, 2, 1)
    )
    bound = relative_variance_class_bound(7, 5)

    assert isinstance(relative, Fraction)
    assert 0 <= relative <= bound


def test_physical_orientation_rank_identity_is_exact_but_not_equal_finitely() -> None:
    labels = (
        ((6,), (2, 2, 2)),
        ((5, 1), (2, 2, 1, 1)),
        ((4, 2), (2, 1, 1, 1, 1)),
        ((3, 3), (1, 1, 1, 1, 1, 1)),
    )

    record = audit_orientation_rank_identity((6,), labels)

    assert record.exact_rank_identity_verified
    assert record.minimum_orientation_rank == 0
    assert record.maximum_orientation_rank == 2025
    assert not record.finite_orientation_ranks_equal


def test_natural_depth_union_bound_survives_distinct_conditioning() -> None:
    early = uniform_rank_concentration_record(12)
    onset = uniform_rank_concentration_record(16)
    late = uniform_rank_concentration_record(48)

    assert not early.uniform_all_orientation_all_target_concentration_certified
    assert onset.uniform_all_orientation_all_target_concentration_certified
    assert late.uniform_all_orientation_all_target_concentration_certified
    assert late.log2_collision_free_conditioned_failure_upper_bound < -1000
    assert (
        late.log2_collision_free_conditioned_failure_upper_bound
        < early.log2_collision_free_conditioned_failure_upper_bound
    )


def test_report_removes_rank_obstruction_but_not_operator_gate() -> None:
    report = run_uniform_orientation_rank_concentration()

    assert report.claim_gate["exact_multiplicity_second_moment_proved"]
    assert report.claim_gate[
        "all_orientation_all_target_rank_concentration_proved"
    ]
    assert report.claim_gate[
        "collision_free_conditioned_rank_concentration_proved"
    ]
    assert not report.claim_gate["exact_unequal_source_translation_covariance"]
    assert not report.claim_gate["pair_core_operator_concentration_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
