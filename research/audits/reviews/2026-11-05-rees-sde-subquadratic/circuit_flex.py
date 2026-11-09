"""Exact checks of Theorem 1 (one circuit gives at most one flexible direction).

For a column set S in F_p^q, R(S) = {sum_{i in S} x_i lambda_i : x in Sq^S}.
A subspace T is *flexible* for S if T is contained in R(S).  (Working in F_p^q
is working modulo the current flexible space U; Theorem 1 is stated mod U.)

Theorem 1: if S is a circuit (rank |S|-1, dependency delta with full support)
and delta is not monochromatic, then R(S) contains no 2-dimensional subspace;
moreover for i, j with cls(delta_i) != cls(delta_j) and every nonzero
u in H_ij = span(S \\ {i, j}), at most one class of multiples c*u lies in R(S).

Usage:  python circuit_flex.py circuits   -> T1 checks on random + adversarial circuits
        python circuit_flex.py kernel2    -> e = 2 objects (|S| = q + 2): max flexible dim
"""
import itertools
import random
import sys

import numpy as np

from common import F, kernel, rank, realizable, proj_points


def flexible_lines(Fd, R, q):
    p, k = Fd.p, Fd.k
    cs = np.arange(1, p)
    cls_of_c = np.array([Fd.cls(int(c)) for c in cs])
    fl = set()
    for u in proj_points(p, q):
        pts = tuple((cs * x) % p for x in u)
        hit = R[pts]
        if len(set(cls_of_c[hit].tolist())) == k:
            fl.add(u)
    return fl


def classes_on_line(Fd, R, u):
    p = Fd.p
    cs = np.arange(1, p)
    pts = tuple((cs * x) % p for x in u)
    hit = R[pts]
    return {Fd.cls(int(c)) for c in cs[hit]}


def canon(v, p):
    nz = next(x for x in v if x % p)
    iv = pow(nz, p - 2, p)
    return tuple((x * iv) % p for x in v)


def contains_plane(Fd, fl, q):
    """Does some 2-dim subspace have all its p+1 lines flexible?  (q = 2 or 3)."""
    p = Fd.p
    if q == 2:
        return len(fl) == p + 1
    for n in proj_points(p, 3):
        # basis of the plane n.v = 0
        basis = []
        for e in ([1, 0, 0], [0, 1, 0], [0, 0, 1]):
            pass
        # find two independent solutions
        sols = []
        for v in itertools.product(range(p), repeat=3):
            if any(v) and (n[0] * v[0] + n[1] * v[1] + n[2] * v[2]) % p == 0:
                if not sols or rank([sols[0], list(v)], p) == 2:
                    sols.append(list(v))
                    if len(sols) == 2:
                        break
        b1, b2 = sols
        ok = True
        for s in range(p + 1):
            v = b1 if s == p else [(b2[i] + s * b1[i]) % p for i in range(3)]
            if canon(v, p) not in fl:
                ok = False
                break
        if ok:
            return True
    return False


def make_circuit(Fd, rng, q, pattern):
    """Columns lambda_1..lambda_{q+1} in F_p^q with dependency delta of class pattern."""
    p = Fd.p
    while True:
        B = [[rng.randrange(p) for _ in range(q)] for _ in range(q)]
        if rank(B, p) == q:
            break
    if pattern is None:
        delta = [rng.randrange(1, p) for _ in range(q + 1)]
    else:
        delta = [(Fd.rep(c) * pow(rng.choice(Fd.P), 1, p)) % p for c in pattern]
    # lambda_{q+1} = -(1/delta_{q+1}) sum delta_i lambda_i
    iv = pow(delta[q], p - 2, p)
    last = [(-iv * sum(delta[i] * B[i][j] for i in range(q))) % p for j in range(q)]
    cols = B + [last]
    return cols, delta


def h_ij_points(Fd, cols, i, j, q):
    """projective points of span(cols minus {i,j})."""
    p = Fd.p
    rest = [cols[l] for l in range(len(cols)) if l not in (i, j)]
    pts = set()
    for coef in itertools.product(range(p), repeat=len(rest)):
        if not any(coef):
            continue
        v = [sum(c * r[t] for c, r in zip(coef, rest)) % p for t in range(q)]
        if any(v):
            pts.add(canon(v, p))
    return pts


