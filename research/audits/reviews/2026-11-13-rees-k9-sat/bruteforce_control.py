#!/opt/anaconda3/bin/python
"""Independent encoding control for sat3.py (finite exact computation).

For tiny (p, k) and every nonempty K in Z_k, decide by brute force whether there are
F1, F2, F3 : Z_k^2 -> F_p with B(i,j,l) = F1(j,l) + F2(i,l) + F3(i,j) in {0} u U_{m in K} Q_{m-i-j-l}
for all (i,j,l) and B(0,0,0) != 0 (Q_m = g^m * (k-th powers), g = least primitive root, computed here
independently of exponents_hcd.py).
  mode 'free'  : all 3 k^2 values free (no gauge fixing)  -- tests the gauge fixing
  mode 'gauge' : F2(0,.) = F3(0,.) = F3(.,0) = 0
Then compares with kissat on the CNF written by sat3.py.
usage: bruteforce_control.py workdir
"""
import sys, itertools, subprocess, os

SAT3 = '/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-12-rees-exponent-k8-attack/sat3.py'


def least_prim_root(p):
    for g in range(2, p):
        if len({pow(g, e, p) for e in range(p - 1)}) == p - 1:
            return g
    return 1  # p = 2 not used


def brute(p, k, K, mode):
    g = least_prim_root(p) if p > 2 else 1
    ind = {pow(g, e, p): e % k for e in range(p - 1)}
    cells = list(itertools.product(range(k), repeat=2))
    keys = [(t, a, b) for t in (1, 2, 3) for a, b in cells]
    if mode == 'gauge':
        fixed = {(2, 0, l) for l in range(k)} | {(3, 0, j) for j in range(k)} | {(3, i, 0) for i in range(k)}
    else:
        fixed = set()
    free = [kk for kk in keys if kk not in fixed]
    allowed = {}
    for i, j, l in itertools.product(range(k), repeat=3):
        A = {x for x in range(1, p) if ind[x] in {(m - i - j - l) % k for m in K}}
        if (i, j, l) != (0, 0, 0):
            A.add(0)
        allowed[(i, j, l)] = A
    for vals in itertools.product(range(p), repeat=len(free)):
        F = dict.fromkeys(fixed, 0)
        F.update(zip(free, vals))
        if all((F[(1, j, l)] + F[(2, i, l)] + F[(3, i, j)]) % p in allowed[(i, j, l)]
               for i, j, l in itertools.product(range(k), repeat=3)):
            return True
    return False


def kissat(p, k, K, work):
    cnf = os.path.join(work, f'ctl_{p}_{k}_{"".join(map(str, K))}.cnf')
    subprocess.run(['nice', '-n', '19', '/opt/anaconda3/bin/python', SAT3, str(p), str(k),
                    ','.join(map(str, K)), cnf], check=True, capture_output=True)
    r = subprocess.run(['nice', '-n', '19', 'kissat', '-q', cnf], capture_output=True, text=True)
    os.remove(cnf)
    return {10: True, 20: False}[r.returncode]


if __name__ == '__main__':
    work = sys.argv[1]
    bad = 0
    for p, k, modes in ((3, 2, ('free', 'gauge')), (5, 2, ('gauge',)), (7, 2, ('gauge',)),
                        (7, 3, ()), (13, 3, ())):
        for r in range(1, k + 1):
            for K in itertools.combinations(range(k), r):
                b = {md: brute(p, k, K, md) for md in modes}
                s = kissat(p, k, K, work)
                agree = all(v == s for v in b.values())
                bad += not agree
                print(f'p={p} k={k} K={K}: brute={b} sat3+kissat={"SAT" if s else "UNSAT"} '
                      f'{"agree" if agree else "DISAGREE"}', flush=True)
    print('controls:', 'ALL AGREE' if bad == 0 else f'{bad} DISAGREEMENTS')
