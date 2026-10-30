"""Exact two-generator quaternion-order identities, not native curve validation.

Input traces/norms are supplied arithmetic. Even a positive order discriminant
divisible by a claimed characteristic does not authenticate native maps or
the ramification of their algebra.
"""

from pathlib import Path
import sys

from sympy import Matrix, eye

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "native-suborder-preprocessing-2026-10-26"))
from native_preprocessing import check_order
from kernel_output import QuaternionOrder


def commutator_norm(t, n, u, m, v):
    """N([a,b]) from Tr(a), N(a), Tr(b), N(b), Tr(ab)."""
    if any(type(value) is not int for value in (t, n, u, m, v)):
        raise ValueError("exact integer traces and norms required")
    return 4*n*m-n*u*u-m*t*t-v*v+t*u*v


def pair_order(t, n, u, m, v):
    """Return the formal positive order with basis (1,a,b,ab).

    This constructs Z[a,b] when a,b are genuine noncommuting integral
    elements of a definite quaternion algebra. It does not find a or b.
    """
    discriminant = commutator_norm(t, n, u, m, v)
    if n <= 0 or m <= 0 or t*t >= 4*n or u*u >= 4*m:
        raise ValueError("nonscalar positive quadratic norms required")
    if discriminant <= 0:
        raise ValueError("positive commutator norm required")
    one, a, b, ab = (eye(4)[:, i] for i in range(4))
    products = (
        (one, a, b, ab),
        (a, -n*one+t*a, ab, -n*b+t*ab),
        (b, (v-t*u)*one+u*a+t*b-ab, -m*one+u*b,
         -t*m*one+m*a+v*b),
        (ab, -u*n*one+v*a+n*b, -m*a+u*ab, -n*m*one+v*ab),
    )
    traces = Matrix([[2, t, u, v]])
    order = QuaternionOrder(products, one, one*traces-eye(4), traces)
    gram = check_order(order)
    if gram.det() != discriminant**2:
        raise ArithmeticError("pair discriminant identity failed")
    return order


def trace(order, element):
    return (order.traces*Matrix(element))[0]


def norm(order, element):
    element = Matrix(element)
    square = order.multiply(element, order.star(element))
    result = trace(order, square)/2
    if square != result*order.unit:
        raise ValueError("scalar quaternion norm required")
    return result
