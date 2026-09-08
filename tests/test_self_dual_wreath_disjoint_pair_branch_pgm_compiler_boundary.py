from pathlib import Path

from self_dual_wreath_disjoint_pair_branch_pgm_compiler_boundary import (
    audit_disjoint_pair_source_compiler,
    audit_natural_disjoint_pair_compiler,
    perfect_matching_count,
    residual_coupling_scaling_record,
    run_disjoint_pair_branch_pgm_compiler_boundary,
    write_disjoint_pair_branch_pgm_compiler_boundary_report,
)


def test_shared_hidden_label_covariance_breaks_pair_local_factorization() -> None:
    control = audit_disjoint_pair_source_compiler(
        5,
        2,
        (1, 1),
        (1, 1),
    )
    assert control.hidden_involution_count == 15
    assert abs(control.total_joint_branch_probability - 1.0) <= 1e-10
    assert control.maximum_covariance_identity_residual <= 1e-10
    assert control.weighted_frame_covariance_fraction > 0.38
    assert control.global_branch_pgm_bayes_success > 0.50
    assert control.pair_local_pgm_map_bayes_success < 0.31
    assert control.global_advantage_over_pair_local_map > 0.19
    assert control.nonzero_shared_label_covariance_verified is True
    assert control.global_pgm_differs_from_pair_local_map_verified is True
    assert control.exact_control_verified is True


def test_scaled_same_label_product_effects_are_not_a_povm() -> None:
    control = audit_disjoint_pair_source_compiler(
        5,
        2,
        (0, 1),
        (0, 1),
    )
    assert control.weighted_scaled_diagonal_completeness_residual > 0.99
    assert control.maximum_scaled_diagonal_eigenvalue_excess > 0.99
    assert control.weighted_global_effect_factorization_residual > 0.16
    assert control.scaled_diagonal_product_fails_povm_verified is True


def test_natural_s3_s4_pair_local_map_is_strictly_weaker() -> None:
    s3, s3_controls = audit_natural_disjoint_pair_compiler(3, 1)
    s4, s4_controls = audit_natural_disjoint_pair_compiler(4, 2)
    assert len(s3_controls) == 9
    assert len(s4_controls) == 225
    for aggregate in (s3, s4):
        assert abs(aggregate.total_natural_source_probability - 1.0) <= 1e-10
        assert aggregate.natural_global_advantage_over_pair_local_map > 0
        assert aggregate.source_mass_with_nonzero_covariance > 0.5
        assert (
            aggregate.source_mass_where_scaled_diagonal_product_fails_povm
            > 0.5
        )
        assert aggregate.all_controls_verified is True
    assert s3.natural_global_advantage_over_pair_local_map > 0.13
    assert s4.natural_global_advantage_over_pair_local_map > 0.008


def test_logarithmic_disjoint_depth_leaves_a_growing_shared_label_frame() -> None:
    assert perfect_matching_count(8) == 105
    records = [residual_coupling_scaling_record(n) for n in (8, 16, 32, 64)]
    assert all(
        record.conditioned_state_tensor_factorization_proved for record in records
    )
    assert all(
        record.hypothesis_average_tensor_factorization_proved is False
        for record in records
    )
    assert all(record.bounded_residual_block_count_proved is False for record in records)
    assert all(
        later.residual_shared_hidden_label_block_count
        > earlier.residual_shared_hidden_label_block_count
        for earlier, later in zip(records[:-1], records[1:], strict=True)
    )


def test_report_keeps_covariance_aware_compiler_and_speedup_blocked() -> None:
    report = run_disjoint_pair_branch_pgm_compiler_boundary()
    assert report.theorem.conditioned_state_factorization_proved is True
    assert report.theorem.shared_label_covariance_identity_proved is True
    assert report.theorem.naive_pair_local_branch_pgm_compiler_falsified is True
    assert report.theorem.pair_local_pgm_equals_global_branch_pgm is False
    assert report.theorem.scaled_diagonal_product_is_povm is False
    assert report.claim_gate["covariance_aware_branch_pgm_compiled"] is False
    assert report.claim_gate["hidden_involution_decoder_compiled"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False


def test_writer_emits_artifact_without_registry(tmp_path: Path) -> None:
    output = tmp_path / "disjoint-pair-compiler-boundary.json"
    payload = write_disjoint_pair_branch_pgm_compiler_boundary_report(
        output,
        write_registry=False,
    )
    assert output.exists()
    assert payload["status"] == (
        "naive-pair-local-pgm-falsified-covariance-aware-polar-open"
    )
    assert (
        payload["headline_metrics"][
            "naive_pair_local_branch_pgm_compiler_no_go_count"
        ]
        == 1
    )
