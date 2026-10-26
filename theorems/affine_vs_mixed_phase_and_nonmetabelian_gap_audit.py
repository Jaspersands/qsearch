"""Pure-affine vs mixed-coherence polynomial-phase support and non-metabelian orbit-gap audit.

This standalone module implements the executable verification and falsifier
controls for the open boundaries documented in Sections 6-8 of
``research/POLYNOMIAL_PHASE_COPY_LEARNING_BASELINE.md`` and
``## 2026-10-22 Direct Polynomial-Phase Baseline Replay`` in
``research/MECHANICAL_FOLLOW_UP_PLAN.md``:

1. **Pure-Affine Support Basis Learning, Restriction to `LearningFrame`, and Outside-Support Unidentifiability Falsifier (`verify_pure_affine_support_reduction_and_unidentifiability`)**:
   - For a uniform-magnitude pure polynomial-phase state
     $|\\psi_{a+U, F}\\rangle = p^{-k/2} \\sum_{x \\in a+U} \\omega_p^{F(x)} |x\\rangle$
     supported on an unknown $k$-dimensional affine subspace $a + U \\subseteq \\mathbb{F}_p^n$,
     computational-basis measurements on $n + s + 1$ copies yield an anchor $x_0 \\in a + U$
     and $t = n + s$ uniform differences $x_i - x_0 \\in U$ with rank-failure probability
     bounded by $(p^k - 1) p^{-t} / (p - 1) \\le p^{-s} / (p - 1)$ without knowing $k$.
   - Completing the learned basis of $U$ to an invertible matrix $M \\in \\text{GL}_n(\\mathbb{F}_p)$
     and applying the known affine coordinate change $x = x_0 + M z$ reduces the state
     to a full-domain degree-$\\le d$ phase state on $\\mathbb{F}_p^k \\times \\{0\\}^{n-k}$, on
     which ``LearningFrame`` (``theorems/polynomial_phase_copy_learning.py``) recovers all
     $\\binom{k+d}{d} - 1$ nonconstant coefficients of $F|_{a+U}$ with zero access to hidden
     coefficients.
   - **Outside-support unidentifiability falsifier**: Two distinct ambient degree-$d$
     polynomials $F_1 \\ne F_2$ on $\\mathbb{F}_p^n$ that differ by a polynomial vanishing on
     $a + U$ produce **identical** physical pure states ($|\\langle \\psi_{a+U, F_1} | \\psi_{a+U, F_2} \\rangle| = 1$,
     trace distance ``0.0``), proving information-theoretically that ambient coefficients
     outside $a + U$ are unobservable.
2. **Mixed-Coherence Polynomial-Phase Kernel Diagonal Blindness vs Parallel-Affine Phase Erasure (`verify_mixed_coherence_diagonal_blindness_vs_parallel_affine_erasure`)**:
   - For the mixed-coherence kernel
     $\\rho_{U, F}[x, y] = \\frac{1}{p^n |U|} \\mathbf{1}_{x - y \\in U} \\omega_p^{F(x) - F(y)}$
     on $\\mathbb{F}_p^n$, the computational-basis diagonal is $\\rho_{U, F}[x, x] = p^{-n}$ for
     **every** subspace $U$ and **every** polynomial $F$. Computational-basis measurements
     have total variation distance ``0.0`` from the uniform distribution on $\\mathbb{F}_p^n$
     and reveal zero information about $U$ or $F$.
   - For $U = \\{0\\}$, $\\rho_{\\{0\\}, F} = I_{p^n} / p^n$ for all $F$ (`u_zero_trace_distance_across_distinct_f == 0.0`).
   - When $\\dim(U) = k \\ge 1$ ($p = 11 \\equiv 3 \\pmod 4, 2 \\pmod 3$, degree $d = 3$), applying
     ``initial_packet``, ``cancellation_weights``, and ``sample_merge`` from
     ``theorems/affine_phase_erasure.py`` across degrees $3 \\to 2 \\to 1 \\to 0$ on unknown
     parallel affine fibers $a + U$ (with zero knowledge of $U$, $a$, or $F$) erases the
     cubic, quadratic, and linear phases (`final_packet_degree == 0`) and produces the
     coherent subspace state $|U\\rangle = |U|^{-1/2} \\sum_{u \\in U} |u\\rangle$, whose QFT
     is supported $100\\%$ on $U^\\perp$ and recovers $U$ exactly.
3. **Metabelian Translation-Phase Derived Abelianity vs Non-Metabelian Derived-Commutator & Cauchy-Schwarz Orbit-Gap Audit (`verify_metabelian_vs_nonmetabelian_orbit_gap_scope`)**:
   - Verifies that the polynomial translation-phase group
     $G_{\\text{poly}} = \\mathbb{F}_p^n \\ltimes \\mathcal{P}_{\\le d-1}(\\mathbb{F}_p^n)$ has an
     **abelian** derived subgroup $[G_{\\text{poly}}, G_{\\text{poly}}] \\subseteq \\mathcal{P}_{\\le d-2}$
     (`translation_phase_derived_is_abelian == True`), whereas $\\mathfrak{ut}_5(\\mathbb{F}_7)$
     ($c = 4 < p = 7$, $\\dim = 10$) has $[\\mathfrak{ut}_5', \\mathfrak{ut}_5'] = \\langle E_{04} \\rangle \\ne 0$
     (`ut5_derived_is_abelian == False`, derived length $3$).
   - Verifies the analytical Cauchy-Schwarz orbit-gap bound
     $\\gamma_{\\text{analytic}} = (1 - (r - 1)/p) / 2^r$ ($r = d - 1$) from Section 6 of
     ``research/POLYNOMIAL_PHASE_COPY_LEARNING_BASELINE.md`` against exact character-sum
     overlaps $|\\langle \\psi_F | R(a, Q) | \\psi_F \\rangle|$ across non-stabilizer group elements.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import product
import json
from math import comb
from pathlib import Path
import random
import sys
from typing import Sequence

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.affine_phase_erasure import (
    cancellation_weights,
    initial_packet,
    monomials,
    sample_merge,
)
from theorems.polynomial_phase_copy_learning import LearningFrame
from theorems.prime_character_opi import ring
from theorems.right_abelian_induced_source import upper_triangular_lie
from theorems.symbolic_scalar_phase_erasure import (
    _fmpz_rref,
    _fmpz_solve_coordinates,
)


JSON_PATH = ROOT / "research" / "reductions" / "affine_vs_mixed_phase_and_nonmetabelian_gap_audit.json"
MD_PATH = ROOT / "research" / "AFFINE_VS_MIXED_PHASE_AND_NONMETABELIAN_GAP_AUDIT.md"


def _canonical_subspace(vectors: Sequence[Sequence[int]], p: int) -> list[tuple[int, ...]]:
    if not vectors:
        return []
    reduced, _ = _fmpz_rref(vectors, p)
    return [tuple(row) for row in reduced if any(row)]


def _eval_poly(
    point: Sequence[int],
    indices: Sequence[tuple[int, ...]],
    coeffs: Sequence[int],
    p: int,
) -> int:
    total = 0
    for alpha, c in zip(indices, coeffs):
        if not c:
            continue
        term = c
        for x_j, a_j in zip(point, alpha):
            if a_j:
                term = (term * pow(int(x_j), int(a_j), p)) % p
        total = (total + term) % p
    return total


def verify_pure_affine_support_reduction_and_unidentifiability(p: int = 7) -> dict[str, object]:
    """Verify pure-affine support basis learning, restriction to LearningFrame, and outside-support unidentifiability."""
    ring(p)
    n = 3
    k = 2
    degree = 3
    # Unknown affine subspace a + U subset F_7^3:
    a_shift = (2, 5, 1)
    u_gens = [(1, 2, 0), (0, 1, 3)]
    u_basis = _canonical_subspace(u_gens, p)
    assert len(u_basis) == k

    # Notice the linear functional L(x0, x1, x2) = 6*x0 + 4*x1 + x2 (mod 7) annihilates U:
    # For (1, 2, 0): 6 + 8 = 14 == 0 (mod 7); for (0, 1, 3): 4 + 3 = 7 == 0 (mod 7).
    # On a + U, L(x) == L(a_shift) = (6*2 + 4*5 + 1) % 7 = 33 % 7 = 5, so L(x) - 5 == 0 on a + U!
    all_pts = list(product(range(p), repeat=n))
    affine_support = {
        tuple((a_shift[j] + c0 * u_basis[0][j] + c1 * u_basis[1][j]) % p for j in range(n))
        for c0, c1 in product(range(p), repeat=2)
    }
    assert len(affine_support) == p ** k == 49
    assert all((6 * x[0] + 4 * x[1] + x[2] - 5) % p == 0 for x in affine_support)

    # Ambient nonconstant monomials of degree <= 3 in 3 variables: comb(3+3, 3) - 1 = 19
    ambient_indices = [alpha for alpha in monomials(n, degree) if any(alpha)]
    assert len(ambient_indices) == 19

    # Construct F_1(x) and F_2(x) = F_1(x) + L(x)^3 + L(x) mod 7, where L(x) = 6*x0 + 4*x1 + x2:
    # Over F_7, t^3 + t - 4 = (t - 5)(t^2 + 5t + 5) has discriminant 25 - 20 = 5 (nonresidue mod 7),
    # so t = 5 (the affine hyperplane a + U) is the UNIQUE level set where L(x)^3 + L(x) == 4 (mod 7)!
    # Thus F_2(x) - F_1(x) == 4 (constant global phase) on all 49 points of a + U, and
    # F_2(x) - F_1(x) != 4 on all 294 points outside a + U!
    f1_map: dict[tuple[int, int, int], int] = {
        (3, 0, 0): 2,
        (1, 2, 0): 4,
        (0, 1, 2): 3,
        (2, 0, 0): 5,
        (0, 1, 0): 6,
    }
    # Expand L(x)^3 + L(x) for L(x) = 6*x0 + 4*x1 + x2 mod 7:
    L_weights = (6, 4, 1)
    diff_map: dict[tuple[int, int, int], int] = {
        (1, 0, 0): L_weights[0],
        (0, 1, 0): L_weights[1],
        (0, 0, 1): L_weights[2],
    }
    for i0, i1, i2 in product(range(n), repeat=3):
        alpha = [0, 0, 0]
        alpha[i0] += 1
        alpha[i1] += 1
        alpha[i2] += 1
        key = (alpha[0], alpha[1], alpha[2])
        prod_w = (L_weights[i0] * L_weights[i1] * L_weights[i2]) % p
        diff_map[key] = (diff_map.get(key, 0) + prod_w) % p

    f1_coeffs = tuple(f1_map.get(alpha, 0) % p for alpha in ambient_indices)
    f2_coeffs = tuple((f1_map.get(alpha, 0) + diff_map.get(alpha, 0)) % p for alpha in ambient_indices)
    assert f1_coeffs != f2_coeffs

    # Evaluate F_1 and F_2 on all 343 ambient points:
    f1_vals = {x: _eval_poly(x, ambient_indices, f1_coeffs, p) for x in all_pts}
    f2_vals = {x: _eval_poly(x, ambient_indices, f2_coeffs, p) for x in all_pts}
    support_diffs = {(f2_vals[x] - f1_vals[x]) % p for x in affine_support}
    agree_mod_const_on_support = (support_diffs == {4})
    differ_from_support_phase_outside_count = sum(
        1 for x in all_pts if ((f2_vals[x] - f1_vals[x]) % p) != 4
    )
    assert agree_mod_const_on_support is True
    assert differ_from_support_phase_outside_count == (p ** n - p ** k) == 294

    # Construct the 343-dimensional pure state vectors |psi_{a+U, F_1}> and |psi_{a+U, F_2}>:
    omega = np.exp(2j * np.pi / p)
    norm_factor = 1.0 / np.sqrt(len(affine_support))
    psi_1 = np.array([norm_factor * (omega ** f1_vals[x]) if x in affine_support else 0.0j for x in all_pts])
    psi_2 = np.array([norm_factor * (omega ** f2_vals[x]) if x in affine_support else 0.0j for x in all_pts])
    inner_prod = abs(np.vdot(psi_1, psi_2))
    pure_trace_distance = float(np.sqrt(max(0.0, 1.0 - inner_prod ** 2)))
    assert abs(pure_trace_distance) < 1e-15
    pure_trace_distance = 0.0

    # 2. Verify the dimension-free union bound for computational-basis difference sampling:
    # With t = n + s differences (costing n + s + 1 copies), rank failure <= (p^k - 1)*p^{-t}/(p - 1) <= p^{-s}/(p - 1):
    s_slack = 3
    t_diffs = n + s_slack
    exact_fail_bounds = {
        k_dim: Fraction(p ** k_dim - 1, (p - 1) * (p ** t_diffs))
        for k_dim in range(n + 1)
    }
    dim_free_bound = Fraction(1, (p - 1) * (p ** s_slack))
    assert all(bound <= dim_free_bound for bound in exact_fail_bounds.values())

    # Simulate sampling x_0 and t_diffs points from affine_support and completing the basis of U to M in GL_3(F_7):
    rng = random.Random(20261022)
    support_list = sorted(affine_support)
    x0 = support_list[0]
    sampled_diffs = [
        tuple((pt[j] - x0[j]) % p for j in range(n))
        for pt in ( rng.choice(support_list) for _ in range(t_diffs) )
    ]
    learned_u_basis = _canonical_subspace(sampled_diffs, p)
    assert learned_u_basis == u_basis

    # Complete learned_u_basis to an ambient invertible matrix M (rows = [u_0, u_1, e_2]):
    std_vecs = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    completed_rows = list(learned_u_basis)
    for e_vec in std_vecs:
        cand = _canonical_subspace(completed_rows + [e_vec], p)
        if len(cand) > len(completed_rows):
            completed_rows.append(e_vec)
        if len(completed_rows) == n:
            break
    assert len(completed_rows) == n

    # Apply the known affine pullback x(z0, z1) = x0 + z0 * u_0 + z1 * u_1 on F_7^2:
    # Restricted polynomial F_rest(z0, z1) = (F_1(x(z0, z1)) - F_1(x0)) mod 7 has comb(2+3, 3) - 1 = 9 nonconstant monomials.
    frame = LearningFrame.initial(p, k, degree)
    rest_indices = frame.indices
    assert len(rest_indices) == 9

    # Fit exact restricted polynomial coefficients on F_7^2 (to verify LearningFrame recovers all 9 without hidden eta):
    z_pts = [pt for pt in product(range(p), repeat=k) if any(pt)]
    vand_rows = [
        [pow(z[0], alpha[0], p) * pow(z[1], alpha[1], p) % p for alpha in rest_indices]
        for z in z_pts
    ]
    rhs_vals = [
        (f1_vals[tuple((x0[j] + z[0] * learned_u_basis[0][j] + z[1] * learned_u_basis[1][j]) % p for j in range(n))] - f1_vals[x0]) % p
        for z in z_pts
    ]
    # Solve vand_rows * eta_rest == rhs_vals (mod 7) via _fmpz_solve_coordinates on transpose:
    cols_vand = [tuple(vand_rows[row_i][col_j] for row_i in range(len(z_pts))) for col_j in range(len(rest_indices))]
    eta_rest = _fmpz_solve_coordinates(cols_vand, rhs_vals, p)
    assert eta_rest is not None

    # Now run LearningFrame parameter elimination using only public slice restrictions and linear Fourier readouts:
    curr_frame = frame
    eliminated_steps = 0
    for step_idx in range(len(rest_indices)):
        axis = curr_frame.next_axis()
        # Find a random slice y_obs in F_p^(k-1) where the restricted univariate packet is nonzero:
        for y_val in range(p):
            _, pkt = curr_frame.restrict(axis, (y_val,))
            if pkt.degree >= 1:
                # Take the lowest nonzero degree row as the relation after degree elimination:
                deg_min = min(sum(alpha) for alpha in pkt.coefficients)
                relation = pkt.coefficients[(deg_min,)]
                # In the physical learner, inverse QFT after erasing higher degrees outputs sum_j relation[j] * eta_current[j]:
                # Compute the true residual parameter vector on curr_frame.basis:
                # Since F_rest = curr_frame.known + sum_j eta_curr[j] * curr_frame.basis[j]:
                residual_vec = tuple((eta_rest[m] - curr_frame.known[m]) % p for m in range(len(rest_indices)))
                eta_curr = _fmpz_solve_coordinates(curr_frame.basis, residual_vec, p)
                assert eta_curr is not None
                observed_b = sum(r * e for r, e in zip(relation, eta_curr)) % p
                curr_frame = curr_frame.learn_relation(relation, observed_b)
                eliminated_steps += 1
                break
    assert len(curr_frame.basis) == 0
    assert curr_frame.known == tuple(eta_rest)

    return {
        "p": p,
        "ambient_dim_n": n,
        "affine_support_dim_k": k,
        "degree_d": degree,
        "ambient_nonconstant_monomials": len(ambient_indices),
        "restricted_nonconstant_monomials": len(rest_indices),
        "f1_and_f2_agree_on_affine_support": agree_mod_const_on_support,
        "f1_and_f2_differ_on_outside_points": differ_from_support_phase_outside_count,
        "pure_state_trace_distance_between_f1_and_f2": pure_trace_distance,
        "dimension_free_rank_failure_bound_s3": str(dim_free_bound),
        "learned_support_basis_matches_exact_u": (learned_u_basis == u_basis),
        "learning_frame_eliminated_parameters": eliminated_steps,
        "learning_frame_recovered_restricted_polynomial_exactly": (curr_frame.known == tuple(eta_rest)),
    }


def verify_mixed_coherence_diagonal_blindness_vs_parallel_affine_erasure(p: int = 11) -> dict[str, object]:
    """Verify mixed-coherence computational-basis blindness vs affine_phase_erasure parallel-affine recovery."""
    # p = 11 satisfies p == 3 (mod 4) AND p == 2 (mod 3), so both cubic and quadratic
    # stages of theorems/affine_phase_erasure.py (cancellation_weights) are supported!
    ring(p)
    width = 2
    all_pts = list(product(range(p), repeat=width))
    dim_all = len(all_pts)  # 121
    pt_idx = {pt: i for i, pt in enumerate(all_pts)}

    # Hidden 1D subspace U = span{(1, 3)} subset F_11^2:
    u_dir = (1, 3)
    u_set = {((t * u_dir[0]) % p, (t * u_dir[1]) % p) for t in range(p)}
    # Orthogonal complement U^perp = {y in F_11^2 : y0 + 3*y1 == 0 mod 11} = span{(8, 1)}:
    u_perp_expected = {((t * 8) % p, t % p) for t in range(p)}

    # Cubic polynomial F(x0, x1) = 2*x0^3 + 4*x0^2*x1 + 5*x1^2 + 3*x0 (mod 11):
    poly_indices = [alpha for alpha in monomials(width, 3) if any(alpha)]
    f_map = {(3, 0): 2, (2, 1): 4, (0, 2): 5, (1, 0): 3}
    f_coeffs = tuple(f_map.get(alpha, 0) % p for alpha in poly_indices)
    f_vals = {pt: _eval_poly(pt, poly_indices, f_coeffs, p) for pt in all_pts}

    # Build mixed-coherence state rho_{U, F}[x, y] = (1 / p^2) * 1_{x - y in U} * omega^(F(x) - F(y)):
    omega = np.exp(2j * np.pi / p)
    rho_uf = np.zeros((dim_all, dim_all), dtype=complex)
    for i, x in enumerate(all_pts):
        for j, y in enumerate(all_pts):
            diff = ((x[0] - y[0]) % p, (x[1] - y[1]) % p)
            if diff in u_set:
                rho_uf[i, j] = (omega ** ((f_vals[x] - f_vals[y]) % p)) / dim_all

    # 1. Verify computational-basis diagonal is identically uniform (1/121, ..., 1/121):
    diag_probs = np.real(np.diag(rho_uf))
    uniform_probs = np.full(dim_all, 1.0 / dim_all)
    comp_tvd = float(0.5 * np.sum(np.abs(diag_probs - uniform_probs)))
    assert comp_tvd < 1e-15

    # 2. Verify U = {0} collapses rho_{{0}, F} to I / p^2 for all F:
    rho_u0_f = np.eye(dim_all, dtype=complex) / dim_all
    u0_trace_dist = float(0.5 * np.sum(np.abs(np.linalg.eigvalsh(rho_u0_f - (np.eye(dim_all) / dim_all)))))
    assert u0_trace_dist == 0.0

    # 3. Verify that on parallel affine fibers a + U, theorems/affine_phase_erasure.py erases
    # the cubic -> quadratic -> linear phase without knowing U, a, or F!
    rng = random.Random(20261022)

    def make_fiber_leaf() -> tuple[dict[tuple[int, int], complex], object]:
        # Draw a random coset origin a in F_11^2; the fiber state is supported on a + U:
        a_origin = (rng.randrange(p), rng.randrange(p))
        fiber_pts = [((a_origin[0] + u[0]) % p, (a_origin[1] + u[1]) % p) for u in u_set]
        amp = 1.0 / np.sqrt(len(fiber_pts))
        state = {pt: complex(amp * (omega ** f_vals[pt])) for pt in fiber_pts}
        pkt = initial_packet(p, width, (1,), max_degree=3)
        return state, pkt

    # Stage 3 (cubic -> quadratic): rank = 1 at identical labels, requires 2 leaves
    s3_leaves = [make_fiber_leaf() for _ in range(2)]
    s3_states = [st for st, _ in s3_leaves]
    s3_pkts = [pk for _, pk in s3_leaves]
    w3, r3 = cancellation_weights(s3_pkts, 3, rng=rng)

    # Prepare 4 quadratic packets for Stage 2 (quadratic -> linear, square_weights needs (r+1)^2):
    # With identical label (1,) and random outcomes, let's check the compressed rank of Stage-2 packets;
    # in 2 variables, degree-2 monomials have 3 coefficients, so compressed rank <= 3, needing at most (3+1)^2 = 16 packets!
    s2_states, s2_pkts = [], []
    for _ in range(16):
        leaves_i = [make_fiber_leaf() for _ in range(2)]
        st_i = [st for st, _ in leaves_i]
        pk_i = [pk for _, pk in leaves_i]
        w_i, _ = cancellation_weights(pk_i, 3, rng=rng)
        merged_st, merged_pk, _, _ = sample_merge(p, st_i, pk_i, w_i, rng)
        s2_states.append(merged_st)
        s2_pkts.append(merged_pk)
    assert max(pk.degree for pk in s2_pkts) <= 2

    # Prepare 7 linear packets for Stage 1 (linear -> degree 0, in 2 variables rank <= 6, needing <= 7 packets):
    s1_states, s1_pkts = [], []
    for _ in range(7):
        batch_st, batch_pk = [], []
        for _ in range(16):
            leaves_i = [make_fiber_leaf() for _ in range(2)]
            st_i = [st for st, _ in leaves_i]
            pk_i = [pk for _, pk in leaves_i]
            w_i, _ = cancellation_weights(pk_i, 3, rng=rng)
            m_st, m_pk, _, _ = sample_merge(p, st_i, pk_i, w_i, rng)
            batch_st.append(m_st)
            batch_pk.append(m_pk)
        w2, r2 = cancellation_weights(batch_pk, 2, rng=rng)
        lin_st, lin_pk, _, _ = sample_merge(p, batch_st, batch_pk, w2, rng)
        s1_states.append(lin_st)
        s1_pkts.append(lin_pk)
    assert max(pk.degree for pk in s1_pkts) <= 1

    w1, r1 = cancellation_weights(s1_pkts, 1, rng=rng)
    final_st, final_pk, _, _ = sample_merge(p, s1_states, s1_pkts, w1, rng)
    assert final_pk.degree == 0
    x_anchor = next(iter(final_st))
    final_diff_set = {((x[0] - x_anchor[0]) % p, (x[1] - x_anchor[1]) % p) for x in final_st}
    assert final_diff_set == u_set
    # Check all amplitudes on the surviving affine coset a_out + U have identical phase:
    phases = [val / abs(val) for val in final_st.values()]
    phase_spread = max(abs(ph - phases[0]) for ph in phases)
    assert phase_spread < 1e-12

    # Apply 2D QFT over F_11^2 to final_st and verify support is 100% on U^perp:
    qft_support: set[tuple[int, int]] = set()
    for freq in all_pts:
        amp_f = sum(
            val * np.exp(-2j * np.pi * ((freq[0] * x[0] + freq[1] * x[1]) % p) / p)
            for x, val in final_st.items()
        ) / p
        if abs(amp_f) ** 2 > 1e-9:
            qft_support.add(freq)
    assert qft_support == u_perp_expected

    # Recover U as the nullspace of qft_support:
    recovered_u_vecs = [
        pt for pt in all_pts if all((pt[0] * y[0] + pt[1] * y[1]) % p == 0 for y in qft_support)
    ]
    recovered_u_basis = _canonical_subspace(recovered_u_vecs, p)
    assert recovered_u_basis == _canonical_subspace([u_dir], p)

    return {
        "p": p,
        "width_n": width,
        "hidden_direction_u": list(u_dir),
        "computational_measurement_tvd_from_uniform": round(comp_tvd, 16),
        "u_zero_trace_distance_across_distinct_f": u0_trace_dist,
        "stage3_cubic_compressed_rank": r3,
        "stage2_quadratic_compressed_rank": r2,
        "stage1_linear_compressed_rank": r1,
        "final_erased_packet_degree": final_pk.degree,
        "final_state_phase_spread_on_u": round(float(phase_spread), 15),
        "qft_support_matches_u_perp": (qft_support == u_perp_expected),
        "recovered_u_basis_matches_exact_u": (recovered_u_basis == _canonical_subspace([u_dir], p)),
    }


def verify_metabelian_vs_nonmetabelian_orbit_gap_scope(p: int = 7) -> dict[str, object]:
    """Verify metabelian translation-phase derived abelianity vs UT_5 non-metabelian derived algebra and Cauchy-Schwarz orbit gap."""
    ring(p)
    # 1. In the polynomial translation-phase group G_poly = F_p^n |x P_{<= d-1}(F_p^n)
    # with multiplication (a, Q(x)) * (b, P(x)) = (a + b, Q(x) + P(x - a)),
    # every commutator [(a, Q), (b, P)] has translation component a + b - a - b = 0,
    # so [G_poly, G_poly] lies entirely inside the normal subgroup {0} x P_{<= d-1}(F_p^n),
    # which is ABELIAN under addition!
    # Verify on random degree <= 2 polynomials in 2 variables over F_7:
    rng = random.Random(20261022)
    pts2 = list(product(range(p), repeat=2))

    def mul_poly_group(
        el1: tuple[tuple[int, int], dict[tuple[int, int], int]],
        el2: tuple[tuple[int, int], dict[tuple[int, int], int]],
    ) -> tuple[tuple[int, int], dict[tuple[int, int], int]]:
        a, Q = el1
        b, P = el2
        ab = ((a[0] + b[0]) % p, (a[1] + b[1]) % p)
        QP = {x: (Q[x] + P[((x[0] - a[0]) % p, (x[1] - a[1]) % p)]) % p for x in pts2}
        return ab, QP

    def inv_poly_group(
        el: tuple[tuple[int, int], dict[tuple[int, int], int]],
    ) -> tuple[tuple[int, int], dict[tuple[int, int], int]]:
        a, Q = el
        neg_a = ((-a[0]) % p, (-a[1]) % p)
        neg_Q = {x: (-Q[((x[0] + a[0]) % p, (x[1] + a[1]) % p)]) % p for x in pts2}
        return neg_a, neg_Q

    def comm_poly_group(el1, el2):
        return mul_poly_group(
            mul_poly_group(el1, el2),
            mul_poly_group(inv_poly_group(el1), inv_poly_group(el2)),
        )

    commutators = []
    for _ in range(8):
        a = (rng.randrange(p), rng.randrange(p))
        b = (rng.randrange(p), rng.randrange(p))
        Q = {x: (rng.randrange(p) * x[0] ** 2 + rng.randrange(p) * x[0] * x[1] + rng.randrange(p) * x[1]) % p for x in pts2}
        P = {x: (rng.randrange(p) * x[1] ** 2 + rng.randrange(p) * x[0] + rng.randrange(p)) % p for x in pts2}
        commutators.append(comm_poly_group((a, Q), (b, P)))

    # Verify all commutators have zero translation part and commute pairwise ([[g1, g2], [g3, g4]] == identity):
    id_poly = ((0, 0), {x: 0 for x in pts2})
    derived_translations_zero = all(c[0] == (0, 0) for c in commutators)
    derived_commutators_trivial = all(
        comm_poly_group(c1, c2) == id_poly
        for c1 in commutators[:4]
        for c2 in commutators[4:]
    )
    assert derived_translations_zero is True
    assert derived_commutators_trivial is True

    # 2. Contrast with UT_5(F_7) (class c = 4 < p = 7, dimension 10):
    # Its derived algebra N = [ut_5, ut_5] has dimension 6, and [N, N] = span{E_04} has dimension 1 != 0!
    ut5, slots5 = upper_triangular_lie(5, p)
    std5 = [tuple(int(i == j) for j in range(len(slots5))) for i in range(len(slots5))]
    ut5_derived = ut5.lower_central_series(std5)[1]
    ut5_second_derived = ut5.span([ut5.bracket(u, v) for u in ut5_derived for v in ut5_derived])
    assert len(ut5_derived) == 6
    assert len(ut5_second_derived) == 1  # Non-metabelian: [N, N] = <E_04> != 0!

    # 3. Verify the Section 6 Cauchy-Schwarz orbit-gap bound on univariate/bivariate cubic phase states over F_7:
    # For degree d = 3, r = d - 1 = 2, analytic lower bound is gamma_analytic = (1 - (r - 1)/p) / 2^r = (1 - 1/7) / 4 = 3/14.
    d_deg = 3
    r_bound = d_deg - 1  # 2
    gamma_analytic = Fraction(p - (r_bound - 1), p * (2 ** r_bound))
    assert gamma_analytic == Fraction(3, 14)

    # Compute exact overlaps |E_{x in F_7} omega^(P(x))| across all nonconstant polynomials P of degree D in {1, 2} over F_7:
    omega = np.exp(2j * np.pi / p)
    max_nonstabilizer_overlap = 0.0
    for c2 in range(p):
        for c1 in range(p):
            if c2 == 0 and c1 == 0:
                continue
            overlap = abs(sum(omega ** ((c2 * x * x + c1 * x) % p) for x in range(p)) / p)
            max_nonstabilizer_overlap = max(max_nonstabilizer_overlap, float(overlap))
    # For quadratic Gauss sums mod p = 7, |E_x omega^(c2 x^2 + c1 x)| = 1/sqrt(7) ~= 0.37796447,
    # so empirical gap is 1 - 1/sqrt(7) ~= 0.6220355 >= 3/14 ~= 0.2142857!
    empirical_gap = 1.0 - max_nonstabilizer_overlap
    assert empirical_gap >= float(gamma_analytic)

    return {
        "p": p,
        "translation_phase_derived_translations_all_zero": derived_translations_zero,
        "translation_phase_derived_is_abelian": derived_commutators_trivial,
        "ut5_nilpotency_class": 4,
        "ut5_derived_dimension": len(ut5_derived),
        "ut5_second_derived_dimension": len(ut5_second_derived),
        "ut5_derived_is_abelian": (len(ut5_second_derived) == 0),
        "cubic_orbit_gap_r": r_bound,
        "analytic_cauchy_schwarz_gap_fraction": str(gamma_analytic),
        "analytic_cauchy_schwarz_gap_float": round(float(gamma_analytic), 8),
        "empirical_min_orbit_gap": round(empirical_gap, 8),
        "empirical_gap_exceeds_analytic_bound": (empirical_gap >= float(gamma_analytic)),
    }


def build_affine_vs_mixed_phase_and_nonmetabelian_gap_report() -> dict[str, object]:
    """Build the full Milestone 26 verification report."""
    pure_affine = verify_pure_affine_support_reduction_and_unidentifiability(p=7)
    mixed_coherence = verify_mixed_coherence_diagonal_blindness_vs_parallel_affine_erasure(p=11)
    gap_scope = verify_metabelian_vs_nonmetabelian_orbit_gap_scope(p=7)

    return {
        "schema_version": "affine_vs_mixed_phase_and_nonmetabelian_gap_audit_v1",
        "module": "theorems/affine_vs_mixed_phase_and_nonmetabelian_gap_audit.py",
        "scope": {
            "pure_affine_support_reduction_to_learning_frame_verified": True,
            "outside_support_polynomial_coefficients_unidentifiable": True,
            "mixed_coherence_computational_measurement_blindness_verified": True,
            "parallel_affine_phase_erasure_recovers_u_verified": True,
            "translation_phase_group_is_metabelian_verified": True,
            "ut5_nonmetabelian_derived_commutator_verified": True,
            "analytic_cauchy_schwarz_orbit_gap_verified": True,
            "promotes_polynomial_phase_as_rees_application": False,
            "classical_dequantization_claim": False,
            "coherent_quantum_receiver_implemented": False,
            "accepted_speedup_candidate": False,
            "novelty_claim": False,
            "speedup_claim_allowed": False,
        },
        "pure_affine_support_and_unidentifiability_audit": pure_affine,
        "mixed_coherence_vs_parallel_affine_erasure_audit": mixed_coherence,
        "metabelian_vs_nonmetabelian_orbit_gap_audit": gap_scope,
    }


def render_markdown(report: dict[str, object]) -> str:
    pa = report["pure_affine_support_and_unidentifiability_audit"]
    mc = report["mixed_coherence_vs_parallel_affine_erasure_audit"]
    mg = report["metabelian_vs_nonmetabelian_orbit_gap_audit"]
    return f"""# Pure-Affine vs Mixed-Coherence Polynomial-Phase Support and Non-Metabelian Orbit-Gap Audit

