import json

from self_dual_wreath_gpe_fusion_tree_cs_boundary import (
    audit_fusion_tree_subblock,
    gpe_fusion_tree_scaling_record,
    run_gpe_fusion_tree_cs_boundary,
    write_gpe_fusion_tree_cs_boundary_report,
)


def test_pair_subblock_has_scalar_active_spectrum_but_is_not_isometric() -> None:
    control = audit_fusion_tree_subblock(
        "S3-PAIR",
        (2, 1),
        (((3,), (2, 1)),),
    )
    assert control.orientation_count == 2
    assert control.active_singular_value_count == 1
    assert control.distinct_active_singular_value_count == 1
    assert control.active_subblock_is_scalar_times_partial_isometry
    assert not control.active_subblock_already_partial_isometry
    assert abs(control.minimum_active_singular_value - 2**-0.5) < 1e-12


def test_first_higher_control_has_nonuniform_active_singular_values() -> None:
    control = audit_fusion_tree_subblock(
        "S3-TWO-PAIR",
        (2, 1),
        (
            ((3,), (2, 1)),
            ((2, 1), (1, 1, 1)),
        ),
    )
    assert control.orientation_count == 4
    assert control.active_singular_value_count == 5
    assert control.distinct_active_singular_value_count == 3
    assert not control.active_subblock_is_scalar_times_partial_isometry
    assert not control.active_subblock_already_partial_isometry
    assert abs(control.minimum_active_singular_value - 2**-1.5) < 1e-12
    assert abs(control.maximum_active_singular_value - (3 / 8) ** 0.5) < 1e-12


def test_exact_rectangular_subblock_polar_identity_is_verified() -> None:
    control = audit_fusion_tree_subblock(
        "S4-POLAR",
        (3, 1),
        (
            ((4,), (3, 1)),
            ((2, 2), (2, 1, 1)),
        ),
    )
    assert control.active_singular_value_count > 0
    assert control.exact_subblock_polar_identity_verified


def test_scaling_separates_tree_recoupling_from_global_cs_polar() -> None:
    record = gpe_fusion_tree_scaling_record(12)
    assert record.tensor_factor_count == 2 * record.copy_count + 1
    assert record.binary_fusion_internal_node_count == record.tensor_factor_count - 1
    assert record.gpe_call_count_for_tree_change_upper_bound == (
        2 * record.binary_fusion_internal_node_count
    )
    assert record.coherent_opaque_multiplicity_preserved
    assert record.full_tree_recoupling_unitary_polynomial
    assert record.generic_reflection_query_scale_log2 > 0
    assert record.direct_pair_reassociation_available
    assert not record.direct_global_rectangular_cs_polar_available


def test_report_records_gpe_capability_and_rectangular_cs_boundary() -> None:
    report = run_gpe_fusion_tree_cs_boundary()
    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics["scalar_direct_reassociation_control_count"] >= 1
    assert report.headline_metrics["matrix_valued_subblock_control_count"] >= 1
    assert report.claim_gate["recursive_gpe_fusion_tree_transform_polynomial"]
    assert report.claim_gate["full_gpe_tree_recoupling_unitary_polynomial"]
    assert report.claim_gate[
        "connected_fixed_space_overlap_is_rectangular_racah_subblock"
    ]
    assert not report.claim_gate[
        "full_recoupling_unitary_automatically_compiles_subblock_polar"
    ]


def test_report_has_no_fake_global_polar_or_speedup_claim() -> None:
    report = run_gpe_fusion_tree_cs_boundary()
    assert report.headline_metrics["direct_global_rectangular_cs_polar_compiler_count"] == 0
    assert report.headline_metrics["complete_orientation_polar_compiler_count"] == 0
    assert report.headline_metrics["new_quantum_algorithm_count"] == 0
    assert not report.claim_gate["direct_global_rectangular_cs_polar_compiled"]
    assert not report.claim_gate["complete_natural_orientation_polar_compiled"]
    assert not report.claim_gate["classical_separation_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
    assert report.status == (
        "gpe-fusion-trees-compile-recoupling-rectangular-cs-polar-open"
    )


def test_report_writer_records_the_boundary(tmp_path) -> None:
    path = tmp_path / "gpe_fusion_tree_cs_boundary.json"
    payload = write_gpe_fusion_tree_cs_boundary_report(path)
    stored = json.loads(path.read_text())
    assert stored["status"] == payload["status"]
    assert stored["headline_metrics"]["finite_control_count"] == 3
    assert stored["headline_metrics"]["rectangular_subblock_cs_boundary_theorem_count"] == 1
    assert stored["headline_metrics"]["direct_global_rectangular_cs_polar_compiler_count"] == 0
    assert not stored["claim_gate"]["speedup_claim_allowed"]
