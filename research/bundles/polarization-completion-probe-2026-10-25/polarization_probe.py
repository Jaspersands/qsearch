"""Supplied-order controls for a geometric polarization-completion lead.

The order enumeration is a verification fixture, NOT legal access for the
proposed native algorithm. No theta decomposition or unknown map is computed.
"""

from collections import defaultdict
from itertools import product
from math import isqrt, prod
from pathlib import Path
import sys

from sympy import Matrix, eye

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "kernel-output-2026-10-23"))
from kernel_output import (
    QuaternionOrder, matrix_multiply, matrix_star, odd_maximal_order,
    odd_maximal_split, reconstruct, action, mod,
)


def norm(order, value):
    result = (order.traces*order.multiply(order.star(value), value))[0]/2
    if result.q != 1 or result < 0:
        raise ValueError("integral definite quaternion norm required")
    return int(result)


def neighbor_fixture(characteristic=23, direction=None, twisted=False):
    """Known maximal order of a degree-three quotient, not its curve model."""
    source = odd_maximal_order(characteristic)
    split = odd_maximal_split(characteristic, 3)
    known = (source.multiply(eye(4)[:, 1], 2*eye(4)[:, 2]-source.unit)
             if twisted else eye(4)[:, 2])
    if direction is None:
        local = mod(action(known, split), 3)
        direction = next(v for v in ((1, 0), (0, 1), (1, 1), (2, 1))
                         if Matrix.hstack(Matrix(v), local*Matrix(v)).det() % 3 == 0)
    basis = reconstruct(source, split, Matrix(direction), 3).order_basis
    inverse = basis.inv()
    products = tuple(tuple(inverse*source.multiply(basis[:, i], basis[:, j])
                           for j in range(4)) for i in range(4))
    order = QuaternionOrder(products, inverse*source.unit,
                            inverse*source.involution*basis, source.traces*basis)
    if any(x.q != 1 for row in products for value in row for x in value):
        raise ArithmeticError("neighbor order not closed integrally")
    alpha = inverse*known
    if any(x.q != 1 for x in alpha):
        raise ValueError("this neighbor does not retain the stated quadratic orientation")
    return order, alpha, basis


