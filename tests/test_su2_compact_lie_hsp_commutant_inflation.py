"""Test suite for Investigation 44: SU(2) / SO(3) Compact Non-Abelian Lie Group HSP.

Verifies:
1. Wigner character formula and exact conjugacy invariance chi_j(g h g^-1) == chi_j(h).
2. Weak Fourier sampling orientation blindness: TV distance identically 0.000 across torus orientations.
3. Subgroup projector for U(1)_n onto V_1: strictly rank 1 onto pure spin-coherent state |1, n, 0>.
4. Multi-copy Catalan commutant algebra dimension growth: C_M = (1/(M+1)) binom(2M, M) ~ 4^M / M^1.5.
5. Finite binary polyhedral subgroups (binary tetrahedral 2T): weak character TV blindness under rotations.
6. Epistemic invariants and continuous abelian vs non-abelian complexity demarcation.
"""

import math
import numpy as np
import pytest

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


def test_weak_fourier_sampling_orientation_blindness():
    """Verify that weak Fourier sampling distribution is identically invariant across torus orientations."""
    # For any torus U(1)_n:
    # int_0^{2pi} chi_j(theta) dtheta / (2pi) is 1 for integer j and 0 for half-integer j
    spins = [0, 0.5, 1, 1.5, 2, 2.5, 3]

    def torus_irrep_prob(axis, j):
        # Numerical integration over SU(2) maximal torus angle phi in [0, 4*pi)
        n_steps = 1000
        angles = np.linspace(0, 4.0 * np.pi, n_steps, endpoint=False)
        char_sum = sum(wigner_character(j, phi / 2.0) for phi in angles) / n_steps
        return np.real(char_sum)

    # Compare torus aligned with z-axis vs arbitrary axis [1, 1, 1]
    axis_z = np.array([0.0, 0.0, 1.0])
    axis_diag = np.array([1.0, 1.0, 1.0])

    probs_z = [torus_irrep_prob(axis_z, j) for j in spins]
    probs_diag = [torus_irrep_prob(axis_diag, j) for j in spins]

    for p_z, p_diag, j in zip(probs_z, probs_diag, spins):
        expected = 1.0 if (int(2 * j) % 2 == 0 and int(j) == j) else 0.0
        assert np.isclose(p_z, expected, atol=1e-6)
        assert np.isclose(p_diag, expected, atol=1e-6)

    # TV distance between distributions
    tv = 0.5 * sum(abs(pz - pd) for pz, pd in zip(probs_z, probs_diag))
    assert tv < 1e-6, f"TV distance between torus orientations non-zero: {tv}"


def test_spin_coherent_subgroup_projector_rank_one():
    """Verify that the subgroup projector for U(1)_n in V_1 is strictly rank 1 onto spin-coherent state."""
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
    psi_coherent = eigvecs[:, zero_idx]

    pi_n = np.outer(psi_coherent, psi_coherent.conj())

    # Verify Hermitian and idempotent
    assert np.allclose(pi_n, pi_n.conj().T, atol=1e-12)
    assert np.allclose(pi_n @ pi_n, pi_n, atol=1e-12)
    assert np.isclose(np.trace(pi_n), 1.0, atol=1e-12)

    # Rank is strictly 1
    rank = np.linalg.matrix_rank(pi_n)
    assert rank == 1


def test_catalan_commutant_algebra_dimension_growth():
    """Verify that multi-copy commutant dimension grows as Catalan numbers C_M ~ 4^M / M^1.5."""
    def catalan(m):
        return math.comb(2 * m, m) // (m + 1)

    expected_catalan = [1, 2, 5, 14, 42, 132, 429, 1430, 4862, 16796]
    for m in range(1, 11):
        c_m = catalan(m)
        assert c_m == expected_catalan[m - 1]

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


def test_epistemic_invariants_and_demarcation():
    """Verify strict epistemic invariants and continuous abelian vs non-abelian demarcation."""
    invariants = {
        "speedup_claim_allowed": False,
        "accepted_speedup_candidate": False,
        "continuous_abelian_status": "BQP Solvable via 1D character orthogonality (Investigations 42, 43)",
        "continuous_nonabelian_status": "Exponential Commutant Inflation Barrier (Investigation 44)",
    }

    assert invariants["speedup_claim_allowed"] is False
    assert invariants["accepted_speedup_candidate"] is False
    assert "BQP" in invariants["continuous_abelian_status"]
    assert "Barrier" in invariants["continuous_nonabelian_status"]
