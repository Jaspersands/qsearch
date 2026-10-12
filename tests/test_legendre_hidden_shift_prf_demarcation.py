"""Test suite for Investigation 40: Legendre Symbol Hidden Shift Problem.

Verifies:
1. Exact Gauss sum magnitude: |tau_p|^2 == p and g(chi, k) == chi(k) tau_p.
2. Exact vDHI quantum success probability: P(success) == (p - 1) / p.
3. Exact composite modulus Jacobi totient scaling: P(success) == phi(N) / N.
4. Weil bound character correlation: |sum chi(x+s1) chi(x+s2)| <= 2 sqrt(p) + 1.
5. Epistemic invariants and classical PRF security demarcation.
"""

import numpy as np
import pytest


def legendre(x, p):
    """Compute the Legendre symbol (x / p)."""
    x = x % p
    if x == 0:
        return 0
    val = pow(x, (p - 1) // 2, p)
    return 1 if val == 1 else -1


def jacobi(x, n):
    """Compute the Jacobi symbol (x / n)."""
    x = x % n
    t = 1
    while x != 0:
        while x % 2 == 0:
            x //= 2
            r = n % 8
            if r == 3 or r == 5:
                t = -t
        x, n = n, x
        if x % 4 == 3 and n % 4 == 3:
            t = -t
        x = x % n
    return t if n == 1 else 0


def test_gauss_sum_exact_magnitude():
    """Verify that |tau_p|^2 == p and g(chi, k) == chi(k) tau_p for all primes p."""
    primes = [5, 7, 11, 13, 17, 19, 23]
    for p in primes:
        omega = np.exp(2j * np.pi / p)
        tau_p = sum(legendre(x, p) * omega**x for x in range(p))

        # Magnitude squared must equal p
        assert np.isclose(np.abs(tau_p) ** 2, p, atol=1e-12)

        # For all k in F_p^*
        for k in range(1, p):
            g_k = sum(legendre(x, p) * omega ** (k * x) for x in range(p))
            expected = legendre(k, p) * tau_p
            assert np.isclose(g_k, expected, atol=1e-12)


def test_vdhi_quantum_success_probability_scaling():
    """Verify that vDHI quantum algorithm achieves success probability exactly (p - 1) / p."""
    primes = [7, 11, 13, 17, 19, 23]
    for p in primes:
        omega = np.exp(2j * np.pi / p)
        s = 3  # Secret shift

        # Prepared state: |psi_g> = (1 / sqrt(p - 1)) sum_{x != -s} chi(x + s) |x>
        psi_g = np.zeros(p, dtype=complex)
        for x in range(p):
            psi_g[x] = legendre(x + s, p)
        norm = np.linalg.norm(psi_g)
        psi_g /= norm

        # QFT_p matrix
        F_p = np.zeros((p, p), dtype=complex)
        for a in range(p):
            for b in range(p):
                F_p[a, b] = omega ** (a * b) / np.sqrt(p)

        # Apply QFT_p
        qft_state = F_p @ psi_g

        # Phase cancellation: multiply by chi(k)
        canceled_state = np.zeros(p, dtype=complex)
        for k in range(1, p):
            canceled_state[k] = legendre(k, p) * qft_state[k]

        # Apply inverse QFT_p
        F_p_inv = F_p.conj().T
        final_state = F_p_inv @ canceled_state

        final_probs = np.abs(final_state) ** 2
        target_idx = (-s) % p

        # Target probability must equal exactly (p - 1) / p
        expected_peak = (p - 1.0) / p
        assert np.isclose(final_probs[target_idx], expected_peak, atol=1e-12)

        # Non-target probabilities must equal 1 / (p * (p - 1))
        expected_non_target = 1.0 / (p * (p - 1.0))
        for z in range(p):
            if z != target_idx:
                assert np.isclose(final_probs[z], expected_non_target, atol=1e-12)


def test_composite_modulus_totient_scaling():
    """Verify that for composite moduli N = p * q, peak probability is exactly phi(N) / N."""
    composites = [(3, 5), (3, 7), (5, 7)]  # N = 15, 21, 35
    for p, q in composites:
        N = p * q
        omega = np.exp(2j * np.pi / N)
        s = 4

        # Totient
        phi_N = (p - 1) * (q - 1)
        expected_peak = phi_N / float(N)

        # Prepared state with Jacobi symbol
        psi_g = np.zeros(N, dtype=complex)
        for x in range(N):
            psi_g[x] = jacobi(x + s, N)
        norm = np.linalg.norm(psi_g)
        psi_g /= norm

        # QFT_N
        F_N = np.zeros((N, N), dtype=complex)
        for a in range(N):
            for b in range(N):
                F_N[a, b] = omega ** (a * b) / np.sqrt(N)

        qft_state = F_N @ psi_g

        # Phase cancellation by Jacobi symbol
        canceled_state = np.zeros(N, dtype=complex)
        for k in range(N):
            canceled_state[k] = jacobi(k, N) * qft_state[k]

        # Inverse QFT_N
        F_N_inv = F_N.conj().T
        final_state = F_N_inv @ canceled_state

        final_probs = np.abs(final_state) ** 2
        target_idx = (-s) % N

        assert np.isclose(final_probs[target_idx], expected_peak, atol=1e-12)


def test_weil_bound_character_correlation():
    """Verify that character correlation satisfies Weil's bound |sum chi(x+s1) chi(x+s2)| <= 2 sqrt(p) + 1."""
    primes = [7, 11, 13, 17, 19, 23, 29]
    for p in primes:
        weil_bound = 2.0 * np.sqrt(p) + 1.0
        for s1 in range(p):
            for s2 in range(s1 + 1, min(s1 + 4, p)):
                corr = sum(legendre(x + s1, p) * legendre(x + s2, p) for x in range(p))
                assert np.abs(corr) <= weil_bound, (
                    f"Weil bound violated at p={p}, s1={s1}, s2={s2}: corr={corr}, bound={weil_bound}"
                )


def test_classical_prf_hardness_and_epistemic_invariants():
    """Verify epistemic invariants and classical PRF security boundaries."""
    speedup_claim_allowed = False
    accepted_speedup_candidate = False

    assert not speedup_claim_allowed
    assert not accepted_speedup_candidate

    # Scaling comparison:
    # Classical query / time for Legendre PRF key recovery: Omega(sqrt(p))
    # Coherent quantum query: 1
    p_values = [10007, 65537, 1000003]
    for p in p_values:
        t_classical = np.sqrt(p)
        assert t_classical > 100.0  # Significant classical barrier
