import math
from fractions import Fraction

from self_dual_wreath_sibling_frame_jacobi_surrogate import (
    ADAPTIVE_GAP_FLOOR,
    adaptive_copy_record,
    audit_gaussian_projection_reduction,
    effective_jacobi_parameter,
    jacobi_aspect_record,
    jacobi_fractional_edges,
    run_sibling_frame_jacobi_surrogate,
)


def test_rank_deficient_and_full_rank_edges_use_correct_parameters() -> None:
    lower, upper = jacobi_fractional_edges(0.625)
    assert math.isclose(lower, 0.1)
    assert math.isclose(upper, 0.9)
    assert math.isclose(effective_jacobi_parameter(0.625), 2.5)

    threshold_lower, threshold_upper = jacobi_fractional_edges(0.75)
    extra_lower, extra_upper = jacobi_fractional_edges(1.5)
    assert math.isclose(threshold_lower, ADAPTIVE_GAP_FLOOR)
    assert math.isclose(extra_lower, ADAPTIVE_GAP_FLOOR)
    assert math.isclose(threshold_upper, 1.0 - ADAPTIVE_GAP_FLOOR)
    assert math.isclose(extra_upper, 1.0 - ADAPTIVE_GAP_FLOOR)


def test_atom_masses_and_hard_edge_are_explicit() -> None:
    singular = jacobi_aspect_record(0.625)
    assert math.isclose(singular.zero_atom_mass, 0.375)
    assert math.isclose(singular.one_atom_mass, 0.375)
    assert math.isclose(singular.fractional_mass, 0.25)
    assert singular.regime == "rank-deficient-complement-jacobi"

    hard = jacobi_aspect_record(1.0)
    assert hard.hard_edge
    assert hard.fractional_support_lower == 0.0
    assert hard.fractional_support_upper == 1.0


def test_finite_gaussian_row_projection_and_complement_reductions() -> None:
    singular = audit_gaussian_projection_reduction(48, 30, seed=101)
    full = audit_gaussian_projection_reduction(40, 60, seed=103)

    assert singular.observed_zero_multiplicity == 18
    assert singular.observed_one_multiplicity == 18
    assert singular.observed_fractional_multiplicity == 12
    assert singular.row_projection_spectrum_residual < 1e-10
    assert singular.complement_fractional_spectrum_residual is not None
    assert singular.complement_fractional_spectrum_residual < 1e-10
    assert singular.exact_projection_reduction_verified

    assert full.observed_zero_multiplicity == 0
    assert full.observed_one_multiplicity == 0
    assert full.observed_fractional_multiplicity == 40
    assert full.row_projection_spectrum_residual < 1e-10
    assert full.complement_fractional_spectrum_residual is None
    assert full.exact_projection_reduction_verified


def test_adaptive_schedule_uses_at_most_one_copy_and_has_uniform_gap() -> None:
    for n in range(3, 101):
        row = adaptive_copy_record(n)
        threshold = Fraction(row.threshold_child_aspect_exact)
        selected = Fraction(row.selected_child_aspect_exact)

        assert Fraction(1, 2) <= threshold < 1
        assert row.extra_copy_count in (0, 1)
        assert row.selected_copy_count == (
            row.information_threshold_copy_count + row.extra_copy_count
        )
        assert selected <= Fraction(3, 4) or selected >= Fraction(3, 2)
        assert row.hard_edge_avoided
        assert row.selected_endpoint_gap + 1e-14 >= ADAPTIVE_GAP_FLOOR
        assert row.uniform_gap_bound_verified
        assert not row.natural_frame_jacobi_transfer_proved


def test_report_proves_only_the_surrogate_and_blocks_natural_overclaim() -> None:
    report = run_sibling_frame_jacobi_surrogate()

    assert report.headline_metrics[
        "projection_reduction_control_failure_count"
    ] == 0
    assert report.headline_metrics["adaptive_scaling_failure_count"] == 0
    assert report.claim_gate["finite_gaussian_projection_reduction_proved"]
    assert report.claim_gate["gaussian_fractional_jacobi_support_proved"]
    assert report.claim_gate[
        "adaptive_at_most_one_extra_copy_surrogate_gap_proved"
    ]
    assert not report.claim_gate[
        "natural_sibling_frames_joint_jacobi_law_proved"
    ]
    assert not report.claim_gate[
        "globally_distinct_natural_spectral_edge_proved"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]
