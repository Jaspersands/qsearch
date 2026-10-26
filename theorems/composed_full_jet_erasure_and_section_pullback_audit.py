"""Composed full-jet erasure verifier, terminal unit-character kernel check, non-homomorphic section pullback audit, and adaptive resource composition ledger.

This standalone module implements the executable verification controls for
``## 2026-10-21 Composed Full-Jet Erasure Contract`` and the section-pullback /
adaptive resource composition obligations in ``research/MECHANICAL_FOLLOW_UP_PLAN.md``
and ``formal/Formal/FullJetWeightedErasure.lean``:

1. **Composed Full-Jet Degree-Reduced Branch & Terminal Unit-Character Kernel (`verify_composed_degree_reduced_branch_and_terminal_kernel`)**:
   - Pins concrete ``625 x 625`` density matrices on ``F_p^m x Jets(D=2)`` at ``p = 5``
     to ``QSearch.FullJetWeightedErasure.degree_reduced_branch`` and ``terminal_kernel``.
   - Verifies that combining active tensor-product ``curveRho`` inputs under public
     scales ``t_i != 0`` and outcomes ``o_i = (y_i, z_i)`` reduces the weighted
     degree of ``mergedPolynomial(D, t, o, P)`` from ``d = 2`` to ``< 2`` (and then
     from ``d = 1`` to ``0``), while preserving a nonzero constant term
     ``c_0 = R.coeff(0) != 0`` that depends on ``o_i`` and the unknown parameters.
   - Verifies ``terminal_kernel``: when ``chi`` has unit modulus
     (``chi(r) * conj(chi(r)) == 1``), the outcome-dependent constant term ``c_0``
     cancels identically in ``curveRho`` (``frobenius_error == 0.0`` against
     ``curveRho(U, curve, 1)``), whereas for a non-unit character ``chi_bad``
     (``|chi_bad(c_0)| != 1``), ``curveRho`` fails to match ``curveRho(U, curve, 1)``!
2. **Non-Homomorphic Quotient Section Pullback Audit (`verify_non_homomorphic_section_pullback_invariance`)**:
   - Tests a genuine non-homomorphic linear section ``sigma: M/K -> M`` on the
     class-3 BCH group ``UT_4(F_p)`` where ``sigma(s_1 *_S s_2) != sigma(s_1) *_G sigma(s_2)``.
   - Verifies that when the correctness premise ``K <= H`` holds, the section defect
     ``k(s, h_bar) = (sigma(s) *_G sigma(h_bar))^-1 *_G sigma(s *_S h_bar)`` lies in
     ``K <= H``, so the pulled-back oracle ``f_S(s) = f(sigma(s))`` (computed by
     reversible ``compute sigma(s) -> query f -> uncompute sigma(s)``) is strictly
     right-invariant under ``H_S = (H intersect M)/K`` and separates distinct cosets.
   - Proves the negative control: when ``K`` is NOT contained in ``H`` (an erroneous
     prior recursive answer), ``k(s, h_bar)`` escapes ``H`` and breaks right-``H_S``
     invariance on ``f_S``.
3. **Twisted Non-Homomorphic Section Character Covariance (`verify_twisted_section_character_covariance`)**:
   - Verifies on ``S = M_chi / K_0`` (with ``K_0 = ker(chi_K)``) that even when the
     public section ``sigma: S -> M_chi`` is not a group homomorphism, the section
     defect ``k_0(s, h_bar)`` lies in ``K_0 <= ker(chi_H)``, so the induced phase
     ``chi_H(sigma(s)^-1 *_G sigma(s *_S h_bar)) = chi_H(sigma(h_bar))`` is a
     well-defined character on ``H_S = (H intersect M_chi)/K_0`` independent of ``s``.
   - Proves the negative control: if ``chi_K`` was mislearned so ``K_0`` is not
     contained in ``ker(chi_H)``, the section defect injects an ``s``-dependent phase
     error that destroys right-coset character covariance.
4. **Adaptive Resource Composition Ledger (`audit_adaptive_recursion_resource_composition`)**:
   - Verifies that across a multi-step adaptive recursion trace (e.g., ``Solve(L, f)``
     on ``ut_7(F_p)``), arities multiply **within** each step's two-stage phase-erasure
     tree while total oracle queries and reversible lift gates **add** across sequential
     recursion steps (never multiplying tree sizes across sequential group restrictions
     and never dropping the internal multiplicative tree arities).
"""
from __future__ import annotations

