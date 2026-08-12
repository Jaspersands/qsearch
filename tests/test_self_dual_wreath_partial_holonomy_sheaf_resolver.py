from __future__ import annotations

import numpy as np
import pytest

from self_dual_wreath_partial_holonomy_sheaf_resolver import (
    PartialTransportEdge,
    _flat_tree,
    _partial_triangle,
    audit_partial_sheaf_resolver,
    kernel_basis,
    partial_connection_incidence,
    partial_sheaf_scaling_record,
    rank_one_partial_edge,
    run_partial_holonomy_sheaf_resolver,
)


def test_rank_one_transport_satisfies_partial_isometry_identities() -> None:
    edge = rank_one_partial_edge(
        0,
        1,
        np.asarray([1.0, 1.0j]),
        np.asarray([1.0j, -1.0]),
    )
    initial = edge.transport.conj().T @ edge.transport
    final = edge.transport @ edge.transport.conj().T

    assert np.linalg.norm(initial @ initial - initial) < 1e-12
    assert np.linalg.norm(final @ final - final) < 1e-12
    assert np.linalg.matrix_rank(initial, tol=1e-9) == 1
    assert np.linalg.matrix_rank(final, tol=1e-9) == 1


def test_flat_unitary_tree_recovers_scalar_component_effects() -> None:
    control = audit_partial_sheaf_resolver("FLAT", 3, _flat_tree())

    assert control.exact_sheaf_kernel_reduction_verified
    assert control.section_space_dimension == 2
    assert control.component_effects_pairwise_commute
    assert control.normalized_component_m4 == pytest.approx(0, abs=1e-12)


@pytest.mark.parametrize("seed", [5, 17])
def test_partial_triangle_has_noncommuting_coordinate_effects(seed: int) -> None:
    control = audit_partial_sheaf_resolver(
        f"PARTIAL-{seed}",
        3,
        _partial_triangle(seed),
    )

    assert control.exact_sheaf_kernel_reduction_verified
    assert control.section_space_dimension == 3
    assert not control.component_effects_pairwise_commute
    assert control.maximum_component_commutator_norm > 0
    assert control.normalized_component_m4 > 0


def test_sparse_incidence_norm_is_bounded_by_maximum_degree() -> None:
    control = audit_partial_sheaf_resolver("NORM", 3, _partial_triangle(29))

    assert control.maximum_graph_degree == 2
    assert control.incidence_operator_norm <= control.sparse_degree_norm_upper_bound


def test_kernel_basis_equals_laplacian_zero_space() -> None:
    incidence, _, _ = partial_connection_incidence(3, _partial_triangle(31))
    basis = kernel_basis(incidence)
    laplacian = incidence.conj().T @ incidence

    assert np.linalg.norm(incidence @ basis) < 1e-10
    assert np.linalg.norm(laplacian @ basis) < 1e-10
    assert np.linalg.norm(basis.conj().T @ basis - np.eye(basis.shape[1])) < 1e-10


def test_non_partial_edge_is_rejected() -> None:
    bad = PartialTransportEdge(0, 1, np.diag([1.0, 0.5]).astype(complex))
    with pytest.raises(ValueError):
        partial_connection_incidence(2, (bad,))


def test_scaling_record_keeps_all_natural_gates_open() -> None:
    row = partial_sheaf_scaling_record(32)

    assert row.pair_gpe_partial_transport_per_edge_polynomial
    assert not row.polynomial_coherent_edge_select_proved
    assert not row.exact_natural_dependency_kernel_coverage_proved
    assert not row.inverse_polynomial_sheaf_gap_proved
    assert not row.endpoint_intertwiner_polar_proved
    assert not row.natural_component_povm_compiled


def test_report_defines_architecture_without_promoting_it_to_algorithm() -> None:
    report = run_partial_holonomy_sheaf_resolver()

    assert report.headline_metrics["partial_sheaf_kernel_normal_form_theorem_count"] == 1
    assert report.headline_metrics["finite_partial_noncommuting_control_count"] == 2
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["partial_sheaf_resolver_normal_form_proved"]
    assert report.claim_gate["partial_connections_can_have_noncommuting_component_effects"]
    assert not report.claim_gate["natural_sparse_coherent_edge_select_proved"]
    assert not report.claim_gate["natural_exact_dependency_kernel_coverage_proved"]
    assert not report.claim_gate["natural_component_povm_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]
