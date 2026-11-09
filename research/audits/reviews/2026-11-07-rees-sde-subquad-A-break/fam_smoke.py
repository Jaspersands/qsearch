import random, sys, time
from harness import Tally, run_bank
import families
p, k, J, r, n = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
for fam in families.NAMES:
    T = Tally(); t0=time.time()
    for s in range(n):
        bank = families.make(fam, random.Random(s), p, k, J, r)
        run_bank(bank, p, k, J, T, passes=3, tag=fam, seed=s)
    sm = T.summary()
    print(fam, "%.1fs" % (time.time()-t0), sm['outcomes'], sm['branch'], T.fail[:2], flush=True)
