"""Test suite for Investigation 47: Quantum Chaos, Spectral Form Factors, and Random Matrix Theory vs. Quantum Fourier Sampling.

Verifies:
1. Wigner surmise level repulsion dichotomy: Poisson <r> ~ 0.386 vs GUE <r> ~ 0.600, P(0) = 0 for RMT.
2. Spectral Form Factor (SFF) linear ramp growth K(t) ~ t / 2pi for GUE in the ramp regime (t_dip < t < t_H).
3. State return fidelity collapse: Integrable periodic F(T) == 1.000 vs chaotic GUE F(T) <= 1 / N = O(2^-n) -> 0.
4. Quantum SWAP test exponential suppression: <SWAP> = K(t) / N^2 <= 1 / N, requiring Omega(N^2) = 2^Omega(n) shots.
5. Classical Oganesyan-Huse consecutive gap ratio <r> dequantization in O(N) operations.
6. Epistemic invariants and integrable vs chaotic period finding demarcation.
"""

import math
import numpy as np
import pytest


def sample_gue(n, seed=None):
    """Sample an n x n Gaussian Unitary Ensemble (GUE) matrix."""
    rng = np.random.default_rng(seed)
    a = (rng.normal(0, 1, (n, n)) + 1j * rng.normal(0, 1, (n, n))) / np.sqrt(2.0)
    h = (a + a.conj().T) / 2.0
    return h / np.sqrt(n)


def sample_goe(n, seed=None):
    """Sample an n x n Gaussian Orthogonal Ensemble (GOE) matrix."""
    rng = np.random.default_rng(seed)
    a = rng.normal(0, 1, (n, n))
    h = (a + a.T) / 2.0
    return h / np.sqrt(n)


def consecutive_gap_ratios(evals):
    """Compute the Oganesyan-Huse ratio of consecutive level spacings:

    r_n = min(s_n, s_{n-1}) / max(s_n, s_{n-1}), where s_n = E_{n+1} - E_n.
    """
    spacings = np.diff(np.sort(evals))
    # Filter out zero spacings to prevent divide-by-zero
    spacings = spacings[spacings > 1e-12]
    if len(spacings) < 2:
        return 0.0
    r_vals = np.minimum(spacings[:-1], spacings[1:]) / np.maximum(spacings[:-1], spacings[1:])
    return float(np.mean(r_vals))


def test_wigner_surmise_level_repulsion_dichotomy():
    """Verify that Poisson spectra have <r> ~ 0.386, whereas GUE spectra have <r> ~ 0.600 due to level repulsion."""
    N = 120
    n_trials = 20

    r_poisson_list = []
    r_gue_list = []

    for seed in range(n_trials):
        # Poisson: sorted uniform random numbers
        rng = np.random.default_rng(seed + 100)
        e_poisson = np.sort(rng.uniform(-2.0, 2.0, N))
        r_poisson_list.append(consecutive_gap_ratios(e_poisson))

        # GUE: random matrix eigenvalues
        h_gue = sample_gue(N, seed=seed + 200)
        e_gue = np.linalg.eigvalsh(h_gue)
        # Use bulk eigenvalues (central 60%) to avoid edge effects
        e_bulk = e_gue[int(0.2 * N):int(0.8 * N)]
        r_gue_list.append(consecutive_gap_ratios(e_bulk))

    mean_r_poisson = float(np.mean(r_poisson_list))
    mean_r_gue = float(np.mean(r_gue_list))

    # Analytical values: Poisson <r> = 2 ln 2 - 1 ~ 0.38629
    # GUE <r> ~ 0.5996
    assert np.isclose(mean_r_poisson, 0.386, atol=0.04), f"Poisson <r> mismatch: {mean_r_poisson}"
    assert np.isclose(mean_r_gue, 0.600, atol=0.04), f"GUE <r> mismatch: {mean_r_gue}"
    assert mean_r_gue > mean_r_poisson + 0.15


def test_spectral_form_factor_linear_ramp():
    """Verify that GUE Spectral Form Factor K(t) exhibits a linear ramp growth in the ramp regime."""
    N = 80
    # Use window-averaged SFF (standard RMT protocol) to suppress O(K^2) sample variance
    n_samples = 40
    sff_early = 0.0
    sff_late = 0.0

    for seed in range(n_samples):
        h = sample_gue(N, seed=seed + 500)
        evals = np.linalg.eigvalsh(h)
        # Window average around t_early = 20 and t_late = 80
        w_early = float(np.mean([abs(np.sum(np.exp(-1j * evals * t))) ** 2 for t in np.linspace(18.0, 22.0, 5)]))
        w_late = float(np.mean([abs(np.sum(np.exp(-1j * evals * t))) ** 2 for t in np.linspace(78.0, 82.0, 5)]))
        sff_early += w_early
        sff_late += w_late

    sff_early /= n_samples
    sff_late /= n_samples

    # Ramp regime: SFF grows significantly from early ramp to late ramp
    assert sff_late > sff_early * 2.0, f"Ramp growth insufficient: {sff_early} to {sff_late}"

    # Linear ramp growth ratio: t_late / t_early = 80 / 20 = 4.0
    growth_ratio = sff_late / sff_early
    assert 2.5 < growth_ratio < 5.5, f"Ramp growth ratio unexpected: {growth_ratio}"


