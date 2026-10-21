"""Local-resampling classical interval search on VERIFIED sparse RS frames.

Fix the constant coordinate first; otherwise it couples ALL bad events.
The remaining variable-occurrence graph has degree <=s(s-1), where s is
waveform support. Moser--Tardos then gives width O(sqrt(ell log ell)) for
the current norm-O(ell) frames. This is a local theorem application pending
independent review, not a novelty, quantum-speedup or sampling claim.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import random
import sys

from flint import fmpz

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.bpqm_gibbs_frontier import integer
from theorems.interval_character_rounding import _outward, native_moments, parameters
from theorems.interval_subgroup_rounding import coordinates, frame, multiply
from theorems.interval_split_fibers import public_frame, setup_bound
from theorems.prime_character_capacity_source import rational
from theorems.prime_character_opi import interpolate, ring

REPORT = ROOT / "research/classical_baselines/interval_local_lemma.json"


def certificate(p, support_size, squared_norm, u, *, resampling_budget=4096):
    """Pure parameter certificate; it does NOT construct or assert a frame."""
    ring(p)
    integer(support_size, "verified waveform support size", 2, p)
    integer(squared_norm, "verified squared integer waveform norm", support_size, p ** 3)
    integer(u, "centered interval radius", 0, p // 2)
    integer(resampling_budget, "resampling budget", 1, 100000)
    degree = min(p - 1, support_size * (support_size - 1))
    exponent = (2 * u + 1) ** 2 // (2 * squared_norm)
    probability = Fraction(0) if u == p // 2 else min(Fraction(1), Fraction(2, 1 << exponent))
    rhs_lower = Fraction(1, 3 * (degree + 1))
    certified = probability <= rhs_lower
    expected = Fraction(0) if probability == 0 else Fraction(p, degree)
    return {"p_decimal": str(p), "waveform_support_size": support_size,
            "waveform_squared_norm": squared_norm,
            "constant_coefficient_FIXED_nearest_before_sampling": True,
            "dependency_degree_upper": degree, "integer_half_offset_tail_exponent_floor": exponent,
            "per_bad_event_probability_upper_exact": rational(_outward(probability)),
            "symmetric_LLL_rhs_lower_exact": rational(rhs_lower),
            "MT_x_exact": rational(Fraction(1, degree + 1)),
            "uniform_all_target_local_lemma_criterion_certified": certified,
            "expected_total_resampling_steps_upper_exact": rational(expected) if certified else None,
            "resampling_budget": resampling_budget,
            "ideal_coin_budget_failure_Markov_upper_exact": rational(_outward(min(Fraction(1), expected / resampling_budget))) if certified else None,
            "premise": "verified public prime translation frame, fixed affine target, fresh independent exact Bernoulli coins initially and on EVERY resample",
            "pure_parameters_do_not_construct_a_frame": True,
            "seeded_run_frequency_is_not_confidence": True}


def radius(p, support_size, squared_norm):
    ring(p)
    integer(support_size, "support size", 2, p)
    integer(squared_norm, "squared waveform norm", support_size, p ** 3)
    degree = min(p - 1, support_size * (support_size - 1))
    exponent = (6 * (degree + 1) - 1).bit_length()
    square = 2 * squared_norm * exponent
    root = math.isqrt(square)
    root += int(root * root < square)
    return min(p // 2, root // 2)


def event_variables(model, x):
    """Coefficient indices1..p-1 only; constant index0 is NEVER resampled."""
    p = model["p"]
    return sorted((t + 1) for a, _ in model["support"] if (t := (x - a) % p) != p - 1)


def exact_event_model(model, d, u, word):
    """Exact fixed-target marginals, not an all-target probability theorem."""
    p, ell, w = model["p"], model["ell"], model["waveform"]
    parameters(p, d, u)
    if d > ell or sum(w) or not any(w) or any(native_moments(p, ell, list(w))):
        raise ValueError("verified nonzero zero-sum native moment frame required")
    support = tuple((i, a) for i, a in enumerate(w) if a)
    if support != model["support"] or sum(a * a for a in w) != model["squared_waveform_norm"]:
        raise ValueError("support or squared waveform norm was undercounted")
    nums, D = coordinates(model, word)
    z0 = (2 * nums[0] + D) // (2 * D)
    probabilities, variable_sets = [], []
    transitions, max_states, max_span, max_denominator_bits = 0, 1, 0, 1
    for x in range(p):
        base, masses, denominator, active = word[x] - z0, {0: 1}, 1, set()
        for i in event_variables(model, x):
            value = w[(x - i + 1) % p]
            floor, remainder = divmod(nums[i], D)
            base -= floor * value
            if not remainder:
                continue
            active.add(i)
            updated = {}
            for total, mass in masses.items():
                updated[total] = updated.get(total, 0) + mass * (D - remainder)
                updated[total + value] = updated.get(total + value, 0) + mass * remainder
                transitions += 2
            masses, denominator = updated, denominator * D
            max_states = max(max_states, len(masses))
            max_span = max(max_span, max(masses) - min(masses))
        if sum(masses.values()) != denominator:
            raise ArithmeticError("exact event distribution is not normalized")
        failed = sum(mass for total, mass in masses.items()
                     if abs((base - total + p // 2) % p - p // 2) > u)
        probabilities.append(Fraction(failed, denominator))
        variable_sets.append(frozenset(active))
        max_denominator_bits = max(max_denominator_bits, denominator.bit_length())
    return probabilities, variable_sets, {
        "integer_weighted_DP_transitions_charged": transitions,
        "max_DP_states": max_states, "max_DP_integer_span": max_span,
        "max_unreduced_probability_denominator_bits": max_denominator_bits,
        "coordinate_denominator_bits": D.bit_length(),
        "waveform_L1_span_upper": sum(map(abs, w)),
        "all_distributions_exactly_normalized": True}


def check_local_lemma(probabilities, neighbours, witnesses):
    """Check rational inequalities for a SUPPLIED graph, not its validity."""
    n = len(probabilities)
    if len(neighbours) != n or len(witnesses) != n:
        raise ValueError("one probability, neighbourhood and witness per event required")
    for i, (q, x, adjacent) in enumerate(zip(probabilities, witnesses, neighbours)):
        if not isinstance(q, Fraction) or not isinstance(x, Fraction) or not 0 <= q <= 1:
            raise ValueError("exact rational probabilities and witnesses required")
        if i in adjacent or any(type(j) is not int or not 0 <= j < n or i not in neighbours[j] for j in adjacent):
            raise ValueError("symmetric loop-free dependency graph required")
        if q == 0:
            if x != 0 or adjacent:
                raise ValueError("zero-probability events must be removed from the graph")
        elif not 0 < x < 1:
            return False
    for i, q in enumerate(probabilities):
        if q:
            rhs = witnesses[i]
            for j in sorted(neighbours[i]):
                rhs *= 1 - witnesses[j]
            if q > rhs:
                return False
    return True


def target_certificate(model, d, u, word, *, resampling_budget=4096):
    """Exact DP plus verified asymmetric/symmetric LLL on ONE original target."""
    integer(resampling_budget, "resampling budget", 1, 100000)
    probabilities, variables, costs = exact_event_model(model, d, u, word)
    active = [i for i, q in enumerate(probabilities) if q]
    neighbours = [set() for _ in probabilities]
    occurrences = {}
    for i in active:
        for variable in variables[i]:
            occurrences.setdefault(variable, set()).add(i)
    for i in active:
        neighbours[i] = set().union(*(occurrences[v] for v in variables[i])) - {i}
    degree = max(map(len, neighbours), default=0)
    # Outward dyadics keep inequality verification polynomial-sized without
    # multiplying every event's much larger exact DP denominator together.
    upper = [_outward(q) for q in probabilities]
    proposals = [("asymmetric_twice_outward_marginals", [2 * q for q in upper]),
                 ("symmetric_actual_dependency_degree",
                  [Fraction(1, max(2, degree + 1)) if q else Fraction(0) for q in upper])]
    certified, method, witnesses = False, None, None
    for name, proposed in proposals:
        if check_local_lemma(upper, neighbours, proposed):
            certified, method, witnesses = True, name, proposed
            break
    expected = sum((x / (1 - x) for x in witnesses), Fraction(0)) if certified else None
    binding = {"p": model["p"], "d": d, "ell": model["ell"], "u": u,
               "word": list(word), "waveform": list(model["waveform"])}
    return {"scope": "ORIGINAL_FIXED_TARGET_ONLY_NOT_UNIFORM_ALL_TARGETS",
            "input_sha256": hashlib.sha256(json.dumps(binding, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
            "fixed_target_local_lemma_criterion_certified": certified,
            "witness_selection": method,
            "event_probability_upper_128bit_dyadic": [rational(q) for q in upper],
            "LLL_witnesses_exact": [rational(x) for x in witnesses] if certified else None,
            "exact_probability_vector_sha256": hashlib.sha256("\n".join(rational(q) for q in probabilities).encode()).hexdigest(),
            "maximum_event_probability_exact": rational(max(probabilities)),
            "positive_probability_events": len(active), "actual_dependency_degree_upper": degree,
            "zero_remainder_variables_removed": True, "constant_coefficient_is_fixed": True,
            "expected_total_resampling_steps_upper_exact": rational(_outward(expected)) if certified else None,
            "resampling_budget": resampling_budget,
            "ideal_coin_budget_failure_Markov_upper_exact": rational(_outward(min(Fraction(1), expected / resampling_budget))) if certified else None,
            "costs": costs, "graph_search_and_exact_rational_products_charged": True,
            "inconclusive_does_not_mean_hard_or_unsatisfiable": True,
            "ideal_fresh_independent_coins_required_not_seed_frequency": True}


def solve(model, d, u, word, *, seed=4621, resampling_budget=4096, certify_target=False):
    p, ell, w = model["p"], model["ell"], model["waveform"]
    parameters(p, d, u)
    if d > ell or sum(w) or not any(w) or any(native_moments(p, ell, list(w))):
        raise ValueError("verified nonzero zero-sum native moment frame required")
    support = tuple((i, a) for i, a in enumerate(w) if a)
    if support != model["support"] or sum(a * a for a in w) != model["squared_waveform_norm"]:
        raise ValueError("support or squared waveform norm was undercounted")
    bound = certificate(p, len(support), model["squared_waveform_norm"], u, resampling_budget=resampling_budget)
    nums, D = coordinates(model, word)
    floors, remainders = [a // D for a in nums], [a % D for a in nums]
    rng = random.Random(seed)
    z = [(2 * nums[0] + D) // (2 * D)]
    z += [floors[i] + int(rng.randrange(D) < remainders[i]) for i in range(1, p)]
    initial = list(z)
    raw = [a - b for a, b in zip(word, multiply(model, z))]
    target = native_moments(p, d, word)

    def centered(a):
        return (a + p // 2) % p - p // 2

    bad = {x for x, a in enumerate(raw) if abs(centered(a)) > u}
    initial_bad = sorted(bad)
    transcript, coin_count = [], p - 1
    if native_moments(p, d, raw) != target:
        raise ArithmeticError("initial local-lemma assignment changed native syndrome")
    while bad and len(transcript) < resampling_budget:
        x = min(bad)
        variables = event_variables(model, x)
        if not variables or 0 in variables:
            raise ArithmeticError("bad event has no local variables or contains the global constant")
        before = centered(raw[x])
        bits, affected = [], set()
        for i in variables:
            bit = int(rng.randrange(D) < remainders[i])
            coin_count += 1
            new = floors[i] + bit
            change, z[i] = new - z[i], new
            bits.append(bit)
            for a, value in support:
                position = (a + i - 1) % p
                raw[position] -= change * value
                affected.add(position)
        for position in affected:
            if abs(centered(raw[position])) > u:
                bad.add(position)
            else:
                bad.discard(position)
        if native_moments(p, d, raw) != target:
            raise ArithmeticError("local resampling changed ORIGINAL affine equations")
        if z[0] != initial[0]:
            raise ArithmeticError("constant coefficient was resampled")
        transcript.append({"bad_coordinate": x, "prior_centered_value": before,
                           "resampled_coefficient_indices": variables, "new_ceil_bits": bits,
                           "affected_columns": sorted(affected), "remaining_bad_coordinates": len(bad),
                           "native_modular_equations_directly_checked": True})
    e = [centered(a) for a in raw]
    if raw != [a - b for a, b in zip(word, multiply(model, z))] or bad != {x for x, a in enumerate(e) if abs(a) > u}:
        raise ArithmeticError("incremental dependency updates disagree with independent reconstruction")
    solution = None
    if not bad:
        k, c = p - ell, [(a - b) % p for a, b in zip(word, e)]
        poly, _ = interpolate(p, tuple(range(k)), tuple(c[:k]))
        if any(int(poly(x)) != c[x] for x in range(p)) or native_moments(p, d, e) != target:
            raise ArithmeticError("independent RS polynomial/native replay rejects local-lemma output")
        solution = {"centered_affine_witness": e, "polynomial_coefficients": [int(poly[i]) for i in range(k)]}
    return {"p": p, "d": d, "ell": ell, "u": u, "public_particular_word": list(word),
            "target_syndrome": target, "waveform": list(w), "certificate": bound,
            "fixed_target_certificate": target_certificate(model, d, u, word, resampling_budget=resampling_budget) if certify_target else None,
            "coordinate_numerators_decimal": [str(fmpz(a)) for a in nums],
            "coordinate_common_denominator_decimal": str(fmpz(D)), "denominator_bits": D.bit_length(),
            "initial_coefficients_decimal": [str(fmpz(a)) for a in initial],
            "final_coefficients_decimal": [str(fmpz(a)) for a in z],
            "constant_rounding_error_exact": rational(Fraction(nums[0], D) - z[0]),
            "initial_bad_coordinates": initial_bad, "remaining_bad_coordinates": sorted(bad),
            "resampling_transcript": transcript, "resampling_steps": len(transcript),
            "exact_Bernoulli_coin_draws_charged": coin_count, "rounding_seed_for_replay_only": seed,
            "solution": solution, "centered_infinity_norm": max(map(abs, e)),
            "status": "VERIFIED_NATIVE_LOCAL_RESAMPLING_WITNESS" if solution else "LLL_RESAMPLING_BUDGET_EXHAUSTED_NOT_HARDNESS",
            "target_rerolls": 0, "constant_coefficient_resamples": 0,
            "resource_model": "public setup/rational inverse charged; each resampling uses <=s coins and <=s^2 local integer updates, plus PAID O(p*d) direct native checks and event bookkeeping"}


def run_controls():
    controls = []
    for p, ell, kind in ((347, 8, "fibers"), (1019, 16, "fibers"), (2017, 32, "split")):
        if kind == "fibers":
            setup, model = public_frame(p, ell)
            if model is None:
                raise ArithmeticError("declared public setup did not complete")
        else:
            model = frame(p, ell)
            setup = {"family": "split", "p": p, "ell": ell, "frame_actually_constructed": True}
        rng = random.Random(4637 + p)
        y = [rng.randrange(p) for _ in range(p)]
        u = radius(p, len(model["support"]), model["squared_waveform_norm"])
        controls.append({"input_source": "certified_radius_public_word", "public_setup": setup,
                         **solve(model, ell, u, y)})
    # This deliberately aggressive width tests real resampling, NOT the
    # theorem. Its criterion remains inconclusive even if a witness is found.
    _, model = public_frame(347, 8)
    y = [random.Random(4649 + i).randrange(347) for i in range(347)]
    aggressive = solve(model, 8, 3, y, resampling_budget=128)
    if aggressive["certificate"]["uniform_all_target_local_lemma_criterion_certified"]:
        raise ArithmeticError("aggressive finite control unexpectedly marked uniformly certified")
    analytic = []
    for p, ell, kind in (((1 << 31) - 1, 64, "nonsplit"), ((1 << 61) - 1, 256, "nonsplit"),
                         ((1 << 127) - 1, 32, "fiber_Weil")):
        u = radius(p, 2 * ell, 2 * ell)
        record = {"p_decimal": str(p), "ell": ell, "u": u,
                  "no_full_field_frame_or_native_target_executed": True,
                  "classical_radius_below_prior_soft_profile_support_ceiling_threshold": 2 * u + 1 <= ell,
                  "conditional_frame_family": kind, "certificate": certificate(p, 2 * ell, 2 * ell, u)}
        if kind == "nonsplit":
            record["proper_torus_divisor_checked"] = (p + 1) % ell == 0 and (p + 1) // ell >= 5
        else:
            record["public_setup_Weil_certificate"] = setup_bound(p, ell)
        analytic.append(record)
    fixed_target = [solve(model, 8, u, y, resampling_budget=128, certify_target=True) for u in (3, 5)]
    return {"schema_version": "interval-local-lemma-v2", "controls": controls,
            "uncertified_aggressive_resampling_control": aggressive,
            "original_target_exact_probability_controls": fixed_target,
            "analytic_parameter_only_controls": analytic,
            "all_certified_native_controls_verified": all(r["solution"] is not None for r in controls),
            "local_mathematical_application_independent_review_pending": True,
            "novelty_quantum_speedup_or_prescribed_sampling_claimed": False,
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "dependency_sha256": {name: hashlib.sha256((ROOT / "theorems" / name).read_bytes()).hexdigest()
                                  for name in ("interval_subgroup_rounding.py", "interval_split_fibers.py", "interval_character_rounding.py", "prime_character_opi.py", "prime_character_capacity_source.py", "bpqm_gibbs_frontier.py")},
            "literature": ["https://arxiv.org/abs/0903.0544", "https://doi.org/10.1080/01621459.1963.10500830"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"native": [{"p": r["p"], "ell": r["ell"], "u": r["u"], "norm": r["centered_infinity_norm"],
                                  "resamplings": r["resampling_steps"]} for r in report["controls"]],
                      "aggressive": {k: report["uncertified_aggressive_resampling_control"][k]
                                     for k in ("u", "resampling_steps", "status", "centered_infinity_norm")},
                      "analytic_only": [{"p": r["p_decimal"], "ell": r["ell"], "u": r["u"]}
                                        for r in report["analytic_parameter_only_controls"]],
                      "fixed_target": [{"p": r["p"], "u": r["u"],
                                         "certified": r["fixed_target_certificate"]["fixed_target_local_lemma_criterion_certified"],
                                         "resamplings": r["resampling_steps"]}
                                        for r in report["original_target_exact_probability_controls"]]}, indent=2))


if __name__ == "__main__":
    main()
