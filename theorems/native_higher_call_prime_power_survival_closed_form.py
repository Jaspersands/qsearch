"""Higher-call prime-power survival closed forms: Eisenstein isomorphism, trinomial zero law, and Fourier spectra.

Connects `theorems/native_response_path_valuation.py` (`local_difference_counts`, `iid_path_collision_law`)
and `theorems/native_higher_call_signed_path_valuation_audit.py` by proving and auditing:
1. Theorem 1 (Unimodular Eisenstein Isomorphism and Squared-Trinomial Zero-Difference Law):
   The unimodular map `iota(x, y) = (x + y) + y*omega` (`omega = e^(2*pi*i/3)`) maps
   `beta_0 = (1, 0), beta_1 = (-1, 1), beta_2 = (0, -1)` to `1, omega, omega^2`.
   At fixed call count `k >= 1`, `(a, b, c) -> (a - b, b - c)` is strictly injective on the simplex
   `Sigma_k = {(a, b, c) >= 0 : a + b + c = k}`, so the number of distinct integer endpoints is
   `(k + 1)*(k + 2)/2` and the exact integer zero-difference count is
   `N_k(0) = sum_{a+b+c=k} (k! / (a! b! c!))^2`.
2. Theorem 2 (Histogram Congruence Criterion for `3^h | Delta(t, u)`):
   For `delta_a = a - a', delta_b = b - b', delta_c = c - c'`, `3^h | Delta(t, u)` iff
   `delta_a == delta_b == delta_c == r * 3^(h - 1) (mod 3^h)` for some `r in {0, 1, 2}`.
3. Theorem 3 (Exact Fourier Eigenvalue Formula for Prime-Power Survival `N_k(3^h)`):
   `N_k(3^h) = (1 / 9^h) * sum_{u, v in Z_{3^h}^2} Lambda_h(u, v)^k`, where
   `Lambda_h(u, v) = 3 + 2*cos(2*pi*(2u - v)/3^h) + 2*cos(2*pi*(u + v)/3^h) + 2*cos(2*pi*(u - 2v)/3^h)`.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
import math
from pathlib import Path
from typing import Any

from theorems.native_response_path_valuation import DIGITS, iid_path_collision_law, local_difference_counts


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "research" / "hypotheses" / "native_higher_call_prime_power_survival_closed_form_contract.json"
ARTIFACT_PATH = ROOT / "research" / "reductions" / "native_higher_call_prime_power_survival_closed_form.json"
DOC_PATH = ROOT / "research" / "NATIVE_HIGHER_CALL_PRIME_POWER_SURVIVAL_CLOSED_FORM.md"


def _fraction_str(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def trinomial(n: int, a: int, b: int, c: int) -> int:
    if a < 0 or b < 0 or c < 0 or a + b + c != n:
        return 0
    return math.factorial(n) // (math.factorial(a) * math.factorial(b) * math.factorial(c))


def eisenstein_coords(x: int, y: int) -> tuple[int, int]:
    """Return (u, v) in Z^2 such that iota(x, y) = u + v * omega = (x + y) + y * omega."""
    return (int(x) + int(y), int(y))


def eisenstein_norm(u: int, v: int) -> int:
    """Return the algebraic norm N(u + v * omega) = u^2 - u*v + v^2 in Z[omega]."""
    return int(u) * int(u) - int(u) * int(v) + int(v) * int(v)


def squared_trinomial_zero_count(k: int) -> int:
    """Return N_k(0) = sum_{a+b+c=k} (k! / (a! b! c!))^2."""
    total = 0
    for a in range(k + 1):
        for b in range(k - a + 1):
            c = k - a - b
            t = trinomial(k, a, b, c)
            total += t * t
    return total


def histogram_congruence_survival_count(k: int, h: int) -> int:
    """Compute N_k(3^h) using Theorem 2's histogram congruence delta_a == delta_b == delta_c == r*3^(h-1) mod 3^h."""
    if h < 1:
        raise ValueError("Require h >= 1")
    mod = 3**h
    step = 3 ** (h - 1)
    # Group simplex histograms by (a mod 3^h, b mod 3^h, c mod 3^h)
    residue_buckets: dict[tuple[int, int, int], int] = {}
    for a in range(k + 1):
        for b in range(k - a + 1):
            c = k - a - b
            key = (a % mod, b % mod, c % mod)
            residue_buckets[key] = residue_buckets.get(key, 0) + trinomial(k, a, b, c)

    total = 0
    for (ra, rb, rc), mult1 in residue_buckets.items():
        for r in (0, 1, 2):
            shift = r * step
            target_key = ((ra - shift) % mod, (rb - shift) % mod, (rc - shift) % mod)
            mult2 = residue_buckets.get(target_key, 0)
            total += mult1 * mult2
    return total


