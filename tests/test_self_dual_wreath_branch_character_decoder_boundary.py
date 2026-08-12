from __future__ import annotations

import itertools
import math

import numpy as np
import pytest

from representation_obstruction import integer_partitions
from self_dual_wreath_branch_character_decoder_boundary import (
    audit_branch_character_channel,
    branch_character_distribution_from_cycle_type,
    branch_character_scaling_record,
    direct_branch_character_distribution,
    partition_number,
    run_branch_character_decoder_boundary,
)
from self_dual_wreath_character_moments import permutation_cycle_type
from self_dual_wreath_orientation_fourier_reduction import (
    _w4_collision_free_labels,
)


def test_identity_relative_permutation_has_only_trivial_character() -> None:
    labels = (
        ((3,), (2, 1)),
        ((3,), (1, 1, 1)),
        ((2, 1), (1, 1, 1)),
    )
    probabilities = branch_character_distribution_from_cycle_type(
        labels,
        (1, 1, 1),
    )
    assert probabilities[0] == pytest.approx(1.0)
    assert np.max(np.abs(probabilities[1:])) < 1e-12


@pytest.mark.parametrize(
    "n,labels",
    [
        (3, (((3,), (2, 1)),)),
        (
            3,
            (
                ((3,), (2, 1)),
                ((3,), (1, 1, 1)),
                ((2, 1), (1, 1, 1)),
            ),
        ),
        (4, _w4_collision_free_labels()[0]),
    ],
)
def test_product_character_law_matches_explicit_kraus_matrices(
    n: int,
    labels: tuple[tuple[tuple[int, ...], tuple[int, ...]], ...],
) -> None:
    for permutation in itertools.permutations(range(n)):
        direct = direct_branch_character_distribution(labels, permutation)
        predicted = branch_character_distribution_from_cycle_type(
            labels,
            permutation_cycle_type(permutation),
        )
        assert np.allclose(direct, predicted, atol=1e-11)
        assert np.sum(direct) == pytest.approx(1.0)
        assert np.min(direct) >= -1e-12


def test_same_cycle_type_permutations_have_identical_character_law() -> None:
    labels = _w4_collision_free_labels()[0]
    grouped: dict[tuple[int, ...], list[np.ndarray]] = {}
    for permutation in itertools.permutations(range(4)):
        grouped.setdefault(permutation_cycle_type(permutation), []).append(
            direct_branch_character_distribution(labels, permutation)
        )
    assert set(grouped) == set(integer_partitions(4))
    for rows in grouped.values():
        assert all(np.allclose(rows[0], row, atol=1e-11) for row in rows[1:])


def test_optimal_right_correction_obeys_conjugacy_class_ceiling() -> None:
    controls = [
        audit_branch_character_channel(
            3,
            (((3,), (2, 1)),),
            control_id="single",
        ),
        audit_branch_character_channel(
            4,
            _w4_collision_free_labels()[0],
            control_id="pair",
        ),
    ]
    for control in controls:
        assert control.exact_character_channel_verified
        assert control.correction_decoder_bound_verified
        assert control.optimal_character_correction_success <= (
            control.conjugacy_class_success_ceiling + 1e-12
        )
        assert control.passive_group_guess_success == pytest.approx(
            1 / math.factorial(control.n)
        )


def test_partition_counter_and_factorial_scaling_are_exact() -> None:
    assert [partition_number(n) for n in range(1, 11)] == [
        1,
        2,
        3,
        5,
        7,
        11,
        15,
        22,
        30,
        42,
    ]
    record = branch_character_scaling_record(128)
    assert record.character_correction_superpolynomially_suppressed
    assert record.amplitude_amplification_query_log2_lower_bound > 0
    assert not record.carrier_dependent_coherent_decoder_ruled_out


def test_report_closes_only_the_right_correction_architecture() -> None:
    report = run_branch_character_decoder_boundary()
    assert report.headline_metrics["finite_control_count"] == 3
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate[
        "native_branch_character_probability_factorization_proved"
    ]
    assert report.claim_gate[
        "character_controlled_right_correction_factorially_suppressed"
    ]
    assert not report.claim_gate[
        "arbitrary_character_controlled_commutant_unitary_ruled_out"
    ]
    assert not report.claim_gate["carrier_dependent_joint_decoder_ruled_out"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_invalid_equal_or_wrong_degree_labels_are_rejected() -> None:
    with pytest.raises(ValueError, match="unequal partition pairs"):
        branch_character_distribution_from_cycle_type(
            (((3,), (3,)),),
            (1, 1, 1),
        )
    with pytest.raises(ValueError, match="unequal partition pairs"):
        branch_character_distribution_from_cycle_type(
            (((2,), (1, 1)),),
            (1, 1, 1),
        )
