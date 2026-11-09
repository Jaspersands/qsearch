"""Exact model of the class-five BCH product in the truncated free associative
algebra over Q (words of length <= 5). Design aid only; Lean rechecks all.
"""
from fractions import Fraction as Q
from itertools import product

DEG = 5

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

# exp/log check
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

if __name__ == '__main__':
    x, y, z = gen('x'), gen('y'), gen('z')
    assert logo(mul(expo(x), expo(y))) == bch5(x, y), 'bch5 formula'
    print('bch5 formula = log(exp x exp y) mod degree 6: ok')
    assert bch5(bch5(x, y), z) == bch5(x, bch5(y, z))
    print('associativity in free class-5 algebra: ok')
