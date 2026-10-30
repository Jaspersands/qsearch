"""Fresh-pilot public-label controller with mandatory ambient verification.

Callbacks supply measured labels, not physical state handles. Quantum
measurement, IID physics, source ownership and receiver execution remain
external obligations. An incomplete pilot frame may safely succeed.
"""
from fractions import Fraction
import random

from theorems.pilot_submodule import compile_pilot_frame
from theorems.prime_power_rees_descent import _module_contract, verify_module_witness
from theorems.span_regular_sde import span_backend_rng, span_grade_plan, spanning_module_witness


class _OutsidePilotFrame(Exception):
    pass


def _preflight(prime, ambient_exponents, degree, failure_bits, draw_labels, bit_source):
    exponents = tuple(ambient_exponents)
    _module_contract([(0,)*len(exponents)],exponents,prime,degree)
    if not callable(draw_labels):
        raise ValueError("draw_labels callback required")
    plan = span_grade_plan(prime=prime,cyclic_rank=len(exponents),degree=degree,failure_bits=failure_bits)
    return exponents,plan,span_backend_rng(plan,bit_source)


def pilot_module_episode(*, prime, ambient_exponents, degree, draw_labels,
                         bit_source=None, failure_bits=8):
    """One episode. Rejection never silently refreshes or extends its pilots."""
    exponents,plan,rng = _preflight(prime,ambient_exponents,degree,failure_bits,draw_labels,bit_source)
    requests = []
    result = {"status":"ABORT","prime":prime,"degree":degree,"ambient_exponents":exponents,
              "ambient_plan":plan,"requests":requests,"source_labels_consumed":0,
              "public_label_pilot_coordinates_implemented":True,
              "physical_pilot_measurements_executed":False,"quantum_receiver_executed":False,
              "hidden_support_completeness_certified":False,"physical_iid_source_certified":False}

    def acquire(count,stage):
        columns,_,_ = _module_contract(draw_labels(count),exponents,prime,degree)
        if len(columns)!=count:
            raise ValueError("label source returned wrong requested count")
        requests.append({"stage":stage,"count":count,"ambient_columns":columns})
        result["source_labels_consumed"] += count
        if result["source_labels_consumed"]>plan["predecessors_per_episode_upper"]:
            raise ArithmeticError("episode exceeded its uniform source cap")
        return columns

    pilots = acquire(len(exponents)+2,"pilots")
    frame = compile_pilot_frame(prime=prime,ambient_exponents=exponents,pilot_columns=pilots)
    result["frame"] = frame.certificate()

    def intrinsic_draw(width):
        columns = acquire(width,"bank")
        encoded = [frame.encode(column) for column in columns]
        requests[-1]["intrinsic_columns"] = encoded
        if any(c is None for c in encoded):
            requests[-1]["status"] = "OUTSIDE_PILOT_FRAME"
            raise _OutsidePilotFrame
        requests[-1]["status"] = "MEMBERSHIP_VERIFIED"
        return encoded

    if not frame.intrinsic_exponents:
        column = acquire(1,"zero_rank_bank")[0]
        if any(column):
            result["reason"] = "nonzero bank label outside zero-rank pilot frame"
            return result
        selected,scales = [column],[1]
        result["selected_request_indices"] = [1]
        result["zero_rank_branch"] = True
    else:
        try:
            inner = spanning_module_witness(prime=prime,exponents=frame.intrinsic_exponents,
                degree=degree,draw_block=intrinsic_draw,bit_source=rng,failure_bits=failure_bits,
                ambient_cyclic_rank=len(exponents))
        except _OutsidePilotFrame:
            result["reason"] = "bank label outside pilot-generated subgroup"
            return result
        result["intrinsic_run"] = inner
        if inner["source_columns_consumed"]!=sum(row["count"] for row in requests[1:]):
            raise ArithmeticError("intrinsic/ambient source accounting mismatch")
        if inner["status"]!="VERIFIED_SPANNING_MODULE_WITNESS":
            result["reason"] = inner["reason"]
            return result
        indices = [i+1 for i in inner["accepted_trial_indices"]]
        if len(indices)!=len(set(indices)) or any(not 1<=i<len(requests) for i in indices):
            raise ArithmeticError("invalid raw-source selection provenance")
        selected = [c for i in indices for c in requests[i]["ambient_columns"]]
        embedded = [frame.decode(c) for c in inner["raw_columns"]]
        if selected!=embedded:
            raise ArithmeticError("selected raw sources failed original ambient embedding")
        scales = inner["lift"]["scales"]
        result["selected_request_indices"] = indices
        result["zero_rank_branch"] = False

    if not verify_module_witness(selected,scales,prime=prime,exponents=exponents,degree=degree):
        raise ArithmeticError("final cancellation failed original ambient module")
    result.update(status="VERIFIED_AMBIENT_MODULE_WITNESS",selected_ambient_columns=selected,
                  scales=scales,original_ambient_verified=True,
                  reason="exact ambient witness; quantum source/receiver not certified")
    return result


