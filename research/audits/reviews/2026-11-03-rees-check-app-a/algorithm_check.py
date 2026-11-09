"""Run the algorithms of appendix-schedule2.tex end to end, exactly over F_p.

1. Theorem thm:app-s2-main: Phase 0 (symmetric scalars) + Lemma tensor + Lemma
   witness + Bezout exponent, at primes just above 4 k^{2k+2}, on random and
   degenerate columns, for several d with gcd(d, p-1) = k.
2. Lemma stage count: exact Lambda for random admissible prefixes vs p/(2k^l).
3. Prop TA(i): exact fraction of y with every X_j(y) nonempty vs 1 - k(1 - 1/U).
4. Prop TA(iii): empirical round success of the sampler vs 3/8.
5. Symmetric form failures at k = 3; independence of E_2 membership from xi.
Run: /opt/anaconda3/bin/python -I algorithm_check.py
"""
import json, math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sympy import isprime, nthroot_mod, primerange, primitive_root, Matrix, GF
from sympy.polys.matrices import DomainMatrix
from ffcommon import coset_table
from thresholds import U as Ufun
from e2_search import find_contraction

rng = random.Random(7)
OUT = {}


def next_prime(n, k, avoid=None):
    p = n
    while True:
        if isprime(p) and (p - 1) % k == 0 and (avoid is None or (p - 1) % avoid):
            return p
        p += 1


class Field:
    def __init__(self, p, k, xi):
        self.p, self.k, self.h, self.xi = p, k, (p - 1) // k, xi
        self.zeta = pow(xi, self.h, p)
        self.pw = {pow(self.zeta, m, p): m for m in range(k)}
        assert len(self.pw) == k
        self.z = [pow(xi, m, p) for m in range(k)]

    def ind(self, x):
        return self.pw[pow(x % self.p, self.h, self.p)]

    def root(self, w):
        w %= self.p
        if w == 0:
            return 0
        r = nthroot_mod(w, self.k, self.p)
        assert pow(r, self.k, self.p) == w
        return r


