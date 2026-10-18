from fractions import Fraction
from copy import deepcopy
import inspect
import json

import numpy as np
import pytest

from theorems.dcp_clean_source_budget import (
    CONTRACT,CONTRACT_ID,REPORT,build_report,copy_budget_excluded,materialize_public_source,
    noise_physics_controls,plan_sine_source,transfer_budget,verified_easy_source_control,
)
from theorems.lattice_sine_window_source import SineWindowSource,promise_budget
from theorems.dcp_correlated_phase_block import density
from theorems.dcp_native_parity_observables import measurement_operators


@pytest.mark.parametrize("K,eps",[(16,Fraction(1,16)),(1000,Fraction(1,100)),(10**8,Fraction(1,10**6))])
def test_clean_advantage_survives_an_explicit_joint_noise_and_precision_budget(K,eps):
    r=transfer_budget(K,eps,eps/(2*K),joint_preparation_error_per_call=eps/(8*K),adapter_total_error=eps/8)
    assert r["half_clean_advantage_preserved"]
    assert Fraction(r["noisy_average_advantage_lower_IF_clean_predictor_exact"])==eps/2
    assert not r["clean_predictor_implemented_or_certified"]
    assert not r["arbitrary_coherent_noise_with_same_one_qubit_marginals_covered"]


def test_inverse_dimension_benchmark_can_fail_the_transfer_without_invalidating_clean_algorithms():
    r=transfer_budget(2*64*72,Fraction(1,16),Fraction(1,64))
    assert not r["half_clean_advantage_preserved"]
    assert Fraction(r["noisy_average_advantage_lower_IF_clean_predictor_exact"])<=0
    assert not r["fixed_inverse_dimension_benchmark_noise_is_mandatory"]


def test_an_actual_public_clean_parity_measurement_obeys_the_noise_transfer():
    A=((2,2,2,2),)
    K=4
    eps=Fraction(1,4)
    gamma=eps/(2*K)
    budget=transfer_budget(K,eps,gamma)
    O=measurement_operators(A,3,1)["optimal_observable"]
    lower=.5+float(Fraction(budget["noisy_average_advantage_lower_IF_clean_predictor_exact"]))
    for s in range(8):
        clean=.5+(-1)**(s%2)*np.trace(O@density(A,3,(s,),1)).real/2
        noisy=.5+(-1)**(s%2)*np.trace(O@density(A,3,(s,),1-gamma)).real/2
        assert clean>=.5+float(eps)
        assert noisy>=lower-1e-12


@pytest.mark.parametrize("B,a",[
    (((1,0),(0,257)),0),(((1,0),(0,257)),1),
    (((17,0),(16,1)),0),(((17,0),(16,1)),2),
    (((1,0,0),(0,257,0),(0,0,65537)),1),
])
def test_public_fixed_point_closes_at_its_actual_final_modulus(B,a):
    r=plan_sine_source(B,1,2,advantage_power=a)
    t=r["cyclic_phase_bits"]
    n=len(B)
    model=r["sample_model"]
    K=model["copy_multiplier"]*t**model["copy_power"]
    eps=Fraction(model["advantage_coefficient_exact"])/t**model["advantage_power"]
    gamma=eps/(2*K)
    box=int(r["parent_box_side_hex"],16)
    side=int(r["packet_side_hex"],16)
    assert t==n*(box.bit_length())
    assert r["lifted_native_components"]==t-8>=2
    assert Fraction(r["packet_loss_upper_exact"])+Fraction(r["boundary_loss_upper_exact"])<=gamma
    assert Fraction(r["all_trial_parent_shift_l1_upper"],box)<=gamma/2
    assert Fraction(242*2,49*side*side)<=gamma/2
    assert r["required_unique_gap_strict_sufficient"]**2>n*side*side
    assert (r["splitting_prime_lower_bound"]-1)**2>n*side*side
    assert r["fixed_point_history"][-1]["cyclic_phase_bits"]==t
    assert r["clean_transfer_budget"]["original_source_calls"]==K
    assert r["clean_transfer_budget"]["half_clean_advantage_preserved"]
    assert not r["short_vector_gap_correct_trial_and_joint_preparation_precision_certified"]


def test_extra_inverse_polynomial_advantage_is_not_replaced_by_old_stale_box_budget():
    B=((1,0),(0,257))
    loose=plan_sine_source(B,1,2)
    strict=plan_sine_source(B,1,2,advantage_power=2)
    assert strict["parent_box_bits"]>loose["parent_box_bits"]
    assert strict["cyclic_phase_bits"]>loose["cyclic_phase_bits"]
    assert strict["required_unique_gap_strict_sufficient"]>loose["required_unique_gap_strict_sufficient"]
    assert len(strict["fixed_point_history"])>1


def test_plan_uses_only_public_basis_norm_interval_and_declared_algorithm_resources():
    parameters=inspect.signature(plan_sine_source).parameters
    assert "secret" not in parameters and "short_vector" not in parameters
    r=plan_sine_source(((17,0),(16,1)),1,2)
    source=materialize_public_source(r)
    ledger=source["existing_source_promise_budget"]
    assert list(ledger["public_basis_coefficient_bounds"])==r["public_coefficient_absolute_bounds"]
    assert sum(ledger["public_parent_shift_bounds"])<=r["all_trial_parent_shift_l1_upper"]
    assert ledger["nonparallel_aliases_excluded_IF_promises_hold"]
    assert ledger["parallel_cross_colour_aliases_excluded_IF_promises_hold"]
    assert ledger["short_vector_norm_gap_and_correct_trial_are_unverified_assumptions"]
    assert source["symbolic_source_resources"]["position_QFT_qubits"]==r["cyclic_phase_bits"]
    assert source["coordinate_residue_trials_upper"]==2*(source["selected_prime"]-1)
    assert not source["large_source_executed"]
    assert not source["actual_lattice_promises_certified_from_basis"]


