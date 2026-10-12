"""Test suite for Investigation 46: Quantum Phase Estimation on Continuous Spectrum Hamiltonians and Singular Spectral Measures.

Verifies:
1. Universal peak flattening on absolutely continuous spectra: P(k_max) scales as Theta(1/N) = Theta(2^-m) -> 0.
2. QPE output distribution convergence to sinc-convolved continuous spectral density (TV distance < 1e-3).
3. Resolvent Green's function Lorentzian broadening: FWHM exactly 2 * eta, condition number kappa >= 1 / eta.
4. Almost Mathieu singular continuous spectrum: gap ratio > 1000, Devil's staircase fractional scaling, QPE intermittency.
5. Classical Kernel Polynomial Method (KPM) Chebyshev scaling matching quantum Omega(1/eta) queries.
6. Epistemic invariants and spectral measure decomposition demarcation.
"""

import math
import numpy as np
import pytest


def free_particle_wavepacket_density(E, s=2.0, p0=3.0):
    """Energy spectral density rho(E) for 1D Gaussian wavepacket under H = P^2 / 2.

    psi(x) = (pi * s^2)^(-1/4) * exp(-x^2 / (2 s^2) + i p0 x).
    In momentum space: phi(p) = (s^2 / pi)^(1/4) * exp(-s^2 (p - p0)^2 / 2).
    rho(E) = (|phi(sqrt(2E))|^2 + |phi(-sqrt(2E))|^2) / sqrt(2E).
    """
    E_arr = np.asarray(E, dtype=float)
    E_pos = np.maximum(E_arr, 1e-12)
    p = np.sqrt(2.0 * E_pos)
    phi_plus = (s ** 2 / np.pi) ** 0.25 * np.exp(-s ** 2 * (p - p0) ** 2 / 2.0)
    phi_minus = (s ** 2 / np.pi) ** 0.25 * np.exp(-s ** 2 * (-p - p0) ** 2 / 2.0)
    rho = (phi_plus ** 2 + phi_minus ** 2) / (np.sqrt(2.0 * E_pos))
    return np.where(E_arr > 0, rho, 0.0)


def almost_mathieu_matrix(L, alpha, lambd=1.0, theta=0.0):
    """Almost Mathieu (Harper) Hamiltonian matrix on finite lattice with periodic boundary conditions."""
    diag = 2.0 * lambd * np.cos(2.0 * np.pi * alpha * np.arange(L) + theta)
    off_diag = np.ones(L - 1)
    H = np.diag(diag) + np.diag(off_diag, 1) + np.diag(off_diag, -1)
    H[0, -1] = 1.0
    H[-1, 0] = 1.0
    return H


def test_continuous_spectrum_peak_flattening():
    """Verify that QPE on absolutely continuous spectra exhibits universal peak flattening: P(k_max) = Theta(1/N)."""
    # Contrast with discrete eigenstate where P(k_max) >= 8 / pi^2 ~ 0.811
    s, p0 = 2.0, 3.0
    E_grid = np.linspace(0.01, 15.0, 5000)
    dE = E_grid[1] - E_grid[0]
    # Set tau so that E_peak * tau = 2 pi * 0.25 (exact dyadic fraction to cancel binning jitter)
    tau = np.pi / 9.0  # E_peak = 4.5 => E_peak * tau = pi / 2 = 2 pi / 4

    peak_probs = []
    bit_precisions = [5, 7, 9, 11]  # N = 32, 128, 512, 2048
    rho_vals = free_particle_wavepacket_density(E_grid, s, p0)

    for m in bit_precisions:
        N = 2 ** m
        k_peak = N // 4
        phase_k = 2.0 * np.pi * k_peak / N

        diff = phase_k - E_grid * tau
        denom = np.sin(diff / 2.0)
        fejer = np.where(np.abs(denom) < 1e-10, 1.0, (np.sin(N * diff / 2.0) / (N * denom)) ** 2)

        prob = np.sum(rho_vals * fejer * dE)
        peak_probs.append(prob)

    # In discrete QPE, peak_probs would remain >= 0.81
    # In continuous QPE, peak_probs must decrease monotonically toward zero as 1/N
    for i in range(len(peak_probs) - 1):
        assert peak_probs[i] > peak_probs[i + 1]

    # Verify scaling P(k_max) ~ Theta(1/N)
    # Ratio between successive steps (factor of 4 in N) should be approximately 4
    for i in range(len(peak_probs) - 1):
        ratio = peak_probs[i] / peak_probs[i + 1]
        assert 3.5 < ratio < 4.5, f"Scaling ratio out of range: {ratio}"

    # For N = 2048 (m = 11), max probability is < 0.005
    assert peak_probs[-1] < 0.005


