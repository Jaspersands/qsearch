"""Integral quaternion fixtures, explicitly not executed surface geometry."""

from dataclasses import dataclass, field

from sympy import Matrix, eye, zeros

from pullback import ResiduePacket, matrix_multiply, matrix_star, mod, source_gram
from kernel_output import action, odd_maximal_order, odd_maximal_split, product_actions


@dataclass
class ArithmeticSource:
    characteristic: int
    ell: int
    order: object
    phi: Matrix
    gammas: tuple
    calls: list = field(default_factory=list)

    def split(self, prime):
        # This enumerative fixture is called only at the declared small
        # levels. It is not a large-prime splitting implementation.
        return odd_maximal_split(self.characteristic, prime)

    def observe(self, prime):
        self.calls.append(prime)
        actions = product_actions(self.split(prime))
        frame = eye(4)
        frame[0, 1], frame[2, 3] = 2, 3
        inverse = frame.inv()
        mask = 2 if prime > 3 else prime - 1
        weak = mod(mask * inverse * action(self.phi, actions), prime)
        maps = tuple(mod(inverse * action(gamma, actions) * frame, prime) for gamma in self.gammas)
        return ResiduePacket(weak, maps)

    def norms(self):
        gram = source_gram(self.order)
        return tuple(int((x.T * gram * x)[0]) for x in self.gammas)

    def reference_pullbacks(self):
        return tuple(matrix_multiply(self.order, matrix_multiply(
            self.order, matrix_star(self.order, self.phi), gamma), self.phi)
                     for gamma in self.gammas)

    def levels(self):
        return tuple(x for x in (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47)
                     if x not in (self.characteristic, self.ell))


def word_fixture():
    order = odd_maximal_order(11)
    phi = Matrix.vstack(order.unit, 2 * order.unit, -2 * order.unit, order.unit)
    gamma = Matrix([0, 1, 0, 0, -1, -1, 0, 0, -1, 1, 1, -1, 1, 0, -1, -1])
    return ArithmeticSource(11, 5, order, phi, (gamma,))


def frobenius_relation_fixture(mixed_factors):
    if mixed_factors not in (0, 1, 2):
        raise ValueError("zero, one or two noncommuting factors required")
    order = odd_maximal_order(7)
    j, ij = Matrix([-1, 0, 2, 0]), Matrix([0, -1, 0, 2])
    factors = [2 * order.unit + (ij if i < mixed_factors else j) for i in range(2)]
    phi = Matrix.vstack(factors[0], zeros(4, 1), zeros(4, 1), factors[1])
    gamma = Matrix.vstack(j, zeros(4, 1), zeros(4, 1), j)
    return ArithmeticSource(7, 11, order, phi, (gamma,))


def unit(order):
    return Matrix.vstack(order.unit, zeros(4, 1), zeros(4, 1), order.unit)
