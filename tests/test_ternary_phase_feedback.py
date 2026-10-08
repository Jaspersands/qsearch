from copy import deepcopy
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import random
import subprocess

import numpy as np
import pytest

from ternary_covariant_noise import CovariantRecord, phase, simulated_record
from ternary_phase_feedback import (
    PublicPhasePolicy, compile_covariant_feedback, feedback_posterior,
    filter_trine_orbit, physical_phase_control, recover_raw_records,
    run_trine_resampling, trine_resampling_budget,
)
from ternary_posterior_dual import solve_least_trit
from ternary_product_trine import randomized_outcome


def example_records():
    rng=random.Random(81291)
    return [simulated_record((1,2),(3,4),(4,7),9,rng)[0],
            simulated_record((3,5),(2,0),(4,7),9,rng)[0],
            simulated_record((8,6),(7,4),(4,7),9,rng)[0]]


@pytest.mark.parametrize("kind", ["zero","known_offset","quadratic_feedback"])
def test_causal_phase_feedback_preserves_every_raw_record_and_exact_posterior(kind):
    policy=PublicPhasePolicy(kind,(2,5) if kind=="known_offset" else ())
    records=example_records();ids=[10,11,13]
    transcript=compile_covariant_feedback(records,ids,policy)
    recovered,recovered_ids=recover_raw_records(transcript)
    assert list(recovered)==records and list(recovered_ids)==ids
    original=solve_least_trit(records,ids)
    replay=feedback_posterior(transcript)
    assert original["coefficient_numerators"]==replay["coefficient_numerators"]
    assert original["posterior"]==replay["posterior"]
    assert not replay["feedback_adds_information_about_secret"]
    assert replay["physical_covariant_record_source_still_required"]
    assert transcript["cost_ledger"]["supplied_covariant_records_consumed"]==3
    assert not transcript["original_unknown_states_or_DCP_classically_simulated"]


def test_exponential_reference_budget_failure_is_preserved_after_feedback_removal():
    c=compile_covariant_feedback(example_records(),[0,1,2],PublicPhasePolicy("quadratic_feedback"))
    result=feedback_posterior(c,max_half_states=1)
    assert result["status"]=="EXACT_REFERENCE_BUDGET_EXHAUSTED_NO_POSTERIOR"
    assert result["posterior"] is None and result["feedback_removed_by_exact_classical_inverse"]


def test_feedback_uses_only_earlier_reported_outcomes_not_current_or_future_data():
    records=example_records();policy=PublicPhasePolicy("quadratic_feedback")
    baseline=compile_covariant_feedback(records,[1,2,3],policy)
    changed=records[:2]+[CovariantRecord(records[2].first,records[2].second,(0,0),9)]
    other=compile_covariant_feedback(changed,[1,2,3],policy)
    assert [r["phase_pair"] for r in baseline["steps"]]==[r["phase_pair"] for r in other["steps"]]
    changed=[CovariantRecord(records[0].first,records[0].second,(1,1),9)]+records[1:]
    other=compile_covariant_feedback(changed,[1,2,3],policy)
    assert baseline["steps"][0]["phase_pair"]==other["steps"][0]["phase_pair"]
    assert baseline["steps"][1]["phase_pair"]!=other["steps"][1]["phase_pair"]


@pytest.mark.parametrize("q", [3,9,27])
@pytest.mark.parametrize("secret", [0,3,8])
def test_actual_native_phase_laws_and_fixed_basis_orbit_through_nonprimitive_secrets(q,secret):
    c=physical_phase_control(q,(1,),(q-1,),(secret%q,),(q-1,1))
    assert c["covariant_output_relabel_residual"]<3e-12
    assert c["fixed_trine_conditional_Born_residual"]<3e-12
    assert Fraction(c["orbit_acceptance_probability"])==Fraction(3,q*q)


@pytest.mark.parametrize("q", [3,9])
def test_orbit_effect_is_input_independent_scaled_identity_not_secret_postselection(q):
    for a,b in product(range(q),repeat=2):
        effect=np.zeros((3,3),dtype=complex)
        for z in range(3):
            y=randomized_outcome(q,a,b,z)
            v=np.array([1,phase(y[0],q),phase(y[1],q)])
            effect+=np.outer(v,v.conj())/(q*q)
        assert np.max(abs(effect-3*np.eye(3)/(q*q)))<3e-13


def test_filling_a_stream_counts_rejections_unused_records_and_original_ids():
    q=9;policy=PublicPhasePolicy("quadratic_feedback")
    phase1=policy.choose((1,),(2,),q,())
    z1=2;y1=randomized_outcome(q,*phase1,z1)
    history=[randomized_outcome(q,0,0,z1)]
    phase2=policy.choose((3,),(4,),q,history)
    z2=1;y2=randomized_outcome(q,*phase2,z2)
    records=[CovariantRecord((1,),(2,),((phase1[0]+1)%q,phase1[1]),q),
             CovariantRecord((1,),(2,),y1,q), CovariantRecord((3,),(4,),y2,q),
             CovariantRecord((5,),(6,),(0,0),q)]
    c=run_trine_resampling(records,[8,10,11,15],2,policy)
    assert c["status"]=="TARGET_FIXED_TRINE_STREAM_FILLED"
    assert [r["digit"] for r in c["accepted_records"]]==[2,1]
    assert c["rejected_original_ids"]==[8] and c["unused_original_ids"]==(15,)
    assert c["consumed_original_ids"]==(8,10,11)
    assert c["cost_ledger"]["supplied_covariant_records_consumed"]==3
    assert not c["quantum_unknown_states_classically_simulated"]


