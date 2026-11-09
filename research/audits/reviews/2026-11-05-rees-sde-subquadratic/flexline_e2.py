"""Do single circuits have ANY flexible line at primes in E_2(kappa)?  [exact on samples]

For q = 1 the circuit is two columns (scalars) with ratio r; flexible iff
Sq + r*Sq = F_p.  Exhaustive over r for q = 1; random + patterned circuits for q = 2, 3.
E_2(4) = {5,13,17,29,37,53}, E_2(5) = {11,31,41,61,71,101,131,151,181} (paper, prop:decoupled-sde).
"""
import random, sys
import numpy as np
from common import F, is_prime, realizable
from circuit_flex import flexible_lines, make_circuit

E2 = {4: {5, 13, 17, 29, 37, 53}, 5: {11, 31, 41, 61, 71, 101, 131, 151, 181}, 3: set(), 2: set()}

def q1_flexible_ratios(Fd):
    p = Fd.p
    S = np.zeros(p, bool); S[Fd.Sq] = True
    good = []
    for r in range(1, p):
        T = np.zeros(p, bool)
        for y in Fd.Sq:
            T |= np.roll(S, (r * y) % p)
        if T.all():
            good.append(r)
    return good

rng = random.Random(11)
for k, plist in [(4, [5, 13, 17, 29, 37, 41, 53, 61, 73, 89, 97, 101, 109, 113]),
                 (5, [11, 31, 41, 61, 71, 101, 131, 151, 181, 191, 211, 241])]:
    for p in plist:
        Fd = F(p, k)
        g1 = q1_flexible_ratios(Fd)
        res = []
        for q in (2, 3) if p <= 41 else (2,):
            cnt = tot = 0
            for _ in range(12 if q == 2 else 4):
                cols, delta = make_circuit(Fd, rng, q, None)
                if len({Fd.cls(d) for d in delta}) == 1:
                    continue
                R = realizable(Fd, cols, q)
                tot += 1
                cnt += bool(flexible_lines(Fd, R, q))
            res.append(f"q={q}: {cnt}/{tot} circuits with a flexible line")
        print(f"kappa={k} p={p:4d} inE2={p in E2[k]}  q=1: {len(g1)}/{p-1} flexible ratios;  " + "; ".join(res), flush=True)
