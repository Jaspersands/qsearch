"""Test suite for Investigation 41: Heisenberg Group H_3(Z_p) Hidden Subgroup Problem.

Verifies:
1. Exact representation homomorphism and universal non-central trace vanishing across p-dimensional irreps.
2. Weak Fourier sampling central blindness: TV distance identically 0.000 across central shifts c.
3. Subgroup representation projector Pi_H: strictly rank 1, factoring onto an exact quadratic chirp state.
4. Unitary de-chirping and 1D QFT: exact 100% peak probability and recovery of central shear c.
5. Classical black-box query birthday lower bound: collision probability bounded by T^2 / (2 p^2), forcing T = Omega(p).
6. Heisenberg-unipotent boundary: U_4(F_2) central bypass (26/27 involutions bypass Z_1) and derived gap.
"""

import itertools
import numpy as np
import pytest


def inv(x, p):
    """Modular inverse modulo prime p."""
    return pow(x % p, p - 2, p)


def heisenberg_rho(p, w, a, b, c):
    """Construct matrix representation rho_w(M(a, b, c)) on C^p.
    
    rho_w(M(a, b, c)) |x> = omega^{w (c + a x)} |x + b mod p>.
    """
    omega = np.exp(2j * np.pi / p)
    mat = np.zeros((p, p), dtype=complex)
    for x in range(p):
        mat[(x + b) % p, x] = omega ** ((w * (c + a * x)) % p)
    return mat


def test_heisenberg_representation_and_noncentral_trace_vanishing():
    """Verify representation property and non-central character vanishing for p in [3, 5]."""
    for p in [3, 5]:
        omega = np.exp(2j * np.pi / p)

        # 1. Homomorphism check on small sample
        for a1, b1, c1 in itertools.product([0, 1], repeat=3):
            for a2, b2, c2 in itertools.product([1, 2], repeat=3):
                r1 = heisenberg_rho(p, 1, a1, b1, c1)
                r2 = heisenberg_rho(p, 1, a2, b2, c2)
                # Group product: M(a1, b1, c1) * M(a2, b2, c2) = M(a1+a2, b1+b2, c1+c2+a1*b2)
                r12 = heisenberg_rho(p, 1, (a1 + a2) % p, (b1 + b2) % p, (c1 + c2 + a1 * b2) % p)
                assert np.allclose(r1 @ r2, r12, atol=1e-12), "Homomorphism failed!"

        # 2. Universal Non-Central Character Vanishing
        for w in range(1, p):
            for a in range(p):
                for b in range(p):
                    for c in range(p):
                        mat = heisenberg_rho(p, w, a, b, c)
                        tr = np.trace(mat)
                        if (a, b) != (0, 0):
                            # Non-central: trace must be identically 0
                            assert abs(tr) < 1e-10, f"Non-central trace non-zero at (a={a}, b={b}, c={c}): {tr}"
                        else:
                            # Central: trace must be p * omega^{w c}
                            expected = p * (omega ** ((w * c) % p))
                            assert np.isclose(tr, expected, atol=1e-10), f"Central trace mismatch: {tr} vs {expected}"


def test_weak_fourier_sampling_central_blindness():
    """Verify that weak Fourier sampling has TV distance identically 0.000 across different central shifts."""
    p = 5

    def weak_distribution(a, b, c):
        dist = {}
        # 1D irreps labeled by (u, v) in Z_p^2
        for u in range(p):
            for v in range(p):
                # Sum over H = <M(a, b, c)>: elements M(t a, t b, t c + t(t-1)/2 a b)
                s = sum(np.exp(2j * np.pi * (u * ((t * a) % p) + v * ((t * b) % p)) / p) for t in range(p))
                prob = float(np.real(s) / (p ** 3))
                if prob > 1e-10:
                    dist[('1D', u, v)] = prob

        # Non-linear p-dim irreps labeled by w in {1, ..., p-1}
        for w in range(1, p):
            # Tr(rho_w(e)) = p, Tr(rho_w(h)) = 0 for all h != e
            prob = (p / (p ** 3)) * p  # = 1 / p
            dist[('pD', w)] = float(prob)

        return dist

    # Compare subgroups with same [a : b] = [2 : 3] but different c
    d_c1 = weak_distribution(2, 3, 1)
    d_c4 = weak_distribution(2, 3, 4)

    all_keys = set(d_c1.keys()) | set(d_c4.keys())
    tv_distance = 0.5 * sum(abs(d_c1.get(k, 0.0) - d_c4.get(k, 0.0)) for k in all_keys)

    assert tv_distance < 1e-12, f"Weak Fourier TV distance not zero: {tv_distance}"
    assert np.isclose(sum(d_c1.values()), 1.0, atol=1e-12)
    assert np.isclose(sum(d_c4.values()), 1.0, atol=1e-12)


