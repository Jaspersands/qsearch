"""Complete central Fourier instrument verifier, nontrivial H-intersect-C zero-mass falsifier, and dual-weight class-three phase bounds audit.

This standalone module implements the executable verification controls for
``## 2026-10-21 Complete Central Instrument Contract`` in
``research/MECHANICAL_FOLLOW_UP_PLAN.md``, grounded in
``formal/Formal/CentralRegularSource.lean`` and
``formal/Formal/ClassThreePhaseBounds.lean``:

1. **Complete Central Instrument & Group-Inversion vs Lie-Negation Equivalence (`verify_central_regular_instrument_and_inversion_equivalence`)**:
   - Pins concrete density-matrix contractions on the actual direct product
     ``G = F_p x Heis_3(F_p)`` with a nonlinear PUBLIC normal-first chart to
     ``QSearch.CentralRegularSource.instrument_complete``, ``regular_branch``,
     ``sector_trace``, and ``oracle_source_from_normal_chart``.
   - Verifies exact matrix equality between:
     (a) normal group inversion ``n -> n^-1`` followed by **positive** central
         Fourier ``sum_z omega^{+<lambda, z>}`` (``CentralRegularSource.amplitude``), and
     (b) **negative** central Fourier ``sum_c omega^{-<lambda, c>}`` combined with
         negating the noncentral logarithmic coordinates ``(a, b) -> (-a, -b)``.
   - Verifies that for a transverse subgroup ``H`` (``H intersect N = {1}``), every
     central label ``lambda in F_p^z`` (including ``lambda = 0``) has exact branch
     mass ``1 / |C| = p^-z``, never the irreducible Plancherel expression ``d^2 / |N|``.
2. **Nontrivial H-Intersect-C Zero-Mass Label Falsifier (`verify_nontrivial_central_intersection_zero_mass_obstruction`)**:
   - Demonstrates on concrete oracle density matrices that when ``H intersect C``
     is nontrivial (bypassing recursive intersection learning ``K = H intersect N``),
     every central character ``lambda`` with ``<lambda, H intersect C> != 0`` has
     **identically zero** branch mass (``trace == 0.0``), while characters in
     ``(H intersect C)^perp`` have mass ``|H intersect C| / |C|``.
3. **Dual-Weight Filtered-Polynomial Compiler Bounds (`verify_dual_weight_class_three_phase_bounds`)**:
   - Pins ``compile_full_jet_phase`` to ``QSearch.ClassThreePhaseBounds.operational_bound``
     and ``parameter_bound`` across ``p in {11, 17, 2^127 - 1}`` and ``D in {2, 3, 4}``:
     - Under operational weights ``w_op(q_i) = 1, w_op(t_{alpha, k, a}) = k <= D``,
       every compiled term has operational weight ``<= max(cdeg, 3*D)`` (attaining
       ``3*D`` via ``delta(a, beta(a, x))`` when ``beta != 0``).
     - Under hidden-parameter weights ``w_param(theta_m) = 1, w_param(q_i) = 0, w_param(t_j) = 0``,
       every compiled term has parameter weight ``len(params) <= 2`` (attaining ``2``
       via ``delta(a, b)`` and ``delta(a, beta(a, x))``), certifying why the lifted
       parameter space has dimension ``1 + h + h*(h+1)//2`` without any degree-3
       parameter products in ``delta(x, beta(a, x))`` or ``mu . beta(a, x)``.
"""
from __future__ import annotations

import argparse
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
    FullTaylorJetChart,
    align_full_jet,
    compile_full_jet_phase,
)
from theorems.nonlinear_jet_erasure import weighted_degree
from theorems.prime_character_opi import ring
from theorems.ut5_matrix_phase_alignment import _rank


JSON_PATH = ROOT / "research" / "reductions" / "central_instrument_and_dual_weight_bounds_audit.json"
MD_PATH = ROOT / "research" / "CENTRAL_INSTRUMENT_AND_DUAL_WEIGHT_BOUNDS_AUDIT.md"


