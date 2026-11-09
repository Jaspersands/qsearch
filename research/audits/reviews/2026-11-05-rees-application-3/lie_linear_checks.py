"""Exact checks for the 2026-11-05 Rees application review (third pass).

Part 1: in G = UT_4(F_5) (class 3 < 5, a Lazard group), the normalizer,
centralizer, intersection and automorphism fixed points computed by brute
force over all 5^6 group elements equal exp of the Lie-side linear answers
  N_L(k) = {x : [x,k] <= k},  C_L(k) = {x : [x,k] = 0},  h cap k,
  ker(Ad_b - 1) on n_4.
Part 2: the cyclotomic-coset group G = R^n x| F_p, R = F_p[pi]/(pi^L)
(Boucher-Fouque-Shen, arXiv:2609.34996, with t = 1): lower central series,
class L, the binomial form of lambda_j, and the shape of H_s.
Part 3: the degree->=p control F = x1^p x2 - x1 x2^p under x1 -> x1 + t x2.
Finite checks only; they can falsify, not prove.
"""
import itertools, math, random
import numpy as np

random.seed(20261105)

# ---------------------------------------------------------------- Part 1
p, N = 5, 4
POS = [(i, j) for i in range(N) for j in range(i + 1, N)]   # 6 coords
INV = {k: pow(k, -1, p) for k in range(1, p)}

def vec2mat(v):
    M = np.zeros((N, N), dtype=np.int64)
    for c, (i, j) in zip(v, POS):
        M[i, j] = c
    return M % p

def mat2vec(M):
    return tuple(int(M[i, j]) % p for (i, j) in POS)

def mexp(X):
    I = np.eye(N, dtype=np.int64)
    R, P = I.copy(), I.copy()
    for k in range(1, N):
        P = (P @ X) % p
        R = (R + P * pow(math.factorial(k), -1, p)) % p
    return R

def mlog(g):
    I = np.eye(N, dtype=np.int64)
    Y = (g - I) % p
    R, P = np.zeros((N, N), dtype=np.int64), I.copy()
    for k in range(1, N):
        P = (P @ Y) % p
        R = (R + ((-1) ** (k + 1)) * P * pow(k, -1, p)) % p
    return R % p

def key(M):
    return M.astype(np.int8).tobytes()

def minv(g):
    return mexp((-mlog(g)) % p)

# linear algebra over F_p
def rref(rows):
    A = [list(r) for r in rows]
    piv, r = [], 0
    ncol = len(A[0]) if A else 0
    for c in range(ncol):
        k = next((i for i in range(r, len(A)) if A[i][c] % p), None)
        if k is None:
            continue
        A[r], A[k] = A[k], A[r]
        iv = INV[A[r][c] % p]
        A[r] = [(x * iv) % p for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c] % p:
                f = A[i][c]
                A[i] = [(a - f * b) % p for a, b in zip(A[i], A[r])]
        piv.append(c); r += 1
    return [tuple(x) for x in A[:r]]

def span(vs):
    return rref(vs) if vs else []

def nullspace(rows, ncol):
    """basis of {x : rows . x = 0}"""
    R = rref(rows) if rows else []
    piv = []
    for row in R:
        piv.append(next(c for c in range(ncol) if row[c]))
    free = [c for c in range(ncol) if c not in piv]
    basis = []
    for f in free:
        x = [0] * ncol; x[f] = 1
        for row, pc in zip(R, piv):
            x[pc] = (-row[f]) % p
        basis.append(tuple(x))
    return basis

def bracket(x, y):
    X, Y = vec2mat(x), vec2mat(y)
    return mat2vec((X @ Y - Y @ X) % p)

def lie_closure(vs):
    B = span(vs)
    while True:
        new = span(list(B) + [bracket(a, b) for a in B for b in B])
        if len(new) == len(B):
            return B
        B = new

def in_span(B, v):
    return len(span(list(B) + [v])) == len(B)

def subspace_points(B):
    pts = set()
    for coeffs in itertools.product(range(p), repeat=len(B)):
        v = [0] * len(POS)
        for c, b in zip(coeffs, B):
            v = [(a + c * bb) % p for a, bb in zip(v, b)]
        pts.add(tuple(v))
    return pts

def group_closure(gens):
    I = np.eye(N, dtype=np.int64)
    S = {key(I): I}
    frontier = [I]
    while frontier:
        nf = []
        for a in frontier:
            for g in gens:
                b = (a @ g) % p
                kb = key(b)
                if kb not in S:
                    S[kb] = b; nf.append(b)
        frontier = nf
    return S

ALL = [tuple(v) for v in itertools.product(range(p), repeat=len(POS))]
ALLG = {v: mexp(vec2mat(v)) for v in ALL}

def lie_set_to_group_keys(B):
    return {key(ALLG[v]) for v in subspace_points(B)}

def rand_vec(depth_bias=False):
    return tuple(random.randrange(p) for _ in POS)