import argparse
from itertools import product
import json
from pathlib import Path
import random
import sys
from typing import Sequence

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.class_three_ambient_frontend import class_three_full_jet_resource_budget
from theorems.class_three_monomial_jet import ClassThreeStructure, FullTaylorJetChart
from theorems.nonlinear_jet_erasure import (
    pullback_phase,
    verify_weighted_witness,
    weighted_degree,
    weighted_merge,
)
from theorems.prime_character_opi import ring
from theorems.ut5_scalar_phase_compiler import SymbolicScalarPacket


JSON_PATH = ROOT / "research" / "reductions" / "composed_full_jet_erasure_and_section_pullback_audit.json"
MD_PATH = ROOT / "research" / "COMPOSED_FULL_JET_ERASURE_AND_SECTION_PULLBACK_AUDIT.md"


def _mv(mat: Sequence[Sequence[int]], vec: Sequence[int], p: int) -> tuple[int, ...]:
    return tuple(sum(a * b for a, b in zip(row, vec)) % p for row in mat)


def verify_composed_degree_reduced_branch_and_terminal_kernel(
    p: int = 5,
    degree: int = 2,
) -> dict[str, object]:
    """Verify ``degree_reduced_branch`` and ``terminal_kernel`` from ``Formal/FullJetWeightedErasure.lean``."""
    ring(p)
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

    j_vecs = list(product(range(p), repeat=j_width))
    j_idx = {v: i for i, v in enumerate(j_vecs)}
    vj_points = [(q, jv) for q in range(p) for jv in j_vecs]
    vj_idx = {pt: i for i, pt in enumerate(vj_points)}
    dim_vj = len(vj_points)  # 625
    inv_size = 1.0 / dim_vj

    param_basis = ((0, (1,)), (0, (2,)))
    theta = (2, 3)
    terms_p0 = {
        ((2, 0, 0, 0), (0,)): 1,
        ((0, 0, 0, 1), (1,)): 1,
        ((1, 0, 0, 0), (0,)): 1,
    }
    terms_p1 = {
        ((2, 0, 0, 0), (0,)): 1,
        ((0, 0, 0, 1), (1,)): 1,
        ((1, 0, 0, 0), (0,)): 3,
    }
    pkt0 = SymbolicScalarPacket(p, 1, j_width, param_basis, terms_p0)
    pkt1 = SymbolicScalarPacket(p, 1, j_width, param_basis, terms_p1)
    t_scales = [1, 2]
    verify_weighted_witness(chart, [pkt0, pkt1], t_scales, 2)

    o_outcomes = [((1,), (1, 0, 2)), ((2,), (0, 2, 1))]
    pulled0 = pullback_phase(chart, pkt0, o_outcomes[0][0], o_outcomes[0][1], t_scales[0])
    pulled1 = pullback_phase(chart, pkt1, o_outcomes[1][0], o_outcomes[1][1], t_scales[1])
    full_merged_terms = dict(pulled0.terms)
    for k_term, v_coeff in pulled1.terms.items():
        new_v = (full_merged_terms.get(k_term, 0) + v_coeff) % p
        if new_v:
            full_merged_terms[k_term] = new_v
        else:
            full_merged_terms.pop(k_term, None)
    full_merged_pkt = SymbolicScalarPacket(p, 1, j_width, param_basis, full_merged_terms)
    assert weighted_degree(chart, full_merged_pkt) == 1

    def make_curve_rho(pkt: SymbolicScalarPacket | None, char_base: complex = omega) -> np.ndarray:
        rho = np.zeros((dim_vj, dim_vj), dtype=complex)
        if pkt is None:
            ph_vals = np.ones(dim_vj, dtype=complex)
        else:
            ph_vals = np.array(
                [
                    char_base ** pkt.evaluate_fixture((q_val,) + jv, theta)
                    for q_val, jv in vj_points
                ],
                dtype=complex,
            )
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

    rho0 = make_curve_rho(pkt0)
    rho1 = make_curve_rho(pkt1)
    t_mats = [chart.transport_matrix(o_outcomes[slot][0], t_scales[slot]) for slot in range(2)]

    def public_point(slot: int, x_pt: tuple[int, tuple[int, ...]]) -> tuple[int, tuple[int, ...]]:
        q_val, jv = x_pt
        y_i, z_i = o_outcomes[slot]
        c_i = t_scales[slot]
        q_out = (y_i[0] + c_i * q_val) % p
        j_out = tuple((u + v) % p for u, v in zip(z_i, _mv(t_mats[slot], jv, p)))
        return (q_out, j_out)

    p0_map = np.array([vj_idx[public_point(0, x)] for x in vj_points])
    p1_map = np.array([vj_idx[public_point(1, x)] for x in vj_points])
    branch_deg2 = inv_size * rho0[np.ix_(p0_map, p0_map)] * rho1[np.ix_(p1_map, p1_map)]
    expected_deg2 = (inv_size ** 2) * make_curve_rho(full_merged_pkt)
    deg2_branch_err = float(np.linalg.norm(branch_deg2 - expected_deg2, ord="fro"))
    assert deg2_branch_err < 1e-14

    t_w1 = [1, 4]
    o_w1 = [((2,), (0, 0, 0)), ((1,), (0, 0, 0))]
    pulled_w1_0 = pullback_phase(chart, full_merged_pkt, o_w1[0][0], o_w1[0][1], t_w1[0])
    pulled_w1_1 = pullback_phase(chart, full_merged_pkt, o_w1[1][0], o_w1[1][1], t_w1[1])
    terminal_terms = dict(pulled_w1_0.terms)
    for k_term, v_coeff in pulled_w1_1.terms.items():
        new_v = (terminal_terms.get(k_term, 0) + v_coeff) % p
        if new_v:
            terminal_terms[k_term] = new_v
        else:
            terminal_terms.pop(k_term, None)
    terminal_pkt = SymbolicScalarPacket(p, 1, j_width, param_basis, terminal_terms)
    assert weighted_degree(chart, terminal_pkt) == 0
    const_val = terminal_pkt.evaluate_fixture((0, 0, 0, 0), theta)
    assert const_val != 0

    rho_terminal_unit = make_curve_rho(terminal_pkt, char_base=omega)
    rho_unphased = make_curve_rho(None)
    terminal_unit_err = float(np.linalg.norm(rho_terminal_unit - rho_unphased, ord="fro"))
    assert terminal_unit_err < 1e-14

    rho_terminal_nonunit = make_curve_rho(terminal_pkt, char_base=1.5 * omega)
    terminal_nonunit_err = float(np.linalg.norm(rho_terminal_nonunit - rho_unphased, ord="fro"))
    assert terminal_nonunit_err > 0.1

    return {
        "p": p,
        "degree": degree,
        "hilbert_dim_V_times_J": dim_vj,
        "degree_reduced_branch_frobenius_error": deg2_branch_err,
        "merged_weighted_degree_after_stage2": weighted_degree(chart, full_merged_pkt),
        "terminal_weighted_degree_after_stage1": weighted_degree(chart, terminal_pkt),
        "terminal_constant_residual_value_mod_p": const_val,
        "terminal_kernel_unit_character_frobenius_error": terminal_unit_err,
        "terminal_kernel_nonunit_character_frobenius_error": round(terminal_nonunit_err, 8),
    }


