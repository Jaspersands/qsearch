import math

import numpy as np
import pytest

from self_dual_wreath_leaf_whitening_commutator_no_go import (
    audit_commuting_whitening_counterfamily,
    commuting_whitening_scaling_record,
    construct_commuting_whitening_counterfamily,
    run_leaf_whitening_commutator_no_go,
    verify_diagonal_commuting_projection_frame_certificate,
)


@pytest.mark.parametrize("part_count", [2, 3, 5, 8])
def test_duplicate_free_counterfamily_whitens_to_commuting_effects(
    part_count: int,
) -> None:
    row = audit_commuting_whitening_counterfamily(
        "CONTROL",
        part_count,
        part_size=5,
        leaf_rank=2,
    )

    assert row.exact_counterfamily_verified is True
    assert row.distinct_leaf_projectors is True
    assert row.total_rank_aspect == pytest.approx(2.0)
    assert row.observed_frame_condition_number < 3.0
    assert row.maximum_canonical_effect_commutator_norm < 1e-12
    assert row.observed_cross_leaf_principal_cosine == pytest.approx(
        2 / (5 * part_count)
    )
    assert row.observed_cross_leaf_commutator_norm == pytest.approx(
        row.predicted_cross_leaf_commutator_norm
    )
    assert row.observed_nonscalarity_defect_edge == pytest.approx(
        1 / 2 - 1 / (5 * part_count)
    )


def test_diagonal_certificate_is_exact_and_detects_forbidden_support_edge() -> None:
    frame, effects, _, _ = construct_commuting_whitening_counterfamily(3, 5, 2)
    certificate = verify_diagonal_commuting_projection_frame_certificate(
        frame,
        effects,
    )

    assert certificate["certificate_verified"] is True
    assert certificate["integer_frame_diagonal_residual"] == pytest.approx(0.0)
    assert certificate["reciprocal_spectrum_residual"] == pytest.approx(0.0)
    assert certificate["independent_set_residual"] == pytest.approx(0.0)

    invalid_frame = frame.copy()
    invalid_frame[0, 1] = invalid_frame[1, 0] = 0.1
    invalid = verify_diagonal_commuting_projection_frame_certificate(
        invalid_frame,
        effects,
    )
    assert invalid["certificate_verified"] is False
    assert invalid["independent_set_residual"] > 0
    assert invalid["projection_equation_residual"] > 0


def test_scaling_has_density_one_leaf_noncommutativity_but_commuting_whitening() -> None:
    row = commuting_whitening_scaling_record(
        96,
        part_size=5,
        leaf_rank=2,
    )

    assert row.fiber_dimension == 480
    assert row.total_rank_aspect == pytest.approx(2.0)
    assert row.relative_leaf_rank == pytest.approx(1 / 240)
    assert row.frame_condition_number < 2.02
    assert row.cross_part_pair_fraction > 0.99
    expected_cosine = 1 / 240
    assert row.cross_leaf_commutator_norm == pytest.approx(
        expected_cosine * math.sqrt(1 - expected_cosine**2)
    )
    assert row.density_one_leaf_noncommutativity is True
    assert row.canonical_effects_pairwise_commute is True


def test_commuting_effect_spectrum_is_reciprocal_integer() -> None:
    _, effects, _, _ = construct_commuting_whitening_counterfamily(3, 7, 3)

    positive_values = []
    for effect in effects:
        positive_values.extend(
            value for value in np.linalg.eigvalsh(effect) if value > 1e-12
        )
    assert positive_values
    assert all(value == pytest.approx(1 / 3) for value in positive_values)


def test_report_scopes_spectral_criterion_to_full_support() -> None:
    report = run_leaf_whitening_commutator_no_go()

    assert report.status == (
        "generic-full-support-leaf-transfer-falsified-"
        "compressed-component-analysis-open"
    )
    assert report.headline_metrics[
        "duplicate_free_bounded_condition_counterfamily_count"
    ] == 1
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate[
        "nonreciprocal_full_support_effect_eigenvalue_is_exact_noncommutativity_witness"
    ] is True
    assert report.claim_gate[
        "full_support_integer_cover_applies_after_common_span_compression"
    ] is False
    assert report.claim_gate[
        "natural_canonical_component_effect_algebra_noncommutative_on_positive_mass"
    ] is False
    assert report.claim_gate["speedup_claim_allowed"] is False