def normalizer_lie(B):
    # x with [x, b] in span(B) for all b in B: linear in x
    d = len(POS)
    # build linear map x -> ([x,b_i] mod span B) ; use complement projection via rref test
    # Solve by brute linear algebra: unknown x in F_p^6, constraints = for each b_i and each
    # functional phi vanishing on span(B): phi([x,b_i]) = 0.
    ann = nullspace(B, d) if B else [tuple(int(i == j) for j in range(d)) for i in range(d)]
    rows = []
    for b in B:
        # matrix of x -> [x,b]
        cols = [bracket(tuple(int(i == j) for j in range(d)), b) for i in range(d)]
        for phi in ann:
            rows.append(tuple(sum(phi[t] * cols[i][t] for t in range(d)) % p for i in range(d)))
    return nullspace(rows, d) if rows else [tuple(int(i == j) for j in range(d)) for i in range(d)]

def centralizer_lie(B):
    d = len(POS)
    rows = []
    for b in B:
        cols = [bracket(tuple(int(i == j) for j in range(d)), b) for i in range(d)]
        for t in range(d):
            rows.append(tuple(cols[i][t] for i in range(d)))
    return nullspace(rows, d)

def intersect(B1, B2):
    d = len(POS)
    A1 = nullspace(B1, d) if B1 else [tuple(int(i == j) for j in range(d)) for i in range(d)]
    A2 = nullspace(B2, d) if B2 else [tuple(int(i == j) for j in range(d)) for i in range(d)]
    return nullspace(list(A1) + list(A2), d)

out = []
def log(s):
    print(s); out.append(s)

log("Part 1: UT_4(F_5), |G| = 5^6, exhaustive over all group elements")
fails = 0
trials = 0
for trial in range(6):
    ngen = random.choice([1, 2, 2, 3])
    gens_v = [rand_vec() for _ in range(ngen)]
    # bias: sometimes make generators sparse to get proper small subgroups
    if trial % 2 == 0:
        gens_v = [tuple(c if random.random() < 0.5 else 0 for c in v) for v in gens_v]
    gens = [ALLG[v] for v in gens_v]
    K = group_closure(gens)
    kB = lie_closure(list(gens_v))
    assert len(K) == p ** len(kB), (len(K), len(kB))
    assert set(K.keys()) == lie_set_to_group_keys(kB)
    # brute normalizer and centralizer of K
    Nset, Cset = set(), set()
    for v in ALL:
        g = ALLG[v]; gi = minv(g)
        conj = [(g @ k @ gi) % p for k in gens]
        if all(key(c) in K for c in conj):
            Nset.add(key(g))
        if all(np.array_equal(c, k) for c, k in zip(conj, gens)):
            Cset.add(key(g))
    nB, cB = normalizer_lie(kB), centralizer_lie(kB)
    okN = Nset == lie_set_to_group_keys(nB)
    okC = Cset == lie_set_to_group_keys(cB)
    # second subgroup for intersection
    gens2_v = [rand_vec() for _ in range(2)]
    gens2_v = [tuple(c if random.random() < 0.6 else 0 for c in v) for v in gens2_v]
    K2 = group_closure([ALLG[v] for v in gens2_v])
    k2B = lie_closure(list(gens2_v))
    inter = set(K.keys()) & set(K2.keys())
    okI = inter == lie_set_to_group_keys(intersect(kB, k2B))
    trials += 1
    fails += (not okN) + (not okC) + (not okI)
    log(f"  trial {trial}: dim k={len(kB)} |N|=5^{len(nB)} |C|=5^{len(cB)} "
        f"dim(k cap k2)={len(intersect(kB, k2B))}  normalizer {okN} centralizer {okC} intersection {okI}")

# automorphism fixed points: alpha(g) = b g b^-1, b in B_4(F_5) random invertible upper triangular
for trial in range(3):
    while True:
        b = np.triu(np.array([[random.randrange(p) for _ in range(N)] for _ in range(N)]))
        if all(b[i, i] % p for i in range(N)):
            break
    # inverse of b mod p
    import sympy
    bi = np.array(sympy.Matrix(b.tolist()).inv_mod(p).tolist(), dtype=np.int64)
    Fix = {key(ALLG[v]) for v in ALL if np.array_equal((b @ ALLG[v] @ bi) % p, ALLG[v])}
    d = len(POS)
    cols = []
    for i in range(d):
        e = tuple(int(i == j) for j in range(d))
        img = mat2vec((b @ vec2mat(e) @ bi) % p)
        cols.append(tuple((img[t] - e[t]) % p for t in range(d)))
    rows = [tuple(cols[i][t] for i in range(d)) for t in range(d)]
    fB = nullspace(rows, d)
    okF = Fix == lie_set_to_group_keys(fB)
    fails += (not okF)
    log(f"  fixed points of conjugation by b (diag {[int(b[i,i]) for i in range(N)]}): |Fix|=5^{len(fB)} match {okF}")
