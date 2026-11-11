"""One dependency never gains two dimensions at p = 5, S = {0,+-1}, with ARBITRARY
multiplicities and per-column Phi (no Lemma Q / label-set reduction).

Y a set of columns with dim D(Y) = 1, D(Y) = <w>.  If R(Y) contains a 2-dim subgroup <h1,h2>,
Lemma 2 gives per-column Phi_i = (y_e1(i), y_e2(i)) in S^2 and g(alpha) in F_5 (g(e_j) = 0) with
  y_alpha(i) = <alpha, Phi_i> + g(alpha) w_i  in S  for all alpha in F_5^2, i in Y,
and h_j = sum_i Phi_ij v_i independent: no (a,b) != 0, lam in F_5 with a Phi_.1 + b Phi_.2 = lam w
(since the only relation among the v_i is w).  Columns with w_i = 0 have Phi_i = 0 (they would need
<alpha,Phi_i> in S for all alpha).  A column TYPE is (Phi, c) with Phi in S^2, c = w_i in F_5^*.
Multiplicities are free, so a solution exists iff for some g the set T_g of admissible types
violates every (a,b,lam) (one admissible type with a Phi1 + b Phi2 != lam c for each triple).
CNF over g (one-hot) and type indicators; pycosat; then an exhaustive brute-force cross-check
over g restricted by the 2-adic necessary condition (independent code path).
"""
import itertools
import pycosat

p = 5
S = {0, 1, 4}
F2 = list(itertools.product(range(p), repeat=2))
alphas = [a for a in F2 if any(a)]
free_alphas = [a for a in alphas if a not in ((1, 0), (0, 1))]
types = [(phi, c) for phi in itertools.product(sorted(S), repeat=2) for c in range(1, p)]


def admissible(phi, c, g):
    return all((a[0] * phi[0] + a[1] * phi[1] + c * g[a]) % p in S for a in alphas)


def cnf():
    nv = [0]; cl = []

    def var():
        nv[0] += 1; return nv[0]
    G = {a: [var() for _ in range(p)] for a in free_alphas}
    for a in free_alphas:
        cl.append(G[a][:])
        cl.extend([[-G[a][i], -G[a][j]] for i in range(p) for j in range(i + 1, p)])
    T = {t: var() for t in types}
    for (phi, c), v in T.items():
        for a in alphas:
            base = (a[0] * phi[0] + a[1] * phi[1]) % p
            if a in ((1, 0), (0, 1)):
                if base not in S:
                    cl.append([-v])
                continue
            for x in range(p):
                if (base + c * x) % p not in S:
                    cl.append([-v, -G[a][x]])
    projs = [(1, 0), (0, 1)] + [(1, b) for b in range(1, p)]
    for (a, b) in projs:
        for lam in range(p):
            cl.append([T[(phi, c)] for (phi, c) in types if (a * phi[0] + b * phi[1] - lam * c) % p])
    return cl


def main():
    cl = cnf()
    sol = pycosat.solve(cl)
    print('CNF: %d clauses ->' % len(cl), 'UNSAT' if sol == 'UNSAT' else 'SAT')
    # Independent cross-check: g must satisfy, for every type that is ever usable, all alphas.
    # Brute force over g on the 22 free alphas is 5^22; instead enumerate g direction by direction:
    # for each type (phi,c) and alpha, the admissible values of g(alpha) form a set A(phi,c,alpha).
    # A solution needs a family of admissible types; for each family check feasibility of g by
    # intersecting per-alpha sets.  Families: all subsets of the 36 types is 2^36 -- too many, so
    # use maximal-family closure: for each g-assignment per alpha separately the constraint is
    # separable, hence g exists for a family F iff for every alpha the sets A(t,alpha), t in F,
    # have a common value.  Enumerate families via the 'value profile': for each alpha choose
    # g(alpha) in F_5 independently -> family T_g = intersection over alpha; distinct T_g are
    # obtained from the product of per-alpha admissible-type sets, computed by DP over alphas.
    per = {}
    for a in free_alphas:
        per[a] = [frozenset(t for t in types if (a[0] * t[0][0] + a[1] * t[0][1] + t[1] * x) % p in S)
                  for x in range(p)]
    base = frozenset(t for t in types
                     if all((a[0] * t[0][0] + a[1] * t[0][1]) % p in S for a in ((1, 0), (0, 1))))
    fams = {base}
    for a in free_alphas:
        fams = {f & s for f in fams for s in per[a]}
    projs = [(1, 0), (0, 1)] + [(1, b) for b in range(1, p)]

    def gains2(f):
        return all(any((a * t[0][0] + b * t[0][1] - lam * t[1]) % p for t in f)
                   for (a, b) in projs for lam in range(p))
    good = [f for f in fams if gains2(f)]
    print('distinct admissible-type families T_g: %d; families allowing an independent pair: %d'
          % (len(fams), len(good)))


if __name__ == '__main__':
    main()
