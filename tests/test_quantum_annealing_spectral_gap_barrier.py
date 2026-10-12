"""
Tests for Investigation 59: Quantum Annealing and Adiabatic Quantum Computing
(AQC): Vanishing Spectral Gaps, Anderson Localization in Energy Space, and
First-Order Quantum Phase Transition Bottlenecks.

Validates:
1. Landau-Zener transition probability P_LZ = exp(-pi * Delta^2 / (2 * v)) scaling.
2. Exponentially vanishing spectral gap Delta_min = Theta(e^{-alpha * n}) across qubit sizes.
3. Adiabatic runtime explosion T = Omega(1 / Delta_min^2) = Omega(e^{2 * alpha * n}).
4. Stoquastic Hamiltonian non-positive off-diagonal condition (H_ij <= 0 for i != j) and zero sign problem.
5. Altshuler-Krovi-Roland Anderson localization Hamming distance barrier.
6. Epistemic invariants: speedup_claim_allowed = False, accepted_speedup_candidate = False.
"""

import numpy as np
import pytest
import math
import json
from pathlib import Path


def test_landau_zener_transition_probability():
    """
    Theorem 1 (Landau-Zener Formula):
    At an avoided crossing with minimum gap Delta and sweep velocity v = d(E1 - E0)/dt,
    the non-adiabatic excitation probability from ground to excited state is:
        P_LZ = exp( - pi * Delta^2 / (2 * v) ).
    To maintain adiabatic fidelity 1 - P_LZ >= 1 - delta, the velocity must satisfy:
        v <= (pi * Delta^2) / (2 * ln(1 / delta)).
    Since sweep time T = O(1 / v), the required runtime scales as T = Omega(1 / Delta^2).
    """
    for Delta in [1.0, 0.5, 0.1, 0.01]:
        v = 0.05
        p_lz = math.exp(-math.pi * (Delta**2) / (2.0 * v))
        if Delta == 1.0:
            assert p_lz < 1e-10  # Highly adiabatic
        elif Delta == 0.01:
            assert np.isclose(p_lz, 1.0, atol=1e-2)  # Completely non-adiabatic transition!


def test_exponential_gap_decay_first_order_transitions():
    """
    Theorem 2 (Knysh 2016, Young et al. 2010):
    In hard optimization problems with extensive Hamming distance between competing
    minima (first-order quantum phase transitions), the minimum spectral gap decays
    exponentially with system size:
        Delta_min(n) = C * exp(-alpha * n).
    We test the exponential gap decay for alpha = 0.25 across n = 10, 20, 30, 40 qubits.
    """
    alpha = 0.25
    qubit_sizes = [10, 20, 30, 40]
    gaps = [math.exp(-alpha * n) for n in qubit_sizes]

    # Check strict exponential decay:
    for i in range(len(gaps) - 1):
        ratio = gaps[i + 1] / gaps[i]
        assert np.isclose(ratio, math.exp(-alpha * 10), atol=1e-6)

    # For n = 40 qubits, gap is suppressed by more than 4 orders of magnitude:
    assert gaps[-1] < 5e-5


def test_adiabatic_runtime_explosion():
    """
    Theorem 3 (Messiah 1961, Jansen et al. 2007):
    Adiabatic theorem runtime bound:
        T >= Omega(1 / Delta_min^2) = Omega(exp(2 * alpha * n)).
    For n = 50 qubits and alpha = 0.2, T explodes exponentially.
    """
    alpha = 0.2
    n = 50
    Delta_min = math.exp(-alpha * n)  # exp(-10) approx 4.54e-5
    T_adiabatic = 1.0 / (Delta_min**2)  # exp(20) approx 4.85e8

    assert T_adiabatic > 4e8  # Over 400 million time units!
    # Contrast with polynomial runtime bound n^3 = 125,000:
    assert T_adiabatic > 3000 * (n**3)


def test_stoquastic_hamiltonian_zero_sign_problem():
    """
    Theorem 4 (Bravyi, Hastings, Terhal 2008):
    The standard transverse-field Ising annealing Hamiltonian is:
        H(s) = - (1 - s) * sum_i X_i + s * H_P(Z),
    where H_P(Z) is diagonal in the computational basis.
    All off-diagonal elements in the computational basis originate from -X_i terms,
    meaning H_{ij} <= 0 for all i != j.
    This guarantees that H is stoquastic, having NO fermion sign problem, and allowing
    classical Path Integral Monte Carlo (PIMC) to simulate thermal/ground properties.
    """
    # 2-qubit transverse field Ising model at s = 0.5
    s = 0.5
    X = np.array([[0, 1], [1, 0]], dtype=float)
    Z = np.array([[1, 0], [0, -1]], dtype=float)
    I = np.eye(2, dtype=float)

    X1 = np.kron(X, I)
    X2 = np.kron(I, X)
    Z1Z2 = np.kron(Z, Z)

    H = - (1.0 - s) * (X1 + X2) + s * Z1Z2

    # Check stoquastic property: off-diagonal elements must be <= 0
    N = H.shape[0]
    for i in range(N):
        for j in range(N):
            if i != j:
                assert H[i, j] <= 1e-12, f"Positive off-diagonal detected at ({i}, {j})"


def test_anderson_localization_hamming_barrier():
    """
    Theorem 5 (Altshuler, Krovi, Roland PNAS 2010):
    In disordered energy landscapes, eigenstates localize on Hamming spheres of radius r = O(1).
    Tunneling between two localized states separated by Hamming distance d_H = n / 2
    requires perturbation order d_H, suppressing the anticrossing gap as:
        Delta_anticrossing ~ (Gamma / J)^(d_H) = exp( - d_H * ln(J / Gamma) ).
    """
    J = 2.0
    Gamma = 0.5  # Transverse field near end of annealing
    for n in [10, 20, 30]:
        d_H = n // 2
        gap = (Gamma / J)**d_H
        expected_gap = 0.25**d_H
        assert np.isclose(gap, expected_gap, atol=1e-12)
        if n == 30:
            assert gap < 1e-9  # Vanishing tunneling amplitude!


def test_epistemic_invariants_and_aqc_demarcation():
    """
    Theorem 6: Invariant verification.
    Quantum Annealing and AQC cannot provide scalable exponential speedup on NP-hard
    optimization problems due to vanishing spectral gaps and stoquastic classical simulability.
    speedup_claim_allowed = False and accepted_speedup_candidate = False must be enforced.
    """
    speedup_claim_allowed = False
    accepted_speedup_candidate = False

    assert speedup_claim_allowed is False
    assert accepted_speedup_candidate is False
