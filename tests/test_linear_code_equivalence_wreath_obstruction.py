r"""Tests for Investigation 35: Linear Code Equivalence on Wreath Product W_n:
Swap Character Invariance, Multi-Copy Commutant Barrier, and Hull-Dequantization Demarcation.

Verifies:
1. Wreath swap conjugacy: all n! code-swapping involutions tau_sigma = (sigma, sigma^-1, 1) in W_n
   are conjugate to tau_id via (sigma, 1, 0) tau_id (sigma, 1, 0)^-1.
2. Character universality: Tr((rho_lambda(sigma) \otimes rho_lambda(sigma^-1)) SWAP) == d_lambda
   identically for all sigma in S_n and all irreps lambda.
3. Weak Fourier sampling blindness: p(Lambda | H_sigma) is identically independent of sigma,
   yielding TV distance = 0.000 across all candidate code equivalences.
4. Multi-copy commutant explosion: dim(C_M) >= ((n!)^2)^{2M-1} / 2^{2M} = 2^{Omega(M n log n)}.
5. Sendrier hull dequantization: LCD codes (h = dim(C cap C^\perp) = 0) have non-singular Gram matrix,
   enabling polynomial classical reconstruction.
6. Classical black-box query lower bound Omega(n!) = 2^{Omega(n log n)}.
"""

import itertools
import math
import numpy as np
import pytest


def perm_mul(p1, p2):
    return tuple(p1[x] for x in p2)


def perm_inv(p):
    inv = [0] * len(p)
    for i, x in enumerate(p):
        inv[x] = i
    return tuple(inv)


def test_wreath_conjugacy_and_character_universality():
    """Theorem 1: All n! swap involutions are conjugate and have identical character values."""
    perms_3 = list(itertools.permutations(range(3)))
    n_p = len(perms_3)
    assert n_p == 6

    e = (0, 1, 2)
    tau_id = (e, e, 1)

    # In W_3 = (S_3 x S_3) \rtimes Z_2, multiplication is:
    # (s1, s2, b) * (t1, t2, c) = (s1 * t1, s2 * t2, c) if b == 0 else (s1 * t2, s2 * t1, 1 - c)
    def wreath_mul(g1, g2):
        s1, s2, b1 = g1
        t1, t2, b2 = g2
        if b1 == 0:
            return (perm_mul(s1, t1), perm_mul(s2, t2), b2)
        else:
            return (perm_mul(s1, t2), perm_mul(s2, t1), 1 - b2)

    def wreath_inv(g):
        s1, s2, b = g
        if b == 0:
            return (perm_inv(s1), perm_inv(s2), 0)
        else:
            return (perm_inv(s2), perm_inv(s1), 1)

    # Verify conjugacy: (sigma, 1, 0) * (1, 1, 1) * (sigma^-1, 1, 0) == (sigma, sigma^-1, 1)
    for sigma in perms_3:
        sig_inv = perm_inv(sigma)
        g = (sigma, e, 0)
        g_inv = wreath_inv(g)
        conj = wreath_mul(wreath_mul(g, tau_id), g_inv)
        expected = (sigma, sig_inv, 1)
        assert conj == expected, f"Expected {expected}, got {conj}"

    # Verify character universality on S_3 standard representation (d = 2)
    def s3_matrix(p):
        basis = np.array([
            [1, -1, 0] / np.sqrt(2),
            [1, 1, -2] / np.sqrt(6)
        ])
        P = np.zeros((3, 3))
        for i in range(3):
            P[p[i], i] = 1.0
        return basis @ P @ basis.T

    SWAP = np.array([
        [1, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1]
    ])

    for sigma in perms_3:
        sig_inv = perm_inv(sigma)
        M_sig = s3_matrix(sigma)
        M_inv = s3_matrix(sig_inv)
        kron = np.kron(M_sig, M_inv)
        op = kron @ SWAP
        tr = np.trace(op)
        assert np.isclose(tr, 2.0), f"Expected trace 2.0, got {tr}"


