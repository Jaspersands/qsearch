"""Classical accepted-flat attack on explicit random cubic/dual-RS systems.

Finite witnesses, not an asymptotic dequantization. See the accompanying note
for the conditional MDS rank bound and the failure of fixed-flat extrapolation.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from functools import cached_property, lru_cache
import hashlib
from itertools import combinations
import json
from math import comb
from pathlib import Path
import random
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import flint

from theorems.explicit_quadratic_opi import element, encoded, field

REPORT = ROOT / "research/classical_baselines/cubic_rs_affine_flats.json"
SOURCE = "https://arxiv.org/html/2509.07276v1"


def integer(value, low, high, name):
    if type(value) is not int or not low <= value <= high:
        raise ValueError(f"{name} must be an integer in [{low}, {high}]")


@lru_cache(maxsize=16)
def monomials(bits):
    integer(bits, 1, 64, "Boolean block width")
    return tuple(sum(1 << j for j in indices)
                 for degree in range(4)
                 for indices in combinations(range(bits), degree))


@dataclass(frozen=True)
class Cubic:
    bits: int
    coefficients: int

    def __post_init__(self):
        size = len(monomials(self.bits))
        integer(self.coefficients, 0, (1 << size)-1, "packed ANF")

    @cached_property
    def terms(self):
        return tuple(mask for j, mask in enumerate(monomials(self.bits))
                     if (self.coefficients >> j) & 1)

    @cached_property
    def masks(self):
        linear, quadratic = 0, [0]*self.bits
        cubic = [[0]*self.bits for _ in range(self.bits)]
        for term in self.terms:
            indices = [j for j in range(self.bits) if (term >> j) & 1]
            if len(indices) == 1:
                linear ^= term
            elif len(indices) == 2:
                quadratic[indices[0]] ^= 1 << indices[1]
            elif len(indices) == 3:
                cubic[indices[0]][indices[1]] ^= 1 << indices[2]
        return linear, tuple(quadratic), tuple(tuple(row) for row in cubic)

    def evaluate(self, word):
        integer(word, 0, (1 << self.bits)-1, "Boolean word")
        linear, quadratic, cubic = self.masks
        parity = (self.coefficients & 1) ^ ((linear & word).bit_count() & 1)
        remaining = word
        while remaining:
            bit = remaining & -remaining
            i = bit.bit_length()-1
            remaining ^= bit
            parity ^= (quadratic[i] & word).bit_count() & 1
            tail = remaining
            while tail:
                bit = tail & -tail
                j = bit.bit_length()-1
                tail ^= bit
                parity ^= (cubic[i][j] & word).bit_count() & 1
        return parity

    def direct(self, word):
        """Independent, unoptimized ANF evaluation for witness verification."""
        integer(word, 0, (1 << self.bits)-1, "Boolean word")
        return sum((word & term) == term for term in self.terms) & 1


def flat_points(origin, directions):
    points = [origin]
    for vector in directions:
        points += [point ^ vector for point in points]
    return tuple(points)


def find_flat(polynomial, dimension, attempts, rng):
    """Capped, affine-equivariant search; never alter or resample the input."""
    integer(dimension, 0, polynomial.bits, "flat dimension")
    integer(attempts, 1, 1_000_000, "attempts per stage")
    counts = {"point_evaluations": 0, "random_words": 0,
              "dependent_direction_rejections": 0, "stage_attempts": []}
    origin = None
    for trial in range(1, attempts+1):
        word = rng.getrandbits(polynomial.bits)
        counts["random_words"] += 1
        counts["point_evaluations"] += 1
        if polynomial.evaluate(word) == 0:
            origin = word
            break
    counts["stage_attempts"].append(trial)
    if origin is None:
        return {"status": "UNKNOWN_FLAT_BUDGET", "origin": None,
                "directions": [], "work": counts}
    points, span, directions = [origin], {0}, []
    for _ in range(dimension):
        chosen = None
        for trial in range(1, attempts+1):
            vector = rng.getrandbits(polynomial.bits)
            counts["random_words"] += 1
            if vector in span:
                counts["dependent_direction_rejections"] += 1
                continue
            accepted = True
            for point in points:
                counts["point_evaluations"] += 1
                if polynomial.evaluate(point ^ vector):
                    accepted = False
                    break
            if accepted:
                chosen = vector
                break
        counts["stage_attempts"].append(trial)
        if chosen is None:
            return {"status": "UNKNOWN_FLAT_BUDGET", "origin": origin,
                    "directions": directions, "work": counts}
        directions.append(chosen)
        points += [point ^ chosen for point in points]
        span |= {vector ^ chosen for vector in span}
    return {"status": "ACCEPTED_FLAT", "origin": origin,
            "directions": directions, "work": counts}


def solve_binary(equations, width):
    """Bit-packed echelon elimination; free bits zero, not uniform sampling."""
    integer(width, 1, 1_000_000, "binary width")
    rows, inconsistent, xor_steps = {}, False, 0
    for mask, rhs in equations:
        integer(mask, 0, (1 << width)-1, "binary row")
        integer(rhs, 0, 1, "binary RHS")
        while mask:
            pivot = (mask & -mask).bit_length()-1
            if pivot not in rows:
                rows[pivot] = (mask, rhs)
                break
            old, value = rows[pivot]
            mask ^= old
            rhs ^= value
            xor_steps += 1
        if not mask and rhs:
            inconsistent = True
    solution = 0
    if not inconsistent:
        for pivot, (mask, rhs) in sorted(rows.items(), reverse=True):
            solution |= (rhs ^ ((mask & solution).bit_count() & 1)) << pivot
    return {"rank": len(rows), "consistent": not inconsistent,
            "solution": None if inconsistent else solution,
            "row_xors": xor_steps, "free_bits": width-len(rows)}


def restricted_system(bits, checks, points, flats):
    """Compose H[j,i]=points[i]**j with each accepted affine block."""
    integer(checks, 1, len(points), "field parity checks")
    if len(points) != len(flats) or len(set(points)) != len(points):
        raise ValueError("distinct points and one flat per point required")
    for point in points:
        integer(point, 0, (1 << bits)-1, "field point")
    rows, rhs, column = [0]*(bits*checks), [0]*(bits*checks), 0
    for point, flat in zip(points, flats):
        a, power = element(bits, point), field(bits).one()
        origin = element(bits, flat["origin"])
        directions = tuple(element(bits, word) for word in flat["directions"])
        for j in range(checks):
            offset = encoded(power*origin)
            images = tuple(encoded(power*vector) for vector in directions)
            for b in range(bits):
                rhs[j*bits+b] ^= (offset >> b) & 1
                for local, image in enumerate(images):
                    rows[j*bits+b] ^= ((image >> b) & 1) << (column+local)
            power *= a
        column += len(directions)
    return tuple(zip(rows, rhs)), column


def multiply_binary(left, right, modulus, bits):
    """Verifier-only polynomial-basis multiplication, independent of FLINT."""
    result = 0
    while right:
        if right & 1:
            result ^= left
        right >>= 1
        left <<= 1
        if left >> bits:
            left ^= modulus
    return result


def verify_witness(polynomials, points, checks, witness, modulus):
    if len(polynomials) != len(points) or len(witness) != len(points):
        raise ValueError("complete native witness required")
    bits = polynomials[0].bits
    for word in witness:
        integer(word, 0, (1 << bits)-1, "witness symbol")
    failed = [i for i, (p, word) in enumerate(zip(polynomials, witness))
              if p.direct(word)]
    syndromes = [0]*checks
    for point, word in zip(points, witness):
        power = 1
        for j in range(checks):
            syndromes[j] ^= multiply_binary(power, word, modulus, bits)
            power = multiply_binary(power, point, modulus, bits)
    return {"valid": not failed and not any(syndromes),
            "failed_polynomial_indices": failed,
            "field_syndromes_hex": [hex(word) for word in syndromes],
            "independent_ANF_and_field_replay": True}


def affine_flat_count(bits, dimension):
    integer(bits, 1, 4096, "ambient dimension")
    integer(dimension, 0, bits, "flat dimension")
    gaussian = 1
    for j in range(dimension):
        gaussian = gaussian*((1 << (bits-j))-1)//((1 << (j+1))-1)
    return (1 << (bits-dimension))*gaussian


def flat_absence_bound(bits, dimension):
    integer(bits, 1, 4096, "ambient dimension")
    integer(dimension, 0, bits, "flat dimension")
    constraints = sum(comb(dimension, j) for j in range(min(3, dimension)+1))
    exponent = 2+(dimension+1)*(bits-dimension)-constraints
    return {"bits": bits, "dimension": dimension,
            "restriction_ANF_coefficients": constraints,
            "probability_any_accepted_flat_upper_power_two_exponent": min(0, exponent),
            "unclipped_first_moment_power_two_exponent": exponent,
            "distribution": "uniform degree-at-most-three Boolean ANF",
            "rules_out_all_classical_algorithms": False}


def rank_bound(bits, blocks, checks, dimension):
    integer(bits, 1, 4096, "field bits")
    integer(blocks, 1, 1 << bits, "RS length")
    integer(checks, 1, blocks, "field check rows")
    integer(dimension, 0, bits, "local dimension")
    slack = blocks*dimension-bits*checks
    return {"binary_rows": bits*checks, "flat_parameters": blocks*dimension,
            "slack": slack,
            "rank_failure_upper_power_two_exponent": min(0, -slack),
            "conditional_on_all_local_searches_succeeding": True,
            "requires_independent_uniform_local_direction_spaces": True,
            "affine_equivariance_uses_ideal_independent_randomness": True,
            "seeded_runs_are_probability_certificates": False}


def instance_spec(bits, checks, seed):
    integer(bits, 5, 64, "native block width")
    blocks = bits*bits
    integer(checks, 1, blocks-1, "field parity checks")
    integer(seed, 0, 2**64-1, "public input seed")
    rng = random.Random(seed)
    polynomials = tuple(Cubic(bits, rng.getrandbits(len(monomials(bits))))
                        for _ in range(blocks))
    specification = {
        "bits": bits, "blocks": blocks, "checks": checks,
        "input_seed": seed, "points": list(range(1, blocks+1)),
        "field_modulus_coefficients": list(map(int, field(bits).modulus().coeffs())),
        "ANF_order": "degree 0..3, itertools.combinations(range(bits), degree)",
        "polynomial_coefficients_hex": [hex(p.coefficients) for p in polynomials],
        "input_resampled": False, "planted_witness": False,
    }
    return specification, polynomials


def from_specification(specification):
    bits = specification["bits"]
    if list(map(int, field(bits).modulus().coeffs())) != specification["field_modulus_coefficients"]:
        raise ValueError("field basis changed")
    polynomials = tuple(Cubic(bits, int(word, 16))
                        for word in specification["polynomial_coefficients_hex"])
    if len(polynomials) != specification["blocks"] or len(polynomials) != bits*bits:
        raise ValueError("native m=n^2 input required")
    return polynomials


def run_case(bits, checks, dimension, seed, attempts=4096):
    started = time.perf_counter()
    spec, polynomials = instance_spec(bits, checks, seed)
    rng = random.Random(seed+1_000_000)
    flats = [find_flat(p, dimension, attempts, rng) for p in polynomials]
    failures = [i for i, flat in enumerate(flats) if flat["status"] != "ACCEPTED_FLAT"]
    result = {
        "specification": spec, "flat_dimension": dimension,
        "attack_seed": seed+1_000_000, "attempt_cap_per_stage": attempts,
        "attempted_input_instances": 1, "local_flat_searches": len(flats),
        "flat_failures": failures, "flats": flats,
        "rank_bound": rank_bound(bits, len(flats), checks, dimension),
        "status": "UNKNOWN_FLAT_BUDGET" if failures else "PENDING_LINEAR_SOLVE",
        "total_search_point_evaluations": sum(f["work"]["point_evaluations"] for f in flats),
        "total_random_words": sum(f["work"]["random_words"] for f in flats),
        "native_witness_hex": None, "original_system_unsatisfiable_claimed": False,
        "polynomial_time_asymptotic_solver_claimed": False,
    }
    if not failures:
        equations, width = restricted_system(bits, checks, spec["points"], flats)
        solution = solve_binary(equations, width)
        word = solution.pop("solution")
        result["restricted_linear_solve"] = solution
        result["restricted_linear_solve"]["full_row_rank"] = solution["rank"] == bits*checks
        result["restricted_linear_solve"]["solution_hex"] = None if word is None else hex(word)
        result["status"] = "THIS_PRODUCT_FLAT_INCONSISTENT"
        if word is not None:
            witness, column = [], 0
            for flat in flats:
                symbol = flat["origin"]
                for direction in flat["directions"]:
                    if (word >> column) & 1:
                        symbol ^= direction
                    column += 1
                witness.append(symbol)
            modulus = sum(c << j for j, c in enumerate(spec["field_modulus_coefficients"]))
            verification = verify_witness(polynomials, spec["points"], checks, witness, modulus)
            if not verification["valid"]:
                raise AssertionError("restricted solver produced an invalid native witness")
            result["status"] = "NATIVE_CLASSICAL_WITNESS"
            result["native_witness_hex"] = [hex(value) for value in witness]
            result["verification"] = verification
        # Restrict the same product flat: failure is not input unsatisfiability.
        smaller = [dict(flat, directions=flat["directions"][:-1]) for flat in flats]
        equations, width = restricted_system(bits, checks, spec["points"], smaller)
        if width:
            control = solve_binary(equations, width)
            control.pop("solution")
            result["one_dimension_smaller_control"] = control
    result["elapsed_seconds_diagnostic"] = time.perf_counter()-started
    return result


def run_audit():
    cases = []
    # Fixed before execution: same code rate 113/128, no selection on success.
    for parameters in ((16, 30, 3, 16001), (32, 120, 4, 32001)):
        case = run_case(*parameters)
        cases.append(case)
        print(json.dumps({"bits": parameters[0], "status": case["status"],
                          "flat_failures": len(case["flat_failures"]),
                          "seconds": case["elapsed_seconds_diagnostic"]}), flush=True)
    dependencies = ("explicit_quadratic_opi.py", "bpqm_gibbs_frontier.py",
                    "parity_block_usd_prange.py")
    return {
        "schema": "cubic-rs-accepted-flats-v1",
        "status": "FINITE_CLASSICAL_COUNTERCHECK_REVIEW_PENDING",
        "source_url": SOURCE, "source_sections": ["3", "5.1", "A.3", "B"],
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "dependency_sha256": {name: hashlib.sha256((ROOT/"theorems"/name).read_bytes()).hexdigest()
                              for name in dependencies},
        "python_version": sys.version, "flint_version": flint.__version__,
        "cases": cases,
        "asymptotic_flat_absence_controls": [flat_absence_bound(n, n//8)
                                            for n in (32, 256, 352, 512)],
        "native_rate_flat_absence_controls": [
            flat_absence_bound(n, (15*n+127)//128) for n in (32, 256, 400, 512)],
        "novelty_established": False, "quantum_algorithm_executed": False,
        "classical_hardness_conjecture_refuted": False,
        "general_MQ_or_cryptosystem_attack_claimed": False,
        "central_speedup_candidate_admitted": False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    report = run_audit()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"report": str(args.output),
                      "statuses": [case["status"] for case in report["cases"]]}))
