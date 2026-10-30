"""Prime-square isotropic flags, including non-free kernels.

Exact torsion-module controls only. The returned bases are not geometric
points, quotient maps, or a hidden-kernel recovery algorithm.
"""

from dataclasses import dataclass
from math import gcd, prod

from sympy import GF, Matrix, ZZ, eye, isprime, zeros
from sympy.polys.matrices import DomainMatrix
from sympy.polys.matrices.normalforms import smith_normal_decomp
from sympy.matrices.normalforms import hermite_normal_form


def integral(a):
    a = Matrix(a)
    if any(x.q != 1 for x in a):
        raise ValueError("integral matrix required")
    return Matrix(a.rows, a.cols, [int(x) for x in a])


def mod(a, n):
    return integral(a).applyfunc(lambda x: int(x) % n)


def field_matrix(a, r):
    return DomainMatrix.from_Matrix(mod(a, r)).convert_to(GF(r))


def basis(a, r):
    a = mod(a, r)
    _, pivots = field_matrix(a, r).rref()
    return a[:, list(pivots)]


def nullspace(a, r):
    return mod(field_matrix(a, r).nullspace().to_Matrix().T, r)


def contained(a, b, r):
    return basis(b.row_join(a), r).cols == basis(b, r).cols


def symplectic_form(d):
    return Matrix.diag(*(Matrix([[0, 1], [-1, 0]]) for _ in range(d)))


