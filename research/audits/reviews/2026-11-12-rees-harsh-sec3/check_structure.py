"""Checks of Thm 3.1 (rees-cover) (i)-(iii) on small algebras.

T1 Jacobi and lower central series.
T2 A closed under the bracket of L[t] with no nonzero bracket dropped; class(A)=class(L);
   top grade central.
T3 E_s Lie hom for every s in F_p (including 0), surjective for s != 0;
   delta_theta Lie automorphism; E_s o delta_theta = E_{theta s}.
T4 BCH group axioms (random triples); E_s and delta_theta group homs (random pairs, all s, theta);
   BCH implementation sanity: associativity.
"""
import random, sys
from lie import *

rng = random.Random(20261112)

CASES = [(heisenberg, 3), (heisenberg, 5), (free23, 5), (free23, 7), (free32, 3), (free32, 5),
         (filiform, 5), (filiform, 7), (dixmier_lister, 5), (dixmier_lister, 7)]


def lie_class_of_cover(cov):
    # lower central series of A computed directly on cover elements in coordinates
    p = cov.p
    basis = [cov.from_coords([1 if i == j else 0 for j in range(cov.n)]) for i in range(cov.n)]
    cur = basis
    k = 1
    while True:
        new = [cov.br(x, y) for x in basis for y in cur]
        new = [v for v in new if any(any(u) for u in v)]
        nb = span_basis([list(flat(v)) for v in new], p) if new else []
        if not nb:
            return k
        # back to elements
        cur = [tuple(b[i * cov.m:(i + 1) * cov.m] for i in range(cov.c)) for b in nb]
        k += 1


def run():
    bad = 0
    for mk, p in CASES:
        if mk is filiform:
            n = p  # filiform of dim p has class p-1: edge case p = c+1
            L = filiform(n, p)
        else:
            L = mk(p)
        c = L.c
        assert c < p, (L.name, p)
        ok_j = L.jacobi_ok()
        dims = [len(L.gam(k)) for k in range(1, c + 1)]
        cov = Cover(L)
        # T2
        cls = lie_class_of_cover(cov)
        top_central = True
        for (k, v) in cov.basis:
            if k != c:
                continue
            tv = tuple(v if i == c - 1 else [0] * L.m for i in range(c))
            for (k2, w) in cov.basis:
                tw = tuple(w if i == k2 - 1 else [0] * L.m for i in range(c))
                if any(any(u) for u in cov.br(tw, tv)):
                    top_central = False
        closed = all(cov.in_cover(cov.br(cov.random(rng), cov.random(rng))) for _ in range(30))
        # T3
        hom_ok = True
        for s in range(p):
            for _ in range(10):
                a, b = cov.random(rng), cov.random(rng)
                if cov.E(s, cov.br(a, b)) != L.br(cov.E(s, a), cov.E(s, b)):
                    hom_ok = False
        surj = all(rank(cov.E_matrix(s), p) == L.m for s in range(1, p))
        dil_ok = True
        for th in range(1, p):
            for _ in range(10):
                a, b = cov.random(rng), cov.random(rng)
                if cov.dil(th, cov.br(a, b)) != cov.br(cov.dil(th, a), cov.dil(th, b)):
                    dil_ok = False
                for s in range(p):
                    if cov.E(s, cov.dil(th, a)) != cov.E((th * s) % p, a):
                        dil_ok = False
        # T4
        Gp = Group(L, c)
        grp_ok = True
        for _ in range(15):
            a, b, d = cov.random(rng), cov.random(rng), cov.random(rng)
            if cov.mul(cov.mul(a, b), d) != cov.mul(a, cov.mul(b, d)):
                grp_ok = False
            if cov.mul(a, cov.neg(a)) != cov.zero() or cov.mul(a, cov.zero()) != a:
                grp_ok = False
            x, y, z = [rng.randrange(p) for _ in range(L.m)], [rng.randrange(p) for _ in range(L.m)], [rng.randrange(p) for _ in range(L.m)]
            if Gp.mul(Gp.mul(x, y), z) != Gp.mul(x, Gp.mul(y, z)):
                grp_ok = False
        ghom = True
        for s in range(p):
            for _ in range(6):
                a, b = cov.random(rng), cov.random(rng)
                if cov.E(s, cov.mul(a, b)) != Gp.mul(cov.E(s, a), cov.E(s, b)):
                    ghom = False
        for th in range(1, p):
            for _ in range(4):
                a, b = cov.random(rng), cov.random(rng)
                if cov.dil(th, cov.mul(a, b)) != cov.mul(cov.dil(th, a), cov.dil(th, b)):
                    ghom = False
        # nonabelian sanity: group really nonabelian when L is
        nonab = any(cov.mul(a, b) != cov.mul(b, a) for a, b in [(cov.random(rng), cov.random(rng)) for _ in range(5)])
        row = dict(alg=L.name, p=p, jacobi=ok_j, lcs=dims, n=cov.n, classA=cls, classL=c,
                   top_central=top_central, closed=closed, E_lie_hom_all_s=hom_ok, E_surj=surj,
                   dil_aut_and_Edil=dil_ok, bch_group=grp_ok, E_dil_group_hom=ghom, nonabelian=nonab)
        flags = [ok_j, cls == c, top_central, closed, hom_ok, surj, dil_ok, grp_ok, ghom]
        if not all(flags):
            bad += 1
        print(row)
        sys.stdout.flush()
    print("FAILURES:", bad)


if __name__ == "__main__":
    run()
