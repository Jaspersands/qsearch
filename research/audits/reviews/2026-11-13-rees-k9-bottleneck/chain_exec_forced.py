#!/opt/anaconda3/bin/python
"""Forced full-path test of one-stage R8 plans (finite exact checks; can only falsify).

The stage node usually returns a one-sided relation (an early exit that is itself a solution).  To exercise
Lemma S + Lemma F on every call, groups of fresh random columns are drawn until the stage output is two-sided;
one-sided outputs are verified as solutions and discarded.  The surviving objects are fed to the finish, and
the final x is verified against ALL columns drawn (the discarded columns get weight 0).
Usage: chain_exec_forced.py trials name...
"""
import sys, random
import chain_exec as CE

def forced(p, kap, plan, a, rng, bank):
    g, Lg = CE.dlog(p)
    (_, m, path), fin = plan
    node = CE.Chain(p, kap, path)
    A = node.arity(a)
    zm = pow(g, m, p); izm = CE.inv(zm, p); eps = (-izm) % p
    fnode = None if fin[0] in ('F0', 'F1') else CE.Chain(p, kap, fin[-1])
    need = (a + 1) if fin[0] == 'F1' else fnode.arity(a)
    lams, objs, onesided = [], [], 0
    tries = 0
    while len(objs) < need:
        tries += 1
        assert tries < 5000, 'too many one-sided stage outputs'
        base = len(lams)
        grp = bank(A)
        lams += grp
        x = node(grp, a)
        I = [n for n in range(A) if x[n] and Lg[x[n]] % kap == 0]
        J = [n for n in range(A) if x[n] and Lg[x[n]] % kap == m]
        assert len(I) + len(J) == sum(1 for y in x if y)
        if not I or not J:
            sol = [0] * len(lams)
            for n in I: sol[base + n] = x[n]
            for n in J: sol[base + n] = x[n] * izm % p
            assert CE.verify(sol, lams, p, kap, a); onesided += 1
            continue
        u = [0] * a
        for n in I: u = [(y + x[n] * q) % p for y, q in zip(u, grp[n])]
        r1 = {base + n: x[n] for n in I}
        r2 = {base + n: x[n] * izm % p for n in J}
        # check the object: value(r1) = u, value(r2) = eps*u
        assert CE.lin(r1, lams, p, a) == u and CE.lin(r2, lams, p, a) == [eps * y % p for y in u]
        objs.append((u, [(1, r1), (eps, r2)]))
    Pv = [y for y in range(1, p) if Lg[y] % kap == 0]
    tab = {}
    for y1 in [0] + Pv:
        for y2 in [0] + Pv:
            if y1 or y2: tab.setdefault((y1 + eps * y2) % p, (y1, y2))
    vec = [o[0] for o in objs]
    if fin[0] == 'F1':
        eta = CE.rref_null(vec, a, p)
    else:
        eta = fnode(vec, a)
    rho = next((pow(g, c, p) for c in range(kap) if all(not e or pow(g, c, p) * e % p in tab for e in eta)), None)
    assert rho is not None, 'finish class condition fails'
    x = [0] * len(lams)
    for n, e in enumerate(eta):
        if e:
            y = tab[rho * e % p]
            for yk, (r, d) in zip(y, objs[n][1]):
                if yk:
                    for col, cc in d.items(): x[col] = yk * cc % p
    return CE.verify(x, lams, p, kap, a), onesided, len(lams)

if __name__ == '__main__':
    trials = int(sys.argv[1]); rng = random.Random(77)
    for nm in sys.argv[2:]:
        p, kap, plan = CE.PLANS[nm]
        g = CE.prim_root(p)
        for a in (1, 2, 3):
            banks = {'uniform': lambda n: [[rng.randrange(p) for _ in range(a)] for _ in range(n)],
                     'sparse-coset': lambda n: [[pow(g, rng.randrange(p - 1), p) * (i == rng.randrange(a)) for i in range(a)] for _ in range(n)],
                     'two-dim-span': lambda n: (lambda W: [[(rng.randrange(p) * W[0][i] + rng.randrange(p) * W[1][i]) % p for i in range(a)] for _ in range(n)])([[rng.randrange(p) for _ in range(a)] for _ in range(2)])}
            for bn, bank in banks.items():
                good = tot = one = cols = 0
                for _ in range(trials):
                    ok, o, nc = forced(p, kap, plan, a, rng, bank)
                    good += ok; tot += 1; one += o; cols += nc
                print(f'{nm} a={a} bank={bn}: {good}/{tot} full-path runs verified (one-sided stage outputs verified and discarded: {one}; columns drawn {cols})', flush=True)
