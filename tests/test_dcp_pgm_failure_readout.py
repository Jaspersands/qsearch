from fractions import Fraction

import pytest

from dcp_pgm_failure_readout import (
    _fault_law, _program, _root_dyadic, bounded_control,
    failure_readout_certificate, reflection_program, run_controls,
)


def read(row):
    return Fraction(int(row["numerator_hex"],16),int(row["denominator_hex"],16))


@pytest.fixture(scope="module")
def report():
    return run_controls()


def test_complete_raw_channel_operationally_matches_random_trial_local_readout(report):
    raw = [r for r in report["physical_processor_controls"] if not r["program"]]
    assert len(raw)==9
    for row in raw:
        assert row["full_channel_matches_legal_local_baseline_before_processing"]
        assert row["mean_full_record_total_variation"]<1e-9
        assert row["optimal_all_record_uniform_secret_success"]==pytest.approx(row["matched_random_trial_product_readout_success"])
        assert not row["unknown_secret_classically_reconstructed"]


def test_every_failure_and_auxiliary_record_is_retained_and_normalized(report):
    for row in report["physical_processor_controls"]:
        G = row["modulus"]**len(row["labels"])
        N = 2**len(row["labels"][0])
        assert row["all_herald_failures_and_auxiliary_outcomes_retained"]
        for table in (row["full_probabilities_by_secret"],row["reference_probabilities_by_secret"]):
            assert len(table)==G
            assert all(len(v)==2*G*N and sum(v)==pytest.approx(1) for v in table)


def test_coherent_ancillary_controls_and_correlated_faults_obey_fixed_source_hybrid(report):
    controls = report["physical_processor_controls"]
    assert len(controls)==45
    assert sum(len(r["physical_controls"]) for r in controls)==700
    for row in controls:
        for physical in row["physical_controls"]:
            assert physical["raw_herald"]<=float(read(row["clean_herald_exact"]))+1e-9
            assert physical["state_distance"]<=physical["hybrid_state_distance_bound"]+1e-9
            assert physical["full_record_total_variation"]<=physical["pure_trace_distance"]+1e-9
            assert physical["physical_norm"]==pytest.approx(1)
        assert abs(row["optimal_all_record_uniform_secret_success"]-row["matched_random_trial_product_readout_success"])<=row["mean_full_record_total_variation"]+1e-9


def test_small_adaptive_amplification_positive_control_is_not_falsely_rejected(report):
    row = next(r for r in report["physical_processor_controls"] if r["labels"]==[[2,1]] and len(r["fault_law"])==1 and r["output_projector_kicks"]==1)
    assert row["matched_random_trial_product_readout_success"]==pytest.approx(0.75)
    assert row["optimal_all_record_uniform_secret_success"]==pytest.approx(1)


def test_native_plus16_all_record_gate_is_nonvacuous_but_not_general_hardness(report):
    rows = report["native_growing_ledgers"]
    assert [r["conservative_all_record_success_dyadic_exponent"] for r in rows]==[49,210,850]
    for r in rows:
        G,N = 1 << (r["dimension"]*r["modulus_bits"]),1 << r["phase_qubits"]
        assert read(r["native_mean_clean_herald"])==Fraction(N+G-1,N*G)
        assert read(r["native_mean_trace_distance_gain_squared_bound"])==4*r["maximum_output_projector_kicks"]**2*Fraction(N+G-1,N*G)
        assert read(r["all_record_native_mean_success_conservative_upper"])==read(r["baseline_mean_success_dyadic_upper"])+read(r["trace_gain_dyadic_upper"])
        assert not r["arbitrary_terminal_collective_measurements_or_signal_interleavings_covered"]
        assert not r["secret_dependent_fault_laws_or_general_reduction_noise_covered"]
        assert not r["bound_is_vacuous"] and not r["speedup_claim_allowed"]
    assert report["claim_gate"]["all_failure_records_in_declared_terminal_measurement_class_covered"]
    assert not any(v for k,v in report["claim_gate"].items() if k!="all_failure_records_in_declared_terminal_measurement_class_covered")


