"""Exact native affine inverse-trace SAT attack, with no complexity claim.

No field tables, hidden witness, planted syndrome, or quantum access. A
successful model is independently checked with integer field arithmetic.
"""

from dataclasses import dataclass
from functools import reduce
from operator import xor
from time import perf_counter

import z3


def remainder(a, b):
    while a and a.bit_length() >= b.bit_length():
        a ^= b << (a.bit_length() - b.bit_length())
    return a


def polynomial_gcd(a, b):
    while b:
        a, b = b, remainder(a, b)
    return a


@dataclass(frozen=True)
class BinaryField:
    bits: int
    modulus: int

    def __post_init__(self):
        if (type(self.bits) is not int or not 2 <= self.bits <= 128
                or type(self.modulus) is not int
                or self.modulus.bit_length() != self.bits+1):
            raise ValueError("invalid field presentation")
        value = 2
        for j in range(1, self.bits+1):
            value = self.multiply(value, value)
            if j <= self.bits//2 and polynomial_gcd(value ^ 2, self.modulus) != 1:
                raise ValueError("reducible field modulus")
        if value != 2:
            raise ValueError("reducible field modulus")

    @property
    def order(self):
        return 1 << self.bits

    def element(self, value):
        if type(value) is not int or not 0 <= value < self.order:
            raise ValueError("noncanonical field element")
        return value

    def multiply(self, a, b):
        out = 0
        while b:
            if b & 1:
                out ^= a
            b >>= 1
            a <<= 1
        return remainder(out, self.modulus)

    def inverse(self, a):
        if not a:
            return 0
        u, v, s, t = a, self.modulus, 1, 0
        while u != 1:
            shift = u.bit_length()-v.bit_length()
            if shift < 0:
                u, v, s, t = v, u, t, s
                shift = -shift
            u ^= v << shift
            s ^= t << shift
        return remainder(s, self.modulus)

    def trace(self, a):
        out = 0
        for _ in range(self.bits):
            out ^= a
            a = self.multiply(a, a)
        if out not in (0, 1):
            raise ArithmeticError("invalid absolute trace")
        return out


def syndrome(field, points, values, checks):
    if len(points) != len(values):
        raise ValueError("point/value length mismatch")
    out = [0]*checks
    for a, x in zip(points, values):
        term = x
        for j in range(checks):
            out[j] ^= term
            term = field.multiply(term, a)
    return tuple(out)


def verify(field, points, values, checks, target, rhs):
    if (len(values) != len(points) or len(target) != len(points) or len(rhs) != checks
            or any(type(b) is not int or b not in (0, 1) for b in target)
            or any(type(x) is not int or not 0 <= x < field.order for x in values)):
        return False
    return (syndrome(field, points, values, checks) == tuple(rhs)
            and all(field.trace(field.inverse(x)) == b for x, b in zip(values, target)))


def affine_chart(field, points, checks, rhs):
    """Invert the pivot Vandermonde using Lagrange coefficients, not a table."""
    if not 1 <= checks <= len(points) or len(rhs) != checks:
        raise ValueError("invalid residual check dimensions")
    if len(set(points)) != len(points):
        raise ValueError("distinct original evaluation points required")
    for value in tuple(points)+tuple(rhs):
        field.element(value)
    pivot_points, free_points = points[:checks], points[checks:]
    polynomial = [1]
    for a in pivot_points:
        new = [0]*(len(polynomial)+1)
        for j, c in enumerate(polynomial):
            new[j] ^= field.multiply(a, c)
            new[j+1] ^= c
        polynomial = new
    constants, coefficients = [], []
    for a in pivot_points:
        quotient = [0]*checks
        quotient[-1] = polynomial[-1]
        for j in range(checks-2, -1, -1):
            quotient[j] = polynomial[j+1] ^ field.multiply(a, quotient[j+1])
        denominator = 0
        for c in reversed(quotient):
            denominator = field.multiply(denominator, a) ^ c
        scale = field.inverse(denominator)
        lagrange = [field.multiply(c, scale) for c in quotient]
        constants.append(reduce(xor, (field.multiply(c, h) for c, h in zip(lagrange, rhs)), 0))
        row = []
        for b in free_points:
            value = 0
            for c in reversed(lagrange):
                value = field.multiply(value, b) ^ c
            row.append(value)
        coefficients.append(tuple(row))
    return tuple(constants), tuple(coefficients)


def symbolic_multiply(field, a, b):
    """Polynomial-basis carryless product reduced modulo the supplied modulus."""
    n = field.bits
    zero = z3.BitVecVal(0, n)
    residue = z3.BitVecVal(field.modulus ^ (1 << n), n)
    out, shifted = zero, a
    for j in range(n):
        out = out ^ z3.If(z3.Extract(j, j, b) == 1, shifted, zero)
        shifted = (shifted << 1) ^ z3.If(z3.Extract(n-1, n-1, shifted) == 1, residue, zero)
    return out


