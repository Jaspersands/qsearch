"""Hostile-referee independent recomputation (2026-11-14) of Schedule 1H+ with candidate (a) (S1)
deleted at every degree, written from the text of main-core.tex Sec. 5.2 (sec:plus) only.
Shares no code with isfree_check.py, plus_mine.py, run2.py or any earlier script.

Data reused (definitions' data only, each entry RE-VERIFIED here against Def. plus-rc / plus-ell):
  certs_stage1.json, tierB_witnesses.json      (2026-11-13-rees-headline-below-38/)
  v2/certs_tl6_all.json                         (same folder)
  B4_19/B4_37/B4_73/B3_13_4/B3_13_6.json        (2026-11-13-rees-k9-below-21/)
Availability is UNDER-approximated: a step counts as available iff p >= T_exist (Lemma plus-sm(i),
table thresholds re-checked below) or a stored contraction passes the check here. A step without a
verified certificate is treated as unavailable. Under-approximating availability can only raise every
IS-free arity (all candidate arities are monotone in the inner arities), so any dominance found here
holds for the true schedule; degree agreement with the authors' dump then also tests their negatives
indirectly (a missing certificate on a step they used would show as a higher degree here).

Usage: python indep_isfree.py N   (all primes 3 <= p < N)
"""
import sys, os, json, math, time
from math import gcd
import numpy as np

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # research/audits/reviews
HB = os.path.join(R, '2026-11-13-rees-headline-below-38')
K9 = os.path.join(R, '2026-11-13-rees-k9-below-21')

def primes_below(N):
    s = bytearray([1]) * N; s[0:2] = b'\x00\x00'
    for i in range(2, int(N ** 0.5) + 1):
        if s[i]: s[i * i::i] = bytearray(len(range(i * i, N, i)))
    return [i for i in range(3, N) if s[i]]

def prime_factors(n):
    f, d = [], 2
    while d * d <= n:
        if n % d == 0:
            f.append(d)
            while n % d == 0: n //= d
        d += 1
    if n > 1: f.append(n)
    return f

