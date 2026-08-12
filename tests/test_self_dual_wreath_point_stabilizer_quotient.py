from __future__ import annotations

import math

import numpy as np
import pytest

from representation_obstruction import hook_length_dimension, integer_partitions
from self_dual_wreath_joint_character_correlation_decoder import (
    _permutations,
    joint_character_state,
    left_covariant_state,
)
from self_dual_wreath_point_stabilizer_quotient import (
    audit_natural_point_signal,
    audit_point_quotient,
    fixed_tuple_overlap_kernel,
    natural_annealed_overlap_kernel,
    point_centered_gram,
    point_quotient_states,
    removable_children,
    run_point_stabilizer_quotient,
    share_young_child,
    stabilizer_chain_reduction_record,
    young_edge_scaling_record,
)


THRESHOLD_LABELS = (
    ((3,), (2, 1)),
    ((3,), (1, 1, 1)),
    ((2, 1), (1, 1, 1)),
)


def test_young_children_and_shared_child_rule() -> None:
    assert removable_children((4, 2, 1)) == ((3, 2, 1), (4, 1, 1), (4, 2))
    assert share_young_child((3,), (2, 1))
    assert share_young_child((2, 1), (1, 1, 1))
    assert not share_young_child((3,), (1, 1, 1))
    with pytest.raises(ValueError, match="positive"):
        removable_children((2, 0))


def test_point_quotient_is_covariant_and_centered_gram_is_standard() -> None:
    states = point_quotient_states(THRESHOLD_LABELS)
    permutations = _permutations(3)
    for hidden in permutations:
        for image, state in enumerate(states):
            transformed = left_covariant_state(state, permutations, hidden, 8)
            assert np.allclose(transformed, states[hidden[image]], atol=1e-10)
    gram = point_centered_gram(states)
    diagonal = gram[0, 0]
    expected = np.full((3, 3), -diagonal / 2)
    np.fill_diagonal(expected, diagonal)
    assert np.allclose(gram, expected, atol=1e-10)
    assert np.linalg.matrix_rank(gram, tol=1e-10) == 2


def test_fixed_tuple_relative_overlap_formula_matches_direct_states() -> None:
    labels = THRESHOLD_LABELS
    permutations = _permutations(3)
    base = joint_character_state(labels, tuple(range(3)))
    predicted = fixed_tuple_overlap_kernel(3, labels)
    observed_by_class: dict[tuple[int, ...], list[float]] = {}
    from self_dual_wreath_character_moments import permutation_cycle_type

    for hidden in permutations:
        state = left_covariant_state(base, permutations, hidden, 8)
        overlap = float(np.einsum("ij,ji->", base, state).real)
        cycle = permutation_cycle_type(hidden)
        observed_by_class.setdefault(cycle, []).append(overlap)
        assert overlap == pytest.approx(predicted[cycle], abs=1e-10)
    assert all(max(values) - min(values) < 1e-10 for values in observed_by_class.values())


def test_plancherel_overlap_formula_reduces_to_known_native_purity() -> None:
    from self_dual_wreath_joint_character_purity_decoupling import (
        natural_annealed_joint_purity,
    )

    for copies in (1, 2, 3):
        kernel = natural_annealed_overlap_kernel(3, copies)
        purity, _ = natural_annealed_joint_purity(3, copies)
        assert kernel[(1, 1, 1)] == pytest.approx(purity, abs=1e-12)


def test_plancherel_overlap_formula_matches_exhaustive_character_average() -> None:
    partitions = tuple(integer_partitions(3))
    order = math.factorial(3)
    weights = {
        partition: hook_length_dimension(partition) ** 2 / order
        for partition in partitions
    }
    exhaustive = {cycle: 0.0 for cycle in partitions}
    for left in partitions:
        for right in partitions:
            probability = weights[left] * weights[right]
            kernel = fixed_tuple_overlap_kernel(3, ((left, right),))
            for cycle, value in kernel.items():
                exhaustive[cycle] += probability * value
    predicted = natural_annealed_overlap_kernel(3, 1)
    assert exhaustive == pytest.approx(predicted, abs=1e-12)


