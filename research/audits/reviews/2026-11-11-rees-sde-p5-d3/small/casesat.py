#!/usr/bin/env python3
"""LRAT certificate of infeasibility of a label set L (p = 5, S = {0,+-1}, d = 3) by a case split on the
class s = H Phi_1 in F_5^{n-3}, H = relation map y |-> (y_k - sum_q c_{k,q} y_{piv_q})_{k nonpivot}.

Base CNF = labelsat.encode(L) (with (R), (N); unchanged) + definitional literals
  f[l][v] <-> Phi(l)_1 = v,   sv[j][w] <-> (H Phi_1)_j = w   (forced by pivot/nonpivot values, AMO on sv[j]).
Cases (each: CaDiCaL --lrat=true --binary=false UNSAT, FIXED lrat-check exit 0 + 'c VERIFIED'):
  case C  : H Phi_1 is not a nonzero multiple of any s in STAR   (clauses  OR_j -sv[j][lambda s_j])
  case s  : H Phi_1 = s, for each s in STAR (projective points, first nonzero coordinate 1).
STAR is computed here (numpy, Sigma = H S^L); the certificate does not depend on its correctness: the
cases cover every value of H Phi_1 that is a nonzero multiple of a STAR point, and case C covers the rest.
Exhaustiveness (proof in the note): let (Phi,gamma) be an (R),(N) model and t = H Phi_1.  If t is not a
nonzero multiple of a STAR point the model satisfies case C.  If t = lambda s, s in STAR normalised, the
GL_3 transform (sbsat.py) with A = diag(lambda^{-1},1,1) gives an (R),(N) model with Phi'_1 = y_{lambda^{-1} e1},
whose class is lambda^{-1} t = s (H kills linear functions).  With LEX23=1 a further transform with rows
(e1, a2, a3), a2 = argmin |supp y_alpha| over alpha outside <e1>, a3 = argmin outside <e1,a2>, keeps
y_{e1} (so the case) and gives |supp y_{e2}| <= |supp y_alpha| (alpha outside <e1>) and
|supp y_{e3}| <= |supp y_alpha| (alpha outside <e1,e2>); these support clauses are added.
So all cases UNSAT => no model.
usage: [PROOF_CAP_GB=1] [LEX23=1] [ONLY=s1,s2,...] casesat.py WORKDIR TIMEOUT < oneset.txt
"""
import sys, os, itertools, hashlib, subprocess, time
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import labelsat
CHK = labelsat.LRATCHECK
CAP = int(float(os.environ.get('PROOF_CAP_GB', '1')) * 2**30)
p = 5; SV = (0, 1, 4)

def relations(L):
    n = len(L); piv = []
    for i in range(n):
        if labelsat.rank([L[j] for j in piv] + [L[i]], p, 3) > len(piv): piv.append(i)
        if len(piv) == 3: break
    nonp = [i for i in range(n) if i not in piv]; coef = {}
    for k in nonp:
        for c in itertools.product(range(p), repeat=3):
            if all(sum(c[q] * L[piv[q]][u] for q in range(3)) % p == L[k][u] for u in range(3)): coef[k] = c; break
    return piv, nonp, coef

def star_points(L, piv, nonp, coef):
    n = len(L); r = len(nonp)
    Hm = np.zeros((r, n), dtype=np.int64)
    for j, k in enumerate(nonp):
        Hm[j, k] = 1
        for q in range(3): Hm[j, piv[q]] = (-coef[k][q]) % p
    Y = np.array(list(itertools.product(SV, repeat=n)), dtype=np.int64)
    pw = p ** np.arange(r)
    sig = np.zeros(p ** r, bool); sig[((Y @ Hm.T) % p) @ pw] = True
    out = []
    for v in itertools.product(range(p), repeat=r):
        if any(v) and next(x for x in v if x) == 1:
            if all(sig[int(((lam * np.array(v)) % p) @ pw)] for lam in range(1, p)): out.append(v)
    return out, int(sig.sum())

def base(L):
    nv, cl, info = labelsat.encode(L)
    L = info['L']; n = len(L); PV = info['PHIV']
    nvar = [nv]
    def new():
        nvar[0] += 1; return nvar[0]
    piv, nonp, coef = relations(L)
    f = {}
    for li in range(n):
        for v in SV:
            x = new(); f[li, v] = x; ks = [k for k, w in enumerate(PV) if w[0] == v]
            cl.append([-x] + [info['phi'][li][k] for k in ks])
            for k in ks: cl.append([x, -info['phi'][li][k]])
    sv = {(j, w): new() for j in range(len(nonp)) for w in range(p)}
    for j in range(len(nonp)):
        for w1, w2 in itertools.combinations(range(p), 2): cl.append([-sv[j, w1], -sv[j, w2]])
    for u in itertools.product(SV, repeat=3):
        bs = [-f[piv[q], u[q]] for q in range(3)]
        for j, k in enumerate(nonp):
            for w in SV:
                cl.append(bs + [-f[k, w], sv[j, (w - sum(coef[k][q] * u[q] for q in range(3))) % p]])
    if os.environ.get('LEX23') == '1':
        reps = info['reps']; Z = {}
        for ai in range(len(reps)):
            for li in range(n):
                z = new(); Z[ai, li] = z; A = info['A'][ai, li]; G = info['G'][ai, li]
                for u in range(p):   # z <-> y_alpha(l) = 0
                    cl.append([-z, -A[u], G[(-u) % p]]); cl.append([z, -A[u], -G[(-u) % p]])
        for e, excl in (((0, 1, 0), lambda a: a[1] == 0 and a[2] == 0), ((0, 0, 1), lambda a: a[2] == 0)):
            ej = reps.index(e)
            for t in range(1, n + 1):
                c = new()
                for T in itertools.combinations(range(n), t): cl.append([Z[ej, li] for li in T] + [c])
                for ai, a in enumerate(reps):
                    if excl(a): continue
                    for U in itertools.combinations(range(n), n - t + 1): cl.append([-c] + [-Z[ai, li] for li in U])
    return nvar[0], cl, info, (piv, nonp, coef), sv

