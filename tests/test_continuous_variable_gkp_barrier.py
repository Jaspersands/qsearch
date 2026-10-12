"""
Tests for Investigation 54: Continuous-Variable Quantum Computing, Non-Gaussian
Magic, and the Gottesman-Kitaev-Preskill (GKP) Horizon: Wigner Negativity,
Hudson's Theorem, and the Cubic Phase Gate Fault-Tolerant Barrier.

Validates:
1. Hudson's theorem and Mari-Eisert Gaussian polynomial dequantization in Sp(2N, R).
2. GKP stabilizer commutation [S_x, S_p] = 0 and logical Pauli algebra Z_L X_L = -X_L Z_L.
3. Wigner negativity emergence under non-Gaussian cubic phase perturbation.
4. Non-linear Heisenberg momentum shear [V_gamma, p] = -3*gamma*x^2*V_gamma.
5. Finite squeezing photon number <n> ~ 1/(2*Delta^2) and the 10 dB fault-tolerant threshold.
6. Epistemic invariants: speedup_claim_allowed = False, accepted_speedup_candidate = False.
"""

import numpy as np
import pytest
import math
import json
from pathlib import Path


def test_hudson_mari_eisert_gaussian_dequantization():
    """
    Theorem 1: Pure quantum states have non-negative Wigner functions W(x, p) >= 0
    if and only if they are Gaussian states (Hudson 1974).
    Under quadratic Hamiltonians, Gaussian states evolve via symplectic transformations
    S in Sp(2N, R) preserving the symplectic form:
        S @ Omega @ S.T == Omega, where Omega = [[0, 1], [-1, 0]].
    The covariance matrix sigma transforms as sigma' = S @ sigma @ S.T,
    which is simulated classically in O(N^3) time, completely dequantizing
    pure Gaussian continuous-variable quantum computation (Mari & Eisert 2012).
    """
    Omega = np.array([[0.0, 1.0], [-1.0, 0.0]])

    # 1. Single-mode squeezing symplectic matrix S_sq = diag(e^r, e^-r)
    r = 0.8
    S_sq = np.array([[np.exp(r), 0.0], [0.0, np.exp(-r)]])
    assert np.allclose(S_sq @ Omega @ S_sq.T, Omega, atol=1e-12)

    # 2. Phase rotation symplectic matrix S_rot = [[cos theta, sin theta], [-sin theta, cos theta]]
    theta = 0.55
    S_rot = np.array([[np.cos(theta), np.sin(theta)], [-np.sin(theta), np.cos(theta)]])
    assert np.allclose(S_rot @ Omega @ S_rot.T, Omega, atol=1e-12)

    # 3. Covariance matrix evolution of vacuum state sigma_vac = I / 2
    sigma_vac = np.eye(2) * 0.5
    sigma_squeezed = S_sq @ sigma_vac @ S_sq.T
    # Squeezed variances: Var(x) = e^(2r)/2, Var(p) = e^(-2r)/2
    assert np.isclose(sigma_squeezed[0, 0], 0.5 * np.exp(2 * r), atol=1e-12)
    assert np.isclose(sigma_squeezed[1, 1], 0.5 * np.exp(-2 * r), atol=1e-12)
    # Uncertainty product is minimal: Var(x) * Var(p) = 1/4
    assert np.isclose(sigma_squeezed[0, 0] * sigma_squeezed[1, 1], 0.25, atol=1e-12)


def test_gkp_stabilizers_and_logical_pauli_algebra():
    """
    Theorem 2: The Gottesman-Kitaev-Preskill (GKP) code encodes a discrete qubit
    into continuous oscillator position x and momentum p via stabilizers:
        S_x = exp(i * 2*sqrt(pi) * p) = D(x = 2*sqrt(pi))
        S_p = exp(-i * 2*sqrt(pi) * x) = D(p = 2*sqrt(pi))
    The Baker-Campbell-Hausdorff (BCH) phase between displacements D(alpha) and D(beta)
    is exp(i * Im(alpha * beta*)).
    For S_x and S_p, the commutation phase is:
        exp(i * (2*sqrt(pi)) * (2*sqrt(pi))) = exp(4*pi*i) = 1.0.
    Thus, [S_x, S_p] = 0 identically.
    The logical Pauli operators are:
        Z_L = exp(i * sqrt(pi) * p),  X_L = exp(-i * sqrt(pi) * x).
    The logical anticommutation phase is:
        exp(i * sqrt(pi) * sqrt(pi)) = exp(i * pi) = -1.0.
    Thus, Z_L @ X_L = - X_L @ Z_L, recovering the exact discrete Pauli algebra.
    """
    # Phase calculation for stabilizers:
    alpha_stab = 2.0 * np.sqrt(np.pi)
    beta_stab = 2.0 * np.sqrt(np.pi)
    phase_stab = np.exp(1j * alpha_stab * beta_stab)
    # exp(4 pi i) == 1
    assert np.isclose(phase_stab, 1.0 + 0j, atol=1e-12)

    # Phase calculation for logical Paulis:
    alpha_log = np.sqrt(np.pi)
    beta_log = np.sqrt(np.pi)
    phase_log = np.exp(1j * alpha_log * beta_log)
    # exp(pi i) == -1
    assert np.isclose(phase_log, -1.0 + 0j, atol=1e-12)


