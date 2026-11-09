"""Feasibility table: which (p, S, k, d, L) admit a class-constant realization (gadget_cnf)."""
import sys, time
from gadget_sat import parse_S, parse_L
from gadget_cnf import solve

CASES = [
    # (a) kappa = 2: S = squares + 0
    *[(p, 'pow:2', k, d, L) for p in (5, 7, 11, 13) for (k, d, L) in
      [(1, 1, 'all'), (1, 2, 'all'), (2, 2, 'nest'), (2, 2, 'all')]],
    # (a) kappa = 3: S = cubes + 0
    *[(p, 'pow:3', k, d, L) for p in (7, 13) for (k, d, L) in
      [(1, 1, 'all'), (1, 2, 'all'), (2, 2, 'nest'), (2, 2, 'all')]],
    # (b) KOW small coefficients C = [-floor(q/4), floor(q/4)]
    *[(q, f'int:{q // 4}', k, d, L) for q in (5, 7, 11, 13) for (k, d, L) in
      [(1, 1, 'all'), (1, 2, 'all'), (2, 2, 'nest'), (2, 2, 'all')]],
    # (c) subset sum, S = {0,1}, one dimension
    *[(p, 'set:0,1', k, d, L) for p in (5, 7) for (k, d, L) in
      [(1, 1, 'all'), (2, 1, 'nest'), (2, 1, 'all'), (3, 1, 'nest')]],
    # more dimensions at p = 5, kappa = 2
    (5, 'pow:2', 2, 3, 'all'), (5, 'pow:2', 3, 3, 'nest'), (5, 'pow:2', 3, 3, 'all'),
    (7, 'pow:2', 2, 3, 'all'), (7, 'pow:2', 3, 3, 'nest'),
]
only = sys.argv[1:] 
for (p, Sspec, k, d, Lspec) in CASES:
    tag = f'{p} {Sspec} {k} {d} {Lspec}'
    if only and not any(o in tag for o in only):
        continue
    S = parse_S(p, Sspec)
    L = parse_L(p, k, Lspec)
    t0 = time.time()
    r, sol, dt = solve(p, S, k, d, L, nondeg=True)
    print(f'p={p:2d} S={Sspec:8s} k={k} d={d} L={Lspec:5s} |L|={len(L):4d}: {r.upper():5s} [{dt:7.1f}s]', flush=True)
