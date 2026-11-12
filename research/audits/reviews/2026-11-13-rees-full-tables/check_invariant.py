"""Check that tab:full-grade-budget (class-3 and class-12 profiles) and tab:random-column-budget
do not depend on the Schedule-1 depth, so the change 145 -> 53 (depth ceil(log2 t_d)) leaves
them unchanged.

(1) tab:full-grade-budget: re-run theorems.uniform_bch_rees.symmetric_recovery_budget on every
    recorded case of research/reductions/rees_full_grade_budget.json and compare all fields;
    check that every stage is linear (kappa_d = 1, arity g_d + 1) or Schedule 2 (guard
    p >= 16 kappa^(2kappa+2), arity (g+1)((kappa-1)g+1)), i.e. that no stage uses Schedule 1.
    The function raises "field guard" rather than fall back to Schedule 1.
(2) tab:random-column-budget: every stage of every case of
    research/reductions/random_column_rees.json has width = width_per_grade (M = 4u), so no
    Schedule-1 arity enters.
(3) The UiThree/UiTwelve macros (rees_uniform_instrument.json) are built from the same
    symmetric_recovery_budget stages (theorems/rees_uniform_instrument.py line 13 import).

Run (repo root):
  nice -n 19 /opt/anaconda3/bin/python research/audits/reviews/2026-11-13-rees-full-tables/check_invariant.py
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT))

from theorems.uniform_bch_rees import symmetric_recovery_budget  # noqa: E402


def frac(x):
    return Fraction(x["numerator"], x["denominator"])


def norm(x):
    """Fractions as {numerator, denominator}, as in the recorded JSON."""
    if isinstance(x, Fraction):
        return {"numerator": x.numerator, "denominator": x.denominator}
    if isinstance(x, dict):
        return {k: norm(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [norm(v) for v in x]
    return x


def main():
    ok = True
    report = {"full_grade": [], "random_column": []}
    fg = json.loads((ROOT / "research/reductions/rees_full_grade_budget.json").read_text())
    for case in fg["cases"]:
        prof, p = tuple(case["lower_central_dimensions"]), case["supplied_prime"]
        err = frac(case["error_target"])
        fresh = symmetric_recovery_budget(prof, prime=p, error=err)
        fresh = json.loads(json.dumps(norm(fresh)))
        diffs = [k for k in case if k in fresh and json.dumps(case[k], sort_keys=True, default=str)
                 != json.dumps(fresh[k], sort_keys=True, default=str)]
        kinds = []
        for st in case["stages_top_down"]:
            d, a, k, M = st["grade"], st["rank"], st["reduced_degree"], st["arity"]
            assert k == gcd(d, p - 1)
            if k == 1:
                kind = "lin" if M == a + 1 else "??"
            elif p >= 16 * k ** (2 * k + 2) and M == (a + 1) * ((k - 1) * a + 1):
                kind = "S2"
            else:
                kind = "??"
            kinds.append((d, kind))
        no_s1 = all(kd != "??" for _, kd in kinds)
        ok &= (not diffs) and no_s1
        report["full_grade"].append(dict(profile=prof, p=str(p), fields_differing=diffs,
                                         stage_kinds=kinds, no_schedule1=no_s1))
        print(f"full-grade {prof} p={p}: differing fields {diffs}; stages {kinds}; no Schedule 1: {no_s1}")
    rc = json.loads((ROOT / "research/reductions/random_column_rees.json").read_text())
    for i, case in enumerate(rc["cases"]):
        w = case["width_per_grade"]
        widths = [st["width"] for st in case["stages_top_down"]]
        same = all(x == w for x in widths)
        ok &= same
        report["random_column"].append(dict(case=i, width_per_grade=w, stage_widths=widths, uniform=same))
        print(f"random-column case {i}: width per grade {w}, stage widths {widths}, uniform {same}")
    src = (ROOT / "theorems/rees_uniform_instrument.py").read_text()
    uses = "from theorems.uniform_bch_rees import symmetric_recovery_budget" in src
    ok &= uses
    report["uniform_instrument_uses_symmetric_recovery_budget"] = uses
    report["all_ok"] = ok
    (HERE / "check_invariant.json").write_text(json.dumps(report, indent=1, default=str) + "\n")
    print("uniform instrument built on symmetric_recovery_budget:", uses)
    print("all ok:", ok)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
