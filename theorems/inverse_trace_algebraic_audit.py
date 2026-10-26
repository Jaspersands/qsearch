"""Exact inverse-graph models and a block-local linearization countercertificate.

Known low-degree relations, not a new solver. See INVERSE_TRACE_ALGEBRAIC_AUDIT.md.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import hashlib
from itertools import combinations
import json
from pathlib import Path
from random import Random

from theorems.balanced_codeword_filter import integer, reciprocal_trace, trace_mask
from theorems.cubic_rs_affine_flats import solve_binary
from theorems.explicit_quadratic_opi import element, encoded, field


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/classical_baselines/inverse_trace_algebraic_audit.json"


def multiplier_certificate(bits):
    """Sparse FIELD-valued multiplier; the target-one zero must be excluded."""
    integer(bits, 3, 256, "field bits")
    modulus = (1 << bits)-1
    options = []
    for weight in range(2, bits):
        positions = tuple(j*bits//weight for j in range(weight))
        exponent = sum(1 << j for j in positions)
        products = tuple((exponent-(1 << j)) % modulus for j in range(bits))
        if not all(products):
            raise ArithmeticError("zero exponent requires a separate zero-extension term")
        degree = max(weight, max(e.bit_count() for e in products))
        options.append((degree, weight, exponent, products, positions))
    degree, weight, exponent, products, positions = min(options)
    gaps = [positions[j+1]-positions[j] for j in range(len(positions)-1)]
    gaps.append(bits+positions[0]-positions[-1])
    return {"bits": bits, "multiplier_exponent": exponent,
            "multiplier_degree": weight, "product_exponents": products,
            "product_degree": max(e.bit_count() for e in products),
            "equation_degree": degree, "maximum_cyclic_gap": max(gaps),
            "zero_is_spurious_for_target_one": True,
            "single_boolean_multiplier_is_equivalent": False,
            "coupled_system_solver_implemented": False}


def multiplier_value(bits, word, target):
    integer(word, 0, (1 << bits)-1, "field element")
    integer(target, 0, 1, "target bit")
    certificate = multiplier_certificate(bits)
    x = element(bits, word)
    value = sum((x**e for e in certificate["product_exponents"]), field(bits).zero())
    return encoded(value+target*x**certificate["multiplier_exponent"])


def inverse_graph_residuals(bits, left, right):
    integer(bits, 2, 128, "field bits")
    for word in (left, right):
        integer(word, 0, (1 << bits)-1, "field element")
    x, y = element(bits, left), element(bits, right)
    return tuple(encoded(value) for value in
                 (x*x*y+x, x*y*y+y, x**4*y+x**3, x*y**4+y**3, (x*y)**2+x*y))


@lru_cache(maxsize=16)
def monomial_masks(bits):
    integer(bits, 2, 128, "field bits")
    variables = tuple(1 << j for j in range(2*bits))
    return (0,)+variables+tuple(a | b for a, b in combinations(variables, 2))


def quadratic_lift(bits, left, right):
    word = left | (right << bits)
    return sum(1 << j for j, mask in enumerate(monomial_masks(bits)) if word & mask == mask)


@lru_cache(maxsize=16)
def compiled_relations(bits):
    """Five field identities, expanded as sparse Boolean quadratic polynomials.

    Each polynomial maps square-free bit-variable monomials to encoded field
    coefficients. This is O(poly(bits)) arithmetic, with no field truth table.
    """
    integer(bits, 2, 128, "field bits")

    def frobenius(offset, power):
        return {1 << (offset+j): encoded(element(bits, 1 << j)**(1 << power)) for j in range(bits)}

    def multiply(left, right):
        result = {}
        for a, c in left.items():
            for b, d in right.items():
                mask = a | b
                result[mask] = result.get(mask, 0) ^ encoded(element(bits, c)*element(bits, d))
        return result

    def add(left, right):
        result = dict(left)
        for mask, value in right.items():
            result[mask] = result.get(mask, 0) ^ value
        return {mask: value for mask, value in result.items() if value}

    x, x2, x4 = [frobenius(0, j) for j in range(3)]
    y, y2, y4 = [frobenius(bits, j) for j in range(3)]
    return (add(multiply(x2, y), x), add(multiply(x, y2), y),
            add(multiply(x4, y), multiply(x2, x)),
            add(multiply(x, y4), multiply(y2, y)),
            add(multiply(x2, y2), multiply(x, y)))


def compiled_residuals(bits, left, right):
    word = left | (right << bits)
    result = []
    for polynomial in compiled_relations(bits):
        value = 0
        for mask, coefficient in polynomial.items():
            if word & mask == mask:
                value ^= coefficient
        result.append(value)
    return tuple(result)


def linearized_rows(bits):
    index = {mask: j for j, mask in enumerate(monomial_masks(bits))}
    return tuple(sum(((coefficient >> bit) & 1) << index[mask] for mask, coefficient in polynomial.items())
                 for polynomial in compiled_relations(bits) for bit in range(bits))


def affine_lift_countercontrol(bits, seed=1022, samples=None, rng=None):
    """An odd sum of TRUE graph lifts with a FALSE projected inverse pair.

    The sampled points supply a short certificate, not the all-n proof.
    Failed span acquisition is UNKNOWN. No fresh input is selected on success.
    """
    integer(bits, 3, 128, "field bits")
    samples = 4*(2*bits+1) if samples is None else samples
    integer(samples, 1, 100_000, "graph sample cap")
    rng = Random(seed) if rng is None else rng
    graph = []
    for _ in range(samples):
        x = rng.getrandbits(bits)
        integer(x, 0, (1 << bits)-1, "sampled field element")
        y = encoded(element(bits, x)**-1) if x else 0
        graph.append((x, y))
    columns = [1 | (x << 1) | (y << (bits+1)) for x, y in graph]
    trace = trace_mask(bits, 1)
    target_y = trace & -trace
    target = 1 | (target_y << (bits+1))
    equations = [(sum(((column >> j) & 1) << k for k, column in enumerate(columns)), (target >> j) & 1)
                 for j in range(2*bits+1)]
    system = solve_binary(equations, samples)
    result = {"bits": bits, "seed": seed, "samples": samples,
              "status": "UNKNOWN_AFFINE_SPAN_BUDGET", "graph_affine_rank": system["rank"],
              "required_augmented_rank": 2*bits+1, "field_table_enumerated": False,
              "native_witness": False, "general_classical_attack_excluded": False,
              "scope": "BLOCK_LOCAL_INDEPENDENT_MONOMIAL_LINEARIZATION_ONLY"}
    if system["rank"] != 2*bits+1:
        return result
    weights = system["solution"]
    if weights is None:
        raise ArithmeticError("full-rank affine graph span failed to represent a target")
    selected = [point for j, point in enumerate(graph) if (weights >> j) & 1]
    augmented, lifted = 0, 0
    for x, y in selected:
        if any(inverse_graph_residuals(bits, x, y)):
            raise ArithmeticError("a supplied graph point is not native inversion")
        augmented ^= 1 | (x << 1) | (y << (bits+1))
        lifted ^= quadratic_lift(bits, x, y)
    rows = linearized_rows(bits)
    if augmented != target or len(selected) % 2 != 1:
        raise ArithmeticError("invalid affine graph combination")
    if any((row & lifted).bit_count() % 2 for row in rows):
        raise ArithmeticError("true local quadratic identity rejected the affine lift")
    if reciprocal_trace(bits, 0) == 1 or int(element(bits, target_y).trace()) != 1:
        raise ArithmeticError("countercontrol does not violate the native trace-inverse predicate")
    mismatch = lifted ^ quadratic_lift(bits, 0, target_y)
    if mismatch == 0:
        raise ArithmeticError("false inverse pair unexpectedly has a genuine quadratic lift")
    result.update(status="VERIFIED_SPURIOUS_LOCAL_LINEARIZATION_POINT",
                  field_modulus=sum(int(c) << j for j, c in enumerate(field(bits).modulus().coeffs())),
                  selected_graph_points=selected, selected_point_count=len(selected),
                  projected_pair=(0, target_y), quadratic_lift_hex=hex(lifted),
                  genuine_lift_disagreement_count=mismatch.bit_count(),
                  compiled_equation_count=len(rows),
                  compiled_equation_rank=solve_binary([(row, 0) for row in rows], len(monomial_masks(bits)))["rank"],
                  direct_graph_residuals=inverse_graph_residuals(bits, 0, target_y),
                  linearized_residuals=[(row & lifted).bit_count() % 2 for row in rows])
    return result


def native_model_budget(bits, length, checks):
    integer(bits, 3, 128, "field bits")
    integer(length, 2, 1 << bits, "native length")
    integer(checks, 1, length-1, "native parity checks")
    variables = 2*bits*length
    linear = bits*checks+length
    return {"bits": bits, "length": length, "checks": checks,
            "binary_variables_before_linear_elimination": variables,
            "independent_native_linear_constraints": linear,
            "remaining_binary_variables": variables-linear,
            "minimal_quadratic_equations_raw_count": 2*bits*length,
            "redundant_quadratic_equations_raw_count": 5*bits*length,
            "equations_claimed_independent_or_semiregular": False,
            "polynomial_time_solver_established": False}


def report():
    return {"status": "EXACT_ALGEBRAIC_MODEL_AND_LOCAL_RELAXATION_AUDIT_REVIEW_PENDING",
            "new_algorithm_or_hardness_proof": False, "speedup_established": False,
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "proof_sha256": hashlib.sha256((ROOT / "research/INVERSE_TRACE_ALGEBRAIC_AUDIT.md").read_bytes()).hexdigest(),
            "literature": ["https://cacr.uwaterloo.ca/techreports/2006/cacr2006-09.pdf",
                           "https://eprint.iacr.org/2013/585",
                           "https://cacr.uwaterloo.ca/techreports/2006/cacr2006-34.pdf"],
            "multipliers": [multiplier_certificate(n) for n in (17, 31, 61)],
            "native_models": [native_model_budget(n, n*n, n*n//8) for n in (17, 31, 61)],
            "false_local_relaxation_certificates": [affine_lift_countercontrol(n, seed=1000*n+22)
                                                    for n in (17, 31, 61)]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = report()
    if args.write:
        REPORT.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status": result["status"],
                      "multiplier_degrees": [r["equation_degree"] for r in result["multipliers"]],
                      "affine_ranks": [r["graph_affine_rank"] for r in result["false_local_relaxation_certificates"]],
                      "report": str(REPORT) if args.write else None}, indent=2))


if __name__ == "__main__":
    main()
