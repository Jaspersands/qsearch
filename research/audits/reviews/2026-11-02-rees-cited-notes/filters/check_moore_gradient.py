"""Item (M): Moore-form family, orbit rank b^m versus the gradient row space.

Smallest note-covered instance: p = 5 (note needs p > 4), b = 3, m = 2,
Gamma = UT_3(F_5)^2 block-diagonal on D = 6, ell_i = first coordinate of
block i, F = det[[y1, y2], [y1^p, y2^p]].  Exact, formal, exhaustive:
  orbit rank = b^m = 9 (so cap 4 fails), via full orbit enumeration;
  W_F = row space of the formal gradient coefficients = span(e_0, e_3);
  Stab(F) = Stab(W) = {first-row off-diagonals zero} = UT_2(F_5)^2, |.| = 25.
Also b = 3, m = 3 (D = 9) orbit rank 27 by exact closure under generators.
And the Section-5 caveat: x0 + x1^p and x0 share a gradient, not a stabilizer.
"""
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from fp import act, block_diag, inverse, padd, pmul, ppow, pvar, rank, ut_group, identity, rref  # noqa: E402


def moore(rows_vars, n, p):
    y1, y2 = (pvar(v, n) for v in rows_vars[:2])
    if len(rows_vars) == 2:
        return padd(pmul(y1, ppow(y2, p, p, n), p), pmul(y2, ppow(y1, p, p, n), p), p, -1)
    # 3x3 Moore determinant det(y_j^(p^i))
    y = [pvar(v, n) for v in rows_vars]
    pw = [[ppow(y[j], p ** i, p, n) for j in range(3)] for i in range(3)]
    det = {}
    from itertools import permutations
    for perm in permutations(range(3)):
        sign = 1
        for a in range(3):
            for b_ in range(a + 1, 3):
                if perm[a] > perm[b_]:
                    sign = -sign
        term = pmul(pmul(pw[0][perm[0]], pw[1][perm[1]], p), pw[2][perm[2]], p)
        det = padd(det, term, p, sign)
    return det


def gradient_rowspace(F, n, p):
    """Row space of all coefficient vectors of the formal gradient (dF/dx_i)_i."""
    grads = []
    for i in range(n):
        g = {}
        for m, c in F.items():
            if m[i] and (m[i] * c) % p:
                mm = list(m); mm[i] -= 1
                g[tuple(mm)] = (g.get(tuple(mm), 0) + m[i] * c) % p
        grads.append({k: v for k, v in g.items() if v})
    monos = sorted({m for g in grads for m in g})
    rows = [[grads[i].get(mo, 0) for i in range(n)] for mo in monos]
    return rref([r for r in rows if any(r)], p)[0]


def key(g):
    return tuple(map(tuple, g))


if __name__ == "__main__":
    p, b, m = 5, 3, 2
    n = b * m
    F = moore([0, 3], n, p)
    G = [block_diag([g1, g2]) for g1 in ut_group(b, p) for g2 in ut_group(b, p)]
    orbit = {}
    for g in G:
        orbit[key(g)] = act(F, inverse(g, p), p)
    monos = sorted({mo for f in orbit.values() for mo in f})
    vecs = [[f.get(mo, 0) for mo in monos] for f in orbit.values()]
    r = rank(vecs, p)
    print(f"b={b}, m={m}, p={p}: |Gamma|={len(G)} exact orbit rank={r} (b^m={b**m}); cap 4 exceeded: {r > 4}")
    W = gradient_rowspace(F, n, p)
    print("gradient row space W_F (RREF):", W, "== span(e0,e3):", W == [[1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0]])
    stab = {key(g) for g in G if orbit[key(g)] == F}
    def preserves_W(g):
        gi = inverse(g, p)
        imgs = [[sum(w[k] * gi[k][j] for k in range(n)) % p for j in range(n)] for w in W]  # W * g^-1
        return rank(W + imgs, p) == len(W)
    stabW = {key(g) for g in G if preserves_W(g)}
    first_row_zero = {key(g) for g in G if all(g[0][j] == 0 for j in (1, 2)) and all(g[3][j] == 0 for j in (4, 5))}
    print(f"|Stab F|={len(stab)}  |Stab W|={len(stabW)}  |first-row-zero UT2^2|={len(first_row_zero)}  "
          f"all equal: {stab == stabW == first_row_zero}")

    # b=3, m=3: orbit rank by exact closure of the span under the generators
    m3, n3 = 3, 9
    F3 = moore([0, 3, 6], n3, p)
    gens = []
    for blk in range(m3):
        for (i, j) in ((0, 1), (1, 2)):
            g = identity(n3); g[3 * blk + i][3 * blk + j] = 1
            gens.append(g)
    ginv = [inverse(g, p) for g in gens]
    basis = [F3]
    monos3 = set(F3)
    def vec(f, ms):
        return [f.get(mo, 0) for mo in ms]
    queue = [F3]
    while queue:
        f = queue.pop()
        for gi in ginv:
            h = act(f, gi, p)
            ms = sorted(monos3 | set(h))
            if rank([vec(x, ms) for x in basis] + [vec(h, ms)], p) > len(basis):
                basis.append(h); monos3 |= set(h); queue.append(h)
    print(f"b=3, m=3, p=5: degree {1 + p + p * p}, exact orbit-span dimension by generator closure = {len(basis)} (b^m=27)")
    W3 = gradient_rowspace(F3, n3, p)
    print("m=3 gradient row space:", W3)

    # Section 5 caveat
    n2 = 2
    Fa = padd(pvar(0, n2), ppow(pvar(1, n2), p, p, n2), p)
    Fb = pvar(0, n2)
    shear_inv = inverse([[1, 0], [1, 1]], p)   # x1 -> x1 + x0
    print("x0 + x1^5 vs x0: same gradient row space:", gradient_rowspace(Fa, n2, p) == gradient_rowspace(Fb, n2, p),
          "; shear fixes x0:", act(Fb, shear_inv, p) == Fb, "; shear fixes x0+x1^5:", act(Fa, shear_inv, p) == Fa)
