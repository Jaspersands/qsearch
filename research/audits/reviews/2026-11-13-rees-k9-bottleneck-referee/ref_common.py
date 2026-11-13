"""Referee's own primitives (written from the definitions of appendix-schedule2.tex, sec. app:s2-chains;
no code shared with the report's rc.py / rcdfs.c / chain_exec.py / exponents_*.py).

RC(D; R -> K): alpha in F_p^{Z_D}, beta in F_p^R, alpha_0 + beta_0 in Q^(D)_0 and
  alpha_j + beta_i in {0} u U_{k in K} Q^(D)_{k-i-j}  for all i in R, j in Z_D.
Normal form alpha_0 = 1, beta_0 = 0 (translation, then scaling by (alpha_0+beta_0)^{-1} in P_D).
Classes: ind w.r.t. the least primitive root g, reduced mod D.
"""
import functools, itertools


def factor_set(n):
    s, d = set(), 2
    while d * d <= n:
        while n % d == 0:
            s.add(d); n //= d
        d += 1
    if n > 1:
        s.add(n)
    return s


def is_prime(n):
    return n > 1 and all(n % d for d in range(2, int(n ** .5) + 1))


@functools.lru_cache(None)
def prim_root(p):
    fs = factor_set(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fs):
            return g


@functools.lru_cache(None)
def dlog(p):
    g = prim_root(p)
    L = [None] * p
    x = 1
    for e in range(p - 1):
        L[x] = e
        x = x * g % p
    return g, L


def cls(x, p, D):
    return dlog(p)[1][x % p] % D


def rc_check(p, D, R, K, alpha, beta):
    """beta: dict on R. Direct cell-by-cell check from the definition."""
    g, L = dlog(p)
    Ks = set(k % D for k in K)
    v00 = (alpha[0] + beta[0]) % p
    if v00 == 0 or L[v00] % D != 0:
        return False
    for i in R:
        for j in range(D):
            v = (alpha[j] + beta[i]) % p
            if v and (L[v] % D + i + j) % D not in Ks:
                return False
    return True


class Cap(Exception):
    pass


@functools.lru_cache(None)
def _masks(p, D, K):
    """A[s] = bitmask of y in F_p with y == 0 or cls_D(y) + s in K   (s = i + j mod D)."""
    g, L = dlog(p)
    A = []
    for s in range(D):
        m = 1
        for y in range(1, p):
            if (L[y] + s) % D in K:
                m |= 1 << y
        A.append(m)
    return A


@functools.lru_cache(None)
def _shifted(p, D, K):
    full = (1 << p) - 1
    out = []
    for m in _masks(p, D, K):
        row = [m]
        for b in range(1, p):
            row.append(((m >> b) | (m << (p - b))) & full)
        out.append(row)
    return out


def rc_search(p, D, R, K, cap=None):
    """Complete DFS in normal form. Returns (status, alpha, beta): status 1 feasible, 0 infeasible,
    -1 abandoned at cap nodes."""
    K = tuple(sorted(set(k % D for k in K)))
    R = [0] + sorted(set(i % D for i in R) - {0})
    A = _masks(p, D, K)
    SH = _shifted(p, D, K)   # SH[s][b] = {x : x + b in A[s]}
    # row 0 (beta_0 = 0): alpha_j in A[(0+j)] ; alpha_0 = 1 fixed (cell (0,0) = 1 in Q_0)
    X = [A[j % D] for j in range(D)]
    X[0] = 1 << 1
    if not (A[0] >> 1) & 1:
        return 0, None, None
    rows = R[1:]
    cnt = [0]
    beta = {0: 0}
    # candidates for beta_i: column 0 needs 1 + b allowed in cell (i, 0)
    cand = {i: [b for b in range(p) if (A[i % D] >> ((1 + b) % p)) & 1] for i in rows}

    def rec(t, X):
        if t == len(rows):
            return X
        cnt[0] += 1
        if cap is not None and cnt[0] > cap:
            raise Cap
        i = rows[t]
        S = [SH[(i + j) % D] for j in range(D)]
        for b in cand[i]:
            Y = [None] * D
            Y[0] = X[0]
            ok = True
            for j in range(1, D):
                y = X[j] & S[j][b]
                if not y:
                    ok = False
                    break
                Y[j] = y
            if ok:
                beta[i] = b
                r = rec(t + 1, Y)
                if r is not None:
                    return r
        return None
    try:
        r = rec(0, X)
    except Cap:
        return -1, None, None
    if r is None:
        return 0, None, None
    alpha = [(m & -m).bit_length() - 1 for m in r]   # least element of each X_j
    be = {i: beta[i] for i in R}
    assert rc_check(p, D, R, K, alpha, be), ('own witness rejected', p, D, R, K)
    return 1, alpha, be


def lift(D, K, D2):
    return tuple(x for x in range(D2) if x % D in K)


def subsets0(D):
    return [tuple(sorted((0,) + s)) for r in range(D) for s in itertools.combinations(range(1, D), r)]


def chain_bfs(kap, p, LMAX=None, cap=None):
    """Shortest flexible-line chains. Node (D, K), D | kap, 0 in K subset Z_D, start (1,(0,)).
    Edge (D,K) -> (D2,K2), D | D2, D2 >= 2: RC(D2; lift(K) -> K2) feasible.  Dominance: (D,K0) at level <= l
    dominates (D,K) with K0 subset K (fewer rows next step, smaller output class set).
    Runs to a fixpoint (complete reachability) when LMAX is None.
    Returns level dict, parent dict, number of tests, list of undecided tests."""
    divs = [d for d in range(2, kap + 1) if kap % d == 0]
    level = {(1, (0,)): 0}
    parent = {(1, (0,)): None}
    tests, und = {}, []

    def feas(D, K, D2, K2):
        key = (D2, lift(D, K, D2), K2)
        if key not in tests:
            st, a, b = rc_search(p, D2, key[1], K2, cap=cap)
            if st == -1:
                und.append(key)
            tests[key] = (st, a, b)
        return tests[key][0] == 1

    def dominated(D2, K2):
        return any(D0 == D2 and set(K0) <= set(K2) for (D0, K0) in level)

    front = [(1, (0,))]
    L = 0
    while front and (LMAX is None or L < LMAX):
        L += 1
        new = []
        for (D, K) in front:
            for D2 in divs:
                if D2 % D:
                    continue
                for K2 in sorted(subsets0(D2), key=lambda s: (len(s), s)):
                    if len(K2) == D2:
                        continue
                    if dominated(D2, K2):
                        continue
                    if feas(D, K, D2, K2):
                        level[(D2, K2)] = L
                        parent[(D2, K2)] = (D, K)
                        new.append((D2, K2))
        # keep only non-dominated new nodes on the frontier (strict subsets at same D)
        front = [x for x in new if not any(y[0] == x[0] and set(y[1]) < set(x[1]) for y in level)]
    return level, parent, tests, und


def chain_degrees(kap, level):
    """deg0[K] for K subset Z_kap with 0 in K: least L+1 over reached nodes (D,K0), D > 1, lift(K0) subset K."""
    deg = {}
    for K in subsets0(kap):
        ds = [l + 1 for (D, K0), l in level.items() if D > 1 and set(lift(D, K0, kap)) <= set(K)]
        deg[K] = min(ds) if ds else None
    return deg


def path(parent, node):
    out = []
    while node is not None:
        out.append(node)
        node = parent[node]
    return out[::-1]
