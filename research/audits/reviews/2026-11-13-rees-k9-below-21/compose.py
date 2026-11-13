#!/opt/anaconda3/bin/python
"""Composition of chain steps into one l-level contraction (Lemma P of the report).  /opt/anaconda3/bin/python.

A step is (D, R, K, f) with f(s, y) -> F_p, s in Z_kappa (running kappa-class, only s mod D is read),
y a tuple of new coordinates in Z_kappa^n (n = 1 for a two-level step, 2 for a three-level step), and
cell condition  f(s, y) = 0  or  cl_D(f(s,y)) in K - s - |y|  (mod D), for s mod D in R.
The product B(x) = prod_t f_t(s_t, y_t), s_1 = x_1, s_{t+1} = s_t + |y_t| + cl_kappa(f_t(s_t, y_t)), is an
l-level lift_kappa(K_L)-contraction when every f_t is of the form F(y) + sum_r G_r(s, y without y_r) (checked
numerically by ell_common.verify on the full table; the algebraic proof is in the report).
usage: compose.py   (runs the positive and negative controls)
"""
import itertools, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ell_common as E


def two_level(D, R, K, alpha, beta):
    return (D, tuple(R), tuple(K), 1, lambda s, y: (alpha[y[0] % D] + beta[s % D]))


def three_level(D, R, K, F, G, H):
    """F[(i,j)], G[(s,j)], H[(s,i)]: f(s,(i,j)) = F(i,j) + G(s,j) + H(s,i)."""
    return (D, tuple(R), tuple(K), 2, lambda s, y: (F[(y[0], y[1])] + G[(s % D, y[1])] + H[(s % D, y[0])]))


def compose(p, k, steps):
    g = E.primitive_root(p)
    l = 1 + sum(st[3] for st in steps)
    B = {}
    for x in itertools.product(range(k), repeat=l):
        s, val, pos = x[0], 1, 1
        for (D, R, K, n, f) in steps:
            y = x[pos:pos + n]; pos += n
            assert s % D in {r % D for r in R}, ('running class outside R', x, s, D, R)
            v = f(s, y) % p
            if v == 0:
                val = 0
                break
            c = E.cls(v, p, g, k)
            assert (E.cls(v, p, g, D) + s + sum(y)) % D in {m % D for m in K}, ('step cell condition', x)
            val = val * v % p
            s = (s + sum(y) + c) % k
        B[x] = val
    return B, l


if __name__ == '__main__':
    out = []
    # positive control 1: p = 37, chain (1,{0}) -> (3,{0}) -> (9,{0,4}) -> 3-level {0,4}-contraction
    st = [two_level(3, (0, 1, 2), (0,), [1, 0, 12], {0: 0, 1: 2, 2: 1}),
          two_level(9, (0, 3, 6), (0, 4), [1, 0, 17, 10, 36, 34, 0, 10, 32], {0: 0, 3: 1, 6: 27})]
    B, l = compose(37, 9, st)
    out.append(('37 chain->{0,4} as 3-level', E.verify(B, 37, 9, (0, 4), l)))
    # same table checked against the wrong target {0,5} (negative control)
    out.append(('37 chain->{0,4} checked as {0,5} (must FAIL)', E.verify(B, 37, 9, (0, 5), l, sample=0)))
    # perturb one cell (negative control: span must fail)
    Bp = dict(B); Bp[(1, 2, 3)] = (Bp[(1, 2, 3)] + 1) % 37
    out.append(('37 table with one cell perturbed (must FAIL)', E.verify(Bp, 37, 9, (0, 4), l, sample=20)))
    # positive control 2: p = 127, the R8 chain (1,{0}) -> (3,{0}) -> (9,{0,3}) -> (9,{0}): a 4-level {0}-contraction
    st = [two_level(3, (0, 1, 2), (0,), [1, 18, 56], {0: 0, 1: 8, 2: 2}),
          two_level(9, (0, 3, 6), (0, 3), [1, 45, 71, 0, 39, 26, 0, 17, 3], {0: 0, 3: 0, 6: 4}),
          two_level(9, (0, 3), (0,), [1, 45, 71, 47, 105, 75, 0, 17, 3], {0: 0, 3: 4})]
    B, l = compose(127, 9, st)
    out.append(('127 chain->{0} as 4-level', E.verify(B, 127, 9, (0,), l, sample=30)))
    for name, (ok, info) in out:
        print(('OK   ' if ok else 'FAIL ') + name, info)
