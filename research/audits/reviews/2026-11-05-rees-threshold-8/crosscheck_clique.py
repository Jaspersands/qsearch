"""Independent cross-check of clique.py's CLIQUE/NOCLIQUE verdicts (no shared code).
Plain recursive search over cosets in fixed order 1..k-1, no scaling normalisation, coset
membership by Euler's criterion x^h == zeta^i with zeta = g^h for g = least primitive root.
Usage: python crosscheck_clique.py K PMAX"""
import sys, re
from sympy import primerange, isprime, n_order
K, PMAX = int(sys.argv[1]), int(sys.argv[2])
def least_prim_root(p):
    for g in range(2, p):
        if n_order(g, p) == p - 1: return g
def verdict(p):
    h = (p-1)//K; g = least_prim_root(p); z = pow(g, h, p)
    zi = {pow(z, i, p): i for i in range(K)}
    cls = lambda x: zi[pow(x, h, p)]
    Q = [[x for x in range(1, p) if cls(x) == i] for i in range(K)]
    Q0 = set(Q[0])
    def rec(i, chosen):
        if i == K: return True
        for y in Q[i]:
            if all(((y - c) % p) in Q0 for c in chosen):
                if rec(i+1, chosen + [y]): return True
        return False
    return rec(1, [])
mine = {}
for l in open(f'clique_k{K}.out'):
    m = re.match(r'(CLIQUE|NOCLIQUE) k=\d+ p=(\d+)', l)
    if m: mine[int(m.group(2))] = (m.group(1) == 'CLIQUE')
agree = dis = 0
for p in primerange(3, PMAX+1):
    if p % K != 1 or p not in mine: continue
    v = verdict(p)
    if v == mine[p]: agree += 1
    else: dis += 1; print('DISAGREE', K, p, 'clique.py', mine[p], 'crosscheck', v)
print(f'K={K} p<={PMAX}: agree={agree} disagree={dis}')
