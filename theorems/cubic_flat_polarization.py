"""Exact third-polar contraction for classical cubic zero-flat extension.

Local controls only at n=64: no complete n=64 dual-RS solution is implied.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
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

from theorems.cubic_rs_affine_flats import (
    Cubic, REPORT as FLAT_REPORT, flat_points, from_specification, integer,
    monomials, rank_bound, restricted_system, solve_binary, verify_witness,
)
from theorems.parity_block_usd_prange import affine_system

REPORT = ROOT / "research/classical_baselines/cubic_flat_polarization.json"


def polar_mask(polynomial, u, v):
    """Mask t with parity(t&w)=D_u D_v D_w f(0), in the Boolean quotient."""
    bits = polynomial.bits
    integer(u, 0, (1 << bits)-1, "polar direction")
    integer(v, 0, (1 << bits)-1, "polar direction")
    cubic = polynomial.masks[2]
    result = 0
    for i in range(bits):
        ui, vi = (u >> i) & 1, (v >> i) & 1
        for j in range(i+1, bits):
            row = cubic[i][j]
            uj, vj = (u >> j) & 1, (v >> j) & 1
            du, dv = (row & u).bit_count() & 1, (row & v).bit_count() & 1
            result ^= (uj*dv ^ vj*du) << i
            result ^= (ui*dv ^ vi*du) << j
            if ui*vj ^ vi*uj:
                result ^= row
    return result


def null_basis(rows, bits):
    system = affine_system(tuple((row, 0) for row in rows), bits)
    basis = []
    for free in system["free"]:
        word = 1 << free
        for row, pivot in zip(system["rref"], system["pivots"]):
            word |= row[free] << pivot
        basis.append(word)
    return tuple(basis), system["rank"]


def sample_span(basis, rng):
    coefficients, word = rng.getrandbits(len(basis)), 0
    for i, vector in enumerate(basis):
        if (coefficients >> i) & 1:
            word ^= vector
    return word


def local_density_bound(bits, old_dimension, kernel_dimension=None):
    """Minimum-weight Boolean polynomial bound, conditional on a zero flat."""
    integer(bits, 1, 4096, "block width")
    integer(old_dimension, 0, bits-1, "old flat dimension")
    minimum = max(0, bits-comb(old_dimension, 2))
    dimension = minimum if kernel_dimension is None else kernel_dimension
    integer(dimension, minimum, bits, "polar kernel dimension")
    degree = 2*old_dimension+3
    return max(Fraction(0), Fraction(2)**(-degree)-Fraction(2)**(old_dimension-dimension))


def finite_success_bound(bits, blocks, checks, dimension, attempts):
    """Ensemble bound including constant-one inputs, caps, and global rank."""
    integer(dimension, 1, bits, "target flat dimension")
    integer(attempts, 1, 1_000_000, "stage attempt cap")
    rank = rank_bound(bits, blocks, checks, dimension)
    densities = [Fraction(1, 8)] + [
        local_density_bound(bits, k) for k in range(dimension)]
    # (1-p)^T <= exp(-Tp) <= 2^(-floor(10Tp/7)); ln(2)<7/10.
    exponents = [(10*attempts*d.numerator)//(7*d.denominator) for d in densities]
    coefficient_bits = len(monomials(bits))
    failure = (blocks*Fraction(2)**(-coefficient_bits)
               + blocks*sum(Fraction(2)**(-e) for e in exponents)
               + Fraction(2)**rank["rank_failure_upper_power_two_exponent"])
    lower = max(Fraction(0), 1-failure)
    rounded = Fraction((lower.numerator*1000)//lower.denominator, 1000)
    return {
        "stage_density_lowers": [str(d) for d in densities],
        "stage_failure_upper_negative_power_two_exponents": exponents,
        "constant_one_input_probability_per_block": f"2^-{coefficient_bits}",
        "rank_bound": rank,
        "certified_success_lower_rounded_down": str(rounded),
        "rounding": "down to multiples of 1/1000 using exact rational arithmetic",
        "requires_uniform_independent_random_cubics_and_ideal_random_draws": True,
        "probability_assertion_for_the_recorded_PRNG_seed": False,
        "asymptotic_polynomial_time_claim": False,
        "proof_review_pending": True,
    }


def find_polar_flat(polynomial, dimension, attempts, rng):
    integer(dimension, 0, polynomial.bits, "flat dimension")
    integer(attempts, 1, 1_000_000, "attempt cap")
    work = {"point_evaluations": 0, "random_draws": 0,
            "dependent_direction_rejections": 0, "polar_contractions": 0,
            "linear_systems": 0, "stages": []}
    origin = None
    for trial in range(1, attempts+1):
        word = rng.getrandbits(polynomial.bits)
        work["point_evaluations"] += 1
        work["random_draws"] += 1
        if polynomial.evaluate(word) == 0:
            origin = word
            break
    work["origin_attempts"] = trial
    if origin is None:
        return {"status": "UNKNOWN_FLAT_BUDGET", "origin": None,
                "directions": [], "work": work}
    directions, span, rows = [], {0}, []
    for k in range(dimension):
        if k:
            rows.extend(polar_mask(polynomial, u, directions[-1])
                        for u in directions[:-1])
            work["polar_contractions"] += k-1
        basis, rank = null_basis(rows, polynomial.bits)
        work["linear_systems"] += 1
        stage = {"old_dimension": k, "polar_rank": rank,
                 "kernel_dimension": len(basis), "draws": 0}
        work["stages"].append(stage)
        # The old zero-flat span lies in this kernel. Equality blocks THIS flat.
        if len(basis) <= k:
            return {"status": "THIS_FLAT_HAS_NO_POLAR_EXTENSION", "origin": origin,
                    "directions": directions, "work": work}
        chosen = None
        for trial in range(1, attempts+1):
            vector = sample_span(basis, rng)
            stage["draws"] = trial
            work["random_draws"] += 1
            if vector in span:
                work["dependent_direction_rejections"] += 1
                continue
            accepted = True
            for direction in (0, *directions):
                work["point_evaluations"] += 1
                if polynomial.evaluate(origin ^ vector ^ direction):
                    accepted = False
                    break
            if accepted:
                chosen = vector
                break
        if chosen is None:
            return {"status": "UNKNOWN_FLAT_BUDGET", "origin": origin,
                    "directions": directions, "work": work}
        directions.append(chosen)
        span |= {vector ^ chosen for vector in span}
    return {"status": "ACCEPTED_FLAT", "origin": origin,
            "directions": directions, "work": work}


def native_case(previous):
    """Same full cubic input, new local algorithm, independently checked output."""
    started = time.perf_counter()
    spec = previous["specification"]
    polynomials = from_specification(spec)
    dimension, seed = previous["flat_dimension"], previous["attack_seed"]
    rng = random.Random(seed)
    flats = [find_polar_flat(p, dimension, 4096, rng) for p in polynomials]
    failures = [i for i, flat in enumerate(flats) if flat["status"] != "ACCEPTED_FLAT"]
    result = {
        "bits": spec["bits"], "blocks": spec["blocks"], "checks": spec["checks"],
        "flat_dimension": dimension, "attack_seed": seed, "attempt_cap_per_stage": 4096,
        "original_input_sha256": hashlib.sha256(json.dumps(spec, sort_keys=True).encode()).hexdigest(),
        "status": "UNKNOWN_FLAT_BUDGET", "flat_failures": failures, "flats": flats,
        "native_witness_hex": None, "input_resampled": False,
        "total_search_point_evaluations": sum(f["work"]["point_evaluations"] for f in flats),
        "total_polar_contractions": sum(f["work"]["polar_contractions"] for f in flats),
        "total_local_linear_systems": sum(f["work"]["linear_systems"] for f in flats),
        "total_random_draws": sum(f["work"]["random_draws"] for f in flats),
        "rank_bound": rank_bound(spec["bits"], spec["blocks"], spec["checks"], dimension),
        "finite_success_bound": finite_success_bound(
            spec["bits"], spec["blocks"], spec["checks"], dimension, 4096),
    }
    if not failures:
        equations, width = restricted_system(spec["bits"], spec["checks"], spec["points"], flats)
        solution = solve_binary(equations, width)
        word = solution.pop("solution")
        result["restricted_linear_solve"] = solution
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
            verification = verify_witness(polynomials, spec["points"], spec["checks"], witness, modulus)
            if not verification["valid"]:
                raise AssertionError("polar attack gave an invalid native witness")
            result["status"] = "NATIVE_CLASSICAL_WITNESS"
            result["verification"] = verification
            result["native_witness_hex"] = [hex(x) for x in witness]
    result["elapsed_seconds_diagnostic"] = time.perf_counter()-started
    return result


def larger_local_control():
    """Predeclared 16 cubic blocks, NOT a complete n=64, m=4096 instance."""
    started = time.perf_counter()
    bits, dimension, blocks, seed = 64, 8, 16, 64001
    input_rng, search_rng = random.Random(seed), random.Random(seed+1_000_000)
    rows = []
    for _ in range(blocks):
        polynomial = Cubic(bits, input_rng.getrandbits(len(monomials(bits))))
        flat = find_polar_flat(polynomial, dimension, 4096, search_rng)
        verified = None
        if flat["status"] == "ACCEPTED_FLAT":
            points = flat_points(flat["origin"], flat["directions"])
            verified = len(set(points)) == 1 << dimension and all(polynomial.direct(x) == 0 for x in points)
            if not verified:
                raise AssertionError("polar identity failed exhaustive local replay")
        rows.append({"polynomial_coefficients_hex": hex(polynomial.coefficients),
                     "flat": flat, "all_flat_points_independently_verified": verified})
    return {
        "bits": bits, "dimension": dimension, "blocks_tested": blocks,
        "input_seed": seed, "attack_seed": seed+1_000_000,
        "attempt_cap_per_stage": 4096, "rows": rows,
        "flat_failures": sum(row["flat"]["status"] != "ACCEPTED_FLAT" for row in rows),
        "total_search_point_evaluations": sum(row["flat"]["work"]["point_evaluations"] for row in rows),
        "total_polar_contractions": sum(row["flat"]["work"]["polar_contractions"] for row in rows),
        "all_n_squared_blocks_tested": False,
        "global_RS_constraints_solved": False,
        "end_to_end_n64_solver_demonstrated": False,
        "input_resampled": False,
        "elapsed_seconds_diagnostic": time.perf_counter()-started,
    }


def run_audit():
    original = json.loads(FLAT_REPORT.read_text())
    cases = [native_case(case) for case in original["cases"]]
    print(json.dumps({"native_statuses": [case["status"] for case in cases]}), flush=True)
    local = larger_local_control()
    return {
        "schema": "cubic-polar-flat-extension-v1",
        "status": "EXACT_IDENTITY_AND_FINITE_WITNESSES_REVIEW_PENDING",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "dependency_sha256": {
            name: hashlib.sha256((ROOT/"theorems"/name).read_bytes()).hexdigest()
            for name in ("cubic_rs_affine_flats.py", "explicit_quadratic_opi.py",
                         "parity_block_usd_prange.py", "bpqm_gibbs_frontier.py")},
        "input_report_sha256": hashlib.sha256(FLAT_REPORT.read_bytes()).hexdigest(),
        "native_cases": cases, "larger_local_control": local,
        "classical_hardness_conjecture_refuted": False,
        "asymptotic_polynomial_success_proved": False,
        "novelty_established": False, "quantum_algorithm_executed": False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    report = run_audit()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"report": str(args.output),
                      "local_n64_failures": report["larger_local_control"]["flat_failures"]}))