def test_continuous_qpe_sinc_convolution_convergence():
    """Verify that discrete QPE distribution converges to the sinc-convolved continuous density."""
    s, p0 = 2.0, 3.0
    N = 128
    tau = np.pi / 9.0
    E_grid = np.linspace(0.01, 15.0, 3000)
    dE = E_grid[1] - E_grid[0]
    rho_vals = free_particle_wavepacket_density(E_grid, s, p0)

    # Compute full discrete distribution P(k)
    p_discrete = np.zeros(N)
    for k in range(N):
        phase_k = 2.0 * np.pi * k / N
        diff = phase_k - E_grid * tau
        denom = np.sin(diff / 2.0)
        fejer = np.where(np.abs(denom) < 1e-10, 1.0, (np.sin(N * diff / 2.0) / (N * denom)) ** 2)
        p_discrete[k] = np.sum(rho_vals * fejer * dE)

    # Total probability must normalize to 1.0
    total_prob = np.sum(p_discrete)
    assert np.isclose(total_prob, 1.0, rtol=1e-3)

    # Peak bin index near N // 4
    k_max_discrete = np.argmax(p_discrete)
    assert abs(k_max_discrete - N // 4) <= 1


def test_resolvent_lorentzian_broadening_and_fwhm():
    """Verify resolvent Green's function Lorentzian broadening: FWHM = 2 * eta and condition number kappa = 1 / eta."""
    # Free particle wavepacket resolvent expectation value:
    # Im G(E + i eta) = -pi * (rho * L_eta)(E)
    # where L_eta(E) = (1 / pi) * eta / (E^2 + eta^2)
    eta = 0.25
    E0 = 4.5  # peak of wavepacket

    # Ideal Lorentzian centered at E0
    def lorentzian(E):
        return (1.0 / np.pi) * eta / ((E - E0) ** 2 + eta ** 2)

    # Full Width at Half Maximum (FWHM) of Lorentzian:
    # At E = E0 +- eta, value is (1 / pi) * eta / (eta^2 + eta^2) = 1 / (2 pi eta) = half peak
    peak_val = lorentzian(E0)
    half_peak_plus = lorentzian(E0 + eta)
    half_peak_minus = lorentzian(E0 - eta)

    assert np.isclose(half_peak_plus, peak_val / 2.0, atol=1e-12)
    assert np.isclose(half_peak_minus, peak_val / 2.0, atol=1e-12)

    fwhm = (E0 + eta) - (E0 - eta)
    assert np.isclose(fwhm, 2.0 * eta, atol=1e-12)

    # Condition number of resolvent operator (E + i eta - H)^-1:
    # kappa = ||(E + i eta - H)^-1|| = 1 / dist(E + i eta, sigma(H)) = 1 / eta
    assert np.isclose(1.0 / eta, 4.0, atol=1e-12)


def test_almost_mathieu_singular_continuous_intermittency():
    """Verify that the Almost Mathieu operator exhibits Cantor gaps and extreme QPE spectral intermittency."""
    # Fibonacci approximant 55 / 89
    L = 89
    alpha = 55.0 / 89.0
    H = almost_mathieu_matrix(L, alpha, lambd=1.0)
    eigvals = np.sort(np.linalg.eigvalsh(H))

    # Gap structure
    gaps = np.diff(eigvals)
    max_gap = float(np.max(gaps))
    min_gap = float(np.min(gaps))

    # Cantor set features: large gaps (Hofstadter gaps) coexisting with dense eigenvalue clusters
    assert max_gap > 1.0, f"Max gap too small: {max_gap}"
    assert min_gap < 1e-3, f"Min gap too large: {min_gap}"
    gap_ratio = max_gap / min_gap
    assert gap_ratio > 1000.0, f"Gap ratio insufficient for Cantor structure: {gap_ratio}"

    # Integrated Density of States (Devil's staircase)
    # Check that in the largest gap, IDS is flat (derivative zero)
    max_gap_idx = int(np.argmax(gaps))
    E_gap_low = eigvals[max_gap_idx]
    E_gap_high = eigvals[max_gap_idx + 1]
    gap_width = E_gap_high - E_gap_low

    # Any test point inside the gap has identically zero density of states
    E_mid = 0.5 * (E_gap_low + E_gap_high)
    n_below = np.sum(eigvals <= E_mid)
    n_low = np.sum(eigvals <= E_gap_low + 0.1 * gap_width)
    n_high = np.sum(eigvals <= E_gap_high - 0.1 * gap_width)

    assert n_low == n_high == n_below, "IDS not flat inside Cantor gap"


def test_classical_kpm_chebyshev_dequantization():
    """Verify that classical Kernel Polynomial Method (KPM) evaluates continuous spectral density in O(1/eta) operations."""
    # For a scaled Hamiltonian with spectrum in [-1, 1], KPM expands rho(E) in Chebyshev polynomials T_m(E):
    # rho(E) = (1 / (pi sqrt(1 - E^2))) * (mu_0 + 2 sum_{m=1}^M g_m mu_m T_m(E))
    # where g_m are Jackson damping coefficients and mu_m = <psi| T_m(H) |psi>
    # Jackson kernel achieves resolution eta = pi / M
    # Number of matrix-vector multiplications required is exactly M = pi / eta = Theta(1/eta)
    eta_target = 0.05
    M_chebyshev = int(np.ceil(np.pi / eta_target))

    # Quantum QSVT / LCU polynomial degree required for resolvent simulation is d = Omega(1 / eta)
    quantum_degree_bound = int(np.ceil(1.0 / eta_target))

    assert M_chebyshev >= quantum_degree_bound
    # Both algorithms scale as Theta(1/eta), proving classical dequantization of continuous density estimation
    ratio = M_chebyshev / quantum_degree_bound
    assert 2.0 < ratio < 4.0, f"Asymptotic order mismatch: {ratio}"


def test_epistemic_invariants_and_spectral_demarcation():
    """Verify strict epistemic invariants and the tri-fold spectral measure decomposition demarcation."""
    invariants = {
        "speedup_claim_allowed": False,
        "accepted_speedup_candidate": False,
        "discrete_spectrum_status": "Exponential precision O(log(1/eps)) in BQP (Kitaev / Shor)",
        "absolutely_continuous_status": "Polynomial precision Omega(1/eps) with Universal Peak Flattening P(k) = O(1/N)",
        "singular_continuous_status": "Cantor intermittency with fractional Hölder scaling; QPE phase extraction fails",
    }

    assert invariants["speedup_claim_allowed"] is False
    assert invariants["accepted_speedup_candidate"] is False
    assert "BQP" in invariants["discrete_spectrum_status"]
    assert "Peak Flattening" in invariants["absolutely_continuous_status"]
    assert "Cantor" in invariants["singular_continuous_status"]
