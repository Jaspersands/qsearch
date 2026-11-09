"""Independent check of the mu_h-digit weight-doubling sampler (Theorem H, H', Cor. H.6/H.7).

Written from the statements in 2026-11-05-rees-s3-witness-h3.md without reading that report's
code. Usage:  python hcheck.py <task> <out.json>   with task in
  depth | sp | solver | node | scaled | neg | exponent | budget | mitm
"""
from __future__ import annotations

import json
import math
import random
import sys
import time
from fractions import Fraction as Fr
from functools import lru_cache
from math import gcd, isqrt


# ----------------------------------------------------------------------------- arithmetic

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % q == 0:
            return n == q
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def primes_upto(N: int):
    sieve = bytearray([1]) * (N + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, isqrt(N) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
    return [i for i in range(N + 1) if sieve[i]]


def mu_set(p: int, h: int) -> set:
    """The subgroup of order h of F_p^*, computed as the set of kappa-th powers."""
    k = (p - 1) // h
    s = {pow(x, k, p) for x in range(1, p)}
    assert len(s) == h
    return s


def ceil_log2(x) -> int:
    """Least integer e with 2^e >= x (x > 0, int or Fraction)."""
    e = 0
    while Fr(2) ** e < x:
        e += 1
    if x < 1:
        while e > -10**6 and Fr(2) ** (e - 1) >= x:
            e -= 1
    return e


# ----------------------------------------------------------------------------- digit chain

def mask_of(S, p):
    m = 0
    for x in S:
        m |= 1 << (x % p)
    return m


def diff_mask(m: int, p: int) -> int:
    """Bitmask of A - A for A given by bitmask m (bit x <-> x in A)."""
    full = (1 << p) - 1
    out = 0
    x = m
    i = 0
    while x:
        if x & 1:
            # A - i: rotate right by i
            out |= ((m >> i) | (m << (p - i))) & full
        x >>= 1
        i += 1
    return out


def corr(ind):
    """Integer array c[x] = #{(u, v) in A^2 : u - v = x} for the 0/1 array ind of A (FFT)."""
    import numpy as np
    f = np.fft.rfft(ind)
    return np.rint(np.fft.irfft(f * np.conj(f), n=len(ind))).astype(np.int64)


def chain(p: int, h: int, jmax: int = 64, method=None):
    """Sizes |D_0|, |D_1|, ... until D_J = F_p; returns (jstar, sizes, masks).
    Bitset differences for p <= 3000 (default), FFT correlation above."""
    if method is None:
        method = "bits" if p <= 3000 else "fft"
    D0 = mu_set(p, h) | {0}
    if method == "fft":
        import numpy as np
        ind = np.zeros(p)
        ind[list(D0)] = 1
        sizes, j = [int(ind.sum())], 0
        while sizes[-1] < p:
            ind = (corr(ind) > 0).astype(float)
            j += 1
            sizes.append(int(ind.sum()))
            assert j <= jmax
        return j, sizes, None
    m = mask_of(D0, p)
    full = (1 << p) - 1
    sizes, masks = [bin(m).count("1")], [m]
    j = 0
    while m != full:
        m = diff_mask(m, p)
        j += 1
        sizes.append(bin(m).count("1"))
        masks.append(m)
        assert j <= jmax
    return j, sizes, masks


def jstar(p: int, h: int) -> int:
    return chain(p, h)[0]


def c_h(h: int) -> int:
    """max_t ||zeta_h^t||_1 in the power basis 1..zeta^{phi-1} of Z[zeta_h]."""
    # cyclotomic polynomial by division
    import sympy
    x = sympy.symbols("x")
    Phi = sympy.Poly(sympy.cyclotomic_poly(h, x), x)
    best = 0
    for t in range(h):
        r = sympy.Poly(x ** t, x).rem(Phi)
        best = max(best, sum(abs(int(c)) for c in r.all_coeffs()))
    return best


def euler_phi(n: int) -> int:
    r, m, q = n, n, 2
    while q * q <= m:
        if m % q == 0:
            while m % q == 0:
                m //= q
            r -= r // q
        q += 1
    if m > 1:
        r -= r // m
    return r


# ----------------------------------------------------------------------------- linear algebra mod p

def kernel_vector(cols, d, p):
    """cols: list of d+1 (or more) vectors; uses first d coordinates. Returns nonzero x with
    sum x_i cols_i[:d] = 0 (length len(cols))."""
    k = len(cols)
    assert k > d
    # matrix d x k
    A = [[cols[i][r] % p for i in range(k)] for r in range(d)]
    piv_cols, row = [], 0
    for col in range(k):
        if row >= d:
            break
        pr = next((r for r in range(row, d) if A[r][col]), None)
        if pr is None:
            continue
        A[row], A[pr] = A[pr], A[row]
        inv = pow(A[row][col], p - 2, p)
        A[row] = [a * inv % p for a in A[row]]
        for r in range(d):
            if r != row and A[r][col]:
                f = A[r][col]
                A[r] = [(a - f * b) % p for a, b in zip(A[r], A[row])]
        piv_cols.append(col)
        row += 1
    free = next(c for c in range(k) if c not in piv_cols)
    x = [0] * k
    x[free] = 1
    for r, pc in enumerate(piv_cols):
        x[pc] = (-A[r][free]) % p
    return x


def rref_basis(vecs, p):
    """Return (basis rows in rref, pivots)."""
    rows = []
    pivs = []
    for v in vecs:
        w = [a % p for a in v]
        for r, pc in zip(rows, pivs):
            if w[pc]:
                f = w[pc]
                w = [(a - f * b) % p for a, b in zip(w, r)]
        pc = next((i for i, a in enumerate(w) if a), None)
        if pc is None:
            continue
        inv = pow(w[pc], p - 2, p)
        w = [a * inv % p for a in w]
        new_rows = []
        for r in rows:
            if r[pc]:
                f = r[pc]
                r = [(a - f * b) % p for a, b in zip(r, w)]
            new_rows.append(r)
        rows = new_rows + [w]
        pivs = pivs + [pc]
    return rows, pivs


def coords_in(rows, pivs, v, p):
    """Coordinates of v in the rref basis, or None if v is outside the span."""
    w = [a % p for a in v]
    coeff = []
    for r, pc in zip(rows, pivs):
        f = w[pc]
        coeff.append(f)
        if f:
            w = [(a - f * b) % p for a, b in zip(w, r)]
    if any(w):
        return None
    return coeff


# ----------------------------------------------------------------------------- the sampler

class Overrun(Exception):
    pass


class Source:
    """Column supply: either an i.i.d. generator or a finite list (a block of a bank)."""

    def __init__(self, gen=None, lst=None, cap=None):
        self.gen, self.lst, self.cap = gen, lst, cap
        self.cols = []

    def read(self):
        i = len(self.cols)
        if self.cap is not None and i >= self.cap:
            raise Overrun
        v = self.gen() if self.lst is None else self.lst[i]
        self.cols.append(v)
        return i


class Sampler:
    """Algorithm A_j(d, y) of Theorem H with tables chosen at random (x(0) = x'(0) = 0)."""

    def __init__(self, p, h, rng, table_mode="random", broken=False, J=None):
        self.p, self.h = p, h
        self.J, sizes, masks = chain(p, h)
        if J is not None:
            self.J = J  # negative control: wrong depth
        self.D = [{x for x in range(p) if (m >> x) & 1} for m in masks]
        self.tab = []
        for j in range(len(self.D) - 1):
            t = {}
            Dj = sorted(self.D[j])
            for a in self.D[j + 1]:
                if a == 0:
                    t[0] = (0, 0)
                    continue
                opts = [x for x in Dj if (x - a) % p in self.D[j]]
                assert opts
                x = rng.choice(opts) if table_mode == "random" else opts[0]
                t[a] = (x, (x - a) % p)
            if broken and j == 0:
                # break one entry: x - x' != alpha
                a = next(a for a in sorted(t) if a)
                x, xp = t[a]
                t[a] = (x, (xp + 1) % p if (xp + 1) % p in self.D[j] else xp)
                if (t[a][0] - t[a][1]) % p == a:  # could not break with that choice
                    t[a] = (xp, x)
            self.tab.append(t)

    def run(self, src: Source, n: int, y=None):
        p = self.p
        if y is None:
            y = [0] * n
        return self.A(0, n, list(y), src)

    def A(self, j, d, y, src):
        p = self.p
        if j == self.J:
            assert not any(y[:d])
            idx = [src.read() for _ in range(d + 1)]
            if d == 0:
                return {idx[0]: 1}
            x = kernel_vector([src.cols[i] for i in idx], d, p)
            return {i: w for i, w in zip(idx, x) if w}
        if d == 0:
            return {src.read(): 1}
        # switches
        blocks = []
        reach = {0: None}  # value -> (prev value, block index)
        while len(reach) < p:
            out = self.A(j + 1, d - 1, [0] * (d - 1), src)
            beta = sum(w * src.cols[i][d - 1] for i, w in out.items()) % p
            k = len(blocks)
            blocks.append(out)
            new = {}
            for v in reach:
                u = (v + beta) % p
                if u not in reach and u not in new:
                    new[u] = (v, k)
            reach.update(new)
        tab = self.tab[j]
        u = [0] * d
        for out in blocks:
            for i, a in out.items():
                xp = tab[a][1]
                if xp:
                    col = src.cols[i]
                    for r in range(d):
                        u[r] = (u[r] + xp * col[r]) % p
        tgt = [(y[r] - u[r]) % p for r in range(d - 1)]
        rec = self.A(j, d - 1, tgt, src)
        s_d = (u[d - 1] + sum(w * src.cols[i][d - 1] for i, w in rec.items())) % p
        a = (y[d - 1] - s_d) % p
        T = set()
        v = a
        while reach[v] is not None:
            v, k = reach[v]
            T.add(k)
        res = dict(rec)
        for k, out in enumerate(blocks):
            for i, al in out.items():
                x, xp = tab[al]
                w = x if k in T else xp
                assert i not in res
                if w:
                    res[i] = w
        return res


def check_output(res, cols, p, Dset, y):
    """Exact check: nonempty, nonzero weights in Dset, sum = y (first len(y) coords)."""
    if not res:
        return False
    d = len(y)
    s = [0] * d
    for i, w in res.items():
        if w == 0 or w not in Dset:
            return False
        for r in range(d):
            s[r] = (s[r] + w * cols[i][r]) % p
    return s == [a % p for a in y]


# ----------------------------------------------------------------------------- s_p and N_j(d)

def s_p_exact(p: int):
    full = (1 << p) - 1

    @lru_cache(maxsize=None)
    def E(m):
        if m == full:
            return Fr(0)
        tot = Fr(p)
        for b in range(1, p):
            rot = ((m << b) | (m >> (p - b))) & full
            tot += E(m | rot)
        return tot / (p - 1)

    sys.setrecursionlimit(10000)
    return E(1)


def s_p_mc(p: int, trials: int, rng):
    full = (1 << p) - 1
    tot = 0
    for _ in range(trials):
        m, k = 1, 0
        while m != full:
            b = rng.randrange(p)
            k += 1
            m |= ((m << b) | (m >> (p - b))) & full
        tot += k
    return tot / trials


def N_table(J: int, s, nmax: int):
    """N_j(d) for j = 0..J, d = 0..nmax with N_J(d) = d+1, N_j(d) = 1 + s sum_{e<d} N_{j+1}(e)."""
    N = {J: [Fr(d + 1) for d in range(nmax + 1)]}
    for j in range(J - 1, -1, -1):
        row, acc = [], Fr(0)
        for d in range(nmax + 1):
            row.append(1 + s * acc)
            acc += N[j + 1][d]
        N[j] = row
    return N


# ----------------------------------------------------------------------------- tasks

def task_depth(out):
    res = {"jstar": {}, "lemma0": [], "weil": [], "bounds": [], "first_prime": {}}
    viol = []
    # test primes
    for (h, p) in [(3, 7), (3, 13), (3, 19), (3, 31), (4, 13), (4, 17), (4, 5)]:
        J, sizes, _ = chain(p, h)
        res["jstar"][f"h={h},p={p}"] = {"jstar": J, "sizes": sizes}
    # cross-check the two set methods
    xc = []
    for h in (3, 4, 5, 6):
        for p in primes_upto(2500):
            if p % h == 1 and p > h + 1:
                a, b = chain(p, h, method="bits")[1], chain(p, h, method="fft")[1]
                xc.append(a == b)
    res["bits_vs_fft_agree"] = [all(xc), len(xc)]
    if not all(xc):
        viol.append("bits_vs_fft")
    # Lemma 0 and Lemma J(iii)/(iv) on all primes p = 1 mod h, p < LIM
    LIM = {3: 20000, 4: 20000, 6: 20000, 5: 8000, 8: 8000, 12: 8000}
    ch = {h: c_h(h) for h in LIM}
    res["c_h"] = ch
    for h, lim in LIM.items():
        phi = euler_phi(h)
        first = {}
        exc = []
        for p in primes_upto(lim):
            if p % h != 1:
                continue
            k = (p - 1) // h
            J, sizes, _ = chain(p, h)
            for j, sz in enumerate(sizes):
                if sz < min(p, 2 ** j * h + 1):
                    viol.append(("lemma0", h, p, j))
            if k >= 1 and J > max(0, math.ceil(math.log2(k)) if k > 1 else 0):
                viol.append(("ceil_log2_kappa", h, p, J))
            lo = math.log2((p ** (1 / phi) - 1) / (2 * ch[h])) if p ** (1 / phi) > 1 else -99
            hi = (h % 2) + math.ceil(math.log2(ch[h] * phi ** 2 * p ** (1 / phi) / 2))
            if not (J >= lo - 1e-9 and J <= hi):
                viol.append(("lemmaJ", h, p, J, lo, hi))
            A = (k - 1) * (k - 2)
            if math.sqrt(p) > A + 3 and J > 1:
                viol.append(("weil_range", h, p, J))
            first.setdefault(J, p)
            exc.append(J - math.log2(p) / phi)
        res["first_prime"][h] = first
        res["bounds"].append({"h": h, "lim": lim, "phi": phi,
                              "excess_min": min(exc), "excess_max": max(exc), "nprimes": len(exc)})
    # Jacobi-sum pair count for every y != 0 (kappa <= 8, p < 3000)
    for k in range(2, 9):
        for p in primes_upto(3000):
            if p % k != 1 or (p - 1) // k < 2:
                continue
            h = (p - 1) // k
            mu = mu_set(p, h)
            A = (k - 1) * (k - 2)
            bound = (p - A * math.sqrt(p) - 3 * k + 1) / k ** 2
            import numpy as np
            ind = np.zeros(p)
            ind[list(mu)] = 1
            cnt = corr(ind)
            mn = int(cnt[1:].min())
            if mn < bound - 1e-9:
                viol.append(("jacobi", k, p, mn, bound))
            if math.sqrt(p) > A + 3 and mn == 0:
                viol.append(("jacobi_pos", k, p))
            if math.sqrt(p) >= 2 * A + 4 and mn / h < 1 / (2 * k) - 1e-12:
                viol.append(("jacobi_prob", k, p))
            res["weil"].append([k, p, mn, round(bound, 3)])
    res["weil"] = {"cases": len(res["weil"]), "sample": res["weil"][:5]}
    res["violations"] = viol
    res["ok"] = not viol
    json.dump(res, open(out, "w"), indent=1, default=str)
    print("depth ok" if not viol else f"VIOLATIONS {viol[:5]}")


def task_sp(out):
    res = {}
    for p in (5, 7, 13, 17, 19, 31):
        t = time.time()
        s = s_p_exact(p)
        res[p] = {"exact": f"{s.numerator}/{s.denominator}", "float": float(s), "sec": round(time.time() - t, 2)}
        print(p, res[p])
    rng = random.Random(11)
    for p in (19, 31):
        res[p]["mc_200000"] = s_p_mc(p, 200000, rng)
        print(p, res[p])
    json.dump(res, open(out, "w"), indent=1)


def load_sp(path):
    d = json.load(open(path))
    sp = {}
    for p, v in d.items():
        sp[int(p)] = Fr(v["exact"]) if "exact" in v else v["mc_200000"]
    return sp


def task_solver(out, sp_path):
    sp = load_sp(sp_path)
    rng = random.Random(2026_11_05)
    rows = []
    allok = True
    cases = [(3, 7, [4, 8, 16, 24], 60), (3, 13, [4, 8, 16], 40), (3, 19, [3, 5, 7], 40),
             (3, 31, [3, 5, 7], 30), (4, 13, [4, 8, 16], 40), (4, 17, [3, 5, 7], 40),
             (4, 5, [5, 10], 40)]
    for h, p, ns, runs in cases:
        smp = Sampler(p, h, rng)
        D0 = smp.D[0]
        s = sp[p]
        for n in ns:
            N = N_table(smp.J, Fr(s) if isinstance(s, Fr) else s, n)
            mean_th = float(N[0][n])
            reads = []
            ok = True
            for _ in range(runs):
                src = Source(gen=lambda: [rng.randrange(p) for _ in range(n)])
                res = smp.run(src, n)
                ok &= check_output(res, src.cols, p, D0, [0] * n)
                reads.append(len(src.cols))
            m = sum(reads) / runs
            sd = (sum((r - m) ** 2 for r in reads) / (runs - 1)) ** 0.5
            z = (m - mean_th) / (sd / runs ** 0.5) if sd > 0 else 0.0
            rows.append(dict(h=h, p=p, J=smp.J, n=n, runs=runs, mean=m, theory=mean_th,
                             z=round(z, 2), all_ok=ok))
            allok &= ok
            print(rows[-1], flush=True)
        # inhomogeneous targets at every level j < J
        okt = True
        for j in range(smp.J):
            for _ in range(10):
                n = 4
                src = Source(gen=lambda: [rng.randrange(p) for _ in range(n)])
                y = [rng.randrange(p) for _ in range(n)]
                res = smp.A(j, n, y, src)
                okt &= check_output(res, src.cols, p, smp.D[j], y)
        rows.append(dict(h=h, p=p, targets_all_levels_ok=okt))
        allok &= okt
    # exact degree of N_0
    deg = []
    for h, p in [(3, 7), (3, 13), (3, 19), (4, 17)]:
        J = jstar(p, h)
        s = sp[p]
        s = Fr(s) if isinstance(s, Fr) else Fr(s).limit_denominator(10 ** 6)
        N = N_table(J, s, 512)
        slope = math.log2(float(N[0][512]) / float(N[0][256]))
        lead = float(N[0][512]) / (float(s) ** J * 512 ** (1 + J) / math.factorial(1 + J))
        deg.append(dict(h=h, p=p, J=J, slope_256_512=round(slope, 4), lead_ratio=round(lead, 4)))
    json.dump(dict(rows=rows, degree=deg, all_ok=allok), open(out, "w"), indent=1)
    print("solver all_ok", allok, deg)


def bezout(d, pm1):
    # alpha d + alpha' (p-1) = gcd
    def eg(a, b):
        if b == 0:
            return a, 1, 0
        g, x, y = eg(b, a % b)
        return g, y, x - (a // b) * y
    g, x, _ = eg(d, pm1)
    return g, x % pm1


def node(p, d, g, a, tau, rng, bank=None, smp=None):
    """Cor. H.6 node. Returns ('ok', s, M) or ('abort', reason, M) or ('WRONG', ..)."""
    k = gcd(d, p - 1)
    h = (p - 1) // k
    if smp is None:
        smp = Sampler(p, h, rng)
    J = smp.J
    t = g
    while Fr(p) ** (t - g) < Fr(2) / tau:
        t += 1
    kb = ceil_log2(Fr(2) / tau)
    sig = min(p, math.ceil(2 * math.log2(p - 1)) + 4)
    Nbar = N_table(J, Fr(sig), g)[0][g]
    L = math.ceil(2 * Nbar)
    M = t + kb * L
    if bank is None:
        E = [[rng.randrange(p) for _ in range(a)] for _ in range(g)]  # g x a, rank a whp
        bank = []
        for _ in range(M):
            x = [rng.randrange(p) for _ in range(a)]
            bank.append([sum(E[r][c] * x[c] for c in range(a)) % p for r in range(g)])
    rows, pivs = rref_basis(bank[:t], p)
    coords = []
    for v in bank[t:]:
        c = coords_in(rows, pivs, v, p)
        if c is None:
            return ("abort", "span", M)
        coords.append(c)
    r = len(rows)
    for b in range(kb):
        blk = coords[b * L:(b + 1) * L]
        src = Source(lst=blk, cap=L)
        try:
            res = smp.run(src, r)
        except Overrun:
            continue
        # witness y on bank indices t + b*L + i
        y = {t + b * L + i: w for i, w in res.items()}
        # conversion: sigma^kappa = y, s = sigma^alpha
        gg, alpha = bezout(d, p - 1)
        assert gg == k
        roots = {}
        for x in range(1, p):
            roots.setdefault(pow(x, k, p), x)
        s = {}
        for i, w in y.items():
            if w not in roots:
                return ("WRONG", "not a kappa-th power", M)
            s[i] = pow(roots[w], alpha, p)
        if not s:
            return ("WRONG", "empty", M)
        tot = [0] * g
        for i, si in s.items():
            e = pow(si, d, p)
            for rr in range(g):
                tot[rr] = (tot[rr] + e * bank[i][rr]) % p
        if any(tot):
            return ("WRONG", "sum", M)
        return ("ok", len(s), M)
    return ("abort", "overrun", M)


def task_node(out):
    rng = random.Random(77)
    grid = [(7, 2), (13, 4), (13, 8), (19, 6), (31, 10), (13, 3), (13, 9), (17, 4)]
    rows = []
    wrong = 0
    for p, d in grid:
        k = gcd(d, p - 1)
        h = (p - 1) // k
        smp = Sampler(p, h, rng)
        gs = [2, 4, 6] if smp.J == 1 else [2, 3, 4]
        for g in gs:
            for tau in (Fr(1, 20), Fr(1, 2)):
                trials = 40 if smp.J == 1 else 20
                cnt = {"ok": 0, "abort": 0, "WRONG": 0}
                reasons = {}
                M = None
                for _ in range(trials):
                    a = rng.randint(0, g)
                    st, info, M = node(p, d, g, a, tau, rng, smp=smp)
                    cnt[st] += 1
                    if st != "ok":
                        reasons[info] = reasons.get(info, 0) + 1
                wrong += cnt["WRONG"]
                rows.append(dict(p=p, d=d, kappa=k, h=h, J=smp.J, g=g, tau=str(tau), M=M,
                                 trials=trials, **cnt, reasons=reasons,
                                 abort_rate=cnt["abort"] / trials))
                print(rows[-1], flush=True)
    # abort rate must be <= tau (+ small): check at tau = 1/20 aggregated
    json.dump(dict(rows=rows, wrong=wrong), open(out, "w"), indent=1)
    print("node wrong", wrong)


def task_scaled(out):
    """Theorem H' (j* = 1, switches rescaled to 2^k, random splitting)."""
    import sympy
    rng = random.Random(5)
    rows = []
    for k, p, ns, runs in [(3, 2 ** 31 - 1, [4, 8], 8), (6, 2 ** 61 - 1, [4, 6], 6), (4, 101, [4, 8], 20),
                           (3, 13, [4, 8], 20)]:
        h = (p - 1) // k
        assert (p - 1) % k == 0
        K = (p - 1).bit_length()
        A = (k - 1) * (k - 2)
        inD = lambda x: x == 0 or pow(x, h, p) == 1
        for n in ns:
            reads, ok, tries = [], True, []

            def split(e):
                if e == 0:
                    return 0, 0
                if p < 10 ** 6:  # table by search
                    for u in range(p):
                        if inD(u) and inD((u - e) % p):
                            return u, (u - e) % p
                for c in range(10 ** 5):
                    b = rng.randrange(1, p)
                    u = pow(b, k, p)
                    if inD((u - e) % p):
                        tries.append(c + 1)
                        return u, (u - e) % p
                raise RuntimeError("split cap")

            def solve(dd, y, src):
                if dd == 0:
                    return {src.read(): 1}
                sw = []
                for kk in range(K):
                    while True:
                        idx = [src.read() for _ in range(dd)]
                        al = kernel_vector([src.cols[i] for i in idx], dd - 1, p) if dd > 1 else [1]
                        beta = sum(w * src.cols[i][dd - 1] for i, w in zip(idx, al)) % p
                        if beta:
                            break
                    sc = pow(2, kk, p) * pow(beta, p - 2, p) % p
                    sw.append([(i, split(w * sc % p)) for i, w in zip(idx, al) if w])
                u = [0] * dd
                for blk in sw:
                    for i, (x, xp) in blk:
                        for r in range(dd):
                            u[r] = (u[r] + xp * src.cols[i][r]) % p
                rec = solve(dd - 1, [(y[r] - u[r]) % p for r in range(dd - 1)], src)
                sd = (u[dd - 1] + sum(w * src.cols[i][dd - 1] for i, w in rec.items())) % p
                a = (y[dd - 1] - sd) % p
                res = dict(rec)
                for kk, blk in enumerate(sw):
                    for i, (x, xp) in blk:
                        w = x if (a >> kk) & 1 else xp
                        if w:
                            res[i] = w
                return res

            for _ in range(runs):
                src = Source(gen=lambda: [rng.randrange(p) for _ in range(n)])
                res = solve(n, [0] * n, src)
                good = bool(res) and all(inD(w) and w for w in res.values())
                s = [0] * n
                for i, w in res.items():
                    for r in range(n):
                        s[r] = (s[r] + w * src.cols[i][r]) % p
                good &= not any(s)
                # conversion check on two entries: sigma^k = w
                for w in list(res.values())[:2]:
                    rt = sympy.ntheory.residue_ntheory.nthroot_mod(w, k, p)
                    good &= rt is not None and pow(int(rt), k, p) == w
                ok &= good
                reads.append(len(src.cols))
            exact = 1 + K * Fr(p, p - 1) * n * (n + 1) / 2
            m = sum(reads) / runs
            rows.append(dict(kappa=k, p=str(p), n=n, runs=runs, mean_reads=m, exact=float(exact),
                             all_ok=ok, mean_split_trials=(sum(tries) / len(tries) if tries else None)))
            print(rows[-1], flush=True)
    json.dump(dict(rows=rows), open(out, "w"), indent=1)


def task_neg(out, sp_path):
    sp = load_sp(sp_path)
    rng = random.Random(9)
    res = {}
    # (1) broken table: x - x' != alpha at level 0 -> the exact check must fail on some run
    p, h = 13, 3
    smp = Sampler(p, h, rng, broken=True)
    fails = 0
    for _ in range(40):
        n = 5
        src = Source(gen=lambda: [rng.randrange(p) for _ in range(n)])
        r = smp.run(src, n)
        fails += not check_output(r, src.cols, p, smp.D[0], [0] * n)
    res["broken_table_failed_checks"] = fails
    # (2) wrong depth J = j* - 1 at (3,19): base kernel entries leave D_{J}: weights outside D_0
    p, h = 19, 3
    smp = Sampler(p, h, rng, J=jstar(p, h) - 1)
    bad = 0
    for _ in range(30):
        n = 4
        src = Source(gen=lambda: [rng.randrange(p) for _ in range(n)])
        try:
            r = smp.run(src, n)
            bad += not check_output(r, src.cols, p, smp.D[0], [0] * n)
        except KeyError:  # table lookup of a kernel entry outside D_J
            bad += 1
    res["wrong_depth_bad_runs_of_30"] = bad
    # (3) biased columns {0,1}: reads differ from N_0
    p, h = 13, 3
    smp = Sampler(p, h, rng)
    n = 8
    N = N_table(smp.J, sp[p], n)
    reads, ok = [], True
    for _ in range(60):
        src = Source(gen=lambda: [rng.randrange(2) for _ in range(n)])
        r = smp.run(src, n)
        ok &= check_output(r, src.cols, p, smp.D[0], [0] * n)
        reads.append(len(src.cols))
    m = sum(reads) / len(reads)
    sd = (sum((x - m) ** 2 for x in reads) / (len(reads) - 1)) ** 0.5
    res["biased"] = dict(mean=m, theory=float(N[0][n]), z=(m - float(N[0][n])) / (sd / len(reads) ** 0.5),
                         outputs_ok=ok)
    # (4) hyperplane bank: last coordinate = first coordinate -> node aborts, never wrong
    p, d, g = 13, 4, 3
    smp = Sampler(p, 3, rng)
    st = {"ok": 0, "abort": 0, "WRONG": 0}
    for _ in range(30):
        tau = Fr(1, 2)
        # build a bank: first g labels e_1..e_g, later labels with coord g == coord 1
        t = g
        while Fr(p) ** (t - g) < 2 / tau:
            t += 1
        kb = ceil_log2(2 / tau)
        sig = min(p, math.ceil(2 * math.log2(p - 1)) + 4)
        L = math.ceil(2 * N_table(smp.J, Fr(sig), g)[0][g])
        M = t + kb * L
        bank = [[1 if r == i else 0 for r in range(g)] for i in range(g)]
        while len(bank) < M:
            v = [rng.randrange(p) for _ in range(g)]
            v[g - 1] = v[0]
            bank.append(v)
        s, info, _ = node(p, d, g, g, tau, rng, bank=bank, smp=smp)
        st[s] += 1
    res["hyperplane_bank"] = st
    json.dump(res, open(out, "w"), indent=1)
    print(res)


def task_exponent(out):
    res = {}
    cache = {}

    def jd(p, d):
        k = gcd(d, p - 1)
        if k == 1:
            return 0, "G1"
        if k == p - 1:
            return math.ceil(math.log2(p - 1)), "G0"
        A = (k - 1) * (k - 2)
        if math.sqrt(p) > A + 3:
            return 1, "F"
        key = (p, k)
        if key not in cache:
            cache[key] = jstar(p, (p - 1) // k)
        return cache[key], "F"

    for c in range(2, 13):
        bound = max(((k - 1) * (k - 2) + 3) ** 2 for k in range(2, c + 1))
        best, arg = 0, None
        for p in primes_upto(bound + 1):
            if p <= c:
                continue
            E = 1 + sum(1 + jd(p, d)[0] for d in range(2, c + 1))
            if E > best:
                best, arg = E, p
        res[c] = dict(E_new=best, argmax_p=arg, scan_bound=bound, beyond_bound_at_most=2 * c - 1,
                      E1=1 + sum(d * math.ceil(math.log2(d + 1)) for d in range(2, c + 1)))
        print(c, res[c], flush=True)
    # spot check: beyond the bound the per-grade j is 1 (verified directly on a few primes)
    spot = []
    for p in [3491, 3499, 4001, 5003]:
        for d in range(2, 10):
            k = gcd(d, p - 1)
            if 2 <= k < p - 1:
                spot.append([p, d, k, jstar(p, (p - 1) // k)])
    res["spot_beyond_c9_bound"] = spot
    res["spot_all_one"] = all(s[3] == 1 for s in spot)
    json.dump(res, open(out, "w"), indent=1)


def task_budget(out):
    """Class-nine profile: log2 Q with Cor. H.6 nodes at every Gamma_F grade (owner-decision data)."""
    prof = (19, 17, 16, 14, 12, 9, 6, 3, 1)
    eps = Fr(1, 3)
    c, m = len(prof), prof[0]
    res = {}
    for p in [11, 1031, 5281, 2 ** 31 - 1, 2 ** 61 - 1, 2 ** 127 - 1]:
        t0 = 0
        while Fr(p) ** t0 < 3 / eps:
            t0 += 1
        S = m + t0
        acc = 1
        grades = {}
        for d in range(2, c + 1):
            g = prof[d - 1]
            nd = acc
            k = gcd(d, p - 1)
            if k == 1:
                M = g + 1
                info = "lin"
            elif k == p - 1:
                raise RuntimeError("Gamma_0 not in these rows")
            else:
                h = (p - 1) // k
                A = (k - 1) * (k - 2)
                tau = eps / (9 * (c - 1) * S * nd)
                t = g
                while Fr(p) ** (t - g) < 2 / tau:
                    t += 1
                kb = ceil_log2(2 / tau)
                if p >= (2 * A + 4) ** 2:
                    K = (p - 1).bit_length()
                    Nbar = 1 + K * Fr(p, p - 1) * g * (g + 1) / 2
                    J = 1
                    info = "H'"
                else:
                    J = jstar(p, h)
                    sig = min(p, math.ceil(2 * math.log2(p - 1)) + 4)
                    Nbar = N_table(J, Fr(sig), g)[0][g]
                    info = "H"
                L = math.ceil(2 * Nbar)
                M = t + kb * L
                info += f" k={k} J={J} blocks={kb}"
            grades[d] = (M, info)
            acc *= M
        Q = c * S * acc
        res[str(p)] = dict(log2Q=round(math.log2(Q), 1), grades={d: [round(math.log2(M), 2), i] for d, (M, i) in grades.items()})
        print(p, res[str(p)], flush=True)
    json.dump(res, open(out, "w"), indent=1)


def task_mitm(out):
    """Meet-in-the-middle at about the existence threshold (relevant to proposed F2)."""
    rng = random.Random(3)
    rows = []
    for h, p, a in [(3, 31, 3), (3, 31, 4), (3, 61, 3), (4, 41, 3)]:
        k = (p - 1) // h
        mu = sorted(mu_set(p, h))
        D = [0] + mu
        thr = a * math.log(p) / math.log(h + 1)
        M = math.ceil(thr + math.log(2 * h) / math.log(h + 1)) + 1
        if M % 2:
            M += 1
        succ, work = 0, []
        T = 30
        for _ in range(T):
            X = [[rng.randrange(p) for _ in range(a)] for _ in range(M)]
            half = M // 2
            import itertools
            left = {}
            ops = 0
            for ys in itertools.product(D, repeat=half):
                s = tuple(sum(y * X[i][r] for i, y in enumerate(ys)) % p for r in range(a))
                left.setdefault(s, ys)
                ops += 1
            found = None
            for ys in itertools.product(D, repeat=M - half):
                s = tuple((-sum(y * X[half + i][r] for i, y in enumerate(ys))) % p for r in range(a))
                ops += 1
                if s in left:
                    yl = left[s]
                    if any(yl) or any(ys):
                        found = list(yl) + list(ys)
                        break
            if found:
                tot = [sum(found[i] * X[i][r] for i in range(M)) % p for r in range(a)]
                assert not any(tot) and any(found) and all(f in D for f in found)
                succ += 1
            work.append(ops)
        rows.append(dict(h=h, p=p, kappa=k, a=a, threshold=round(thr, 2), M=M, success=succ / T,
                         mean_ops=sum(work) / T, p_half_a=p ** (a / 2), kappa_a=k ** a,
                         fcs_trials_q_minus_a=round((p / (h + 1)) ** a)))
        print(rows[-1], flush=True)
    json.dump(dict(rows=rows), open(out, "w"), indent=1)


if __name__ == "__main__":
    task, outp = sys.argv[1], sys.argv[2]
    t0 = time.time()
    if task == "depth":
        task_depth(outp)
    elif task == "sp":
        task_sp(outp)
    elif task == "solver":
        task_solver(outp, sys.argv[3])
    elif task == "node":
        task_node(outp)
    elif task == "scaled":
        task_scaled(outp)
    elif task == "neg":
        task_neg(outp, sys.argv[3])
    elif task == "exponent":
        task_exponent(outp)
    elif task == "budget":
        task_budget(outp)
    elif task == "mitm":
        task_mitm(outp)
    print(f"[{task}] {time.time() - t0:.1f}s")
