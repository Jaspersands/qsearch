from functools import lru_cache

import numpy as np
import pytest

from involution_character_arithmetic import (
    fixed_point_free_character, fixed_point_free_character_certificate,
    label_arithmetic_scaling_controls, two_copy_label_decision,
)
from representation_obstruction import conjugate_partition, hook_length_dimension, integer_partitions
from weak_fourier_signal import character_on_involution, removable_dominoes


@lru_cache(maxsize=None)
def exhaustive_domino_character(partition):
    if not partition:
        return 1
    return sum((-1 if height == 2 else 1) * exhaustive_domino_character(reduced)
               for reduced, height in removable_dominoes(partition))


def test_two_quotient_matches_independent_exhaustive_domino_recursion():
    for degree in range(0, 21, 2):
        for shape in integer_partitions(degree):
            certificate = fixed_point_free_character_certificate(shape)
            expected = exhaustive_domino_character(shape)
            assert certificate.character == expected, shape
            assert character_on_involution(shape, degree // 2) == expected
            assert certificate.two_core_empty == (expected != 0)
            assert abs(certificate.character) <= certificate.dimension
            assert fixed_point_free_character(conjugate_partition(shape)) == (-1)**(degree // 2) * expected


def test_nonempty_two_core_is_not_accidentally_promoted_to_signal():
    certificate = fixed_point_free_character_certificate((3, 2, 1))
    assert not certificate.two_core_empty
    assert certificate.character == 0
    assert certificate.quotient == ((), ())


def test_uniform_formula_does_not_call_the_recursive_path(monkeypatch):
    import weak_fourier_signal
    def forbidden(*args):
        raise AssertionError("domino path enumeration must not occur")
    monkeypatch.setattr(weak_fourier_signal, "removable_dominoes", forbidden)
    weak_fourier_signal.character_on_involution.cache_clear()
    assert weak_fourier_signal.character_on_involution((2048, 2048), 2048) == fixed_point_free_character((2048, 2048))
    controls = label_arithmetic_scaling_controls()
    assert [row["degree"] for row in controls] == [128, 512, 2048, 4096]
    assert all(row["absolute_ratio_at_most_one"] for row in controls)
    assert all(row["tableau_paths_enumerated"] == 0 for row in controls)
    assert not any(row["natural_source_coverage_claimed"] for row in controls)


def test_classical_score_attains_dense_two_copy_helstrom_without_joint_law_oracle():
    from coset_hidden_involution_binary_decision_reduction import (
        dense_binary_states, involution_conjugacy_class,
    )
    from self_dual_wreath_physical_frame_blocks import permutation_representation_matrices
    from coset_binary_carrier_instruments import _pair_gpe_instrument
    degree, order = 4, 24
    partitions = integer_partitions(degree)
    representations = {shape: dict(permutation_representation_matrices(shape)) for shape in partitions}
    hidden = involution_conjugacy_class(degree, 2)
    probability_gap = 0.0
    for left in partitions:
        for right in partitions:
            dimension = hook_length_dimension(left) * hook_length_dimension(right)
            null = dimension / order**2 * np.eye(dimension)
            alternative = sum(np.kron(np.eye(hook_length_dimension(left)) + representations[left][h],
                                      np.eye(hook_length_dimension(right)) + representations[right][h])
                              for h in hidden) * (dimension / (order**2 * len(hidden)))
            instrument = _pair_gpe_instrument(left, right)
            for target, projector in instrument.projectors.items():
                decision = two_copy_label_decision(left, right, target)
                mass_gap = float(np.trace(projector @ (alternative - null)).real)
                null_mass = float(np.trace(projector @ null).real)
                assert mass_gap == pytest.approx(null_mass * float(decision["likelihood_difference"]), abs=1e-12)
                if decision["accept_hidden_class"]:
                    probability_gap += mass_gap
                assert not decision["classical_sampler_for_joint_label_law_supplied"]
    null, alternative = dense_binary_states(degree, 2, 2)
    assert probability_gap == pytest.approx(np.abs(np.linalg.eigvalsh(alternative - null)).sum() / 2)


@pytest.mark.parametrize("shape", [(2, 1), (1, 2, 1), (2, 0), (True, 1), [2, 2], (2.0, 2)])
def test_bad_partitions_are_rejected(shape):
    with pytest.raises(ValueError):
        fixed_point_free_character_certificate(shape)


def test_label_degrees_and_ties_are_explicit():
    with pytest.raises(ValueError):
        two_copy_label_decision((4,), (2,), (4,))
    row = two_copy_label_decision((3, 2, 1), (3, 2, 1), (3, 2, 1))
    assert row["tie"] and not row["accept_hidden_class"]
    assert not row["constant_copy_algorithm_has_scalable_advantage"]
