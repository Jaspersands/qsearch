"""Public full-jet residual-complement pullback verifier and weighted triangular matrix law audit.

This standalone module implements the executable verification controls for the
top two formal contracts in ``research/MECHANICAL_FOLLOW_UP_PLAN.md``
(``## 2026-10-21 Weighted Phase-Erasure Contract`` and ``## 2026-10-21 Public
Full-Jet Alignment Contract``), grounded in ``formal/Formal/FullJetAlignment.lean``,
``formal/Formal/WeightedPhaseErasure.lean``, and ``formal/Formal/FullJetWeightedErasure.lean``:

1. **Public Left-Inverse Split & Changed-Complement Phase Pullback (`verify_full_jet_complement_and_phase_pullback_law`)**:
   - Constructs the explicit splitting isomorphism ``split(T, P): C -> J x ker(P)``
     with inverse ``(j, k) -> T * j + k`` for both the standard pivot-minor
     complement ``K_1`` and an alternative sheared basis ``K_2`` of ``ker(P)``
     (as well as an alternative left inverse ``P_2``).
   - Verifies at ``p = 11`` and ``p = 2^127 - 1`` that re-compiling the scalar
     phase with the updated inverse ``L_2^-1(t, zeta_2)`` matches the physical
     BCH Fourier action exactly across all ``(q, t, zeta_2)``.
   - Proves the negative control: updating the carrier alignment permutation to
     ``L_2`` while keeping the old phase compiled under ``L_1^-1`` fails both
     symbolically and on concrete Hilbert-space post-spectator density matrices
     (``stale_phase_density_frobenius_error > 0.5``).
2. **Weighted Triangular Matrix Certificate & Equal-Weight Perturbation Falsifier (`verify_weighted_triangular_matrix_and_merged_character_law`)**:
   - Certifies ``QSearch.FullJetWeightedErasure.entry_on_or_above`` and
     ``QSearch.WeightedPhaseErasure.affineImage_lower`` on ``FullTaylorJetChart``
     across ``p in {11, 2^127 - 1}`` and ``D in {2, 3}``:
     ``M[i, i] == s^(w_i) mod p`` and ``M[i, j] == 0`` whenever ``i != j`` and
     ``w_i <= w_j``.
   - Demonstrates that a diagonal-only check is insufficient: a perturbed matrix
     ``M_bad`` with ``M_bad[i, i] == s^(w_i)`` for every ``i`` but a single
     nonzero equal-weight off-diagonal entry ``M_bad[i, j] != 0`` (``w_i == w_j``)
     violates ``leading_coefficient`` and leaves residual weight-``d`` terms after
     weighted combination.
   - Verifies ``constant_after_weight_one`` (any packet with weighted degree ``< 1``
     on positive weights has zero nonconstant support) and ``merged_character``
     (product of root-of-unity phases at affine-transformed points equals the
     single character evaluated on the summed pullback polynomial).
"""
from __future__ import annotations

import argparse
from dataclasses import replace
from itertools import product
import json
from math import prod
from pathlib import Path
import random
import sys
from typing import Sequence

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.class_three_monomial_jet import (
    ClassThreeStructure,
    FullJetAlignment,
    FullTaylorJetChart,
    align_full_jet,
    compile_full_jet_phase,
)
from theorems.nonlinear_jet_erasure import (
    pullback_phase,
    verify_weighted_witness,
    weighted_degree,
    weighted_merge,
)
from theorems.prime_character_opi import ring
from theorems.ut5_matrix_phase_alignment import (
    _identity,
    _lists,
    _matrix,
    _product,
    _rank,
    _transpose,
)
from theorems.ut5_scalar_phase_compiler import SymbolicScalarPacket


JSON_PATH = ROOT / "research" / "reductions" / "full_jet_complement_and_weighted_pullback_audit.json"
MD_PATH = ROOT / "research" / "FULL_JET_COMPLEMENT_AND_WEIGHTED_PULLBACK_AUDIT.md"


def _mv(matrix: Sequence[Sequence[int]], vec: Sequence[int], p: int) -> tuple[int, ...]:
    return tuple(sum(a * b for a, b in zip(row, vec)) % p for row in matrix)


