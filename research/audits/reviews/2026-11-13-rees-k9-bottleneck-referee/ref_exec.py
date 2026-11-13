#!/opt/anaconda3/bin/python
"""Referee's independent executor (finite checks; can only falsify).  Written from the proof of thm:app-s2-chain
(procedures P_t: rounds, back-substitution, subspaces) and Lemmas S, F of 2026-11-12-rees-exponent-k8-attack sec. 2.
RC witnesses come from the referee's own solver (ref_common.rc_search), not from the report.
Every chain call asserts: value in U, every nonzero weight of D_t-class in K_t, designated weight 1.
Every stage asserts each rep's value (c_k u, resp. eps c_k u).  Final output: weights in P_kappa, nonempty,
sum x_b lambda_b = 0.
usage: ref_exec.py TRIALS [neg]
"""
import sys, random, math, itertools
from ref_common import rc_search, dlog, rc_check


class Sub:
    def __init__(self, a, p, basis=()):
        self.a, self.p, self.B = a, p, []
        for v in basis:
            self.add(v)

    def copy(self):
        s = Sub(self.a, self.p)
        s.B = list(self.B)
        return s

    def reduce(self, v):
        p = self.p
        v = list(v)
        for piv, b in self.B:
            if v[piv]:
                f = v[piv]
                v = [(x - f * y) % p for x, y in zip(v, b)]
        return v

    def contains(self, v):
        return not any(self.reduce(v))

    def add(self, v):
        r = self.reduce(v)
        if any(r):
            piv = next(i for i, x in enumerate(r) if x)
            inv = pow(r[piv], self.p - 2, self.p)
            self.B.append((piv, [x * inv % self.p for x in r]))
            return True
        return False

    def codim(self):
        return self.a - len(self.B)


def lin(vecs, w, p, a):
    s = [0] * a
    for b, c in w.items():
        if c:
            s = [(x + c * y) % p for x, y in zip(s, vecs[b])]
    return s


class Fresh:
    def __init__(self, idx):
        self.idx = list(idx)
        self.pos = 0

    def take(self, n):
        if self.pos + n > len(self.idx):
            raise RuntimeError('out of columns')
        out = self.idx[self.pos:self.pos + n]
        self.pos += n
        return out


def P0(U, vecs, fresh, p, a):
    m = U.codim()
    cols = fresh.take(m + 1)
    rows = []  # (pivot, reduced vec, combination)
    for b in cols:
        v = U.reduce(vecs[b])
        comb = {b: 1}
        for piv, rv, rc in rows:
            if v[piv]:
                f = v[piv]
                v = [(x - f * y) % p for x, y in zip(v, rv)]
                for bb, cc in rc.items():
                    comb[bb] = (comb.get(bb, 0) - f * cc) % p
        if not any(v):
            comb = {bb: cc for bb, cc in comb.items() if cc}
            bstar = min(comb)
            inv = pow(comb[bstar], p - 2, p)
            w = {bb: cc * inv % p for bb, cc in comb.items()}
            assert U.contains(lin(vecs, w, p, a))
            return w, bstar
        piv = next(i for i, x in enumerate(v) if x)
        inv = pow(v[piv], p - 2, p)
        rows.append((piv, [x * inv % p for x in v], {bb: cc * inv % p for bb, cc in comb.items()}))
    raise AssertionError('no dependence among m+1 columns')


