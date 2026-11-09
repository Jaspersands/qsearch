"""Independent exact checks for appendix-free-coordinate.tex (checker fc, 9 Nov 2026).

Finite checks only: they can falsify, not prove.
Run: nice -n 19 timeout 600 /opt/anaconda3/bin/python -I fc_exact_checks.py
"""
import itertools, random, math
from fractions import Fraction as Fr
from collections import Counter, defaultdict

def rref(rows, p):
    """Reduced row echelon form over F_p. rows: list of lists. Returns (R nonzero rows, pivots)."""
    A = [list(r) for r in rows]
    if not A:
        return [], []
    nr, nc = len(A), len(A[0])
    piv = []
    r = 0
    for c in range(nc):
        k = None
        for i in range(r, nr):
            if A[i][c] % p:
                k = i; break
        if k is None:
            continue
        A[r], A[k] = A[k], A[r]
        inv = pow(A[r][c], p - 2, p)
        A[r] = [(x * inv) % p for x in A[r]]
        for i in range(nr):
            if i != r and A[i][c] % p:
                f = A[i][c]
                A[i] = [(A[i][j] - f * A[r][j]) % p for j in range(nc)]
        piv.append(c)
        r += 1
        if r == nr:
            break
    return [tuple(A[i]) for i in range(r)], piv

def powers_set(p, kappa):
    return sorted({pow(x, kappa, p) for x in range(1, p)})

def beta(M, n0, a, p, kappa):
    h = (p - 1) // kappa
    q = Fr(h + 1, p)
    L = M - n0
    return Fr(4, 1) / (Fr(h) ** (n0 - 1) * q ** a) + Fr(p ** a - 1, (p - 1) * p ** L)

out = []
def say(*a):
    s = " ".join(str(x) for x in a)
    print(s); out.append(s)

# ---------------------------------------------------------------- [1] lem:fc-rref (a),(b),(c)
say("[1] lem:fc-rref: exhaustive over X in F_p^{a x M}")
for (p, a, M) in [(3, 2, 4), (5, 2, 3), (3, 2, 5), (3, 3, 3), (2, 2, 4)]:
    tot = p ** (a * M)
    by_pat = defaultdict(Counter)
    npr = Counter()
    for flat in itertools.product(range(p), repeat=a * M):
        X = [flat[i * M:(i + 1) * M] for i in range(a)]
        R, piv = rref(X, p)
        by_pat[tuple(piv)][tuple(R)] += 1
        npr[piv[-1] + 1 if piv else 0] += 1   # p_r (1-based), 0 if r=0
    ok = True
    for pat, cnt in by_pat.items():
        r = len(pat)
        # number of free entries f for this pattern
        f = 0
        for i, pi in enumerate(pat):
            for l in range(M):
                if l > pi and l not in pat:
                    f += 1
        vals = set(cnt.values())
        if len(cnt) != p ** f or len(vals) != 1:
            ok = False
    # (c): Pr[n' < n0] <= (p^a-1)/((p-1)p^L), n' = M - p_r
    okc = True
    for n0 in range(1, M + 1):
        L = M - n0
        prob = Fr(sum(c for pr, c in npr.items() if M - pr < n0), tot)
        bound = Fr(p ** a - 1, (p - 1) * p ** L)
        if prob > bound:
            okc = False
            say("   VIOLATION (c)", p, a, M, n0, prob, bound)
    say(f"   p={p} a={a} M={M}: free entries uniform given (r,pi): {ok}; (c) bound holds for all n0: {okc}")

# (a): R(Lambda) = R(X) for Lambda = E X with injective E (random checks)
rng = random.Random(20261109)
oka = True
for trial in range(3000):
    p = rng.choice([3, 5, 7]); a = rng.randint(1, 3); g = a + rng.randint(0, 2); M = rng.randint(1, 5)
    while True:
        E = [[rng.randrange(p) for _ in range(a)] for _ in range(g)]
        if len(rref(E, p)[0]) == a:   # rank a (columns independent): rank of g x a matrix
            break
    X = [[rng.randrange(p) for _ in range(M)] for _ in range(a)]
    Lam = [[sum(E[i][k] * X[k][j] for k in range(a)) % p for j in range(M)] for i in range(g)]
    if rref(Lam, p) != rref(X, p):
        oka = False
