from functools import lru_cache

import pytest

from self_dual_wreath_affine_recoupling_bundle import (
    affine_basis,
    run_affine_recoupling_bundle,
)


@lru_cache(maxsize=1)
def _report():
    return run_affine_recoupling_bundle()


def test_affine_basis_recovers_plane_generators() -> None:
    origin, generators = affine_basis((0, 2, 5, 7), 3)

    assert origin == 0
    assert generators == (2, 5)


def test_label_simple_controls_are_exact_flat_affine_bundles() -> None:
    controls = _report().finite_controls[:3]

    assert all(row.affine_recoupling_bundle_certificate for row in controls)
    assert all(row.exact_flat_fiber_transport_verified for row in controls)
    assert all(row.maximum_transport_cocycle_residual < 1e-8 for row in controls)
    assert {row.active_support_affine_dimension for row in controls} == {1, 2}


def test_w3_requires_internal_transport_but_w5_anchor_line_does_not() -> None:
    w3, scaled_w3, w5 = _report().finite_controls[:3]

    assert not w3.simple_mask_relabeling_suffices
    assert not scaled_w3.simple_mask_relabeling_suffices
    assert w3.maximum_generator_fiber_map_difference == pytest.approx(2**0.5)
    assert scaled_w3.maximum_generator_fiber_map_difference == pytest.approx(
        3**0.5
    )
    assert w5.simple_mask_relabeling_suffices


def test_balanced_repeated_control_is_not_an_affine_bundle() -> None:
    report = _report()
    control = report.finite_controls[3]

    assert control.child_metric_equality_residual < 1e-8
    assert not control.coefficient_support_is_affine
    assert not control.exact_flat_fiber_transport_verified
    assert not control.affine_recoupling_bundle_certificate
    assert report.claim_gate["balanced_nonaffine_support_falsifier_present"]
    assert report.claim_gate[
        "selected_finite_generator_transports_compiled_by_gpe"
    ]
    assert report.claim_gate[
        "natural_collision_free_scalar_affine_falsifier_present"
    ]
    assert not report.claim_gate[
        "generator_transports_identified_as_racah_maps"
    ]
    assert not report.claim_gate[
        "polynomial_controlled_generator_transport_circuit_proved"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]
