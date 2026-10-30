"""Exact algebra controls for a recovered prime-to-characteristic kernel.

This does not recover K, construct torsion points, or run a quantum algorithm.
The generic routines consume an integral quaternion order and its specified
split action modulo ell. The Hurwitz example is an arithmetic fixture only.
"""

from dataclasses import dataclass
from itertools import combinations
from math import gcd

from sympy import Matrix, Rational, eye, isprime, zeros
from sympy.matrices.normalforms import hermite_normal_form


def mod(a, modulus):
    a = Matrix(a)
    if type(modulus) is not int or modulus < 2 or any(x.q != 1 for x in a):
        raise ValueError("integral matrix and integer modulus >= 2 required")
    return a.applyfunc(lambda x: int(x) % modulus)


def inverse_mod(a, modulus):
    """Unit-pivot elimination, with an adjugate fallback for composite levels."""
    a = Matrix(a)
    if a.rows != a.cols or any(x.q != 1 for x in a):
        raise ValueError("square integral matrix required")
    n = a.rows
    work = mod(a.row_join(eye(n)), modulus)
    for col in range(n):
        pivot = next((r for r in range(col, n)
                      if gcd(int(work[r, col]), modulus) == 1), None)
        if pivot is None:
            determinant = int(a.det())
            if gcd(determinant, modulus) != 1:
                raise ValueError("matrix is not invertible over the residue ring")
            return mod(pow(determinant, -1, modulus)*a.adjugate(), modulus)
        work.row_swap(col, pivot)
        work[col, :] = mod(work[col, :] * pow(int(work[col, col]), -1, modulus), modulus)
        for row in range(n):
            if row != col:
                work[row, :] = mod(work[row, :] - work[row, col] * work[col, :], modulus)
    return work[:, n:]


def flat(a):
    return Matrix(list(Matrix(a)))


def integer_matrix(a):
    a = Matrix(a)
    if any(x.q != 1 for x in a):
        raise ValueError("nonintegral matrix")
    return Matrix(a.rows, a.cols, [int(x) for x in a])


def coordinate_map(actions):
    return Matrix.hstack(*(flat(a) for a in actions))


def action(coefficients, actions):
    result = zeros(*actions[0].shape)
    for coefficient, image in zip(coefficients, actions):
        result += coefficient * image
    return result


@dataclass
class QuaternionOrder:
    products: tuple
    unit: Matrix
    involution: Matrix
    traces: Matrix

    def multiply(self, x, y):
        out = zeros(4, 1)
        for i in range(4):
            for j in range(4):
                if x[i] and y[j]:
                    out += x[i] * y[j] * self.products[i][j]
        return out

    def star(self, x):
        return self.involution * Matrix(x)


def _quaternion_order(change, p):
    inv = change.inv()

    def multiply(x, y):
        w, a, b, c = x
        z, d, e, f = y
        return Matrix([w*z-a*d-p*b*e-p*c*f, w*d+a*z+p*b*f-p*c*e,
                       w*e-a*f+b*z+c*d, w*f+a*e-b*d+c*z])

    products = tuple(tuple(inv * multiply(change[:, i], change[:, j])
                           for j in range(4)) for i in range(4))
    return QuaternionOrder(products, Matrix([1, 0, 0, 0]),
                           inv * Matrix.diag(1, -1, -1, -1) * change,
                           Matrix([[2, 0, 0, 0]])*change)


def hurwitz_order():
    """The full maximal order Z[1,i,j,(1+i+j+ij)/2] in (-1,-1)."""
    change = Matrix([[1, 0, 0, Rational(1, 2)], [0, 1, 0, Rational(1, 2)],
                     [0, 0, 1, Rational(1, 2)], [0, 0, 0, Rational(1, 2)]])
    return _quaternion_order(change, 1)


