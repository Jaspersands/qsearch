"""Planted q-ary offset-average pair-mass frontier and q-independent dyadic (M_box, W) schedules.

Connects `theorems/planted_qary_usvp_source.py`, `theorems/lattice_cube_coset_source.py`
(`offset_average_pair_mass`), and `theorems/planted_qary_cube_basis_coordinate_bridge.py` by proving:
1. Theorem 1 (Support-Only Cube Survival Law):
   For any planted ternary vector `u in {-1, 0, 1}^n \\ {0}` with Hamming support `s = ||u||_1`,
   `P_cube(W, u) = (1 - 1/W)^s`, satisfying `1 - s/W <= P_cube(W, u) <= 1 / (1 + s/W)`.
2. Theorem 2 (Worst-Case Multiplicative and Additive Box Survival Bounds):
   On any hitting free coordinate `j_coord = m + j_0` with deterministic `(p_split = nextprime(W), g_res = 1)`,
   `P_box(M_box, delta) >= P_box^min(M_box, m, s_F) := (1 - 1/M_box)^(s_F - 1) * (1 - B_tern(s_F)/M_box)^m`
   `>= 1 - L_box(m, s_F) / M_box`, where `L_box(m, s_F) = (s_F - 1) + m * B_tern(s_F)`.
3. Theorem 3 (Modulus-Independent Dyadic Schedule for the `1/ell` Partner-Failure Budget):
   Choosing the smallest integer `b >= 1` with `2^b >= max(2, 2*n*(b + 1)*L_box(m, s_F))` and
   `w = ceil(log_2(2*n*(b + 1)*s))` gives `M_box = 2^b` and `W = 2^w` certifying
   `partner_failure <= 1 / ell` (`ell = n*(b + 1)`) for all prime moduli `q >= 3`.
   This is a DCP bad-register bound ONLY under an independently established
   at-most-two/common-partner geometry promise. No such promise is inferred here.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from math import prod
from pathlib import Path
from typing import Any

from sympy import nextprime

from theorems.lattice_cube_coset_source import CubeCosetSource, exact_int, offset_average_pair_mass
from theorems.planted_qary_cube_basis_coordinate_bridge import (
    basis_coordinates_from_public_lattice,
    ternary_pivot_envelope,
)
from theorems.planted_qary_usvp_source import PublicQaryLattice, generate_source


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "research" / "hypotheses" / "planted_qary_offset_pair_mass_frontier_audit_contract.json"
ARTIFACT_PATH = ROOT / "research" / "reductions" / "planted_qary_offset_pair_mass_frontier_audit.json"
DOC_PATH = ROOT / "research" / "PLANTED_QARY_OFFSET_PAIR_MASS_FRONTIER_AUDIT.md"


def _fraction_str(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def _ceil_log2_int(val: int) -> int:
    if val <= 1:
        return 1
    return (int(val) - 1).bit_length()


def worst_case_box_l1_ceiling(m: int, s_F: int) -> int:
    """Return L_box(m, s_F) = (s_F - 1) + m * B_tern(s_F)."""
    if s_F < 1:
        raise ValueError("Require s_F >= 1")
    exact_int(m, "positive constraint count", 1)
    return (s_F - 1) + m * ternary_pivot_envelope(s_F)


def worst_case_multiplicative_box_survival(m_box: int, m: int, s_F: int) -> Fraction:
    """Return P_box^min(M_box, m, s_F) = (1 - 1/M_box)^(s_F - 1) * (1 - B_tern(s_F)/M_box)^m."""
    b_tern = ternary_pivot_envelope(s_F)
    exact_int(m, "positive constraint count", 1)
    exact_int(m_box, "box", 2)
    if m_box <= b_tern or m_box < 2:
        raise ValueError("Require M_box > B_tern(s_F) and M_box >= 2")
    free_factor = Fraction(m_box - 1, m_box) ** (s_F - 1)
    piv_factor = Fraction(m_box - b_tern, m_box) ** m
    return free_factor * piv_factor


def compute_dyadic_f1_schedule(n: int, m: int, s: int, s_F: int) -> dict[str, Any]:
    """Schedule partner survival; geometry and public parameter selection remain separate."""
    for value in (n, m, s, s_F):
        exact_int(value, "positive schedule parameter", 1)
    if not (1 <= m < n and 1 <= s <= n and 1 <= s_F <= min(s, n - m)):
        raise ValueError("Invalid (n, m, s, s_F) parameters")
    l_box = worst_case_box_l1_ceiling(m, s_F)
    b_tern = ternary_pivot_envelope(s_F)

    b = 1
    while (1 << b) < max(2, b_tern + 1, 2 * n * (b + 1) * l_box):
        b += 1
    m_box = 1 << b
    ell = n * (b + 1)
    w = max(1, _ceil_log2_int(2 * ell * s))
    width = 1 << w

    p_cube = Fraction(width - 1, width) ** s
    p_box_min = worst_case_multiplicative_box_survival(m_box, m, s_F)
    p_good_min = p_box_min * p_cube
    p_bad_max_mult = Fraction(1, 1) - p_good_min
    p_bad_max_add = Fraction(l_box, m_box) + Fraction(s, width)
    f1_budget = Fraction(1, ell)

    return {
        "n": int(n),
        "m": int(m),
        "support_s": int(s),
        "free_support_s_F": int(s_F),
        "B_tern_s_F": int(b_tern),
        "L_box_ceiling": int(l_box),
        "b_box_exponent": int(b),
        "M_box": int(m_box),
        "w_width_exponent": int(w),
        "width_W": int(width),
        "ell_position_wires": int(ell),
        "f1_budget_fraction": _fraction_str(f1_budget),
        "P_cube_exact_fraction": _fraction_str(p_cube),
        "P_box_min_multiplicative_fraction": _fraction_str(p_box_min),
        "partner_failure_multiplicative_upper_fraction": _fraction_str(p_bad_max_mult),
        "partner_failure_multiplicative_upper_float": float(p_bad_max_mult),
        "partner_failure_additive_upper_fraction": _fraction_str(p_bad_max_add),
        "partner_failure_additive_upper_float": float(p_bad_max_add),
        "source_bad_register_rate_certified": False,
        "requires_independent_two_point_geometry": True,
        "fresh_uniform_offsets_required": True,
        "f1_budget_float": float(f1_budget),
        "multiplicative_bound_within_f1_budget": bool(p_bad_max_mult <= f1_budget),
        "additive_bound_within_f1_budget": bool(p_bad_max_add <= f1_budget),
    }


def conditional_geometry_obligation(n: int, width: int, split_prime: int,
                                    nonparallel_norm_squared_lower: int) -> dict[str, Any]:
    """Check sufficient inequalities, NEVER certify the supplied norm promise.

    Same-cell integer differences have squared norm <= n*(W-1)^2.
    A primitive ternary vector has |k*u|_infinity=|k|; splitting at a
    hitting free coordinate admits only k=0 within a colour and k=+/-1
    across colours when p-1>=W. Other vectors need a separate lower bound.
    """
    for value, name, lower in ((n, "dimension", 1), (width, "width", 2),
                               (split_prime, "split modulus", 3),
                               (nonparallel_norm_squared_lower, "norm lower bound", 1)):
        exact_int(value, name, lower)
    nonparallel = nonparallel_norm_squared_lower > n * (width - 1) ** 2
    collinear = split_prime - 1 >= width
    return {
        "same_cell_squared_distance_upper": n * (width - 1) ** 2,
        "assumed_nonparallel_squared_norm_lower": nonparallel_norm_squared_lower,
        "nonparallel_exclusion_inequality_satisfied": nonparallel,
        "collinear_exclusion_inequality_satisfied": collinear,
        "conditional_geometry_inequalities_satisfied": nonparallel and collinear,
        "nonparallel_norm_lower_bound_verified": False,
        "requires_primitive_ternary_vector_and_hitting_free_trial": True,
        "requires_prime_split_modulus": True,
        "source_geometry_certified": False,
    }


def same_colour_collision_counterexample() -> dict[str, Any]:
    """Exact public counterexample to inferring source quality from partner mass."""
    problem = PublicQaryLattice(3, ((1, 1, 1),))
    schedule = compute_dyadic_f1_schedule(3, 1, 3, 2)
    source = CubeCosetSource(problem.basis, int(nextprime(schedule["width_W"])),
                             1, 1, schedule["M_box"], schedule["width_W"], (1, 1, 1))
    positions = ((0, 0, 2), (0, 0, 3))
    points = tuple(source.lattice_point(0, a) for a in positions)
    cells = tuple(source.cell(0, a) for a in positions)
    return {"public_source": json.loads(json.dumps(source.public_access())), "schedule": schedule,
            "same_colour": 0, "distinct_positions": [list(a) for a in positions],
            "public_lattice_points": [list(x) for x in points], "cells": [list(c) for c in cells],
            "partner_budget_inequality_passes": schedule["multiplicative_bound_within_f1_budget"],
            "same_colour_collision_verified": positions[0] != positions[1] and cells[0] == cells[1],
            "two_point_source_promise_falsified": cells[0] == cells[1],
            "scope": "COUNTEREXAMPLE_TO_UNCONDITIONAL_PARTNER_MASS_TO_DCP_TRANSFER"}


def audit_planted_instance_offset_pair_mass_frontier() -> list[dict[str, Any]]:
    """Audit Theorems 1, 2, and 3 across planted q-ary instances up to n=32 and q > 2^80."""
    configs = [
        {"n": 4, "m": 2, "q": 257, "support": 3, "seed": 11},
        {"n": 6, "m": 3, "q": 1009, "support": 4, "seed": 17},
        {"n": 8, "m": 4, "q": 65537, "support": 6, "seed": 23},
        {"n": 10, "m": 5, "q": 1000003, "support": 7, "seed": 29},
        {"n": 12, "m": 6, "q": 1000000007, "support": 8, "seed": 37},
        {"n": 16, "m": 8, "q": 1000000007, "support": 10, "seed": 41},
        {"n": 32, "m": 16, "q": 1000000007, "support": 18, "seed": 47},
        {"n": 8, "m": 4, "q": int(nextprime(2**80)), "support": 6, "seed": 53},
    ]
    rows: list[dict[str, Any]] = []
    for cfg in configs:
        gen = generate_source(
            n=cfg["n"],
            m=cfg["m"],
            q=cfg["q"],
            gap=2,
            support=cfg["support"],
            plant_seed=cfg["seed"],
            matrix_seed=cfg["seed"] + 300,
        )
        problem = gen.problem
        u = gen.private.plant
        d_full = basis_coordinates_from_public_lattice(problem, u)
        m = problem.rows
        n = problem.dimension
        s = sum(1 for x in u if x != 0)
        s_F = sum(1 for j in range(n - m) if d_full[m + j] != 0)

        sched = compute_dyadic_f1_schedule(n=n, m=m, s=s, s_F=s_F)
        m_box = sched["M_box"]
        width = sched["width_W"]
        p_split = int(nextprime(width))

        # Orient u so that the first nonzero free coordinate equals +1
        j0 = next(j for j in range(n - m) if d_full[m + j] != 0)
        j_coord = m + j0
        sign = 1 if d_full[j_coord] == 1 else -1
        u_oriented = tuple(sign * x for x in u)
        d_oriented = tuple(sign * x for x in d_full)

        delta = list(d_oriented)
        assert delta[j_coord] == 1
        delta[j_coord] = (delta[j_coord] - 1) // p_split
        delta_tuple = tuple(delta)

        # Exact factors vs offset_average_pair_mass
        p_box_actual = prod(Fraction(m_box - abs(x), m_box) for x in delta_tuple)
        p_cube_actual = prod(Fraction(width - abs(x), width) for x in u_oriented)
        p_good_actual = offset_average_pair_mass(m_box, width, delta_tuple, u_oriented)
        p_bad_actual = Fraction(1, 1) - p_good_actual

        # Theorem 1 checks
        p_cube_formula = Fraction(width - 1, width) ** s
        p_cube_lower = Fraction(width - s, width)
        p_cube_upper = Fraction(width, width + s)
        t1_holds = bool(
            p_cube_actual == p_cube_formula and p_cube_lower <= p_cube_actual <= p_cube_upper
        )

        # Theorem 2 checks
        p_box_min = worst_case_multiplicative_box_survival(m_box, m, s_F)
        l_box = sched["L_box_ceiling"]
        p_box_add_lower = Fraction(m_box - l_box, m_box)
        t2_holds = bool(
            p_box_actual >= p_box_min >= p_box_add_lower
            and p_good_actual == p_box_actual * p_cube_actual
        )

        # Theorem 3 checks
        f1_budget = Fraction(1, sched["ell_position_wires"])
        p_bad_mult_upper = Fraction(1, 1) - (p_box_min * p_cube_formula)
        p_bad_add_upper = Fraction(l_box, m_box) + Fraction(s, width)
        t3_holds = bool(
            p_bad_actual <= p_bad_mult_upper <= p_bad_add_upper <= f1_budget
        )

        rows.append(
            {
                "n": n,
                "m": m,
                "q": int(problem.prime),
                "support_s": s,
                "free_support_s_F": s_F,
                "schedule": sched,
                "delta_l1_actual": int(sum(abs(x) for x in delta_tuple)),
                "P_box_actual_fraction": _fraction_str(p_box_actual),
                "P_cube_actual_fraction": _fraction_str(p_cube_actual),
                "intended_partner_survival_fraction": _fraction_str(p_good_actual),
                "intended_partner_failure_fraction": _fraction_str(p_bad_actual),
                "intended_partner_failure_float": float(p_bad_actual),
                "geometry_obligation": conditional_geometry_obligation(n, width, p_split, 4 * s),
                "generator_gap_assumption": 2,
                "source_bad_register_rate_certified": False,
                "source_bad_register_rate": None,
                "schedule_and_hitting_trial_selected_with_private_witness": True,
                "all_public_coordinate_trials_executed": False,
                "theorem_1_cube_survival_enclosure_holds": t1_holds,
                "theorem_2_box_survival_lower_bound_holds": t2_holds,
                "theorem_3_partner_failure_budget_bound_verified": t3_holds,
            }
        )
    return rows


def build_planted_qary_offset_pair_mass_frontier_audit_report() -> dict[str, Any]:
    """Build the complete JSON artifact for Subsystem 12."""
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    instance_rows = audit_planted_instance_offset_pair_mass_frontier()

    t1_ok = all(r["theorem_1_cube_survival_enclosure_holds"] for r in instance_rows)
    t2_ok = all(r["theorem_2_box_survival_lower_bound_holds"] for r in instance_rows)
    t3_ok = all(r["theorem_3_partner_failure_budget_bound_verified"] for r in instance_rows)
    collision = same_colour_collision_counterexample()

    return {
        "schema_version": "2.0.0",
        "subsystem": "planted_qary_offset_pair_mass_frontier_audit",
        "contract_id": contract["contract_id"],
        "doc_path": str(DOC_PATH.relative_to(ROOT)),
        "summary_of_theorems": {
            "T1_support_only_cube_survival_law": (
                "P_cube(W, u) = (1 - 1/W)^s with 1 - s/W <= P_cube(W, u) <= 1 / (1 + s/W)."
            ),
            "T2_worst_case_box_survival_bounds": (
                "P_box(M_box, delta) >= (1 - 1/M_box)^(s_F - 1) * (1 - B_tern(s_F)/M_box)^m "
                ">= 1 - L_box(m, s_F) / M_box."
            ),
            "T3_modulus_independent_dyadic_f1_schedule": (
                "Choosing minimal b >= 1 with 2^b >= max(2, 2*n*(b+1)*L_box(m, s_F)) and "
                "w = ceil(log_2(2*n*(b+1)*s)) bounds intended partner failure by 1/(n*(b+1)). "
                "It bounds DCP bad-register mass only conditional on independent two-point geometry."
            ),
        },
        "planted_instance_frontier_audit": instance_rows,
        "source_geometry_counterexample": collision,
        "verification": {
            "theorem_1_cube_survival_enclosure_verified": bool(t1_ok),
            "theorem_2_box_survival_bounds_verified": bool(t2_ok),
            "theorem_3_modulus_independent_partner_schedule_verified": bool(t3_ok),
            "unconditional_transfer_counterexample_verified": collision["same_colour_collision_verified"],
        },
        "guardrails": contract["guardrails"],
    }


def write_planted_qary_offset_pair_mass_frontier_audit_report(
    path: Path = ARTIFACT_PATH,
) -> dict[str, Any]:
    report = build_planted_qary_offset_pair_mass_frontier_audit_report()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Write JSON artifact to research/reductions/.")
    parser.add_argument("--no-write", action="store_true", help="Build and validate report without writing.")
    args = parser.parse_args(argv)

    if args.write and not args.no_write:
        report = write_planted_qary_offset_pair_mass_frontier_audit_report()
    else:
        report = build_planted_qary_offset_pair_mass_frontier_audit_report()

    print(
        json.dumps(
            {
                "subsystem": report["subsystem"],
                "verification": report["verification"],
                "instances_checked": len(report["planted_instance_frontier_audit"]),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