def Pt(t, steps, U, vecs, fresh, p, a):
    """steps[t-1] = (D, K, alpha, beta)."""
    if t == 0:
        return P0(U, vecs, fresh, p, a)
    D, K, al, be = steps[t - 1]
    g, L = dlog(p)
    V = U.copy()
    rounds = []
    while True:
        c, bst = Pt(t - 1, steps, V, vecs, fresh, p, a)
        e = lin(vecs, c, p, a)
        ib = {b: L[w] % D for b, w in c.items()}
        assert all(i in be for i in ib.values()), 'chain condition violated'
        v = lin(vecs, {b: be[ib[b]] * w % p for b, w in c.items()}, p, a)
        rounds.append((c, bst, e, v, ib, V.copy()))
        if V.contains(v):
            break
        V.add(v)
    c, bst, e, v, ib, Vk = rounds[-1]
    W = {}
    for b, w in c.items():
        x = w * (al[0] + be[ib[b]]) % p
        if x:
            W[b] = x
    rho = [(x + y) % p for x, y in zip(e, v)]
    tau = [(-x) % p for x in rho]
    for k in range(len(rounds) - 2, -1, -1):
        c, _, e, v, ib, Vk = rounds[k]
        rt, rv = Vk.reduce(tau), Vk.reduce(v)
        piv = next(i for i, x in enumerate(rv) if x)
        gam = rt[piv] * pow(rv[piv], p - 2, p) % p
        assert all((x - gam * y) % p == 0 for x, y in zip(rt, rv)), 'tau not in V_k + F v_k'
        if gam:
            n = L[gam] % D
            for b, w in c.items():
                x = gam * w * (al[n] + be[ib[b]]) % p
                if x:
                    assert b not in W
                    W[b] = x
            tau = [(tt - gam * (al[n] * x + y)) % p for tt, x, y in zip(tau, e, v)]
        assert Vk.contains(tau)
    # checks of the induction claim C(t)
    assert U.contains(lin(vecs, W, p, a)), 'value not in U'
    assert all((L[x] % D) in K for x in W.values()), 'class outside K_t'
    bstar = rounds[-1][1]
    assert W.get(bstar) == 1, 'designated weight != 1'
    return W, bstar


def chain_node(steps, vecs, idx, p, a):
    U = Sub(a, p)
    W, _ = Pt(len(steps), steps, U, vecs, Fresh(idx), p, a)
    assert not any(lin(vecs, W, p, a))
    return W


def witnesses(p, path, perturb=False):
    """path: [(D_1,K_1),...]; returns steps with the referee's own RC witnesses."""
    steps, prevD, prevK = [], 1, (0,)
    for (D, K) in path:
        R = tuple(x for x in range(D) if x % prevD in prevK)
        st, al, be = rc_search(p, D, R, K)
        assert st == 1, ('no witness', p, D, R, K)
        if perturb and D == 9 and len(R) == 3:
            al = list(al); al[2] = (al[2] + 1) % p
        steps.append((D, set(K), al, be))
        prevD, prevK = D, K
    return steps


def binom(n, k):
    return math.comb(n, k)


def bank(kind, n, p, a, rng):
    if kind == 'uniform':
        return [[rng.randrange(p) for _ in range(a)] for _ in range(n)]
    if kind == 'repeat':   # few distinct directions, each repeated with scalar multiples
        base = [[rng.randrange(p) for _ in range(a)] for _ in range(a + 1)]
        return [[rng.randrange(1, p) * x % p for x in rng.choice(base)] for _ in range(n)]
    if kind == 'lowrank':  # columns in a random line plus occasional generic column
        w = [rng.randrange(1, p) for _ in range(a)]
        return [([rng.randrange(1, p) * x % p for x in w] if rng.random() < .7 else
                 [rng.randrange(p) for _ in range(a)]) for _ in range(n)]


