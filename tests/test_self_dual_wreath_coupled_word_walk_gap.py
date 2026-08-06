from fractions import Fraction

from self_dual_wreath_coupled_word_walk_gap import (
    coupled_scaling_record,
    exact_coupled_walk_moment,
    run_wreath_coupled_word_walk_gap,
    validate_bridge_subgroup,
    validate_coupled_walk_moment,
)


def test_bridge_class_generates_the_expected_index_two_subgroup() -> None:
    for n in (2, 3, 4):
        record = validate_bridge_subgroup(n)
        assert record.index_two_verified
        assert record.generated_subgroup_order * 2 == record.wreath_group_order


def test_coupled_chain_matches_direct_shared_sequence_moment() -> None:
    for parameters in ((2, 3, 3), (3, 2, 3)):
        record = validate_coupled_walk_moment(*parameters)
        assert record.exact_match


def test_exact_coupled_moment_is_a_probability_scale_statistic() -> None:
    value = exact_coupled_walk_moment(
        n=3,
        copy_count=2,
        moment_order=3,
    )
    assert isinstance(value, Fraction)
    assert 0 < value <= 1


def test_constant_gap_bound_is_independent_of_copy_count() -> None:
    records = [
        coupled_scaling_record(
            n=8,
            copy_count=copy_count,
            moment_order=506,
            second_moment_eigenvalue_scale=4.005999792189825e-5,
        )
        for copy_count in (2, 8, 16)
    ]
    assert {record.coupled_spectral_gap_lower_bound for record in records} == {
        0.25
    }
    assert {
        record.coupled_nonconstant_spectral_radius_upper_bound
        for record in records
    } == {0.75}


def test_constant_gap_does_not_overclaim_typical_moment_control() -> None:
    report = run_wreath_coupled_word_walk_gap()
    assert report.claim_gate["constant_coupled_spectral_gap_proved"]
    assert report.claim_gate["coupled_k_walk_contraction_proved"]
    assert not report.claim_gate[
        "certificate_order_reaches_stationary_scale"
    ]
    assert not report.claim_gate[
        "typical_all_unequal_conditioned_kernel_derived"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]
    assert report.headline_metrics[
        "tail_log2_root_to_second_moment_scale_gap"
    ] > 0
