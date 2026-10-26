"""Polynomial local zero-flat construction and a scoped classical easy region.

Cohen--Tal degree reduction plus quadratic isotropy, not a new primitive.
The global theorem is average-case and does not cover fixed redundancy rate.
Supports arbitrary Boolean block widths up to 256 bits for local degree-reduction
controls while preserving exact replay of the n=16, 32 native dual-RS cases and
the predeclared 16-block n=64 local control.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from functools import cached_property, lru_cache
import hashlib
from itertools import combinations
import json
from math import comb, isqrt
from pathlib import Path
import random
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.cubic_flat_polarization import null_basis, polar_mask, sample_span
from theorems.cubic_rs_affine_flats import (
    REPORT as INPUT_REPORT, from_specification, integer,
    rank_bound, restricted_system, solve_binary, verify_witness,
)

REPORT = ROOT / "research/classical_baselines/cubic_degree_reduction.json"
MAX_LOCAL_BITS = 256


@lru_cache(maxsize=32)
def monomials(bits):
    integer(bits, 1, MAX_LOCAL_BITS, "Boolean block width")
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
        if not self.coefficients:
            return ()
        bits_lsb = bin(self.coefficients)[:1:-1]
        return tuple(mask for bit, mask in zip(bits_lsb, monomials(self.bits))
                     if bit == "1")

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


def dimensions(bits):
    integer(bits, 3, 4096, "Boolean width")
    lowered = (1+isqrt(8*bits-7))//2
    return lowered, (lowered-1)//2


def remainder(word, echelon):
    while word:
        pivot = (word & -word).bit_length()-1
        if pivot not in echelon:
            break
        word ^= echelon[pivot]
    return word


def combine(basis, coefficients):
    word = 0
    for j, vector in enumerate(basis):
        if (coefficients >> j) & 1:
            word ^= vector
    return word


def bilinear(rows, u, v):
    return (combine(rows, u) & v).bit_count() & 1


def quadratic_value(linear, rows, word):
    value = (linear & word).bit_count() & 1
    for i, row in enumerate(rows):
        if (word >> i) & 1:
            value ^= (row & word & ~((1 << (i+1))-1)).bit_count() & 1
    return value


def quadratic_zero_space(linear, rows):
    """Alternating Gram--Schmidt, then kernel of q on an isotropic space."""
    width = len(rows)
    if any((row >> i) & 1 for i, row in enumerate(rows)):
        raise ValueError("alternating polar matrix required")
    if any(((rows[i] >> j) ^ (rows[j] >> i)) & 1
           for i in range(width) for j in range(width)):
        raise ValueError("symmetric polar matrix required")
    remaining, isotropic, pairs = [1 << i for i in range(width)], [], 0
    while remaining:
        pair = next(((i, j) for i in range(len(remaining))
                     for j in range(i+1, len(remaining))
                     if bilinear(rows, remaining[i], remaining[j])), None)
        if pair is None:
            isotropic.extend(remaining)
            break
        i, j = pair
        u, v = remaining[i], remaining[j]
        isotropic.append(u)
        rest = [w for index, w in enumerate(remaining) if index not in (i, j)]
        remaining = [w ^ (u if bilinear(rows, w, v) else 0)
                     ^ (v if bilinear(rows, w, u) else 0) for w in rest]
        pairs += 1
    values = [quadratic_value(linear, rows, u) for u in isotropic]
    if any(values):
        pivot = values.index(1)
        zero = [u ^ (isotropic[pivot] if value else 0)
                for j, (u, value) in enumerate(zip(isotropic, values)) if j != pivot]
    else:
        zero = isotropic
    if len(zero) < (width-1)//2:
        raise AssertionError("quadratic zero-space dimension guarantee failed")
    return tuple(zero), {"polar_rank": 2*pairs, "bilinear_isotropic_dimension": len(isotropic),
                         "zero_space_dimension": len(zero)}


def zero_flat(polynomial, rng):
    """Bounded polynomial work; no field table or 2**flat_dimension list."""
    bits = polynomial.bits
    target, zero_dimension = dimensions(bits)
    work = {"origin_evaluations": 0, "kernel_draws": 0, "polar_contractions": 0,
            "linear_systems": 0, "quadratic_restriction_evaluations": 0,
            "certificate_evaluations": 0, "span_points_enumerated": 0}
    result = {"status": "PENDING", "origin": None, "directions": [],
              "target_lowered_dimension": target, "target_zero_dimension": zero_dimension,
              "origin_cap": 64*bits, "direction_draw_cap_per_stage": 2*bits,
              "work": work, "stages": []}
    if polynomial.coefficients == 1:
        result["status"] = "CONSTANT_ONE_INPUT"
        return result
    origin = None
    for _ in range(64*bits):
        word = rng.getrandbits(bits)
        work["origin_evaluations"] += 1
        if not polynomial.evaluate(word):
            origin = word
            break
    if origin is None:
        result["status"] = "UNKNOWN_ORIGIN_BUDGET"
        return result
    result["origin"] = origin
    directions, polar_rows, echelon = [], [], {}
    for k in range(target):
        if k:
            polar_rows.extend(polar_mask(polynomial, u, directions[-1]) for u in directions[:-1])
            work["polar_contractions"] += k-1
        kernel, rank = null_basis(polar_rows, bits)
        work["linear_systems"] += 1
        if len(kernel) <= k:
            raise AssertionError("guaranteed cubic degree-reduction kernel exhausted")
        chosen = None
        for draws in range(1, 2*bits+1):
            word = sample_span(kernel, rng)
            work["kernel_draws"] += 1
            reduced = remainder(word, echelon)
            if reduced:
                chosen = word
                echelon[(reduced & -reduced).bit_length()-1] = reduced
                break
        result["stages"].append({"old_dimension": k, "polar_rank": rank,
                                 "kernel_dimension": len(kernel), "draws": draws})
        if chosen is None:
            result["status"] = "UNKNOWN_DIRECTION_BUDGET"
            return result
        directions.append(chosen)
    # Cubic coefficients vanish. Read the remaining quadratic in this basis.
    values = [polynomial.evaluate(origin ^ u) for u in directions]
    rows = [0]*target
    work["quadratic_restriction_evaluations"] += target
    for i, j in combinations(range(target), 2):
        value = polynomial.evaluate(origin ^ directions[i] ^ directions[j]) ^ values[i] ^ values[j]
        rows[i] |= value << j
        rows[j] |= value << i
        work["quadratic_restriction_evaluations"] += 1
    linear = sum(value << i for i, value in enumerate(values))
    zero, reduction = quadratic_zero_space(linear, tuple(rows))
    kept = tuple(combine(directions, word) for word in zero[:zero_dimension])
    result.update(status="ACCEPTED_FLAT", directions=list(kept),
                  degree_reduction_basis=directions, quadratic_reduction=reduction)
    certificate = certify_zero_flat(polynomial, origin, kept)
    work["certificate_evaluations"] = certificate["evaluations"]
    if not certificate["valid"]:
        raise AssertionError("native polynomial zero-flat certificate failed")
    result["certificate"] = certificate
    return result


def certify_zero_flat(polynomial, origin, directions):
    """Low-weight input tests determine every coefficient of a cubic restriction."""
    echelon = {}
    for word in directions:
        word = remainder(word, echelon)
        if not word:
            return {"valid": False, "evaluations": 0, "reason": "DEPENDENT_DIRECTIONS"}
        echelon[(word & -word).bit_length()-1] = word
    evaluations = 0
    for weight in range(min(3, len(directions))+1):
        for subset in combinations(range(len(directions)), weight):
            point = origin
            for i in subset:
                point ^= directions[i]
            evaluations += 1
            if polynomial.direct(point):
                return {"valid": False, "evaluations": evaluations, "reason": "NONZERO_RESTRICTION"}
    return {"valid": True, "evaluations": evaluations,
            "reason": "ALL_DEGREE_AT_MOST_THREE_COEFFICIENTS_ZERO"}


def success_bound(bits, blocks, checks):
    lowered, zero_dimension = dimensions(bits)
    rank = rank_bound(bits, blocks, checks, zero_dimension)
    coefficients = sum(comb(bits, j) for j in range(4))
    # Bound four positive terms separately; never materialize 2**S(n).
    term_exponents = [(blocks-1).bit_length()-coefficients,
                      (blocks-1).bit_length()-8*bits,
                      (blocks*lowered-1).bit_length()-2*bits,
                      rank["rank_failure_upper_power_two_exponent"]]
    exponent = min(0, 2+max(term_exponents))
    return {
        "bits": bits, "blocks": blocks, "field_checks": checks,
        "lowered_dimension": lowered, "zero_flat_dimension": zero_dimension,
        "failure_upper_power_two_exponent": exponent,
        "four_term_upper_exponents": term_exponents,
        "union_bound_rounding": "sum of four terms <= four times largest dyadic ceiling",
        "rank_bound": rank,
        "ideal_IID_uniform_cubic_ensemble_required": True,
        "fixed_PRNG_seed_probability_claim": False,
        "fixed_positive_check_rate_dequantized": False,
        "proof_review_pending": True,
    }


def sample_deterministic_cubic(bits, input_seed, block_index):
    """Deterministic cubic ANF generator for any width in [1, MAX_LOCAL_BITS]."""
    integer(bits, 1, MAX_LOCAL_BITS, "Boolean block width")
    integer(block_index, 0, 1_000_000, "block index")
    rng = random.Random(input_seed)
    size = len(monomials(bits))
    coefficients = None
    for _ in range(block_index + 1):
        coefficients = rng.getrandbits(size)
    return Cubic(bits, coefficients)


def local_block_campaign(bits, blocks_tested, input_seed, search_seed):
    """Execute and certify local degree-reduction zero-flats across `blocks_tested` blocks."""
    integer(bits, 3, MAX_LOCAL_BITS, "Boolean block width")
    integer(blocks_tested, 1, 4096, "tested block count")
    started = time.perf_counter()
    input_rng = random.Random(input_seed)
    search_rng = random.Random(search_seed)
    size = len(monomials(bits))
    lowered, zero_dim = dimensions(bits)
    rows = []
    for block_index in range(blocks_tested):
        coeffs = input_rng.getrandbits(size)
        polynomial = Cubic(bits, coeffs)
        flat = zero_flat(polynomial, search_rng)
        coeffs_hex = hex(coeffs)
        rows.append({
            "block_index": block_index,
            "polynomial_coefficients_sha256": hashlib.sha256(coeffs_hex.encode()).hexdigest(),
            "active_monomial_count": len(polynomial.terms),
            "status": flat["status"],
            "origin": flat["origin"],
            "directions": flat["directions"],
            "degree_reduction_basis": flat["degree_reduction_basis"],
            "quadratic_reduction": flat["quadratic_reduction"],
            "certificate": flat["certificate"],
            "work": flat["work"],
        })
    failures = sum(row["status"] != "ACCEPTED_FLAT" for row in rows)
    return {
        "bits": bits,
        "anf_monomial_capacity": size,
        "target_lowered_dimension": lowered,
        "target_zero_dimension": zero_dim,
        "blocks_tested": blocks_tested,
        "full_code_blocks_m_equals_n_squared": bits * bits,
        "all_n_squared_blocks_tested": blocks_tested == bits * bits,
        "input_seed": input_seed,
        "search_seed": search_seed,
        "flat_failures": failures,
        "total_origin_evaluations": sum(row["work"]["origin_evaluations"] for row in rows),
        "total_kernel_draws": sum(row["work"]["kernel_draws"] for row in rows),
        "total_polar_contractions": sum(row["work"]["polar_contractions"] for row in rows),
        "total_linear_systems": sum(row["work"]["linear_systems"] for row in rows),
        "total_quadratic_restriction_evaluations": sum(
            row["work"]["quadratic_restriction_evaluations"] for row in rows
        ),
        "total_certificate_evaluations": sum(
            row["work"]["certificate_evaluations"] for row in rows
        ),
        "total_span_points_enumerated": sum(
            row["work"]["span_points_enumerated"] for row in rows
        ),
        "rows": rows,
        "global_RS_constraints_solved": False,
        "asymptotic_result_claimed": False,
        "elapsed_seconds_diagnostic": time.perf_counter() - started,
    }


def native_case(previous):
    started = time.perf_counter()
    spec = previous["specification"]
    bits = spec["bits"]
    _, k = dimensions(bits)
    checks = bits*(k-1)
    polynomials = from_specification(spec)
    rng = random.Random(spec["input_seed"]+2_000_000)
    flats = [zero_flat(p, rng) for p in polynomials]
    failures = [i for i, flat in enumerate(flats) if flat["status"] != "ACCEPTED_FLAT"]
    report = {
        "bits": bits, "blocks": len(flats), "checks": checks,
        "previous_checks": spec["checks"], "code_constraints_changed": True,
        "same_original_cubic_coefficients": True,
        "base_specification_sha256": hashlib.sha256(json.dumps(spec, sort_keys=True).encode()).hexdigest(),
        "search_seed": spec["input_seed"]+2_000_000, "input_resampled": False,
        "status": "LOCAL_FAILURE", "flat_failures": failures, "flats": flats,
        "success_bound": success_bound(bits, len(flats), checks),
        "native_witness_hex": None,
    }
    if not failures:
        equations, width = restricted_system(bits, checks, spec["points"], flats)
        solved = solve_binary(equations, width)
        word = solved.pop("solution")
        report["restricted_linear_solve"] = solved
        report["status"] = "THIS_PRODUCT_FLAT_INCONSISTENT"
        if word is not None:
            witness, column = [], 0
            for flat in flats:
                local = (word >> column) & ((1 << k)-1)
                witness.append(flat["origin"] ^ combine(flat["directions"], local))
                column += k
            modulus = sum(c << i for i, c in enumerate(spec["field_modulus_coefficients"]))
            verification = verify_witness(polynomials, spec["points"], checks, witness, modulus)
            if not verification["valid"]:
                raise AssertionError("native RS verification failed")
            report.update(status="NATIVE_CLASSICAL_WITNESS",
                          native_witness_hex=[hex(x) for x in witness], verification=verification)
    report["elapsed_seconds_diagnostic"] = time.perf_counter()-started
    return report


def run_audit():
    original = json.loads(INPUT_REPORT.read_text())
    native = [native_case(case) for case in original["cases"]]
    # Same n64 polynomial descriptions as the preceding local audit.
    local_path = ROOT/"research/classical_baselines/cubic_flat_polarization.json"
    local_input = json.loads(local_path.read_text())["larger_local_control"]
    if local_input["bits"] != 64 or local_input["blocks_tested"] != 16:
        raise ValueError("predeclared n64 local input inventory changed")
    rng = random.Random(2_064_001)
    local = [zero_flat(Cubic(64, int(row["polynomial_coefficients_hex"], 16)), rng)
             for row in local_input["rows"]]
    n64_expanded = local_block_campaign(64, 64, 64002, 2_064_002)
    beyond_64bit = [
        local_block_campaign(96, 4, 96001, 2_096_001),
        local_block_campaign(128, 2, 128001, 2_128_001),
    ]
    scaling = []
    for n in (16, 32, 64, 128, 256, 512, 1024):
        _, k = dimensions(n)
        scaling.append(success_bound(n, n*n, n*(k-1)))
    return {
        "schema": "cubic-degree-reduction-v2",
        "status": "POLYNOMIAL_EASY_REGION_DERIVATION_REVIEW_PENDING",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "dependency_sha256": {name: hashlib.sha256((ROOT/"theorems"/name).read_bytes()).hexdigest()
                              for name in ("cubic_flat_polarization.py", "cubic_rs_affine_flats.py",
                                           "explicit_quadratic_opi.py", "parity_block_usd_prange.py",
                                           "bpqm_gibbs_frontier.py")},
        "input_report_sha256": hashlib.sha256(INPUT_REPORT.read_bytes()).hexdigest(),
        "local_input_report_sha256": hashlib.sha256(local_path.read_bytes()).hexdigest(),
        "primary_prior_art": "https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.APPROX-RANDOM.2015.680",
        "native_cases": native,
        "n64_local_flats": local,
        "n64_expanded_local_campaign": n64_expanded,
        "beyond_64bit_local_controls": beyond_64bit,
        "n64_full_code_constrained_instance_solved": False,
        "analytical_scaling_not_empirical_runs": scaling,
        "reference_input_bits_cap": 64,
        "local_degree_reduction_bits_cap": MAX_LOCAL_BITS,
        "new_quantum_algorithm_claimed": False,
        "novelty_established": False,
        "paper_fixed_rate_classical_hardness_conjecture_refuted": False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    report = run_audit()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({
        "report": str(args.output),
        "native_statuses": [row["status"] for row in report["native_cases"]],
        "n64_local_failures": sum(row["status"] != "ACCEPTED_FLAT"
                                  for row in report["n64_local_flats"]),
        "n64_expanded_failures": report["n64_expanded_local_campaign"]["flat_failures"],
        "beyond_64bit_controls": [
            {"bits": c["bits"], "blocks_tested": c["blocks_tested"], "failures": c["flat_failures"]}
            for c in report["beyond_64bit_local_controls"]
        ],
    }))
