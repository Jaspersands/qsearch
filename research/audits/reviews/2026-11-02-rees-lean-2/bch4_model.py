"""Exact model of the class-four BCH product in the truncated free associative algebra.

Used to design (not to prove) the Lean files `BCHClassFour.lean` and
`BCHClassFourSubgroups.lean`. Elements are dicts word -> Fraction, truncated at
length 4. Lie brackets are commutators, so identities found here hold in the
free class-four nilpotent Lie algebra over Q (and over Z[1/6], since every
coefficient below has 2,3-smooth denominator).
"""
from fractions import Fraction as Q
from itertools import product

DEG = 4


def add(*es):
    out = {}
    for e in es:
        for w, c in e.items():
            out[w] = out.get(w, 0) + c
    return {w: c for w, c in out.items() if c != 0}


def sc(a, e):
    return {w: a * c for w, c in e.items() if a * c != 0}


def mul(a, b):
    out = {}
    for u, cu in a.items():
        for v, cv in b.items():
            if len(u) + len(v) <= DEG:
                w = u + v
                out[w] = out.get(w, 0) + cu * cv
    return {w: c for w, c in out.items() if c != 0}


def br(a, b):
    return add(mul(a, b), sc(-1, mul(b, a)))


def gen(ch):
    return {(ch,): Q(1)}


def bch(a, b):
    """x + y + [x,y]/2 + ([x,[x,y]] + [y,[y,x]])/12 - [y,[x,[x,y]]]/24."""
    xy = br(a, b)
    return add(a, b, sc(Q(1, 2), xy),
               sc(Q(1, 12), add(br(a, xy), br(b, br(b, a)))),
               sc(Q(-1, 24), br(b, br(a, xy))))


def rn(word):
    """Right-normed bracket [w1,[w2,...,[w_{k-1},w_k]]] of letters."""
    e = gen(word[-1])
    for ch in reversed(word[:-1]):
        e = br(gen(ch), e)
    return e


def neg(a):
    return sc(-1, a)


def power(a, t):
    return sc(t, a)


def comm(a, b):
    return bch(bch(bch(a, b), neg(a)), neg(b))


def express(target, basis_words):
    """Solve target = sum c_w rn(w) exactly (Gaussian elimination)."""
    vecs = [rn(w) for w in basis_words]
    keys = sorted({k for v in vecs + [target] for k in v})
    n = len(vecs)
    rows = [[v.get(k, Q(0)) for v in vecs] + [target.get(k, Q(0))] for k in keys]
    piv = []
    r = 0
    for col in range(n):
        p = next((i for i in range(r, len(rows)) if rows[i][col] != 0), None)
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        rows[r] = [x / rows[r][col] for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][col] != 0:
                f = rows[i][col]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        piv.append(col)
        r += 1
    for i in range(r, len(rows)):
        assert rows[i][n] == 0, "target not in span"
    assert len(piv) == n, "basis words dependent"
    sol = {basis_words[c]: rows[i][n] for i, c in enumerate(piv)}
    return {w: c for w, c in sol.items() if c != 0}


x, y, z = gen('x'), gen('y'), gen('z')

# 1. Associativity in the free class-four nilpotent algebra on three generators.
assert bch(bch(x, y), z) == bch(x, bch(y, z)), "class-four BCH not associative"
print("associativity: ok")
# Additional group-law identities.
assert bch({}, x) == x and bch(x, {}) == x and bch(neg(x), x) == {} and bch(x, neg(x)) == {}
print("identity/inverse: ok")

# 2. Canonical (right-normed, sorted innermost pair) words and a basis.
letters = 'xyz'
canon = [w for k in range(2, DEG + 1) for w in product(letters, repeat=k) if w[-2] < w[-1]]
basis = []
for w in canon:
    trial = basis + [w]
    try:
        express(rn(w), basis) if basis else None
        in_span = bool(basis)
    except AssertionError:
        in_span = False
    if not in_span:
        basis.append(w)
print("canonical words:", len(canon), "basis size:", len(basis))