def run(cnf, prf, timeout):
    t0 = time.time()
    pr = subprocess.Popen(['cadical', '-q', '--lrat=true', '--binary=false', cnf, prf], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    st = None
    while pr.poll() is None:
        time.sleep(0.05)
        if time.time() - t0 > timeout: st = 'TIMEOUT'
        elif os.path.exists(prf) and os.path.getsize(prf) > CAP: st = 'PROOF_CAP'
        if st: pr.kill(); pr.wait(); break
    if st is None:
        out = pr.stdout.read(); st = 'UNSAT' if 's UNSATISFIABLE' in out else ('SAT' if 's SATISFIABLE' in out else 'ERR')
    pb = os.path.getsize(prf) if os.path.exists(prf) else 0; ver = False
    if st == 'UNSAT':
        c = subprocess.run([CHK, cnf, prf], capture_output=True, text=True)
        ver = c.returncode == 0 and 'c VERIFIED' in c.stdout and 'NOT VERIFIED' not in c.stdout
    for x in (prf,):
        if os.path.exists(x): os.remove(x)
    return st, ver, pb, time.time() - t0

if __name__ == '__main__':
    wd, timeout = sys.argv[1], int(sys.argv[2])
    L = sorted(set(tuple(int(c) for c in w) for w in sys.stdin.read().split('|')[0].split() if len(w) == 3 and w.isdigit()))
    sf = [g for g in itertools.product(range(p), repeat=3) if any(g) and all(sum(a * b for a, b in zip(g, l)) % p in SV for l in L)]
    assert not sf and labelsat.rank(L, p, 3) == 3
    t0 = time.time()
    nv, cl, info, rel, sv = base(L)
    stars, nsig = star_points(L, *rel)
    body = ''.join(' '.join(map(str, c)) + ' 0\n' for c in cl)
    tag = 'cs%d' % os.getpid(); cnf = os.path.join(wd, tag + '.cnf'); prf = os.path.join(wd, tag + '.lrat')
    hb = hashlib.sha256(body.encode()).hexdigest()
    Ls = ' '.join('%d%d%d' % l for l in L)
    print('# set %s  pivots %s  |Sigma| %d  star-projective %d  base clauses %d sha256 %s  checker sha256 %s' % (
        Ls, rel[0], nsig, len(stars), len(cl), hb[:16], hashlib.sha256(open(CHK, 'rb').read()).hexdigest()[:16])); sys.stdout.flush()
    r = len(rel[1])
    cases = [('C', [[-sv[j, (lam * s[j]) % p] for j in range(r)] for s in stars for lam in range(1, p)])]
    cases += [(''.join(map(str, s)), [[sv[j, s[j]]] for j in range(r)]) for s in stars]
    if os.environ.get('ONLY'): cases = [c for c in cases if c[0] in os.environ['ONLY'].split(',')]
    nok = 0; maxpb = 0; tot = 0; bad = []
    agg = hashlib.sha256()
    for name, extra in cases:
        with open(cnf, 'w') as fo:
            fo.write('p cnf %d %d\n' % (nv, len(cl) + len(extra))); fo.write(body)
            fo.write(''.join(' '.join(map(str, c)) + ' 0\n' for c in extra))
        agg.update(open(cnf, 'rb').read())
        st, ver, pb, dt = run(cnf, prf, timeout); tot += dt; maxpb = max(maxpb, pb)
        if st == 'UNSAT' and ver: nok += 1
        else: bad.append((name, st, ver)); print('  case %s: %s verified=%s' % (name, st, ver)); sys.stdout.flush()
        if name == 'C' or os.environ.get('VERBOSE'): print('  case %s: %s verified=%s proof %d %.1fs' % (name, st, ver, pb, dt)); sys.stdout.flush()
    os.remove(cnf)
    print('%s | %s | cases %d verified %d | max proof %d bytes | solve+check %.0fs total %.0fs | all-CNF sha256 %s' % (
        'INFEASIBLE_CERTIFIED' if not bad else 'NOT_CERTIFIED', Ls, len(cases), nok, maxpb, tot, time.time() - t0, agg.hexdigest()[:16]))
