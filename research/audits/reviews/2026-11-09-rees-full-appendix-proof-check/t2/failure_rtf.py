"""t2 check 2b: RtF (with (N1)-(N6)) on failure-branch charts of Lemma tb-chart that pass the
Lie-ring check stated after lem:tb-howell-rounds but have class > c.  Adversarial solver (random
answers, as an erring call may give).  Records whether some socle handed to the field solver
has class > c, i.e. is outside Definition def:input-contract.  Finite search, fixed seeds."""
import random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_chart as cc
import check_rtf as cr
from zmod import Ring, FreeLieZ, howell
cc.rng = random.Random(99); cr.rng = random.Random(98)
out = []

def socle_class_gt(tensor, m0, p, c):
    if m0 == 0:
        return False
    Rp = Ring(p, 1)
    E = [[1 if t == i else 0 for t in range(m0)] for i in range(m0)]
    def br(x, y):
        o = [0] * m0
        for a in range(m0):
            if x[a]:
                for b in range(m0):
                    if y[b]:
                        o = [(u + x[a] * y[b] * t) % p for u, t in zip(o, tensor[a, b])]
        return o
    gam = E
    for _ in range(c):
        rows, _ = howell(Rp, gam, m0)
        gam = [br(r, x) for (_, _, r) in rows for x in E]
        gam = [g for g in gam if any(g)]
        if not gam:
            return False
    return True

found = []
for (p, e, s, c) in [(5, 2, 2, 3), (5, 3, 2, 3), (7, 2, 2, 4), (5, 2, 3, 2), (7, 2, 3, 3)]:
    R = Ring(p, e); FL = FreeLieZ(s, c); d = FL.d
    charts = calls = bad_calls = 0
    for _ in range(150):
        I = cc.random_ideal(FL, R, cc.rng.randrange(1, 4))
        idx, n = I.index(), 0
        while idx % p == 0:
            idx //= p; n += 1
        N = cc.dual_generators(I)
        for kk in range(1, n + 1):
            Y = cc.sample_perp(N, R, d, kk)
            if cc.span_order(Y, d, R.M) == p ** n:
                continue
            ch = cc.chart(R, FL, Y)
            br = cc.lie_check(R, ch["exps"], ch["c"])
            if not br or cc.chart_class(R, ch["exps"], br, c) or not ch["exps"]:
                continue
            if sum(ch["exps"]) * 1 > 7:
                continue
            charts += 1
            L = cr.Chart(p, ch["exps"], ch["c"])
            for _ in range(20):
                rec = []
                cr.rtf(L, None, "adv", False, None, lambda T, m0, pp: rec.append(socle_class_gt(T, m0, pp, c)))
                calls += len(rec); bad_calls += sum(rec)
                if any(rec) and len(found) < 3 and not any(f[0] == (p, e, s, c) for f in found):
                    found.append(((p, e, s, c), ch["exps"], {k: v for k, v in ch["c"].items() if any(v)}))
    out.append(f"{(p, e, s, c)}: {charts} passing charts of class > c; {calls} solver calls, {bad_calls} on a socle of class > c")
for f in found:
    out.append(f"  example chart {f}")
print("\n".join(out))
(Path(__file__).resolve().parent / "failure_rtf.out").write_text("\n".join(out) + "\n")
