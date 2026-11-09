"""One complete good level-4 node (746496 columns) at kappa = 6, a = 1: the level-4 merge runs.

Run: nice -n 10 /opt/anaconda3/bin/python level4_check.py   (several minutes)
"""
import time
import composite_restarts as c

for p in (58321, 15361):
    t0 = time.time()
    k = 6
    star, r = c.best_ell_star(p, k), c.rho(p, k)
    # family_c fills the first free slots; later free level-2 nodes use y = x
    pre = c.family_c(p, k, 1, star, 4)
    v = c.prefix_run(p, k, pre, collapse=True, level=4)
    print(f"p={p} nu={c.nus(p, k)} rho={r} variant runs={v['runs']} collapsed={v['collapsed']} "
          f"completed={v['completed']} columns={len(pre)} time={time.time()-t0:.0f}s", flush=True)
    assert v["runs"] == r
print("LEVEL4 OK")
