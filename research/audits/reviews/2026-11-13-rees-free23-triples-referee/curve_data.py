"""Level-2 weight variety C = {u in P^5 : K u^3 = 0, E u^2 = 0} for random labels at a given prime.
(AI-written, pending human review.)  K = W+S conditions after eliminating Q3, E = E3; built with the referee's own
public routines (pipeline.Triple), labels only (the W/S/E3 data do not depend on the IS outcomes).
Writes JSON {p, configs: [{K, E, M_ref, labels, rankK, rankE, fit_failures}]}."""
import sys, json, numpy as np
import pipeline as P
from f23 import Label

def build(p, rng, m=6, maxlines=14):
    while True:
        trips = []
        while len(trips) < m:
            labs = [tuple(int(v) for v in rng.integers(0, p, 2)) for _ in range(3)]
            if any(l == (0, 0) for l in labs): continue
            try:
                cps = []
                for l in labs:
                    c = P.Copy(dict(lam=l, L=Label(l, p), y=(0, 0, p - 1), phi=None), p); cps.append(c)
                t = P.Triple(cps, p)
            except AssertionError:
                continue
            if len(t.gen) > maxlines:
                idx = rng.choice(len(t.gen), maxlines, replace=False); t.gen = [t.gen[i] for i in sorted(idx)]
            trips.append(t)
        Mref = trips[0].M.copy()
        AW, AS, E3, fails = [], [], [], 0
        for t in trips:
            t.set_ref(Mref); cW, cS, cE, chk = t.public_W_S_E3()
            fails += chk['fitW'] + chk['fitS'] + chk['fitE3'] + chk['a3_y_e3_ec'] + chk['ec_along']
            AW.append(cW.ravel()); AS.append(cS.ravel()); E3.append(cE.ravel())
        AW = np.array(AW).T % p; AS = np.array(AS).T % p; E3 = np.array(E3).T % p
        A = np.vstack([np.hstack([AW, P.gradQ_form(p, Mref)]), np.hstack([AS, P.dQ_form(p, Mref)])]) % p
        Nl = P.left_null(A[:, m:], p); K = (Nl @ A[:, :m]) % p
        # row-reduce K to a basis
        Kb = []
        for row in K:
            if P.rank_mod(Kb + [list(row)], p) > len(Kb): Kb.append([int(v) for v in row])
        return dict(K=Kb, E=E3.tolist(), labels=[[c.lam for c in t.c] for t in trips], Mref=Mref.tolist(),
                    rankK=len(Kb), rankE=P.rank_mod(E3, p), rankQ=P.rank_mod(A[:, m:], p), fit_failures=int(fails))

if __name__ == '__main__':
    p = int(sys.argv[1]); n = int(sys.argv[2]); seed = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    rng = np.random.default_rng(seed)
    out = dict(p=p, configs=[build(p, rng) for _ in range(n)])
    json.dump(out, open('curve_%d.json' % p, 'w'))
    for c in out['configs']: print({k: c[k] for k in ('rankK', 'rankE', 'rankQ', 'fit_failures')})
