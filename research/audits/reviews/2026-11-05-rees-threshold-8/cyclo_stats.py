"""Do E_2 members have unusual cyclotomic numbers? [computed, exploratory]
For each decided prime p = 1 mod kappa: A(a,b) = #{x in Q_a : x+1 in Q_b}.
Statistics: z00 = (A(0,0) - p/k^2)/sqrt(p); V = sum_{a,b}(A(a,b)-p/k^2)^2/(k^2 p);
T = number of triangles {0,1,x} per p/k^2... (= A(0,0)/(p/k^2)).
Compares members (INFEASIBLE) and non-members in a band around k^((k+1)/2).
Usage: python cyclo_stats.py"""
import re, glob, math
from sympy import primerange, primitive_root
base = '../'
def members_and_decided(k):
    if k == 7:
        mem = set(int(x) for x in open(base+'2026-11-02-rees-threshold-2/E2_k7.txt').read().split())
        dec = set(p for p in primerange(3, 60000) if p % 7 == 1)   # E_2(7) exact (no member above 3221 below T_A)
        return mem, dec
    if k == 6:
        mem, dec = set(), set()
        for l in open(base+'2026-11-02-rees-threshold-2/xval_k6.out'):
            m = re.match(r'(IN)?FEASIBLE k=6 p=(\d+)', l)
            if m:
                dec.add(int(m.group(2)))
                if m.group(1): mem.add(int(m.group(2)))
        return mem, dec
    mem, fea = set(), set()
    for f in glob.glob(base+f'2026-11-02-rees-schedules/small-prime/*_k{k}*.out'):
        for l in open(f):
            m = re.match(r'(INFEASIBLE|FEASIBLE) k=(\d+) p=(\d+)', l)
            if m and int(m.group(2)) == k:
                (mem if m.group(1) == 'INFEASIBLE' else fea).add(int(m.group(3)))
    for l in open(f'clique_k{k}.out'):
        m = re.match(r'CLIQUE k=\d+ p=(\d+).*verified=True', l)
        if m: fea.add(int(m.group(1)))
    assert not (mem & fea), sorted(mem & fea)
    return mem, mem | fea
def stats(p, k):
    g = primitive_root(p); h = (p-1)//k
    ind = [0]*p; x = 1
    for e in range(p-1):
        ind[x] = e % k; x = x*g % p
    A = [[0]*k for _ in range(k)]
    for x in range(1, p-1):
        A[ind[x]][ind[x+1]] += 1
    mu = p/k**2
    z00 = (A[0][0]-mu)/math.sqrt(p)
    V = sum((A[a][b]-mu)**2 for a in range(k) for b in range(k))/(k*k*p)
    return z00, V
for k in (6, 7, 8, 9):
    mem, dec = members_and_decided(k)
    X = k**((k+1)/2)
    lo, hi = 0.3*X, 2.0*X
    band = sorted(p for p in dec if lo <= p <= hi)
    rows = [(p, p in mem) + stats(p, k) for p in band]
    M = [r for r in rows if r[1]]; F = [r for r in rows if not r[1]]
    def mean(L, i): return sum(r[i] for r in L)/len(L) if L else float('nan')
    # rank AUC for z00: probability a random member has smaller z00 than a random non-member
    def auc(i):
        if not M or not F: return float('nan')
        s = sum((m[i] < f[i]) + 0.5*(m[i] == f[i]) for m in M for f in F)
        return s/(len(M)*len(F))
    print(f"k={k} band [{lo:.0f},{hi:.0f}] decided={len(rows)} members={len(M)} "
          f"mean z00: mem {mean(M,2):+.3f} non {mean(F,2):+.3f} AUC(z00 mem<non)={auc(2):.3f} | "
          f"mean V: mem {mean(M,3):.3f} non {mean(F,3):.3f} AUC(V mem<non)={auc(3):.3f}", flush=True)