def verify_central_regular_instrument_and_inversion_equivalence(
    p: int = 5,
) -> dict[str, object]:
    """Verify ``QSearch.CentralRegularSource`` completeness, inversion equivalence, and ``1/|C|`` branch mass."""
    ring(p)
    omega = np.exp(2j * np.pi / p)
    # Class-2 Heisenberg N = A + C with a_width = 2, b_width = 0, c_width = 1
    st = ClassThreeStructure(p, (), (((0, 1), (p - 1, 0)),), (((), ()),))
    t_list = list(product(range(p), repeat=2))  # T = A = F_p^2
    c_list = list(range(p))                     # C = F_p
    n_list = [(x, z) for x in t_list for z in c_list]
    t_idx = {x: i for i, x in enumerate(t_list)}
    n_idx = {nz: i for i, nz in enumerate(n_list)}
    dim_t = len(t_list)  # 25
    dim_c = len(c_list)  # 5
    dim_n = len(n_list)  # 125

    # In exponential BCH coordinates on N = A x C, exp(x, (), (z,))^-1 = exp(-x, (), (-z,)):
    def inv_n(nz: tuple[tuple[int, int], int]) -> tuple[tuple[int, int], int]:
        (x0, x1), z = nz
        return (((-x0) % p, (-x1) % p), (-z) % p)

    def mult_n(
        nz1: tuple[tuple[int, int], int],
        nz2: tuple[tuple[int, int], int],
    ) -> tuple[tuple[int, int], int]:
        a_out, _, c_out = st.multiply_fixture(
            (nz1[0], (), (nz1[1],)),
            (nz2[0], (), (nz2[1],)),
        )
        return (a_out, c_out[0])

    # 1. Build CentralRegularSource.amplitude(chi, x, n) = fourierAmplitude(chi, x, coordinates(n^-1))
    # using POSITIVE central Fourier on n^-1, and compare with NEGATIVE central Fourier + A-negation!
    amp_inversion_pos = np.zeros((dim_c * dim_t, dim_n), dtype=complex)
    amp_neg_fourier_neg_a = np.zeros((dim_c * dim_t, dim_n), dtype=complex)

    for col_n, nz in enumerate(n_list):
        x_inv, z_inv = inv_n(nz)
        (a0, a1), c_orig = nz
        for lam in range(p):
            # Method A (CentralRegularSource.lean): invert n -> (x_inv, z_inv), then apply positive chi(z_inv)
            row_a = lam * dim_t + t_idx[x_inv]
            amp_inversion_pos[row_a, col_n] = (omega ** ((lam * z_inv) % p)) / np.sqrt(dim_c)
            # Method B (CENTRAL_REGULAR_JET_SOURCE.md): negate A -> (-a0, -a1) and apply negative chi(-c_orig)
            row_b = lam * dim_t + t_idx[((-a0) % p, (-a1) % p)]
            amp_neg_fourier_neg_a[row_b, col_n] = (omega ** ((-lam * c_orig) % p)) / np.sqrt(dim_c)

    inversion_equivalence_err = float(
        np.linalg.norm(amp_inversion_pos - amp_neg_fourier_neg_a, ord="fro")
    )
    assert inversion_equivalence_err == 0.0

    # 2. Verify QSearch.CentralRegularSource.instrument_complete: A^dag A == I_{|N|}
    completeness_err = float(
        np.linalg.norm(
            amp_inversion_pos.conj().T @ amp_inversion_pos - np.eye(dim_n),
            ord="fro",
        )
    )
    assert completeness_err < 1e-13

    # 3. Verify regular_branch == sector(chi, g) for g = ((1, 2), 3)
    g_sample = ((1, 2), 3)
    right_mult_perm = [n_idx[mult_n(nz, g_sample)] for nz in n_list]
    max_regular_branch_err = 0.0
    for lam in range(p):
        amp_lam = amp_inversion_pos[lam * dim_t : (lam + 1) * dim_t, :]
        # regularBranch(chi, g)[x, y] = sum_{a, b} amp(x, a) * [b == a*g] * conj(amp(y, b))
        reg_branch = amp_lam @ amp_lam[:, right_mult_perm].conj().T
        # sector(chi, g)[x, y] = [x == (g*y).1] * chi((g*y).2)
        sec_expected = np.zeros((dim_t, dim_t), dtype=complex)
        for y_i, y_vec in enumerate(t_list):
            act_x, act_z = mult_n(g_sample, (y_vec, 0))
            sec_expected[t_idx[act_x], y_i] = omega ** ((lam * act_z) % p)
        max_regular_branch_err = max(
            max_regular_branch_err,
            float(np.linalg.norm(reg_branch - sec_expected, ord="fro")),
        )
    assert max_regular_branch_err < 1e-13

    # 4. Start from actual gH labels in the direct product, not from the
    # desired potential kernel. The potential is derived only afterward.
    identity_n = ((0, 0), 0)
    powers = [identity_n]
    for _ in range(1, p):
        powers.append(mult_n(powers[-1], g_sample))
    assert mult_n(powers[-1], g_sample) == identity_n

    def mult_g(left, right):
        q, n = left
        u, h = right
        return ((q+u) % p, mult_n(n, h))

    hidden = tuple((u, powers[u]) for u in range(p))
    assert all(mult_g(hidden[u], hidden[v]) == hidden[(u+v) % p]
               for u, v in product(range(p), repeat=2))
    assert [g for g in hidden if g[0] == 0] == [(0, identity_n)]

    def public_section_n(q):
        return ((0, q*q % p), pow(q, 3, p))

    def chart(q, n):
        return (q, mult_n(n, public_section_n(q)))

    def coordinates(g):
        q, physical_n = g
        return (q, mult_n(physical_n, inv_n(public_section_n(q))))

    labels = {}
    for q, n in product(range(p), n_list):
        if (q, n) in labels:
            continue
        label = len(labels)//p
        for h in hidden:
            element = mult_g((q, n), h)
            assert element not in labels
            labels[element] = label
    assert len(labels) == p*dim_n
    assert all(sum(value == label for value in labels.values()) == p
               for label in set(labels.values()))

    label_rows = [[labels[chart(q, n)] for n in n_list] for q in range(p)]
    assert all(len(set(row)) == dim_n for row in label_rows)
    flat_labels = np.asarray(label_rows).reshape(-1)
    dim_g = p*dim_n
    inv_size_g = 1.0/dim_g
    rho_oracle = (flat_labels[:, None] == flat_labels[None, :])*inv_size_g

    # For the full quotient U=F_p and pi=id, the SAME section word gives
    # P(q)=section(0)*h(q)*section(q)^-1. A nonlinear chart allows nonlinear
    # P even though H itself is an actual subgroup of the direct product.
    def potential_n(q_val: int) -> tuple[tuple[int, int], int]:
        return mult_n(powers[q_val], inv_n(public_section_n(q_val)))

    right_action_checks = 0
    for q, u, n in product(range(p), range(p), n_list):
        assert coordinates(chart(q, n)) == (q, n)
        increment = mult_n(inv_n(potential_n(q)), potential_n((q+u) % p))
        assert coordinates(mult_g(chart(q, n), hidden[u])) == ((q+u) % p, mult_n(n, increment))
        assert labels[mult_g(chart(q, n), hidden[u])] == labels[chart(q, n)]
        right_action_checks += 1

    potential_is_homomorphism = all(
        mult_n(potential_n(q), potential_n(u)) == potential_n((q+u) % p)
        for q, u in product(range(p), repeat=2))
    assert not potential_is_homomorphism

    sector_traces: list[float] = []
    max_oracle_source_err = 0.0
    for lam in range(p):
        amp_lam = amp_inversion_pos[lam * dim_t : (lam + 1) * dim_t, :]
        # Apply (I_V x amp_lam) to rho_oracle:
        kraus_v = np.kron(np.eye(p, dtype=complex), amp_lam)
        oracle_branch = kraus_v @ rho_oracle @ kraus_v.conj().T
        sector_traces.append(float(np.trace(oracle_branch).real))

        # Expected from oracle_source_from_normal_chart:
        # invSize(C) * invSize(V) * invSize(T) * sector(chi, P(q)^-1 * P(r))
        expected_branch = np.zeros((p * dim_t, p * dim_t), dtype=complex)
        for q_val in range(p):
            for r_val in range(p):
                rel_n = mult_n(inv_n(potential_n(q_val)), potential_n(r_val))
                sec_qr = np.zeros((dim_t, dim_t), dtype=complex)
                for y_i, y_vec in enumerate(t_list):
                    act_x, act_z = mult_n(rel_n, (y_vec, 0))
                    sec_qr[t_idx[act_x], y_i] = omega ** ((lam * act_z) % p)
                expected_branch[
                    q_val * dim_t : (q_val + 1) * dim_t,
                    r_val * dim_t : (r_val + 1) * dim_t,
                ] = inv_size_g * sec_qr
        max_oracle_source_err = max(
            max_oracle_source_err,
            float(np.linalg.norm(oracle_branch - expected_branch, ord="fro")),
        )

    assert max_oracle_source_err < 1e-13
    # Every central label (including 0) has trace 1/|C| = 1/p, NEVER d_irrep^2 / |N| = p^2 / p^3 = 1/p vs reducible carrier dim^2 / |N| = p^4 / p^3 = p > 1!
    reducible_plancherel_fallacy = (dim_t ** 2) / dim_n
    assert reducible_plancherel_fallacy > 1.0

    return {
        "p": p,
        "normal_group_size": dim_n,
        "carrier_size_T": dim_t,
        "center_size_C": dim_c,
        "group_model": "direct_product_Fp_times_Heisenberg",
        "source_construction": "ordinary_gH_label_equality_after_public_chart",
        "hidden_subgroup_closure_verified": True,
        "hidden_intersection_normal_trivial_verified": True,
        "nonlinear_public_section_verified": True,
        "ordinary_coset_label_count": len(set(labels.values())),
        "ordinary_coset_fiber_size": p,
        "public_chart_right_action_checks": right_action_checks,
        "potential_is_group_homomorphism": potential_is_homomorphism,
        "inversion_vs_neg_fourier_frobenius_error": inversion_equivalence_err,
        "instrument_completeness_frobenius_error": completeness_err,
        "max_regular_branch_frobenius_error": max_regular_branch_err,
        "max_oracle_source_frobenius_error": max_oracle_source_err,
        "sector_traces_all_labels_including_zero": sector_traces,
        "wrong_reducible_plancherel_d2_over_N": reducible_plancherel_fallacy,
    }


