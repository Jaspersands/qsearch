"""Residue subset completion and regular mixed-order lifting.

This executes public-label arithmetic, not a quantum receiver. Probability
bounds require fresh IID sources; accepted data cannot certify that premise.
"""
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import random

from theorems.pilot_submodule import compile_pilot_frame
from theorems.prime_power_rees_descent import (
    _module_contract, lift_regular_module_witness, verify_module_witness,
)
from theorems.regular_subset_sum import regular_subset_witness, subset_sum_moments
from theorems.unit_power_module import unit_tree_source_bound


def _positive(value, name):
    if type(value) is not int or value < 1:
        raise ValueError(f"positive integer {name} required")
    return value


def subset_module_plan(*, prime, degree, cyclic_rank_bound, failure_bits=8,
                       max_states=None):
    """A fixed acquisition clock; a smaller DP cap loses the source guarantee."""
    R = _positive(cyclic_rank_bound, "cyclic rank bound")
    b = _positive(failure_bits, "failure bits")
    _module_contract([(0,)], (1,), prime, degree)
    states = prime**R
    cap = states if max_states is None else _positive(max_states, "state cap")
    prefix = pilots = R+b+2
    suffix = R*(prime-1).bit_length()+b+2
    rank_failure = Fraction(1, (prime-1)*prime**(prefix-R))
    pilot_failure = Fraction(1, (prime-1)*prime**(pilots-R))
    moments = subset_sum_moments(prime, R, suffix)
    subset_failure = Fraction(prime**R, (1 << suffix)-1)
    ideal_bound = pilot_failure+rank_failure+subset_failure
    if ideal_bound > Fraction(1, 1 << b):
        raise ArithmeticError("subset episode failure allocation is invalid")
    return dict(
        prime=prime, degree=degree, cyclic_rank_bound=R, failure_bits=b,
        pilot_source_count=pilots, prefix_source_count=prefix,
        suffix_source_count=suffix, bank_source_count=prefix+suffix,
        source_labels_cap=pilots+prefix+suffix,
        complete_dp_state_bound=states, dp_state_cap=cap,
        complete_state_cap_met=cap >= states,
        pilot_incompleteness_bound=pilot_failure,
        prefix_rank_failure_bound=rank_failure,
        iid_subset_absence_bound=subset_failure, suffix_moments=moments,
        ideal_uncapped_episode_abort_bound=ideal_bound,
        episode_abort_bound=ideal_bound if cap >= states else Fraction(1),
        fresh_iid_source_required=True, source_law_certified=False,
        normal_form_clock_certified=False, quantum_receiver_implemented=False,
    )


def subset_module_witness(columns, *, prime, exponents, degree, prefix_count,
                          max_states=None):
    """Find a regular Boolean residue witness and freeze all zeros while lifting."""
    columns, exponents, _ = _module_contract(columns, exponents, prime, degree)
    field = regular_subset_witness(
        [tuple(x % prime for x in col) for col in columns], prime=prime,
        degree=degree, prefix_count=prefix_count, max_states=max_states)
    result = dict(status="ABORT", reason=field.get("reason"), scales=None,
                  bank_columns=columns, exponents=exponents, original_degree=degree,
                  field_run=field, labels_resampled=False,
                  source_law_certified=False, quantum_receiver_implemented=False)
    if field["status"] != "VERIFIED_REGULAR_SUBSET_WITNESS":
        return result
    weights = list(field["scales"])
    if not any(weights) or any(type(x) is not int or x not in (0, 1) for x in weights):
        raise ArithmeticError("subset solver did not return a nonzero Boolean witness")
    lifted = lift_regular_module_witness(columns, weights, prime=prime,
                                        exponents=exponents, degree=degree)
    if (not lifted["original_module_verified"]
            or any(lifted["scales"][i] != 0 for i, w in enumerate(weights) if w == 0)):
        raise ArithmeticError("regular lift lost cancellation or an exact zero")
    result.update(status="VERIFIED_REGULAR_SUBSET_MODULE_WITNESS",
                  reason="EXACT_MIXED_ORDER_CANCELLATION", lift=lifted,
                  field_witness_original_degree=weights, scales=lifted["scales"])
    return result


