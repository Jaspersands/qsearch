"""Exact model of the class-seven BCH product in the truncated free associative
algebra over Q (words of length <= 7). Design aid only; Lean rechecks all.
"""
from fractions import Fraction as Q

DEG = 7

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
# As in class six (model6.py); the Lean definition uses exactly this list.
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

# The degree-7 BCH terms, as (coefficient, right-normed word in x, y): an exact
# basis solution (find_z7.py found no form with at most 8 words); the Lean
# definition uses exactly this list, cross-checked by cross7.py.
Z7 = [(Q(c), tuple(w)) for c, w in [('1/30240', 'xxxxxxy'), ('1/10080', 'xxxxyxy'), ('-1/30240', 'xxxyyxy'), ('1/10080', 'xxyyyxy'), ('1/5040', 'xyxxxxy'), ('1/1120', 'xyxxyxy'), ('-1/10080', 'xyyxxxy'), ('1/2520', 'xyyxyxy'), ('1/10080', 'xyyyyxy'), ('-1/10080', 'yxxxxxy'), ('-1/2520', 'yxxxyxy'), ('1/10080', 'yxxyyxy'), ('-1/1120', 'yxyxyxy'), ('-1/5040', 'yxyyyxy'), ('-1/10080', 'yyxxxxy'), ('1/30240', 'yyyxxxy'), ('-1/10080', 'yyyxyxy'), ('-1/30240', 'yyyyyxy')]]

def bch7(a, b, z7=None, brf=br, addf=add, scf=sc, base=None):
    z7 = z7 if z7 is not None else Z7
    env = {'x': a, 'y': b}
    t = (base or (lambda u, v: bch6(u, v, brf=brf, addf=addf, scf=scf)))(a, b)
    for c, w in z7:
        t = addf(t, scf(c, word_eval(w, env, brf)))
    return t

if __name__ == '__main__':
    x, y, z = gen('x'), gen('y'), gen('z')
    assert logo(mul(expo(x), expo(y))) == bch7(x, y), 'bch7 formula'
    print('bch7 formula = log(exp x exp y) mod degree 8: ok')
    assert bch7(bch7(x, y), z) == bch7(x, bch7(y, z))
    print('associativity in free class-7 algebra: ok')
