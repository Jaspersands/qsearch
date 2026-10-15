"""Finite public classical attacks with exact reducedness and claim corrections.

RREF search uses polynomial working storage, not constant space. Determinant
growth alone does not imply an increasing successive-minimum gap or LLL success.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
from typing import Any

from sympy import nextprime

from theorems.planted_qary_cube_basis_coordinate_bridge import (
    _centered_mod,
    extract_centered_rref_structure,
)
from theorems.planted_qary_usvp_source import (
    PublicQaryLattice,
    canonical_sign,
    generate_source,
    norm_squared,
    public_LLL_attack,
    sparse_column_attack,
    ternary_MITM_attack,
    exact_json,
)


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "research" / "hypotheses" / "planted_qary_classical_attack_threshold_bridge_contract.json"
ARTIFACT_PATH = ROOT / "research" / "reductions" / "planted_qary_classical_attack_threshold_bridge.json"
DOC_PATH = ROOT / "research" / "PLANTED_QARY_CLASSICAL_ATTACK_THRESHOLD_BRIDGE.md"


def lll_alpha(delta: Fraction, eta: Fraction = Fraction(1, 2)) -> Fraction:
    if type(delta) not in (int, Fraction) or type(eta) not in (int, Fraction):
        raise ValueError("exact rational LLL parameters required")
    delta, eta = Fraction(delta), Fraction(eta)
    if not Fraction(1, 2) <= eta < 1 or not eta * eta < delta <= 1:
        raise ValueError("require 1/2<=eta<1 and eta^2<delta<=1")
    return 1 / (delta - eta * eta)


def rational_record(value):
    value = Fraction(value)
    return {"numerator": str(value.numerator), "denominator": str(value.denominator)}


def exact_reducedness(rows, delta=Fraction(3, 4), eta=Fraction(51, 100)):
    """Verify actual returned rows, rather than infer reduction from library name."""
    lll_alpha(delta, eta)
    rows = tuple(tuple(row) for row in rows)
    if not rows or any(len(row) != len(rows) or any(type(x) is not int for x in row) for row in rows):
        raise ValueError("square exact integer row basis required")
    orthogonal, norms, mu = [], [], []
    for row in rows:
        v = [Fraction(x) for x in row]
        coefficients = []
        for b, norm in zip(orthogonal, norms):
            coefficient = sum(Fraction(x) * y for x, y in zip(row, b)) / norm
            coefficients.append(coefficient)
            v = [x - coefficient * y for x, y in zip(v, b)]
        norm = sum(x*x for x in v)
        if not norm:
            raise ValueError("independent full-rank row basis required")
        orthogonal.append(v)
        norms.append(norm)
        mu.append(coefficients)
    size = all(abs(x) <= eta for row in mu for x in row)
    lovasz = all(norms[i] + mu[i][i-1]**2 * norms[i-1] >= delta * norms[i-1]
                 for i in range(1, len(rows)))
    return {"delta": rational_record(delta), "eta": rational_record(eta),
            "alpha": rational_record(lll_alpha(delta, eta)),
            "gram_schmidt_squared_norms": [rational_record(x) for x in norms],
            "size_reduction_verified": size, "lovasz_verified": lovasz,
            "actual_lambda2_certified": False}


def determinant_gap_counterfamily():
    H = ((1, -1, 0, 0, 0), (0, 0, 1, -1, 0), (1, 0, -1, 0, -2))
    u, v = (1, 1, 1, 1, 0), (1, 1, -1, -1, 1)
    controls = []
    for q in (7, 11, 101, 1009):
        problem = PublicQaryLattice(q, tuple(tuple(x % q for x in row) for row in H))
        attack = public_LLL_attack(problem)
        controls.append({"public_problem": problem.public_record(),
                         "lll_returned_vector": attack["vector"],
                         "lambda1_squared": 4, "lambda2_squared": 5,
                         "determinant": q**3,
                         "determinant_normalized_plant_gap_fifth_power": rational_record(Fraction(q**3, 32)),
                         "successive_minimum_gap_squared": rational_record(Fraction(5, 4))})
    return {"integer_constraint_rows": H, "primitive_unique_shortest_plant": u,
            "independent_next_vector": v, "ordinary_integer_kernel_basis": (u, v),
            "ordinary_kernel_norm_polynomial": "4*a^2+5*b^2 for integer a,b",
            "maximum_constraint_row_squared_norm": 6,
            "proof_radius_squared": 5,
            "prime_threshold_inclusive": 7,
            "all_nonzero_modular_wraps_excluded_within_proof_radius": True,
            "controls": controls,
            "determinant_growth_proves_successive_gap_growth": False,
            "finite_LLL_recovery_proves_monotone_success_probability": False}


def projective_free_coordinate_rref_search(problem: PublicQaryLattice, max_states=100000) -> dict[str, Any]:
    """No exponential table; O(m*(n-m)+n) additional integer slots."""
    struct = extract_centered_rref_structure(problem)
    m = struct["m"]
    n = struct["n"]
    q = struct["q"]
    pivots = struct["pivot_cols"]
    free = struct["free_cols"]
    C = struct["C_centered"]
    k_free = n - m
    expected_states = (3**k_free - 1) // 2
    if type(max_states) is not int or max_states < 1:
        raise ValueError("positive exact state cap required")
    if expected_states > max_states:
        raise ValueError("UNKNOWN: complete projective RREF enumeration cap; no negative result")

    states_checked = 0
    best: tuple[int, tuple[int, ...]] | None = None

    for first_nz in range(k_free):
        rem_len = k_free - 1 - first_nz
        for tail in product((-1, 0, 1), repeat=rem_len):
            u_free = (0,) * first_nz + (1,) + tail
            states_checked += 1
            valid_pivots = True
            u_piv = [0] * m
            for i in range(m):
                s_i = sum(C[i][j] * u_free[j] for j in range(first_nz, k_free))
                val_p = _centered_mod(-s_i, q)
                if val_p not in (-1, 0, 1):
                    valid_pivots = False
                    break
                u_piv[i] = val_p
            if not valid_pivots:
                continue

            u_full = [0] * n
            for i, p_col in enumerate(pivots):
                u_full[p_col] = u_piv[i]
            for j, f_col in enumerate(free):
                u_full[f_col] = u_free[j]
            cand = canonical_sign(u_full)
            cand_norm_sq = norm_squared(cand)
            item = (cand_norm_sq, cand)
            if best is None or item < best:
                best = item

    if states_checked != expected_states:
        raise ArithmeticError(f"Expected {expected_states} projective states, checked {states_checked}")

    split = n // 2
    ambient_mitm_states = 3**split + 3 ** (n - split)
    return {
        "n": n,
        "m": m,
        "n_minus_m": k_free,
        "q": q,
        "projective_free_states_checked": states_checked,
        "ambient_mitm_states": ambient_mitm_states,
        "state_reduction_ratio_vs_mitm": float(ambient_mitm_states) / float(max(1, states_checked)),
        "auxiliary_table_entries_stored": 0,
        "constant_working_space": False,
        "working_storage_order": "O(m*(n-m)+n) integer slots; bit cost depends on log q",
        "recovered_vector": list(best[1]) if best is not None else None,
        "recovered_squared_norm": int(best[0]) if best is not None else None,
    }


def audit_free_support_and_classical_attacks() -> list[dict[str, Any]]:
    """Finite source controls, not verification of lambda2 or general LLL success."""
    configs = [
        {"n": 4, "m": 2, "q": 257, "support": 3, "seed": 11},
        {"n": 6, "m": 3, "q": 1009, "support": 4, "seed": 17},
        {"n": 8, "m": 4, "q": 65537, "support": 6, "seed": 23},
        {"n": 10, "m": 6, "q": 1000003, "support": 8, "seed": 29},
        {"n": 12, "m": 7, "q": 1000000007, "support": 9, "seed": 37},
        {"n": 8, "m": 4, "q": int(nextprime(2**80)), "support": 6, "seed": 43},
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
            matrix_seed=cfg["seed"] + 400,
        )
        problem = gen.problem
        plant_canon = canonical_sign(gen.private.plant)
        n = problem.dimension
        m = problem.rows
        q = problem.prime
        free = problem.free
        pivots = problem.pivots

        s = sum(1 for x in plant_canon if x != 0)
        s_F = sum(1 for f_col in free if plant_canon[f_col] != 0)
        s_P = sum(1 for p_col in pivots if plant_canon[p_col] != 0)
        min_s_F = max(1, s - m)
        max_s_F = min(s, n - m)

        sparse_res = sparse_column_attack(problem)
        lll_res = public_LLL_attack(problem)
        mitm_res = ternary_MITM_attack(problem)
        rref_res = projective_free_coordinate_rref_search(problem)

        lll_recovered = tuple(lll_res["vector"]) == plant_canon
        rref_recovered = tuple(rref_res["recovered_vector"]) == plant_canon
        mitm_recovered = (
            tuple(mitm_res["vector"]) == plant_canon if mitm_res["vector"] is not None else False
        )

        reducedness = exact_reducedness(lll_res["reduced_row_basis"])
        ceiling = s * lll_alpha(Fraction(3, 4), Fraction(51, 100))**(n-1)
        det_root_gap = (float(q) ** (float(m) / float(n))) / (float(s) ** 0.5)

        rows.append(
            {
                "n": n,
                "public_problem": problem.public_record(),
                "PRIVATE_AUDIT_ONLY_plant": plant_canon,
                "public_LLL_vector": lll_res["vector"],
                "public_LLL_reduced_row_basis": lll_res["reduced_row_basis"],
                "public_LLL_unimodular_transform": lll_res["unimodular_row_transform"],
                "projective_RREF_vector": rref_res["recovered_vector"],
                "RREF_constant_space": False,
                "RREF_exponential_table_stored": False,
                "RREF_working_storage_order": rref_res["working_storage_order"],
                "m": m,
                "n_minus_m": n - m,
                "q": int(q),
                "total_support_s": s,
                "pivot_support_s_P": s_P,
                "free_support_s_F": s_F,
                "theoretical_min_s_F": min_s_F,
                "theoretical_max_s_F": max_s_F,
                "free_support_within_sharp_bounds": bool(
                    min_s_F <= s_F <= max_s_F and s_P + s_F == s
                ),
                "sparse_column_attack_status": sparse_res["status"],
                "sparse_column_immune_at_s_ge_3": bool(
                    sparse_res["status"] == "NO_UNIT_OR_COLUMN_PAIR_RELATION"
                ),
                "lll_recovered_squared_norm": int(lll_res["squared_norm"]),
                "LLL_reducedness_certificate": reducedness,
                "certified_LLL_squared_norm_ceiling": rational_record(ceiling),
                "LLL_squared_norm_bound_verified": lll_res["squared_norm"] <= ceiling,
                "lambda2_isolation_premise_verified": False,
                "determinant_normalized_proxy_NOT_lambda2_gap": det_root_gap,
                "public_lll_recovered_planted_vector": bool(lll_recovered),
                "ambient_mitm_recovered_planted_vector": bool(mitm_recovered),
                "projective_rref_recovered_planted_vector": bool(rref_recovered),
                "projective_rref_states_checked": rref_res["projective_free_states_checked"],
                "ambient_mitm_states": rref_res["ambient_mitm_states"],
                "projective_rref_strictly_fewer_states_than_mitm": bool(
                    rref_res["projective_free_states_checked"] < rref_res["ambient_mitm_states"]
                ),
            }
        )
    return rows


def build_planted_qary_classical_attack_threshold_bridge_report() -> dict[str, Any]:
    """Build the complete JSON artifact for Subsystem 15."""
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    audit_rows = audit_free_support_and_classical_attacks()

    t1_ok = all(
        r["free_support_within_sharp_bounds"] and r["sparse_column_immune_at_s_ge_3"]
        for r in audit_rows
    )
    t2_ok = all(
        r["public_lll_recovered_planted_vector"]
        and r["LLL_squared_norm_bound_verified"]
        and r["LLL_reducedness_certificate"]["size_reduction_verified"]
        and r["LLL_reducedness_certificate"]["lovasz_verified"]
        for r in audit_rows
    )
    t3_ok = all(
        r["projective_rref_recovered_planted_vector"]
        and r["projective_rref_strictly_fewer_states_than_mitm"]
        and r["projective_rref_states_checked"] == (3 ** r["n_minus_m"] - 1) // 2
        for r in audit_rows
    )

    return exact_json({
        "schema_version": "2.0.0",
        "subsystem": "planted_qary_classical_attack_threshold_bridge",
        "contract_id": contract["contract_id"],
        "doc_path": str(DOC_PATH.relative_to(ROOT)),
        "summary_of_theorems": {
            "T1_sharp_free_support_bound_and_column_pair_immunity": (
                "max(1, s - m) <= s_F <= min(s, n - m), and unique plants with s >= 3 are immune "
                "to unit/column-pair collisions in sparse_column_attack."
            ),
            "T2_conditional_LLL_bound_not_determinant_monotonicity": (
                "For a VERIFIED (delta,eta)-reduced basis, alpha=1/(delta-eta^2). "
                "The lambda2 isolation criterion is conditional; no growing lambda2 or LLL success follows from determinant alone."
            ),
            "T3_projective_free_coordinate_rref_search": (
                "Projective enumeration over u_F in {-1, 0, 1}^(n-m) \\ {0} checks exactly "
                "(3^(n-m) - 1)/2 states without an exponential table, using O(m*(n-m)+n) additional integer slots. "
                "State counts do not certify wall-time dominance over MITM."
            ),
        },
        "classical_attack_threshold_audit": audit_rows,
        "verification": {
            "finite_free_support_and_sparse_attack_controls": bool(t1_ok),
            "finite_LLL_membership_reducedness_and_bounds": bool(t2_ok),
            "finite_projective_rref_search_controls": bool(t3_ok),
        },
        "LLL_parameter_arithmetic": {
            "delta_3_4_eta_1_2_alpha": rational_record(lll_alpha(Fraction(3, 4))),
            "finite_certificates_use_delta": rational_record(Fraction(3, 4)),
            "finite_certificates_use_eta": rational_record(Fraction(51, 100)),
            "finite_certificate_alpha": rational_record(lll_alpha(Fraction(3, 4), Fraction(51, 100))),
            "library_defaults_substituted_for_verified_reducedness": False,
        },
        "determinant_growth_counterfamily": determinant_gap_counterfamily(),
        "unresolved_or_withdrawn_claims": {
            "general_large_q_LLL_success_monotonicity_proved": False,
            "lambda2_isolation_of_generated_controls_certified": False,
            "constant_working_memory": False,
            "finite_recovery_is_a_general_complexity_theorem": False,
        },
        "guardrails": contract["guardrails"],
    })


def write_planted_qary_classical_attack_threshold_bridge_report(
    path: Path = ARTIFACT_PATH,
) -> dict[str, Any]:
    report = build_planted_qary_classical_attack_threshold_bridge_report()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Write JSON artifact to research/reductions/.")
    parser.add_argument("--no-write", action="store_true", help="Build and validate report without writing.")
    args = parser.parse_args(argv)

    if args.write and not args.no_write:
        report = write_planted_qary_classical_attack_threshold_bridge_report()
    else:
        report = build_planted_qary_classical_attack_threshold_bridge_report()

    print(
        json.dumps(
            {
                "subsystem": report["subsystem"],
                "verification": report["verification"],
                "instances_checked": len(report["classical_attack_threshold_audit"]),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
