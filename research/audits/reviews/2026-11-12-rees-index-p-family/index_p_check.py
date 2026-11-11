"""Exact finite checks for 2026-11-12-rees-index-p-family.md (falsifiers only).

(1) The filiform algebra L_{5,6} ([x1,x2]=x3,[x1,x3]=x4,[x1,x4]=x5,[x2,x3]=x5)
    satisfies Jacobi, has class 4, and has NO abelian ideal of codimension 1
    over F_p (p = 5, 7); the model filiform L_5 has one.
(2) In L = F x (+) A with A = F_p^m abelian and ad_x = N nilpotent, class >= 3:
    the abelian hyperplanes are exactly {A}, and C_L([L,L]) = A.
(3) Filiform L_4 over F_5: every subalgebra S satisfies dim S - dim(S cap A) <= 1,
    and if S is not inside A then S cap A is an ideal (BCvD Lemma 1 shape).
"""
import itertools, random, sys
import numpy as np

def rref(M, p):
    M = [list(r) for r in M]; piv = []; r = 0
    if not M: return [], []
    n = len(M[0])
    for c in range(n):
        k = next((i for i in range(r, len(M)) if M[i][c] % p), None)
        if k is None: continue
        M[r], M[k] = M[k], M[r]
        inv = pow(M[r][c], p - 2, p)
        M[r] = [(v * inv) % p for v in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] % p:
                f = M[i][c]; M[i] = [(a - f * b) % p for a, b in zip(M[i], M[r])]
        piv.append(c); r += 1
    return [tuple(x) for x in M[:r]], piv

def rank(M, p): return len(rref(M, p)[0])

def br(T, u, v, p):  # T[i][j] = vector [e_i, e_j]
    n = len(u); out = [0] * n
    for i in range(n):
        if u[i] % p == 0: continue
        for j in range(n):
            if v[j] % p == 0: continue
            for k in range(n): out[k] = (out[k] + u[i] * v[j] * T[i][j][k]) % p
    return out

def make(n, rels, p):
    T = [[[0] * n for _ in range(n)] for _ in range(n)]
    for (i, j), vec in rels.items():
        T[i][j] = [x % p for x in vec]; T[j][i] = [(-x) % p for x in vec]
    return T

def e(n, k): v = [0] * n; v[k] = 1; return v

def jacobi_ok(T, n, p):
    E = [e(n, i) for i in range(n)]
    for a, b, c in itertools.product(range(n), repeat=3):
        s = [(x + y + z) % p for x, y, z in zip(br(T, E[a], br(T, E[b], E[c], p), p),
                                             br(T, E[b], br(T, E[c], E[a], p), p),
                                             br(T, E[c], br(T, E[a], E[b], p), p))]
        if any(s): return False
    return True

def lcs_dims(T, n, p):
    E = [e(n, i) for i in range(n)]; cur = E; dims = [n]
    while True:
        nxt = [br(T, u, v, p) for u in E for v in cur]
        nxt = list(rref(nxt, p)[0]); d = len(nxt)
        dims.append(d)
        if d == 0 or d == dims[-2]: return dims
        cur = nxt

def hyperplanes(n, p):  # kernels of nonzero functionals up to scalar
    for f in itertools.product(range(p), repeat=n):
        if not any(f): continue
        if f[next(i for i in range(n) if f[i])] != 1: continue
        basis = []
        for v in itertools.product(range(p), repeat=n):
            if sum(a * b for a, b in zip(f, v)) % p == 0: basis.append(list(v))
        yield f, list(rref(basis, p)[0])

def abelian(T, B, p): return all(not any(br(T, u, v, p)) for u in B for v in B)
def ideal(T, n, B, p):
    E = [e(n, i) for i in range(n)]
    return all(rank(B + [br(T, x, u, p)], p) == len(B) for x in E for u in B)

