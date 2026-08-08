from functools import lru_cache

import pytest

from self_dual_wreath_partial_support_child_embedding import (
    run_partial_support_child_embedding,
)


@lru_cache(maxsize=1)
def _report():
    return run_partial_support_child_embedding()


def test_w3_retains_scalar_flat_affine_positive_control() -> None:
    control = _report().controls[0]
    assert control.exact_gram_reconstruction_verified
    assert control.active_support_is_affine
    assert control.scalar_flat_affine_child_embedding_certificate
    assert not control.matrix_partial_support_required
    assert control.maximum_component_full_fiber_scalar_residual < 1e-8


def test_collision_free_s6_falsifies_scalar_affine_fibers() -> None:
    control = _report().controls[1]
    assert control.globally_distinct_source_partitions
    assert control.active_support_is_affine
    assert control.active_orientation_masks == (2, 5, 11, 12)
    assert control.common_span_dimension == 34
    assert control.exact_gram_reconstruction_verified
    assert not control.scalar_flat_affine_child_embedding_certificate
    assert control.matrix_partial_support_required
    assert control.maximum_component_full_fiber_scalar_residual > 0.7
    assert control.maximum_cross_child_effect_commutator_norm == pytest.approx(
        1 / 356,
        abs=1e-10,
    )


def test_s6_partial_support_effects_and_endpoint_spectrum_are_exact() -> None:
    control = _report().controls[1]
    effects = {
        (row.side, row.orientation_mask): row for row in control.component_effects
    }
    assert effects[("left", 2)].support_rank == 9
    assert effects[("left", 5)].support_rank == 25
    assert effects[("right", 11)].support_rank == 9
    assert effects[("right", 11)].minimum_positive_eigenvalue == pytest.approx(
        1 / 178,
        abs=1e-10,
    )
    assert effects[("right", 12)].support_rank == 34
    assert effects[("right", 12)].minimum_positive_eigenvalue == pytest.approx(
        177 / 178,
        abs=1e-10,
    )
    assert control.endpoint_left_weight_spectrum == (
        ("81/170", 9),
        ("1/2", 16),
        ("9/17", 9),
    )
    assert control.endpoint_right_weight_spectrum == (
        ("8/17", 9),
        ("1/2", 16),
        ("89/170", 9),
    )


def test_report_pivots_to_partial_support_without_algorithm_claim() -> None:
    report = _report()
    assert report.headline_metrics[
        "natural_collision_free_scalar_affine_falsifier_count"
    ] == 1
    assert report.claim_gate[
        "gram_only_normalized_child_embedding_reconstruction_proved"
    ]
    assert report.claim_gate["natural_s6_requires_matrix_partial_support"]
    assert report.claim_gate[
        "direct_s6_trivial_sign_mechanism_has_vanishing_natural_mass"
    ]
    assert not report.claim_gate[
        "collision_free_affine_support_suffices_for_scalar_fibers"
    ]
    assert not report.claim_gate["matrix_partial_support_gpe_compiler_proved"]
    assert not report.claim_gate[
        "positive_native_mass_partial_support_obstruction_proved"
    ]
    assert not report.claim_gate["recursive_orientation_polar_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
