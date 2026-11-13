"""Small exact library for the diagonal-equation (kappa-solution) problem.

A bank is a list of columns lambda_i in F_p^a (tuples of ints mod p).
A kappa-solution is x in (P u {0})^n, x != 0, with sum x_i lambda_i = 0,
where P = (F_p^*)^kappa.  Everything here is exact integer arithmetic mod p.
Interpreter: /opt/anaconda3/bin/python (fpylll parts use the qsearch-cas env).
"""
import itertools
import random


def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def primitive_root(p):
    fac, m, d = [], p - 1, 2
    while d * d <= m:
        if m % d == 0:
            fac.append(d)
            while m % d == 0:
                m //= d
        d += 1
    if m > 1:
        fac.append(m)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fac):
            return g
    return 1  # p = 2


class Field:
    """F_p with coset index cos(y) in Z_kappa: y in g^cos(y) P."""

    def __init__(self, p, kappa):
        assert is_prime(p) and (p - 1) % kappa == 0
        self.p, self.k = p, kappa
        self.g = primitive_root(p)
        self.h = (p - 1) // kappa
        self.dlog = {}
        x = 1
        for e in range(p - 1):
            self.dlog[x] = e
            x = x * self.g % p
        self.P = sorted(y for y in range(1, p) if self.dlog[y] % kappa == 0)
        self.P0 = [0] + self.P
        self.Pset = set(self.P)
        # one kappa-th root per element of P (table)
        self.root = {}
        for r in range(1, p):
            self.root.setdefault(pow(r, kappa, p), r)

    def cos(self, y):
        y %= self.p
        assert y
        return self.dlog[y] % self.k

    def inP0(self, y):
        y %= self.p
        return y == 0 or y in self.Pset

    def coset_elt(self, nu):
        return pow(self.g, nu % self.k, self.p)


# ---------------------------------------------------------------- linear algebra
def rref(rows, p, ncols):
    R = [list(r) for r in rows]
    piv, r = [], 0
    for c in range(ncols):
        pr = next((i for i in range(r, len(R)) if R[i][c] % p), None)
        if pr is None:
            continue
        R[r], R[pr] = R[pr], R[r]
        inv = pow(R[r][c], -1, p)
        R[r] = [v * inv % p for v in R[r]]
        for i in range(len(R)):
            if i != r and R[i][c] % p:
                f = R[i][c]
                R[i] = [(x - f * y) % p for x, y in zip(R[i], R[r])]
        piv.append(c)
        r += 1
    return R[:r], piv


def kernel(cols, p):
    """Basis of {y : sum y_i cols_i = 0}, cols are vectors in F_p^a."""
    n = len(cols)
    if n == 0:
        return []
    a = len(cols[0])
    rows = [[cols[j][i] % p for j in range(n)] for i in range(a)]
    R, piv = rref(rows, p, n)
    free = [c for c in range(n) if c not in piv]
    ker = []
    for fc in free:
        y = [0] * n
        y[fc] = 1
        for i, pc in enumerate(piv):
            y[pc] = (-R[i][fc]) % p
        ker.append(y)
    return ker


def coords(basis, v, p):
    """Coordinates of v in the (independent) basis, or None if v not in span."""
    m = len(basis)
    if m == 0:
        return [] if all(x % p == 0 for x in v) else None
    cols = list(basis) + [[(-x) % p for x in v]]
    ker = kernel(cols, p)
    for y in ker:
        if y[m] % p:
            inv = pow(y[m], -1, p)
            return [yi * inv % p for yi in y[:m]]
    return None


def vadd(u, v, p, s=1):
    return [(x + s * y) % p for x, y in zip(u, v)]


def vscale(u, s, p):
    return [x * s % p for x in u]


def combo(cols, x, p):
    a = len(cols[0])
    out = [0] * a
    for xi, c in zip(x, cols):
        if xi % p:
            for t in range(a):
                out[t] = (out[t] + xi * c[t]) % p
    return out


def is_solution(F, cols, x):
    return (any(xi % F.p for xi in x) and all(F.inP0(xi) for xi in x)
            and all(t == 0 for t in combo(cols, x, F.p)))


# ---------------------------------------------------------------- contractions
def contraction_ok(F, alpha, beta):
    k, p = F.k, F.p
    for i in range(k):
        for j in range(k):
            y = (alpha[j] + beta[i]) % p
            if y and F.cos(y) != (-(i + j)) % k:
                return False
    return True


