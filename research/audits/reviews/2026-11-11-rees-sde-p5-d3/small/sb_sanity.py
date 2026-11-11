#!/usr/bin/env python3
"""Soundness control for sbsat.build3 (default) and msplit.py (MSPLIT=M0): take checked models of feasible no-S-functional 10-sets (feas.c
'M' lines), apply the GL_3 transform of sbsat.py with a_1, a_2, a_3 = support argmins, re-check the new
model with labelsat.check_model, then fix the build3 CNF's Phi and gamma variables to it by unit clauses
and require CaDiCaL SAT.  usage: sb_sanity.py F_10.txt EVERY WORKDIR"""
import sys, os, itertools, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import labelsat, sbsat, msplit
MS = int(os.environ.get('MSPLIT', '0'))
p = 5
ALL = [a for a in itertools.product(range(p), repeat=3) if any(a)]
REPS = [a for a in ALL if next(x for x in a if x) in (1, 2)]
def pv(s): return [tuple(int(c) for c in w) for w in s.split()]
def neg(v): return tuple((-x) % p for x in v)
fn, every, wd = sys.argv[1], int(sys.argv[2]), sys.argv[3]; ntest = 0
for i, line in enumerate(open(fn)):
    if not line.startswith('M ') or i % every: continue
    parts = line.split('|'); L = pv(parts[0][2:]); Phi = dict(zip(L, pv(parts[1]))); gam = {}
    for a, g in zip(REPS, pv(parts[2])): gam[a] = g; gam[neg(a)] = neg(g)
    if os.environ.get('MINREP'):   # re-choose gamma_alpha (reps; -alpha by (R)) to give a min-support S-rep
        for a in REPS:
            best = None
            for g in itertools.product(range(p), repeat=3):
                v = [(sum(x * f for x, f in zip(a, Phi[l])) + sum(x * c for x, c in zip(g, l))) % p for l in L]
                if all(t in (0, 1, 4) for t in v) and (best is None or sum(1 for t in v if t) < best[0]): best = (sum(1 for t in v if t), g)
            gam[a] = best[1]; gam[neg(a)] = neg(best[1])
        if any(gam[e] != (0, 0, 0) for e in ((1,0,0),(0,1,0),(0,0,1))):   # restore (N): Phi_j := y_{e_j}
            rows0 = [(1,0,0),(0,1,0),(0,0,1)]
            Phi = {l: tuple((Phi[l][j] + sum(x * c for x, c in zip(gam[rows0[j]], l))) % p for j in range(3)) for l in L}
            gam = {al: tuple((gam[al][k] - sum(al[j] * gam[rows0[j]][k] for j in range(3))) % p for k in range(3)) for al in ALL}
        ok, msg = labelsat.check_model(L, Phi, gam, p, 3, (0, 1, 4)); assert ok, msg
    y = {a: tuple((sum(x * f for x, f in zip(a, Phi[l])) + sum(x * c for x, c in zip(gam[a], l))) % p for l in L) for a in ALL}
    sup = lambda a: sum(1 for v in y[a] if v)
    a1 = min(ALL, key=sup)
    a2 = min((a for a in ALL if labelsat.rank([a1, a], p, 3) == 2), key=sup)
    a3 = min((a for a in ALL if labelsat.rank([a1, a2, a], p, 3) == 3), key=sup)
    rows = [a1, a2, a3]
    Phi2 = {l: tuple(y[rows[j]][li] for j in range(3)) for li, l in enumerate(L)}
    gam2 = {}
    for al in ALL:
        At = tuple(sum(al[j] * rows[j][k] for j in range(3)) % p for k in range(3))
        gam2[al] = tuple((gam[At][k] - sum(al[j] * gam[rows[j]][k] for j in range(3))) % p for k in range(3))
    ok, msg = labelsat.check_model(L, Phi2, gam2, p, 3, (0, 1, 4)); assert ok, msg
    assert all(gam2[neg(a)] == neg(gam2[a]) for a in ALL) and all(gam2[e] == (0, 0, 0) for e in ((1,0,0),(0,1,0),(0,0,1)))
    if not MS: nv, cl, info = sbsat.build3(L)
    else:
        m = sup(a1); Ls = sorted(L)
        first = [l for l in Ls if Phi2[l][0]][0]
        if Phi2[first][0] == 4:   # sign normalisation: rows (-a_1, a_2, a_3)
            Phi2 = {l: ((-v[0]) % p, v[1], v[2]) for l, v in Phi2.items()}
            gam2 = {al: gam2[((-al[0]) % p, al[1], al[2])] for al in ALL}
            ok, msg = labelsat.check_model(L, Phi2, gam2, p, 3, (0, 1, 4)); assert ok, msg
        assert Phi2[first][0] == 1 and sum(1 for l in L if Phi2[l][0]) == m
        nv, cl, info, Z = msplit.base(L); cl = cl + msplit.minsupp(info, Z, min(m, MS), len(L))
        if os.environ.get('MINREP'): cl = cl + msplit.minrep_supp(info, min(m, MS), len(L))   # strong clauses at level min(m, M0)
        if m < MS:   # the fixed-Phi_1 case clauses of msplit.py
            for li, l in enumerate(info['L']):
                for k, w in enumerate(info['PHIV']):
                    if w[0] != Phi2[l][0]: cl.append([-info['phi'][li][k]])
    for li, l in enumerate(info['L']): cl.append([info['phi'][li][info['PHIV'].index(Phi2[l])]])
    for ai, a in enumerate(info['reps']): cl.append([info['gam'][ai][info['GAMV'].index(gam2[a])]])
    cnf = os.path.join(wd, 'sanity_%d.cnf' % i); labelsat.write_cnf(cnf, nv, cl)
    r = subprocess.run(['cadical', '-q', cnf], capture_output=True, text=True, timeout=600); os.remove(cnf)
    st = 'SAT' if 's SATISFIABLE' in r.stdout else 'NOT SAT'
    print(i, ' '.join('%d%d%d' % l for l in L), 'supports', sup(a1), sup(a2), sup(a3), st); sys.stdout.flush()
    assert st == 'SAT'; ntest += 1
print('sanity OK on', ntest, 'models')
