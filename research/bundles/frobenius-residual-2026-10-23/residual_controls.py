"""Small integral/opaque-label controls, not geometric source execution."""

from itertools import product

from sympy import GF, Matrix, eye, zeros
from sympy.polys.matrices import DomainMatrix

from residual import mod
from controls import ArithmeticSource, unit
from kernel_output import action, alternating_form, odd_maximal_order, product_actions


def split_frobenius_fixture(rank):
    order = odd_maximal_order(11)
    j = Matrix([-1, 0, 2, 0])
    stable, unstable = Matrix([1, 0, 1, 0]), Matrix([1, 2, 0, 0])
    factors = [unstable if i < rank else stable for i in range(2)]
    phi = Matrix.vstack(factors[0], zeros(4, 1), zeros(4, 1), factors[1])
    gamma = Matrix.vstack(j, zeros(4, 1), zeros(4, 1), j)
    return ArithmeticSource(11, 5, order, phi, (gamma,))


def inert_stable_fixture():
    order = odd_maximal_order(7)
    j = Matrix([-1, 0, 2, 0])
    phi = Matrix.vstack(order.unit, 2 * order.unit, -2 * order.unit, order.unit)
    gamma = Matrix.vstack(j, zeros(4, 1), zeros(4, 1), j)
    return ArithmeticSource(7, 5, order, phi, (gamma,))


def incompatible_inert_pullback():
    order = odd_maximal_order(7)
    # q=7i+3j+3ij has norm 175, as does 5j. These are true integral
    # source maps with the Frobenius relation, but no valid neighbor exists.
    a = Matrix.vstack(Matrix([-3, 4, 6, 6]), zeros(4, 1), zeros(4, 1),
                      Matrix([-5, 0, 10, 0]))
    return order, a


def lagrangians(prime):
    if prime > 11:
        raise ValueError("exhaustive fixture is restricted to primes at most eleven")
    lines = [Matrix([1, 0])] + [Matrix([z, 1]) for z in range(prime)]
    for first in lines:
        for second in lines:
            k = zeros(4, 2)
            k[:2, 0], k[2:, 1] = first, second
            yield k
    for entries in product(range(prime), repeat=4):
        a = Matrix(2, 2, entries)
        if int(a.det()) % prime == prime - 1:
            yield eye(2).col_join(a)


def space_key(space, prime):
    reduced = DomainMatrix.from_Matrix(Matrix(space).T).convert_to(GF(prime)).rref()[0].to_Matrix()
    return tuple(int(x) % prime for x in reduced)


class OpaqueLabels:
    """Reference implementation of the ORIGINAL full Sp4 stabilizer oracle."""

    def __init__(self, kernel, prime):
        self._kernel, self._prime, self._labels = Matrix(kernel), prime, {}
        self.calls = 0

    def __call__(self, matrix):
        matrix = mod(matrix, self._prime)
        form = alternating_form(2)
        if mod(matrix.T * form * matrix - form, self._prime) != zeros(4):
            raise ValueError("query lies outside the original symplectic group")
        self.calls += 1
        key = space_key(matrix * self._kernel, self._prime)
        if key not in self._labels:
            self._labels[key] = f"opaque:{len(self._labels)}"
        return self._labels[key]
