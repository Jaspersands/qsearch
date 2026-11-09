"""Small-order-ratio excess and progressions, split into generic (G) and symmetric witnesses.
Usage: python witness_generic_stats.py FILE [FILE ...]"""
import sys
from witness_structure import parse, analyse
from witness_table import classify
data = parse(sys.argv[1:])
acc = {"G": [0, 0.0, 0, 0], "sym": [0, 0.0, 0, 0]}
progs = []
for (K, p), (g, al, be) in sorted(data.items()):
    o = analyse(K, p, g, al, be)
    t = "G" if classify(K, p, o) == {"G"} else "sym"
    s, pairs, e = o["small_order_ratio_pairs"]
    acc[t][0] += s; acc[t][1] += e; acc[t][2] += 1; acc[t][3] += bool(o["progressions"])
    if o["progressions"]:
        progs.append((K, p, t, o["progressions"]))
for t, (s, e, n, npg) in acc.items():
    print(f"{t}: witnesses={n} small-order ratio pairs={s} expected(random)={e:.1f} with progression={npg}")
for r in progs:
    print("progression:", r)