def test_strict_parallel_alias_boundary_and_broad_norm_interval_are_explicit():
    r=plan_sine_source(((1,0),(0,257)),1,100)
    assert not r["constant_factor_norm_interval"]
    source=materialize_public_source(r)
    assert source["existing_source_promise_budget"]["parallel_cross_colour_aliases_excluded_IF_promises_hold"]


@pytest.mark.parametrize("field",["cyclic_phase_bits","splitting_prime_lower_bound","required_unique_gap_strict_sufficient","all_trial_parent_shift_l1_upper"])
def test_materialized_source_rejects_forged_fixed_point_or_alias_receipts(field):
    r=plan_sine_source(((1,0),(0,257)),1,2)
    fake=deepcopy(r)
    fake[field]=1
    with pytest.raises(ValueError,match="receipt"):
        materialize_public_source(fake)


def test_same_local_marginals_do_not_license_arbitrary_coherent_noise_transfer():
    r=noise_physics_controls()
    for c in r["classical_Z_mixture_controls"]:
        assert c["actual_fixed_secret_joint_trace_distance_max"]<=float(Fraction(c["marginal_union_upper_exact"]))+1e-12
    coherent=r["coherent_noise_marginal_counterexample"]
    assert coherent["joint_trace_distance"]==pytest.approx(Fraction(1,8))
    assert coherent["sum_two_marginal_trace_distances"]==pytest.approx(Fraction(1,32))
    assert not coherent["classical_Z_mask_assumption_satisfied"]


def test_live_source_calibration_has_an_actual_public_uniqueness_certificate_not_just_assumed_gap():
    r=verified_easy_source_control()
    B=r["public_plan"]["public_basis_rows"]
    W=r["unimodular_left_transform"]
    product=[[sum(W[i][k]*B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    assert product==r["diagonalized_basis"]
    assert W[0][0]*W[1][1]-W[0][1]*W[1][0]==1
    assert r["shortest_nonparallel_norm_squared_exact"]>2*int(r["public_plan"]["packet_side_hex"],16)**2
    assert r["actual_lattice_promises_certified_from_basis"]
    assert r["known_parent_shift_FOR_CALIBRATION_ONLY"]==[0,-1]
    assert not r["short_vector_was_input_to_planner_or_source_constructor"]
    assert not r["large_source_executed"]


def test_larger_declared_copy_count_changes_the_required_source_not_a_fake_decoder():
    B=((1,0),(0,257))
    small=plan_sine_source(B,1,2,copy_power=2)
    large=plan_sine_source(B,1,2,copy_power=4)
    assert large["required_unique_gap_strict_sufficient"]>small["required_unique_gap_strict_sufficient"]
    assert not large["native_clean_predictor_supplied"]
    assert not large["higher_required_gap_is_a_classical_hardness_certificate"]


def test_source_plan_rejects_impossible_copy_hypotheses_and_keeps_scalar_rank_distinct():
    B=((1,0),(0,257))
    with pytest.raises(ValueError,match="INCONSISTENT"):
        plan_sine_source(B,1,2,copy_power=1)
    scalar=plan_sine_source(B,1,2,copy_power=1,predictor_family="scalar")
    native=plan_sine_source(B,1,2)
    assert scalar["predictor_secret_components"]==1
    assert scalar["lifted_native_components"] is None
    assert scalar["required_unique_gap_strict_sufficient"]<native["required_unique_gap_strict_sufficient"]


def test_copy_budget_comparison_is_exact_without_enormous_native_group_integers():
    for n in range(1,5):
        for t in range(3,12):
            for K in range(1,n*t+3):
                for eps in (Fraction(1,2),Fraction(1,16),Fraction(1,3),Fraction(1,7)):
                    exact=Fraction(2**K-1,2**(n*t+1))<eps
                    assert copy_budget_excluded(n,t,K,eps)==exact
    assert copy_budget_excluded(10**8,10**8,10**6,Fraction(1,16))


def test_live_report_and_contract_do_not_promote_the_tradeoff_to_a_reduction_algorithm():
    r=build_report()
    assert json.loads(REPORT.read_text())==r
    assert json.loads(CONTRACT.read_text())["contract_id"]==r["contract_id"]==CONTRACT_ID
    assert len(r["public_fixed_point_plans"])==6
    assert not r["accepted_speedup_candidate"]
    assert not r["new_lattice_reduction_or_novelty_claim"]
    assert not r["classically_easy_calibration_bases_are_hard_instances"]


@pytest.mark.parametrize("call",[
    lambda:transfer_budget(0,Fraction(1,16),0),
    lambda:transfer_budget(10,0,0),
    lambda:transfer_budget(10,Fraction(1,16),-1),
    lambda:plan_sine_source(((1,2),(2,4)),1,2),
    lambda:plan_sine_source(((1,),),2,1),
    lambda:plan_sine_source(((1,),),1,2,copy_power=0),
    lambda:plan_sine_source(((1,),),1,2,advantage_coefficient=0),
])
def test_invalid_resource_or_public_source_promises_fail_closed(call):
    with pytest.raises(ValueError):
        call()
