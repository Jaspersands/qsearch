"""Exact supplied-order controls for ALL binary polarized factor projectors.

The argument does not assume the factor is the original E. The code consumes
a known ambient order to check a supplied projector, not native geometry.
"""

from pathlib import Path
import sys

from sympy import Matrix, zeros

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "polarization-completion-probe-2026-10-25"))
from polarization_probe import gram_matrix, matrix_multiply, noncommuting_corners, norm
from kernel_output import matrix_star


def scalar_value(order, value):
    value = Matrix(value)
    result = (order.traces*value)[0]/2
    if result.is_Integer is not True or value != result*order.unit:
        raise ValueError("integral scalar diagonal required")
    return int(result)


def factor_certificate(order, alpha, a, beta, d, projector):
    """Extract w=a*(H*P)_12-m*beta and certify deg(w)=m*(a-m)."""
    alpha, beta, projector = map(Matrix, (alpha, beta, projector))
    if alpha.shape != (4, 1) or any(x.is_Integer is not True for x in alpha):
        raise ValueError("integral known orientation required")
    if alpha == ((order.traces*alpha)[0]/2)*order.unit:
        raise ValueError("nonscalar known orientation required")
    if beta.shape != (4, 1) or order.multiply(alpha, beta) != order.multiply(beta, alpha):
        raise ValueError("beta must stay in the known quadratic algebra")
    h = gram_matrix(order, a, beta, d)
    if projector.shape != (16, 1) or any(x.is_Integer is not True for x in projector):
        raise ValueError("integral binary quaternion projector required")
    identity = Matrix.vstack(order.unit, zeros(4, 1), zeros(4, 1), order.unit)
    if projector == zeros(16, 1) or projector == identity:
        raise ValueError("proper nonzero factor required")
    if matrix_multiply(order, projector, projector) != projector:
        raise ValueError("idempotent required")
    s = matrix_multiply(order, h, projector)
    if matrix_star(order, s) != s:
        raise ValueError("H-orthogonal projector required")
    m = scalar_value(order, s[:4, :])
    n = scalar_value(order, s[12:, :])
    cross = s[4:8, :]
    if not 0 <= m <= a or not 0 <= n <= d or norm(order, cross) != m*n:
        raise ArithmeticError("rank-one positive factor Gram identity failed")
    witness = a*cross-m*beta
    degree = norm(order, witness)
    if degree != m*(a-m):
        raise ArithmeticError("short endomorphism norm identity failed")
    outside = bool(noncommuting_corners(order, alpha, projector))
    witness_outside = order.multiply(alpha, witness) != order.multiply(witness, alpha)
    if outside != witness_outside:
        raise ArithmeticError("commutant equivalence failed")
    return {"a": a, "d": d, "first_factor_degree": m,
            "witness_coefficients": [int(x) for x in witness],
            "witness_degree": degree, "degree_bound": a*a//4,
            "factor_leaves_known_quadratic_algebra": outside,
            "witness_does_not_commute": witness_outside,
            "factor_assumed_isomorphic_to_original_curve": False,
            "supplied_order_and_projector_control": True,
            "native_decomposition_or_enumeration_executed": False}


def shear_product_control(order, x, y, reverse=False):
    """Construct a positive CONTROL from a known unimodular matrix.

    Its hidden factor basis is supplied here. This is not a native search or
    a positive algorithmic discovery; alpha is the resulting cross entry.
    """
    zero, one = zeros(4, 1), order.unit
    upper = Matrix.vstack(one, x, zero, one)
    lower = Matrix.vstack(one, zero, y, one)
    upper_inverse = Matrix.vstack(one, -x, zero, one)
    lower_inverse = Matrix.vstack(one, zero, -y, one)
    left, right = (upper, lower) if reverse else (lower, upper)
    left_inv, right_inv = ((upper_inverse, lower_inverse) if reverse
                          else (lower_inverse, upper_inverse))
    w = matrix_multiply(order, left, right)
    inverse = matrix_multiply(order, right_inv, left_inv)
    h = matrix_multiply(order, matrix_star(order, w), w)
    coordinate_projector = Matrix.vstack(one, zero, zero, zero)
    projector = matrix_multiply(order, matrix_multiply(order, inverse, coordinate_projector), w)
    a, d = scalar_value(order, h[:4, :]), scalar_value(order, h[12:, :])
    beta = h[4:8, :]
    return a, beta, d, projector


def automorphism_certificate(order, alpha, a, beta, d, automorphism):
    """A binary H-unitary escape forces a short map or a native elliptic unit."""
    alpha, beta, automorphism = map(Matrix, (alpha, beta, automorphism))
    if alpha.shape != (4, 1) or any(x.is_Integer is not True for x in alpha):
        raise ValueError("integral known orientation required")
    if alpha == ((order.traces*alpha)[0]/2)*order.unit:
        raise ValueError("nonscalar known orientation required")
    if beta.shape != (4, 1) or order.multiply(alpha, beta) != order.multiply(beta, alpha):
        raise ValueError("beta must stay in the known quadratic algebra")
    h = gram_matrix(order, a, beta, d)
    if automorphism.shape != (16, 1) or any(x.is_Integer is not True for x in automorphism):
        raise ValueError("integral binary quaternion automorphism required")
    if matrix_multiply(order, matrix_multiply(order, matrix_star(order, automorphism), h), automorphism) != h:
        raise ValueError("H-unitary automorphism required")
    result = {"a": a, "d": d, "degree_bound": a*a,
              "witness_coefficients": None, "witness_degree": None,
              "branch": "known_quadratic_automorphism",
              "supplied_order_and_automorphism_control": True,
              "native_automorphism_computation_executed": False}
    if not noncommuting_corners(order, alpha, automorphism):
        return result
    x, u, y, v = (automorphism[i:i+4, :] for i in (0, 4, 8, 12))
    z = a*x+order.multiply(beta, y)
    if norm(order, z)+norm(order, y) != a*a:
        raise ArithmeticError("automorphism first-column norm identity failed")
    for branch, witness in (("first_column_y", y), ("first_column_completed_square", z)):
        if order.multiply(alpha, witness) != order.multiply(witness, alpha):
            break
    else:
        # The determinant-like phase is integral even though the comparison
        # SU(2) matrix in the proof can have denominator a.
        branch = "elliptic_unit_phase"
        witness = order.multiply(x, v)-order.multiply(y, u)
        if norm(order, witness) != 1:
            raise ArithmeticError("residual phase is not a native elliptic unit")
        if order.multiply(alpha, witness) == order.multiply(witness, alpha):
            raise ArithmeticError("noncommuting automorphism lost its phase")
    degree = norm(order, witness)
    if degree > a*a:
        raise ArithmeticError("automorphism short-map bound failed")
    result.update(branch=branch, witness_coefficients=[int(c) for c in witness], witness_degree=degree)
    return result
