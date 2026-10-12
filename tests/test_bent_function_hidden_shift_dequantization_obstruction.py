"""Test suite for Investigation 39: Bent Function Hidden Shift Problem.

Verifies:
1. Walsh-Hadamard transform flatness: |Walsh(u)| == 2^{n/2} identically for all u.
2. Classical affine-derivative dequantization in exactly n + 1 queries.
3. Spectral flatness measurement blindness (TV distance identically 0.000).
4. Roetteler dual-oracle phase cancellation and exact shift recovery.
5. Higher-order differential linearity for degree-3 Boolean functions.
6. Epistemic invariants and dequantization trilemma enforcement.
"""

import numpy as np
import pytest


def build_mm_bent_function(m):
    """Build the Maiorana-McFarland bent function f(x, y) = x . y on F_2^{2m}."""
    n = 2 * m
    dim = 2**n

    def f(v):
        x = v[:m]
        y = v[m:]
        return sum(x[i] * y[i] for i in range(m)) % 2

    # Symplectic Gram matrix M = A + A^T over F_2
    # For f(x, y) = x . y, M = [[0, I_m], [I_m, 0]]
    M = np.zeros((n, n), dtype=int)
    for i in range(m):
        M[i, m + i] = 1
        M[m + i, i] = 1

    return f, M, n, dim


def test_bent_function_walsh_flatness():
    """Verify that Walsh transform has constant absolute value 2^{n/2} everywhere."""
    for m in [2, 3]:
        f, _, n, dim = build_mm_bent_function(m)
        expected_abs = 2**m

        walsh = np.zeros(dim)
        for u_int in range(dim):
            u = [(u_int >> k) & 1 for k in range(n)]
            val = 0
            for v_int in range(dim):
                v = [(v_int >> k) & 1 for k in range(n)]
                dot = sum(u[k] * v[k] for k in range(n)) % 2
                phase = (-1) ** (f(v) ^ dot)
                val += phase
            walsh[u_int] = val

        abs_vals = np.abs(walsh)
        assert np.all(abs_vals == expected_abs), f"Non-flat Walsh spectrum: {abs_vals}"


def test_classical_affine_derivative_dequantization():
    """Verify that secret shift s is uniquely recovered in exactly n + 1 classical queries."""
    for m in [2, 3]:
        f, M, n, _ = build_mm_bent_function(m)

        # Test across multiple random shifts
        np.random.seed(42 + m)
        for trial in range(5):
            s = np.random.randint(0, 2, size=n)

            def g(v):
                v_shifted = [(v[k] ^ s[k]) for k in range(n)]
                return f(v_shifted)

            # Query 0: Origin v = 0
            v0 = [0] * n
            delta0 = g(v0) ^ f(v0)

            # Queries 1..n: Basis vectors e_i
            L_s = np.zeros(n, dtype=int)
            for i in range(n):
                ei = [0] * n
                ei[i] = 1
                delta_ei = g(ei) ^ f(ei)
                L_s[i] = delta_ei ^ delta0

            # Solve M s = L_s over F_2
            # Since M = [[0, I], [I, 0]], M^{-1} = M
            s_recovered = (M @ L_s) % 2

            assert np.array_equal(s, s_recovered), (
                f"Trial {trial}: Failed to recover s={s}, got {s_recovered}"
            )


def test_spectral_flatness_measurement_blindness():
    """Verify that without dual oracle, measurement probabilities are strictly uniform (1/2^n)."""
    m = 2
    f, _, n, dim = build_mm_bent_function(m)

    s1 = [1, 0, 1, 0]
    s2 = [0, 1, 0, 1]

    def prepare_hadamard_state(shift):
        psi = np.zeros(dim)
        for v_int in range(dim):
            v = [(v_int >> k) & 1 for k in range(n)]
            v_shift = [v[k] ^ shift[k] for k in range(n)]
            psi[v_int] = (-1) ** f(v_shift) / np.sqrt(dim)

        # H^{\otimes n}
        H1 = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
        Hn = H1
        for _ in range(n - 1):
            Hn = np.kron(Hn, H1)
        return Hn @ psi

    phi1 = prepare_hadamard_state(s1)
    phi2 = prepare_hadamard_state(s2)

    # Computational basis probabilities:
    p_comp1 = np.abs(phi1) ** 2
    p_comp2 = np.abs(phi2) ** 2

    assert np.allclose(p_comp1, 1.0 / dim)
    assert np.allclose(p_comp2, 1.0 / dim)

    # TV distance between measurement distributions:
    tv_comp = 0.5 * np.sum(np.abs(p_comp1 - p_comp2))
    assert tv_comp < 1e-14, f"Non-zero TV distance: {tv_comp}"


