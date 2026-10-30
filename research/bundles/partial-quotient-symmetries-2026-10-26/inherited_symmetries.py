"""Supplied-matrix controls for symmetries forced by interpolation.

This does not compute a quotient variety or any geometric automorphism.
"""

from pathlib import Path
import sys

from sympy import Matrix, eye, kronecker_product

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "interpolation-leakage-2026-10-26"))
from interpolation_closure import adjoint, category_contains, interpolation_diamond


def quaternion_copy_group():
    i = Matrix([[0, -1, 0, 0], [1, 0, 0, 0], [0, 0, 0, -1], [0, 0, 1, 0]])
    j = Matrix([[0, 0, -1, 0], [0, 0, 0, 1], [1, 0, 0, 0], [0, -1, 0, 0]])
    return tuple(sign*x for x in (eye(4), i, j, i*j) for sign in (1, -1))


def product_action(copy_matrix):
    """Lift a supplied four-copy action to the source/target Tate control."""
    copy_matrix = Matrix(copy_matrix)
    if copy_matrix.shape != (4, 4) or any(x.is_Integer is not True for x in copy_matrix):
        raise ValueError("four-copy integral matrix required")
    return kronecker_product(Matrix.diag(copy_matrix, copy_matrix), eye(2))


def graph_intertwining(q, roots):
    """Exact identity in proof coordinates, before reduction at ANY divisor."""
    psi, multiplier = interpolation_diamond(q, roots)
    # The upper block is A4 tensor I2; the negative lower-left is phi I4.
    scalar = psi[:8, :8]
    graph = scalar.T.col_join(-psi[8:, :8])
    group = quaternion_copy_group()
    for b in group:
        u = product_action(b)
        if u*graph != graph*kronecker_product(b, eye(2)):
            raise ArithmeticError("graph is not invariant under copy symmetry")
        if adjoint(u)*u != eye(16) or not category_contains(u, q, 4):
            raise ArithmeticError("copy symmetry left the known category")
    return graph, multiplier


def supplied_pullbacks(q, roots, divisor):
    _, multiplier = graph_intertwining(q, roots)
    if type(divisor) is not int or divisor < 1 or multiplier % divisor:
        raise ValueError("positive divisor of auxiliary multiplier required")
    return tuple(divisor*product_action(b) for b in quaternion_copy_group())


def control(q, roots, divisor):
    maps = supplied_pullbacks(q, roots, divisor)
    if not all(adjoint(x)*x == divisor**2*eye(16) for x in maps):
        raise ArithmeticError("pullback norm identity failed")
    return {"prime": q, "roots": list(roots), "partial_multiplier": divisor,
            "forced_group_order": len(maps),
            "all_supplied_pullbacks_in_known_category": all(
                category_contains(x, q, 4) for x in maps),
            "native_partial_quotient_computed": False,
            "geometric_automorphism_list_computed": False,
            "useful_native_map_found": False}
