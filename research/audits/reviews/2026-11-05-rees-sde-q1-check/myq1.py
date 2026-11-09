"""Independent re-implementation of ALG-Q1 (report 2026-11-05-rees-sde-q1.md, section 3) for the
referee check.  Written from the report's text only; imports nothing from the authors' code.

- exact arithmetic mod p, own Gaussian elimination, own primitive root and coset classes;
- Theorem-2 forward pass with swaps (own tie rules: the LAST eligible sigma is swapped out, and
  blocks are split by a selectable rule 'last' / 'random' / 'first');
- stall case analysis of the report's table, every inequality of the proof asserted;
- absorption (Lemma R) by an exact minimum-load search (brute force over absorption bases),
  with the code's optional heavy fallbacks (Y- and U-recursion) switchable;
- CODIM1 (closure / top pair / recursion on H);
- backward pass of Lemma 2 by rejection sampling of s (forced value tested on a cross-class
  coincidence), so large primes work;
- (S) checked at every leaf, (F1)/(F2) checked for every flag;
- verify(): independent witness check (x != 0, x_i in P u {0}, sum x_i lambda_i = 0).
"""
import random
from itertools import combinations


# ----------------------------------------------------------------------------- field
class GF:
    def __init__(self, p, k):
        assert (p - 1) % k == 0
        self.p, self.k, self.h = p, k, (p - 1) // k
        n, fac, d = p - 1, [], 2
        while d * d <= n:
            if n % d == 0:
                fac.append(d)
                while n % d == 0:
                    n //= d
            d += 1
        if n > 1:
            fac.append(n)
        g = 2
        while any(pow(g, (p - 1) // f, p) == 1 for f in fac):
            g += 1
        self.g = g
        z = pow(g, self.h, p)
        self.root = {pow(z, j, p): j for j in range(k)}

    def cls(self, y):
        """coset index nu with y in g^nu P (y != 0)."""
        return self.root[pow(y % self.p, self.h, self.p)]

    def inQ0(self, y, c):
        y %= self.p
        return y == 0 or self.cls(y) == c % self.k

    def randP(self, rng):
        while True:
            y = rng.randrange(1, self.p)
            if pow(y, self.h, self.p) == 1:
                return y


def verify(p, k, cols, x):
    """independent witness check."""
    if x is None or len(x) != len(cols) or not any(v % p for v in x):
        return False
    h = (p - 1) // k
    for v in x:
        if v % p and pow(v % p, h, p) != 1:
            return False
    a = len(cols[0])
    return all(sum(x[i] * cols[i][t] for i in range(len(cols))) % p == 0 for t in range(a))


# ----------------------------------------------------------------------------- linear algebra
def coords(gens, v, p):
    """c with sum c_j gens_j = v, or None.  gens need not be independent (returns one solution)."""
    n = len(gens)
    a = len(v)
    if n == 0:
        return [] if not any(x % p for x in v) else None
    # rows = coordinates t, columns = gens + rhs
    A = [[gens[j][t] % p for j in range(n)] + [v[t] % p] for t in range(a)]
    piv = []
    row = 0
    for col in range(n):
        pr = next((i for i in range(row, a) if A[i][col]), None)
        if pr is None:
            continue
        A[row], A[pr] = A[pr], A[row]
        inv = pow(A[row][col], p - 2, p)
        A[row] = [x * inv % p for x in A[row]]
        for i in range(a):
            if i != row and A[i][col]:
                f = A[i][col]
                A[i] = [(x - f * y) % p for x, y in zip(A[i], A[row])]
        piv.append(col)
        row += 1
        if row == a:
            break
    for i in range(row, a):
        if A[i][n]:
            return None
    c = [0] * n
    for i, col in enumerate(piv):
        c[col] = A[i][n]
    return c


def rk(vecs, p):
    basis = []
    for v in vecs:
        if coords(basis, v, p) is None:
            basis.append(v)
    return len(basis), basis


def inspan(basis, v, p):
    return coords(basis, v, p) is not None


def lin(cols, coef, idx, p, a):
    return [sum(coef[i] * cols[i][t] for i in idx) % p for t in range(a)]


# ----------------------------------------------------------------------------- D_3, f
def D3(q):
    return (q + 2) ** 2 // 4 if q > 0 else 0


CC = 3   # budget constant: f(r) = D_3(r) + CC*r (the report uses CC = 3; the referee tests CC = 1)


def f(r, C=None):
    C = CC if C is None else C
    return D3(r) + C * r if r > 0 else 0


# ----------------------------------------------------------------------------- flags
class Rnd:
    def __init__(self, F, cols, S, delta, blocks):
        p, a = F.p, len(cols[0])
        self.S, self.delta = sorted(S), dict(delta)
        self.blocks = [list(G) for G in blocks]
        assert sorted(i for G in self.blocks for i in G) == self.S and all(self.blocks)
        self.bcls = []
        for G in self.blocks:
            cs = {F.cls(self.delta[i]) for i in G}
            assert len(cs) == 1, "block not inside one class"
            self.bcls.append(cs.pop())
        self.W = [lin(cols, self.delta, G, p, a) for G in self.blocks]
        self.e = lin(cols, self.delta, self.S, p, a)
        self.extra = 0


def flag_basis(F, rounds):
    """Check (F1), (F2); return the flag basis (W_1..W_{n-1} of each round, in order) and offsets."""
    p = F.p
    basis, start = [], []
    for R in rounds:
        assert inspan(basis, R.e, p), "(F2) violated"
        start.append(len(basis))
        for w in R.W[1:]:
            assert not inspan(basis, w, p), "(F1) violated"
            basis.append(w)
    return basis, start


def split_rule(F, S, delta, rule, rng, E=3):
    cl = {}
    for i in S:
        cl.setdefault(F.cls(delta[i]), []).append(i)
    blocks = [cl[c] for c in sorted(cl)]
    target = min(E, len(S))
    while len(blocks) < target:
        j = max(range(len(blocks)), key=lambda b: (len(blocks[b]), -b))
        G = list(blocks[j])
        if rule == "random":
            rng.shuffle(G)
            cut = rng.randrange(1, len(G))
        elif rule == "first":
            cut = 1
        else:  # 'last': split off the last element
            cut = len(G) - 1
        blocks[j] = G[:cut]
        blocks.append(G[cut:])
    return blocks


# ----------------------------------------------------------------------------- forward pass
def forward(F, cols, rule, rng, order=None):
    p, a = F.p, len(cols[0])
    M = len(cols)
    order = list(range(M)) if order is None else list(order)
    B, bas = [], []
    for i in order:
        if not inspan(bas, cols[i], p):
            bas.append(cols[i])
            B.append(i)
    r = len(B)
    unused = [i for i in order if i not in set(B)]
    rounds, pool = [], []
    while True:
        U, _ = flag_basis(F, rounds)
        if len(U) == r:
            return dict(status="ok", rounds=rounds, B=B, pool=pool, T=[], r=r)
        T, hit = [], None
        for c in unused:
            co = coords(U + [cols[i] for i in T], cols[c], p)
            if co is None:
                T.append(c)
                continue
            delta = {c: 1}
            for j, i in enumerate(T):
                if co[len(U) + j]:
                    delta[i] = (-co[len(U) + j]) % p
            hit = (c, delta)
            break
        if hit is None:
            return dict(status="stall", rounds=rounds, B=B, pool=pool, T=T, r=r)
        c, delta = hit
        S = sorted(delta)
        if len(S) == 1:
            unused.remove(c)
            g = coords([cols[i] for i in B], cols[c], p)
            outs = [j for j in range(r) if g[j] and not inspan(U, cols[B[j]], p)]
            if outs:
                j = outs[-1]           # own tie rule: last eligible sigma
                unused.append(B[j])
                B[j] = c
            else:
                pool.append(c)
            continue
        for i in S:
            unused.remove(i)
        e = lin(cols, delta, S, p, a)
        if len({F.cls(delta[i]) for i in S}) == 1 and not any(e):
            cc = F.cls(delta[S[0]])
            zeta = pow(F.g, (-cc) % F.k, p)
            x = [0] * M
            for i in S:
                x[i] = zeta * delta[i] % p
            return dict(status="direct", x=x)
        rounds.append(Rnd(F, cols, S, delta, split_rule(F, S, delta, rule, rng)))


# ----------------------------------------------------------------------------- steering, backward
def steer_bad(F, cols, rounds, sources):
    p = F.p
    basis, start = flag_basis(F, rounds)
    cs = []
    for s in sources:
        c = coords(basis, cols[s], p)
        assert c is not None, "source outside realized space"
        cs.append(c)
    ce = [coords(basis, R.e, p) for R in rounds]
    bad = 0
    for j, R in enumerate(rounds):
        n = len(R.blocks)
        for b in range(n):
            for b2 in range(b + 1, n):
                if R.bcls[b] == R.bcls[b2]:
                    continue

                def phi(c):
                    u = c[start[j] + b - 1] if b else 0
                    w = c[start[j] + b2 - 1] if b2 else 0
                    return (u - w) % p
                if any(phi(c) for c in cs) or any(phi(ce[l]) for l in range(j + 1, len(rounds))):
                    continue
                bad += 1
    return bad


def cross_pairs(rounds):
    return sum(1 for R in rounds for b in range(len(R.blocks)) for b2 in range(b + 1, len(R.blocks))
               if R.bcls[b] != R.bcls[b2])


def backward(F, cols, rounds, sources, rng, cap=400000):
    p, a = F.p, len(cols[0])
    M = len(cols)
    basis, start = flag_basis(F, rounds)
    x = [0] * M
    tau = [0] * a
    for s in sources:
        t = F.randP(rng)
        x[s] = t
        tau = [(u - t * v) % p for u, v in zip(tau, cols[s])]
    for j in range(len(rounds) - 1, -1, -1):
        R = rounds[j]
        end = start[j] + len(R.blocks) - 1
        co = coords(basis[:end], tau, p)
        assert co is not None
        beta = [0] + co[start[j]:end]
        n = len(beta)
        # cross-class coincidence?
        forced = None
        for b in range(n):
            for b2 in range(b + 1, n):
                if beta[b] == beta[b2] and R.bcls[b] != R.bcls[b2]:
                    forced = (-beta[b]) % p
        ok = lambda s: all(F.inQ0(beta[b] + s, -R.bcls[b]) for b in range(n))
        if forced is not None:
            if not ok(forced):
                return None
            s = forced
        else:
            s = None
            for _ in range(cap):
                z = rng.randrange(p)
                if ok(z):
                    s = z
                    break
            if s is None:
                return None
        for b, G in enumerate(R.blocks):
            for i in G:
                x[i] = R.delta[i] * (beta[b] + s) % p
        val = lin(cols, x, R.S, p, a)
        tau = [(u - v) % p for u, v in zip(tau, val)]
    assert not any(tau), "residual"
    return x


# ----------------------------------------------------------------------------- absorption
def absorb_set(F, cols, rounds, seq):
    """Lemma R: absorb the round columns in seq, in order.  Asserts Lemma R's 'moreover'."""
    p = F.p
    rounds = [r for r in rounds]
    for i in seq:
        U, _ = flag_basis(F, rounds)
        assert not inspan(U, cols[i], p)
        l = next(l for l, R in enumerate(rounds) if i in R.S)
        R = rounds[l]
        b = next(b for b, G in enumerate(R.blocks) if i in G)
        assert len(R.blocks[b]) >= 2, "Lemma R 'moreover' violated"
        nb = [list(G) for G in R.blocks]
        nb[b] = [j for j in nb[b] if j != i]
        nb.append([i])
        R2 = Rnd(F, cols, R.S, R.delta, nb)
        R2.extra = R.extra + 1
        rounds[l] = R2
        U2, _ = flag_basis(F, rounds)
        assert len(U2) == len(U) + 1, "Lemma R dimension"
    return rounds


def min_load_basis(F, cols, rounds, U, need, maxcomb=200000):
    """Exact minimum over absorption bases (need round columns independent mod U) of the max number
    taken from one round.  Brute force over subsets of Rout (bounded)."""
    p = F.p
    if need == 0:
        return (0, []), False
    Rout = [i for R in rounds for i in R.S if not inspan(U, cols[i], p)]
    owner = {i: l for l, R in enumerate(rounds) for i in R.S}
    best = None
    cnt = 0
    for C in combinations(Rout, need):
        cnt += 1
        if cnt > maxcomb:
            break
        load = max(sum(1 for i in C if owner[i] == l) for l in set(owner[i] for i in C))
        if best is not None and load >= best[0]:
            continue
        if rk(U + [cols[i] for i in C], p)[0] == len(U) + need:
            best = (load, list(C))
            if load == 1 or load == -(-need // len(rounds)):
                pass
    return best, cnt > maxcomb


# ----------------------------------------------------------------------------- ALG-Q1
class Fail(Exception):
    pass


def solve(F, cols, rng, rule="last", fallback=True, passes=8, trace=None, depth=0, check_counts=True):
    p, a = F.p, len(cols[0])
    M = len(cols)
    trace = [] if trace is None else trace
    for i, c in enumerate(cols):
        if not any(v % p for v in c):
            x = [0] * M
            x[i] = 1
            trace.append((depth, "zero", {}))
            return x
    r = rk(cols, p)[0]
    if check_counts:
        assert M >= f(r), ("budget", M, f(r))
    st = forward(F, cols, rule, rng)
    if st["status"] == "direct":
        trace.append((depth, "direct", {}))
        return st["x"]
    rounds, B = st["rounds"], st["B"]
    if st["status"] == "ok":
        return leaf(F, cols, rounds, B, rng, passes, trace, depth, "thm2", 0)
    U, _ = flag_basis(F, rounds)
    q = r - len(U)
    pool, T = st["pool"], st["T"]
    Rcols = [i for R in rounds for i in R.S]
    assert len(Rcols) <= D3(r) - D3(q), "Theorem 2(b) round count"
    assert M == r + len(Rcols) + len(pool) + len(T) and len(T) <= q
    inU = [i for i in range(M) if inspan(U, cols[i], p)]
    Fr = [i for i in range(M) if i not in set(Rcols)]
    Fin = [i for i in Fr if i in set(inU)]
    BinU = [i for i in B if i in set(inU)]
    b = len(BinU)
    assert rk([cols[i] for i in BinU], p)[0] == b
    assert rk([cols[i] for i in Fin], p)[0] == b, "Corollary A: Fin spans span(B cap U)"
    assert len(B) - b == r - b
    eps = len(U) - b
    assert len(pool) >= 1 and b >= 1 and r >= 2
    assert len(pool) >= (CC - 1) * r + D3(q) - q if M >= f(r) else True
    Up = rk([cols[i] for i in Rcols], p)[1]
    qplus = r - len(Up)
    info = dict(r=r, q=q, qplus=qplus, b=b, eps=eps, pi=len(pool), T=len(T))
    trace.append((depth, "stall", info))
    if eps == 0:
        return leaf(F, cols, rounds, Fin, rng, passes, trace, depth, "closure", 0)
    if q >= 3 and b <= q - 2:
        Y = rk([cols[i] for i in BinU], p)[1]
        idx = [i for i in range(M) if inspan(Y, cols[i], p)]
        assert len(idx) >= f(b), ("case 2 count", len(idx), f(b))
        trace.append((depth, "rec-Y", dict(dim=b, cols=len(idx))))
        return recurse(F, cols, idx, rng, rule, fallback, passes, trace, depth)
    if qplus >= 2:
        idx = [i for i in range(M) if inspan(Up, cols[i], p)]
        assert M - len(idx) <= r + 1, "case 3: |X| <= r+1"
        assert len(idx) >= f(r - qplus), ("case 3 count", len(idx), f(r - qplus))
        trace.append((depth, "rec-U+", dict(dim=r - qplus, cols=len(idx))))
        return recurse(F, cols, idx, rng, rule, fallback, passes, trace, depth)
    need = q - qplus
    best, trunc = min_load_basis(F, cols, rounds, U, need)
    assert best is not None, "no absorption basis (Lemma R)"
    load, seq = best
    if q <= 2:
        assert load <= 2
    else:
        assert b >= q - 1 and r >= 2 * q and load <= r // 2
    if load >= 3:
        Y = rk([cols[i] for i in BinU], p)[1]
        colsY = sum(1 for i in range(M) if inspan(Y, cols[i], p))
        colsU = len(inU)
        hinfo = dict(info, load=load, trunc=trunc, colsY=colsY, fY=f(b), colsU=colsU, fU=f(r - q),
                     rounds=[(len(R.S), len(R.blocks), sum(1 for i in R.S if i not in set(inU)))
                             for R in rounds])
        trace.append((depth, "heavy", hinfo))
        if fallback and colsY >= f(b):
            idx = [i for i in range(M) if inspan(Y, cols[i], p)]
            trace.append((depth, "rec-Y", dict(dim=b, cols=len(idx))))
            return recurse(F, cols, idx, rng, rule, fallback, passes, trace, depth)
        if fallback and colsU >= f(r - q):
            trace.append((depth, "rec-U", dict(dim=r - q, cols=len(inU))))
            return recurse(F, cols, inU, rng, rule, fallback, passes, trace, depth)
    rounds2 = absorb_set(F, cols, rounds, seq)
    U2, _ = flag_basis(F, rounds2)
    assert len(U2) == len(Up)
    trace.append((depth, "absorb", dict(dirs=need, load=load)))
    if qplus == 0:
        return leaf(F, cols, rounds2, B, rng, passes, trace, depth, "absorb-leaf", load)
    # CODIM1, H = U+
    H = U2
    assert all(inspan(H, cols[i], p) for i in Rcols)
    FinH = [i for i in Fr if inspan(H, cols[i], p)]
    X = [i for i in Fr if not inspan(H, cols[i], p)]
    if rk([cols[i] for i in FinH], p)[0] == len(H):
        return leaf(F, cols, rounds2, FinH, rng, passes, trace, depth, "codim1-closure", load)
    if len(X) >= 3:
        # Lemma T': every pair works; test all pairs for (S), use a random one
        nbad = 0
        prs = list(combinations(X, 2))
        for (a1, a2) in prs:
            top = toppair(F, cols, H, a1, a2)
            src = [i for i in Fr if i not in (a1, a2)]
            nbad += steer_bad(F, cols, rounds2 + [top], src) > 0
        assert nbad == 0, "Lemma T' violated"
        a1, a2 = rng.choice(prs)
        top = toppair(F, cols, H, a1, a2)
        src = [i for i in Fr if i not in (a1, a2)]
        trace.append((depth, "top-pair-checked", dict(pairs=len(prs))))
        return leaf(F, cols, rounds2 + [top], src, rng, passes, trace, depth, "top-pair", load)
    idx = [i for i in range(M) if inspan(H, cols[i], p)]
    assert len(idx) == M - len(X) and len(idx) >= f(r - 1), "CODIM1 count"
    trace.append((depth, "rec-H", dict(dim=r - 1, cols=len(idx))))
    return recurse(F, cols, idx, rng, rule, fallback, passes, trace, depth)


def toppair(F, cols, H, a1, a2):
    p = F.p
    co = coords(H + [cols[a2]], cols[a1], p)
    assert co is not None and co[-1] % p
    delta = {a1: 1, a2: (-co[-1]) % p}
    return Rnd(F, cols, [a1, a2], delta, [[a1], [a2]])


def leaf(F, cols, rounds, src, rng, passes, trace, depth, kind, load):
    nbad = steer_bad(F, cols, rounds, src)
    assert nbad == 0, ("(S) fails at leaf", kind, nbad)
    nmax = max([len(R.blocks) for R in rounds] + [0])
    assert nmax <= 3 + load
    rho = cross_pairs(rounds)
    dimU = len(flag_basis(F, rounds)[0])
    assert rho <= (3 + load) * dimU / 2
    fails = 0
    for _ in range(passes):
        x = backward(F, cols, rounds, src, rng)
        if x is not None:
            assert verify(F.p, F.k, cols, x), "invalid witness"
            trace.append((depth, kind, dict(load=load, nmax=nmax, rho=rho, fails=fails)))
            return x
        fails += 1
    trace.append((depth, kind, dict(load=load, nmax=nmax, rho=rho, fails=fails, unsolved=True)))
    return None


def recurse(F, cols, idx, rng, rule, fallback, passes, trace, depth):
    p = F.p
    _, sub = rk([cols[i] for i in idx], p)
    sc = [coords(sub, cols[i], p) for i in idx]
    y = solve(F, sc, rng, rule, fallback, passes, trace, depth + 1)
    if y is None:
        return None
    x = [0] * len(cols)
    for j, i in enumerate(idx):
        x[i] = y[j]
    assert verify(p, F.k, cols, x)
    return x