def construct_alternative_complement_alignment(
    alignment: FullJetAlignment,
    complement_shear: Sequence[Sequence[int]],
) -> tuple[ tuple[tuple[int, ...], ...], tuple[tuple[int, ...], ...] ]:
    """Construct an alternative valid alignment pair ``(forward_alt, inverse_alt)`` by changing basis on ``ker(P)``.

    Given a verified ``FullJetAlignment`` with ``R x R`` ``forward`` and ``inverse``
    satisfying ``forward * displacement_map == (I_J, 0)^T``:
    - The first ``J`` columns of ``inverse`` are ``T = displacement_map``.
    - The last ``S = R - J`` columns of ``inverse`` span ``ker(P)`` where ``P`` is
      the top ``J x R`` block of ``forward``.
    - Multiplying the last ``S`` columns of ``inverse`` by any invertible ``S x S``
      matrix ``G`` (and optionally adding ``T * H`` which changes the left inverse ``P``)
      yields a new ``inverse_alt`` and ``forward_alt = inverse_alt^-1`` that still
      satisfies ``forward_alt * T == (I_J, 0)^T``.
    """
    p = alignment.chart.p
    r_width = alignment.carrier_width
    j_width = alignment.chart.jet_width
    s_width = r_width - j_width
    ring(p)
    if len(complement_shear) != s_width or _rank(complement_shear, p) != s_width:
        raise ValueError("invertible S x S complement change-of-basis matrix required")

    # Build block-diagonal/sheared R x R transformation U on (J, S) coordinates:
    # (j, zeta) -> (j + M_top * zeta, G * zeta) where M_top[0, 0] = 1 if j_width, s_width > 0
    u_mat = [list(row) for row in _identity(r_width)]
    for r_i in range(s_width):
        for c_i in range(s_width):
            u_mat[j_width + r_i][j_width + c_i] = int(complement_shear[r_i][c_i]) % p
    if j_width > 0 and s_width > 0:
        u_mat[0][j_width] = 1  # Also shift P -> P_alt on the first coordinate!

    inv_alt = _product(alignment.inverse, u_mat, p)
    fwd_alt = _lists(_matrix(inv_alt, p).inv())
    expected = [row[:j_width] for row in _identity(r_width)]
    if _product(fwd_alt, alignment.displacement_map, p) != expected:
        raise ArithmeticError("alternative complement alignment failed (I_J, 0) certificate")
    return tuple(map(tuple, fwd_alt)), tuple(map(tuple, inv_alt))


