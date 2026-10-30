"""Checked sparse receiver plans; no physical quantum handles or execution.

Every slot in a fixed padded tensor is consumed. Pilots, rejected banks,
zero weights and unused suffixes get identity action and are traced out.
Unique numerical positions are provenance accounting, NOT proof of IID
physics or of one-use quantum source ownership.
"""
from fractions import Fraction

import numpy as np

from theorems.pilot_module_descent import report as pilot_report
from theorems.prime_power_rees_descent import _module_contract, verify_module_witness
from theorems.span_regular_sde import span_grade_plan


def _positive(value, name):
    if type(value) is not int or value<1:
        raise ValueError(f"positive integer {name} required")


def compile_receiver_plan(search):
    """Verify a recorded policy's native equations and sparse raw-slot map.

    This does not certify an arbitrary transcript's probability, hidden
    support, runtime, or physical source. Quantum implementation must supply
    the independent tensor, measured characters and legal automorphisms.
    """
    cap = search["episode_cap"]
    _positive(cap,"episode_cap")
    episodes = search["episodes"]
    if not episodes or len(episodes)>cap:
        raise ValueError("nonempty episode history within the cap required")
    first = episodes[0]
    p,d,es = first["prime"],first["degree"],tuple(first["ambient_exponents"])
    b = first["ambient_plan"]["failure_bits"]
    envelope = span_grade_plan(prime=p,cyclic_rank=len(es),degree=d,failure_bits=b)
    limit = cap*envelope["predecessors_per_episode_upper"]
    offset,ledger,active = 0,[],[]
    success = None
    for j,episode in enumerate(episodes):
        if ((episode["prime"],episode["degree"],tuple(episode["ambient_exponents"]))!=(p,d,es)
                or episode["ambient_plan"]["failure_bits"]!=b):
            raise ValueError("all episodes must use one fixed ambient contract")
        requests = episode["requests"]
        if not requests or requests[0]["stage"]!="pilots" or requests[0]["count"]!=len(es)+2:
            raise ValueError("every episode must begin with R+2 fresh pilot slots")
        starts = []
        start_episode = offset
        for k,request in enumerate(requests):
            count = request["count"]
            _positive(count,"request count")
            columns,_,_ = _module_contract(request["ambient_columns"],es,p,d)
            if len(columns)!=count or (k and request["stage"] not in ("bank","zero_rank_bank")):
                raise ValueError("invalid source request contents or stage")
            starts.append(offset)
            ledger.append({"episode":j,"request":k,"stage":request["stage"],
                           "start":offset,"stop":offset+count})
            offset += count
        if (offset-start_episode!=episode["source_labels_consumed"]
                or offset-start_episode>envelope["predecessors_per_episode_upper"]):
            raise ValueError("episode source count disagrees with its charged envelope")
        if episode["status"]=="VERIFIED_AMBIENT_MODULE_WITNESS":
            if success is not None or j!=len(episodes)-1:
                raise ValueError("policy must stop at its first successful episode")
            success = j
            indices = episode["selected_request_indices"]
            if (not indices or any(type(i) is not int or not 1<=i<len(requests) for i in indices)
                    or len(indices)!=len(set(indices))):
                raise ValueError("selected raw requests must be unique bank positions, never pilots")
            columns = [tuple(c) for i in indices for c in requests[i]["ambient_columns"]]
            recorded = [tuple(c) for c in episode["selected_ambient_columns"]]
            # Verification and slot construction must see the same values,
            # including when a caller supplies a one-shot iterable.
            scales = tuple(episode["scales"])
            if columns!=recorded or not verify_module_witness(columns,scales,prime=p,exponents=es,degree=d):
                raise ValueError("accepted transcript failed its original ambient equation/provenance")
            slots = [starts[i]+k for i in indices for k in range(requests[i]["count"])]
            active = [{"slot":slot,"scale":scale,"ambient_label":column}
                      for slot,scale,column in zip(slots,scales,columns) if scale]
            if not active:
                raise ValueError("an accepted receiver requires nonempty active support")
        elif episode["status"]!="ABORT":
            raise ValueError("unknown episode outcome")
    expected = "ABORT" if success is None else "VERIFIED_AMBIENT_MODULE_WITNESS"
    if (search["status"]!=expected or (success is not None and search.get("successful_episode_index")!=success)
            or (success is None and len(episodes)!=cap)
            or offset!=search["source_labels_consumed"] or search["source_labels_cap"]!=limit or offset>limit):
        raise ValueError("whole-policy status or source cap is inconsistent")
    if len({a["slot"] for a in active})!=len(active):
        raise ArithmeticError("a raw source slot would be used more than once")
    return {"status":"CHECKED_ACCEPTED_TRANSCRIPT" if success is not None else "CHECKED_ABORT_TRANSCRIPT",
            "prime":p,"degree":d,"ambient_exponents":es,"episode_cap":cap,
            "preallocated_copy_cap":limit,"observed_label_count":offset,
            "unobserved_padding":limit-offset,"request_slot_ranges":ledger,
            "active_slots":active,"identity_action_slots":limit-len(active),
            "output_flag":"accept" if success is not None else "abort",
            "original_ambient_equations_checked":success is not None,
            "padded_tensor_copies_charged":limit,"zero_dilation_is_used":False,
            "requires_joint_independent_coset_tensor":True,
            "requires_hidden_subgroup_preserving_automorphisms":True,
            "requires_original_character_phase_action":True,
            "requires_label_only_policy_with_private_randomness":True,
            "physical_ownership_certified":False,"quantum_receiver_executed":False,
            "policy_availability_certified_by_transcript":False}


