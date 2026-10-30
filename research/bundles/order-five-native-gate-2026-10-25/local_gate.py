"""Exact local reference checks for the public order-five/Frobenius algebra.

The orbit checker receives a control Lagrangian; it is NOT the attack.
The actual attack uses the predecessor's source-side extract_kernel.
"""

from pathlib import Path
from itertools import combinations
import sys

from sympy import Matrix, eye, isprime, zeros

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT/"source-pullback-2026-10-23"))
from pullback import adjoint, column_basis, mod
from kernel_output import alternating_form, integer_matrix, inverse_mod


def check_actions(gamma, frobenius, p, ell):
    if (type(p) is not int or p <= 5 or p % 5 != 4 or not isprime(p)
            or type(ell) is not int or ell in (2, 5, p) or not isprime(ell)):
        raise ValueError("outside the characteristic/ell contract")
    g, t = mod(integer_matrix(gamma), ell), mod(integer_matrix(frobenius), ell)
    if g.shape != (4, 4) or t.shape != (4, 4):
        raise ValueError("four-dimensional actions required")
    if tuple(int(x) % ell for x in g.charpoly().all_coeffs()) != (1, 1, 1, 1, 1):
        raise ValueError("order-five characteristic polynomial required")
    if mod(adjoint(g)*g, ell) != eye(4) or mod(adjoint(t)*t-p*eye(4), ell) != zeros(4):
        raise ValueError("polarization multipliers failed")
    if mod(t*g-adjoint(g)*t, ell) != zeros(4):
        raise ValueError("Frobenius inversion relation failed")
    return g, adjoint(g), t, mod(adjoint(t), ell)


def orbit_control(lagrangian, gamma, frobenius, p, ell):
    alphabet = check_actions(gamma, frobenius, p, ell)
    plane = mod(integer_matrix(lagrangian), ell)
    if (plane.shape != (4, 2) or column_basis(plane, ell).cols != 2
            or mod(plane.T*alternating_form(2)*plane, ell) != zeros(2)):
        raise ValueError("Lagrangian control plane required")
    span, ranks = plane, [2]
    for _ in range(2):
        span = column_basis(Matrix.hstack(span, *(a*span for a in alphabet)), ell)
        ranks.append(span.cols)
    if ranks[-1] != 4:
        raise AssertionError("counterexample to the proposed two-layer theorem")
    return tuple(ranks)


def split_control(ell=11, zeta=3, p=19):
    """A local split-spectrum fixture, not a Tate basis of a native isogeny."""
    if zeta % ell == 1 or pow(zeta, 5, ell) != 1:
        raise ValueError("primitive fifth root required")
    # Standard (e1,e2,f1,f2) coordinates, then repository pairwise ordering.
    g = Matrix.diag(zeta, pow(zeta, 2, ell), pow(zeta, -1, ell), pow(zeta, -2, ell))
    t = zeros(2).row_join(-p*eye(2)).col_join(eye(2).row_join(zeros(2)))
    permutation = eye(4)[:, [0, 2, 1, 3]]
    g, t = mod(permutation.T*g*permutation, ell), mod(permutation.T*t*permutation, ell)
    check_actions(g, t, p, ell)
    return g, t


def pullback_control(plane, gamma, frobenius, p, ell):
    """Independent prime-square neighbor calculation with a KNOWN control L.

    This constructs reference pullbacks, not source-coordinate acquisition.
    No hidden target/kernel data from this function may feed the attack.
    """
    check_actions(gamma, frobenius, p, ell)
    plane, form = mod(integer_matrix(plane), ell), alternating_form(2)
    if (plane.shape != (4, 2) or column_basis(plane, ell).cols != 2
            or mod(plane.T*form*plane, ell) != zeros(2)):
        raise ValueError("Lagrangian control plane required")
    pairing = mod(plane.T*form, ell)
    indices = next(pair for pair in combinations(range(4), 2)
                   if int(pairing[:, list(pair)].det()) % ell)
    complement = zeros(4, 2)
    inverse = pairing[:, list(indices)].inv_mod(ell)
    for j, index in enumerate(indices):
        complement[index, :] = inverse[j, :]
    b = mod(complement.T*form*complement, ell)
    complement = mod(complement+plane*b*pow(2, -1, ell), ell)
    frame = plane.row_join(complement)[:, [0, 2, 1, 3]]
    error = integer_matrix((frame.T*form*frame-form)/ell)
    correction = mod(-pow(2, -1, ell)*form.inv()*error, ell)
    frame = mod(frame*(eye(4)+ell*correction), ell*ell)
    if mod(frame.T*form*frame-form, ell*ell) != zeros(4):
        raise ArithmeticError("public-chart reference lift failed")
    inverse = inverse_mod(frame, ell*ell)
    phi = Matrix.diag(1, ell, 1, ell)
    dual = adjoint(phi)
    actions = [mod(dual*inverse*a*frame*phi, ell*ell) for a in (gamma, frobenius)]
    actions += [mod(adjoint(a), ell*ell) for a in actions]
    first = column_basis(Matrix.hstack(*actions), ell)
    words = [integer_matrix(mod(a*b, ell*ell)/ell) for a in actions for b in actions]
    second = column_basis(Matrix.hstack(first, *words), ell)
    expected = eye(4)[:, [1, 3]]
    if second.cols != 2 or column_basis(second.row_join(expected), ell).cols != 2:
        raise AssertionError("source-side kernel extraction did not match the control")
    return (first.cols, second.cols)