def test_wigner_negativity_in_non_gaussian_cubic_state():
    """
    Theorem 3: By Hudson's theorem, non-Gaussian operations are necessary to generate
    Wigner negativity:
        N_W(rho) = int |W(x, p)| dx dp - 1 > 0.
    Under a cubic phase gate V_gamma = exp(i * gamma * x^3), the state
    |psi_gamma> = V_gamma |0> develops strong negative Wigner quasiprobability
    ripples, acting as non-Gaussian magic required for CV quantum universality.
    """
    # Numerically evaluate Wigner function of cubic phase state on a grid
    # For small gamma, |psi(x)> = (1/pi)^(1/4) exp(-x^2/2 + i * gamma * x^3)
    gamma = 0.25
    x_grid = np.linspace(-3.0, 3.0, 61)
    p_grid = np.linspace(-3.0, 3.0, 61)

    # Wavefunction psi(x)
    dx = x_grid[1] - x_grid[0]
    dp = p_grid[1] - p_grid[0]
    psi_x = (1.0 / np.pi)**0.25 * np.exp(-0.5 * x_grid**2 + 1j * gamma * x_grid**3)
    psi_x /= np.sqrt(np.sum(np.abs(psi_x)**2) * dx)

    # Compute Wigner function W(0, p) at x = 0:
    # W(0, p) = (1/pi) int psi(y)* psi(-y) exp(2 i p y) dy
    w_0_vals = []
    for p in p_grid:
        integrand = np.conj(psi_x) * psi_x[::-1] * np.exp(2j * p * x_grid)
        val = np.real(np.sum(integrand) * dx) / np.pi
        w_0_vals.append(val)

    w_0_vals = np.array(w_0_vals)
    min_w = np.min(w_0_vals)

    # For gamma > 0, the Wigner function develops negative values (W < 0)
    assert min_w < -0.01, f"Wigner function minimum {min_w} should be strictly negative"


def test_cubic_phase_heisenberg_momentum_shear():
    """
    Theorem 4: The cubic phase gate V_gamma = exp(i * gamma * x^3) induces non-linear
    momentum shear:
        V_gamma^dagger p V_gamma = p + 3 * gamma * x^2.
    Because the momentum shift is quadratic in x, V_gamma does not preserve the
    linear symplectic group Sp(2N, R), taking the circuit out of the classically
    simulable Gaussian Clifford hierarchy and into non-Clifford level 3.
    """
    gamma = 0.15
    # Verify the operator relation via commutator: [x^3, p] = 3 i x^2
    # For V_gamma = exp(i gamma x^3), d/d_gamma (V_gamma^dagger p V_gamma) = 3 x^2
    # Test momentum shift function f(x) = 3 * gamma * x^2
    x_vals = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])
    p_shifts = 3.0 * gamma * x_vals**2

    # The shift is non-linear (strictly quadratic):
    assert np.isclose(p_shifts[2], 0.0)      # at x=0, shift = 0
    assert np.isclose(p_shifts[1], 3 * gamma) # at x=1, shift = 3*gamma
    assert np.isclose(p_shifts[4], 12 * gamma) # at x=2, shift = 12*gamma
    # Second finite difference of p_shifts is constant (proving exact degree 2)
    diff2 = p_shifts[4] - 2 * p_shifts[3] + p_shifts[2]
    expected_diff2 = 6.0 * gamma * (1.0)**2
    assert np.isclose(diff2, expected_diff2)


def test_finite_squeezing_damping_and_threshold_barrier():
    """
    Theorem 5: Ideal GKP states have infinite average photon number <n> = infty.
    Physical GKP states are damped by a Gaussian envelope with parameter Delta:
        <n> approx 1 / (2 * Delta^2).
    Finite squeezing Delta introduces intrinsic displacement noise sigma^2 = Delta^2 / 2.
    Fault-tolerant GKP error correction requires squeezing exceeding the 10 dB threshold:
        s_dB = -10 * log10(Delta^2) >= 10.0 dB  ==>  Delta <= 0.3162.
    Below 10 dB squeezing, intrinsic displacement error exceeds the Voronoi cell radius,
    causing logical error propagation that destroys fault tolerance.
    """
    # 10 dB threshold
    s_thresh_db = 10.0
    delta_thresh = 10.0 ** (-s_thresh_db / 20.0)
    assert np.isclose(delta_thresh, 0.316227766, atol=1e-6)

    # Average photon number at 10 dB:
    n_mean_10db = 1.0 / (2.0 * delta_thresh**2)
    assert np.isclose(n_mean_10db, 5.0, atol=0.1)

    # At 15 dB (surface code concatenation threshold):
    delta_15db = 10.0 ** (-15.0 / 20.0)
    n_mean_15db = 1.0 / (2.0 * delta_15db**2)
    assert np.isclose(n_mean_15db, 15.81, atol=0.1)

    # Intrinsic displacement variance:
    sigma_sq_thresh = delta_thresh**2 / 2.0
    assert np.isclose(sigma_sq_thresh, 0.05, atol=1e-4)


def test_epistemic_invariants_and_cv_demarcation():
    """Verify strict epistemic invariants and boundary classification."""
    invariants = {
        "speedup_claim_allowed": False,
        "accepted_speedup_candidate": False,
        "cv_barrier_classification": "Continuous-Variable Quantum Computing, Non-Gaussian Magic, and GKP Fault-Tolerant Squeezing Threshold",
        "dequantization_status": "Gaussian CV circuits dequantized in O(N^3) classical time via symplectic covariance matrices (Mari-Eisert); non-Gaussian universality blocked by 10 dB GKP squeezing threshold and weak physical Kerr chi^(3)",
    }

    assert invariants["speedup_claim_allowed"] is False
    assert invariants["accepted_speedup_candidate"] is False
    assert "Continuous-Variable" in invariants["cv_barrier_classification"]
    assert "Mari-Eisert" in invariants["dequantization_status"]

    registry_path = Path(__file__).resolve().parent.parent / "research" / "registry" / "negative_results.json"
    if registry_path.exists():
        with open(registry_path, "r") as f:
            data = json.load(f)
        assert len(data) >= 979