say(f"   (a) RREF(EX) == RREF(X) for 3000 random injective E: {oka}")

# ---------------------------------------------------------------- [2] lem:fc-moment exact
say("[2] lem:fc-moment: exact mean/variance/Chebyshev over all C in F_p^{r x n}")
for (p, kappa, r, n) in [(7, 2, 1, 2), (7, 2, 2, 2), (7, 3, 2, 3), (13, 3, 1, 3), (13, 3, 2, 2), (13, 4, 2, 2), (11, 5, 2, 2), (5, 2, 3, 2)]:
    h = (p - 1) // kappa
    P = powers_set(p, kappa); D = set(P) | {0}
    q = Fr(h + 1, p)
    Ns = Counter()
    xs = list(itertools.product(P, repeat=n))
    for flat in itertools.product(range(p), repeat=r * n):
        C = [flat[i * n:(i + 1) * n] for i in range(r)]
        N = 0
        for x in xs:
            if all((sum(C[i][l] * x[l] for l in range(n)) % p) in D for i in range(r)):
                N += 1
        Ns[N] += 1
    tot = p ** (r * n)
    EN = Fr(sum(k * v for k, v in Ns.items()), tot)
    EN2 = Fr(sum(k * k * v for k, v in Ns.items()), tot)
    Var = EN2 - EN ** 2
    EN_claim = Fr(h) ** n * q ** r
    Var_claim = Fr(h) ** (n + 1) * (q ** r - q ** (2 * r))
    low = Fr(sum(v for k, v in Ns.items() if k < EN / 2), tot)
    cheb = Fr(4, 1) / (Fr(h) ** (n - 1) * q ** r)
    say(f"   p={p} k={kappa} r={r} n={n}: EN ok={EN==EN_claim} Var ok={Var==Var_claim} Var<=h*EN {Var <= h*EN}  Pr[N<EN/2]={float(low):.4g} <= {float(cheb):.4g}: {low <= cheb}")
# last claim: Pr_C[Cx in D^r] = q^r for every fixed x != 0 (including x outside P^n)
okl = True
for (p, kappa, r, n) in [(7, 2, 2, 2), (13, 3, 1, 2), (11, 5, 1, 2)]:
    h = (p - 1) // kappa; D = set(powers_set(p, kappa)) | {0}; q = Fr(h + 1, p)
    for x in itertools.product(range(p), repeat=n):
        if not any(x):
            continue
        cnt = 0
        for flat in itertools.product(range(p), repeat=r * n):
            if all((sum(flat[i * n + l] * x[l] for l in range(n)) % p) in D for i in range(r)):
                cnt += 1
        if Fr(cnt, p ** (r * n)) != q ** r:
            okl = False
say(f"   last claim Pr_C[Cx in D^r] = q^r for all x != 0: {okl}")

# ---------------------------------------------------------------- [3] lem:fc-node exhaustive (a = 1) and Monte Carlo (a = 2)
say("[3] lem:fc-node: bank event <= beta, acceptance, witness validity")
def node_stats_fast(X, p, kappa, M, n0):
    """a = 1 only: N by convolution."""
    h = (p - 1) // kappa
    P = powers_set(p, kappa); D = set(P) | {0}
    q = Fr(h + 1, p)
    R, piv = rref(X, p)
    r = len(piv); pr = piv[-1] + 1 if piv else 0; nprime = M - pr
    if nprime < n0:
        return False, None, True
    if r == 0:
        return True, Fr(1), True
    dist = {0: 1}
    for l in range(pr, M):
        c = R[0][l]
        nd = defaultdict(int)
        for s0, w in dist.items():
            for x in P:
                nd[(s0 + c * x) % p] += w
        dist = nd
    N = sum(w for s0, w in dist.items() if (-s0) % p in D)
    acc = Fr(N, h ** nprime)
    return N >= Fr(1, 2) * h ** nprime * q ** r, acc, True

