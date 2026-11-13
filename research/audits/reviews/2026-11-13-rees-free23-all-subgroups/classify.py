"""Exhaustive classification of the subalgebras (= subgroups, Lazard) of free23 over F_p, p in {5, 7}.
AI-written 2026-11-13, pending human review.  Finite check only (falsification).

Basis X0, X1, Z=[X0,X1], U=[X0,Z], W=[X1,Z]; coordinates (v0, v1, vz, vu, vw).
For every subspace h of F_p^5 closed under the bracket we record
  d1 = dim of the image in V = L/gamma_2,  s = h cap gamma_2,  s3 = h cap gamma_3,
and check (a) the type list and counts of the report's Lemma T (sec. B1), and (b) the branch implications P1-P6
used by the decision procedure (sec. B3).  Usage: python classify.py p
"""
import sys, itertools, numpy as np

p = int(sys.argv[1])

def br(a, b):
    return np.array([0, 0, a[0]*b[1]-a[1]*b[0], a[0]*b[2]-a[2]*b[0], a[1]*b[2]-a[2]*b[1]], dtype=np.int64) % p

def rref(M):
    M = [list(map(int, r)) for r in M]; rows = len(M); cols = 5 if rows == 0 else len(M[0]); r = 0; piv = []
    for c in range(cols):
        q = next((i for i in range(r, rows) if M[i][c] % p), None)
        if q is None: continue
        M[r], M[q] = M[q], M[r]; iv = pow(M[r][c], -1, p); M[r] = [x*iv % p for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c] % p:
                f = M[i][c]; M[i] = [(x - f*y) % p for x, y in zip(M[i], M[r])]
        piv.append(c); r += 1
    return [tuple(x) for x in M[:r]], piv

def rank(M): return len(rref(M)[0]) if len(M) else 0

def subspaces(k):
    """all k-dim subspaces of F_p^5 as RREF bases"""
    for piv in itertools.combinations(range(5), k):
        free = [(i, c) for i in range(k) for c in range(5) if c > piv[i] and c not in piv]
        for vals in itertools.product(range(p), repeat=len(free)):
            M = np.zeros((k, 5), dtype=np.int64)
            for i in range(k): M[i, piv[i]] = 1
            for (i, c), v in zip(free, vals): M[i, c] = v
            yield M

def in_span(B, v):
    return rank(list(B) + [v]) == rank(B)

def intersect_with_coords(B, coords):
    """h cap span(e_c : c in coords): null-space computation"""
    # x in h with x_c = 0 for c not in coords: solve t B restricted to other coords = 0
    k = len(B)
    if k == 0: return []
    other = [c for c in range(5) if c not in coords]
    A = np.array([[int(B[i][c]) for i in range(k)] for c in other], dtype=np.int64) if other else np.zeros((0, k), dtype=np.int64)
    # null space of A (len(other) x k)
    R, piv = rref(A.tolist()) if len(A) else ([], [])
    freev = [j for j in range(k) if j not in piv]
    basis = []
    for fv in freev:
        t = [0]*k; t[fv] = 1
        for row, pc in zip(R, piv): t[pc] = (-row[fv]) % p
        basis.append(tuple(int(x) % p for x in (np.array(t) @ np.array(B)) ))
    return rref(basis)[0] if basis else []

G2 = [2, 3, 4]; G3 = [3, 4]
cnt = {}; viol = {f'P{i}': 0 for i in range(1, 8)}; total = 0
for k in range(0, 6):
    gen = [np.zeros((0, 5), dtype=np.int64)] if k == 0 else subspaces(k)
    for M in gen:
        B = [tuple(int(x) for x in r) for r in M]
        ok = all(in_span(B, br(np.array(B[i]), np.array(B[j]))) for i in range(k) for j in range(i+1, k)) if k else True
        if not ok: continue
        total += 1
        d1 = rank([b[:2] for b in B]) if k else 0
        s = intersect_with_coords(B, G2); s3 = intersect_with_coords(B, G3)
        ds, ds3 = len(s), len(s3)
        # type label (Lemma T)
        if d1 == 2: t = 'G'
        elif d1 == 0:
            t = {(0, 0): 'trivial', (1, 1): 'central line', (1, 0): 'line Z+c', (2, 2): 'gamma3', (2, 1): 'plane Z+c,q', (3, 2): 'gamma2'}[(ds, ds3)]
        else:
            e = next(b[:2] for b in B if (b[0] or b[1]))
            ez = (0, 0, 0, e[0] % p, e[1] % p)
            if ds == 0: t = 'hard cyclic (F23)'
            elif ds == 1 and ds3 == 1: t = 'eta+central line: special' if in_span(s, ez) else 'eta+central line: generic (b)'
            elif ds == 2 and ds3 == 2: t = 'eta+gamma3 (c)'
            elif ds == 2 and ds3 == 1:
                t = 'eta+Heis plane (d)'
                viol['P7'] += int(not in_span(s, ez))          # S not in gamma3 forces [e,Z] in S
            elif ds == 3: t = 'eta+gamma2 (e)'
            else: t = 'UNEXPECTED %s' % ((d1, ds, ds3),)
        cnt[t] = cnt.get(t, 0) + 1
        # branch implications
        if ds3 == 0 and ds == 1: viol['P1'] += int(d1 != 0)
        if ds3 == 0 and ds == 0: viol['P2'] += int(not ((d1 == 0 and k == 0) or (d1 == 1 and k == 1)))
        if ds3 == 1:
            q = s3[0]; g0 = (q[3], q[4])
            m = [(g0[0], g0[1], 0, 0, 0), (0, 0, 1, 0, 0), (0, 0, 0, 1, 0), (0, 0, 0, 0, 1)]
            # T = h cap m
            Bm = rref(m)[0]
            Tb = [b for b in B]  # compute h cap m via dimension formula and explicit check
            inter = []
            for tvec in itertools.product(range(p), repeat=k):
                v = tuple(int(x) % p for x in np.array(tvec) @ np.array(B)) if k else ()
                if k and in_span(Bm, v): inter.append(v)
            T = rref(inter)[0] if inter else []
            TnotG2 = any(r[0] or r[1] for r in T)
            if TnotG2: viol['P3'] += int(len(T) != k)
            else:
                if ds == 1: viol['P3'] += int(not (k == 1 or (d1 == 1 and k == 2)))
                if ds == 2: viol['P3'] += int(k != 2)
        if ds == 2 and ds3 == 2: viol['P4'] += int(not (k == 2 or (d1 == 1 and k == 3)))
        if ds == 3: viol['P5'] += int(k < 3)
        if d1 == 2: viol['P6'] += int(k != 5)

pred = {'trivial': 1, 'central line': p+1, 'line Z+c': p*p, 'gamma3': 1, 'plane Z+c,q': (p+1)*p, 'gamma2': 1,
        'hard cyclic (F23)': (p+1)*p**3, 'eta+central line: generic (b)': (p+1)*p*p*p, 'eta+central line: special': (p+1)*p*p,
        'eta+gamma3 (c)': (p+1)*p, 'eta+Heis plane (d)': (p+1)*p*p, 'eta+gamma2 (e)': p+1, 'G': 1}
print('p = %d: %d subalgebras (predicted %d)' % (p, total, sum(pred.values())))
for t in pred: print('  %-32s observed %8d  predicted %8d  %s' % (t, cnt.get(t, 0), pred[t], 'OK' if cnt.get(t, 0) == pred[t] else 'MISMATCH'))
extra = set(cnt) - set(pred)
print('  unexpected types:', extra if extra else 'none')
print('  branch-implication violations:', viol)