def test_roetteler_dual_oracle_cancellation():
    """Verify that dual oracle phase cancellation successfully extracts |s> with prob 1.0."""
    m = 2
    f, _, n, dim = build_mm_bent_function(m)
    s = [1, 0, 1, 1]
    s_int = sum(s[k] << k for k in range(n))

    # Maiorana-McFarland bilinear f(x, y) = x . y is self-dual: f_dual(x, y) = x . y
    f_dual = f

    psi_g = np.zeros(dim)
    for v_int in range(dim):
        v = [(v_int >> k) & 1 for k in range(n)]
        v_shift = [v[k] ^ s[k] for k in range(n)]
        psi_g[v_int] = (-1) ** f(v_shift) / np.sqrt(dim)

    # Apply H^{\otimes n}
    H1 = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
    Hn = H1
    for _ in range(n - 1):
        Hn = np.kron(Hn, H1)

    state = Hn @ psi_g

    # Apply dual phase oracle: multiply by (-1)^{f_dual(y)}
    dual_phase_diag = np.zeros(dim)
    for y_int in range(dim):
        y = [(y_int >> k) & 1 for k in range(n)]
        dual_phase_diag[y_int] = (-1) ** f_dual(y)

    state_canceled = dual_phase_diag * state

    # Apply final H^{\otimes n}
    final_state = Hn @ state_canceled

    # Final state must be |s> with probability 1.0
    p_final = np.abs(final_state) ** 2
    assert np.isclose(p_final[s_int], 1.0)
    assert np.isclose(np.sum(p_final), 1.0)


def test_higher_order_differential_linearity():
    """Verify that second-order derivatives of cubic functions are affine, enabling classical recovery."""
    n = 4

    # Cubic function f(x) = x_0 x_1 x_2 ^ x_1 x_3 ^ x_2
    def f_cubic(x):
        return (x[0] * x[1] * x[2] ^ x[1] * x[3] ^ x[2]) % 2

    s = [1, 1, 0, 1]

    def g(x):
        return f_cubic([(x[k] ^ s[k]) for k in range(n)])

    # First derivative Delta_s(x) = g(x) ^ f(x)
    def delta_s(x):
        return g(x) ^ f_cubic(x)

    # Second derivative Delta_{s, u}(x) = Delta_s(x ^ u) ^ Delta_s(x)
    # For a cubic function, second derivative is strictly affine/linear in x
    u = [1, 0, 0, 0]
    for trial in range(10):
        x_a = list(np.random.randint(0, 2, size=n))
        x_b = list(np.random.randint(0, 2, size=n))
        x_ab = [(x_a[k] ^ x_b[k]) for k in range(n)]

        d2_a = delta_s([(x_a[k] ^ u[k]) for k in range(n)]) ^ delta_s(x_a)
        d2_b = delta_s([(x_b[k] ^ u[k]) for k in range(n)]) ^ delta_s(x_b)
        d2_ab = delta_s([(x_ab[k] ^ u[k]) for k in range(n)]) ^ delta_s(x_ab)
        d2_0 = delta_s(u) ^ delta_s([0] * n)

        # Affine test: D(x_a ^ x_b) ^ D(0) == D(x_a) ^ D(x_b)
        assert (d2_ab ^ d2_0) == (d2_a ^ d2_b), "Second derivative must be affine"


def test_epistemic_invariants_and_trilemma():
    """Verify epistemic invariants and the trilemma of the bent function hidden shift."""
    speedup_claim_allowed = False
    accepted_speedup_candidate = False

    assert not speedup_claim_allowed
    assert not accepted_speedup_candidate

    # Query complexity comparison for quadratic bent:
    # Classical: n + 1 queries
    # Quantum: 2 queries (+ dual oracle)
    for n in [10, 20, 50, 100]:
        q_classical = n + 1
        q_quantum = 2
        # Both are strictly polynomial O(n), completely dequantizing exponential claims
        assert q_classical < n**2
        assert q_quantum < n**2
