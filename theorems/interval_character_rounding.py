"""Constructive classical interval RS-ISIS using a bounded character basis.

Full support F_p, prime p, codimension d <= (p-1)/2 only. The all-target
rounding bound is a local derivation, not a novelty claim or a quantum run.
Seeded runs replay witnesses; their frequencies are NOT confidence estimates.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import random
import sys

from flint import fmpz_mat, nmod_mat

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.bpqm_gibbs_frontier import integer
from theorems.prime_character_capacity_source import rational
from theorems.prime_character_opi import interpolate, ring

REPORT = ROOT / "research/classical_baselines/interval_character_rounding.json"
MATCHED_REPORT = ROOT / "research/classical_baselines/interval_soft_decoder.json"


def field(p):
    integer(p, "explicit full-field implementation cap", 3, 4096)
    ring(p)
    return p


def parameters(p, d, u):
    field(p)
    integer(d, "character-kernel codimension", 1, (p - 1) // 2)
    integer(u, "centered interval radius", 0, (p - 1) // 2)


@lru_cache(maxsize=4)
def character(p):
    field(p)
    return tuple(0 if x == 0 else (1 if pow(x, (p - 1) // 2, p) == 1 else -1)
                 for x in range(p))


def multiply_basis(p, coefficients):
    """Row coordinates times B; stream rows instead of storing p squared entries."""
    chi = character(p)
    if len(coefficients) != p or any(type(a) is not int for a in coefficients):
        raise ValueError("one exact integer per row required")
    word = [coefficients[0]] * p
    for t, a in enumerate(coefficients[1:]):
        for x in range(p):
            word[x] += a * chi[(x - t) % p]
    return word


def native_moments(p, d, word):
    """H_d[j,x]=x**j, x=0,...,p-1. No dense parity matrix or floating FFT."""
    parameters(p, d, 0)
    if len(word) != p or any(type(a) is not int for a in word):
        raise ValueError("whole exact integer word required")
    result = [0] * d
    for x, a in enumerate(word):
        power = 1
        for j in range(d):
            result[j] = (result[j] + a * power) % p
            power = power * x % p
    return result


def coefficient_numerators(p, word):
    """Exact y = (a/p) B from the character Gram inverse, no lattice reduction."""
    chi = character(p)
    if len(word) != p or any(type(a) is not int or not 0 <= a < p for a in word):
        raise ValueError("canonical full public particular word required")
    beta = [sum(y * chi[(x - t) % p] for x, y in enumerate(word)) for t in range(p)]
    numerators = [sum(word)] + [b - beta[-1] for b in beta[:-1]]
    if multiply_basis(p, numerators) != [p * y for y in word]:
        raise ArithmeticError("closed-form character coordinates fail exact reconstruction")
    return numerators


def round_numerator(a, p, rng):
    """Unbiased rounding of a/p with an exact remainder/p Bernoulli coin."""
    if type(a) is not int or type(p) is not int or p < 1:
        raise ValueError("integer numerator and positive denominator required")
    q, r = divmod(a, p)
    return q + int(rng.randrange(p) < r)


def _outward(value, bits=128):
    scale = 1 << bits
    return Fraction(-(-value.numerator * scale // value.denominator), scale)


def failure_certificate(p, d, u, *, attempts=16):
    """Uniform over every public y, conditional on ideal independent exact coins.

    Failure implies an INTEGER raw residual of magnitude at least u+1.
    Hoeffding plus a union bound gives 2p exp(-2(u+1)^2/p). Since e>2,
    replacing the exponential by 2**(-floor(2(u+1)^2/p)) is outward-safe.
    """
    parameters(p, d, u)
    integer(attempts, "same-target independent rounding budget", 1, 64)
    exponent = 2 * (u + 1) ** 2 // p
    exact = Fraction(0) if u == p // 2 else min(Fraction(1), Fraction(2 * p, 1 << exponent))
    upper = _outward(exact)
    return {"p": p, "d": d, "u": u, "attempt_budget": attempts,
            "integer_tail_threshold": u + 1, "dyadic_exponent_floor": exponent,
            "Hoeffding_failure_expression": "min(1, 2*p*exp(-2*(u+1)^2/p)); full interval has failure0",
            "per_attempt_failure_upper_exact": rational(upper),
            "all_attempts_fail_upper_exact": rational(_outward(exact ** attempts)),
            "expected_attempts_upper_exact": rational(1 / (1 - upper)) if upper < 1 else None,
            "uniform_all_target_success_bound_nontrivial": upper < 1,
            "probability_enclosures_rounded_up_bits": 128,
            "premise": "fresh independent exact Bernoulli(remainder/p) coins on each attempt, SAME target",
            "seeded_runs_are_not_confidence_estimates": True,
            "novelty_or_general_OPI_dequantization_claimed": False}


def certified_radius(p):
    """An integer radius with all-target failure <=1/2; no floating sqrt/log."""
    field(p)
    exponent = (4 * p - 1).bit_length()
    r = math.isqrt(p * exponent // 2)
    while 2 * r * r < p * exponent:
        r += 1
    return min(p // 2, r - 1)


def particular_for_syndrome(p, d, target):
    """Public Vandermonde solve; charges O(d^3) field work and O(d^2) storage."""
    parameters(p, d, 0)
    if len(target) != d or any(type(a) is not int or not 0 <= a < p for a in target):
        raise ValueError("canonical d-coordinate syndrome required")
    matrix = nmod_mat([[pow(x, j, p) for x in range(d)] for j in range(d)], p)
    solution = matrix.solve(nmod_mat([[s] for s in target], p))
    word = [int(solution[i, 0]) if i < d else 0 for i in range(p)]
    if native_moments(p, d, word) != list(target):
        raise ArithmeticError("public particular solution fails native moments")
    return word


def solve(p, d, u, word, *, seed=4463, attempts=16):
    """Exact native solver; retains all failures and never changes the target.

    O(p^2) integer operations and O(p) working storage per rounding attempt;
    optional syndrome-to-particular Gaussian elimination is a separate cost.
    Returned polynomial replay uses independent exact Lagrange interpolation.
    """
    certificate = failure_certificate(p, d, u, attempts=attempts)
    numerators = coefficient_numerators(p, word)
    target = native_moments(p, d, word)
    rng, records, solution = random.Random(seed), [], None
    for _ in range(attempts):
        z = [round_numerator(a, p, rng) for a in numerators]
        lattice = multiply_basis(p, z)
        raw = [y - b for y, b in zip(word, lattice)]
        centered = [(a + p // 2) % p - p // 2 for a in raw]
        if native_moments(p, d, raw) != target or native_moments(p, d, centered) != target:
            raise ArithmeticError("rounded witness fails the ORIGINAL affine equations")
        raw_norm, norm = max(map(abs, raw)), max(map(abs, centered))
        if norm > raw_norm:
            raise ArithmeticError("centering increased a residual norm")
        valid = norm <= u
        records.append({"rounded_coefficients": z, "raw_infinity_norm": raw_norm,
                        "centered_infinity_norm": norm, "valid_interval_solution": valid,
                        "original_modular_equations_verified": True})
        if valid:
            c = [(a - b) % p for a, b in zip(word, centered)]
            h = (p - 1) // 2
            polynomial, _ = interpolate(p, tuple(range(h + 1)), tuple(c[:h + 1]))
            if any(int(polynomial(x)) != c[x] for x in range(p)):
                raise ArithmeticError("independent interpolation rejects character-lattice witness")
            solution = {"centered_affine_witness": centered,
                        "polynomial_coefficients": [int(polynomial[i]) for i in range(h + 1)],
                        "degree_upper_bound": h, "native_polynomial_replay_verified": True}
            break
    return {"p": p, "d": d, "u": u, "public_particular_word": list(word),
            "original_target_syndrome": target, "coefficient_numerators_denominator_p": numerators,
            "closed_form_coordinates_exactly_reconstructed": True,
            "rounding_seed_for_replay_only": seed, "attempts": records, "solution": solution,
            "status": "VERIFIED_NATIVE_INTERVAL_WITNESS" if solution else "ROUNDING_BUDGET_EXHAUSTED_NOT_HARDNESS",
            "failure_certificate": certificate, "target_rerolls": 0, "basis_search_or_LLL_calls": 0,
            "failed_rounding_attempts_retained": True,
            "canonical_interpolation_uniform_syndrome_success_exact": rational(Fraction(2 * u + 1, p) ** d),
            "resource_model": {"block_length_N": p, "field_bit_length": p.bit_length(),
                               "coefficient_and_rounding_arithmetic": "O(p^2) integer operations per attempt, O(log p)-bit integers for canonical y",
                               "streaming_working_storage": "O(p) integers; saved r-attempt transcript O(r*p)",
                               "independent_polynomial_replay": "polynomial in p, additional verification cost",
                               "polynomial_in_log_p_for_punctured_input": False}}


def deterministic_certificate(p, d, u):
    """Exact log enclosure for the rational exponential potential base.

    log(c)=2*atanh((c-1)/(c+1)); eight positive series terms give a lower
    bound, and a geometric tail gives an upper bound. No numerical logs.
    """
    parameters(p, d, u)
    k = u + 1
    base = Fraction(p + 4 * k, p)
    t = (base - 1) / (base + 1)
    lower = 2 * sum((t ** (2 * j + 1) / (2 * j + 1) for j in range(8)), Fraction(0))
    upper = lower + 2 * t ** 17 / (17 * (1 - t * t))
    margin = k * lower - Fraction(p, 8) * upper * upper
    exponent = margin.numerator // margin.denominator
    ratio = Fraction(2 * p, 1 << exponent) if exponent >= 0 else Fraction((2 * p) << -exponent)
    return {"rational_potential_base": rational(base),
            "log_base_lower_exact": rational(lower), "log_base_upper_exact": rational(upper),
            "Hoeffding_exponent_margin_lower_exact": rational(margin),
            "initial_potential_to_bad_threshold_upper_exact": rational(_outward(ratio)),
            "uniform_all_target_potential_certificate": ratio < 1,
            "full_interval_trivially_solved": u == p // 2,
            "random_coins_or_seed_required": False,
            "square_root_logarithmic_width_loss_removed": False}


def deterministic_radius(p):
    """Find a certified width; unlike random rounding it can be slightly larger."""
    u = certified_radius(p)
    while u < p // 2 and not deterministic_certificate(p, p // 2, u)["uniform_all_target_potential_certificate"]:
        u += 1
    return u


def solve_deterministic(p, d, u, word):
    """Conditional expectations with EXACT INTEGER common-denominator weights.

    Greedily fix floor/ceil choices while decreasing E sum_x(c^e+c^-e).
    This is an actual deterministic solver, not an assumed discrepancy oracle.
    Its larger O(p log p)-bit integers and O(p^2 log p)-bit storage are charged.
    """
    certificate = deterministic_certificate(p, d, u)
    numerators = coefficient_numerators(p, word)
    q = [a // p for a in numerators]
    remainders = [a % p for a in numerators]
    floors = multiply_basis(p, q)
    w = [y - a for y, a in zip(word, floors)]
    if any(abs(a) > p for a in w):
        raise ArithmeticError("floor residual violates its exact fractional-coordinate bound")
    base = Fraction(certificate["rational_potential_base"])
    a, b, chi = base.numerator, base.denominator, character(p)
    ab, denominator = a * b, (a * b) ** (2 * p) * p ** p
    plus = [a ** (p + v) * b ** (p - v) for v in w]
    minus = [a ** (p - v) * b ** (p + v) for v in w]

    def row_value(i, x):
        return 1 if i == 0 else chi[(x - i + 1) % p]

    def coin_factor(r, sign):
        return (p - r) * ab + r * (b * b if sign == 1 else a * a if sign == -1 else ab)

    def branch_factor(bit, sign):
        return p * (ab if bit == 0 or sign == 0 else b * b if sign == 1 else a * a)

    for i, r in enumerate(remainders):
        for x in range(p):
            sign = row_value(i, x)
            plus[x] *= coin_factor(r, sign)
            minus[x] *= coin_factor(r, -sign)
    current = initial = sum(plus) + sum(minus)
    k = u + 1
    threshold_numerator = denominator * a ** k
    initial_below = initial * b ** k < threshold_numerator
    if certificate["uniform_all_target_potential_certificate"] and not initial_below:
        raise ArithmeticError("exact initial potential contradicts the uniform analytic bound")
    choices = []
    digest = hashlib.sha256()
    for i, r in enumerate(remainders):
        signs = [row_value(i, x) for x in range(p)]
        stripped_plus, stripped_minus = [], []
        for x, sign in enumerate(signs):
            v, rem = divmod(plus[x], coin_factor(r, sign))
            vneg, remneg = divmod(minus[x], coin_factor(r, -sign))
            if rem or remneg:
                raise ArithmeticError("common-denominator potential division is not exact")
            stripped_plus.append(v)
            stripped_minus.append(vneg)
        branch_zero = p * ab * (sum(stripped_plus) + sum(stripped_minus))
        branch_one = sum(v * branch_factor(1, sign) + vneg * branch_factor(1, -sign)
                         for v, vneg, sign in zip(stripped_plus, stripped_minus, signs))
        if (p - r) * branch_zero + r * branch_one != p * current:
            raise ArithmeticError("conditional expectation does not equal its weighted branches")
        bit = int(r != 0 and branch_one < branch_zero)
        next_value = branch_one if bit else branch_zero
        if next_value > current:
            raise ArithmeticError("greedy conditional expectation increased the potential")
        plus = [v * branch_factor(bit, sign) for v, sign in zip(stripped_plus, signs)]
        minus = [v * branch_factor(bit, -sign) for v, sign in zip(stripped_minus, signs)]
        choices.append(bit)
        current = next_value
        encoded = current.to_bytes(max(1, (current.bit_length() + 7) // 8), "big")
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
    z = [v + bit for v, bit in zip(q, choices)]
    lattice = multiply_basis(p, z)
    raw = [y - v for y, v in zip(word, lattice)]
    centered = [(v + p // 2) % p - p // 2 for v in raw]
    target = native_moments(p, d, word)
    if native_moments(p, d, raw) != target or native_moments(p, d, centered) != target:
        raise ArithmeticError("deterministic witness fails ORIGINAL modular equations")
    for x, v in enumerate(raw):
        numerator, divisor = (a ** v, b ** v) if v >= 0 else (b ** -v, a ** -v)
        if plus[x] * divisor != denominator * numerator or minus[x] * numerator != denominator * divisor:
            raise ArithmeticError("final integer weights do not equal the actual residual potential")
    norm = max(map(abs, centered))
    if initial_below and norm > u:
        raise ArithmeticError("potential certificate accepted an invalid interval witness")
    solution = None
    if norm <= u:
        h = (p - 1) // 2
        c = [(y - e) % p for y, e in zip(word, centered)]
        polynomial, _ = interpolate(p, tuple(range(h + 1)), tuple(c[:h + 1]))
        if any(int(polynomial(x)) != c[x] for x in range(p)):
            raise ArithmeticError("independent interpolation rejects deterministic interval witness")
        solution = {"centered_affine_witness": centered,
                    "polynomial_coefficients": [int(polynomial[i]) for i in range(h + 1)]}
    return {"p": p, "d": d, "u": u, "public_particular_word": list(word),
            "original_target_syndrome": target, "rounded_coefficients": z, "chosen_ceil_bits": choices,
            "certificate": certificate,
            "initial_exact_potential_certifies_this_target": initial_below,
            "initial_potential_ratio_upper_exact": rational(_outward(Fraction(initial * b ** k, threshold_numerator))),
            "final_potential_ratio_upper_exact": rational(_outward(Fraction(current * b ** k, threshold_numerator))),
            "p_conditional_expectation_steps_verified": p,
            "potential_chain_sha256": digest.hexdigest(), "integer_potential_denominator_bit_length": denominator.bit_length(),
            "raw_infinity_norm": max(map(abs, raw)), "centered_infinity_norm": norm,
            "solution": solution,
            "status": "VERIFIED_DETERMINISTIC_NATIVE_WITNESS" if solution else "POTENTIAL_BOUND_INCONCLUSIVE_NO_WITNESS",
            "target_rerolls": 0, "random_coins_or_seed_used": False,
            "resource_model": "O(p^2) arithmetic on O(p log p)-bit integers, O(p^2 log p) bits working storage; no stochastic or numerical-log step"}


def bounded_basis_audit(p):
    """Materialize small matrices only; no finite check substitutes for the proof."""
    field(p)
    integer(p, "independent Gram/determinant calibration cap", 3, 127)
    h, chi = (p - 1) // 2, character(p)
    rows = [[1] * p] + [[chi[(x - t) % p] for x in range(p)] for t in range(p - 1)]
    B = fmpz_mat(rows)
    gram = B * B.transpose()
    expected = fmpz_mat([[p if i == j == 0 else (0 if i == 0 or j == 0 else (p - 1 if i == j else -1))
                          for j in range(p)] for i in range(p)])
    kernel = all(not any(native_moments(p, h, row)) for row in rows)
    next_moments = [sum(pow(x, h, p) * row[x] for x in range(p)) % p for row in rows[1:]]
    if gram != expected or abs(int(B.det())) != p ** h or not kernel or set(next_moments) != {p - 1}:
        raise ArithmeticError("character-basis identity or sharp half-rate boundary failed")
    return {"p": p, "determinant_magnitude_decimal": str(p ** h),
            "Gram_identity_verified": True, "half_rate_native_kernel_verified": True,
            "first_forbidden_moment_of_every_character_row": p - 1,
            "codimension_above_half_rate_rejected": True}


def run_controls():
    matched = json.loads(MATCHED_REPORT.read_text())
    records = []
    for family in matched["uniform_target_lattice_controls"]:
        p, d, u = family["profile"]["p"], family["decoder_dimension"], family["profile"]["u"]
        for i, prior in enumerate(family["trials"]):
            row = solve(p, d, u, prior["particular_word"], seed=4463 + i)
            if row["original_target_syndrome"] != prior["uniform_target_syndrome"]:
                raise ArithmeticError("matched interval target silently changed")
            records.append({"input_source": "EXACT_SAVED_INTERVAL_LLL_TARGET_NOT_REROLLED", **row})
    for p in (257, 509, 1021):
        d, u = (p - 1) // 2, certified_radius(p)
        rng = random.Random(4471 + p)
        for label, word in (("canonical_ramp", list(range(p))),
                            ("spike", [p - 1] + [0] * (p - 1)),
                            ("uniform_public_word", [rng.randrange(p) for _ in range(p)])):
            records.append({"input_source": label, **solve(p, d, u, word)})
    impossible = solve(7, 3, 0, particular_for_syndrome(7, 3, [1, 0, 0]), attempts=3)
    if impossible["solution"] is not None:
        raise ArithmeticError("impossible zero-width nonzero-syndrome control accepted")
    deterministic = []
    for p in (31, 61, 127, 257):
        rng = random.Random(4507 + p)
        for label, word in (("uniform_public_word", [rng.randrange(p) for _ in range(p)]),
                            ("quarter_field_spike", [p // 4] + [0] * (p - 1))):
            row = solve_deterministic(p, p // 2, deterministic_radius(p), word)
            numerators = coefficient_numerators(p, word)
            nearest = multiply_basis(p, [(2 * a + p) // (2 * p) for a in numerators])
            nearest_norm = max(abs((y - a + p // 2) % p - p // 2) for y, a in zip(word, nearest))
            deterministic.append({"input_source": label, "naive_nearest_coefficient_residual_norm": nearest_norm, **row})
    return {"schema_version": "interval-character-rounding-v2",
            "local_derivation_status": "EXPLICIT_PROOF_PENDING_INDEPENDENT_REVIEW_NOT_FORMAL_VERIFICATION",
            "scope": "prime p, N=p support0..p-1, H_d[j,x]=x^j, d<=(p-1)/2, coordinatewise translated modular intervals",
            "asymptotic_statement": "all-target classical randomized polynomial search for u>=certified_radius(p)=O(sqrt(p log p)); ideal fresh exact coins",
            "basis_audits": [bounded_basis_audit(p) for p in (3, 5, 7, 11, 31)],
            "controls": records, "impossible_target_control": impossible,
            "deterministic_controls": deterministic,
            "all_saved_targets_have_verified_witnesses": all(r["solution"] is not None for r in records),
            "matched_input_report_sha256": hashlib.sha256(MATCHED_REPORT.read_bytes()).hexdigest(),
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "dependency_sha256": {name: hashlib.sha256((ROOT / "theorems" / name).read_bytes()).hexdigest()
                                  for name in ("bpqm_gibbs_frontier.py", "prime_character_capacity_source.py", "prime_character_opi.py")},
            "novelty_or_quantum_speedup_claimed": False,
            "arbitrary_sets_or_weighted_sampling_dequantized": False,
            "punctured_exponential_field_input_dequantized": False,
            "new_central_candidate_negative_or_proof_registered": False,
            "literature": ["https://arxiv.org/abs/2411.12553",
                           "https://doi.org/10.1002/sapm1933121311",
                           "https://doi.org/10.1080/01621459.1963.10500830",
                           "https://arxiv.org/abs/2202.07736",
                           "https://www2.eecs.berkeley.edu/Pubs/TechRpts/1987/5986.html"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"controls": len(report["controls"]),
                      "witnesses": sum(r["solution"] is not None for r in report["controls"]),
                      "certified_scaling_controls": [{"p": r["p"], "d": r["d"], "u": r["u"],
                          "input": r["input_source"], "norm": r["attempts"][-1]["centered_infinity_norm"],
                          "attempts": len(r["attempts"]), "failure_upper": r["failure_certificate"]["per_attempt_failure_upper_exact"]}
                          for r in report["controls"] if r["p"] > 127],
                      "deterministic": [{"p": r["p"], "input": r["input_source"],
                          "norm": r["centered_infinity_norm"], "naive_nearest_norm": r["naive_nearest_coefficient_residual_norm"],
                          "uniform_certificate": r["certificate"]["uniform_all_target_potential_certificate"]}
                          for r in report["deterministic_controls"]],
                      "impossible_target_status": report["impossible_target_control"]["status"]}, indent=2))


if __name__ == "__main__":
    main()