def verify_nontrivial_central_intersection_zero_mass_obstruction(
    p: int = 5,
) -> dict[str, object]:
    """Verify that a nontrivial ``H intersect C`` creates zero-mass central labels if intersection preprocessing is bypassed."""
    ring(p)
    omega = np.exp(2j * np.pi / p)
    # Take N with 2D center C = F_p^2 and 2D noncentral T = F_p^2 (e.g., Heis_3(F_p) x F_p)
    # Suppose H intersect C = <(1, 2)> <= C = F_p^2 (a 1D central subgroup of size p inside |C| = p^2).
    # On the central register C = F_p^2, each right coset of H averages over c + u * (1, 2) for u in F_p!
    c_vecs = list(product(range(p), repeat=2))
    c_idx = {cv: i for i, cv in enumerate(c_vecs)}
    dim_c = len(c_vecs)  # 25

    # Build the central marginal density matrix of a coset state when H intersect C = <(1, 2)>:
    rho_c = np.zeros((dim_c, dim_c), dtype=complex)
    for c0 in c_vecs:
        orbit = [c_idx[((c0[0] + u) % p, (c0[1] + 2 * u) % p)] for u in range(p)]
        for i1 in orbit:
            for i2 in orbit:
                rho_c[i1, i2] += 1.0 / (dim_c * p)

    assert abs(np.trace(rho_c).real - 1.0) < 1e-12

    zero_mass_label_count = 0
    surviving_label_count = 0
    zero_mass_max_val = 0.0
    surviving_masses: list[float] = []

    for lam0, lam1 in c_vecs:
        f_vec = np.array(
            [omega ** ((lam0 * z0 + lam1 * z1) % p) for z0, z1 in c_vecs],
            dtype=complex,
        ) / np.sqrt(dim_c)
        mass = float(np.real(np.vdot(f_vec, rho_c @ f_vec)))
        if (lam0 + 2 * lam1) % p == 0:
            surviving_label_count += 1
            surviving_masses.append(round(mass, 12))
        else:
            zero_mass_label_count += 1
            zero_mass_max_val = max(zero_mass_max_val, abs(mass))

    assert zero_mass_label_count == p * (p - 1)
    assert surviving_label_count == p
    assert zero_mass_max_val < 1e-15
    assert all(abs(m - 1.0 / p) < 1e-12 for m in surviving_masses)

    return {
        "p": p,
        "center_size_C": dim_c,
        "h_intersect_c_generator": [1, 2],
        "zero_mass_label_count": zero_mass_label_count,
        "surviving_annihilator_label_count": surviving_label_count,
        "max_zero_mass_label_probability": zero_mass_max_val,
        "surviving_label_probability": surviving_masses[0],
    }