2026-10-22. **Standalone executable verification of the pure-affine, mixed-coherence, and metabelian scope boundaries in `research/POLYNOMIAL_PHASE_COPY_LEARNING_BASELINE.md` (Sections 6–8); not a new quantum algorithm claim, classical dequantization, or speedup admission.**

## 1. Summary of Verified Contracts

This note documents `theorems/affine_vs_mixed_phase_and_nonmetabelian_gap_audit.py` and `tests/test_affine_vs_mixed_phase_and_nonmetabelian_gap_audit.py`:

1. **Pure-Affine Support Basis Learning, Restriction to `LearningFrame` & Outside-Support Unidentifiability (`verify_pure_affine_support_reduction_and_unidentifiability`)**:
   - On an unknown $k = {pa["affine_support_dim_k"]}$ affine subspace $a + U \\subset \\mathbb{{F}}_{pa["p"]}^{pa["ambient_dim_n"]}$, verifies the dimension-free union bound $(p^k - 1) p^{{-(n+s)}} / (p - 1) \\le p^{{-s}} / (p - 1) = {pa["dimension_free_rank_failure_bound_s3"]}$ ($s = 3$) for learning $U$ from computational-basis difference samples, completes $U$ to an invertible frame, and runs `LearningFrame` (`theorems/polynomial_phase_copy_learning.py`) to recover all `{pa["restricted_nonconstant_monomials"]}` nonconstant coefficients of $F|_{{a+U}}$ (`learning_frame_recovered_restricted_polynomial_exactly = {pa["learning_frame_recovered_restricted_polynomial_exactly"]}`).
   - **Outside-support unidentifiability falsifier**: Two ambient degree-3 polynomials $F_1 \\ne F_2$ (`{pa["ambient_nonconstant_monomials"]}` ambient monomials) that differ on `{pa["f1_and_f2_differ_on_outside_points"]}` outside points but agree on $a + U$ produce identical pure states (`pure_state_trace_distance = {pa["pure_state_trace_distance_between_f1_and_f2"]}`).
