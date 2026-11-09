"""t2 check 1c: Lemma tb-chart Part B at e = 1 (success event), and k = n exactly (minimal rows)."""
import random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_chart as cc
from zmod import Ring, FreeLieZ
cc.rng = random.Random(4242)
out = []
tot = good = 0
for (p, e, s, c, extra) in [(3, 1, 2, 2, 3), (5, 1, 2, 3, 3), (5, 1, 3, 2, 3), (7, 1, 2, 4, 3), (5, 2, 2, 3, 0), (3, 3, 2, 2, 0)]:
    R = Ring(p, e); FL = FreeLieZ(s, c); d = FL.d
    loc = 0
    for _ in range(40):
        I = cc.random_ideal(FL, R, cc.rng.randrange(1, 4))
        idx, n = I.index(), 0
        while idx % p == 0:
            idx //= p; n += 1
        N = cc.dual_generators(I)
        Y = cc.sample_perp(N, R, d, n + extra)
        if cc.span_order(Y, d, R.M) != p ** n:
            continue
        ch = cc.chart(R, FL, Y)
        ok = cc.verify_chart(R, FL, I, n, ch)
        br = cc.lie_check(R, ch["exps"], ch["c"])
        ok = ok and bool(br) and cc.chart_class(R, ch["exps"], br, c)
        tot += 1; good += ok; loc += 1
    out.append(f"(p,e,s,c)={(p, e, s, c)} rows=n+{extra}: {loc} charts on the success event")
out.append(f"RESULT {good}/{tot} charts verified against F/I (e = 1 cases and k = n cases)")
print("\n".join(out))
(Path(__file__).resolve().parent / "check_chart_e1.out").write_text("\n".join(out) + "\n")