def run_plan(p, kap, stage, finish, a, rng, kind, forced, neg=None):
    """stage = (m, path) or None; finish = path of a K-node (kappa-classes in lift) or None (direct {0}-node)."""
    g, L = dlog(p)
    P = {x for x in range(1, p) if L[x] % kap == 0}
    if stage is None:
        steps = witnesses(p, finish)
        Ls = len(steps)
        n = binom(a + Ls + 1, Ls + 1)
        vecs = bank(kind, n, p, a, rng)
        W = chain_node(steps, vecs, range(n), p, a)
        return W, vecs, 'direct'
    m, spath = stage
    st_steps = witnesses(p, spath, perturb=(neg == 'perturb'))
    m_decl = 5 if neg == 'wrongm' else m
    fsteps = witnesses(p, finish)
    N1 = binom(a + len(st_steps) + 1, len(st_steps) + 1)
    Nf = binom(a + len(fsteps) + 1, len(fsteps) + 1)
    eps = (-pow(pow(g, m_decl, p), p - 2, p)) % p
    allvecs, objs, exits, onesided = [], [], [], 0
    gm_inv = pow(pow(g, m_decl, p), p - 2, p)
    groups = 0
    while len(objs) < Nf:
        groups += 1
        if groups > 3000:
            return None, allvecs, 'GROUP-CAP (full path not reached)'
        base = len(allvecs)
        allvecs += bank(kind, N1, p, a, rng)
        x = chain_node(st_steps, allvecs, range(base, base + N1), p, a)
        I = {b: w for b, w in x.items() if L[w] % kap == 0}
        J = {b: w * gm_inv % p for b, w in x.items() if L[w] % kap == m_decl % kap}
        assert len(I) + len(J) == len(x), 'stage output class outside {0,m}'
        if not J or not I:
            sol = I if I else J
            onesided += 1
            if not forced:
                return sol, allvecs, 'stage-onesided'
            assert verify(sol, allvecs, p, kap, a, P)
            continue
        u = lin(allvecs, I, p, a)
        if not any(u):   # I alone is a solution
            onesided += 1
            if not forced:
                return I, allvecs, 'zero-object'
            continue
        reps = [dict(I), dict(J)]
        types = [1, eps]
        for rep, cc in zip(reps, types):
            assert lin(allvecs, rep, p, a) == [cc * y % p for y in u], 'rep value wrong'
        objs.append((u, reps, types))
    # finish: K-node on the objects' vectors
    ovecs = [o[0] for o in objs]
    y = chain_node(fsteps, ovecs, range(len(ovecs)), p, a)
    types = objs[0][2]
    Tn = {}
    for ys in itertools.product(sorted(P | {0}), repeat=len(types)):
        if any(ys):
            Tn.setdefault(sum(yy * cc for yy, cc in zip(ys, types)) % p, ys)
    C = {L[v] % kap for v in Tn if v}
    Kcls = {L[w] % kap for w in y.values()}
    rho = None
    for c in range(kap):
        if {(k + c) % kap for k in Kcls} <= C:
            rho = pow(g, c, p)
            break
    assert rho is not None, 'finish classes not in Tn'
    sol = {}
    for nu, xv in y.items():
        ys = Tn[rho * xv % p]
        for yy, rep in zip(ys, objs[nu][1]):
            if yy:
                for b, w in rep.items():
                    assert b not in sol
                    sol[b] = yy * w % p
    return sol, allvecs, ('finish', onesided)


def verify(sol, vecs, p, kap, a, P):
    return bool(sol) and all(w in P for w in sol.values()) and not any(lin(vecs, sol, p, a))


PLANS = {
    'p37': (37, 9, (4, [(3, (0,)), (9, (0, 4))]), [(9, (0, 2, 5))]),
    'p73': (73, 9, (1, [(3, (0,)), (9, (0, 1))]), [(3, (0,))]),
    'p19': (19, 9, (1, [(3, (0,)), (9, (0, 1))]), [(9, (0, 1, 4, 7)), (9, (0, 3, 8))]),
    'p127': (127, 9, None, [(3, (0,)), (9, (0, 3)), (9, (0,))]),
    'p181': (181, 9, None, [(3, (0,)), (9, (0, 1)), (9, (0,))]),
}

if __name__ == '__main__':
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    neg = sys.argv[2] if len(sys.argv) > 2 else None
    rng = random.Random(20261113)
    tot = ok = 0
    for name, (p, kap, stage, finish) in PLANS.items():
        if neg and name not in ('p37',):
            continue
        g, L = dlog(p)
        P = {x for x in range(1, p) if L[x] % kap == 0}
        for a in (1, 2, 3):
            for kind in ('uniform', 'repeat', 'lowrank'):
                for forced in ((False, True) if stage else (False,)):
                    good = ran = capped = 0
                    exits = {}
                    for t in range(trials):
                        try:
                            sol, vecs, ex = run_plan(p, kap, stage, finish, a, rng, kind, forced, neg)
                            v = None if sol is None else verify(sol, vecs, p, kap, a, P)
                        except AssertionError as e:
                            v, ex = False, 'ASSERT:' + str(e)
                        if v is None:
                            capped += 1
                        else:
                            good += v
                            ran += 1
                        k = ex if isinstance(ex, str) else ex[0]
                        exits[k] = exits.get(k, 0) + 1
                    tot += ran
                    ok += good
                    print(f'{name} a={a} {kind:8s} forced={forced!s:5s}: {good}/{ran} verified'
                          f'{f" ({capped} capped, no output)" if capped else ""}; exits {exits}', flush=True)
    print(f'TOTAL {ok}/{tot}' + (f'   (negative control {neg}: expect failures)' if neg else ''))
