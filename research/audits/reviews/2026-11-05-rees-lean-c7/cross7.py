"""Coefficient cross-check for the degree-7 BCH law used in BCHClassSeven.lean.

Compared, degree by degree in the free associative algebra on x, y:
  (A) the Lean law: bch5 terms + Z6 + Z7 (model7.bch7), right-normed words;
  (B) log(exp x exp y) by truncated series (model7.logo/expo);
  (C) Dynkin's explicit formula (dynkin7.py; no exp/log series);
  (D) Varadarajan's recursion in Sage's free Lie algebra, Lyndon basis
      (sage_bch7.json, key 'varadarajan');
  (E) exact log(exp X exp Y) of random strictly upper triangular 8x8 matrices.
Sage's library bch_iterator ('library') is reported but disagrees from degree 6."""
import json, random
from fractions import Fraction as Q
import model7 as m
import dynkin7 as D

S = json.load(open('sage_bch7.json'))
x, y = m.gen('x'), m.gen('y')
A = m.bch7(x, y)
B = m.logo(m.mul(m.expo(x), m.expo(y)))
C = D.dynkin()
for n in range(1, 8):
    a = m.deg(A, n)
    var = {tuple(w): Q(c) for w, c in S['varadarajan'][str(n)].items()}
    lib = {tuple(w): Q(c) for w, c in S['library'][str(n)].items()}
    assert a == m.deg(B, n) == {w: c for w, c in C.items() if len(w) == n} == var, n
    print(f"degree {n}: Lean law = log(exp x exp y) = Dynkin = Sage Varadarajan ({len(a)} words);"
          f" Sage library bch_iterator {'agrees' if lib == a else 'DISAGREES'}")
random.seed(7)
for trial in range(3):
    X = [[Q(random.randint(-3, 3)) if j > i else Q(0) for j in range(8)] for i in range(8)]
    Y = [[Q(random.randint(-3, 3)) if j > i else Q(0) for j in range(8)] for i in range(8)]
    assert D.mlog(D.mmul(D.mexp(X), D.mexp(Y))) == D.evaluate(A, {'x': X, 'y': Y})
print('8x8 strictly upper triangular rational matrices (3 random pairs): log(exp X exp Y) = Lean law')
print('Z7 =', ' '.join(f"{'+' if c > 0 else '-'} {abs(c)} {''.join(w)}" for c, w in m.Z7))
dens = sorted({c.denominator for c, _ in m.Z7})
def primes(n):
    out, p = set(), 2
    while n > 1:
        while n % p == 0:
            out.add(p); n //= p
        p += 1
    return out
from math import lcm
allden = sorted({c.denominator for c in A.values()})
print('Z7 denominators', dens, 'lcm', lcm(*dens))
print('all denominators of the degree-<=7 law (associative form)', 'lcm', lcm(*allden),
      'primes', sorted(set().union(*map(primes, allden))))