def flagged_error_bound(*, ideal_abort, joint_input_distance, measurement_calls,
                       measurement_half_diamond, action_calls, action_half_diamond,
                       control_preparation_distance, classical_clock_abort):
    """Unconditional trace-distance/total-error upper bound, not a noise estimate.

    Half-diamond tolerances must hold for COMPLETE channels, uniformly over
    classical transcripts and arbitrary reference systems. Single marginals
    or accepted-only branches cannot substitute for these promises.
    """
    values = (ideal_abort,joint_input_distance,measurement_half_diamond,
              action_half_diamond,control_preparation_distance,classical_clock_abort)
    if any(type(x) is not Fraction or not 0<=x<=1 for x in values):
        raise ValueError("exact Fraction error allowances between zero and one required")
    if any(type(n) is not int or n<0 for n in (measurement_calls,action_calls)):
        raise ValueError("nonnegative integer complete-channel call counts required")
    hybrid = joint_input_distance+measurement_calls*measurement_half_diamond
    hybrid += action_calls*action_half_diamond+control_preparation_distance
    total = ideal_abort+hybrid+classical_clock_abort
    return {"unconditional_hybrid_distance":hybrid,"total_error_upper":min(Fraction(1),total),
            "unclipped_sum":total,"acceptance_probability_division_used":False,
            "assumptions_verified_by_calculator":False}


def _cyclic_output(density, order):
    """Finite falsifier only: two slots with the same controlled translation."""
    out = np.zeros((order,order),dtype=complex)
    for q in range(order):
        for r in range(order):
            g = (q-r)%order
            out[q,r] = sum(density[((x+g)%order)*order+(y+g)%order,x*order+y]
                           for x in range(order) for y in range(order))/order
    return out


def _trace_distance(a,b):
    return float(np.abs(np.linalg.eigvalsh(a-b)).sum()/2)


