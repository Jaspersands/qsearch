"""Scoped mobility bound and exact output-law controls for independent menus.

No general classical lower bound. The finite reference grants exact restricted
fiber enumeration; it is not a scalable sampler for the native relation.
"""
from __future__ import annotations

from fractions import Fraction as Q
import hashlib
from itertools import combinations, product
from math import comb
from pathlib import Path

from theorems.balanced_codeword_filter import integer, reciprocal_trace
from theorems.inverse_trace_gibbs_target import (
    _ceil_log2, _parameters, _syndrome_columns, residual_variance_bound,
)

ROOT = Path(__file__).resolve().parents[1]


def mobility_bound(bits, length, checks, menu_size):
    """Uniform every-native-start bound for independent uniform anchored menus.

    The supplied parameters describe a Vandermonde code with distinct points;
    this analytic budget does not certify a particular matrix or source.
    """
    _parameters(bits, length, checks)
    integer(menu_size, 1, 1 << (bits-1), "menu size")
    if menu_size == 1:
        return Q(0)
    alternatives = menu_size-1
    count = menu_size**length-sum(comb(length, w)*alternatives**w
                                 for w in range(checks+1))
    return min(Q(1), Q(count, ((1 << (bits-1))-1)**checks))


def support_tv_lower(move_upper, steps, initial_mass_upper):
    """Full-law TV lower bound, including ABORT, for the stated menu policy."""
    integer(steps, 0, 10**18, "step cap")
    if any(not isinstance(x, Q) or not 0 <= x <= 1
           for x in (move_upper, initial_mass_upper)):
        raise ValueError("exact rational probability bounds in [0,1] required")
    return max(Q(0), 1-steps*move_upper-initial_mass_upper)


def certificate(bits, menu_size):
    length, checks = bits*bits, bits*bits//8
    bound = mobility_bound(bits, length, checks, menu_size)
    return {"bits": bits, "length": length, "checks": checks,
            "menu_size": menu_size, "mobility_power2_upper": _ceil_log2(bound),
            "mobility_exactly_zero": bound == 0,
            "nonvacuous": bound < 1,
            "uniform_every_native_start": True,
            "independent_uniform_anchored_menus_required": True,
            "restricted_fiber_solver_granted_for_bound": True,
            "native_large_chain_executed": False,
            "general_classical_hardness": False}


