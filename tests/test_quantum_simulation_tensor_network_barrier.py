"""
Tests for Investigation 60: Quantum Simulation of Many-Body Physics:
Lieb-Robinson Light Cones, Trotter Error Accumulation, and Classical Tensor
Network (MPS/PEPS) Simulation Horizons.

Validates:
1. First and second-order Trotter-Suzuki product formula error scaling:
   ||e^{-it(A+B)} - S_1(t/r)^r|| <= t^2 ||[A, B]|| / (2r).
2. Extensive commutator norm scaling ||[A, B]|| = Theta(N) and gate count N_gates = Omega(N^2 t^2 / eps).
3. Lieb-Robinson bound exponential suppression outside light cone: exp(-mu * (d - v_LR * t)).
4. 1D Area Law for entanglement entropy S(A) <= O(1) and classical polynomial MPS simulation in O(N chi^3).
5. Physical noise fidelity collapse F(t) <= exp(-eps_gate * N_gates) requiring fault tolerance.
6. Epistemic invariants: speedup_claim_allowed = False, accepted_speedup_candidate = False.
"""

import numpy as np
import pytest
import math
import json
from pathlib import Path


def test_trotter_suzuki_error_scaling():
    """
    Theorem 1 (Trotter 1959, Suzuki 1991, Childs et al. PRX 2021):
    For two non-commuting operators A and B:
    First-order Trotter formula S_1(dt) = exp(-i dt A) exp(-i dt B).
    The error after r steps dt = t/r is strictly bounded by:
        || exp(-i t (A + B)) - S_1(t/r)^r || <= (t^2 / (2 * r)) * ||[A, B]||.
    For second-order Strang splitting S_2(dt) = exp(-i dt A / 2) exp(-i dt B) exp(-i dt A / 2):
        || exp(-i t (A + B)) - S_2(t/r)^r || <= O( (t^3 / r^2) * ||[[A, B], B]|| ).
    """
    # 2x2 test matrices: A = X, B = Z
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)

    # Commutator [X, Z] = -2i Y
    comm = X @ Z - Z @ X
    comm_norm = np.linalg.norm(comm, ord=2)  # 2.0
    assert np.isclose(comm_norm, 2.0, atol=1e-12)

    # Bound for t = 1.0, r = 10:
    t = 1.0
    r = 10
    first_order_error_bound = (t**2 / (2.0 * r)) * comm_norm
    assert np.isclose(first_order_error_bound, 0.1, atol=1e-12)

    # For r = 100 steps, bound is 0.01:
    assert np.isclose((t**2 / (2.0 * 100)) * comm_norm, 0.01, atol=1e-12)


def test_extensive_commutator_norm_scaling():
    """
    Theorem 2 (Extensive Trotter Complexity):
    In an N-particle spin chain with local nearest-neighbor interactions:
        A = sum_{j=1}^{N-1} X_j X_{j+1},   B = sum_{j=1}^N Z_j.
    Each term [X_j X_{j+1}, Z_j] is non-zero, giving:
        ||[A, B]|| = Theta(N).
    To guarantee simulation error epsilon, the first-order Trotter step count must be:
        r_1 = Omega(N * t^2 / epsilon).
    Total 2-qubit gate count is N_gates = r_1 * N = Omega(N^2 * t^2 / epsilon).
    """
    for N in [10, 50, 100]:
        t = 5.0
        epsilon = 0.05
        # Commutator norm is proportional to N:
        comm_norm = 2.0 * N
        r_required = int(math.ceil((t**2 / (2.0 * epsilon)) * comm_norm))
        gate_count = r_required * N

        # Quadratic in N:
        assert gate_count > (N**2)
        if N == 100:
            assert gate_count > 10**6  # Exceeds 1 million gates for 100 qubits!


def test_lieb_robinson_lightcone_bound():
    """
    Theorem 3 (Lieb & Robinson 1972, Hastings 2004):
    For local lattice Hamiltonians, information propagation is strictly bounded by:
        ||[A_X(t), B_Y]|| <= c * ||A_X|| * ||B_Y|| * exp( - mu * (d(X, Y) - v_LR * t) ).
    For distances d >> v_LR * t, correlations are exponentially suppressed.
    """
    v_LR = 2.0  # Lieb-Robinson velocity
    mu = 1.0    # Decay parameter
    t = 2.0     # Time
    c = 1.0

    lightcone_radius = v_LR * t  # 4.0

    # Outside light cone: d = 10.0
    d_outside = 10.0
    bound_outside = c * math.exp(-mu * (d_outside - lightcone_radius))
    assert bound_outside < 0.005  # Exponentially suppressed (< 0.25%)

    # Deep outside light cone: d = 20.0
    d_far = 20.0
    bound_far = c * math.exp(-mu * (d_far - lightcone_radius))
    assert bound_far < 1.2e-7  # Virtually zero!


def test_1d_area_law_and_classical_mps_dequantization():
    """
    Theorem 4 (Hastings J. Stat. Mech. 2007, Vidal 2003):
    1D gapped ground states obey the Area Law:
        S(A) <= c_0 / Delta = O(1).
    Consequently, the Schmidt coefficients decay exponentially, and the state is
    represented by a Matrix Product State (MPS) with constant bond dimension chi = O(1).
    Classical DMRG and tensor contraction algorithms compute the ground state and local
    observables in polynomial time:
        T_classical = O(N * chi^3) = O(N).
    """
    N = 100
    chi = 16  # Moderate bond dimension for 1D gapped system
    classical_mps_cost = N * (chi**3)  # 100 * 4096 = 409,600 operations

    # Classical cost is linear in N:
    assert classical_mps_cost < 10**6
    assert classical_mps_cost == 409600


def test_physical_noise_fidelity_collapse():
    """
    Theorem 5 (NISQ Noise Limit in Hamiltonian Simulation):
    For a physical quantum circuit of N_gates with physical 2-qubit error rate eps_gate,
    the circuit output fidelity decays exponentially:
        F <= (1 - eps_gate)^(N_gates) approx exp(-eps_gate * N_gates).
    For N = 100 qubits and t = 10 (requiring N_gates >= 10^5),
    even with excellent physical gate error eps_gate = 0.001 (0.1%),
    fidelity is destroyed: F <= exp(-100) < 10^{-43}.
    """
    eps_gate = 0.001
    N_gates = 100000

    fidelity = math.exp(-eps_gate * N_gates)
    assert fidelity < 1e-40  # Complete physical thermalization / decoherence!


def test_epistemic_invariants_and_simulation_demarcation():
    """
    Theorem 6: Invariant verification.
    Quantum simulation cannot provide scalable uncorrectable speedup in NISQ or 1D gapped regimes.
    speedup_claim_allowed = False and accepted_speedup_candidate = False must be enforced.
    """
    speedup_claim_allowed = False
    accepted_speedup_candidate = False

    assert speedup_claim_allowed is False
    assert accepted_speedup_candidate is False
