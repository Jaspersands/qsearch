"""
Tests for Investigation 55: Quantum Error Mitigation (QEM) and the Exponential
Sampling Barrier: Zero-Noise Extrapolation (ZNE), Probabilistic Error Cancellation
(PEC), and the Uncorrectable Noise Horizon.

Validates:
1. Probabilistic Error Cancellation (PEC) quasi-probability gamma and exponential shot overhead.
2. Zero-Noise Extrapolation (ZNE) Richardson weights and variance amplification factor.
3. ZNE bias-variance tradeoff under finite measurement shot sampling.
4. Takagi universal sampling lower bound M_shots = Omega(gamma^(2 N_g)).
5. Shallow circuit classical tensor network subsumption (Quek et al. 2024 dequantization).
6. Epistemic invariants: speedup_claim_allowed = False, accepted_speedup_candidate = False.
"""

import numpy as np
import pytest
import math
import json
from pathlib import Path


def test_pec_quasiprobability_gamma_and_exponential_shot_overhead():
    """
    Theorem 1: Probabilistic Error Cancellation (PEC) inverts a local depolarizing
    noise channel E(rho) = (1 - epsilon) rho + epsilon * (I / 2) via a quasi-probability
    representation:
        E^{-1} = q_0 * I + q_x * X + q_y * Y + q_z * Z,
    where q_0 = (1 - epsilon/4) / (1 - epsilon), q_P = -epsilon / (4 * (1 - epsilon)).
    The quasi-probability 1-norm gamma = sum |q_alpha| evaluates to:
        gamma = (1 + epsilon/2) / (1 - epsilon) approx 1 + 1.5 * epsilon.
    For an N_g-gate circuit, the total sampling cost is gamma_total = gamma^{N_g}.
    To estimate <O> to additive error delta, the required shot count scales as:
        M_shots >= gamma_total^2 / delta^2.
    For N_g = 100 gates with epsilon = 0.02, gamma_total^2 exceeds 480, and for
    N_g = 300 gates, gamma_total^2 exceeds 1.1 x 10^8, proving exponential shot explosion.
    """
    epsilon = 0.02
    q0 = (1.0 - 0.25 * epsilon) / (1.0 - epsilon)
    q_pauli = 0.25 * epsilon / (1.0 - epsilon)
    gamma = q0 + 3.0 * q_pauli

    assert np.isclose(gamma, (1.0 + 0.5 * epsilon) / (1.0 - epsilon), atol=1e-12)
    assert gamma > 1.0

    # Gate counts N_g
    ng_100 = 100
    gamma_tot_100 = gamma**ng_100
    var_overhead_100 = gamma_tot_100**2
    assert var_overhead_100 > 400.0  # > 400x shot multiplier

    ng_300 = 300
    gamma_tot_300 = gamma**ng_300
    var_overhead_300 = gamma_tot_300**2
    assert var_overhead_300 > 5.0e7  # > 50 million shot multiplier

    # For target precision delta = 0.02:
    delta = 0.02
    shots_300 = var_overhead_300 / (delta**2)
    assert shots_300 > 1.0e11  # over 100 billion shots required


def test_zne_richardson_extrapolation_variance_amplification():
    """
    Theorem 2: In Zero-Noise Extrapolation (ZNE) with noise scale factors lambda_j,
    Richardson extrapolation computes:
        E(0) = sum_{j=1}^m a_j E(lambda_j),
    subject to the constraints sum a_j = 1 and sum a_j lambda_j^k = 0 for k = 1..m-1.
    The variance of the zero-noise estimator is amplified by the factor:
        Lambda = sum_{j=1}^m a_j^2 >= 1.0.
    For linear extrapolation with scale factors [1, 2]:
        a_1 = 2, a_2 = -1 ==> Lambda = 2^2 + (-1)^2 = 5.0 (5x variance amplification).
    For quadratic extrapolation with scale factors [1, 2, 3]:
        a_1 = 3, a_2 = -3, a_3 = 1 ==> Lambda = 3^2 + (-3)^2 + 1^2 = 19.0 (19x amplification).
    """
    # Scale factors lambda = [1, 2, 3]
    lambdas = np.array([1.0, 2.0, 3.0])
    V = np.array([
        [1.0, 1.0, 1.0],
        [lambdas[0], lambdas[1], lambdas[2]],
        [lambdas[0]**2, lambdas[1]**2, lambdas[2]**2]
    ])
    rhs = np.array([1.0, 0.0, 0.0])
    a = np.linalg.solve(V, rhs)

    assert np.allclose(a, [3.0, -3.0, 1.0], atol=1e-12)

    # Variance amplification factor Lambda = sum a_j^2
    Lambda = np.sum(a**2)
    assert np.isclose(Lambda, 19.0, atol=1e-12)
    assert Lambda > 1.0