def test_zero_output_queries_leave_complete_product_record_unchanged():
    program = [{"kind":"aux","gate":"H"},{"kind":"P","on":"S","off":"X"},
               {"kind":"aux","gate":"T"},{"kind":"P","on":"H","off":"Z"}]
    row = bounded_control([[1,3]],4,program)
    assert row["output_projector_kicks"]==0
    assert row["mean_full_record_total_variation"]<1e-9
    assert row["optimal_all_record_uniform_secret_success"]==pytest.approx(row["matched_random_trial_product_readout_success"])
    cert = failure_readout_certificate(8,33,280,0)
    assert read(cert["trace_gain_dyadic_upper"])==0 and cert["gain_dyadic_exponent"] is None


def test_easy_binary_and_high_sample_regimes_remain_vacuous():
    assert failure_readout_certificate(8,1,8,10)["bound_is_vacuous"]
    assert failure_readout_certificate(1,2,20,0)["bound_is_vacuous"]


def test_nonzero_precision_budget_prevents_false_exponential_physical_claim(report):
    row = report["precision_floor_counterledger"]
    error = read(row["assumed_total_composed_output_trace_error_budget"])
    assert error==Fraction(1,10**6)
    assert read(row["all_record_native_mean_success_conservative_upper"])==read(row["ideal_all_record_native_mean_success_upper"])+error
    assert row["conservative_all_record_success_dyadic_exponent"]<20
    assert row["common_squared_bound_is_for_ideal_operations"]
    for value in (-1,Fraction(2),0.0,True):
        with pytest.raises(ValueError):
            failure_readout_certificate(1,2,2,1,value)


def test_data_Hadamard_escape_and_secret_dependent_faults_are_real_scope_counterexamples():
    # Outside the allowed projector/auxiliary algebra: decode identity F2 labels.
    for secret in range(4):
        assert all((1+(-1)**((secret>>i)&1)*(-1)**((secret>>i)&1))/2==1 for i in range(2))
    # Zero public labels, but a secret-dependent Z mask writes two secret bits.
    # It is NOT an independent corruption of the native source.
    for secret in range(4):
        mask = [(secret>>1)&1,secret&1]
        assert sum(bit << (1-i) for i,bit in enumerate(mask))==secret
    with pytest.raises(ValueError):
        _program([{"kind":"data_Hadamard","gate":"H"}])
    with pytest.raises(ValueError):
        _fault_law(lambda secret:[(1,[secret&1])],1)


@pytest.mark.parametrize("x",[Fraction(0),Fraction(1,3),Fraction(1,16),Fraction(1,17),Fraction(1),Fraction(2)])
def test_dyadic_root_rounding_is_conservative_with_explicit_clamping(x):
    upper,exponent = _root_dyadic(x)
    assert upper**2>=min(x,1)
    if exponent is not None:
        assert upper==Fraction(1,1 << exponent)


@pytest.mark.parametrize("args",[(0,2,2,1),(1,0,2,1),(1,2,0,1),(1,2,2,-1),(1,2,2,True),(1,2,2,1.0)])
def test_invalid_native_gate_parameters_rejected(args):
    with pytest.raises(ValueError):
        failure_readout_certificate(*args)


@pytest.mark.parametrize("program",[None,[None],[{"kind":"aux","gate":[]}],[{"kind":"aux","gate":"unknown"}],
                                    [{"kind":"P","on":"H","off":"X","secret":0}],
                                    [{"kind":"Q","on":"I"}],reflection_program(34)])
def test_uncosted_or_malformed_processor_operations_rejected(program):
    with pytest.raises(ValueError):
        bounded_control([[1]],4,program)


@pytest.mark.parametrize("law",[[],[(0,[0])],[(0.5,[0])],[(1,[True])],[(1,[0,1])],[(Fraction(1,2),[0])],[(1,)]])
def test_fault_mass_is_not_silently_renormalized(law):
    with pytest.raises(ValueError):
        bounded_control([[1]],4,[],law)