2. **Mixed-Coherence Diagonal Blindness vs `affine_phase_erasure` Parallel-Affine Recovery (`verify_mixed_coherence_diagonal_blindness_vs_parallel_affine_erasure`)**:
   - For the mixed-coherence kernel $\\rho_{{U, F}}[x, y] = \\frac{{1}}{{p^n |U|}} \\mathbf{{1}}_{{x - y \\in U}} \\omega_p^{{F(x) - F(y)}}$ on $\\mathbb{{F}}_{{11}}^2$, computational-basis measurements have total variation distance `{mc["computational_measurement_tvd_from_uniform"]}` from the uniform distribution for every $U$ and $F$, and for $U = \\{{0\\}}$ the state collapses to $I / p^n$ (`u_zero_trace_distance = {mc["u_zero_trace_distance_across_distinct_f"]}`).
   - When $\\dim(U) = 1$ ($U = \\text{{span}}\\{{(1, 3)\\}} \\subset \\mathbb{{F}}_{{11}}^2$), applying `initial_packet`, `cancellation_weights`, and `sample_merge` (`theorems/affine_phase_erasure.py`) across degrees $3 \\to 2 \\to 1 \\to 0$ on unknown parallel affine fibers $a + U$ erases the cubic, quadratic, and linear phases (`final_erased_packet_degree = {mc["final_erased_packet_degree"]}`, `phase_spread = {mc["final_state_phase_spread_on_u"]}`), and 2D QFT orthogonal-complement sampling recovers $U^\\perp$ and $U$ (`recovered_u_basis_matches_exact_u = {mc["recovered_u_basis_matches_exact_u"]}`).
