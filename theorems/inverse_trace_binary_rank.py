"""A polynomial-time sampling falsifier, not a new hardness candidate.

Rank deficiency detects extra binary zero-syndrome subwords. Passing this
observable never certifies uniformity or a quantum/classical separation.
"""
from fractions import Fraction
from math import isqrt

from theorems.balanced_codeword_filter import integer, ceil_log2_fraction
from theorems.cubic_rs_affine_flats import multiply_binary
from theorems.inverse_trace_smt import validate_instance, verify_word


def binary_subword_diagnostic(instance, word):
    bits, points, _, checks = validate_instance(instance)
    if not verify_word(instance, word):
        raise ValueError("a verified full original native word is required")
    modulus = sum(c << j for j, c in enumerate(instance["field_modulus_coefficients"]))
    columns = []
    for point, value in zip(points, word, strict=True):
        packed = 0
        for j in range(checks):
            packed |= value << (bits*j)
            value = multiply_binary(value, point, modulus, bits)
        columns.append(packed)
    pivots, dependencies, xors = {}, [], 0
    for i, column in enumerate(columns):
        mask = 1 << i
        while column:
            pivot = column.bit_length()-1
            if pivot not in pivots:
                pivots[pivot] = (column, mask)
                break
            row, certificate = pivots[pivot]
            column ^= row
            mask ^= certificate
            xors += 1
        if not column:
            dependencies.append(mask)
    all_mask = (1 << len(points))-1

    def syndrome(mask):
        result = 0
        for i, column in enumerate(columns):
            if (mask >> i) & 1:
                result ^= column
        return result

    if syndrome(all_mask) or any(syndrome(mask) for mask in dependencies):
        raise ArithmeticError("binary elimination failed original syndrome verification")
    rank, zeros = len(pivots), sum(value == 0 for value in word)
    return {"status": "VERIFIED_NATIVE_BINARY_SUBWORD_DIAGNOSTIC",
            "field_bits": bits, "binary_rows": bits*checks, "columns": len(points),
            "binary_rank": rank, "binary_nullity": len(points)-rank,
            "zero_coordinates": zeros, "nonzero_support_nullity": len(points)-zeros-rank,
            "rank_saturates_native_maximum": rank == len(points)-1,
            "additional_binary_dependence": rank < len(points)-1,
            "kernel_basis_hex": [hex(mask) for mask in dependencies],
            "column_xors": xors, "all_ones_relation_verified": True,
            "kernel_basis_verified": True, "subsets_enumerated": False,
            "uniformity_certified": False, "hardness_evidence": False}


def uniform_rank_failure_bound(bits, length, checks, zeros):
    """Conservative rational probability bound under the UNIFORM native law."""
    integer(bits, 2, 127, "field degree")
    integer(length, 2, min(1 << bits, 100_000), "length")
    integer(checks, 1, length-1, "original parity checks")
    integer(zeros, 0, length, "zero targets")
    q, half = 1 << bits, (length+1)//2
    result = {"status": "BOUND_INCONCLUSIVE", "uniform_native_law_required": True,
              "observed_rank_is_not_uniformity_certificate": True,
              "rank_failure_probability_upper": None}
    if half <= checks:
        return result
    root = isqrt(q)
    root += int(root*root < q)
    beta = min(Fraction(1), Fraction(2*root+1, q))
    eta = lambda m: (q**checks-1)*beta**(m-checks+1)
    native = eta(length)
    if native >= 1:
        return result
    zero_error = Fraction(2*zeros, q)*(1+eta(length-1))/(1-native)
    extra_error = 2**(length-1)*Fraction(2, q)**checks*(1+eta(half))/(1-native)
    bound = min(Fraction(1), zero_error+extra_error)
    result.update(status="CERTIFIED_UNIFORM_NATIVE_RANK_FAILURE_BOUND",
                  rank_failure_probability_upper=[bound.numerator, bound.denominator],
                  zero_coordinate_probability_upper=[zero_error.numerator, zero_error.denominator],
                  nonzero_decomposition_probability_power2_upper=ceil_log2_fraction(extra_error),
                  rank_failure_probability_power2_upper=ceil_log2_fraction(bound))
    return result
