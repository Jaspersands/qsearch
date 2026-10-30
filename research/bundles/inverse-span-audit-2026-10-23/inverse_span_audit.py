"""A finite algebraic falsifier, NOT a native solver or hardness experiment."""

from collections import Counter
from functools import reduce
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from operator import xor
from pathlib import Path
import sys


FIELD_SOURCE = (Path(__file__).resolve().parents[1]
                / "inverse-trace-residual-2026-10-23" / "residual_sat.py")
SPEC = importlib.util.spec_from_file_location("inverse_span_field_dependency", FIELD_SOURCE)
FIELD_MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = FIELD_MODULE
SPEC.loader.exec_module(FIELD_MODULE)
BinaryField = FIELD_MODULE.BinaryField


def independent_indices(values):
    pivots, indices = {}, []
    for index, value in enumerate(values):
        while value:
            pivot = value.bit_length()-1
            if pivot not in pivots:
                pivots[pivot] = value
                indices.append(index)
                break
            value ^= pivots[pivot]
    return tuple(indices)


def span(basis):
    if len(independent_indices(basis)) != len(basis):
        raise ValueError("independent binary basis required")
    points = [0]
    for direction in basis:
        points += [x ^ direction for x in points]
    return tuple(points)


def subspaces(bits, dimension):
    """Complete RREF enumeration, explicitly restricted to tiny proof controls."""
    if type(bits) is not int or not 1 <= dimension <= bits <= 8:
        raise ValueError("finite exhaustive control only: 1 <= dimension <= bits <= 8")
    for pivots in combinations(range(bits), dimension):
        slots = [(i, j) for i, p in enumerate(pivots)
                 for j in range(p+1, bits) if j not in pivots]
        for mask in range(1 << len(slots)):
            basis = [1 << p for p in pivots]
            for k, (i, j) in enumerate(slots):
                basis[i] |= ((mask >> k) & 1) << j
            yield tuple(basis)


def evaluate_linearized(field, coefficients, point):
    value, power = 0, point
    for coefficient in coefficients:
        value ^= field.multiply(coefficient, power)
        power = field.multiply(power, power)
    return value


def subspace_polynomial(field, basis):
    coefficients = [1]  # L_{0}(X)=X, in linearized-exponent order.
    for direction in basis:
        value = evaluate_linearized(field, coefficients, direction)
        if value == 0:
            raise ValueError("dependent direction")
        new = [0]*(len(coefficients)+1)
        for j, coefficient in enumerate(coefficients):
            new[j] ^= field.multiply(value, coefficient)
            new[j+1] ^= field.multiply(coefficient, coefficient)
        coefficients = new
    return tuple(coefficients)


def boolean_degree(values):
    coefficients = list(values)
    if not coefficients or len(coefficients) & (len(coefficients)-1):
        raise ValueError("binary-cube ordered values required")
    for bit in range((len(coefficients)-1).bit_length()):
        for index in range(len(coefficients)):
            if index & (1 << bit):
                coefficients[index] ^= coefficients[index ^ (1 << bit)]
    return max((i.bit_count() for i, c in enumerate(coefficients) if c), default=-1)


def certificate(bits=7, modulus=131, basis=(1, 18, 36, 8)):
    field = BinaryField(bits, modulus)
    for x in basis:
        field.element(x)
    points = span(basis)
    inverses = tuple(field.inverse(x) for x in points)
    inverse_sum = reduce(xor, inverses, 0)
    pivot_indices = independent_indices(inverses)
    polynomial = subspace_polynomial(field, basis)
    ratio = field.multiply(polynomial[1], field.inverse(polynomial[0]))
    if ratio != inverse_sum or any(evaluate_linearized(field, polynomial, x) for x in points):
        raise ArithmeticError("subspace-polynomial identity failed")
    trace_values = tuple(field.trace(x) for x in inverses)
    scalar_zero_flat_count = 0
    for scalar in range(1, field.order):
        scalar_zero_flat_count += all(field.trace(field.multiply(scalar, y)) == 0 for y in inverses)
    predicted = (1 << (bits-len(pivot_indices)))-1
    if scalar_zero_flat_count != predicted:
        raise ArithmeticError("trace-pairing annihilator dimension disagrees")
    return {
        "bits": bits, "modulus": modulus, "basis": basis, "points": points,
        "inverse_values": inverses, "inverse_sum": inverse_sum,
        "linearized_polynomial_coefficients": polynomial,
        "inverse_sum_from_b1_div_b0": ratio,
        "inverse_span_rank": len(pivot_indices),
        "independent_inverse_points": [points[i] for i in pivot_indices],
        "independent_inverse_values": [inverses[i] for i in pivot_indices],
        "inverse_trace_values": trace_values,
        "vectorial_inverse_degree_on_subspace": boolean_degree(inverses),
        "scalar_inverse_trace_degree_on_subspace": boolean_degree(trace_values),
        "nonzero_scalars_making_all_traces_zero": scalar_zero_flat_count,
        "scalar_count_from_annihilator_dimension": predicted,
        "enumerated_scalars_charged": field.order-1,
        "scope": "finite_exact_counterexample_not_native_input_or_asymptotic_bound",
    }


def census(bits=7, dimension=4, modulus=131):
    field = BinaryField(bits, modulus)
    inverse_table = [field.inverse(x) for x in range(field.order)]
    counts, total = Counter(), 0
    for basis in subspaces(bits, dimension):
        points = span(basis)
        inverses = [inverse_table[x] for x in points]
        zero_sum = reduce(xor, inverses, 0) == 0
        rank = len(independent_indices(inverses))
        counts[(zero_sum, rank)] += 1
        total += 1
    return {
        "bits": bits, "dimension": dimension, "modulus": modulus,
        "subspaces_enumerated": total,
        "zero_sum_by_inverse_span_rank": {str(r): count for (z, r), count in sorted(counts.items()) if z},
        "nonzero_sum_by_inverse_span_rank": {str(r): count for (z, r), count in sorted(counts.items()) if not z},
        "field_elements_tabulated_charged": len(inverse_table),
        "asymptotic_inference": False,
    }


def report():
    root = Path(__file__).resolve().parent
    paths = [root/name for name in ("inverse_span_audit.py", "test_inverse_span_audit.py", "DECISION.md")]
    paths.append(FIELD_SOURCE)
    result = {
        "status": "ZERO_SUM_DOES_NOT_IMPLY_ACCEPTED_FLAT_EVEN_AFTER_RESCALING",
        "certificate": certificate(),
        "censuses": [census(dimension=3), census(dimension=4)],
        "native_inverse_trace_search_solved": False,
        "normality_upper_bound_proved": False,
        "quantum_speedup_claim_allowed": False,
        "sha256": {str(p): sha256(p.read_bytes()).hexdigest() for p in paths},
    }
    (root/"inverse_span_receipt.json").write_text(json.dumps(result, indent=2)+"\n")
    return result


if __name__ == "__main__":
    print(json.dumps(report(), indent=2))
