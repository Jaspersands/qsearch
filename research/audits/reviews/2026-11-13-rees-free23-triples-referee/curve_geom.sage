# Geometry of the level-2 weight variety C = {K u^3 = 0, E u^2 = 0} in P^5 (AI-written, pending human review).
# For each config: affine dimension and degree of the cone, singular locus (Jacobian 4-minors), and the (c)-solver:
# random hyperplane section u6 = t*u1, u1 = 1, zero-dimensional solve, F_p-points with all u_j != 0.
import json, sys, time
p = int(sys.argv[1]); nfib = int(sys.argv[2])
D = json.load(open('curve_%d.json' % p))
F = GF(p); R = PolynomialRing(F, 'u', 6); u = R.gens()
set_random_seed(int(1))
for ci, c in enumerate(D['configs']):
    K = c['K']; E = c['E']
    eqs = [sum(F(K[r][j]) * u[j]**3 for j in range(6)) for r in range(len(K))] + \
          [sum(F(E[r][j]) * u[j]**2 for j in range(6)) for r in range(len(E))]
    I = R.ideal(eqs); t0 = time.time()
    dimI = I.dimension(); degI = I.hilbert_polynomial() if dimI > 0 else None
    J = matrix(R, [[e.derivative(x) for x in u] for e in eqs])
    Sing = I + R.ideal(J.minors(4))
    dimS = Sing.dimension()
    t1 = time.time()
    # (c) solver: fibres u1 = 1, u6 = t
    S2 = PolynomialRing(F, 'v', 4); v = S2.gens()
    good = 0; npts = 0
    for k in range(nfib):
        t = F.random_element()
        while t == 0: t = F.random_element()
        sub = [1] + list(v) + [t]
        Ifib = S2.ideal([e(*sub) for e in eqs])
        if Ifib.dimension() != 0: continue
        pts = [P for P in Ifib.variety() if all(P[x] != 0 for x in v)]
        npts += len(pts); good += int(len(pts) > 0)
    t2 = time.time()
    print('p=%d config %d: dim(cone)=%d (projective %d), Hilbert poly %s, dim(singular locus cone)=%d [%.1fs]; '
          'fibres with a torus point: %d/%d, mean points/fibre %.2f [%.1fs]' %
          (p, ci, dimI, dimI - 1, degI, dimS, t1 - t0, good, nfib, npts / nfib, t2 - t1), flush=True)