def verify_non_homomorphic_section_pullback_invariance(p: int = 11) -> dict[str, object]:
    """Verify that non-homomorphic section pullback ``f_S(s) = f(sigma(s))`` is right-``H_S``-invariant iff ``K <= H``."""
    ring(p)
    st = ClassThreeStructure(
        p,
        (((0, 1, 0), (p - 1, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 1), (0, p - 1, 0))),
        (((0, 0, 1), (0, 0, 0), (p - 1, 0, 0)),),
        (((0, 1), (0, 0), (p - 1, 0)),),
    )

    def sigma(s_vec: tuple[int, int, int, int, int]) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
        a = s_vec[:3]
        b = s_vec[3:]
        c = ((a[0] + b[0]) % p,)
        return (a, b, c)

    def proj_s(g_elem: tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]) -> tuple[int, int, int, int, int]:
        return g_elem[0] + g_elem[1]

    def mult_s(s1: tuple[int, int, int, int, int], s2: tuple[int, int, int, int, int]) -> tuple[int, int, int, int, int]:
        return proj_s(st.multiply_fixture(sigma(s1), sigma(s2)))

    rng = random.Random(20261021)
    non_homomorphic_pairs = 0
    for _ in range(25):
        s1 = tuple(rng.randrange(p) for _ in range(5))
        s2 = tuple(rng.randrange(p) for _ in range(5))
        prod_lift = st.multiply_fixture(sigma(s1), sigma(s2))
        lift_prod = sigma(mult_s(s1, s2))
        if prod_lift != lift_prod:
            non_homomorphic_pairs += 1
        assert prod_lift[0] == lift_prod[0] and prod_lift[1] == lift_prod[1]
    assert non_homomorphic_pairs > 20

    half = pow(2, -1, p)

    def coset_invariant_valid_H(g_elem: tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]) -> tuple[int, int, int]:
        a, b, _c = g_elem
        return (a[0], a[2], (b[0] - half * a[0] * a[1]) % p)

    valid_invariance_checks = 0
    for _ in range(30):
        s_vec = tuple(rng.randrange(p) for _ in range(5))
        h_bar = (0, rng.randrange(p), 0, 0, rng.randrange(p))
        f_s1 = coset_invariant_valid_H(sigma(s_vec))
        f_s2 = coset_invariant_valid_H(sigma(mult_s(s_vec, h_bar)))
        assert f_s1 == f_s2
        valid_invariance_checks += 1

    def coset_invariant_violated_K(g_elem: tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]) -> tuple[int, ...]:
        a, b, c = g_elem
        sixth = pow(6, -1, p)
        inv_b0 = (b[0] - half * a[0] * a[1]) % p
        inv_b1 = (b[1] + half * a[2] * a[1]) % p
        inv_c0 = (c[0] + sixth * a[0] * a[2] * a[1]) % p
        return (a[0], a[2], inv_b0, inv_b1, inv_c0)

    violated_k_mismatches = 0
    for _ in range(30):
        s_vec = tuple(rng.randrange(1, p) for _ in range(5))
        h_bar = (0, rng.randrange(1, p), 0, 0, 0)
        h_true = ((0, h_bar[1], 0), (0, 0), (0,))
        assert coset_invariant_violated_K(st.multiply_fixture(sigma(s_vec), h_true)) == coset_invariant_violated_K(sigma(s_vec))
        if coset_invariant_violated_K(sigma(mult_s(s_vec, h_bar))) != coset_invariant_violated_K(sigma(s_vec)):
            violated_k_mismatches += 1
    assert violated_k_mismatches > 20

    return {
        "p": p,
        "non_homomorphic_section_pairs_out_of_25": non_homomorphic_pairs,
        "valid_k_in_h_right_invariance_checks": valid_invariance_checks,
        "violated_k_not_in_h_mismatches_out_of_30": violated_k_mismatches,
    }


