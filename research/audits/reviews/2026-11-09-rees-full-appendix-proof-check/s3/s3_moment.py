#!/usr/bin/env python
"""s3 (9 Nov 2026 proof check): exhaustive exact check of Lemma s3-moment (a)-(d) and of
Lemma s3-node(a)-(b) on small cases (p, kappa, M, a).  For a <= 2 the full law of N(X) over
uniform a x M matrices X is enumerated (via row-indicator products); for a = 3 only the first
two moments are computed exactly (pair counts).  Exact Fractions throughout."""
from fractions import Fraction as Fr
from itertools import product
import numpy as np

def rank_mod_p(rows, p):
    A = [list(r) for r in rows]
    r = 0; ncol = len(A[0]) if A else 0
    for c in range(ncol):
        piv = None
        for i in range(r, len(A)):
            if A[i][c] % p: piv = i; break
        if piv is None: continue
        A[r], A[piv] = A[piv], A[r]
        inv = pow(A[r][c], p-2, p)
        A[r] = [x*inv % p for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c] % p:
                f = A[i][c]
                A[i] = [(x - f*y) % p for x, y in zip(A[i], A[r])]
        r += 1
    return r

def case(p, kap, M, a):
    assert (p-1) % kap == 0
    h = (p-1)//kap
    D = sorted({pow(x, kap, p) for x in range(1, p)} | {0})
    assert len(D) == h+1
    S = [y for y in product(D, repeat=M) if any(y)]
    assert len(S) == (h+1)**M - 1
    # (a): classes {t y : t^h = 1}, size h; distinct classes on distinct lines
    Th = [t for t in range(1, p) if pow(t, h, p) == 1]
    Sset = set(S)
    for y in S[:200]:
        for t in range(1, p):
            ty = tuple(t*v % p for v in y)
            assert (ty in Sset) == (t in Th)
    nclass = len(S) // h
    assert nclass * h == len(S) and nclass == ((h+1)**M - 1)//h
    mu = Fr((h+1)**M - 1, h * p**a)
    EN_formula = h * mu
    Var_formula = Fr(h*h*nclass, p**a) * (1 - Fr(1, p**a))
    rows = list(product(range(p), repeat=M))
    R = len(rows)
    Rarr = np.array(rows, dtype=np.int64)
    Sarr = np.array(S, dtype=np.int64)
    I = ((Rarr @ Sarr.T) % p == 0).astype(np.int64)      # R x |S| indicator r.y = 0
    res = {}
    if a == 0:
        EN = Fr(len(S)); VarN = Fr(0); dist = {len(S): Fr(1)}
        rank_def = Fr(0)
        good_min_acc = Fr(len(S), p**M)
    elif a == 1:
        Nvals = I.sum(axis=1)                              # N for each 1 x M matrix
        dist = {}
        for v in Nvals: dist[int(v)] = dist.get(int(v), 0) + 1
        dist = {k: Fr(c, R) for k, c in dist.items()}
        EN = sum(k*w for k, w in dist.items()); VarN = sum(k*k*w for k, w in dist.items()) - EN**2
        zero_row = tuple([0]*M)
        rank_def = Fr(1, R)                               # only the zero row has rank 0
        # good banks: rank 1 and N >= EN/2; acceptance N / p^{M-1}
        accs = [Fr(int(Nvals[i]), p**(M-1)) for i in range(R) if rows[i] != zero_row and Nvals[i] >= EN/2]
        good_min_acc = min(accs) if accs else None
    elif a == 2:
        Nmat = I @ I.T                                     # N(x1, x2)
        vals, counts = np.unique(Nmat, return_counts=True)
        dist = {int(v): Fr(int(c), R*R) for v, c in zip(vals, counts)}
        EN = sum(k*w for k, w in dist.items()); VarN = sum(k*k*w for k, w in dist.items()) - EN**2
        # rank < 2 iff rows dependent
        def line_id(r):
            if not any(r): return None
            j = next(k for k in range(M) if r[k])
            inv = pow(r[j], p-2, p)
            return tuple(x*inv % p for x in r)
        lid = [line_id(r) for r in rows]
        # spot-check the line criterion against Gaussian elimination
        for i in range(0, R, max(1, R//40)):
            for j in range(0, R, max(1, R//40)):
                d1 = (lid[i] is None or lid[j] is None or lid[i] == lid[j])
                assert d1 == (rank_mod_p([rows[i], rows[j]], p) < 2)
        dep = 0; good_min_acc = None
        for i in range(R):
            for j in range(R):
                if lid[i] is None or lid[j] is None or lid[i] == lid[j]:
                    dep += 1
                elif Nmat[i, j] >= EN/2:
                    acc = Fr(int(Nmat[i, j]), p**(M-2))
                    good_min_acc = acc if good_min_acc is None or acc < good_min_acc else good_min_acc
        rank_def = Fr(dep, R*R)
    else:
        # a = 3: exact first and second moments only, via pair counts
        P1 = Fr(1, 1)
        EN = Fr(0); E2 = Fr(0)
        cnt1 = I.sum(axis=0)                               # rows with r.y = 0, per y
        EN = sum(Fr(int(c), R)**a for c in cnt1)
        pair = I.T @ I                                     # |S| x |S|: rows with r.y = r.y' = 0
        E2 = sum(Fr(int(c), R)**a for c in pair.flatten())
        VarN = E2 - EN**2
        dist = None; rank_def = None; good_min_acc = None
    ok = (EN == EN_formula) and (VarN == Var_formula) and (VarN <= h*EN)
    msg = f"(p,k,M,a)=({p},{kap},{M},{a}) h={h} |S|={len(S)} EN={EN} [{EN==EN_formula}] Var={VarN} [{VarN==Var_formula}]"
    if dist is not None:
        pr_low = sum(w for k, w in dist.items() if k < EN/2)
        cheb = Fr(4)/mu
        ok = ok and pr_low <= cheb
        msg += f" Pr[N<EN/2]={float(pr_low):.4g}<=4/mu={float(cheb):.4g} [{pr_low <= cheb}]"
    if rank_def is not None and a >= 1:
        rb = Fr(p**a - 1, p-1) / p**M
        ok = ok and rank_def <= rb
        msg += f" Pr[rank<a]={rank_def}<={rb} [{rank_def <= rb}]"
    if good_min_acc is not None:
        target = Fr((h+1)**M - 1, 2*p**M)
        ok = ok and good_min_acc >= target
        msg += f" min good acc={float(good_min_acc):.4g}>= {float(target):.4g} [{good_min_acc >= target}]"
    print(("OK  " if ok else "FAIL") + " " + msg)
    return ok

cases = [(5,2,3,1),(5,2,4,1),(5,4,3,1),(7,3,3,1),(7,2,3,2),(7,3,4,1),(5,2,3,2),
         (7,6,3,1),(11,5,3,1),(11,2,3,1),(13,3,3,1),(13,4,4,1),(5,2,4,2),(7,3,3,2),
         (5,2,0+3,0),(5,4,4,3),(7,3,4,3)]
allok = True
for cs in cases:
    allok &= case(*cs)
print("ALL OK" if allok else "SOME FAIL")