def correlation_falsifier():
    """Correct one-copy marginals do not justify tensor correlation factoring."""
    p = 3
    correlated = np.array([[int((x-u-y+v)%p==0)/p**2
                            for u in range(p) for v in range(p)]
                           for x in range(p) for y in range(p)],dtype=complex)
    independent = np.eye(p*p)/p**2
    marginal_a = np.trace(correlated.reshape(p,p,p,p),axis1=1,axis2=3)
    marginal_b = np.trace(correlated.reshape(p,p,p,p),axis1=0,axis2=2)
    ideal = np.eye(p)/p
    wrong = _cyclic_output(correlated,p)
    return {"control":"same_marginals_are_not_independent_sources","dimension":p,
            "joint_trace":float(np.trace(correlated).real),
            "joint_min_eigenvalue":float(np.linalg.eigvalsh(correlated).min()),
            "marginal_a_error":float(np.max(np.abs(marginal_a-ideal))),
            "marginal_b_error":float(np.max(np.abs(marginal_b-ideal))),
            "independent_output_error":float(np.max(np.abs(_cyclic_output(independent,p)-ideal))),
            "correlated_output_trace_distance":_trace_distance(wrong,ideal),
            "correlated_output_real":wrong.real.tolist(),"ideal_output_real":ideal.tolist(),
            "character_cancellation_alone_is_sufficient":False,
            "finite_control_is_algorithm_discovery":False}


def postselection_falsifier():
    alpha,delta = Fraction(1,100),Fraction(1,1000)
    # Coordinates are abort, accept-good and accept-bad. Both full states
    # are normalized; the accepted branch alone has trace alpha.
    ideal = (1-alpha,alpha,Fraction(0))
    perturbed = (1-alpha,alpha-delta,delta)
    distance = sum(abs(a-b) for a,b in zip(ideal,perturbed))/2
    return {"acceptance_probability":alpha,"unconditional_distance":distance,
            "conditional_distance":delta/alpha,"unconditional_budget_survives":distance==delta,
            "accepted_only_error_bound_without_division_is_valid":False}


def policy_side_information_falsifier():
    """A classical choice table alone cannot exclude source-steering advice."""
    p = 3
    ideal = np.eye(p)/p
    correlated = np.zeros((p,p),dtype=complex)
    independent = np.zeros_like(correlated)
    source = np.zeros_like(correlated)
    for k in range(p):
        vector = np.exp(2j*np.pi*k*np.arange(p)/p)/np.sqrt(p)
        rho = np.outer(vector,vector.conj())
        source += rho/p
        scale = 1 if k!=2 else 2
        for q in range(p):
            for r in range(p):
                g = scale*(q-r)%p
                correlated[q,r] += sum(rho[(x+g)%p,x] for x in range(p))/p**2
                independent[q,r] += sum(ideal[(x+g)%p,x] for x in range(p))/p**2
    return {"control":"source_correlated_policy_coins_are_not_private_randomness",
            "source_marginal_error":float(np.max(np.abs(source-ideal))),
            "choice_scale_counts":[2,1],"choice_denominator":3,
            "independent_choice_output_error":float(np.max(np.abs(independent-ideal))),
            "source_correlated_choice_output_trace_distance":_trace_distance(correlated,ideal),
            "source_correlated_choice_output_real":correlated.real.tolist(),
            "source_correlated_choice_output_imag":correlated.imag.tolist(),
            "conditional_choice_table_alone_is_sufficient":False,
            "finite_control_is_algorithm_discovery":False}


def report():
    pilots = pilot_report()
    histories = [(c["name"],c["result"]) for c in pilots["cases"]]
    histories += [(name,pilots[name]) for name in ("incomplete_pilot_retry_control","zero_support_control")]
    return {"status":"CHECKED_CLASSICAL_POLICY_NOT_QUANTUM_IMPLEMENTATION",
            "source_artifact":"research/reductions/pilot_module_descent.json",
            "plans":[dict(name=name,plan=compile_receiver_plan(history)) for name,history in histories],
            "correlation_falsifier":correlation_falsifier(),
            "postselection_falsifier":postselection_falsifier(),
            "policy_side_information_falsifier":policy_side_information_falsifier(),
            "proof_note":"research/PILOT_RECEIVER_POLICY.md",
            "quantum_receiver_executed":False,"speedup_established":False}