def least_prim_root(p):
    qs = prime_factors(p - 1)
    g = 2
    while True:
        if all(pow(g, (p - 1) // q, p) != 1 for q in qs): return g
        g += 1

def f2(x): return x * (x - 1) // 2

class Cls:
    """D-class of x w.r.t. generator g: i with x in g^i P_D, via x^((p-1)/D)."""
    def __init__(self, p, g):
        self.p, self.g, self.cache = p, g, {}
    def tab(self, D):
        if D not in self.cache:
            p = self.p; r = pow(self.g, (p - 1) // D, p)
            self.cache[D] = {pow(r, i, p): i for i in range(D)}
        return self.cache[D]
    def cl(self, x, D):
        x %= self.p
        assert x
        return self.tab(D)[pow(x, (self.p - 1) // D, self.p)]

def check_rc(p, g, D, Delta, Omega, alpha, beta, C):
    """Definition plus-rc, verbatim: alpha in F_p^{Z_D}, beta in F_p^Delta, alpha_0+beta_0 in P_D,
    and for all i in Delta, j in Z_D: alpha_j+beta_i = 0 or cl_D(alpha_j+beta_i)+i+j in Omega."""
    if len(alpha) != D or set(beta) != set(Delta) or 0 not in Delta or 0 not in Omega: return False
    s0 = (alpha[0] + beta[0]) % p
    if s0 == 0 or C.cl(s0, D) != 0: return False
    Om = set(Omega)
    for i in Delta:
        for j in range(D):
            s = (alpha[j] + beta[i]) % p
            if s and (C.cl(s, D) + i + j) % D not in Om: return False
    return True

# ---------------------------------------------------------------- Table tab:plus-thresholds
STD = {  # name: (D, Delta, Omega, T_exist)
    'TL3': (3, (0, 1, 2), (0,), 430), 'TL4': (4, (0, 1, 2, 3), (0,), 9395),
    'TL5': (5, tuple(range(5)), (0,), 99745), 'TL6': (6, tuple(range(6)), (0,), 837384),
    'TW': (9, (0, 3, 6), (0,), 1124521)}
for m in range(1, 7): STD['U%d' % m] = (7, tuple(range(7)), (0, m), 1995734)

def Phi(p, D, r, w):
    """Lemma plus-sm(i), in floating point (only used to re-check the table thresholds)."""
    hD = (p - 1) / D
    gam = (1 + (D - 1) ** 2 / math.sqrt(p)) * p * p / (p - 1) ** 2
    mu0 = hD * (w * hD / p) ** (r - 1); mu1 = w * hD * (w * hD / p) ** (r - 1)
    rho0 = 1 / mu0 + gam ** (r - 1); rho1 = 1 / mu1 + gam ** (r - 1)
    return (1 - 1 / rho0) + (D - 1) * (1 - 1 / rho1)

def check_thresholds():
    out = []
    for nm in ['TL3', 'TL4', 'TL5', 'TL6', 'TW', 'U1']:
        D, De, Om, T = STD[nm]
        out.append((nm, T, Phi(T, D, len(De), len(Om)) < 1, Phi(T - 1, D, len(De), len(Om)) >= 1))
    return out

# ---------------------------------------------------------------- certificates (data, re-verified)
def load_certs():
    """returns dict (p, D, Delta, Omega) -> (g, alpha, beta)"""
    certs = {}
    s1 = json.load(open(os.path.join(HB, 'certs_stage1.json')))
    for k, v in s1.items():
        D, De = v['D'], tuple(v['R'])
        for ps, c in v['found'].items():
            certs[(int(ps), D, De, tuple(c['K']))] = (c['g'], c['alpha'], {int(a): b for a, b in c['beta'].items()})
    t6 = json.load(open(os.path.join(HB, 'v2', 'certs_tl6_all.json')))
    for ps, c in t6['found'].items():
        certs[(int(ps), 6, tuple(range(6)), (0,))] = (c['g'], c['alpha'], {int(a): b for a, b in c['beta'].items()})
    for c in json.load(open(os.path.join(HB, 'tierB_witnesses.json'))):
        certs[(c['p'], c['D'], tuple(c['R']), tuple(c['K']))] = (c['g'], c['alpha'], {int(a): b for a, b in c['beta'].items()})
    # search cache of the core-plus referee (FOUND entries only; beta listed in the order of Delta)
    rc = {} if os.environ.get('NO_RC') else json.load(open(os.path.join(R, '2026-11-14-rees-is-free', 'ref20_copy', 'rc_cache.json')))
    for key, (st, cert) in rc.items():  # NO_RC=1 skips this data source
        if st != 'FOUND': continue
        ps, Ds, Des, Oms = key.split('|')
        p, D = int(ps), int(Ds)
        De = tuple(int(x) for x in Des.split(',')); Om = tuple(int(x) for x in Oms.split(','))
        if (p, D, De, Om) in certs: continue
        a, b = cert
        certs[(p, D, De, Om)] = (None, a, dict(zip(De, b)))
    by_p = {}
    for (p, D, De, Om), v in certs.items(): by_p.setdefault(p, {})[(D, De, Om)] = v
    return by_p

CAPPED = []
SEARCH_BUDGET = int(os.environ.get('RC_BUDGET', '20000'))

def rc_search(p, g, D, De, Om, budget, seed):
    """Own DFS for an RC(D;De->Om) contraction (beta_0 = 0), bitsets over F_p. Returns
    ('FOUND', alpha, beta) | ('NONE',) (search exhausted) | ('CAP',)."""
    import random
    rng = random.Random(seed)
    pw = [1] * (p - 1)
    for i in range(1, p - 1): pw[i] = pw[i - 1] * g % p
    dl = [0] * p
    for i, x in enumerate(pw): dl[x] = i
    mask = (1 << p) - 1
    Oms = set(Om)
    H = []
    for s in range(D):
        b = 1  # y = 0 allowed
        for y in range(1, p):
            if (dl[y] + s) % D in Oms: b |= 1 << y
        H.append(b)
    P0 = 0
    for y in range(1, p):
        if dl[y] % D == 0: P0 |= 1 << y
    def rot(G, b):
        return ((G >> b) | (G << (p - b))) & mask if b else G
    X = [H[j] for j in range(D)]
    X[0] &= P0
    if not all(X): return ('NONE',)
    rest = [i for i in De if i != 0]
    cnt = [0]
    beta = {0: 0}
    def dfs(idx, X):
        if idx == len(rest): return X
        i = rest[idx]
        order = list(range(p)); rng.shuffle(order)
        for b in order:
            cnt[0] += 1
            if cnt[0] > budget: return 'CAP'
            Y = []
            ok = True
            for j in range(D):
                v = X[j] & rot(H[(i + j) % D], b)
                if not v: ok = False; break
                Y.append(v)
            if not ok: continue
            beta[i] = b
            r = dfs(idx + 1, Y)
            if r == 'CAP': return 'CAP'
            if r is not None: return r
        return None
    r = dfs(0, X)
    if r == 'CAP': return ('CAP',)
    if r is None: return ('NONE',)
    alpha = [((x & -x).bit_length() - 1) for x in r]
    return ('FOUND', alpha, dict(beta))

# ---------------------------------------------------------------- l-level tables (Prop. plus-tables)
ELL = {(19, 9): 'B4_19.json', (37, 9): 'B4_37.json', (73, 9): 'B4_73.json', (13, 4): 'B3_13_4.json', (13, 6): 'B3_13_6.json'}

def check_ell(p, k, fn):
    """Def. plus-ell (i)-(iii); (iii) tested on all (k-1)^l basis tensors of W^{(x)l}, W basis e_m - z_m e_0."""
    tab = json.load(open(os.path.join(K9, fn)))
    l = len(next(iter(tab)))
    g = least_prim_root(p)
    if len(tab) != k ** l: return False, l
    C = {}
    for key, b in tab.items():
        y = tuple(int(ch) for ch in key)
        C[y] = pow(g, sum(y), p) * int(b) % p
    Cl = Cls(p, g)
    if C[(0,) * l] == 0 or Cl.cl(C[(0,) * l], k) != 0: return False, l
    if any(v and Cl.cl(v, k) != 0 for v in C.values()): return False, l
    z = [pow(g, m, p) for m in range(k)]
    import itertools
    for ms in itertools.product(range(1, k), repeat=l):
        tot = 0
        for S in range(1 << l):   # coordinates in S take value 0 with factor -z_m
            y = tuple(0 if (S >> r) & 1 else ms[r] for r in range(l))
            fac = 1
            for r in range(l):
                if (S >> r) & 1: fac = fac * (-z[ms[r]]) % p
            tot = (tot + fac * C[y]) % p
        if tot: return False, l
    return True, l

# ---------------------------------------------------------------- per-prime machinery
class Prime:
    def __init__(self, p, certs_p):
        self.p = p; self.g = least_prim_root(p); self.C = Cls(p, self.g)
        self.certs = certs_p or {}
        self.avail_cache = {}
        self.dl = None
        self.stats = {'cert_ok': 0, 'cert_bad': 0, 'cert_wrong_g': 0, 'lemma': 0, 'none': 0, 'own_found': 0, 'own_bad': 0, 'own_none': 0, 'own_cap': 0}

    def avail(self, D, De, Om):
        key = (D, tuple(De), tuple(Om))
        if key in self.avail_cache: return self.avail_cache[key]
        ok = False
        for nm, (D2, De2, Om2, T) in STD.items():
            if (D2, De2, Om2) == key and self.p >= T:
                ok = True; self.stats['lemma'] += 1
        if not ok and key in self.certs:
            g, a, b = self.certs[key]
            if g is not None and g != self.g: self.stats['cert_wrong_g'] += 1
            elif check_rc(self.p, self.g, D, key[1], key[2], a, b, self.C):
                ok = True; self.stats['cert_ok'] += 1
            else: self.stats['cert_bad'] += 1
        if not ok and self.p <= 523:
            r = rc_search(self.p, self.g, D, key[1], key[2], SEARCH_BUDGET, hash(key) & 0xffff)
            if r[0] == 'FOUND':
                if check_rc(self.p, self.g, D, key[1], key[2], r[1], r[2], self.C):
                    ok = True; self.stats['own_found'] += 1
                else: self.stats['own_bad'] += 1
            elif r[0] == 'NONE': self.stats['own_none'] += 1
            else: self.stats['own_cap'] += 1; CAPPED.append((self.p, key))
        if not ok: self.stats['none'] += 1
        self.avail_cache[key] = ok
        return ok

    # class sumset data for P = P_kappa, only for small p
    def setup_small(self, k):
        p, g = self.p, self.g
        if self.dl is None:
            pw = np.empty(p - 1, dtype=np.int64); x = 1
            for i in range(p - 1): pw[i] = x; x = x * g % p
            dl = np.zeros(p, dtype=np.int64); dl[pw] = np.arange(p - 1)
            self.pw, self.dl = pw, dl
        h = (p - 1) // k
        Ck, Zk = [], []
        for c in range(k):
            idx = (c + k * np.arange(h)) % (p - 1)
            vals = (1 + self.pw[idx]) % p
            Zk.append(bool((vals == 0).any()))
            Ck.append(frozenset(int(v) for v in np.unique(self.dl[vals[vals != 0]] % k)))
        return Ck, Zk

def tsets(k, Ck, Zk, ecl, smax):
    """T_0..T_smax as (classes frozenset, zero flag); eps has class ecl. T_j = T_{j-1} u eps T_{j-1} u
    {alpha + eps beta}; for nonzero alpha in class i, beta in class j: classes i + C_{j+ecl-i}."""
    S, z = frozenset([0]), False
    out = [(S, z)]
    for _ in range(smax):
        S2 = set(S) | {(i + ecl) % k for i in S}
        z2 = z
        for i in S:
            for j in S:
                d = (j + ecl - i) % k
                S2 |= {(i + c) % k for c in Ck[d]}
                z2 = z2 or Zk[d]
        S, z = frozenset(S2), z2
        out.append((S, z))
    return out

def t_value(p, k, Ck, Zk):
    S, z, n = frozenset([0]), False, 1
    while True:
        n += 1
        S2, z2 = set(), False
        for i in S:
            d = (-i) % k
            S2 |= {(i + c) % k for c in Ck[d]}; z2 = z2 or Zk[d]
        if z2: return n
        S = frozenset(S2)
        assert n <= k + 1

def divisors(n): return [d for d in range(1, n + 1) if n % d == 0]

def lift(D, Dp, Om):
    return tuple(i for i in range(D) if (i % Dp) in Om)

def omegas(D):
    out = [(0,)]
    out += [(0, a) for a in range(1, D)]
    out += [(0, a, b) for a in range(1, D) for b in range(a + 1, D)]
    return out

def chains(P, k, E, Kc):
    """Candidate (d) / nodes (f3) / finishes: chains with 1 <= L <= 3, D_L = k, |Omega_t| <= 3.
    Returns dict Omega_L -> set of (degree, constant). Base: GE (D0=1, Omega0=Z_1) or H_{D0}, 2<=D0<k, D0|k."""
    res = {}
    divs = [d for d in divisors(k) if d >= 2]
    bases = [(1, (0,), 1, 1)] + [(D0, (0,), E[D0], Kc[D0]) for D0 in divs if D0 < k and D0 in E]
    def rec(Dprev, Omprev, e, K, depth):
        if depth == 3: return
        for Dt in divs:
            if Dt % Dprev: continue
            De = lift(Dt, Dprev, Omprev)
            if len(De) < 2: continue
            for Om in omegas(Dt):
                if not P.avail(Dt, De, Om): continue
                e2, K2 = e + 1, K * (len(De) - 1)
                if Dt == k: res.setdefault(Om, set()).add((e2, K2))
                rec(Dt, Om, e2, K2, depth + 1)
    for (D0, Om0, e0, K0) in bases:
        rec(D0, Om0, e0, K0, 0)
    return res

def solve_prime(p, certs_p, ellok):
    P = Prime(p, certs_p)
    E, Kc = {1: 1}, {1: 1}
    rows = {}
    ks = [k for k in divisors(gcd(p - 1, 2520)) if 2 <= k <= 9]
    for k in ks:
        h = (p - 1) // k
        small = p < 4 * k ** 4
        if small:
            Ck, Zk = P.setup_small(k)
            t = t_value(p, k, Ck, Zk)
        else:
            t = 2 if h % 2 == 0 else 3
        L = math.ceil(math.log2(t))
        cands = []   # (degree, constant, label)
        if k in (3, 4, 5, 6) and P.avail(*STD['TL%d' % k][:3]):
            cands.append((2, k - 1, 'TL%d' % k))
        if k == 9 and 3 in E and P.avail(*STD['TW'][:3]):
            cands.append((E[3] + 1, 2 * Kc[3], 'TW'))
        ch = chains(P, k, E, Kc) if p <= 523 else {}
        for (e, K) in ch.get((0,), ()):
            cands.append((e, K, 'TB'))
        if (p, k) in ellok and ellok[(p, k)][0]:
            l = ellok[(p, k)][1]
            cands.append((l, (k - 1) ** f2(l), 'L%d' % l))
        # plans
        nodes = []   # (m, e, K, label)
        if k % 2 == 0 and (k // 2) in E:
            nodes.append((k // 2, E[k // 2], Kc[k // 2], 'f1'))
        if k == 7:
            for m in range(1, 7):
                if P.avail(*STD['U%d' % m][:3]): nodes.append((m, 2, 6, 'f2U%d' % m))
        for Om, s in ch.items():
            if len(Om) == 2:
                for (e, K) in s: nodes.append((Om[1], e, K, 'f3'))
        fins = [(None, 0, 1, 'F0'), (tuple(range(k)), 1, 1, 'F1')]
        for D2 in divisors(k):
            if 2 <= D2 < k and D2 in E:
                fins.append((tuple(range(0, k, D2)), E[D2], Kc[D2], 'fH%d' % D2))
        for Om, s in ch.items():
            for (e, K) in s: fins.append((Om, e, K, 'fTB'))
        Tcache = {}
        for (m, eN, KN, lab) in nodes:
            if not small:
                cands.append((eN + 1, KN, 'P(%s,1,F1)' % lab))
                continue
            if m not in Tcache:
                eps = (-pow(pow(P.g, m, p), p - 2, p)) % p
                Tcache[m] = tsets(k, Ck, Zk, P.C.cl(eps, k), k + 1)
            T = Tcache[m]
            for s in range(1, k + 2):
                S, z = T[s]
                for (Om, eF, KF, flab) in fins:
                    if Om is None: ok = z
                    else: ok = any(all((u + kk) % k in S for kk in Om) for u in range(k))
                    if ok: cands.append((s * eN + eF, KN ** s * KF, 'P(%s,%d,%s)' % (lab, s, flab)))
        if not cands:
            rows[k] = None; continue
        e = min(c[0] for c in cands)
        K = min(c[1] for c in cands if c[0] == e)
        # dominance witness per Lemma plus-free-const hypothesis: e_Z <= kL and K_Z < k^{f(k) L}
        dom = [c for c in cands if c[0] <= k * L and c[1] < k ** (f2(k) * L)]
        domk = [c for c in cands if c[0] <= k]
        # bound check of the lemma itself: every candidate K_Z <= (k-1)^{f(e_Z)}
        lemma_viol = [c for c in cands if c[1] > (k - 1) ** f2(c[0])]
        E[k], Kc[k] = e, K
        best = min(cands, key=lambda c: (c[0], c[1]))
        rows[k] = dict(e=e, K=K, t=t, L=L, dom=bool(dom), domk=bool(domk), lemma_viol=lemma_viol,
                       best=best[2], margin=(k ** (f2(k) * L)) / min(c[1] for c in dom) if dom else None)
    return rows, P.stats

if __name__ == '__main__':
    N = int(sys.argv[1])
    t0 = time.time()
    print('thresholds (name, T_exist, Phi(T)<1, Phi(T-1)>=1):', check_thresholds())
    ellok = {}
    for (p, k), fn in ELL.items():
        ellok[(p, k)] = check_ell(p, k, fn)
    print('ell tables verified:', ellok)
    certs = load_certs()
    print('certificate primes loaded:', len(certs), 'load time %.0fs' % (time.time() - t0), flush=True)
    degs, fails, nodom, nodomk, lv = {}, [], [], [], []
    tot = {}
    Kmax = {}
    margins = {}
    for p in primes_below(N):
        rows, st = solve_prime(p, certs.get(p), ellok)
        for a, b in st.items(): tot[a] = tot.get(a, 0) + b
        for k, r in rows.items():
            if r is None: fails.append((p, k)); continue
            degs['%d,%d' % (p, k)] = r['e']
            if not r['dom']: nodom.append((p, k))
            if not r['domk']: nodomk.append((p, k, r['e'], r['L']))
            if r['lemma_viol']: lv.append((p, k, r['lemma_viol'][:2]))
            Kmax[k] = max(Kmax.get(k, 0), r['K'])
            if r['margin'] is not None and (k not in margins or r['margin'] < margins[k][0]):
                margins[k] = (r['margin'], p)
    print('pairs:', len(degs), 'time %.0fs' % (time.time() - t0))
    print('no IS-free candidate:', fails)
    print('no dominating candidate (e<=kL, K<k^{f(k)L}):', nodom)
    print('no candidate of degree <= kappa:', nodomk)
    print('lemma plus-free-const bound violations K_Z > (k-1)^{f(e_Z)}:', len(lv), lv[:5])
    print('max least constant K per kappa:', dict(sorted(Kmax.items())))
    print('smallest margin k^{f(k)L}/K_Z over dominating Z, per kappa:', {k: ('%.3g' % v[0], v[1]) for k, v in sorted(margins.items())})
    print('availability stats:', tot)
    print('own searches capped (treated unavailable):', len(CAPPED), CAPPED[:30])
    # exponents with S1 forbidden, p < N
    def kd(p, d): return gcd(d, p - 1)
    Ev = {}
    att = {}
    for c in range(2, 10):
        best, who = 0, []
        for p in primes_below(N):
            if p <= c: continue
            s = 0
            for d in range(2, c + 1):
                k = kd(p, d)
                s += 1 if k == 1 else degs['%d,%d' % (p, k)]
            if s > best: best, who = s, [p]
            elif s == best: who.append(p)
        Ev[c] = 1 + best; att[c] = who
    print('E(c) with S1 forbidden, p < N, c=2..9:', [Ev[c] for c in range(2, 10)])
    w9 = att[9]
    print('c=9 attainers:', len(w9), 'not 1 mod 2520:', [p for p in w9 if (p - 1) % 2520])
    json.dump(degs, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'degs_indep_%d%s.json' % (N, '_norc' if os.environ.get('NO_RC') else '')), 'w'))
    print('total time %.0fs' % (time.time() - t0))
