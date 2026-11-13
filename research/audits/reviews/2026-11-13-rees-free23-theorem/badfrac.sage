# Empirical fraction of label configurations whose weight curve C = {sum u_j^3 P3_j = 0, sum u_j^2 P2_j = 0}
# in P^5 is singular (or not a curve), using Lemma W (structure).  Also uniform (A,B) for comparison.
# (AI-written, pending human review.)  Finite evidence only.
import sys, time
set_random_seed(int(7))
def triple_cols(F):
    while True:
        L = [vector(F,[F.random_element(),F.random_element()]) for _ in range(3)]
        d = lambda x,y: x[0]*y[1]-x[1]*y[0]
        if d(L[0],L[1]) and d(L[1],L[2]) and d(L[0],L[2]): break
    s = [d(L[1],L[2]), d(L[2],L[0]), d(L[0],L[1])]
    return sum(s[i]^3*L[i] for i in range(3)), sum(s[i]^2*L[i] for i in range(3))
def smooth(F, A, B):
    R = PolynomialRing(F, 'u', 6); u = R.gens()
    eqs = [sum(A[j][r]*u[j]^3 for j in range(6)) for r in range(2)] + [sum(B[j][r]*u[j]^2 for j in range(6)) for r in range(2)]
    I = R.ideal(eqs)
    if I.dimension() != 2: return False
    J = matrix(R, [[e.derivative(x) for x in u] for e in eqs])
    return (I + R.ideal(J.minors(4))).dimension() == 0
mode = sys.argv[1]; N = int(sys.argv[2])
for p in [int(x) for x in sys.argv[3].split(',')]:
    F = GF(p); bad = 0; t0 = time.time()
    for _ in range(N):
        if mode == 'labels':
            cols = [triple_cols(F) for _ in range(6)]; A = [c[0] for c in cols]; B = [c[1] for c in cols]
        else:
            A = [vector(F,[F.random_element(),F.random_element()]) for _ in range(6)]
            B = [vector(F,[F.random_element(),F.random_element()]) for _ in range(6)]
        bad += int(not smooth(F, A, B))
    print('%s p=%d: singular or not a curve in %d/%d  (p*fraction = %.1f) [%.0fs]' % (mode, p, bad, N, p*bad/N, time.time()-t0), flush=True)
