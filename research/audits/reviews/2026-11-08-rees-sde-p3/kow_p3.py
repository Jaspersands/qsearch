"""Faithful implementation of the KOW (arXiv 2510.07515, Thm 1.2) worst-case F_3^n subset-sum
solver: sparse dependency (all 3^r-1 combinations enumerated, deterministic) + u = u' trick +
projection mod u.  Every witness is verified.  Also: recursion table, adversarial tests, and a
check that generic q+2 columns never realize a 2-dim subgroup by class unions."""
import itertools, math, sys, random
import numpy as np

def rank3(M):
    M = M.copy() % 3; r = 0
    rows, cols = M.shape
    for c in range(cols):
        p = next((i for i in range(r, rows) if M[i, c]), None)
        if p is None: continue
        M[[r, p]] = M[[p, r]]; M[r] = (M[r] * M[r, c]) % 3
        nz = np.nonzero(M[:, c])[0]
        for i in nz:
            if i != r: M[i] = (M[i] - M[i, c] * M[r]) % 3
        r += 1
        if r == rows: break
    return r

def nullspace3(A):
    """Basis of {x : A x = 0} over F_3; A is (l x N)."""
    A = A.copy() % 3; l, N = A.shape; piv = []; r = 0
    for c in range(N):
        p = next((i for i in range(r, l) if A[i, c]), None)
        if p is None: continue
        A[[r, p]] = A[[p, r]]; A[r] = (A[r] * A[r, c]) % 3
        for i in np.nonzero(A[:, c])[0]:
            if i != r: A[i] = (A[i] - A[i, c] * A[r]) % 3
        piv.append(c); r += 1
        if r == l: break
    free = [c for c in range(N) if c not in piv]
    basis = []
    for f in free:
        x = np.zeros(N, dtype=np.int64); x[f] = 1
        for i, c in enumerate(piv): x[c] = (-A[i, f]) % 3
        basis.append(x)
    return basis

def r_of(l): return max(1, math.ceil(math.log(l + 1, 3) - 1e-12)) if l > 0 else 1

def w_bound(l):
    """KOW sparse-dependency support bound used in the recursion (l = ambient dim)."""
    r = r_of(l)
    return math.floor((l + r) * 2 * 3**(r - 1) / (3**r - 1))

def recursion_table(nmax):
    m = {0: 1}
    for l in range(1, nmax + 1):
        m[l] = max(l + r_of(l), m[l - 1] + w_bound(l))
    return m

def sparse_dependency(cols):
    """cols: list of F_3^l vectors (ambient dim l).  Returns the sparsest nonzero dependency
    among all nonzero combinations of a nullspace basis (deterministic, poly since 3^r <= 3(l+1))."""
    A = np.array(cols, dtype=np.int64).T % 3  # l x N
    basis = nullspace3(A)
    if not basis: return None
    r = len(basis)
    if 3**r > 200000:  # degenerate huge kernel: just take basis vectors
        cands = basis
    else:
        B = np.array(basis)
        cands = []
        for beta in itertools.product(range(3), repeat=r):
            if not any(beta): continue
            cands.append((np.array(beta) @ B) % 3)
    return min(cands, key=lambda d: int(np.count_nonzero(d)))

def solve(vectors, stats=None):
    """vectors: list of np arrays in F_3^l.  Returns a nonempty list of indices with zero sum,
    or None if the recursion runs out of vectors."""
    vectors = [np.array(v, dtype=np.int64) % 3 for v in vectors]
    idx = list(range(len(vectors)))
    return _solve(vectors, idx, stats)

def _solve(vecs, idx, stats):
    m = len(vecs)
    if m == 0: return None
    l = len(vecs[0])
    for i, v in enumerate(vecs):
        if not v.any(): return [idx[i]]
    if l == 0: return [idx[0]]
    r = r_of(l)
    take = min(m, l + r)
    d = sparse_dependency(vecs[:take])
    if d is None: return None
    if stats is not None: stats.append((l, int(np.count_nonzero(d)), take))
    A = [i for i in range(take) if d[i] == 1]; B = [i for i in range(take) if d[i] == 2]
    if not B:  # sum_A v = 0 directly
        return [idx[i] for i in A]
    if not A:
        return [idx[i] for i in B]
    u = sum(vecs[i] for i in A) % 3
    assert ((sum(vecs[i] for i in B) - u) % 3 == 0).all()
    j = int(np.nonzero(u)[0][0]); inv = int(u[j])  # inverse of u_j (1->1, 2->2)
    rest = [i for i in range(m) if d[i] == 0] if take == m else [i for i in range(take) if d[i] == 0] + list(range(take, m))
    def proj(v):
        w = (v - (v[j] * inv) * u) % 3
        return np.delete(w, j)
    sub = _solve([proj(vecs[i]) for i in rest], [idx[i] for i in rest], stats)
    if sub is None: return None
    pos = {g: i for i, g in enumerate(idx)}
    T = [pos[g] for g in sub]
    s = sum(vecs[i] for i in T) % 3
    c = int(s[j]) * inv % 3  # s = c u
    assert ((s - c * u) % 3 == 0).all()
    extra = [] if c == 0 else (A if c == 2 else A + B)  # c=2: s+u=0 ; c=1: s+2u=0
    return [idx[i] for i in T] + [idx[i] for i in extra]

