"""s2b, finding 1: on the failure event of Lemma tb-kernel, the chart of Lemma tb-chart
(route (R2), used by Theorem bb-envelope) can be a Lie ring that is not nilpotent, so a call
of Theorem main on it is outside Definition input-contract.

Setting: c = 2, s = 2, F = F_{2,2} over Z/p in its Lyndon basis w_1 = x, w_2 = y, w_3 = z = [x,y].
G = the Heisenberg group of order p^3 (class 2 = c, exponent p, so e_p = 1), g_1, g_2 its
standard generators; pi : F -> log G is bijective, ker pi = 0, (ker pi)^perp = all of F^*.
Failure event of Lemma tb-kernel: the k Fourier samples (rows of Y) span only the hyperplane
W = (z - x + y)^perp, so ker Y = W^perp = span{z - x + y}, which contains ker pi but is not an
ideal ([x, z - x + y] = z). The column scan of Lemma tb-chart(a) keeps Yx, Yy (Yz = Yx - Yy),
the lifts are x, y, and (d) gives [eps_1, eps_2] = Y[x, y] = Yz = eps_1 - eps_2.
For e_p = 1 Theorem bb-envelope calls Theorem main on this chart with no check. The same
constants over Z/p^2 (a class-2 group of exponent p^2) pass the Lie-ring check of
appendix-torsion-blackbox.tex:1196-1200 (c_ii = 0, antisymmetry, torsion compatibility, Jacobi)."""
import itertools

def run(p):
    # F basis: 0 = x, 1 = y, 2 = z; bracket on basis of F
    def brF(i, j):
        v = [0, 0, 0]
        if (i, j) == (0, 1): v[2] = 1
        if (i, j) == (1, 0): v[2] = -1
        return v
    # projection Y: F -> A = F/K, K = span{z - x + y}: z == x - y mod K
    def Y(v):
        return [(v[0] + v[2]) % p, (v[1] - v[2]) % p]
    sec = {0: [1, 0, 0], 1: [0, 1, 0]}
    # chart structure constants c[i][j] = Y[s(e_i), s(e_j)]
    c = {(i, j): Y(brF(i, j)) for i in range(2) for j in range(2)}
    def br(u, v):
        w = [0, 0]
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    w[k] = (w[k] + u[i] * v[j] * c[(i, j)][k]) % p
        return w
    E = [[1, 0], [0, 1]]
    anti = all(c[(i, i)] == [0, 0] for i in range(2)) and all(
        [(a + b) % p for a, b in zip(c[(i, j)], c[(j, i)])] == [0, 0] for i in range(2) for j in range(2))
    jac = all(
        [(a + b + d) % p for a, b, d in zip(br(br(E[i], E[j]), E[k]), br(br(E[j], E[k]), E[i]), br(br(E[k], E[i]), E[j]))] == [0, 0]
        for i, j, k in itertools.product(range(2), repeat=3))
    # lower central series: gamma_1 = A, gamma_{n+1} = [gamma_n, A]; track one spanning vector
    gam = [E]
    for n in range(1, 6):
        new = [br(u, e) for u in gam[-1] for e in E]
        new = [v for v in new if v != [0, 0]]
        gam.append(new)
    dims = [min(2, len({tuple(v) for v in g})) if g else 0 for g in gam]
    print("p=%d: [xbar,ybar] = %s (i.e. xbar - ybar); antisymmetric: %s; Jacobi: %s; "
          "gamma_n nonzero for n = 1..6: %s" % (p, c[(0, 1)], anti, jac, [bool(g) for g in gam]))

for p in (3, 5, 7):
    run(p)
print("So gamma_{c+1}(A) = gamma_3(A) != 0 (A is not nilpotent): the chart passes a Lie check, "
      "fails gamma_{c+1} = 0, and Theorem main (class <= c) is called on it with no rule for that case.")