def finite_reference(bits, points, checks, targets, menu_size, syndrome=None):
    """Capped exact native kernels, unanchored bias and size-bias repair."""
    integer(bits, 2, 4, "finite reference field bits")
    points, targets = tuple(points), tuple(targets)
    length = len(points)
    _parameters(bits, length, checks)
    q, alphabet_size = 1 << bits, 1 << (bits-1)
    integer(menu_size, 1, alphabet_size, "menu size")
    if len(set(points)) != length:
        raise ValueError("distinct public evaluation points required")
    for value in points:
        integer(value, 0, q-1, "evaluation point")
    if len(targets) != length:
        raise ValueError("one target bit per coordinate required")
    for value in targets:
        integer(value, 0, 1, "target bit")
    syndrome = (0,)*checks if syndrome is None else tuple(syndrome)
    if len(syndrome) != checks:
        raise ValueError("syndrome length mismatch")
    for value in syndrome:
        integer(value, 0, q-1, "syndrome entry")
    menu_count = comb(alphabet_size, menu_size)**length
    fiber_cap = min(menu_size**length, alphabet_size**(length-checks))
    if (alphabet_size**length > 4096 or menu_count > 65536
            or menu_count*fiber_cap**2 > 10_000_000):
        raise ValueError("exponential reference cap exceeded")
    alphabets = [tuple(x for x in range(q) if reciprocal_trace(bits, x) == b) for b in targets]
    columns = _syndrome_columns(bits, points, checks)
    packed = sum(value << (bits*j) for j, value in enumerate(syndrome))

    def valid(word):
        residual = packed
        for i, value in enumerate(word):
            residual ^= columns[i][value]
        return residual == 0

    words = tuple(word for word in product(*alphabets) if valid(word))
    if not words:
        return {"status": "EMPTY_NATIVE_FIBER", "native_words": 0,
                "conditional_tv": None, "reference_is_scalable_sampler": False}
    if len(words) > 256:
        raise ValueError("exponential transition matrix cap exceeded")
    incidence = comb(alphabet_size-1, menu_size-1)**length
    matrix = [[Q(0) for _ in words] for _ in words]
    naive, repaired, mds_repaired = ([Q(0) for _ in words] for _ in range(3))
    abort = Q(0)
    for menus in product(*(tuple(combinations(a, menu_size)) for a in alphabets)):
        fiber = [j for j, word in enumerate(words)
                 if all(value in menu for value, menu in zip(word, menus))]
        if not fiber:
            abort += Q(1, menu_count)
            continue
        if len(fiber) > menu_size**(length-checks):
            raise ArithmeticError("MDS information-set fiber cap failed")
        for j in fiber:
            naive[j] += Q(1, menu_count*len(fiber))
            repaired[j] += Q(1, menu_count*menu_size**length)
            mds_repaired[j] += Q(1, menu_count*menu_size**(length-checks))
            for i in fiber:
                matrix[i][j] += Q(1, incidence*len(fiber))
    if any(sum(row) != 1 for row in matrix):
        raise ArithmeticError("anchored kernel lost mass")
    if any(matrix[i][j] != matrix[j][i] for i in range(len(words)) for j in range(len(words))):
        raise ArithmeticError("anchored kernel failed symmetry")
    if sum(naive)+abort != 1 or any(p != Q(1, alphabet_size**length) for p in repaired):
        raise ArithmeticError("unanchored output law failed")
    if any(p != Q(menu_size**checks, alphabet_size**length) for p in mds_repaired):
        raise ArithmeticError("MDS-corrected output law failed")
    success = sum(naive)
    return {"status": "EXACT_FINITE_NATIVE_MENU_CONTROL", "bits": bits,
            "points": points, "checks": checks, "targets": targets, "syndrome": syndrome,
            "menu_size": menu_size, "native_words": len(words),
            "menus_enumerated": menu_count, "anchored_matrix": matrix,
            "detailed_balance_exact": True, "abort_probability": abort,
            "conditional_tv": sum(abs(p/success-Q(1, len(words))) for p in naive)/2,
            "repaired_success": sum(repaired), "repair_exactly_uniform": True,
            "mds_repaired_success": sum(mds_repaired),
            "mds_repair_exactly_uniform": True,
            "reference_is_scalable_sampler": False}


def report():
    controls = []
    for size in (1, 2, 3, 4):
        row = finite_reference(3, (0, 1, 2, 3), 1, (1, 1, 1, 1), size)
        matrix = row.pop("anchored_matrix")
        row["self_loop_min"] = min(matrix[i][i] for i in range(len(matrix)))
        row["self_loop_max"] = max(matrix[i][i] for i in range(len(matrix)))
        controls.append(row)
    files = (Path(__file__), ROOT / "research/INVERSE_TRACE_MENU_REFRESH.md",
             ROOT / "tests/test_inverse_trace_menu_refresh.py",
             ROOT / "theorems/inverse_trace_gibbs_target.py",
             ROOT / "research/INVERSE_TRACE_COMPLETION_TRANSFER.md")
    residuals = []
    for bits in (17, 31, 61):
        length, checks = bits*bits, bits*bits//8
        surplus = (3*checks+2*bits-1)//(2*bits)
        residual = checks+surplus
        residuals.append({"bits": bits, "checks": checks,
                          "previous_free_field_variables": (4*checks+bits-1)//bits,
                          "free_field_variables": surplus, "residual_length": residual,
                          "residual_variance_power2_upper": _ceil_log2(
                              residual_variance_bound(bits, residual, checks)),
                          "prefix_variance_power2_upper": _ceil_log2(
                              residual_variance_bound(bits, length-residual, checks)),
                          "average_uniform_syndrome_scope": True,
                          "residual_sampler_implemented": False})
    return {"status": "SCOPED_INDEPENDENT_MENU_SAMPLER_FALSIFIER",
            "general_classical_hardness": False, "speedup_established": False,
            "new_efficient_native_sampler": False,
            "accepted_systematic_root_sampler_already_uniform": True,
            "certificates": [certificate(n, size) for n in (17, 31, 61, 127)
                             for size in (2, n, n*n)],
            "finite_controls": controls,
            "conditional_residual_forecasts": residuals,
            "source_hashes": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                              for p in files}}


def json_value(value):
    if isinstance(value, Q):
        return {"numerator": value.numerator, "denominator": value.denominator}
    raise TypeError(type(value).__name__)
