import itertools

from self_dual_wreath_all_unequal_conditioned_kernel import (
    conditioned_character_kernel,
    conditioned_scaling_record,
    conditioned_unequal_probability,
    plancherel_collision_probability,
    run_all_unequal_conditioned_kernel,
    unequal_descriptors,
    validate_conditioned_kernel,
    validate_conditioned_word_formula,
)


def test_conditioned_unequal_source_law_is_normalized() -> None:
    for n in (2, 3, 4, 5):
        total = sum(
            conditioned_unequal_probability(descriptor)
            for descriptor in unequal_descriptors(n)
        )
        assert total == 1
        assert 0 < plancherel_collision_probability(n) < 1


def test_conditioned_kernel_is_exact_and_annihilates_swap_coset() -> None:
    for n in (2, 3, 4):
        record = validate_conditioned_kernel(n)
        assert record.exact_kernel_verified
        assert record.failed_element_count == 0
        assert record.identity_kernel_value == "1"
        assert record.maximum_swap_coset_absolute_value == 0

    n = 3
    identity = tuple(range(n))
    for permutation in itertools.permutations(range(n)):
        assert (
            conditioned_character_kernel(
                n,
                (permutation, identity, 1),
            )
            == 0
        )


def test_conditioned_word_formula_and_half_power_mean_are_exact() -> None:
    for parameters in ((2, 3), (3, 2), (3, 3)):
        record = validate_conditioned_word_formula(*parameters)
        assert record.exact_sequence_formula_verified
        assert record.annealed_half_power_verified


def test_half_norm_bound_remains_far_above_k_coordinate_scale() -> None:
    record = conditioned_scaling_record(
        n=64,
        copy_count=296,
        moment_order=175526,
        second_moment_eigenvalue_scale=1.5735581757746686e-89,
    )
    assert record.all_unequal_frame_half_norm_bound_proved
    assert not record.simultaneous_k_coordinate_contraction_proved
    assert record.log2_root_to_second_moment_scale_gap > 290


def test_report_proves_kernel_without_unlocking_speedup() -> None:
    report = run_all_unequal_conditioned_kernel()
    assert report.claim_gate["conditioned_character_kernel_proved"]
    assert report.claim_gate[
        "all_order_conditioned_word_map_reduction_proved"
    ]
    assert report.claim_gate["all_unequal_frame_half_norm_bound_proved"]
    assert not report.claim_gate[
        "simultaneous_k_coordinate_contraction_proved"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]
