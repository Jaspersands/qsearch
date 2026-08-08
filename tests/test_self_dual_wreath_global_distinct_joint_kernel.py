from fractions import Fraction

import pytest

from self_dual_wreath_character_moments import (
    projector_word_character_sum,
    unequal_pair_descriptor,
)
from self_dual_wreath_all_unequal_conditioned_kernel import (
    conditioned_word_factor,
)
from self_dual_wreath_global_collision_free_mass import plancherel_weights
from self_dual_wreath_global_distinct_joint_kernel import (
    conditioning_total_variation,
    conditioning_tv_bounds,
    direct_global_distinct_joint_word_factor,
    direct_injective_plancherel_transform,
    injective_plancherel_transform,
    pair_factor_from_components,
    run_global_distinct_joint_kernel,
    structured_global_distinct_joint_word_factor,
    unequal_word_components,
)
from representation_obstruction import integer_partitions


def test_injective_subset_dp_matches_direct_assignment_exactly() -> None:
    weights = plancherel_weights(4)
    features = (
        tuple(Fraction(index - 1) for index in range(len(weights))),
        tuple(Fraction(index + 2, 3) for index in range(len(weights))),
        tuple(Fraction((-1) ** index) for index in range(len(weights))),
    )

    assert injective_plancherel_transform(
        weights,
        features,
    ) == direct_injective_plancherel_transform(weights, features)


def test_word_rank_one_components_reconstruct_every_unequal_pair() -> None:
    n = 4
    sequence = ((0, 1, 2, 3), (1, 0, 3, 2))
    components = unequal_word_components(n, sequence)
    partitions = integer_partitions(n)

    for left_index, left in enumerate(partitions):
        for right_index, right in enumerate(partitions):
            if left_index == right_index:
                continue
            descriptor = unequal_pair_descriptor(left, right)
            direct = Fraction(
                projector_word_character_sum(descriptor, sequence),
                descriptor.dimension * (1 << len(sequence)),
            )
            assert pair_factor_from_components(
                components,
                left_index,
                right_index,
            ) == direct


@pytest.mark.parametrize(
    "n,sequence",
    [
        (4, ((0, 1, 2, 3), (1, 0, 3, 2))),
        (5, ((0, 1, 2, 3, 4), (0, 2, 1, 4, 3))),
    ],
)
def test_structured_global_joint_word_kernel_matches_direct_and_does_not_factor(
    n: int,
    sequence: tuple[tuple[int, ...], ...],
) -> None:
    sequences = (sequence, sequence)
    structured = structured_global_distinct_joint_word_factor(n, sequences)
    direct = direct_global_distinct_joint_word_factor(n, sequences)

    assert structured == direct
    assert structured > 0
    assert structured != conditioned_word_factor(n, sequence) ** 2


@pytest.mark.parametrize("n,copy_count", [(4, 2), (5, 2), (5, 3)])
def test_conditioning_total_variation_satisfies_exact_cross_collision_bounds(
    n: int,
    copy_count: int,
) -> None:
    distance = conditioning_total_variation(n, copy_count)
    lower, upper = conditioning_tv_bounds(n, copy_count)

    assert 0 < distance <= 1
    assert lower <= distance <= upper


def test_report_exposes_injective_kernel_and_rejects_generic_transfer() -> None:
    report = run_global_distinct_joint_kernel()

    assert report.claim_gate["injective_plancherel_transform_proved"]
    assert report.claim_gate[
        "global_distinct_joint_character_kernel_proved"
    ]
    assert report.claim_gate["global_distinct_joint_word_kernel_proved"]
    assert not report.claim_gate["globally_distinct_source_law_factorizes"]
    assert report.claim_gate[
        "conditioning_distance_scale_separation_proved"
    ]
    assert not report.claim_gate[
        "independent_all_unequal_kernel_transfer_sufficient"
    ]
    assert not report.claim_gate[
        "uniform_collision_free_signed_contraction_proved"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]
