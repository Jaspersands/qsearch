"""Degree-<=7 BCH coefficients in Sage's free Lie algebra (Lyndon basis), lifted to
the free associative algebra. Run with
    /opt/anaconda3/envs/qsearch-cas/bin/python sage_bch7.py > sage_bch7.json

Two computations are recorded:
* 'library': Sage 10.9's own sage.algebras.lie_algebras.bch.bch_iterator. Its
  Bernoulli cache test reads `if p <= len(norm_ber): norm_ber.append(...)`, so
  from degree 6 on it uses B_2/2! where B_4/4! is meant; its degree-6 part has
  the coefficient -61/8640 on [x,[x,[x,[x,[x,y]]]]], which the y-linear part
  ad_x/(1 - e^{-ad_x}) y of BCH forbids (B_5 = 0). Recorded, not used.
* 'varadarajan': the same recursion of Varadarajan (1984) written out here with
  the Bernoulli numbers indexed correctly, using Sage's Lie bracket.
"""
import json
from sage.all import QQ, LieAlgebra, bernoulli, factorial, IntegerListsLex
from sage.algebras.lie_algebras.bch import bch_iterator

L = LieAlgebra(QQ, 'x,y').Lyndon()
X, Y = L.gens()

def varadarajan(X, Y, top):
    xdif = X - Y
    Z = [0, X + Y]
    yield Z[1]
    for m in range(2, top + 1):
        Zm = ~QQ(2 * m) * xdif.bracket(Z[-1])
        for p in range(1, (m - 1) // 2 + 1):
            coeff = bernoulli(2 * p) / QQ(factorial(2 * p)) / QQ(m)
            temp = L.zero()
            for kvec in IntegerListsLex(m - 1, length=2 * p, min_part=1):
                W = Z[1]
                for k in kvec:
                    W = Z[k].bracket(W)
                temp += W
            Zm += coeff * temp
        Z.append(Zm)
        yield Zm

def assoc(Z):
    d = {}
    for mono, c in Z.lift().monomial_coefficients().items():
        d[''.join(str(g) * int(e) for g, e in mono)] = str(c)
    return d

out = {'sage_version': __import__('sage.version').version.version}
for name, it in (('library', bch_iterator(X, Y)), ('varadarajan', varadarajan(X, Y, 7))):
    res = {}
    for n, Z in enumerate(it, start=1):
        if n > 7:
            break
        res[n] = assoc(Z)
    out[name] = res
print(json.dumps(out, indent=1, sort_keys=True))
