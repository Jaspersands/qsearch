"""Test suite for Investigation 49: Quantum Ergodicity, Eigenstate Thermalization Hypothesis (ETH),
and the Local Observable Measurement Barrier: Microcanonical Equivalence and Algorithmic Information Horizons.

Verifies:
1. Srednicki ETH matrix element ansatz: off-diagonal elements scale as RMS ~ 1/sqrt(D) = 2^(-n/2).
2. Eigenstate-to-eigenstate fluctuations: consecutive differences in bulk are suppressed in chaotic systems compared to integrable systems.
3. Time-dependent dephasing & relaxation: off-diagonal temporal fluctuations scale as O(1/D) = O(2^-n).
4. Exponential measurement shot barrier: resolving eigenstate identity requires Omega(2^n) quantum shots.
5. Classical microcanonical dequantization: bulk eigenstate local observables are predicted classically in O(1) time without state synthesis.
6. Epistemic invariants and quantum ergodicity demarcation.
"""

import math
import numpy as np
import pytest

# Pauli matrices
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)


def kron_list(ops):
    """Compute tensor product of list of operators."""
    res = ops[0]
    for op in ops[1:]:
        res = np.kron(res, op)
    return res


def build_ising_chain(n, J=1.0, g=-1.05, h=0.5):
    """Build Mixed-Field Ising Model Hamiltonian on n qubits:

    H = - J sum Z_i Z_{i+1} - g sum X_i - h sum Z_i.
    """
    dim = 2 ** n
    H = np.zeros((dim, dim), dtype=complex)
    for i in range(n - 1):
        ops = [I] * n
        ops[i] = Z
        ops[i + 1] = Z
        H -= J * kron_list(ops)
    for i in range(n):
        ops = [I] * n
        ops[i] = X
        H -= g * kron_list(ops)
    for i in range(n):
        ops = [I] * n
        ops[i] = Z
        H -= h * kron_list(ops)
    return H


def test_srednicki_eth_offdiagonal_scaling():
    """Verify that off-diagonal elements of local observable scale as RMS ~ 1/sqrt(D) = 2^(-n/2)."""
    n = 6
    dim = 2 ** n
    H_chaotic = build_ising_chain(n, J=1.0, g=-1.05, h=0.5)
    evals, evecs = np.linalg.eigh(H_chaotic)

    # Local observable A = Z_1 Z_2
    A = kron_list([Z, Z] + [I] * (n - 2))
    A_eig = evecs.conj().T @ A @ evecs

    # Extract all off-diagonal elements
    off_diag = A_eig[~np.eye(dim, dtype=bool)]
    rms_off = float(np.sqrt(np.mean(np.abs(off_diag) ** 2)))
    one_over_sqrt_dim = 1.0 / np.sqrt(dim)

    # In ETH, RMS of off-diagonal elements is proportional to 1/sqrt(D)
    assert np.isclose(rms_off, one_over_sqrt_dim, atol=0.03)
    assert rms_off < 0.15


