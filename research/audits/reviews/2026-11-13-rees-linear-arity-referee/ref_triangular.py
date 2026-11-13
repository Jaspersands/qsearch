"""Referee re-implementation (written from main.tex prop:triangular-sde, not from the report's
scripts) of the triangular two-level solver with the Lemma K contractions.

kappa = 3: alpha = (1, 0, -b), beta = (0, b, -1), b in C_1, 1 + b in C_2, C_nu = g^nu P.
kappa = 2: alpha = (1, 0), beta = (0, nu - 1), nu the least quadratic non-residue.

Every output is re-verified independently: x_i in P u {0}, x != 0, sum x_i lambda_i = 0,
columns used <= (a+1)(a+2)/2, and every nonzero x_i has an explicit kappa-th root (table).
A negative control runs the same solver with an INVALID b and must fail somewhere.

Usage: /opt/anaconda3/bin/python ref_triangular.py [reps]
"""
import itertools
import random
import sys


def is_prime(n):
    return n > 1 and all(n % q for q in range(2, int(n ** 0.5) + 1))


def prim_root(p):
    fac = [q for q in range(2, p) if (p - 1) % q == 0 and is_prime(q)]
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fac):
            return g
    return 1


class Ctx:
    def __init__(self, p, kappa, gexp=1):
        """Coset generator g = g0^gexp (gexp coprime to kappa), cos(y) = nu iff y in g^nu P."""
        self.p, self.k = p, kappa
        self.h = (p - 1) // kappa
        g0 = prim_root(p)
        self.g = pow(g0, gexp, p)
        self.cls = {pow(self.g, nu * self.h, p): nu for nu in range(kappa)}
        assert len(self.cls) == kappa
        self.root = {}
        for r in range(1, p):
            self.root.setdefault(pow(r, kappa, p), r)

    def cos(self, y):
        return self.cls[pow(y % self.p, self.h, self.p)]

    def inP0(self, y):
        y %= self.p
        return y == 0 or pow(y, self.h, self.p) == 1


def kernel_vector(cols, p):
    """Nonzero x with sum x_j cols[j] = 0 (cols: list of equal-length lists), or None."""
    n = len(cols)
    if n == 0:
        return None
    a = len(cols[0])
    M = [[cols[j][i] % p for j in range(n)] for i in range(a)]
    piv = []
    r = 0
    for c in range(n):
        pr = next((i for i in range(r, a) if M[i][c]), None)
        if pr is None:
            continue
        M[r], M[pr] = M[pr], M[r]
        inv = pow(M[r][c], p - 2, p)
        M[r] = [x * inv % p for x in M[r]]
        for i in range(a):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [(x - f * y) % p for x, y in zip(M[i], M[r])]
        piv.append(c)
        r += 1
        if r == a:
            break
    free = [c for c in range(n) if c not in piv]
    if not free:
        return None
    fc = free[0]
    x = [0] * n
    x[fc] = 1
    for i, c in enumerate(piv):
        x[c] = (-M[i][fc]) % p
    return x


def coords(V, w, p):
    """c with sum c_l V[l] = w (V linearly independent), or None."""
    a = len(w)
    if not V:
        return [] if all(x % p == 0 for x in w) else None
    ker = kernel_vector(V + [[(-x) % p for x in w]], p)
    # V independent: a kernel vector with last coordinate != 0 exists iff w in span(V)
    # (kernel of [V | -w] has dim <= 1, so the kernel vector found is the only one up to scale)
    if ker is None or ker[-1] == 0:
        return None
    inv = pow(ker[-1], p - 2, p)
    return [c * inv % p for c in ker[:-1]]


def lin(coefs, vecs, p, a):
    out = [0] * a
    for c, v in zip(coefs, vecs):
        if c:
            for i in range(a):
                out[i] = (out[i] + c * v[i]) % p
    return out


