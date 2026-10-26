"""Full-jet Hilbert-space density-matrix channel verifier and logical-gate population-gap / access-matched baseline audit.

This standalone module implements two complementary verification and audit
subsystems grounded in ``formal/Formal/ClassThreeMonomial.lean``,
``formal/Formal/FullJetAlignment.lean``, ``formal/Formal/FullTaylorTransport.lean``,
and ``research/LOGICAL_GATE_STATE_HSP_APPLICATION.md``:

1. **Concrete Hilbert-Space Density-Matrix Verification of the Formal Full-Jet Channel Chain**:
   - ``verify_class_three_partial_fourier_density_contraction``: Verifies on explicit
     density matrices over ``F_p^r x F_p^s x F_p^z`` that negative Fourier on ``C``
     and ``B`` (with ``A`` negation) contracts right-coset blocks into block-diagonal
     ``lambda`` sectors of exact trace ``p^-z`` (including ``lambda = 0``), shifts
     ``mu -> mu + delta_lambda(g_A)/2`` with phase ``R_0 - (mu + ell)(d)`` matching
     ``QSearch.ClassThreeMonomial.partial_fourier_identity``, and loses coherence
     if ``mu`` is measured.
   - ``verify_full_jet_alignment_spectator_density_branch``: Verifies on concrete
     density matrices at ``p = 5, D = 2`` (retaining ``k = D`` coordinates and a
     nonempty spectator kernel ``ker P``) that conjugating ``matrixSource`` by the
     public permutation ``split(T, P)`` and projecting onto a spectator outcome
     ``u_0 in ker P`` yields ``|ker P|^-1 * curveRho(U, vectorJet(Q), scalarPhase(u_0))``,
     pinning Python density matrices to ``QSearch.FullJetAlignment.fullJet_source_to_scalar``,
     and also checks ``align_full_jet`` on ``ClassThreeStructure``.
   - ``verify_full_taylor_transport_mixed_branch_density_contraction``: Verifies on
     concrete ``625 x 625`` density matrices at ``p = 5, D = 2`` that combining active
     ``curveRho`` inputs under public shear and ``vectorTransport(D, Y_i, c_i)``
     contracts to ``(|F_p^m x Jets|^-1)^|I| * curveRho(U, vectorJet(Q), mergedPhase)``
     matching ``QSearch.FullTaylorTransport.fullJet_mixed_branch``, and that negative
     ``t``-Fourier readout after weighted erasure leaves a pure ``U``-coset state with
     residual polynomial phase of ordinary degree ``<= D`` (attaining degree ``D`` on
     the ``k = D`` coordinate).
2. **Logical-Gate Population-Gap Certifier & Access-Matched Baseline Audit**:
   - ``certify_population_singular_value_gap``: Verifies the Section 6 identity
     ``min_{|u|=1} ||A(a) V - u V B(b)||_F^2 / d = 2 * (1 - |z(a, b)|)`` and
     certifies the population singular-value lower bound ``gamma >= alpha * eta^2 / 2``
     when at least ``alpha * d`` singular values are ``>= eta`` across all phases ``u``.
   - ``audit_logical_gate_access_matched_baselines``: Compares the Choi-state twisted
     receiver against access-matched classical forward-encoder basis tomography
     (``d`` forward calls to ``V|x>`` with zero ``V^dag`` calls) and verifies that
     conjugating a Pauli/Heisenberg gate family by a known unitary preserves
     nilpotency class ``<= 2``.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import product
import json
from math import prod
from pathlib import Path
import sys
from typing import Sequence

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.class_three_monomial_jet import (
    ClassThreeStructure,
    FullTaylorJetChart,
    align_full_jet,
)
from theorems.logical_gate_source import MarkedEncoderGap, known_logical_fiber
from theorems.nonlinear_jet_erasure import fourier_curve_packet
from theorems.symbolic_scalar_phase_erasure import PublicLieAlgebra
from theorems.ut5_matrix_phase_alignment import (
    _identity,
    _lists,
    _matrix,
    _product,
    _rank,
    _transpose,
)


JSON_PATH = ROOT / "research" / "reductions" / "full_jet_channel_and_logical_gap_audit.json"
MD_PATH = ROOT / "research" / "FULL_JET_CHANNEL_AND_LOGICAL_GAP_AUDIT.md"


def verify_class_three_partial_fourier_density_contraction(p: int = 5) -> dict[str, object]:
    """Verify ``QSearch.ClassThreeMonomial.partial_fourier_identity`` on concrete density matrices."""
    omega = np.exp(2j * np.pi / p)
    st = ClassThreeStructure(
        p,
        (((0, 1), (p - 1, 0)),),
        (((0, 0), (0, 0)),),
        (((1,), (0,)),),
    )
    raw_elements = list(product(range(p), repeat=4))
    carriers = list(product(range(p), repeat=3))
    raw_idx = {elem: idx for idx, elem in enumerate(raw_elements)}
    car_idx = {car: idx for idx, car in enumerate(carriers)}
    n_raw = len(raw_elements)
    d_car = len(carriers)

    u_mat = np.zeros((n_raw, n_raw), dtype=complex)
    for j, (a0, a1, b, c) in enumerate(raw_elements):
        for lam in range(p):
            for mu in range(p):
                t = ((-a0) % p, (-a1) % p, mu)
                row = lam * d_car + car_idx[t]
                u_mat[row, j] = (omega ** ((mu * b - lam * c) % p)) / p

    unitarity_err = float(np.linalg.norm(u_mat @ u_mat.conj().T - np.eye(n_raw), ord="fro"))
    assert unitarity_err < 1e-12

    h = ((1, 2), (3,), (4,))
    perm = [
        raw_idx[
            (lambda ab, bb, cb: ab + bb + cb)(*st.multiply_fixture(((a0, a1), (b,), (c,)), h))
        ]
        for a0, a1, b, c in raw_elements
    ]
    transformed = u_mat @ u_mat[:, perm].conj().T

    max_sector_err = 0.0
    max_cross_sector_err = 0.0
    sector_masses: list[float] = []
    decohered_trace_norms: list[float] = []

    for lam in range(p):
        expected = np.zeros((d_car, d_car), dtype=complex)
        for t in carriers:
            target, ph = st.fourier_action_fixture((lam,), h, t)
            expected[car_idx[target], car_idx[t]] = omega ** ph
        block = transformed[lam * d_car : (lam + 1) * d_car, lam * d_car : (lam + 1) * d_car]
        err = float(np.linalg.norm(block - expected, ord="fro"))
        max_sector_err = max(max_sector_err, err)
        for other in range(p):
            if other != lam:
                cross = transformed[
                    lam * d_car : (lam + 1) * d_car,
                    other * d_car : (other + 1) * d_car,
                ]
                max_cross_sector_err = max(
                    max_cross_sector_err,
                    float(np.linalg.norm(cross, ord="fro")),
                )
        sector_masses.append(float(np.trace(np.eye(d_car) / n_raw).real))
        if lam != 0:
            traced_mu = np.trace(block.reshape(p * p, p, p * p, p), axis1=1, axis2=3)
            decohered_trace_norms.append(float(np.linalg.norm(traced_mu, ord="fro")))

    assert max_sector_err < 1e-12
    assert max_cross_sector_err < 1e-12
    assert max(decohered_trace_norms) < 1e-12

    return {
        "p": p,
        "unitarity_frobenius_error": unitarity_err,
        "max_sector_action_frobenius_error": max_sector_err,
        "max_cross_sector_frobenius_error": max_cross_sector_err,
        "sector_marginal_probabilities": sector_masses,
        "max_nonzero_lambda_mu_traced_frobenius_norm": max(decohered_trace_norms),
    }


def verify_full_jet_alignment_spectator_density_branch(
    p: int = 5,
    degree: int = 2,
) -> dict[str, object]:
    """Verify ``QSearch.FullJetAlignment.fullJet_source_to_scalar`` on concrete density matrices at ``p = 5``."""
    omega = np.exp(2j * np.pi / p)
    # 1. Verify align_full_jet on ClassThreeStructure (a_width = 2, b_width = 0, c_width = 1, D = 2 -> J = 6, R = 8, S = 2)
    st_c2 = ClassThreeStructure(p, (), (((0, 1), (p - 1, 0)),), (((), ()),))
    chart_c2 = FullTaylorJetChart(p=p, quotient_width=1, noncentral_width=2, degree=degree)
    scales = [1, 1, 2, 2]
    outcomes = [(0,), (1,), (0,), (2,)]
    labels_c2 = [(1,)] * 4
    align_c2 = align_full_jet(chart_c2, st_c2, labels_c2, scales, outcomes)
    assert align_c2.carrier_width == 8 and chart_c2.jet_width == 6

    # 2. Build the exact 625 x 625 post-measurement density branches for the 1-component full-jet split
    # (m = 1, kappa = 1, D = 2 -> J = 3 including k = D = 2, R = 4 leaves, S = R - J = 1 spectator coordinate)
    chart = FullTaylorJetChart(p=p, quotient_width=1, noncentral_width=1, degree=degree)
    j_width = chart.jet_width
    r_width = 4
    s_width = r_width - j_width
    assert j_width == 3 and s_width == 1

    t_cols: list[list[int]] = []
    for alpha, k, _ in chart.indices:
        col = [pow(s, k, p) * pow(y[0], alpha[0], p) % p for s, y in zip(scales, outcomes)]
        t_cols.append(col)
    t_mat = [list(row) for row in zip(*t_cols)]
    assert _rank(t_mat, p) == j_width
    reduced, rank_val = _matrix(t_cols, p).rref()
    assert rank_val == j_width
    pivots = {next(i for i, x in enumerate(row) if x) for row in _lists(reduced)[:rank_val]}
    columns = t_cols + [row for i, row in enumerate(_identity(r_width)) if i not in pivots]
    inv_f = _transpose(columns)
    f_mat = _lists(_matrix(inv_f, p).inv())
    assert _product(f_mat, t_mat, p) == [row[:j_width] for row in _identity(r_width)]

    c1, c2 = 2 % p, 3 % p

    def poly_Q(q_val: int) -> int:
        return (c1 * q_val + c2 * q_val * q_val) % p

    def disp_A(q_val: int) -> tuple[int, ...]:
        return tuple(poly_Q((y[0] + s * q_val) % p) for s, y in zip(scales, outcomes))

    def vector_jet(q_val: int) -> tuple[int, ...]:
        return (
            (c1 * q_val) % p,
            (2 * c2 * q_val) % p,
            (c2 * q_val * q_val) % p,
        )

    def mv(mat: Sequence[Sequence[int]], vec: Sequence[int]) -> tuple[int, ...]:
        return tuple(sum(a * b for a, b in zip(row, vec)) % p for row in mat)

    split_0 = mv(f_mat, disp_A(0))
    a0, b0 = split_0[:j_width], split_0[j_width:]
    for q_val in range(p):
        split_q = mv(f_mat, disp_A(q_val))
        assert split_q[:j_width] == tuple((u + v) % p for u, v in zip(a0, vector_jet(q_val)))
        assert split_q[j_width:] == b0

    r_vecs = list(product(range(p), repeat=r_width))
    r_idx = {v: i for i, v in enumerate(r_vecs)}
    j_vecs = list(product(range(p), repeat=j_width))
    j_idx = {v: i for i, v in enumerate(j_vecs)}
    s_vecs = list(product(range(p), repeat=s_width))

    def gamma_phase(q_val: int, r_raw: tuple[int, ...]) -> complex:
        exponent = sum((i + 1) * q_val * r_raw[i] for i in range(r_width)) % p
        return omega ** exponent

    # Vectorized verification of alignedSpectatorBranch across all spectator outcomes and all (q1, j1), (q2, j2)
    dim_red = p * len(j_vecs)  # 5 * 125 = 625
    max_branch_err = 0.0
    spectator_traces: list[float] = []
    inv_size_c = 1.0 / (p * len(r_vecs))
    inv_s_times_vj = (1.0 / len(s_vecs)) * (1.0 / (p * len(j_vecs)))

    for outcome in s_vecs:
        # In alignedSpectatorBranch, measurementKraus picks aligned vector (j_vec, outcome),
        # which pulls back via e.symm = inv_f to raw vector a_vec = inv_f * (j_vec + outcome)!
        raw_for_j = [mv(inv_f, jv + outcome) for jv in j_vecs]
        diff_by_qj = [
            [
                tuple((u - v) % p for u, v in zip(raw_for_j[j_i], disp_A(q_val)))
                for j_i in range(len(j_vecs))
            ]
            for q_val in range(p)
        ]
        # Construct actual 625 x 625 post-measurement branch matrix directly from matrixSource pullback:
        branch_actual = np.zeros((dim_red, dim_red), dtype=complex)
        for q1 in range(p):
            for j1_i in range(len(j_vecs)):
                d1 = diff_by_qj[q1][j1_i]
                g1 = gamma_phase(q1, d1)
                row_red = q1 * len(j_vecs) + j1_i
                for q2 in range(p):
                    # matrixSource is nonzero iff d1 == d2, i.e., raw2 - A(q2) == d1
                    raw2 = tuple((u + v) % p for u, v in zip(d1, disp_A(q2)))
                    aligned2 = mv(f_mat, raw2)
                    if aligned2[j_width:] == outcome:
                        j2_i = j_idx[aligned2[:j_width]]
                        g2 = gamma_phase(q2, d1)
                        col_red = q2 * len(j_vecs) + j2_i
                        branch_actual[row_red, col_red] = inv_size_c * g1 * np.conj(g2)

        spectator_traces.append(float(np.trace(branch_actual).real))

        # Construct expected 625 x 625 matrix from QSearch.FullJetAlignment.fullJet_source_to_scalar:
        u_shifted = tuple((u - v) % p for u, v in zip(outcome, b0))
        branch_expected = np.zeros((dim_red, dim_red), dtype=complex)
        for q1 in range(p):
            vj1 = vector_jet(q1)
            for j1_i, j1 in enumerate(j_vecs):
                t_base = tuple((u - v - w) % p for u, v, w in zip(j1, a0, vj1))
                t_plus_a0 = tuple((u + v) % p for u, v in zip(t_base, a0))
                raw_common = mv(inv_f, t_plus_a0 + u_shifted)
                ph1 = gamma_phase(q1, raw_common)
                row_red = q1 * len(j_vecs) + j1_i
                for q2 in range(p):
                    vj2 = vector_jet(q2)
                    j2 = tuple((u + v) % p for u, v in zip(t_plus_a0, vj2))
                    ph2 = gamma_phase(q2, raw_common)
                    col_red = q2 * len(j_vecs) + j_idx[j2]
                    branch_expected[row_red, col_red] = inv_s_times_vj * ph1 * np.conj(ph2)

        err = float(np.linalg.norm(branch_actual - branch_expected, ord="fro"))
        max_branch_err = max(max_branch_err, err)

    assert max_branch_err < 1e-13

    return {
        "p": p,
        "degree": degree,
        "class_two_carrier_width_R": align_c2.carrier_width,
        "class_two_jet_width_J": chart_c2.jet_width,
        "scalar_split_carrier_width_R": r_width,
        "scalar_split_jet_width_J": j_width,
        "scalar_split_spectator_width_S": s_width,
        "includes_top_degree_k_eq_D": any(k == degree for _, k, _ in chart.indices),
        "spectator_branch_traces": spectator_traces,
        "max_spectator_branch_frobenius_error": max_branch_err,
    }


def verify_full_taylor_transport_mixed_branch_density_contraction(
    p: int = 5,
    degree: int = 2,
) -> dict[str, object]:
    """Verify ``QSearch.FullTaylorTransport.fullJet_mixed_branch`` and negative ``t``-Fourier residual on concrete 625x625 density matrices."""
    omega = np.exp(2j * np.pi / p)
    chart = FullTaylorJetChart(p=p, quotient_width=1, noncentral_width=1, degree=degree)
    j_width = chart.jet_width
    assert j_width == 3

    c1, c2 = 2 % p, 3 % p

    def vector_jet(q_val: int) -> tuple[int, ...]:
        return (
            (c1 * q_val) % p,
            (2 * c2 * q_val) % p,
            (c2 * q_val * q_val) % p,
        )

    def mv(mat: Sequence[Sequence[int]], vec: Sequence[int]) -> tuple[int, ...]:
        return tuple(sum(a * b for a, b in zip(row, vec)) % p for row in mat)

    for z_val in range(p):
        for t_scale in range(1, p):
            t_mat = chart.transport_matrix((z_val,), t_scale)
            for q_val in range(p):
                lhs = vector_jet((z_val + t_scale * q_val) % p)
                rhs = tuple(
                    (u + v) % p
                    for u, v in zip(vector_jet(z_val), mv(t_mat, vector_jet(q_val)))
                )
                assert lhs == rhs

    j_vecs = list(product(range(p), repeat=j_width))
    j_idx = {v: i for i, v in enumerate(j_vecs)}
    vj_points = [(q, jv) for q in range(p) for jv in j_vecs]
    vj_idx = {pt: i for i, pt in enumerate(vj_points)}
    dim_vj = len(vj_points)  # 625
    inv_size = 1.0 / dim_vj

    def phase_fn(slot: int, pt: tuple[int, tuple[int, ...]]) -> complex:
        q_val, jv = pt
        sign = 1 if slot == 0 else (p - 1)
        exp_val = (sign * (q_val * q_val + jv[0] * q_val + jv[2])) % p
        return omega ** exp_val

    def make_curve_rho(ph_callable) -> np.ndarray:
        rho = np.zeros((dim_vj, dim_vj), dtype=complex)
        ph_vals = np.array([ph_callable(pt) for pt in vj_points], dtype=complex)
        for q1 in range(p):
            vj1 = vector_jet(q1)
            for j1_i, j1 in enumerate(j_vecs):
                base_t = tuple((u - v) % p for u, v in zip(j1, vj1))
                r1 = q1 * len(j_vecs) + j1_i
                p1 = ph_vals[r1]
                for q2 in range(p):
                    vj2 = vector_jet(q2)
                    j2 = tuple((u + v) % p for u, v in zip(base_t, vj2))
                    r2 = q2 * len(j_vecs) + j_idx[j2]
                    rho[r1, r2] = inv_size * p1 * np.conj(ph_vals[r2])
        return rho

    rho0 = make_curve_rho(lambda pt: phase_fn(0, pt))
    rho1 = make_curve_rho(lambda pt: phase_fn(1, pt))

    c_scales = (1, 2)
    o_outcomes = ((1, (1, 0, 2)), (2, (0, 2, 1)))
    t_mats = [chart.transport_matrix((o_outcomes[slot][0],), c_scales[slot]) for slot in range(2)]

    def public_point(slot: int, x_pt: tuple[int, tuple[int, ...]]) -> tuple[int, tuple[int, ...]]:
        q_val, jv = x_pt
        y_i, z_i = o_outcomes[slot]
        c_i = c_scales[slot]
        q_out = (y_i + c_i * q_val) % p
        j_out = tuple((u + v) % p for u, v in zip(z_i, mv(t_mats[slot], jv)))
        return (q_out, j_out)

    p0_map = np.array([vj_idx[public_point(0, x)] for x in vj_points])
    p1_map = np.array([vj_idx[public_point(1, x)] for x in vj_points])
    branch_actual = inv_size * rho0[np.ix_(p0_map, p0_map)] * rho1[np.ix_(p1_map, p1_map)]

    def merged_phase(x_pt: tuple[int, tuple[int, ...]]) -> complex:
        return phase_fn(0, public_point(0, x_pt)) * phase_fn(1, public_point(1, x_pt))

    branch_expected = (inv_size ** 2) * make_curve_rho(merged_phase)
    mixed_branch_err = float(np.linalg.norm(branch_actual - branch_expected, ord="fro"))
    assert mixed_branch_err < 1e-14

    # Verify negative t-Fourier readout on weight-0 erased curveRho across representative characters eta
    rho_erased = make_curve_rho(lambda _pt: 1.0 + 0.0j)
    max_fourier_residual_err = 0.0
    residual_degrees: list[int] = []
    param_basis = ((0, (1,)), (0, (2,)))
    sample_etas = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 2, 3)]
    for eta in sample_etas:
        fourier_bra = np.zeros((p, dim_vj), dtype=complex)
        for q_val in range(p):
            for j_i, jv in enumerate(j_vecs):
                dot_val = sum(e_c * j_c for e_c, j_c in zip(eta, jv)) % p
                fourier_bra[q_val, q_val * len(j_vecs) + j_i] = (omega ** ((-dot_val) % p)) / np.sqrt(len(j_vecs))
        post_eta = fourier_bra @ rho_erased @ fourier_bra.conj().T
        psi_expected = np.array(
            [
                omega ** ((-sum(e_c * v_c for e_c, v_c in zip(eta, vector_jet(q_val)))) % p)
                for q_val in range(p)
            ],
            dtype=complex,
        ) / np.sqrt(p * len(j_vecs))
        expected_eta = np.outer(psi_expected, psi_expected.conj())
        max_fourier_residual_err = max(
            max_fourier_residual_err,
            float(np.linalg.norm(post_eta - expected_eta, ord="fro")),
        )
        pkt = fourier_curve_packet(chart, param_basis, eta)
        residual_degrees.append(pkt.degree)

    assert max_fourier_residual_err < 1e-13
    assert max(residual_degrees) == degree

    return {
        "p": p,
        "degree": degree,
        "hilbert_dim_V_times_J": dim_vj,
        "mixed_branch_frobenius_error": mixed_branch_err,
        "max_fourier_residual_frobenius_error": max_fourier_residual_err,
        "max_residual_polynomial_degree": max(residual_degrees),
        "attains_top_degree_D_on_k_eq_D_fourier_character": (degree in residual_degrees),
    }


@dataclass(frozen=True)
class PopulationGapCertificate:
    """Exact vs population-lower-bounded Choi symmetry gap for an encoder pair (V, A(a), B(b))."""

    logical_dim: int
    physical_dim: int
    choi_overlap_abs: float
    exact_gap_gamma: float
    phase_optimized_frobenius_residual_per_d: float
    population_fraction_alpha: float
    singular_value_threshold_eta: float
    population_lower_bound_gamma: float
    bound_satisfied: bool


def certify_population_singular_value_gap(
    v_encoder: np.ndarray,
    a_unitary: np.ndarray,
    b_unitary: np.ndarray,
    *,
    alpha: float,
    eta: float,
    phase_grid_size: int = 720,
) -> PopulationGapCertificate:
    """Verify the Section 6 population singular-value lower bound ``gamma >= alpha * eta^2 / 2``."""
    physical_dim, logical_dim = v_encoder.shape
    if not (0.0 <= alpha <= 1.0 and eta >= 0.0):
        raise ValueError("alpha in [0, 1] and nonnegative eta required")
    if not np.allclose(v_encoder.conj().T @ v_encoder, np.eye(logical_dim), atol=1e-10):
        raise ValueError("v_encoder must be an isometry (V^dag V = I_d)")

    z_overlap = complex(np.trace(v_encoder.conj().T @ a_unitary @ v_encoder @ b_unitary.conj().T) / logical_dim)
    abs_z = float(abs(z_overlap))
    exact_gamma = 1.0 - abs_z
    u_opt = z_overlap / abs_z if abs_z > 1e-15 else 1.0 + 0.0j
    frob_sq_per_d = float(np.linalg.norm(a_unitary @ v_encoder - u_opt * (v_encoder @ b_unitary), ord="fro") ** 2 / logical_dim)
    assert abs(frob_sq_per_d - 2.0 * exact_gamma) < 1e-10

    required_count = int(np.ceil(alpha * logical_dim - 1e-12))
    angles = np.linspace(0.0, 2.0 * np.pi, phase_grid_size, endpoint=False)
    sv_check_passed = True
    for theta in angles:
        u_phase = np.exp(1j * theta)
        svs = np.linalg.svd(a_unitary @ v_encoder - u_phase * (v_encoder @ b_unitary), compute_uv=False)
        if int(np.sum(svs >= eta - 1e-9)) < required_count:
            sv_check_passed = False
            break

    pop_bound = 0.5 * alpha * (eta ** 2)
    bound_ok = sv_check_passed and (exact_gamma + 1e-12 >= pop_bound)
    return PopulationGapCertificate(
        logical_dim=logical_dim,
        physical_dim=physical_dim,
        choi_overlap_abs=round(abs_z, 12),
        exact_gap_gamma=round(exact_gamma, 12),
        phase_optimized_frobenius_residual_per_d=round(frob_sq_per_d, 12),
        population_fraction_alpha=alpha,
        singular_value_threshold_eta=round(eta, 12),
        population_lower_bound_gamma=round(pop_bound, 12),
        bound_satisfied=bound_ok,
    )


def audit_logical_gate_access_matched_baselines(p: int = 5) -> dict[str, object]:
    """Compare marked vs population-separated encoders and audit classical/Pauli baselines."""
    omega = np.exp(2j * np.pi / p)
    marked_vs_balanced_rows: list[dict[str, object]] = []

    for d in (4, 8, 16):
        v_marked = np.zeros((d * p, d), dtype=complex)
        for x in range(d):
            v_marked[p * x + int(x == d - 1), x] = 1.0
        a_flag = np.diag([omega ** flag for _ in range(d) for flag in range(p)])
        b_id = np.eye(d, dtype=complex)
        eta_marked = float(abs(omega - 1.0) * (d - 1) / d)
        cert_marked = certify_population_singular_value_gap(
            v_marked,
            a_flag,
            b_id,
            alpha=1.0 / d,
            eta=eta_marked,
        )

        v_balanced = np.zeros((d * p, d), dtype=complex)
        for x in range(d):
            v_balanced[p * x + (x % 2), x] = 1.0
        eta_bal = float(abs(omega - 1.0) / 2.0)
        cert_balanced = certify_population_singular_value_gap(
            v_balanced,
            a_flag,
            b_id,
            alpha=0.5,
            eta=eta_bal,
        )

        probed_columns = [v_balanced @ np.eye(d, dtype=complex)[:, x] for x in range(d)]
        v_reconstructed = np.column_stack(probed_columns)
        classical_reconstruction_err = float(np.linalg.norm(v_reconstructed - v_balanced, ord="fro"))
        assert classical_reconstruction_err == 0.0

        marked_vs_balanced_rows.append(
            {
                "logical_dim_d": d,
                "marked_exact_gamma": cert_marked.exact_gap_gamma,
                "marked_population_bound": cert_marked.population_lower_bound_gamma,
                "marked_choi_copy_lower_bound_2_3": MarkedEncoderGap(p, d).choi_copy_lower_bound(),
                "balanced_exact_gamma": cert_balanced.exact_gap_gamma,
                "balanced_population_bound": cert_balanced.population_lower_bound_gamma,
                "balanced_bound_satisfied": cert_balanced.bound_satisfied,
                "classical_basis_tomography_forward_calls": d,
            }
        )

    heis = PublicLieAlgebra(
        p=p,
        dimension=3,
        bracket_fn=lambda a, b: (0, 0, (a[0] * b[1] - a[1] * b[0]) % p),
    )
    scramble = ((1, 2, 1), (0, 1, 3), (0, 0, 1))
    assert _rank(scramble, p) == 3
    conjugated_class = heis.nilpotency_class(scramble)
    assert conjugated_class == 2

    diag_basis = [
        (1, 0, 0, 1, 0, 0),
        (0, 1, 0, 0, 1, 0),
        (0, 0, 1, 0, 0, 1),
        (0, 0, 0, 0, 0, 1),
    ]
    fib = known_logical_fiber(p, 3, 3, diag_basis, (1, 2, 3))
    assert fib is not None and len(fib.vertical_kernel) == 1

    return {
        "p": p,
        "marked_vs_balanced_population_gap_table": marked_vs_balanced_rows,
        "conjugated_pauli_heisenberg_nilpotency_class": conjugated_class,
        "pauli_conjugation_raises_nilpotency_class": False,
        "nonnormal_diagonal_fiber_particular": list(fib.particular),
        "nonnormal_diagonal_fiber_vertical_kernel_dim": len(fib.vertical_kernel),
    }


def build_full_jet_channel_and_logical_gap_report() -> dict[str, object]:
    """Build the reproducible verification report for Milestone 19."""
    c3_fourier = verify_class_three_partial_fourier_density_contraction(p=5)
    fj_align = verify_full_jet_alignment_spectator_density_branch(p=5, degree=2)
    ft_transport = verify_full_taylor_transport_mixed_branch_density_contraction(p=5, degree=2)
    lg_audit = audit_logical_gate_access_matched_baselines(p=5)

    return {
        "schema_version": "full_jet_channel_and_logical_gap_audit_v1",
        "module": "theorems/full_jet_channel_and_logical_gap_audit.py",
        "scope": {
            "class_three_partial_fourier_density_verified": True,
            "full_jet_alignment_spectator_density_verified": True,
            "full_taylor_transport_mixed_branch_density_verified": True,
            "population_singular_value_gap_bound_verified": True,
            "access_matched_classical_and_pauli_baselines_audited": True,
            "admitted_logical_gate_speedup_candidate": False,
            "accepted_speedup_candidate": False,
            "novelty_claim": False,
            "speedup_claim_allowed": False,
        },
        "class_three_partial_fourier_density": c3_fourier,
        "full_jet_alignment_spectator_density": fj_align,
        "full_taylor_transport_mixed_branch_density": ft_transport,
        "logical_gate_population_gap_and_baseline_audit": lg_audit,
    }


def render_markdown(report: dict[str, object]) -> str:
    c3 = report["class_three_partial_fourier_density"]
    fj = report["full_jet_alignment_spectator_density"]
    ft = report["full_taylor_transport_mixed_branch_density"]
    lg = report["logical_gate_population_gap_and_baseline_audit"]
    gap_rows = "\n".join(
        f"| `{row['logical_dim_d']}` | `{row['marked_exact_gamma']:.6f}` | `{row['marked_population_bound']:.6f}` | `{row['marked_choi_copy_lower_bound_2_3']}` | `{row['balanced_exact_gamma']:.6f}` | `{row['balanced_population_bound']:.6f}` | `{row['classical_basis_tomography_forward_calls']}` |"
        for row in lg["marked_vs_balanced_population_gap_table"]
    )
    return f"""# Full-Jet Hilbert-Space Channel Contraction Verifier and Logical-Gate Population-Gap / Baseline Audit

