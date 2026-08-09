import math

import numpy as np
import pytest

from self_dual_wreath_component_leaf_resolved_green_normal_form import (
    audit_leaf_resolved_green_normal_form,
    component_green_kernel,
    green_scaling_record,
    leaf_resolved_commutator_trace,
    run_component_leaf_resolved_green_normal_form,
)


def _trine_leaves() -> tuple[np.ndarray, ...]:
    leaves = []
    for angle in (0.0, 2 * math.pi / 3, 4 * math.pi / 3):
        vector = np.asarray(
            [[1.0], [complex(math.cos(angle), math.sin(angle))]],
            dtype=complex,
        ) / math.sqrt(2)
        leaves.append(vector @ vector.conj().T)
    return tuple(leaves)


def test_green_kernel_reconstructs_trine_component_effects() -> None:
    leaves = _trine_leaves()
    frame, green, effects = component_green_kernel(
        leaves,
        np.eye(2, dtype=complex),
    )

    assert frame == pytest.approx(1.5 * np.eye(2))
    assert green == pytest.approx((2 / 3) * np.eye(2))
    assert sum(effects) == pytest.approx(np.eye(2))
    for leaf, effect in zip(leaves, effects):
        assert effect == pytest.approx((2 / 3) * leaf)


def test_leaf_resolved_AABB_minus_ABAB_equals_direct_commutator_trace() -> None:
    leaves = _trine_leaves()
    _, green, effects = component_green_kernel(
        leaves,
        np.eye(2, dtype=complex),
    )
    direct = 0.0
    for left_index, left in enumerate(effects):
        for right in effects[left_index + 1 :]:
            commutator = left @ right - right @ left
            direct += np.trace(commutator.conj().T @ commutator).real

    resolved = leaf_resolved_commutator_trace(leaves, green)
    assert direct == pytest.approx(2 / 9)
    assert resolved == pytest.approx(direct)


def test_green_is_reflexive_inverse_and_whitened_projection() -> None:
    leaves = _trine_leaves()
    frame, green, _ = component_green_kernel(
        leaves,
        np.eye(2, dtype=complex),
    )
    values, vectors = np.linalg.eigh(frame)
    root = (vectors * np.sqrt(values)) @ vectors.conj().T
    whitened = root @ green @ root

    assert green @ frame @ green == pytest.approx(green)
    assert whitened @ whitened == pytest.approx(whitened)


@pytest.mark.parametrize("dimension", [2, 3, 4])
def test_complete_degree_four_word_identity_on_MUB_frames(dimension: int) -> None:
    computational = tuple(
        np.outer(vector, vector.conj())
        for vector in np.eye(dimension, dtype=complex).T
    )
    root = np.exp(2j * np.pi / dimension)
    fourier = np.asarray(
        [
            [root ** (row * column) / math.sqrt(dimension) for column in range(dimension)]
            for row in range(dimension)
        ],
        dtype=complex,
    )
    leaves = (*computational, *(np.outer(v, v.conj()) for v in fourier.T))
    row = audit_leaf_resolved_green_normal_form(
        "MUB",
        leaves,
        np.eye(dimension, dtype=complex),
    )

    assert row.exact_green_normal_form_verified is True
    assert row.maximum_leaf_word_trace_residual < 1e-10
    assert row.commutator_trace_residual < 1e-10
    assert row.direct_component_commutator_trace / dimension == pytest.approx(
        (1 - 1 / dimension) / 8
    )


def test_natural_scaling_keeps_group_to_leaf_prefactor_constant() -> None:
    group_order = math.factorial(32)
    threshold = (group_order - 1).bit_length()
    child_leaves = 1 << (threshold + 1)
    row = green_scaling_record(group_order, child_leaves)

    assert 0.25 < row.green_prefactor <= 0.5
    assert row.normalized_walk_scale == pytest.approx(row.green_prefactor)
    assert row.leaf_resolved_fourth_word_required is True
    assert row.aggregate_frame_words_sufficient is False
    assert row.natural_green_moment_bound_proved is False


def test_report_keeps_natural_leaf_marked_green_gap_open() -> None:
    report = run_component_leaf_resolved_green_normal_form()

    assert report.status == (
        "exact-leaf-resolved-green-target-derived-natural-gap-open"
    )
    assert report.headline_metrics[
        "leaf_resolved_green_word_normal_form_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "component_M4_green_AABB_minus_ABAB_identity_theorem_count"
    ] == 1
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["leaf_resolved_green_normal_form_proved"] is True
    assert report.claim_gate[
        "aggregate_sibling_words_suffice_for_component_M4"
    ] is False
    assert report.claim_gate["natural_leaf_marked_green_gap_positive"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False
