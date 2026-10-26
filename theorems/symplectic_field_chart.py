"""Public prime-field arithmetic for a proposed Siegel-parabolic reduction.

NOT a quantum HSP or HPGP solver. Reference coefficients use a known secret
only for proof controls. Query constructors and candidate verifiers do not.
The caller supplies a verified odd prime; these guards do not prove primality.
The accompanying note also treats extension fields, not Z/(p**a).
"""

from __future__ import annotations

from collections.abc import Sequence
from fractions import Fraction

from theorems.symplectic_socle_probes import (
    Matrix, add, elementary, eye, multiply, scale, symplectic_form, transpose,
)


def _scope(n: int, q: int) -> None:
    if n < 2 or q < 3 or q % 2 == 0:
        raise ValueError("Requires n >= 2 and a supplied odd field order")


def _symmetric(a: Sequence[Sequence[int]], prime: int) -> Matrix:
    n = len(a)
    _scope(n, prime)
    if any(len(row) != n for row in a):
        raise ValueError("Requires a square symmetric matrix")
    result = tuple(tuple(int(x) % prime for x in row) for row in a)
    if result != transpose(result):
        raise ValueError("Requires a symmetric matrix modulo the supplied prime")
    return result


def upper_unipotent(x: Sequence[Sequence[int]], prime: int) -> Matrix:
    x = _symmetric(x, prime)
    n = len(x)
    return tuple(tuple(int(r == c) + (x[r][c - n] if r < n <= c else 0)
                       for c in range(2 * n)) for r in range(2 * n))


def query_matrix(x: Sequence[Sequence[int]], t: int, i: int, j: int,
                 prime: int) -> Matrix:
    """U_X diag(I+tE_ij, I-tE_ji), entirely in the original field group."""
    x = _symmetric(x, prime)
    n = len(x)
    e = elementary(n, i, j)
    a = add(eye(n), scale(e, t, prime), prime)
    inverse_transpose = add(eye(n), scale(transpose(e), -t, prime), prime)
    diagonal = tuple(tuple(a[r][c] if r < n and c < n else
                           inverse_transpose[r - n][c - n] if r >= n and c >= n
                           else 0 for c in range(2 * n)) for r in range(2 * n))
    return multiply(upper_unipotent(x, prime), diagonal, prime)


def graph_basis(s: Sequence[Sequence[int]], prime: int) -> Matrix:
    """Column basis [S; I], NOT [I; pS] from the ring construction."""
    s = _symmetric(s, prime)
    return s + eye(len(s))


def graph_polynomial(s: Sequence[Sequence[int]], i: int, j: int,
                     prime: int) -> tuple[Matrix, Matrix]:
    """Reference P(t)=tB+t^2C from a KNOWN S; the HPGP convention has Q=-P."""
    s = _symmetric(s, prime)
    e = elementary(len(s), i, j)
    b = add(multiply(e, s, prime), multiply(s, transpose(e), prime), prime)
    c = multiply(multiply(e, s, prime), transpose(e), prime)
    return b, c


def recover_symmetric_matrix(linear_coefficients: Sequence[Matrix],
                             prime: int) -> Matrix:
    """Postprocess correct B_j with i=(j+1) mod n; does NOT learn B_j.

    Consistency is not certification: a bad chart may pass every local check.
    Apply the final candidate verifier against the original oracle.
    """
    n = len(linear_coefficients)
    _scope(n, prime)
    coefficients = [_symmetric(b, prime) for b in linear_coefficients]
    if any(len(b) != n for b in coefficients):
        raise ValueError("Requires n coefficient matrices of size n by n")
    result = [[0] * n for _ in range(n)]
    inverse_two = pow(2, -1, prime)
    for j, b in enumerate(coefficients):
        i = (j + 1) % n
        for k in range(n):
            result[j][k] = b[i][k] * (inverse_two if k == i else 1) % prime
    s = _symmetric(result, prime)
    for j, b in enumerate(coefficients):
        if graph_polynomial(s, (j + 1) % n, j, prime)[0] != b:
            raise ValueError("Inconsistent hidden-polynomial coefficients")
    return s


def coefficient_verification_pairs(b: Matrix, c: Matrix, i: int, j: int,
                                   prime: int) -> tuple[tuple[Matrix, Matrix], ...]:
    """Four field queries; conclusive ONLY under the good-chart promise."""
    b, c = _symmetric(b, prime), _symmetric(c, prime)
    if len(b) != len(c):
        raise ValueError("Coefficient dimensions differ")
    zero = scale(eye(len(b)), 0, prime)
    return tuple((query_matrix(zero, t, i, j, prime),
                  upper_unipotent(add(scale(b, t, prime), scale(c, t * t, prime),
                                     prime), prime)) for t in (1, prime - 1))


def symplectic_inverse(g: Sequence[Sequence[int]], prime: int) -> Matrix:
    dimension = len(g)
    if dimension % 2 or any(len(row) != dimension for row in g):
        raise ValueError("Requires an even square matrix")
    _scope(dimension // 2, prime)
    g = tuple(tuple(int(x) % prime for x in row) for row in g)
    j = symplectic_form(dimension // 2)
    inverse = scale(multiply(multiply(j, transpose(g), prime), j, prime), -1, prime)
    if multiply(inverse, g, prime) != eye(dimension):
        raise ValueError("Matrix is not symplectic")
    return inverse


def candidate_verification_queries(s: Sequence[Sequence[int]], prime: int,
                                   conjugator: Matrix | None = None) -> tuple[Matrix, ...]:
    """Compare EVERY returned original-domain query to f(I).

    For an exact oracle hiding a Lagrangian stabilizer, all comparisons pass
    iff its hidden subspace is conjugator*[S; I], even on a bad chart.
    The constructor has no access to the true hidden subspace.
    """
    s = _symmetric(s, prime)
    n = len(s)
    c = eye(2 * n) if conjugator is None else conjugator
    if len(c) != 2 * n:
        raise ValueError("Conjugator dimension differs")
    symplectic_inverse(c, prime)
    transport = tuple(tuple(s[r][k] if r < n and k < n else
                            -int(r == k - n) if r < n else
                            int(r - n == k) if k < n else 0
                            for k in range(2 * n)) for r in range(2 * n))
    t = multiply(c, transport, prime)
    t_inverse = symplectic_inverse(t, prime)
    queries = []
    for i in range(n):
        for j in range(i, n):
            b = tuple(tuple(int((r, k) == (i, j) or (r, k) == (j, i))
                            for k in range(n)) for r in range(n))
            queries.append(multiply(multiply(t, upper_unipotent(b, prime), prime),
                                    t_inverse, prime))
    return tuple(queries)


def chart_probability(n: int, field_order: int) -> Fraction:
    """Exact probability for a UNIFORM symplectic chart, not a random walk."""
    _scope(n, field_order)
    result = Fraction(1)
    for i in range(1, n + 1):
        result *= Fraction(field_order**i, field_order**i + 1)
    return result


def classical_success_bound(n: int, field_order: int, queries: int) -> Fraction:
    """Distributional bound with random opaque coset labels, not all encodings.

    Allows adaptive classical queries anywhere in Sp. Known center collisions
    are factored out. This is a proved bound's formula, not empirical hardness.
    """
    _scope(n, field_order)
    if queries < 0:
        raise ValueError("Query count must be nonnegative")
    m = n * (n + 1) // 2
    return min(Fraction(1), Fraction(1, field_order**m)
               + Fraction(queries * (queries - 1), field_order))
