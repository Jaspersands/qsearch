from fractions import Fraction

import numpy as np
import pytest

from dcp_direct_witness_filter import (
    bounded_purified_filter_control, bounded_tagged_solver_fixture,
    direct_filter_resource_certificate, purified_finder_interface_gate, run_controls,
)
from dcp_physical_phase_noise import read


@pytest.mark.parametrize("weights", [(0,0,0,0),(1,1,1,1),(Fraction(1,4),Fraction(1,2),Fraction(3,4),1)])
def test_target_tagged_noncanonical_purified_solver_garbage_is_erased(weights):
    matrices=bounded_tagged_solver_fixture(((1,1,2),),4,weights)
    row=bounded_purified_filter_control(((1,1,2),),4,matrices)
    assert row["target_verified_output_probabilities"] == pytest.approx(weights)
    assert row["herald_probability_after_all_workspace_zero_projection"] == pytest.approx(sum(w*w for w in weights)/8)
    assert row["correct_full_secret_probability_for_every_secret"] == pytest.approx(sum(weights)**2/32)
    assert row["fixed_secret_controls"] == 4
    assert row["clean_filter_operator_norm"] <= 1+1e-10
    # The solver stores orthogonal target histories, including arbitrary complex phases.
    for t,U in enumerate(matrices):
        support=np.where(abs(U[:,0])>1e-10)[0]
        assert all(w//8==t for w in support)
    assert not row["bounded_matrix_fixture_is_uniform_polynomial_finder"]


def test_binary_rank_deficiency_is_charged_through_coverage_without_aborting():
    matrices=bounded_tagged_solver_fixture(((2,0,2),),4,(1,0,Fraction(1,2),0))
    row=bounded_purified_filter_control(((2,0,2),),4,matrices)
    assert row["correct_full_secret_probability_for_every_secret"] == pytest.approx(9/128)
    assert row["fixed_secret_controls"] == 4


def test_forgetting_or_measuring_target_history_is_not_compute_uncompute():
    weights=(Fraction(1,4),Fraction(1,2),Fraction(3,4),1)
    matrices=bounded_tagged_solver_fixture(((1,1,2),),4,weights)
    row=bounded_purified_filter_control(((1,1,2),),4,matrices)
    dirty_correct=float(sum(weights)/32)
    assert row["correct_full_secret_probability_for_every_secret"] > dirty_correct
    gate=purified_finder_interface_gate(known_uniform_bounded_circuit=True,accessible_purification_and_inverse=False)
    assert "accessible retained purification and circuit inverse" in gate["issues"]
    assert not gate["arbitrary_measured_output_only_black_box_suffices"]


def test_noncanonical_raw_filter_survives_scoped_fair_physical_dephasing():
    weights=(Fraction(1,4),Fraction(1,2),Fraction(3,4),1)
    matrices=bounded_tagged_solver_fixture(((1,1,2),),4,weights)
    row=bounded_purified_filter_control(((1,1,2),),4,matrices)
    p=np.asarray(row["clean_filter_matrix"]).sum(axis=0)
    ideal=row["correct_full_secret_probability_for_every_secret"]
    for bad in range(8):
        coins=[z for z in range(8) if not z&~bad]
        averaged=sum(sum(a*(-1)**((x&z).bit_count()%2) for x,a in enumerate(p))**2/32 for z in coins)/len(coins)
        assert averaged+1e-12 >= ideal/2**bad.bit_count()


@pytest.mark.parametrize("n,delta",[(8,0),(8,16),(16,0),(16,16),(32,0)])
def test_raw_resource_ledger_has_no_rank_loss_alignment_or_top_bit_cost(n,delta):
    attempts=(1<<(40+delta))*n**4
    row=direct_filter_resource_certificate(n,4*n+1,delta,Fraction(1,n*n),attempts)
    assert read(row["ideal_full_secret_success_per_original_attempt_lower_bound"]) == Fraction(1,n**4*2**delta)
    assert row["original_states_per_complete_attempt"] == n*(4*n+1)+delta+row["fresh_candidate_verification_states"]
    assert row["original_states_preallocated_for_all_attempts"] == attempts*row["original_states_per_complete_attempt"]
    assert not row["parity_measurement_binary_rank_rejection_or_target_alignment_required"]
    assert not row["full_secret_top_bit_completion_required"]
    assert row["full_secret_failure_bound_below_one_third_as_declared"]
    assert not row["uniform_polynomial_finder_supplied"]
    assert not row["candidate_record_accepted"]


def test_full_vector_group_and_all_report_claim_gates():
    report=run_controls()
    row=report["known_purified_quantum_finder_controls"][-1]
    assert row["fixed_secret_controls"] == 16
    assert row["correct_full_secret_probability_for_every_secret"] == pytest.approx(Fraction(1,4))
    assert not report["claim_gate"]["quantum_arithmetic_finder_constructed"]
    assert not report["claim_gate"]["speedup_claim_allowed"]


def test_bad_programs_and_incompatible_coverage_fail_closed():
    matrices=bounded_tagged_solver_fixture(((1,1,2),),4,(1,1,1,1))
    matrices[0][0,0]=7
    with pytest.raises(ValueError):
        bounded_purified_filter_control(((1,1,2),),4,matrices)
    with pytest.raises(ValueError):
        bounded_tagged_solver_fixture(((2,0,2),),4,(1,1,1,1))
    with pytest.raises(ValueError):
        direct_filter_resource_certificate(8,33,0,0,16)
    with pytest.raises(ValueError):
        direct_filter_resource_certificate(8,33,-1,1,16)
    declarations=dict(known_uniform_bounded_circuit=True,accessible_purification_and_inverse=True,
                      preserves_classical_target_register=True,verifiable_boolean_output=True,
                      native_independent_target_coverage_proved=True,no_unknown_state_or_unavailable_oracle_inverse=True)
    gate=purified_finder_interface_gate(**declarations)
    assert gate["obligations_satisfied_as_declared"]
    assert not gate["declarations_prove_an_algorithm"]
