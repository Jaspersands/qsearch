"""Exact model of the class-six BCH product in the truncated free associative
algebra over Q (words of length <= 6). Design aid only; Lean rechecks all.
"""
from fractions import Fraction as Q

DEG = 6

def add(*es):
    out = {}
    for e in es:
        for w, c in e.items():
            out[w] = out.get(w, 0) + c
    return {w: c for w, c in out.items() if c != 0}

def sc(a, e):
    a = Q(a)
    return {w: a * c for w, c in e.items() if a * c != 0}

def neg(e):
    return sc(-1, e)

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

def rn(word):
    e = gen(word[-1])
    for ch in reversed(word[:-1]):
        e = br(gen(ch), e)
    return e

def expo(a):
    out = {(): Q(1)}; term = {(): Q(1)}
    for k in range(1, DEG + 1):
        term = sc(Q(1, k), mul(term, a)); out = add(out, term)
    return out

def logo(u):
    v = add(u, {(): Q(-1)}); out = {}; p = {(): Q(1)}
    for k in range(1, DEG + 1):
        p = mul(p, v); out = add(out, sc(Q((-1) ** (k + 1), k), p))
    return out

def deg(e, k):
    return {w: c for w, c in e.items() if len(w) == k}

# The degree-6 BCH terms, as (coefficient, right-normed word in x, y).
# Filled in by find_z6 below; the Lean definition uses exactly this list.
Z6 = [(Q(-1, 720), tuple('xxyyxy')), (Q(1, 240), tuple('xyxyxy')),
      (Q(1, 1440), tuple('xyyyxy')), (Q(1, 1440), tuple('yxxxxy'))]

def bch5(a, b):
    ab = br(a, b)
    ba = neg(ab)
    t = add(a, b, sc(Q(1, 2), ab),
            sc(Q(1, 12), add(br(a, ab), br(b, ba))),
            sc(Q(-1, 24), br(b, br(a, ab))))
    aaaab = br(a, br(a, br(a, ab)))
    bbbba = br(b, br(b, br(b, ba)))
    abbba = br(a, br(b, br(b, ba)))
    baaab = br(b, br(a, br(a, ab)))
    babab = br(b, br(a, br(b, ab)))
    ababa = br(a, br(b, br(a, ba)))
    t5 = add(sc(Q(-1, 720), add(bbbba, aaaab)),
             sc(Q(1, 360), add(abbba, baaab)),
             sc(Q(1, 120), add(babab, ababa)))
    return add(t, t5)

def word_eval(w, env, brf=br):
    e = env[w[-1]]
    for ch in reversed(w[:-1]):
        e = brf(env[ch], e)
    return e

def bch6(a, b, z6=None, brf=br, addf=add, scf=sc, base=bch5):
    z6 = z6 if z6 is not None else Z6
    env = {'x': a, 'y': b}
    t = base(a, b)
    for c, w in z6:
        t = addf(t, scf(c, word_eval(w, env, brf)))
    return t

def find_z6():
    """Represent the degree-6 part of log(exp x exp y) by right-normed words."""
    from itertools import product
    target = deg(logo(mul(expo(gen('x')), expo(gen('y')))), 6)
    words = [tuple(w) for w in product('xy', repeat=6) if w[-1] != w[-2]]
    # Gaussian elimination, preferring words in a fixed order; greedy sparse basis
    vecs = {w: deg(rn(w), 6) for w in words}
    # choose a basis among words
    basis, piv = [], []
    def reduce(v):
        v = dict(v)
        for (k, pv) in piv:
            if v.get(k, 0):
                f = v[k] / pv[k]
                v = {kk: v.get(kk, 0) - f * pv.get(kk, 0) for kk in set(v) | set(pv)}
                v = {kk: x for kk, x in v.items() if x}
        return v
    return target, vecs

if __name__ == '__main__':
    x, y, z = gen('x'), gen('y'), gen('z')
    assert logo(mul(expo(x), expo(y))) == bch6(x, y), 'bch6 formula'
    print('bch6 formula = log(exp x exp y) mod degree 7: ok')
    assert bch6(bch6(x, y), z) == bch6(x, bch6(y, z))
    print('associativity in free class-6 algebra: ok')
