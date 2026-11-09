"""Exact logarithms of the class-six subgroup words, in the two-letter Lean
normal form (a = x < b = y). Design aid for BCHClassSixSubgroups.lean."""
from fractions import Fraction as Q
import rules2 as R
import model6 as m

add, sc = R.addd, R.scd
def br(A, B): return R.br(A, B)
def neg(A): return sc(Q(-1), A)
def L(*ws): return {tuple(w): Q(1) for w in ws}
X, Y = L('x'), L('y')

def bch(A, B):
    return m.bch6(A, B, brf=br, addf=add, scf=sc, base=bch5)

def bch5(A, B):
    ab = br(A, B); ba = neg(ab)
    t = add(A, B, sc(Q(1, 2), ab), sc(Q(1, 12), add(br(A, ab), br(B, ba))),
            sc(Q(-1, 24), br(B, br(A, ab))))
    t5 = add(sc(Q(-1, 720), add(br(B, br(B, br(B, ba))), br(A, br(A, br(A, ab))))),
             sc(Q(1, 360), add(br(A, br(B, br(B, ba))), br(B, br(A, br(A, ab))))),
             sc(Q(1, 120), add(br(B, br(A, br(B, ab))), br(A, br(B, br(A, ba))))))
    return add(t, t5)

def comm(A, B):
    return bch(bch(bch(A, B), neg(A)), neg(B))

assert R.to_assoc(bch(X, Y)) == m.bch6(m.gen('x'), m.gen('y'))
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
        assert set(len(w) for w in A) == {6}
        SIX.append((l2 + nm, l2, 'c5' + nm, A))
DEGLIST = {3: ['c3x', 'c3y'], 4: ['c4xx', 'c4yx', 'c4yy'], 5: ['c5' + n for n, _, _ in FIVE]}

# degree-six commutators whose normal form is a single basis word
SIXUSE = [(n, l, inner, A) for n, l, inner, A in SIX if len(A) == 1 and list(A.values())[0] in (1, -1)]
for n, l, inner, A in SIX:
    C['c6' + n] = (l, inner, A)

def word_of(A):
    (w, c), = A.items(); return w, c

# bracketWord: c2 * prod powerScalar(t, comm word) over degrees 3..6
fac = [('c2', Q(1))]
cur = C['c2'][2]
for k in (3, 4, 5, 6):
    res = deg(cur, k)
    cands = [(n, C[n][2]) for n in DEGLIST[k]] if k < 6 else [('c6' + n, A) for n, _, _, A in SIXUSE]
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
    for nm, t, A in chosen:
        fac.append((nm, t)); cur = bch(cur, sc(t, A))
    assert not deg(cur, k)
assert cur == L('xy'), cur

# addWord: x * y * prod mk(t_w * w) over basis monomials of degree 2..6
mon = {k: [''.join(w) for w in R.BASIS[k]] for k in range(2, 7)}
cur = bch(X, Y); afac = []
for k in range(2, 7):
    res = deg(cur, k)
    assert set(res) <= {tuple(w) for w in mon[k]}, res
    for w in mon[k]:
        t = -res.get(tuple(w), 0)
        if t == 0:
            continue
        afac.append((w, t)); cur = bch(cur, sc(t, L(w)))
    assert not deg(cur, k), (k, cur)
assert cur == add(X, Y)

if __name__ == '__main__':
    def show(nm, A):
        print(nm, {''.join(k): str(v) for k, v in sorted(A.items(), key=lambda kv: (len(kv[0]), kv[0]))})
    for nm in ['c2', 'c3x', 'c3y', 'c4xx', 'c4yx', 'c4yy'] + ['c5' + n for n, _, _ in FIVE]:
        print(nm, len(C[nm][2]))
    for n, l, inner, A in SIX:
        show('c6' + n, A)
    print('bracketWord', [(n, str(t)) for n, t in fac])
    print('addWord', [(w, str(t)) for w, t in afac])
