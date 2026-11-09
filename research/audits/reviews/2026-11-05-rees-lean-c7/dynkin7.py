"""Independent degree-<=7 BCH coefficients by Dynkin's explicit formula
    Z = sum_n (-1)^(n-1)/n sum_{r_i+s_i>0} [x^r1 y^s1 ... x^rn y^sn]
          / ((sum r_i + s_i) prod r_i! s_i!),
where [w] is the right-nested bracket of the word w, expanded in the free
associative algebra. It does not use exp, log or the series product of
model7.py. A second check evaluates both laws on random strictly upper
triangular 8x8 rational matrices, where log(exp X exp Y) is computed with
matrix exponentials and logarithms (products of 8 such matrices vanish, so the
degree-7 truncation is exact)."""
from fractions import Fraction as Q
from itertools import product
from math import factorial
import random

N = 7

def addto(d, w, c):
    v = d.get(w, 0) + c
    if v:
        d[w] = v
    else:
        d.pop(w, None)

def rnest(word):
    """Right-nested bracket [w1,[w2,...[w_{k-1},w_k]]] in the free associative algebra."""
    e = {(word[-1],): Q(1)}
    for ch in reversed(word[:-1]):
        out = {}
        for w, c in e.items():
            addto(out, (ch,) + w, c)
            addto(out, w + (ch,), -c)
        e = out
    return e

def dynkin():
    Z = {}
    pairs = [(r, s) for r in range(N + 1) for s in range(N + 1) if 0 < r + s <= N]
    def rec(n, total, blocks):
        if blocks:
            k = len(blocks)
            word = tuple(ch for r, s in blocks for ch in 'x' * r + 'y' * s)
            den = total
            for r, s in blocks:
                den *= factorial(r) * factorial(s)
            coef = Q((-1) ** (k - 1), k) / den
            for w, c in rnest(word).items():
                addto(Z, w, coef * c)
        for r, s in pairs:
            if total + r + s <= N:
                rec(n, total + r + s, blocks + [(r, s)])
    rec(0, 0, [])
    return Z

# --- exact matrix check ---
def mzero(n): return [[Q(0)] * n for _ in range(n)]
def mid(n): return [[Q(int(i == j)) for j in range(n)] for i in range(n)]
def madd(A, B, c=1): return [[a + c * b for a, b in zip(ra, rb)] for ra, rb in zip(A, B)]
def mmul(A, B):
    n = len(A)
    return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
def msc(c, A): return [[c * a for a in r] for r in A]
def mexp(A):
    n = len(A); out = mid(n); term = mid(n)
    for k in range(1, n + 1):
        term = msc(Q(1, k), mmul(term, A)); out = madd(out, term)
    return out
def mlog(U):
    n = len(U); V = madd(U, mid(n), -1); out = mzero(n); p = mid(n)
    for k in range(1, n + 1):
        p = mmul(p, V); out = madd(out, p, Q((-1) ** (k + 1), k))
    return out
def evaluate(poly, env):
    n = len(env['x']); out = mzero(n)
    for w, c in poly.items():
        P = mid(n)
        for ch in w:
            P = mmul(P, env[ch])
        out = madd(out, P, c)
    return out

if __name__ == '__main__':
    import model7 as m
    Z = dynkin()
    x, y = m.gen('x'), m.gen('y')
    law = m.bch7(x, y)
    for n in range(1, N + 1):
        assert {w: c for w, c in Z.items() if len(w) == n} == m.deg(law, n), n
        print(f'degree {n}: Dynkin formula = Lean law ({sum(1 for w in Z if len(w) == n)} words)')
    random.seed(7)
    for trial in range(3):
        X = [[Q(random.randint(-3, 3)) if j > i else Q(0) for j in range(8)] for i in range(8)]
        Y = [[Q(random.randint(-3, 3)) if j > i else Q(0) for j in range(8)] for i in range(8)]
        lhs = mlog(mmul(mexp(X), mexp(Y)))
        assert lhs == evaluate(law, {'x': X, 'y': Y})
        assert lhs == evaluate(Z, {'x': X, 'y': Y})
    print('8x8 strictly upper triangular matrices: log(exp X exp Y) = Lean law = Dynkin, 3 random pairs')
