"""Exact logarithms of the class-seven subgroup words, in the two-letter Lean
normal form (a = x < b = y). Design aid for BCHClassSevenSubgroups.lean."""
from fractions import Fraction as Q
import rules2_7 as R
import model7 as m

add, sc = R.addd, R.scd
def br(A, B): return R.br(A, B)
def neg(A): return sc(Q(-1), A)
def L(*ws): return {tuple(w): Q(1) for w in ws}
X, Y = L('x'), L('y')

def bch5(A, B):
    ab = br(A, B); ba = neg(ab)
    t = add(A, B, sc(Q(1, 2), ab), sc(Q(1, 12), add(br(A, ab), br(B, ba))),
            sc(Q(-1, 24), br(B, br(A, ab))))
    t5 = add(sc(Q(-1, 720), add(br(B, br(B, br(B, ba))), br(A, br(A, br(A, ab))))),
             sc(Q(1, 360), add(br(A, br(B, br(B, ba))), br(B, br(A, br(A, ab))))),
             sc(Q(1, 120), add(br(B, br(A, br(B, ab))), br(A, br(B, br(A, ba))))))
    return add(t, t5)

def bch6(A, B):
    return m.bch6(A, B, brf=br, addf=add, scf=sc, base=bch5)

def bch(A, B):
    return m.bch7(A, B, brf=br, addf=add, scf=sc, base=bch6)

def comm(A, B):
    return bch(bch(bch(A, B), neg(A)), neg(B))

assert R.to_assoc(bch(X, Y)) == m.bch7(m.gen('x'), m.gen('y'))
def deg(A, k): return {w: c for w, c in A.items() if len(w) == k}

# iterated commutators: name -> (letter, inner name, polynomial)
C = {'c2': (None, None, comm(X, Y))}
C['c3x'] = ('x', 'c2', comm(X, C['c2'][2])); C['c3y'] = ('y', 'c2', comm(Y, C['c2'][2]))
C['c4xx'] = ('x', 'c3x', comm(X, C['c3x'][2])); C['c4yx'] = ('y', 'c3x', comm(Y, C['c3x'][2]))
C['c4yy'] = ('y', 'c3y', comm(Y, C['c3y'][2]))
FIVE = [('xxx', 'x', 'c4xx'), ('yxx', 'y', 'c4xx'), ('xyx', 'x', 'c4yx'), ('yyx', 'y', 'c4yx'),
        ('xyy', 'x', 'c4yy'), ('yyy', 'y', 'c4yy')]
for nm, l, inner in FIVE:
    C['c5' + nm] = (l, inner, comm(X if l == 'x' else Y, C[inner][2]))
SIX = []
for nm, l, inner in FIVE:
    for l2 in 'xy':
        A = comm(X if l2 == 'x' else Y, C['c5' + nm][2])
        assert min(len(w) for w in A) == 6 and max(len(w) for w in A) <= 7
        SIX.append((l2 + nm, l2, 'c5' + nm, A))
        C['c6' + l2 + nm] = (l2, 'c5' + nm, A)
DEGLIST = {3: ['c3x', 'c3y'], 4: ['c4xx', 'c4yx', 'c4yy'], 5: ['c5' + n for n, _, _ in FIVE]}

# degree-six commutators whose leading part is a single basis word (as in class six)
SIXUSE = [(n, l, inner, A) for n, l, inner, A in SIX
          if len(deg(A, 6)) == 1 and list(deg(A, 6).values())[0] in (1, -1)]

def solve_exact(cands, res):
    """Pick independent candidates (in order) and solve res + sum t_i lead_i = 0."""
    keys = sorted(set(res) | set().union(*[set(A) for _, A in cands]))
    chosen, piv = [], []
    def red(v):
        v = dict(v)
        for k, pv in piv:
            if v.get(k, 0):
                f = v[k] / pv[k]
                v = {kk: v.get(kk, 0) - f * pv.get(kk, 0) for kk in set(v) | set(pv)}
                v = {kk: c for kk, c in v.items() if c}
        return v
    for nm, A in cands:
        r = red(A)
        if r:
            piv.append((min(r), r)); chosen.append((nm, A))
    import sympy as sp
    M = sp.Matrix([[sp.Rational(A.get(k, 0).numerator, A.get(k, 0).denominator) if A.get(k, 0) else 0
                    for _, A in chosen] for k in keys])
    b = sp.Matrix([-sp.Rational(res.get(k, 0).numerator, res.get(k, 0).denominator) if res.get(k, 0) else 0
                   for k in keys])
    sol, params = M.gauss_jordan_solve(b)
    assert params.shape[0] == 0
    return [(nm, Q(int(sp.fraction(s)[0]), int(sp.fraction(s)[1])), A) for (nm, A), s in zip(chosen, sol)]