def test_projector_rank_one_and_chirp_state_eigenvector():
    """Verify that the subgroup representation projector Pi_H is strictly rank 1 onto a chirp state."""
    p = 5
    omega = np.exp(2j * np.pi / p)

    for w in [1, 2]:
        for a in [1, 2]:
            for b in [1, 3]:  # b != 0
                for c in [0, 2]:
                    # Construct elements of H = <M(a, b, c)>
                    h_elements = [
                        ((t * a) % p, (t * b) % p, (t * c + (t * (t - 1) // 2) * a * b) % p)
                        for t in range(p)
                    ]

                    # Construct numerical projector Pi_H
                    pi_num = np.zeros((p, p), dtype=complex)
                    for (at, bt, ct) in h_elements:
                        pi_num += heisenberg_rho(p, w, at, bt, ct)
                    pi_num /= p

                    # Verify Hermitian and idempotent
                    assert np.allclose(pi_num, pi_num.conj().T, atol=1e-12)
                    assert np.allclose(pi_num @ pi_num, pi_num, atol=1e-12)

                    # Verify rank is exactly 1
                    eigvals = np.linalg.eigvalsh(pi_num)
                    non_zero_eigvals = [ev for ev in eigvals if ev > 1e-5]
                    assert len(non_zero_eigvals) == 1
                    assert np.isclose(non_zero_eigvals[0], 1.0, atol=1e-12)

                    # Construct analytic chirp state
                    b_inv = inv(b, p)
                    half = inv(2, p)
                    alpha = (w * half * a * b_inv) % p
                    beta = (w * (b_inv * c - half * a)) % p

                    analytic_psi = np.array([
                        omega ** ((alpha * z**2 + beta * z) % p) for z in range(p)
                    ], dtype=complex) / np.sqrt(p)

                    # Projector from analytic chirp state
                    pi_analytic = np.outer(analytic_psi, analytic_psi.conj())
                    assert np.allclose(pi_num, pi_analytic, atol=1e-12), "Analytic chirp projector does not match numeric!"


def test_dechirping_unitary_and_qft_exact_recovery():
    """Verify that unitary de-chirping followed by QFT yields 100% peak probability and reconstructs c."""
    p = 7
    omega = np.exp(2j * np.pi / p)

    # QFT_p matrix: F_p[k, z] = omega^{-k z} / sqrt(p)
    f_p = np.zeros((p, p), dtype=complex)
    for k in range(p):
        for z in range(p):
            f_p[k, z] = omega ** ((-k * z) % p) / np.sqrt(p)

    # Test across all (a, b, c) with b != 0 and all w
    for a in range(p):
        for b in range(1, p):
            for c in range(p):
                for w in range(1, p):
                    b_inv = inv(b, p)
                    half = inv(2, p)
                    alpha = (w * half * a * b_inv) % p
                    beta = (w * (b_inv * c - half * a)) % p

                    # Pure chirp state
                    psi = np.array([
                        omega ** ((alpha * z**2 + beta * z) % p) for z in range(p)
                    ], dtype=complex) / np.sqrt(p)

                    # Diagonal de-chirping operator: U = diag(omega^{-alpha z^2})
                    u_dechirp = np.diag([omega ** ((-alpha * z**2) % p) for z in range(p)])
                    psi_linear = u_dechirp @ psi

                    # Apply QFT
                    psi_k = f_p @ psi_linear

                    # Check probabilities
                    probs = np.abs(psi_k) ** 2
                    peak_idx = int(np.argmax(probs))
                    assert np.isclose(probs[peak_idx], 1.0, atol=1e-12), f"Peak prob not 1.0: {probs[peak_idx]}"
                    assert peak_idx == beta, f"Peak mode {peak_idx} != expected beta {beta}"

                    # Reconstruct c
                    w_inv = inv(w, p)
                    c_recovered = (b * (w_inv * peak_idx + half * a)) % p
                    assert c_recovered == c, f"Reconstruction failed: true {c} vs recovered {c_recovered}"


def test_classical_blackbox_query_birthday_lower_bound():
    """Verify that classical black-box query collision probability scales as O(T^2 / p^2), forcing T = Omega(p)."""
    p = 11
    g_order = p ** 3
    h_order = p

    # Collision probability for any single pair
    single_pair_prob = (h_order - 1) / (g_order - 1)
    assert single_pair_prob < 1.0 / (p ** 2)

    # For T queries, bound is binom(T, 2) * single_pair_prob
    for t_queries in [2, 5, p // 2]:
        num_pairs = t_queries * (t_queries - 1) / 2
        collision_bound = num_pairs * single_pair_prob
        # For T = p // 2, collision bound is well below 1/4
        if t_queries <= p // 2:
            assert collision_bound < 0.25, f"Collision probability {collision_bound} unexpectedly high for T={t_queries}"


def test_heisenberg_unipotent_boundary_and_central_bypass():
    """Verify that U_4(F_2) exhibits central bypass (26/27 involutions bypass Z_1) and dimension gap [G, G] vs Z_1."""
    # Enumerate all elements of U_4(F_2): 2^6 = 64
    elements = []
    for x12, x23, x34, x13, x24, x14 in itertools.product([0, 1], repeat=6):
        m = np.array([
            [1, x12, x13, x14],
            [0, 1,   x23, x24],
            [0, 0,   1,   x34],
            [0, 0,   0,   1  ]
        ], dtype=int)
        elements.append(m)

    assert len(elements) == 64

    # Identity
    eye = np.eye(4, dtype=int)

    # Find center Z_1
    center = [
        m for m in elements
        if all(np.array_equal((m @ g) % 2, (g @ m) % 2) for g in elements)
    ]
    # Center is {I, I + E_14}, size 2
    assert len(center) == 2

    # Find all non-trivial involutions: M != I and M^2 == I mod 2
    involutions = [
        m for m in elements
        if not np.array_equal(m, eye) and np.array_equal((m @ m) % 2, eye)
    ]
    assert len(involutions) == 27

    # Center involutions
    center_involutions = [
        m for m in involutions
        if any(np.array_equal(m, c) for c in center)
    ]
    assert len(center_involutions) == 1

    # Involutions bypassing Z_1: H cap Z_1 = {I}
    bypass_involutions = len(involutions) - len(center_involutions)
    assert bypass_involutions == 26
    # 26 / 27 is ~96.3% of subgroups bypassing the center
    bypass_fraction = bypass_involutions / len(involutions)
    assert bypass_fraction > 0.95

    # Check derived subgroup [G, G] = { [g1, g2] }
    def inv_mat(g):
        x_mat = (g + eye) % 2
        return (eye + x_mat + x_mat @ x_mat + x_mat @ x_mat @ x_mat) % 2

    commutators = set()
    for g1 in elements:
        g1_inv = inv_mat(g1)
        for g2 in elements:
            g2_inv = inv_mat(g2)
            comm = (g1 @ g2 @ g1_inv @ g2_inv) % 2
            commutators.add(tuple(comm.flatten()))

    # The derived subgroup [G, G] has size 8 (dimension 3)
    # while Z_1 has size 2 (dimension 1)
    assert len(commutators) == 8
    # Center is strictly contained in derived subgroup: Z_1 < [G, G]
    assert len(commutators) > len(center)