def pilot_module_search(*, prime, ambient_exponents, degree, draw_labels,
                        bit_source=None, failure_bits=8, episode_cap=2):
    """Capped whole-episode retries, always with new pilots and a new bank."""
    if type(episode_cap) is not int or episode_cap<1:
        raise ValueError("positive integer episode_cap required")
    exponents,plan,rng = _preflight(prime,ambient_exponents,degree,failure_bits,draw_labels,bit_source)
    failure = Fraction(3,16)**episode_cap
    result = {"status":"ABORT","episode_cap":episode_cap,"episodes":[],
              "source_labels_consumed":0,"source_labels_cap":episode_cap*plan["predecessors_per_episode_upper"],
              "conditional_all_episodes_abort_upper":[failure.numerator,failure.denominator],
              "fresh_iid_source_promise_required":True,"whole_workflow_clock_enforced":False,
              "public_label_pilot_coordinates_implemented":True,"quantum_receiver_executed":False,
              "speedup_established":False}
    for _ in range(episode_cap):
        episode = pilot_module_episode(prime=prime,ambient_exponents=exponents,degree=degree,
            draw_labels=draw_labels,bit_source=rng,failure_bits=failure_bits)
        result["episodes"].append(episode)
        result["source_labels_consumed"] += episode["source_labels_consumed"]
        if episode["status"]=="VERIFIED_AMBIENT_MODULE_WITNESS":
            result["status"] = episode["status"]
            result["successful_episode_index"] = len(result["episodes"])-1
            break
    if result["source_labels_consumed"]>result["source_labels_cap"]:
        raise ArithmeticError("whole search exceeded charged source cap")
    return result


def report():
    cases = []
    for name,p,es,generators,orders,seed in (
        ("ambient_mod_p_zero",3,(3,),[(3,)],(9,),301),
        ("oblique_mixed_order",3,(3,4),[(3,3),(0,9)],(27,9),302),
        ("cubic_embedded_support",7,(2,3),[(7,7),(7,0)],(49,7),303),
    ):
        labels = random.Random(seed)
        def draw(count):
            columns = []
            for _ in range(count):
                coefficients = [labels.randrange(order) for order in orders]
                columns.append(tuple(sum(a*g[j] for a,g in zip(coefficients,generators))%p**e
                                     for j,e in enumerate(es)))
            return columns
        value = pilot_module_search(prime=p,ambient_exponents=es,degree=2 if p==3 else 3,
                                    draw_labels=draw,bit_source=random.Random(seed+100),episode_cap=3)
        cases.append(dict(name=name,source_seed=seed,solver_seed=seed+100,
                          fixture_generators=generators,fixture_generator_orders=orders,result=value))
    # A deliberately incomplete frame must abort; the next episode gets new pilots.
    stream = iter([[(0,)]*3,[(3,)],[(3,)]*3]+[[(3,)]*2]*4)
    retry = pilot_module_search(prime=3,ambient_exponents=(2,),degree=2,
        draw_labels=lambda count:next(stream),bit_source=random.Random(1),episode_cap=2)
    zero = pilot_module_search(prime=3,ambient_exponents=(2,3),degree=2,
        draw_labels=lambda count:[(0,0)]*count,episode_cap=1)
    return {"status":"PUBLIC_LABEL_CONTROLLER_NOT_QUANTUM_RECEIVER","cases":cases,
            "incomplete_pilot_retry_control":retry,"zero_support_control":zero,
            "proof_note":"research/PILOT_SUBMODULE_COORDINATES.md",
            "public_label_pilot_coordinates_implemented":True,
            "quantum_receiver_executed":False,"physical_iid_source_certified":False,
            "normal_form_backend_bit_complexity_certified":False,"speedup_established":False}
