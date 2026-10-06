"""Exact A2 ternary congruence geometry and ordinary pair-finder falsifiers.

LOCAL DERIVATIONS / REVIEW PENDING. LLL/Babai outputs are verified witnesses,
not closest-vector certificates, coverage guarantees, or a quantum speedup.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from itertools import islice, product
import json
import math
from pathlib import Path
import random
import time

from flint import fmpz_mat

from native_rlwe_primal_babai import exact_row_profile, nearest_plane
from ternary_pair_collimation import LowProblem, verify_pair

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/ternary_pair_lattice.json"


def _positive(value, name):
    if type(value) is not int or value < 1:
        raise ValueError(f"positive integer {name} required")
    return value


def embed(z):
    z = tuple(z)
    if not z or len(z) % 2 or any(type(x) is not int for x in z):
        raise ValueError("nonempty canonical integer pairs required")
    return tuple(x for a, b in zip(z[::2], z[1::2]) for x in (a+b, -a, -b))


def inverse_embed(point):
    point = tuple(point)
    if not point or len(point) % 3 or any(type(x) is not int for x in point):
        raise ValueError("canonical integer A2 plane point required")
    if any(sum(point[i:i+3]) for i in range(0, len(point), 3)):
        raise ValueError("point is outside the A2 planes")
    return tuple(x for i in range(0, len(point), 3) for x in (-point[i+1], -point[i+2]))


def word_coordinates(word):
    word = tuple(word)
    if not word or any(type(x) is not int or x not in (0, 1, 2) for x in word):
        raise ValueError("canonical native ternary word required")
    return tuple(int(x == digit) for x in word for digit in (1, 2))


def shell_norm(z):
    z = tuple(z)
    embed(z)
    return sum(x*x for x in embed(tuple(3*x-1 for x in z)))


def decode_shell(z):
    z = tuple(z)
    norm = shell_norm(z)
    M = len(z)//2
    if norm != 6*M:
        return None
    alphabet = {(0, 0): 0, (1, 0): 1, (0, 1): 2}
    word = tuple(alphabet.get(pair) for pair in zip(z[::2], z[1::2]))
    if any(x is None for x in word):
        raise ArithmeticError("exact A2 shell identity failed")
    return word


def scalar_labels(problem):
    if not isinstance(problem, LowProblem) or len(problem.moduli) != 1:
        raise ValueError("original scalar stripped-label problem required")
    return tuple(row[0] for pair in problem.frequencies for row in pair)


def congruence_basis(problem):
    """Complete scalar kernel, including nonunits via an exact gcd quotient."""
    original = scalar_labels(problem); original_Q = problem.moduli[0]
    g = math.gcd(original_Q, *original)
    A = tuple(a//g for a in original); Q = original_Q//g; d = len(A)
    pivot = next(i for i, a in enumerate(A) if math.gcd(a, Q) == 1)
    inv = pow(A[pivot], -1, Q) if Q > 1 else 0
    B = []
    for j in range(d):
        row = [0]*d
        if j == pivot:
            row[j] = Q
        else:
            row[j] = 1
            row[pivot] = -(A[j]*inv % Q)
        B.append(tuple(row))
    assert abs(int(fmpz_mat(B).det())) == Q
    return {"labels": original, "original_modulus": original_Q, "common_divisor": g,
            "normalized_labels": A, "modulus": Q, "pivot": pivot, "inverse": inv,
            "kernel_rows": tuple(B), "embedded_rows": tuple(tuple(3*x for x in embed(row)) for row in B),
            "kernel_index": Q, "gram_determinant": 3**(5*problem.width)*Q*Q}


def coset_target(problem, target, geometry):
    t, = problem.target(target)
    if t % geometry["common_divisor"]:
        return None
    t //= geometry["common_divisor"]
    z0 = [0]*(2*problem.width)
    z0[geometry["pivot"]] = t*geometry["inverse"] % geometry["modulus"]
    E0, center = embed(z0), embed([1]*len(z0))
    return tuple(z0), tuple(a-3*b for a, b in zip(center, E0))


def extract_witness(problem, target, z0, lattice_point):
    if any(type(x) is not int or x % 3 for x in lattice_point):
        raise ValueError("integer embedded lattice point divisible by three required")
    l = inverse_embed(tuple(x//3 for x in lattice_point))
    if len(l) != len(z0):
        raise ValueError("coset dimension mismatch")
    z = tuple(a+b for a, b in zip(z0, l))
    word = decode_shell(z)
    if word is not None and problem.value(word) != problem.target(target):
        raise ValueError("shell word is not in the original congruence coset")
    return word, z, shell_norm(z)


def _round(value):
    return (2*value.numerator+value.denominator)//(2*value.denominator)


def nearest_plane_list(rows, target, profile):
    """One exact Babai path plus each single +/-1 rounding deviation.

    Lower coordinates are recomputed after the forced deviation. List size is
    1+2*rank, not enumeration of all combinations of rounding errors.
    """
    d = len(rows); mu = profile["mu"]; gs = profile["gs_squared"]
    inner = []
    for i, row in enumerate(rows):
        inner.append(sum(a*b for a, b in zip(row, target))-
                     sum(mu[i][j]*inner[j] for j in range(i)))
    original = [inner[i]/gs[i] for i in range(d)]
    for forced, sign in [(None, 0)]+[(i, sign) for i in range(d-1, -1, -1) for sign in (-1, 1)]:
        coordinates = list(original); coeff = [0]*d
        for i in range(d-1, -1, -1):
            coeff[i] = _round(coordinates[i])+(sign if i == forced else 0)
            for j in range(i):
                coordinates[j] -= coeff[i]*mu[i][j]
        point = tuple(sum(coeff[i]*rows[i][j] for i in range(d)) for j in range(len(target)))
        yield {"point": point, "coefficients": tuple(coeff), "forced_row": forced,
               "forced_deviation": sign, "rounding_steps": d}


def prepared_bases(problem, seed=0, basis_count=2):
    _positive(basis_count, "basis count")
    if type(seed) is not int:
        raise ValueError("public integer seed required")
    geometry = congruence_basis(problem)
    original = fmpz_mat(geometry["embedded_rows"]); d = original.nrows()
    rng = random.Random(seed); bases = []
    for index in range(basis_count):
        order = list(range(d))
        if index: rng.shuffle(order)
        permutation = [[0]*d for _ in range(d)]
        for i, j in enumerate(order): permutation[i][j] = 1 if not index else rng.choice((-1, 1))
        P = fmpz_mat(permutation)
        reduced, transform = (P*original).lll(transform=True, gram="exact")
        transform = transform*P
        if transform*original != reduced or abs(int(transform.det())) != 1:
            raise ArithmeticError("LLL changed the integer lattice")
        rows = tuple(tuple(int(x) for x in row) for row in reduced.tolist())
        profile = exact_row_profile(rows)
        if profile["leading_gram_determinants"][-1] != geometry["gram_determinant"]:
            raise ArithmeticError("embedded Gram determinant mismatch")
        bases.append({"rows": rows, "transform": tuple(tuple(int(x) for x in row) for row in transform.tolist()),
                      "profile": profile})
    return geometry, bases


def public_center_offsets(width, seed=0, perturbations=2):
    _positive(width, "native width")
    if type(seed) is not int or type(perturbations) is not int or perturbations < 0:
        raise ValueError("integer public seed and nonnegative perturbation count required")
    rng = random.Random(seed)
    offsets = [(Fraction(0),)*(3*width)]
    for _ in range(perturbations):
        vector = embed([rng.choice((-1, 1)) for _ in range(2*width)])
        offsets.append(tuple(Fraction(x, 12*width) for x in vector))
    return tuple(offsets)


def lattice_pair(problem, target, seed=0, basis_count=2, max_decodes=256,
                 max_width=32, perturbations=2, prepared=None):
    """Work-capped public classical baseline; no internal LLL time deadline."""
    A = scalar_labels(problem); target = problem.target(target)
    _positive(max_decodes, "decode cap"); _positive(max_width, "width cap")
    _positive(basis_count, "basis count")
    if type(perturbations) is not int or perturbations < 0:
        raise ValueError("nonnegative public perturbation count required")
    if type(seed) is not int:
        raise ValueError("integer public seed required")
    cost = {"lll_calls": 0, "exact_profiles": 0, "candidate_decodes": 0, "rounding_steps": 0,
            "duplicate_verified_words": 0, "non_shell_candidates": 0, "decode_cap": max_decodes,
            "uses_only_stripped_labels_and_target": True, "lll_internal_time_deadline": False,
            "finite_width_guard": max_width, "asymptotic_pair_coverage_proved": False}
    if problem.width > max_width:
        return {"status": "WIDTH_GUARD_NO_PAIR", "pair": (), "witnesses": (), "cost": cost, "attempts": []}
    if target[0] % math.gcd(problem.moduli[0], *A):
        return {"status": "DIVISIBILITY_CERTIFIED_EMPTY_TARGET", "pair": (), "witnesses": (), "cost": cost, "attempts": []}
    if prepared is None:
        prepared = prepared_bases(problem, seed, basis_count)
        cost["lll_calls"] = cost["exact_profiles"] = basis_count
    else:
        # Reuse is explicit and checked; its preparation costs belong to the caller.
        if prepared[0]["labels"] != A or prepared[0]["original_modulus"] != problem.moduli[0]:
            raise ValueError("prepared basis belongs to different public labels")
        cost["preparation_charged_by_caller"] = True
    geometry, bases = prepared
    z0, target_row = coset_target(problem, target, geometry)
    targets = [tuple(x+y for x, y in zip(target_row, offset))
               for offset in public_center_offsets(problem.width, seed, perturbations)]
    found, attempts, exhausted = [], [], False
    for basis_index, basis in enumerate(bases):
        for center_index, center in enumerate(targets):
            remaining = max_decodes-cost["candidate_decodes"]
            if not remaining:
                exhausted = True; break
            for answer in islice(nearest_plane_list(basis["rows"], center, basis["profile"]), remaining):
                cost["candidate_decodes"] += 1; cost["rounding_steps"] += answer["rounding_steps"]
                word, z, norm = extract_witness(problem, target, z0, answer["point"])
                record = {"basis": basis_index, "center": center_index, "forced_row": answer["forced_row"],
                          "forced_deviation": answer["forced_deviation"], "exact_original_norm": str(norm),
                          "word": word}
                if word is None: cost["non_shell_candidates"] += 1
                elif word in found: cost["duplicate_verified_words"] += 1
                else:
                    found.append(word)
                    record.update({"integer_coset_coordinates": z, "embedded_lattice_point": answer["point"],
                                   "reduced_basis_coefficients": answer["coefficients"]})
                attempts.append(record)
                if len(found) == 2:
                    return {"status": "VERIFIED_PAIR_NO_COVERAGE_THEOREM", "pair": verify_pair(problem, target, found),
                            "witnesses": tuple(found), "cost": cost, "attempts": attempts}
            if remaining < 1+2*len(basis["rows"]):
                exhausted = True
            if exhausted: break
        if exhausted: break
    return {"status": "DECODE_CAP_NO_PAIR" if exhausted else "HEURISTIC_SEARCH_EXHAUSTED_NOT_UNSAT_PROOF",
            "pair": (), "witnesses": tuple(found), "cost": cost, "attempts": attempts}


def deflated_second_witness(problem, target, first, seed=0, max_sub_decodes=1):
    """Force a changed native digit, then decode a smaller ordinary coset.

    This is a polynomial number of HEURISTIC calls. A pointwise single-witness
    guarantee on every sliced instance would imply pair completeness; success
    on the original random distribution alone does not imply that guarantee.
    """
    scalar_labels(problem); target = problem.target(target); first = tuple(first)
    word_coordinates(first)
    if len(first) != problem.width or problem.value(first) != target:
        raise ValueError("verified original first witness required")
    if type(seed) is not int: raise ValueError("public integer seed required")
    _positive(max_sub_decodes, "subinstance decode cap")
    attempts = []; cost = {"maximum_slice_calls": 2*problem.width, "slice_calls": 0,
                          "lll_calls": 0, "candidate_decodes": 0, "rounding_steps": 0,
                          "direct_terminal_checks": 0, "pointwise_solver_guarantee_supplied": False}
    Q = problem.moduli[0]
    for i in range(problem.width):
        for digit in range(3):
            if digit == first[i]: continue
            fixed = problem.frequencies[i][digit-1][0] if digit else 0
            residual = (target[0]-fixed) % Q; cost["slice_calls"] += 1
            if problem.width == 1:
                cost["direct_terminal_checks"] += 1
                candidate = (digit,) if residual == 0 else None
                status = "DIRECT_ORIGINAL_DIGIT_CHECK"
            else:
                sub = LowProblem((Q,), problem.frequencies[:i]+problem.frequencies[i+1:], 0)
                solved = lattice_pair(sub, (residual,), seed+3*i+digit, basis_count=1,
                                      perturbations=0, max_decodes=max_sub_decodes)
                for key in ("lll_calls", "candidate_decodes", "rounding_steps"):
                    cost[key] += solved["cost"][key]
                word = solved["witnesses"][0] if solved["witnesses"] else None
                candidate = (*word[:i], digit, *word[i:]) if word is not None else None
                status = solved["status"]
            attempts.append({"fixed_coordinate": i, "fixed_digit": digit, "residual_target": str(residual),
                             "status": status, "candidate": candidate})
            if candidate is not None:
                return {"status": "VERIFIED_DEFLATED_SECOND_WITNESS",
                        "pair": verify_pair(problem, target, (first, candidate)), "cost": cost, "attempts": attempts}
    return {"status": "SLICES_EXHAUSTED_NO_PAIR_NOT_UNSAT_PROOF", "pair": (), "cost": cost, "attempts": attempts}


def complete_census():
    """All Q9/M1 labels and independent targets; not planted witnesses."""
    counters = Counter(); cases = []; C_weighted_decodes = 0; total_decodes = 0
    for a, c in product(range(9), repeat=2):
        problem = LowProblem((9,), (((a,), (c,)),), 0)
        prepared = prepared_bases(problem, seed=83271, basis_count=1)
        for t in range(9):
            answer = lattice_pair(problem, (t,), seed=83271, basis_count=1,
                                  max_decodes=15, perturbations=2, prepared=prepared)
            actual = tuple(w for w in product(range(3), repeat=1) if problem.value(w) == (t,))
            counters["uniform_target_instances"] += 1
            counters["truth_pairs"] += len(actual) >= 2
            counters["found_pairs"] += bool(answer["pair"])
            counters["found_single_witness_or_pair"] += bool(answer["witnesses"])
            counters["divisibility_certified_empty_targets"] += answer["status"] == "DIVISIBILITY_CERTIFIED_EMPTY_TARGET"
            total_decodes += answer["cost"]["candidate_decodes"]
            C_weighted_decodes += len(actual)*answer["cost"]["candidate_decodes"]
            if answer["pair"]: assert set(answer["pair"]).issubset(set(actual))
            cases.append({"labels": (a, c), "target": t, "fiber_size": len(actual),
                          "pair": answer["pair"], "single_witness_count": len(answer["witnesses"]),
                          "status": answer["status"], "decodes": answer["cost"]["candidate_decodes"]})
    beta = Fraction(counters["found_pairs"], counters["uniform_target_instances"])
    return {**dict(counters), "uniform_pair_coverage_exact": str(beta), "all_cases": cases,
            "exact_source_average_informative_acceptance": str(4*beta),
            "exact_source_average_raw_least_trit_success": str(Fraction(1, 3)+4*beta/3),
            "decode_work_uniform_average": str(Fraction(total_decodes, 729)),
            "decode_work_Born_average": str(Fraction(3*C_weighted_decodes, 729)),
            "basis_preparation_lll_calls_separately_charged": 81,
            "basis_preparations_per_label_array_before_all_nine_targets": 1,
            "decode_work_excludes_separately_charged_basis_preparation": True}


def uniform_sweep(digits=(4, 8, 12, 16, 24, 32), trials=16, seed=83270, max_decodes=None):
    _positive(trials, "IID trials")
    rng = random.Random(seed); records = []
    for r in digits:
        if type(r) is not int or r < 3: raise ValueError("native root digits at least three required")
        M = r-2; Q = 3**(r-1)
        for trial in range(trials):
            A = tuple(rng.randrange(Q) for _ in range(2*M)); t = rng.randrange(Q)
            problem = LowProblem((Q,), tuple(((a,), (c,)) for a, c in zip(A[::2], A[1::2])), 0)
            public_seed = rng.randrange(2**32); start = time.perf_counter()
            cap = 6*(1+4*M) if max_decodes is None else max_decodes
            solved = lattice_pair(problem, (t,), public_seed, max_decodes=cap)
            deflated = None
            if len(solved["witnesses"]) == 1:
                deflated = deflated_second_witness(problem, (t,), solved["witnesses"][0], public_seed)
            wall = time.perf_counter()-start
            # Reference costs are separate, never supplied to the lattice attack.
            truth = None
            if 3**M <= 60_000:
                truth = sum(problem.value(w) == (t,) for w in product(range(3), repeat=M))
            records.append({"root_digits": r, "width": M, "modulus": str(Q), "labels": [str(a) for a in A],
                            "target": str(t), "trial": trial, "public_seed": public_seed,
                            "reference_fiber_size": truth, "reference_word_enumerations": 3**M if truth is not None else 0,
                            "pair": solved["pair"], "witnesses": solved["witnesses"], "status": solved["status"],
                            "deflated_second_witness": deflated,
                            "cost": solved["cost"], "wall_seconds_including_basis_preparation": wall,
                            "truth_unknown_does_not_mean_hard": truth is None})
    summaries = []
    for r in digits:
        group = [x for x in records if x["root_digits"] == r]; successes = sum(bool(x["pair"]) for x in group)
        summaries.append({"root_digits": r, "IID_trials": trials, "pairs_found": successes,
                          "one_witness_or_pair": sum(bool(x["witnesses"]) for x in group),
                          "pairs_after_coordinate_deflation": sum(bool(x["pair"] or (x["deflated_second_witness"] or {}).get("pair")) for x in group),
                          "deflation_slice_calls": sum((x["deflated_second_witness"] or {}).get("cost", {}).get("slice_calls", 0) for x in group),
                          "deflation_lll_calls": sum((x["deflated_second_witness"] or {}).get("cost", {}).get("lll_calls", 0) for x in group),
                          "deflation_candidate_decodes": sum((x["deflated_second_witness"] or {}).get("cost", {}).get("candidate_decodes", 0) for x in group),
                          "empirical_uniform_pair_coverage_not_a_proof": str(Fraction(successes, trials)),
                          "zero_success_probability_if_population_beta_1_over_32": str(Fraction(31, 32)**trials),
                          "total_candidate_decodes": sum(x["cost"]["candidate_decodes"] for x in group),
                          "total_lll_calls": sum(x["cost"]["lll_calls"] for x in group),
                          "wall_seconds": sum(x["wall_seconds_including_basis_preparation"] for x in group)})
    return {"IID_fresh_labels_and_independent_uniform_target_each_trial": True,
            "planted_or_conditioned_nonempty_targets": False, "summaries": summaries, "trials": records,
            "no_confidence_or_polynomial_coverage_claim": True,
            "beta_source_transfer_requires_population_coverage_not_sample_fraction": True}


def build_report():
    census = complete_census(); sweep = uniform_sweep()
    example = LowProblem((27,), (((1,), (7,)), ((11,), (18,))), 0)
    geometry, bases = prepared_bases(example, seed=83270, basis_count=2)
    controls = []
    for t in range(27):
        answer = lattice_pair(example, (t,), 83270, prepared=(geometry, bases), max_decodes=54)
        z0, T = coset_target(example, (t,), geometry)
        controls.append({"target": t, "z0": z0, "target_row": T, **answer})
    return {"status": "EXACT_REPRESENTATION_ORDINARY_HEURISTIC_NO_SPEEDUP",
            "local_derivations_review_pending": True, "polynomial_pair_finder_proved": False,
            "quantum_secret_given_to_attack": False, "new_algorithm_claim": False,
            "native_problem": "scalar stripped original ternary source; Q=3^(r-1), M=r-2",
            "legal_norm": "6*M", "minimum_illegal_norm": "6*M+18",
            "approximate_CVP_factor_sufficient_to_exclude_illegal_if_a_word_exists_squared": "strictly_less_than_1+3/M",
            "two_distinct_witnesses_not_one_closest_vector_required": True,
            "coordinate_deflation_pointwise_single_witness_oracle_calls_at_most": "2*M+1",
            "average_case_original_single_witness_coverage_is_not_sliced_pointwise_guarantee": True,
            "kernel_gram_determinant": "3^(5*M)*(Q/g)^2, g=gcd(Q,A); for g=1 at source scale,3^(7*M+2)",
            "nonunit_labels_resolved_by_exact_common_gcd_quotient": True,
            "inconsistent_gcd_target_is_a_genuine_empty_coset_certificate": True,
            "exact_census": census, "scaling": sweep,
            "independent_replay_control": {"modulus": 27, "labels": (1, 7, 11, 18), "geometry": geometry,
                                           "bases": [{"rows": b["rows"], "transform": b["transform"]} for b in bases],
                                           "targets": controls},
            "blockers": ["No polynomial uniform-target two-witness coverage theorem.",
                         "LLL/Babai failure is not a classical hardness certificate.",
                         "No scalar-to-vector native problem reduction supplied.",
                         "Preparation, physical syndrome retention, and Born-weighted runtime remain charged."]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(); report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": report["status"], "exact_beta": report["exact_census"]["uniform_pair_coverage_exact"],
                      "scaling": report["scaling"]["summaries"]}, indent=2))