def verify_dual_weight_class_three_phase_bounds(
    p: int = 17,
    degree: int = 3,
) -> dict[str, object]:
    """Verify ``QSearch.ClassThreePhaseBounds.operational_bound`` and ``parameter_bound`` on ``compile_full_jet_phase``."""
    ring(p)
    # Use UT_4(F_p) where beta != 0 and delta != 0 so degree-3D operational and degree-2 parameter terms are active!
    st = ClassThreeStructure(
        p,
        (((0, 1, 0), (p - 1, 0, 0), (0, 0, 0)), ((0, 0, 0), (0, 0, 1), (0, p - 1, 0))),
        (((0, 0, 1), (0, 0, 0), (p - 1, 0, 0)),),
        (((0, 1), (0, 0), (p - 1, 0)),),
    )
    chart = FullTaylorJetChart(p=p, quotient_width=1, noncentral_width=3, degree=degree)
    rows: list[list[int]] = []
    scales: list[int] = []
    outcomes: list[tuple[int, ...]] = []
    for s_val, y_val in product(range(1, degree + 2), product(range(degree + 1), repeat=1)):
        row = [
            pow(s_val, k, p) * prod(pow(v, e, p) for v, e in zip(y_val, alpha)) % p
            for alpha, k, a in chart.indices
            if a == 0
        ]
        if _rank(rows + [row], p) > len(rows):
            rows.append(row)
            scales.append(s_val)
            outcomes.append(y_val)

    labels = [((i % (p - 1)) + 1,) for i in range(len(rows))]
    alignment = align_full_jet(chart, st, labels, scales, outcomes)
    spectator = tuple((i + 1) % p for i in range(alignment.carrier_width - chart.jet_width))
    cdeg = degree + 2
    pkt = compile_full_jet_phase(alignment, spectator, cdeg)

    # 1. Operational weight w_op: w_op(q) = 1, w_op(t_{alpha, k, a}) = k
    max_op_weight = weighted_degree(chart, pkt)
    op_bound = max(cdeg, 3 * degree)
    assert max_op_weight == op_bound

    # 2. Hidden-parameter weight w_param: w_param(theta_m) = 1, w_param(q) = 0, w_param(t) = 0
    param_weights = {len(params) for (_, params), coeff in pkt.terms.items() if coeff}
    max_param_weight = max(param_weights)
    assert max_param_weight == 2
    assert param_weights <= {0, 1, 2}

    # 3. Verify that parameter-weight-2 terms come exclusively from A/B noncentral coordinates (never C coordinates!)
    c_coord_idx = st.a_width + st.b_width  # 3 + 2 = 5
    c_param_indices = {
        idx for idx, (coord, _) in enumerate(pkt.parameter_basis) if coord >= c_coord_idx
    }
    c_in_quadratic_param_terms = any(
        len(params) == 2 and any(p_i in c_param_indices for p_i in params)
        for (_, params), coeff in pkt.terms.items()
        if coeff
    )
    assert not c_in_quadratic_param_terms

    return {
        "prime_bits": p.bit_length(),
        "jet_degree_D": degree,
        "central_degree_c": cdeg,
        "operational_weight_bound_max_c_3D": op_bound,
        "attained_max_operational_weight": max_op_weight,
        "parameter_weight_bound": 2,
        "attained_parameter_weights": sorted(param_weights),
        "central_parameters_appear_in_quadratic_parameter_lifts": c_in_quadratic_param_terms,
    }


