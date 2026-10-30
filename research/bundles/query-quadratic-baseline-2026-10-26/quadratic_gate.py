"""Known-order arithmetic proposals for a classical gate; no native backend.

An algebraically integral candidate is NEVER certified as an endomorphism
of the user's curve. Native division and evaluator construction are external.
"""

from functools import reduce
from math import gcd, prod
from pathlib import Path
import sys

from sympy import Matrix, eye, isprime

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "full-suborder-impact-audit-2026-10-26"))
from pair_order import norm, trace


def integral_vector(value):
    value = Matrix(value)
    if value.shape != (4, 1) or any(x.is_Integer is not True for x in value):
        raise ValueError("four integral input-order coordinates required")
    return value


def query_intersection_generator(order, beta):
    """Generator of R intersect Q(beta), with the primitive unit FIRST.

    Returns None for scalar beta. Integer basis combinations construct the
    output; this performs no native scalar-division operation.
    """
    if order.unit != eye(4)[:, 0]:
        raise ValueError("unit-adapted input basis required")
    beta = integral_vector(beta)
    content = reduce(gcd, (abs(int(beta[i])) for i in range(1, 4)))
    if content == 0:
        return None
    return integral_vector((beta-beta[0]*order.unit)/content)


def index_prime_plan(index, factorization):
    """Validate SUPPLIED factorization; no factoring algorithm is invoked."""
    if type(index) is not int or index < 1 or index % 2 == 0:
        raise ValueError("positive odd index required after 2-saturation")
    factors = tuple(factorization)
    if any(type(p) is not int or p < 3 or not isprime(p)
           or type(e) is not int or e < 1 for p, e in factors):
        raise ValueError("odd prime factors and positive exponents required")
    if len({p for p, _ in factors}) != len(factors):
        raise ValueError("distinct prime factors required")
    if prod(p**e for p, e in factors) != index:
        raise ValueError("factorization does not match the input index")
    return tuple(sorted(factors))


def centered_division_proposal(order, beta, divisor):
    """Prepare (beta-shift)/divisor; NEVER assert native integrality."""
    if type(divisor) is not int or divisor < 3 or divisor % 2 == 0:
        raise ValueError("odd divisor >=3 required")
    beta = Matrix(beta)
    if beta.shape != (4, 1) or any(x.is_Rational is not True for x in beta):
        raise ValueError("exact rational coordinates required")
    t = trace(order, beta)
    if t.is_Integer is not True:
        raise ValueError("integral trace of a supplied native generator required")
    shift = int(t)*pow(2, -1, divisor) % divisor
    return {
        "divisor": divisor,
        "shift": shift,
        "numerator": beta-shift*order.unit,
        "candidate": (beta-shift*order.unit)/divisor,
        "native_integrality_certified": False,
    }


def quadratic_prime_proposal(order, theta, prime):
    """Unique odd-prime quadratic overorder, or no algebraic step.

    A proposal with integral trace and norm may still be non-native.
    Subsequent rational coordinates are legal only after real native division
    certified previous steps; the helper cannot authenticate that provenance.
    """
    if type(prime) is not int or prime < 3 or not isprime(prime):
        raise ValueError("odd prime required")
    theta = Matrix(theta)
    if theta.shape != (4, 1) or any(x.is_Rational is not True for x in theta):
        raise ValueError("exact rational coordinates required")
    t, n = trace(order, theta), norm(order, theta)
    if t.is_Integer is not True or n.is_Integer is not True:
        raise ValueError("integral quadratic trace and norm required")
    delta = int(t*t-4*n)
    if delta >= 0:
        raise ValueError("nonscalar definite quadratic generator required")
    if delta % (prime*prime):
        return None
    result = centered_division_proposal(order, theta, prime)
    candidate = result["candidate"]
    new_t, new_n = trace(order, candidate), norm(order, candidate)
    if (new_t.is_Integer is not True or new_n.is_Integer is not True
            or new_t*new_t-4*new_n != delta//(prime*prime)):
        raise ArithmeticError("quadratic overorder identity failed")
    result.update({"old_discriminant": delta, "new_discriminant": delta//(prime*prime),
                   "new_trace": int(new_t), "new_norm": int(new_n)})
    return result
