"""Exact controls for a classical geometric-symmetry extraction proposal.

The verifier consumes supplied matrices in a known ambient order. It does
NOT find geometric automorphisms, authenticate native maps or execute a
native EndRing algorithm. The native attack is specified in HARVEST.md.
"""

from math import gcd
from pathlib import Path
import sys

from sympy import Matrix, eye, isprime, kronecker_product, zeros
from sympy.matrices.normalforms import hermite_normal_form

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "additive-framed-source-2026-10-26"))
from additive_source import adjoint, multiply, scalar_matrix
from kernel_output import integer_matrix


def integral_coordinates(value):
    matrix = Matrix(value)
    return all(x.is_Integer is True for x in matrix)


def entries(matrix):
    rows, cols = matrix.shape
    return tuple(Matrix([a[i, j] for a in matrix.coefficients])
                 for i in range(rows) for j in range(cols))


def outside_lattice(matrix, basis):
    """Known-order test adapter; native code instead reconstructs trace coordinates."""
    basis = Matrix(basis)
    if basis.shape != (4, 4) or basis.det() == 0 or not integral_coordinates(basis):
        raise ValueError("full integral lattice basis required")
    inverse = basis.inv()
    return tuple(i for i, value in enumerate(entries(matrix))
                 if not integral_coordinates(inverse*value))


def pullback_certificate(order, z, c, f, w, multiplier, index):
    """Verify L=C*w*F, not an implementation of q^dagger*a*q."""
    if type(multiplier) is not int or multiplier < 1 or type(index) is not int or index < 1:
        raise ValueError("positive integral multiplier and index required")
    if z.shape[0] != z.shape[1] or any(m.shape != z.shape for m in (c, f, w)):
        raise ValueError("common square matrix shape required")
    if not all(m.integral for m in (z, c, f, w)):
        raise ValueError("integral morphism coordinates required")
    identity = scalar_matrix(order, eye(z.shape[0]))
    q = multiplier
    if adjoint(order, z) != z:
        raise ValueError("Hermitian polarization required")
    if (multiply(order, f, c) != identity.scale(q)
            or multiply(order, c, f) != identity.scale(q)
            or multiply(order, adjoint(order, c), c) != z.scale(q)
            or multiply(order, multiply(order, adjoint(order, f), z), f) != identity.scale(q)):
        raise ValueError("converter certificate failed")
    if multiply(order, multiply(order, adjoint(order, w), z), w) != z:
        raise ValueError("not a polarized symmetry")
    pulled = multiply(order, multiply(order, c, w), f)
    if multiply(order, adjoint(order, pulled), pulled) != identity.scale(q*q):
        raise ArithmeticError("pullback norm identity failed")
    if multiply(order, multiply(order, f, pulled), c) != w.scale(q*q):
        raise ArithmeticError("recovery identity failed")
    return pulled, {
        "multiplier": q, "index": index,
        "coprime_index_transport": gcd(q, index) == 1,
        "corner_degree_bound": q*q,
        "native_pullback_executed": False,
    }


def adjoin_and_close(order, basis, new_elements):
    """Exact supplied-coordinate ring closure, not unknown-order discovery."""
    basis = Matrix(basis)
    if basis.shape != (4, 4) or basis.det() == 0 or not integral_coordinates(basis):
        raise ValueError("full integral lattice basis required")
    basis = hermite_normal_form(integer_matrix(basis))
    if not integral_coordinates(basis.inv()*order.unit):
        raise ValueError("input lattice must contain the identity")
    additions = []
    for value in new_elements:
        value = Matrix(value)
        if value.shape != (4, 1) or not integral_coordinates(value):
            raise ValueError("integral ambient-order elements required")
        additions.append(value)
    chain = [int(basis.det())]
    enlarged = hermite_normal_form(integer_matrix(Matrix.hstack(basis, *additions)))
    for _ in range(chain[0].bit_length()+1):
        determinant = int(enlarged.det())
        if determinant != chain[-1]:
            if determinant <= 0 or chain[-1] % determinant:
                raise ArithmeticError("nonmonotone containment index")
            chain.append(determinant)
        products = [order.multiply(enlarged[:, i], enlarged[:, j])
                    for i in range(4) for j in range(4)]
        closed = hermite_normal_form(integer_matrix(Matrix.hstack(enlarged, *products)))
        if closed == enlarged:
            return enlarged, chain
        enlarged = closed
    raise ArithmeticError("strict index-descent bound exceeded")


def trace_coordinates(gram, mixed_traces):
    gram, mixed_traces = Matrix(gram), Matrix(mixed_traces)
    if gram.shape != (4, 4) or mixed_traces.shape != (4, 1) or gram.det() == 0:
        raise ValueError("nonsingular four-dimensional trace data required")
    if any(x.is_Rational is not True for x in list(gram)+list(mixed_traces)):
        raise ValueError("exact rational trace data required")
    return gram.inv()*mixed_traces


def coprime_scalar_shift(characteristic, trace, degree):
    """Select a prime-to-p endomorphism for compression; no interpolation is run."""
    if type(characteristic) is not int or characteristic <= 3 or not isprime(characteristic):
        raise ValueError("prime characteristic greater than three required")
    if type(trace) is not int or type(degree) is not int or degree < 0:
        raise ValueError("integer trace and nonnegative degree required")
    for shift in (0, 1, 2):
        shifted_degree = degree+trace*shift+shift*shift
        if shifted_degree > 0 and shifted_degree % characteristic:
            return shift, shifted_degree
    raise ValueError("degree/trace data violate the positive norm promise")


def pell_product_factor(n, k):
    """Integral P with Z_0=P^T*P for n^2-2k^2=1, roots=(2k^2,2k,0,0)."""
    if type(n) is not int or type(k) is not int or n < 2 or k <= 0 or n*n-2*k*k != 1:
        raise ValueError("positive nontrivial Pell pair required")
    j = Matrix([[0, -1], [1, 0]])
    rotation = Matrix.diag(j, j)
    identity = eye(4)
    p = (identity+k*rotation).row_join(k*rotation).col_join(
        (k*identity).row_join(rotation+k*identity))
    inverse = (identity-k*rotation).row_join(-k*identity).col_join(
        (k*rotation).row_join(k*identity-rotation))
    if p*inverse != eye(8) or inverse*p != eye(8):
        raise ArithmeticError("Pell factor is not integral unimodular")
    return kronecker_product(p, eye(2)), kronecker_product(inverse, eye(2))
