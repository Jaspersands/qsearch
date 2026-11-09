"""Referee run 1: own ALG-Q1 (myq1.py) on the search agent's 33 banks and on the 8 saved heavy banks.
Usage: run_banks.py seed"""
import sys, os, json, glob, random
from collections import Counter
from myq1 import GF, solve, verify, forward, flag_basis, inspan, rk, steer_bad, backward

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
rng = random.Random(seed)
here = os.path.dirname(os.path.abspath(__file__))
bd = os.path.join(here, "..", "2026-11-05-rees-sde-q1-search", "banks")
print("== search-agent banks: own ALG-Q1 at their budget D_3(a)+a (counts below f not asserted) ==")
tot = Counter()
for fn in sorted(glob.glob(os.path.join(bd, "*.json"))):
    bk = json.load(open(fn))
    F, cols = GF(bk["p"], bk["kappa"]), bk["cols"]
    for rule in ("first", "last", "random"):
        # identity order: closure check
        st = forward(F, cols, rule, rng)
        line = [os.path.basename(fn), rule, st["status"]]
        if st["status"] == "stall":
            U, _ = flag_basis(F, st["rounds"])
            r = st["r"]; q = r - len(U)
            BinU = [i for i in st["B"] if inspan(U, cols[i], F.p)]
            eps = len(U) - len(BinU)
            Rc = set(i for R in st["rounds"] for i in R.S)
            Fin = [i for i in range(len(cols)) if i not in Rc and inspan(U, cols[i], F.p)]
            line += ["q=%d eps=%d BminusU=%d T=%d pi=%d" % (q, eps, r - len(BinU), len(st["T"]), len(st["pool"]))]
            if eps == 0:
                nb = steer_bad(F, cols, st["rounds"], Fin)
                fails = 0
                for _ in range(20):
                    x = backward(F, cols, st["rounds"], Fin, rng)
                    if x is None:
                        fails += 1
                    else:
                        assert verify(F.p, F.k, cols, x)
                line += ["closure bad=%d fails=%d/20" % (nb, fails)]
                tot["closure-solved" if fails < 20 else "closure-unsolved"] += 1
            else:
                tot["eps>0"] += 1
        elif st["status"] == "ok":
            x = backward(F, cols, st["rounds"], st["B"], rng)
            tot["ok"] += 1
        else:
            assert verify(F.p, F.k, cols, st["x"]); tot["direct"] += 1
        print(*line, flush=True)
print("totals", dict(tot))

print("== saved heavy banks (heavy_found_3.jsonl): table ALG-Q1 (no fallback) and code ALG-Q1 ==")
hf = os.path.join(here, "..", "2026-11-05-rees-sde-q1", "heavy_found_3.jsonl")
for ln, l in enumerate(open(hf)):
    d = json.loads(l)
    F, cols = GF(d["p"], d["k"]), d["cols"]
    res = Counter()
    heavy_seen = []
    for t in range(40):
        for fb in (False, True):
            tr = []
            x = solve(F, cols, rng, rule="random", fallback=fb, passes=8, trace=tr)
            ok = x is not None and verify(F.p, F.k, cols, x)
            res[(fb, ok)] += 1
            for dd, c, info in tr:
                if c == "heavy":
                    heavy_seen.append((fb, info["load"], info["colsY"], info["fY"], info["colsU"], info["fU"], info["rounds"]))
                if c == "absorb-leaf" and info["load"] >= 3:
                    res[("leaf-load>=3", fb, info["nmax"], info["fails"])] += 1
    print("bank", ln, dict(res), "heavy events", len(heavy_seen), heavy_seen[:2], flush=True)
