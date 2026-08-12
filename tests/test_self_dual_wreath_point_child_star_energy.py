import json

from self_dual_wreath_point_child_star_energy import (
    audit_point_child_star_energy,
    point_child_star_energy_scaling_record,
    run_point_child_star_energy,
    write_point_child_star_energy_report,
)


def test_child_star_energy_matches_direct_centered_norm() -> None:
    control = audit_point_child_star_energy(
        3,
        (
            ((3,), (2, 1)),
            ((3,), (1, 1, 1)),
            ((2, 1), (1, 1, 1)),
        ),
        control_id="TEST-W3-THRESHOLD",
    )
    assert control.exact_child_star_energy_theorem_verified
    assert control.maximum_purification_gram_residual < 1e-9
    assert control.maximum_full_twirl_parent_block_residual < 1e-9
    assert control.centered_energy_decomposition_residual < 1e-9
    assert abs(control.direct_centered_energy - control.decomposed_centered_energy) < 1e-9


def test_collective_zero_zero_portfolio_has_positive_channel_witness() -> None:
    control = audit_point_child_star_energy(
        4,
        (((4,), (2, 2)), ((3, 1), (1, 1, 1, 1))),
        control_id="TEST-W4-ZERO-ZERO",
    )
    assert control.exact_child_star_energy_theorem_verified
    assert control.direct_centered_energy > 0
    assert control.strongest_witness_energy > 0
    assert any(
        row.active_offdiagonal_parent_block_count > 0
        for row in control.child_records
    )


def test_parent_pair_blocks_partition_every_child_energy() -> None:
    control = audit_point_child_star_energy(
        4,
        (((4,), (3, 1)), ((2, 2), (2, 1, 1))),
        control_id="TEST-W4-PAIR",
    )
    for row in control.child_records:
        assert abs(
            row.child_energy
            - row.diagonal_parent_energy
            - row.offdiagonal_parent_energy
        ) < 1e-9
        assert row.strongest_parent_block_energy <= row.child_energy + 1e-9


def test_scaling_record_does_not_promote_state_access_to_decoder() -> None:
    row = point_child_star_energy_scaling_record(64)
    assert row.native_purification_and_group_qft_polynomial
    assert not row.explicit_subgroup_element_average_required
    assert row.positive_channel_witness_extraction_formula_proved
    assert not row.dense_orientation_gram_materialization_polynomial
    assert not row.coherent_relative_scale_gram_access_proved
    assert not row.efficient_child_star_measurement_proved


def test_report_preserves_magnitude_and_access_gates() -> None:
    report = run_point_child_star_energy()
    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics["finite_offdiagonal_recoupling_witness_count"] > 0
    assert report.claim_gate["positive_child_star_energy_decomposition_proved"]
    assert not report.claim_gate["scalable_collective_witness_magnitude_proved"]
    assert not report.claim_gate["coherent_relative_scale_child_star_access_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_report_writer_emits_valid_json(tmp_path) -> None:
    path = tmp_path / "point_child_star_energy.json"
    payload = write_point_child_star_energy_report(path)
    parsed = json.loads(path.read_text())
    assert parsed["status"] == payload["status"]
    assert parsed["headline_metrics"] == payload["headline_metrics"]