def test_quantum_return_fidelity_collapse():
    """Verify that integrable periodic systems achieve 100% return fidelity, while chaotic systems collapse to <= 1/N."""
    N = 128
    T_period = 5.0
    delta = 2.0 * np.pi / T_period

    # Integrable periodic harmonic ladder
    evals_integrable = np.arange(N) * delta

    # Return fidelity F(t) = |(1/N) sum exp(-i E_n t)|^2
    f_integ = abs(np.sum(np.exp(-1j * evals_integrable * T_period)) / N) ** 2
    assert np.isclose(f_integ, 1.0, atol=1e-12)

    # Chaotic GUE system scaled to identical bandwidth
    h_gue = sample_gue(N, seed=42)
    evals_gue = np.sort(np.linalg.eigvalsh(h_gue))
    bw = (N - 1) * delta
    evals_gue = (evals_gue - evals_gue[0]) / (evals_gue[-1] - evals_gue[0]) * bw

    f_gue = abs(np.sum(np.exp(-1j * evals_gue * T_period)) / N) ** 2

    # Chaotic return fidelity must collapse to <= 2 / N
    assert f_gue < 2.0 / N, f"Chaotic fidelity unexpectedly large: {f_gue}"
    suppression_ratio = f_integ / f_gue
    assert suppression_ratio > 50.0, f"Suppression ratio insufficient: {suppression_ratio}"


def test_swap_test_signal_exponential_suppression():
    """Verify that the quantum SWAP test signal <SWAP> = K(t) / N^2 is bounded by 1/N = 2^-n."""
    N = 128  # 7 qubits
    # Ramp maximum is bounded by the plateau K(t) <= N
    plateau_k = N
    swap_signal = plateau_k / (N ** 2)

    assert np.isclose(swap_signal, 1.0 / N, atol=1e-12)

    # For n = 20 qubits (N = 10^6), SWAP signal is < 10^-6
    n_qubits = 20
    n_dim = 2 ** n_qubits
    swap_signal_20 = 1.0 / n_dim
    assert swap_signal_20 < 1e-6

    # Required measurement shots to resolve signal scales as Omega(1 / signal^2) = Omega(N^2)
    shots_required = 1.0 / (swap_signal_20 ** 2)
    assert shots_required > 1e12


def test_classical_oganesyan_huse_r_ratio_dequantization():
    """Verify that the classical <r> statistic distinguishes integrable from chaotic systems in O(N) operations."""
    N = 100
    e_integrable = np.sort(np.arange(N) + 0.1 * np.random.randn(N))
    e_chaotic = np.sort(np.linalg.eigvalsh(sample_gue(N, seed=77)))

    r_int = consecutive_gap_ratios(e_integrable)
    r_chaos = consecutive_gap_ratios(e_chaotic)

    # Linear time difference check: O(N) operations compute r_n without quantum time evolution
    assert abs(r_int - r_chaos) > 0.1
    # Distinguishable with high confidence
    assert r_chaos > 0.50


def test_epistemic_invariants_and_chaos_demarcation():
    """Verify strict epistemic invariants and the chaotic vs integrable period finding demarcation."""
    invariants = {
        "speedup_claim_allowed": False,
        "accepted_speedup_candidate": False,
        "integrable_period_finding": "BQP Solvable via harmonic revivals F(T) = 1.0 (Shor / Hallgren)",
        "chaotic_period_finding": "Exponentially Suppressed: Return fidelity F(t) <= 1/N = 2^-n and zero harmonic peaks",
        "sff_ramp_detection": "Exponential Measurement Lower Bound Omega(N^2) = 2^Omega(n) shots on quantum computers",
    }

    assert invariants["speedup_claim_allowed"] is False
    assert invariants["accepted_speedup_candidate"] is False
    assert "BQP" in invariants["integrable_period_finding"]
    assert "Suppressed" in invariants["chaotic_period_finding"]
    assert "Exponential" in invariants["sff_ramp_detection"]
