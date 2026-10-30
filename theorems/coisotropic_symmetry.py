"""Exact public symplectic algebra for already accepted Pauli labels.

This module neither verifies symmetry membership nor accesses rho, a hidden
stabilizer basis, or a quantum simulator. The input span need not be isotropic
or coisotropic. Any symmetry interpretation is conditional on the caller's
acceptance procedure; no learning, copy-complexity, or speedup claim is made.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from theorems.prime_character_opi import ring
from theorems.ut5_matrix_phase_alignment import _basis, _canonical, symplectic_pair


Vector = tuple[int, ...]


@dataclass(frozen=True)
class IsotropicDecomposition:
    """A radical plus mutually orthogonal hyperbolic pairs for the input span.

    Each pair (a, b) satisfies [a,b]=1. The radical and the first vector of
    each pair form ``isotropic_basis``, a maximum-dimensional isotropic
    subspace of the supplied span, not an extension outside that span.
    """

    prime: int
    n: int
    span_basis: tuple[Vector, ...]
    radical_basis: tuple[Vector, ...]
    symplectic_pairs: tuple[tuple[Vector, Vector], ...]

    @property
    def span_dimension(self) -> int:
        return len(self.span_basis)

    @property
    def radical_dimension(self) -> int:
        return len(self.radical_basis)

    @property
    def pair_count(self) -> int:
        return len(self.symplectic_pairs)

    @property
    def isotropic_basis(self) -> tuple[Vector, ...]:
        return self.radical_basis + tuple(a for a, _ in self.symplectic_pairs)

    @property
    def isotropic_dimension(self) -> int:
        return self.radical_dimension + self.pair_count

    @property
    def n_generators(self) -> tuple[Vector, ...] | None:
        """First n isotropic generators, or None if that dimension is impossible."""
        if self.isotropic_dimension < self.n:
            return None
        return self.isotropic_basis[:self.n]


def maximal_isotropic_subspace(
    prime: int, n: int, rows: Sequence[Sequence[int]],
) -> IsotropicDecomposition:
    """Decompose arbitrary accepted rows and extract a maximal isotropic space.

    Coordinates are canonical Python integers in [0, prime), in global (x,z)
    order, with [u,v] = z.x' - x.z'. ``prime`` must be an odd prime and ``n``
    a nonnegative integer; explicit n makes empty input unambiguous. Zero,
    duplicate, and dependent rows are allowed and the input is not mutated.

    If the span has dimension d and radical dimension r, its restricted form
    has (d-r)/2 hyperbolic pairs. Taking the radical and one vector from each
    pair attains the maximum isotropic dimension (d+r)/2. In particular, no
    n-dimensional result is manufactured when the accepted span is too small.

    Deterministic row reduction and symplectic Gram-Schmidt use polynomial
    finite-field arithmetic, with no enumeration of the ambient field space.
    """
    ring(prime)
    if type(n) is not int or n < 0:
        raise ValueError("nonnegative integer qudit count required")
    rows = list(rows)
    for row in rows:
        _canonical(row, 2*n, prime)
    # FLINT need not construct a zero-column matrix for the zero-qudit case.
    basis = _basis(rows, prime) if n else []
    remaining = [list(row) for row in basis]
    radical, pairs = [], []
    while remaining:
        a = remaining.pop(0)
        partner = next((i for i, b in enumerate(remaining)
                        if symplectic_pair(a, b, prime)), None)
        if partner is None:
            radical.append(tuple(a))
            continue
        b = remaining.pop(partner)
        inverse = pow(symplectic_pair(a, b, prime), -1, prime)
        b = [inverse*x % prime for x in b]
        pairs.append((tuple(a), tuple(b)))
        # Project to the orthogonal complement of this pair: [a,b]=1.
        for i, v in enumerate(remaining):
            vb = symplectic_pair(v, b, prime)
            va = symplectic_pair(v, a, prime)
            remaining[i] = [(x-vb*y+va*z) % prime
                            for x, y, z in zip(v, a, b)]
    return IsotropicDecomposition(
        prime, n, tuple(map(tuple, basis)), tuple(radical), tuple(pairs),
    )
