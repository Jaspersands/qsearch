"""Exceptional primes split by the parity of h = (p-1)/K (equivalently: is -1 in Q_0?).
Reads dfs2b-format outputs (INFEASIBLE / FEASIBLE lines), read-only. For each K and each
parity class, prints decided primes, infeasible count and the largest infeasible prime.
Usage: python parity_table.py FILE [FILE ...]"""
import re, sys
from collections import defaultdict
st = {}
for f in sys.argv[1:]:
    for line in open(f):
        m = re.match(r"(INFEASIBLE|FEASIBLE) k=(\d+) p=(\d+)", line)
        if m:
            st[(int(m.group(2)), int(m.group(3)))] = m.group(1)
agg = defaultdict(list)
for (K, p), s in st.items():
    agg[(K, ((p - 1) // K) % 2)].append((p, s))
for (K, par), L in sorted(agg.items()):
    L.sort()
    inf = [p for p, s in L if s == "INFEASIBLE"]
    lo, hi = L[0][0], L[-1][0]
    top = [p for p, s in L if p > (max(inf) if inf else 0)]
    print(f"K={K} h {'even' if par == 0 else 'odd'}: decided={len(L)} in [{lo},{hi}] infeasible={len(inf)} "
          f"max_infeasible={max(inf) if inf else None} feasible_above_max={len(top)}")
    # windowed infeasible fraction
    if K >= 8:
        for a in range(4000, 20001, 2000):
            w = [s for p, s in L if a <= p < a + 2000]
            if w:
                print(f"   [{a},{a+2000}): decided {len(w)}, infeasible {sum(s=='INFEASIBLE' for s in w)}")
