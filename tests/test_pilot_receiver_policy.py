"""Receiver-boundary falsifiers, not quantum speedup experiments."""
from copy import deepcopy
from fractions import Fraction
import random

import numpy as np
import pytest

from theorems.pilot_module_descent import pilot_module_search, report as pilot_report
from theorems.pilot_receiver_policy import (
    compile_receiver_plan, correlation_falsifier, flagged_error_bound, postselection_falsifier,
    policy_side_information_falsifier,
)


@pytest.fixture
def accepted_history():
    return pilot_module_search(prime=3,ambient_exponents=(2,),degree=2,
        draw_labels=lambda count:[(3,)]*count,bit_source=random.Random(1),episode_cap=2)


def test_checked_plan_retains_all_copy_costs_and_only_nonzero_unit_actions(accepted_history):
    plan = compile_receiver_plan(accepted_history)
    assert plan["output_flag"]=="accept"
    assert plan["observed_label_count"]==11 and plan["preallocated_copy_cap"]==166
    assert plan["unobserved_padding"]==155
    slots = [a["slot"] for a in plan["active_slots"]]
    assert len(set(slots))==len(slots) and all(3<=s<11 for s in slots)
    assert 0<len(slots)<8  # zero-weight raw copies are still charged, not acted on
    assert plan["identity_action_slots"]+len(slots)==166
    assert plan["padded_tensor_copies_charged"]==166
    assert all(a["scale"]%3 for a in plan["active_slots"])
    assert not plan["physical_ownership_certified"] and not plan["quantum_receiver_executed"]
    assert not plan["zero_dilation_is_used"]


def test_failed_episode_and_new_pilots_never_become_active_targets():
    history = pilot_report()["incomplete_pilot_retry_control"]
    plan = compile_receiver_plan(history)
    assert plan["observed_label_count"]==15
    assert all(7<=a["slot"]<15 for a in plan["active_slots"])
    ranges = plan["request_slot_ranges"]
    assert [(r["start"],r["stop"]) for r in ranges[:3]]==[(0,3),(3,4),(4,7)]


def test_one_shot_scales_cannot_disappear_after_equation_verification(accepted_history):
    expected = compile_receiver_plan(accepted_history)
    episode = accepted_history["episodes"][0]
    episode["scales"] = iter(episode["scales"])
    actual = compile_receiver_plan(accepted_history)
    assert actual==expected and actual["active_slots"]


def test_zero_support_still_uses_one_fresh_nonpilot_source():
    plan = compile_receiver_plan(pilot_report()["zero_support_control"])
    assert plan["active_slots"]==[{"slot":4,"scale":1,"ambient_label":(0,0)}]
    assert plan["identity_action_slots"]==plan["preallocated_copy_cap"]-1


def test_all_abort_plan_has_no_target_or_active_dilation():
    def draw(count):
        return [(1,0),(0,1),(1,0),(0,1)] if count==4 else [(1,0)]*count
    history = pilot_module_search(prime=3,ambient_exponents=(2,3),degree=2,
                                 draw_labels=draw,episode_cap=2,failure_bits=4)
    plan = compile_receiver_plan(history)
    assert plan["output_flag"]=="abort" and not plan["active_slots"]
    assert not plan["original_ambient_equations_checked"]
    assert plan["identity_action_slots"]==plan["preallocated_copy_cap"]


@pytest.mark.parametrize("mutation",["pilot","duplicate","negative","cap","count","zero_witness",
                                     "source_mismatch","success_index","extra_episode"])
def test_corrupt_slot_provenance_and_native_claims_fail_closed(accepted_history,mutation):
    history = deepcopy(accepted_history)
    episode = history["episodes"][0]
    if mutation=="pilot":
        episode["selected_request_indices"][0] = 0
    elif mutation=="duplicate":
        episode["selected_request_indices"].append(episode["selected_request_indices"][0])
    elif mutation=="negative":
        episode["selected_request_indices"][0] = -1
    elif mutation=="cap":
        history["source_labels_cap"] -= 1
    elif mutation=="count":
        episode["requests"][1]["count"] += 1
    elif mutation=="zero_witness":
        episode["scales"] = [0]*len(episode["scales"])
    elif mutation=="source_mismatch":
        episode["selected_ambient_columns"][0] = (0,)
    elif mutation=="success_index":
        history["successful_episode_index"] = 1
    else:
        history["episodes"].append(deepcopy(episode))
    with pytest.raises((ValueError,ArithmeticError)):
        compile_receiver_plan(history)


