from functools import lru_cache

import pytest

from self_dual_wreath_pair_polar_transport_network import (
    pair_polar_transport_scaling_record,
    run_pair_polar_transport_network,
)


@lru_cache(maxsize=1)
def _report():
    return run_pair_polar_transport_network()


def test_w3_affine_fibers_have_exact_diameter_two_transport_networks() -> None:
    controls = _report().finite_controls[:2]

    assert all(row.transport_graph_connected for row in controls)
    assert all(row.transport_graph_diameter == 2 for row in controls)
    assert all(row.transport_graph_edge_count == 4 for row in controls)
    assert all(row.two_edge_pair_transport_count == 4 for row in controls)
    assert all(
        row.minimum_used_edge_principal_correlation == pytest.approx(0.5)
        for row in controls
    )
    assert all(row.exact_pair_polar_transport_network_verified for row in controls)


def test_w5_anchor_line_is_one_direct_common_range_edge() -> None:
    control = _report().finite_controls[2]

    assert control.active_orientation_masks == (3, 6)
    assert control.transport_graph_edge_count == 1
    assert control.transport_graph_diameter == 1
    assert control.minimum_used_edge_principal_correlation == pytest.approx(1.0)
    assert control.two_edge_pair_transport_count == 0
    assert control.exact_pair_polar_transport_network_verified


def test_asymptotic_pair_transport_correlation_gate_stays_open() -> None:
    small = pair_polar_transport_scaling_record(8)
    large = pair_polar_transport_scaling_record(512)

    assert large.smallest_possible_nonzero_pair_correlation_log2_lower_bound < (
        small.smallest_possible_nonzero_pair_correlation_log2_lower_bound
    )
    assert large.smallest_possible_nonzero_pair_correlation_can_be_exponential
    assert not large.inverse_polynomial_used_edge_correlation_proved
    assert large.gpe_direct_pair_polar_bypasses_edge_correlation
    assert not large.polynomial_transport_graph_diameter_proved
    assert not large.polynomial_coherent_path_finder_proved


def test_report_does_not_confuse_stacked_pair_conditioning_with_transport() -> None:
    report = _report()

    assert report.claim_gate["finite_affine_fiber_pair_transport_compiled"]
    assert report.claim_gate[
        "w3_orthogonal_generator_transport_resolved_by_two_edges"
    ]
    assert report.claim_gate["w5_anchor_transport_is_direct_common_range"]
    assert not report.claim_gate[
        "all_n_inverse_polynomial_used_edge_correlation_proved"
    ]
    assert report.claim_gate[
        "gpe_direct_pair_polar_bypasses_edge_correlation"
    ]
    assert not report.claim_gate[
        "all_n_polynomial_transport_graph_diameter_proved"
    ]
    assert not report.claim_gate["polynomial_coherent_path_finder_proved"]
    assert not report.claim_gate["hierarchical_orientation_polar_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