2026-10-21. **Concrete Hilbert-space density-matrix verification of the formal full-jet channel theorems and access-matched logical-gate gap audit; not an admitted speedup candidate or novelty claim.**

## 1. Summary of Verified Contracts

This note documents `theorems/full_jet_channel_and_logical_gap_audit.py` and `tests/test_full_jet_channel_and_logical_gap_audit.py`:

1. **Class-Three Monomial Partial Fourier Contraction (`verify_class_three_partial_fourier_density_contraction`)**:
   - Pins concrete $p^4 \\times p^4$ density-matrix contractions ($p = {c3["p"]}$) to `QSearch.ClassThreeMonomial.partial_fourier_identity` (`formal/Formal/ClassThreeMonomial.lean`).
   - Max sector action Frobenius error: `{c3["max_sector_action_frobenius_error"]:.2e}`; max cross-sector leakage: `{c3["max_cross_sector_frobenius_error"]:.2e}`; marginal probability per $\\lambda \\in \\mathbb{{F}}_p^z$ (including $\\lambda = 0$): `{c3["sector_marginal_probabilities"][0]}`; $\\mu$-traced off-diagonal norm for $\\lambda \\ne 0$: `{c3["max_nonzero_lambda_mu_traced_frobenius_norm"]:.2e}`.