def fourier_spectral_survival_count(k: int, h: int) -> float:
    """Compute N_k(3^h) via Theorem 3's Fourier eigenvalue sum (1 / 9^h) sum_{u,v} Lambda_h(u, v)^k."""
    mod = 3**h
    acc = 0.0
    for u in range(mod):
        for v in range(mod):
            lam = (
                3.0
                + 2.0 * math.cos(2.0 * math.pi * (2 * u - v) / float(mod))
                + 2.0 * math.cos(2.0 * math.pi * (u + v) / float(mod))
                + 2.0 * math.cos(2.0 * math.pi * (u - 2 * v) / float(mod))
            )
            acc += max(0.0, lam) ** k
    return acc / float(mod * mod)


def audit_eisenstein_isomorphism_and_simplex_injectivity() -> list[dict[str, Any]]:
    """Verify Theorem 1 across call counts k = 1..10."""
    # Check digit images under iota(x, y) = (x + y) + y * omega
    digit_images = [eisenstein_coords(dx, dy) for dx, dy in DIGITS]
    # 1 = (1, 0), omega = (0, 1), omega^2 = -1 - omega = (-1, -1)
    expected_digit_images = [(1, 0), (0, 1), (-1, -1)]
    digits_are_cube_roots = bool(digit_images == expected_digit_images and all(eisenstein_norm(u, v) == 1 for u, v in digit_images))

    rows: list[dict[str, Any]] = []
    for k in range(1, 11):
        diffs = local_difference_counts(k)
        # Reconstruct single-path endpoint map on Sigma_k
        endpoints: set[tuple[int, int]] = set()
        for a in range(k + 1):
            for b in range(k - a + 1):
                c = k - a - b
                endpoints.add((a - b, b - c))
        simplex_size = (k + 1) * (k + 2) // 2
        injective = len(endpoints) == simplex_size

        actual_zero_pairs = int(diffs[(0, 0)])
        formula_zero_pairs = squared_trinomial_zero_count(k)

        rows.append(
            {
                "calls_k": k,
                "simplex_size_binom_k_plus_2_2": simplex_size,
                "distinct_single_path_endpoints": len(endpoints),
                "simplex_map_strictly_injective": bool(injective),
                "actual_integer_zero_difference_pairs": actual_zero_pairs,
                "squared_trinomial_closed_form_zero_pairs": formula_zero_pairs,
                "zero_pair_fraction": _fraction_str(Fraction(actual_zero_pairs, 9**k)),
                "matches_theorem_1": bool(
                    digits_are_cube_roots and injective and actual_zero_pairs == formula_zero_pairs
                ),
            }
        )
    return rows