def test_natural_point_signal_is_exact_standard_character_coefficient() -> None:
    normalized = []
    for n in range(3, 7):
        control = audit_natural_point_signal(n)
        assert control.nonnegative_signal_verified
        assert control.subgroup_average_standard_coefficient_residual < 1e-12
        assert control.expected_point_state_purity >= control.expected_average_state_purity
        assert control.expected_centered_hilbert_schmidt_norm_squared > 0
        assert not control.collision_free_conditioned_signal_formula_proved
        assert not control.asymptotic_inverse_polynomial_signal_proved
        normalized.append(control.normalized_expected_centered_signal)
    assert all(left > right for left, right in zip(normalized, normalized[1:]))
    assert normalized[-1] < 0.011


def test_finite_point_controls_reject_standard_fourier_sector_shortcut() -> None:
    control = audit_point_quotient(
        3,
        THRESHOLD_LABELS,
        control_id="threshold",
    )
    assert control.exact_point_quotient_theorem_verified
    assert control.centered_state_span_rank == 2
    assert control.centered_gram_isotropy_residual < 1e-10
    assert control.maximum_forbidden_young_block_norm < 1e-10
    assert control.active_nonstandard_young_irrep_pair_count > 0
    assert control.point_pretty_good_success > 0.58
    assert control.covariance_error_law_residual < 1e-10


def test_s4_point_control_has_real_but_weak_signal() -> None:
    control = audit_point_quotient(
        4,
        (((4,), (3, 1)), ((2, 2), (2, 1, 1))),
        control_id="w4",
    )
    assert control.exact_point_quotient_theorem_verified
    assert control.point_pretty_good_success > 0.27
    assert control.point_pretty_good_success < 0.28
    assert control.random_guess_success == 0.25
    assert control.point_holevo_information_bits > 0.06
    assert control.maximum_forbidden_young_block_norm < 1e-9


def test_young_edge_scaling_is_local_but_does_not_claim_whitening() -> None:
    records = [young_edge_scaling_record(n) for n in (8, 12, 16)]
    for record in records:
        assert record.allowed_ordered_irrep_pair_count < record.total_ordered_irrep_pair_count
        assert record.maximum_allowed_neighbor_count <= (
            record.maximum_removable_corner_count
            * record.maximum_addable_parent_count
        )
        assert record.local_young_edge_navigation_polynomial
        assert not record.simultaneous_multiplicity_whitening_proved


def test_stabilizer_chain_reduction_keeps_physical_hypotheses_explicit() -> None:
    record = stabilizer_chain_reduction_record(128)
    assert record.stabilizer_stage_count == 127
    assert record.inverse_polynomial_point_excess_suffices
    assert record.recursive_full_recovery_reduction_proved
    assert record.fresh_subgroup_native_blocks_required
    assert record.public_oracle_restriction_required
    assert not record.inverse_polynomial_natural_point_excess_proved
    assert not record.efficient_point_measurement_proved
    assert not record.polynomial_full_hidden_shift_algorithm_proved


def test_report_records_reduction_without_speedup_claim() -> None:
    report = run_point_stabilizer_quotient()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["point_quotient_isotropic_standard_geometry_proved"]
    assert report.claim_gate["point_quotient_young_edge_locality_proved"]
    assert not report.claim_gate["point_signal_confined_to_standard_fourier_irrep"]
    assert report.claim_gate["exact_natural_point_signal_formula_proved"]
    assert not report.claim_gate[
        "collision_free_conditioned_point_signal_formula_proved"
    ]
    assert report.claim_gate[
        "conditional_stabilizer_chain_recovery_reduction_proved"
    ]
    assert not report.claim_gate["inverse_polynomial_natural_point_signal_proved"]
    assert not report.claim_gate["efficient_point_measurement_proved"]
    assert not report.claim_gate["polynomial_full_hidden_shift_decoder_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