def subset_pilot_episode(*, prime, ambient_exponents, degree, draw_labels,
                         failure_bits=8, max_states=None, cyclic_rank_bound=None):
    """Charge fresh pilots and a complete bank, including unused/aborted slots.

    A supplied cyclic rank bound concerns the hidden support, not the ambient
    factor count. Its validity is a premise, never certified by finite pilots.
    Source callbacks and normal-form arithmetic are not wall-clocked here.
    Canonical membership/rank/search failures abort. Backend defects raise.
    """
    exponents = tuple(ambient_exponents)
    _module_contract([(0,)*len(exponents)], exponents, prime, degree)
    rank_bound = len(exponents) if cyclic_rank_bound is None else cyclic_rank_bound
    plan = subset_module_plan(prime=prime, degree=degree,
                              cyclic_rank_bound=rank_bound, failure_bits=failure_bits,
                              max_states=max_states)
    if not callable(draw_labels):
        raise ValueError("finite label-bank callback required")
    requests = []
    result = dict(status="ABORT", reason=None, scales=None, plan=plan, requests=requests,
                  source_labels_consumed=0, hidden_support_completeness_certified=False,
                  hidden_support_rank_bound_certified=False,
                  physical_iid_source_certified=False, quantum_receiver_implemented=False,
                  normal_form_clock_certified=False)

    def acquire(count, stage):
        raw = draw_labels(count)
        if not isinstance(raw, (list, tuple)) or len(raw) != count:
            raise ValueError("source must return exactly the requested finite bank")
        columns, _, _ = _module_contract(raw, exponents, prime, degree)
        requests.append(dict(stage=stage, count=count, ambient_columns=columns))
        result["source_labels_consumed"] += count
        return columns

    pilots = acquire(plan["pilot_source_count"], "pilots")
    frame = compile_pilot_frame(prime=prime, ambient_exponents=exponents, pilot_columns=pilots)
    result["frame"] = frame.certificate()
    bank = acquire(plan["bank_source_count"], "prefix_and_independent_suffix")
    if len(frame.intrinsic_exponents) > rank_bound:
        result["reason"] = "PILOT_RANK_EXCEEDS_BOUND"
        return result
    encoded = [frame.encode(col) for col in bank]
    requests[-1]["intrinsic_columns"] = encoded
    if any(col is None for col in encoded):
        result["reason"] = "OUTSIDE_PILOT_FRAME"
        return result
    if [frame.decode(col) for col in encoded] != list(bank):
        raise ArithmeticError("pilot embedding did not recover original bank")
    if not frame.intrinsic_exponents:
        scales = [1]+[0]*(len(bank)-1)
        result["zero_rank_branch"] = True
    else:
        inner = subset_module_witness(
            encoded, prime=prime, exponents=frame.intrinsic_exponents,
            degree=degree, prefix_count=plan["prefix_source_count"],
            max_states=plan["dp_state_cap"])
        result["intrinsic_run"] = inner
        if inner["status"] != "VERIFIED_REGULAR_SUBSET_MODULE_WITNESS":
            result["reason"] = inner["reason"]
            return result
        scales = inner["scales"]
        result["zero_rank_branch"] = False
    if not verify_module_witness(bank, scales, prime=prime, exponents=exponents, degree=degree):
        raise ArithmeticError("subset witness failed original ambient verification")
    if result["source_labels_consumed"] != plan["source_labels_cap"]:
        raise ArithmeticError("fixed episode source clock mismatch")
    result.update(status="VERIFIED_AMBIENT_REGULAR_SUBSET_WITNESS",
                  reason="EXACT_AMBIENT_CANCELLATION", scales=scales,
                  selected_request_indices=[1], selected_ambient_columns=bank,
                  original_ambient_verified=True)
    return result