def tri_solve(cols, C, alpha, beta):
    p, a = C.p, len(cols[0]) if cols and cols[0] is not None else 0
    a = len(cols[0])
    V, rounds, ptr = [], [], 0
    x = [0] * len(cols)
    while True:
        k = len(V)
        m = a - k + 1
        idx = list(range(ptr, ptr + m))
        ptr += m
        if ptr > len(cols):
            raise RuntimeError("ran out of columns")
        lam = [cols[i] for i in idx]
        ker = kernel_vector(lam + [[(-t) % p for t in v] for v in V], p)
        assert ker is not None
        delta = ker[:m]
        assert any(delta), "delta zero although V independent"
        f = next(d for d in delta if d)
        finv = pow(f, p - 2, p)
        delta = [d * finv % p for d in delta]
        e = lin(delta, lam, p, a)
        assert coords(V, e, p) is not None
        bco = [beta[C.cos(d)] * d % p if d else 0 for d in delta]
        v = lin(bco, lam, p, a)
        if coords(V, v, p) is not None:
            for i, d in zip(idx, delta):
                if d:
                    x[i] = d * (alpha[0] + beta[C.cos(d)]) % p
            rho = [(s + t) % p for s, t in zip(e, v)]
            break
        V.append(v)
        rounds.append((idx, delta, e, v))
    tau = [(-t) % p for t in rho]
    for l in range(len(V), 0, -1):
        c = coords(V[:l], tau, p)
        assert c is not None
        z = c[l - 1]
        idx, delta, e, v = rounds[l - 1]
        if z:
            n = C.cos(z)
            for i, d in zip(idx, delta):
                if d:
                    x[i] = z * d * (alpha[n] + beta[C.cos(d)]) % p
            tau = [(t - z * (alpha[n] * s + w)) % p for t, s, w in zip(tau, e, v)]
        assert coords(V[:l - 1], tau, p) is not None
    assert all(t == 0 for t in tau)
    return x, ptr


def verify(cols, x, C, used, a):
    p = C.p
    if not any(x):
        return "zero output"
    if any(not C.inP0(t) for t in x):
        return "weight not in P0"
    s = lin(x, cols, p, a)
    if any(s):
        return "sum nonzero"
    if used > (a + 1) * (a + 2) // 2:
        return "too many columns"
    for t in x:
        if t and pow(C.root[t], C.k, p) != t:
            return "no root"
    if any(x[used:]):
        return "weight beyond used columns"
    return None


def contractions(C):
    p = C.p
    if C.k == 2:
        nu = next(y for y in range(2, p) if C.cos(y) == 1)
        return [((1, 0), (0, (nu - 1) % p))]
    out = []
    for b in range(1, p):
        if C.cos(b) == 1 and (1 + b) % p and C.cos(1 + b) == 2:
            out.append(((1, 0, (-b) % p), (0, b, p - 1)))
    return out


def contraction_ok(C, alpha, beta):
    k = C.k
    for i in range(k):
        for j in range(k):
            y = (alpha[j] + beta[i]) % C.p
            if y and C.cos(y) != (-(i + j)) % k:
                return False
    return alpha[0] == 1 and beta[0] == 0


def banks(C, a, rng):
    p, M = C.p, (a + 1) * (a + 2) // 2
    k = C.k
    g = C.g
    def unit(j, s=1):
        v = [0] * a
        v[j] = s % p
        return v
    def rnd():
        return [rng.randrange(p) for _ in range(a)]
    fam = {}
    fam['random'] = [rnd() for _ in range(M)]
    fam['zero'] = [[0] * a for _ in range(M)]
    fam['sparse'] = [[rng.randrange(p) if rng.random() < 0.2 else 0 for _ in range(a)] for _ in range(M)]
    if a:
        w = rnd()
        fam['rank1_coset1'] = [[pow(g, 1 + k * rng.randrange(p), p) * t % p for t in w] for _ in range(M)]
        fam['rank1_rand'] = [[rng.randrange(p) * t % p for t in w] for _ in range(M)]
        # dead-pair style: e_j with all nontrivial coset multipliers, cycling j, then filler
        cols = []
        for j in itertools.cycle(range(a)):
            for nu in range(k):
                cols.append(unit(j, pow(g, nu, p)))
            if len(cols) >= M:
                break
        fam['dead_cycle'] = cols[:M]
        fam['units_C1'] = [unit(rng.randrange(a), pow(g, 1 + k * rng.randrange(p), p)) for _ in range(M)]
        w2 = rnd()
        fam['repeated'] = [list(w2) for _ in range(M)]
        fam['pm1'] = [[rng.choice((0, 1, p - 1)) for _ in range(a)] for _ in range(M)]
        # low rank 2 with coset-structured coefficients
        u1, u2 = rnd(), rnd()
        fam['rank2_cosets'] = [lin([pow(g, rng.randrange(k), p), pow(g, rng.randrange(k), p) * rng.randrange(2)],
                                   [u1, u2], p, a) for _ in range(M)]
        # triangular / echelon (general position worst case for the rounds)
        fam['echelon'] = [[(rng.randrange(1, p) if i <= (c % (a)) else 0) for i in range(a)] for c in range(M)]
    return fam


