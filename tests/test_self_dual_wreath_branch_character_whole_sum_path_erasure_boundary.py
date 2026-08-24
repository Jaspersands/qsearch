import math

import numpy as np

from self_dual_wreath_branch_character_whole_sum_path_erasure_boundary import (
    audit_orthogonal_range_classifier,
    audit_whole_sum_path_identity,
    run_whole_sum_path_erasure_boundary,
    uniform_path_coisometry,
    whole_sum_path_scaling_record,
)


def test_uniform_path_coisometry_is_normalized():
    path = uniform_path_coisometry(5, 3)
    assert path.shape == (15, 75)
    assert np.linalg.norm(path @ path.conj().T - np.eye(15), ord=2) < 1e-12


def test_single_pair_whole_sum_dilation_has_exact_projected_block():
    control = audit_whole_sum_path_identity(
        "single",
        (((3,), (2, 1)),),
    )
    assert control.exact_whole_sum_path_identity_verified
    assert control.group_order == 6
    assert control.dilation_isometry_residual < 1e-9
    assert control.path_projection_block_residual < 1e-9


def test_threshold_whole_sum_dilation_preserves_singular_scale():
    control = audit_whole_sum_path_identity(
        "threshold",
        (
            ((3,), (2, 1)),
            ((3,), (1, 1, 1)),
            ((2, 1), (1, 1, 1)),
        ),
    )
    assert control.exact_whole_sum_path_identity_verified
    assert control.source_pair_count == 3
    assert control.singular_scale_identity_residual < 1e-9
    assert math.isclose(
        control.projected_maximum_singular_value,
        control.convolution_maximum_singular_value / math.sqrt(6),
        rel_tol=1e-9,
    )


def test_near_isometric_convolution_still_has_inverse_sqrt_group_path_amplitude():
    control = audit_whole_sum_path_identity(
        "threshold",
        (
            ((3,), (2, 1)),
            ((3,), (1, 1, 1)),
            ((2, 1), (1, 1, 1)),
        ),
    )
    assert control.maximum_principal_amplitude < control.convolution_maximum_singular_value
    assert control.maximum_principal_amplitude <= 1 / math.sqrt(2)


def test_orthogonal_range_classifier_erases_path_without_amplification():
    control = audit_orthogonal_range_classifier(4, 2)
    assert control.exact_classifier_bypass_verified
    assert control.maximum_cross_range_overlap < 1e-12
    assert control.coherent_classifier_path_erasure_residual < 1e-9
    assert math.isclose(control.generic_uniform_path_amplitude, 0.5)


def test_natural_scaling_rejects_generic_path_unpreparation():
    row = whole_sum_path_scaling_record(64)
    assert row.generic_path_unpreparation_superpolynomial
    assert row.log2_canonical_reflection_query_lower_bound > row.polynomial_benchmark_log2
    assert not row.coherent_range_classifier_compiled


def test_report_preserves_classifier_escape_and_speedup_gate():
    report = run_whole_sum_path_erasure_boundary()
    assert report.theorem.theorem_verified
    assert report.claim_gate["complete_quadrant_sum_explicit_path_dilation_compiled"]
    assert report.claim_gate["generic_reflection_path_unpreparation_superpolynomial"]
    assert report.claim_gate["coherent_range_classifier_is_sufficient"]
    assert not report.claim_gate["natural_wreath_range_classifier_compiled"]
    assert not report.claim_gate["arbitrary_whole_sum_circuit_lower_bound_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
