#!/usr/bin/env python
"""Summarize tri_results.json (written by tri.py) for the review note."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
fn = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "tri_results.json")
d = json.load(open(fn))
print("summary:", {k: v for k, v in d["summary"].items() if k != "primes"})
for k, ps in d["summary"]["primes"].items():
    print(f"kappa={k}: {len(ps)} primes, {min(ps)}..{max(ps)}")
agg = {}
for r in d["random_and_adversarial"]:
    for a, st in r["by_a"].items():
        key = (r["kappa"], int(a))
        A = agg.setdefault(key, dict(runs=0, used_all=0, max_used=0, max_elims=0, max_pow=0))
        A["runs"] += st["runs"]
        A["used_all"] += st["used_all"]
        for f in ("max_used", "max_elims", "max_pow"):
            A[f] = max(A[f], st[f])
print("kappa a  M  runs  used_all_M  max_used  max_elims(<=3(a+1))  max_pow(<=M+a)")
for (k, a), A in sorted(agg.items()):
    M = (a + 1) * (a + 2) // 2
    print(f"{k:5d} {a:2d} {M:3d} {A['runs']:6d} {A['used_all']:9d} {A['max_used']:8d} "
          f"{A['max_elims']:6d}/{3*(a+1):<3d} {A['max_pow']:6d}/{M+a}")
print("exhaustive:")
for e in d["exhaustive"]:
    print("  p=%d kappa=%d a=%d M=%d tuples=%d fails=%d used_all_M=%d  (alpha,beta)=(%s,%s)" % (
        e["p"], e["kappa"], e["a"], e["M"], e["tuples"], e["fails"], e["used_all"], e["alpha"], e["beta"]))
print("tightness (M-1 columns, existence of any nonzero x in (P u {0})^(M-1)):")
for t in d["tightness"]:
    print("  p=%d kappa=%d a=%d N=%d tried=%d -> %s %s" % (
        t["p"], t["kappa"], t["a"], t["N"], t["tried"],
        ("COUNTEREXAMPLE " + str(t["counterexample"])) if t["counterexample"] else "none found",
        ("| solver: " + t["solver_on_counterexample"]) if t["counterexample"] else ""))
print("seconds:", round(d["seconds"]))
