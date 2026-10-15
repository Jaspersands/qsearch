"""DCP shifted-box source producer, equal-label heralding, and collective majority audit.

Implements and proves:
1. Finite Regev shifted-box intersection [0,M)^n cap ([0,M)^n - v_shift) producer,
   deriving the exact balanced bad-register PhaseDensity law (a=1/2, v=1-p_bad)
   from translation symmetry |B_0| = |B_1| = M^n - |G|.
2. Two-copy equal-label collision CNOT heralding dichotomy (sum branch 2k vs
   secret-independent difference branch 0).
3. Exact collective quantum Helstrom optimality of product X-basis majority vote
   on R = 2m+1 parity-label target copies and Fuchs-van de Graaf fidelity copy bounds.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
from itertools import product
import json
from math import comb, isqrt
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "core") not in sys.path:
    sys.path.insert(0, str(ROOT / "core"))

from dcp_physical_bad_register_lineage import PhaseDensity, balanced_lineage_ledger, merge, source_density
from native_basis_lottery import _certificate_int
from native_small_multiple_completion import _rational
from ternary_measured_lattice_decoder import exact_json, integer

DERIVATION = ROOT / "research/DCP_COLLECTIVE_MAJORITY_PURIFICATION_AUDIT.md"
CONTRACT = ROOT / "research/hypotheses/dcp_collective_majority_purification_audit_contract.json"
REPORT = ROOT / "research/phase_workbench/dcp_collective_majority_purification_audit.json"


def shifted_box_source_producer(box_side_M, shift_vector, dcp_modulus_N, measured_label_k, source_id, max_cells=100000):
    """Construct the exact Regev shifted-box cell partition and PhaseDensity."""
    integer(box_side_M, "positive box side M", 2)
    integer(dcp_modulus_N, "positive DCP modulus N", 2)
    integer(measured_label_k, "canonical measured label k", 0)
    integer(max_cells, "positive cell census cap", 1)
    if measured_label_k >= dcp_modulus_N:
        raise ValueError("canonical measured label k < N required")
    shift = tuple(shift_vector)
    if not shift or any(type(v) is not int or abs(v) >= box_side_M for v in shift):
        raise ValueError("nonempty integer shift vector with |v_i| < M required")
    n = len(shift)
    total_box_points = box_side_M ** n

    # Analytical good-pair count |G| = prod_i (M - |v_i|)
    good_pairs_count = 1
    for v in shift:
        good_pairs_count *= box_side_M - abs(v)
    bad_zero_count = total_box_points - good_pairs_count
    bad_one_count = total_box_points - good_pairs_count
    total_basis_states = 2 * total_box_points
    if good_pairs_count * 2 + bad_zero_count + bad_one_count != total_basis_states:
        raise ArithmeticError("shifted-box basis-state conservation failed")

    # Explicit cell enumeration when total_box_points <= max_cells
    explicit_census_verified = False
    if total_box_points <= max_cells:
        box0 = set(product(range(box_side_M), repeat=n))
        box1 = {tuple(x - v for x, v in zip(pt, shift)) for pt in box0}
        G_set = box0 & box1
        B0_set = box0 - box1
        B1_set = box1 - box0
        if (
            len(G_set) != good_pairs_count
            or len(B0_set) != bad_zero_count
            or len(B1_set) != bad_one_count
        ):
            raise ArithmeticError("explicit shifted-box set intersection disagreed with product formula")
        explicit_census_verified = True

    p_good = Fraction(2 * good_pairs_count, total_basis_states)
    p_bad = 1 - p_good
    union_bad_upper = min(Fraction(1), sum(Fraction(abs(v), box_side_M) for v in shift))
    if p_bad > union_bad_upper:
        raise ArithmeticError("exact box bad probability exceeded additive union upper bound")

    b_zero = Fraction(1, 2) if p_bad == 0 else Fraction(bad_zero_count, bad_zero_count + bad_one_count)
    if b_zero != Fraction(1, 2):
        raise ArithmeticError("translation symmetry |B_0| == |B_1| violated")

    density = source_density(dcp_modulus_N, measured_label_k, source_id, p_bad, b_zero)
    return {
        "dimension_n": n,
        "box_side_M": box_side_M,
        "shift_vector": shift,
        "dcp_modulus_N": dcp_modulus_N,
        "measured_Fourier_label": measured_label_k,
        "total_box_cells_M_pow_n": total_box_points,
        "total_superposition_basis_states_2_M_pow_n": total_basis_states,
        "good_interior_pair_cells_G": good_pairs_count,
        "bad_zero_boundary_cells_B0": bad_zero_count,
        "bad_one_boundary_cells_B1": bad_one_count,
        "translation_symmetry_B0_equals_B1": bad_zero_count == bad_one_count,
        "exact_good_register_probability": str(p_good),
        "exact_bad_register_probability": str(p_bad),
        "additive_union_bad_probability_upper": str(union_bad_upper),
        "exact_bad_zero_conditional_probability": str(b_zero),
        "explicit_cell_intersection_verified": explicit_census_verified,
        "produced_phase_density_audit": density.audit_record(),
        "phase_density_object": density,
    }


def equal_label_collision_heralding(dcp_modulus_N, nonzero_label_k, p_bad_left, p_bad_right):
    """Audit CNOT merging of two independent copies at the SAME nonzero label k."""
    integer(dcp_modulus_N, "DCP modulus N", 3)
    integer(nonzero_label_k, "nonzero measured label k", 1)
    if nonzero_label_k >= dcp_modulus_N:
        raise ValueError("nonzero label k in [1, N-1] required")
    left = source_density(dcp_modulus_N, nonzero_label_k, "equal-label:left", p_bad_left, "1/2")
    right = source_density(dcp_modulus_N, nonzero_label_k, "equal-label:right", p_bad_right, "1/2")

    sum_merge, sum_out = merge(left, right, 0, independent_given_secret=True)
    diff_merge, diff_out = merge(left, right, 1, independent_given_secret=True)

    v1 = left.phase_visibility
    v2 = right.phase_visibility
    v_prod = v1 * v2
    if Fraction(sum_out.phase_visibility) != v_prod or Fraction(diff_out.phase_visibility) != v_prod:
        raise ArithmeticError("equal-label CNOT visibility product mismatch")
    if diff_out.label != 0 or sum_out.label != (2 * nonzero_label_k) % dcp_modulus_N:
        raise ArithmeticError("equal-label CNOT output labels mismatch")

    # On the difference branch (label 0), the state is independent of s in Z_N:
    # rho_diff(0) = [[1/2, v1*v2/2], [v1*v2/2, 1/2]] = ((1+v1*v2)/2)|+><+| + ((1-v1*v2)/2)|-><-|
    plus_accept = (1 + v_prod) / 2
    minus_accept = (1 - v_prod) / 2

    return {
        "dcp_modulus_N": dcp_modulus_N,
        "colliding_input_label_k": nonzero_label_k,
        "left_bad_probability": str(_rational(p_bad_left)),
        "right_bad_probability": str(_rational(p_bad_right)),
        "left_visibility_v1": str(v1),
        "right_visibility_v2": str(v2),
        "product_visibility_v1_v2": str(v_prod),
        "sum_branch_z0": sum_merge,
        "difference_branch_z1": diff_merge,
        "difference_branch_has_zero_label": diff_out.label == 0,
        "difference_branch_X_plus_acceptance": str(plus_accept),
        "difference_branch_X_minus_acceptance": str(minus_accept),
        "difference_branch_estimates_v1_v2_without_secret_s": True,
        "difference_branch_carries_hidden_secret_information": False,
        "postselecting_difference_branch_leaves_surviving_label_k_copy": False,
    }


def exact_majority_vote_ledger(odd_copies_R, single_copy_visibility):
    """Compute exact majority-vote and Helstrom success on R = 2m+1 parity copies."""
    integer(odd_copies_R, "positive odd copy count R", 1)
    if odd_copies_R % 2 != 1 or odd_copies_R > 511:
        raise ValueError("odd copy count R in [1, 511] required")
    v = _rational(single_copy_visibility)
    if not 0 <= v <= 1:
        raise ValueError("single-copy visibility v in [0, 1] required")
    m = (odd_copies_R - 1) // 2
    q_plus = (1 + v) / 2
    q_minus = (1 - v) / 2

    p_maj = Fraction(0)
    for j in range(m + 1, odd_copies_R + 1):
        p_maj += comb(odd_copies_R, j) * (q_plus ** j) * (q_minus ** (odd_copies_R - j))

    # Helstrom trace norm (1/2)*||rho_even^(tensor R) - rho_odd^(tensor R)||_1
    # Because [rho_even, rho_odd] = 0 in the X-basis, eigenvalues of the difference are:
    # q_plus^j q_minus^(R-j) - q_minus^j q_plus^(R-j)
    half_trace_norm = Fraction(0)
    for j in range(odd_copies_R + 1):
        eig_diff = (q_plus ** j) * (q_minus ** (odd_copies_R - j)) - (q_minus ** j) * (q_plus ** (odd_copies_R - j))
        half_trace_norm += abs(eig_diff) * comb(odd_copies_R, j)
    half_trace_norm /= 2

    p_helstrom = Fraction(1, 2) + half_trace_norm / 2
    v_maj = 2 * p_maj - 1
    if p_maj != p_helstrom or v_maj != half_trace_norm:
        raise ArithmeticError("product X-basis majority vote disagreed with collective Helstrom optimum")

    # Fuchs-van de Graaf / fidelity upper bound: v_maj^2 <= 1 - (1 - v^2)^R <= R * v^2
    fidelity_sq = (1 - v * v) ** odd_copies_R
    fvdg_upper_sq = 1 - fidelity_sq
    linear_upper_sq = odd_copies_R * v * v
    if not (v_maj * v_maj <= fvdg_upper_sq <= linear_upper_sq):
        raise ArithmeticError("Fuchs-van de Graaf fidelity inequality failed")

    return {
        "odd_target_copies_R": odd_copies_R,
        "single_copy_visibility_v": str(v),
        "single_copy_X_plus_probability": str(q_plus),
        "exact_majority_vote_success_probability": str(p_maj),
        "exact_collective_Helstrom_success_probability": str(p_helstrom),
        "purified_majority_visibility_v_maj": str(v_maj),
        "half_trace_distance_norm": str(half_trace_norm),
        "product_X_majority_equals_collective_Helstrom_optimum": p_maj == p_helstrom,
        "v_maj_squared": str(v_maj * v_maj),
        "fuchs_van_de_graaf_1_minus_fidelity_sq_upper": str(fvdg_upper_sq),
        "linear_R_v_squared_upper": str(linear_upper_sq),
        "fidelity_chain_inequality_verified": v_maj * v_maj <= fvdg_upper_sq <= linear_upper_sq,
        "entangling_collective_POVM_can_beat_X_majority_at_parity_label": False,
    }


def end_to_end_purified_lineage_profile(logN, failure_parameter, merge_depth, target_purified_visibility="1/2"):
    """Combine balanced merge-tree lineage with Fuchs-van de Graaf copy lower bounds."""
    base = balanced_lineage_ledger(logN, failure_parameter, merge_depth)
    v_upper = Fraction(base["output_phase_visibility_upper"])
    v_targ = _rational(target_purified_visibility)
    if not 0 < v_targ <= 1:
        raise ValueError("positive target purified visibility required")
    leaves_per_copy = _certificate_int(base["disjoint_original_state_leaves"])

    if v_upper == 0:
        raise ArithmeticError("positive visibility upper bound expected")
    # From v_maj(R, v)^2 <= R * v^2, reaching v_maj >= v_targ requires R >= ceil(v_targ^2 / v_upper^2)
    ratio = (v_targ * v_targ) / (v_upper * v_upper)
    min_copies_fvdg = (ratio.numerator + ratio.denominator - 1) // ratio.denominator
    if min_copies_fvdg % 2 == 0:
        min_copies_fvdg += 1
    total_disjoint_leaves_lower = min_copies_fvdg * leaves_per_copy

    return {
        "log2_original_modulus": logN,
        "failure_parameter": failure_parameter,
        "balanced_merge_depth": merge_depth,
        "disjoint_leaves_per_target_copy": leaves_per_copy,
        "single_target_visibility_upper": str(v_upper),
        "target_purified_visibility": str(v_targ),
        "minimum_odd_target_copies_by_fvdg_bound": min_copies_fvdg,
        "minimum_total_disjoint_original_leaves": total_disjoint_leaves_lower,
        "base_lineage_ledger": base,
        "collective_entangling_parity_readout_reduces_copy_requirement": False,
    }


def build_report():
    deps = (
        "dcp_physical_bad_register_lineage.py",
        "native_basis_lottery.py",
        "native_small_multiple_completion.py",
        "ternary_measured_lattice_decoder.py",
    )
    box_controls = []
    for M, shift, N, k, sid in (
        (8, (1, -2), 32, 11, "box:2d:small"),
        (6, (1, 1, -2), 64, 19, "box:3d:small"),
        (2 ** 20, (3, -5, 7, -2), 1024, 33, "box:4d:large"),
    ):
        prod = shifted_box_source_producer(M, shift, N, k, sid)
        box_controls.append({k_name: v_val for k_name, v_val in prod.items() if k_name != "phase_density_object"})

    heralding_controls = (
        equal_label_collision_heralding(32, 7, "1/8", "1/8"),
        equal_label_collision_heralding(64, 15, "1/16", "1/4"),
        equal_label_collision_heralding(32, 9, "0", "1"),
    )

    majority_controls = tuple(
        exact_majority_vote_ledger(R, v)
        for R, v in ((1, "1/2"), (3, "1/2"), (5, "1/3"), (7, "1/4"), (9, "1/5"))
    )

    purified_profiles = tuple(
        end_to_end_purified_lineage_profile(logN, f, isqrt(logN) + int(isqrt(logN) ** 2 < logN))
        for logN, f in ((32, 1), (128, 1), (1024, 2), (4096, 2))
    )

    return {
        "status": "DCP_SHIFTED_BOX_PRODUCER_AND_COLLECTIVE_MAJORITY_AUDIT_REVIEW_PENDING",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
        "contract_sha256": hashlib.sha256(CONTRACT.read_bytes()).hexdigest(),
        "dependency_sha256": {
            f: hashlib.sha256((ROOT / "theorems" / f).read_bytes()).hexdigest() for f in deps
        },
        "shifted_box_source_controls": tuple(box_controls),
        "equal_label_heralding_controls": heralding_controls,
        "collective_majority_helstrom_controls": majority_controls,
        "end_to_end_purified_lineage_profiles": purified_profiles,
        "finite_shifted_box_lattice_producer_implemented": True,
        "general_dcp_or_dhsp_no_go_claimed": False,
        "full_bad_register_dcp_solver_supplied": False,
        "accepted_speedup_candidate": False,
        "new_active_negative_result_created": False,
        "novelty_claim": False,
        "research_decision": "SHIFTED_BOX_GEOMETRY_EXPLAINS_BALANCED_BAD_LAW_AND_PRODUCT_X_MAJORITY_IS_HELSTROM_OPTIMAL_ON_PARITY_COPIES",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    rep = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(rep), indent=2) + "\n")
    print(
        json.dumps(
            {
                "status": rep["status"],
                "shifted_box_controls": len(rep["shifted_box_source_controls"]),
                "majority_helstrom_matches": [
                    m["product_X_majority_equals_collective_Helstrom_optimum"]
                    for m in rep["collective_majority_helstrom_controls"]
                ],
                "full_dcp_solver_supplied": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
