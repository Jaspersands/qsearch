"""Exact coupled inverse-trace SAT baseline; timeouts are not hardness evidence.

The optional random-prefix restriction preserves the original public instance.
Any model is checked with FLINT against every original parity and trace equation.
This is a search experiment, not a uniform sampler or a polynomial-time claim.
"""
from functools import reduce
import hashlib
import json
from math import isqrt
from random import Random
from time import perf_counter
from typing import Sequence

from theorems.balanced_codeword_filter import integer, reciprocal_trace, trace_mask
from theorems.explicit_quadratic_opi import element, encoded, field


def validate_instance(instance):
    bits = instance["bits"]
    integer(bits, 2, 128, "field bits")
    points, targets = tuple(instance["points"]), tuple(instance["targets"])
    integer(len(points), 2, min(1 << bits, 100_000), "length")
    integer(instance["checks"], 1, len(points)-1, "parity checks")
    if len(targets) != len(points) or len(set(points)) != len(points):
        raise ValueError("aligned targets and distinct original points required")
    for point in points:
        integer(point, 0, (1 << bits)-1, "field point")
    for target in targets:
        integer(target, 0, 1, "target bit")
    modulus = list(map(int, field(bits).modulus().coeffs()))
    if instance["field_modulus_coefficients"] != modulus:
        raise ValueError("recorded field modulus does not match this arithmetic backend")
    return bits, points, targets, instance["checks"]


def native_instance(bits=17, seed=1028, target_mode="ones"):
    integer(bits, 5, 128, "native field bits")
    integer(seed, 0, 2**32-1, "input seed")
    if any(bits % d == 0 for d in range(2, isqrt(bits)+1)):
        raise ValueError("this campaign targets prime extension degrees")
    if target_mode not in ("ones", "random"):
        raise ValueError("target_mode must be ones or random")
    length = bits*bits
    rng = Random(seed)
    # Sample public points, never a solution followed by its target pattern.
    points, seen = [], set()
    while len(points) < length:
        point = rng.getrandbits(bits)
        if point not in seen:
            points.append(point)
            seen.add(point)
    targets = [1]*length if target_mode == "ones" else [rng.getrandbits(1) for _ in points]
    return {"bits": bits, "points": points, "targets": targets,
            "checks": length//8,
            "field_modulus_coefficients": list(map(int, field(bits).modulus().coeffs()))}


def syndrome(bits, points, values, checks):
    result = [field(bits).zero() for _ in range(checks)]
    for point, value in zip(points, values, strict=True):
        alpha, power, x = element(bits, point), field(bits).one(), element(bits, value)
        for j in range(checks):
            result[j] += power*x
            power *= alpha
    return tuple(map(encoded, result))


def verify_word(instance, values):
    bits, points, targets, checks = validate_instance(instance)
    if len(values) != len(points):
        return False
    for value in values:
        integer(value, 0, (1 << bits)-1, "witness symbol")
    return (not any(syndrome(bits, points, values, checks))
            and all(reciprocal_trace(bits, x) == b for x, b in zip(values, targets)))


