from fractions import Fraction

import numpy as np
import pytest

from self_dual_wreath_orientation_laplacian_gap import (
    _commuting_controls,
    _star_controls,
    audit_star_law_control,
    dense_core_workload,
    graph_algebraic_connectivity,
    live_pair_cores,
    run_orientation_laplacian_gap,
    sample_transport_uniformity,
    screen_laplacian_floor,
    star_law_spectrum,
)


D5_LABELS = (
    ((6,), (2, 2, 2)),
    ((5, 1), (4, 1, 1)),
    ((4, 2), (3, 1, 1, 1)),
    ((3, 3), (1, 1, 1, 1, 1, 1)),
)
NONCOMMUTING_LABELS = (
    ((6,), (4, 2)),
    ((5, 1), (2, 2, 2)),
    ((3, 3), (2, 1, 1, 1, 1)),
    ((2, 2, 1, 1), (1, 1, 1, 1, 1, 1)),
)


def test_complete_graph_connectivity_is_the_vertex_count() -> None:
    single = graph_algebraic_connectivity(((0, 1),))
    square = graph_algebraic_connectivity(
        ((0, 2), (0, 3), (1, 2), (1, 3))
    )
    star = graph_algebraic_connectivity(((0, 1), (0, 2), (0, 3)))

    assert single == pytest.approx(2.0)
    assert square == pytest.approx(2.0)
    # a star subgraph is exactly the trap the module warns about
    assert star == pytest.approx(1.0)


def test_p_star_low_eigenvalue_does_not_move_with_width() -> None:
    gamma = Fraction(1, 11)
    lows = []
    highs = []
    for edges in (2, 3, 8, 1024):
        low, high = star_law_spectrum(gamma, edges)
        lows.append(low)
        highs.append(high)

    assert lows == pytest.approx([2 - 1 / 11] * 4)
    assert highs[-1] > highs[0]
    with pytest.raises(ValueError):
        star_law_spectrum(gamma, 1)
    with pytest.raises(ValueError):
        star_law_spectrum(Fraction(3, 2), 3)


def test_noncommuting_s6_counterexample_matches_the_star_law() -> None:
    control = audit_star_law_control(
        "W6-NONCOMMUTING-THREE-STAR-CARRIER-9",
        (6,),
        NONCOMMUTING_LABELS,
        ((2, 12), (5, 12), (11, 12)),
    )

    assert control.shared_vertex == 12
    assert control.star_edge_count == 3
    assert Fraction(
        control.residual_correlation_numerator,
        control.residual_correlation_denominator,
    ) == Fraction(1, 9)
    assert control.observed_minimum_positive_eigenvalue == pytest.approx(17 / 9)
    assert control.observed_maximum_eigenvalue == pytest.approx(20 / 9)
    assert control.maximum_residual < 1e-12
    assert control.low_eigenvalue_is_width_independent
    assert control.verified


def test_d5_plane_two_star_matches_the_star_law() -> None:
    control = audit_star_law_control(
        "W6-D5-TWO-STAR-CARRIER-5",
        (6,),
        D5_LABELS,
        ((0, 14), (7, 14)),
    )

    assert control.observed_minimum_positive_eigenvalue == pytest.approx(9 / 5)
    assert control.observed_maximum_eigenvalue == pytest.approx(11 / 5)
    assert control.verified


def test_star_law_needs_a_single_shared_vertex() -> None:
    with pytest.raises(ValueError):
        audit_star_law_control(
            "BAD-STAR",
            (6,),
            D5_LABELS,
            ((0, 14), (3, 7)),
        )


def test_commuting_atoms_split_into_affine_complete_graphs() -> None:
    controls = _commuting_controls()

    assert len(controls) == 2
    for control in controls:
        assert control.projectors_commute
        # the module's own commuting threshold is 100 * 1e-8
        assert control.maximum_pair_commutator_norm < 1e-6
        assert control.every_atom_support_is_affine
        assert control.prediction_residual < 1e-8
        assert control.observed_minimum_positive_eigenvalue == pytest.approx(2.0)
        assert control.predicted_minimum_positive_eigenvalue >= 2.0 - 1e-9
        assert control.verified


def test_dense_workload_matches_ambient_times_total_rank() -> None:
    edges = live_pair_cores((6,), D5_LABELS, (0, 7, 3, 14))
    workload = dense_core_workload((6,), D5_LABELS, edges)

    assert edges
    assert workload > 0
    # 1 * 5 * 50 * 90 * 5 ambient times the summed live core ranks
    assert workload % 112_500 == 0


def test_full_graph_screen_never_violates_the_width_independent_floor() -> None:
    screen = screen_laplacian_floor(6, 4, 200_000, 24)

    assert screen.audited_control_count == 24
    assert screen.floor_violation_count == 0
    assert screen.worst_floor_slack >= -1e-9
    assert screen.minimum_observed_positive_eigenvalue >= 1.0


def test_natural_residual_correlation_uniformity_collapses() -> None:
    early = sample_transport_uniformity(9, sample_count=16)
    late = sample_transport_uniformity(12, sample_count=16)

    assert late.distinct_off_common_correlation_count <= (
        early.distinct_off_common_correlation_count
    )
    assert late.matches_minimal_irrep_reciprocal
    assert late.maximum_off_common_correlation == pytest.approx(1 / 11)
    assert late.uniform_transport_floor == pytest.approx(2 - 2 / 11)
    assert late.sign_blind_floor < 0
    assert late.uniform_transport_floor > late.sign_blind_floor


def test_report_proves_the_floor_and_keeps_trivialization_open() -> None:
    report = run_orientation_laplacian_gap(
        sampled_degrees=(9, 12),
        uniformity_sample_count=8,
        screen_control_cap=12,
    )

    assert report.claim_gate["dirichlet_form_verified"]
    assert report.claim_gate["commuting_atom_splitting_proved"]
    assert report.claim_gate["exact_p_star_spectrum_proved"]
    assert report.claim_gate["width_independent_floor_respected_on_all_screens"]
    assert not report.claim_gate["vertex_trivialization_proved"]
    assert not report.claim_gate["all_depth_conditioning_proved"]
    assert not report.claim_gate["grading_defect_bounded"]
    assert not report.claim_gate["speedup_claim_allowed"]
    assert report.headline_metrics["screened_floor_violation_count"] == 0
    assert report.headline_metrics["star_law_failure_count"] == 0
    assert report.headline_metrics["new_quantum_algorithm_count"] == 0
    assert all(
        row["floor_is_width_independent"]
        and not row["vertex_trivialization_proved"]
        for row in report.scaling_records
    )
    assert all(
        row["uniform_transport_floor"] > row["sign_blind_floor"]
        for row in report.scaling_records
    )
