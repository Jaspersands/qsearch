import json

import numpy as np

from self_dual_wreath_orientation_fixed_space_recoupling import (
    audit_global_fixed_space_recoupling,
    audit_local_fixed_space,
    fixed_space_compiler_scaling_record,
    run_fixed_space_recoupling,
    symmetric_pair_basis,
    tensor_flip,
    write_fixed_space_recoupling_report,
)


def test_symmetric_and_exterior_pair_bases_have_correct_swap_charge() -> None:
    dimension = 4
    flip = tensor_flip(dimension, dimension)
    symmetric = symmetric_pair_basis(dimension, 1)
    exterior = symmetric_pair_basis(dimension, -1)
    assert symmetric.shape == (16, 10)
    assert exterior.shape == (16, 6)
    assert np.linalg.norm(symmetric.T @ symmetric - np.eye(10), ord=2) < 1e-12
    assert np.linalg.norm(exterior.T @ exterior - np.eye(6), ord=2) < 1e-12
    assert np.linalg.norm(flip @ symmetric - symmetric, ord=2) < 1e-12
    assert np.linalg.norm(flip @ exterior + exterior, ord=2) < 1e-12


def test_unequal_wreath_fixed_space_and_selected_restriction_are_exact() -> None:
    control = audit_local_fixed_space((3, 1), (2, 2), None)
    assert control.wreath_carrier_dimension == 12
    assert control.branch_fixed_dimension == 6
    assert control.selected_restriction_dimension == 12
    assert control.maximum_compressed_selected_action_residual < 1e-12
    assert control.exact_local_fixed_space_formula_verified


def test_equal_extension_signs_give_symmetric_and_exterior_dimensions() -> None:
    plus = audit_local_fixed_space((3, 1), (3, 1), 1)
    minus = audit_local_fixed_space((3, 1), (3, 1), -1)
    assert plus.branch_fixed_dimension == 6
    assert minus.branch_fixed_dimension == 3
    assert plus.exact_local_fixed_space_formula_verified
    assert minus.exact_local_fixed_space_formula_verified


def test_global_fixed_space_kernel_is_matrix_valued_inside_one_outer_block() -> None:
    control = audit_global_fixed_space_recoupling(
        "S3-MIXED",
        (2, 1),
        (
            ((3,), (2, 1), None),
            ((2, 1), (2, 1), 1),
        ),
    )
    assert control.branch_fixed_dimension == 12
    assert control.diagonal_fixed_dimension == 6
    assert control.occupied_overlap_rank == 6
    assert control.distinct_positive_principal_cosine_squared_count == 3
    assert abs(control.minimum_positive_principal_cosine_squared - 0.25) < 1e-12
    assert abs(control.maximum_positive_principal_cosine_squared - 0.5) < 1e-12
    assert control.matrix_cs_block_non_scalar
    assert control.exact_global_fixed_space_formula_verified


def test_scaling_keeps_recent_semisimple_qft_and_global_compiler_gates_false() -> None:
    record = fixed_space_compiler_scaling_record(8)
    assert record.local_branch_fixed_basis_polynomial
    assert record.diagonal_fixed_projector_gpe_polynomial
    assert record.pair_gpe_carrier_reassociation_polynomial
    assert record.native_occupied_rank_threshold_log2 > 60
    assert record.high_occupied_rank_native_regular_master_mass_lower_bound > 0.999999
    assert record.arbitrary_plancherel_irrep_factors_present
    assert record.diagram_order_lower_bound == record.copy_count + 1
    assert not record.published_semisimple_qft_unitary_regime_verified
    assert not record.matrix_cs_polar_compiled


def test_report_preserves_global_matrix_polar_claim_boundary() -> None:
    report = run_fixed_space_recoupling()
    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics["matrix_valued_global_control_count"] == 2
    assert report.claim_gate["branch_fixed_space_local_basis_compiled"]
    assert report.claim_gate[
        "diagonal_fixed_space_many_way_kronecker_formula_proved"
    ]
    assert not report.claim_gate[
        "pair_gpe_automatically_compiles_global_matrix_cs_polar"
    ]
    assert not report.claim_gate[
        "published_semisimple_algebra_qft_applies_in_natural_regime"
    ]
    assert not report.claim_gate["normalization_one_global_matrix_cs_polar_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_report_writer_records_fixed_space_artifact(tmp_path) -> None:
    path = tmp_path / "fixed_space.json"
    payload = write_fixed_space_recoupling_report(path)
    stored = json.loads(path.read_text())
    assert stored["status"] == payload["status"]
    assert stored["status"] == "fixed-spaces-explicit-global-kronecker-cs-polar-open"
    assert stored["headline_metrics"]["local_control_count"] == 6
    assert stored["headline_metrics"]["global_control_count"] == 2
    assert stored["headline_metrics"]["global_matrix_cs_polar_compiler_count"] == 0
    assert not stored["claim_gate"]["speedup_claim_allowed"]
