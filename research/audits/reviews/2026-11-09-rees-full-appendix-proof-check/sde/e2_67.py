import sys, time
sys.path.insert(0, '.')
from e2 import E2_upto
t0 = time.time()
s6 = E2_upto(6, 4000)
print("E_2(6) up to 4000:", len(s6), "primes, max", max(s6), f"[{time.time()-t0:.1f}s]"); print(s6); sys.stdout.flush()
s7 = E2_upto(7, 6000)
print("E_2(7) up to 6000:", len(s7), "primes, max", max(s7), f"[{time.time()-t0:.1f}s]"); print(s7)
