"""Public Lie-algebra reduction for a bounded-codimension HSP hypothesis.

No hidden-intersection learner or quantum receiver is implemented. A step
requires the EXACT intersection with its public abelian ideal, not merely
some verified elements of the hidden subgroup. Public checks cannot certify
that unknown-source promise. All arithmetic reuses existing exact helpers.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

from theorems.symbolic_scalar_phase_erasure import (
    PublicLieAlgebra,
    _canonical_vec,
    _fmpz_nullspace_basis,
    _fmpz_solve_coordinates,
)


def units(n):
    return tuple(tuple(int(i == j) for j in range(n)) for i in range(n))


def combine(coefficients, basis, width, p):
    coefficients = tuple(coefficients)
    if len(coefficients) != len(basis) or any(
        type(x) is not int or not 0 <= x < p for x in coefficients
    ):
        raise ValueError("canonical coordinates of the declared width required")
    return tuple(sum(a * row[j] for a, row in zip(coefficients, basis)) % p
                 for j in range(width))


def contains(basis, vector, p):
    return _fmpz_solve_coordinates(basis, vector, p) is not None


def _from_tensor(p, n, tensor):
    sparse = tuple((i, j, tuple((k, v) for k, v in enumerate(row) if v))
                   for (i, j), row in tensor.items() if any(row))

    def bracket(left, right):
        output = [0] * n
        for i, j, row in sparse:
            weight = left[i] * right[j] % p
            for k, v in row:
                output[k] += weight * v
        return tuple(x % p for x in output)

    return PublicLieAlgebra(p, n, bracket)


def freeze_lazard_algebra(algebra):
    """Interpret a callback through basis constants, then validate that table.

    This does not certify that an arbitrary external callback is bilinear.
    Every subsequent operation uses the frozen bilinear reconstruction.
    """
    p, n = algebra.p, algebra.dimension
    if p == 2:
        raise ValueError("this interface requires an odd prime")
    basis = units(n)
    tensor = {(i, j): algebra.bracket(a, b)
              for i, a in enumerate(basis) for j, b in enumerate(basis)}
    for i in range(n):
        if any(tensor[i, i]):
            raise ValueError("nonalternating structure table")
        for j in range(n):
            if any((x + y) % p for x, y in zip(tensor[i, j], tensor[j, i])):
                raise ValueError("nonantisymmetric structure table")
    frozen = _from_tensor(p, n, tensor)
    for i, j, k in combinations(range(n), 3):
        terms = [frozen.bracket(basis[a], tensor[b, c])
                 for a, b, c in ((i, j, k), (j, k, i), (k, i, j))]
        if any(sum(row[t] for row in terms) % p for t in range(n)):
            raise ValueError("Jacobi identity failed")
    nilpotency_class = frozen.nilpotency_class(basis)
    if nilpotency_class >= p:
        raise ValueError("Lazard input requires nilpotency class below p")
    return frozen, nilpotency_class


def _constraint_rows(algebra, right_vectors, output_space):
    """Linear conditions [x,v] in output_space for every supplied v."""
    p, n = algebra.p, algebra.dimension
    annihilator = _fmpz_nullspace_basis(output_space, n, p)
    basis = units(n)
    rows = []
    for v in right_vectors:
        columns = [algebra.bracket(e, v) for e in basis]
        rows.extend(tuple(sum(a * b for a, b in zip(functional, column)) % p
                          for column in columns) for functional in annihilator)
    return rows


def centralizer(algebra, subspace):
    basis = algebra.span(subspace)
    return tuple(_fmpz_nullspace_basis(
        _constraint_rows(algebra, basis, ()), algebra.dimension, algebra.p))


def normalizer(algebra, subspace):
    basis = algebra.span(subspace)
    return tuple(_fmpz_nullspace_basis(
        _constraint_rows(algebra, basis, basis), algebra.dimension, algebra.p))


@dataclass(frozen=True)
class AbelianProbe:
    algebra: PublicLieAlgebra
    nilpotency_class: int
    codimension_bound: int
    ideal_flag: tuple

    @property
    def terminal(self):
        return len(self.ideal_flag) <= self.codimension_bound

    @property
    def terminal_dimension_bound(self):
        k = self.codimension_bound
        return k * (k + 1) // 2


def make_abelian_probe(algebra, codimension_bound):
    """Construct an inclusion-maximal abelian IDEAL and a triangular flag.

    No maximum-dimension optimization, hidden basis or field enumeration
    is used. If a>k, dimension alone forces dim(h intersect A)>=a-k.
    The codimension promise itself is not checked against an unknown h.
    """
    n, p = algebra.dimension, algebra.p
    if type(codimension_bound) is not int or not 0 <= codimension_bound <= n:
        raise ValueError("codimension bound must be an integer in [0,n]")
    algebra, c = freeze_lazard_algebra(algebra)
    ideal = []
    for _ in range(n + 1):
        rows = (_constraint_rows(algebra, ideal, ())
                + _constraint_rows(algebra, units(n), ideal))
        extensions = _fmpz_nullspace_basis(rows, n, p)
        new = next((v for v in extensions if not contains(ideal, v, p)), None)
        if new is None:
            break
        ideal.append(tuple(new))
    else:
        raise ArithmeticError("abelian ideal construction failed to terminate")
    commutant = centralizer(algebra, ideal)
    if len(commutant) != len(ideal) or any(not contains(ideal, v, p) for v in commutant):
        raise ArithmeticError("constructed ideal is not self-centralizing")
    a = len(ideal)
    if n > a * (a + 1) // 2 or c > 2 * a - 1:
        raise ArithmeticError("nilpotent triangular-action bound failed")
    return AbelianProbe(algebra, c, codimension_bound, tuple(ideal))


@dataclass(frozen=True)
class NormalizerReduction:
    parent: PublicLieAlgebra
    intersection: tuple
    normalizer_basis: tuple
    section_basis: tuple
    quotient: PublicLieAlgebra | None
    next_codimension_bound: int

    def lift(self, vector):
        return combine(vector, self.section_basis, self.parent.dimension, self.parent.p)

    def project(self, vector):
        _canonical_vec(vector, self.parent.dimension, self.parent.p)
        coordinates = _fmpz_solve_coordinates(
            self.intersection + self.section_basis, vector, self.parent.p)
        if coordinates is None:
            raise ValueError("vector is outside the normalizer")
        return coordinates[len(self.intersection):]

    def pullback(self, quotient_subspace):
        return tuple(self.parent.span(list(self.intersection)
                                     + [self.lift(v) for v in quotient_subspace]))


def reduce_at_known_intersection(probe, intersection):
    """Build N_L(K)/K, conditional on K being EXACTLY h intersect A.

    Checks public linear/algebraic conditions only. Even a nonzero proper
    subspace of h intersect A can pass these checks and discard part of h.
    A hidden-source learner and its completeness/error guarantee are absent.
    """
    algebra, ideal = probe.algebra, probe.ideal_flag
    p, n, k = algebra.p, algebra.dimension, probe.codimension_bound
    kernel = tuple(algebra.span(intersection))
    if not kernel or len(kernel) < len(ideal) - k:
        raise ValueError("intersection dimension violates the reduction contract")
    if any(not contains(ideal, v, p) for v in kernel):
        raise ValueError("intersection must be contained in the public abelian ideal")
    ambient = normalizer(algebra, kernel)
    drop = n - len(ambient)
    if drop > k:
        raise ValueError("normalizer drop contradicts the hidden codimension promise")
    adapted = tuple(algebra.span(list(kernel) + list(ambient)))
    section = adapted[len(kernel):]
    dimension = len(section)
    if dimension >= n:
        raise ArithmeticError("reduction must strictly decrease dimension")
    result = NormalizerReduction(algebra, kernel, ambient, section, None,
                                 min(dimension, k - drop))
    if dimension == 0:
        return result
    tensor = {(i, j): result.project(algebra.bracket(a, b))
              for i, a in enumerate(section) for j, b in enumerate(section)}
    quotient, _ = freeze_lazard_algebra(_from_tensor(p, dimension, tensor))
    return NormalizerReduction(algebra, kernel, ambient, section, quotient,
                               result.next_codimension_bound)
