"""Exact public algebra for a large-prime abelian-action normalizer.

This is NOT a black-box group or quantum HSP implementation. The input is
the already acquired action on an explicitly decomposed abelian p-group.
See ABELIAN_ACTION_NORMALIZER.md for the paid input and lifting obligations.
"""

from dataclasses import dataclass
from math import prod

from flint import fmpz, fmpz_mat


def _rows(matrix):
    return tuple(tuple(int(matrix[i, j]) for j in range(matrix.ncols()))
                 for i in range(matrix.nrows()))


def _lattice(moduli, generators):
    """Full-rank inverse-image lattice of a finite additive subgroup."""
    d = len(moduli)
    rows = []
    for row in generators:
        if len(row) != d:
            raise ValueError("wrong generator dimension")
        rows.append([int(x) % m for x, m in zip(row, moduli)])
    rows.extend([[m if i == j else 0 for j in range(d)]
                 for i, m in enumerate(moduli)])
    h = fmpz_mat(rows).hnf()
    nonzero = [row for row in _rows(h) if any(row)]
    if len(nonzero) != d:
        raise ArithmeticError("inverse-image lattice lost full rank")
    return tuple(nonzero)


def _generators(moduli, lattice):
    return tuple(row for raw in lattice
                 if any(row := tuple(x % m for x, m in zip(raw, moduli))))


def _order(moduli, lattice):
    return prod(moduli) // abs(int(fmpz_mat(lattice).det()))


@dataclass(frozen=True)
class StabilizerResult:
    action_log_generators: tuple
    stabilizer_log_generators: tuple
    stabilizer_group_generators: tuple
    action_order: int
    stabilizer_order: int
    status: str = "EXACT_PUBLIC_ACTION_STABILIZER"


