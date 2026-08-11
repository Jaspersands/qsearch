from diagram_hidden_subalgebra_coset_no_go import (
    audit_monoid_submonoid,
    bell_number,
    diagram_qft_scaling_boundary,
    enumerate_submonoids,
    run_diagram_hidden_subalgebra_coset_no_go,
    submonoid_is_group,
    transformation_monoid,
    translate_partition_statistics,
    write_diagram_hidden_subalgebra_coset_no_go,
)


def test_group_of_units_has_equal_or_disjoint_translates():
    elements, table = transformation_monoid(2)
    identity = (0, 1)
    row = audit_monoid_submonoid(
        "UNITS", elements, identity, table, (identity, (1, 0))
    )
    assert row.submonoid_is_group
    assert row.right_translates_equal_or_disjoint
    assert row.theorem_equivalence_verified


def test_reset_idempotent_has_overlapping_unequal_translates():
    elements, table = transformation_monoid(2)
    identity = (0, 1)
    row = audit_monoid_submonoid(
        "RESET", elements, identity, table, (identity, (0, 0))
    )
    assert not row.submonoid_is_group
    assert not row.right_translates_equal_or_disjoint
    assert row.overlapping_unequal_translate_pair_count > 0
    assert row.theorem_equivalence_verified


def test_equivalence_holds_for_every_submonoid_of_t2():
    elements, table = transformation_monoid(2)
    identity = (0, 1)
    submonoids = enumerate_submonoids(elements, identity, table)
    assert len(submonoids) >= 4
    for subset in submonoids:
        equal_or_disjoint = translate_partition_statistics(
            elements, subset, table
        )[1]
        assert equal_or_disjoint == submonoid_is_group(
            subset, identity, table
        )


def test_bell_numbers_and_qft_scaling_boundaries_are_exact():
    assert [bell_number(index) for index in range(7)] == [1, 1, 2, 5, 15, 52, 203]
    row = diagram_qft_scaling_boundary(4)
    assert int(row.brauer_basis_dimension_decimal) == 105
    assert int(row.partition_basis_dimension_decimal) == 4140
    assert not row.ordinary_coset_partition_available_for_bridge_generated_subalgebra
    assert not row.efficient_qft_implies_hidden_problem_solver
    assert row.module_spectrum_direction_not_killed_by_coset_no_go


def test_replacement_hypothesis_remains_proof_gated():
    report = run_diagram_hidden_subalgebra_coset_no_go()
    hypothesis = report.replacement_hypothesis
    assert not hypothesis.natural_decision_reduction_proved
    assert not hypothesis.coherent_input_preparation_proved
    assert not hypothesis.asymptotically_unitary_parameter_regime_proved
    assert not hypothesis.dequantization_survived
    assert not hypothesis.proof_gate_passed
    assert report.claim_gate[
        "module_spectrum_replacement_direction_structurally_open"
    ]


def test_report_writes_and_keeps_algorithm_gates_closed(tmp_path):
    payload = write_diagram_hidden_subalgebra_coset_no_go(
        tmp_path / "report.json"
    )
    assert payload["headline_metrics"][
        "exhaustive_t2_equivalence_failure_count"
    ] == 0
    assert not payload["claim_gate"]["naive_diagram_hidden_subalgebra_has_hsp_cosets"]
    assert not payload["claim_gate"]["module_spectrum_replacement_passes_proof_gate"]
    assert not payload["claim_gate"]["speedup_claim_allowed"]
