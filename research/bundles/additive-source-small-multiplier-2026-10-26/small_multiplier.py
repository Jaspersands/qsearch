"""Supplied-order certificates for the additive source's small multiplier.

No native endomorphism, geometric automorphism or PPAV model is discovered.
The order, query and symmetry are supplied arithmetic controls. In particular,
outside a quadratic FIELD must not be confused with outside a known ORDER.
"""

from pathlib import Path
import sys

from sympy import Matrix, eye, isprime, zeros

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "additive-framed-source-2026-10-26"))
sys.path.insert(0, str(ROOT / "full-suborder-impact-audit-2026-10-26"))
from additive_source import (
    QMatrix, adjoint, blocks, construct, multiply, scalar_matrix,
)
from pair_order import norm, trace


LOW_HIGH = (0, 2, 4, 6, 9, 11, 13, 15, 1, 3, 5, 7, 8, 10, 12, 14)


def reorder(value, inverse=False):
    """Use low/high coordinates separately in each original 16-dimensional copy."""
    size, cols = value.shape
    if size != cols or size % 16:
        raise ValueError("square dimension divisible by 16 required")
    indices = tuple(16*k+j for k in range(size//16) for j in LOW_HIGH)
    if inverse:
        indices = tuple(indices.index(j) for j in range(size))
    return QMatrix(tuple(a.extract(indices, indices) for a in value.coefficients))


def _integral_vector(value):
    value = Matrix(value)
    if value.shape != (4, 1) or any(x.is_Integer is not True for x in value):
        raise ValueError("four integral quaternion coordinates required")
    return value


def small_multiplier(order, beta, denominator, roots, copies=1):
    """Return H,C,Cbar with Cbar*C=a*I and C^dagger*H*C=a*I, a=n^2."""
    if type(copies) is not int or copies < 1:
        raise ValueError("positive integral copy count required")
    source = construct(order, beta, denominator, roots)
    h = reorder(source["polarization"])
    a, b = denominator**2, denominator**2+source["degree"]
    identity = scalar_matrix(order, eye(8))
    null = scalar_matrix(order, zeros(8))
    cross = QMatrix(tuple(x[:8, 8:] for x in h.coefficients))
    cross_adjoint = adjoint(order, cross)
    if h != blocks(identity.scale(a), cross, cross_adjoint, identity.scale(b)):
        raise ArithmeticError("scalar-diagonal block identity failed")
    if (multiply(order, cross, cross_adjoint) != identity.scale(a*b-1)
            or multiply(order, cross_adjoint, cross) != identity.scale(a*b-1)):
        raise ArithmeticError("cross-block norm identity failed")
    inverse_h = blocks(identity.scale(b), cross.scale(-1),
                       cross_adjoint.scale(-1), identity.scale(a))
    c = blocks(identity, cross.scale(-1), null, identity.scale(a))
    cbar = blocks(identity.scale(a), cross, null, identity)
    identity16 = scalar_matrix(order, eye(16))
    if (multiply(order, h, inverse_h) != identity16
            or multiply(order, inverse_h, h) != identity16
            or multiply(order, c, cbar) != identity16.scale(a)
            or multiply(order, cbar, c) != identity16.scale(a)
            or multiply(order, multiply(order, adjoint(order, c), h), c)
            != identity16.scale(a)):
        raise ArithmeticError("small-multiplier certificate failed")
    return {
        "beta": _integral_vector(beta), "denominator": denominator,
        "a": a, "b": b, "copies": copies,
        "h": h.repeat(copies), "inverse_h": inverse_h.repeat(copies),
        "c": c.repeat(copies), "cbar": cbar.repeat(copies),
        "corner_degree_bound": a*a,
        "supplied_order_control": True, "native_model_constructed": False,
    }


def noncommuting_entries(order, value, alpha):
    alpha = _integral_vector(alpha)
    if alpha == trace(order, alpha)*order.unit/2:
        raise ValueError("nonscalar orientation required")
    rows, cols = value.shape
    found = []
    for i in range(rows):
        for j in range(cols):
            entry = Matrix([x[i, j] for x in value.coefficients])
            if order.multiply(alpha, entry) != order.multiply(entry, alpha):
                found.append((i, j))
    return tuple(found)


def pullback_certificate(order, source, automorphism, alpha=None):
    """Check supplied W in ORIGINAL coordinates; return T in low/high coordinates.

    Recovery is W = C*T*Cbar/a^2, followed by inverse permutation. This is
    rational recovery; outside-R membership need not survive the pullback.
    """
    h, c, cbar, a = (source[k] for k in ("h", "c", "cbar", "a"))
    if automorphism.shape != h.shape or not automorphism.integral:
        raise ValueError("matching integral symmetry required")
    identity = scalar_matrix(order, eye(h.shape[0]))
    if (not all(value.integral for value in (h, c, cbar))
            or multiply(order, c, cbar) != identity.scale(a)
            or multiply(order, cbar, c) != identity.scale(a)
            or multiply(order, multiply(order, adjoint(order, c), h), c)
            != identity.scale(a)):
        raise ValueError("invalid small-multiplier data")
    w = reorder(automorphism)
    if multiply(order, multiply(order, adjoint(order, w), h), w) != h:
        raise ValueError("H-unitary symmetry required")
    pulled = multiply(order, multiply(order, cbar, w), c)
    if multiply(order, adjoint(order, pulled), pulled) != identity.scale(a*a):
        raise ArithmeticError("short-column norm identity failed")
    recovered = multiply(order, multiply(order, c, pulled), cbar)
    if recovered != w.scale(a*a):
        raise ArithmeticError("rational recovery identity failed")
    degrees = Matrix(h.shape[0], h.shape[1], lambda i, j:
                     norm(order, Matrix([x[i, j] for x in pulled.coefficients])))
    if any(x.is_Integer is not True or not 0 <= x <= a*a for x in degrees):
        raise ArithmeticError("invalid corner degree")
    if any(sum(degrees[:, j]) != a*a for j in range(degrees.cols)):
        raise ArithmeticError("column degree sum failed")
    result = {
        "dimension": h.shape[0], "multiplier": a,
        "corner_degree_bound": a*a, "degrees": degrees,
        "outside_quadratic_field": None, "noncommuting_entries": (),
        "outside_order_preservation_claimed": False,
        "supplied_order_and_automorphism_control": True,
        "native_extraction_executed": False,
    }
    if alpha is not None:
        alpha = _integral_vector(alpha)
        beta = source["beta"]
        if order.multiply(alpha, beta) != order.multiply(beta, alpha):
            raise ValueError("orientation must commute with the source query")
        before = noncommuting_entries(order, w, alpha)
        after = noncommuting_entries(order, pulled, alpha)
        if bool(before) != bool(after):
            raise ArithmeticError("quadratic-field equivalence failed")
        result.update(outside_quadratic_field=bool(after), noncommuting_entries=after)
    return pulled, result


def commutator_obstruction(characteristic, discriminant, degree_bound):
    """Numerical implication, CONDITIONAL on a genuine native orientation.

    The declared characteristic and discriminant do not authenticate that
    provenance. Failure of the inequality gives no evidence for a symmetry.
    """
    if (type(characteristic) is not int or characteristic <= 3
            or not isprime(characteristic)):
        raise ValueError("prime characteristic greater than three required")
    if (type(discriminant) is not int or discriminant >= 0
            or discriminant % 4 not in (0, 1)):
        raise ValueError("negative quadratic-order discriminant required")
    if type(degree_bound) is not int or degree_bound < 0:
        raise ValueError("nonnegative integral degree bound required")
    upper = abs(discriminant)*degree_bound
    return {
        "characteristic": characteristic, "discriminant": discriminant,
        "degree_bound": degree_bound, "commutator_norm_upper_bound": upper,
        "all_bounded_maps_commute_conditional": characteristic > upper,
        "native_orientation_authenticated": False,
        "conclusion_if_inequality_fails": "no_conclusion",
    }


def source_obstruction(order, alpha, beta, denominator, characteristic):
    """Apply the conditional obstruction using any native nonscalar alpha in K."""
    alpha, beta = _integral_vector(alpha), _integral_vector(beta)
    if type(denominator) is not int or denominator < 2:
        raise ValueError("denominator >=2 required")
    if beta == trace(order, beta)*order.unit/2:
        raise ValueError("scalar query needs a separate analysis")
    if alpha == trace(order, alpha)*order.unit/2:
        raise ValueError("nonscalar orientation required")
    if order.multiply(alpha, beta) != order.multiply(beta, alpha):
        raise ValueError("orientation must commute with the source query")
    discriminant = trace(order, alpha)**2-4*norm(order, alpha)
    if discriminant.is_Integer is not True:
        raise ValueError("integral orientation discriminant required")
    result = commutator_obstruction(characteristic, int(discriminant), denominator**4)
    result.update(denominator=denominator, all_stabilization_counts=True,
                  no_order_growth_requires_quadratic_saturation=True)
    return result