def node_stats(X, p, kappa, M, n0):
    """Return (good, accept_prob, witness_ok) for bank X (intrinsic a x M)."""
    h = (p - 1) // kappa
    P = powers_set(p, kappa); D = set(P) | {0}
    q = Fr(h + 1, p)
    R, piv = rref(X, p)
    r = len(piv)
    pr = piv[-1] + 1 if piv else 0
    nprime = M - pr
    Fp_ = list(range(pr, M))
    if nprime < n0:
        return False, None, True
    if r == 0:
        return True, Fr(1), True
    N = 0
    wit_ok = True
    for x in itertools.product(P, repeat=nprime):
        v = [(-sum(R[i][Fp_[l]] * x[l] for l in range(nprime))) % p for i in range(r)]
        if all(vi in D for vi in v):
            N += 1
            y = [0] * M
            for l in range(nprime):
                y[Fp_[l]] = x[l]
            for i in range(r):
                y[piv[i]] = v[i]
            # y in ker X, y in D^M, y != 0
            if any(sum(X[k][j] * y[j] for j in range(M)) % p for k in range(len(X))) or not any(y) or any(yy not in D for yy in y):
                wit_ok = False
    acc = Fr(N, h ** nprime)
    good = N >= Fr(1, 2) * h ** nprime * q ** r
    return good, acc, wit_ok

for (p, kappa, M, n0) in [(31, 2, 3, 2), (31, 3, 3, 2), (19, 2, 4, 3)]:
    a = 1
    tot = 0; bad = 0; wit = True; accmin = None
    h = (p - 1) // kappa; q = Fr(h + 1, p)
    for flat in itertools.product(range(p), repeat=M):
        X = [flat]
        good, acc, w = node_stats_fast(X, p, kappa, M, n0)
        tot += 1
        wit = wit and w
        if not good:
            bad += 1
        else:
            R, piv = rref(X, p); r = len(piv)
            if acc < q ** r / 2:
                accmin = acc
    b = beta(M, n0, a, p, kappa)
    say(f"   exhaustive p={p} k={kappa} a=1 M={M} n0={n0}: Pr[bad]={bad}/{tot}={bad/tot:.4g} <= beta={float(b):.4g}: {Fr(bad,tot) <= b}; acceptance >= q^r/2 on good banks: {accmin is None}")

for (p, kappa, a, M, n0, T) in [(31, 2, 2, 5, 3, 300), (61, 3, 2, 5, 3, 300), (13, 2, 2, 4, 2, 300)]:
    rng = random.Random(p * 1000 + a)
    bad = 0; wit = True
    for t in range(T):
        X = [[rng.randrange(p) for _ in range(M)] for _ in range(a)]
        good, acc, w = node_stats(X, p, kappa, M, n0)
        wit = wit and w
        bad += (not good)
    b = beta(M, n0, a, p, kappa)
    say(f"   Monte Carlo p={p} k={kappa} a={a} M={M} n0={n0} ({T} banks): Pr[bad]~{bad/T:.4g} vs beta={float(b):.4g}; witnesses valid: {wit}")

# ---------------------------------------------------------------- [4] prop:rc-lower mean identity and the p=5 example
say("[4] prop:rc-lower: E[acceptance of uniform kernel vector | generic] = (q^n - p^-n) q^a")
for (p, kappa, a, M) in [(7, 2, 1, 3), (7, 3, 1, 3), (5, 2, 2, 3), (13, 3, 1, 3), (7, 2, 2, 3)]:
    h = (p - 1) // kappa; D = set(powers_set(p, kappa)) | {0}; q = Fr(h + 1, p); n = M - a
    num = Fr(0); cnt = 0
    for flat in itertools.product(range(p), repeat=a * M):
        X = [flat[i * M:(i + 1) * M] for i in range(a)]
        R, piv = rref(X, p)
        if piv != list(range(a)):
            continue
        cnt += 1
        acc = 0
        for x in itertools.product(range(p), repeat=n):
            if not any(x) or any(xx not in D for xx in x):
                continue
            if all((-sum(R[i][a + l] * x[l] for l in range(n))) % p in D for i in range(a)):
                acc += 1
        num += Fr(acc, p ** n)
    mean = num / cnt
    claim = (q ** n - Fr(1, p ** n)) * q ** a
    gen = Fr(cnt, p ** (a * M))
    sing = 1 - math.prod(1 - Fr(1, p ** i) for i in range(1, a + 1))
    say(f"   p={p} k={kappa} a={a} M={M}: mean={mean} claim={claim} equal={mean == claim}; Pr[not generic]={1-gen} == 1-prod(1-p^-i)={sing}: {1-gen == sing}, <= 1/(p-1): {1-gen <= Fr(1,p-1)}")