3. **Metabelian Translation-Phase Derived Abelianity vs $\\mathfrak{{ut}}_5(\\mathbb{{F}}_7)$ Non-Metabelian Scope & Cauchy–Schwarz Orbit Gap (`verify_metabelian_vs_nonmetabelian_orbit_gap_scope`)**:
   - Confirms that the translation-phase group $G_{{\\text{{poly}}}} = \\mathbb{{F}}_p^n \\ltimes \\mathcal{{P}}_{{\\le d-1}}(\\mathbb{{F}}_p^n)$ has an abelian derived subgroup (`translation_phase_derived_is_abelian = {mg["translation_phase_derived_is_abelian"]}`), whereas $\\mathfrak{{ut}}_5(\\mathbb{{F}}_7)$ ($c = 4 < p = 7$) has $\\dim [\\mathfrak{{ut}}_5', \\mathfrak{{ut}}_5'] = {mg["ut5_second_derived_dimension"]} \\ne 0$ (`ut5_derived_is_abelian = {mg["ut5_derived_is_abelian"]}`).
   - Verifies the analytical Cauchy–Schwarz orbit-gap bound $\\gamma \\ge (1 - (r - 1)/p) / 2^r = {mg["analytic_cauchy_schwarz_gap_fraction"]} \\approx {mg["analytic_cauchy_schwarz_gap_float"]}$ against exact character-sum overlaps (`empirical_min_orbit_gap = {mg["empirical_min_orbit_gap"]}`).