def norm_table(order, bound, max_box=1_000_000):
    """Complete finite enumeration with an explicit coefficient-box charge."""
    if type(bound) is not int or bound < 0:
        raise ValueError("nonnegative norm bound required")
    if type(max_box) is not int or max_box < 1:
        raise ValueError("positive enumeration budget required")
    gram = Matrix(4, 4, lambda i, j:
                  (order.traces*order.multiply(order.star(eye(4)[:, i]), eye(4)[:, j]))[0]/2)
    if not gram.is_positive_definite:
        raise ValueError("positive norm form required")
    inverse = gram.inv()
    radii = []
    for i in range(4):
        square = bound*inverse[i, i]
        radii.append(isqrt(int(square.p)//int(square.q)))
    box = prod(2*r+1 for r in radii)
    if box > max_box:
        raise ValueError("supplied-order enumeration exceeds declared box budget")
    table = defaultdict(list)
    for coefficients in product(*(range(-r, r+1) for r in radii)):
        vector = Matrix(coefficients)
        value = (vector.T*gram*vector)[0]
        if value <= bound:
            if value.q != 1:
                raise ArithmeticError("fixture contains a nonintegral norm")
            table[int(value)].append(vector)
    return dict(table), {"norm_bound": bound, "coefficient_box": box,
                         "retained_elements": sum(map(len, table.values())),
                         "full_order_advice_used": True}


def gram_matrix(order, a, beta, d):
    beta = Matrix(beta)
    if beta.shape != (4, 1) or any(c.q != 1 for c in beta):
        raise ValueError("integral quaternion coefficients required")
    if type(a) is not int or type(d) is not int or a <= 0 or a*d-norm(order, beta) != 1:
        raise ValueError("positive unimodular binary Hermitian form required")
    return Matrix.vstack(a*order.unit, Matrix(beta), order.star(beta), d*order.unit)


def unit_projectors(order, a, beta, d, table):
    """Free E-factor witnesses only, not all polarized decompositions.

    Completeness also requires a complete supplied table through norm a.
    The search identity is norm(a*x+beta*y)+norm(y)=a.
    """
    h = gram_matrix(order, a, beta, d)
    for y_norm in range(a+1):
        for y in table.get(y_norm, ()):
            beta_y = order.multiply(beta, y)
            for z in table.get(a-y_norm, ()):
                x = (z-beta_y)/a
                if any(c.q != 1 for c in x):
                    continue
                row0 = a*order.star(x)+order.multiply(order.star(y), order.star(beta))
                row1 = order.multiply(order.star(x), beta)+d*order.star(y)
                assert order.multiply(row0, x)+order.multiply(row1, y) == order.unit
                projector = Matrix.vstack(*(order.multiply(v, w) for v in (x, y) for w in (row0, row1)))
                assert matrix_multiply(order, projector, projector) == projector
                assert matrix_multiply(order, matrix_star(order, projector), h) == matrix_multiply(order, h, projector)
                yield (x, y), projector


def noncommuting_corners(order, alpha, projector):
    return [i for i in range(4)
            if order.multiply(alpha, projector[4*i:4*i+4, :]) !=
            order.multiply(projector[4*i:4*i+4, :], alpha)]


def low_degree_witness(order, alpha, a, beta, column):
    """Check the small-a attack certificate, never fabricate native access."""
    if order.multiply(alpha, beta) != order.multiply(beta, alpha):
        raise ValueError("beta already leaves the known quadratic algebra")
    x, y = column
    if any(v.shape != (4, 1) or any(c.q != 1 for c in v) for v in (x, y)):
        raise ValueError("integral witness column required")
    z = a*x+order.multiply(beta, y)
    if norm(order, z)+norm(order, y) != a:
        raise ValueError("column does not satisfy the norm-one identity")
    for name, value in (("y", y), ("a*x+beta*y", z)):
        if order.multiply(alpha, value) != order.multiply(value, alpha):
            return {"witness": name, "degree": norm(order, value),
                    "coefficients": [int(c) for c in value],
                    "degree_bound": a, "native_enumeration_executed": False}
    return None


def completion_control(a_max=8, characteristic=23, twisted=False):
    """Blind form generation uses only quadratic coefficients; oracle is a fixture."""
    if type(a_max) is not int or a_max < 2:
        raise ValueError("a_max must be an integer at least two")
    order, alpha, basis = neighbor_fixture(characteristic, twisted=twisted)
    table, resources = norm_table(order, a_max)
    units = table.get(1, ())
    if len(units) != 2:
        raise ValueError("extra-automorphism fixture is already an easy classical case")
    attempted = 0
    for a in range(2, a_max+1):
        for u in range(-a, a+1):
            for v in range(1, a+1):
                beta = u*order.unit+v*alpha
                value = norm(order, beta)+1
                if value % a:
                    continue
                d = value//a
                if d < a:
                    continue
                attempted += 1
                for column, projector in unit_projectors(order, a, beta, d, table):
                    corners = [projector[i:i+4, :] for i in range(0, 16, 4)]
                    outside = noncommuting_corners(order, alpha, projector)
                    if outside:
                        attack = low_degree_witness(order, alpha, a, beta, column)
                        assert attack is not None
                        return {"found": True, "characteristic": characteristic,
                                "orientation": "twisted Frobenius" if twisted else "half Frobenius",
                                "order_unit_count": len(units), "forms_tested": attempted,
                                "a": a, "d": d, "beta_coefficients": [u, v], "trace": a+d,
                                "column": [[int(c) for c in x] for x in column],
                                "projector": [int(c) for c in projector],
                                "noncommuting_corners": outside,
                                "corner_norms": [norm(order, x) for x in corners],
                                "small_a_classical_certificate": attack,
                                "norm_enumeration": resources,
                                **scope()}
    return {"found": False, "characteristic": characteristic, "forms_tested": attempted,
            "orientation": "twisted Frobenius" if twisted else "half Frobenius",
            "a_max": a_max, "order_unit_count": len(units),
            "norm_enumeration": resources, **scope()}


def scope():
    return {"supplied_order_control": True,
            "native_geometric_decomposition": False,
            "all_polarized_decompositions_searched": False,
            "search_scope": "free original-E factors within the stated finite form box",
            "global_nonexistence_claim": False,
            "speedup_claim": False}


if __name__ == "__main__":
    import json
    print(json.dumps([completion_control(), completion_control(characteristic=47, twisted=True)], indent=2))
