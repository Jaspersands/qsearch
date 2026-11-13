"""Symbolic check (over Q(l0,l1,a,b,e0,e1,e3,cU,cW,j,k,x)) of the closed form in Lemma 0 of the target
(AI-written, pending human review).  Structure (proved in the referee report, sec. 2): the coset element with
chart coordinate x is n_g * exp(nu(x)) * exp(x x'), nu(x) = log(exp(x eta') exp(-x x')), eta' = eta/f(e), so the
N_lam-QFT outcome y = (j, k, l) leaves phase -[j nu_g0 + k nu_z + l lam(nu_gamma3)] (+ global), and the label
twist puts all weight in one l-sector (l = -1 in the target's convention).  Here: the identity
   f(e) * ( -j nu_g0(x) - k nu_z(x) + lam(nu_gamma3(x)) ) = A1 x + A2 x^2 + A3 x^3
with A3 = -(n delta/6) h(e), A2 = (k delta/2) h(e) + (n/2) e3, A1 = -j h(e) - k e3 + lam(eta_c)
is checked as a rational-function identity (class-3 BCH is exact)."""
import sympy as sp
l0, l1, a, b, e0, e1, e3, cU, cW, j, k, x = sp.symbols('l0 l1 a b e0 e1 e3 cU cW j k x')

def br(u, v):   # free23 coordinates (X0, X1, Z, U, W)
    return [0, 0, u[0] * v[1] - u[1] * v[0], u[0] * v[2] - u[2] * v[0], u[1] * v[2] - u[2] * v[1]]
def add(*vs): return [sp.expand(sum(c)) for c in zip(*vs)]
def sc(s, v): return [s * c for c in v]
def bch(A, B):
    AB = br(A, B)
    return add(A, B, sc(sp.Rational(1, 2), AB), sc(sp.Rational(1, 12), br(A, AB)), sc(sp.Rational(-1, 12), br(B, AB)))

n = l0 * a + l1 * b                       # lam.x', x' = (a, b)
g0 = (l1, -l0)
delta = g0[0] * b - g0[1] * a             # det(g0, x')
fe = (l0 * e0 + l1 * e1) / n
h = (a * e1 - b * e0) / (a * g0[1] - b * g0[0])   # det(x', e) / det(x', g0)
eta = [e0, e1, e3, cU, cW]
etap = [c / fe for c in eta]
nu = bch(sc(x, etap), [-x * a, -x * b, 0, 0, 0])
# V-part of nu lies on F g0: coefficient
nu_g0 = sp.simplify(nu[0] / g0[0])
assert sp.simplify(nu[1] - nu_g0 * g0[1]) == 0
lam_g3 = l0 * nu[3] + l1 * nu[4]
P = -j * nu_g0 - k * nu[2] + lam_g3
lhs = sp.simplify(sp.expand(fe * P))
A3 = -(n * delta / 6) * h
A2 = (k * delta / 2) * h + (n / 2) * e3
A1 = -j * h - k * e3 + (l0 * cU + l1 * cW)
diff = sp.simplify(lhs - (A1 * x + A2 * x ** 2 + A3 * x ** 3))
print('f(e) P(x) - (A1 x + A2 x^2 + A3 x^3) =', diff)
print('delta - n =', sp.simplify(delta - n))
