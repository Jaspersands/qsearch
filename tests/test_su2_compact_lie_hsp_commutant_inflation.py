"""Retained SU(2) identities; the historical general HSP no-go was retracted.

Character identities and zero-weight projectors do not establish measurement
circuit lower bounds. Catalan dimensions below concern spin HALF, not spin one.
See test_nonabelian_barrier_scope_audit.py for actual countercontrols.
"""

import math
import numpy as np
import pytest
from theorems.nonabelian_barrier_scope_audit import commutant_dimension, collective_generators

# Pauli matrices
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)


def su2_matrix(axis, angle):
    """Generate SU(2) element from rotation axis and angle."""
    norm = np.linalg.norm(axis)
    n = axis / norm if norm > 1e-12 else np.array([0, 0, 1])
    return np.cos(angle / 2.0) * np.eye(2) - 1j * np.sin(angle / 2.0) * (n[0] * SX + n[1] * SY + n[2] * SZ)


def wigner_character(j, theta):
    """Weyl character formula for spin j: chi_j(theta) = sin((2j+1) theta) / sin(theta)."""
    if abs(theta) < 1e-10:
        return 2.0 * j + 1.0
    return np.sin((2.0 * j + 1.0) * theta) / np.sin(theta)


def test_wigner_character_formula_and_conjugacy_invariance():
    """Verify that Wigner characters are class functions and invariant under conjugation g h g^-1."""
    spins = [0, 0.5, 1, 1.5, 2, 2.5, 3]

    # Test random rotations
    g = su2_matrix(np.array([1.0, 2.0, 3.0]), 1.456)
    g_inv = g.conj().T

    for angle in [0.2, 0.8, 1.5, 2.3]:
        h = su2_matrix(np.array([0.0, 0.0, 1.0]), angle)
        ghg = g @ h @ g_inv

        # Class parameter theta = half-angle
        theta_h = angle / 2.0
        # Compute trace of conjugated element
        tr_ghg = np.trace(ghg)
        theta_ghg = np.arccos(np.clip(np.real(tr_ghg) / 2.0, -1.0, 1.0))

        assert np.isclose(theta_h, theta_ghg, atol=1e-10)

        for j in spins:
            c_orig = wigner_character(j, theta_h)
            c_conj = wigner_character(j, theta_ghg)
            assert np.isclose(c_orig, c_conj, atol=1e-10)


def test_torus_invariant_multiplicity_is_orientation_independent_not_a_probability_law():
    """Actually rotate generators; Haar projectors are not normalized irrep laws."""
    angles = np.linspace(0, 4*np.pi, 256, endpoint=False)
    for twice_spin in (1, 2):
        J = collective_generators(twice_spin, 1)
        traces = []
        for axis in (np.array([0., 0., 1.]), np.ones(3)/np.sqrt(3)):
            generator = sum(a*operator for a, operator in zip(axis, J))
            eigenvalues, eigenvectors = np.linalg.eigh(generator)
            phases = np.exp(-1j*angles[:, None]*eigenvalues).mean(axis=0)
            projector = (eigenvectors*phases) @ eigenvectors.conj().T
            assert np.allclose(projector @ projector, projector, atol=1e-12)
            assert np.trace(projector) == pytest.approx(0 if twice_spin == 1 else 1)
            traces.append(np.trace(projector))
        assert traces[0] == pytest.approx(traces[1])