# example: p=5, kappa=2, R=[1 2]
D5 = {0, 1, 4}
say("   p=5 example: -2x for x in {1,4}:", [(-2 * x) % 5 for x in (1, 4)], "in D?", [((-2 * x) % 5) in D5 for x in (1, 4)],
    "; beta(2,n0;1) for n0=1,2:", [float(beta(2, n0, 1, 5, 2)) for n0 in (1, 2)])

# ---------------------------------------------------------------- [5] lem:fc-zero-sum (a),(b)
say("[5] lem:fc-zero-sum")
for (p, a, M) in [(3, 1, 3), (3, 2, 4), (5, 1, 3), (3, 2, 5), (5, 2, 3), (7, 1, 4)]:
    tot = p ** (a * M); nos = 0
    for flat in itertools.product(range(p), repeat=a * M):
        cols = [tuple(flat[i * M + j] for i in range(a)) for j in range(M)]
        has = False
        for mask in range(1, 2 ** M):
            s = [0] * a
            for j in range(M):
                if mask >> j & 1:
                    for i in range(a):
                        s[i] += cols[j][i]
            if all(x % p == 0 for x in s):
                has = True; break
        nos += (not has)
    bnd = Fr(p ** a - 1, 2 ** M - 1)
    say(f"   (a) p={p} a={a} M={M}: Pr[no zero-sum]={Fr(nos,tot)} <= {bnd}: {Fr(nos,tot) <= bnd}")
# (b) Davenport: every bank of g(p-1)+1 columns in F_p^g has a zero-sum; g(p-1) columns can fail
for (p, g) in [(3, 2), (5, 1), (7, 1), (2, 3)]:
    M = g * (p - 1) + 1
    allok = True
    for cols in itertools.product(list(itertools.product(range(p), repeat=g)), repeat=M):
        has = False
        for mask in range(1, 2 ** M):
            s = [0] * g
            for j in range(M):
                if mask >> j & 1:
                    for i in range(g):
                        s[i] += cols[j][i]
            if all(x % p == 0 for x in s):
                has = True; break
        if not has:
            allok = False; break
    # tight example: each unit vector repeated p-1 times
    ex = [tuple(1 if i == k else 0 for i in range(g)) for k in range(g) for _ in range(p - 1)]
    exhas = any(all(sum(ex[j][i] for j in range(len(ex)) if mask >> j & 1) % p == 0 for i in range(g)) for mask in range(1, 2 ** len(ex)))
    say(f"   (b) p={p} g={g}: all banks of {M} columns have a zero-sum: {allok}; {len(ex)} columns (unit vectors x(p-1)) have none: {not exhas}")

# ---------------------------------------------------------------- [6] split counterexample 69/325
say("[6] split law counterexample (p=5, kappa=2, V=F_5^2, pi_1,pi_2 coordinates, M_1=2, n0=1)")
p = 5; P = [1, 4]; D = {0, 1, 4}
num = 0; den = 0
for l1 in itertools.product(range(p), repeat=2):
    for l2 in itertools.product(range(p), repeat=2):
        row = [l1[0], l2[0]]
        R, piv = rref([row], p)
        r = len(piv); pr = piv[-1] + 1 if piv else 0; nprime = 2 - pr
        if nprime < 1:
            continue
        Fp_ = list(range(pr, 2))
        acc = []
        for x in itertools.product(P, repeat=nprime):
            v = [(-sum(R[i][Fp_[l]] * x[l] for l in range(nprime))) % p for i in range(r)]
            if all(vi in D for vi in v):
                y = [0, 0]
                for l in range(nprime):
                    y[Fp_[l]] = x[l]
                for i in range(r):
                    y[piv[i]] = v[i]
                acc.append(tuple(y))
        if not acc:
            continue
        acc.sort()
        z = lambda y: ((y[0] * l1[0] + y[1] * l2[0]) % p, (y[0] * l1[1] + y[1] * l2[1]) % p)
        pick = next((y for y in acc if z(y)[1] == 0), acc[0])
        den += 1
        num += (z(pick) == (0, 0))
say(f"   Pr[z_eta = 0 | no abort] = {Fr(num, den)} (claim 69/325 = {Fr(69,325)}): {Fr(num,den) == Fr(69,325)}")

open(__file__.replace('.py', '_out.txt'), 'w').write("\n".join(out) + "\n")
