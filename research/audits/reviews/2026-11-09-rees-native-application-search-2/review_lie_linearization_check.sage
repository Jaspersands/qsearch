# Review check for claim (a): "degree d < p: Stab_U(Q) = exp{X in u : X.Q = 0} (linear)".
# Compare, for unipotent affine g in U=UT_{n+1}(F_p) acting on F_p^n, the fixed space
# Fix(g) = {Q in V_d : Q(g x) = Q(x)} with ker D_X, X = log g (vector field), on V_d = polys of degree <= d.
# Weight argument: D_X^(nd+1) = 0 on V_d, so p > nd guarantees Fix(g) = ker D_X; d < p alone does not.
# Run: nice -n 19 /opt/anaconda3/envs/qsearch-cas/bin/sage review_lie_linearization_check.sage
import itertools, random
set_random_seed(11); random.seed(int(11))

def mons(n, d):
    return [e for e in itertools.product(range(d + 1), repeat=n) if sum(e) <= d]

def check(p, n, d, Mg, label):
    F = GF(p); R = PolynomialRing(F, n, 'x'); xs = R.gens()
    M = matrix(QQ, Mg)                      # (n+1)x(n+1) unipotent upper triangular, integer entries
    N = M - 1
    L = sum((-1)**(k+1) * N**k / k for k in range(1, n+1))   # log, denominators k <= n < p
    Lp = L.change_ring(F); Mp = M.change_ring(F)
    hom = vector(R, list(xs) + [R(1)])
    gx = Mp * hom                           # g acting on (x,1)
    Xv = Lp * hom                           # vector field components X_i(x)
    B = [prod(x**a for x, a in zip(xs, e)) for e in mons(n, d)]
    idx = {b: i for i, b in enumerate(B)}
    def vec(P):
        v = [F(0)] * len(B)
        for c, m in zip(P.coefficients(), P.monomials()):
            v[idx[m]] = c
        return vector(F, v)
    Ag = matrix(F, [vec(b(*gx[:n]) - b) for b in B]).transpose()
    AD = matrix(F, [vec(sum(Xv[i] * b.derivative(xs[i]) for i in range(n))) for b in B]).transpose()
    fix = Ag.right_kernel(); kD = AD.right_kernel()
    nil = next(k for k in range(1, 400) if (AD**k).is_zero())
    print("%s p=%d n=%d d=%d nd=%d: dim Fix(g)=%d dim ker D=%d kerD<=Fix:%s equal:%s nilindex(D)=%d"
          % (label, p, n, d, n*d, fix.dimension(), kD.dimension(), kD.is_subspace(fix), fix == kD, nil))
    if fix != kD:
        # exhibit Q in Fix(g) \ ker D and compare its true stabilizer in <g> with the Lie-algebra prediction
        for v in fix.basis():
            if v not in kD:
                Q = sum(c * b for c, b in zip(v, B))
                print("   witness Q =", Q, "  Q(gx)==Q:", Q(*gx[:n]) == Q, "  X.Q==0:",
                      sum(Xv[i] * Q.derivative(xs[i]) for i in range(n)) == 0)
                break

def reg(n):  # regular unipotent: ones on superdiagonal
    return [[1 if j == i else (1 if j == i+1 else 0) for j in range(n+1)] for i in range(n+1)]

for (p, n, d) in [(3, 2, 2), (5, 2, 3), (5, 2, 4), (5, 3, 3), (5, 3, 4), (7, 3, 3), (7, 3, 4), (7, 3, 6), (11, 3, 3), (11, 3, 4)]:
    check(p, n, d, reg(n), "regular")
