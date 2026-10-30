"""Exact controls for completion of transported maps by product corners.

These functions receive reference coordinates for proof controls. They
are not geometric extraction code and do not claim to discover a target
endomorphism lattice from an arbitrary modeled PPAV.
"""

from pathlib import Path
import sys

from sympy import GF, Matrix, eye, isprime, zeros
from sympy.matrices.normalforms import hermite_normal_form
from sympy.polys.matrices import DomainMatrix

sys.path.insert(0, str(Path(__file__).resolve().parent.parent/"kernel-output-2026-10-23"))
from kernel_output import (
    alternating_form, integer_matrix, matrix_multiply, matrix_star, mod, odd_maximal_order,
)


def rank_mod(matrix, prime):
    return DomainMatrix.from_Matrix(mod(matrix, prime)).convert_to(GF(prime)).rank()


def corner_ranks(transport, prime):
    """Local ranks of span pi_i * phi * X * phi^dagger * iota_j."""
    if not isprime(prime) or prime == 2:
        raise ValueError("odd prime required")
    transport, j = mod(transport, prime), alternating_form(2)
    if transport.shape != (4, 4) or rank_mod(transport, prime) != 2:
        raise ValueError("rank-two surface transport required")
    adjoint = mod(j.inv()*transport.T*j, prime)
    if mod(transport*adjoint, prime) != zeros(4) or mod(adjoint*transport, prime) != zeros(4):
        raise ValueError("isotropic image and kernel required")
    images = []
    for column in range(16):
        a = zeros(4)
        a[column//4, column % 4] = 1
        images.append(mod(transport*a*adjoint, prime))
    return tuple(tuple(rank_mod(Matrix.hstack(*(
        Matrix(list(a[2*i:2*i+2, 2*k:2*k+2])) for a in images)), prime)
                       for k in range(2)) for i in range(2))


def transport_generators(order, phi):
    phi = Matrix(phi)
    if phi.shape != (16, 1):
        raise ValueError("rank-two quaternion matrix coordinates required")
    adjoint = matrix_star(order, phi)
    return tuple(matrix_multiply(order, matrix_multiply(order, phi, eye(16)[:, a]), adjoint)
                 for a in range(16))


def complete_by_corners(order, phi):
    generators = []
    for transported in transport_generators(order, phi):
        for block in range(4):
            corner = zeros(16, 1)
            corner[4*block:4*block+4, :] = transported[4*block:4*block+4, :]
            generators.append(corner)
    return hermite_normal_form(Matrix.hstack(*generators))


def complete_with_known_map(order, phi, gamma):
    """Integral span of F, gamma*F, F*gamma, gamma*F*gamma."""
    gamma = integer_matrix(gamma)
    generators = []
    for f in transport_generators(order, phi):
        left, right = matrix_multiply(order, gamma, f), matrix_multiply(order, f, gamma)
        generators.extend((f, left, right, matrix_multiply(order, left, gamma)))
    return hermite_normal_form(integer_matrix(Matrix.hstack(*generators)))


def weak_corner_actions(source_actions, weak_action, ell, prime):
    """Actual usable interface: only small-torsion actions, no secret K."""
    if not isprime(prime) or prime == 2 or ell % prime == 0:
        raise ValueError("odd auxiliary prime coprime to ell required")
    w = mod(weak_action, prime)
    if w.shape != (4, 4) or len(source_actions) != 16:
        raise ValueError("surface actions of a full source basis required")
    inverse = w.inv_mod(prime)
    result = []
    for a in source_actions:
        f = mod(ell*w*Matrix(a)*inverse, prime)
        for row in range(2):
            for col in range(2):
                corner = zeros(4)
                corner[2*row:2*row+2, 2*col:2*col+2] = f[2*row:2*row+2, 2*col:2*col+2]
                result.append(corner)
    return tuple(result)


def reference_gram(order):
    basis, gram = eye(16), zeros(16)
    for i in range(16):
        for k in range(16):
            product = matrix_multiply(order, matrix_star(order, basis[:, i]), basis[:, k])
            gram[i, k] = (order.traces*(product[:4, :]+product[12:16, :]))[0]
    return gram


def gaussian_fixture(p, real=6, imaginary=3, off_diagonal=4):
    """Integral phi with phi^dagger phi=(a^2+b^2+c^2)I in M_2(O)."""
    order = odd_maximal_order(p)
    a = Matrix([real, imaginary, 0, 0])
    b = off_diagonal*order.unit
    return order, Matrix.vstack(a, b, -b, order.star(a))