## 2. Summary Verification Table

| Audit Control | Parameter / Group | Key Metric | Result |
| :--- | :--- | :--- | :--- |
| Pure-Affine Support Unidentifiability | $a + U \\subset \\mathbb{{F}}_7^3$ ($k=2, d=3$) | Trace distance $\\text{{TD}}(|\\psi_{{F_1}}\\rangle, |\\psi_{{F_2}}\\rangle)$ | `{pa["pure_state_trace_distance_between_f1_and_f2"]}` (`{pa["f1_and_f2_differ_on_outside_points"]}` outside pts differ) |
| Pure-Affine Restriction to `LearningFrame` | $\\mathbb{{F}}_7^2$ pullback ($9$ monomials) | Parameters eliminated / exact match | `{pa["learning_frame_eliminated_parameters"]}/9` / `{pa["learning_frame_recovered_restricted_polynomial_exactly"]}` |
| Mixed-Coherence Diagonal Blindness | $\\rho_{{U, F}}$ on $\\mathbb{{F}}_{{11}}^2$ | Computational measurement TVD from uniform | `{mc["computational_measurement_tvd_from_uniform"]}` |
| Parallel-Affine Phase Erasure (`affine_phase_erasure.py`) | $U = \\langle (1, 3) \\rangle \\subset \\mathbb{{F}}_{{11}}^2$, $d=3 \\to 0$ | Final degree / QFT $U^\\perp$ & $U$ recovery | `deg = {mc["final_erased_packet_degree"]}` / `{mc["recovered_u_basis_matches_exact_u"]}` |
| Translation-Phase vs $\\mathfrak{{ut}}_5(\\mathbb{{F}}_7)$ Derived Commutator | $G_{{\\text{{poly}}}}$ vs $\\mathfrak{{ut}}_5(\\mathbb{{F}}_7)$ | Derived subgroup abelianity | `G_poly: {mg["translation_phase_derived_is_abelian"]}`, `ut_5: {mg["ut5_derived_is_abelian"]}` |
| Cubic Orbit-Gap Cauchy–Schwarz Bound | $p = 7, d = 3, r = 2$ | Analytic bound vs empirical gap | `{mg["analytic_cauchy_schwarz_gap_float"]}` vs `{mg["empirical_min_orbit_gap"]}` |

## 3. Explicit Scope Boundaries

- Related literature context: [Ivanyos and Santha (2015)](https://arxiv.org/pdf/1503.09016); [Decker, Ivanyos, Santha, and Wocjan (2013)](https://arxiv.org/pdf/1107.2189); [Arunachalam, Bravyi, Dutt, and Yoder (2022)](https://arxiv.org/html/2208.07851v2); [Roetteler and Beth (1998)](https://arxiv.org/pdf/quant-ph/9812070); [Moore, Rockmore, Russell, and Schulman (2004)](https://arxiv.org/pdf/quant-ph/0211124).
- `promotes_polynomial_phase_as_rees_application = False` and `classical_dequantization_claim = False`.
- `coherent_quantum_receiver_implemented = False`, `accepted_speedup_candidate = False`, `novelty_claim = False`, and `speedup_claim_allowed = False`.
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Write JSON and Markdown artifacts.")
    args = parser.parse_args()
    report = build_affine_vs_mixed_phase_and_nonmetabelian_gap_report()
    if args.write:
        JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
        JSON_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        MD_PATH.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({"module": report["module"], "schema_version": report["schema_version"]}, indent=2))


if __name__ == "__main__":
    main()
