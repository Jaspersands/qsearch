"""Independent implementation of the degree/constant recursion of Schedule 1H+ (main-core.tex,
Definition plus-schedule, Lemma plus-exponent), written 2026-11-14 by a referee agent strictly from
the merged text.  No existing schedule script was read or imported.

Data read from artifacts (each item re-checked here before use):
  * RC certificates (certs_stage1.json, v2/certs_tl6_all.json) for availability of the six table
    steps above DFS_TABLE_BOUND and below T_exist (checked against Definition plus-rc);
  * the five l-level tables (Prop. plus-tables), checked against Definition plus-ell with the
    stated storage convention C_y = g^{y_1+...+y_l} B(y).
Everything else (t_{p,kappa}, T_s, Tier-B availability, gaps) is computed here: exhaustive DFS
(rcdfs.c) for p <= DFS_TABLE_BOUND, class sumsets for p < 4 kappa^4.

usage: python plus_mine.py N variant [variant ...]
variants: full, H (Schedule 1H: (a)+plans over (f1) with F0/F1 only), noTL6noE, noS1, d28 (Tier B
only at the 28 primes, no TL6, no (e)), noTB (no (d),(f3), chain finishes).
"""
import sys, json, math, subprocess, os, itertools, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REV = os.path.dirname(HERE)
B38 = os.path.join(REV, '2026-11-13-rees-headline-below-38')
K9 = os.path.join(REV, '2026-11-13-rees-k9-below-21')

DFS_TABLE_BOUND = 600          # text: availability by exhaustive search for p <= 600
TB_BOUND = 523
DFS_CAP = 400_000_000
T_EXIST = {'TL3': 430, 'TL4': 9395, 'TL5': 99745, 'TL6': 837384, 'TW': 1124521, 'U': 1995734}  # recomputed in thresholds.out
TIERB28 = [5, 7, 11, 13, 19, 29, 31, 37, 41, 43, 61, 71, 73, 101, 109, 113, 127, 131, 151, 163, 181,
           199, 271, 307, 379, 433, 487, 523]
FIVE = {(19, 9): ('B4_19.json', 4), (37, 9): ('B4_37.json', 4), (73, 9): ('B4_73.json', 4),
        (13, 4): ('B3_13_4.json', 3), (13, 6): ('B3_13_6.json', 3)}


def sieve(n):
    s = np.ones(n + 1, dtype=bool); s[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]: s[i * i::i] = False
    return np.nonzero(s)[0]


def factor_primes(n):
    fs, d = [], 2
    while d * d <= n:
        if n % d == 0:
            fs.append(d)
            while n % d == 0: n //= d
        d += 1
    if n > 1: fs.append(n)
    return fs


