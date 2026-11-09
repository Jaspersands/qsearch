import random, sys, time
from harness import Tally, run_bank
import families
from collections import Counter
p, k = 10007, 2
for J in (2,3,4):
  for st in ["design_rado","design_top","design_u30","design_mix"]:
    T=Tally(); t0=time.time(); rs=Counter()
    for s in range(8):
        bank = families.make(st, random.Random(s), p, k, J, 40)
        rs[len(bank[0])]+=1
        run_bank(bank, p, k, J, T, passes=3, tag=st, seed=s)
    sm=T.summary(); print(J, st, "%.1fs"%(time.time()-t0), sm['outcomes'], sm['branch'], dict(rs), T.fail[:2], flush=True)
