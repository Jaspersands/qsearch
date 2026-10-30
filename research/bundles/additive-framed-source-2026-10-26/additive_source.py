"""Exact certificates for an UNREVIEWED framed-polarization HSP proposal.

No theta quotient, native label, unknown order recovery or quantum source is
implemented. Quaternion-order fixtures provide exact algebra controls only.
"""

from dataclasses import dataclass
from math import isqrt
from pathlib import Path
import sys

from sympy import Matrix, eye, kronecker_product, zeros
from sympy.matrices.normalforms import hermite_normal_form

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "kernel-output-2026-10-23"))
from kernel_output import QuaternionOrder


@dataclass(frozen=True)
class QMatrix:
    """Four coefficient matrices in the supplied quaternion-order basis."""
    coefficients: tuple

    def __post_init__(self):
        if len(self.coefficients) != 4 or not self.coefficients[0].rows:
            raise ValueError("four nonempty rational coefficient matrices required")
        shape = self.coefficients[0].shape
        if any(a.shape != shape or any(x.is_Rational is not True for x in a)
               for a in self.coefficients):
            raise ValueError("matching rational coefficient matrices required")

    @property
    def shape(self):
        return self.coefficients[0].shape

    @property
    def integral(self):
        return all(x.q == 1 for a in self.coefficients for x in a)

    def __add__(self, other):
        return QMatrix(tuple(a+b for a, b in zip(self.coefficients, other.coefficients)))

    def __sub__(self, other):
        return QMatrix(tuple(a-b for a, b in zip(self.coefficients, other.coefficients)))

    def scale(self, scalar):
        return QMatrix(tuple(scalar*a for a in self.coefficients))

    def repeat(self, copies):
        return QMatrix(tuple(kronecker_product(eye(copies), a) for a in self.coefficients))


def scalar_matrix(order, matrix):
    return QMatrix(tuple(c*Matrix(matrix) for c in order.unit))


def quaternion_matrix(rows):
    return QMatrix(tuple(Matrix([[Matrix(x)[i] for x in row] for row in rows]) for i in range(4)))


def blocks(a, b, c, d):
    return QMatrix(tuple(x.row_join(y).col_join(z.row_join(w))
                         for x, y, z, w in zip(a.coefficients, b.coefficients,
                                              c.coefficients, d.coefficients)))


def multiply(order, left, right):
    rows, inner = left.shape
    if right.shape[0] != inner:
        raise ValueError("incompatible matrix dimensions")
    result = [zeros(rows, right.shape[1]) for _ in range(4)]
    for i, a in enumerate(left.coefficients):
        if a.is_zero_matrix:
            continue
        for j, b in enumerate(right.coefficients):
            if b.is_zero_matrix:
                continue
            product = a*b
            for k, coefficient in enumerate(order.products[i][j]):
                if coefficient:
                    result[k] += coefficient*product
    return QMatrix(tuple(result))


def adjoint(order, matrix):
    return QMatrix(tuple(sum((order.involution[k, i]*a.T
                              for i, a in enumerate(matrix.coefficients)),
                             zeros(matrix.shape[1], matrix.shape[0])) for k in range(4)))


def norm(order, vector):
    return (order.traces*order.multiply(vector, order.star(vector)))[0]/2


def four_square_matrix(roots):
    if len(roots) != 4 or any(type(x) is not int for x in roots):
        raise ValueError("four integer roots required")
    a, b, c, d = roots
    return Matrix([[a, -b, -c, -d], [b, a, -d, c],
                   [c, d, a, -b], [d, -c, b, a]])


def construct(order, beta, denominator, roots):
    if type(denominator) is not int or denominator < 2:
        raise ValueError("denominator >=2 required; index one needs no HSP")
    beta = Matrix(beta)
    if beta.shape != (4, 1) or any(x.is_Integer is not True for x in beta):
        raise ValueError("integral numerator coordinates required")
    n = denominator
    t4 = four_square_matrix(roots)
    if sum(x*x for x in roots) != n**4-1:
        raise ValueError("wrong fixed four-square norm")
    degree = norm(order, beta)
    if degree.is_Integer is not True or degree < 0 or (degree == 0 and beta != zeros(4, 1)):
        raise ValueError("positive definite integral norm required")
    one = order.unit
    small = quaternion_matrix([[n*n*one, n*beta],
                               [n*order.star(beta), (n*n+degree)*one]])
    trace = int(2*n*n+degree)
    small_adjugate = scalar_matrix(order, trace*eye(2))-small
    cross = scalar_matrix(order, kronecker_product(t4, eye(2)))
    z = blocks(small.repeat(4), cross, adjoint(order, cross), small_adjugate.repeat(4))
    return {"polarization": z, "small": small, "small_adjugate": small_adjugate,
            "cross": cross, "trace": trace, "degree": int(degree),
            "denominator": n, "roots": roots}