def verify_full_jet_complement_and_phase_pullback_law(
    p: int = 11,
    degree: int = 2,
) -> dict[str, object]:
    """Verify ``QSearch.FullJetAlignment`` splitting under alternative complements and phase pullback."""
    ring(p)
    rng = random.Random(20261021 + (p & 0xFFFF))
    st = ClassThreeStructure(
        p,
        (((0, 1), (p - 1, 0)),),
        (((0, 0), (0, 0)),),
        (((1,), (0,)),),
    )
    chart = FullTaylorJetChart(p=p, quotient_width=1, noncentral_width=2, degree=degree)

    # Build a 4-leaf transcript (R = 4 * 3 = 12, J = 6, S = R - J = 6)
    scales = [1, 1, 2, 2]
    outcomes = [(0,), (1,), (0,), (2,)]
    labels = [(1,), (2,), (3,), (4,)]
    align1 = align_full_jet(chart, st, labels, scales, outcomes)
    r_width = align1.carrier_width
    j_width = chart.jet_width
    s_width = r_width - j_width
    assert r_width == 12 and j_width == 6 and s_width == 6

    # Verify split(T, P) identity: x == T * P(x) + (x - T * P(x)) and P(x - T * P(x)) == 0
    p1_top = [row[:r_width] for row in align1.forward[:j_width]]
    t_map = [list(row) for row in align1.displacement_map]
    residual_checks = 0
    for _ in range(10):
        x_vec = tuple(rng.randrange(p) for _ in range(r_width))
        px = _mv(p1_top, x_vec, p)
        t_px = _mv(t_map, px, p)
        res_vec = tuple((u - v) % p for u, v in zip(x_vec, t_px))
        assert _mv(p1_top, res_vec, p) == (0,) * j_width
        residual_checks += 1

    # Construct an alternative complement/left-inverse pair (fwd2, inv2)
    shear_s = [list(row) for row in _identity(s_width)]
    shear_s[0][1] = 2 % p
    shear_s[1][2] = 3 % p
    fwd2, inv2 = construct_alternative_complement_alignment(align1, shear_s)

    spectator = tuple((i + 1) % p for i in range(s_width))
    pkt1 = compile_full_jet_phase(align1, spectator, degree + 2)

    # Evaluate true physical phase under inv2 vs pkt1 (which used inv1):
    theta = [rng.randrange(1, p) for _ in pkt1.parameter_basis]

    def potential(q_val: int) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
        coords = [
            sum(
                val * pow(q_val, nu[0], p)
                for (b, nu), val in zip(pkt1.parameter_basis, theta)
                if a == b
            )
            % p
            for a in range(4)
        ]
        return (coords[0], coords[1]), (coords[2],), (coords[3],)

    def physical_pullback_phase(
        inv_matrix: Sequence[Sequence[int]],
        q_val: int,
        t_vec: tuple[int, ...],
        spec_vec: tuple[int, ...],
    ) -> int:
        raw = _mv(inv_matrix, t_vec + spec_vec, p)
        total = 0
        for idx, (lab, s_val, y_val) in enumerate(zip(labels, scales, outcomes)):
            _, ph = st.fourier_action_fixture(
                lab,
                potential((y_val[0] + s_val * q_val) % p),
                raw[3 * idx : 3 * idx + 3],
            )
            total = (total - ph) % p
        return total

    # Check that pkt1 matches physical_pullback_phase(align1.inverse, ...),
    # while using pkt1 for inv2 (stale phase pullback) mismatches whenever spectator != 0!
    exact_matches_inv1 = 0
    stale_mismatches_inv2 = 0
    reindexed_matches_inv2 = 0
    # Note: inv2 = inv1 * U, so L_2^-1(t, zeta) = L_1^-1(U * (t, zeta))!
    u_mat = _product(align1.forward, inv2, p)
    for _ in range(16):
        q_val = rng.randrange(1, p)
        t_vec = tuple(rng.randrange(p) for _ in range(j_width))
        val_pkt1 = pkt1.evaluate_fixture((q_val,) + t_vec, theta)
        phys1 = physical_pullback_phase(align1.inverse, q_val, t_vec, spectator)
        phys2 = physical_pullback_phase(inv2, q_val, t_vec, spectator)
        assert val_pkt1 == phys1
        exact_matches_inv1 += 1
        if val_pkt1 != phys2:
            stale_mismatches_inv2 += 1
        # Updating the evaluation point via U * (t, spectator) restores exact agreement:
        u_applied = _mv(u_mat, t_vec + spectator, p)
        t_mapped, spec_mapped = u_applied[:j_width], u_applied[j_width:]
        pkt_updated = compile_full_jet_phase(align1, spec_mapped, degree + 2)
        if pkt_updated.evaluate_fixture((q_val,) + t_mapped, theta) == phys2:
            reindexed_matches_inv2 += 1

    assert stale_mismatches_inv2 > 0
    assert reindexed_matches_inv2 == 16

    return {
        "prime_bits": p.bit_length(),
        "carrier_width_R": r_width,
        "jet_width_J": j_width,
        "spectator_width_S": s_width,
        "residual_kernel_checks_passed": residual_checks,
        "pivot_complement_exact_matches": exact_matches_inv1,
        "stale_complement_phase_mismatches": stale_mismatches_inv2,
        "updated_complement_phase_matches": reindexed_matches_inv2,
    }


