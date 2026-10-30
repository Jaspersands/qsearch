"""Prime-only source arithmetic; no geometric label generator is implemented."""

from math import gcd
from pathlib import Path
import sys

from sympy import Matrix, isprime, nextprime, zeros

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "kernel-output-2026-10-23"))
sys.path.insert(0, str(ROOT / "smooth-repolarization-2026-10-23"))
from kernel_output import integer_matrix, matrix_multiply, matrix_star, mod
from uniform_source_bound import lift_symplectic, uniform_surface_bound
from smooth_repolarization import (
    Quadratic, _four_square_witness, matmul, norm_matrix, transpose,
)


def odd_trace_lift(order, split, matrix, ell):
    """Lift the SAME symplectic query, forcing sigma == [[1,1],[0,1]] mod 2."""
    matrix = integer_matrix(matrix)
    if matrix.shape != (4, 4):
        raise ValueError("surface-only lift requires a four by four query")
    old = lift_symplectic(order, split, matrix, ell)
    identity = Matrix.vstack(order.unit, zeros(4, 1), zeros(4, 1), order.unit)
    sigma, inverse = identity.copy(), identity.copy()
    factors = []
    for a, b, q in old["factors"]:
        q = mod(pow(2, -1, ell) * q, ell)
        q = q.applyfunc(lambda x: 2*(int(x)-ell if 2*x > ell else int(x)))
        factors.append((a, b, q))
    factors.append((0, 1, ell * order.unit))
    for a, b, q in factors:
        forward, backward = identity.copy(), identity.copy()
        forward[4*(2*a+b):4*(2*a+b)+4, :] += q
        backward[4*(2*a+b):4*(2*a+b)+4, :] -= q
        sigma = matrix_multiply(order, sigma, forward)
        inverse = matrix_multiply(order, backward, inverse)
    s = matrix_multiply(order, matrix_star(order, sigma), sigma)
    t = (order.traces * (s[:4, :] + s[12:, :]))[0]/2
    if t.q != 1 or t < 3 or int(t) % 2 != 1:
        raise ArithmeticError("parity-controlled lift failed")
    return {"sigma": sigma, "inverse": inverse, "S": s, "trace": int(t),
            "factors": tuple(factors), "quaternion_length": len(factors),
            "physical_length": old["physical_length"]}


def odd_trace_bound(order, ell):
    old = uniform_surface_bound(order, ell)
    u = 2 + 4*(ell-1)**2*old["basis_norm_sum"]
    return {"basis_norm_sum": old["basis_norm_sum"],
            "even_factor_bound": u, "even_factor_count_bound": 156,
            "last_factor_bound": 2+ell*ell, "quaternion_length_bound": 157,
            "trace_bound": u**156 * (2+ell*ell)}


def prime_coin_witness(trace, multiplier):
    """Odd-trace certificate, without requiring or factoring a square target."""
    if type(trace) is not int or trace < 3 or trace % 2 != 1:
        raise ValueError("odd integer trace >= 3 required")
    if (type(multiplier) is not int or multiplier % 2 != 1
            or multiplier < trace*trace-4):
        raise ValueError("odd multiplier >= trace squared minus four required")
    a, b = trace+2, trace-2
    x = 0 if b == 1 else multiplier*pow(a, -1, b) % b
    y = (multiplier-a*x)//b
    if min(x, y) < 0 or a*x+b*y != multiplier:
        raise ArithmeticError("invalid coin witness")
    return x, y


def prime_certificate(trace, multiplier):
    """Formal identity only; squarefree access comes from prime_resource_plan.

    SymPy produces checked four-square witnesses, not a verified uniform
    polynomial-time four-square implementation or a geometric polarization.
    """
    x, y = prime_coin_witness(trace, multiplier)
    rx, ry = _four_square_witness(x), _four_square_witness(y)
    one, h = Quadratic(trace, 1), Quadratic(trace, 0, 1)
    coefficients = tuple(a*(h+one) for a in rx) + tuple(b*(one-h) for b in ry)
    c = norm_matrix(coefficients)
    hinv = Quadratic(trace, trace, -1)
    f = tuple(tuple(hinv*z for z in row) for row in transpose(c))
    return {"trace": trace, "multiplier": multiplier,
            "coin_x": x, "coin_y": y, "four_squares_x": rx, "four_squares_y": ry,
            "C": c, "F": f}


def verify_prime_certificate(record):
    t, n = record["trace"], record["multiplier"]
    prime_coin_witness(t, n)
    one, zero, h = Quadratic(t, 1), Quadratic(t), Quadratic(t, 0, 1)
    scaled = lambda z: tuple(tuple(z if i == j else zero for j in range(8)) for i in range(8))
    c, f = record["C"], record["F"]
    hf = tuple(tuple(h*z for z in row) for row in f)
    return {
        "coin": (t+2)*record["coin_x"]+(t-2)*record["coin_y"] == n,
        "four_squares": all(sum(a*a for a in record[key]) == record[value]
                            for key, value in (("four_squares_x", "coin_x"),
                                               ("four_squares_y", "coin_y"))),
        "C_adjoint_C": matmul(transpose(c), c) == scaled(n*h),
        "C_C_adjoint": matmul(c, transpose(c)) == scaled(n*h),
        "F_adjoint_H_F": matmul(transpose(f), hf) == scaled(n*one),
        "F_C": matmul(f, c) == scaled(n*one),
        "C_F": matmul(c, f) == scaled(n*one),
    }


def prime_resource_plan(trace_bound, ell, characteristic):
    """Fixed plan from a public bound, never from an observed query trace."""
    if type(trace_bound) is not int or trace_bound < 3:
        raise ValueError("integer public trace bound >= 3 required")
    if (type(ell) is not int or type(characteristic) is not int or ell < 3
            or characteristic <= 3 or not isprime(ell) or not isprime(characteristic)
            or ell == characteristic):
        raise ValueError("distinct odd primes ell and characteristic > 3 required")
    n, r, primes = 1, 3, []
    while n <= trace_bound*trace_bound:
        if r not in (ell, characteristic):
            n *= r
            primes.append(r)
        r = int(nextprime(r))
    marking_product, marks = 1, []
    threshold = 8*16**3*ell**2
    while marking_product*marking_product <= threshold:
        if gcd(r, characteristic*ell*n) == 1:
            marking_product *= r
            marks.append(r)
        r = int(nextprime(r))
    return {"trace_bound": trace_bound, "multiplier": n,
            "quotient_primes": primes, "marking_primes": marks,
            "weak_evaluation_orders": primes+marks,
            "marking_product": marking_product, "marking_threshold_squared": threshold,
            "quotient_torsion_exponent": 1,
            "auxiliary_field_degree_bounds": {str(r): r-1 for r in primes+marks},
            "largest_quotient_kernel_point_list": max(r**16 for r in primes),
            "stabilized_dimension": 16, "theta_level_four_still_required": True,
            "geometric_backend_executed": False, "quantum_execution": False,
            "speedup_established": False}
