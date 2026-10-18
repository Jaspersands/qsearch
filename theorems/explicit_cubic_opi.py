"""Compact cubic-target RS interpolation versus constructive classical attacks.

Known DQI score law only. No random-oracle lower bound, novel quantum circuit,
or hardness inference from an attack cap. Local derivations need review.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from functools import cached_property, lru_cache, reduce
import hashlib
from itertools import combinations
import json
from math import comb
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import flint
import numpy as np

from theorems.bpqm_gibbs_frontier import affine_system, integer
from theorems.explicit_quadratic_opi import (
    OPIReferenceLimit, element, encoded, evaluation_masks, field, filter_bound,
)
from theorems.linear_erasure_prange_duality import null_basis
from theorems.parity_block_usd_prange import uniform_affine_solution

REPORT = ROOT/"research/classical_baselines/explicit_cubic_opi.json"


@lru_cache(maxsize=64)
def monomials(variables):
    integer(variables, "Boolean variables", 1, 62)
    return tuple(sum(1 << i for i in indices)
                 for degree in range(4) for indices in combinations(range(variables), degree))


@dataclass(frozen=True)
class BooleanCubic:
    variables: int
    coefficients: int

    def __post_init__(self):
        integer(self.coefficients, "canonical RM(3,m) coefficient bits", 0,
                (1 << len(monomials(self.variables)))-1)

    @cached_property
    def terms(self):
        return tuple(mask for i, mask in enumerate(monomials(self.variables)) if (self.coefficients >> i) & 1)

    @cached_property
    def triples(self):
        return tuple(tuple(i for i in range(self.variables) if (mask >> i) & 1)
                     for mask in self.terms if mask.bit_count() == 3)

    def value(self, word):
        integer(word, "Boolean argument", 0, (1 << self.variables)-1)
        return sum((word & mask) == mask for mask in self.terms) % 2

    def polar_row(self, v, w):
        """Mask of a -> Delta_v Delta_w Delta_a g, by exact cubic contraction."""
        integer(v, "first direction", 0, (1 << self.variables)-1)
        integer(w, "second direction", 0, (1 << self.variables)-1)
        out = 0
        for i, j, k in self.triples:
            vi, vj, vk = (v >> i) & 1, (v >> j) & 1, (v >> k) & 1
            wi, wj, wk = (w >> i) & 1, (w >> j) & 1, (w >> k) & 1
            out ^= ((vj*wk) ^ (vk*wj)) << i
            out ^= ((vi*wk) ^ (vk*wi)) << j
            out ^= ((vi*wj) ^ (vj*wi)) << k
        return out


@dataclass(frozen=True)
class CubicOPI:
    bits: int
    length: int
    dimension: int
    transforms: tuple[tuple[int, ...], ...]
    polynomials: tuple[BooleanCubic, ...]

    def __post_init__(self):
        integer(self.bits, "field extension degree", 3, 63)
        integer(self.length, "distinct nonzero RS positions", 1, min(4095, (1 << self.bits)-1))
        integer(self.dimension, "RS coefficient dimension", 1, self.length)
        if (type(self.transforms) is not tuple or len(self.transforms) != self.length
                or type(self.polynomials) is not tuple or len(self.polynomials) != self.length
                or any(not isinstance(p, BooleanCubic) or p.variables != self.bits-1 for p in self.polynomials)):
            raise ValueError("canonical public predicate descriptions required")
        for rows in self.transforms:
            if (type(rows) is not tuple or len(rows) != self.bits
                    or any(type(x) is not int or not 0 <= x < 1 << self.bits for x in rows)
                    or affine_system(tuple((x, 0) for x in rows), self.bits)["rank"] != self.bits):
                raise ValueError("invertible binary predicate transform required")

    @property
    def message_bits(self):
        return self.bits*self.dimension

    @cached_property
    def forms(self):
        return tuple(tuple(reduce(int.__xor__, (row[b] for b in range(self.bits) if (h >> b) & 1), 0)
                           for h in T)
                     for row, T in zip(evaluation_masks(self.bits, self.dimension, self.length), self.transforms))

    def transformed_accepted(self, index, z):
        return ((z & 1) ^ self.polynomials[index].value(z >> 1)) == 0

    def accepted(self, index, symbol):
        integer(index, "predicate position", 0, self.length-1)
        integer(symbol, "field symbol", 0, (1 << self.bits)-1)
        z = sum(((h & symbol).bit_count() % 2) << j for j, h in enumerate(self.transforms[index]))
        return self.transformed_accepted(index, z)

    def evaluations(self, message):
        integer(message, "binary RS coefficient word", 0, (1 << self.message_bits)-1)
        coefficients = [element(self.bits, (message >> (j*self.bits)) & ((1 << self.bits)-1))
                        for j in range(self.dimension)]
        out = []
        for point in range(1, self.length+1):
            x, y = element(self.bits, point), field(self.bits).zero()
            for c in reversed(coefficients):
                y = y*x+c
            out.append(encoded(y))
        return out

    def score_count(self, message):
        return sum(self.accepted(i, y) for i, y in enumerate(self.evaluations(message)))

    def specification(self):
        return {"field_bits": self.bits, "positions": self.length, "RS_dimension": self.dimension,
                "message_bits": self.message_bits,
                "field_modulus_coefficients": list(map(int, field(self.bits).modulus().coeffs())),
                "predicate_transforms": [list(T) for T in self.transforms],
                "RM3_coefficients_hex": [hex(p.coefficients) for p in self.polynomials],
                "monomial_order": "degrees 0..3, itertools.combinations of coordinates 0..t-2",
                "acceptance_equation": "z0 = g(z1,...,z[t-1]); z=T_i y",
                "predicate_description_bits": self.length*(self.bits**2+len(monomials(self.bits-1))),
                "full_acceptance_tables_materialized": False, "membership_oracle_supplied": False}


def instance(bits, length, dimension, seed):
    integer(bits, "field bits", 3, 63)
    integer(length, "RS positions", 1, min(4095, (1 << bits)-1))
    integer(dimension, "RS dimension", 1, length)
    integer(seed, "public replay seed", 0, (1 << 64)-1)
    rng, transforms = random.Random(seed), []
    for _ in range(length):
        while True:
            rows = tuple(rng.getrandbits(bits) for _ in range(bits))
            if affine_system(tuple((h, 0) for h in rows), bits)["rank"] == bits:
                transforms.append(rows)
                break
    polys = tuple(BooleanCubic(bits-1, rng.getrandbits(len(monomials(bits-1)))) for _ in range(length))
    return CubicOPI(bits, length, dimension, tuple(transforms), polys)


def from_specification(spec):
    bits = spec["field_bits"]
    if spec["field_modulus_coefficients"] != list(map(int, field(bits).modulus().coeffs())):
        raise ValueError("field basis/modulus mismatch")
    if spec["monomial_order"] != "degrees 0..3, itertools.combinations of coordinates 0..t-2":
        raise ValueError("polynomial coefficient convention mismatch")
    return CubicOPI(bits, spec["positions"], spec["RS_dimension"],
                    tuple(tuple(T) for T in spec["predicate_transforms"]),
                    tuple(BooleanCubic(bits-1, int(x, 16)) for x in spec["RM3_coefficients_hex"]))


def accepted_flat(poly, seed=0, *, attempts=4, target_dimension=None):
    """Find a cubic-isotropic direction space; solve the affine base by Gaussian elimination.

    Inconsistency triggers a paid retry then dimension fallback, not source rejection.
    A checked witness is returned; no claim that it is a maximum flat.
    """
    m = poly.variables
    integer(seed, "flat search seed", 0, (1 << 64)-1)
    integer(attempts, "paid direction retries per dimension", 1, 64)
    if target_dimension is None:
        target_dimension = max(d for d in range(1, m+1) if comb(d, 2)+d <= m)
    integer(target_dimension, "requested flat dimension", 1, min(m, 12))
    rng, trace, contractions, solves, evaluations = random.Random(seed), [], 0, 0, 0
    for target in range(target_dimension, 0, -1):
        for trial in range(attempts):
            directions, rows = [], {}
            while len(directions) < target:
                system = affine_system(tuple((h, 0) for h in rows.values()), m)
                solves += 1
                span_system = affine_system(tuple((v, 0) for v in directions), m)
                solves += 1
                if m-system["rank"] <= len(directions):
                    break
                # Kernel contains the existing direction space. Avoid conditioning the input.
                v = None
                for _ in range(64):
                    candidate = uniform_affine_solution(system, m, rng)
                    test = affine_system(tuple((w, 0) for w in directions)+( (candidate, 0),), m)
                    solves += 1
                    if test["rank"] > span_system["rank"]:
                        v = candidate
                        break
                if v is None:
                    break
                for j, w in enumerate(directions):
                    rows[(j, len(directions))] = poly.polar_row(w, v)
                    contractions += 1
                directions.append(v)
            equations = []
            for (i, j), row in rows.items():
                v, w = directions[i], directions[j]
                rhs = poly.value(v ^ w) ^ poly.value(v) ^ poly.value(w) ^ poly.value(0)
                evaluations += 4
                equations.append((row, rhs))
            system = affine_system(tuple(equations), m)
            solves += 1
            trace.append({"requested_dimension": target, "trial": trial,
                          "achieved_direction_dimension": len(directions),
                          "base_system_rank": system["rank"], "base_consistent": system["consistent"]})
            if len(directions) != target or not system["consistent"]:
                continue
            base = uniform_affine_solution(system, m, rng)
            g0 = poly.value(base)
            slopes = [poly.value(base ^ v) ^ g0 for v in directions]
            evaluations += 1+len(directions)
            origin = (base << 1) | g0
            graph_directions = tuple((v << 1) | s for v, s in zip(directions, slopes))
            checks = null_basis(graph_directions, m+1)
            solves += 1
            # Independent pointwise validation of this small flat, not the full field table.
            for subset in range(1 << target):
                z = origin
                for j, v in enumerate(graph_directions):
                    if (subset >> j) & 1:
                        z ^= v
                evaluations += 1
                if (z & 1) != poly.value(z >> 1):
                    raise ArithmeticError("cubic polarization/base equations failed native acceptance")
            return {"dimension": target, "codimension": m+1-target, "origin": origin,
                    "directions": list(graph_directions), "parity_checks": list(checks),
                    "attempt_trace": trace, "linear_solves": solves,
                    "cubic_tensor_contractions": contractions, "polynomial_evaluations": evaluations,
                    "maximum_flat_certified": False, "source_rejected_or_resampled": False}
    raise ArithmeticError("every Boolean graph has an accepted affine line")


def _affine_coordinates(system, width):
    origin = sum(row[-1] << pivot for row, pivot in
                 zip((r for r in system["rref"] if any(r[:-1])), system["pivots"]))
    basis = []
    for free in system["free"]:
        v = 1 << free
        for row, pivot in zip((r for r in system["rref"] if any(r[:-1])), system["pivots"]):
            v |= row[free] << pivot
        basis.append(v)
    return origin, tuple(basis)


def optimize_affine_space(problem, system, *, max_free_bits=18):
    """Exact restricted cubic ANF interpolation + Mobius transform, all costs exposed."""
    integer(max_free_bits, "residual table dimension cap", 0, 22)
    if not system["consistent"]:
        raise ValueError("cannot optimize an inconsistent affine space")
    origin, basis = _affine_coordinates(system, problem.message_bits)
    d = len(basis)
    if d > max_free_bits:
        raise OPIReferenceLimit(f"UNKNOWN: {d} free bits exceed residual table cap {max_free_bits}")
    size = 1 << d
    scores = np.zeros(size, dtype=np.int32)
    small_masks = tuple(sum(1 << j for j in indices)
                       for degree in range(min(3, d)+1) for indices in combinations(range(d), degree))
    evaluations = 0
    for i, forms in enumerate(problem.forms):
        z0 = sum(((h & origin).bit_count() % 2) << j for j, h in enumerate(forms))
        zb = tuple(sum(((h & v).bit_count() % 2) << j for j, h in enumerate(forms)) for v in basis)
        values, table = {}, np.zeros(size, dtype=np.uint8)
        for mask in small_masks:
            z = z0
            for j in range(d):
                if (mask >> j) & 1:
                    z ^= zb[j]
            values[mask] = int(not problem.transformed_accepted(i, z))
            evaluations += 1
            sub, coefficient = mask, 0
            while True:
                coefficient ^= values[sub]
                if sub == 0:
                    break
                sub = (sub-1) & mask
            table[mask] = coefficient
        for j in range(d):
            blocks = table.reshape(-1, 1 << (j+1))
            blocks[:, 1 << j:] ^= blocks[:, :1 << j]
        np.subtract(1, table, out=table)
        scores += table
    best = int(np.argmax(scores))
    message = origin
    for j, v in enumerate(basis):
        if (best >> j) & 1:
            message ^= v
    score = int(scores[best])
    if problem.score_count(message) != score:
        raise ArithmeticError("restricted ANF optimizer failed independent field-Horner verification")
    return {"message_hex": hex(message), "score_count": score, "free_dimension": d,
            "candidate_messages_enumerated": size, "restricted_polynomial_evaluations": evaluations,
            "Mobius_xor_cells": problem.length*d*(size//2),
            "peak_table_entries": 2*size, "table_entry_widths_bits": [8, 32],
            "peak_candidate_dense_table_bytes": 5*size,
            "restricted_sample_dictionary_entries": len(small_masks),
            "affine_score_histogram": np.bincount(scores, minlength=problem.length+1).tolist(),
            "native_field_polynomial_evaluations": problem.length,
            "exact_optimum_on_this_affine_space": True, "global_optimum_claimed": False}


def flat_attack(problem, seed=0, *, flat_attempts=4, max_free_bits=18):
    integer(seed, "attack replay seed", 0, (1 << 64)-1)
    rng, equations, flats, failures = random.Random(seed), (), [], []
    solves = exposed = 0
    spent = {"linear_solves": 0, "cubic_tensor_contractions": 0, "polynomial_evaluations": 0}
    for position in range(problem.length):
        exposed += 1
        flat = accepted_flat(problem.polynomials[position], rng.getrandbits(64), attempts=flat_attempts)
        for key in spent:
            spent[key] += flat[key]
        if len(equations)+flat["codimension"] > problem.message_bits:
            break
        local = []
        for h in flat["parity_checks"]:
            lhs = reduce(int.__xor__, (f for j, f in enumerate(problem.forms[position]) if (h >> j) & 1), 0)
            local.append((lhs, (h & flat["origin"]).bit_count() % 2))
        system = affine_system(equations+tuple(local), problem.message_bits)
        solves += 1
        if not system["consistent"]:
            failures.append({"position": position, "flat": flat, "status": "THIS_FLAT_INCONSISTENT_NOT_OPI_UNSAT"})
            continue
        equations += tuple(local)
        flats.append({"position": position, "flat": flat})
    system = affine_system(equations, problem.message_bits)
    solves += 1
    try:
        optimized = optimize_affine_space(problem, system, max_free_bits=max_free_bits)
        status = "EXACT_RESIDUAL_AFFINE_OPTIMUM"
    except OPIReferenceLimit as exc:
        message = uniform_affine_solution(system, problem.message_bits, rng)
        optimized = {"message_hex": hex(message), "score_count": problem.score_count(message),
                     "free_dimension": len(system["free"]), "candidate_messages_enumerated": 1,
                     "native_field_polynomial_evaluations": problem.length,
                     "exact_optimum_on_this_affine_space": False, "cap_status": str(exc)}
        status = "RESIDUAL_OPTIMIZER_UNKNOWN_UNIFORM_FALLBACK"
    message = int(optimized["message_hex"], 16)
    symbols = problem.evaluations(message)
    if not all(problem.accepted(row["position"], symbols[row["position"]]) for row in flats):
        raise ArithmeticError("flat witness fails independent native field evaluation")
    optimized["native_field_polynomial_evaluations"] += problem.length
    return {"status": status, **optimized, "attack_seed": seed,
            "flat_attempts_per_dimension": flat_attempts, "residual_dimension_cap": max_free_bits,
            "exposed_predicate_prefix": exposed, "forced_positions": [row["position"] for row in flats],
            "flat_witnesses": flats, "failed_interpolation_attempts": failures,
            "flat_finder_work_including_unused_terminal_flat": spent,
            "message_space_linear_solves": solves, "message_space_rank": system["rank"],
            "source_rejected_or_resampled": False, "classical_hardness_inferred": False}


def arbitrary_flat_bound(bits, dimension, predicates=1):
    """First moment for ANY accepted d-flat of an IID uniform RM(3,t-1) graph."""
    integer(bits, "predicate width", 3, 255)
    integer(dimension, "accepted flat dimension", 0, bits-1)
    integer(predicates, "number of predicates in union", 1, 1 << bits)
    m, d = bits-1, dimension
    numerator = denominator = 1
    for i in range(d):
        numerator *= (1 << (m-i))-1
        denominator *= (1 << (d-i))-1
    gaussian = numerator//denominator
    if numerator % denominator:
        raise ArithmeticError("Gaussian binomial not integral")
    coefficient_dimension = sum(comb(d, j) for j in range(min(3, d)+1))
    count = predicates*(1 << bits)*gaussian
    raw = Fraction(count, 1 << coefficient_dimension)
    # Decimal conversion of enormous integers has a Python safety limit. Preserve
    # the exact dyadic expression without changing that interpreter-wide limit.
    decimal_safe = max(raw.numerator.bit_length(), raw.denominator.bit_length()) <= 12000
    ceil_log_count = count.bit_length()-int(count & (count-1) == 0)
    return {"field_bits": bits, "accepted_flat_dimension": d, "predicates": predicates,
            "RM3_restriction_dimension": coefficient_dimension,
            "raw_first_moment_union_bound": str(raw) if decimal_safe else None,
            "raw_first_moment_numerator_hex": hex(count),
            "raw_first_moment_denominator_power_two": coefficient_dimension,
            "probability_upper": str(min(1, raw)) if decimal_safe or raw >= 1 else None,
            "probability_upper_power_two_exponent": max(0, coefficient_dimension-ceil_log_count),
            "requires_IID_uniform_RM3_coefficients": True,
            "seeded_instances_are_not_probability_certificates": True,
            "absence_of_large_flats_proves_OPI_hardness": False,
            "local_derivation_review_pending": True}


def blind_pool_tail_bound(length, exposed, candidates, threshold):
    """Scoped IID suffix bound, allowing the winner to be selected using all scores.

    Candidate *pool* must depend only on an exposed predicate prefix. This
    upper-bounds this attack, not all classical algorithms or the quantum tail.
    """
    integer(length, "number of predicates", 1, 4095)
    integer(exposed, "exposed predicate prefix", 0, length)
    integer(candidates, "total candidate pool size", 1, 1 << 64)
    integer(threshold, "score threshold", 0, length)
    remaining, need = length-exposed, max(0, threshold-exposed)
    tail = Fraction(sum(comb(remaining, j) for j in range(need, remaining+1)), 1 << remaining)
    return {"score_threshold": threshold, "exposed_prefix": exposed, "candidate_pool_upper": candidates,
            "suffix_binomial_tail": str(tail), "success_probability_union_upper": str(min(1, candidates*tail)),
            "requires_independent_uniform_RM3_suffix_not_seeded_probability_certificate": True,
            "pool_must_be_fixed_before_suffix_scores_are_seen": True,
            "bounds_only_this_pool_not_all_classical_algorithms": True,
            "quantum_tail_or_runtime_comparison_supplied": False,
            "local_derivation_review_pending": True}


def run_controls():
    rows = []
    for bits, length, dimension in ((4, 7, 3), (15, 31, 9), (31, 31, 9), (31, 127, 39)):
        for seed in (29, 71):
            problem = instance(bits, length, dimension, seed)
            trials = [flat_attack(problem, seed+10000+1000*j) for j in range(4)]
            best = max(range(len(trials)), key=lambda j: trials[j]["score_count"])
            quantum = filter_bound(problem)
            mean_count = length*Fraction(quantum["expected_score_lower"])
            threshold = -(-mean_count.numerator//mean_count.denominator)
            rows.append({"public_seed": seed, "specification": problem.specification(),
                         "paid_classical_trials": trials, "best_trial_index": best,
                         "best_score_count": trials[best]["score_count"],
                         "known_quantum_filter_bound": quantum,
                         "IID_blind_pool_tail_bound": blind_pool_tail_bound(
                             length, max(t["exposed_predicate_prefix"] for t in trials),
                             sum(t["candidate_messages_enumerated"] for t in trials), threshold),
                         "all_predeclared_instances_and_attempts_retained": True,
                         "best_classical_score_vs_quantum_mean_is_not_a_matched_speedup_test": True})
    helpers = ("explicit_quadratic_opi.py", "bpqm_gibbs_frontier.py", "parity_block_usd_prange.py",
               "linear_erasure_prange_duality.py")
    return {"schema_version": "1.0", "subsystem": "explicit_cubic_opi", "instances": rows,
            "arbitrary_affine_flat_bounds": [arbitrary_flat_bound(3, 2), arbitrary_flat_bound(63, 20, 127)],
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "dependency_sha256": {name: hashlib.sha256((ROOT/"theorems"/name).read_bytes()).hexdigest() for name in helpers},
            "python_flint_version": flint.__version__, "numpy_version": np.__version__,
            "literature": ["https://arxiv.org/abs/1404.0654", "https://arxiv.org/abs/1410.1318",
                           "https://arxiv.org/html/2610.02145v2"],
            "accepted_speedup_candidate": False, "classical_hardness_proved": False,
            "new_quantum_algorithm_claimed": False, "oracle_problem_generated": False,
            "coherent_decoder_and_filter_executed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(json.dumps([{"bits": row["specification"]["field_bits"], "N": row["specification"]["positions"],
                       "K": row["specification"]["RS_dimension"], "seed": row["public_seed"],
                       "classical_scores": [trial["score_count"] for trial in row["paid_classical_trials"]],
                       "quantum_filter_mean": row["known_quantum_filter_bound"]["expected_score_lower_decimal"]}
                      for row in report["instances"]], indent=2))


if __name__ == "__main__":
    main()
