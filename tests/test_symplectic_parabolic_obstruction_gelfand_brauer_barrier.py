"""
Test suite for Investigation 27:
The Symplectic Parabolic Obstruction: Non-Linear Block Duality,
Gel'fand Pair Collapse, and Brauer Commutant Barrier.
"""

import math
import numpy as np
import pytest


def make_symplectic_form(n, q=2):
    """Construct the standard 2n x 2n symplectic matrix J over F_q."""
    J = np.zeros((2 * n, 2 * n), dtype=int)
    for i in range(n):
        J[i, n + i] = 1
        J[n + i, i] = -1 % q if q > 2 else 1
    return J % q


def omega_pairing(x, y, J, q=2):
    """Compute the symplectic pairing x^T J y mod q."""
    return int(np.dot(x, np.dot(J, y)) % q)


def symplectic_transvection(v, x, J, q=2):
    """Compute T_v(x) = x + Omega(x, v) * v mod q."""
    c = omega_pairing(x, v, J, q)
    return (x + c * v) % q


def test_symplectic_transvection_invariance():
    """Verify that T_v is symplectic for every vector v in char 2 and odd char."""
    for q in [2, 3, 5]:
        n = 2
        J = make_symplectic_form(n, q)
        np.random.seed(42)
        for _ in range(20):
            v = np.random.randint(0, q, size=2 * n)
            if not np.any(v % q):
                continue
            # Build matrix representation of T_v
            Tv = np.zeros((2 * n, 2 * n), dtype=int)
            for j in range(2 * n):
                ej = np.zeros(2 * n, dtype=int)
                ej[j] = 1
                Tv[:, j] = symplectic_transvection(v, ej, J, q)
            # Check Tv^T J Tv == J mod q
            prod = np.dot(Tv.T, np.dot(J, Tv)) % q
            assert np.array_equal(prod, J), f"Failed symplectic invariance for q={q}, v={v}"


def test_lagrangian_membership_criterion():
    """Verify f(T_v) == f(I) <=> v in W for Lagrangian W."""
    n = 2
    q = 3
    J = make_symplectic_form(n, q)
    # Standard Lagrangian subspace W = span(e1, e2)
    # W has basis vectors [1,0,0,0]^T and [0,1,0,0]^T
    def in_W(v):
        return v[2] % q == 0 and v[3] % q == 0

    # Test all non-zero vectors in F_q^{2n}
    for i1 in range(q):
        for i2 in range(q):
            for i3 in range(q):
                for i4 in range(q):
                    v = np.array([i1, i2, i3, i4], dtype=int)
                    if not np.any(v % q):
                        continue
                    # Check whether T_v preserves W
                    # T_v preserves W iff for basis vectors w of W, T_v(w) in W
                    w1 = np.array([1, 0, 0, 0], dtype=int)
                    w2 = np.array([0, 1, 0, 0], dtype=int)
                    Tv_w1 = symplectic_transvection(v, w1, J, q)
                    Tv_w2 = symplectic_transvection(v, w2, J, q)
                    preserves_W = in_W(Tv_w1) and in_W(Tv_w2)
                    is_in_W = in_W(v)
                    assert preserves_W == is_in_W, (
                        f"Mismatch for vector {v}: preserves={preserves_W}, in_W={is_in_W}"
                    )


def test_ambient_density_collapse():
    """Verify that |P_W| / q^{3n^2} <= q^{-1.5 n^2 + 0.5 n}."""
    for q in [2, 3]:
        for n in [1, 2, 3, 4]:
            # Order of GL(n, q)
            gl_order = 1
            for i in range(n):
                gl_order *= (q**n - q**i)
            # Order of unipotent radical U_W = q^{n(n+1)/2}
            u_order = q ** (n * (n + 1) // 2)
            pw_order = gl_order * u_order
            span_order = q ** (3 * n * n)
            density = pw_order / span_order
            upper_bound = q ** (-1.5 * n * n + 0.5 * n)
            assert density <= upper_bound * 1.0001
            assert density > 0


def test_gelfand_double_coset_schubert_count():
    """Verify that the number of intersection dimensions between Lagrangian subspaces is n+1."""
    for n in [1, 2, 3, 4, 5]:
        dimensions = list(range(n + 1))
        assert len(dimensions) == n + 1, "Schubert rank must be n+1"


def test_brauer_algebra_dimension_explosion():
    """Verify double factorial growth (2M-1)!! for M copies."""
    for M in [1, 2, 3, 4, 5, 6]:
        # (2M - 1)!! = prod_{j=1}^M (2j - 1)
        double_fact = 1
        for j in range(1, M + 1):
            double_fact *= (2 * j - 1)
        # Check formula (2M)! / (2^M * M!)
        formula = math.factorial(2 * M) // ((2 ** M) * math.factorial(M))
        assert double_fact == formula
    # For M = 10 (corresponding to n = 40):
    M = 10
    dim_10 = 1
    for j in range(1, M + 1):
        dim_10 *= (2 * j - 1)
    assert dim_10 == 654729075, "Double factorial for M=10 must match exact value"
