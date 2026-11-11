#!/usr/bin/env python3
"""Criterion-level LRAT certificate (WEAKER than an LRAT proof of the labelsat CNF): L is infeasible iff
it has no S-functional and Sigma_L = H S^L contains no 3-dim subspace (decision criterion of the note,
proved there; re-derived in the small-set section).  A 3-space V in Sigma has all nonzero points in
STAR = {s != 0 : F_5^* s in Sigma}.  We write V by its reduced row echelon basis s1, s2, s3 in F_5^r
(r = n-3), one CNF per pivot triple c1 < c2 < c3, require each of the 31 projective combinations
a s1 + b s2 + c s3 to avoid every point outside STAR, and prove each CNF UNSAT with CaDiCaL LRAT checked
by the FIXED lrat-check.  Trusted beyond LRAT: the criterion, and the STAR table, which is computed here
by plain enumeration of S^L (3^n vectors) and cross-checked against feas.c's star count.
usage: crit_lrat.py WORKDIR TIMEOUT < oneset.txt"""
import sys, os, itertools, hashlib, subprocess, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import labelsat
from casesat import relations, star_points
CHK = os.path.normpath(labelsat.LRATCHECK); p = 5
CAP = int(float(os.environ.get('PROOF_CAP_GB', '2')) * 2**30)

def run(cnf, prf, timeout):
    t0 = time.time(); out = open(prf + '.out', 'w+')
    pr = subprocess.Popen(['cadical', '-q', '--lrat=true', '--binary=false', cnf, prf], stdout=out, stderr=subprocess.DEVNULL)
    st = None
    while pr.poll() is None:            # wall-clock timeout and proof-size cap (PROOF_CAP_GB, default 2)
        time.sleep(0.05)
        if time.time() - t0 > timeout: st = 'TIMEOUT'
        elif os.path.exists(prf) and os.path.getsize(prf) > CAP: st = 'PROOF_CAP'
        if st: pr.kill(); pr.wait(); break
    out.seek(0); o = out.read(); out.close(); os.remove(prf + '.out')
    if st is None: st = 'UNSAT' if 's UNSATISFIABLE' in o else ('SAT' if 's SATISFIABLE' in o else 'ERR')
    pb = os.path.getsize(prf) if os.path.exists(prf) else 0; ver = False
    if st == 'UNSAT':
        c = subprocess.run([CHK, cnf, prf], capture_output=True, text=True)
        ver = c.returncode == 0 and 'c VERIFIED' in c.stdout and 'NOT VERIFIED' not in c.stdout
    if os.path.exists(prf): os.remove(prf)
    return st, ver, pb, time.time() - t0

if __name__ == '__main__':
    wd, timeout = sys.argv[1], int(sys.argv[2])
    L = sorted(set(tuple(int(c) for c in w) for w in sys.stdin.read().split('|')[0].split() if len(w) == 3 and w.isdigit()))
    assert labelsat.rank(L, p, 3) == 3
    assert not [g for g in itertools.product(range(p), repeat=3) if any(g) and all(sum(a * b for a, b in zip(g, l)) % p in (0, 1, 4) for l in L)]
    rel = relations(L); r = len(rel[1])
    stars, nsig = star_points(L, *rel)
    starset = set()
    for s in stars:
        for lam in range(1, p): starset.add(tuple(lam * x % p for x in s))
    nonstar = [v for v in itertools.product(range(p), repeat=r) if v not in starset]   # includes 0
    combos = [c for c in itertools.product(range(p), repeat=3) if any(c) and next(x for x in c if x) == 1]
    Ls = ' '.join('%d%d%d' % l for l in L)
    print('# %s | |Sigma| %d (incl. 0) | star %d | nonstar %d | checker sha256 %s' % (Ls, nsig, len(starset), len(nonstar),
          hashlib.sha256(open(CHK, 'rb').read()).hexdigest()[:16])); sys.stdout.flush()
    allok = True; t0 = time.time(); agg = hashlib.sha256(); maxpb = 0
    for piv in itertools.combinations(range(r), 3):
        nv = [0]
        def new():
            nv[0] += 1; return nv[0]
        x = {(i, d, v): new() for i in range(3) for d in range(r) for v in range(p)}
        cl = []
        for i in range(3):
            for d in range(r):
                cl.append([x[i, d, v] for v in range(p)])
                for v1, v2 in itertools.combinations(range(p), 2): cl.append([-x[i, d, v1], -x[i, d, v2]])
                fixed = None
                if d in piv: fixed = 1 if piv.index(d) == i else 0
                elif d < piv[i]: fixed = 0
                if fixed is not None: cl.append([x[i, d, fixed]])
        for (a, b, c) in combos:
            w = {(d, v): new() for d in range(r) for v in range(p)}
            for d in range(r):
                for u in itertools.product(range(p), repeat=3):
                    cl.append([-x[0, d, u[0]], -x[1, d, u[1]], -x[2, d, u[2]], w[d, (a * u[0] + b * u[1] + c * u[2]) % p]])
            for v in nonstar: cl.append([-w[d, v[d]] for d in range(r)])
        tag = 'crit%d' % os.getpid(); cnf = os.path.join(wd, tag + '.cnf'); prf = os.path.join(wd, tag + '.lrat')
        labelsat.write_cnf(cnf, nv[0], cl); agg.update(open(cnf, 'rb').read())
        st, ver, pb, dt = run(cnf, prf, timeout); os.remove(cnf); maxpb = max(maxpb, pb)
        print('  pivots %s: %s verified=%s clauses %d proof %d %.1fs' % (piv, st, ver, len(cl), pb, dt)); sys.stdout.flush()
        allok &= (st == 'UNSAT' and ver)
    print('%s | %s | 35 pivot cases | max proof %d | %.0fs | all-CNF sha256 %s' % ('CRITERION_INFEASIBLE_LRAT' if allok else 'NOT_CERTIFIED',
          Ls, maxpb, time.time() - t0, agg.hexdigest()[:16]))
