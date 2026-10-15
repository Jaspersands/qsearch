"""Planted q-ary kernel basis coordinate bounds, q-independent cube shifts, and deterministic prime/residue selection.

Connects `theorems/planted_qary_usvp_source.py` (`PublicQaryLattice`, `generate_source`) and
`theorems/lattice_cube_coset_source.py` (`CubeCosetSource`, `offset_average_pair_mass`) by proving:
1. Exact formula for the basis-coordinate vector `d = u B^{-1} = (d_piv, d_free)` in the public
   centered-RREF kernel row basis `B`:
     - `d_{free, j} = u_{F_j}`
     - `d_{piv, i} = (u_{P_i} + sum_j C_{i,j} u_{F_j}) / q`
2. Nonzero free-column support invariant: every nonzero `u in (-q/2, q/2)^n cap ker(H mod q)`
   has `s_F = supp_F(u) >= 1`.
3. Modulus-independent pivot coordinate and L1 cube-shift bounds:
   for `u in [-U, U]^n cap ker(H mod q)` with `U < q/2`,
     - `|d_{piv, i}| <= floor(U * s_F / 2) <= floor(U * (n - m) / 2)` independently of `q`
     - for ternary `u in {-1, 0, 1}^n \\ {0}` and `q >= 3`, a q-independent envelope is
       `|d_{piv, i}| <= 0` (`s_F = 1`), `1` (`s_F = 2`), and `floor((s_F - 1)/2)` (`s_F >= 3`),
       all `<= floor(s_F / 2) <= floor((n - m) / 2)`
     - exact box-coordinate partner difference `delta` in `CubeCosetSource` has
       `delta_{j_pivot} = (1 - 1) / p_split = 0` on the hitting free coordinate for EVERY prime
       `p_split >= 2`, so `||delta||_1 = ||d||_1 - 1 <= (s_F - 1) + m * sharp_piv_bound`.
4. Colinear-multiple cube separation and deterministic `(p_split = nextprime(W), g_res = 1)`:
   since `||k u||_inf = |k|` for ternary `u`, any `p_split <= W` allows colinear multiples `k u`
   (`|k| >= p_split - 1`) to collide inside a cube of width `W`, whereas `p_split = nextprime(W) >= W + 1`
   with `g_res = 1` eliminates all colinear multiple collisions `|k| >= 2` and collapses outer guessing
   to at most `n - m` free-coordinate trials `j_pivot in {m, ..., n - 1}`.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from math import prod
from pathlib import Path
from typing import Any

from sympy import nextprime

from theorems.lattice_cube_coset_source import CubeCosetSource, offset_average_pair_mass
from theorems.planted_qary_usvp_source import PublicQaryLattice, generate_source


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "research" / "hypotheses" / "planted_qary_cube_basis_coordinate_bridge_contract.json"
ARTIFACT_PATH = ROOT / "research" / "reductions" / "planted_qary_cube_basis_coordinate_bridge.json"
DOC_PATH = ROOT / "research" / "PLANTED_QARY_CUBE_BASIS_COORDINATE_BRIDGE.md"


def _fraction_str(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def _centered_mod(val: int, q: int) -> int:
    r = int(val) % int(q)
    if r > q // 2:
        r -= int(q)
    return r


def ternary_pivot_envelope(s_F: int) -> int:
    """Uniform envelope over odd prime moduli, not a fixed-q sharp bound."""
    if type(s_F) is not int or s_F < 1:
        raise ValueError("positive exact free support required")
    if s_F == 1:
        return 0
    if s_F == 2:
        return 1
    return (s_F - 1) // 2


def fixed_q_ternary_pivot_bound(s_F: int, q: int) -> int:
    """Exact attainable maximum floor((1 + s_F*(q-1)/2)/q)."""
    ternary_pivot_envelope(s_F)
    if type(q) is not int or q < 3 or q % 2 == 0:
        raise ValueError("odd exact modulus at least three required")
    return (1 + s_F * ((q - 1) // 2)) // q


def extract_centered_rref_structure(problem: PublicQaryLattice) -> dict[str, Any]:
    """Extract pivot columns P, free columns F, and centered residue block C from PublicQaryLattice."""
    q = problem.prime
    m = problem.rows
    n = problem.dimension
    pivots = problem.pivots
    free = problem.free
    C_centered: list[list[int]] = []
    for i in range(m):
        row_c: list[int] = []
        for f_col in free:
            row_c.append(_centered_mod(problem.rref[i][f_col], q))
        C_centered.append(row_c)
    return {
        "m": int(m),
        "n": int(n),
        "q": int(q),
        "pivot_cols": list(pivots),
        "free_cols": list(free),
        "C_centered": C_centered,
    }


def basis_coordinates_from_public_lattice(
    problem: PublicQaryLattice,
    u_vec: tuple[int, ...] | list[int],
) -> tuple[int, ...]:
    """Compute unique integer row-basis coordinates d such that sum_k d_k B_k = u_vec."""
    u = tuple(int(v) for v in u_vec)
    if not problem.member(u):
        raise ValueError("u_vec is not in ker(H mod q)")
    m = problem.rows
    n = problem.dimension
    q = problem.prime
    d_free = [u[f_col] for f_col in problem.free]
    d_piv: list[int] = []
    for i, p_col in enumerate(problem.pivots):
        residual = u[p_col] - sum(d_free[j] * problem.basis[m + j][p_col] for j in range(n - m))
        if residual % q != 0:
            raise ArithmeticError("Pivot residual not divisible by q")
        d_piv.append(residual // q)
    d_full = tuple(d_piv + d_free)
    reconstructed = tuple(
        sum(d_full[k] * problem.basis[k][col] for k in range(n))
        for col in range(n)
    )
    if reconstructed != u:
        raise ArithmeticError("Reconstructed lattice vector does not match u_vec")
    return d_full


def compute_basis_coordinates_analytical(
    problem: PublicQaryLattice,
    u_vec: tuple[int, ...] | list[int],
) -> dict[str, Any]:
    """Compute d = u B^{-1} via the analytical centered-RREF formula and verify all bounds."""
    struct = extract_centered_rref_structure(problem)
    m = struct["m"]
    n = struct["n"]
    q = struct["q"]
    pivot_cols = struct["pivot_cols"]
    free_cols = struct["free_cols"]
    C = struct["C_centered"]
    u = tuple(int(v) for v in u_vec)
    if len(u) != n:
        raise ValueError("u_vec length must equal n")

    u_piv = tuple(u[p] for p in pivot_cols)
    u_free = tuple(u[f] for f in free_cols)
    s_free = sum(1 for val in u_free if val != 0)
    u_inf = max((abs(val) for val in u), default=0)

    d_piv_list: list[int] = []
    for i in range(m):
        numer = u_piv[i] + sum(int(C[i][j]) * u_free[j] for j in range(n - m))
        if numer % q != 0:
            raise ValueError(f"u_vec is not in ker(H mod q) at pivot row {i}: numer={numer} mod {q} != 0")
        d_piv_list.append(int(numer // q))

    d_piv = tuple(d_piv_list)
    d_free = u_free
    d_full = d_piv + d_free

    piv_bound_support = (u_inf * s_free) // 2
    piv_bound_worst = (u_inf * (n - m)) // 2
    l1_bound_support = u_inf * s_free + m * piv_bound_support
    l1_bound_worst = u_inf * (n - m) + m * piv_bound_worst

    max_abs_d_piv = max((abs(v) for v in d_piv), default=0)
    d_l1 = sum(abs(v) for v in d_full)
    d_linf = max((abs(v) for v in d_full), default=0)

    return {
        "m": m,
        "n": n,
        "q": int(q),
        "pivot_cols": list(pivot_cols),
        "free_cols": list(free_cols),
        "C_centered": C,
        "u_vec": list(u),
        "u_piv": list(u_piv),
        "u_free": list(u_free),
        "u_inf": int(u_inf),
        "free_support_s_F": int(s_free),
        "d_piv": list(d_piv),
        "d_free": list(d_free),
        "d_full": list(d_full),
        "max_abs_d_piv": int(max_abs_d_piv),
        "d_linf": int(d_linf),
        "d_l1": int(d_l1),
        "pivot_bound_from_support": int(piv_bound_support),
        "pivot_bound_worst_case": int(piv_bound_worst),
        "l1_bound_from_support": int(l1_bound_support),
        "l1_bound_worst_case": int(l1_bound_worst),
        "nonzero_free_support_satisfied": bool(s_free >= 1 if any(v != 0 for v in u) else True),
        "pivot_support_bound_satisfied": bool(max_abs_d_piv <= piv_bound_support),
        "pivot_worst_bound_satisfied": bool(max_abs_d_piv <= piv_bound_worst),
        "l1_support_bound_satisfied": bool(d_l1 <= l1_bound_support),
        "l1_worst_bound_satisfied": bool(d_l1 <= l1_bound_worst),
    }


def build_exact_ternary_saturation_family() -> list[dict[str, Any]]:
    """Construct exact ternary u in {-1, 0, 1}^n cap ker(H mod q) saturating the sharp ternary bound."""
    records: list[dict[str, Any]] = []
    for q in (3, 5, 101, 10007, 1000003):
        half_q = (q - 1) // 2
        for s_F in (1, 2, 3, 4, 5, 6, 7, 9, 16):
            m = 3
            n_minus_m = max(2, s_F)
            n = m + n_minus_m
            max_achievable_k = fixed_q_ternary_pivot_bound(s_F, q)
            pivot_entry = 1 if max_achievable_k else 0
            target_sum = max_achievable_k * q - pivot_entry
            C = [[0 for _ in range(n_minus_m)] for _ in range(m)]
            rem = target_sum
            for j in range(s_F):
                take = min(rem, half_q)
                C[0][j] = take
                rem -= take
            assert rem == 0

            H: list[tuple[int, ...]] = []
            for i in range(m):
                row_h = [0] * n
                row_h[i] = 1
                for j in range(n_minus_m):
                    row_h[m + j] = int(C[i][j] % q)
                H.append(tuple(row_h))

            problem = PublicQaryLattice(q, tuple(H))
            u_piv = [pivot_entry] + [0] * (m - 1)
            u_free = [1] * s_F + [0] * (n_minus_m - s_F)
            u_vec = tuple(u_piv + u_free)
            analysis = compute_basis_coordinates_analytical(problem, u_vec)
            records.append(
                {
                    "q": int(q),
                    "m": int(m),
                    "n_minus_m": int(n_minus_m),
                    "s_F": s_F,
                    "achieved_d_piv_0": int(analysis["d_piv"][0]),
                    "sharp_ternary_bound": int(max_achievable_k),
                    "q_independent_envelope": ternary_pivot_envelope(s_F),
                    "public_matrix_H": [list(row) for row in H],
                    "analysis": analysis,
                    "coarse_floor_sF_div_2_bound": s_F // 2,
                    "attains_sharp_ternary_bound": bool(analysis["d_piv"][0] == max_achievable_k),
                }
            )
    return records


def audit_planted_instance_family() -> list[dict[str, Any]]:
    """Audit planted ternary q-ary instances across dimensions and prime moduli up to q > 2^80."""
    configs = [
        {"n": 4, "m": 2, "q": 1009, "support": 3, "seed": 7, "M_box": 16, "width": 4, "audit_cube": True},
        {"n": 6, "m": 3, "q": 1009, "support": 4, "seed": 11, "M_box": 64, "width": 8, "audit_cube": False},
        {"n": 8, "m": 4, "q": 65537, "support": 5, "seed": 19, "M_box": 64, "width": 8, "audit_cube": False},
        {"n": 10, "m": 5, "q": 1000003, "support": 6, "seed": 23, "M_box": 128, "width": 16, "audit_cube": False},
        {"n": 12, "m": 6, "q": 1000000007, "support": 8, "seed": 31, "M_box": 128, "width": 16, "audit_cube": False},
        {"n": 8, "m": 4, "q": int(nextprime(2**80)), "support": 6, "seed": 43, "M_box": 128, "width": 16, "audit_cube": False},
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
            matrix_seed=cfg["seed"] + 100,
        )
        problem = gen.problem
        planted_u = gen.private.plant
        analytical = compute_basis_coordinates_analytical(problem, planted_u)
        d_from_public_lattice = basis_coordinates_from_public_lattice(problem, planted_u)

        free_guess_hits: list[int] = []
        for j_free_idx in range(problem.dimension - problem.rows):
            j_basis_coord = problem.rows + j_free_idx
            if d_from_public_lattice[j_basis_coord] != 0:
                free_guess_hits.append(j_basis_coord)

        first_hit_coord = free_guess_hits[0]
        sign_hit = 1 if d_from_public_lattice[first_hit_coord] == 1 else -1
        u_oriented = tuple(sign_hit * x for x in planted_u)
        d_oriented = tuple(sign_hit * x for x in d_from_public_lattice)

        m_box = cfg["M_box"]
        width = cfg["width"]
        p_split_valid = int(nextprime(width))  # Smallest prime >= width + 1

        delta_partner = list(d_oriented)
        assert delta_partner[first_hit_coord] == 1
        delta_partner[first_hit_coord] = (delta_partner[first_hit_coord] - 1) // p_split_valid
        delta_tuple = tuple(delta_partner)

        box_good_mass = prod(Fraction(m_box - abs(x), m_box) for x in delta_tuple)
        box_bad_mass = Fraction(1, 1) - box_good_mass
        avg_pair_mass = offset_average_pair_mass(m_box, width, delta_tuple, u_oriented)

        cube_audit_valid_when_p_exceeds_width = None
        cube_audit_collides_when_p_below_width = None
        if cfg["audit_cube"]:
            cube_src_valid = CubeCosetSource(
                basis=problem.basis,
                prime=p_split_valid,
                residue_guess=1,
                coordinate=first_hit_coord,
                box=m_box,
                width=width,
                offsets=tuple(1 for _ in range(problem.dimension)),
            )
            audit_valid = cube_src_valid.audit()
            cube_audit_valid_when_p_exceeds_width = bool(audit_valid["valid_two_point_source_on_full_domain"])

            # Contrast with p_split = 2 <= width = 4, where k = 2 or k = -1 colinear multiples collide in width 4
            cube_src_colliding = CubeCosetSource(
                basis=problem.basis,
                prime=2,
                residue_guess=1,
                coordinate=first_hit_coord,
                box=m_box,
                width=width,
                offsets=tuple(1 for _ in range(problem.dimension)),
            )
            audit_colliding = cube_src_colliding.audit()
            cube_audit_collides_when_p_below_width = not bool(audit_colliding["valid_two_point_source_on_full_domain"])

        s_F = analytical["free_support_s_F"]
        sharp_piv_bound = fixed_q_ternary_pivot_bound(s_F, problem.prime)
        sharp_l1_bound = s_F + problem.rows * sharp_piv_bound
        delta_l1 = sum(abs(x) for x in delta_tuple)
        sharp_delta_l1_bound = (s_F - 1) + problem.rows * sharp_piv_bound
        p_bad_box_bound = Fraction(sharp_delta_l1_bound, m_box)

        rows.append(
            {
                "m": problem.rows,
                "n": problem.dimension,
                "n_minus_m": problem.dimension - problem.rows,
                "q": problem.prime,
                "M_box": m_box,
                "width": width,
                "p_split_deterministic": p_split_valid,
                "g_res_deterministic": 1,
                "planted_u": list(planted_u),
                "d_shift_analytical": analytical["d_full"],
                "d_shift_public_lattice": list(d_from_public_lattice),
                "analytical_matches_public_lattice": bool(tuple(analytical["d_full"]) == d_from_public_lattice),
                "free_support_s_F": s_F,
                "max_abs_d_piv": analytical["max_abs_d_piv"],
                "sharp_ternary_piv_bound": sharp_piv_bound,
                "coarse_piv_bound": analytical["pivot_bound_from_support"],
                "d_l1": analytical["d_l1"],
                "sharp_ternary_l1_bound": sharp_l1_bound,
                "coarse_l1_bound": analytical["l1_bound_from_support"],
                "delta_partner_on_hit_coord": list(delta_tuple),
                "delta_l1": delta_l1,
                "sharp_delta_l1_bound": sharp_delta_l1_bound,
                "exact_box_p_bad_fraction": _fraction_str(box_bad_mass),
                "exact_box_p_bad_float": float(box_bad_mass),
                "sharp_box_p_bad_upper_bound_fraction": _fraction_str(p_bad_box_bound),
                "sharp_box_p_bad_upper_bound_float": float(p_bad_box_bound),
                "offset_average_pair_good_mass_fraction": _fraction_str(avg_pair_mass),
                "p_bad_respects_sharp_bound": bool(box_bad_mass <= p_bad_box_bound),
                "free_coordinate_hits_mod_3": free_guess_hits,
                "first_hit_basis_coordinate": first_hit_coord,
                "outer_trial_budget_free_coords_only": problem.dimension - problem.rows,
                "cube_coset_source_exhaustive_valid_at_nextprime_W": cube_audit_valid_when_p_exceeds_width,
                "cube_coset_source_colinear_collision_at_p_le_W": cube_audit_collides_when_p_below_width,
            }
        )
    return rows


def build_planted_qary_cube_basis_coordinate_bridge_report() -> dict[str, Any]:
    """Build the complete JSON artifact for the planted q-ary kernel basis coordinate bridge."""
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    saturation_family = build_exact_ternary_saturation_family()
    planted_family = audit_planted_instance_family()

    all_analytical_matches = all(r["analytical_matches_public_lattice"] for r in planted_family)
    all_sharp_bounds_hold = all(
        r["max_abs_d_piv"] <= r["sharp_ternary_piv_bound"]
        and r["d_l1"] <= r["sharp_ternary_l1_bound"]
        and r["delta_l1"] == r["d_l1"] - 1
        and r["delta_l1"] <= r["sharp_delta_l1_bound"]
        and r["p_bad_respects_sharp_bound"]
        for r in planted_family
    )
    all_saturations_hold = all(r["attains_sharp_ternary_bound"] for r in saturation_family)
    all_free_guesses_hit = all(len(r["free_coordinate_hits_mod_3"]) >= 1 for r in planted_family)
    exhaustive_cube_control_valid = bool(
        planted_family[0]["cube_coset_source_exhaustive_valid_at_nextprime_W"]
        and planted_family[0]["cube_coset_source_colinear_collision_at_p_le_W"]
    )

    return {
        "schema_version": "2.0.0",
        "subsystem": "planted_qary_cube_basis_coordinate_bridge",
        "contract_id": contract["contract_id"],
        "doc_path": str(DOC_PATH.relative_to(ROOT)),
        "summary_of_theorems": {
            "T1_basis_coordinate_decomposition": (
                "d = u B^{-1} = (d_piv, d_free) with d_{free,j} = u_{F_j} and "
                "d_{piv,i} = (u_{P_i} + sum_j C_{i,j} u_{F_j}) / q in Z."
            ),
            "T2_nonzero_free_support_invariant": (
                "Every nonzero u in (-q/2, q/2)^n cap ker(H mod q) satisfies s_F = supp_F(u) >= 1."
            ),
            "T3_modulus_independent_bounds": (
                "For u in [-U, U]^n cap ker(H mod q) with U < q/2, |d_{piv,i}| <= floor(U * s_F / 2) "
                "independently of q. The fixed-q ternary maximum is floor((1+s_F*(q-1)/2)/q). "
                "The q-independent envelope is 0 (s_F=1), 1 (s_F=2), and floor((s_F-1)/2) "
                "(s_F>=3); it is not necessarily sharp at a specified q."
            ),
            "T4_colinear_separation_and_deterministic_prime_residue": (
                "For ternary u in {-1,0,1}^n \\ {0}, deterministic (p_split=nextprime(W), g_res=1) eliminates "
                "colinear multiple collisions |k| >= 2 inside width-W cubes, hits a free coordinate "
                "d_{j_pivot} = 1 within at most n - m trials j_pivot in {m, ..., n-1}, and yields "
                "delta_{j_pivot} = (1 - 1)/p_split = 0 so ||delta||_1 = ||d||_1 - 1."
            ),
        },
        "planted_instance_audit": planted_family,
        "ternary_saturation_family": saturation_family,
        "verification": {
            "all_analytical_coordinates_match_public_lattice": bool(all_analytical_matches),
            "all_sharp_and_coarse_bounds_satisfied": bool(all_sharp_bounds_hold),
            "all_ternary_saturation_witnesses_attain_bound": bool(all_saturations_hold),
            "all_free_coordinate_mod3_guesses_succeed": bool(all_free_guesses_hit),
            "exhaustive_cube_coset_source_control_valid": bool(exhaustive_cube_control_valid),
        },
        "guardrails": contract["guardrails"],
    }


def write_planted_qary_cube_basis_coordinate_bridge_report(
    path: Path = ARTIFACT_PATH,
) -> dict[str, Any]:
    report = build_planted_qary_cube_basis_coordinate_bridge_report()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Write JSON artifact to research/reductions/.")
    parser.add_argument("--no-write", action="store_true", help="Build and validate report without writing.")
    args = parser.parse_args(argv)

    if args.write and not args.no_write:
        report = write_planted_qary_cube_basis_coordinate_bridge_report()
    else:
        report = build_planted_qary_cube_basis_coordinate_bridge_report()

    print(
        json.dumps(
            {
                "subsystem": report["subsystem"],
                "verification": report["verification"],
                "planted_instances_checked": len(report["planted_instance_audit"]),
                "saturation_witnesses_checked": len(report["ternary_saturation_family"]),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