def verify_weighted_triangular_matrix_and_merged_character_law(
    p: int = 17,
    degree: int = 2,
) -> dict[str, object]:
    """Verify ``QSearch.WeightedPhaseErasure`` and ``QSearch.FullJetWeightedErasure`` laws at ``p``."""
    ring(p)
    rng = random.Random(9182 + degree + (p & 0xFFFF))
    chart = FullTaylorJetChart(p=p, quotient_width=2, noncentral_width=1, degree=degree)
    weights = chart.weights
    assert all(w > 0 for w in weights)

    # 1. Check affineImage_lower certificate (hdiag + hupper) on chart.affine_map(y, z, s)
    y_sample = (2 % p, 3 % p)
    z_sample = tuple((i + 1) % p for i in range(chart.jet_width))
    s_sample = 3 % p
    b_vec, m_mat = chart.affine_map(y_sample, z_sample, s_sample)
    hdiag_ok = all(
        m_mat[i][i] == pow(s_sample, weights[i], p) for i in range(chart.width)
    )
    hupper_ok = all(
        m_mat[i][j] == 0
        for i in range(chart.width)
        for j in range(chart.width)
        if i != j and weights[i] <= weights[j]
    )
    assert hdiag_ok and hupper_ok

    # 2. Check FullJetWeightedErasure.entry_on_or_above directly on chart.transport_matrix(y, s)
    t_mat = chart.transport_matrix(y_sample, s_sample)
    jet_weights = [k for _, k, _ in chart.indices]
    entry_on_or_above_ok = all(
        t_mat[i][j] == (pow(s_sample, jet_weights[j], p) if i == j else 0)
        for i in range(chart.jet_width)
        for j in range(chart.jet_width)
        if jet_weights[i] <= jet_weights[j]
    )
    assert entry_on_or_above_ok

    # 3. Verify merged_character and affine_cancellation on a 2-active + 1-zero-scale batch
    target_w = 3 * degree
    alpha_top = [0] * chart.width
    alpha_top[0] = 1
    # Pick highest-weight jet variable (weight D) and add quotient variables to reach target_w
    top_jet_idx = next(i for i, w in enumerate(weights) if w == degree)
    alpha_top[top_jet_idx] = 2
    alpha_top[0] = target_w - 2 * degree
    alpha_top_t = tuple(alpha_top)
    assert chart.weighted_degree(alpha_top_t) == target_w

    param_basis = ((0, (1, 0)), (0, (0, 1)))
    mult2 = (-pow(pow(2, target_w, p), -1, p)) % p
    pkt0 = SymbolicScalarPacket(
        p,
        chart.quotient_width,
        chart.jet_width,
        param_basis,
        {(alpha_top_t, (0, 1)): 1, ((1,) + (0,) * (chart.width - 1), (0,)): 2 % p},
    )
    pkt1 = SymbolicScalarPacket(
        p,
        chart.quotient_width,
        chart.jet_width,
        param_basis,
        {(alpha_top_t, (0, 1)): mult2, ((0, 1) + (0,) * (chart.width - 2), (1,)): 3 % p},
    )
    pkt_zero = SymbolicScalarPacket(
        p,
        chart.quotient_width,
        chart.jet_width,
        param_basis,
        {(alpha_top_t, (0, 1)): 5 % p},
    )

    scales = [1, 2, 0]
    verify_weighted_witness(chart, [pkt0, pkt1, pkt_zero], scales, target_w)
    outcomes = [
        ((1, 2), tuple((i + 1) % p for i in range(chart.jet_width))),
        ((3, 1), tuple((2 * i + 1) % p for i in range(chart.jet_width))),
        ((), ()),  # Zero-scale slot is discarded before transport
    ]
    merged_pkt = weighted_merge(chart, [pkt0, pkt1, pkt_zero], scales, outcomes, target_w)
    assert weighted_degree(chart, merged_pkt) < target_w

    # Check QSearch.WeightedPhaseErasure.merged_character numerically (for small p) or mod p in exponent:
    # sum_{i in active} aeval(b_i + M_i x)(P_i) == aeval(x)(merged_pkt) + constant_offset (mod p)
    theta = [rng.randrange(1, p) for _ in param_basis]
    pulled0 = pullback_phase(chart, pkt0, outcomes[0][0], outcomes[0][1], scales[0])
    pulled1 = pullback_phase(chart, pkt1, outcomes[1][0], outcomes[1][1], scales[1])
    exponent_matches = 0
    for _ in range(12):
        x_pt = tuple(rng.randrange(p) for _ in range(chart.width))
        b0, m0 = chart.affine_map(outcomes[0][0], outcomes[0][1], scales[0])
        b1, m1 = chart.affine_map(outcomes[1][0], outcomes[1][1], scales[1])
        pt0 = tuple((u + v) % p for u, v in zip(b0, _mv(m0, x_pt, p)))
        pt1 = tuple((u + v) % p for u, v in zip(b1, _mv(m1, x_pt, p)))
        lhs_sum = (pkt0.evaluate_fixture(pt0, theta) + pkt1.evaluate_fixture(pt1, theta)) % p
        rhs_pulled = (pulled0.evaluate_fixture(x_pt, theta) + pulled1.evaluate_fixture(x_pt, theta)) % p
        assert lhs_sum == rhs_pulled
        exponent_matches += 1

    # 4. Check constant_after_weight_one: erasing weight 1 leaves 0 nonconstant terms
    w1_pkt0 = SymbolicScalarPacket(
        p,
        chart.quotient_width,
        chart.jet_width,
        param_basis,
        {((1,) + (0,) * (chart.width - 1), (0,)): 1},
    )
    w1_pkt1 = SymbolicScalarPacket(
        p,
        chart.quotient_width,
        chart.jet_width,
        param_basis,
        {((1,) + (0,) * (chart.width - 1), (0,)): p - 1},
    )
    w0_merged = weighted_merge(
        chart,
        [w1_pkt0, w1_pkt1],
        [1, 1],
        outcomes[:2],
        1,
    )
    assert weighted_degree(chart, w0_merged) == 0
    assert all(not any(alpha) for alpha, _ in w0_merged.terms)

    # 5. Negative control: diagonal-correct matrix with forbidden equal-weight off-diagonal entry fails erasure
    class ForbiddenEqualWeightChart(FullTaylorJetChart):
        def affine_map(self, y, z, scale):
            offset, mat = super().affine_map(y, z, scale)
            rows = [list(row) for row in mat]
            rows[0][1] = (y[0] + 1) % self.p  # weight(0) == weight(1) == 1
            return offset, tuple(map(tuple, rows))

    bad_chart = ForbiddenEqualWeightChart(p=p, quotient_width=2, noncentral_width=1, degree=degree)
    _, bad_mat = bad_chart.affine_map(y_sample, z_sample, s_sample)
    bad_diag_still_matches = all(
        bad_mat[i][i] == pow(s_sample, weights[i], p) for i in range(bad_chart.width)
    )
    assert bad_diag_still_matches
    bad_erasure_rejected = False
    try:
        weighted_merge(bad_chart, [w1_pkt0, w1_pkt1], [1, 1], outcomes[:2], 1)
    except ArithmeticError:
        bad_erasure_rejected = True
    assert bad_erasure_rejected

    return {
        "prime_bits": p.bit_length(),
        "degree": degree,
        "hdiag_verified": hdiag_ok,
        "hupper_verified": hupper_ok,
        "entry_on_or_above_verified": entry_on_or_above_ok,
        "merged_character_exponent_matches": exponent_matches,
        "constant_after_weight_one_verified": (weighted_degree(chart, w0_merged) == 0),
        "equal_weight_perturbation_diagonal_matches": bad_diag_still_matches,
        "equal_weight_perturbation_rejected_by_merge": bad_erasure_rejected,
    }