def check1():
    for p in (5, 7):
        n = 5
        L56 = make(n, {(0, 1): e(n, 2), (0, 2): e(n, 3), (0, 3): e(n, 4), (1, 2): e(n, 4)}, p)
        L5 = make(n, {(0, 1): e(n, 2), (0, 2): e(n, 3), (0, 3): e(n, 4)}, p)
        for name, T in (("L_{5,6}", L56), ("L_5 model", L5)):
            ab = [f for f, B in hyperplanes(n, p) if abelian(T, B, p) and ideal(T, n, B, p)]
            print(f"p={p} {name}: jacobi={jacobi_ok(T, n, p)} lcs_dims={lcs_dims(T, n, p)} "
                  f"abelian_codim1_ideals={len(ab)}")

def check2(trials=40):
    rng = random.Random(20261112); bad = 0; done = 0
    for _ in range(trials):
        p = rng.choice([5, 7]); m = rng.choice([2, 3, 4])
        # N strictly upper triangular after random similarity
        N = np.zeros((m, m), dtype=int)
        for i in range(m):
            for j in range(i + 1, m): N[i, j] = rng.randrange(p)
        n = m + 1  # basis x=e0, A=e1..em ; [x, a_j] = N a_j
        rels = {(0, j + 1): [0] + [int(N[i, j]) % p for i in range(m)] for j in range(m)}
        T = make(n, rels, p)
        dims = lcs_dims(T, n, p); cls = len([d for d in dims if d > 0]) - 1
        if cls < 3: continue
        done += 1
        A = [e(n, i) for i in range(1, n)]
        ab = [B for f, B in hyperplanes(n, p) if abelian(T, B, p)]
        uniq = len(ab) == 1 and rank(ab[0] + A, p) == m
        E = [e(n, i) for i in range(n)]
        g2 = list(rref([br(T, u, v, p) for u in E for v in E], p)[0])
        # centralizer of g2: solve sum c_i [e_i, g] = 0 for all g in g2
        rows = []
        for g in g2:
            cols = [br(T, E[i], g, p) for i in range(n)]
            for k in range(n): rows.append([cols[i][k] for i in range(n)])
        r = rank(rows, p) if rows else 0
        cent_dim = n - r
        # A inside centralizer?
        a_in = all(not any(br(T, a, g, p)) for a in A for g in g2)
        ok = uniq and cent_dim == m and a_in
        bad += (not ok)
    print(f"check2: class>=3 instances={done} failures={bad}")

def check3():
    p = 5; n = 4
    T = make(n, {(0, 1): e(n, 2), (0, 2): e(n, 3)}, p)
    A = [e(n, i) for i in range(1, n)]
    seen = set(); count = 0; bad = 0
    vecs = [list(v) for v in itertools.product(range(p), repeat=n) if any(v)]
    for k in range(0, n + 1):
        for combo in itertools.combinations(range(len(vecs)), k) if k <= 1 else []:
            pass
    # enumerate subspaces by closure from random generating pairs/triples exhaustively by rref keys
    subs = {()}
    frontier = [[]]
    while frontier:
        new = []
        for B in frontier:
            for v in vecs:
                if rank(B + [v], p) == len(B): continue
                R = tuple(rref(B + [v], p)[0])
                if R not in subs: subs.add(R); new.append([list(x) for x in R])
        frontier = new
    for S in subs:
        S = [list(x) for x in S]
        if not all(rank(S + [br(T, u, v, p)], p) == len(S) for u in S for v in S): continue
        count += 1
        # S cap A: vectors of S with x-coordinate 0
        if S:
            dimSA = len(S) - (1 if any(s[0] % p for s in S) else 0)
        else: dimSA = 0
        SA = [s for s in rref(S, p)[0] if s[0] % p == 0] if S else []
        SA = [list(s) for s in SA]
        if len(SA) != dimSA: bad += 1; continue
        if len(S) - dimSA > 1: bad += 1
        if dimSA < len(S) and SA and not ideal(T, n, SA, p): bad += 1
    print(f"check3: filiform4 p=5 subspaces={len(subs)} subalgebras={count} failures={bad}")

if __name__ == "__main__":
    check1(); check2(); check3()
