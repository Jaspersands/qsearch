import json

from self_dual_wreath_point_parent_coherence_witness import (
    audit_parent_coherence,
    run_point_parent_coherence_witness,
    sign_twist_parent_coherence_record,
    write_point_parent_coherence_witness_report,
)


def test_parent_pinching_splits_point_energy_orthogonally() -> None:
    control = audit_parent_coherence(
        3,
        (
            ((3,), (2, 1)),
            ((3,), (1, 1, 1)),
            ((2, 1), (1, 1, 1)),
        ),
        control_id="TEST-W3-THRESHOLD",
    )
    assert control.exact_parent_coherence_decomposition_verified
    assert control.energy_pythagorean_residual < 1e-9
    assert abs(
        control.parent_dephased_energy_fraction
        + control.parent_offdiagonal_energy_fraction
        - 1
    ) < 1e-9


def test_zero_zero_collective_portfolio_is_entirely_parent_coherent() -> None:
    control = audit_parent_coherence(
        4,
        (((4,), (2, 2)), ((3, 1), (1, 1, 1, 1))),
        control_id="TEST-W4-ZERO-ZERO",
    )
    assert control.exact_parent_coherence_decomposition_verified
    assert control.parent_dephasing_erases_all_point_information
    assert control.parent_dephased_point_energy < 1e-12
    assert control.maximum_parent_dephased_point_state_variation < 1e-9
    assert abs(control.parent_offdiagonal_energy_fraction - 1) < 1e-9


def test_generic_collision_free_control_retains_both_energy_types() -> None:
    control = audit_parent_coherence(
        4,
        (((4,), (3, 1)), ((2, 2), (2, 1, 1))),
        control_id="TEST-W4-PAIR",
    )
    assert control.parent_dephased_point_energy > 0
    assert control.parent_offdiagonal_point_energy > 0
    assert not control.parent_dephasing_erases_all_point_information


def test_all_n_sign_twist_signal_is_offdiagonal_but_naturally_rare() -> None:
    for n in (6, 7, 8, 10, 16, 32, 64, 128):
        row = sign_twist_parent_coherence_record(n)
        assert row.pairwise_nonadjacent_sources
        assert row.exactly_two_distinct_parent_edges
        assert row.exact_parent_diagonal_energy == "0"
        assert row.exact_parent_offdiagonal_energy == row.exact_conditional_point_energy
        assert row.parent_dephasing_erases_conditional_point_signal
        assert row.inverse_polynomial_conditional_signal
        assert not row.inverse_polynomial_natural_source_admission
        assert not row.complete_mrs_transcript_separation_proved


def test_report_keeps_mrs_source_and_circuit_gates_closed() -> None:
    report = run_point_parent_coherence_witness()
    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["all_n_sign_twist_signal_entirely_parent_coherent"]
    assert not report.claim_gate["inverse_polynomial_natural_coherence_mass_proved"]
    assert not report.claim_gate["complete_mrs_transcript_povm_separation_proved"]
    assert not report.claim_gate["coherent_parent_recombination_filter_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_report_writer_emits_valid_json(tmp_path) -> None:
    path = tmp_path / "point_parent_coherence_witness.json"
    payload = write_point_parent_coherence_witness_report(path)
    parsed = json.loads(path.read_text())
    assert parsed["status"] == payload["status"]
    assert parsed["headline_metrics"] == payload["headline_metrics"]
