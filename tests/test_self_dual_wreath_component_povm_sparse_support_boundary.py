import pytest

from self_dual_wreath_component_povm_sparse_support_boundary import (
    audit_haar_component_povm,
    free_jacobi_fractional_edges,
    generic_component_atom_multiplicities,
    run_component_povm_sparse_support_boundary,
    sparse_outcome_jacobi_record,
)
from self_dual_wreath_sibling_frame_jacobi_surrogate import (
    jacobi_fractional_edges,
)


def test_generic_component_atom_multiplicities_cover_all_regimes() -> None:
    assert generic_component_atom_multiplicities(100, 60, 10) == (50, 0, 10)
    assert generic_component_atom_multiplicities(100, 60, 50) == (10, 10, 40)
    assert generic_component_atom_multiplicities(100, 30, 60) == (0, 0, 30)


def test_free_projection_edges_match_existing_equal_block_reduction() -> None:
    for sibling_aspect in (0.625, 0.75, 1.5, 2.0):
        fiber_aspect = 1.0 / (2.0 * sibling_aspect)
        observed = free_jacobi_fractional_edges(fiber_aspect, 0.5)
        expected = jacobi_fractional_edges(sibling_aspect)
        assert observed == pytest.approx(expected)


def test_finite_haar_coordinate_components_form_exact_povm_with_rank_atoms() -> None:
    control = audit_haar_component_povm(
        "test",
        48,
        30,
        (8, 8, 8, 8, 8, 8),
        seed=91,
    )
    assert control.exact_finite_projection_geometry_verified
    assert control.maximum_atom_multiplicity_error == 0
    assert control.effect_sum_identity_residual < 1e-12
    assert control.maximum_nonzero_spectrum_duality_residual < 1e-12
    assert all(row.observed_zero_multiplicity == 22 for row in control.component_effects)
    assert all(row.observed_one_multiplicity == 0 for row in control.component_effects)


def test_sparse_outcomes_have_small_trace_but_constant_positive_edge() -> None:
    coarse = sparse_outcome_jacobi_record(0.625, 64)
    fine = sparse_outcome_jacobi_record(0.625, 65536)
    assert fine.expected_effect_trace_fraction == pytest.approx(2**-16)
    assert fine.positive_support_rank_fraction_within_fiber < 2**-15
    assert fine.average_positive_eigenvalue == pytest.approx(0.625)
    assert fine.fractional_edge_lower > 0.61
    assert fine.maximum_edge_deviation_from_fiber_aspect < coarse.maximum_edge_deviation_from_fiber_aspect
    assert fine.small_trace_caused_by_low_rank_not_small_positive_edge


def test_report_redirects_bottleneck_without_promoting_natural_claim() -> None:
    report = run_component_povm_sparse_support_boundary()
    assert report.headline_metrics[
        "exact_component_projection_geometry_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "sparse_outcome_jacobi_limit_theorem_count"
    ] == 1
    assert not report.claim_gate["small_trace_implies_small_positive_effect_edge"]
    assert not report.claim_gate[
        "generic_square_root_qsvt_obstruction_applies_from_trace_alone"
    ]
    assert report.claim_gate["haar_sparse_outcome_effects_become_support_scalar"]
    assert not report.claim_gate["natural_component_effects_obey_haar_jacobi_law"]
    assert not report.claim_gate["natural_positive_effect_edge_proved"]
    assert not report.claim_gate["natural_component_support_select_compiled"]
    assert not report.claim_gate["recursive_orientation_polar_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