def audit_prime_power_survival_closed_forms() -> list[dict[str, Any]]:
    """Verify Theorems 2 and 3 across call counts k = 1..7 and valuation thresholds h = 1, 2, 3."""
    rows: list[dict[str, Any]] = []
    for k in range(1, 8):
        law = iid_path_collision_law(n=1, d=3, sites=1, calls=k)
        strata = {int(s["valuation"]): int(s["local_count"]) for s in law["ideal_strata"]}
        for h in (1, 2, 3):
            actual_survival = sum(strata[v] for v in range(h, 4))
            hist_congruence_survival = histogram_congruence_survival_count(k, h)
            fourier_survival_float = fourier_spectral_survival_count(k, h)
            fourier_rel_err = abs(fourier_survival_float - float(actual_survival)) / max(1.0, float(actual_survival))

            rows.append(
                {
                    "calls_k": k,
                    "valuation_threshold_h": h,
                    "modulus_3_pow_h": 3**h,
                    "actual_survival_count_v3_ge_h": actual_survival,
                    "histogram_congruence_closed_form_count": hist_congruence_survival,
                    "fourier_spectral_sum_float": fourier_survival_float,
                    "fourier_relative_error": fourier_rel_err,
                    "survival_fraction": _fraction_str(Fraction(actual_survival, 9**k)),
                    "matches_theorems_2_and_3": bool(
                        actual_survival == hist_congruence_survival and fourier_rel_err < 1e-11
                    ),
                }
            )
    return rows


def build_native_higher_call_prime_power_survival_closed_form_report() -> dict[str, Any]:
    """Build the complete JSON artifact for Subsystem 14."""
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    t1_rows = audit_eisenstein_isomorphism_and_simplex_injectivity()
    t23_rows = audit_prime_power_survival_closed_forms()

    t1_ok = all(r["matches_theorem_1"] for r in t1_rows)
    t23_ok = all(r["matches_theorems_2_and_3"] for r in t23_rows)

    return {
        "schema_version": "1.0.0",
        "subsystem": "native_higher_call_prime_power_survival_closed_form",
        "contract_id": contract["contract_id"],
        "doc_path": str(DOC_PATH.relative_to(ROOT)),
        "summary_of_theorems": {
            "T1_eisenstein_isomorphism_and_squared_trinomial_law": (
                "iota(x, y) = (x + y) + y*omega maps beta_0, beta_1, beta_2 to 1, omega, omega^2; "
                "(a, b, c) -> (a - b, b - c) is strictly injective on Sigma_k, so "
                "N_k(0) = sum_{a+b+c=k} (k! / (a! b! c!))^2."
            ),
            "T2_histogram_congruence_criterion": (
                "3^h | Delta(t, u) iff delta_a == delta_b == delta_c == r * 3^(h - 1) (mod 3^h) "
                "for some r in {0, 1, 2}."
            ),
            "T3_fourier_eigenvalue_survival_formula": (
                "N_k(3^h) = (1 / 9^h) sum_{u,v in Z_{3^h}^2} Lambda_h(u, v)^k."
            ),
        },
        "eisenstein_and_squared_trinomial_audit": t1_rows,
        "prime_power_survival_closed_form_audit": t23_rows,
        "verification": {
            "theorem_1_eisenstein_and_squared_trinomial_verified": bool(t1_ok),
            "theorems_2_and_3_prime_power_survival_closed_forms_verified": bool(t23_ok),
        },
        "guardrails": contract["guardrails"],
    }


def write_native_higher_call_prime_power_survival_closed_form_report(
    path: Path = ARTIFACT_PATH,
) -> dict[str, Any]:
    report = build_native_higher_call_prime_power_survival_closed_form_report()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Write JSON artifact to research/reductions/.")
    parser.add_argument("--no-write", action="store_true", help="Build and validate report without writing.")
    args = parser.parse_args(argv)

    if args.write and not args.no_write:
        report = write_native_higher_call_prime_power_survival_closed_form_report()
    else:
        report = build_native_higher_call_prime_power_survival_closed_form_report()

    print(
        json.dumps(
            {
                "subsystem": report["subsystem"],
                "verification": report["verification"],
                "trinomial_call_counts_checked": len(report["eisenstein_and_squared_trinomial_audit"]),
                "prime_power_survival_configs_checked": len(report["prime_power_survival_closed_form_audit"]),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
