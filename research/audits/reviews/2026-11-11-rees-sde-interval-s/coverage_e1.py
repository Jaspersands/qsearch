"""Coverage check for the e1-line-data case split (2026-11-11-rees-sde-interval-s.md, section 3).

(a) Recompute the admissible e1 line data A by a third method (v ranges over T* - u), independently of
    linedata.py.
(b) Implement the two symmetry families on FULL P-equivariant normalised solutions (Phi, gamma):
      label side  sigma(a,b) = (lam a, mu b + nu a):  Phi'(l) = Phi(sigma l),  gamma'_alpha = sigma^T gamma_alpha;
      alpha side  A in GL_2:  y'_alpha = y_{A alpha},  Phi' = (y_{A e1}, y_{A e2}),
                  gamma'_alpha = gamma_{A alpha} - alpha_1 gamma_{A e1} - alpha_2 gamma_{A e2}.
    Check on SAT models of smaller cells (p = 5 {0,+-1}, p = 7 {0,+-1,+-2}, nested) that random group
    elements map solutions to solutions (int_cnf.check_solution, which also checks normalisation and
    nondegeneracy), and that the images stay P-equivariant.
(c) Coverage: starting from the case representatives read from the case file, close under the
    generators sigma in {(g,1,0), (1,g,0), (1,1,1)} and A = diag(g,1) (g a primitive root), acting on e1
    line data THROUGH the lifted actions of (b) (embed the data in a full gamma, act, read the e1 data
    back).  Every element of A must be reached, and nothing outside A.
usage: coverage_e1.py p K casefile
"""
import sys, os, itertools, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import int_cnf as IC
import pycosat


def mul(q, Ab, x): return ((Ab[0][0] * x[0] + Ab[0][1] * x[1]) % q, (Ab[1][0] * x[0] + Ab[1][1] * x[1]) % q)


def act_label(q, sig, Phi, gamma):
    lam, mu, nu = sig
    s = lambda l: ((lam * l[0]) % q, (mu * l[1] + nu * l[0]) % q)
    Phi2 = {l: Phi[s(l)] for l in Phi} if Phi is not None else None
    gamma2 = {a: ((lam * g[0] + nu * g[1]) % q, (mu * g[1]) % q) for a, g in gamma.items()}
    return Phi2, gamma2


def act_alpha(q, Ab, Phi, gamma):
    e1, e2 = mul(q, Ab, (1, 0)), mul(q, Ab, (0, 1))
    Phi2 = None
    if Phi is not None:
        def y(a, l):
            g = gamma[a]; return (a[0] * Phi[l][0] + a[1] * Phi[l][1] + g[0] * l[0] + g[1] * l[1]) % q
        Phi2 = {l: (y(e1, l), y(e2, l)) for l in Phi}
    gamma2 = {}
    for a in gamma:
        Aa = mul(q, Ab, a)
        gamma2[a] = tuple((gamma[Aa][i] - a[0] * gamma[e1][i] - a[1] * gamma[e2][i]) % q for i in range(2))
    return Phi2, gamma2


def equivariant(q, Phi, gamma):
    return all(Phi[((q - l[0]) % q, (q - l[1]) % q)] == ((q - Phi[l][0]) % q, (q - Phi[l][1]) % q) for l in Phi) and \
        all(gamma[((q - a[0]) % q, (q - a[1]) % q)] == ((q - g[0]) % q, (q - g[1]) % q) for a, g in gamma.items())


