"""Proof controls only: local matrices and integral quaternion source fixtures."""

from sympy import Matrix, zeros

import residual_algebra
from controls import ArithmeticSource
from kernel_output import odd_maximal_order


def local_action(beta, ell):
    a = zeros(4)
    a[0, 0], a[1, 1], a[0, 1] = 2 * ell, 3 * ell, 1
    a[2:, 2:] = ell * beta
    return a


def quartic_fixture(kind):
    """Actual integral maps on a product; no surface geometry is executed."""
    order = odd_maximal_order(7)
    i, j, ij = Matrix([0, 1, 0, 0]), Matrix([-1, 0, 2, 0]), Matrix([0, -1, 0, 2])
    first = 2 * order.unit + ij
    if kind == "two":
        second, target_second = 2 * order.unit + j, order.unit + j
    elif kind == "one":
        second = target_second = 2 * i + j
    elif kind == "scalar":
        second, target_second = 2 * order.unit + j, order.unit
    else:
        raise ValueError("unknown fixture")
    phi = Matrix.vstack(first, zeros(4, 1), zeros(4, 1), second)
    gamma = Matrix.vstack(j, zeros(4, 1), zeros(4, 1), target_second)
    return ArithmeticSource(7, 11, order, phi, (gamma,))
