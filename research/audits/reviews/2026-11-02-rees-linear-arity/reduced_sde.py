"""Reduced-relation collision schemes for  sum_i x_i lambda_i = 0,  x in P^M \\ {0}.

P = {0} U (F_p^*)^kappa.  A witness x gives s_i = x_i^{1/kappa}, then a Bezout
exponent u (u*d = kappa mod p-1) turns it into a solution of sum s_i^d lambda_i = 0.

Unnormalised coordinates.  A level-t object is a list of entries
(column, coef, m) with m in Z_kappa^t; coef is the product of the dependency
coefficients gamma_1..gamma_t on the path to the column, and m_s is the coset
of gamma_s (gamma in g^{m} H).  Its cell tensor is T_m = sum coef * lambda.

Contraction.  F : Z_kappa^L -> F_p with F(m) in Q_{-|m|} U {0}, F(0) != 0, and
Prod_t (1 - pi_t) F = 0  (pi_t = average over axis t).  The final weight of a
column is x = coef * F(m), which lies in P.  Telescoping,
    F = sum_t H_t,   H_t = pi_t Prod_{s<t} (1 - pi_s) F   (independent of m_t),
and  sum_m F(m) T_m = sum_t sum_K coef(K, m_{>t}) * sum_{m_<t} H_t(m_<t, m_>t) R^K_{m_<t},
with R^K the level-t residual.  So level t only has to kill the functionals
phi_{m_>t} = H_t(., m_>t): r_t = rank(H_t as an (m_<t) x (m_>t) matrix) linear
conditions per coordinate, i.e. r_t * q + 1 lower objects in a q-dim quotient.

Schemes
  product    : levels 1..L with U = 0; arity prod_t (r_t a + 1).
  triangular : top level is replaced by a back-substitution over flexible
               vectors v = sum H_L(m) T_m built in quotients F_p^a / U;
               arity sum_{q=1}^{a} prod_{t<L} (r_t q + 1) + 1.
For L = 2 with the decoupled two-level contraction F(m1, m2) = alpha_{m2} +
beta_{m1}: r_1 = r_2 = 1, arity (a+1)^2 (product) or (a+1)(a+2)/2 (triangular),
against Schedule 2's (a+1)((kappa-1)a+1).

Every witness is checked exactly: x_i in P, x != 0, sum x_i lambda_i = 0 mod p.

Usage
  python reduced_sde.py two  p kappa a N [scheme] [family]
  python reduced_sde.py llev p kappa L a N [scheme] [family]   (needs pycosat)
  python reduced_sde.py ranks p kappa L                         (SAT contraction ranks)
"""
import itertools
import random
import sys

from sympy import primitive_root, factorint


