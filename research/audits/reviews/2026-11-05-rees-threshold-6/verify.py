"""Independent checker for refinement-step contractions RC(D; R -> K).  No code shared
with rect*.c.  For every FEASIBLE line it checks: p prime, p = 1 (mod D), g a primitive
root mod p, and for all i in R, j in Z_D the cell v = alpha_j + beta_i satisfies
    (i,j) = (0,0):  v != 0 and v in Q_0;
    otherwise:      v = 0 (only if --zeros) or v in Q_{k-(i+j)} for some k in K,
where v in Q_c  <=>  (v * g^c... ) i.e. (v * g^{-c})^{(p-1)/D} = 1.
For every INFEASIBLE line with p <= --brute it re-decides the prime by an independent
exhaustive search (normal form beta_0 = 0, alpha_0 = 1).  With --cover lo hi mod it lists
every prime p = 1 (mod lcm(D,mod)) in [lo,hi] that has no line, or contradictory lines.
Usage: python verify.py D R K file... [--zeros] [--brute N] [--cover lo hi mod]
"""
import sys, itertools
from sympy import isprime, factorint

def is_primroot(g, p):
    return all(pow(g, (p-1)//q, p) != 1 for q in factorint(p-1))

def in_coset(v, c, g, p, D):
    return pow(v * pow(g, (-c) % (p-1), p) % p, (p-1)//D, p) == 1

def cell_ok(v, i, j, D, K, g, p, zeros):
    if (i, j) == (0, 0):
        return v != 0 and in_coset(v, 0, g, p, D)
    if v == 0:
        return zeros
    return any(in_coset(v, (k - i - j) % D, g, p, D) for k in K)

def brute(p, D, R, K, zeros):
    g = next(x for x in range(2, p) if is_primroot(x, p))
    e = (p-1)//D
    z = pow(g, e, p); tab = {pow(z, t, p): t for t in range(D)}
    ind = [None]*p
    for v in range(1, p): ind[v] = tab[pow(v, e, p)]
    def ok(v, i, j):
        if v == 0: return zeros and (i, j) != (0, 0)
        return any(ind[v] == (k - i - j) % D for k in K) if (i, j) != (0, 0) else ind[v] == 0
    cands = [[b for b in range(p) if ok((1 + b) % p, i, 0)] for i in R[1:]]
    cols = {j: [x for x in range(p) if ok(x, 0, j)] for j in range(1, D)}
    for bs in itertools.product(*cands):
        if len(set(bs)) < len(bs) or 0 in bs: continue
        beta = (0,) + bs
        if all(any(all(ok((x + beta[t]) % p, R[t], j) for t in range(1, len(R))) for x in cols[j]) for j in range(1, D)):
            return True
    return False

def main():
    a = sys.argv[1:]
    D = int(a[0]); R = [int(x) for x in a[1].split(',')]; K = [int(x) for x in a[2].split(',')]
    zeros = '--zeros' in a; brute_lim = 0; cover = None; files = []
    i = 3
    while i < len(a):
        if a[i] == '--zeros': i += 1
        elif a[i] == '--brute': brute_lim = int(a[i+1]); i += 2
        elif a[i] == '--cover': cover = tuple(int(x) for x in a[i+1:i+4]); i += 4
        else: files.append(a[i]); i += 1
    feas, infeas = {}, set(); bad = 0; nchk = 0
    for fn in files:
        for line in open(fn):
            w = line.split()
            if len(w) < 2: continue
            p = int(w[0])
            if w[1] == 'FEASIBLE':
                g = int(w[2].split('=')[1]); bi = w.index('beta'); ai = w.index('alpha')
                beta = [int(x) for x in w[bi+1:ai]]
                alpha = [int(x) for x in w[ai+1:ai+1+D]]
                good = isprime(p) and p % D == 1 and is_primroot(g, p) and len(beta) == len(R)
                good = good and all(cell_ok((alpha[j] + beta[t]) % p, R[t], j, D, K, g, p, zeros)
                                    for t in range(len(R)) for j in range(D))
                nchk += 1
                if good: feas[p] = True
                else: bad += 1; print('BAD', line.strip())
            elif w[1] == 'INFEASIBLE':
                infeas.add(p)
    both = sorted(set(feas) & infeas)
    print(f'D={D} R={R} K={K} zeros={zeros}: checked {nchk} witnesses, bad={bad}, infeasible claims={len(infeas)}, contradictions={both}')
    if brute_lim:
        rech = sorted(q for q in infeas if q <= brute_lim)
        wrong = [q for q in rech if brute(q, D, R, K, zeros)]
        print(f'  brute-force re-decided {len(rech)} INFEASIBLE claims <= {brute_lim}: disagreements={wrong}')
        # also re-decide a few FEASIBLE small primes as a control
        ctrl = sorted(q for q in feas if q <= min(brute_lim, 400))[:8]
        print(f'  control: brute says feasible for {sum(brute(q, D, R, K, zeros) for q in ctrl)}/{len(ctrl)} small feasible primes')
    if cover:
        lo, hi, mod = cover
        from math import lcm
        L = lcm(D, mod); missing = []
        for q in range(lo - (lo - 1) % L + (L if (lo - 1) % L else 0), hi + 1, L):
            if q >= lo and isprime(q) and q not in feas and q not in infeas: missing.append(q)
        print(f'  cover [{lo},{hi}] p=1 mod {L}: missing={missing[:20]}{"..." if len(missing)>20 else ""} (count {len(missing)})')
    print('  exceptional (INFEASIBLE):', sorted(infeas))

main()
