"""Recompute the mixed-instance statements after prop:mixed-schedule (appendix-schedule3.tex,
paragraph after the proof) at the Schedule-1 depth L_d of eq:Bd:
  "at p = 151 ... the rule adds 60 columns at grade 9 (at 226 primes below 3600 some column is
   added)", "At the six primes of the table no column is added", the tree-abort range
  2^-6.91 .. 2^-6.38, and the Schedule-2 grades kept.

Method: reuse research/audits/reviews/2026-11-04-rees-mixed-rule/mixed_rule.py (written from the
statement of prop:mixed-schedule, independent of theorems/rees_fcs_budget.py) UNCHANGED, and
replace its module-level `ivanyos_santha_arity(k, a)` (the Schedule-1 arity, full depth) by
G(k, a)^{L} with L = ceil(log2 t_{p,k}). Since that function takes no p, the replacement is done
per prime through a closure set before each call (worst_case_choice and the (S1) hypothesis
check both call it with k = kappa_d of the current p).

Run (repo root):
  nice -n 19 /opt/anaconda3/bin/python research/audits/reviews/2026-11-13-rees-full-tables/scan_mixed.py PMAX
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT))

from theorems.rees_hsp_reduction import zero_sum_length  # noqa: E402

spec = importlib.util.spec_from_file_location(
    "mixed_rule", ROOT / "research/audits/reviews/2026-11-04-rees-mixed-rule/mixed_rule.py")
mr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mr)
FULL = mr.ivanyos_santha_arity
CURRENT_P = [None]


def zero_sum_arity(k: int, a: int) -> int:
    p = CURRENT_P[0]
    t = zero_sum_length(p, k)
    return (k ** (k * (k - 1) // 2) * (a + 1) ** k) ** ((t - 1).bit_length())


_orig_mixed = mr.mixed_rule


def mixed_rule_at(p, *args, **kw):
    CURRENT_P[0] = p
    return _orig_mixed(p, *args, **kw)


def run(depth: str, pmax: int):
    mr.ivanyos_santha_arity = FULL if depth == "full" else zero_sum_arity
    mr.mixed_rule = mixed_rule_at
    rows = []
    for label, p in mr.PRIMES:
        r = mixed_rule_at(p)
        if r is None:
            rows.append(dict(label=label, uses_S3=False))
            continue
        rows.append(dict(label=label, uses_S3=True, Q=mr.round_log2_1dp(r["Q"]),
                         trials=mr.round_log2_1dp(r["max_trials"]), bumps=r["bumps"],
                         types={str(d): t for d, t in r["types"].items()},
                         M={str(d): v for d, v in r["M"].items()},
                         bank_log2=round(mr.f_up_log2(r["bank"]), 3),
                         tree_abort_log2=round(mr.f_up_log2(r["tree_abort"]), 4),
                         hypotheses_ok=r["hypotheses_ok"], error_ok=r["error_ok"]))
    sc = mr.scan(mr.PROFILE, pmax)
    # count of bump primes below 3600 (the paper's phrase); scan() truncates its list at 40
    bump_all = []
    p = len(mr.PROFILE) + 1
    while p <= pmax:
        if mr.is_prime(p):
            r = mixed_rule_at(p)
            if r is not None and not r.get("nonterminating") and r["bumps"]:
                bump_all.append((p, r["bumps"]))
        p += 1
    r151 = mixed_rule_at(151)
    return dict(depth=depth, pmax=pmax, rows=rows,
                scan={k: v for k, v in sc.items() if k != "bump_primes"},
                bump_primes_total=len(bump_all),
                bump_primes_below_3600=sum(1 for q, _ in bump_all if q < 3600),
                largest_bump_prime=max((q for q, _ in bump_all), default=None),
                first_bump_primes=bump_all[:12],
                p151=dict(types={str(d): t for d, t in r151["types"].items()},
                          M={str(d): str(v) for d, v in r151["M"].items()},
                          M_initial={str(d): str(v) for d, v in r151["M_initial"].items()},
                          bumps=r151["bumps"]))


def main():
    pmax = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    out = [run("full", pmax), run("zero_sum", pmax)]
    mr.ivanyos_santha_arity = FULL
    (HERE / f"scan_mixed_{pmax}.json").write_text(json.dumps(out, indent=1, default=str) + "\n")
    for o in out:
        print("==", o["depth"], "pmax", pmax)
        for r in o["rows"]:
            print("  ", r)
        print("   scan:", o["scan"])
        print("   bump primes total", o["bump_primes_total"], "below 3600", o["bump_primes_below_3600"],
              "largest", o["largest_bump_prime"], "first", o["first_bump_primes"])
        print("   p=151:", o["p151"]["bumps"], "bumps; types", o["p151"]["types"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
