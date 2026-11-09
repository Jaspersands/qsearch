"""Sanity: reproduce E_2(4) below 120, E_2(5) below 200 and E_2(7) below 400 with rcdfs (R = Z_D, K = {0})."""
from rc import feasible, is_prime
for D, top in [(4, 120), (5, 200), (7, 400)]:
    bad = []
    for p in range(D + 1, top, D):
        if not is_prime(p): continue
        st, a, b, n = feasible(p, D, list(range(D)), [0])
        assert st in (0, 1)
        if st == 0: bad.append(p)
    print("E_2(%d) below %d:" % (D, top), bad, flush=True)