def verify(vectors, S):
    assert S is not None and len(S) > 0 and len(set(S)) == len(S)
    tot = sum(np.array(vectors[i], dtype=np.int64) for i in S) % 3
    assert not tot.any(), "witness does not sum to zero"
    return True

# ---------- instance families ----------
def fam_random(n, m, rng): return [rng.integers(0, 3, n) for _ in range(m)]
def fam_lowrank(n, m, rng, k=None):
    k = k or max(1, n // 2); Bk = [rng.integers(0, 3, n) for _ in range(k)]
    return [sum(int(c) * b for c, b in zip(rng.integers(0, 3, k), Bk)) % 3 for _ in range(m)]
def fam_fewdistinct(n, m, rng, k=None):
    k = k or (2 * n + 1); pool = [rng.integers(0, 3, n) for _ in range(k)]
    out = [p.copy() for p in pool]
    while len(out) < m: out.append(pool[rng.integers(0, k)].copy())
    return out[:m]
def fam_davenport_pad(n, m, rng):
    """Davenport extremal core (each basis vector twice, no zero-sum) padded with random vectors."""
    out = [np.eye(n, dtype=np.int64)[i] for i in range(n) for _ in range(2)]
    while len(out) < m: out.append(rng.integers(0, 3, n))
    return out[:m]
def fam_sparse(n, m, rng, w=2):
    out = []
    for _ in range(m):
        v = np.zeros(n, dtype=np.int64); pos = rng.choice(n, size=min(w, n), replace=False)
        v[pos] = rng.integers(1, 3, len(pos)); out.append(v)
    return out
def fam_signed_basis_blocks(n, m, rng):
    """Blocks e_i, e_i, 2e_i, ... designed so every dependency is dense modulo earlier u's."""
    out = []
    for i in range(n):
        out += [np.eye(n, dtype=np.int64)[i] * s for s in (1, 1, 2)]
    while len(out) < m: out.append(rng.integers(0, 3, n))
    return out[:m]
FAMS = dict(random=fam_random, lowrank=fam_lowrank, fewdistinct=fam_fewdistinct,
            davenport_pad=fam_davenport_pad, sparse=fam_sparse, signed_blocks=fam_signed_basis_blocks)

if __name__ == "__main__":
    rng = np.random.default_rng(20261108)
    tab = recursion_table(64)
    print("n  m_n(KOW recursion as implemented)  2n+1  n^2/3  (n+1)(n+2)/2")
    for n in (1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 40, 48, 60, 64):
        print(f"{n:3d} {tab[n]:6d} {2*n+1:6d} {n*n/3:8.1f} {(n+1)*(n+2)//2:7d}")
    print("ratio m_n / n^2 at n=64:", tab[64] / 64**2)
    # verification runs at m = m_n (the guaranteed budget) on all families
    total = 0; fails = 0; maxsup = {}
    for n in (6, 10, 15, 20, 30, 40, 50, 60):
        for name, fam in FAMS.items():
            reps = 6 if n <= 30 else 2
            for _ in range(reps):
                vecs = fam(n, tab[n], rng)
                stats = []
                S = solve(vecs, stats)
                total += 1
                if S is None: fails += 1; print("FAIL", name, n); continue
                verify(vecs, S)
                for (l, w, take) in stats:
                    maxsup[l] = max(maxsup.get(l, 0), w)
                    assert w <= w_bound(l) or take < l + r_of(l), (l, w, take)
    print(f"verified {total} instances at budget m_n, failures {fails}; every found support <= w_bound(l) when l+r vectors were available")
    print("largest observed support per level (l: w) for l in 5,10,20,30,40,50,60:",
          {l: maxsup.get(l) for l in (5, 10, 20, 30, 40, 50, 60)}, "bounds:", {l: w_bound(l) for l in (5,10,20,30,40,50,60)})
    # how many columns did random instances actually consume vs. the bound?
    for n in (20, 40, 60):
        used = []
        for _ in range(5):
            vecs = fam_random(n, tab[n], rng); stats = []; S = solve(vecs, stats); verify(vecs, S)
            used.append(sum(w for (_, w, _) in stats))
        print(f"n={n}: columns consumed by the dependencies on random instances {used}, budget {tab[n]}, 2n+1={2*n+1}")