def odd_maximal_order(p):
    """Z[1,i,(1+j)/2,(i+ij)/2] in (-1,-p), p prime = 3 mod 4."""
    if not isprime(p) or p % 4 != 3:
        raise ValueError("prime characteristic = 3 mod 4 required")
    change = Matrix([[1, 0, Rational(1, 2), 0], [0, 1, 0, Rational(1, 2)],
                     [0, 0, Rational(1, 2), 0], [0, 0, 0, Rational(1, 2)]])
    return _quaternion_order(change, p)


def odd_maximal_split(p, ell):
    """Small-prime fixture only; generic algorithms take the split as input."""
    odd_maximal_order(p)
    if not isprime(ell) or ell in (2, p):
        raise ValueError("odd unramified prime required")
    a, b = next((a, b) for a in range(ell) for b in range(ell)
                if (a*a+b*b+p) % ell == 0)
    i, j = Matrix([[0, -1], [1, 0]]), Matrix([[a, b], [b, -a]])
    h = (eye(2)+j)*pow(2, -1, ell)
    return tuple(mod(x, ell) for x in (eye(2), i, h, i*h))


def hurwitz_split(ell):
    """Small-prime fixture; the search for a,b is NOT a polylog algorithm."""
    if not isprime(ell) or ell == 2:
        raise ValueError("odd unramified prime required")
    a, b = next((a, b) for a in range(ell) for b in range(ell)
                if (a*a+b*b+1) % ell == 0)
    i = Matrix([[0, -1], [1, 0]])
    j = Matrix([[a, b], [b, -a]])
    h = (eye(2)+i+j+i*j) * pow(2, -1, ell)
    return tuple(mod(x, ell) for x in (eye(2), i, j, h))


def check_split(order, actions, modulus):
    if len(actions) != 4 or any(Matrix(a).shape != (2, 2) for a in actions):
        raise ValueError("four 2 by 2 action matrices required")
    inverse_mod(coordinate_map(actions), modulus)
    if mod(action(order.unit, actions)-eye(2), modulus) != zeros(2):
        raise ValueError("unit is not preserved")
    j = Matrix([[0, 1], [-1, 0]])
    for i in range(4):
        if mod(action(order.star(eye(4)[:, i]), actions)
               - j.inv()*actions[i].T*j, modulus) != zeros(2):
            raise ValueError("quaternion involution is not preserved")
        for k in range(4):
            if mod(action(order.products[i][k], actions)-actions[i]*actions[k], modulus) != zeros(2):
                raise ValueError("multiplication is not preserved")


def lift_split(order, actions, ell, idempotent_lift_shift=None):
    """Lift a supplied split O/ell to O/ell^2 using a rank-one idempotent."""
    if not isprime(ell) or ell == 2:
        raise ValueError("odd prime required")
    check_split(order, actions, ell)
    inverse = inverse_mod(coordinate_map(actions), ell)
    e0 = mod(inverse * Matrix([1, 0, 0, 0]), ell)
    if idempotent_lift_shift is not None:
        shift = Matrix(idempotent_lift_shift)
        if shift.shape != (4, 1) or any(x.q != 1 for x in shift):
            raise ValueError("integral idempotent lift shift required")
        e0 += ell * shift
    modulus = ell*ell
    square = order.multiply(e0, e0)
    e = mod(3*square-2*order.multiply(square, e0), modulus)
    if mod(order.multiply(e, e)-e, modulus) != zeros(4, 1):
        raise ValueError("idempotent lift failed")
    e21 = mod(inverse * Matrix([0, 0, 1, 0]), ell)
    module = Matrix.hstack(e, mod(order.multiply(e21, e), modulus))
    rows = next(indices for indices in combinations(range(4), 2)
                if int(module[list(indices), :].det()) % ell)
    minor_inverse = inverse_mod(module[list(rows), :], modulus)
    lifted = []
    for i in range(4):
        image = Matrix.hstack(*(order.multiply(eye(4)[:, i], module[:, c]) for c in range(2)))
        coefficients = mod(minor_inverse * image[list(rows), :], modulus)
        if mod(module*coefficients-image, modulus) != zeros(4, 2):
            raise ValueError("left ideal does not carry the proposed action")
        lifted.append(coefficients)
    result = tuple(lifted)
    if any(mod(a-b, ell) != zeros(2) for a, b in zip(result, actions)):
        raise ValueError("lift changed the specified mod-ell coordinates")
    check_split(order, result, modulus)
    return result


