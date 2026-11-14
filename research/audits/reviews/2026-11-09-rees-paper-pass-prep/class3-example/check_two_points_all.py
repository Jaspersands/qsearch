"""For EVERY Lie subalgebra h of the filiform n4 over F_5 and F_7, by exact linear algebra:
 (a) the three-point pullback E_1^-1(h) cap E_2^-1(h) cap E_3^-1(h) equals hlift;
 (b) the two-point pullback P_12 = E_1^-1(h) cap E_2^-1(h) equals hlift iff x4 in h,
     and otherwise equals hlift + F_p u with u = 2X4 - 3Y4 + W;
 (c) some dilation delta_theta, theta != 1, preserves P_12 iff x4 in h
     (and then every dilation does).
Usage: nice -n 19 /opt/anaconda3/bin/python check_two_points_all.py
"""
import numpy as np
from verify_class3 import subalgebras, GRADE, LIDX, N, M, U_TWO, hlift_from_definition, rank


def nullspace(A, p):
    """Basis of {x : A x = 0} over F_p, A given as list of rows of length N."""
    A = [list(map(int, r)) for r in A]
    ncol = N
    piv, r = [], 0
    for c in range(ncol):
        k = next((i for i in range(r, len(A)) if A[i][c] % p), None)
        if k is None:
            continue
        A[r], A[k] = A[k], A[r]
        inv = pow(A[r][c], -1, p)
        A[r] = [x*inv % p for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c] % p:
                f = A[i][c]
                A[i] = [(x - f*y) % p for x, y in zip(A[i], A[r])]
        piv.append(c)
        r += 1
    free = [c for c in range(ncol) if c not in piv]
    basis = []
    for f in free:
        v = [0]*ncol
        v[f] = 1
        for i, c in enumerate(piv):
            v[c] = (-A[i][f]) % p
        basis.append(v)
    return basis


def quotient_functionals(h, p):
    """Rows spanning h^perp in F_p^4 (so x in h iff all rows . x = 0)."""
    rows = [list(map(int, r)) for r in h] if len(h) else []
    # nullspace of h as a k x 4 matrix
    ns = []
    A = rows
    if not A:
        return [list(r) for r in np.eye(M, dtype=int)]
    # reuse nullspace on padded matrix
    pad = [r + [0]*(N - M) for r in A]
    for v in nullspace(pad, p):
        if any(v[M:]):
            continue
        ns.append(v[:M])
    return ns


def pullback(h, points, p):
    F = quotient_functionals(h, p)
    rows = []
    for s in points:
        Es = np.zeros((M, N), dtype=np.int64)
        for j in range(N):
            Es[LIDX[j], j] = pow(s, int(GRADE[j]), p)
        for f in F:
            rows.append(list((np.array(f) @ Es) % p))
    return nullspace(rows, p) if rows else [list(r) for r in np.eye(N, dtype=int)]


def same_space(A, B, p):
    return rank(A, p) == rank(B, p) == rank(list(A) + list(B), p)


def contains(A, B, p):
    return rank(list(A) + list(B), p) == rank(A, p)


for p in (5, 7):
    subs = subalgebras(p)
    u = [x % p for x in U_TWO]
    bad = []
    for B in subs:
        hl = hlift_from_definition(B, p)
        hl = hl if hl else []
        x4in = len(B) > 0 and rank(list(B) + [[0, 0, 0, 1]], p) == rank(B, p)
        P123 = pullback(B, (1, 2, 3), p)
        P12 = pullback(B, (1, 2), p)
        ok_a = same_space(P123, hl, p) if hl else rank(P123, p) == 0
        target = hl if x4in else hl + [u]
        ok_b = same_space(P12, target, p) if target else rank(P12, p) == 0
        pres = [th for th in range(2, p)
                if contains(P12, [[(x*pow(th, int(GRADE[j]), p)) % p for j, x in enumerate(v)] for v in P12], p)]
        ok_c = (pres == list(range(2, p))) if x4in else (pres == [])
        if not (ok_a and ok_b and ok_c):
            bad.append((B.tolist(), ok_a, ok_b, pres))
    print(f"[C4h] {'PASS' if not bad else 'FAIL'}: p={p}: all {len(subs)} subalgebras: three-point pullback = hlift; "
          f"two-point pullback = hlift (x4 in h) or hlift + F_p u (x4 not in h); a dilation theta != 1 preserves "
          f"it iff x4 in h. bad = {bad[:3]}", flush=True)
