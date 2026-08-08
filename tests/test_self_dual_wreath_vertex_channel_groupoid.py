import pytest

from self_dual_wreath_vertex_channel_groupoid import (
    run_vertex_channel_groupoid,
    simplex_groupoid_failure,
)


@pytest.mark.parametrize("width", [3, 4, 5, 8, 12])
def test_simplex_is_partial_isometric_but_path_frustrated(width: int) -> None:
    record = simplex_groupoid_failure(width)

    assert record.normalized_pair_map == -1
    assert record.partial_isometry_residual == 0
    assert record.support_projection_commutator_norm == 0
    assert record.path_composition_residual == 2
    assert record.triangle_holonomy == -1
    assert record.normalized_gram_minimum_eigenvalue == 2 - width
    assert record.path_law_is_essential


def test_natural_w6_controls_form_flat_clique_groupoids() -> None:
    report = run_vertex_channel_groupoid()

    assert report.headline_metrics[
        "natural_finite_groupoid_control_failure_count"
    ] == 0
    assert report.headline_metrics[
        "natural_finite_psd_certification_failure_count"
    ] == 0
    assert report.headline_metrics[
        "maximum_natural_path_composition_residual"
    ] < 1e-12
    assert report.headline_metrics[
        "maximum_natural_triangle_holonomy_residual"
    ] < 1e-12
    assert report.headline_metrics[
        "maximum_natural_integer_spectrum_residual"
    ] < 1e-12

    spectra = {
        row.control_id: row.normalized_gram_distinct_eigenvalues
        for row in report.natural_finite_controls
    }
    assert spectra["W6-CARRIER-9-THREE-EDGE-GROUPOID"] == (
        0.0,
        1.0,
        3.0,
    )
    assert spectra["W6-CARRIER-5-FULL-LIVE-FIVE-EDGE-GROUPOID"] == (
        -0.0,
        1.0,
        3.0,
    )


def test_report_keeps_all_depth_and_speedup_gates_closed() -> None:
    report = run_vertex_channel_groupoid()

    assert report.claim_gate[
        "flat_groupoid_suffices_for_vertex_trivialization"
    ]
    assert report.claim_gate["clique_atom_gram_decomposition_proved"]
    assert report.claim_gate["selected_natural_finite_groupoids_verified"]
    assert not report.claim_gate["partial_isometries_alone_sufficient"]
    assert not report.claim_gate["commuting_supports_alone_sufficient"]
    assert not report.claim_gate[
        "all_depth_natural_carrier_groupoid_proved"
    ]
    assert not report.claim_gate[
        "unconditional_width_independent_laplacian_floor_proved"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]
