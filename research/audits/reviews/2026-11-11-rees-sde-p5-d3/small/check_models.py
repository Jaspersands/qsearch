#!/usr/bin/env python3
"""Independent checks for the small-set certification (p = 5, S = {0,+-1}, d = 3).

usage: check_models.py ORBITDIR KMIN KMAX [--closure] [--allow-inf]
  ORBITDIR holds Q_k.txt (orbit reps from orbits.c) and F_k.txt (models from feas.c).
(1) every F_k line is SF or M, its label set equals the k-th Q_k line, and its (Phi, gamma) passes
    labelsat.check_model (plain arithmetic on the ORIGINAL conditions, all 124 alpha, every
    direction); gamma_{-alpha} := -gamma_alpha for the 62 listed reps; SF lines: Phi = 0,
    gamma_alpha = g for all alpha.
(2) --closure: an independent numpy canonical form (min over frames of the sorted tuple of
    class codes min(v,-v); not the C bitmask) shows the Q_k reps are pairwise inequivalent,
    spanning, one vector per class, and that every one-point extension of a Q_k rep is
    equivalent to a Q_{k+1} rep (k < KMAX).  With Q_3 = one basis (GL_3 is transitive on bases),
    induction gives: Q_k is a complete, irredundant list of the GL_3-orbits of spanning k-subsets
    of the 62 classes.
"""
import sys, os, itertools, hashlib
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from labelsat import check_model, rank

p = 5
def code(v): return v[0] * 25 + v[1] * 5 + v[2]
def negv(v): return tuple((-x) % p for x in v)
ALL = [v for v in itertools.product(range(p), repeat=3) if any(v)]
CLS = np.zeros(125, dtype=np.int64)
for v in ALL: CLS[code(v)] = min(code(v), code(negv(v)))
REPS = [a for a in ALL if (next(x for x in a if x)) in (1, 2)]
assert len(REPS) == 62

def parse_vecs(s): return [tuple(int(c) for c in w) for w in s.split()]

def check_file(d, k):
    Q = [parse_vecs(l) for l in open(os.path.join(d, 'Q_%d.txt' % k))]
    F = open(os.path.join(d, 'F_%d.txt' % k)).read().splitlines()
    assert len(Q) == len(F), (k, len(Q), len(F))
    nsf = nm = ninf = 0
    for L, line in zip(Q, F):
        parts = [x.strip() for x in line.split('|')]
        tag, Ls = parts[0].split(' ', 1)
        assert parse_vecs(Ls) == L, (k, line)
        if tag == 'SF':
            g = parse_vecs(parts[1])[0]
            Phi = {l: (0, 0, 0) for l in L}; gamma = {a: g for a in ALL}; nsf += 1
        elif tag == 'M':
            ph = parse_vecs(parts[1]); gs = parse_vecs(parts[2]); assert len(ph) == len(L) and len(gs) == 62
            Phi = dict(zip(L, ph)); gamma = {}
            for a, g in zip(REPS, gs): gamma[a] = g; gamma[negv(a)] = negv(g)
            nm += 1
        elif tag == 'INF' and ALLOW_INF:
            ninf += 1; continue
        else:
            raise SystemExit('k=%d not certified: %s' % (k, line))
        ok, msg = check_model(L, Phi, gamma, p, 3, (0, 1, 4))
        if not ok: raise SystemExit('k=%d CHECK FAILED %s: %s' % (k, msg, line))
    h = hashlib.sha256(open(os.path.join(d, 'F_%d.txt' % k), 'rb').read()).hexdigest()
    print('k=%d lines %d: SF %d, M %d (all pass check_model), INF %d (not checked here); F_%d.txt sha256 %s' % (k, len(F), nsf, nm, ninf, k, h)); sys.stdout.flush()

# ---- independent canonical form ----
def inv3(B):  # batch inverse mod 5 of (N,3,3) int arrays, via adjugate
    a = B
    cof = np.empty_like(a)
    for r in range(3):
        for c in range(3):
            r1, r2 = [x for x in range(3) if x != r]; c1, c2 = [x for x in range(3) if x != c]
            cof[:, r, c] = ((-1) ** (r + c)) * (a[:, r1, c1] * a[:, r2, c2] - a[:, r1, c2] * a[:, r2, c1])
    det = (a[:, 0, 0] * cof[:, 0, 0] + a[:, 0, 1] * cof[:, 0, 1] + a[:, 0, 2] * cof[:, 0, 2]) % p
    dinv = np.array([0, 1, 3, 2, 4])[det]
    return (np.transpose(cof, (0, 2, 1)) * dinv[:, None, None]) % p, det

def canon(X):
    X = np.array(X, dtype=np.int64); k = len(X)
    tr = np.array(list(itertools.permutations(range(k), 3)))
    sg = np.array([(1, s, t) for s in (1, 4) for t in (1, 4)])
    B = X[tr]                                   # (T,3 vectors,3 coords)
    B = (B[:, None, :, :] * sg[None, :, :, None]) % p   # (T,4,3,3)
    B = np.transpose(B.reshape(-1, 3, 3), (0, 2, 1))     # columns = frame vectors
    A, det = inv3(B); A = A[det != 0]
    img = np.einsum('nij,kj->nki', A, X) % p              # (N,k,3)
    cl = np.sort(CLS[img[:, :, 0] * 25 + img[:, :, 1] * 5 + img[:, :, 2]], axis=1)
    return min(map(tuple, cl))

def closure(d, kmin, kmax):
    Qs = {k: [parse_vecs(l) for l in open(os.path.join(d, 'Q_%d.txt' % k))] for k in range(kmin, kmax + 1)}
    C = {}
    for k in range(kmin, kmax + 1):
        cs = set()
        for X in Qs[k]:
            assert len(X) == k and len(set(CLS[[code(v) for v in X]])) == k and rank(X, p, 3) == 3
            cs.add(canon(X))
        assert len(cs) == len(Qs[k]), 'reps not pairwise inequivalent at k=%d' % k
        C[k] = cs; print('k=%d: %d reps, pairwise inequivalent, spanning' % (k, len(cs))); sys.stdout.flush()
    for k in range(kmin, kmax):
        n = 0
        for X in Qs[k]:
            used = set(CLS[[code(v) for v in X]])
            for v in REPS:
                if CLS[code(v)] in used: continue
                assert canon(X + [v]) in C[k + 1], ('extension missing', k, X, v)
                n += 1
        print('k=%d -> %d: %d extensions, all equivalent to a listed rep' % (k, k + 1, n)); sys.stdout.flush()

ALLOW_INF = '--allow-inf' in sys.argv
if __name__ == '__main__':
    d, kmin, kmax = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    if '--closure' in sys.argv: closure(d, kmin, kmax)
    else:
        for k in range(kmin, kmax + 1): check_file(d, k)