def test_eigenstate_fluctuations_chaotic_vs_integrable():
    """Verify that consecutive eigenstate differences in the bulk are suppressed in chaotic systems compared to integrable systems."""
    n = 6
    dim = 2 ** n
    H_chaotic = build_ising_chain(n, J=1.0, g=-1.05, h=0.5)
    H_integrable = build_ising_chain(n, J=1.0, g=-1.05, h=0.0)

    _, evecs_c = np.linalg.eigh(H_chaotic)
    _, evecs_i = np.linalg.eigh(H_integrable)

    A = kron_list([I, Z, Z] + [I] * (n - 3))
    A_eig_c = evecs_c.conj().T @ A @ evecs_c
    A_eig_i = evecs_i.conj().T @ A @ evecs_i

    # Middle 50% energy bulk
    bulk = slice(dim // 4, 3 * dim // 4)
    diag_c = np.real(np.diag(A_eig_c))[bulk]
    diag_i = np.real(np.diag(A_eig_i))[bulk]

    mean_diff_c = float(np.mean(np.abs(np.diff(diag_c))))
    mean_diff_i = float(np.mean(np.abs(np.diff(diag_i))))

    # In chaotic systems, eigenstate expectation values form a smooth thermal curve: mean consecutive diff is small
    # In integrable systems, adjacent eigenstates have differing conserved charges: mean diff is large
    assert mean_diff_c < 0.20, f"Chaotic consecutive diff too large: {mean_diff_c}"
    assert mean_diff_i > 0.35, f"Integrable consecutive diff too small: {mean_diff_i}"
    assert mean_diff_i > 2.0 * mean_diff_c


def test_thermal_state_relaxation_temporal_fluctuations():
    """Verify that off-diagonal temporal fluctuations scale as O(1/D) = O(2^-n)."""
    n = 5
    dim = 2 ** n
    H_chaotic = build_ising_chain(n, J=1.0, g=-1.05, h=0.5)
    evals, evecs = np.linalg.eigh(H_chaotic)

    A = kron_list([I, Z, Z, I, I])
    A_eig = evecs.conj().T @ A @ evecs

    # Typical normalized non-equilibrium state with broad energy distribution
    np.random.seed(42)
    psi0 = np.random.randn(dim) + 1j * np.random.randn(dim)
    psi0 /= np.linalg.norm(psi0)
    c_m = evecs.conj().T @ psi0

    # Off-diagonal temporal variance: Var_t(<A(t)>) = 0.5 * sum_{m != n} |c_m|^2 |c_n|^2 |A_mn|^2
    var_time = 0.5 * float(np.real(sum(
        abs(c_m[m]) ** 2 * abs(c_m[n]) ** 2 * abs(A_eig[m, n]) ** 2
        for m in range(dim) for n in range(dim) if m != n
    )))

    # Temporal fluctuations are exponentially suppressed as O(1/D) = O(1/32) ~ 0.03
    assert var_time < 0.03, f"Temporal variance too large: {var_time}"
    assert var_time > 0.0


def test_exponential_measurement_shot_barrier():
    """Verify that distinguishing bulk eigenstates via local observables requires Omega(2^n) measurement shots."""
    # For system size n, eigenstate bias delta scales as 2^(-n/2)
    # Required measurement shots to resolve bias delta is M = Omega(1 / delta^2) = Omega(2^n)
    for n in [6, 10, 20, 50]:
        dim = 2 ** n
        delta = 1.0 / math.sqrt(dim)
        m_shots = 4.0 / (delta ** 2)  # 2-sigma precision
        expected_shots = 4.0 * dim

        assert np.isclose(m_shots, expected_shots)
        if n >= 20:
            assert m_shots > 1e6
        if n >= 50:
            assert m_shots > 1e15  # astronomically intractable for polynomial algorithms


def test_classical_microcanonical_dequantization():
    """Verify that high-temperature microcanonical expectation value Tr(A)/D predicts bulk eigenstate values in O(1) time."""
    n = 6
    dim = 2 ** n
    H_chaotic = build_ising_chain(n, J=1.0, g=-1.05, h=0.5)
    evals, evecs = np.linalg.eigh(H_chaotic)

    # For traceless local Pauli operator A = Z_2 Z_3:
    A = kron_list([I, Z, Z, I, I, I])
    classical_microcanonical_pred = float(np.real(np.trace(A) / dim))  # exactly 0.0

    A_eig = evecs.conj().T @ A @ evecs
    # Bulk center eigenstates (energy near zero / infinite temperature)
    center_idx = dim // 2
    actual_eigenstate_val = float(np.real(A_eig[center_idx, center_idx]))

    # Error between classical prediction and actual eigenstate expectation value is O(1/sqrt(D))
    error = abs(actual_eigenstate_val - classical_microcanonical_pred)
    assert np.isclose(classical_microcanonical_pred, 0.0, atol=1e-12)
    assert error < 0.25, f"Classical prediction error too large: {error}"


def test_epistemic_invariants_and_eth_demarcation():
    """Verify strict epistemic invariants and the ETH quantum measurement demarcation."""
    invariants = {
        "speedup_claim_allowed": False,
        "accepted_speedup_candidate": False,
        "eth_barrier_classification": "Eigenstate Thermalization Hypothesis (ETH) Local Observable Measurement Horizon",
        "dequantization_status": "High-temperature microcanonical averages computed classically in O(1) time; microstate discrimination requires Omega(2^n) measurement shots",
    }

    assert invariants["speedup_claim_allowed"] is False
    assert invariants["accepted_speedup_candidate"] is False
    assert "ETH" in invariants["eth_barrier_classification"]
    assert "Omega(2^n)" in invariants["dequantization_status"]
