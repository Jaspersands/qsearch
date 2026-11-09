"""Exact logarithms of the class-five subgroup words, in the Lean normal form
(two letters a = x, b = y). Design aid for BCHClassFiveSubgroups.lean."""
from fractions import Fraction as Q
import rules5 as R
import model5 as m

add, sc = R.addd, R.scd
def br(A, B): return R.br(A, B)
def neg(A): return sc(Q(-1), A)
def L(*ws): return {tuple(w): Q(1) for w in ws}
X, Y = L('x'), L('y')

def bch(A, B):
    ab = br(A, B); ba = neg(ab)
    t = add(A, B, sc(Q(1, 2), ab), sc(Q(1, 12), add(br(A, ab), br(B, ba))),
            sc(Q(-1, 24), br(B, br(A, ab))))
    t5 = add(sc(Q(-1, 720), add(br(B, br(B, br(B, ba))), br(A, br(A, br(A, ab))))),
             sc(Q(1, 360), add(br(A, br(B, br(B, ba))), br(B, br(A, br(A, ab))))),
             sc(Q(1, 120), add(br(B, br(A, br(B, ab))), br(A, br(B, br(A, ba))))))
    return add(t, t5)

def comm(A, B):
    return bch(bch(bch(A, B), neg(A)), neg(B))

def check(A):  # NF element -> assoc model, against the true value
    return R.to_assoc(A)

# sanity: NF bch agrees with the associative model
assert check(bch(X, Y)) == m.bch5(m.gen('x'), m.gen('y'))
c2 = comm(X, Y)
c3x, c3y = comm(X, c2), comm(Y, c2)
c4xx, c4yx, c4yy = comm(X, c3x), comm(Y, c3x), comm(Y, c3y)
c5 = {'xxx': comm(X, c4xx), 'yxx': comm(Y, c4xx), 'xyx': comm(X, c4yx),
      'yyx': comm(Y, c4yx), 'xyy': comm(X, c4yy), 'yyy': comm(Y, c4yy)}
def show(nm, A):
    print(nm, {''.join(k): str(v) for k, v in sorted(A.items(), key=lambda kv: (len(kv[0]), kv[0]))})
for nm, A in [('c2', c2), ('c3x', c3x), ('c3y', c3y), ('c4xx', c4xx), ('c4yx', c4yx), ('c4yy', c4yy)] + list(c5.items()):
    show(nm, A)

def deg(A, k): return {w: c for w, c in A.items() if len(w) == k}
# bracketWord: c2 * c3x^a * c3y^b * c4..^.. * c5..^..
fac = [('c2', Q(1), c2)]
cur = c2
for k, cands in [(3, [('c3x', c3x), ('c3y', c3y)]),
                 (4, [('c4xx', c4xx), ('c4yx', c4yx), ('c4yy', c4yy)]),
                 (5, [(n, A) for n, A in c5.items()])]:
    res = deg(cur, k)
    for nm, A in cands:
        lead = deg(A, k)
        assert len(lead) == 1, (nm, lead)
        (w, c), = lead.items()
        t = -res.get(w, 0) / c
        fac.append((nm, t, A))
        res = add(res, sc(t, lead))
    assert not res, res
    for nm, t, A in fac[-len(cands):]:
        cur = bch(cur, sc(t, A))
    assert not deg(cur, k)
assert cur == L('xy'), cur
print('bracketWord', [(n, str(t)) for n, t, _ in fac])

# addWord: x * y * prod mk(t_w * w) over monomials w of degree 2..5
mon = {2: ['xy'], 3: ['xxy', 'yxy'], 4: ['xxxy', 'yxxy', 'yyxy'],
       5: ['xxxxy', 'yxxxy', 'xyxxy', 'yyxxy', 'xyyxy', 'yyyxy']}
cur = bch(X, Y); afac = []
for k in range(2, 6):
    res = deg(cur, k)
    assert set(res) <= {tuple(w) for w in mon[k]}, res
    for w in mon[k]:
        t = -res.get(tuple(w), 0)
        afac.append((w, t))
        cur = bch(cur, sc(t, L(w)))
    assert not deg(cur, k), (k, cur)
assert cur == add(X, Y)
print('addWord', [(w, str(t)) for w, t in afac])
