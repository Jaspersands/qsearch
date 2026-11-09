import random, sys, time
from harness import Tally, run_bank
import families
from collections import Counter
p, k = 10007, 2
for J in (4,5):
  for c_ in range(2):
    T=Tally(); t0=time.time(); rs=Counter()
    for s in range(5):
        rng=random.Random(100*J+s+1000*c_)
        PL=[2*(J-1)]*3 if c_ else [rng.randrange(J, 2*J-1) for _ in range(3)]
        bank = families.fam_design(rng, p, k, J, P_list=PL, m=2, b=sum(PL)+3, degenerate=True, tcount=sum(PL)+1, rmax=56)
        if bank is None: print('none'); continue
        rs[len(bank[0])]+=1
        out, rec, ex = run_bank(bank, p, k, J, T, passes=3, tag='ts', seed=s)
        print(J, len(bank[0]), dict(rec.branch), [ (e['q'],e['b'],e['eps'],e['qp']) for e in rec.events][:3], flush=True)
    sm=T.summary(); print(J, "%.1fs"%(time.time()-t0), sm['outcomes'], sm['branch'], dict(rs), T.fail[:2], flush=True)
