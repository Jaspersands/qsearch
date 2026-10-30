"""Exact Gram-completion controls, not a geometric repolarization backend.

Integer matrices act on powers of the same elliptic curve with product
polarization. These tests construct no curves, quotient models, torsion
points or coherent oracle. Square decompositions are finite test controls;
the research note cites the separate polynomial-time existence algorithm.
"""

from math import gcd, prod

import pytest
from flint import nmod_mat
from sympy import Matrix, eye, zeros
from sympy.solvers.diophantine.diophantine import sum_of_four_squares

from tests.test_siegel_repolarization import (
    ONE, ROOTS, ZERO, add, adj, compile_word, eye as quaternion_eye,
    mul, polarization, qa, qc, qm, qs, scale,
)


def gram_completion(f, characteristic=11, ell=5):
    """Fixture specialization of the rectangular completion to real entries."""
    g = f.rows
    assert f == f.T and f.cols == g
    rows = eye(g).tolist()
    for i in range(g):
        for j in range(i + 1, g):
            row = [0] * g
            row[i], row[j] = f[i, j], -1
            rows.append(row)
    u = Matrix(rows)
    threshold = max(f[i, i] + (u.T * u)[i, i] for i in range(g))
    primes = []
    for r in (3, 5, 7, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47):
        if r not in (characteristic, ell):
            primes.append(r)
            if prod(primes) > threshold:
                break
    n = prod(primes)
    assert n > threshold
    for i in range(g):
        remainder = int(n - f[i, i] - (u.T * u)[i, i])
        squares = sum_of_four_squares(remainder)
        assert sum(a * a for a in squares) == remainder
        for a in squares:
            row = [0] * g
            row[i] = a
            rows.append(row)
    return Matrix(rows), n, primes


def fixture(a, b, shear):
    ell = a * a + b * b
    phi = Matrix([[a, -b], [b, a]])
    sigma = Matrix([[1, shear * ell], [0, 1]])
    psi = phi * sigma.inv()
    h = phi * sigma.T * sigma * phi.inv()
    assert phi.T * phi == ell * eye(2)
    assert h == h.T and h.det() == 1
    assert all(x.is_Integer for x in h)
    assert psi.T * h * psi == ell * eye(2)
    return ell, psi, h


@pytest.mark.parametrize("a,b", [(2, 1), (3, 2), (6, 5)])
@pytest.mark.parametrize("shear", [-1, 1, 2])
def test_source_completion_and_complementary_polarization(a, b, shear):
    ell, psi, h = fixture(a, b, shear)
    f = psi.T * psi
    c, n, primes = gram_completion(f, ell=ell)
    assert len(set(primes)) == len(primes)
    assert n % ell != 0 and n % 11 != 0
    assert c.rows == 5 * 2 + 1
    assert c[:2, :] == eye(2)
    assert c.T * c == n * eye(2) - f

    j = psi.col_join(c)
    assert j.T * j == n * eye(2)
    projection = eye(j.rows) - j * j.T / n
    assert projection == projection.T == projection * projection
    inclusion = eye(2).col_join(zeros(c.rows, 2))
    pulled_back = n * inclusion.T * projection * inclusion
    assert pulled_back == n * eye(2) - psi * psi.T
    assert pulled_back == n * eye(2) - ell * h.inv()
    assert pulled_back[0, 0] > 0 and pulled_back.det() > 0
    assert pulled_back != h

    # A different scalar multiplier does not repair the coprime-N output.
    assert h[0, 1] != 0
    scalar = pulled_back[0, 1] / h[0, 1]
    assert pulled_back != scalar * h


@pytest.mark.parametrize("a,b", [(2, 1), (3, 2), (6, 5)])
@pytest.mark.parametrize("k", [1, 2, 3])
def test_dimension_two_direct_repair_forces_secret_prime_in_quotient(a, b, k):
    ell, psi, h = fixture(a, b, 1)
    trace = h.trace()
    assert h + h.inv() == trace * eye(2)
    forced_n = k * k * ell * trace
    assert forced_n % ell == 0
    assert forced_n * eye(2) - k * k * psi * psi.T == k * k * ell * h
    for offset in [-1, 1, 2]:
        n = forced_n + offset
        assert n % ell != 0
        wrong = n * eye(2) - k * k * psi * psi.T
        scalar = wrong[0, 1] / h[0, 1]
        assert wrong != scalar * h


def test_no_repolarization_needed_for_scalar_control():
    psi = Matrix([[2, -1], [1, 2]])
    h = eye(2)
    assert 7 * eye(2) - psi * psi.T == 2 * h
    # The nonscalar hypothesis in the obstruction is essential.


def test_quaternion_completion_uses_the_correct_conjugate_orientation():
    q = (1, 1, 1, 0)
    f = ((qs(5, ONE), q), (qc(q), qs(10, ONE)))
    rows = [(ONE, ZERO), (ZERO, ONE), (qc(q), qs(-1, ONE))]
    # Here N=21; the diagonal deficits are 2 and 9.
    rows.extend([(ONE, ZERO), (ONE, ZERO), (ZERO, qs(3, ONE))])
    gram = [[ZERO, ZERO], [ZERO, ZERO]]
    for row in rows:
        for i in range(2):
            for j in range(2):
                gram[i][j] = qa(gram[i][j], qm(qc(row[i]), row[j]))
    expected = add(scale(21, quaternion_eye(2)), scale(-1, f))
    assert tuple(tuple(row) for row in gram) == expected


@pytest.mark.parametrize("root", ROOTS)
def test_actual_quaternion_lifts_obey_the_transferred_quadratic_identity(root):
    sigma, _ = compile_word(root)
    s = mul(adj(sigma), sigma)
    trace = s[0][0][0] + s[1][1][0]
    assert s[0][0][1:] == s[1][1][1:] == (0, 0, 0)
    unit = quaternion_eye(2)
    assert add(mul(s, s), unit) == scale(trace, s)
    h = polarization(sigma)
    assert add(mul(h, h), unit) == scale(trace, h)
    assert h != unit and trace >= 3


@pytest.mark.parametrize("a,b", [(1, 2), (3, 2), (6, 5)])
def test_intrinsically_trivial_elliptic_restrictions_leave_nonintegral_projectors(a, b):
    ell = a * a + b * b
    phi = Matrix([[a, b], [-b, a]])
    other = phi.T
    assert gcd(a, b) == 1  # Bezout gives a retraction of each column map.
    assert phi.T * phi == ell * eye(2)
    e = Matrix([[1, 0], [0, 0]])
    q = phi * e * phi.inv()
    assert q == q.T == q * q
    assert q * (eye(2) - q) == zeros(2)
    assert max(x.q for x in q) == ell
    assert max(x.q for x in eye(2) - q) == ell
    assert ell * q == phi * e * phi.T

    kernel = Matrix([b, -a])
    assert all(int(x) % ell == 0 for x in phi * kernel)
    assert any(int(x) % ell for x in other * kernel)
    assert any(int(x) % ell for x in phi * e * kernel)
    for r in (3, 7, 17, 19):
        def mod(matrix):
            return nmod_mat([[int(x.p) * pow(int(x.q), -1, r) % r
                              for x in row] for row in matrix.tolist()], r)

        for mask in range(1, r):
            w = mask * mod(phi)
            assert w * mod(e) * w.inv() == mod(q)
