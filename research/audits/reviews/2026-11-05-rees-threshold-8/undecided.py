"""List primes p = 1 mod k in (lo, hi] not decided by the dfs2/dfs2b outputs and not clique-certified."""
import re, glob, sys
from sympy import primerange
k, lo, hi = map(int, sys.argv[1:4])
dec = set(); fea=set()
for f in glob.glob(f'2026-11-02-rees-schedules/small-prime/*_k{k}*.out'):
    for l in open(f):
        m = re.match(r'(INFEASIBLE|FEASIBLE) k=(\d+) p=(\d+)', l)
        if m and int(m.group(2)) == k: dec.add(int(m.group(3)))
cl = set()
for l in open(f'2026-11-05-rees-threshold-8/clique_k{k}.out'):
    m = re.match(r'CLIQUE k=\d+ p=(\d+).*verified=True', l)
    if m: cl.add(int(m.group(1)))
ps = [p for p in primerange(lo+1, hi+1) if p % k == 1]
und = [p for p in ps if p not in dec and p not in cl]
print(f'k={k} ({lo},{hi}]: {len(ps)} primes, dfs-decided {sum(p in dec for p in ps)}, clique-certified (new) {sum(p in cl and p not in dec for p in ps)}, still undecided {len(und)}')
print(' undecided:', ' '.join(map(str, und)))
