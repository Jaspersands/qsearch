import math

import numpy as np
import pytest

from self_dual_wreath_matrix_povm_recursive_compiler import (
    _projective_components,
    _trine_components,
    audit_matrix_povm_normal_form,
    audit_recursive_matrix_povm_normal_form,
    run_matrix_povm_recursive_compiler,
    square_root_povm_degree_boundary,
)


def test_projective_partial_support_has_exact_povm_normal_form() -> None:
    control = audit_matrix_povm_normal_form(
        "projective",
        _projective_components(),
    )
    assert control.exact_matrix_povm_normal_form_verified
    assert control.component_effects_commute
    assert control.minimum_positive_effect_eigenvalue == 1.0
    assert control.maximum_component_polar_reconstruction_residual <= 1e-10


def test_noncommuting_trine_has_exact_povm_normal_form() -> None:
    control = audit_matrix_povm_normal_form("trine", _trine_components())
    assert control.exact_matrix_povm_normal_form_verified
    assert not control.component_effects_commute
    assert control.maximum_effect_commutator_norm > 0.1
    assert control.minimum_positive_effect_eigenvalue == pytest.approx(2 / 3)


def test_recursive_endpoint_and_child_povms_factor_exactly() -> None:
    angle = 0.37
    rotation = np.asarray(
        [
            [math.cos(angle), -math.sin(angle)],
            [math.sin(angle), math.cos(angle)],
        ],
        dtype=complex,
    )
    control = audit_recursive_matrix_povm_normal_form(
        "nested",
        _trine_components(),
        _projective_components(),
        np.diag([1.0, 5.0]).astype(complex),
        rotation @ np.diag([4.0, 1.5]) @ rotation.conj().T,
    )
    assert control.exact_nested_matrix_povm_compiler_normal_form_verified
    assert control.maximum_child_effect_commutator_norm > 0.1
    assert control.direct_recursive_relation_isometry_residual <= 1e-9
    assert control.nested_povm_factorization_residual <= 1e-9


def test_generic_square_root_degree_boundary_becomes_superpolynomial() -> None:
    rows = [square_root_povm_degree_boundary(size) for size in (64, 128, 256, 512)]
    assert all(
        right.markov_degree_lower_bound_log2
        > left.markov_degree_lower_bound_log2
        for left, right in zip(rows, rows[1:])
    )
    assert rows[-1].generic_block_encoding_degree_superpolynomial_signal
    assert not rows[-1].representation_specific_direct_dilation_proved


def test_report_keeps_natural_dilation_and_algorithm_gates_closed() -> None:
    report = run_matrix_povm_recursive_compiler()
    assert report.headline_metrics[
        "matrix_component_povm_normal_form_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "nested_recursive_povm_normal_form_theorem_count"
    ] == 1
    assert report.claim_gate[
        "noncommuting_component_effects_algebraically_supported"
    ]
    assert not report.claim_gate[
        "intrinsic_square_root_outcome_count_loss_required"
    ]
    assert report.claim_gate[
        "generic_square_root_block_encoding_can_be_superpolynomial"
    ]
    assert not report.claim_gate["natural_component_povm_dilation_compiled"]
    assert not report.claim_gate[
        "all_n_component_support_polars_gpe_compatible"
    ]
    assert not report.claim_gate[
        "high_dimension_partial_support_native_mass_controlled"
    ]
    assert not report.claim_gate["recursive_orientation_polar_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