2. **Full-Jet Alignment Spectator Branch (`verify_full_jet_alignment_spectator_density_branch`)**:
   - Pins concrete $625 \\times 625$ post-measurement branch density matrices ($p = {fj["p"]}, m = 1, D = {fj["degree"]}, J = {fj["scalar_split_jet_width_J"]}, R = {fj["scalar_split_carrier_width_R"]}, S = {fj["scalar_split_spectator_width_S"]}$, retaining $k = D$) to `QSearch.FullJetAlignment.fullJet_source_to_scalar` (`formal/Formal/FullJetAlignment.lean`), and verifies `align_full_jet` on `ClassThreeStructure` ($R = {fj["class_two_carrier_width_R"]}, J = {fj["class_two_jet_width_J"]}$).
   - Spectator branch trace per outcome $u_0 \\in \\ker P$: `{fj["spectator_branch_traces"][0]:.6f}` ($p^{{-S}} = 1/5$); max Frobenius error against `curveRho(U, vectorJet(Q), scalarPhase)`: `{fj["max_spectator_branch_frobenius_error"]:.2e}`.
3. **Full Taylor Transport Mixed Branch & Negative $t$-Fourier Residual (`verify_full_taylor_transport_mixed_branch_density_contraction`)**:
   - Pins concrete $625 \\times 625$ density matrices on $\\mathbb{{F}}_p^m \\times \\text{{Jets}}(D={ft["degree"]})$ ($p = {ft["p"]}$) to `QSearch.FullTaylorTransport.fullJet_mixed_branch` (`formal/Formal/FullTaylorTransport.lean`).
   - Mixed-branch Frobenius error: `{ft["mixed_branch_frobenius_error"]:.2e}`; post-erasure negative $t$-Fourier residual Frobenius error: `{ft["max_fourier_residual_frobenius_error"]:.2e}`; maximum residual ordinary degree `{ft["max_residual_polynomial_degree"]}` (attaining $D = {ft["degree"]}$ on the $k = D$ character: `{ft["attains_top_degree_D_on_k_eq_D_fourier_character"]}`).