# degree-seven (central) commutators of the used degree-six ones
fac = [('c2', Q(1))]
cur = C['c2'][2]
USED6 = []
for k in (3, 4, 5, 6, 7):
    res = deg(cur, k)
    if k < 6:
        cands = [(n, C[n][2]) for n in DEGLIST[k]]
    elif k == 6:
        cands = [('c6' + n, A) for n, _, _, A in SIXUSE]
    else:
        cands = []
        for n6 in USED6:
            for l3 in 'xy':
                A = comm(X if l3 == 'x' else Y, C[n6][2])
                assert set(len(w) for w in A) <= {7}
                if A:
                    C['c7' + l3 + n6[2:]] = (l3, n6, A)
                    cands.append(('c7' + l3 + n6[2:], A))
    if k < 7:
        chosen = []
        for nm, A in cands:
            lead = deg(A, k)
            assert len(lead) == 1, (nm, lead)
            (w, c), = lead.items()
            t = -res.get(w, 0) / c
            if k == 6 and t == 0:
                continue
            chosen.append((nm, t, A)); res = add(res, sc(t, lead))
        assert not res, (k, res)
    else:
        chosen = [(nm, t, A) for nm, t, A in solve_exact(cands, res) if t != 0]
    for nm, t, A in chosen:
        fac.append((nm, t)); cur = bch(cur, sc(t, A))
        if k == 6:
            USED6.append(nm)
    assert not deg(cur, k), (k, deg(cur, k))
assert cur == L('xy'), cur
USED7 = [n for n, _ in fac if n.startswith('c7')]

# addWord: x * y * prod mk(t_w * w) over basis monomials of degree 2..7
mon = {k: [''.join(w) for w in R.BASIS[k]] for k in range(2, 8)}
cur = bch(X, Y); afac = []
for k in range(2, 8):
    res = deg(cur, k)
    assert set(res) <= {tuple(w) for w in mon[k]}, res
    for w in mon[k]:
        t = -res.get(tuple(w), 0)
        if t == 0:
            continue
        afac.append((w, t)); cur = bch(cur, sc(t, L(w)))
    assert not deg(cur, k), (k, cur)
assert cur == add(X, Y)

# the staged values used by the Lean proofs: value after each factor
def stages(start, factors):
    out, cur = [], start
    for A in factors:
        cur = bch(cur, A); out.append(cur)
    return out
BW_STAGES = stages(C['c2'][2], [sc(t, C[n][2]) for n, t in fac[1:]])
AW_STAGES = stages(bch(X, Y), [sc(t, L(w)) for w, t in afac])
assert BW_STAGES[-1] == L('xy') and AW_STAGES[-1] == add(X, Y)

if __name__ == '__main__':
    def show(nm, A):
        print(nm, {''.join(k): str(v) for k, v in sorted(A.items(), key=lambda kv: (len(kv[0]), kv[0]))})
    for nm in ['c2', 'c3x', 'c3y', 'c4xx', 'c4yx', 'c4yy'] + ['c5' + n for n, _, _ in FIVE]:
        print(nm, len(C[nm][2]))
    for n, l, inner, A in SIX:
        print('c6' + n, len(A), 'lead', {''.join(k): str(v) for k, v in deg(A, 6).items()})
    for n in USED7:
        show(n, C[n][2])
    print('bracketWord', len(fac), [(n, str(t)) for n, t in fac])
    print('addWord', len(afac), [(w, str(t)) for w, t in afac])
    print('stage sizes bw', [len(s) for s in BW_STAGES])
    print('stage sizes aw', [len(s) for s in AW_STAGES])