def shear(order, delta):
    delta = Matrix(delta)
    if delta.shape != (4, 1):
        raise ValueError("four quaternion coordinates required")
    zero, one = zeros(4, 1), order.unit
    w = quaternion_matrix([[one, delta], [zero, one]])
    inverse_adjoint = quaternion_matrix([[one, zero], [-order.star(delta), one]])
    null = scalar_matrix(order, zeros(8))
    return blocks(w.repeat(4), null, null, inverse_adjoint.repeat(4))


def block_isometry(order, w, v, multiplicity=4):
    left, right = w.repeat(multiplicity), v.repeat(multiplicity)
    null = scalar_matrix(order, zeros(2*multiplicity))
    return blocks(left, null, null, right)


def frame_operators(multiplicity):
    """Scalar frame. After eightfold stabilization use multiplicity=32."""
    if type(multiplicity) is not int or multiplicity < 1:
        raise ValueError("positive multiplicity required")
    half = 2*multiplicity
    operators = []
    for block in range(2):
        for i in range(multiplicity):
            for j in range(multiplicity):
                unit = zeros(multiplicity)
                unit[i, j] = 1
                value = zeros(2*half)
                value[block*half:(block+1)*half, block*half:(block+1)*half] = kronecker_product(unit, eye(2))
                operators.append(value)
    return tuple(operators)


def fixes_inclusions(order, matrix, multiplicity=4):
    dimension = 4*multiplicity
    inclusions = eye(dimension)[:, [0, 2*multiplicity+1]]
    fixed = scalar_matrix(order, inclusions)
    return multiply(order, matrix, fixed) == fixed


def input_index(order, characteristic):
    """Native geometric provenance and characteristic are external promises."""
    if type(characteristic) is not int or characteristic <= 3:
        raise ValueError("declared characteristic greater than three required")
    basis = [eye(4)[:, i] for i in range(4)]
    gram = Matrix(4, 4, lambda i, j:
                  (order.traces*order.multiply(basis[i], order.star(basis[j])))[0])
    determinant = gram.det()
    if determinant.is_Integer is not True or determinant <= 0:
        raise ValueError("positive integer discriminant required")
    root = isqrt(int(determinant))
    if root*root != determinant or root % characteristic:
        raise ValueError("discriminant does not match p^2*d^2")
    return root//characteristic


def candidate_lattice(generators, index):
    """Index-checked CANDIDATE in R coordinates; native division is still needed."""
    if type(index) is not int or index < 2:
        raise ValueError("index >=2 required")
    columns = []
    for value in generators:
        value = Matrix(value)
        if value.shape != (4, 1) or any(x.is_Integer is not True for x in value):
            raise ValueError("four integer coordinates per subgroup generator required")
        columns.append(value)
    lattice = hermite_normal_form(Matrix.hstack(index*eye(4), *columns))
    if lattice.det() != index**3:
        raise ValueError("candidate subgroup has the wrong order")
    return lattice/index


def uniform_plan(index, basis_degree_bound):
    if type(index) is not int or index < 2 or type(basis_degree_bound) is not int or basis_degree_bound < 1:
        raise ValueError("index >=2 and positive degree bound required")
    dimension = 128
    trace = (2+16*basis_degree_bound)*index**2
    return {
        "query_group_rank": 4, "query_modulus": index,
        "query_count_domain": index**4, "hidden_subgroup_order": index,
        "initial_polarization_dimension": 16, "stabilized_dimension": dimension,
        "frame_operator_count": 2*32**2,
        "theta_coordinates_per_point": 4**dimension,
        "fixed_inclusion_points_per_prime": 4,
        "trace_bound": trace,
        "marking_product_squared_must_exceed": 8*dimension*trace**2,
        "graph_points_per_prime_exponent": 2*dimension,
        "direct_prime_square_kernel_points_exponent": 2*dimension,
        "refined_prime_kernel_points_exponent": dimension,
        "native_geometric_label_executed": False,
    }
