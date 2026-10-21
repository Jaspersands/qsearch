"""Matched explicit folded norm predicates and classical square completions.

No membership oracle, source selection or claimed hard regime. Every search
proposal is charged; all final witnesses are verified on the original input.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from functools import cached_property
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import random
import sys

from flint import fq_default_poly_ctx

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.bpqm_gibbs_frontier import integer
from theorems.folded_norm_source import character, dyadic_upper, extension_model, fraction, score_certificate
from theorems.prime_character_capacity_source import rational
from theorems.prime_character_opi import interpolate, ring

REPORT = ROOT / "research/classical_baselines/folded_norm_attacks.json"


@dataclass(frozen=True)
class Problem:
    p: int
    n: int
    m: int
    K: int
    gamma: int
    shifts: tuple
    signs: tuple
    include_zero: bool = True

    def __post_init__(self):
        ring(self.p)
        integer(self.n, "native blocks", 1, 4096)
        integer(self.m, "odd folding factor", 1, 63)
        integer(self.K, "native scalar polynomial dimension", self.m, self.n*self.m - 1)
        integer(self.gamma, "folding generator", 1, self.p - 1)
        if self.p % 4 != 3 or self.m % 2 != 1 or type(self.include_zero) is not bool:
            raise ValueError("this explicit flat family requires p3mod4, odd m and a zero policy")
        if (len(self.shifts) != self.n or any(len(t) != self.m for t in self.shifts)
                or any(type(a) is not int or not 0 <= a < self.p for t in self.shifts for a in t)
                or len(self.signs) != self.n or any(type(a) is not int or a not in (-1, 1) for a in self.signs)):
            raise ValueError("canonical complete public shifts and signs required")
        if len(set(self.points)) != self.n*self.m:
            raise ValueError("distinct folding powers required")

    @cached_property
    def points(self):
        points, x = [], 1
        for _ in range(self.n*self.m):
            points.append(x)
            x = x*self.gamma % self.p
        return tuple(points)

    def specification(self):
        return {"p_decimal": str(self.p), "n_blocks": self.n, "m_fold": self.m,
                "ORIGINAL_scalar_dimension_K": self.K, "gamma": self.gamma,
                "shifts": [list(t) for t in self.shifts], "signs": list(self.signs),
                "include_zero": self.include_zero,
                "field": extension_model(self.p, self.m)["record"]}

    def evaluate(self, coefficients):
        if len(coefficients) > self.K or any(type(a) is not int or not 0 <= a < self.p for a in coefficients):
            raise ValueError("canonical polynomial below ORIGINAL scalar dimension required")
        values = list(map(int, ring(self.p)(list(coefficients)).multipoint_evaluate(self.points)))
        model = extension_model(self.p, self.m)
        E = model["field"]
        accepted = []
        for i in range(self.n):
            z = E(values[i*self.m:(i + 1)*self.m]) - E(list(self.shifts[i]))
            accepted.append(character(model, z) == self.signs[i] or (self.include_zero and z == 0))
        return values, accepted


def instance(p, n, m, K, gamma, seed, *, include_zero=True):
    rng = random.Random(seed)
    return Problem(p, n, m, K, gamma,
                   tuple(tuple(rng.randrange(p) for _ in range(m)) for _ in range(n)),
                   tuple(rng.choice((-1, 1)) for _ in range(n)), include_zero)


def population_tail(p, n, m, K, threshold, *, include_zero=True, nonadaptive_trials=1):
    """IID-SHIFT population law, NOT a fixed-input or adaptive-repair law."""
    ring(p)
    integer(n, "blocks", 1, 4096)
    integer(m, "block symbols", 1, 63)
    integer(K, "scalar polynomial dimension", m, n*m - 1)
    integer(threshold, "native accepted count threshold", 0, n + 1)
    integer(nonadaptive_trials, "charged nonadaptive fits", 1, 4096)
    if type(include_zero) is not bool:
        raise ValueError("explicit zero convention required")
    b, Q = K // m, p ** m
    free = n - b
    eta = 1 if include_zero else -1
    numerator = sum(math.comb(free, j)*(Q + eta) ** j*(Q - eta) ** (free - j)
                    for j in range(max(0, threshold - b), free + 1))
    denominator = (2*Q) ** free
    probability = Fraction(numerator, denominator)
    return {"scope": "TRULY_IID_UNIFORM_PUBLIC_SHIFTS_POPULATION_ONLY",
            "guaranteed_complete_blocks": b, "remaining_binomial_trials": free,
            "single_trial_tail_upper_128bit_dyadic": rational(dyadic_upper(probability)),
            "nonadaptive_trials": nonadaptive_trials,
            "nonadaptive_union_upper_128bit_dyadic": rational(dyadic_upper(min(Fraction(1), nonadaptive_trials*probability))),
            "fixed_input_or_independent_restarts_law": False,
            "adaptive_block_exchange_covered": False,
            "source_assumption": "shifts independent uniform E, anchor selection independent of unanchored shift values; arbitrary fixed public signs"}


def joint_acceptance_error(p, m, K, blocks, *, include_zero=True):
    """Fixed-input Fourier/MDS bound for ANY selected predicate subset."""
    ring(p)
    integer(m, "flat odd extension degree", 1, 63)
    integer(K, "effective scalar coefficient dimension", 1, 1 << 20)
    integer(blocks, "selected block count", 0, 4096)
    if p % 4 != 3 or m % 2 != 1 or type(include_zero) is not bool:
        raise ValueError("flat odd-extension family and explicit zero policy required")
    if m*blocks <= K:
        return Fraction(0)
    Q = p ** m
    root = math.isqrt(Q + 1)
    root += int(root*root < Q + 1)
    rho = Fraction(Q + (1 if include_zero else -1), 2*Q)
    # Nonzero indicator Fourier magnitude is sqrt(Q+1)/(2Q).
    # Summing the safe p^(m*r-K) bound for every Fourier support yields
    # p^-K * (rho + sqrt(Q+1)/2)^blocks, including harmless extra terms.
    return (rho + Fraction(root, 2)) ** blocks / p ** K


def fixed_input_fit_tail(p, n, m, K, threshold, *, include_zero=True, fits=32):
    """Fresh FULL-anchor square fits, NOT repairs or arbitrary classical search."""
    ring(p)
    integer(n, "blocks", 1, 4096)
    integer(m, "odd block degree", 1, 63)
    integer(K, "allowed scalar dimension", m, n*m - 1)
    integer(threshold, "accepted-count target", 0, n + 1)
    integer(fits, "fresh complete-block proposals", 1, 1 << 30)
    if n*m > p - 1 or p % 4 != 3 or m % 2 != 1 or type(include_zero) is not bool:
        raise ValueError("distinct scalar points and flat odd-extension family required")
    b, Q = K // m, p ** m
    effective = b*m  # The implemented fit leaves the final K%m coefficients0.
    rho = Fraction(Q + (1 if include_zero else -1), 2*Q)
    bias = min(Fraction(1), Fraction(b*(Q - 1), Q*(Q + 1))) if include_zero else Fraction(0)
    needed, free = threshold - b, n - b
    witnesses, best, order = [], Fraction(1), 0
    if threshold == n + 1:
        best = Fraction(0)
    elif needed > 0:
        for r in range(1, needed + 1):
            joint_error = joint_acceptance_error(p, m, effective, b + r, include_zero=include_zero)
            conditional = min(Fraction(1), Fraction(math.comb(free, r), math.comb(needed, r))
                              * (rho ** r + joint_error / rho ** b))
            bound = dyadic_upper(min(Fraction(1), conditional + bias))
            witnesses.append({"factorial_moment_order": r, "fit_tail_upper_128bit_dyadic": rational(bound)})
            if bound < best:
                best, order = bound, r
    half = Fraction(1, 2) / best if best else None
    count = -(-half.numerator // half.denominator) if half is not None else None
    return {"scope": "FIXED_PUBLIC_INPUT_FRESH_FULL_ANCHOR_SAMPLING_CLASS_ONLY",
            "p_decimal": str(p), "n_blocks": n, "m_fold": m, "allowed_dimension_K": K,
            "effective_uniform_polynomial_dimension": effective, "scalar_degrees_unused": K - effective,
            "guaranteed_accepted_anchors": b, "target_accepted_count": threshold,
            "indicator_density_exact": rational(rho),
            "root_square_sampler_TV_from_uniform_anchor_conditioning_upper_exact": rational(bias),
            "factorial_moment_witness": order, "checked_factorial_moment_bounds": witnesses,
            "one_fresh_fit_success_upper_128bit_dyadic": rational(best),
            "fits": fits, "union_success_upper_128bit_dyadic": rational(dyadic_upper(min(Fraction(1), fits*best))),
            "necessary_fits_for_half_success_in_this_sampling_class": count,
            "no_IID_public_shift_or_independent_restart_assumption": True,
            "adaptive_anchor_choice_covered_ONLY_when_ALL_targets_freshly_resampled": True,
            "retained_anchor_block_exchange_or_other_adaptive_repairs_covered": False,
            "deterministic_seed_selection_is_not_uniform_root_randomness": True,
            "all_classical_algorithms_or_general_norm_solvers_bounded": False,
            "premises": "distinct-point scalar RS generator, arbitrary fixed public shifts/signs; independent uniform E square roots on ALL anchors each proposal; exact native F_p interpolation",
            "local_Fourier_and_factorial_moment_derivation_review_pending": True}


def attack(problem, *, seed=4813, trials=32, repair_steps=64):
    integer(trials, "charged complete-block fits", 1, 4096)
    integer(repair_steps, "charged block-exchange proposals", 0, 4096)
    p, n, m, K = problem.p, problem.n, problem.m, problem.K
    model = extension_model(p, m)
    E, rng, anchors = model["field"], random.Random(seed), K // m
    nonsquare = next(a for a in range(2, p) if pow(a, (p - 1) // 2, p) == p - 1)
    records, best, square_draws = [], None, 0

    def accepted_values(block):
        nonlocal square_draws
        while True:
            root = E([rng.randrange(p) for _ in range(m)])
            square_draws += 1
            if problem.include_zero or root != 0:
                break
        z = (E(1) if problem.signs[block] == 1 else E(nonsquare))*root*root + E(list(problem.shifts[block]))
        return list(map(int, z.to_list()))

    def proposal(selected, targets, phase):
        points = tuple(problem.points[i*m + r] for i in selected for r in range(m))
        values = tuple(a for block in selected for a in targets[block])
        poly, _ = interpolate(p, points, values)
        coefficients = [int(poly[i]) for i in range(K)]
        native, flags = problem.evaluate(coefficients)
        if any(not flags[i] for i in selected):
            raise ArithmeticError("square completion did not satisfy its actual native anchor")
        record = {"phase": phase, "anchor_blocks": list(selected), "score": sum(flags),
                  "accepted_blocks": [i for i, yes in enumerate(flags) if yes],
                  "polynomial_coefficients": coefficients}
        records.append(record)
        return record, native, flags

    for _ in range(trials):
        selected = sorted(rng.sample(range(n), anchors))
        row, native, flags = proposal(selected, {i: accepted_values(i) for i in selected}, "complete_block_square_interpolation")
        if best is None or row["score"] > best[0]["score"]:
            best = row, native, flags
    for _ in range(repair_steps):
        row, native, flags = best
        bad = [i for i, yes in enumerate(flags) if not yes]
        if not bad:
            break
        old, new = rng.choice(row["anchor_blocks"]), rng.choice(bad)
        selected = sorted([i for i in row["anchor_blocks"] if i != old] + [new])
        targets = {i: native[i*m:(i + 1)*m] for i in selected if i != new}
        targets[new] = accepted_values(new)
        next_row, next_native, next_flags = proposal(selected, targets, "block_exchange_square_completion")
        next_row["accepted_as_current"] = next_row["score"] >= row["score"]
        if next_row["accepted_as_current"]:
            best = next_row, next_native, next_flags
    spec = problem.specification()
    binding = hashlib.sha256(json.dumps(spec, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {"specification": spec, "input_sha256": binding, "seed_for_replay_only": seed,
            "trials_requested": trials, "repair_steps_requested": repair_steps,
            "proposals": records, "best_polynomial_coefficients": best[0]["polynomial_coefficients"],
            "best_score": best[0]["score"], "best_accepted_blocks": best[0]["accepted_blocks"],
            "complete_block_interpolation_guarantee": anchors,
            "scalar_degrees_unused_by_anchor_rounding": K % m,
            "source_rerolls": 0, "hidden_oracle_or_field_table_used": False,
            "field_square_draws_charged": square_draws,
            "public_base_field_nonsquare_tests_charged": nonsquare - 1,
            "folding_point_products_charged": n*m,
            "polynomial_interpolations_charged": len(records),
            "native_norm_character_evaluations_charged": n*len(records),
            "native_scalar_values_evaluated_charged": n*m*len(records),
            "scope": "finite unchanged public input; not a runtime comparison or classical hardness result",
            "global_quadratic_system_solver_or_norm_pencil_attack_implemented": False}


def _polynomial_product(context, factors):
    if not factors:
        return context(1)
    while len(factors) > 1:
        factors = [factors[i]*factors[i + 1] if i + 1 < len(factors) else factors[i]
                   for i in range(0, len(factors), 2)]
    return factors[0]


def norm_line_polynomial(model, a, b):
    """Compile Norm(a*T+b) by Frobenius products, checking F_p descent."""
    E, p, m = model["field"], model["p"], model["m"]
    R = ring(p)
    if a == 0:
        return R([int(b.norm())]), {"extension_norm_checks": 1,
                                   "extension_frobenius_maps": 0,
                                   "extension_polynomial_products": 0}
    S = fq_default_poly_ctx(E)
    aa, bb, factors = a, b, []
    for _ in range(m):
        factors.append(S([bb, aa]))
        aa, bb = aa.frobenius(), bb.frobenius()
    if aa != a or bb != b:
        raise ArithmeticError("Frobenius orbit did not close in the declared field")
    norm = _polynomial_product(S, factors)
    coefficients = []
    for c in norm.coeffs():
        coordinates = list(map(int, c.to_list()))
        if any(coordinates[1:]):
            raise ArithmeticError("norm polynomial did not descend to the ORIGINAL base field")
        coefficients.append(coordinates[0] if coordinates else 0)
    result = R(coefficients)
    if result.degree() != m or int(result[m]) != int(a.norm()) or int(result[0]) != int(b.norm()):
        raise ArithmeticError("norm polynomial degree or endpoint norm checks failed")
    return result, {"extension_norm_checks": 2,
                    "extension_frobenius_maps": 2*m,
                    "extension_polynomial_products": m - 1}


def pencil_pattern_certificate(p, m, norm_polynomials, signs, *, include_zero=True):
    """Known Weil bound for one FIXED line, after checking its square classes.

    Counting all-good parameters is not an efficient method of finding one.
    Zero/duplicate/conflicting predicates are never treated as independent.
    """
    R = ring(p)
    integer(m, "odd separable norm degree", 1, 63)
    if m % 2 == 0 or m >= p or type(include_zero) is not bool:
        raise ValueError("odd norm degree below p and explicit zero policy required")
    if (len(norm_polynomials) != len(signs) or not signs
            or any(type(sign) is not int or sign not in (-1, 1) for sign in signs)):
        raise ValueError("one canonical sign per norm polynomial required")
    classes, reductions, failed_constants, conflicts = {}, [], [], []
    gcds, irreducibility_tests = 0, 0
    for block, (record, sign) in enumerate(zip(norm_polynomials, signs)):
        poly = R(record["norm_polynomial_coefficients"])
        if poly.degree() <= 0:
            value = int(poly[0])
            symbol = 0 if value == 0 else (1 if pow(value, (p - 1)//2, p) == 1 else -1)
            if symbol != sign and not (include_zero and value == 0):
                failed_constants.append(block)
            continue
        if poly.degree() != m:
            raise ValueError("variable polynomial does not have the declared norm degree")
        squarefree = (poly // poly.gcd(poly.derivative())).monic()
        gcds += 1
        degree, leading = squarefree.degree(), int(poly[m])
        irreducibility_tests += 1
        if (not squarefree.is_irreducible() or m % degree
                or (m//degree) % 2 != 1 or R(leading)*squarefree ** (m//degree) != poly):
            raise ValueError("norm polynomial is not a verified odd power of one irreducible orbit")
        orientation = sign*(1 if pow(leading, (p - 1)//2, p) == 1 else -1)
        key = tuple(map(int, squarefree.coeffs()))
        reductions.append({"block": block, "monic_irreducible_coefficients": list(key),
                           "odd_power": m//degree, "leading_coefficient": leading,
                           "required_monic_character": orientation})
        if key in classes:
            if classes[key]["required_monic_character"] != orientation:
                conflicts.append(block)
            classes[key]["blocks"].append(block)
        else:
            classes[key] = {"monic_irreducible_coefficients": list(key), "degree": degree,
                            "required_monic_character": orientation, "blocks": [block]}
    r, total_degree = len(classes), sum(row["degree"] for row in classes.values())
    linear_roots = sum(row["degree"] == 1 for row in classes.values())
    root = math.isqrt(p) + int(math.isqrt(p) ** 2 < p)
    if failed_constants or conflicts:
        lower, coefficient = 0, None
    elif not r:
        lower, coefficient = p, 0
    else:
        denominator = 1 << r
        coefficient = (denominator//2)*total_degree - denominator + 1
        numerator = p - coefficient*root - denominator*linear_roots
        lower = max(0, -(-numerator//denominator))
    return {"scope": "ONE_FIXED_NATIVE_PENCIL_NONZERO_PATTERN_COUNT_LOWER_BOUND",
            "monic_irreducible_orbit_reductions": reductions,
            "distinct_square_classes": list(classes.values()),
            "number_of_distinct_variable_square_classes": r,
            "sum_of_distinct_irreducible_degrees": total_degree,
            "distinct_base_field_roots_subtracted": linear_roots,
            "failed_constant_blocks": failed_constants,
            "conflicting_duplicate_square_class_blocks": conflicts,
            "Weil_sum_error_coefficient_before_2_power_denominator": coefficient,
            "sqrt_p_integer_ceiling": root,
            "all_variable_nonzero_and_all_blocks_accepted_parameters_lower": lower,
            "one_fresh_uniform_base_field_parameter_success_lower_exact": rational(Fraction(lower, p)),
            "positive_count_is_not_an_efficient_finding_algorithm": True,
            "applies_to_adaptive_line_choice_only_after_its_actual_polynomials_are_checked": True,
            "independent_predicate_or_IID_public_input_assumption": False,
            "seeded_finite_transcript_is_not_a_uniform_randomness_certificate": True,
            "analysis_costs": {"base_field_squarefree_GCDs": gcds,
                               "base_field_irreducibility_tests": irreducibility_tests,
                               "base_field_odd_power_reconstructions": len(reductions),
                               "base_field_constant_or_leading_Legendre_evaluations": len(signs)},
            "local_application_of_known_Weil_bound_review_pending": True}


def pencil_attack(problem, coefficients, *, seed=4921, rounds=4, parameters=2048):
    """Retained-value native polynomial lines; outside the fresh-full-fit bound.

    The finite parameter budget is an experiment, not a tail certificate or
    an efficient solver for arbitrary inputs. No extension coefficient freedom.
    """
    integer(rounds, "native norm-pencil rounds", 1, 256)
    integer(parameters, "parameters including zero per pencil", 1, 1 << 16)
    p, n, m, K = problem.p, problem.n, problem.m, problem.K
    model, R, rng = extension_model(p, m), ring(p), random.Random(seed)
    E = model["field"]
    current = list(coefficients)
    native, flags = problem.evaluate(current)
    start_score, records = sum(flags), []
    parameter_count = min(parameters, p)
    for _ in range(rounds):
        accepted = [i for i, yes in enumerate(flags) if yes]
        selected = sorted(rng.sample(accepted, min(len(accepted), (K - 1)//m)))
        roots = [i*m + r for i in selected for r in range(m)]
        extra = K - 1 - len(roots)
        if extra:
            remaining = [i for i in range(n) if i not in selected]
            if extra < m:
                available_accepted = [i for i in remaining if flags[i]]
                block = rng.choice(available_accepted or remaining)
                roots.extend(block*m + r for r in rng.sample(range(m), extra))
            else:
                roots.extend(rng.sample([i*m + r for i in remaining for r in range(m)], extra))
        roots.sort()
        direction = _polynomial_product(R, [R([-problem.points[j], 1]) for j in roots])
        v_values = list(map(int, direction.multipoint_evaluate(problem.points)))
        if direction.degree() != K - 1 or any(v_values[j] for j in roots):
            raise ArithmeticError("native degree/retained-coordinate pencil invariant failed")
        chosen, seen, draws = [0], {0}, 0
        if parameter_count == p:
            chosen = list(range(p))  # Only possible for p<=the explicit finite budget.
        else:
            while len(chosen) < parameter_count:
                value = rng.randrange(p)
                draws += 1
                if value not in seen:
                    seen.add(value)
                    chosen.append(value)
        scores, polynomials = [0]*len(chosen), []
        costs = {"extension_norm_checks": 0, "extension_frobenius_maps": 0,
                 "extension_polynomial_products": 0,
                 "base_field_norm_polynomial_evaluations": 0,
                 "base_field_Legendre_evaluations": 0}
        for i in range(n):
            a = E(v_values[i*m:(i + 1)*m])
            b = E(native[i*m:(i + 1)*m]) - E(list(problem.shifts[i]))
            poly, setup = norm_line_polynomial(model, a, b)
            for key, value in setup.items():
                costs[key] += value
            constant = poly.degree() <= 0
            values = [int(poly[0])] if constant else list(map(int, poly.multipoint_evaluate(chosen)))
            costs["base_field_norm_polynomial_evaluations"] += len(values)
            costs["base_field_Legendre_evaluations"] += len(values)
            hits = []
            for value in values:
                symbol = 0 if value == 0 else (1 if pow(value, (p - 1)//2, p) == 1 else -1)
                hits.append(symbol == problem.signs[i] or (problem.include_zero and value == 0))
            if constant:
                scores = [score + int(hits[0]) for score in scores]
            else:
                scores = [score + int(hit) for score, hit in zip(scores, hits)]
            polynomials.append({"block": i, "constant_on_pencil": constant,
                                "norm_polynomial_coefficients": list(map(int, poly.coeffs()))})
        if scores[0] != sum(flags):
            raise ArithmeticError("norm-pencil zero parameter changed the original score")
        pattern = pencil_pattern_certificate(p, m, polynomials, problem.signs,
                                             include_zero=problem.include_zero)
        # A nonzero equal-score move explores a new line without lowering score.
        winner = max(range(len(chosen)), key=lambda j: (scores[j], chosen[j] != 0))
        parameter = chosen[winner]
        base_poly = R(current)
        next_coefficients = [int(base_poly[j] + parameter*direction[j]) for j in range(K)]
        next_native, next_flags = problem.evaluate(next_coefficients)
        compiled_flags = []
        for row in polynomials:
            value = 0
            for coefficient in reversed(row["norm_polynomial_coefficients"]):
                value = (value*parameter + coefficient) % p
            symbol = 0 if value == 0 else (1 if pow(value, (p - 1)//2, p) == 1 else -1)
            compiled_flags.append(symbol == problem.signs[row["block"]] or (problem.include_zero and value == 0))
        costs["winner_norm_polynomial_Horner_checks"] = n
        costs["winner_Legendre_checks"] = n
        if (next_native != [(x + parameter*y) % p for x, y in zip(native, v_values)]
                or next_flags != compiled_flags or sum(next_flags) != scores[winner]
                or any(not next_flags[i] for i in selected)):
            raise ArithmeticError("native polynomial verification disagreed with compiled norm predicates")
        records.append({"base_polynomial_coefficients": current,
                        "retained_accepted_blocks": selected, "retained_scalar_indices": roots,
                        "direction_polynomial_coefficients": list(map(int, direction.coeffs())),
                        "direction_base_field_polynomial_products": max(0, len(roots) - 1),
                        "parameter_values": chosen, "parameter_rng_draws": draws,
                        "parameter_generation": "ALL_BASE_FIELD_PARAMETERS" if parameter_count == p else "DISTINCT_BASE_FIELD_SAMPLES_INCLUDING_ZERO",
                        "scores": scores, "starting_score": sum(flags), "best_score": scores[winner],
                        "winner_parameter": parameter, "norm_polynomials": polynomials,
                        "fixed_line_character_pattern_certificate": pattern,
                        "precomputation_and_evaluation_costs": costs,
                        "winner_polynomial_coefficients": next_coefficients,
                        "winner_accepted_blocks": [i for i, yes in enumerate(next_flags) if yes]})
        current, native, flags = next_coefficients, next_native, next_flags
    return {"method": "NATIVE_RETAINED_VALUE_FROBENIUS_NORM_PENCILS",
            "seed_for_replay_only": seed, "rounds_requested": rounds,
            "parameters_requested_including_zero": parameters,
            "starting_score": start_score, "best_score": sum(flags),
            "best_polynomial_coefficients": current,
            "best_accepted_blocks": [i for i, yes in enumerate(flags) if yes],
            "pencils": records, "source_rerolls": 0,
            "native_scalar_values_evaluated_for_base_and_winner_checks": n*m*(1 + rounds),
            "native_extension_norm_characters_for_base_and_winner_checks": n*(1 + rounds),
            "direction_scalar_values_evaluated": n*m*rounds,
            "shared_public_field_setup_recorded_in_input_specification": True,
            "full_extension_field_table_or_extension_coefficient_relaxation": False,
            "fresh_full_fit_bound_applies_to_this_attack": False,
            "general_quadratic_system_solver_implemented": False,
            "finite_search_failure_is_a_hardness_certificate": False,
            "scope": "adaptive finite same-input classical search; no independent-score law, general runtime guarantee or quantum refutation"}


def run_controls():
    controls = []
    for n, K, ell in ((25, 310, 6), (65, 806, 15), (127, 1550, 30)):
        problem = instance((1 << 61) - 1, n, 31, K, 3, 4877 + n)
        baseline = attack(problem)
        pencil = pencil_attack(problem, baseline["best_polynomial_coefficients"])
        pencil["input_sha256"] = baseline["input_sha256"]
        reference = score_certificate(problem.p, n, 31, K, ell, thresholds=(baseline["best_score"],))
        mean = n*fraction(reference["heralded_mean_lower_exact"])
        threshold = -(-mean.numerator // mean.denominator)
        target_reference = score_certificate(problem.p, n, 31, K, ell, thresholds=(threshold,))
        if target_reference["heralded_mean_lower_exact"] != reference["heralded_mean_lower_exact"]:
            raise ArithmeticError("the same source unexpectedly changed its finite mean")
        reference["tails"].extend(target_reference["tails"])
        controls.append({"classical": baseline, "native_norm_pencil_attack": pencil,
                         "conditional_quantum_reference": reference,
                         "population_first_trial_reference_NOT_fixed_instance_law": population_tail(problem.p, n, 31, K, threshold, nonadaptive_trials=32),
                         "fixed_input_fresh_full_fit_sampling_bound": fixed_input_fit_tail(problem.p, n, 31, K, threshold),
                         "classical_word_exceeds_conditional_quantum_mean_lower_bound":
                         baseline["best_score"] > n*fraction(reference["heralded_mean_lower_exact"]),
                         "norm_pencil_word_exceeds_conditional_quantum_mean_lower_bound":
                         pencil["best_score"] > mean,
                         "exceeding_a_mean_lower_bound_refutes_quantum_algorithm_or_proves_dequantization": False,
                         "matched_runtime_advantage_or_candidate_accepted": False})
    return {"schema_version": "folded-norm-attacks-v2", "controls": controls,
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "dependency_sha256": {name: hashlib.sha256((ROOT / "theorems" / name).read_bytes()).hexdigest()
                                  for name in ("folded_norm_source.py", "folded_rs_decoder.py", "prime_character_opi.py", "bpqm_gibbs_frontier.py")}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print(json.dumps([{"n": r["classical"]["specification"]["n_blocks"],
                       "classical_score": r["classical"]["best_score"],
                       "norm_pencil_score": r["native_norm_pencil_attack"]["best_score"],
                       "norm_pencil_parameter_scores": sum(len(row["scores"]) for row in r["native_norm_pencil_attack"]["pencils"]),
                       "proposals": r["classical"]["polynomial_interpolations_charged"],
                       "conditional_quantum_mean_lower": float(fraction(r["conditional_quantum_reference"]["heralded_mean_lower_exact"]))*r["classical"]["specification"]["n_blocks"],
                       "target": r["fixed_input_fresh_full_fit_sampling_bound"]["target_accepted_count"],
                       "fixed_input_fresh_FULL_fit_success_upper": float(fraction(r["fixed_input_fresh_full_fit_sampling_bound"]["one_fresh_fit_success_upper_128bit_dyadic"])),
                       "conditional_quantum_composition_target_success_lower": float(fraction(r["conditional_quantum_reference"]["tails"][-1]["bounded_pruning_one_attempt_lower_exact"])),
                       "partial_repair_and_general_classical_algorithms_NOT_bounded": True}
                      for r in report["controls"]], indent=2))


if __name__ == "__main__":
    main()