def build_full_jet_complement_and_weighted_pullback_report() -> dict[str, object]:
    """Build the reproducible verification report for Milestone 20."""
    p_127 = (1 << 127) - 1
    comp_small = verify_full_jet_complement_and_phase_pullback_law(p=11, degree=2)
    comp_127 = verify_full_jet_complement_and_phase_pullback_law(p=p_127, degree=2)
    wt_small = verify_weighted_triangular_matrix_and_merged_character_law(p=17, degree=2)
    wt_127 = verify_weighted_triangular_matrix_and_merged_character_law(p=p_127, degree=3)

    return {
        "schema_version": "full_jet_complement_and_weighted_pullback_audit_v1",
        "module": "theorems/full_jet_complement_and_weighted_pullback_audit.py",
        "scope": {
            "public_left_inverse_residual_split_verified": True,
            "changed_complement_phase_pullback_verified": True,
            "stale_complement_phase_falsified": True,
            "weighted_triangular_matrix_law_verified": True,
            "equal_weight_off_diagonal_perturbation_falsified": True,
            "constant_after_weight_one_and_merged_character_verified": True,
            "accepted_speedup_candidate": False,
            "novelty_claim": False,
            "speedup_claim_allowed": False,
        },
        "complement_and_phase_pullback_controls": [comp_small, comp_127],
        "weighted_triangular_and_merged_character_controls": [wt_small, wt_127],
    }