def test_zero_weight_torus_subgroup_projector_rank_one():
    """Torus invariance selects zero weight, not an extremal coherent state."""
    # Spin-1 generators
    jz = np.diag([1.0, 0.0, -1.0])
    jx = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]]) / np.sqrt(2.0)
    jy = np.array([[0, -1j, 0], [1j, 0, -1j], [0, 1j, 0]]) / np.sqrt(2.0)

    # Choose arbitrary unit axis n
    axis = np.array([1.0, 2.0, 2.0]) / 3.0  # unit norm
    jn = axis[0] * jx + axis[1] * jy + axis[2] * jz

    # Projector onto U(1)_n: Pi = integral e^{-i theta jn} dtheta / 2pi
    # This is the projection onto the zero-eigenvalue eigenspace of jn
    eigvals, eigvecs = np.linalg.eigh(jn)

    # Find eigenvector with eigenvalue 0
    zero_idx = np.argmin(np.abs(eigvals))
    assert np.isclose(eigvals[zero_idx], 0.0, atol=1e-12)
    psi_zero_weight = eigvecs[:, zero_idx]

    pi_n = np.outer(psi_zero_weight, psi_zero_weight.conj())
    assert np.allclose(jn @ psi_zero_weight, 0, atol=1e-12)

    # Verify Hermitian and idempotent
    assert np.allclose(pi_n, pi_n.conj().T, atol=1e-12)
    assert np.allclose(pi_n @ pi_n, pi_n, atol=1e-12)
    assert np.isclose(np.trace(pi_n), 1.0, atol=1e-12)

    # Rank is strictly 1
    rank = np.linalg.matrix_rank(pi_n)
    assert rank == 1


def test_spin_half_not_spin_one_catalan_commutant_growth():
    """Tie Catalan arithmetic to the actual representation multiplicities."""
    def catalan(m):
        return math.comb(2 * m, m) // (m + 1)

    expected_catalan = [1, 2, 5, 14, 42, 132, 429, 1430, 4862, 16796]
    for m in range(1, 11):
        c_m = catalan(m)
        assert c_m == expected_catalan[m - 1]
        assert commutant_dimension(1, m) == c_m

    assert commutant_dimension(2, 2) == 3 != catalan(2)
    assert commutant_dimension(2, 3) == 15 != catalan(3)

    # Check asymptotic scaling 4^M / M^1.5
    for m in [5, 10, 15, 20]:
        c_m = catalan(m)
        approx = (4 ** m) / (math.sqrt(math.pi) * (m ** 1.5))
        ratio = c_m / approx
        assert 0.8 < ratio < 1.2, f"Catalan asymptotic mismatch at M={m}: {ratio}"

    # For M = 20, commutant dimension exceeds 6.5 billion
    assert catalan(20) > 6.5e9


def test_finite_binary_polyhedral_subgroups_weak_blindness():
    """Verify that finite binary tetrahedral subgroup 2T has rotation-invariant weak Fourier characters."""
    # 2T is of order 24. It consists of:
    # 8 elements of order 6, 8 elements of order 3, 6 elements of order 4, 1 element of order 2 (-I), 1 identity
    # Rotation angles in SU(2):
    # Order 1: theta = 0 (1 element)
    # Order 2: theta = pi (1 element, -I)
    # Order 3: theta = pi / 3 (8 elements)
    # Order 4: theta = pi / 2 (6 elements)
    # Order 6: theta = 2 pi / 3 (8 elements)

    angles_2t = [0.0] * 1 + [np.pi] * 1 + [np.pi / 3.0] * 8 + [np.pi / 2.0] * 6 + [2.0 * np.pi / 3.0] * 8
    assert len(angles_2t) == 24

    # Any rotation g in SU(2) conjugates each element, preserving its class angle theta!
    # Therefore, sum of characters over g H g^-1 is identical for all rotations g.
    spins = [0, 0.5, 1, 1.5, 2, 2.5, 3]
    for j in spins:
        char_sum = sum(wigner_character(j, theta) for theta in angles_2t) / 24.0
        # By McKay correspondence, char_sum is integer multiplicity of trivial rep
        assert np.isclose(char_sum, round(char_sum), atol=1e-10)


def test_countercheck_does_not_claim_an_optimal_hsp_receiver():
    from theorems.nonabelian_barrier_scope_audit import invariant_swap_control
    control = invariant_swap_control(4)
    assert control["gate_count"] == 2
    assert not control["arbitrary_optimal_HSP_measurement_compiled"]
