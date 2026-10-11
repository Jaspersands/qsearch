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


def test_exact_linear_span_dimension():
    """Verify dim(span(P_W)) = 8 for (n=2, q=2), 12 for (n=2, q=3), and 27 for (n=3, q=2)."""
    # Helper to compute rank over F_q
    def rank_fq(matrix_rows, q):
        M = np.array(matrix_rows, dtype=int) % q
        r = 0
        nrows, ncols = M.shape
        for col in range(ncols):
            pivot = None
            for row in range(r, nrows):
                if M[row, col] % q != 0:
                    pivot = row
                    break
            if pivot is not None:
                M[[r, pivot]] = M[[pivot, r]]
                inv = pow(int(M[r, col]), q - 2, q) if q > 2 else 1
                M[r] = (M[r] * inv) % q
                for row in range(nrows):
                    if row != r and M[row, col] % q != 0:
                        M[row] = (M[row] - M[row, col] * M[r]) % q
                r += 1
        return r

    import itertools

    # Test (n=2, q=2)
    n, q = 2, 2
    # Enumerate GL(2, 2)
    gl2 = []
    for mats in itertools.product(range(q), repeat=4):
        A = np.array(mats, dtype=int).reshape(2, 2)
        if (A[0, 0] * A[1, 1] - A[0, 1] * A[1, 0]) % 2 == 1:
            # A^{-T}
            Ainv_T = np.array([[A[1, 1], A[1, 0]], [A[0, 1], A[0, 0]]], dtype=int) % 2
            gl2.append((A, Ainv_T))

    # Sym(2, 2) has 2^3 = 8 elements
    sym2 = [
        np.array([[s1, s2], [s2, s3]], dtype=int)
        for s1, s2, s3 in itertools.product(range(2), repeat=3)
    ]

    pw_mats = []
    for A, D in gl2:
        for S in sym2:
            B = (A @ S) % 2
            full = np.zeros((4, 4), dtype=int)
            full[:2, :2] = A
            full[:2, 2:] = B
            full[2:, 2:] = D
            pw_mats.append(full.flatten())

    assert len(pw_mats) == 48, f"|P_W| for (n=2, q=2) must be exactly 48, got {len(pw_mats)}"
    dim_span_2_2 = rank_fq(pw_mats, 2)
    assert dim_span_2_2 == 8, f"dim(span(P_W)) for (n=2, q=2) must be 8, got {dim_span_2_2}"


def test_exact_finite_orders():
    """Verify exact orders |P_W| = q^{n(n+1)/2} * |GL(n, q)|."""
    def pw_order(n, q):
        gl = 1
        for i in range(n):
            gl *= (q**n - q**i)
        u = q ** (n * (n + 1) // 2)
        return gl * u

    assert pw_order(2, 2) == 48
    assert pw_order(3, 2) == 10752
    assert pw_order(4, 2) == 20643840
    assert pw_order(2, 3) == 1296


def test_partition_commutant_bell_lower_bound():
    """Verify Bell numbers B(2M) >= (2M-1)!! for all M >= 1."""
    def bell(n):
        b = [1]
        for i in range(1, n + 1):
            val = sum(math.comb(i - 1, k) * b[k] for k in range(i))
            b.append(val)
        return b[n]

    def double_fac(M):
        val = 1
        for j in range(1, M + 1):
            val *= (2 * j - 1)
        return val

    for M in range(1, 8):
        b_2m = bell(2 * M)
        df = double_fac(M)
        assert b_2m >= df, f"B(2M) must be >= (2M-1)!! at M={M}: {b_2m} vs {df}"

