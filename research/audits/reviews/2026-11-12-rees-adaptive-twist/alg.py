"""Nilpotent Lie algebras over F_p -> Lazard p-group pc presentations for GAP (adaptive-twist audit).

Algebras are given by structure constants {(i,j): {k: c}} in a natural basis (0-based).
adapt() rewrites them in a basis adapted to the lower central series (every span(e_i..e_m) is
an ideal and [e_i, L] lies in span(e_{i+1}..)), so exp(e_1),...,exp(e_m) is a pc sequence.
Group law: BCH truncated at class <= 4 (lie.bch), valid for p > class."""
import sys, os, itertools, json, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', '2026-11-12-rees-direct-twist-class3-referee'))
from lie import tensor, br, jacobi_ok, rref, rank, lcs, bch

HAND = {
    # class 3
    'fil4':    (4, {(0, 1): {2: 1}, (0, 2): {3: 1}}),
    'free23':  (5, {(0, 1): {2: 1}, (0, 2): {3: 1}, (1, 2): {4: 1}}),
    'fil4+1':  (5, {(0, 1): {2: 1}, (0, 2): {3: 1}}),
    'L55':     (5, {(0, 1): {2: 1}, (0, 2): {4: 1}, (1, 3): {4: 1}}),       # degrees (1,1,2,2,3), not Carnot
    'N7a':     (7, {(0, 1): {3: 1}, (0, 2): {4: 1}, (1, 2): {5: 1}, (0, 3): {6: 1}}),
    'N7b':     (7, {(0, 1): {3: 1}, (0, 2): {4: 1}, (1, 2): {5: 1}, (0, 5): {6: 1}, (1, 4): {6: 1}}),
    # class 4
    'L57':     (5, {(0, 1): {2: 1}, (0, 2): {3: 1}, (0, 3): {4: 1}}),       # standard filiform, Carnot
    'L56':     (5, {(0, 1): {2: 1}, (0, 2): {3: 1}, (0, 3): {4: 1}, (1, 2): {4: 1}}),  # degrees (1,2,3,4,5)
    'free24':  (8, {(0, 1): {2: 1}, (0, 2): {3: 1}, (1, 2): {4: 1},
                    (0, 3): {5: 1}, (1, 3): {6: 1}, (0, 4): {6: 1}, (1, 4): {7: 1}}),
}
# free24: x,y,z=[x,y],u=[x,z],w=[y,z],[x,u]=a,[y,u]=[x,w]=b,[y,w]=c  (Hall basis, dim 8)


def adapt(m, brk, p):
    C = tensor(m, brk, p)
    assert jacobi_ok(C, p), 'Jacobi fails'
    series = lcs(C, p)                       # [L, g2, g3, ..., 0] as RREF row bases
    cls = len(series) - 1; assert len(series[-1]) == 0
    # build basis: complement of g2 in L, then of g3 in g2, ...
    basis = []; level = []
    for k in range(len(series) - 1):
        top = [list(r) for r in series[k]]; low = [list(r) for r in series[k + 1]]
        cur = list(low)
        for v in top:
            if rank(cur + [v], p) > rank(cur, p):
                cur.append(v); basis.append(v); level.append(k + 1)
    B = np.array(basis, dtype=np.int64) % p          # rows = new basis in old coords
    Binv = np.array(inv_mod(B, p))
    m2 = len(basis); assert m2 == m
    # new structure constants: [b_i, b_j] = sum_k D[i,j,k] b_k
    D = np.zeros((m, m, m), dtype=np.int64)
    for i in range(m):
        for j in range(m):
            v = br(B[i], B[j], C, p)                 # old coords
            D[i, j] = (v @ Binv) % p                 # new coords (row vector times B^{-1})
    return D, level, cls


def inv_mod(B, p):
    m = len(B)
    aug = [list(map(int, B[i])) + [int(i == j) for j in range(m)] for i in range(m)]
    R, piv = rref(aug, p)
    assert piv[:m] == list(range(m))
    return [r[m:] for r in R]


def normal_word(X, D, p, cls):
    """exponents a with exp(X) = exp(e_1)^{a_1} ... exp(e_m)^{a_m}"""
    m = D.shape[0]; X = np.array(X, dtype=np.int64) % p; a = []
    for i in range(m):
        ai = int(X[i]); a.append(ai)
        e = np.zeros(m, dtype=np.int64); e[i] = (-ai) % p
        X = bch(e, X, D, p, cls)
        assert not X[:i + 1].any()
    return a


def gap_pc(name, D, level, cls, p):
    m = D.shape[0]; E = np.eye(m, dtype=np.int64)
    lines = [f'# {name} over F_{p}, dim {m}, class {cls}, levels {level}',
             f'F := FreeGroup({m});; g := GeneratorsOfGroup(F);;',
             f'coll := SingleCollector(F, ListWithIdenticalEntries({m}, {p}));;']
    for i in range(m):
        for j in range(i + 1, m):
            Y = bch(bch((-E[i]) % p, E[j], D, p, cls), E[i], D, p, cls)   # g_i^-1 g_j g_i
            a = normal_word(Y, D, p, cls)
            if a == [int(k == j) for k in range(m)]: continue
            w = '*'.join(f'g[{k + 1}]^{a[k]}' for k in range(m) if a[k]) or 'One(F)'
            lines.append(f'SetConjugate(coll, {j + 1}, {i + 1}, {w});')
    lines.append('G := GroupByRws(coll);;')
    lines.append(f'LEVEL := {[int(x) for x in level]};; CLS := {cls};; P := {p};; NAME := "{name}";;')
    return '\n'.join(lines)