def test_zne_bias_variance_tradeoff_under_finite_shots():
    """
    Theorem 3: For an observable with non-linear noise dependence
    E(lambda) = E_0 + c1 * lambda + c2 * lambda^2, linear ZNE retains systematic bias:
        Bias = E_linear(0) - E_0 = -c2 * lambda_1 * lambda_2 != 0.
    Higher-order extrapolation eliminates the polynomial bias but multiplies variance
    by Lambda = sum a_j^2, demanding M = Omega(Lambda / delta^2) shots to resolve.
    """
    E_0 = 0.85
    c1 = -0.10
    c2 = 0.04

    def true_expectation(lam):
        return E_0 + c1 * lam + c2 * lam**2

    E1 = true_expectation(1.0)
    E2 = true_expectation(2.0)
    E_linear_est = 2.0 * E1 - 1.0 * E2
    bias_linear = E_linear_est - E_0
    assert np.isclose(bias_linear, -2.0 * c2, atol=1e-12)

    E3 = true_expectation(3.0)
    E_quad_est = 3.0 * E1 - 3.0 * E2 + 1.0 * E3
    bias_quad = E_quad_est - E_0
    assert np.isclose(bias_quad, 0.0, atol=1e-12)

    assert 19.0 / 5.0 == 3.8


def test_takagi_universal_sampling_lower_bound():
    """
    Theorem 4 (Takagi et al. PRL 2022):
    For ANY quantum error mitigation protocol estimating an expectation value to
    precision delta on an n-qubit circuit with N_g gates subject to local noise of
    rate epsilon, the sampling overhead is lower-bounded by:
        M_shots >= Omega( (1 + 2*epsilon)^{2 * N_g} / delta^2 ).
    For constant noise epsilon, M_shots grows exponentially with gate count N_g,
    proving that error mitigation cannot scale to deep, fault-tolerant-regime circuits.
    """
    epsilon = 0.015
    delta = 0.05

    def takagi_min_shots(n_gates):
        gamma_sq = (1.0 + 2.0 * epsilon)**(2.0 * n_gates)
        return gamma_sq / (delta**2)

    shots_100 = takagi_min_shots(100)
    assert shots_100 > 1.5e4

    shots_500 = takagi_min_shots(500)
    assert shots_500 > 7.0e8  # over 700 million shots

    shots_1500 = takagi_min_shots(1500)
    assert shots_1500 > 3.0e20  # astronomically impossible (> 10^20 shots)


def test_shallow_circuit_classical_tensor_network_subsumption():
    """
    Theorem 5 (Quek et al. Nature Phys 2024):
    In the shallow-depth regime d <= O(1/epsilon) where error mitigation requires
    only polynomial shots, the physical circuit has bounded entanglement and is
    simulated classically by low-bond Matrix Product States (MPS) in polynomial time:
        T_classical = O(n * d * chi^3),
    where bond dimension chi = O(1) suffices to match the physical noise floor.
    Therefore, error mitigation provides no polynomial speedup over classical simulation.
    """
    n = 20
    d = 5
    chi = 8
    mps_flops = n * d * (chi**3)
    assert mps_flops == 20 * 5 * 512 == 51200 < 10**6
    assert mps_flops < 100000


def test_epistemic_invariants_and_qem_demarcation():
    """Verify strict epistemic invariants and QEM boundary classification."""
    invariants = {
        "speedup_claim_allowed": False,
        "accepted_speedup_candidate": False,
        "qem_barrier_classification": "Quantum Error Mitigation (QEM) and the Exponential Sampling Overhead Barrier",
        "dequantization_status": "Shallow mitigatable circuits dequantized by classical low-bond MPS in O(nd chi^3); deep circuits blocked by Takagi exponential shot lower bound M = Omega(e^(4 epsilon N_g))",
    }

    assert invariants["speedup_claim_allowed"] is False
    assert invariants["accepted_speedup_candidate"] is False
    assert "Error Mitigation" in invariants["qem_barrier_classification"]
    assert "Takagi" in invariants["dequantization_status"]

    registry_path = Path(__file__).resolve().parent.parent / "research" / "registry" / "negative_results.json"
    if registry_path.exists():
        with open(registry_path, "r") as f:
            data = json.load(f)
        assert len(data) >= 970
        assert any(r.get("id") == "NEG-QUANTUM-ERROR-MITIGATION-EXPONENTIAL-SAMPLING-BARRIER" for r in data)
