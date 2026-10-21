"""Sparse translation-frame classical attack on full-prime RS interval search.

Use split multiplicative cosets (ell|p-1), or norm-one torus trace cosets
(ell|p+1). Exact rational cyclic inversion provides coordinates, not a hidden
lattice inverse oracle. The actual squared waveform norm determines the tail
bound; trace multiplicities are NOT discarded. Local proof pending review.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import random
import sys

from flint import fmpq, fmpq_poly, fmpz
from sympy import factorint
from sympy.ntheory import primitive_root

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.bpqm_gibbs_frontier import integer
from theorems.interval_character_rounding import _outward, certified_radius, field, native_moments, parameters
from theorems.prime_character_capacity_source import rational
from theorems.prime_character_opi import interpolate
from theorems.prime_character_norm_attack import extension

REPORT = ROOT / "research/classical_baselines/interval_subgroup_rounding.json"


def family_parameters(p, ell, torus, minimum=1):
    field(p)
    integer(ell, "proper torus subgroup order", minimum, p // 2)
    if torus not in ("split", "nonsplit"):
        raise ValueError("explicit split or nonsplit torus required")
    order = p - 1 if torus == "split" else p + 1
    if order % ell:
        raise ValueError("ell must divide the selected torus order p-1 or p+1")
    index = order // ell
    norm = 2 * ell if torus == "split" or index >= 5 else 3 * ell - math.gcd(ell, 2)
    return order, index, norm


@lru_cache(maxsize=8)
def norm_one_generator(p):
    """Deterministic Cayley-chart search, with verified exact group order."""
    field(p)
    nu = next(a for a in range(2, p) if pow(a, (p - 1) // 2, p) == p - 1)
    E, _ = extension(p, nu)
    root, one = E.gen(), E(1)
    factors = tuple(map(int, factorint(p + 1)))
    for s in range(1, p):
        g = (one + s * root) / (one - s * root)
        if g ** (p + 1) == one and all(g ** ((p + 1) // r) != one for r in factors):
            if int(g.norm()) != 1:
                raise ArithmeticError("Cayley generator is not norm one")
            return E, g, nu, s
    raise ArithmeticError("norm-one primitive generator missing from exhaustive Cayley chart")


@lru_cache(maxsize=16)
def frame(p, ell, torus="split"):
    _, index, expected_norm = family_parameters(p, ell, torus)
    metadata = {"torus_type": torus, "torus_quotient_index": index}
    if torus == "split":
        g = int(primitive_root(p))
        H = {pow(g, (p - 1) // ell * i, p) for i in range(ell)}
        other = {g * x % p for x in H}
        if len(H) != ell or len(other) != ell or H & other:
            raise ArithmeticError("split cosets are not distinct of the declared order")
        w = tuple(int(x in H) - int(x in other) for x in range(p))
        expected_first = ell * (1 - pow(g, ell, p)) % p
        metadata["primitive_generator"] = g
    else:
        E, g, nu, trials = norm_one_generator(p)
        exponents = (1, 2) if index >= 5 else (0, 1)
        step = g ** ((p + 1) // ell)
        H = [step ** i for i in range(ell)]
        # Trace identifies z with z^-1. Only generic inverse classes are
        # injective; small quotient indices must keep multiplicity2.
        traces = [Counter(int(((g ** a) * z).trace()) for z in H) for a in exponents]
        w = tuple(traces[0][x] - traces[1][x] for x in range(p))
        expected_first = ell * (int((g ** (exponents[0] * ell)).trace())
                                - int((g ** (exponents[1] * ell)).trace())) % p
        metadata.update({"primitive_generator": list(map(int, g.to_list())),
                         "quadratic_nonresidue": nu, "generator_Cayley_parameters_tested": trials,
                         "trace_coset_exponents": list(exponents),
                         "maximum_trace_fiber_multiplicities": [max(t.values()) for t in traces]})
    return translation_frame(p, ell, w, expected_first=expected_first, expected_norm=expected_norm) | metadata


def translation_frame(p, ell, w, *, expected_first, expected_norm):
    """Compute and verify the same translation inverse for a proven waveform.

    Used by torus frames and explicit split-fiber construction, not an inverse
    oracle. The waveform must be supplied by a charged public construction.
    """
    parameters(p, ell, 0)
    w = tuple(w)
    if len(w) != p or any(type(a) is not int for a in w) or sum(w) != 0 or not any(w):
        raise ValueError("nonzero integer zero-sum waveform on all p points required")
    if any(native_moments(p, ell, list(w))):
        raise ArithmeticError("waveform fails native moments below ell")
    first = sum(pow(x, ell, p) * v for x, v in enumerate(w)) % p
    if first != expected_first or first == 0:
        raise ArithmeticError("sharp waveform-moment boundary is wrong")
    squared_norm = sum(v * v for v in w)
    if squared_norm != expected_norm:
        raise ArithmeticError("waveform squared norm disagrees with the claimed variance parameter")
    X, Phi = fmpq_poly([0, 1]), fmpq_poly([1] * p)
    V, remainder = divmod(fmpq_poly(list(w)), X - 1)
    if not remainder.is_zero():
        raise ArithmeticError("zero-sum row did not divide by X-1")
    gcd, inverse, _ = V.xgcd(Phi)
    inverse %= Phi
    if gcd != fmpq_poly([1]) or V * inverse % Phi != fmpq_poly([1]):
        raise ArithmeticError("exact rational translation inverse failed")
    return {"p": p, "ell": ell, "waveform": w, "squared_waveform_norm": squared_norm,
            "support": tuple((i, v) for i, v in enumerate(w) if v),
            "inverse": inverse, "first_forbidden_moment": first}


def multiply(model, coefficients):
    p = model["p"]
    if len(coefficients) != p or any(type(a) is not int for a in coefficients):
        raise ValueError("whole integer translation coefficient vector required")
    word = [coefficients[0]] * p
    for t, a in enumerate(coefficients[1:]):
        for x, v in model["support"]:
            word[(x + t) % p] += a * v
    return word


def coordinates(model, word):
    p = model["p"]
    if len(word) != p or any(type(a) is not int or not 0 <= a < p for a in word):
        raise ValueError("canonical full public particular word required")
    mean = fmpq(sum(word), p)
    X, Phi = fmpq_poly([0, 1]), fmpq_poly([1] * p)
    T = fmpq_poly(word) - mean * Phi
    U, remainder = divmod(T, X - 1)
    if not remainder.is_zero():
        raise ArithmeticError("mean-centered target is not zero-sum over Q")
    C = U * model["inverse"] % Phi
    alpha = [mean] + [C[i] for i in range(p - 1)]
    denominator = math.lcm(*(int(v.denominator) for v in alpha))
    numerators = [int(v * denominator) for v in alpha]
    if multiply(model, numerators) != [denominator * v for v in word]:
        raise ArithmeticError("rational cyclic inverse does not reconstruct the original target")
    return numerators, denominator


def failure_certificate(p, d, ell, u, *, attempts=16, torus="split"):
    parameters(p, d, u)
    _, _, squared_norm = family_parameters(p, ell, torus, d)
    return waveform_failure_certificate(p, d, ell, u, squared_norm, attempts=attempts) | {
        "torus_type": torus, "general_all_prime_subgroup_smoothness_assumed": False}


def waveform_failure_certificate(p, d, ell, u, squared_norm, *, attempts=16):
    parameters(p, d, u)
    integer(ell, "verified moment order at least codimension", d, p // 2)
    integer(squared_norm, "charged squared waveform norm", 1, p * p * p)
    integer(attempts, "fixed-target rounding budget", 1, 64)
    variance = squared_norm + 1
    exponent = 2 * (u + 1) ** 2 // variance
    bound = Fraction(0) if u == p // 2 else min(Fraction(1), Fraction(2 * p, 1 << exponent))
    return {"column_squared_range_sum_upper": variance, "integer_tail_threshold": u + 1,
            "exponent_floor": exponent,
            "per_attempt_all_target_failure_upper_exact": rational(_outward(bound)),
            "all_attempts_fail_upper_exact": rational(_outward(bound ** attempts)),
            "uniform_all_target_bound_nontrivial": bound < 1,
            "expected_attempts_upper_exact": rational(1 / (1 - _outward(bound))) if _outward(bound) < 1 else None,
            "premise": "fresh independent exact remainder/denominator Bernoulli coins; unchanged target"}


def radius(p, ell, *, torus="split"):
    _, _, squared_norm = family_parameters(p, ell, torus)
    product = (squared_norm + 1) * (4 * p - 1).bit_length()
    r = math.isqrt(product // 2)
    while 2 * r * r < product:
        r += 1
    return min(p // 2, r - 1)


def solve(p, d, ell, u, word, *, seed=4513, attempts=16, torus="split", rounding="independent"):
    certificate = failure_certificate(p, d, ell, u, attempts=attempts, torus=torus)
    model = frame(p, ell, torus)
    return round_frame(model, d, u, word, seed=seed, attempts=attempts, rounding=rounding) | {
        "primitive_generator": model["primitive_generator"],
        "torus_type": torus, "torus_quotient_index": model["torus_quotient_index"],
        "nonsplit_setup": {k: model[k] for k in ("quadratic_nonresidue", "generator_Cayley_parameters_tested", "trace_coset_exponents", "maximum_trace_fiber_multiplicities")} if torus == "nonsplit" else None,
        "failure_certificate": certificate | {"comparison_only_not_active_rounding_model": rounding != "independent"}}


def nearest_certificate(model, u):
    """All-target INTEGER bound from nearest row-coordinate rounding."""
    p, w = model["p"], model["waveform"]
    # Omitting translate p-1 subtracts |w[x+1]| from the full column L1 norm.
    column_l1 = 1 + sum(map(abs, w)) - min(map(abs, w))
    raw_radius = column_l1 // 2
    centered_radius = min(p // 2, raw_radius)
    return {"maximum_column_l1_exact": column_l1,
            "all_target_raw_integer_radius": raw_radius,
            "all_target_centered_integer_radius": centered_radius,
            "requested_interval_uniformly_solved": u >= centered_radius,
            "rounding_coins_required": False}


def round_frame(model, d, u, word, *, seed=4513, attempts=16, rounding="independent"):
    """Shared exact rounding, after an actual public waveform construction."""
    p, ell = model["p"], model["ell"]
    w = model["waveform"]
    if sum(w) or not any(w) or any(native_moments(p, ell, list(w))):
        raise ValueError("nonzero zero-sum native-kernel waveform required")
    if sum(a * a for a in w) != model["squared_waveform_norm"]:
        raise ValueError("waveform norm undercounted")
    if rounding not in ("independent", "nearest"):
        raise ValueError("explicit independent or nearest rounding required")
    certificate = waveform_failure_certificate(p, d, ell, u, model["squared_waveform_norm"], attempts=attempts)
    certificate["comparison_only_not_active_rounding_model"] = rounding != "independent"
    nearest = nearest_certificate(model, u)
    numerators, denominator = coordinates(model, word)
    target, rng, records, solution = native_moments(p, d, word), None if rounding == "nearest" else random.Random(seed), [], None
    for _ in range(1 if rounding == "nearest" else attempts):
        z = []
        for a in numerators:
            if rounding == "nearest":
                z.append((2 * a + denominator) // (2 * denominator))
            else:
                q, r = divmod(a, denominator)
                z.append(q + int(rng.randrange(denominator) < r))
        raw = [a - b for a, b in zip(word, multiply(model, z))]
        e = [(a + p // 2) % p - p // 2 for a in raw]
        if native_moments(p, d, raw) != target or native_moments(p, d, e) != target:
            raise ArithmeticError("sparse rounding changed ORIGINAL modular equations")
        norm = max(map(abs, e))
        if rounding == "nearest" and (max(map(abs, raw)) > nearest["all_target_raw_integer_radius"]
                                      or norm > nearest["all_target_centered_integer_radius"]):
            raise ArithmeticError("actual nearest residual contradicts its all-target column bound")
        records.append({"rounded_coefficients_decimal": [str(fmpz(a)) for a in z],
                        "raw_infinity_norm": max(map(abs, raw)), "centered_infinity_norm": norm,
                        "valid_interval_solution": norm <= u})
        if norm <= u:
            k = p - ell
            c = [(a - b) % p for a, b in zip(word, e)]
            poly, _ = interpolate(p, tuple(range(k)), tuple(c[:k]))
            if any(int(poly(x)) != c[x] for x in range(p)):
                raise ArithmeticError("independent polynomial replay rejects sparse witness")
            solution = {"centered_affine_witness": e, "polynomial_coefficients": [int(poly[i]) for i in range(k)]}
            break
    return {"p": p, "d": d, "ell": ell, "u": u, "public_particular_word": list(word),
            "target_syndrome": target,
            "support_size": len(model["support"]), "squared_waveform_norm": model["squared_waveform_norm"],
            "first_forbidden_moment": model["first_forbidden_moment"],
            "coordinate_numerators_decimal": [str(fmpz(a)) for a in numerators],
            "coordinate_common_denominator_decimal": str(fmpz(denominator)),
            "coordinate_denominator_bits": denominator.bit_length(),
            "maximum_coordinate_numerator_bits": max(abs(a).bit_length() for a in numerators),
            "inverse_polynomial_coefficients_exact": [rational(Fraction(int(model["inverse"][i].numerator), int(model["inverse"][i].denominator))) for i in range(p - 1)],
            "closed_form_rational_cyclic_inverse_reconstructed": True,
            "attempts": records, "solution": solution, "rounding_seed_for_replay_only": seed if rounding == "independent" else None,
            "rounding_mode": rounding, "nearest_rounding_certificate": nearest,
            "status": "VERIFIED_NATIVE_SPARSE_FRAME_WITNESS" if solution else ("ROUNDING_BUDGET_EXHAUSTED_NOT_HARDNESS" if rounding == "independent" else "NEAREST_FAILED_REQUESTED_WIDTH_NOT_HARDNESS"),
            "failure_certificate": certificate, "target_rerolls": 0,
            "resource_model": {"inverse": "exact polynomial xgcd over Q, polynomial cost in explicit p; coefficients NOT assumed small",
                               "coordinate_bit_bound": "O(p log(norm_squared+1)+log p) via cofactors and Hadamard; norm_squared=O(ell) in current families",
                               "rounding": "O(p*nnz(w)) streamed multiply plus O(p*d) native moments; " + ("p exact coins on the charged denominator" if rounding == "independent" else "exact signed nearest comparisons, NO rounding coins"),
                               "setup": "public waveform construction and rational inverse charged separately; no supplied short-vector oracle or log-p-only complexity claim",
                               "input_output_field": "original PRIME p and length p; auxiliary fields used internally do not change the problem"}}


def run_controls():
    controls = []
    for p, ell in ((31, 5), (61, 5), (127, 7), (257, 16), (1021, 17)):
        rng = random.Random(4523 + p)
        for label, word in (("uniform_public_word", [rng.randrange(p) for _ in range(p)]),
                            ("quarter_field_spike", [p // 4] + [0] * (p - 1))):
            u = radius(p, ell)
            L = 2 * u + 1
            score = Fraction(2 * L, 3 * p) + Fraction(1, 3 * p * L)
            controls.append({"input_source": label, "dense_character_certified_radius": certified_radius(p),
                             "uniform_interval_KV_score_exact": rational(score),
                             "quantum_uniform_interval_sufficient_condition_met": 4 * u <= p - 1 and Fraction(ell, p) < score,
                             **solve(p, ell, ell, u, word)})
    nonsplit = []
    for p, ell in ((47, 6), (107, 9), (509, 15), (1019, 17)):
        rng = random.Random(4561 + p)
        split_ell = next(e for e in range(ell, p // 2 + 1) if (p - 1) % e == 0)
        for label, word in (("uniform_public_word", [rng.randrange(p) for _ in range(p)]),
                            ("quarter_field_spike", [p // 4] + [0] * (p - 1))):
            u = radius(p, ell, torus="nonsplit")
            L = 2 * u + 1
            score = Fraction(2 * L, 3 * p) + Fraction(1, 3 * p * L)
            nonsplit.append({"input_source": label, "best_split_order_at_least_d": split_ell,
                             "best_split_certified_radius": radius(p, split_ell),
                             "uniform_interval_KV_score_exact": rational(score),
                             "quantum_uniform_interval_sufficient_condition_met": 4 * u <= p - 1 and Fraction(ell, p) < score,
                             **solve(p, ell, ell, u, word, torus="nonsplit")})
    fiber_controls = []
    for ell in (12, 16):
        model = frame(47, ell, "nonsplit")
        fiber_controls.append({k: model[k] for k in ("p", "ell", "torus_quotient_index", "trace_coset_exponents", "maximum_trace_fiber_multiplicities", "squared_waveform_norm", "first_forbidden_moment")}
                              | {"waveform": list(model["waveform"]), "incorrect_unit_fiber_variance_rejected": model["squared_waveform_norm"] > 2 * ell})
    nearest_controls = []
    for p, ell, torus in ((61, 5, "split"), (47, 6, "nonsplit")):
        rng = random.Random(4603 + p)
        nearest_controls.append({"input_source": "uniform_public_word_nearest",
                                 **solve(p, ell, ell, ell, [rng.randrange(p) for _ in range(p)], torus=torus, rounding="nearest")})
    return {"schema_version": "interval-subgroup-rounding-v3", "controls": controls,
            "nonsplit_controls": nonsplit, "small_quotient_trace_fiber_controls": fiber_controls,
            "nearest_controls": nearest_controls,
            "all_declared_targets_verified": all(r["solution"] is not None for r in controls + nonsplit + nearest_controls),
            "local_derivation_independent_review_pending": True,
            "asymptotic_scope": "full-prime N=p, d<=ell<=floor(p/2), proper divisor ell of p-1 (split) or p+1 (nonsplit); all-target search at width O(sqrt(ell log p)), actual trace-fiber costs retained",
            "novelty_quantum_speedup_or_weighted_sampling_claimed": False,
            "arbitrary_sets_punctured_inputs_or_all_prime_smoothness_claimed": False,
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "dependency_sha256": {name: hashlib.sha256((ROOT / "theorems" / name).read_bytes()).hexdigest()
                                  for name in ("interval_character_rounding.py", "prime_character_opi.py", "prime_character_capacity_source.py", "bpqm_gibbs_frontier.py", "prime_character_norm_attack.py")},
            "literature": ["https://arxiv.org/abs/2411.12553", "https://arxiv.org/abs/2202.07736",
                           "https://doi.org/10.1080/01621459.1963.10500830", "https://doi.org/10.53733/579"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print(json.dumps([{k: r[k] for k in ("p", "ell", "d", "u", "torus_type", "rounding_mode", "input_source", "coordinate_denominator_bits")}
                      | {"norm": r["attempts"][-1]["centered_infinity_norm"], "success": r["solution"] is not None}
                      for r in report["controls"] + report["nonsplit_controls"] + report["nearest_controls"]], indent=2))


if __name__ == "__main__":
    main()
