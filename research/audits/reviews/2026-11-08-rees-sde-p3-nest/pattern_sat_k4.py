"""d = 3 from a 4-dimensional bundle with ALL 80 patterns present (generic 4-dim D(X)).
Together with rank(C) <= 2 being impossible (Theorem 3) and the k = 3 all-pattern UNSAT, a
negative answer shows that a pattern-complete bundle of any dimension k <= 4 never gains 3."""
import time, sys
from pattern_sat import feasible, nz
SOLVER = 'cadical'   # pycosat (earlier version) did not finish the 54-pattern case in 30 min
t = time.time()
print("d=3,k=4, all 80 patterns:", feasible(3, 4, nz(4), solver=SOLVER)[0], f"[{time.time()-t:.0f}s]"); sys.stdout.flush()
t = time.time()
off = [p for p in nz(4) if p[0] != 0]
print("d=3,k=4, delta_1 full support (54 patterns):", feasible(3, 4, off, solver=SOLVER)[0], f"[{time.time()-t:.0f}s]"); sys.stdout.flush()
t = time.time()
two_full = [p for p in nz(4) if p[0] != 0 and p[1] != 0]
print("d=3,k=4, delta_1 and delta_2 both full support (36 patterns):", feasible(3, 4, two_full, solver=SOLVER)[0], f"[{time.time()-t:.0f}s]"); sys.stdout.flush()
t = time.time()
two_full3 = [p for p in nz(3) if p[0] != 0 and p[1] != 0]
print("d=3,k=3, delta_1 and delta_2 both full support (12 patterns, 6 points):", feasible(3, 3, two_full3, solver=SOLVER)[0], f"[{time.time()-t:.0f}s]"); sys.stdout.flush()
