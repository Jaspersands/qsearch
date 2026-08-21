from coset_hidden_involution_joint_primitive_ambient_lift_obstruction import (
    Schur_commutant_control,
    audit_primitive_offdiagonal,
    build_ambient_lift_report,
    write_ambient_lift_report,
)


def test_nonzero_Young_primitive_projectors_mix_partition_labels():
    for rank in range(2, 9):
        row = audit_primitive_offdiagonal(rank)
        assert row.primitive_dimension > 0
        assert row.projector_offdiagonal_nonzero_entry_count > 0
        assert row.projector_coupled_label_count >= 2
        assert not row.projector_is_label_diagonal
        assert row.nonzero_primitive_requires_cross_label_superposition


def test_Schur_commutant_has_only_within_irrep_multiplicity_blocks():
    row = Schur_commutant_control(
        irrep_dimensions=(1, 2, 3, 5),
        branching_multiplicities=(2, 4, 1, 3),
    )
    assert row.K_commutant_dimension == 2**2 + 4**2 + 1**2 + 3**2
    assert row.allowed_diagonal_multiplicity_block_dimension == (
        row.K_commutant_dimension
    )
    assert row.forbidden_cross_irrep_block_dimension > 0
    assert row.offdiagonal_irrep_blocks_in_K_commutant == 0
    assert row.Schur_block_formula_verified


def test_label_projector_cannot_be_a_K_centralizing_ambient_operator():
    report = build_ambient_lift_report()
    assert report.theorem.exact_Schur_block_obstruction_proved
    assert report.theorem.primitive_projector_crosses_inequivalent_labels_proved
    assert not report.theorem.K_centralizing_label_projector_lift_exists
    assert not report.theorem.non_K_equivariant_subduction_lift_compiled
    assert not report.theorem.within_mu_primitive_commutant_generators_compiled
    assert not report.theorem.source_aware_normalized_subduction_transform_compiled
    assert not report.theorem.hidden_involution_detector_constructed
    assert not report.theorem.speedup_claim_allowed
    assert report.theorem.theorem_verified


def test_obstruction_does_not_claim_full_matrix_polar_impossibility():
    report = build_ambient_lift_report()
    challenges = {row["challenge"]: row["answer"] for row in report.adversarial_audit}
    assert any("full polar" in challenge for challenge in challenges)
    assert report.claim_gate["K_centralizing_ambient_lift_exists"] is False
    assert report.claim_gate["non_K_equivariant_subduction_lift_compiled"] is False


def test_live_ambient_lift_report_is_json_serializable(tmp_path):
    output = tmp_path / "ambient-lift.json"
    payload = write_ambient_lift_report(output)
    assert output.exists()
    assert payload["theorem"]["theorem_verified"]
    assert payload["claim_gate"][
        "primitive_label_projector_crosses_inequivalent_K_labels"
    ]
    assert not payload["claim_gate"]["K_centralizing_ambient_lift_exists"]
    assert not payload["claim_gate"]["speedup_claim_allowed"]
