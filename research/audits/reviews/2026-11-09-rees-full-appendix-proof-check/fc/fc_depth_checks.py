"""Checks for rem:fc-zero-sum-arity and rem:fc-witness-h3 (checker fc, 9 Nov 2026):
 [1] sigma_p exactly (Markov chain on subset-sum sets) vs <= p and <= ceil(2 log2(p-1)) + 4;
 [2] Jacobi-sum count bound N(y) >= (p-(k-1)(k-2)sqrt p-3k+1)/k^2 and the 1/(2k) split probability;
 [3] depths j*_h (stated values; bounds via c_h, phi(h); j*_3 - log2(p)/2 range);
 [4] max_{p>c} E for c = 2..9;
 [5] simulation of the weight-doubling solvers (binary digit sets, D_j tables, rescaled form):
     every output checked exactly; mean column count vs N_0(n).
Finite checks only.  Run: nice -n 19 timeout 900 /opt/anaconda3/bin/python -I fc_depth_checks.py
"""
import math, random, itertools, functools
from fractions import Fraction as Fr
import numpy as np
from sympy import primerange, isprime, primitive_root

out = []
def say(*a):
    s = " ".join(str(x) for x in a); print(s); out.append(s)

# ------------------------------------------------------------------ [1] sigma_p
say("[1] sigma_p = E[# uniform draws until subset sums (with empty sum) cover F_p]")
@functools.lru_cache(maxsize=None)
def sigma_exact(p):
    full = (1 << p) - 1
    nst = 1 << p
    E = np.zeros(nst)
    states = np.arange(nst, dtype=np.int64)
    valid = (states & 1) == 1          # contains 0
    pc = np.array([bin(s).count('1') for s in range(nst)])
    mask = full
    for k in range(p - 1, 0, -1):     # popcount k states containing 0, decreasing
        S = states[valid & (pc == k)]
        acc = np.zeros(len(S))
        for a in range(1, p):
            rot = ((S << a) | (S >> (p - a))) & mask
            acc += E[S | rot]
        E[S] = (p + acc) / (p - 1)
    return E[1]
for p in [3, 5, 7, 11, 13, 17, 19]:
    s = sigma_exact(p)
    b = math.ceil(2 * math.log2(p - 1)) + 4
    say(f"   p={p}: sigma_p={s:.4f}  <= p: {s <= p + 1e-9}  <= ceil(2log2(p-1))+4={b}: {s <= b + 1e-9}")
say("   (sigma_3 = 3 gives N_0(n) = 1 + 3n(n+1)/2 at p = 3)")

# ------------------------------------------------------------------ [2] Jacobi-sum count and split probability
say("[2] min_{y!=0} #{(u,v) in P_k^2: u-v=y} vs (p-(k-1)(k-2)sqrt p-3k+1)/k^2; Pr_u[u-y in P_k] >= 1/(2k) when sqrt p >= 2(k-1)(k-2)+4")
okJ = True; okS = True; okD = True; nchk = 0
for kappa in range(2, 8):
    for p in primerange(3, 6000):
        if (p - 1) % kappa or kappa >= p - 1:
            continue
        h = (p - 1) // kappa
        P = np.zeros(p, dtype=bool)
        for x in range(1, p):
            P[pow(x, kappa, p)] = True
        Pi = P.astype(float)
        f = np.fft.rfft(Pi)
        corr = np.rint(np.fft.irfft(f * np.conj(f), n=p)).astype(int)   # corr[y] = #{v: v+y in P, v in P}
        minN = corr[1:].min()
        bound = (p - (kappa - 1) * (kappa - 2) * math.sqrt(p) - 3 * kappa + 1) / kappa ** 2
        nchk += 1
        if minN < bound - 1e-9:
            okJ = False; say("   Jacobi VIOLATION", p, kappa, minN, bound)
        if math.sqrt(p) > (kappa - 1) * (kappa - 2) + 3 and minN == 0:
            okD = False; say("   N(y)>0 VIOLATION (check D0-D0 directly)", p, kappa)
        if math.sqrt(p) >= 2 * (kappa - 1) * (kappa - 2) + 4 and Fr(int(minN), h) < Fr(1, 2 * kappa):
            okS = False; say("   split VIOLATION", p, kappa, minN, h)
say(f"   {nchk} (p,kappa) pairs, p < 6000, kappa = 2..7: Jacobi bound holds {okJ}; N(y) > 0 for all y != 0 when sqrt p > (k-1)(k-2)+3: {okD}; split prob >= 1/(2k): {okS}")

