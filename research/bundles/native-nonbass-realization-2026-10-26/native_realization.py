"""Known-order arithmetic controls for a native IsERP reduction.

No isogeny, unknown native order, theta label, or quantum receiver runs here.
The source constructor receives only the supplied suborder's table.
"""

from pathlib import Path
import sys

from sympy import Matrix, eye, zeros
from sympy.solvers.diophantine.diophantine import sum_of_four_squares

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "additive-framed-source-2026-10-26"))
from additive_source import QMatrix, construct, input_index
from kernel_output import (
    QuaternionOrder, integer_matrix, mod, odd_maximal_order,
    odd_maximal_split, reconstruct,
)


def rebase_order(order, basis):
    """Build a table for a supplied lattice, checking integral ring operations."""
    basis = Matrix(basis)
    if basis.shape != (4, 4) or basis.det() == 0:
        raise ValueError("full rational basis required")
    inverse = basis.inv()
    products = tuple(tuple(integer_matrix(inverse*order.multiply(basis[:, i], basis[:, j]))
                           for j in range(4)) for i in range(4))
    unit = integer_matrix(inverse*order.unit)
    involution = integer_matrix(inverse*order.involution*basis)
    traces = integer_matrix(order.traces*basis)
    return QuaternionOrder(products, unit, involution, traces)


def change_coordinates(matrix, change):
    change = Matrix(change)
    if change.shape != (4, 4) or change.det() == 0:
        raise ValueError("invertible quaternion basis change required")
    return QMatrix(tuple(sum((change[k, i]*matrix.coefficients[i] for i in range(4)),
                             zeros(*matrix.shape)) for k in range(4)))


def fixture(q, direction=0):
    """A known neighbor of the characteristic-11 order; all secrets supplied."""
    source = odd_maximal_order(11)
    split = odd_maximal_split(11, q)
    line = Matrix([0, 1]) if direction is None else Matrix([1, direction])
    target_basis = reconstruct(source, split, line, q).order_basis
    r_basis = Matrix.diag(1, q, q, q)
    target = rebase_order(source, target_basis)
    suborder = rebase_order(source, r_basis)
    index = input_index(suborder, 11)
    if index != q**3 or abs(target_basis.det()) != 1:
        raise AssertionError("wrong order indices")
    integer_matrix(target_basis.inv()*r_basis)
    return {"q": q, "source": source, "target": target,
            "target_basis": target_basis, "suborder": suborder,
            "r_basis": r_basis, "index": index}


def query_for(f, delta):
    """Convert a supplied rational delta to a legal residue query modulo d."""
    d, r = f["index"], f["r_basis"]
    beta = mod(integer_matrix(d*r.inv()*delta), d)
    gamma = r*beta/d
    roots = tuple(map(int, sum_of_four_squares(d**4-1)))
    result = construct(f["suborder"], beta, d, roots)
    return {"beta_in_r": beta, "gamma_in_source": gamma, "roots": roots,
            "construction": result}


def opposite_queries(f):
    """Integral in exactly one of the two known maximal orders."""
    b = f["target_basis"]
    new = next(b[:, i] for i in range(4) if any(x.q != 1 for x in b[:, i]))
    wrong = next(eye(4)[:, i] for i in range(4)
                 if any(x.q != 1 for x in b.inv()*eye(4)[:, i]))
    return query_for(f, new), query_for(f, wrong)