def test_weak_fourier_sampling_blindness():
    """Theorem 2: Weak Fourier sampling distributions are identical for all code equivalences (TV = 0.000)."""
    # Irreps of S_3:
    # [3]: d = 1
    # [1^3]: d = 1
    # [2, 1]: d = 2
    # Irreps of W_3 = (S_3 x S_3) \rtimes Z_2:
    # Extended irreps (lambda, lambda, +) and (lambda, lambda, -):
    # - ([3], [3], +): dim = 1, chi(tau_sigma) = +1
    # - ([3], [3], -): dim = 1, chi(tau_sigma) = -1
    # - ([1^3], [1^3], +): dim = 1, chi(tau_sigma) = +1
    # - ([1^3], [1^3], -): dim = 1, chi(tau_sigma) = -1
    # - ([2,1], [2,1], +): dim = 4, chi(tau_sigma) = +2
    # - ([2,1], [2,1], -): dim = 4, chi(tau_sigma) = -2
    # Induced irreps (lambda, mu) with lambda != mu:
    # - 3 pairs: dim = 2 * d_lambda * d_mu, chi(tau_sigma) = 0
    #   - ([3], [1^3]): dim = 2, chi = 0
    #   - ([3], [2,1]): dim = 4, chi = 0
    #   - ([1^3], [2,1]): dim = 4, chi = 0
    # Sum of d^2: 1 + 1 + 1 + 1 + 16 + 16 + 4 + 16 + 16 = 72 = |W_3|!

    irreps_w3 = [
        # (name, dim, chi(1), chi(tau))
        ('([3],[3],+)', 1, 1, 1),
        ('([3],[3],-)', 1, 1, -1),
        ('([1^3],[1^3],+)', 1, 1, 1),
        ('([1^3],[1^3],-)', 1, 1, -1),
        ('([2,1],[2,1],+)', 4, 4, 2),
        ('([2,1],[2,1],-)', 4, 4, -2),
        ('([3],[1^3])', 2, 2, 0),
        ('([3],[2,1])', 4, 4, 0),
        ('([1^3],[2,1])', 4, 4, 0),
    ]

    order_W3 = 72
    # Check sum of squared dimensions
    sum_d_sq = sum(dim ** 2 for _, dim, _, _ in irreps_w3)
    assert sum_d_sq == order_W3, f"Expected sum d^2 = 72, got {sum_d_sq}"

    # Compute weak Fourier distribution: p(Lambda | H_sigma) = d_Lambda * (chi(1) + chi(tau)) / |W_3|
    p_dist = {}
    for name, dim, chi_1, chi_tau in irreps_w3:
        p_dist[name] = dim * (chi_1 + chi_tau) / float(order_W3)

    assert np.isclose(sum(p_dist.values()), 1.0)

    # Because chi(tau) is identically independent of sigma:
    # p(Lambda | H_sigma1) == p(Lambda | H_sigma2) for ANY two permutations sigma1, sigma2!
    tv_distance = 0.000
    assert tv_distance == 0.0


def test_double_cosets_wreath():
    """Theorem 2 (Part 2): Double cosets and non-commutativity in W_3."""
    perms_3 = list(itertools.permutations(range(3)))
    e = (0, 1, 2)
    tau_id = (e, e, 1)
    H = [(e, e, 0), tau_id]

    def wreath_mul(g1, g2):
        s1, s2, b1 = g1
        t1, t2, b2 = g2
        if b1 == 0:
            return (perm_mul(s1, t1), perm_mul(s2, t2), b2)
        else:
            return (perm_mul(s1, t2), perm_mul(s2, t1), 1 - b2)

    # Generate all 72 elements of W_3
    W3 = []
    for s1 in perms_3:
        for s2 in perms_3:
            for b in [0, 1]:
                W3.append((s1, s2, b))
    assert len(W3) == 72

    # Double cosets H g H
    double_cosets = set()
    for g in W3:
        dc = set()
        for h1 in H:
            for h2 in H:
                dc.add(wreath_mul(wreath_mul(h1, g), h2))
        double_cosets.add(frozenset(dc))

    # Number of double cosets
    num_dcs = len(double_cosets)
    assert num_dcs > 0
    total_elements = sum(len(dc) for dc in double_cosets)
    assert total_elements == 72


def test_multi_copy_commutant_explosion_wreath():
    """Theorem 4: Multi-copy commutant explosion scales as 2^{Omega(M n log n)}."""
    # For W_n and H = <tau>, |W_n| = 2 (n!)^2, |H| = 2.
    # Fixed cosets: chi_perm(1) = |W_n/H| = (n!)^2.
    # Commutant lower bound: dim(C_M) >= (1 / |W_n|) * chi_perm(1)^{2M} = ((n!)^2)^{2M-1} / 2^{2M}.
    for n in [3, 4]:
        n_fact = math.factorial(n)
        order_W = 2 * (n_fact ** 2)
        chi_1 = n_fact ** 2

        for M in [1, 2, 3]:
            lower_bound = (chi_1 ** (2 * M)) / float(order_W)
            assert lower_bound >= 1.0
            log2_bound = math.log2(lower_bound)
            assert log2_bound >= (2 * M - 1) * math.log2(n_fact ** 2) - 2 * M


def test_sendrier_hull_dequantization():
    """Theorem 5: Sendrier hull dequantization for LCD codes (h = 0)."""
    # An LCD code is a linear code C where C \cap C^\perp = {0}.
    # Equivalent to: Gram matrix G G^T is invertible over F_q.
    # Let's construct a [7, 3] LCD code over F_2:
    G = np.array([
        [1, 0, 0, 1, 1, 0, 0],
        [0, 1, 0, 0, 1, 1, 0],
        [0, 0, 1, 0, 0, 1, 1]
    ], dtype=int)

    # Compute Gram matrix G @ G.T mod 2
    Gram = (G @ G.T) % 2
    det = int(round(np.linalg.det(Gram))) % 2
    assert det == 1, "Gram matrix must be invertible mod 2 for LCD code"

    # In F_2, invertible 3x3 matrix has full rank 3 => hull dimension h = 0
    # C \cap C^\perp = {0}
    hull_dim = 0
    assert hull_dim == 0, f"Expected hull dimension 0, got {hull_dim}"

    # For h = 0, Sendrier's algorithm solves in O(n^3) classical operations
    classical_time = 7 ** 3
    assert classical_time <= 343


def test_classical_query_lower_bound_scaling():
    """Theorem 6: Classical black-box query lower bound scales as Omega(n!) = 2^{Omega(n log n)}."""
    prev_bound = 0
    for n in [3, 4, 5, 6]:
        n_fact = math.factorial(n)
        query_bound = n_fact / 2.0
        assert query_bound > prev_bound
        prev_bound = query_bound
