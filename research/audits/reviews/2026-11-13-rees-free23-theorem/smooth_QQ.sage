# Cross-check of Lemma G (generic smoothness) in characteristic 0: one integer label configuration.
# (AI-written, pending human review.)  Prints dim of the cone of C and of its singular locus over QQ.
import time
labs = [[(1,0),(0,1),(1,2)], [(1,1),(2,-1),(1,3)], [(3,1),(1,-2),(2,5)], [(1,4),(5,1),(-3,2)], [(2,3),(-1,1),(4,1)], [(5,2),(1,-3),(2,7)]]
d = lambda x,y: x[0]*y[1]-x[1]*y[0]
A, B = [], []
for L in labs:
    assert d(L[0],L[1]) and d(L[1],L[2]) and d(L[0],L[2])
    s = [d(L[1],L[2]), d(L[2],L[0]), d(L[0],L[1])]
    A.append([sum(s[i]^3*L[i][r] for i in range(3)) for r in range(2)])
    B.append([sum(s[i]^2*L[i][r] for i in range(3)) for r in range(2)])
    assert [sum(s[i]*L[i][r] for i in range(3)) for r in range(2)] == [0,0]
R = PolynomialRing(QQ, 'u', 6, order='degrevlex'); u = R.gens()
eqs = [sum(A[j][r]*u[j]^3 for j in range(6)) for r in range(2)] + [sum(B[j][r]*u[j]^2 for j in range(6)) for r in range(2)]
I = R.ideal(eqs); t0 = time.time()
print('P3 columns', A); print('P2 columns', B)
print('dim cone', I.dimension(), 'Hilbert poly', I.hilbert_polynomial(), '[%.1fs]' % (time.time()-t0), flush=True)
J = matrix(R, [[e.derivative(x) for x in u] for e in eqs])
S = I + R.ideal(J.minors(4))
print('dim singular cone over QQ:', S.dimension(), '[%.1fs]' % (time.time()-t0), flush=True)