def least_primroot(p):
    if p == 2: return 1
    fs = factor_primes(p - 1)
    g = 2
    while True:
        if all(pow(g, (p - 1) // q, p) != 1 for q in fs): return g
        g += 1


# ---------------------------------------------------------------- per-prime context
class Ctx:
    def __init__(self, p, dfs):
        self.p = p; self.g = least_primroot(p); self.dfs = dfs
        self.dl = None
        self.av = {}
        self.tcache = {}

    def dlog(self):
        if self.dl is None:
            p, g = self.p, self.g
            dl = np.full(p, -1, dtype=np.int64)
            x = 1
            pw = np.empty(p - 1, dtype=np.int64)
            for k in range(p - 1):
                pw[k] = x; x = x * g % p
            dl[pw] = np.arange(p - 1)
            self.dl = dl
        return self.dl

    def cl(self, x, D):
        """cl_D(x) for xi = g, by the power test of the text."""
        p, g = self.p, self.g
        e = (p - 1) // D
        y = pow(x % p, e, p); z = pow(g, e, p)
        acc = 1
        for i in range(D):
            if acc == y: return i
            acc = acc * z % p
        raise ValueError('class not found')


# ---------------------------------------------------------------- sumsets
def class_tables(ctx, kappa, eps):
    """S[delta] = classes of 1+eps*z (z in xi^delta P, 1+eps z != 0); Z[delta] = exists zero."""
    p = ctx.p; dl = ctx.dlog()
    z = np.arange(1, p, dtype=np.int64)
    cz = dl[z] % kappa
    v = (1 + eps * z) % p
    S = [set() for _ in range(kappa)]; Zf = [False] * kappa
    nz = v != 0
    cv = dl[v[nz]] % kappa
    czn = cz[nz]
    for d in range(kappa):
        S[d] = set(np.unique(cv[czn == d]).tolist())
        Zf[d] = bool(np.any((~nz) & (cz == d)))
    return S, Zf


def t_value(ctx, kappa):
    """shortest zero sum of kappa-th powers (least number of nonzero terms), by class sumsets."""
    if kappa == 1: return None
    S, Zf = class_tables(ctx, kappa, 1)
    cur, zero = {0}, False
    for k in range(1, kappa + 2):
        if zero: return k
        new, nz = set(), False
        for a in cur:
            new |= {(a + s) % kappa for s in S[(-a) % kappa]}
            nz |= Zf[(-a) % kappa]
        if zero: new.add(0)
        cur, zero = new, nz
        if zero: return k + 1
    raise RuntimeError('t > kappa+1')


def T_sets(ctx, kappa, m):
    """T_s for s = 0..kappa+1 with eps = -xi^{-m}; returns list of (frozenset classes, zeroflag)."""
    key = (kappa, m)
    if key in ctx.tcache: return ctx.tcache[key]
    p, g = ctx.p, ctx.g
    eps = (-pow(g, (p - 1 - m) % (p - 1), p)) % p
    ce = ctx.cl(eps, kappa)
    S, Zf = class_tables(ctx, kappa, eps)
    T = [(frozenset([0]), False)]
    for j in range(1, kappa + 2):
        A, za = T[-1]
        new = set(A) | {(a + ce) % kappa for a in A}
        nz = za
        for a in A:
            for b in A:
                d = (b - a) % kappa
                new |= {(a + s) % kappa for s in S[d]}
                nz |= Zf[d]
        T.append((frozenset(new), nz))
    ctx.tcache[key] = T
    return T


# ---------------------------------------------------------------- availability
def load_certs():
    d = json.load(open(os.path.join(B38, 'certs_stage1.json')))
    e = json.load(open(os.path.join(B38, 'v2', 'certs_tl6_all.json')))
    certs = {}
    name = {'two-level 3': 'TL3', 'two-level 4': 'TL4', 'two-level 5': 'TL5',
            'tower (9;{0,3,6})': 'TW', 'union (7;Z7->{0,m})': 'U'}
    for k, v in d.items():
        for ps, c in v['found'].items():
            certs.setdefault(name[k], {})[int(ps)] = c
    for ps, c in e['found'].items():
        certs.setdefault('TL6', {})[int(ps)] = c
    return certs


def table_step(D, Delta, Omega):
    Delta, Omega = tuple(sorted(Delta)), tuple(sorted(Omega))
    if Omega == (0,) and Delta == tuple(range(D)) and D in (3, 4, 5, 6): return 'TL%d' % D
    if D == 9 and Delta == (0, 3, 6) and Omega == (0,): return 'TW'
    if D == 7 and Delta == tuple(range(7)) and len(Omega) == 2: return 'U'
    return None


def check_cert(ctx, D, Delta, Omega, alpha, beta):
    p = ctx.p
    if len(alpha) != D or set(beta) != set(Delta): return False
    s00 = (alpha[0] + beta[0]) % p
    if s00 == 0 or ctx.cl(s00, D) != 0: return False
    for i in Delta:
        for j in range(D):
            s = (alpha[j] + beta[i]) % p
            if s == 0: continue
            if (ctx.cl(s, D) + i + j) % D not in Omega: return False
    return True


STATS = {'dfs': 0, 'dfs_none': 0, 'cap': 0, 'cert_ok': 0, 'cert_bad': 0, 'lemma': 0, 'missing': 0}
UNKNOWN = []


def avail(ctx, D, Delta, Omega, certs):
    key = (D, tuple(sorted(Delta)), tuple(sorted(Omega)))
    if key in ctx.av: return ctx.av[key]
    p = ctx.p
    ts = table_step(D, Delta, Omega)
    res = None
    if ts is not None and p >= T_EXIST[ts]:
        res = True; STATS['lemma'] += 1
    elif p <= DFS_TABLE_BOUND or ts is None or (ts is not None and p not in certs.get(ts, {})):
        r = ctx.dfs(p, ctx.g, D, key[1], key[2])
        STATS['dfs'] += 1
        if r == 'CAP':
            STATS['cap'] += 1; UNKNOWN.append((p, key)); res = None
        else:
            res = (r == 'FOUND')
            if not res: STATS['dfs_none'] += 1
        if ts is not None and p > DFS_TABLE_BOUND and p in certs.get(ts, {}):
            pass
    else:
        c = certs[ts][p]
        om = tuple(sorted(c.get('K', [0])))
        if ts == 'U' and om != key[2]:
            # certificate is for another m: decide this m by DFS (capped)
            r = ctx.dfs(p, ctx.g, D, key[1], key[2]); STATS['dfs'] += 1
            if r == 'CAP': STATS['cap'] += 1; UNKNOWN.append((p, key)); res = None
            else: res = (r == 'FOUND')
        else:
            ok = (c['g'] == ctx.g) and check_cert(ctx, D, key[1], key[2], c['alpha'],
                                                  {int(k): v for k, v in c['beta'].items()})
            if ok: STATS['cert_ok'] += 1; res = True
            else:
                STATS['cert_bad'] += 1
                r = ctx.dfs(p, ctx.g, D, key[1], key[2]); STATS['dfs'] += 1
                res = (r == 'FOUND') if r != 'CAP' else None
    ctx.av[key] = res
    if ts is not None:
        TABLE_LOG.setdefault(ts if ts != 'U' else 'U%d' % key[2][1], {})[p] = res
    return res


TABLE_LOG = {}


class DFS:
    def __init__(self):
        self.proc = subprocess.Popen([os.path.join(HERE, 'rcdfs')], stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE, text=True, bufsize=1)
        self.cache = {}

    def __call__(self, p, g, D, Delta, Omega):
        key = (p, D, Delta, Omega)
        if key in self.cache: return self.cache[key]
        self.proc.stdin.write(f"{p} {g} {D} {len(Delta)} {' '.join(map(str, Delta))} {len(Omega)} "
                              f"{' '.join(map(str, Omega))} {DFS_CAP}\n")
        self.proc.stdin.flush()
        line = self.proc.stdout.readline().split()
        if line[0] == 'ERR': raise RuntimeError(' '.join(line))
        self.cache[key] = line[0]
        return line[0]


# ---------------------------------------------------------------- l-level tables
def verify_table(p, kappa, fname, ell):
    g = least_primroot(p)
    raw = json.load(open(os.path.join(K9, fname)))
    C = np.zeros((kappa,) * ell, dtype=np.int64)
    for k, v in raw.items():
        y = tuple(int(ch) for ch in k)
        assert len(y) == ell
        C[y] = pow(g, sum(y), p) * v % p
    # (i) classes of nonzero entries in {0}; (ii) C_0 in P
    h = (p - 1) // kappa
    nz = [int(x) for x in C.flatten() if x]
    ok_i = all(pow(x, h, p) == 1 for x in nz)
    ok_ii = C[(0,) * ell] != 0 and pow(int(C[(0,) * ell]), h, p) == 1
    # (iii) contract each axis with x -> (x_m - z_m x_0)_{m != 0}
    z = np.array([pow(g, m, p) for m in range(kappa)], dtype=np.int64)
    Phi = np.zeros((kappa - 1, kappa), dtype=np.int64)
    for m in range(1, kappa):
        Phi[m - 1, m] = 1; Phi[m - 1, 0] = (-z[m]) % p
    X = C.copy()
    for ax in range(ell):
        X = np.tensordot(Phi, X, axes=([1], [ax])) % p
        X = np.moveaxis(X, 0, ax)
    ok_iii = not X.any()
    # control: reading the stored values as C must fail
    Craw = np.zeros((kappa,) * ell, dtype=np.int64)
    for k, v in raw.items(): Craw[tuple(int(ch) for ch in k)] = v % p
    Xr = Craw.copy()
    for ax in range(ell):
        Xr = np.moveaxis(np.tensordot(Phi, Xr, axes=([1], [ax])) % p, 0, ax)
    return ok_i and ok_ii and ok_iii, (ok_i, bool(ok_ii), ok_iii, 'raw-as-C fails:' + str(bool(Xr.any())))


# ---------------------------------------------------------------- the recursion
def lift(Om, Dp, D):
    return tuple(i for i in range(D) if (i % Dp) in Om)


def subsets_with0(D, maxsize=3):
    out = []
    rest = list(range(1, D))
    for k in range(0, min(maxsize, D) ):
        for c in itertools.combinations(rest, k):
            out.append((0,) + c)
    return out


def chains(ctx, kappa, sol, certs, flags):
    """all chains of (d), aggregated: list of (Omega_L, degree, least constant, a description)."""
    res = {}
    bases = [(1, (0,), 1, 1, 'GE')]
    for D0 in range(2, kappa):
        if kappa % D0 == 0 and D0 in sol:
            bases.append((D0, (0,), sol[D0][0], sol[D0][1], 'H%d' % D0))

    def ext(Dp, Omp, e, K, L, desc):
        for Dt in range(2, kappa + 1):
            if kappa % Dt or Dt % Dp: continue
            if flags.get('strict') and Dt == Dp: continue
            Delta = lift(Omp, Dp, Dt)
            if len(Delta) < 2: continue
            for Om in subsets_with0(Dt, 3):
                a = avail(ctx, Dt, Delta, Om, certs)
                if not a: continue
                nd = desc + ';(%d,%s,%s)' % (Dt, Delta, Om)
                nK = K * (len(Delta) - 1)
                if Dt == kappa:
                    kk = (Om, e + L + 1)
                    if kk not in res or nK < res[kk][0]:
                        res[kk] = (nK, nd)
                if L + 1 < 3:
                    ext(Dt, Om, e, nK, L + 1, nd)
    for (D0, Om0, e0, K0, d0) in bases:
        ext(D0, Om0, e0, K0, 0, d0)
    return [(Om, e, K, d) for (Om, e), (K, d) in res.items()]


def solve_prime(ctx, certs, tables_ok, flags):
    p = ctx.p
    Np = math.gcd(p - 1, 2520)
    kappas = [k for k in range(1, 10) if Np % k == 0]
    sol = {1: (1, 1, 'GE')}
    for kappa in kappas:
        if kappa == 1: continue
        big = p >= 4 * kappa ** 4
        cands = []   # (degree, constant, label)
        # (a) S1
        if flags['S1']:
            if big:
                t = 2 if ((p - 1) // kappa) % 2 == 0 else 3
            else:
                t = t_value(ctx, kappa)
            L = math.ceil(math.log2(t))
            cands.append((kappa * L, kappa ** (kappa * (kappa - 1) * L // 2), 'S1(t=%d)' % t))
        new = flags['new']
        # (b) TL
        if new and kappa in (3, 4, 5, 6) and (kappa != 6 or flags['TL6']):
            if avail(ctx, kappa, tuple(range(kappa)), (0,), certs):
                cands.append((2, kappa - 1, 'TL%d' % kappa))
        # (c) TW
        if new and kappa == 9 and 3 in sol:
            if avail(ctx, 9, (0, 3, 6), (0,), certs):
                cands.append((sol[3][0] + 1, sol[3][1] * 2, 'TW'))
        # (d) Tier B
        tb = new and flags['TB'] and p <= TB_BOUND and (not flags['d28'] or p in TIERB28)
        chs = chains(ctx, kappa, sol, certs, flags) if tb else []
        for (Om, e, K, d) in chs:
            if Om == (0,): cands.append((e, K, 'TB:' + d))
        # (e) l-level
        if new and flags['ELL'] and (p, kappa) in FIVE and tables_ok[(p, kappa)]:
            ell = FIVE[(p, kappa)][1]
            cands.append((ell, (kappa - 1) ** (ell * (ell - 1) // 2), 'L%d' % ell))
        # (f) plans
        nodes = []
        if kappa % 2 == 0:
            nodes.append((kappa // 2, sol[kappa // 2][0], sol[kappa // 2][1], 'H%d' % (kappa // 2)))
        if new and kappa == 7:
            order = list(range(1, 7))
            cu = certs.get('U', {}).get(p)
            if p > DFS_TABLE_BOUND and cu is not None:
                mc = cu['K'][1]; order = [mc] + [m for m in order if m != mc]
            for m in order:
                if avail(ctx, 7, tuple(range(7)), (0, m), certs):
                    nodes.append((m, 2, 6, 'U%d' % m))
                    # above 523 a degree-3 plan is the least possible degree at kappa = 7
                    # (S1 has degree >= 7, every plan over a degree-2 node has degree >= 3);
                    # all U_m nodes have the same degree and constant, so stop at the first m
                    # whose plan (s=1, F1) is admissible.
                    if p > TB_BOUND and (big or all(((u) % 7) in T_sets(ctx, 7, m)[1][0] for u in range(7))):
                        break
        if tb:
            for (Om, e, K, d) in chs:
                if len(Om) == 2: nodes.append((Om[1], e, K, 'TBn:' + d))
        fins = [(None, 0, 1, 'F0'), (tuple(range(kappa)), 1, 1, 'F1')]
        if new and flags['FOM']:
            for Dp in range(2, kappa):
                if kappa % Dp == 0:
                    fins.append((tuple(range(0, kappa, Dp)), sol[Dp][0], sol[Dp][1], 'FH%d' % Dp))
        if tb:
            for (Om, e, K, d) in chs: fins.append((Om, e, K, 'FTB:' + d))
        for (m, eN, KN, dN) in nodes:
            if big:
                cands.append((eN + 1, KN, 'P(%s,1,F1)' % dN))
                continue
            T = T_sets(ctx, kappa, m)
            for s in range(1, kappa + 2):
                cls, z = T[s]
                for (Om, eF, KF, dF) in fins:
                    if Om is None:
                        adm = z
                    else:
                        adm = any(all(((u + k) % kappa) in cls for k in Om) for u in range(kappa))
                    if adm:
                        cands.append((s * eN + eF, KN ** s * KF, 'P(%s,%d,%s)' % (dN, s, dF)))
        if not cands:
            raise RuntimeError('no candidate at p=%d kappa=%d' % (p, kappa))
        e = min(c[0] for c in cands)
        best = [c for c in cands if c[0] == e]
        K = min(c[1] for c in best)
        lab = sorted(best, key=lambda c: (c[1], len(c[2])))[0][2]
        sol[kappa] = (e, K, lab)
    return sol


VARIANTS = {
    'full':     dict(S1=True, new=True, TL6=True, ELL=True, TB=True, FOM=True, d28=False),
    'H':        dict(S1=True, new=False, TL6=False, ELL=False, TB=False, FOM=False, d28=False),
    'noTL6noE': dict(S1=True, new=True, TL6=False, ELL=False, TB=True, FOM=True, d28=False),
    'noS1':     dict(S1=False, new=True, TL6=True, ELL=True, TB=True, FOM=True, d28=False),
    'd28':      dict(S1=True, new=True, TL6=False, ELL=False, TB=True, FOM=True, d28=True),
    'strict':   dict(S1=True, new=True, TL6=True, ELL=True, TB=True, FOM=True, d28=False, strict=True),
    'noTB':     dict(S1=True, new=True, TL6=True, ELL=True, TB=False, FOM=True, d28=False),
}


def cbound(k):
    return k ** (k * (k - 1) * math.ceil(math.log2(k + 1)) // 2)


def main():
    N = int(sys.argv[1]); variants = sys.argv[2:] or ['full']
    t0 = time.time()
    certs = load_certs()
    tables_ok = {}
    for (p, k), (f, ell) in FIVE.items():
        ok, det = verify_table(p, k, f, ell)
        tables_ok[(p, k)] = ok
        print('table', p, k, f, 'ok' if ok else 'FAIL', det, flush=True)
    dfs = DFS()
    primes = [int(q) for q in sieve(N) if q >= 3]
    for var in variants:
        flags = VARIANTS[var]
        best = {c: (0, []) for c in range(2, 10)}
        kbad = []
        profiles = {}
        degs = {}
        for p in primes:
            ctx = Ctx(p, dfs)
            sol = solve_prime(ctx, certs, tables_ok, flags)
            for k, (e, K, lab) in sol.items():
                degs[(p, k)] = (e, lab)
                if k >= 2 and K > cbound(k): kbad.append((p, k, K))
            ev = [sol[math.gcd(d, p - 1)][0] for d in range(2, 10)]
            if p in (13, 19, 37, 43, 73, 127, 181, 631, 2521):
                profiles[p] = (ev, {k: sol[k][2] for k in sol})
            for c in range(2, 10):
                if p <= c: continue
                val = 1 + sum(ev[:c - 1])
                if val > best[c][0]: best[c] = (val, [p])
                elif val == best[c][0]: best[c][1].append(p)
        print('== variant', var, 'N =', N, 'time %.0fs' % (time.time() - t0), flush=True)
        print('E(c), c=2..9:', [best[c][0] for c in range(2, 10)])
        for c in range(2, 10):
            ps = best[c][1]
            print('  c=%d E=%d #attainers=%d first=%s' % (c, best[c][0], len(ps), ps[:12]),
                  ('non-2520 attainers: %s' % [q for q in ps if (q - 1) % 2520] if c == 9 else ''))
        print('  constants K^+ > c_kappa:', kbad[:20], len(kbad))
        for p, (ev, labs) in sorted(profiles.items()):
            print('  profile', p, ev, labs)
        json.dump({'%d,%d' % k: v for k, v in degs.items()}, open(os.path.join(HERE, 'degs_%s_%d.json' % (var, N)), 'w'))
    for ts in sorted(TABLE_LOG):
        d = TABLE_LOG[ts]
        gaps = sorted(q for q, r in d.items() if r is False)
        unk = sorted(q for q, r in d.items() if r is None)
        print('table step %s: queried at %d primes, unavailable at %s, unknown at %s' % (ts, len(d), gaps, unk))
    print('STATS', STATS, 'UNKNOWN', UNKNOWN[:20], len(UNKNOWN))


if __name__ == '__main__':
    main()
