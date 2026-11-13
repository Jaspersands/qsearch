"""Symbolic check of Lemma W, Claim 1's closed form (AI-written, pending human review).
Per copy, the (S)-tensor is t(a;b,c) = 3 A3(a) f(b) f(c) with A3 = -(n delta/6) h; its part outside Sym^3,
evaluated at (e; w, w), is (2/3)[t(e;w,w) - t(w;e,w)].  Claim: this equals  kappa * det(e, w) * (lam . w)  with a
universal constant kappa (independent of the chart x' and of lam), so the obstruction of a level-2 state is
kappa * det(e,w) * (sum_j u_j^3 P3(T_j)) . w."""
import sympy as sp
l0, l1, a, b, e0, e1, w0, w1 = sp.symbols('l0 l1 a b e0 e1 w0 w1')
n = l0 * a + l1 * b; g0 = (l1, -l0); delta = g0[0] * b - g0[1] * a
h = lambda v: (a * v[1] - b * v[0]) / (a * g0[1] - b * g0[0])
f = lambda v: (l0 * v[0] + l1 * v[1]) / n
A3 = lambda v: -(n * delta / 6) * h(v)
t = lambda A, B, C: 3 * A3(A) * f(B) * f(C)
e = (e0, e1); w = (w0, w1)
ns = sp.Rational(2, 3) * (t(e, w, w) - t(w, e, w))
kappa = sp.simplify(ns / ((e0 * w1 - e1 * w0) * (l0 * w0 + l1 * w1)))
print('non-symmetric part / (det(e,w) lam.w) =', kappa)