def restrict_instance(instance, seed, *, full=False):
    bits, points, targets, checks = validate_instance(instance)
    integer(seed, 0, 2**32-1, "prefix seed")
    size = len(points) if full else min(len(points), checks+(4*checks+bits-1)//bits)
    indices = tuple(range(size))  # Fixed before any prefix draw.
    rng, prefix = Random(seed), {}
    mask = trace_mask(bits, 1)
    pivot = mask & -mask
    for i in range(size, len(points)):
        y = rng.getrandbits(bits)
        if ((y & mask).bit_count() & 1) != targets[i]:
            y ^= pivot
        prefix[i] = encoded(element(bits, y)**-1) if y else 0
    target_syndrome = syndrome(bits, [points[i] for i in prefix], list(prefix.values()), checks)
    return indices, prefix, target_syndrome


def vandermonde_eliminate_residual(
    bits: int,
    points: Sequence[int],
    indices: Sequence[int],
    target_syndrome: Sequence[int],
    checks: int,
) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...], tuple[tuple[int, ...], ...]]:
    """Exact Vandermonde parity elimination on residual coordinate positions.

    Given residual positions U = indices with len(U) >= checks >= 1, splits U into
    pivot_indices = tuple(indices[:checks]) of length K = checks and
    free_indices = tuple(indices[checks:]) of length d = len(indices) - checks.
    Inverts the K x K Vandermonde matrix via Lagrange basis polynomials:
        L_r(Z) = P(Z) / ((Z - alpha_{p_r}) * P'(alpha_{p_r})) = sum_{j=0}^{K-1} ell_{r, j} Z^j
    where P(Z) = prod_{r=0}^{K-1} (Z - alpha_{p_r}).
    Returns (pivot_indices, free_indices, constants, coeffs) where
        x_{p_r} = constants[r] ^ sum_s coeffs[r][s] * x_{f_s}
    satisfies sum_{i in U} alpha_i^j x_i = target_syndrome[j] for all 0 <= j < checks.
    """
    integer(bits, 2, 128, "field bits")
    points, indices, target_syndrome = tuple(points), tuple(indices), tuple(target_syndrome)
    integer(len(points), 1, 1 << bits, "public point count")
    for point in points:
        integer(point, 0, (1 << bits)-1, "public field point")
    if len(set(points)) != len(points):
        raise ValueError("distinct public field points required")
    for index in indices:
        integer(index, 0, len(points)-1, "residual coordinate index")
    if len(set(indices)) != len(indices):
        raise ValueError("distinct residual coordinate indices required")
    integer(checks, 1, len(indices), "parity checks")
    if len(target_syndrome) != checks:
        raise ValueError("target_syndrome length must equal checks")
    for value in target_syndrome:
        integer(value, 0, (1 << bits)-1, "syndrome field element")

    pivot_indices = tuple(indices[:checks])
    free_indices = tuple(indices[checks:])
    K = checks
    d = len(free_indices)

    from flint import fq_default_poly_ctx

    ctx = field(bits)
    poly_ring = fq_default_poly_ctx(ctx)
    Z = poly_ring.gen()

    piv_alphas = [element(bits, points[i]) for i in pivot_indices]
    free_alphas = [element(bits, points[i]) for i in free_indices]
    h = [element(bits, target_syndrome[j]) for j in range(K)]

    P = poly_ring.one()
    for a in piv_alphas:
        P *= (Z - a)
    deriv = P.derivative()

    constants: list[int] = []
    coeffs: list[tuple[int, ...]] = []
    for r, a in enumerate(piv_alphas):
        denom = deriv(a)
        Lr = (P // (Z - a)) * (denom**-1)
        cr = sum((Lr[j] * h[j] for j in range(K)), ctx.zero())
        constants.append(encoded(cr))
        row = tuple(encoded(Lr(fa)) for fa in free_alphas)
        coeffs.append(row)

    # Deterministic algebraic verification of the elimination identities
    for j in range(K):
        val = sum((piv_alphas[r]**j * element(bits, constants[r]) for r in range(K)), ctx.zero())
        if val != h[j]:
            raise ArithmeticError("Vandermonde pivot syndrome identity failed")
    for s in range(d):
        for j in range(K):
            val = sum((piv_alphas[r]**j * element(bits, coeffs[r][s]) for r in range(K)), ctx.zero())
            if val != free_alphas[s]**j:
                raise ArithmeticError("Vandermonde free column elimination failed")

    return pivot_indices, free_indices, tuple(constants), tuple(coeffs)


class BinaryFieldCircuit:
    """Translate polynomial-basis field operations to exact bit-vector logic."""

    def __init__(self, bits):
        import z3
        self.z3, self.bits = z3, bits
        coefficients = field(bits).modulus().coeffs()
        self.reduction = sum(int(c) << j for j, c in enumerate(coefficients[:-1]))
        self.zero, self.one = z3.BitVecVal(0, bits), z3.BitVecVal(1, bits)

    def shifts(self, value):
        result = [value]
        for _ in range(1, self.bits):
            previous = result[-1]
            high = self.z3.Extract(self.bits-1, self.bits-1, previous) == 1
            result.append((previous << 1) ^ self.z3.If(high, self.reduction, self.zero))
        return result

    def constant_product(self, shifts, coefficient):
        return reduce(lambda a, b: a ^ b,
                      (v for j, v in enumerate(shifts) if (coefficient >> j) & 1), self.zero)

    def multiply(self, left, right):
        return reduce(lambda a, b: a ^ b,
                      (self.z3.If(self.z3.Extract(j, j, right) == 1, shifted, self.zero)
                       for j, shifted in enumerate(self.shifts(left))), self.zero)

    def inverse_graph(self, left, right):
        return self.z3.Or(self.z3.And(left == self.zero, right == self.zero),
                          self.multiply(left, right) == self.one)

    def trace(self, value):
        bits = [self.z3.Extract(j, j, value) for j in range(self.bits)
                if (trace_mask(self.bits, 1) >> j) & 1]
        return reduce(lambda a, b: a ^ b, bits, self.z3.BitVecVal(0, 1))


def run_experiment(instance, *, prefix_seed=1029, full=False, timeout_ms=30000,
                   resource_limit=50_000_000, solver_seed=0, pipeline="direct"):
    integer(timeout_ms, 1, 600_000, "solver timeout milliseconds")
    integer(resource_limit, 1, 2**31-1, "solver resource limit")
    integer(solver_seed, 0, 2**31-1, "solver seed")
    if pipeline not in ("direct", "qfbv", "vandermonde"):
        raise ValueError("pipeline must be direct, qfbv, or vandermonde")
    start = perf_counter()
    bits, points, targets, checks = validate_instance(instance)
    instance = {"bits": bits, "points": list(points), "targets": list(targets),
                "checks": checks, "field_modulus_coefficients": instance["field_modulus_coefficients"]}
    digest = hashlib.sha256(json.dumps(instance, sort_keys=True).encode()).hexdigest()
    indices, prefix, target_syndrome = restrict_instance(instance, prefix_seed, full=full)
    result = {"instance": instance, "instance_sha256": digest,
              "method": "Z3_exact_zero_complete_inverse_graph",
              "solver_pipeline": pipeline,
              "scope": "full_original_instance" if full else "fixed_accepted_prefix",
              "prefix_seed": prefix_seed, "residual_indices": list(indices),
              "accepted_prefix": [[i, x] for i, x in prefix.items()],
              "residual_syndrome": list(target_syndrome),
              "residual_free_field_variables": len(indices)-checks,
              "solver_timeout_ms": timeout_ms, "solver_resource_limit": resource_limit,
              "solver_seed": solver_seed, "full_original_word_verified": False,
              "witness": None, "hardness_evidence": False,
              "polynomial_time_solver_established": False, "uniform_sampler": False,
              "whole_workflow_wall_clock_cap_enforced": False}
    try:
        import z3
    except ImportError:
        return {**result, "status": "UNKNOWN_SOLVER_UNAVAILABLE",
                "total_seconds": perf_counter()-start}
    circuit = BinaryFieldCircuit(bits)
    if pipeline == "vandermonde":
        pivot_indices, free_indices, constants, coeffs = vandermonde_eliminate_residual(
            bits, points, indices, target_syndrome, checks
        )
        x_free = [z3.BitVec(f"x_{i}", bits) for i in free_indices]
        y = [z3.BitVec(f"y_{i}", bits) for i in indices]
        free_shifts = [circuit.shifts(xf) for xf in x_free]
        x_piv = [
            reduce(
                lambda a, b: a ^ b,
                (
                    circuit.constant_product(free_shifts[s], coeffs[r][s])
                    for s in range(len(free_indices))
                    if coeffs[r][s]
                ),
                z3.BitVecVal(constants[r], bits),
            )
            for r in range(checks)
        ]
        x_exprs = x_piv + x_free
        solver = z3.Then("simplify", "bit-blast", "sat").solver()
        solver.set(timeout=timeout_ms, rlimit=resource_limit, random_seed=solver_seed)
        for index, left_expr, right_var in zip(indices, x_exprs, y):
            solver.add(
                circuit.inverse_graph(left_expr, right_var),
                circuit.trace(right_var) == targets[index],
            )
        symbolic_field_vars = len(free_indices) + len(indices)
    else:
        x = [z3.BitVec(f"x_{i}", bits) for i in indices]
        y = [z3.BitVec(f"y_{i}", bits) for i in indices]
        # QF_BV preprocessing can exhaust the budget before any SAT search.
        solver = (z3.Then("simplify", "bit-blast", "sat").solver()
                  if pipeline == "direct" else z3.SolverFor("QF_BV"))
        solver.set(timeout=timeout_ms, rlimit=resource_limit, random_seed=solver_seed)
        parity = [circuit.zero for _ in range(checks)]
        for index, left, right in zip(indices, x, y):
            solver.add(circuit.inverse_graph(left, right), circuit.trace(right) == targets[index])
            shifts = circuit.shifts(left)
            alpha, power = element(bits, points[index]), field(bits).one()
            for j in range(checks):
                parity[j] = parity[j] ^ circuit.constant_product(shifts, encoded(power))
                power *= alpha
        solver.add(*(value == target for value, target in zip(parity, target_syndrome)))
        x_exprs = x
        symbolic_field_vars = 2 * len(indices)
    check_start = perf_counter()
    status = solver.check()
    check_end = perf_counter()
    statistics = solver.statistics()
    counters = {key: statistics.get_key_value(key) for key in statistics.keys()}
    result.update(z3_version=z3.get_version_string(),
                  setup_seconds=check_start-start, check_seconds=check_end-check_start,
                  solver_status=str(status), symbolic_field_variables=symbolic_field_vars,
                  solver_statistics=counters,
                  sat_search_observed=any(counters.get(key, 0) > 0
                                          for key in ("sat decisions", "sat conflicts")),
                  status="UNKNOWN_SOLVER_LIMIT")
    if status == z3.sat:
        model = solver.model()
        word = [prefix.get(i, 0) for i in range(len(points))]
        for index, expr in zip(indices, x_exprs):
            word[index] = model.eval(expr, model_completion=True).as_long()
        if not verify_word(instance, word):
            raise ArithmeticError("SMT witness failed independent original-instance verification")
        result.update(status="VERIFIED_NATIVE_WITNESS", witness=word,
                      full_original_word_verified=True)
    elif status == z3.unsat:
        result["status"] = "UNSAT_FULL_INSTANCE_REPORTED" if full else "UNSAT_THIS_RESIDUAL_ONLY"
    else:
        result["reason_unknown"] = solver.reason_unknown()
    result["total_seconds"] = perf_counter()-start
    return result