def main():
    p, K, casefile = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    S = sorted({x % p for x in range(-K, K + 1)})
    m = (p - 1) // 2; R = list(range(2, m + 1)); n = len(R)
    rng = random.Random(7)
    # (a)
    if len(S) ** n <= 500000:
        T = set()
        for f in S:
            for t in itertools.product(*[[(s - r * f) % p for s in S] for r in R]): T.add(t)
        Ts = {t for t in T if all(tuple((a * x) % p for x in t) in T for a in range(1, p))}
    else:
        Sset = set(S)
        tables = []
        for r in R:
            per_val = []
            for val in range(p):
                amasks = []
                for a in range(1, m + 1):
                    bm = 0
                    for fi, f in enumerate(S):
                        if (a * val + r * f) % p in Sset:
                            bm |= 1 << fi
                    amasks.append(bm)
                per_val.append(tuple(amasks))
            tables.append(per_val)
        proj_pts = []
        for idx0 in range(n):
            ms = list(tables[idx0][1])
            for j in range(idx0):
                zm = tables[j][0]
                ms = [ms[a] & zm[a] for a in range(m)]
            if any(x == 0 for x in ms): continue
            states = [((0,) * idx0 + (1,), tuple(ms))]
            for idx in range(idx0 + 1, n):
                tbl = tables[idx]; nxt = []
                for pref, cur_ms in states:
                    for val in range(p):
                        vm = tbl[val]; new_ms = []; ok = True
                        for a in range(m):
                            nm = cur_ms[a] & vm[a]
                            if nm == 0: ok = False; break
                            new_ms.append(nm)
                        if ok: nxt.append((pref + (val,), tuple(new_ms)))
                states = nxt
            for pref, _ in states: proj_pts.append(pref)
        Ts = {(0,) * n}
        for q in proj_pts:
            for c in range(1, p): Ts.add(tuple((c * x) % p for x in q))
    A = set()
    for u in Ts:
        for t in Ts:
            v = tuple((t[i] - u[i]) % p for i in range(n))
            if all(tuple((u[i] + b * v[i]) % p for i in range(n)) in Ts for b in range(p)) and (any(u) or any(v)):
                A.add((u, v))
    print(f'(a) p={p} S={S}: |T*| = {len(Ts)}, admissible e1 data |A| = {len(A)}', flush=True)
    # (b)
    for q, Sq in ((5, [0, 1, 4]), (7, [0, 1, 2, 5, 6])):
        Lq = IC.parse_L(q, 2, 'nest')
        _, cl, meta = IC.build(q, Sq, 2, Lq, 'equi')
        nmod = nimg = 0
        for sol in itertools.islice(pycosat.itersolve(cl), 0, 400, 20):
            Phi, gamma = IC.decode(q, Sq, 2, Lq, 'equi', meta, {v for v in sol if v > 0})
            assert IC.check_solution(q, Sq, 2, Lq, Phi, gamma)[0]
            nmod += 1
            for _ in range(10):
                sig = (rng.randrange(1, q), rng.randrange(1, q), rng.randrange(q))
                while True:
                    Ab = ((rng.randrange(q), rng.randrange(q)), (rng.randrange(q), rng.randrange(q)))
                    if (Ab[0][0] * Ab[1][1] - Ab[0][1] * Ab[1][0]) % q: break
                for P2, g2 in (act_label(q, sig, Phi, gamma), act_alpha(q, Ab, Phi, gamma),
                               act_alpha(q, Ab, *act_label(q, sig, Phi, gamma))):
                    ok, why = IC.check_solution(q, Sq, 2, Lq, P2, g2)
                    assert ok and equivariant(q, P2, g2), (q, sig, Ab, why)
                    nimg += 1
        print(f'(b) p={q} S={Sq}: {nmod} SAT models, {nimg} images under random symmetries, all solutions', flush=True)
    # (c)
    def prim(q):
        return next(g for g in range(2, q) if len({pow(g, e, q) for e in range(q - 1)}) == q - 1)
    g0 = prim(p)
    alphas = [a for a in itertools.product(range(p), repeat=2) if any(a)]
    def embed(uv):
        u, v = uv
        c = {1: (0, 0), p - 1: (0, 0)}
        for i, r in enumerate(R):
            c[r] = (u[i], v[i]); c[p - r] = ((-u[i]) % p, (-v[i]) % p)
        gamma = {}
        for a in alphas:
            if a[1] == 0: gamma[a] = c[a[0]]
            else: gamma[a] = (rng.randrange(p), rng.randrange(p))   # other directions: arbitrary
        gamma[(0, 1)] = (0, 0)
        for a in alphas:   # make it P-equivariant
            na = ((p - a[0]) % p, (p - a[1]) % p)
            if a[1] != 0 and a < na: gamma[na] = ((-gamma[a][0]) % p, (-gamma[a][1]) % p)
        return gamma
    def read(gamma):
        return (tuple(gamma[(r, 0)][0] for r in R), tuple(gamma[(r, 0)][1] for r in R))
    gens = [lambda g: act_label(p, (g0, 1, 0), None, g)[1], lambda g: act_label(p, (1, g0, 0), None, g)[1],
            lambda g: act_label(p, (1, 1, 1), None, g)[1], lambda g: act_alpha(p, ((g0, 0), (0, 1)), None, g)[1]]
    reps = []
    for line in open(casefile):
        fx = IC.parse_fix(line.strip())
        assert set(fx) == {((1, 0), r) for r in R}, line
        reps.append((tuple(fx[((1, 0), r)][0] for r in R), tuple(fx[((1, 0), r)][1] for r in R)))
    assert all(r in A for r in reps), 'a case representative is not admissible'
    reached = set(reps); stack = list(reps); outside = 0
    while stack:
        x = stack.pop()
        for G in gens:
            y = read(G(embed(x)))
            if y not in A: outside += 1
            if y not in reached: reached.add(y); stack.append(y)
    print(f'(c) {len(reps)} case representatives ({len(set(reps))} distinct); closure under the lifted generators '
          f'has {len(reached)} elements; |A| = {len(A)}; outside A: {outside}; missing from A: {len(A - reached)}')
    print('COVERAGE OK' if reached == A and outside == 0 else 'COVERAGE FAILED')


main()
