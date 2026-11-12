"""Check 4 (exact, finite): phase rank and pole invariance.
For a list of copies (lam_i, kappa_i), possibly twisted by public automorphisms alpha_i, the
hidden phase of copy i at register value s is a1 s + a2 s^2 + a3 s^3 with (a1,a2,a3) functions
of the hypothesis v (closed form, Check 1).  We compute the F_p-rank R of the span of
{1} u {a_j^(i)} as functions on the hypothesis set, and the poles.
Prediction (Prop R): R = 1 + 3 * (number of distinct central-label LINES before twisting).
A twist alpha changes the label to lam o alpha but leaves the pole set {v : lam(iota v_1) = 0}
unchanged:  D_{lam o alpha}(alpha^{-1} v) = det(A) D_lam(v),  A = alpha on L/g2.
Usage: python check_rank.py p"""
import sys, random, numpy as np
from core import *

p = int(sys.argv[1]); rng = random.Random(5 * p)
labels = [(a, b) for a in range(p) for b in range(p) if (a, b) != (0, 0)]
E = np.eye(5, dtype=np.int64)


def aut(X1, Y1):
    Z1 = br(X1, Y1, p); return np.array([X1, Y1, Z1, br(X1, Z1, p), br(Y1, Z1, p)]).T % p  # columns


def inv_mod(M):
    n = len(M); A = [list(map(int, M[i])) + [int(i == j) for j in range(n)] for i in range(n)]
    for c in range(n):
        r = next(r for r in range(c, n) if A[r][c] % p); A[c], A[r] = A[r], A[c]
        iv = pow(A[c][c], -1, p); A[c] = [(x * iv) % p for x in A[c]]
        for r in range(n):
            if r != c and A[r][c] % p:
                f = A[r][c]; A[r] = [(x - f * y) % p for x, y in zip(A[r], A[c])]
    return np.array([row[n:] for row in A], dtype=np.int64)


def rank_mod(M):
    M = [list(map(int, r)) for r in M]; rk = 0; ncol = len(M[0])
    for c in range(ncol):
        piv = next((r for r in range(rk, len(M)) if M[r][c] % p), None)
        if piv is None:
            continue
        M[rk], M[piv] = M[piv], M[rk]; iv = pow(M[rk][c], -1, p)
        M[rk] = [(x * iv) % p for x in M[rk]]
        for r in range(len(M)):
            if r != rk and M[r][c] % p:
                f = M[r][c]; M[r] = [(x - f * y) % p for x, y in zip(M[r], M[rk])]
        rk += 1
        if rk == len(M):
            break
    return rk


def random_aut():
    while True:
        X1 = np.array([rng.randrange(p) for _ in range(5)]); Y1 = np.array([rng.randrange(p) for _ in range(5)])
        if (X1[0] * Y1[1] - X1[1] * Y1[0]) % p:
            return aut(X1, Y1)


def aut_mapping_line(lam_from, lam_to):
    """a public graded alpha with lam_from o alpha  proportional to lam_to on g3."""
    while True:
        al = random_aut()
        lu = (lam_from[0] * al[U, U] + lam_from[1] * al[W, U]) % p   # (lam o alpha)(u)
        lw = (lam_from[0] * al[U, W] + lam_from[1] * al[W, W]) % p   # (lam o alpha)(w)
        if (lu * lam_to[1] - lw * lam_to[0]) % p == 0 and (lu, lw) != (0, 0):
            return al


hyps = [np.array([1, r, c, d, e]) for r in range(p) for c in range(p) for d in range(p) for e in range(p)]


def rank_of(copies):
    """copies: list of (lam, kappa, alpha or None).  Returns R and number of distinct pole lines."""
    rows = []; good = []
    fr = []
    for lam, kap, al in copies:
        if al is None:
            fr.append((Frame(lam, kap, p), None, lam))
        else:
            lu = (lam[0] * al[U, U] + lam[1] * al[W, U]) % p
            lw = (lam[0] * al[U, W] + lam[1] * al[W, W]) % p
            fr.append((Frame((lu, lw), kap, p), inv_mod(al), lam))
    for v in hyps:
        vs = [(v if ai is None else (ai @ v) % p) for F, ai, _ in fr]
        if all(F.D(w) for (F, _, _), w in zip(fr, vs)):
            good.append([F.phase_coeffs(w) for (F, _, _), w in zip(fr, vs)])
    cols = len(good)
    M = [[1] * cols]
    for i in range(len(copies)):
        for j in range(3):
            M.append([good[c][i][j] for c in range(cols)])
    lines = {min(((t * l[0]) % p, (t * l[1]) % p) for t in range(1, p)) for _, _, l in fr}
    return rank_mod(M), len(lines)


# pole invariance identity on random data
bad_pole = 0
for _ in range(300):
    al = random_aut(); ai = inv_mod(al); lam = rng.choice(labels); v = random_v(p, rng)
    lu = (lam[0] * al[U, U] + lam[1] * al[W, U]) % p; lw = (lam[0] * al[U, W] + lam[1] * al[W, W]) % p
    w = (ai @ v) % p
    Dnew = (lu * w[X] + lw * w[Y]) % p; Dold = (lam[0] * v[X] + lam[1] * v[Y]) % p
    detA = int(al[X, X] * al[Y, Y] - al[X, Y] * al[Y, X]) % p
    if (Dnew - detA * Dold) % p:
        bad_pole += 1
print(f'p={p} pole_identity_failures={bad_pole}/300  (D_new == det(A) * D_old)')

cases = []
line_reps = sorted({min(((t * l[0]) % p, (t * l[1]) % p) for t in range(1, p)) for l in labels})
for k in (1, 2, 3, 4):
    cases.append((f'{k} distinct lines', [(l, rng.randrange(p), None) for l in rng.sample(line_reps, k)]))
lam0 = rng.choice(labels)
for k in (3, 4):
    cases.append((f'{k} copies, one line', [(((m * lam0[0]) % p, (m * lam0[1]) % p), rng.randrange(p), None)
                                           for m in rng.sample(range(1, p), k)]))
# public twists that put all LABELS on lam0's line
base = [l for l in rng.sample(line_reps, 3)]
tw = [(base[0], rng.randrange(p), None)] + [(l, rng.randrange(p), aut_mapping_line(l, base[0])) for l in base[1:]]
cases.append(('3 lines, copies 2-3 twisted onto line of copy 1', tw))
cases.append(('3 lines, all twisted by random public auts', [(l, rng.randrange(p), random_aut()) for l in base]))
for name, cps in cases:
    R, nl = rank_of(cps)
    k = len(cps)
    print(f'p={p} {name:50s} k={k} distinct_pole_lines={nl} rank={R} predicted={1 + 3 * nl} '
          f'template_bound p^(k-R+1)={float(p) ** (k - R + 1):.3g}')