def kernel_generators(matrix, r):
    """Use integer Smith transformations to produce the exact mod-r^2 kernel."""
    if not isprime(r):
        raise ValueError("prime required")
    n = r*r
    matrix = mod(matrix, n)
    if matrix.rows != matrix.cols:
        raise ValueError("square matrix required")
    dm = DomainMatrix.from_Matrix(matrix).convert_to(ZZ)
    diagonal, left, right = smith_normal_decomp(dm)
    if diagonal != left*dm*right:
        raise AssertionError("Smith transformation identity failed")
    diagonal, right = diagonal.to_Matrix(), right.to_Matrix()
    columns, orders = [], []
    for i in range(matrix.cols):
        order = gcd(int(diagonal[i, i]), n)
        if order > 1:
            columns.append(mod((n//order)*right[:, i], n))
            orders.append(order)
    generators = Matrix.hstack(*columns) if columns else zeros(matrix.cols, 0)
    if mod(matrix*generators, n) != zeros(matrix.rows, generators.cols):
        raise AssertionError("kernel generator check failed")
    return generators, tuple(orders)


@dataclass
class PrimeSquareFlag:
    prime: int
    dimension: int
    generators: Matrix
    generator_orders: tuple
    multiplied_kernel: Matrix
    torsion_kernel: Matrix
    first_kernel: Matrix

    @property
    def free_rank(self):
        return self.generator_orders.count(self.prime**2)

    @property
    def first_kernel_points_in_source_coordinates(self):
        return self.prime*self.first_kernel

    def receipt(self):
        r, d = self.prime, self.dimension
        return {
            "prime": r, "dimension": d,
            "kernel_type": {"r_squared_factors": self.free_rank,
                            "r_factors": self.generator_orders.count(r)},
            "rG_dimension": self.multiplied_kernel.cols,
            "G_torsion_dimension": self.torsion_kernel.cols,
            "first_kernel_dimension": self.first_kernel.cols,
            "direct_kernel_list_size": str(r**(2*d)),
            "two_prime_kernel_lists_total_size": str(2*r**d),
            "second_quotient_order": str(r**d),
            "geometric_quotients_executed": False,
            "field_stability_requires_separate_check": True,
        }


def refine(matrix, r, pairing=None):
    matrix = integral(matrix)
    if matrix.rows != matrix.cols or matrix.rows % 2 or matrix.rows < 2:
        raise ValueError("nonempty even-dimensional square matrix required")
    if not isprime(r):
        raise ValueError("prime required")
    n, d = r*r, matrix.rows//2
    j = symplectic_form(d) if pairing is None else integral(pairing)
    if j.shape != matrix.shape or any(j[i, i] % n for i in range(2*d)):
        raise ValueError("alternating pairing required")
    if mod(j+j.T, n) != zeros(2*d) or gcd(int(j.det()), n) != 1:
        raise ValueError("perfect alternating pairing required")
    generators, orders = kernel_generators(matrix, r)
    if prod(orders) != r**(2*d):
        raise ValueError("kernel does not have maximal-isotropic order")
    if mod(generators.T*j*generators, n) != zeros(len(orders)):
        raise ValueError("kernel is not isotropic")

    free_columns = [generators[:, i] for i, order in enumerate(orders) if order == n]
    multiplied = basis(Matrix.hstack(*free_columns), r) if free_columns else zeros(2*d, 0)
    torsion = basis(Matrix.hstack(*(generators[:, i] if order == n else generators[:, i]/r
                                  for i, order in enumerate(orders))), r)
    orthogonal = basis(nullspace(multiplied.T*j, r), r)
    if torsion.cols != orthogonal.cols or not contained(torsion, orthogonal, r):
        raise AssertionError("G[r] differs from (rG)^perp")

    h = multiplied
    while h.cols < d:
        candidates = nullspace(h.T*j, r)
        candidate = next(candidates[:, i] for i in range(candidates.cols)
                         if not contained(candidates[:, i], h, r))
        h = h.row_join(candidate)
    h = basis(h, r)
    if not contained(multiplied, h, r) or not contained(h, torsion, r):
        raise AssertionError("flag inclusions failed")
    if mod(h.T*j*h, r) != zeros(d) or mod(matrix*(r*h), n) != zeros(2*d, d):
        raise AssertionError("first kernel is not an isotropic subgroup of G")
    return PrimeSquareFlag(int(r), d, generators, orders, multiplied, torsion, h)


def stable_under(h, frobenius, r):
    h, frobenius = integral(h), integral(frobenius)
    if frobenius.shape != (h.rows, h.rows) or int(frobenius.det()) % r == 0:
        raise ValueError("invertible Frobenius matrix required")
    return contained(frobenius*h, h, r)


def residual_quotient(flag, pairing=None):
    """Model the quotient Tate lattice; this does not construct a PPAV.

    If T spans r Z^(2d) + H, the first quotient lattice is (T/r) Z^(2d).
    Its integral alternating form is T^t J T/r. This independently checks
    that the image of G is a Lagrangian in the quotient's r-torsion.
    """
    r, d = flag.prime, flag.dimension
    j = symplectic_form(d) if pairing is None else integral(pairing)
    if j.shape != (2*d, 2*d):
        raise ValueError("pairing dimension mismatch")
    t = hermite_normal_form(integral((r*eye(2*d)).row_join(flag.first_kernel)))
    q = integral(r*t.inv())
    quotient_pairing = integral(t.T*j*t/r)
    residual = basis(integral(t.inv()*flag.generators), r)
    if q.T*quotient_pairing*q != r*j:
        raise AssertionError("first quotient polarization identity failed")
    if abs(int(quotient_pairing.det())) != 1:
        raise AssertionError("quotient lattice pairing is not unimodular")
    if residual.cols != d or mod(residual.T*quotient_pairing*residual, r) != zeros(d):
        raise AssertionError("residual kernel is not maximal isotropic")
    return {"quotient_matrix": q, "pairing": quotient_pairing,
            "residual_kernel": residual}


def scalar_torsion_extension(scalar, r):
    """Small-r exact order mod r^2; NOT an algorithm for large secret torsion."""
    if not isprime(r) or gcd(scalar, r) != 1:
        raise ValueError("prime and coprime scalar required")
    upper = r*(r-1)
    value = 1
    for degree in range(1, upper+1):
        value = value*scalar % (r*r)
        if value == 1:
            return degree
    raise AssertionError("Euler bound violated")
