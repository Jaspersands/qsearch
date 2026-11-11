#!/usr/bin/env python3
"""Infeasibility of a label set L by labelsat.encode (R),(N) + a minimum-support case split.
Normal form (proof in the note, small-set section): for any (R),(N) model, the GL_3 transform of sbsat.py
with rows a_1 = an alpha of minimum support m among all y_alpha, a_2 = argmin outside <a_1>,
a_3 = argmin outside <a_1,a_2>, then a sign change a_1 -> -a_1 if needed, gives an (R),(N) model with
  (i) |supp y_alpha| >= m for every alpha, (ii) Phi_1 = y_{e1} has support m and its first nonzero entry
  (in sorted label order) is +1, (iii) |supp y_{e2}| <= |supp y_alpha| for alpha outside <e1>,
  |supp y_{e3}| <= |supp y_alpha| for alpha outside <e1,e2>.
Cases: for m < M0 and every such Phi_1 (C(n,m) 2^(m-1) vectors): (i) + Phi_1 fixed + (iii);
        final case: |supp y_alpha| >= M0 for all alpha + (iii).
Each case: CaDiCaL --lrat=true --binary=false UNSAT, FIXED lrat-check exit 0 and 'c VERIFIED'.
usage: [PROOF_CAP_GB=2] msplit.py WORKDIR TIMEOUT M0 [final|fixed|all] < oneset.txt"""
import sys, os, itertools, hashlib, subprocess, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import labelsat
from crit_lrat import run
p = 5

def base(L):
    nv, cl, info = labelsat.encode(L); n = len(info['L']); reps = info['reps']
    nvar = [nv]
    def new():
        nvar[0] += 1; return nvar[0]
    Z = {}
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
    return nvar[0], cl, info, Z

def minsupp(info, Z, m, n):
    return [[-Z[ai, li] for li in U] for ai in range(len(info['reps'])) for U in itertools.combinations(range(n), n - m + 1)]

def minrep_supp(info, m, n):
    """For every rep alpha and every gamma in F_5^3: the vector <alpha,Phi(l)> + <gamma,l> is not in S^L
    with fewer than m nonzeros (valid in the final case when each gamma_alpha is first chosen to give a
    minimum-support S-representative; see the note)."""
    out = []; S = (0, 1, 4)
    for ai, a in enumerate(info['reps']):
        for g in itertools.product(range(p), repeat=3):
            c = [sum(x * y for x, y in zip(g, l)) % p for l in info['L']]
            for U in itertools.combinations(range(n), n - m + 1):
                cl = [-info['A'][ai, li][(-c[li]) % p] for li in U]
                for li in range(n):
                    if li in U: continue
                    cl += [info['A'][ai, li][u] for u in range(p) if (u + c[li]) % p not in S]
                out.append(cl)
    return out

if __name__ == '__main__':
    wd, timeout, M0 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); which = sys.argv[4] if len(sys.argv) > 4 else 'all'
    L = sorted(set(tuple(int(c) for c in w) for w in sys.stdin.read().split('|')[0].split() if len(w) == 3 and w.isdigit()))
    assert labelsat.rank(L, p, 3) == 3
    assert not [g for g in itertools.product(range(p), repeat=3) if any(g) and all(sum(a * b for a, b in zip(g, l)) % p in (0, 1, 4) for l in L)]
    nv, cl, info, Z = base(L); n = len(L); PV = info['PHIV']
    Ls = ' '.join('%d%d%d' % l for l in info['L'])
    cases = []
    if which in ('all', 'fixed'):
        for m in range(1, M0):
            for T in itertools.combinations(range(n), m):
                for sg in itertools.product((1, 4), repeat=m - 1):
                    vals = dict(zip(T, (1,) + sg)); extra = minsupp(info, Z, m, n)
                    for li in range(n):   # Phi(l)_1 = vals.get(l, 0): forbid the other 18 Phi-values
                        for k, w in enumerate(PV):
                            if w[0] != vals.get(li, 0): extra.append([-info['phi'][li][k]])
                    cases.append(('m%d:%s' % (m, ','.join('%d=%d' % (li, vals[li]) for li in T)), extra))
    if which in ('all', 'final'):
        cases.append(('supp>=%d' % M0, minsupp(info, Z, M0, n)))
    print('# %s | base vars %d clauses %d | cases %d' % (Ls, nv, len(cl), len(cases))); sys.stdout.flush()
    body = ''.join(' '.join(map(str, c)) + ' 0\n' for c in cl)
    tag = 'ms%d' % os.getpid(); cnf = os.path.join(wd, tag + '.cnf'); prf = os.path.join(wd, tag + '.lrat')
    agg = hashlib.sha256(); nok = 0; t0 = time.time(); maxpb = 0
    for name, extra in cases:
        with open(cnf, 'w') as fo:
            fo.write('p cnf %d %d\n' % (nv, len(cl) + len(extra))); fo.write(body); fo.write(''.join(' '.join(map(str, c)) + ' 0\n' for c in extra))
        agg.update(open(cnf, 'rb').read())
        st, ver, pb, dt = run(cnf, prf, timeout); maxpb = max(maxpb, pb); nok += (st == 'UNSAT' and ver)
        print('  case %s: %s verified=%s proof %d %.1fs' % (name, st, ver, pb, dt)); sys.stdout.flush()
    os.remove(cnf)
    print('%s | %s | M0 %d %s | cases %d verified %d | max proof %d | %.0fs | all-CNF sha256 %s' % (
        'INFEASIBLE_CERTIFIED' if nok == len(cases) and which == 'all' else 'PARTIAL', Ls, M0, which, len(cases), nok, maxpb, time.time() - t0, agg.hexdigest()[:16]))