class AbelianAction:
    """Endomorphisms of direct_sum_i Z/(p**exponents[i]), acting on columns."""

    def __init__(self, prime, exponents):
        self.p = int(prime)
        self.exponents = tuple(int(e) for e in exponents)
        if not fmpz(self.p).is_prime():
            raise ValueError("prime must be prime")
        if not self.exponents or any(e <= 0 for e in self.exponents):
            raise ValueError("nonempty positive exponents required")
        self.length = sum(self.exponents)
        if self.p <= self.length:
            raise ValueError("this backend requires p > log_p(|A|)")
        self.rank = len(self.exponents)
        self.moduli = tuple(self.p**e for e in self.exponents)
        self.end_moduli = tuple(self.p**min(ei, ej)
                                for ei in self.exponents for ej in self.exponents)
        self.scales = tuple(self.p**max(ei - ej, 0)
                            for ei in self.exponents for ej in self.exponents)
        self.zero = tuple((0,) * self.rank for _ in self.exponents)
        self.identity = tuple(tuple(int(i == j) for j in range(self.rank))
                              for i in range(self.rank))

    def matrix(self, values):
        if len(values) != self.rank or any(len(row) != self.rank for row in values):
            raise ValueError("wrong matrix shape")
        out = tuple(tuple(int(x) % self.moduli[i] for x in row)
                    for i, row in enumerate(values))
        for i, row in enumerate(out):
            for j, x in enumerate(row):
                if x % self.p**max(self.exponents[i] - self.exponents[j], 0):
                    raise ValueError("matrix is not an endomorphism of the mixed module")
        return out

    def encode(self, matrix):
        matrix = self.matrix(matrix)
        return tuple(x // scale for x, scale in
                     zip((x for row in matrix for x in row), self.scales))

    def decode(self, coefficients):
        if len(coefficients) != self.rank**2:
            raise ValueError("wrong endomorphism coordinate count")
        flat = [int(x) % m * scale for x, m, scale in
                zip(coefficients, self.end_moduli, self.scales)]
        return self.matrix([flat[i*self.rank:(i+1)*self.rank]
                            for i in range(self.rank)])

    def add(self, x, y):
        return self.matrix([[x[i][j] + y[i][j] for j in range(self.rank)]
                            for i in range(self.rank)])

    def scale(self, scalar, x):
        return self.matrix([[int(scalar) * a for a in row] for row in x])

    def multiply(self, x, y):
        return self.matrix([[sum(x[i][k] * y[k][j] for k in range(self.rank))
                             for j in range(self.rank)] for i in range(self.rank)])

    def apply(self, x, vector):
        if len(vector) != self.rank:
            raise ValueError("wrong vector dimension")
        return tuple(sum(x[i][j] * int(vector[j]) for j in range(self.rank))
                     % self.moduli[i] for i in range(self.rank))

    def bracket(self, x, y):
        return self.add(self.multiply(x, y), self.scale(-1, self.multiply(y, x)))

    def _additive_basis(self, matrices):
        lattice = _lattice(self.end_moduli, [self.encode(x) for x in matrices])
        return lattice, tuple(self.decode(x) for x in
                              _generators(self.end_moduli, lattice))

    def certify_action(self, generators):
        """Check ALL products of a differences vanish, not only each power."""
        generators = tuple(self.matrix(g) for g in generators)
        differences = tuple(self.add(g, self.scale(-1, self.identity))
                            for g in generators)
        _, layer = self._additive_basis(differences)
        for _ in range(1, self.length):
            _, layer = self._additive_basis(
                [self.multiply(x, y) for x in layer for y in differences])
        if layer:
            raise ValueError("joint augmentation products do not vanish at module length")
        return generators

    def logarithm(self, g):
        x = self.add(self.matrix(g), self.scale(-1, self.identity))
        power, total = self.identity, self.zero
        modulus = max(self.moduli)
        for j in range(1, self.length):
            power = self.multiply(power, x)
            coefficient = (-1)**(j + 1) * pow(j, -1, modulus)
            total = self.add(total, self.scale(coefficient, power))
        if self.multiply(power, x) != self.zero:
            raise ValueError("difference is not nilpotent at module length")
        return total

    def exponential(self, x):
        x = self.matrix(x)
        power, total, coefficient = self.identity, self.identity, 1
        modulus = max(self.moduli)
        for j in range(1, self.length):
            power = self.multiply(power, x)
            coefficient = coefficient * pow(j, -1, modulus) % modulus
            total = self.add(total, self.scale(coefficient, power))
        if self.multiply(power, x) != self.zero:
            raise ValueError("logarithm is not nilpotent at module length")
        return total

    def lie_closure(self, generators):
        generators = self.certify_action(generators)
        lattice, basis = self._additive_basis([self.logarithm(g) for g in generators])
        # Every strict enlargement increases order by at least p.
        for _ in range(sum(min(ei, ej) for ei in self.exponents
                           for ej in self.exponents) + 1):
            next_lattice, next_basis = self._additive_basis(
                list(basis) + [self.bracket(x, y) for i, x in enumerate(basis)
                               for y in basis[i+1:]])
            if next_lattice == lattice:
                return lattice, basis
            lattice, basis = next_lattice, next_basis
        raise ArithmeticError("additive closure exceeded its strict-growth bound")

    def preserves(self, matrix, subgroup_generators):
        """Containment only; equality follows for certified automorphisms."""
        generators = tuple(tuple(int(x) for x in v) for v in subgroup_generators)
        lattice = _lattice(self.moduli, generators)
        return _lattice(self.moduli, generators + tuple(
            self.apply(matrix, v) for v in generators)) == lattice

    def stabilizer(self, generators, subgroup_generators):
        """Generate the action-group setwise stabilizer of the supplied K."""
        lattice, basis = self.lie_closure(generators)
        k_lattice = _lattice(self.moduli, subgroup_generators)
        k_basis = _generators(self.moduli, k_lattice)
        if not basis or not k_basis:
            stable_lattice, stable_basis = lattice, basis
        else:
            # X*K <= K is an integer congruence system. Unimodular HNF zero
            # rows generate its FULL integer relation lattice; a rational
            # nullspace with denominators cleared need not be saturated.
            width = self.rank * len(k_basis)
            rows = [tuple(v for k in k_basis for v in self.apply(x, k))
                    for x in basis]
            for block in range(len(k_basis)):
                for k in k_basis:
                    row = [0] * width
                    row[block*self.rank:(block+1)*self.rank] = [-x for x in k]
                    rows.append(tuple(row))
            output_moduli = self.moduli * len(k_basis)
            rows.extend(tuple(m if i == j else 0 for j in range(width))
                        for i, m in enumerate(output_moduli))
            h, transform = fmpz_mat(rows).hnf(transform=True)
            candidates = []
            for i, row in enumerate(_rows(h)):
                if any(row):
                    continue
                x = self.zero
                for j, b in enumerate(basis):
                    x = self.add(x, self.scale(int(transform[i, j]), b))
                candidates.append(x)
            stable_lattice, stable_basis = self._additive_basis(candidates)
        group_basis = tuple(self.exponential(x) for x in stable_basis)
        if not all(self.preserves(g, k_basis) for g in group_basis):
            raise ArithmeticError("returned action failed native subgroup preservation")
        return StabilizerResult(
            basis, stable_basis, group_basis,
            _order(self.end_moduli, lattice),
            _order(self.end_moduli, stable_lattice),
        )
