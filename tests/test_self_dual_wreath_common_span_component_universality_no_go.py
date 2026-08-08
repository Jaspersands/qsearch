import math

import numpy as np
import pytest

from self_dual_wreath_common_span_component_universality_no_go import (
    audit_naimark_compression,
    audit_structured_common_span_counterfamily,
    canonical_common_span_effects,
    construct_structured_common_span_counterfamily,
    naimark_dilation,
    run_common_span_component_universality_no_go,
    structured_common_span_scaling_record,
)


def test_naimark_common_span_compression_realizes_arbitrary_commuting_spectrum() -> None:
    effects = (
        np.diag([0.3, 0.7]).astype(complex),
        np.diag([0.7, 0.3]).astype(complex),
    )
    isometry, projectors = naimark_dilation(effects)
    control = audit_naimark_compression("COMMUTING", effects)

    assert np.linalg.norm(isometry.conj().T @ isometry - np.eye(2)) < 1e-12
    for projector, effect in zip(projectors, effects):
        assert isometry.conj().T @ projector @ isometry == pytest.approx(effect)
    assert control.arbitrary_povm_compression_verified is True
    assert control.compressed_effect_algebra_commutative is True
    assert control.maximum_effect_commutator_norm == pytest.approx(0.0)


def test_naimark_common_span_compression_also_realizes_noncommuting_povm() -> None:
    trine = []
    for angle in (0.0, 2 * math.pi / 3, 4 * math.pi / 3):
        vector = np.asarray(
            [[1.0], [complex(math.cos(angle), math.sin(angle))]],
            dtype=complex,
        ) / math.sqrt(2)
        trine.append((2 / 3) * (vector @ vector.conj().T))
    control = audit_naimark_compression("TRINE", tuple(trine))

    assert control.arbitrary_povm_compression_verified is True
    assert control.compressed_effect_algebra_commutative is False
    assert control.maximum_effect_commutator_norm > 0.1


@pytest.mark.parametrize("part_count", [2, 3, 5, 8])
def test_structured_family_matches_coarse_data_but_components_commute(
    part_count: int,
) -> None:
    row = audit_structured_common_span_counterfamily(
        "CONTROL",
        part_count,
        part_size=5,
        alpha=1 / 3,
    )

    assert row.exact_common_span_counterfamily_verified is True
    assert row.distinct_leaf_projectors is True
    assert row.common_span_relative_rank == pytest.approx(1 / 3)
    assert row.total_leaf_rank_to_common_aspect == pytest.approx(4.0)
    assert row.maximum_leaf_rank_to_common_ratio == pytest.approx(
        4 / (5 * part_count)
    )
    assert row.observed_first_frame_condition_number < 4.0
    assert row.minimum_positive_component_eigenvalue == pytest.approx(1 / 3)
    assert row.maximum_component_eigenvalue == pytest.approx(2 / 3)
    assert row.distance_to_nearest_reciprocal_integer == pytest.approx(1 / 6)
    assert row.maximum_component_commutator_norm < 1e-12
    assert row.observed_nonscalarity_defect_edge == pytest.approx(
        5 / 9 - 1 / (5 * part_count)
    )


def test_equation_one_reconstructs_nonreciprocal_commuting_components() -> None:
    frame, leaves, common, target = construct_structured_common_span_counterfamily(
        3,
        5,
        alpha=1 / 3,
    )
    observed = canonical_common_span_effects(frame, leaves, common)

    for actual, expected in zip(observed, target):
        assert actual == pytest.approx(expected)
    assert np.linalg.norm(sum(observed) - np.eye(15), ord=2) < 1e-12
    assert max(
        np.linalg.norm(left @ right - right @ left, ord=2)
        for left in observed
        for right in observed
    ) < 1e-12


def test_scaling_preserves_every_coarse_obstruction() -> None:
    row = structured_common_span_scaling_record(96)

    assert row.common_span_dimension == 480
    assert row.first_child_ambient_dimension == 1440
    assert row.common_span_relative_rank == pytest.approx(1 / 3)
    assert row.maximum_leaf_rank_to_common_ratio == pytest.approx(1 / 120)
    assert row.first_frame_condition_number < 4
    assert row.cross_part_leaf_pair_fraction > 0.99
    assert row.cross_leaf_commutator_norm > 1 / 241
    assert row.cross_leaf_commutator_norm < 1 / 240
    assert row.component_positive_edge == pytest.approx(1 / 3)
    assert row.nonscalarity_defect_edge > 0.55
    assert row.component_effects_commute is True


def test_report_closes_spectral_shortcut_and_keeps_natural_gate_open() -> None:
    report = run_common_span_component_universality_no_go()

    assert report.status == (
        "generic-common-span-rigidity-falsified-"
        "direct-natural-commutator-analysis-required"
    )
    assert report.headline_metrics["common_span_povm_universality_theorem_count"] == 1
    assert report.headline_metrics[
        "all_coarse_data_commuting_component_counterfamily_count"
    ] == 1
    assert report.headline_metrics["naimark_control_failure_count"] == 0
    assert report.headline_metrics["structured_control_failure_count"] == 0
    assert report.claim_gate["arbitrary_povm_common_span_compression_proved"] is True
    assert report.claim_gate[
        "nonreciprocal_compressed_effect_spectrum_implies_noncommutativity"
    ] is False
    assert report.claim_gate[
        "natural_compressed_component_commutator_mass_proved"
    ] is False
    assert report.claim_gate["speedup_claim_allowed"] is False