def test_original_character_phase_cancels_in_every_mixed_order_coordinate():
    rng = random.Random(1)
    for case in pilot_report()["cases"]:
        plan = compile_receiver_plan(case["result"])
        p,d,es = plan["prime"],plan["degree"],plan["ambient_exponents"]
        totals = [sum(a["ambient_label"][j]*a["scale"]**d for a in plan["active_slots"])
                  for j in range(len(es))]
        assert all(t%p**e==0 for t,e in zip(totals,es))
        for _ in range(10):
            z = [rng.randrange(p**e) for e in es]
            phase = sum(Fraction(t*x,p**e) for t,x,e in zip(totals,z,es))
            assert phase.denominator==1


def test_unobserved_padding_cannot_influence_the_prefix_policy():
    plans = []
    for padding in (0,1):
        tape = [(3,)]*11+[(padding,)]*155
        cursor = 0
        def draw(count):
            nonlocal cursor
            result = tape[cursor:cursor+count]
            cursor += count
            return result
        history = pilot_module_search(prime=3,ambient_exponents=(2,),degree=2,
            draw_labels=draw,bit_source=random.Random(1),episode_cap=2)
        assert cursor==11
        plans.append(compile_receiver_plan(history))
    assert plans[0]==plans[1]


def test_same_marginals_and_perfect_cancellation_do_not_replace_independence():
    control = correlation_falsifier()
    assert control["joint_trace"]==pytest.approx(1)
    assert control["joint_min_eigenvalue"]>=-1e-12
    assert control["marginal_a_error"]==control["marginal_b_error"]==0
    assert control["independent_output_error"]<1e-12
    assert control["correlated_output_trace_distance"]==pytest.approx(2/3)
    assert np.allclose(control["correlated_output_real"],np.ones((3,3))/3)
    assert not control["character_cancellation_alone_is_sufficient"]


def test_conditional_error_can_be_a_hundred_times_unconditional_error():
    control = postselection_falsifier()
    assert control["unconditional_distance"]==Fraction(1,1000)
    assert control["conditional_distance"]==Fraction(1,10)
    assert not control["accepted_only_error_bound_without_division_is_valid"]


def test_policy_choice_table_does_not_replace_private_source_independent_coins():
    control = policy_side_information_falsifier()
    assert control["source_marginal_error"]<1e-14
    assert control["choice_scale_counts"]==[2,1]
    assert control["independent_choice_output_error"]<1e-14
    assert control["source_correlated_choice_output_trace_distance"]==pytest.approx(1/3)
    assert not control["conditional_choice_table_alone_is_sufficient"]


def test_complete_channel_budget_adds_uniform_errors_without_acceptance_division():
    result = flagged_error_bound(ideal_abort=Fraction(9,256),joint_input_distance=Fraction(1,1000),
        measurement_calls=166,measurement_half_diamond=Fraction(1,100000),
        action_calls=166,action_half_diamond=Fraction(1,200000),
        control_preparation_distance=Fraction(1,10000),classical_clock_abort=Fraction(1,1000))
    expected = Fraction(9,256)+Fraction(2,1000)+Fraction(166,100000)+Fraction(166,200000)+Fraction(1,10000)
    assert result["total_error_upper"]==expected
    assert not result["assumptions_verified_by_calculator"]
    assert not result["acceptance_probability_division_used"]


@pytest.mark.parametrize("value",[0.01,Fraction(-1,100),Fraction(101,100)])
def test_inexact_or_invalid_error_promises_rejected(value):
    with pytest.raises(ValueError):
        flagged_error_bound(ideal_abort=value,joint_input_distance=Fraction(0),
            measurement_calls=0,measurement_half_diamond=Fraction(0),action_calls=0,
            action_half_diamond=Fraction(0),control_preparation_distance=Fraction(0),
            classical_clock_abort=Fraction(0))
