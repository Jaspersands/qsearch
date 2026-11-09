"""Exhaustive check of Lemma s3-moment and Lemma s3-node(a),(b) on small fields.

For each (p, kappa, M, a), enumerate every a x M matrix X over F_p and compute
N(X) = |ker X cap S| with S = P_kappa^M minus 0. Checks, in exact arithmetic:
  E N = h mu, Var N = h^2 |D| q (1-q) (q = p^-a), Var N <= h E N,
  Pr[N < EN/2] <= 4/mu, Pr[rank X < a] <= (p^a-1)/(p-1) p^-M <= 2 p^{a-M},
  on good banks (rank a, N >= EN/2) the acceptance N/p^{M-a} >= ((h+1)^M-1)/(2p^M),
  and, when p >= 2 kappa, that this is >= 1/(4 kappa^M).
Also checks Lemma s3-moment(a): classes {ty : t^h = 1} have size h and distinct
classes span distinct lines. Tuples are chosen independently of the appendix's list.

Run: /opt/anaconda3/bin/python -I moment_exhaustive.py
"""
import itertools
from fractions import Fraction as Fr

import numpy as np

CASES = [
    (3, 2, 4, 1), (3, 2, 5, 2), (3, 1, 3, 2), (5, 2, 4, 2), (5, 4, 4, 2), (5, 4, 3, 0),
    (7, 2, 3, 2), (7, 3, 3, 2), (7, 6, 3, 2), (7, 3, 5, 1), (11, 5, 4, 1), (11, 2, 3, 1),
    (13, 3, 4, 1), (13, 4, 5, 1), (13, 6, 4, 1), (5, 1, 3, 2),
]


def rank_mod_p(A, p):
    A = [list(r) for r in A]
    rows, cols = len(A), len(A[0]) if A else 0
    r = 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if A[i][c] % p), None)
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        inv = pow(A[r][c], p - 2, p)
        A[r] = [x * inv % p for x in A[r]]
        for i in range(rows):
            if i != r and A[i][c] % p:
                f = A[i][c]
                A[i] = [(x - f * y) % p for x, y in zip(A[i], A[r])]
        r += 1
    return r


def run(p, kappa, M, a):
    assert (p - 1) % kappa == 0
    h = (p - 1) // kappa
    P = sorted({0} | {pow(x, kappa, p) for x in range(1, p)})
    assert len(P) == h + 1
    S = [y for y in itertools.product(P, repeat=M) if any(y)]
    Sset = set(S)
    # Lemma s3-moment(a)
    units = [t for t in range(1, p) if pow(t, h, p) == 1]
    seen, classes = set(), []
    for y in S:
        if y in seen:
            continue
        cl = {tuple(t * v % p for v in y) for t in units}
        assert cl <= Sset and len(cl) == h
        for t in range(1, p):
            if pow(t, h, p) != 1:
                ty = tuple(t * v % p for v in y)
                assert ty not in Sset, (p, kappa, y, t)
        seen |= cl
        classes.append(y)
    D = len(classes)
    assert D * h == len(S) == (h + 1) ** M - 1
    Sarr = np.array(S, dtype=np.int64)  # |S| x M
    q = Fr(1, p ** a)
    mu = Fr((h + 1) ** M - 1, h * p ** a)
    EN_formula = h * mu
    VarN_formula = h * h * D * q * (1 - q)
    total = p ** (a * M)
    sumN = sumN2 = 0
    low = 0
    rankdef = 0
    worst_acc = None
    entries = list(itertools.product(range(p), repeat=a * M)) if a > 0 else [()]
    chunk = 20000
    for start in range(0, len(entries), chunk):
        block = np.array(entries[start:start + chunk], dtype=np.int64)
        if a == 0:
            Ns = np.array([len(S)])
            Xs = [np.zeros((0, M), dtype=np.int64)]
        else:
            Xs = block.reshape(-1, a, M)
            # (n, a, M) x (M, |S|) -> (n, a, |S|)
            prod = np.einsum('nam,sm->nas', Xs, Sarr) % p
            Ns = (prod == 0).all(axis=1).sum(axis=1)
        for X, N in zip(Xs, Ns):
            N = int(N)
            sumN += N
            sumN2 += N * N
            r = rank_mod_p(X.tolist(), p) if a > 0 else 0
            if r < a:
                rankdef += 1
            if Fr(N) < EN_formula / 2:
                low += 1
            if r == a and Fr(N) >= EN_formula / 2:
                acc = Fr(N, p ** (M - a))
                if worst_acc is None or acc < worst_acc:
                    worst_acc = acc
    EN = Fr(sumN, total)
    VarN = Fr(sumN2, total) - EN * EN
    out = {
        "EN_exact": EN == EN_formula,
        "Var_exact": VarN == VarN_formula,
        "Var<=hEN": VarN <= h * EN,
        "cheb": Fr(low, total) <= 4 / mu,
        "rank": Fr(rankdef, total) <= Fr(p ** a - 1, p - 1) / p ** M <= 2 * Fr(p ** a, p ** M),
        "acc_good": worst_acc is None or worst_acc >= Fr((h + 1) ** M - 1, 2 * p ** M),
    }
    if p >= 2 * kappa and worst_acc is not None:
        out["acc>=1/4k^M"] = Fr((h + 1) ** M - 1, 2 * p ** M) >= Fr(1, 4 * kappa ** M)
    return out, float(Fr(low, total)), float(4 / mu), float(Fr(rankdef, total))


allok = True
for case in CASES:
    res, plow, cheb, prk = run(*case)
    ok = all(res.values())
    allok &= ok
    print(case, "ok" if ok else "FAIL", res, f"Pr[N<EN/2]={plow:.4g} 4/mu={cheb:.4g} Pr[rank<a]={prk:.4g}")
print("ALL OK" if allok else "SOME FAIL")
