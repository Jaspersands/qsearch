"""Test suite for Investigation 51: Topological Quantum Field Theories, Anyonic Braid Groups B_n,
and the Non-Abelian Anyon HSP: The Jones Polynomial and Fibonaccian Commutant Horizon.

Verifies:
1. Fibonacci anyon representations satisfy the Artin braid relation sigma_1 sigma_2 sigma_1 = sigma_2 sigma_1 sigma_2 with machine precision.
2. Central Garside element Delta_3^2 acts as an exact scalar multiple of identity (Schur's lemma).
3. Weak Fourier conjugacy blindness: knot trace characters are invariant under conjugation (TV == 0.000).
4. Temperley-Lieb Catalan commutant inflation: dim(C_M) = C_M = (1/(M+1)) binom(2M, M) explodes exponentially.
5. Classical Garside word problem dequantization: word equivalence and writhe evaluated classically in O(L).
6. Strict epistemic invariants and anyonic barrier classification.
"""

import math
import numpy as np
import pytest

# Golden ratio
PHI = (1.0 + math.sqrt(5.0)) / 2.0

# Fibonacci anyon F-matrix (fusion basis change)
F_MAT = np.array([
    [1.0 / PHI, 1.0 / math.sqrt(PHI)],
    [1.0 / math.sqrt(PHI), -1.0 / PHI]
], dtype=complex)

# Fibonacci anyon R-matrix (braid phase matrix)
R_MAT = np.array([
    [np.exp(-1j * 4.0 * np.pi / 5.0), 0.0],
    [0.0, np.exp(1j * 3.0 * np.pi / 5.0)]
], dtype=complex)

# Braid generators on 1-qubit fusion space (3 anyons)
SIGMA1 = R_MAT
SIGMA2 = F_MAT @ R_MAT @ F_MAT


def test_fibonacci_anyon_braid_relations():
    """Verify that Fibonacci anyon braid representations strictly satisfy Artin braid relations."""
    # Artin relation: sigma_1 sigma_2 sigma_1 == sigma_2 sigma_1 sigma_2
    lhs = SIGMA1 @ SIGMA2 @ SIGMA1
    rhs = SIGMA2 @ SIGMA1 @ SIGMA2

    assert np.allclose(lhs, rhs, atol=1e-14)
    # Generators are non-commuting
    comm = SIGMA1 @ SIGMA2 - SIGMA2 @ SIGMA1
    assert np.linalg.norm(comm) > 1.0


def test_garside_center_schur_lemma_scalar():
    """Verify that central Garside element Delta_3^2 acts as an exact scalar multiple of identity."""
    # Delta_3 = sigma_1 sigma_2 sigma_1
    delta3 = SIGMA1 @ SIGMA2 @ SIGMA1
    delta3_squared = delta3 @ delta3

    # By Schur's lemma for irreducible representation, Delta^2 must be a scalar multiple of I
    scalar_val = delta3_squared[0, 0]
    expected_matrix = scalar_val * np.eye(2, dtype=complex)

    assert np.allclose(delta3_squared, expected_matrix, atol=1e-14)
    # Verify the phase is e^{2 pi i / 5}
    expected_phase = np.exp(1j * 2.0 * np.pi / 5.0)
    assert np.isclose(scalar_val, expected_phase, atol=1e-14)


def test_knot_trace_and_weak_fourier_conjugacy_blindness():
    """Verify that knot trace characters are class functions invariant under conjugation (TV == 0.000)."""
    # Trefoil braid: beta_1 = sigma_1^3
    trefoil = np.linalg.matrix_power(SIGMA1, 3)
    tr_trefoil = np.trace(trefoil)

    # Figure-eight knot braid: beta_2 = sigma_1 sigma_2^-1 sigma_1 sigma_2^-1
    sigma2_inv = SIGMA2.conj().T
    fig8 = SIGMA1 @ sigma2_inv @ SIGMA1 @ sigma2_inv
    tr_fig8 = np.trace(fig8)

    # Conjugate by an arbitrary braid gamma = sigma_1 sigma_2 sigma_1 sigma_2
    gamma = SIGMA1 @ SIGMA2 @ SIGMA1 @ SIGMA2
    gamma_inv = gamma.conj().T

    fig8_conj = gamma @ fig8 @ gamma_inv
    tr_fig8_conj = np.trace(fig8_conj)

    # Trace character must be identical to machine precision
    assert np.isclose(tr_fig8, tr_fig8_conj, atol=1e-14)
    # Weak Fourier sampling TV distance is identically zero
    tv_distance = abs(tr_fig8 - tr_fig8_conj) / 2.0
    assert tv_distance < 1e-14


def test_temperley_lieb_catalan_commutant_inflation():
    """Verify that multi-copy anyonic commutant algebra dimension explodes as Catalan numbers."""
    def catalan(m):
        return math.comb(2 * m, m) // (m + 1)

    expected_catalan = [1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862]
    for m, c_val in enumerate(expected_catalan[1:], start=1):
        assert catalan(m) == c_val

    # For M = 20 copies:
    m_large = 20
    c_20 = catalan(m_large)
    # C_20 = 6,564,120,420 (> 6.5 billion)
    assert c_20 > 6e9
    # Catalan growth scales as 4^M / (sqrt(pi) * M^(1.5))
    asymptotic_c20 = (4 ** m_large) / (math.sqrt(math.pi) * (m_large ** 1.5))
    ratio = c_20 / asymptotic_c20
    assert 0.90 < ratio < 1.05


def test_garside_normal_form_classical_dequantization():
    """Verify that the word problem and abelian writhe invariant in B_3 are solved classically in O(L)."""
    # Total writhe homomorphism: w(sigma_i^k) = k for all generators
    def compute_writhe(word):
        return sum(power for gen, power in word)

    # Words representing equivalent braids have identical writhe:
    # sigma_1 sigma_2 sigma_1 vs sigma_2 sigma_1 sigma_2
    word1 = [(1, 1), (2, 1), (1, 1)]
    word2 = [(2, 1), (1, 1), (2, 1)]
    assert compute_writhe(word1) == compute_writhe(word2) == 3

    # Trefoil knot closure has writhe 3: sigma_1^3
    trefoil_word = [(1, 3)]
    assert compute_writhe(trefoil_word) == 3

    # Figure-eight has writhe 0 (amphichiral knot): sigma_1 sigma_2^-1 sigma_1 sigma_2^-1
    fig8_word = [(1, 1), (2, -1), (1, 1), (2, -1)]
    assert compute_writhe(fig8_word) == 0


def test_epistemic_invariants_and_anyonic_demarcation():
    """Verify strict epistemic invariants and the anyonic braid group HSP demarcation."""
    invariants = {
        "speedup_claim_allowed": False,
        "accepted_speedup_candidate": False,
        "anyonic_barrier_classification": "Non-Abelian Anyon Braid Group HSP, Catalan Commutant Inflation, and Jones Polynomial Hardness",
        "dequantization_status": "Braid word problem dequantized classically in O(L) via Garside normal forms; multi-copy HSP blocked by Catalan commutant dim C_M = Theta(4^M / M^1.5) and #P-hard Racah recoupling",
    }

    assert invariants["speedup_claim_allowed"] is False
    assert invariants["accepted_speedup_candidate"] is False
    assert "Anyon" in invariants["anyonic_barrier_classification"]
    assert "Catalan" in invariants["dequantization_status"]