def main():
    reps = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    rng = random.Random(20261113)
    runs = fails = 0
    failures = []
    stats = {}
    for kappa, pmax in ((3, 103), (2, 103)):
        for p in range(3, pmax + 1):
            if not is_prime(p) or (p - 1) % kappa:
                continue
            for gexp in ([1, 2] if kappa == 3 else [1]):
                C = Ctx(p, kappa, gexp)
                cons = contractions(C)
                assert cons, ("no contraction", p, kappa)
                for al, be in cons:
                    assert contraction_ok(C, al, be), (p, kappa, al, be)
                for a in range(1, 7):
                    for rep in range(reps):
                        al, be = rng.choice(cons)
                        for name, cols in banks(C, a, rng).items():
                            try:
                                x, used = tri_solve(cols, C, al, be)
                                err = verify(cols, x, C, used, a)
                            except Exception as ex:  # noqa
                                err = f"exception {ex!r}"
                            runs += 1
                            stats[(kappa, name)] = stats.get((kappa, name), 0) + 1
                            if err:
                                fails += 1
                                failures.append((kappa, p, gexp, a, name, err))
    print(f"random/adversarial runs: {runs}, failures: {fails}")
    for f in failures[:10]:
        print("  FAIL", f)
    # every valid b at every p (kappa = 3), a = 3, random bank
    allb = allb_fail = 0
    for p in range(7, 104):
        if not is_prime(p) or p % 3 != 1:
            continue
        for gexp in (1, 2):
            C = Ctx(p, 3, gexp)
            for al, be in contractions(C):
                for a in (2, 4):
                    cols = [[rng.randrange(p) for _ in range(a)] for _ in range((a + 1) * (a + 2) // 2)]
                    x, used = tri_solve(cols, C, al, be)
                    allb += 1
                    if verify(cols, x, C, used, a):
                        allb_fail += 1
    print(f"every valid b, both coset generators, p<=103, a in (2,4): runs {allb}, failures {allb_fail}")
    # exhaustive a = 1
    ex = ex_fail = 0
    for kappa, plist in ((3, [7, 13, 19, 31, 37, 43]), (2, [3, 5, 7, 11, 13, 17, 19, 23])):
        for p in plist:
            for gexp in ([1, 2] if kappa == 3 else [1]):
                C = Ctx(p, kappa, gexp)
                for al, be in contractions(C)[:2]:
                    for t in itertools.product(range(p), repeat=3):
                        cols = [[t[0]], [t[1]], [t[2]]]
                        x, used = tri_solve(cols, C, al, be)
                        ex += 1
                        if verify(cols, x, C, used, 1):
                            ex_fail += 1
    print(f"exhaustive a=1 (all p^3 banks, kappa=3 p<=43, kappa=2 p<=23): runs {ex}, failures {ex_fail}")
    # exhaustive a=2, p=7, kappa=3, columns from a 13-element set (units, multiples, sums) -- all 6-tuples
    C = Ctx(7, 3, 1)
    al, be = contractions(C)[0]
    S = [[1, 0], [0, 1], [3, 0], [0, 3], [1, 1], [1, 3], [2, 5], [0, 0], [6, 1]]
    ex2 = ex2_fail = 0
    for t in itertools.product(range(len(S)), repeat=6):
        cols = [S[i] for i in t]
        x, used = tri_solve(cols, C, al, be)
        ex2 += 1
        if verify(cols, x, C, used, 2):
            ex2_fail += 1
    print(f"exhaustive a=2 p=7 kappa=3 over 9^6 tuples from a fixed 9-set: runs {ex2}, failures {ex2_fail}")
    # random a=2, p=7 and p=13, 20000 banks each
    r2 = r2f = 0
    for p in (7, 13):
        for gexp in (1, 2):
            C = Ctx(p, 3, gexp)
            cons = contractions(C)
            for _ in range(10000):
                cols = [[rng.randrange(p) for _ in range(2)] for _ in range(6)]
                al, be = rng.choice(cons)
                x, used = tri_solve(cols, C, al, be)
                r2 += 1
                if verify(cols, x, C, used, 2):
                    r2f += 1
    print(f"random a=2, p in (7,13), both generators: runs {r2}, failures {r2f}")
    # negative control: invalid b (1 + b in C_1, or b in C_2)
    nc_runs = nc_fail = 0
    for p in (7, 13, 19, 31):
        C = Ctx(p, 3, 1)
        bad = [b for b in range(1, p) if (1 + b) % p and not (C.cos(b) == 1 and C.cos(1 + b) == 2)]
        for b in bad:
            al, be = (1, 0, (-b) % p), (0, b, p - 1)
            for _ in range(30):
                a = 3
                cols = [[rng.randrange(p) for _ in range(a)] for _ in range(10)]
                try:
                    x, used = tri_solve(cols, C, al, be)
                    err = verify(cols, x, C, used, a)
                except Exception as exn:  # noqa
                    err = "exc"
                nc_runs += 1
                if err:
                    nc_fail += 1
    print(f"NEGATIVE CONTROL (invalid b): runs {nc_runs}, detected failures {nc_fail} (must be > 0)")
    print("per-family run counts:", {f"{k}:{n}": c for (k, n), c in sorted(stats.items())})


if __name__ == "__main__":
    main()