# ------------------------------------------------------------------ [3] depths
def mu_set(p, h):
    g0 = primitive_root(p); w = pow(g0, (p - 1) // h, p)
    S = np.zeros(p, dtype=bool); S[0] = True; x = 1
    for _ in range(h):
        S[x] = True; x = x * w % p
    return S
def diffset(D):
    # D - D (mod p) via zero-padded linear correlation, folded mod p
    p = len(D); L = 1 << (2 * p).bit_length()
    f = np.fft.rfft(D.astype(float), n=L)
    c = np.fft.irfft(f * np.conj(f), n=L)
    circ = c[:p] + c[L - p:L]
    return circ > 0.5
@functools.lru_cache(maxsize=None)
def depth(p, h):
    D = mu_set(p, h); J = 0
    while not D.all():
        D = diffset(D)
        J += 1
    return J
say("[3] depths j*_h")
say("   j*_3 at p=7,13,19,31:", [depth(p, 3) for p in (7, 13, 19, 31)], " (claim 1,1,2,2)")
say("   j*_4 at p=13,17:", [depth(p, 4) for p in (13, 17)], " (claim 1,2)")
# bounds: log2((p^(1/phi)-1)/(2c_h)) <= j*_h <= ceil(log2(c_h phi^2 p^(1/phi)/2)) + 1
ch = {3: (2, 2), 4: (1, 2), 6: (2, 2), 5: (4, 4)}   # h: (c_h, phi(h))
okB = True; cnt = 0
for h, (c_h, ph) in ch.items():
    for p in primerange(h + 2, 20000 if h != 5 else 8000):
        if (p - 1) % h or (p - 1) // h < 2:
            continue
        j = depth(p, h); cnt += 1
        lo = math.log2((p ** (1 / ph) - 1) / (2 * c_h)) if p ** (1 / ph) > 1 else -1
        hi = math.ceil(math.log2(c_h * ph * ph * p ** (1 / ph) / 2)) + 1
        if not (lo <= j <= hi):
            okB = False; say("   depth bound VIOLATION", h, p, j, lo, hi)
        # Cauchy-Davenport bound j*_h <= ceil(log2 kappa)
        if j > math.ceil(math.log2((p - 1) // h)):
            okB = False; say("   CD bound VIOLATION", h, p, j)
say(f"   depth bounds (h = 3,4,6 to 2e4; h = 5 to 8e3; {cnt} primes) and j*_h <= ceil(log2 kappa): {okB}")
# j*_3 - log2(p)/2 over primes p = 1 mod 3 below 6e4
vals = []
for p in primerange(7, 60000):
    if p % 3 == 1:
        vals.append(depth(p, 3) - 0.5 * math.log2(p))
say(f"   j*_3 - log2(p)/2 over {len(vals)} primes p = 1 mod 3 < 6e4: [{min(vals):.3f}, {max(vals):.3f}] (claim [-0.85, 0.60])")

# ------------------------------------------------------------------ [4] max_{p>c} E
say("[4] E(p) = 1 + sum_{d=2}^c (1 + j_d); claim max_{p>c} E = 3,6,8,10,13,14,16,19 for c = 2..9 (c=9 at p=19)")
res = []
for c in range(2, 10):
    T = max(((k - 1) * (k - 2) + 3) ** 2 for k in range(2, c + 1))
    best = (0, None)
    for p in primerange(c + 1, T + 2):
        E = 1
        for d in range(2, c + 1):
            k = math.gcd(d, p - 1)
            if k == 1:
                j = 0
            elif k == p - 1:
                j = math.ceil(math.log2(p - 1))
            else:
                j = depth(p, (p - 1) // k)
            E += 1 + j
        if E > best[0]:
            best = (E, p)
    best = (max(best[0], 2 * c - 1), best[1])
    res.append(best)
say("   computed:", [b[0] for b in res], "; maximizing primes:", [b[1] for b in res])

# ------------------------------------------------------------------ [5] weight-doubling solvers
say("[5] weight-doubling solvers: exact output checks and mean column counts")
class Stream:
    def __init__(self, p, n, rng):
        self.p, self.n, self.rng = p, n, rng; self.cols = []
    def take(self):
        v = tuple(self.rng.randrange(self.p) for _ in range(self.n)); self.cols.append(v); return len(self.cols) - 1

def kernel_vec(vecs, k, p):
    """nonzero alpha with sum alpha_i vecs[i][:k] = 0; len(vecs) = k+1."""
    m = len(vecs)
    A = [[vecs[i][r] % p for i in range(m)] for r in range(k)]
    # rref
    piv = []; r = 0
    for cidx in range(m):
        sel = None
        for i in range(r, k):
            if A[i][cidx]:
                sel = i; break
        if sel is None:
            continue
        A[r], A[sel] = A[sel], A[r]
        inv = pow(A[r][cidx], p - 2, p)
        A[r] = [x * inv % p for x in A[r]]
        for i in range(k):
            if i != r and A[i][cidx]:
                f = A[i][cidx]; A[i] = [(A[i][j] - f * A[r][j]) % p for j in range(m)]
        piv.append(cidx); r += 1
        if r == k: break
    free = [j for j in range(m) if j not in piv][0]
    alpha = [0] * m; alpha[free] = 1
    for i, pc in enumerate(piv):
        alpha[pc] = (-A[i][free]) % p
    return alpha

def make_solver(p, digit_sets, tables, jstar):
    """digit_sets[j] (j<=jstar) as sets of residues; tables[j][alpha] = (x, x') in D_j^2 for alpha in D_{j+1}."""
    def solve(j, n, y, st):
        if n == 0:
            return [(st.take(), 1)]
        if j == jstar:
            idx = [st.take() for _ in range(n + 1)]
            al = kernel_vec([st.cols[i] for i in idx], n, p)
            assert all(a == 0 for a in y[:n])
            return list(zip(idx, al))
        blocks = []; sums = {0}
        while len(sums) < p:
            wts = solve(j + 1, n - 1, [0] * (n - 1), st)
            b = sum(w * st.cols[i][n - 1] for i, w in wts) % p
            blocks.append((wts, b))
            sums = sums | {(s + b) % p for s in sums}
        u = [0] * st.n
        for wts, b in blocks:
            for i, w in wts:
                x, xp = tables[j][w % p]
                for r in range(st.n):
                    u[r] = (u[r] + xp * st.cols[i][r]) % p
        rec = solve(j, n - 1, [(y[r] - u[r]) % p for r in range(n - 1)], st)
        last = (y[n - 1] - u[n - 1] - sum(w * st.cols[i][n - 1] for i, w in rec)) % p
        # subset of blocks with beta-sum = last (DP)
        reach = {0: []}
        for k, (wts, b) in enumerate(blocks):
            new = dict(reach)
            for s, T in reach.items():
                s2 = (s + b) % p
                if s2 not in new:
                    new[s2] = T + [k]
            reach = new
        T = set(reach[last])
        res = list(rec)
        for k, (wts, b) in enumerate(blocks):
            for i, w in wts:
                x, xp = tables[j][w % p]
                res.append((i, x if k in T else xp))
        return res
    return solve

def build_tables(p, D0):
    Ds = [set(D0)]; tables = []
    while len(Ds[-1]) < p:
        Dj = Ds[-1]; nxt = {}
        for x in sorted(Dj):
            for xp in sorted(Dj):
                nxt.setdefault((x - xp) % p, (x, xp))
        nxt[0] = (0, 0)
        tables.append(nxt); Ds.append(set(nxt))
    return Ds, tables

def N0_formula(n, sigma, jstar):
    vals = [e + 1 for e in range(n + 1)]
    for _ in range(jstar):
        new = []; acc = 0
        for e in range(n + 1):
            new.append(1 + sigma * acc); acc += vals[e]
        vals = new
    return vals[n]

rng = random.Random(9112026)
cases = []
# binary digit sets of rem:fc-zero-sum-arity(a) (kappa = p - 1): D^(0) = {0,1}, D^(j) = {-2^(j-1),...,2^(j-1)} mod p
for p in (3, 5, 7):
    js = math.ceil(math.log2(p - 1))
    Ds = [{0, 1}] + [{x % p for x in range(-2 ** (j - 1), 2 ** (j - 1) + 1)} for j in range(1, js + 1)]
    tables = []
    for j in range(js):
        tb = {}
        for a in range(-2 ** j if j >= 1 else -1, (2 ** j if j >= 1 else 1) + 1):
            x = math.ceil(a / 2); xp = -math.floor(a / 2)
            tb.setdefault(a % p, (x % p, xp % p))
        tb[0] = (0, 0)
        tables.append(tb)
    assert Ds[js] >= set(range(p)) or len(Ds[js]) == p
    cases.append(("binary", p, Ds, tables, js, {0, 1}))
# D_j tables for h >= 2 (rem:fc-witness-h3(b), table form)
for (p, kappa) in ((13, 3), (17, 4), (19, 6), (13, 4), (7, 2)):
    D0 = {pow(x, kappa, p) for x in range(1, p)} | {0}
    Ds, tables = build_tables(p, D0)
    cases.append((f"h={(p-1)//kappa}", p, Ds, tables, len(Ds) - 1, D0))
for (name, p, Ds, tables, js, D0) in cases:
    sig = sigma_exact(p)
    solve = make_solver(p, Ds, tables, js)
    for n in (2, 3):
        runs = 400 if p <= 13 else 150
        tot = 0; tot2 = 0; ok = True
        for _ in range(runs):
            st = Stream(p, n, rng)
            res = solve(0, n, [0] * n, st)
            idxs = [i for i, w in res]
            if len(set(idxs)) != len(idxs): ok = False
            if any(w % p not in D0 for i, w in res): ok = False
            if not any(w % p for i, w in res): ok = False
            s = [sum(w * st.cols[i][r] for i, w in res) % p for r in range(n)]
            if any(s): ok = False
            R = len(st.cols); tot += R; tot2 += R * R
        mean = tot / runs; sd = math.sqrt(max(tot2 / runs - mean ** 2, 0) / runs)
        Nf = N0_formula(n, sig, js)
        say(f"   {name} p={p} j*={js} n={n}: outputs valid {ok}; mean columns {mean:.2f} +- {sd:.2f} vs N_0={Nf:.2f} ({(mean-Nf)/sd if sd else 0:+.1f} se)")

# rescaled form (sqrt p >= 2(k-1)(k-2)+4): expected columns 1 + ceil(log2 p) p/(p-1) n(n+1)/2
def rescaled(p, kappa, n, rng, cap=10 ** 6):
    D = {pow(x, kappa, p) for x in range(1, p)} | {0}
    K = math.ceil(math.log2(p))
    cols = []
    def take():
        v = tuple(rng.randrange(p) for _ in range(n)); cols.append(v); return len(cols) - 1
    def split(e):
        for _ in range(cap):
            b = rng.randrange(1, p); x = pow(b, kappa, p)
            if (x - e) % p in D:
                return x, (x - e) % p
        raise RuntimeError
    def solve(dim, y):
        if dim == 0:
            return [(take(), 1)]
        blocks = []
        for k in range(K):
            while True:
                idx = [take() for _ in range(dim)]
                al = kernel_vec([cols[i] for i in idx], dim - 1, p)
                b = sum(a * cols[i][dim - 1] for i, a in zip(idx, al)) % p
                if b: break
            sc = pow(2, k, p) * pow(b, p - 2, p) % p
            blocks.append([(i, a * sc % p) for i, a in zip(idx, al)])
        sp = [[(i,) + split(a) for i, a in blk] for blk in blocks]
        u = [0] * n
        for blk in sp:
            for i, x, xp in blk:
                for r in range(n):
                    u[r] = (u[r] + xp * cols[i][r]) % p
        rec = solve(dim - 1, [(y[r] - u[r]) % p for r in range(dim - 1)])
        last = (y[dim - 1] - u[dim - 1] - sum(w * cols[i][dim - 1] for i, w in rec)) % p
        res = list(rec)
        for k, blk in enumerate(sp):
            on = (last >> k) & 1
            for i, x, xp in blk:
                res.append((i, x if on else xp))
        return res
    res = solve(n, [0] * n)
    s = [sum(w * cols[i][r] for i, w in res) % p for r in range(n)]
    ok = not any(s) and any(w % p for _, w in res) and all(w % p in D for _, w in res) and len({i for i, _ in res}) == len(res)
    return ok, len(cols)
for (p, kappa) in ((17, 2), (29, 2), (67, 3), (73, 3), (257, 4)):
    assert math.sqrt(p) >= 2 * (kappa - 1) * (kappa - 2) + 4
    for n in (2, 3, 4):
        runs = 300; tot = 0; tot2 = 0; ok = True
        for _ in range(runs):
            o, R = rescaled(p, kappa, n, rng); ok = ok and o; tot += R; tot2 += R * R
        mean = tot / runs; sd = math.sqrt(max(tot2 / runs - mean ** 2, 0) / runs)
        Nf = 1 + math.ceil(math.log2(p)) * p / (p - 1) * n * (n + 1) / 2
        say(f"   rescaled p={p} k={kappa} n={n}: outputs valid {ok}; mean columns {mean:.2f} +- {sd:.2f} vs formula {Nf:.2f}")

open(__file__.replace('.py', '_out.txt'), 'w').write("\n".join(out) + "\n")