def build_central_instrument_and_dual_weight_bounds_report() -> dict[str, object]:
    """Build the report from an independently prepared ordinary hiding source."""
    p_127 = (1 << 127) - 1
    inst_audit = verify_central_regular_instrument_and_inversion_equivalence(p=5)
    obstruction_audit = verify_nontrivial_central_intersection_zero_mass_obstruction(p=5)
    bounds_d2 = verify_dual_weight_class_three_phase_bounds(p=11, degree=2)
    bounds_d3 = verify_dual_weight_class_three_phase_bounds(p=17, degree=3)
    bounds_127 = verify_dual_weight_class_three_phase_bounds(p=p_127, degree=2)

    return {
        "schema_version": "central_instrument_and_dual_weight_bounds_audit_v2",
        "module": "theorems/central_instrument_and_dual_weight_bounds_audit.py",
        "scope": {
            "central_regular_instrument_completeness_verified": True,
            "normal_inversion_vs_lie_negation_equivalence_verified": True,
            "transverse_uniform_1_over_C_branch_mass_verified": True,
            "ordinary_hiding_source_and_public_chart_verified": True,
            "full_jet_algorithm_input_premises_verified": False,
            "nontrivial_h_intersect_c_zero_mass_obstruction_verified": True,
            "dual_weight_operational_and_parameter_bounds_verified": True,
            "accepted_speedup_candidate": False,
            "novelty_claim": False,
            "speedup_claim_allowed": False,
        },
        "central_regular_instrument_audit": inst_audit,
        "nontrivial_central_intersection_obstruction_audit": obstruction_audit,
        "dual_weight_phase_bounds_controls": [bounds_d2, bounds_d3, bounds_127],
    }