def symbolic_scale(field, coefficient, value):
    n = field.bits
    terms = [z3.If(z3.Extract(j, j, value) == 1,
                   z3.BitVecVal(field.multiply(coefficient, 1 << j), n),
                   z3.BitVecVal(0, n)) for j in range(n)]
    return reduce(xor, terms, z3.BitVecVal(0, n))


def inverse_trace_constraint(field, x, y, bit):
    trace_bits = [z3.Extract(j, j, y) for j in range(field.bits)
                  if field.trace(1 << j)]
    traced = reduce(xor, trace_bits, z3.BitVecVal(0, 1))
    inverse_graph = z3.Or(z3.And(x == 0, y == 0), symbolic_multiply(field, x, y) == 1)
    return z3.And(inverse_graph, traced == bit)


def symbolic_square(field, value):
    terms = [z3.If(z3.Extract(j, j, value) == 1,
                   z3.BitVecVal(field.multiply(1 << j, 1 << j), field.bits),
                   z3.BitVecVal(0, field.bits)) for j in range(field.bits)]
    return reduce(xor, terms, z3.BitVecVal(0, field.bits))


def conic_constraint(field, x, u, bit):
    trace_one = next(1 << j for j in range(field.bits) if field.trace(1 << j))
    expression = symbolic_square(field, u) ^ symbolic_multiply(field, x, u)
    if bit:
        expression ^= symbolic_scale(field, trace_one, symbolic_square(field, x))
    return z3.And(expression == 1, x != 0) if bit else expression == 1


def solve_residual(field, points, checks, target, rhs, *, seconds=30, resource_limit=5_000_000,
                   seed=23, encoding="inverse", algebraic=False):
    start = perf_counter()
    if len(points) != len(target) or any(type(b) is not int or b not in (0, 1) for b in target):
        raise ValueError("one original target bit per point required")
    if seconds <= 0 or resource_limit < 1:
        raise ValueError("positive wall and solver resource caps required")
    if encoding not in ("inverse", "conic"):
        raise ValueError("unknown algebraic encoding")
    constants, coefficients = affine_chart(field, points, checks, rhs)
    solver = z3.SolverFor("QF_BV")
    solver.set(rlimit=resource_limit, random_seed=seed)
    if algebraic:
        solver.set(anf=True)
        solver.set("anf.exlin", True)
    x = [z3.BitVec(f"x_{i}", field.bits) for i in range(len(points))]
    y = [z3.BitVec(f"inverse_{i}", field.bits) for i in range(len(points))]
    for i, (constant, row) in enumerate(zip(constants, coefficients)):
        value = reduce(xor, (symbolic_scale(field, c, v) for c, v in zip(row, x[checks:])),
                       z3.BitVecVal(constant, field.bits))
        solver.add(x[i] == value)
    constraint = inverse_trace_constraint if encoding == "inverse" else conic_constraint
    for value, auxiliary, bit in zip(x, y, target):
        solver.add(constraint(field, value, auxiliary, bit))
    build_seconds = perf_counter()-start
    report = {"status": "UNKNOWN", "z3_version": z3.get_version_string(), "encoding": encoding,
              "algebraic_simplification": algebraic,
              "build_seconds": build_seconds, "wall_budget_seconds": seconds,
              "solver_resource_limit": resource_limit, "solver_seed": seed,
              "free_field_variables": len(points)-checks,
              "free_boolean_coordinates_before_predicates": field.bits*(len(points)-checks),
              "field_addresses_enumerated": 0, "hidden_witness_supplied": False,
              "polynomial_time_proved": False, "uniform_sampling_claim": False}
    remaining = seconds-build_seconds
    if remaining <= 0:
        report.update(reason="build_clock_exhausted", elapsed_seconds=perf_counter()-start)
        return report
    solver.set(timeout=max(1, int(1000*remaining)))
    outcome = solver.check()
    report["statistics"] = {key: solver.statistics().get_key_value(key) for key in solver.statistics().keys()}
    if outcome == z3.sat:
        model = solver.model()
        witness = tuple(model.eval(v, model_completion=True).as_long() for v in x)
        if not verify(field, points, witness, checks, target, rhs):
            raise ArithmeticError("SAT model failed independent native verification")
        report.update(status="VERIFIED_RESIDUAL_WITNESS", witness=witness)
    elif outcome == z3.unsat:
        report.update(status="UNSAT_REPORTED_BY_Z3", independent_unsat_certificate=False)
    else:
        report["reason"] = solver.reason_unknown()
    report["elapsed_seconds"] = perf_counter()-start
    return report
