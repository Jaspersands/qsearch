# Review checks for claims (a) and (d).
# (a) line restriction + stitching: for random lines a+tb, Q(a+tb) = Q_d(b)*M_b(t), M_b monic;
#     frequency of squarefree degree-d restrictions vs the bound 1 - d/p - d(d-1)/p;
#     frequency of IRREDUCIBLE restrictions (needed only by the irreducible-only readout);
#     reconstruct Q/Q(a) from monic restrictions M_b through a common point a (the learner is
#     simulated by exact factor-free data: this tests only the stitching algebra).
# (d) restriction-to-lines character-sum bound for squarefree S of degree D < p in n variables:
#     |sum_x chi(S(x))| <= (D-1) p^(n-1/2) + D(D-1) p^(n-1).
# Run: nice -n 19 /opt/anaconda3/envs/qsearch-cas/bin/sage review_line_stitch_check.sage
import itertools
set_random_seed(2026)

def rand_sqfree(R, d):
    while True:
        Q = R.random_element(degree=d, terms=Infinity)
        if Q.degree() == d and all(e == 1 for _, e in Q.factor()):
            return Q

def stitch(p, n, d, lines_extra=8):
    F = GF(p); R = PolynomialRing(F, n, 'x'); xs = R.gens(); T = PolynomialRing(F, 't'); t = T.gen()
    Q = rand_sqfree(R, d)
    Qd = sum(c * m for c, m in zip(Q.coefficients(), Q.monomials()) if m.degree() == d)
    sqf = irr = tot = 0
    for _ in range(400):
        a = [F.random_element() for _ in range(n)]; b = [F.random_element() for _ in range(n)]
        f = Q(*[a[i] + t * b[i] for i in range(n)])
        tot += 1
        if f.degree() == d and f.is_squarefree(): sqf += 1
        if f.degree() == d and f.is_irreducible(): irr += 1
    # stitching through a common point a with Q(a) != 0
    while True:
        a = [F.random_element() for _ in range(n)]
        if Q(*a) != 0: break
    from sage.all import binomial
    need = binomial(n + d - 1, d) + lines_extra
    data = []
    while len(data) < need:
        b = [F.random_element() for _ in range(n)]
        f = Q(*[a[i] + t * b[i] for i in range(n)])
        if f.degree() != d or not f.is_squarefree(): continue
        M = f / f.leading_coefficient()               # what the univariate learner returns (monic)
        assert f.leading_coefficient() == Qd(*b)      # leading coefficient is the top form at b
        data.append((b, T(M) / M(0)))                 # = Q(a+tb)/Q(a)
    # interpolate Qt(y) := Q(a+y)/Q(a) homogeneous part by part
    Rec = R(0)
    for k in range(d + 1):
        mons = [prod(x**e for x, e in zip(xs, ex)) for ex in itertools.product(range(k + 1), repeat=n) if sum(ex) == k]
        A = matrix(F, [[m(*b) for m in mons] for b, _ in data]); v = vector(F, [g[k] for _, g in data])
        c = A.solve_right(v); assert A * c == v
        Rec += sum(ci * m for ci, m in zip(c, mons))
    shift = Q(*[xs[i] + a[i] for i in range(n)]) / Q(*a)
    print("p=%d n=%d d=%d: squarefree-restriction rate %.3f (bound %.3f), irreducible rate %.3f (~1/d=%.3f); stitched Q/Q(a) correct: %s (lines=%d)"
          % (p, n, d, sqf / tot, 1 - d / p - d * (d - 1) / p, irr / tot, 1.0 / d, Rec == shift, len(data)))

def weil(p, n, D, trials=6):
    F = GF(p); R = PolynomialRing(F, n, 'x')
    chi = [0] + [1 if pow(z, (p - 1) // 2, p) == 1 else -1 for z in range(1, p)]
    pts = list(itertools.product(range(p), repeat=n))
    worst = 0.0
    for _ in range(trials):
        S = rand_sqfree(R, D)
        s = sum(chi[int(S(*x))] for x in pts)
        bound = (D - 1) * p**(n - 0.5) + D * (D - 1) * p**(n - 1)
        worst = max(worst, abs(s) / bound)
    print("Weil-by-lines p=%d n=%d D=%d: max |sum chi(S)| / bound over %d squarefree S = %.3f (<=1 required)" % (p, n, D, trials, worst))

for (p, n, d) in [(101, 2, 4), (101, 3, 5), (1009, 3, 6), (1009, 2, 10)]:
    stitch(p, n, d)
for (p, n, D) in [(31, 2, 2), (31, 2, 6), (61, 2, 8), (17, 3, 4)]:
    weil(p, n, D)