def verify_twisted_section_character_covariance(p: int = 11) -> dict[str, object]:
    """Verify twisted character covariance under non-homomorphic section ``sigma: M_chi / K_0 -> M_chi``."""
    ring(p)
    half = pow(2, -1, p)

    def mult_heis(g1: tuple[int, int, int], g2: tuple[int, int, int]) -> tuple[int, int, int]:
        x1, y1, z1 = g1
        x2, y2, z2 = g2
        return (
            (x1 + x2) % p,
            (y1 + y2) % p,
            (z1 + z2 + half * (x1 * y2 - y1 * x2)) % p,
        )

    def inv_heis(g: tuple[int, int, int]) -> tuple[int, int, int]:
        return ((-g[0]) % p, (-g[1]) % p, (-g[2]) % p)

    def sigma_m(s_vec: tuple[int, int, int, int]) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
        x1, y1, z_tot, y2 = s_vec
        return ((x1, y1, (z_tot + x1) % p), (0, y2, (-3 * y2) % p))

    def proj_m(pair: tuple[tuple[int, int, int], tuple[int, int, int]]) -> tuple[int, int, int, int]:
        (x1, y1, z1), (x2, y2, z2) = pair
        assert x2 == 0
        return (x1, y1, (z1 + 3 * y2 + z2 - x1) % p, y2)

    def mult_m(
        p1: tuple[tuple[int, int, int], tuple[int, int, int]],
        p2: tuple[tuple[int, int, int], tuple[int, int, int]],
    ) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
        return (mult_heis(p1[0], p2[0]), mult_heis(p1[1], p2[1]))

    def inv_m(
        pair: tuple[tuple[int, int, int], tuple[int, int, int]],
    ) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
        return (inv_heis(pair[0]), inv_heis(pair[1]))

    def mult_s(s1: tuple[int, int, int, int], s2: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
        return proj_m(mult_m(sigma_m(s1), sigma_m(s2)))

    def ell_true(pair: tuple[tuple[int, int, int], tuple[int, int, int]]) -> int:
        (x1, y1, z1), (x2, y2, z2) = pair
        assert y1 == 0 and x2 == 0
        return (4 * x1 + z1 + 3 * y2 + z2) % p

    def ell_mislearned(pair: tuple[tuple[int, int, int], tuple[int, int, int]]) -> int:
        (x1, y1, z1), (x2, y2, z2) = pair
        return (4 * x1 + z1 + 5 * y2 + z2) % p

    rng = random.Random(7719)
    valid_covariant_trials = 0
    mislearned_char_mismatches = 0

    for _ in range(25):
        s_vec = tuple(rng.randrange(1, p) for _ in range(4))
        h_bar = (rng.randrange(1, p), 0, rng.randrange(1, p), rng.randrange(1, p))
        delta_g = mult_m(inv_m(sigma_m(s_vec)), sigma_m(mult_s(s_vec, h_bar)))
        assert ell_true(delta_g) == ell_true(sigma_m(h_bar))
        valid_covariant_trials += 1

        def sigma_perturbed(sv: tuple[int, int, int, int]):
            base_p = sigma_m(sv)
            t_shift = (sv[0] * sv[1]) % p
            k0_elem = ((0, 0, (-3 * t_shift) % p), (0, t_shift, 0))
            return mult_m(base_p, k0_elem)

        delta_pert = mult_m(inv_m(sigma_perturbed(s_vec)), sigma_perturbed(mult_s(s_vec, h_bar)))
        assert ell_true(delta_pert) == ell_true(sigma_perturbed(h_bar))
        if ell_mislearned(delta_pert) != ell_mislearned(sigma_perturbed(h_bar)):
            mislearned_char_mismatches += 1

    assert mislearned_char_mismatches == 25

    return {
        "p": p,
        "valid_character_covariance_trials": valid_covariant_trials,
        "mislearned_character_mismatches_out_of_25": mislearned_char_mismatches,
    }


def audit_adaptive_recursion_resource_composition(p: int = 19) -> dict[str, object]:
    """Verify additive across-step vs multiplicative within-tree resource composition on ``ut_7(F_p)``."""
    step_specs = [
        {"step": 1, "ambient_class": 6, "m": 6, "r": 9, "s": 2, "z": 4, "lift_gates_per_call": 42},
        {"step": 2, "ambient_class": 5, "m": 4, "r": 7, "s": 1, "z": 4, "lift_gates_per_call": 34},
        {"step": 3, "ambient_class": 4, "m": 3, "r": 6, "s": 0, "z": 4, "lift_gates_per_call": 28},
    ]
    per_step_budgets: list[dict[str, object]] = []
    sum_log2_across_steps_fallacy = 0.0
    max_step_log2_queries = 0.0
    total_b0_sources_across_steps = 0
    total_reversible_lift_gates_per_b0_batch = 0

    for spec in step_specs:
        b = class_three_full_jet_resource_budget(
            p=p,
            ambient_class=spec["ambient_class"],
            quotient_width=spec["m"],
            a_width=spec["r"],
            b_width=spec["s"],
            c_width=spec["z"],
        )
        within_tree_log2 = b["log2_weighted_tree_leaves"] + b["log2_ordinary_tree_leaves_full_D"]
        assert b["log2_total_matrix_leaves_M"] > within_tree_log2
        assert b["log2_raw_queries_upper_bound"] > b["log2_total_matrix_leaves_M"]
        sum_log2_across_steps_fallacy += b["log2_raw_queries_upper_bound"]
        max_step_log2_queries = max(max_step_log2_queries, b["log2_raw_queries_upper_bound"])
        total_b0_sources_across_steps += b["matrix_batch_sources_b0"]
        step_lift_gates = 2 * spec["lift_gates_per_call"] * b["matrix_batch_sources_b0"]
        total_reversible_lift_gates_per_b0_batch += step_lift_gates
        per_step_budgets.append(
            {
                "step": spec["step"],
                "ambient_class": spec["ambient_class"],
                "jet_degree_D": b["jet_degree_D"],
                "weighted_degree_e": b["weighted_phase_degree_e"],
                "matrix_batch_sources_b0": b["matrix_batch_sources_b0"],
                "log2_total_matrix_leaves_M": round(b["log2_total_matrix_leaves_M"], 3),
                "log2_raw_queries_upper_bound": round(b["log2_raw_queries_upper_bound"], 3),
                "reversible_lift_gates_per_b0_batch": step_lift_gates,
            }
        )

    additive_across_steps_log2_bound = round(max_step_log2_queries + float(np.log2(len(step_specs))), 3)
    forbid_across_step_product_log2 = round(sum_log2_across_steps_fallacy, 3)
    assert additive_across_steps_log2_bound < forbid_across_step_product_log2

    return {
        "p": p,
        "per_step_tree_budgets": per_step_budgets,
        "total_b0_sources_across_steps": total_b0_sources_across_steps,
        "additive_across_steps_log2_queries_bound": additive_across_steps_log2_bound,
        "forbid_across_step_product_log2_queries": forbid_across_step_product_log2,
        "total_reversible_lift_overhead_gates_per_b0_batch": total_reversible_lift_gates_per_b0_batch,
    }


def build_composed_full_jet_erasure_and_section_pullback_report() -> dict[str, object]:
    """Build the reproducible verification report for Milestone 21."""
    branch_kernel = verify_composed_degree_reduced_branch_and_terminal_kernel(p=5, degree=2)
    section_pullback = verify_non_homomorphic_section_pullback_invariance(p=11)
    twisted_section = verify_twisted_section_character_covariance(p=11)
    resource_ledger = audit_adaptive_recursion_resource_composition(p=19)

    return {
        "schema_version": "composed_full_jet_erasure_and_section_pullback_audit_v1",
        "module": "theorems/composed_full_jet_erasure_and_section_pullback_audit.py",
        "scope": {
            "composed_degree_reduced_branch_verified": True,
            "terminal_kernel_unit_character_cancellation_verified": True,
            "terminal_kernel_nonunit_character_falsified": True,
            "non_homomorphic_section_pullback_invariance_verified": True,
            "erroneous_k_section_pullback_falsified": True,
            "twisted_section_character_covariance_verified": True,
            "adaptive_across_step_additive_within_tree_multiplicative_verified": True,
            "accepted_speedup_candidate": False,
            "novelty_claim": False,
            "speedup_claim_allowed": False,
        },
        "composed_degree_reduced_branch_and_terminal_kernel": branch_kernel,
        "non_homomorphic_section_pullback_audit": section_pullback,
        "twisted_section_character_covariance_audit": twisted_section,
        "adaptive_recursion_resource_composition_ledger": resource_ledger,
    }


def render_markdown(report: dict[str, object]) -> str:
    bk = report["composed_degree_reduced_branch_and_terminal_kernel"]
    sp = report["non_homomorphic_section_pullback_audit"]
    ts = report["twisted_section_character_covariance_audit"]
    rl = report["adaptive_recursion_resource_composition_ledger"]
    step_rows = "\n".join(
        f"| `{row['step']}` | `{row['ambient_class']}` | `{row['jet_degree_D']}` | `{row['weighted_degree_e']}` | `{row['matrix_batch_sources_b0']}` | `{row['log2_total_matrix_leaves_M']}` | `{row['reversible_lift_gates_per_b0_batch']}` |"
        for row in rl["per_step_tree_budgets"]
    )
    return f"""# Composed Full-Jet Erasure, Terminal Unit-Character Kernel, Non-Homomorphic Section Pullback, and Adaptive Resource Composition Audit

2026-10-21. **Standalone executable verification of `Formal/FullJetWeightedErasure.lean` (`degree_reduced_branch`, `terminal_kernel`), non-homomorphic section pullback right-invariance, and adaptive resource composition; not an admitted speedup candidate or novelty claim.**

## 1. Summary of Verified Contracts

This note documents `theorems/composed_full_jet_erasure_and_section_pullback_audit.py` and `tests/test_composed_full_jet_erasure_and_section_pullback_audit.py`:

1. **Composed Full-Jet Degree-Reduced Branch & Terminal Unit-Character Kernel (`verify_composed_degree_reduced_branch_and_terminal_kernel`)**:
   - Pins $625 \\times 625$ density matrices on $\\mathbb{{F}}_5 \\times \\text{{Jets}}(D=2)$ to `QSearch.FullJetWeightedErasure.degree_reduced_branch` and `terminal_kernel` (`formal/Formal/FullJetWeightedErasure.lean`).
   - Stage-2 weighted merge reduces weighted degree from `2` to `{bk["merged_weighted_degree_after_stage2"]}` with branch Frobenius error `{bk["degree_reduced_branch_frobenius_error"]:.2e}`; Stage-1 merge reduces weighted degree to `{bk["terminal_weighted_degree_after_stage1"]}` with nonzero outcome-dependent constant residual $c_0 = {bk["terminal_constant_residual_value_mod_p"]} \\pmod 5$.
   - Verifies `terminal_kernel`: unit-modulus character $\\chi(r) = \\omega^r$ cancels $c_0$ identically (`frobenius_error = {bk["terminal_kernel_unit_character_frobenius_error"]:.2e}`), whereas a non-unit character fails to cancel $c_0$ (`frobenius_error = {bk["terminal_kernel_nonunit_character_frobenius_error"]}`).
2. **Non-Homomorphic Quotient Section Pullback Audit (`verify_non_homomorphic_section_pullback_invariance`)**:
   - On $\\text{{UT}}_4(\\mathbb{{F}}_{{11}})$, a linear section $\\sigma: M/K \\to M$ fails the homomorphism law on `{sp["non_homomorphic_section_pairs_out_of_25"]}/25` random pairs, yet when $K \\le H$, the pulled-back oracle $f_S(s) = f(\\sigma(s))$ is strictly right-$H_S$-invariant on `{sp["valid_k_in_h_right_invariance_checks"]}/30` trials.
   - When $K \\not\\le H$ (erroneous recursive output), the non-homomorphic section defect escapes $H$ and breaks right-$H_S$ invariance on `{sp["violated_k_not_in_h_mismatches_out_of_30"]}/30` trials.
3. **Twisted Non-Homomorphic Section Character Covariance (`verify_twisted_section_character_covariance`)**:
   - On $S = M_\\chi / K_0$, verifies that when $K_0 = \\ker \\chi_K \\subseteq \\ker \\chi_H$, the non-homomorphic section defect in $K_0$ cancels from $\\chi_H(\\sigma(s)^{{-1}} \\sigma(s \\cdot_S \\bar{{h}})) = \\chi_H(\\sigma(\\bar{{h}}))$ across `{ts["valid_character_covariance_trials"]}/25` trials, whereas a mislearned character $\\tilde{{\\chi}}_K$ fails on `{ts["mislearned_character_mismatches_out_of_25"]}/25` trials.
4. **Adaptive Resource Composition Ledger (`audit_adaptive_recursion_resource_composition`)**:
   - Verifies multiplicative arity composition within each step's two-stage phase-erasure tree and additive summation across sequential image steps (`log2_queries <= {rl["additive_across_steps_log2_queries_bound"]}` vs `{rl["forbid_across_step_product_log2_queries"]}` if erroneously multiplied across steps), while charging $2 \\cdot C_{{\\text{{lift}}}}$ reversible compute/uncompute gates per oracle call.

## 2. Adaptive Two-Stage Tree & Reversible Lift Ledger ($p = {rl["p"]}$)

| Step | Ambient Class $c$ | Jet Degree $D$ | Weighted Degree $e$ | Batch Sources $b_0$ | $\\log_2$ Within-Tree Matrix Leaves $M$ | Reversible Lift Gates / $b_0$ Batch |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
{step_rows}

## 3. Explicit Scope Boundaries

- Related literature context: [Ivanyos and Santha (2015)](https://arxiv.org/abs/1503.09016) for fixed-degree polynomial phase erasure; [Holt and Subramanian (2026)](https://arxiv.org/html/2609.38085v2) for state-symmetry reductions.
- All novelty and speedup flags (`accepted_speedup_candidate`, `novelty_claim`, `speedup_claim_allowed`) are `False`.
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Write JSON and Markdown artifacts.")
    args = parser.parse_args()
    report = build_composed_full_jet_erasure_and_section_pullback_report()
    if args.write:
        JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
        JSON_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        MD_PATH.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({"module": report["module"], "schema_version": report["schema_version"]}, indent=2))


if __name__ == "__main__":
    main()