def product_actions(actions, g=2):
    result = []
    for row in range(g):
        for col in range(g):
            for a in actions:
                out = zeros(2*g)
                out[2*row:2*row+2, 2*col:2*col+2] = a
                result.append(out)
    return tuple(result)


def column_actions(actions, g=2):
    result = []
    for row in range(g):
        for a in actions:
            out = zeros(2*g, 2)
            out[2*row:2*row+2, :] = a
            result.append(out)
    return tuple(result)


def adapted_basis(kernel, ell):
    kernel = Matrix(kernel)
    g = kernel.cols
    if not isprime(ell) or ell == 2 or kernel.rows != 2*g or g < 1:
        raise ValueError("a half-dimensional kernel at an odd prime is required")
    if any(x.q != 1 for x in kernel):
        raise ValueError("kernel coordinates must be integral residues")
    n = 2*g
    for indices in combinations(range(n), g):
        candidate = mod(kernel.row_join(eye(n)[:, list(indices)]), ell)
        if int(candidate.det()) % ell:
            return candidate
    raise ValueError("kernel columns must be independent modulo ell")


def alternating_form(g):
    return Matrix.diag(*(Matrix([[0, 1], [-1, 0]]) for _ in range(g)))


def is_lagrangian(kernel, ell):
    kernel = Matrix(kernel)
    adapted_basis(kernel, ell)
    return mod(kernel.T*alternating_form(kernel.cols)*kernel, ell) == zeros(kernel.cols)


def _preimage_lattice(map_matrix, allowed, modulus):
    inverse = inverse_mod(map_matrix, modulus)
    lifts = [mod(inverse*flat(a), modulus) for a in allowed]
    rank = map_matrix.cols
    return hermite_normal_form(Matrix.hstack(*lifts, modulus*eye(rank)))


@dataclass
class KernelOutput:
    ell: int
    g: int
    module_numerator: Matrix
    order_numerator: Matrix
    split_squared: tuple

    @property
    def module_basis(self):
        return self.module_numerator/self.ell

    @property
    def order_basis(self):
        return self.order_numerator/self.ell

    def contains_module(self, vector):
        return all(x.q == 1 for x in self.module_basis.inv()*Matrix(vector))

    def contains_order(self, vector):
        return all(x.q == 1 for x in self.order_basis.inv()*Matrix(vector))


def reconstruct(order, split, kernel, ell, *, require_lagrangian=True,
                split_squared=None, complement=None):
    """Return full congruence lattices, conditional on the geometric inputs."""
    kernel = Matrix(kernel)
    p = adapted_basis(kernel, ell)
    g = kernel.cols
    if require_lagrangian and not is_lagrangian(kernel, ell):
        raise ValueError("the polarized source requires a Lagrangian kernel")
    if complement is not None:
        complement = Matrix(complement)
        if complement.shape != kernel.shape or any(x.q != 1 for x in complement):
            raise ValueError("an integral complementary basis is required")
        p = kernel.row_join(complement)
        inverse_mod(p, ell)
    lifted = lift_split(order, split, ell) if split_squared is None else tuple(split_squared)
    check_split(order, lifted, ell*ell)
    if any(mod(a-b, ell) != zeros(2) for a, b in zip(lifted, split)):
        raise ValueError("incompatible splitting lift")

    # J consists of O^g columns whose mod-ell image is contained in K.
    allowed_columns = []
    for row in range(g):
        for col in range(2):
            a = zeros(2*g, 2)
            a[row, col] = 1
            allowed_columns.append(mod(p*a, ell))
    module = _preimage_lattice(coordinate_map(column_actions(split, g)), allowed_columns, ell)

    # a/ell preserves Lambda + K/ell iff A,D=0 mod ell and C=0 mod ell^2.
    pinverse = inverse_mod(p, ell*ell)
    allowed_matrices = []
    for row in range(2*g):
        for col in range(2*g):
            if row >= g and col < g:
                continue
            a = zeros(2*g)
            a[row, col] = 1 if row < g <= col else ell
            allowed_matrices.append(mod(p*a*pinverse, ell*ell))
    end_order = _preimage_lattice(coordinate_map(product_actions(lifted, g)),
                                 allowed_matrices, ell*ell)
    return KernelOutput(ell, g, module, end_order, lifted)