# The rewrite rules used in Lean, checked exactly.
rules = {
    # degree 3: [c,[a,b]] = [b,[a,c]] - [a,[b,c]]
    'jacobi3': (('z', 'x', 'y'), add(rn('yxz'), neg(rn('xyz')))),
}
for a, b, c in [('x', 'y', 'z'), ('y', 'x', 'z'), ('z', 'x', 'y')]:
    # [a,[a,[b,c]]] = [a,[b,[a,c]]] - [a,[c,[a,b]]]
    assert rn(a + a + b + c) == add(rn(a + b + a + c), neg(rn(a + c + a + b)))
    # [c,[a,[a,b]]] = [a,[b,[a,c]]] - [b,[a,[a,c]]] + [a,[c,[a,b]]]
    assert rn(c + a + a + b) == add(rn(a + b + a + c), neg(rn(b + a + a + c)), rn(a + c + a + b))
for a, b in [('x', 'y'), ('x', 'z'), ('y', 'z')]:
    assert rn(a + b + a + b) == rn(b + a + a + b)
assert rn('zxy') == add(rn('yxz'), neg(rn('xyz')))
print("rewrite rules: ok")

# 3. Two-generator words for the subgroup correspondence.
X = x
Y = y
c1 = comm(X, Y)
B2 = ['xy']
B3 = ['xxy', 'yxy']
B4 = ['xxxy', 'yxxy', 'yyxy']
print("log comm x y =", express(c1, [tuple(w) for w in B2 + B3 + B4]))
c2x = comm(X, c1)
c2y = comm(Y, c1)
print("log comm x (comm x y) =", express(c2x, [tuple(w) for w in B3 + B4]))
print("log comm y (comm x y) =", express(c2y, [tuple(w) for w in B3 + B4]))
c3xx = comm(X, comm(X, c1))
c3yx = comm(Y, comm(X, c1))
c3yy = comm(Y, comm(Y, c1))
for nm, e in [('c3xx', c3xx), ('c3yx', c3yx), ('c3yy', c3yy)]:
    print(nm, express(e, [tuple(w) for w in B4]))

# bracketWord = c1 * c2x^(-1/2) * c2y^(-1/2) * c3xx^a * c3yx^b * c3yy^c
partial = bch(bch(c1, power(c2x, Q(-1, 2))), power(c2y, Q(-1, 2)))
rest = add(partial, neg(rn('xy')))
r = express(rest, [tuple(w) for w in B4])
print("bracket remainder after degree-3 correction:", r)
coef = {'xxxy': -r.get(tuple('xxxy'), 0), 'yxxy': -r.get(tuple('yxxy'), 0),
        'yyxy': -r.get(tuple('yyxy'), 0)}
bw = bch(bch(bch(partial, power(c3xx, coef['xxxy'])), power(c3yx, coef['yxxy'])),
         power(c3yy, coef['yyxy']))
assert bw == rn('xy'), bw
print("bracketWord coefficients:", coef)

# addWord = x * y * bw^(-1/2) * c2x^a * c2y^b * c3xx^.. * c3yx^.. * c3yy^..
s0 = bch(bch(X, Y), power(bw, Q(-1, 2)))
r3 = express(add(s0, neg(X), neg(Y)), [tuple(w) for w in B3 + B4])
print("sum remainder after bracket correction:", r3)
a3 = -r3.get(tuple('xxy'), 0)
b3 = -r3.get(tuple('yxy'), 0)
s1 = bch(bch(s0, power(c2x, a3)), power(c2y, b3))
r4 = express(add(s1, neg(X), neg(Y)), [tuple(w) for w in B4])
print("degree-3 coefficients:", a3, b3, "remainder:", r4)
d = {k: -r4.get(tuple(k), 0) for k in B4}
s2 = bch(bch(bch(s1, power(c3xx, d['xxxy'])), power(c3yx, d['yxxy'])), power(c3yy, d['yyxy']))
assert s2 == add(X, Y), s2
print("addWord degree-4 coefficients:", d)