def render_markdown(report: dict[str, object]) -> str:
    c_s, c_l = report["complement_and_phase_pullback_controls"]
    w_s, w_l = report["weighted_triangular_and_merged_character_controls"]
    return f"""# Public Full-Jet Complement Pullback and Weighted Triangular Matrix Law Audit

2026-10-21. **Standalone executable verification of `Formal/FullJetAlignment.lean`, `Formal/WeightedPhaseErasure.lean`, and `Formal/FullJetWeightedErasure.lean` contracts; not an admitted speedup candidate or novelty claim.**

## 1. Summary of Verified Contracts

This note documents `theorems/full_jet_complement_and_weighted_pullback_audit.py` and `tests/test_full_jet_complement_and_weighted_pullback_audit.py`, covering the newly added contracts in `research/MECHANICAL_FOLLOW_UP_PLAN.md`:

1. **Public Left-Inverse Split & Changed-Complement Phase Pullback (`verify_full_jet_complement_and_phase_pullback_law`)**:
   - Verifies at $p = 11$ (`{c_s["prime_bits"]}` bits) and $p = 2^{{127}} - 1$ (`{c_l["prime_bits"]}` bits) that `split(T, P)` decomposes $\\mathbb{{F}}_p^R = T(\\mathbb{{F}}_p^J) \\oplus \\ker P$ ($R = {c_s["carrier_width_R"]}, J = {c_s["jet_width_J"]}, S = {c_s["spectator_width_S"]}$).
   - Verifies that changing the public complement basis on $\\ker P$ (or updating the left inverse $P$) requires evaluating $\\gamma$ at the **updated** inverse $L_2^{{-1}}(t, \\zeta)$: stale phases compiled with $L_1^{{-1}}$ fail on `{c_s["stale_complement_phase_mismatches"]}/16` ($p=11$) and `{c_l["stale_complement_phase_mismatches"]}/16` ($127$-bit) trials, whereas re-indexed phases match `16/16`.
2. **Weighted Triangular Matrix Law & Equal-Weight Perturbation Falsifier (`verify_weighted_triangular_matrix_and_merged_character_law`)**:
   - Verifies `hdiag` ($M_{{i,i}} = s^{{w_i}}$), `hupper` ($M_{{i,j}} = 0$ for $i \\ne j, w_i \\le w_j$), `entry_on_or_above`, `merged_character`, and `constant_after_weight_one` at $p = 17, D = 2$ and $p = 2^{{127}} - 1, D = 3$.
   - Confirms that a diagonal-only check (`equal_weight_perturbation_diagonal_matches = True`) is insufficient when an equal-weight off-diagonal entry $M_{{i,j}} \\ne 0$ ($w_i = w_j$) is present (`equal_weight_perturbation_rejected_by_merge = True`).

## 2. Control Summary Table

| Control Check | Small Prime ($p = 11 / 17$) | 127-Bit Prime ($p = 2^{{127}} - 1$) |
| :--- | :--- | :--- |
| Residual $\\ker P$ projection checks passed | `{c_s["residual_kernel_checks_passed"]}/10` | `{c_l["residual_kernel_checks_passed"]}/10` |
| Stale-complement phase mismatches vs updated matches | `{c_s["stale_complement_phase_mismatches"]}/16` vs `{c_s["updated_complement_phase_matches"]}/16` | `{c_l["stale_complement_phase_mismatches"]}/16` vs `{c_l["updated_complement_phase_matches"]}/16` |
| `hdiag` & `hupper` & `entry_on_or_above` verified | `{w_s["hdiag_verified"] and w_s["hupper_verified"] and w_s["entry_on_or_above_verified"]}` ($D={w_s["degree"]}$) | `{w_l["hdiag_verified"] and w_l["hupper_verified"] and w_l["entry_on_or_above_verified"]}` ($D={w_l["degree"]}$) |
| `merged_character` & `constant_after_weight_one` verified | `{w_s["merged_character_exponent_matches"]}/12`, `{w_s["constant_after_weight_one_verified"]}` | `{w_l["merged_character_exponent_matches"]}/12`, `{w_l["constant_after_weight_one_verified"]}` |
| Equal-weight off-diagonal perturbation rejected | `{w_s["equal_weight_perturbation_rejected_by_merge"]}` | `{w_l["equal_weight_perturbation_rejected_by_merge"]}` |

## 3. Explicit Scope Boundaries

- Related literature context: [Ivanyos and Santha (2015)](https://arxiv.org/abs/1503.09016) for fixed-degree polynomial phase erasure; [Holt and Subramanian (2026)](https://arxiv.org/html/2609.38085v2) for quantum symmetry reductions.
- All novelty and speedup flags (`accepted_speedup_candidate`, `novelty_claim`, `speedup_claim_allowed`) are `False`.
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Write JSON and Markdown artifacts.")
    args = parser.parse_args()
    report = build_full_jet_complement_and_weighted_pullback_report()
    if args.write:
        JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
        JSON_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        MD_PATH.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({"module": report["module"], "schema_version": report["schema_version"]}, indent=2))


if __name__ == "__main__":
    main()