log(f"Part 1 failures: {fails}")

# ---------------------------------------------------------------- Part 2
log("\nPart 2: cyclotomic-coset group R^n x| F_p, R = F_p[pi]/(pi^L)")

def ccp_checks(p, L, n):
    # element: (tuple of n*L coords, j); x in R^n, coords [r][k] = coefficient of pi^k
    def mul_zeta_pow(x, j):
        # multiply each R-component by zeta^j = (1+pi)^j = sum_k C(j,k) pi^k
        coef = [math.comb(j, k) % p for k in range(L)]
        out = []
        for r in range(n):
            a = x[r * L:(r + 1) * L]
            prod = [0] * L
            for i, ai in enumerate(a):
                if ai:
                    for k, ck in enumerate(coef):
                        if i + k < L:
                            prod[i + k] = (prod[i + k] + ai * ck) % p
            out.extend(prod)
        return tuple(out)
    def mul(g, h):
        x1, j1 = g; x2, j2 = h
        y = mul_zeta_pow(x2, j1)
        return (tuple((a + b) % p for a, b in zip(x1, y)), (j1 + j2) % p)
    def inv(g):
        x, j = g
        jn = (-j) % p
        y = mul_zeta_pow(x, jn)
        return (tuple((-a) % p for a in y), jn)
    def comm(g, h):
        return mul(mul(inv(g), inv(h)), mul(g, h))
    dim = n * L
    zero = tuple([0] * dim)
    # lambda_j s for s in F_p^n embedded as constants
    s = tuple(random.randrange(1, p) for _ in range(n))
    svec = tuple(v for r in range(n) for v in ([s[r]] + [0] * (L - 1)))
    gen = (svec, 1)
    H = [(zero, 0)]
    for _ in range(p - 1):
        H.append(mul(H[-1], gen))
    assert mul(H[-1], gen) == (zero, 0), "order p"
    lam_ok = True
    for j in range(p):
        xj = H[j][0]
        for r in range(n):
            for k in range(L):
                if xj[r * L + k] != (math.comb(j, k + 1) * s[r]) % p:
                    lam_ok = False
    # lower central series via generators: G gens = unit vectors and (0,1)
    Ggens = [(tuple(int(i == t) for i in range(dim)), 0) for t in range(dim)] + [(zero, 1)]
    def subgroup_from(gens):
        # gens lie in abelian normal R^n (j=0): span over F_p
        rows = [g[0] for g in gens if any(g[0])]
        return span(rows) if rows else []
    gamma = [None, None]
    g2 = subgroup_from([comm(a, b) for a in Ggens for b in Ggens])
    gamma.append(g2)
    k = 2
    while gamma[k]:
        gk = gamma[k]
        nxt = subgroup_from([comm(a, (v, 0)) for a in Ggens for v in gk])
        gamma.append(nxt); k += 1
    cls = k - 1
    dims = [len(gamma[i]) for i in range(2, k + 1)]
    # H normal? conjugate generator by unit vector element
    conj = mul(mul(Ggens[0], gen), inv(Ggens[0]))
    normal = conj in set(H)
    # H cap gamma_2 trivial and H does not contain gamma_2
    return lam_ok, cls, dims, normal

for (pp, L, n) in [(5, 4, 1), (5, 4, 2), (7, 6, 1), (7, 3, 2), (11, 4, 2)]:
    lam_ok, cls, dims, normal = ccp_checks(pp, L, n)
    log(f"  p={pp} L={L} n={n}: lambda_j coords = C(j,k+1) s: {lam_ok}; class = {cls} (expected {L}); "
        f"dim gamma_2.. = {dims}; H_s normal: {normal}")

# ---------------------------------------------------------------- Part 3
log("\nPart 3: degree->=p control F = x1^p x2 - x1 x2^p, g_t: x1 -> x1 + t x2")
import sympy as sp
for pp in [5, 7]:
    x1, x2, t = sp.symbols('x1 x2 t')
    F = x1**pp * x2 - x1 * x2**pp
    D = sp.Poly(sp.expand(F.subs(x1, x1 + t * x2) - F), x1, x2, t, modulus=pp)
    deriv = sp.Poly(sp.diff(F.subs(x1, x1 + t * x2), t).subs(t, 0), x1, x2, modulus=pp)
    vanish_Fp = all(sp.Poly(D.as_expr().subs(t, a), x1, x2, modulus=pp).is_zero for a in range(pp))
    log(f"  p={pp}: F(g_t x)-F(x) = {D.as_expr()} ; vanishes formally for every t in F_p: {vanish_Fp}; "
        f"Lie derivative at t=0: {deriv.as_expr()} (nonzero => first-order method reports no symmetry)")

with open(__file__.replace('.py', '.out'), 'w') as fh:
    fh.write("\n".join(out) + "\n")