class Field:
    def __init__(self, p, k):
        assert (p - 1) % k == 0 and k >= 1
        self.p, self.k, self.h = p, k, (p - 1) // k
        self.g = primitive_root(p) if p < 10**7 else self._prim_root_big()
        self.w = pow(self.g, self.h, p)
        self.wpow = {pow(self.w, m, p): m for m in range(k)}

    def _prim_root_big(self):
        p = self.p
        fac = list(factorint(p - 1).keys())
        g = 2
        while any(pow(g, (p - 1) // q, p) == 1 for q in fac):
            g += 1
        return g

    def coset(self, x):
        x %= self.p
        assert x
        return self.wpow[pow(x, self.h, self.p)]

    def inP(self, x):
        x %= self.p
        return x == 0 or pow(x, self.h, self.p) == 1


# ---------------------------------------------------------------- linear algebra mod p

def kernel_basis(cols, p):
    """Basis of {y : sum_j y_j cols[j] = 0} (cols: list of equal-length vectors)."""
    n = len(cols)
    if n == 0:
        return []
    m = len(cols[0])
    A = [[cols[j][i] % p for j in range(n)] for i in range(m)]
    piv_cols, r = [], 0
    for c in range(n):
        pr = next((i for i in range(r, m) if A[i][c]), None)
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        inv = pow(A[r][c], -1, p)
        A[r] = [v * inv % p for v in A[r]]
        for i in range(m):
            if i != r and A[i][c]:
                f = A[i][c]
                A[i] = [(vi - f * vr) % p for vi, vr in zip(A[i], A[r])]
        piv_cols.append(c)
        r += 1
        if r == m:
            break
    free = [c for c in range(n) if c not in piv_cols]
    basis = []
    for fc in free:
        y = [0] * n
        y[fc] = 1
        for i, pc in enumerate(piv_cols):
            y[pc] = (-A[i][fc]) % p
        basis.append(y)
    return basis


def solve_in_span(basis, target, p):
    """Coordinates t with sum t_l basis[l] = target, or None."""
    ker = kernel_basis(list(basis) + [target], p)
    for y in ker:
        if y[-1]:
            inv = pow(-y[-1], -1, p)
            return [v * inv % p for v in y[:-1]]
    return None


def rank_mod(rows, p):
    if not rows:
        return 0
    return len(rows[0]) - len(kernel_basis([list(c) for c in zip(*rows)], p)) if rows else 0


# ---------------------------------------------------------------- contractions

def two_level_contraction(Fd, rng=None, dfs_limit=20000):
    """(alpha, beta) with alpha_j + beta_i in Q_{-(i+j)} U {0}, alpha_0 = 1, beta_0 = 0.
    Explicit beta_i = g^{-i} - 1 (Theorem 2 of the small-prime report) with alpha by
    search; complete DFS over beta for small p.  Returns None if none exists (small p)."""
    p, k = Fd.p, Fd.k

    def ok(x, i, j):
        x %= p
        return x == 0 or Fd.coset(x) == (-(i + j)) % k

    def alphas_for(beta, trials):
        alpha = [1] + [None] * (k - 1)
        for j in range(1, k):
            cands = range(1, p) if p <= dfs_limit else (rng.randrange(1, p) for _ in range(trials))
            for x in cands:
                if all(ok(x + beta[i], i, j) for i in range(k)):
                    alpha[j] = x
                    break
            if alpha[j] is None:
                return None
        return alpha

    rng = rng or random.Random(1)
    gi = pow(Fd.g, -1, p)
    beta = [0] + [(pow(gi, i, p) - 1) % p for i in range(1, k)]
    alpha = alphas_for(beta, 50 * k ** k)
    if alpha is not None:
        return alpha, beta
    if p > dfs_limit:
        return None
    # complete DFS over beta (small p only)
    A = [set(x for x in range(p) if x == 0 or Fd.coset(x) == m) for m in range(k)]
    S0 = [set(A[(-j) % k]) for j in range(k)]
    cand = [sorted((x - 1) % p for x in A[(-i) % k]) for i in range(k)]
    beta = [0] * k

    def dfs(i, S):
        if i == k:
            return S
        for b in cand[i]:
            T = list(S)
            good = True
            for j in range(1, k):
                T[j] = S[j] & {(x - b) % p for x in A[(-(i + j)) % k]}
                if not T[j]:
                    good = False
                    break
            if good:
                beta[i] = b
                r = dfs(i + 1, T)
                if r is not None:
                    return r
        return None

    S = dfs(1, S0)
    if S is None:
        return None
    alpha = [1] + [min(S[j]) for j in range(1, k)]
    return alpha, list(beta)


def F_from_two_level(Fd, alpha, beta):
    k = Fd.k
    return {(m1, m2): (alpha[m2] + beta[m1]) % Fd.p for m1 in range(k) for m2 in range(k)}


def F_from_llevel_C(Fd, L, C):
    """Convert a normalised contraction C (llevel.py, z_i = g^i) to F(m) = C_m / prod z_{m_t}."""
    p = Fd.p
    out = {}
    for m, c in C.items():
        z = 1
        for mt in m:
            z = z * pow(Fd.g, mt, p) % p
        out[m] = c * pow(z, -1, p) % p
    return out


def check_contraction(Fd, L, F):
    p, k = Fd.p, Fd.k
    if F[(0,) * L] % p == 0:
        return False
    for m, v in F.items():
        if v % p and Fd.coset(v) != (-sum(m)) % k:
            return False
    # Prod_t (1 - pi_t) F = 0
    G = dict(F)
    for t in range(L):
        G = apply_center(G, t, k, p)
    return all(v % p == 0 for v in G.values())


def apply_pi(G, t, k, p):
    inv = pow(k, -1, p)
    out = {}
    for m in G:
        s = 0
        for v in range(k):
            mm = m[:t] + (v,) + m[t + 1:]
            s += G[mm]
        out[m] = s * inv % p
    return out


def apply_center(G, t, k, p):
    P = apply_pi(G, t, k, p)
    return {m: (G[m] - P[m]) % p for m in G}


def telescoped(F, L, k, p):
    """H_t = pi_t prod_{s<t} (1 - pi_s) F for t = 0..L-1 (0-based axes)."""
    Hs = []
    G = dict(F)
    for t in range(L):
        Hs.append(apply_pi(G, t, k, p))
        G = apply_center(G, t, k, p)
    return Hs


def functionals(H, t, L, k, p):
    """Independent functionals phi(m_<t) = H(m_<t, *, m_>t) over the columns m_>t.
    Returns list of dicts m_<t -> value; length r_t."""
    lows = list(itertools.product(range(k), repeat=t))
    highs = list(itertools.product(range(k), repeat=L - t - 1))
    vecs = []
    for hi in highs:
        vecs.append([H[lo + (0,) + hi] for lo in lows])
    # greedy independent subset
    chosen = []
    for v in vecs:
        if rank_mod(chosen + [v], p) > len(chosen):
            chosen.append(v)
    return [dict(zip(lows, v)) for v in chosen]


# ---------------------------------------------------------------- objects

class Pool:
    def __init__(self, cols):
        self.cols, self.next = cols, 0

    def take(self):
        if self.next >= len(self.cols):
            raise RuntimeError("out of columns")
        i = self.next
        self.next += 1
        return i


def cells(obj, cols, a, p):
    T = {}
    for (c, coef, m) in obj:
        v = T.setdefault(m, [0] * a)
        lam = cols[c]
        for i in range(a):
            v[i] = (v[i] + coef * lam[i]) % p
    return T


def apply_functional(obj, phi, cols, a, p):
    out = [0] * a
    for (c, coef, m) in obj:
        f = phi.get(m, 0)
        if f:
            lam = cols[c]
            for i in range(a):
                out[i] = (out[i] + f * coef * lam[i]) % p
    return out


def build(level, Fd, funcs, pool, U, a):
    """Build a level-`level` object (level >= 0) whose relations at levels 1..level hold
    modulo span(U).  funcs[t] = functionals for level t+1 (0-based t)."""
    p = Fd.p
    if level == 0:
        c = pool.take()
        return [(c, 1, ())]
    phis = funcs[level - 1]
    q = a - len(U)
    n_children = len(phis) * q + 1
    children = [build(level - 1, Fd, funcs, pool, U, a) for _ in range(n_children)]
    if not phis:
        gamma = [1]
    else:
        # unknowns gamma (n_children) and mu (len(phis) * len(U)); equations per phi: a coords
        big_cols = []
        for ch in children:
            col = []
            for phi in phis:
                col += apply_functional(ch, phi, pool.cols, a, p)
            big_cols.append(col)
        for jj in range(len(phis)):
            for u in U:
                col = [0] * (a * len(phis))
                col[jj * a:(jj + 1) * a] = [(-x) % p for x in u]
                big_cols.append(col)
        ker = kernel_basis(big_cols, p)
        gamma = None
        for y in ker:
            if any(y[:n_children]):
                gamma = y[:n_children]
                break
        assert gamma is not None, "no dependency (U not independent?)"
    first = next(g for g in gamma if g)
    inv = pow(first, -1, p)
    gamma = [g * inv % p for g in gamma]
    obj = []
    for g, ch in zip(gamma, children):
        if g:
            mt = Fd.coset(g)
            for (c, coef, m) in ch:
                obj.append((c, coef * g % p, m + (mt,)))
    return obj


def weights_from(obj, top_coef, n_top, F, Fd, x):
    p = Fd.p
    for (c, coef, m) in obj:
        key = m + ((n_top,) if n_top is not None else ())
        x[c] = (x[c] + top_coef * coef * F[key]) % p


def solve_product(Fd, L, F, cols, a):
    p = Fd.p
    Hs = telescoped(F, L, Fd.k, p)
    funcs = [functionals(Hs[t], t, L, Fd.k, p) for t in range(L)]
    pool = Pool(cols)
    top = build(L, Fd, funcs, pool, [], a)
    x = [0] * len(cols)
    weights_from(top, 1, None, F, Fd, x)
    return x, pool.next, [len(f) for f in funcs]


def solve_triangular(Fd, L, F, cols, a):
    p = Fd.p
    Hs = telescoped(F, L, Fd.k, p)
    funcs = [functionals(Hs[t], t, L, Fd.k, p) for t in range(L - 1)]
    HL = {m[:-1]: v for m, v in Hs[L - 1].items() if m[-1] == 0}   # independent of m_L
    pool = Pool(cols)
    U, objs = [], []
    while True:
        obj = build(L - 1, Fd, funcs, pool, U, a)
        v = apply_functional(obj, HL, cols, a, p)
        degenerate = (not any(v)) or len(U) == a or (U and solve_in_span(U, v, p) is not None)
        if degenerate:
            # degenerate / final: realise with top coefficient 1 (coset 0); lies in span(U)
            x = [0] * len(cols)
            weights_from(obj, 1, 0, F, Fd, x)
            break
        U.append(v)
        objs.append(obj)
    # back-substitution
    tau = [0] * a
    for (c, xc) in enumerate(x):
        if xc:
            for i in range(a):
                tau[i] = (tau[i] - xc * cols[c][i]) % p
    for l in range(len(objs) - 1, -1, -1):
        coords = solve_in_span(U[:l + 1], tau, p)
        assert coords is not None, "target left the span"
        cl = coords[l]
        if cl:
            n = Fd.coset(cl)
            before = list(x)
            weights_from(objs[l], cl, n, F, Fd, x)
            for c in range(len(cols)):
                d = (x[c] - before[c]) % p
                if d:
                    for i in range(a):
                        tau[i] = (tau[i] - d * cols[c][i]) % p
    assert not any(tau), "back-substitution left a residue"
    return x, pool.next, [len(f) for f in funcs] + [1]


def check_witness(Fd, cols, x):
    p = Fd.p
    if not any(v % p for v in x):
        return False, "zero"
    if not all(Fd.inP(v) for v in x):
        return False, "not in P"
    a = len(cols[0])
    for i in range(a):
        if sum(v * c[i] for v, c in zip(x, cols)) % p:
            return False, "nonzero sum"
    return True, "ok"


def sde_roots(Fd, x, d):
    """s with s^d = x_i for d with gcd(d, p-1) = kappa (small p): root table + Bezout."""
    p, k = Fd.p, Fd.k
    from math import gcd
    assert gcd(d, p - 1) == k
    root = {}
    for y in range(1, p):
        root.setdefault(pow(y, k, p), y)
    # u*d = k mod (p-1)
    dd, mod = d // k, (p - 1) // k
    u = pow(dd, -1, mod) if mod > 1 else 1
    return [0 if v % p == 0 else pow(root[v % p], u, p) for v in x]


# ---------------------------------------------------------------- instance families

def family(name, rng, p, a, M):
    if name == "random":
        return [[rng.randrange(p) for _ in range(a)] for _ in range(M)]
    if name == "basis":       # repeated unit vectors (zero-sum-free style)
        return [[1 if i == (j % a) else 0 for i in range(a)] for j in range(M)]
    if name == "scaled":      # e_i and mu*e_i with -mu non-residue-ish, plus random tail
        out = []
        for j in range(M):
            v = [0] * a
            v[j % a] = 1 if (j // a) % 2 == 0 else rng.randrange(1, p)
            out.append(v)
        return out
    if name == "lowrank":     # columns in a 1-dim space
        u = [rng.randrange(1, p) for _ in range(a)]
        return [[rng.randrange(1, p) * ui % p for ui in u] for _ in range(M)]
    if name == "sparse":
        return [[rng.randrange(p) if rng.random() < 0.3 else 0 for _ in range(a)] for _ in range(M)]
    raise ValueError(name)


FAMILIES = ["random", "basis", "scaled", "lowrank", "sparse"]


def arity_formula(L, r, a, scheme):
    if scheme == "product":
        out = 1
        for rt in r:
            out *= rt * a + 1
        return out
    tot = 1
    for q in range(1, a + 1):
        t = 1
        for rt in r[:-1]:
            t *= rt * q + 1
        tot += t
    return tot


def run(Fd, L, F, a, N, scheme, fams, seed=0, d=None):
    rng = random.Random(seed)
    Hs = telescoped(F, L, Fd.k, Fd.p)
    r = [len(functionals(Hs[t], t, L, Fd.k, Fd.p)) for t in range(L)]
    M = arity_formula(L, r, a, scheme)
    res = []
    for fam in fams:
        for it in range(N):
            cols = family(fam, rng, Fd.p, a, M)
            if scheme == "product":
                x, used, _ = solve_product(Fd, L, F, cols, a)
            else:
                x, used, _ = solve_triangular(Fd, L, F, cols, a)
            good, why = check_witness(Fd, cols, x)
            if good and d is not None:
                s = sde_roots(Fd, x, d)
                good = all(pow(si, d, Fd.p) == xi % Fd.p for si, xi in zip(s, x)) and any(s)
                why = "sde ok" if good else "sde fail"
            res.append((fam, it, used, good, why))
            assert used <= M, (used, M)
    return r, M, res


def main():
    mode = sys.argv[1]
    if mode == "two":
        p, k, a, N = map(int, sys.argv[2:6])
        scheme = sys.argv[6] if len(sys.argv) > 6 else "triangular"
        fams = sys.argv[7].split(",") if len(sys.argv) > 7 else FAMILIES
        Fd = Field(p, k)
        ab = two_level_contraction(Fd)
        if ab is None:
            print(f"p={p} kappa={k}: no two-level contraction (p in E_2)")
            return
        F = F_from_two_level(Fd, *ab)
        assert check_contraction(Fd, 2, F)
        d = k if p < 5000 else None
        r, M, res = run(Fd, 2, F, a, N, scheme, fams, d=d)
        ok = sum(1 for z in res if z[3])
        old = (a + 1) * ((k - 1) * a + 1)
        print(f"two p={p} kappa={k} a={a} scheme={scheme} r={r} arity={M} "
              f"(Schedule 2: {old}) witnesses {ok}/{len(res)} max_used={max(z[2] for z in res)}")
        bad = [z for z in res if not z[3]]
        if bad:
            print("FAIL", bad[:5])
    elif mode in ("llev", "ranks"):
        sys.path.insert(0, "../2026-11-02-rees-schedules/small-prime")
        import llevel
        p, k, L = map(int, sys.argv[2:5])
        Fl = llevel.Field(p, k)
        C, nv, nc = llevel.sat_search(Fl, L)
        if C is None:
            print(f"p={p} kappa={k} L={L}: UNSAT")
            return
        assert llevel.verify_contraction(Fl, L, C)
        Fd = Field(p, k)
        assert Fd.g == Fl.g
        F = F_from_llevel_C(Fd, L, C)
        assert check_contraction(Fd, L, F)
        Hs = telescoped(F, L, k, p)
        r = [len(functionals(Hs[t], t, L, k, p)) for t in range(L)]
        old = 1
        for l in range(L):
            old *= (k - 1) ** l + 0
        if mode == "ranks":
            print(f"p={p} kappa={k} L={L} ranks r={r} bounds="
                  f"{[min((k-1)**t, k**(L-t-1)) for t in range(L)]}")
            return
        a, N = map(int, sys.argv[5:7])
        scheme = sys.argv[7] if len(sys.argv) > 7 else "triangular"
        fams = sys.argv[8].split(",") if len(sys.argv) > 8 else FAMILIES
        r, M, res = run(Fd, L, F, a, N, scheme, fams, d=k)
        ok = sum(1 for z in res if z[3])
        oldM = 1
        for l in range(L):
            oldM *= (k - 1) ** l * a + 1
        print(f"llev p={p} kappa={k} L={L} a={a} scheme={scheme} r={r} arity={M} "
              f"(round-1 L-level: {oldM}) witnesses {ok}/{len(res)}")
        bad = [z for z in res if not z[3]]
        if bad:
            print("FAIL", bad[:5])


if __name__ == "__main__" and sys.argv[1:2] != ["sparse"]:
    main()


# ---------------------------------------------------------------- sparse dependencies (L = 2)

def sparse_bound(p, a):
    """Column budget of the triangular two-level scheme with sparse dependencies:
    m_0 = 1, m_l = max(l + r_l, m_{l-1} + floor((1-1/p)/(1-p^{-r_l}) * l) + r_l),
    r_l = max(1, ceil(log_p(l+1))).  (Kothari-O'Donnell-Wu Lemma 3.6 / Thm 3.7 shape.)"""
    from fractions import Fraction
    m = 1
    for l in range(1, a + 1):
        r = 1
        while p ** r < l + 1:
            r += 1
        w = Fraction(p - 1, p) / (1 - Fraction(1, p ** r)) * l
        m = max(l + r, m + int(w) + r)
    return m


def solve_triangular_sparse(Fd, F, cols, a):
    """L = 2 triangular scheme; each dependency mod U is a minimum-weight nonzero
    combination of an r-dim space of dependencies among the first q + r unused columns."""
    p = Fd.p
    Hs = telescoped(F, 2, Fd.k, p)
    H2 = {m[:1]: v for m, v in Hs[1].items() if m[1] == 0}
    unused = list(range(len(cols)))
    U, objs, maxidx = [], [], -1
    while True:
        q = a - len(U)
        if q == 0:
            c = unused.pop(0)
            maxidx = max(maxidx, c)
            obj = [(c, 1, (0,))]
            v = None
        else:
            r = 1
            while p ** r < q + 1:
                r += 1
            take = unused[:q + r]
            if len(take) < q + r:
                raise RuntimeError("out of columns")
            maxidx = max(maxidx, take[-1])
            big = [list(cols[c]) for c in take] + [[(-x) % p for x in u] for u in U]
            ker = [y[:len(take)] for y in kernel_basis(big, p)]
            ker = [y for y in ker if any(y)]
            # independent lambda-parts
            basis = []
            for y in ker:
                if rank_mod(basis + [y], p) > len(basis):
                    basis.append(y)
            basis = basis[:r] if len(basis) >= r else basis
            best = None
            for coeffs in itertools.product(range(p), repeat=len(basis)) if p ** len(basis) <= 4096 else [tuple([1] + [0] * (len(basis) - 1))]:
                if not any(coeffs):
                    continue
                y = [sum(cf * b[i] for cf, b in zip(coeffs, basis)) % p for i in range(len(take))]
                wgt = sum(1 for t in y if t)
                if wgt and (best is None or wgt < best[0]):
                    best = (wgt, y)
            y = best[1]
            first = next(t for t in y if t)
            inv = pow(first, -1, p)
            obj = []
            for c, t in zip(take, y):
                if t:
                    d = t * inv % p
                    obj.append((c, d, (Fd.coset(d),)))
            used = {c for c, _, _ in obj}
            unused = [c for c in unused if c not in used]
            v = apply_functional(obj, H2, cols, a, p)
        if v is None or not any(v) or (U and solve_in_span(U, v, p) is not None):
            x = [0] * len(cols)
            weights_from(obj, 1, 0, F, Fd, x)
            break
        U.append(v)
        objs.append(obj)
    tau = [0] * a
    for (c, xc) in enumerate(x):
        if xc:
            for i in range(a):
                tau[i] = (tau[i] - xc * cols[c][i]) % p
    for l in range(len(objs) - 1, -1, -1):
        coords = solve_in_span(U[:l + 1], tau, p)
        cl = coords[l]
        if cl:
            n = Fd.coset(cl)
            before = list(x)
            weights_from(objs[l], cl, n, F, Fd, x)
            for c in range(len(cols)):
                d = (x[c] - before[c]) % p
                if d:
                    for i in range(a):
                        tau[i] = (tau[i] - d * cols[c][i]) % p
    assert not any(tau)
    return x, maxidx + 1


def main_sparse():
    p, k, a, N = map(int, sys.argv[2:6])
    fams = sys.argv[6].split(",") if len(sys.argv) > 6 else FAMILIES
    Fd = Field(p, k)
    ab = two_level_contraction(Fd)
    if ab is None:
        print(f"p={p} kappa={k}: p in E_2")
        return
    F = F_from_two_level(Fd, *ab)
    M = sparse_bound(p, a)
    rng = random.Random(7)
    ok, need = 0, 0
    tot = 0
    for fam in fams:
        for it in range(N):
            cols = family(fam, rng, p, a, M)
            x, used = solve_triangular_sparse(Fd, F, cols, a)
            good, why = check_witness(Fd, cols, x)
            ok += good
            tot += 1
            need = max(need, used)
            assert used <= M
    print(f"sparse p={p} kappa={k} a={a} budget={M} (dense (a+1)(a+2)/2={(a+1)*(a+2)//2}, "
          f"Schedule 2={(a+1)*((k-1)*a+1)}) max_used={need} witnesses {ok}/{tot}")


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "sparse":
    main_sparse()
