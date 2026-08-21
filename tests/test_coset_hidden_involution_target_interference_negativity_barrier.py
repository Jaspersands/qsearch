from coset_hidden_involution_target_interference_negativity_barrier import (
    build_negativity_barrier_report,
    negativity_scaling_record,
    required_L1_norm,
    write_negativity_barrier_report,
)


def test_required_L1_is_exact_bias_dual_lower_bound():
    for copies in (1, 5, 20, 100):
        for bias in (0.1, 1 / 3, 0.9):
            required = required_L1_norm(copies, bias)
            assert required >= bias * 2**copies
            assert required - 1 < bias * 2**copies


def test_natural_copy_constant_bias_requires_factorial_candidate_scale():
    for half_degree in (4, 8, 16, 32, 64, 128):
        row = negativity_scaling_record(half_degree)
        assert row.required_L1_over_candidate_count >= 16
        assert row.normalization_is_factorial_in_half_degree
        assert int(row.required_group_basis_L1_norm_lower_bound_decimal) == (
            int(row.standard_LCU_amplitude_amplification_query_lower_bound_decimal)
        )


def test_standard_LCU_raw_success_is_inverse_square_normalization():
    for half_degree in (4, 8, 16):
        row = negativity_scaling_record(half_degree)
        required = int(row.required_group_basis_L1_norm_lower_bound_decimal)
        assert row.standard_LCU_raw_postselection_probability_upper_bound <= (
            1 / required**2
        )


def test_report_rules_out_generic_LCU_but_not_structured_fast_forward():
    report = build_negativity_barrier_report()
    theorem = report.theorem
    assert theorem.exact_group_basis_L1_lower_bound_proved
    assert theorem.constant_bias_requires_Omega_candidate_count_L1_proved
    assert theorem.standard_coefficient_PREP_SELECT_route_ruled_out
    assert theorem.direct_quasiprobability_sampling_has_exponential_range
    assert not theorem.all_structured_quantum_compilers_ruled_out
    assert not theorem.matrix_CS_fast_forward_compiled
    assert not theorem.speedup_claim_allowed
    assert theorem.theorem_verified


def test_adversarial_audit_does_not_promote_L1_to_circuit_lower_bound():
    report = build_negativity_barrier_report()
    assert report.claim_gate["constant_bias_requires_factorial_group_basis_L1"]
    assert report.claim_gate["standard_coefficient_PREP_SELECT_route_ruled_out"]
    assert not report.claim_gate["structured_quantum_fast_forward_ruled_out"]
    assert not report.claim_gate["matrix_CS_fast_forward_compiled"]
    assert all(row["resolved"] for row in report.adversarial_audit)


def test_live_negativity_barrier_report_is_json_serializable(tmp_path):
    output = tmp_path / "negativity-barrier.json"
    payload = write_negativity_barrier_report(output)
    assert output.exists()
    assert payload["status"] == (
        "factorial-target-interference-negativity-barrier-proved-fast-forward-open"
    )
    assert payload["claim_gate"][
        "constant_bias_requires_factorial_group_basis_L1"
    ]
    assert not payload["claim_gate"]["speedup_claim_allowed"]
