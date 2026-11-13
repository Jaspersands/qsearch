# Dominance of the per-triple power-sum map psi: (l1,l2,l3) -> (P2, P3), P_k = sum_i s_i^k l_i,
# s = (det(l2,l3), det(l3,l1), det(l1,l2)).  (AI-written, pending human review.)
# Output: the content and a factorisation of one 4x4 Jacobian minor over ZZ.
R = PolynomialRing(ZZ, 'a1,a2,b1,b2,c1,c2'); a1,a2,b1,b2,c1,c2 = R.gens()
L = [vector(R,[a1,a2]), vector(R,[b1,b2]), vector(R,[c1,c2])]
det2 = lambda x,y: x[0]*y[1]-x[1]*y[0]
s = [det2(L[1],L[2]), det2(L[2],L[0]), det2(L[0],L[1])]
assert sum(s[i]*L[i] for i in range(3)) == 0
P1 = sum(s[i]*L[i] for i in range(3))
P2 = sum(s[i]^2*L[i] for i in range(3)); P3 = sum(s[i]^3*L[i] for i in range(3))
F = list(P2) + list(P3)
J = matrix(R, [[f.derivative(v) for v in R.gens()] for f in F])
print('P1 == 0:', P1 == 0)
print('degrees of P2, P3 components:', [f.degree() for f in F])
# normalise with GL2 / scaling: evaluate minors at the point l1=(1,0), l2=(0,1), l3=(c1,c2) generic
best = None
for cols in Subsets(range(6), 4):
    m = J.matrix_from_columns(list(cols)).det()
    if m != 0:
        cont = gcd(m.coefficients())
        if best is None or cont < best[1]: best = (cols, cont, m)
cols, cont, m = best
print('minor on columns', list(cols), ': nonzero, content', cont, ', total degree', m.degree())
print('factorisation:', factor(m))
# at the point l1=(1,0), l2=(0,1), l3=(1,1)  (s = (-1,-1,1))
pt = {a1:1,a2:0,b1:0,b2:1,c1:1,c2:1}
Jp = J.subs(pt); print('Jacobian at l1=(1,0),l2=(0,1),l3=(1,1): rank over QQ', Jp.change_ring(QQ).rank(),
      ', elementary divisors', Jp.change_ring(ZZ).elementary_divisors())
pt2 = {a1:1,a2:0,b1:0,b2:1,c1:1,c2:2}
Jp2 = J.subs(pt2); print('Jacobian at l3=(1,2): elementary divisors', Jp2.change_ring(ZZ).elementary_divisors())
pt3 = {a1:1,a2:0,b1:0,b2:1,c1:2,c2:3}
Jp3 = J.subs(pt3); print('Jacobian at l3=(2,3): elementary divisors', Jp3.change_ring(ZZ).elementary_divisors())
