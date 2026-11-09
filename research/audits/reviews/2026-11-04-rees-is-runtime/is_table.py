"""Compact structural cross-check (full Section 3.3 path, early_exit=False). Run with python -O."""
import random, sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import is_count as C
S = C.S
print("p d k a N L | t11 meas/pred | kernels last-run meas/pred | kernel sizes (R,E):count all runs | GE mults meas <= bound | max GE ratio | cls meas <= bound*(runs) | restarts<=nu")
for p, d, a in [(7,2,1),(97,2,1),(65537,2,1),(13,2,2),(97,2,2),(536870951,2,2),(7,3,1),(163,3,1),(163,3,2),(536871001,3,2)]:
    rnd = random.Random(1)
    need = S.columns_required(p, d, a)
    cols = [tuple(rnd.randrange(1, p) for _ in range(a)) for _ in range(need)]
    r = C.run(p, d, a, cols=cols, early_exit=False)
    k, L = r["kappa"], r["L"]
    pr = C.predicted(k, a, L)
    runs = r["restarts"] + 1
    ok = (r["t11"] == pr["t11"] and r["kernel_calls_reported"] == pr["kernels"] and r["kernel_mults"] <= r["kernel_bound"]
          and r["kernel_mults"] <= runs * pr["la_bound"] + runs * pr["kernels"] * a * k ** (k - 1)
          and r["classify"] <= runs * pr["cls_bound"] and r["restarts"] <= r["nu"])
    print(f"{p} {d} {k} {a} {r['M']} {L} | {r['t11']}/{pr['t11']} | {r['kernel_calls_reported']}/{pr['kernels']} | {dict(r['sizes'])} |"
          f" {r['kernel_mults']} <= {r['kernel_bound']} | {r['kernel_max_ratio']:.2f} | {r['classify']} <= {runs*pr['cls_bound']} | {r['restarts']}<={r['nu']} | {'OK' if ok else 'FAIL'}")
