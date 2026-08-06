from self_dual_wreath_common_core_cech_laplacian import (
    _controls,
    run_common_core_cech_laplacian,
)


def test_four_way_core_cech_boundaries_resolve_pair_cycles() -> None:
    control = _controls()[0]

    assert control.exact_finite_cech_laplacian_audit
    assert control.cech_complex_exact_in_positive_degrees
    assert control.pair_relation_kernel_dimension == 3
    assert control.triple_boundary_rank == 3
    assert control.emergent_pair_cycle_homology_dimension == 0
    assert control.maximum_boundary_composition_residual < 1e-10
    assert control.maximum_pair_boundary_annihilation_residual < 1e-10
    assert [record.homology_dimension for record in control.chain_groups] == [0, 0, 0]


def test_noncommuting_scalar_star_has_no_unexplained_pair_cycle() -> None:
    control = _controls()[1]

    assert control.maximum_pair_core_projector_commutator_norm > 0.1
    assert control.pair_relation_kernel_dimension == 0
    assert control.higher_common_core_count == 0
    assert control.emergent_pair_cycle_homology_dimension == 0
    assert control.minimum_positive_pair_laplacian_eigenvalue > 1.8
    assert control.maximum_pair_laplacian_eigenvalue < 2.3
    assert abs(control.exact_relative_grading_defect_norm - 1 / 17) < 1e-10


def test_cech_quotient_resolves_dense_sign_blind_failure() -> None:
    control = _controls()[2]

    assert not control.sign_blind_endpoint_gap_certified
    assert control.cech_complex_exact_in_positive_degrees
    assert control.pair_relation_kernel_dimension == 3
    assert control.triple_boundary_rank == 3
    assert abs(control.minimum_positive_pair_laplacian_eigenvalue - 2) < 1e-10
    assert abs(control.maximum_pair_laplacian_eigenvalue - 4) < 1e-10
    assert control.pair_laplacian_condition_number < 2.01
    assert control.exact_relative_grading_defect_norm < 1e-10


def test_eight_orientation_cube_keeps_pair_gap_but_not_half_balance() -> None:
    control = _controls()[3]

    assert control.cech_complex_exact_in_positive_degrees
    assert control.pair_core_count == 12
    assert control.pair_relation_kernel_dimension == 3
    assert control.triple_boundary_rank == 3
    assert control.emergent_pair_cycle_homology_dimension == 0
    assert control.minimum_positive_pair_laplacian_eigenvalue > 1.88
    assert control.maximum_pair_laplacian_eigenvalue < 4.01
    assert abs(control.exact_relative_grading_defect_norm - 1 / 17) < 1e-10
    assert not control.sign_blind_endpoint_gap_certified


def test_report_keeps_all_depth_exactness_and_transform_open() -> None:
    report = run_common_core_cech_laplacian()

    assert report.headline_metrics["finite_cech_laplacian_audit_failure_count"] == 0
    assert report.headline_metrics[
        "finite_emergent_pair_cycle_homology_dimension"
    ] == 0
    assert report.claim_gate["finite_relative_cech_complex_verified"]
    assert report.claim_gate["finite_pair_cycle_homology_vanishes"]
    assert not report.claim_gate["sign_blind_pair_graph_sufficient"]
    assert not report.claim_gate["all_n_relative_cech_exactness_proved"]
    assert not report.claim_gate["all_depth_phase_sensitive_laplacian_gap_proved"]
    assert not report.claim_gate["coherent_sparse_cech_transform_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]