if __name__ == '__main__':
    # quick self-test: group law is associative on random triples, pc words reproduce X
    rng = np.random.default_rng(1)
    for name, (m, brk) in HAND.items():
        for p in (5, 7):
            D, level, cls = adapt(m, brk, p)
            for _ in range(50):
                X, Y, Z = (rng.integers(0, p, m) for _ in range(3))
                l = bch(bch(X, Y, D, p, cls), Z, D, p, cls); r = bch(X, bch(Y, Z, D, p, cls), D, p, cls)
                assert (l == r).all(), (name, p)
            print(name, p, 'class', cls, 'levels', level, 'assoc ok')


# de Graaf's 5- and 6-dimensional nilpotent Lie algebras of class 3 and 4 (char != 2), as recalled
# (LieAlgDB is not installed; every table is Jacobi-checked by adapt(); completeness against the
# source was NOT checked). 1-based brackets as in de Graaf; eps runs over {0, 1, nonsquare}.
def _dg(pairs):
    return {(i - 1, j - 1): {k - 1: c for k, c in d.items()} for (i, j), d in pairs.items()}

def degraaf(p):
    ns = next(a for a in range(2, p) if pow(a, (p - 1) // 2, p) == p - 1)
    out = {}
    out['L5,5'] = (5, _dg({(1, 2): {3: 1}, (1, 3): {5: 1}, (2, 4): {5: 1}}))
    out['L5,6'] = (5, _dg({(1, 2): {3: 1}, (1, 3): {4: 1}, (1, 4): {5: 1}, (2, 3): {5: 1}}))
    out['L5,7'] = (5, _dg({(1, 2): {3: 1}, (1, 3): {4: 1}, (1, 4): {5: 1}}))
    out['L5,9'] = (5, _dg({(1, 2): {3: 1}, (1, 3): {4: 1}, (2, 3): {5: 1}}))
    out['L6,10'] = (6, _dg({(1, 2): {3: 1}, (1, 3): {6: 1}, (4, 5): {6: 1}}))
    out['L6,11'] = (6, _dg({(1, 2): {3: 1}, (1, 3): {4: 1}, (1, 4): {6: 1}, (2, 3): {6: 1}, (2, 5): {6: 1}}))
    out['L6,12'] = (6, _dg({(1, 2): {3: 1}, (1, 3): {4: 1}, (1, 4): {6: 1}, (2, 5): {6: 1}}))
    out['L6,13'] = (6, _dg({(1, 2): {3: 1}, (1, 3): {5: 1}, (2, 4): {5: 1}, (1, 5): {6: 1}, (3, 4): {6: 1}}))
    for e in (1, ns):
        out[f'L6,19({e})'] = (6, _dg({(1, 2): {4: 1}, (1, 3): {5: 1}, (2, 4): {6: 1}, (3, 5): {6: e}}))
    out['L6,20'] = (6, _dg({(1, 2): {4: 1}, (1, 3): {5: 1}, (1, 5): {6: 1}, (2, 4): {6: 1}}))
    for e in (0, 1, ns):
        out[f'L6,21({e})'] = (6, _dg({(1, 2): {3: 1}, (1, 3): {4: 1}, (2, 3): {5: 1}, (1, 4): {6: 1}, (2, 5): {6: e}}))
    # recalled L6,23 fails Jacobi unless eps = 0; the eps != 0 entries below are a Jacobi-valid variant
    out['L6,23(0)'] = (6, _dg({(1, 2): {3: 1}, (1, 3): {5: 1}, (1, 4): {6: 1}, (2, 4): {5: 1}}))
    for e in (1, ns):
        out[f'V6,23({e})'] = (6, _dg({(1, 2): {3: 1}, (1, 3): {5: 1}, (1, 4): {6: 1}, (2, 4): {6: e}}))
    for e in (0, 1, ns):
        out[f'L6,24({e})'] = (6, _dg({(1, 2): {3: 1}, (1, 3): {5: 1}, (1, 4): {6: e}, (2, 3): {6: 1}, (2, 4): {5: 1}}))
    out['L6,25'] = (6, _dg({(1, 2): {3: 1}, (1, 3): {5: 1}, (1, 4): {6: 1}}))
    # decomposable 6-dim of class 3/4
    for k in ('L5,5', 'L5,6', 'L5,7', 'L5,9'):
        m, b = out[k]; out[k + '+1'] = (6, dict(b))
    out['L4,3+2'] = (6, _dg({(1, 2): {3: 1}, (1, 3): {4: 1}}))
    out['L4,3+L3,2'] = (7, _dg({(1, 2): {3: 1}, (1, 3): {4: 1}, (5, 6): {7: 1}}))
    return out
