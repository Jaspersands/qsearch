"""Item (i): exact exhaustive check of the faithful orbit-module reduction.

For small Gamma = UT_b(F_p) and explicit F, compute (all exact, formal
polynomials over F_p, no evaluation):
  W = span{T_g F}, (T_g F)(x) = F(g^{-1} x), basis B_0 = F;
  rho_W(g) on that basis; ker rho_W;
  Stab(F) directly;  Stab of v=(0_D, e_0) under diag(g, rho_W(g));
  the quotient-only stabilizer inside rho_W(Gamma).
Claims checked: Stab(F) == vector stabilizer (as subsets of Gamma), rho_W
is a homomorphism, |Stab(F)| = |ker| * |quotient stabilizer|, and explicit
large kernels exist (index p, and the whole nonabelian group).
"""
import random
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from fp import act, coords, identity, inverse, matmul, padd, pmul, ppow, pvar, ut_group, pconst, pscale  # noqa: E402


def key(g):
    return tuple(map(tuple, g))


def analyze(name, b, p, F):
    G = list(ut_group(b, p))
    orbit = {key(g): act(F, inverse(g, p), p) for g in G}
    monos = sorted({m for f in orbit.values() for m in f} | set(F))
    vec = lambda f: [f.get(m, 0) for m in monos]
    basis, basis_vecs = [F], [vec(F)]
    from fp import rank
    for f in orbit.values():
        v = vec(f)
        if rank(basis_vecs + [v], p) > len(basis_vecs):
            basis.append(f)
            basis_vecs.append(v)
    W = len(basis)
    rho = {}
    for g in G:
        gi = inverse(g, p)
        cols = []
        for B in basis:
            c = coords(basis_vecs, vec(act(B, gi, p)), p)
            assert c is not None, "W not invariant"
            cols.append(c)
        rho[key(g)] = [[cols[j][i] for j in range(W)] for i in range(W)]
    # homomorphism check on random pairs
    rng = random.Random(1)
    for _ in range(200):
        g, h = rng.choice(G), rng.choice(G)
        gh = matmul(g, h, p)
        assert rho[key(gh)] == matmul(rho[key(g)], rho[key(h)], p), "rho not a homomorphism"
    I = identity(W)
    ker = [g for g in G if rho[key(g)] == I]
    stab_direct = {key(g) for g in G if orbit[key(g)] == ({m: c for m, c in F.items()})}
    e0 = [1] + [0] * (W - 1)
    stab_vector = {key(g) for g in G if [row[0] for row in rho[key(g)]] == e0}
    image = {key(r) for r in rho.values()}
    image_stab = {r for r in image if [row[0] for row in r] == e0}
    nonabelian_kernel = any(matmul(g, h, p) != matmul(h, g, p) for g in ker for h in ker)
    ok = stab_direct == stab_vector and len(stab_direct) == len(ker) * len(image_stab)
    print(f"{name}: |Gamma|={len(G)} dim W={W} |ker rho_W|={len(ker)} "
          f"(index {len(G)//len(ker)}, nonabelian={nonabelian_kernel}) |Stab F|={len(stab_direct)} "
          f"|Stab in rho_W(Gamma)|={len(image_stab)} faithful-reduction-equal={stab_direct == stab_vector} "
          f"order-identity={ok}")
    return ok


def moore2(i, j, n, p):
    xi, xj = pvar(i, n), pvar(j, n)
    return padd(pmul(xi, ppow(xj, p, p, n), p), pmul(xj, ppow(xi, p, p, n), p), p, -1)


def random_poly(n, p, deg, terms, seed):
    rng = random.Random(seed)
    f = {}
    for _ in range(terms):
        m = [0] * n
        for _ in range(rng.randint(1, deg)):
            m[rng.randrange(n)] += 1
        f = padd(f, {tuple(m): rng.randrange(1, p)}, p)
    return f


if __name__ == "__main__":
    results = [
        analyze("A UT3(F3), F=x1", 3, 3, pvar(1, 3)),
        analyze("B UT3(F5), F=x1", 3, 5, pvar(1, 3)),
        analyze("C UT4(F3), F=x2", 4, 3, pvar(2, 4)),
        analyze("D UT3(F5), F=Moore minor x0 x1^5 - x1 x0^5 (note's control)", 3, 5, moore2(0, 1, 3, 5)),
        analyze("E UT3(F3), F=x2 (invariant coordinate)", 3, 3, pvar(2, 3)),
        analyze("F UT3(F3), F=x2^2 + x1 x2 (kernel+proper stab)", 3, 3,
                padd(ppow(pvar(2, 3), 2, 3, 3), pmul(pvar(1, 3), pvar(2, 3), 3), 3)),
        analyze("G UT4(F3), F=x1 x3 + x2^2", 4, 3,
                padd(pmul(pvar(1, 4), pvar(3, 4), 3), ppow(pvar(2, 4), 2, 3, 4), 3)),
        analyze("H UT3(F3), random cubic", 3, 3, random_poly(3, 3, 3, 6, 7)),
        analyze("I UT4(F3), random cubic", 4, 3, random_poly(4, 3, 3, 6, 11)),
    ]
    print("ALL_PASS" if all(results) else "FAILURE")