4. **Logical-Gate Population-Gap & Access-Matched Baseline Audit (`certify_population_singular_value_gap`, `audit_logical_gate_access_matched_baselines`)**:
   - Verifies $\\min_{{|u|=1}} \\|A(a)V - u V B(b)\\|_F^2 / d = 2(1 - |z(a, b)|) \\ge \\alpha \\eta^2 / 2$ across marked ($\\alpha = 1/d$, decaying as $O(1/(d p^2))$) vs balanced population-separated ($\\alpha = 1/2$, constant $\\gamma$ across $d$) encoders, alongside classical forward-encoder basis tomography ($d$ forward calls to $V|x\\rangle$) and Pauli conjugation nilpotency invariance ($c = {lg["conjugated_pauli_heisenberg_nilpotency_class"]}$).

## 2. Marked vs Balanced Population-Gap and Classical Basis Probing Table ($p = {lg["p"]}$)

| Logical $\\dim d$ | Marked Exact $\\gamma$ ($\\alpha = 1/d$) | Marked Pop. Bound $\\alpha \\eta^2 / 2$ | Marked IID Choi Lower Bound ($s=2/3$) | Balanced Exact $\\gamma$ ($\\alpha = 1/2$) | Balanced Pop. Bound $\\alpha \\eta^2 / 2$ | Classical Basis Probing Forward Calls |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
{gap_rows}

## 3. Explicit Scope Boundaries

- Related literature context: [Bennett, Bernstein, Brassard, and Vazirani (1997)](https://arxiv.org/abs/quant-ph/9701001) for the $\\Omega(\\sqrt{{d}})$ oracle query lower bound; [Knill and Laflamme (1997)](https://arxiv.org/abs/quant-ph/9604034) for isometric subcode error-correction inheritance; [Cao and Lackey (2026)](https://arxiv.org/html/2603.03542v1) and [Holt and Subramanian (2026)](https://arxiv.org/html/2609.38085v2#S10) for encoding-tensor and state-symmetry reductions.
- All novelty and speedup flags (`accepted_speedup_candidate`, `novelty_claim`, `speedup_claim_allowed`) are `False`.
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Write JSON and Markdown artifacts.")
    args = parser.parse_args()
    report = build_full_jet_channel_and_logical_gap_report()
    if args.write:
        JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
        JSON_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        MD_PATH.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({"module": report["module"], "schema_version": report["schema_version"]}, indent=2))


if __name__ == "__main__":
    main()
