"""Random-order failure diagnosis on one saved bank.
usage: order_diag.py bankfile.json N seed
For N random orders: one sss_full iteration; on failure, record status and certificate,
and rerun the SAME order 5 times with fresh coins (block cuts, backward draws) to see
whether the failure is a property of the order."""
import json
import random
import sys
import collections
from q1lib import Field, one_order

rec = json.load(open(sys.argv[1]))
N, seed = int(sys.argv[2]), int(sys.argv[3])
rng = random.Random(seed)
Fd = Field(rec["p"], rec["kappa"])
cols = rec["cols"]
M = len(cols)
C = collections.Counter()
fails = []
for t in range(N):
    perm = list(range(M))
    rng.shuffle(perm)
    x, st, cert = one_order(Fd, cols, perm, rng, passes=10)
    C["ok" if x is not None else st] += 1
    if x is None:
        again = sum(one_order(Fd, cols, perm, random.Random(1000 + j), passes=10)[0] is None for j in range(5))
        c = dict(q=cert["q"], pi=cert["pi"], unused=len(cert["unused"]), BoutU=len(cert["B_out_U"]),
                 swaps=cert["swaps"], rounds=[len(S) for S in cert["rounds"]]) if cert else None
        fails.append(dict(perm=perm, status=st, cert_summary=c, refail_of_5=again))
        print("FAIL", st, c, "same-order refails %d/5" % again, flush=True)
print(rec["family"], rec["kappa"], rec["p"], rec["a"], "orders", N, dict(C))
json.dump(dict(bank=sys.argv[1], N=N, counts=dict(C), fails=fails),
          open(sys.argv[1].replace("banks/", "out/diag_").replace(".json", "_diag.json"), "w"))