def find_coset_generator(p, k, J):
    h = (p - 1) // k
    primes = [q for q in range(2, k + 1) if k % q == 0 and isprime(q)]
    for _ in range(J):
        x = rng.randrange(1, p)
        z = pow(x, h, p)
        if all(pow(z, k // q, p) != 1 for q in primes):
            return x
    return None


def phase0(p, k, kk):
    xi = find_coset_generator(p, k, k * (kk + 3))
    F = Field(p, k, xi)
    tau = kk + 3 + math.ceil(math.log2(k))
    t = [pow(2, p - 2, p)]
    draws = 0
    for j in range(1, k):
        K = math.ceil(2 * k ** (j + 1) * tau)
        for _ in range(K):
            draws += 1
            x = rng.randrange(p)
            if x in t:
                continue
            c = 2 * F.z[j] ** 2 * x % p
            if c == 0 or F.ind(c) != 0:
                continue
            if all((F.z[i] * F.z[j] * (x + t[i])) % p and F.ind(F.z[i] * F.z[j] * (x + t[i])) == 0 for i in range(j)):
                t.append(x)
                break
        else:
            return None, F, draws
    C = [[F.z[i] * F.z[j] * (t[i] + t[j]) % p for j in range(k)] for i in range(k)]
    assert C[0][0] == 1 and all(F.ind(e) == 0 for r in C for e in r if e)
    assert all(e != 0 for r in C for e in r)
    return C, F, draws


def nullvec(cols, p):
    """nonzero c with sum c_b cols[b] = 0; cols are equal-length lists, more cols than rows."""
    A = DomainMatrix([[GF(p)(v) for v in col] for col in cols], (len(cols), len(cols[0])), GF(p)).transpose()
    ns = A.nullspace().to_Matrix()
    v = [int(x) % p for x in ns.row(0)]
    assert any(v)
    return v


def tensor(lams, F, a):
    p, k = F.p, F.k
    N = (k - 1) * a + 1
    blocks = [list(range(nu * (a + 1), (nu + 1) * (a + 1))) for nu in range(N)]
    cells1, T1 = [], []
    for B in blocks:
        c = nullvec([lams[b] for b in B], p)
        bs = next(b for b, cb in zip(B, c) if cb)
        inv = pow(c[B.index(bs)], p - 2, p)
        c = [x * inv % p for x in c]
        cell = {i: {} for i in range(k)}
        for b, cb in zip(B, c):
            if cb == 0:
                continue
            i = F.ind(cb)
            w = 1 if b == bs else F.root(cb * pow(F.z[i], p - 2, p))
            assert F.z[i] * pow(w, k, p) % p == cb
            cell[i][b] = w
        cells1.append(cell)
        T1.append([[sum(pow(w, k, p) * lams[b][r] for b, w in cell[i].items()) % p for r in range(a)] for i in range(k)])
    V = [sum((T1[nu][i] for i in range(1, k)), []) for nu in range(N)]
    eta = nullvec(V, p)
    ns = next(nu for nu in range(N) if eta[nu])
    inv = pow(eta[ns], p - 2, p)
    eta = [x * inv % p for x in eta]
    S = {(i, j): {} for i in range(k) for j in range(k)}
    for nu in range(N):
        if eta[nu] == 0:
            continue
        j = F.ind(eta[nu])
        vp = 1 if nu == ns else F.root(eta[nu] * pow(F.z[j], p - 2, p))
        for i in range(k):
            for b, w in cells1[nu][i].items():
                S[(i, j)][b] = vp * w % p
    T = {ij: [sum(pow(w, k, p) * lams[b][r] for b, w in S[ij].items()) % p for r in range(a)] for ij in S}
    for r in range(a):
        for j in range(k):
            assert sum(F.z[i] * T[(i, j)][r] for i in range(k)) % p == 0
        for i in range(k):
            assert sum(F.z[j] * T[(i, j)][r] for j in range(k)) % p == 0
    assert S[(0, 0)]
    return S


def solve(lams, d, F, C, a):
    p, k = F.p, F.k
    S = tensor(lams, F, a)
    u = [0] * len(lams)
    for (i, j), cell in S.items():
        th = F.root(C[i][j])
        for b, w in cell.items():
            u[b] = th * w % p
    dp, qp = d // k, (p - 1) // k
    t = pow(dp, -1, qp) if qp > 1 else 1
    s = [pow(x, t, p) if x else 0 for x in u]
    assert any(s)
    assert all(sum(pow(sb, d, p) * lb[r] for sb, lb in zip(s, lams)) % p == 0 for r in range(a))
    return s


# ---- 1. full algorithm
runs = []
for k, ds in [(2, [2, 6, 10]), (3, [3, 15, 21]), (4, [4, 12])]:
    p = next_prime(4 * k ** (2 * k + 2) + 1, k, avoid=None)
    while any(math.gcd(d, p - 1) != k for d in ds):
        p = next_prime(p + 1, k)
    C, F, draws = phase0(p, k, 10)
    assert C is not None
    ok = 0
    for a in (1, 2, 3):
        M = (a + 1) * ((k - 1) * a + 1)
        families = {
            'random': [[rng.randrange(p) for _ in range(a)] for _ in range(M)],
            'zero': [[0] * a for _ in range(M)],
            'repeated': [[1] + [0] * (a - 1)] * M,
            'rank1': [[(b + 1) * (r + 1) % p for r in range(a)] for b in range(M)],
            'sparse': [[rng.choice([0, 0, 0, 1, p - 1]) for _ in range(a)] for _ in range(M)],
        }
        for name, lams in families.items():
            for d in ds:
                solve(lams, d, F, C, a)
                ok += 1
    runs.append(dict(kappa=k, p=p, phase0_draws=draws, solved=ok))
OUT['algorithm'] = runs

# ---- 2. stage lemma: exact Lambda at p just above 4 k^{2k+2}
st = []
for k in (2, 3):
    p = next_prime(4 * k ** (2 * k + 2) + 1, k)
    ind, xi = coset_table(p, k)
    z = [pow(xi, m, p) for m in range(k)]
    worst = float('inf')
    for _ in range(40):
        for j in range(1, k):
            ts = [pow(2, p - 2, p)] + rng.sample(range(1, p), j - 1)
            if len(set(ts)) < j:
                continue
            lam = sum(1 for t in range(p) if t not in ts and (2 * z[j] ** 2 * t) % p and ind[(2 * z[j] ** 2 * t) % p] == 0
                      and all((z[i] * z[j] * (t + ts[i])) % p and ind[(z[i] * z[j] * (t + ts[i])) % p] == 0 for i in range(j)))
            worst = min(worst, lam / (p / (2 * k ** (j + 1))))
    st.append(dict(kappa=k, p=p, min_Lambda_over_bound=worst))
OUT['stage_lemma'] = st

# ---- 3. Prop TA(i): exact good-y fraction vs bound
ta = []
for k, plist in [(3, [97, 103, 109, 139, 211]), (4, [881, 929])]:
    for p in plist:
        ind, xi = coset_table(p, k)
        from ffcommon import masks, rot
        full = (1 << p) - 1
        ms = masks(p, k, ind, False)
        good = tot = 0
        import itertools
        ys = itertools.product(range(p), repeat=k - 1) if k == 3 else (tuple(rng.randrange(p) for _ in range(k - 1)) for _ in range(4000))
        for y in ys:
            y = (0,) + tuple(y)
            tot += 1
            if all(ms[(-j) % k] and all_cols for j in range(k) for all_cols in [1]):
                cols = []
                for j in range(k):
                    c = full
                    for i in range(k):
                        c &= rot(ms[(-(i + j)) % k], y[i], p, full)
                    cols.append(c)
                good += all(cols)
        Uv = float(Ufun(k, p)[0])
        ta.append(dict(kappa=k, p=p, exact_or_sampled_good_fraction=good / tot, bound=1 - k * (1 - 1 / Uv),
                       sampled=(k != 3)))
OUT['TA_i'] = ta

# ---- 4. Prop TA(iii) sampler: per-round success at p just above T_S
smp = []
for k, p in [(3, next_prime(736, 3)), (4, next_prime(8597, 4)), (2, next_prime(68, 2))]:
    ind, xi = coset_table(p, k)
    h = (p - 1) // k
    K = math.ceil(2 * (p / h) ** k * math.log(4 * k))
    succ = 0
    R = 300
    for _ in range(R):
        y = [0] + [rng.randrange(p) for _ in range(k - 1)]
        ok = True
        for j in range(k):
            for _ in range(K):
                x = rng.randrange(p)
                if all((x + y[i]) % p and ind[(x + y[i]) % p] == (-(i + j)) % k for i in range(k)):
                    break
            else:
                ok = False
                break
        succ += ok
    smp.append(dict(kappa=k, p=p, K=K, rounds=R, success_rate=succ / R, claimed_lower=3 / 8,
                    U=float(Ufun(k, p)[0]), need=1 + 1 / (8 * k)))
OUT['TA_iii_sampler'] = smp

# ---- 5a. symmetric form at k = 3: t_0 = 1/2 WLOG (scale by Q_0)
sym = {}
for mode in ('zero', 'strict'):
    fails = []
    for p in primerange(5, 400):
        if (p - 1) % 3:
            continue
        ind, xi = coset_table(p, 3)
        z = [1, xi, xi * xi % p]
        t0 = pow(2, p - 2, p)
        def okc(e):
            e %= p
            return (e == 0 and mode == 'zero') or (e != 0 and ind[e] == 0)
        found = False
        for t1 in range(p):
            if not (okc(2 * z[1] ** 2 * t1) and okc(z[1] * (t0 + t1))):
                continue
            for t2 in range(p):
                if okc(2 * z[2] ** 2 * t2) and okc(z[2] * (t0 + t2)) and okc(z[1] * z[2] * (t1 + t2)):
                    found = True
                    break
            if found:
                break
        if not found:
            fails.append(p)
    sym[mode] = fails
OUT['symmetric_k3_failures'] = sym

# ---- 5b. xi independence of E_2 membership (all coset generators)
xi_bad = []
for k in (3, 4, 5):
    for p in primerange(k + 2, 140):
        if (p - 1) % k:
            continue
        g = primitive_root(p)
        res = set()
        for e in range(1, p - 1):
            x = pow(g, e, p)
            if math.gcd(e, k) == 1:  # x is a coset generator iff e is prime to k
                r, _ = find_contraction(p, k, 'zero', xi=x)
                res.add(r is not None)
        if len(res) != 1:
            xi_bad.append((k, p))
OUT['xi_independence_failures'] = xi_bad
print(json.dumps(OUT, indent=1, default=str))