def test_shortage_and_zero_target_have_no_fabricated_success_or_copy_reuse():
    records=[CovariantRecord((1,),(2,),(1,0),9)]
    c=run_trine_resampling(records,[0],1,PublicPhasePolicy())
    assert c["status"]=="SOURCE_CAP_EXHAUSTED_NO_COMPLETE_FIXED_TRINE_STREAM"
    assert c["accepted_records"]==[] and c["rejected_original_ids"]==[0]
    empty=run_trine_resampling(records,[0],0,PublicPhasePolicy())
    assert empty["status"]=="TARGET_FIXED_TRINE_STREAM_FILLED"
    assert empty["cost_ledger"]["supplied_covariant_records_consumed"]==0
    assert empty["unused_original_ids"]==(0,)
    assert trine_resampling_budget(4,0,0)["probability_of_filling_target_upper_by_Markov"]=="1"


def test_unlawful_outcome_adaptive_orbit_choice_shows_why_causal_contract_is_required():
    for y in product(range(9),repeat=2):
        record=CovariantRecord((1,),(2,),y,9)
        assert filter_trine_orbit(record,y)["digit"]==0
    # Looking at Y before choosing the settings would falsely claim acceptance1.
    assert trine_resampling_budget(2,1,1)["acceptance_probability_per_consumed_record"]=="1/27"
    with pytest.raises(ValueError): compile_covariant_feedback(example_records(),[0,1,2],lambda *_: (0,0))


@pytest.mark.parametrize("r", [4,8,16,32,64])
def test_root_scaling_resampling_cost_is_q_squared_not_polynomial_in_root_digits(r):
    target=r-2;cap=target*r*r
    c=trine_resampling_budget(r,target,cap)
    assert Fraction(c["uncapped_expected_covariant_records"])==target*3**(2*r-1)
    assert Fraction(c["probability_of_filling_target_upper_by_Markov"])==min(1,Fraction(r*r,3**(2*r-1)))
    assert c["cost_polynomial_in_q_not_log_q"]
    assert c["polynomial_in_n_only_if_q_is_polynomial_and_source_supply_permits"]
    assert not c["batch_label_lookahead_fixed_trine_compilation_covered"]
    assert not c["same_record_can_be_retried_as_fresh_source"]


def test_corrupted_transcripts_fail_policy_model_and_ancestor_checks():
    c=compile_covariant_feedback(example_records(),[0,1,2],PublicPhasePolicy("quadratic_feedback"))
    mutant=deepcopy(c);mutant["steps"][1]["phase_pair"]=(0,0)
    with pytest.raises(ValueError): recover_raw_records(mutant)
    mutant=deepcopy(c);mutant["steps"][1]["original_id"]=0
    with pytest.raises(ValueError): recover_raw_records(mutant)
    mutant=deepcopy(c);mutant["cost_ledger"]["distinct_original_ids"]=[7,8,9]
    with pytest.raises(ValueError): recover_raw_records(mutant)
    mutant=deepcopy(c);mutant["readout_model"]="FIXED_TRINE"
    with pytest.raises(ValueError): recover_raw_records(mutant)
    with pytest.raises(ValueError): PublicPhasePolicy("unknown_secret")
    with pytest.raises(ValueError): PublicPhasePolicy("zero",(1,))
    with pytest.raises(ValueError): PublicPhasePolicy("known_offset",(1,)).choose((1,2),(3,4),9,())
    with pytest.raises(ValueError): run_trine_resampling(example_records(),[0,0,1],1,PublicPhasePolicy())


@pytest.mark.parametrize("mutation", ["posterior","phase","scope","cost","source","filter"])
def test_standalone_certificate_rejects_changed_access_or_phase_claims(tmp_path,mutation):
    root=Path(__file__).resolve().parents[1]
    record=json.loads((root/"research/classical_baselines/ternary_phase_feedback.json").read_text())
    if mutation=="posterior": record["causal_feedback_controls"][0]["exact_feedback_removed_posterior"]["coefficient_numerators"][0]=[["0","99"]]
    if mutation=="phase": record["causal_feedback_controls"][2]["steps"][1]["phase_pair"]=[0,0]
    if mutation=="scope": record["original_DCP_inputs_classically_simulated"]=True
    if mutation=="cost": record["scaling_resampling_ledgers"][0]["uncapped_expected_covariant_records"]="2"
    if mutation=="source": record["finite_shortage_control"]["status"]="TARGET_FIXED_TRINE_STREAM_FILLED"
    if mutation=="filter": record["physical_phase_and_filter_controls"][0]["orbit_acceptance_probability"]="1"
    path=tmp_path/"mutant.json";path.write_text(json.dumps(record))
    c=subprocess.run(["node",str(root/"research/certificates/ternary_phase_feedback_crosscheck.js"),str(path)],capture_output=True,text=True)
    assert c.returncode!=0,c.stdout
