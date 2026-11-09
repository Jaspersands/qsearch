"""Independent re-decision of dfs2b verdicts for kappa = 10..16 with the threshold-7 checker's
rcdfs.c (R = Z_kappa, K = {0}: exactly the two-level contraction, zeros allowed; written from the
definition, no code shared with dfs2b.c).  rcdfs's own FEASIBLE witnesses are re-checked with pow();
dfs2b's kappa = 10 witnesses are pow-checked separately in lemma5_check.py.
Usage: python xcheck_dfs2b.py K PMAX NODE_LIMIT"""
import sys, re
sys.path.insert(0, '../2026-11-05-rees-threshold-7-check')
from rc import feasible, primitive_root
K, PMAX, LIM = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
dfs = {}
for l in open(f'dfs2b_k{K}.out'):
    m = re.match(r'(INFEASIBLE|FEASIBLE) k=\d+ p=(\d+)', l)
    if m: dfs[int(m.group(2))] = (m.group(1) == 'FEASIBLE')
def powcheck(p, alpha, beta):
    g = primitive_root(p); h = (p-1)//K; zeta = pow(g, h, p)
    for i in range(K):
        for j in range(K):
            c = (alpha[j] + beta[i]) % p
            if c == 0:
                if i == 0 and j == 0: return False
                continue
            if pow(c, h, p) != pow(zeta, (-(i+j)) % K, p): return False
    return True
agree = dis = und = 0
for p in sorted(dfs):
    if p > PMAX: break
    st, a, b, n = feasible(p, K, list(range(K)), [0], limit=LIM)
    if st == -1: und += 1; print('UNDECIDED', K, p, flush=True); continue
    if st == 1:
        bb = [b[i] for i in range(K)]
        ok = powcheck(p, list(a), list(bb))
        if not ok: print('BADWITNESS', K, p, flush=True)
    if (st == 1) == dfs[p]: agree += 1
    else: dis += 1; print('DISAGREE', K, p, 'dfs2b', dfs[p], 'rcdfs', st, flush=True)
print(f'XCHECK K={K} p<={PMAX}: agree={agree} disagree={dis} undecided={und}', flush=True)
