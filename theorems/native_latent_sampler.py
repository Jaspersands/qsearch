"""Constructive native latent-constraint sampler and exact rare-event audit.

The analytical certificates are polynomial-bit calculations. The named
finite audit enumerates a capped code only to falsify the identities. Neither
constitutes classical hardness or a polynomial full-witness solver.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
from itertools import product
import json
from math import comb
from pathlib import Path

from theorems.balanced_filter_channel_audit import _fixture, _integer
from theorems.folded_balanced_filter import _solve, native_budget
from theorems.inverse_trace_gibbs_target import _ceil_log2, _ceiling, _floor, reciprocal_bound

ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "research/NATIVE_LATENT_SAMPLER.md"
REPORT = ROOT / "research/classical_baselines/native_latent_sampler.json"


def binomial_weights(length, probability):
    """Integer weights with a shared denominator; no floating-point tails."""
    _integer(length, 1, 10000, "length")
    if type(probability) not in (int, Q) or not 0 <= probability <= 1:
        raise ValueError("rational binomial probability required")
    p = Q(probability)
    a, b = p.numerator, p.denominator-p.numerator
    return [comb(length, j)*a**j*b**(length-j) for j in range(length+1)]


def latent_budget(length, remaining, base, eta):
    _integer(length, 1, 10000, "length")
    _integer(remaining, 1, length, "remaining unchecked predicates")
    if type(base) not in (int, Q) or base < 1:
        raise ValueError("rational inverse-temperature base at least one required")
    if type(eta) not in (int, Q) or eta < 0:
        raise ValueError("nonnegative rational fiber error required")
    base, eta = Q(base), Q(eta)
    cutoff, p = length-remaining, (base-1)/(base+1)
    weights = binomial_weights(length, p)
    retained = Q(sum(weights[:cutoff+1]), sum(weights))
    tail = 1-retained
    theta = (base-1)/base
    witness_weights = binomial_weights(length, theta)
    witness_retained = Q(sum(witness_weights[:cutoff+1]), sum(witness_weights))
    ideal_factor = (base/(base+1))**length
    native_factor = ideal_factor*witness_retained/retained
    return {"length": length, "remaining": remaining, "cutoff": cutoff,
            "base": base, "active_probability": p,
            "retained_proposal_mass": retained, "discarded_proposal_mass": tail,
            "witness_conditioned_active_probability": theta,
            "witness_conditioned_retained_mass": witness_retained,
            "sampler_tv_upper": (1+eta)*tail/(1+eta*tail),
            "native_success_divided_by_relative_fiber_count": native_factor,
            "native_success_upper": min(Q(1), (1+eta)*native_factor),
            "native_success_lower": max(Q(0), (1-eta)*native_factor),
            "any_feasible_latent_mixture_success_upper": min(Q(1), (1+eta)/(1 << remaining)),
            "relative_native_event_capture_upper": min(Q(1), (1+eta*tail)*witness_retained/retained),
            "ideal_gibbs_native_success_lower": max(Q(0), (1-eta)*ideal_factor/(1+eta*tail)),
            "rejection_latent_draws_expected": 1/retained,
            "direct_truncated_draw_has_rejection_overhead": False}


def draw_active_set(length, cutoff, base, rng):
    """Direct exact truncated-binomial draw, not rejection of rare subsets.

    rng supplies unbiased randrange/sample operations. The theorem uses
    random bits; a seeded pseudorandom generator is only a reproducible pilot.
    """
    _integer(cutoff, 0, length, "active cutoff")
    if type(base) not in (int, Q) or base < 1:
        raise ValueError("rational inverse-temperature base at least one required")
    p = (Q(base)-1)/(Q(base)+1)
    weights = binomial_weights(length, p)[:cutoff+1]
    ticket = rng.randrange(sum(weights))
    for size, weight in enumerate(weights):
        if ticket < weight:
            return tuple(sorted(rng.sample(range(length), size)))
        ticket -= weight
    raise ArithmeticError("integer truncated-binomial sampling lost mass")


def scalar_conditional_draw(context, bits, points, checks, targets, syndrome, active, draw_bits):
    """Uniform native codeword conditional on a tractable active set.

    Uses the caller's PUBLIC FLINT binary field, no field table and no witness.
    All K pivot columns lie outside the active set. This reference recomputes
    elimination on each draw; polynomial preprocessing can be cached later.
    """
    points, targets, syndrome, active = tuple(points), tuple(targets), tuple(syndrome), tuple(active)
    _integer(bits, 2, 128, "field bits")
    length, q = len(points), 1 << bits
    _integer(length, 2, min(q, 10000), "length")
    _integer(checks, 1, length-1, "checks")
    if len(context.modulus().coeffs()) != bits+1 or int(context.characteristic()) != 2:
        raise ValueError("public context must be the specified binary field")
    if len(set(points)) != length or any(type(x) is not int or not 0 <= x < q for x in points):
        raise ValueError("distinct canonical public points required")
    if len(targets) != length or any(type(b) is not int or b not in (0, 1) for b in targets):
        raise ValueError("one target bit per coordinate required")
    if len(syndrome) != checks or any(type(x) is not int or not 0 <= x < q for x in syndrome):
        raise ValueError("one canonical public syndrome label per check required")
    if (len(set(active)) != len(active) or len(active) > length-checks
            or any(type(i) is not int or not 0 <= i < length for i in active)):
        raise ValueError("active set exceeds the exactly samplable projection domain")
    powers = [context.gen()**j for j in range(bits)]
    element = lambda x: sum((power for j, power in enumerate(powers) if x >> j & 1), context.zero())
    encode = lambda x: sum(int(c) << j for j, c in enumerate(x.to_list()))
    trace_pivot = next(j for j, power in enumerate(powers) if int(power.trace()) == 1)
    trace_free = [j for j in range(bits) if j != trace_pivot]
    pivots = [i for i in range(length) if i not in active][:checks]
    free = [i for i in range(length) if i not in pivots]
    rows = [[element(a)**j for a in points] for j in range(checks)]
    word = [context.zero() for _ in points]
    for i in free:
        width = bits-1 if i in active else bits
        label = draw_bits(width)
        _integer(label, 0, (1 << width)-1, "random-bit draw")
        if i in active:
            u = sum((powers[j] for k, j in enumerate(trace_free) if label >> k & 1), context.zero())
            u += powers[trace_pivot]*(targets[i] ^ int(u.trace()))
            word[i] = context.zero() if u == 0 else u**-1
        else:
            word[i] = element(label)
    rhs = [element(y)-sum((row[i]*word[i] for i in free), context.zero())
           for row, y in zip(rows, syndrome)]
    solved = _solve(context, [[row[i] for i in pivots] for row in rows], rhs, checks)
    if solved is None or solved[1] != checks:
        raise ArithmeticError("public Vandermonde pivot solve failed")
    solution, _ = solved
    for i, x in zip(pivots, solution):
        word[i] = x
    if any(sum((a*x for a, x in zip(row, word)), context.zero()) != element(y)
           for row, y in zip(rows, syndrome)):
        raise ArithmeticError("conditional draw escaped the public syndrome")
    if any((0 if word[i] == 0 else int((word[i]**-1).trace())) != targets[i] for i in active):
        raise ArithmeticError("conditional draw violated an active predicate")
    return tuple(map(encode, word))


def finite_audit(bits, length, checks, targets, base, offset=0):
    """Exact capped laws, including partition tilt and the full native event."""
    data = _fixture(bits, length, checks, 0)
    _integer(offset, 0, data["size"]-1, "public offset")
    if len(targets) != length or any(type(b) is not int or b not in (0, 1) for b in targets):
        raise ValueError("one target bit per coordinate required")
    target = sum(b << i for i, b in enumerate(targets))
    labels = [data["target_masks"][x ^ offset] for x, valid in enumerate(data["native_code"]) if valid]
    size, cutoff = len(labels), length-checks
    lambdas = [Q(labels.count(c)*(1 << length), size) for c in range(1 << length)]
    eta = max(abs(v-1) for v in lambdas)
    budget = latent_budget(length, checks, base, eta)
    p, retained = budget["active_probability"], budget["retained_proposal_mass"]
    weights = [Q(base)**(length-(label ^ target).bit_count()) for label in labels]
    gibbs = [v/sum(weights) for v in weights]
    output = [Q(0) for _ in labels]
    for active in range(1 << length):
        count = active.bit_count()
        if count > cutoff:
            continue
        members = [i for i, label in enumerate(labels) if not ((label ^ target) & active)]
        if len(members)*(1 << count) != size:
            raise ArithmeticError("MDS active-set projection failed")
        mass = p**count*(1-p)**(length-count)/retained
        for i in members:
            output[i] += mass/len(members)
    truncated_weights = [sum((comb(length-(label ^ target).bit_count(), j)*(Q(base)-1)**j
                             for j in range(min(cutoff, length-(label ^ target).bit_count())+1)), Q(0))
                         for label in labels]
    normalizer = size*((Q(base)+1)/2)**length*retained
    if sum(truncated_weights) != normalizer or output != [v/normalizer for v in truncated_weights]:
        raise ArithmeticError("direct latent law differs from its truncated polynomial")
    partition_ratio = sum(weights)/(size*((Q(base)+1)/2)**length)
    for label, proposal, ideal in zip(labels, output, gibbs):
        matches = length-(label ^ target).bit_count()
        active_weights = binomial_weights(matches, (Q(base)-1)/Q(base)) if matches else [1]
        capture = Q(sum(active_weights[:cutoff+1]), sum(active_weights))
        if proposal/ideal != partition_ratio*capture/retained:
            raise ArithmeticError("pointwise match-count likelihood-ratio identity failed")
    tv = sum(abs(a-b) for a, b in zip(output, gibbs))/2
    native = sum(v for v, label in zip(output, labels) if label == target)
    ideal_native = sum(v for v, label in zip(gibbs, labels) if label == target)
    predicted = lambdas[target]*budget["native_success_divided_by_relative_fiber_count"]
    if (sum(output) != 1 or tv > budget["sampler_tv_upper"] or native != predicted
            or native > budget["any_feasible_latent_mixture_success_upper"]):
        raise ArithmeticError("latent law, success or TV certificate failed")
    capture = native/ideal_native if ideal_native else None
    if capture is not None and capture != partition_ratio*budget["witness_conditioned_retained_mass"]/retained:
        raise ArithmeticError("rare-event capture identity failed")
    return {"bits": bits, "length": length, "checks": checks, "targets": list(targets),
            "base": Q(base), "offset": offset, "enumerated_codewords": size,
            "relative_fiber_error": eta, "tv_exact": tv, "tv_upper": budget["sampler_tv_upper"],
            "native_success": native, "ideal_gibbs_native_success": ideal_native,
            "relative_native_event_capture": capture, "partition_ratio": partition_ratio,
            "pointwise_likelihood_ratios_checked": True,
            "all_tractable_active_sets_checked": True,
            "reference_has_polynomial_complexity": False}


def report():
    certificates = []
    for n in (17, 31, 61):
        length = n*n
        _, scalar_eta = reciprocal_bound(n, length, length//8)
        folded = native_budget(n)
        for family, remaining, eta, bases in (
            ("scalar", length//8, scalar_eta, (2, 10, length)),
            ("odd_folded_s67", folded["classical_accepted_completion_remaining_blocks"],
             folded["eta_outward_rounded_upper"], (2, 3, length)),
        ):
            for base in bases:
                row = latent_budget(length, remaining, base, eta)
                certificates.append({"family": family, "bits": n, "length": length,
                                     "remaining": remaining, "base": base,
                                     "tv_upper_power2": _ceil_log2(row["sampler_tv_upper"]),
                                     "native_success_upper_power2": _ceil_log2(row["native_success_upper"]),
                                     "relative_native_event_capture_upper_power2": _ceil_log2(row["relative_native_event_capture_upper"]),
                                     "retained_latent_mass_upper_power2": _ceil_log2(row["retained_proposal_mass"]),
                                     "ideal_gibbs_native_success_lower": _floor(row["ideal_gibbs_native_success_lower"]),
                                     "native_success_upper": _ceiling(row["native_success_upper"]),
                                     "direct_latent_draw_is_polynomial_bit_cost": True,
                                     "native_large_sampler_executed": False})
    controls = [finite_audit(2, 3, 1, targets, base, offset)
                for targets in product((0, 1), repeat=3) for base in (1, Q(3, 2), 10)
                for offset in range(4)]
    paths = [Path(__file__), NOTE, ROOT / "theorems/balanced_filter_channel_audit.py",
             ROOT / "theorems/folded_balanced_filter.py", ROOT / "theorems/inverse_trace_gibbs_target.py"]
    return {"status": "CONSTRUCTIVE_MODERATE_TEMPERATURE_SAMPLER_NOT_FULL_SEARCH",
            "source_hashes": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
            "review_origin": "research/independent_review_2026_10_22/CLASSICAL_SAMPLING.md",
            "classical_full_search_solved": False, "quantum_advantage_established": False,
            "native_certificates": certificates, "finite_controls": controls}


def _jsonable(value):
    if isinstance(value, Q):
        return [value.numerator, value.denominator]
    if isinstance(value, dict):
        return {key: _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    data = _jsonable(report())
    if args.write:
        REPORT.write_text(json.dumps(data, indent=2)+"\n")
    print(json.dumps({"status": data["status"], "native_certificates": len(data["native_certificates"]),
                      "finite_controls": len(data["finite_controls"])}))


if __name__ == "__main__":
    main()