def render_markdown(report: dict[str, object]) -> str:
    ia = report["central_regular_instrument_audit"]
    oa = report["nontrivial_central_intersection_obstruction_audit"]
    b_rows = "\n".join(
        f"| `{row['prime_bits']}` | `{row['jet_degree_D']}` | `{row['central_degree_c']}` | `{row['attained_max_operational_weight']} / {row['operational_weight_bound_max_c_3D']}` | `{row['attained_parameter_weights']}` (max `{row['parameter_weight_bound']}`) | `{row['central_parameters_appear_in_quadratic_parameter_lifts']}` |"
        for row in report["dual_weight_phase_bounds_controls"]
    )
    return f"""# Complete Central Fourier Instrument, Nontrivial $H \\cap C$ Zero-Mass Falsifier, and Dual-Weight Class-Three Phase Bounds Audit

2026-10-21. **Standalone finite controls for `Formal/CentralRegularSource.lean` and `Formal/ClassThreePhaseBounds.lean`; not formal Python refinement, an admitted speedup candidate, or a novelty claim.**

## 1. Summary of Verified Contracts

This note documents `theorems/central_instrument_and_dual_weight_bounds_audit.py` and `tests/test_central_instrument_and_dual_weight_bounds_audit.py`, covering `## 2026-10-21 Complete Central Instrument Contract` in `research/MECHANICAL_FOLLOW_UP_PLAN.md`:

1. **Complete Central Instrument & Group-Inversion vs Lie-Coordinate Negation Equivalence (`verify_central_regular_instrument_and_inversion_equivalence`)**:
   - Uses the actual direct product $G = \\mathbb{{F}}_5 \\times \\text{{Heis}}_3(\\mathbb{{F}}_5)$ ($|N| = {ia["normal_group_size"]}, |T| = {ia["carrier_size_T"]}, |C| = {ia["center_size_C"]}$), a verified cyclic transverse subgroup, and a nonlinear PUBLIC normal-first chart.
   - Constructs the density matrix from equality of independently assigned ordinary $gH$ labels: `{ia["ordinary_coset_label_count"]}` fibers of size `{ia["ordinary_coset_fiber_size"]}`. Checks subgroup closure, trivial normal intersection, chart inverses and `{ia["public_chart_right_action_checks"]}` right-action identities. The potential is derived from the shared section word only AFTER the oracle equality table is built.
   - Exact Frobenius difference between normal group inversion $n \\mapsto n^{{-1}}$ + positive central Fourier (`CentralRegularSource.amplitude`) and negative central Fourier + logarithmic coordinate negation $(a, b) \\mapsto (-a, -b)$: `{ia["inversion_vs_neg_fourier_frobenius_error"]}`.
   - Instrument completeness Frobenius error: `{ia["instrument_completeness_frobenius_error"]:.2e}`; regular branch error: `{ia["max_regular_branch_frobenius_error"]:.2e}`; oracle source contraction error: `{ia["max_oracle_source_frobenius_error"]:.2e}`.
   - Every central label $\\lambda \\in \\mathbb{{F}}_5$ (including $\\lambda = 0$) has numerical mass `{ia["sector_traces_all_labels_including_zero"][0]}`, agreeing with the exact theoretical value $1/|C|$. The reducible carrier expression $|T|^2/|N| = {ia["wrong_reducible_plancherel_d2_over_N"]}$ is invalid.
2. **Nontrivial $H \\cap C$ Zero-Mass Label Falsifier (`verify_nontrivial_central_intersection_zero_mass_obstruction`)**:
   - When $H \\cap C = \\langle (1, 2) \\rangle \\le \\mathbb{{F}}_5^2$ is nontrivial (bypassing recursive intersection learning), `{oa["zero_mass_label_count"]}/{oa["center_size_C"]}` central labels have zero branch mass (`max_probability = {oa["max_zero_mass_label_probability"]:.2e}`), while only the `{oa["surviving_annihilator_label_count"]}` labels in $(H \\cap C)^\\perp$ survive with mass `{oa["surviving_label_probability"]}`.
3. **Dual-Weight Filtered-Polynomial Compiler Bounds (`verify_dual_weight_class_three_phase_bounds`)**:
   - Pins `compile_full_jet_phase` to `QSearch.ClassThreePhaseBounds.operational_bound` ($\\le \\max(c, 3D)$) and `parameter_bound` ($\\le 2$) (`formal/Formal/ClassThreePhaseBounds.lean`) across $p \\in \\{{11, 17, 2^{{127}} - 1\\}}$.

## 2. Dual-Weight Compiler Bounds Summary Table

| Prime Bits | Jet Degree $D$ | Central Degree $c$ | Attained / Bound Operational Weight $\\max(c, 3D)$ | Attained Parameter Weights $w_{{\\text{{param}}}}$ | Central Params in Degree-2 Lifts |
| :--- | :--- | :--- | :--- | :--- | :--- |
{b_rows}

## 3. Explicit Scope Boundaries

- Version 1 built its purported ordinary source directly from a chosen nonlinear potential, without specifying a compatible group/subgroup/chart. Its matrix agreement was only a potential-kernel contraction check. Version 2 replaces that circular source fixture with actual group cosets; no theorem is inferred from the old fixture.
- A nonlinear potential is allowed after a verified public section change. Its graph in the STANDARD direct-product coordinates need not be a subgroup. The regression test distinguishes these statements; it does not ban nonlinear potentials.
- This nonlinear public section does NOT satisfy the linear Lie-section premise used to derive the full algorithm's ambient degree bounds. The general central-instrument theorem permits it, but this fixture does not verify the full-jet algorithm's input premises.
- This source control uses class-two Heisenberg N. It is not a class-three/vector-center source-to-B-Fourier composition theorem. The existing independent class-three controls and the universal Lean results retain their separate scopes.
- Related literature context: [Ivanyos and Santha (2015)](https://arxiv.org/abs/1503.09016) for fixed-degree polynomial phase erasure; [Holt and Subramanian (2026)](https://arxiv.org/html/2609.38085v2) for state-symmetry reductions.
- All novelty and speedup flags (`accepted_speedup_candidate`, `novelty_claim`, `speedup_claim_allowed`) are `False`.
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Write JSON and Markdown artifacts.")
    args = parser.parse_args()
    report = build_central_instrument_and_dual_weight_bounds_report()
    if args.write:
        JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
        JSON_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        MD_PATH.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({"module": report["module"], "schema_version": report["schema_version"]}, indent=2))


if __name__ == "__main__":
    main()