def module_pairing(order, x, y, multiplier):
    x, y = Matrix(x), Matrix(y)
    out = zeros(4, 1)
    for row in range(len(x)//4):
        out += order.multiply(order.star(x[4*row:4*row+4, :]), y[4*row:4*row+4, :])
    return multiplier*out


def matrix_star(order, x, g=2):
    x = Matrix(x)
    return Matrix.vstack(*(order.star(x[4*(j*g+i):4*(j*g+i+1), :])
                           for i in range(g) for j in range(g)))


def matrix_on_column(order, x, vector, g=2):
    x, vector = Matrix(x), Matrix(vector)
    blocks = []
    for i in range(g):
        block = zeros(4, 1)
        for j in range(g):
            block += order.multiply(x[4*(i*g+j):4*(i*g+j+1), :], vector[4*j:4*j+4, :])
        blocks.append(block)
    return Matrix.vstack(*blocks)


def matrix_multiply(order, x, y, g=2):
    x, y = Matrix(x), Matrix(y)
    blocks = []
    for i in range(g):
        for j in range(g):
            block = zeros(4, 1)
            for k in range(g):
                block += order.multiply(x[4*(i*g+k):4*(i*g+k+1), :],
                                        y[4*(k*g+j):4*(k*g+j+1), :])
            blocks.append(block)
    return Matrix.vstack(*blocks)


def order_from_module(order, module_numerator, ell):
    """Independent reconstruction, using multiplication in O, no ell^2 split.

    The integral congruences F*a=0 mod ell^2 express that a/ell preserves
    J/ell. Their kernel is the dual of Z^r + (F^t/ell^2)Z^m.
    """
    j = integer_matrix(module_numerator)
    g = j.rows//4
    if not isprime(ell) or ell == 2 or j.rows != j.cols or j.rows != 4*g or g < 1:
        raise ValueError("full column-module lattice and odd prime required")
    ji = j.inv()
    if not integral_matrix_test(ell*ji):
        raise ValueError("module numerator must contain ell*O^g")
    columns = []
    for a in range(4*g*g):
        left = Matrix.hstack(*(matrix_on_column(order, eye(4*g*g)[:, a], eye(4*g)[:, b], g)
                               for b in range(4*g)))
        columns.append(flat(integer_matrix(ell*ji*left*j)))
    constraints = Matrix.hstack(*columns)
    rank, modulus = constraints.cols, ell*ell
    dual_numerator = hermite_normal_form(integer_matrix((modulus*eye(rank)).row_join(constraints.T)))
    return hermite_normal_form(integer_matrix(modulus*dual_numerator.inv().T))


def integral_matrix_test(a):
    return all(x.q == 1 for x in Matrix(a))


def weak_endomorphism_action(a_action, weak_phi_action, ell, modulus):
    """beta = phi*(a/ell)*phi^-1 on auxiliary torsion, with common unit mask."""
    if gcd(ell, modulus) != 1:
        raise ValueError("auxiliary level must be coprime to ell")
    return mod(pow(ell, -1, modulus)*weak_phi_action*a_action
               *inverse_mod(weak_phi_action, modulus), modulus)
