"""Higher-call signed path valuation audit: Z_3-coset invariant, sign invariance, and 1/3 non-unit law.

Extends `theorems/native_response_path_valuation.py` from positive-only call schedules
`epsilon = (+1, ..., +1)` to arbitrary signed response schedules `epsilon in {-1, +1}^k`:
1. Theorem 1 (Universal Z_3-Coset Invariant and Balanced Sign Annihilation):
   For `DIGITS = ((1, 0), (-1, 1), (0, -1))`, `Phi(x, y) = x - y` satisfies `Phi(beta_t) == 1 (mod 3)`
   for all `t in {0, 1, 2}`. Thus every single-path coefficient sum `V_epsilon(t) = (X, Y)` satisfies
   `X - Y == S(epsilon) (mod 3)` where `S(epsilon) = sum_l epsilon_l`. Single-path mod-3 vanishing
   occurs iff `S(epsilon) == 0 (mod 3)` (which holds for all balanced even schedules `k = 2m, S = 0`,
   with exact integer zero-sum count `sum_{a+b+c=m} (m!/(a!b!c!))^2`, whereas unsigned `(+1)^k`
   schedules require `3 | k` with integer zero-sum count `k! / ((k/3)!)^3`).
2. Theorem 2 (Exact Sign-Schedule Invariance of Paired Path Differences):
   For every `k >= 1` and every `epsilon in {-1, +1}^k`, the paired path-difference distribution
   `Delta_epsilon(t, u) = V_epsilon(t) - V_epsilon(u)` is identical to `Delta_{(+1)^k}(t, u)` (`local_difference_counts(k)`).
3. Theorem 3 (Sublattice Congruence `Delta_X == Delta_Y (mod 3)` and Universal `1/3` Non-Unit Law):
   Every paired difference satisfies `3 | (Delta_X - Delta_Y)` over `Z` and
   `(Delta_X, Delta_Y) == (sum_l epsilon_l (u_l - t_l)) * (1, 1) (mod 3)`, so exactly `9^k / 3 = 3^(2k-1)`
   path pairs have `v_3(Delta) >= 1` and `2 * 3^(2k-1)` have `v_3(Delta) = 0` for every `k >= 1`.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from itertools import product
import json
import math
from pathlib import Path
from typing import Any

from theorems.native_response_path_valuation import DIGITS, iid_path_collision_law, local_difference_counts


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "research" / "hypotheses" / "native_higher_call_signed_path_valuation_audit_contract.json"
ARTIFACT_PATH = ROOT / "research" / "reductions" / "native_higher_call_signed_path_valuation_audit.json"
DOC_PATH = ROOT / "research" / "NATIVE_HIGHER_CALL_SIGNED_PATH_VALUATION_AUDIT.md"


def _fraction_str(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def trinomial(n: int, a: int, b: int, c: int) -> int:
    if a < 0 or b < 0 or c < 0 or a + b + c != n:
        return 0
    return math.factorial(n) // (math.factorial(a) * math.factorial(b) * math.factorial(c))


def signed_single_path_sum_counts(signs: tuple[int, ...] | list[int]) -> Counter[tuple[int, int]]:
    """Compute exact distribution of single-path sums V_epsilon(t) over {0, 1, 2}^k."""
    eps = tuple(int(s) for s in signs)
    if not eps or any(s not in (-1, 1) for s in eps):
        raise ValueError("Nonempty sign tuple in {-1, +1}^k required")
    counts: Counter[tuple[int, int]] = Counter({(0, 0): 1})
    for s in eps:
        nxt: Counter[tuple[int, int]] = Counter()
        for (x, y), mult in counts.items():
            for dx, dy in DIGITS:
                nxt[(x + s * dx, y + s * dy)] += mult
        counts = nxt
    return counts


def signed_paired_difference_counts(signs: tuple[int, ...] | list[int]) -> Counter[tuple[int, int]]:
    """Compute exact distribution of paired path differences Delta_epsilon(t, u) over {0,1,2}^k x {0,1,2}^k."""
    sums = signed_single_path_sum_counts(signs)
    diffs: Counter[tuple[int, int]] = Counter()
    for (x, y), a in sums.items():
        for (u, v), b in sums.items():
            diffs[(x - u, y - v)] += a * b
    return diffs


def closed_form_zero_sum_single_path_count(signs: tuple[int, ...] | list[int]) -> int:
    """Closed-form count of paths t in {0, 1, 2}^k with V_epsilon(t) == (0, 0) in Z^2."""
    eps = tuple(int(s) for s in signs)
    k_pos = sum(1 for s in eps if s == 1)
    k_neg = sum(1 for s in eps if s == -1)
    net_s = k_pos - k_neg
    if net_s % 3 != 0:
        return 0
    # Let (a_+, b_+, c_+) be counts among +1 calls and (a_-, b_-, c_-) among -1 calls.
    # Net digits: A = a_+ - a_-, B = b_+ - b_-, C = c_+ - c_-.
    # V_epsilon = (A - B, B - C) = (0, 0) iff A = B = C.
    # Since A + B + C = k_+ - k_- = net_s, we need A = B = C = net_s // 3 = r.
    r = net_s // 3
    total = 0
    for a_neg in range(k_neg + 1):
        for b_neg in range(k_neg - a_neg + 1):
            c_neg = k_neg - a_neg - b_neg
            a_pos = a_neg + r
            b_pos = b_neg + r
            c_pos = c_neg + r
            if a_pos >= 0 and b_pos >= 0 and c_pos >= 0 and (a_pos + b_pos + c_pos == k_pos):
                total += trinomial(k_pos, a_pos, b_pos, c_pos) * trinomial(k_neg, a_neg, b_neg, c_neg)
    return total


def audit_single_path_coset_and_zero_sum_theorem() -> list[dict[str, Any]]:
    """Verify Theorem 1 across call counts k = 1..6 and representative sign schedules."""
    schedules: list[tuple[int, ...]] = [
        (1,),
        (-1,),
        (1, 1),
        (1, -1),
        (1, 1, 1),
        (1, 1, -1),
        (1, 1, 1, 1),
        (1, -1, 1, -1),
        (1, 1, 1, -1),
        (1, 1, 1, 1, -1),
        (1, 1, 1, 1, 1, 1),
        (1, -1, 1, -1, 1, -1),
        (1, 1, 1, 1, 1, -1),
    ]
    rows: list[dict[str, Any]] = []
    for eps in schedules:
        k = len(eps)
        total_paths = 3**k
        net_s = sum(eps)
        expected_coset_mod3 = net_s % 3
        sums = signed_single_path_sum_counts(eps)

        all_in_coset = all(((x - y) - net_s) % 3 == 0 for (x, y) in sums)
        mod3_zero_count = sum(mult for (x, y), mult in sums.items() if x % 3 == 0 and y % 3 == 0)
        expected_mod3_zero_count = (3 ** (k - 1)) if (expected_coset_mod3 == 0) else 0

        int_zero_count = sums.get((0, 0), 0)
        formula_int_zero_count = closed_form_zero_sum_single_path_count(eps)

        rows.append(
            {
                "calls_k": k,
                "signs": list(eps),
                "net_sign_S": net_s,
                "net_sign_mod_3": expected_coset_mod3,
                "total_paths": total_paths,
                "distinct_integer_endpoints": len(sums),
                "all_endpoints_satisfy_X_minus_Y_congruent_S_mod_3": bool(all_in_coset),
                "mod3_zero_path_count": int(mod3_zero_count),
                "expected_mod3_zero_path_count": int(expected_mod3_zero_count),
                "integer_zero_sum_path_count": int(int_zero_count),
                "closed_form_integer_zero_sum_count": int(formula_int_zero_count),
                "matches_theorem_1": bool(
                    all_in_coset
                    and mod3_zero_count == expected_mod3_zero_count
                    and int_zero_count == formula_int_zero_count
                ),
            }
        )
    return rows


def audit_paired_difference_sign_invariance() -> list[dict[str, Any]]:
    """Verify Theorem 2 across all 2^k sign schedules for k = 1, 2, 3, 4, 5."""
    rows: list[dict[str, Any]] = []
    for k in (1, 2, 3, 4, 5):
        ref_diffs = local_difference_counts(k)
        schedules_checked = 0
        all_match_unsigned = True
        for eps in product((-1, 1), repeat=k):
            diffs = signed_paired_difference_counts(eps)
            if diffs != ref_diffs:
                all_match_unsigned = False
                break
            schedules_checked += 1
        rows.append(
            {
                "calls_k": k,
                "sign_schedules_checked": schedules_checked,
                "total_ordered_path_pairs": 9**k,
                "distinct_difference_vectors": len(ref_diffs),
                "zero_difference_pair_count": int(ref_diffs[(0, 0)]),
                "all_sign_schedules_identical_to_unsigned": bool(
                    all_match_unsigned and schedules_checked == (1 << k)
                ),
            }
        )
    return rows


def audit_universal_one_third_valuation_law() -> list[dict[str, Any]]:
    """Verify Theorem 3 across call counts k = 1..8 and cross-check against iid_path_collision_law."""
    rows: list[dict[str, Any]] = []
    for k in range(1, 9):
        diffs = local_difference_counts(k)
        total_pairs = 9**k
        all_divisible_by_3 = all((dx - dy) % 3 == 0 for (dx, dy) in diffs)

        unit_count_v0 = sum(
            mult for (dx, dy), mult in diffs.items() if (dx % 3 != 0 or dy % 3 != 0)
        )
        nonunit_count_v_ge_1 = sum(
            mult for (dx, dy), mult in diffs.items() if (dx % 3 == 0 and dy % 3 == 0)
        )
        expected_v0 = 2 * (3 ** (2 * k - 1))
        expected_v_ge_1 = 3 ** (2 * k - 1)

        # Cross-check with iid_path_collision_law(n=2, d=2, sites=2, calls=k)
        law = iid_path_collision_law(n=2, d=2, sites=2, calls=k)
        strata_by_val = {int(s["valuation"]): s for s in law["ideal_strata"]}
        law_v0_local = int(strata_by_val[0]["local_count"])
        law_v_ge_1_local = sum(int(strata_by_val[h]["local_count"]) for h in (1, 2))
        law_v_ge_1_all_sites = sum(int(strata_by_val[h]["all_sites_path_pair_count"]) for h in (1, 2))
        expected_all_sites_v_ge_1 = expected_v_ge_1**2

        rows.append(
            {
                "calls_k": k,
                "total_local_ordered_pairs": total_pairs,
                "all_pairs_satisfy_3_divides_DeltaX_minus_DeltaY": bool(all_divisible_by_3),
                "local_unit_count_v3_eq_0": int(unit_count_v0),
                "expected_local_unit_count_2_times_3_pow_2k_minus_1": int(expected_v0),
                "local_nonunit_count_v3_ge_1": int(nonunit_count_v_ge_1),
                "expected_local_nonunit_count_3_pow_2k_minus_1": int(expected_v_ge_1),
                "local_nonunit_fraction": _fraction_str(Fraction(nonunit_count_v_ge_1, total_pairs)),
                "local_v3_eq_1_count": int(strata_by_val[1]["local_count"]),
                "local_v3_ge_2_count": int(strata_by_val[2]["local_count"]),
                "local_integer_zero_pair_count": int(diffs[(0, 0)]),
                "two_site_all_sites_v3_ge_1_count": int(law_v_ge_1_all_sites),
                "expected_two_site_v3_ge_1_count": int(expected_all_sites_v_ge_1),
                "two_site_iid_expected_collision_density": law["exact_IID_expected_collision_density"],
                "matches_theorem_3": bool(
                    all_divisible_by_3
                    and unit_count_v0 == expected_v0
                    and nonunit_count_v_ge_1 == expected_v_ge_1
                    and law_v0_local == expected_v0
                    and law_v_ge_1_local == expected_v_ge_1
                    and law_v_ge_1_all_sites == expected_all_sites_v_ge_1
                ),
            }
        )
    return rows


def build_native_higher_call_signed_path_valuation_audit_report() -> dict[str, Any]:
    """Build the complete JSON artifact for Subsystem 9."""
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    single_path_rows = audit_single_path_coset_and_zero_sum_theorem()
    sign_invariance_rows = audit_paired_difference_sign_invariance()
    valuation_rows = audit_universal_one_third_valuation_law()

    t1_ok = all(r["matches_theorem_1"] for r in single_path_rows)
    t2_ok = all(r["all_sign_schedules_identical_to_unsigned"] for r in sign_invariance_rows)
    t3_ok = all(r["matches_theorem_3"] for r in valuation_rows)

    return {
        "schema_version": "1.0.0",
        "subsystem": "native_higher_call_signed_path_valuation_audit",
        "contract_id": contract["contract_id"],
        "doc_path": str(DOC_PATH.relative_to(ROOT)),
        "summary_of_theorems": {
            "T1_single_path_z3_coset_invariant": (
                "For any sign schedule epsilon in {-1, +1}^k with net sign S(epsilon) = sum_l epsilon_l, "
                "every single-path sum V_epsilon(t) = (X, Y) satisfies X - Y == S(epsilon) (mod 3). "
                "Balanced even schedules (k=2m, S=0) annihilate the mod-3 obstruction for all m >= 1."
            ),
            "T2_paired_difference_sign_invariance": (
                "The paired path-difference distribution Delta_epsilon(t, u) = V_epsilon(t) - V_epsilon(u) "
                "is invariant across all 2^k sign schedules epsilon in {-1, +1}^k."
            ),
            "T3_universal_one_third_nonunit_law": (
                "Every paired difference satisfies 3 | (Delta_X - Delta_Y) over Z and "
                "(Delta_X, Delta_Y) == (sum_l epsilon_l (u_l - t_l)) * (1, 1) (mod 3), so exactly "
                "9^k / 3 = 3^(2k-1) pairs have v_3(Delta) >= 1 and 2 * 3^(2k-1) have v_3(Delta) = 0 for all k >= 1."
            ),
        },
        "single_path_coset_audit": single_path_rows,
        "paired_difference_sign_invariance_audit": sign_invariance_rows,
        "universal_one_third_valuation_audit": valuation_rows,
        "verification": {
            "theorem_1_single_path_coset_and_zero_counts_verified": bool(t1_ok),
            "theorem_2_paired_difference_sign_invariance_verified": bool(t2_ok),
            "theorem_3_universal_one_third_valuation_law_verified": bool(t3_ok),
        },
        "guardrails": contract["guardrails"],
    }


def write_native_higher_call_signed_path_valuation_audit_report(
    path: Path = ARTIFACT_PATH,
) -> dict[str, Any]:
    report = build_native_higher_call_signed_path_valuation_audit_report()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Write JSON artifact to research/reductions/.")
    parser.add_argument("--no-write", action="store_true", help="Build and validate report without writing.")
    args = parser.parse_args(argv)

    if args.write and not args.no_write:
        report = write_native_higher_call_signed_path_valuation_audit_report()
    else:
        report = build_native_higher_call_signed_path_valuation_audit_report()

    print(
        json.dumps(
            {
                "subsystem": report["subsystem"],
                "verification": report["verification"],
                "single_path_schedules_checked": len(report["single_path_coset_audit"]),
                "sign_invariance_call_counts_checked": len(report["paired_difference_sign_invariance_audit"]),
                "valuation_call_counts_checked": len(report["universal_one_third_valuation_audit"]),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
