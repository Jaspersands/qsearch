"""Independent implementation and test of the coset-refinement tower
(2026-11-05-rees-threshold-6.md, Theorem 2.3 / Theorem 4.2). Written by the
tower checker; shares no code with that report's tower.py, rect*.c or verify.py.

Coset classes in the tower and in every final check are computed by
exponentiation (x^((p-1)/D) against powers of xi^((p-1)/D)); the contraction
finder uses a discrete-log table, and every contraction it returns is
re-checked by exponentiation before use.

Usage: python tower_check.py <mode> ...   (see main())
"""
import sys
import random
import numpy as np
from sympy import isprime, primitive_root, factorint, nextprime
from sympy.ntheory.residue_ntheory import nthroot_mod

# ---------------------------------------------------------------- field utils


class Field:
    def __init__(self, p, kappa):
        assert isprime(p) and (p - 1) % kappa == 0
        self.p, self.kappa = p, kappa
        self.xi = primitive_root(p)  # a coset generator for every D | kappa
        self._zeta = {}

    def cls(self, x, D):
        """D-class of x != 0 w.r.t. xi, by exponentiation."""
        p = self.p
        x %= p
        assert x != 0
        if D not in self._zeta:
            z = pow(self.xi, (p - 1) // D, p)
            self._zeta[D] = {pow(z, m, p): m for m in range(D)}
            assert len(self._zeta[D]) == D
        return self._zeta[D][pow(x, (p - 1) // D, p)]

    def in_PD(self, x, D):
        return x % self.p != 0 and pow(x, (self.p - 1) // D, self.p) == 1


def nullvec(cols, p):
    """cols: list of n vectors (length m), n > m. Return nonzero c with sum c_j cols_j = 0."""
    n = len(cols)
    m = len(cols[0]) if n else 0
    A = [[cols[j][i] % p for j in range(n)] for i in range(m)]
    piv_cols, r = [], 0
    for c in range(n):
        pr = next((i for i in range(r, m) if A[i][c]), None)
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        inv = pow(A[r][c], p - 2, p)
        A[r] = [v * inv % p for v in A[r]]
        for i in range(m):
            if i != r and A[i][c]:
                f = A[i][c]
                A[i] = [(vi - f * vr) % p for vi, vr in zip(A[i], A[r])]
        piv_cols.append(c)
        r += 1
        if r == m:
            break
    free = next(c for c in range(n) if c not in piv_cols)
    x = [0] * n
    x[free] = 1
    for i, c in enumerate(piv_cols):
        x[c] = (-A[i][free]) % p
    assert any(x)
    for i in range(m):
        assert sum(cols[j][i] * x[j] for j in range(n)) % p == 0
    return x


# ------------------------------------------------------- contraction checking


def check_rc(F, D, R, K, alpha, beta):
    """RC(D; R -> K): alpha_j + beta_i in {0} u U_{k in K} Q_{k-i-j}, alpha_0+beta_0 in Q_0."""
    p = F.p
    a00 = (alpha[0] + beta[0]) % p
    if a00 == 0 or F.cls(a00, D) != 0:
        return False
    for i in R:
        for j in range(D):
            v = (alpha[j] + beta[i]) % p
            if v == 0:
                continue
            if F.cls(v, D) not in {(k - i - j) % D for k in K}:
                return False
    return True


# -------------------------------------------------------- contraction finding


class Finder:
    """Discrete-log table based search for RC(D; R -> K) at prime p."""

    def __init__(self, F):
        self.F = F
        p = F.p
        t = np.empty(p, dtype=np.int64)
        x = 1
        for e in range(p - 1):
            t[x] = e
            x = x * F.xi % p
        t[0] = -1
        self.dlog = t
        self.xs = np.arange(p, dtype=np.int64)

    def okmask(self, D, i, j, K, y):
        """Boolean over y (array of field elements): cell value y admissible at (i,j)."""
        cl = self.dlog[y] % D
        allowed = np.zeros(D, dtype=bool)
        for k in K:
            allowed[(k - i - j) % D] = True
        if i == 0 and j == 0:
            allowed = np.zeros(D, dtype=bool)
            allowed[0] = True
            return (y != 0) & allowed[cl]
        return (y == 0) | ((y != 0) & allowed[cl])

    def columns_for_beta(self, D, R, K, beta):
        """For fixed beta, return alpha (list) or None."""
        p = self.F.p
        alpha = []
        for j in range(D):
            m = np.ones(p, dtype=bool)
            for i in R:
                m &= self.okmask(D, i, j, K, (self.xs + beta[i]) % p)
                if not m.any():
                    return None
            alpha.append(int(np.flatnonzero(m)[0]))
        return alpha

    def weil_beta(self, D, R):
        p, xi = self.F.p, self.F.xi
        return {i: (0 if i == 0 else (pow(xi, (-i) % (p - 1), p) - 1) % p) for i in R}

    def random_search(self, D, R, K, tries, rng):
        p = self.F.p
        for _ in range(tries):
            beta = {i: (0 if i == 0 else rng.randrange(p)) for i in R}
            al = self.columns_for_beta(D, R, K, beta)
            if al is not None:
                return al, beta
        return None

    def complete_search(self, D, R, K):
        """Complete decision for |R| in {2,3} via FFT correlation over beta (beta_0 = 0)."""
        p = self.F.p
        R = list(R)
        assert R[0] == 0 and len(R) in (2, 3)
        f0 = np.array([self.okmask(D, 0, j, K, self.xs) for j in range(D)], dtype=float)
        g = {i: np.array([self.okmask(D, i, j, K, self.xs) for j in range(D)], dtype=float) for i in R[1:]}
        Gl = np.fft.rfft(g[R[-1]], axis=1)
        if len(R) == 2:
            cnt = np.fft.irfft(np.conj(np.fft.rfft(f0, axis=1)) * Gl, n=p, axis=1)
            good = np.flatnonzero((cnt > 0.5).all(axis=0))
            if len(good) == 0:
                return None
            beta = {0: 0, R[1]: int(good[0])}
        else:
            i1, i2 = R[1], R[2]
            found = None
            for b1 in range(p):
                f1 = f0 * np.roll(g[i1], -b1, axis=1)  # f1[j,x] = f0[j,x] g1[j,x+b1]
                if not (f1.sum(axis=1) > 0.5).all():
                    continue
                cnt = np.fft.irfft(np.conj(np.fft.rfft(f1, axis=1)) * Gl, n=p, axis=1)
                good = np.flatnonzero((cnt > 0.5).all(axis=0))
                if len(good):
                    found = {0: 0, i1: b1, i2: int(good[0])}
                    break
            if found is None:
                return None
            beta = found
        al = self.columns_for_beta(D, R, K, beta)
        assert al is not None
        return al, beta


# ---------------------------------------------------------------- the tower


def chain_of(kappa, order="desc"):
    qs = sorted([q for q, e in factorint(kappa).items() for _ in range(e)], reverse=(order == "desc"))
    Ds = [1]
    for q in qs:
        Ds.append(Ds[-1] * q)
    return Ds


def arity(Ds, a):
    M = a + 1
    for t in range(1, len(Ds)):
        M *= (Ds[t] // Ds[t - 1] - 1) * a + 1
    return M


def tower_solve(F, Ds, contr, lams):
    """contr[t] = (alpha, beta) an RC(D_t; R_t) contraction. lams: list of M columns.
    Returns u with u != 0 and sum u_b^kappa lam_b = 0 (asserted by caller)."""
    p, kappa = F.p, F.kappa
    a = len(lams[0])
    M = len(lams)
    assert M == arity(Ds, a)
    # level 0: groups of a+1 columns; relation dict b->coef, designated index with coef 1
    groups = []
    for s in range(0, M, a + 1):
        idx = list(range(s, s + a + 1))
        v = nullvec([lams[b] for b in idx], p)
        bstar = next(k for k in range(len(v)) if v[k])
        inv = pow(v[bstar], p - 2, p)
        rel = {idx[k]: v[k] * inv % p for k in range(len(v)) if v[k]}
        groups.append((rel, idx[bstar]))
    for t in range(1, len(Ds)):
        D, Dp = Ds[t], Ds[t - 1]
        r = D // Dp
        R = [Dp * m for m in range(r)]
        alpha, beta = contr[t]
        N = (r - 1) * a + 1
        assert len(groups) % N == 0
        new = []
        for s in range(0, len(groups), N):
            chunk = groups[s:s + N]
            V = []
            for rel, bs in chunk:
                assert rel[bs] == 1
                U = {i: [0] * a for i in R}
                for b, c in rel.items():
                    i = F.cls(c, D)
                    assert i in U, "class outside R_t"  # hypothesis (i) of the step lemma
                    for k in range(a):
                        U[i][k] = (U[i][k] + c * lams[b][k]) % p
                assert all(sum(U[i][k] for i in R) % p == 0 for k in range(a))
                V.append([U[i][k] for i in R[1:] for k in range(a)])
            eta = nullvec(V, p)
            nus = next(n for n in range(N) if eta[n])
            inv = pow(eta[nus], p - 2, p)
            eta = [e * inv % p for e in eta]
            out = {}
            for n, (rel, bs) in enumerate(chunk):
                if eta[n] == 0:
                    continue
                j = F.cls(eta[n], D)
                for b, c in rel.items():
                    i = F.cls(c, D)
                    v = eta[n] * (alpha[j] + beta[i]) % p * c % p
                    if v:
                        out[b] = v
            bstar = chunk[nus][1]
            piv = out[bstar]
            assert F.in_PD(piv, D)
            inv = pow(piv, p - 2, p)
            out = {b: v * inv % p for b, v in out.items()}
            assert all(F.in_PD(v, D) for v in out.values())
            new.append((out, bstar))
        groups = new
    assert len(groups) == 1
    rel = groups[0][0]
    u = [0] * M
    for b, c in rel.items():
        assert F.in_PD(c, kappa)
        rts = nthroot_mod(c, kappa, p)
        rt = rts if isinstance(rts, int) else rts[0]
        assert pow(rt, kappa, p) == c
        u[b] = rt
    return u


def final_check(F, lams, u, rng):
    p, kappa = F.p, F.kappa
    a = len(lams[0])
    if not any(u):
        return False
    for k in range(a):
        if sum(pow(ub, kappa, p) * lams[b][k] for b, ub in enumerate(u)) % p:
            return False
    # an exponent d with gcd(d, p-1) = kappa, and the Bezout conversion s = u^t
    from math import gcd
    q1 = (p - 1) // kappa
    while True:
        d1 = rng.randrange(1, 4 * q1 + 5)
        if gcd(d1, q1) == 1:
            break
    d = kappa * d1
    assert gcd(d, p - 1) == kappa
    tt = pow(d1, -1, q1) if q1 > 1 else 1
    s = [pow(ub, tt, p) if ub else 0 for ub in u]
    if not any(s):
        return False
    for k in range(a):
        if sum(pow(sb, d, p) * lams[b][k] for b, sb in enumerate(s)) % p:
            return False
    return True


def column_families(p, a, M, rng):
    fam = {}
    fam["random"] = [[rng.randrange(p) for _ in range(a)] for _ in range(M)]
    fam["zeros"] = [[0] * a for _ in range(M)]
    v = [rng.randrange(1, p) for _ in range(a)]
    fam["all-equal"] = [list(v) for _ in range(M)]
    fam["units"] = [[1 if k == b % a else 0 for k in range(a)] for b in range(M)]
    # rank-1: every column a random multiple of one direction
    fam["rank1-scaled"] = []
    for _ in range(M):
        c = rng.randrange(1, p)
        fam["rank1-scaled"].append([c * x % p for x in v])
    fam["mixed-zero-repeat"] = [([0] * a if b % 3 == 0 else (list(v) if b % 3 == 1 else [rng.randrange(p) for _ in range(a)])) for b in range(M)]
    fam["pairs-cancel"] = []
    for b in range(M):
        if b % 2 == 0:
            w = [rng.randrange(p) for _ in range(a)]
            fam["pairs-cancel"].append(w)
        else:
            fam["pairs-cancel"].append([(-x) % p for x in fam["pairs-cancel"][-1]])
    # small-integer columns (coefficients concentrated near 0/±1)
    fam["small-ints"] = [[rng.choice([0, 1, p - 1]) for _ in range(a)] for _ in range(M)]
    return fam


def get_contractions(F, Ds, rng, mode):
    """mode 'weil': fixed beta of Prop 3.1 where p > W; otherwise random beta, then complete search."""
    fd = Finder(F)
    contr = {}
    how = {}
    for t in range(1, len(Ds)):
        D, Dp = Ds[t], Ds[t - 1]
        r = D // Dp
        R = [Dp * m for m in range(r)]
        res = None
        if mode == "weil" and t >= 2:
            beta = fd.weil_beta(D, R)
            al = fd.columns_for_beta(D, R, [0], beta)
            if al is not None:
                res, how[t] = (al, beta), "weil-beta"
        if res is None:
            res = fd.random_search(D, R, [0], 200, rng)
            how[t] = "random-beta"
        if res is None and r <= 3:
            res = fd.complete_search(D, R, [0])
            how[t] = "complete"
        if res is None:
            return None, how
        assert check_rc(F, D, R, [0], *res)
        contr[t] = res
    return contr, how


def run_tower(kappa, p, a_list, seed, order="desc", mode="random"):
    rng = random.Random(seed)
    F = Field(p, kappa)
    Ds = chain_of(kappa, order)
    contr, how = get_contractions(F, Ds, rng, mode)
    if contr is None:
        return f"kappa={kappa} p={p} chain={Ds[1:]}: NO STEP CONTRACTION ({how})"
    lines = []
    allok = True
    for a in a_list:
        M = arity(Ds, a)
        fam = column_families(p, a, M, rng)
        for name, lams in fam.items():
            perm = list(range(M))
            rng.shuffle(perm)
            lams = [lams[i] for i in perm]
            u = tower_solve(F, Ds, contr, lams)
            ok = final_check(F, lams, u, rng)
            allok &= ok
            if not ok:
                lines.append(f"   FAIL a={a} family={name}")
    return (f"kappa={kappa} p={p} chain={Ds[1:]} steps={how} a={a_list} "
            f"families={len(fam)} -> {'OK' if allok else 'FAIL'}" + ("\n" + "\n".join(lines) if lines else ""))


def primes_1mod(k, lo, n):
    out, x = [], lo
    while len(out) < n:
        x = nextprime(x)
        if (x - 1) % k == 0:
            out.append(x)
    return out


def main():
    mode = sys.argv[1]
    if mode == "tower":
        kappa = int(sys.argv[2])
        ps = [int(x) for x in sys.argv[3].split(",")]
        a_list = [int(x) for x in sys.argv[4].split(",")]
        order = sys.argv[5] if len(sys.argv) > 5 else "desc"
        cmode = sys.argv[6] if len(sys.argv) > 6 else "random"
        for p in ps:
            print(run_tower(kappa, p, a_list, seed=p * 1009 + kappa, order=order, mode=cmode), flush=True)
    elif mode == "weilstep":
        # Prop 3.1: the fixed beta extends, at every prime p = 1 mod D in (W, hi]
        D, m, lo, hi = (int(x) for x in sys.argv[2:6])
        R = list(range(0, D, m))
        fails, n = [], 0
        x = lo
        while True:
            x = nextprime(x)
            if x > hi:
                break
            if (x - 1) % D:
                continue
            F = Field(x, D)
            fd = Finder(F)
            beta = fd.weil_beta(D, R)
            al = fd.columns_for_beta(D, R, [0], beta)
            n += 1
            if al is None or not check_rc(F, D, R, [0], al, beta):
                fails.append(x)
        print(f"weil-beta RC({D},{R}) on primes in ({lo},{hi}]: {n} primes, failures {fails}")
    elif mode == "excset":
        # exceptional set E(D; mZ_D) for primes p = 1 mod modk up to hi; random first, complete if needed
        D, m, hi = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
        modk = int(sys.argv[5]) if len(sys.argv) > 5 else D
        R = list(range(0, D, m))
        rng = random.Random(D * 7 + m)
        exc, n, ncomp = [], 0, 0
        x = 2
        while True:
            x = nextprime(x)
            if x > hi:
                break
            if (x - 1) % modk:
                continue
            n += 1
            F = Field(x, D)
            fd = Finder(F)
            res = fd.random_search(D, R, [0], 60, rng)
            if res is None:
                ncomp += 1
                res = fd.complete_search(D, R, [0])
            if res is None:
                exc.append(x)
            else:
                assert check_rc(F, D, R, [0], *res)
        print(f"E({D};{R}) over {n} primes p=1 mod {modk} up to {hi} (complete searches: {ncomp}): {exc}", flush=True)
    else:
        raise SystemExit("unknown mode")


if __name__ == "__main__":
    main()
