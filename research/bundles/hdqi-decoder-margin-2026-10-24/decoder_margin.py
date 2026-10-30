"""Conditional nonlinear-decoder readout reductions, not an executed FPRAS."""

from fractions import Fraction as F
from itertools import combinations
import math
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "hdqi-decoded-observables-2026-10-24"))
import decoded_observables as d
sys.path.insert(0, str(BASE / "hdqi-defect-observables-2026-10-24"))
import defect_observables as defect


def exact(value):
    if isinstance(value, bool) or not isinstance(value, (int, F)):
        raise ValueError("exact integer or Fraction required")
    return F(value)


def radius_check(model, radius):
    if type(radius) is not int or not 0 <= radius <= model.pilot.m:
        raise ValueError("radius outside the generator register")


def tail_bound(model, cutoff):
    """Factorial-moment bound on Pr[|Y|>cutoff], not independence of Y bits."""
    m = model.pilot.m
    if type(cutoff) is not int:
        raise ValueError("integer cutoff required")
    if cutoff < 0:
        return F(1)
    if cutoff >= m:
        return F(0)
    threshold = cutoff + 1
    coefficients = [F(1)] + [F(0)] * threshold
    for i, j in enumerate(model.pilot.couplings):
        q = (model.pilot.beta*j/2)**2
        for k in range(min(i+1, threshold), 0, -1):
            coefficients[k] += q * coefficients[k-1]
    return min([F(1)] + [coefficients[k] / math.comb(threshold, k)
                         for k in range(1, threshold+1)])


def recommended_cutoff(model, epsilon):
    epsilon = exact(epsilon)
    if not 0 < epsilon <= F(1, 4):
        raise ValueError("need 0<epsilon<=1/4")
    mass = sum(((model.pilot.beta*j/2)**2 for j in model.pilot.couplings), F(0))
    bits = 0
    while F(1, 1 << bits) > epsilon**2/256:
        bits += 1
    return min(model.pilot.m, max(1, math.ceil(6*mass), bits)-1)


def verify_ball(model, decoder, radius, max_masks=100000):
    """Exhaustive finite contract check; never infer an all-size decoder theorem."""
    radius_check(model, radius)
    count = sum(math.comb(model.pilot.m, k) for k in range(radius+1))
    if type(max_masks) is not int or max_masks < 1 or count > max_masks:
        raise ValueError("decoder ball audit exceeds explicit mask cap")
    checked = 0
    for k in range(radius+1):
        for subset in combinations(range(model.pilot.m), k):
            y = sum(1 << i for i in subset)
            answer = decoder(model.label(y))
            checked += 1
            if type(answer) is not int or answer != y:
                return {"status": "REJECTED", "radius": radius, "checked": checked,
                        "witness": y, "syndrome": model.label(y), "decoded": answer}
    return {"status": "FINITE_EXHAUSTIVE_CHECK", "radius": radius, "checked": checked,
            "all_size_proof": False}


def lift(model, observable, word):
    d.validate_pauli(model.n, observable)
    if type(word) is not int or not 0 <= word < 1 << model.pilot.m:
        raise ValueError("word outside generator register")
    physical = model.ordered(word)
    if physical[:2] != observable[:2]:
        raise ValueError("word does not represent the physical observable label")
    phase = (observable[2] - physical[2]) % 4
    host = defect.c.Host.create(model.pilot.m, model.pilot.edges)
    result = (word, defect.ell(host, word), phase)
    d.validate_pauli(model.pilot.m, result)
    return result


def _backend(model, lifted, epsilon):
    host = defect.c.Host.create(model.pilot.m, model.pilot.edges)
    return defect.pauli_plan(host, model.pilot.couplings, model.pilot.beta,
                             lifted, epsilon/2)


def _base(model, radius, cutoff, epsilon, factor):
    radius_check(model, radius)
    epsilon = exact(epsilon)
    if not 0 < epsilon <= F(1, 4):
        raise ValueError("need 0<epsilon<=1/4")
    tail = tail_bound(model, cutoff)
    squared_error = min(F(4), factor*factor*tail)
    return {"status": "CONDITIONAL_ON_UNIFORM_DECODER_CONTRACT",
            "decoder_radius_required": radius, "pilot_cutoff": cutoff,
            "tail_probability_upper": tail,
            "transfer_error_squared_upper": squared_error,
            "transfer_budget_met": squared_error <= epsilon**2/4,
            "epsilon": epsilon, "decoder_contract_verified_by_plan": False,
            "production_estimator_executed": False, "independent_review": False,
            "target": "actual decoded output, not an assumed Gibbs state",
            "full_output_sampling": False, "quantum_advantage_claim": False}


def short_word_plan(model, observable, word, decoder_radius, epsilon=F(1, 8)):
    """Assumes Dec(By)=y for EVERY weight<=radius input, not just typical y."""
    lifted = lift(model, observable, word)
    cutoff = decoder_radius - word.bit_count()
    result = _base(model, decoder_radius, cutoff, epsilon, 2)
    result.update(route="short_word", lifted_pauli=lifted,
                  canonical_plan=_backend(model, lifted, result["epsilon"]))
    result["classical_reduction_budget_met"] = (result["transfer_budget_met"]
        and result["canonical_plan"]["status"] != "inconclusive_outside_cluster_regime")
    return result


def arbitrary_pauli_plan(model, decoder, observable, decoder_radius,
                         cutoff=None, epsilon=F(1, 8)):
    d.validate_pauli(model.n, observable)
    if cutoff is None:
        cutoff = recommended_cutoff(model, epsilon)
    result = _base(model, decoder_radius, cutoff, epsilon, 4)
    result.update(route="arbitrary_pauli", classical_reduction_budget_met=False)
    if cutoff < 0 or 2*cutoff > decoder_radius:
        result.update(status="INCONCLUSIVE_INSUFFICIENT_DECODING_MARGIN",
                      required_radius_for_cutoff=2*cutoff)
        return result
    syndrome = observable[0] | (observable[1] << model.n)
    word = decoder(syndrome)
    if type(word) is not int or not 0 <= word < 1 << model.pilot.m:
        raise ValueError("decoder must be total and return an m-bit mask")
    if model.label(word) != syndrome or word.bit_count() > 2*cutoff:
        result.update(lifted_pauli=None,
                      canonical_plan={"status": "zero_on_truncated_ball", "estimate": 0})
    else:
        lifted = lift(model, observable, word)
        result.update(lifted_pauli=lifted,
                      canonical_plan=_backend(model, lifted, result["epsilon"]))
    result["classical_reduction_budget_met"] = (result["transfer_budget_met"]
        and result["canonical_plan"]["status"] != "inconclusive_outside_cluster_regime")
    return result