def all_prime_module_tree_bound(*, prime, class_bound, cyclic_rank_bound,
                                uniform_parameter):
    """Both odd-prime regimes with c<p, not a complete ring HSP theorem."""
    c = _positive(class_bound, "class bound")
    R = _positive(cyclic_rank_bound, "cyclic rank bound")
    u = _positive(uniform_parameter, "uniform parameter")
    if c < 2 or u < max(c, R+1, 2):
        raise ValueError("2<=class_bound<=u and cyclic_rank_bound<u required")
    _module_contract([(0,)], (1,), prime, c)
    if prime >= 16*u*u:
        result = unit_tree_source_bound(prime=prime, class_bound=c,
                                        cyclic_rank_bound=R, uniform_parameter=u)
        result.update(regime="LARGE_PRIME_UNIT_KERNEL", all_prime_branch_coverage=True,
                      prime=prime, class_bound=c, cyclic_rank_bound=R, uniform_parameter=u,
                      class_strictly_below_prime_required=True,
                      uniform_branch_tree_abort_bound=Fraction(1, 16),
                      small_prime_state_enumeration_used=False)
        return result
    ell = (16*u-1).bit_length()
    bits = 4*u*ell
    stages = []
    for grade in range(2, c+1):
        plan = subset_module_plan(prime=prime, degree=grade, cyclic_rank_bound=R,
                                  failure_bits=bits)
        width = plan["source_labels_cap"]
        stages.append(dict(grade=grade, nodes=width**(grade-2), plan=plan))
    width = stages[0]["plan"]["source_labels_cap"]
    if any(s["plan"]["source_labels_cap"] != width for s in stages):
        raise ArithmeticError("grade-independent arity was lost")
    leaves = width**(c-1)
    failure = sum((s["nodes"]*s["plan"]["episode_abort_bound"] for s in stages), Fraction(0))
    if width > 16*u*ell or width > 1 << (2*ell) or failure > Fraction(1, 64):
        raise ArithmeticError("small-prime tree envelope failed")
    return dict(
        status="CONDITIONAL_MIXED_ORDER_SOURCE_TREE_NOT_HSP_BOUND",
        regime="SMALL_PRIME_REGULAR_SUBSET", all_prime_branch_coverage=True,
        class_strictly_below_prime_required=True,
        uniform_branch_tree_abort_bound=Fraction(1, 16),
        prime=prime, class_bound=c, cyclic_rank_bound=R, uniform_parameter=u,
        field_threshold=16*u*u, parameter_log_bound=ell,
        raw_arity_per_grade=width, leaves_per_output_tree=leaves,
        failure_bits_per_node=bits, tree_abort_bound=failure, stages=stages,
        dp_states_per_node_upper=prime**R,
        dp_transition_upper=sum(s["nodes"]*s["plan"]["suffix_source_count"]*prime**R
                                for s in stages),
        small_prime_state_enumeration_used=True, discarded_pilots_charged=True,
        pointwise_source_composition_required=True, original_oracle_queries_included=False,
        quantum_receiver_implemented=False, all_prime_ring_hsp_bound=False,
        complete_quantum_error_accounting_included=False,
        class_bounded_by_derived_cyclic_rank=False, novelty_established=False,
    )


def report():
    """Fixed public-label controls, not sampled or executed quantum states."""
    cases = []
    for name, p, exponents, generators, orders, degree, seed in (
        ("ambient_mod_p_zero", 3, (4,), [(3,)], (27,), 2, 30031),
        ("p5_quadratic_oblique", 5, (2, 3), [(1, 5), (0, 25)], (25, 5), 2, 50032),
        ("p5_quartic_oblique", 5, (2, 3), [(1, 5), (0, 25)], (25, 5), 4, 50034),
    ):
        rng = random.Random(seed)

        def draw(count):
            out = []
            for _ in range(count):
                coefficients = [rng.randrange(order) for order in orders]
                out.append(tuple(sum(a*g[j] for a, g in zip(coefficients, generators)) % p**e
                                 for j, e in enumerate(exponents)))
            return out

        result = subset_pilot_episode(prime=p, ambient_exponents=exponents, degree=degree,
                                      draw_labels=draw, failure_bits=8)
        cases.append(dict(name=name, seed=seed, original_degree=degree, result=result,
                          generator_columns=generators, generator_orders=orders,
                          randomness="SEEDED_CLASSICAL_CONTROL_NOT_CERTIFIED_IID_SOURCE"))
    root = Path(__file__).resolve().parents[1]
    sources = (
        "theorems/regular_subset_sum.py", "theorems/small_prime_module.py",
        "tests/test_regular_subset_sum.py", "tests/test_small_prime_module.py",
        "theorems/pilot_submodule.py", "theorems/prime_power_rees_descent.py",
        "theorems/unit_power_module.py", "research/SMALL_PRIME_REGULAR_SUBSET.md",
    )
    return dict(
        status="CLASSICAL_REGULAR_SUBSET_CONTROLS_NOT_QUANTUM_RECEIVER",
        cases=cases, source_sha256={p: sha256((root/p).read_bytes()).hexdigest() for p in sources},
        source_trees=[all_prime_module_tree_bound(prime=p, class_bound=c,
                                                  cyclic_rank_bound=R, uniform_parameter=u)
                      for p, c, R, u in ((5, 4, 2, 4), (1009, 3, 2, 3))],
        quantum_receiver_implemented=False, iid_source_certified=False,
        all_prime_ring_hsp_bound=False, speedup_claim_allowed=False,
        candidate_promotion=False, proof_promotion=False,
    )
