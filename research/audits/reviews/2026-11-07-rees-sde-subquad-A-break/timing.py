import random, time, sys
from harness import Tally, run_bank
import families
for (J,k,p) in [(2,2,10007),(3,2,10007),(4,2,10007),(3,3,100003)]:
    for fam in ["planted","adapt_rado","twist","uniform"]:
        T=Tally(); t0=time.time()
        bank = families.make(fam, random.Random(5), p, k, J, 40)
        t1=time.time()
        run_bank(bank, p, k, J, T, passes=5, tag=fam)
        print(J,k,fam,"gen %.1fs run %.1fs"%(t1-t0,time.time()-t1), T.summary()['branch'], T.fail[:1], flush=True)
