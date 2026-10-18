"""Explicit balanced quadratic OPI inputs versus structural classical attacks.

Known balanced-DQI score law; no oracle hardness transfer or new quantum
algorithm. FLINT supplies finite-field arithmetic; SMT limits mean UNKNOWN.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from functools import cached_property, lru_cache, reduce
import hashlib
import json
from math import comb, isqrt, sqrt
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import flint
from flint import fq_default_ctx
import numpy as np

from theorems.bpqm_gibbs_frontier import affine_system, integer
from theorems.parity_block_usd_prange import uniform_affine_solution

REPORT = ROOT/"research/classical_baselines/explicit_quadratic_opi.json"


class OPIReferenceLimit(RuntimeError):
    pass


@lru_cache(maxsize=8)
def field(bits):
    return fq_default_ctx(2, bits)


def element(bits, word):
    return field(bits)([(word >> i) & 1 for i in range(bits)])


def encoded(value):
    return sum(int(c) << i for i, c in enumerate(value.to_list()))


@lru_cache(maxsize=16)
def evaluation_masks(bits, dimension, length=None):
    length = (1 << bits)-1 if length is None else length
    integer(length, "distinct nonzero RS positions", 1, (1 << bits)-1)
    integer(dimension, "RS coefficient dimension", 1, length)
    F = field(bits)
    rows = []
    for point in range(1, length+1):
        x, power = element(bits, point), F.one()
        output = [0]*bits
        for j in range(dimension):
            for bit in range(bits):
                image = encoded(power*element(bits, 1 << bit))
                for b in range(bits):
                    if (image >> b) & 1:
                        output[b] ^= 1 << (j*bits+bit)
            power *= x
        rows.append(tuple(output))
    return tuple(rows)


@dataclass(frozen=True)
class QuadraticOPI:
    bits: int
    dimension: int
    transforms: tuple[tuple[int, ...], ...]
    offsets: tuple[int, ...]

    def __post_init__(self):
        integer(self.bits, "field extension degree", 3, 9)
        if self.bits % 2 == 0:
            raise ValueError("odd extension degree gives one radical plus hyperbolic pairs")
        integer(self.dimension, "RS coefficient dimension", 1, self.length)
        if (type(self.transforms) is not tuple or len(self.transforms) != self.length
                or type(self.offsets) is not tuple or len(self.offsets) != self.length
                or any(type(b) is not int or b not in (0, 1) for b in self.offsets)):
            raise ValueError("canonical immutable predicate descriptions required")
        for rows in self.transforms:
            if (type(rows) is not tuple or len(rows) != self.bits
                    or any(type(x) is not int or not 0 <= x < 1 << self.bits for x in rows)
                    or affine_system(tuple((x, 0) for x in rows), self.bits)["rank"] != self.bits):
                raise ValueError("invertible binary predicate transform required")

    @property
    def length(self):
        return (1 << self.bits)-1

    @property
    def message_bits(self):
        return self.bits*self.dimension

    @cached_property
    def forms(self):
        evaluations = evaluation_masks(self.bits, self.dimension)
        return tuple(tuple(reduce(int.__xor__, (linear[b] for b in range(self.bits) if (row >> b) & 1), 0)
                           for row in transform)
                     for linear, transform in zip(evaluations, self.transforms))

    def accepted(self, index, symbol):
        integer(index, "position", 0, self.length-1)
        integer(symbol, "field symbol", 0, self.length)
        z = [(mask & symbol).bit_count() % 2 for mask in self.transforms[index]]
        value = z[0] ^ self.offsets[index]
        for j in range(1, self.bits, 2):
            value ^= z[j]*z[j+1]
        return value == 0

    def evaluations(self, message):
        integer(message, "binary coefficient encoding", 0, (1 << self.message_bits)-1)
        coefficients = [element(self.bits, (message >> (j*self.bits)) & self.length) for j in range(self.dimension)]
        values = []
        for point in range(1, self.length+1):
            x, value = element(self.bits, point), field(self.bits).zero()
            for coefficient in reversed(coefficients):
                value = value*x+coefficient
            values.append(encoded(value))
        return values

    def score_count(self, message):
        return sum(self.accepted(i, y) for i, y in enumerate(self.evaluations(message)))

    def specification(self):
        return {"field_bits": self.bits, "field_modulus_coefficients": list(map(int, field(self.bits).modulus().coeffs())),
                "positions": self.length, "RS_dimension": self.dimension, "message_bits": self.message_bits,
                "predicate_transforms": [list(t) for t in self.transforms], "predicate_offsets": list(self.offsets),
                "predicate_quadratic_rank": self.bits-1,
                "predicate_description_bits": self.length*(self.bits*self.bits+1),
                "full_acceptance_tables_materialized": False, "membership_oracle_supplied": False}


def instance(bits, dimension, seed):
    integer(bits, "field bits", 3, 9)
    if bits % 2 == 0:
        raise ValueError("odd field degree required")
    integer(dimension, "RS coefficient dimension", 1, (1 << bits)-1)
    integer(seed, "public replay seed", 0, (1 << 64)-1)
    rng, rows = random.Random(seed), []
    for _ in range((1 << bits)-1):
        while True:
            candidate = tuple(rng.getrandbits(bits) for _ in range(bits))
            if affine_system(tuple((x, 0) for x in candidate), bits)["rank"] == bits:
                rows.append(candidate)
                break
    return QuadraticOPI(bits, dimension, tuple(rows), tuple(rng.randrange(2) for _ in rows))


def affine_flat_attack(problem, seed=0):
    """Interpolate inside accepted affine flats, not arbitrary accepted points."""
    integer(seed, "attack replay seed", 0, (1 << 64)-1)
    rng = random.Random(seed)
    pairs = (problem.bits-1)//2
    codimension = pairs+1
    prefix = min(problem.length, problem.message_bits//codimension)
    equations, forced, solves = (), [], 0
    for position in range(prefix):
        forms = problem.forms[position]
        choices = list(range(1 << pairs))
        rng.shuffle(choices)
        for choice in choices:
            # Fix each odd hyperbolic coordinate; the residual constraint is linear.
            final = forms[0]
            local = []
            for j in range(pairs):
                bit = (choice >> j) & 1
                local.append((forms[2*j+1], bit))
                if bit:
                    final ^= forms[2*j+2]
            local.append((final, problem.offsets[position]))
            solves += 1
            system = affine_system(equations+tuple(local), problem.message_bits)
            if system["consistent"]:
                equations += tuple(local)
                forced.append(position)
                break
    system = affine_system(equations, problem.message_bits)
    word = uniform_affine_solution(system, problem.message_bits, rng)
    values = problem.evaluations(word)
    if not all(problem.accepted(i, values[i]) for i in forced):
        raise ArithmeticError("accepted-flat constraints failed independent field evaluation")
    return {"method": "accepted_affine_flat_interpolation", "message_hex": hex(word),
            "score_count": sum(problem.accepted(i, y) for i, y in enumerate(values)), "forced_positions": forced,
            "untouched_positions": list(range(prefix, problem.length)), "prefix_budget": prefix,
            "flat_codimension": codimension, "binary_rank": system["rank"],
            "linear_system_solves": solves, "uniform_solution_bits": problem.message_bits-system["rank"],
            "native_field_polynomial_evaluations": problem.length,
            "instance_rejected_or_resampled": False,
            "rank_count_alone_guarantees_consistency": False,
            "conditional_expected_score_numerator_from_forced_and_untouched": str(Fraction(len(forced))+Fraction(problem.length-prefix, 2)),
            "expectation_requires_independent_unused_offsets_not_a_fixed_instance_guarantee": True}


def fixed_flat_attack(problem):
    """Executable all-zero-flat algorithm used in the IID rank argument."""
    equations = tuple(pair for forms, offset in zip(problem.forms, problem.offsets)
                      for pair in [*((forms[j], 0) for j in range(1, problem.bits, 2)), (forms[0], offset)])
    system = affine_system(equations, problem.message_bits)
    report = {"method": "all_positions_fixed_zero_flat_linear_solver", "linear_system_solves": 1,
              "binary_rows": len(equations), "binary_rank": system["rank"],
              "full_row_rank": system["rank"] == len(equations),
              "status": "THIS_FIXED_FLAT_IS_INCONSISTENT", "message_hex": None,
              "original_OPI_unsatisfiable_claimed": False, "native_witness_verified": False}
    if system["consistent"]:
        word = uniform_affine_solution(system, problem.message_bits, random.Random(0))
        if problem.score_count(word) != problem.length:
            raise ArithmeticError("fixed flat solution failed native-field verification")
        report.update(status="PERFECT_NATIVE_WITNESS", message_hex=hex(word), native_witness_verified=True)
    return report


def restarted_flat_attack(problem, seed, restarts=16):
    integer(seed, "restart seed", 0, (1 << 64)-1)
    integer(restarts, "paid restart count", 1, 128)
    rng = random.Random(seed)
    trials = [affine_flat_attack(problem, rng.getrandbits(64)) for _ in range(restarts)]
    best = max(range(restarts), key=lambda i: trials[i]["score_count"])
    return {"method": "paid_random_restarts_of_affine_flat_interpolation", "restart_count": restarts,
            "trials": trials, "best_trial_index": best,
            "message_hex": trials[best]["message_hex"], "score_count": trials[best]["score_count"],
            "total_linear_system_solves": sum(t["linear_system_solves"] for t in trials),
            "total_native_field_polynomial_evaluations": restarts*problem.length,
            "full_instance_scoring_used_to_choose_best": True,
            "better_than_quantum_expected_score_proves_asymptotic_dequantization": False}


def _affine_words(system, width, max_free_bits):
    if not system["consistent"]:
        raise ValueError("consistent affine neighborhood required")
    free = system["free"]
    if len(free) > max_free_bits:
        raise OPIReferenceLimit("UNKNOWN: released affine neighborhood dimension cap")
    particular = 0
    directions = [1 << f for f in free]
    for row, pivot in zip(system["rref"], system["pivots"]):
        particular |= row[-1] << pivot
        for j, f in enumerate(free):
            if row[f]:
                directions[j] |= 1 << pivot
    word, previous = particular, 0
    for i in range(1 << len(free)):
        gray = i ^ (i >> 1)
        if i:
            word ^= directions[(gray ^ previous).bit_length()-1]
        previous = gray
        yield word


def _accepted_message(forms, offset, word):
    z = [(mask & word).bit_count() % 2 for mask in forms]
    value = z[0] ^ offset
    for j in range(1, len(z), 2):
        value ^= z[j]*z[j+1]
    return value == 0


def repair_flat_attack(problem, initial_message, forced_positions, seed, *, passes=None, max_free_bits=12):
    """Release one flat; exactly optimize the remaining small affine neighborhood.

    Preserve every selected predicate's actual nonlinear acceptance. This is
    a capped classical heuristic, not a global optimizer or mixing theorem.
    """
    integer(seed, "repair seed", 0, (1 << 64)-1)
    integer(max_free_bits, "neighborhood enumeration bits", 1, 20)
    if (type(forced_positions) is not tuple or len(set(forced_positions)) != len(forced_positions)
            or any(type(i) is not int or not 0 <= i < problem.length for i in forced_positions)):
        raise ValueError("unique immutable native forced positions required")
    values = problem.evaluations(initial_message)
    if not all(problem.accepted(i, values[i]) for i in forced_positions):
        raise ValueError("initial native word does not satisfy the retained predicates")
    current = initial_message
    score = sum(problem.accepted(i, y) for i, y in enumerate(values))
    initial_score = score
    passes = problem.length-score+1 if passes is None else passes
    integer(passes, "paid repair passes", 1, problem.length+1)
    rng, improvements = random.Random(seed), []
    neighborhoods = skipped = candidates = predicate_evaluations = 0
    maximum_free = 0
    passes_executed, fixed_point = 0, score == problem.length
    for pass_index in range(passes):
        before = score
        skipped_before = skipped
        passes_executed += 1
        order = list(forced_positions)
        rng.shuffle(order)
        for released in order:
            if score == problem.length:
                break
            equations = []
            for i in forced_positions:
                if i == released:
                    continue
                forms, final = problem.forms[i], problem.forms[i][0]
                for j in range(1, problem.bits, 2):
                    value = (forms[j] & current).bit_count() % 2
                    equations.append((forms[j], value))
                    if value:
                        final ^= forms[j+1]
                equations.append((final, problem.offsets[i]))
            system = affine_system(tuple(equations), problem.message_bits)
            if not system["consistent"]:
                raise ArithmeticError("current native word disappeared from its own flat neighborhood")
            neighborhoods += 1
            free = len(system["free"])
            maximum_free = max(maximum_free, free)
            if free > max_free_bits:
                skipped += 1
                continue
            best_word, best_score = current, score
            for word in _affine_words(system, problem.message_bits, max_free_bits):
                candidates += 1
                predicate_evaluations += 1
                if not _accepted_message(problem.forms[released], problem.offsets[released], word):
                    continue
                candidate_score = sum(_accepted_message(f, b, word) for f, b in zip(problem.forms, problem.offsets))
                predicate_evaluations += problem.length
                if candidate_score > best_score:
                    best_word, best_score = word, candidate_score
            if best_score > score:
                current, score = best_word, best_score
                improvements.append({"pass_index": pass_index, "released_position": released,
                                     "message_hex": hex(current), "score_count": score})
        if score == before or score == problem.length:
            fixed_point = score == problem.length or skipped == skipped_before
            break
    values = problem.evaluations(current)
    if (sum(problem.accepted(i, y) for i, y in enumerate(values)) != score
            or not all(problem.accepted(i, values[i]) for i in forced_positions)):
        raise ArithmeticError("binary repair score failed independent native field verification")
    return {"method": "exact_single_flat_release_neighborhood_repair", "seed": seed,
            "initial_message_hex": hex(initial_message), "initial_score_count": initial_score,
            "message_hex": hex(current), "score_count": score, "retained_nonlinear_positions": list(forced_positions),
            "passes_budget": passes, "max_free_bits": max_free_bits,
            "passes_executed": passes_executed, "uncapped_local_fixed_point_reached": fixed_point,
            "linear_neighborhood_solves": neighborhoods, "skipped_UNKNOWN_dimension_caps": skipped,
            "maximum_free_dimension_seen": maximum_free, "candidate_words_enumerated": candidates,
            "binary_predicate_evaluations": predicate_evaluations,
            "native_field_polynomial_evaluations": 2*problem.length,
            "improvement_trace": improvements, "full_native_witness_verified": True,
            "global_optimum_or_polynomial_success_guaranteed": False,
            "counts_are_high_level_not_bit_operation_complexity": True}


def from_specification(spec):
    bits = spec["field_bits"]
    integer(bits, "field degree", 3, 9)
    if list(map(int, field(bits).modulus().coeffs())) != spec["field_modulus_coefficients"]:
        raise ValueError("field basis changed; explicit transport needed before replay")
    return QuadraticOPI(bits, spec["RS_dimension"],
                        tuple(tuple(t) for t in spec["predicate_transforms"]), tuple(spec["predicate_offsets"]))


def flat_rank_failure_bound(bits, dimension, positions=None):
    """Local MDS/random-subspace union bound; no empirical hardness inference."""
    integer(bits, "odd field degree", 3, 9)
    if bits % 2 == 0:
        raise ValueError("odd field degree required")
    q, N = 1 << bits, (1 << bits)-1
    integer(dimension, "RS dimension", 1, N)
    m = N if positions is None else positions
    integer(m, "number of constrained public positions", 1, N)
    codimension = (bits+1)//2
    p = Fraction((1 << codimension)-1, q-1)
    raw = sum((Fraction(comb(m, w)*(q**(w-dimension)-1))*p**w
               for w in range(dimension+1, m+1)), Fraction())
    upper = min(Fraction(1), raw)
    exponent = None if not upper else (upper.denominator//upper.numerator).bit_length()-1
    return {"field_bits": bits, "RS_dimension": dimension, "constrained_positions": m,
            "flat_codimension": codimension, "binary_rows": m*codimension,
            "binary_message_variables": dimension*bits,
            "nonzero_dual_symbol_inclusion_probability": str(p),
            "rank_failure_probability_upper": str(upper),
            "rank_failure_probability_power_two_upper_exponent": exponent,
            "raw_MDS_union_bound": str(raw),
            "requires_independent_uniform_GL_predicate_transforms": True,
            "arbitrary_right_hand_sides_allowed_on_full_row_rank_event": True,
            "seeded_trials_are_not_an_IID_probability_certificate": True,
            "local_derivation_status": "REVIEW_PENDING",
            "proves_classical_ease_for_every_OPI_family": False}


def smt_attack(problem, *, resource_limit=100000, timeout_ms=5000):
    integer(resource_limit, "SMT resource limit", 1, 10**9)
    integer(timeout_ms, "SMT time limit", 1, 60000)
    try:
        import z3
    except ImportError:
        return {"status": "UNKNOWN_SOLVER_UNAVAILABLE", "hardness_evidence": False}
    variables = [z3.Bool(f"x{i}") for i in range(problem.message_bits)]
    solver = z3.Solver()
    solver.set(rlimit=resource_limit, timeout=timeout_ms, random_seed=0)

    @lru_cache(maxsize=None)
    def linear(mask):
        return reduce(z3.Xor, (variables[i] for i in range(problem.message_bits) if (mask >> i) & 1), z3.BoolVal(False))

    for forms, offset in zip(problem.forms, problem.offsets):
        terms = [linear(forms[0]), z3.BoolVal(bool(offset))]
        terms += [z3.And(linear(forms[j]), linear(forms[j+1])) for j in range(1, problem.bits, 2)]
        solver.add(z3.Not(reduce(z3.Xor, terms)))
    status = solver.check()
    report = {"method": "Z3_direct_explicit_quadratic_SAT", "z3_version": z3.get_version_string(),
              "resource_limit": resource_limit, "timeout_ms": timeout_ms,
              "status": str(status).upper(), "message_hex": None, "score_count": None,
              "hardness_evidence": False, "universal_polynomial_solver_claimed": False}
    if status == z3.sat:
        model = solver.model()
        word = sum(int(z3.is_true(model.eval(v, model_completion=True))) << i for i, v in enumerate(variables))
        score = problem.score_count(word)
        if score != problem.length:
            raise ArithmeticError("SMT witness failed independent finite-field scoring")
        report.update(message_hex=hex(word), score_count=score)
    elif status == z3.unknown:
        report["reason_unknown"] = solver.reason_unknown()
    return report


def filter_bound(problem, degree=None, precision_bits=80):
    """Known balanced-DQI score for one rational filter, not an executed circuit."""
    ell = (problem.dimension-1)//2 if degree is None else degree
    integer(ell, "filter degree", 0, problem.length)
    integer(precision_bits, "score enclosure bits", 16, 256)
    distance = problem.dimension+1
    if not 2*ell+1 < distance:
        raise ValueError("observable score law needs strict 2*ell+1 < dual distance")
    matrix = np.zeros((ell+1, ell+1))
    for j in range(ell):
        matrix[j, j+1] = matrix[j+1, j] = sqrt((j+1)*(problem.length-j))
    _, vectors = np.linalg.eigh(matrix)
    weights = tuple(Fraction(abs(float(v))).limit_denominator(1 << 24) for v in vectors[:, -1])
    norm = sum(w*w for w in weights)
    lower = upper = Fraction(1, 2)
    scale = 1 << precision_bits
    for j in range(ell):
        B = (j+1)*(problem.length-j)
        floor = isqrt(B*scale*scale)
        ceiling = floor+int(floor*floor != B*scale*scale)
        multiplier = weights[j]*weights[j+1]/(problem.length*norm)
        lower += multiplier*Fraction(floor, scale)
        upper += multiplier*Fraction(ceiling, scale)
    return {"degree": ell, "dual_minimum_distance": distance,
            "strict_score_no_alias_condition": True, "rational_filter_weights": list(map(str, weights)),
            "expected_score_lower": str(lower), "expected_score_upper": str(upper),
            "expected_score_lower_decimal": float(lower), "expected_score_upper_decimal": float(upper),
            "bound_is_for_this_filter_not_a_certified_global_eigenvalue": True,
            "known_balanced_DQI_score_law": "https://arxiv.org/html/2610.02145v2#A1",
            "coherent_RS_decoder_and_filter_circuit_executed": False,
            "oracle_classical_lower_bound_transferred_to_explicit_predicates": False}


def exact_small_filter_law(problem):
    if problem.message_bits > 12:
        raise OPIReferenceLimit("UNKNOWN: complete finite-message calibration cap")
    bound = filter_bound(problem)
    weights = np.array(list(map(float, map(Fraction, bound["rational_filter_weights"]))))
    weights /= np.linalg.norm(weights)
    hist = [0]*(problem.length+1)
    for word in range(1 << problem.message_bits):
        hist[problem.score_count(word)] += 1
    probability = []
    for accepted, count in enumerate(hist):
        amplitude = 0.
        for j, weight in enumerate(weights):
            krawtchouk = sum((-1)**a*comb(problem.length-accepted, a)*comb(accepted, j-a)
                             for a in range(j+1) if a <= problem.length-accepted and j-a <= accepted)
            amplitude += weight*krawtchouk/sqrt(comb(problem.length, j))
        probability.append(count*amplitude**2/(1 << problem.message_bits))
    return {"message_score_histogram": hist, "ideal_filter_score_probabilities": probability,
            "normalization": sum(probability),
            "mean_score": sum(i*p for i, p in enumerate(probability))/problem.length,
            "enumerated_messages_charged": 1 << problem.message_bits,
            "enumeration_is_quantum_implementation": False}


def run_controls():
    rows = []
    for bits, dimension in ((3, 3), (5, 9), (5, 19), (7, 39)):
        for seed in (29, 71):
            problem = instance(bits, dimension, seed)
            flat = affine_flat_attack(problem, seed+10000)
            restarts = restarted_flat_attack(problem, seed+20000)
            best_trial = restarts["trials"][restarts["best_trial_index"]]
            repaired = repair_flat_attack(problem, int(restarts["message_hex"], 16),
                                          tuple(best_trial["forced_positions"]), seed+30000)
            smt = smt_attack(problem)
            if smt["status"] == "UNSAT" and restarts["score_count"] == problem.length:
                raise ArithmeticError("SMT unsatisfiability contradicts a verified native witness")
            rows.append({"public_seed": seed, "specification": problem.specification(),
                         "affine_flat_attack": flat,
                         "fixed_zero_flat_attack": fixed_flat_attack(problem),
                         "restarted_affine_flat_attack": restarts,
                         "repaired_affine_flat_attack": repaired,
                         "SMT_all_constraints_attack": smt,
                         "known_quantum_filter_bound": filter_bound(problem),
                         "all_generated_instances_retained": True,
                         "complete_small_filter_law": exact_small_filter_law(problem) if problem.message_bits <= 12 else None})
    control = instance(7, 90, 29)
    helpers = ("bpqm_gibbs_frontier.py", "parity_block_usd_prange.py")
    return {"schema_version": "1.0", "subsystem": "explicit_quadratic_opi", "instances": rows,
            "independent_GL_rank_bounds": [flat_rank_failure_bound(3, 2, 3), flat_rank_failure_bound(5, 19), flat_rank_failure_bound(7, 90)],
            "predeclared_high_rate_control": {"public_seed": 29, "specification": control.specification(),
                                              "fixed_zero_flat_attack": fixed_flat_attack(control),
                                              "seed_is_not_an_IID_probability_certificate": True},
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "dependency_sha256": {name: hashlib.sha256((ROOT/"theorems"/name).read_bytes()).hexdigest() for name in helpers},
            "python_flint_version": flint.__version__, "numpy_version": np.__version__,
            "accepted_speedup_candidate": False, "classical_hardness_proved": False,
            "new_quantum_algorithm_claimed": False, "predicate_family_novelty_verified": False,
            "retracted_max_QUADSAT_state_preparation_used": False,
            "oracle_problem_generated": False, "known_DQI_only_theoretical_reference": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(json.dumps([{"field_bits": row["specification"]["field_bits"],
                       "dimension": row["specification"]["RS_dimension"], "seed": row["public_seed"],
                       "flat_score": row["affine_flat_attack"]["score_count"],
                       "paid_restart_score": row["restarted_affine_flat_attack"]["score_count"],
                       "repaired_score": row["repaired_affine_flat_attack"]["score_count"],
                       "length": row["specification"]["positions"],
                       "SMT": row["SMT_all_constraints_attack"]["status"],
                       "quantum_reference": row["known_quantum_filter_bound"]["expected_score_lower_decimal"]}
                      for row in report["instances"]], indent=2))


if __name__ == "__main__":
    main()