def explicit_contraction(F):
    """Explicit universal two-level contraction for kappa in {2,3} (this note, Lemma K).

    kappa = 2: alpha = (1, 0), beta = (0, mu), mu = nu - 1 with nu a non-square, mu a square.
    kappa = 3: alpha = (1, 0, -b), beta = (0, b, -1), b in C_1 = gP, 1 + b in C_2 = g^2 P.
    Returns (alpha, beta) or None.  Search is the trivial scan used for the proof check."""
    p, k = F.p, F.k
    if k == 2:
        for nu in range(2, p):
            if F.cos(nu) == 1 and (nu - 1) % p and F.cos(nu - 1) == 0:
                return (1, 0), (0, (nu - 1) % p)
        return None
    if k == 3:
        for b in range(1, p):
            if F.cos(b) == 1 and (1 + b) % p and F.cos(1 + b) == 2:
                return (1, 0, (-b) % p), (0, b, p - 1)
        return None
    raise ValueError


# ---------------------------------------------------------------- triangular solver
def triangular_solve(F, cols, alpha, beta):
    """Proposition triangular-sde (full version), re-implemented from its proof.

    Uses at most (a+1)(a+2)/2 columns.  Returns x (len(cols)) or raises."""
    p, k = F.p, F.k
    a = len(cols[0])
    used = 0
    U = []           # basis v_1..v_k of U_k
    rounds = []      # (indices, delta, e, v) for rounds that extended U
    while True:
        need = a - len(U) + 1
        idx = list(range(used, used + need))
        if idx[-1] >= len(cols):
            raise RuntimeError("ran out of columns")
        used += need
        S = [cols[i] for i in idx]
        # dependency of S modulo U: kernel of [S | U]
        ker = kernel(S + U, p)
        delta = None
        for y in ker:
            if any(y[t] % p for t in range(need)):
                delta = y[:need]
                break
        assert delta is not None
        first = next(t for t in range(need) if delta[t] % p)
        inv = pow(delta[first], -1, p)
        delta = [d * inv % p for d in delta]
        e = combo(S, delta, p)
        v = [0] * a
        for d, c in zip(delta, S):
            if d:
                v = vadd(v, vscale(c, beta[F.cos(d)] * d % p, p), p)
        if coords(U, v, p) is not None:
            x = [0] * len(cols)
            for t, i in enumerate(idx):
                if delta[t]:
                    x[i] = delta[t] * (alpha[0] + beta[F.cos(delta[t])]) % p
            rho = vadd(e, v, p)
            tau = [(-z) % p for z in rho]
            break
        rounds.append((idx, delta, e, v))
        U.append(v)
    for l in range(len(rounds), 0, -1):
        c = coords(U[:l], tau, p)
        assert c is not None
        zeta = c[l - 1]
        if zeta:
            idx, delta, e, v = rounds[l - 1]
            n = F.cos(zeta)
            for t, i in enumerate(idx):
                if delta[t]:
                    x[i] = zeta * delta[t] * (alpha[n] + beta[F.cos(delta[t])]) % p
            tau = vadd(tau, vadd(vscale(e, alpha[n], p), v, p), p, -zeta)
    assert all(t == 0 for t in tau)
    return x


# ---------------------------------------------------------------- brute force
def brute_solvable(F, cols):
    """Exhaustive: does the bank have a kappa-solution?  Enumerates the kernel."""
    p = F.p
    ker = kernel(cols, p)
    if not ker:
        return None
    n = len(cols)
    for coef in itertools.product(range(p), repeat=len(ker)):
        if not any(coef):
            continue
        x = [0] * n
        for c, y in zip(coef, ker):
            if c:
                for i in range(n):
                    x[i] = (x[i] + c * y[i]) % p
        if all(F.inP0(xi) for xi in x):
            return x
    return None


def random_bank(p, a, n, rng):
    return [[rng.randrange(p) for _ in range(a)] for _ in range(n)]


def dead_pair_bank(F, a):
    """a dead pairs: (e_j, -u e_j) with u not in P (no solution can use them)."""
    p = F.p
    u = next(y for y in range(2, p) if (-y) % p and not F.inP0(y))
    # need -(-u)... a pair (e, c e) is dead iff -c not in P; take c = -u, -c = u not in P
    cols = []
    for j in range(a):
        e = [0] * a
        e[j] = 1
        cols.append(e)
        cols.append([(-u) * t % p for t in e])
    return cols