def check_circuit(Fd, cols, delta, q):
    p = Fd.p
    R = realizable(Fd, cols, q)
    fl = flexible_lines(Fd, R, q)
    plane = contains_plane(Fd, fl, q) if len(fl) >= 2 else False
    classes = [Fd.cls(d) for d in delta]
    mono = len(set(classes)) == 1
    strong_ok = True
    for i, j in itertools.combinations(range(q + 1), 2):
        if classes[i] == classes[j]:
            continue
        for u in h_ij_points(Fd, cols, i, j, q):
            if len(classes_on_line(Fd, R, u)) > 1:
                strong_ok = False
    tri = None
    if Fd.k == 2 and not mono:
        # the triangular flexible vector: w = sum over the class-0 part of delta_i lambda_i
        w = [sum(delta[i] * cols[i][t] for i in range(q + 1) if classes[i] == 0) % p for t in range(q)]
        tri = any(w) and canon(w, p) in fl
    return dict(mono=mono, nflex=len(fl), plane=plane, strong=strong_ok, tri=tri)


def run_circuits():
    rng = random.Random(20261105)
    cases = [(5, 2, 2), (7, 2, 2), (11, 2, 2), (13, 2, 2), (29, 2, 2), (13, 3, 2), (7, 3, 2),
             (13, 4, 2), (5, 4, 2), (13, 2, 3), (7, 2, 3), (7, 3, 3), (13, 3, 3), (13, 4, 3)]
    total = bad = 0
    for p, k, q in cases:
        Fd = F(p, k)
        pats = [None] * 6
        pats += [[0] * q + [1], [0, 1] * ((q + 1) // 2) + [0] * ((q + 1) % 2)]
        if k >= 3:
            pats.append([t % k for t in range(q + 1)])
        pats.append([0] * (q + 1))  # monochromatic control
        stats = []
        for pat in pats:
            pat = None if pat is None else pat[:q + 1]
            cols, delta = make_circuit(Fd, rng, q, pat)
            # skip if not a circuit (some q-subset dependent) -- only possible for random delta? no:
            # delta has full support and B is a basis, so S is a circuit.
            r = check_circuit(Fd, cols, delta, q)
            total += 1
            if not r['mono'] and (r['plane'] or not r['strong']):
                bad += 1
            if r['tri'] is False:
                bad += 1
            stats.append((pat, r))
        print(f"p={p} kappa={k} q={q}:")
        for pat, r in stats:
            print(f"   pattern={pat} mono={r['mono']} flexible_lines={r['nflex']} "
                  f"plane_inside={r['plane']} H_ij_one_class={r['strong']} triangular_line_flexible={r['tri']}")
    print(f"TOTAL circuits {total}; violations of Theorem 1 (non-mono only) or of the triangular line: {bad}")


def run_kernel2():
    rng = random.Random(7)
    cases = [(5, 2, 2), (7, 2, 2), (13, 2, 2), (29, 2, 2), (13, 3, 2), (13, 4, 2),
             (7, 2, 3), (13, 2, 3), (29, 2, 3), (13, 3, 3), (37, 3, 3)]
    for p, k, q in cases:
        Fd = F(p, k)
        dims = []
        for _ in range(4):
            cols = [[rng.randrange(p) for _ in range(q)] for _ in range(q + 2)]
            if rank(cols, p) < q:
                continue
            R = realizable(Fd, cols, q)
            if R.all():
                dims.append(q)
                continue
            fl = flexible_lines(Fd, R, q)
            d = 0 if not fl else (2 if len(fl) >= 2 and contains_plane(Fd, fl, q) else 1)
            dims.append(d)
        print(f"p={p} kappa={k} q={q} |S|=q+2: max flexible dims over 4 random objects = {dims}")


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'circuits'
    if mode == 'circuits':
        run_circuits()
    else:
        run_kernel2()
