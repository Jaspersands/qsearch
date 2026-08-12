from __future__ import annotations

import numpy as np

from self_dual_wreath_physical_pgm_intertwiner import _branch_representation_rows
from self_dual_wreath_physical_orientation_interference import (
    orientation_subspace_transform,
)
from self_dual_wreath_joint_character_correlation_decoder import (
    _partial_trace_character,
    _partial_trace_group,
    _permutations,
    audit_joint_character_correlation,
    joint_character_scaling_record,
    joint_character_state,
    left_covariant_state,
    run_joint_character_correlation_decoder,
)
from self_dual_wreath_orientation_fourier_reduction import (
    _w4_collision_free_labels,
)


THRESHOLD_LABELS = (
    ((3,), (2, 1)),
    ((3,), (1, 1, 1)),
    ((2, 1), (1, 1, 1)),
)


def test_direct_joint_states_obey_left_regular_covariance() -> None:
    permutations = _permutations(3)
    identity = tuple(range(3))
    base = joint_character_state(THRESHOLD_LABELS, identity)
    for hidden in permutations:
        direct = joint_character_state(THRESHOLD_LABELS, hidden)
        predicted = left_covariant_state(base, permutations, hidden, 8)
        assert np.allclose(direct, predicted, atol=1e-10)


def test_each_marginal_is_label_independent_but_joint_state_is_not() -> None:
    permutations = _permutations(3)
    identity = tuple(range(3))
    base = joint_character_state(THRESHOLD_LABELS, identity)
    reference_group = _partial_trace_character(base, 6, 8)
    reference_character = _partial_trace_group(base, 6, 8)
    joint_variations = []
    for hidden in permutations:
        state = joint_character_state(THRESHOLD_LABELS, hidden)
        assert np.allclose(
            _partial_trace_character(state, 6, 8),
            reference_group,
            atol=1e-10,
        )
        assert np.allclose(
            _partial_trace_group(state, 6, 8),
            reference_character,
            atol=1e-10,
        )
        joint_variations.append(np.linalg.norm(state - base, ord=2))
    assert max(joint_variations) > 0.4


def test_operator_gram_state_matches_literal_carrier_partial_trace() -> None:
    labels = THRESHOLD_LABELS
    rows = _branch_representation_rows(labels)
    permutations = tuple(permutation for permutation, _ in rows)
    matrices = dict(rows)
    group_order = len(permutations)
    character_count = 1 << len(labels)
    physical_dimension = len(next(iter(matrices.values())))
    carrier_dimension = physical_dimension // character_count
    walsh, _, _ = orientation_subspace_transform(3, (1, 2, 4))
    walsh = np.kron(walsh, np.eye(carrier_dimension))
    source = np.vstack(
        [np.eye(carrier_dimension) for _ in range(character_count)]
    ) / np.sqrt(character_count)
    hidden = permutations[-1]
    hidden_source = matrices[hidden] @ source
    stinespring = np.stack(
        [
            walsh @ matrices[group].T.conj() @ hidden_source / np.sqrt(group_order)
            for group in permutations
        ]
    ).reshape(
        group_order,
        character_count,
        carrier_dimension,
        carrier_dimension,
    )
    literal_trace = np.einsum(
        "azcx,bwcx->azbw",
        stinespring,
        stinespring.conj(),
    ).reshape(group_order * character_count, group_order * character_count)
    literal_trace /= carrier_dimension
    predicted = joint_character_state(labels, hidden)
    assert np.allclose(literal_trace, predicted, atol=1e-10)
    np.testing.assert_allclose(
        np.trace(predicted),
        1.0,
        atol=1e-10,
    )


def test_information_threshold_control_has_substantial_correlation_signal() -> None:
    control = audit_joint_character_correlation(
        3,
        THRESHOLD_LABELS,
        control_id="threshold",
    )
    assert control.exact_joint_correlation_theorem_verified
    assert control.maximum_covariance_residual < 1e-9
    assert control.maximum_group_marginal_label_variation < 1e-9
    assert control.maximum_character_marginal_label_variation < 1e-9
    assert control.maximum_schur_factorization_residual < 1e-9
    assert control.holevo_information_fraction > 0.62
    assert control.joint_pretty_good_success > 0.58
    assert control.joint_pretty_good_success > control.optimal_right_correction_success
    assert control.maximum_character_offdiagonal_block_norm > 0


def test_s4_pair_retains_nonclassical_joint_information() -> None:
    control = audit_joint_character_correlation(
        4,
        _w4_collision_free_labels()[0],
        control_id="w4",
    )
    assert control.exact_joint_correlation_theorem_verified
    assert control.joint_holevo_information_bits > 0.28
    assert control.joint_pretty_good_success > control.random_guess_success
    assert control.joint_pretty_good_success < control.optimal_right_correction_success
    assert control.maximum_character_offdiagonal_block_norm > 0.1


def test_scaling_contract_keeps_implementation_gates_open() -> None:
    record = joint_character_scaling_record(128)
    assert record.row_copy_and_walsh_polynomial
    assert record.symmetric_group_qft_polynomial
    assert not record.branch_erasure_required
    assert not record.all_n_extensive_holevo_information_proved
    assert not record.multiplicity_operator_block_encoding_proved
    assert not record.polynomial_joint_decoder_proved


def test_report_records_positive_mechanism_without_speedup_claim() -> None:
    report = run_joint_character_correlation_decoder()
    assert report.headline_metrics["finite_control_count"] == 3
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics["finite_positive_holevo_control_count"] == 3
    assert report.claim_gate[
        "joint_group_character_state_is_hidden_label_dependent"
    ]
    assert report.claim_gate[
        "joint_correlations_contain_finite_hidden_label_information"
    ]
    assert not report.claim_gate["group_marginal_contains_hidden_label_information"]
    assert not report.claim_gate[
        "character_marginal_contains_hidden_label_information"
    ]
    assert not report.claim_gate["all_n_extensive_joint_information_proved"]
    assert not report.claim_gate["polynomial_joint_decoder_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
