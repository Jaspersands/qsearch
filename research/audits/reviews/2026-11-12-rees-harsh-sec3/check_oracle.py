"""Group-level checks of the tuple oracle (Lemma 3.2 statement about f-hat, Lemma 3.3 query count),
using an honest coset oracle f on G = (L,*) that is built from H by BCH and is then used as a black box.

O1 exhaustive: Heisenberg over F_3, every subalgebra hh, every pair (a,b) in the cover:
   fhat(a)==fhat(b)  <=>  (-a)*b in hlift.
O2 sampled: larger algebras, adversarial and random H, point sets {1..c}, random c-sets and
   c-sets with s^k collisions; pairs b = a*u with u in hlift / u in P_{c-1}\hlift / random.
O3 exp(hlift) closed under the BCH product of the cover (random pairs).
O4 query count: each fhat costs exactly c queries of f.
O5 paper's worked examples (intro class-3 example, Heisenberg F_3 example after Prop 3.4).
O6 negative control: with c-1 points (1..c-1) a pair with equal labels but (-a)*b not in hlift is found.
"""
import random, sys
from itertools import combinations
from lie import *

rng = random.Random(99)


def member(cov, a, hl):
    return elem_in_coords_space(cov, a, hl)


def rand_in(cov, B):
    alpha = [0] * cov.n
    for b in B:
        c_ = rng.randrange(cov.p)
        alpha = [(x + c_ * y) % cov.p for x, y in zip(alpha, b)]
    return cov.from_coords(alpha)


def O1():
    L = heisenberg(3)
    cov = Cover(L)
    Gp = Group(L)
    pts = [1, 2]
    allA = [cov.from_coords(list(t)) for t in product(range(3), repeat=cov.n)]
    nsub = npairs = bad = 0
    for hh in all_subspaces(3, 3):
        if not L.is_subalgebra(hh):
            continue
        nsub += 1
        f = CosetOracle(Gp, hh)
        hl = cov.hlift_coords(hh)
        lab = {flat(a): tuple_oracle(cov, f, pts, a) for a in allA}
        for a in allA:
            for b in allA:
                npairs += 1
                if (lab[flat(a)] == lab[flat(b)]) != member(cov, cov.mul(cov.neg(a), b), hl):
                    bad += 1
    print("O1 Heisenberg F_3 exhaustive: subalgebras=%d pairs=%d mismatches=%d" % (nsub, npairs, bad))
    return bad


def adversarial_H(L, name):
    p, m = L.p, L.m
    e = lambda i: [1 if j == i else 0 for j in range(m)]
    add = lambda *vs: [sum(x) % p for x in zip(*vs)]
    Hs = [("trivial", []), ("gamma2", L.gam(2)), ("gamma_c", L.gam(L.c))]
    if name == "free(2,3)":
        Hs += [("paper x+z+u", [add(e(0), e(2), e(3))]), ("<x>", [e(0)]), ("<x+u>", [add(e(0), e(3))]),
               ("<x,w>", L.closure([e(0), e(4)])), ("<x+z>", [add(e(0), e(2))])]
    if name == "Dixmier-Lister":
        Hs += [("<e1+e5+e7>", [add(e(0), e(4), e(6))]), ("<e1,e8>", L.closure([e(0), e(7)])),
               ("<e1+e6, e2+e7>", L.closure([add(e(0), e(5)), add(e(1), e(6))]))]
    if name.startswith("filiform"):
        Hs += [("<e1+e3+e4>", [add(e(0), e(2), e(3))]), ("<e2+e3>", [add(e(1), e(2))])]
    for _ in range(6):
        g = rng.randrange(1, 3)
        Hs.append(("random", L.closure([[rng.randrange(p) for _ in range(m)] for _ in range(g)])))
    return Hs


def O2_O3_O4(L, ntrials=40):
    p, c = L.p, L.c
    cov = Cover(L)
    Gp = Group(L)
    units = list(range(1, p))
    psets = [list(range(1, c + 1))]
    psets.append(sorted(rng.sample(units, c)))
    # a set with s^k collisions: contains s and -s (s^2 = (-s)^2)
    coll = [1, p - 1] + [s for s in units if s not in (1, p - 1)][:c - 2]
    if len(coll) == c:
        psets.append(coll)
    bad = checks = closed_bad = qbad = 0
    for hname, hh in adversarial_H(L, L.name):
        hh = span_basis(hh, p) if hh else []
        if p ** len(hh) > 700:
            continue  # keep the honest min-over-coset oracle affordable
        f = CosetOracle(Gp, hh)
        hl = cov.hlift_coords(hh)
        Pc1 = cov.pullback_coords(hh, list(range(1, c))) if c >= 2 else hl
        extra = [b for b in Pc1 if not in_span(b, hl, p)]
        for S in psets:
            for t in range(ntrials):
                a = cov.random(rng)
                kind = t % 3
                if kind == 0:
                    u = rand_in(cov, hl) if hl else cov.zero()
                elif kind == 1 and extra:
                    u = cov.add(rand_in(cov, hl) if hl else cov.zero(), cov.from_coords(extra[0]))
                else:
                    u = cov.random(rng)
                b = cov.mul(a, u)
                q0 = f.queries
                fa = tuple_oracle(cov, f, S, a)
                if f.queries - q0 != c:
                    qbad += 1
                fb = tuple_oracle(cov, f, S, b)
                checks += 1
                if (fa == fb) != member(cov, cov.mul(cov.neg(a), b), hl):
                    bad += 1
        for _ in range(10):
            x, y = rand_in(cov, hl) if hl else cov.zero(), rand_in(cov, hl) if hl else cov.zero()
            if hl and not member(cov, cov.mul(x, y), hl):
                closed_bad += 1
    print("O2-O4 %s p=%d c=%d point sets=%s: checks=%d mismatches=%d closure_fail=%d query_count_fail=%d"
          % (L.name, p, c, psets, checks, bad, closed_bad, qbad))
    return bad + closed_bad + qbad


def O5():
    out = 0
    for p in (5, 7, 11):
        L = free23(p)
        cov = Cover(L)
        hh = [[1, 0, 1, 1, 0]]  # x + z + u, u = [x,z]
        uvec = [0, 0, 0, 1, 0]
        v = (tuple([(2 * a) % p for a in uvec]), tuple([(-3 * a) % p for a in uvec]), tuple(uvec))
        v = tuple(list(x) for x in v)
        res = [in_span(cov.E(s, v), hh, p) for s in (1, 2, 3)]
        Es = [cov.E(s, v) for s in (1, 2, 3)]
        ok = res == [True, True, False] and Es[2] == [(6 * a) % p for a in uvec]
        print("O5 intro example p=%d: E_s(v) in hh for s=1,2,3:" % p, res, "E_3(v)=6u:", Es[2] == [(6 * a) % p for a in uvec])
        out += 0 if ok else 1
    L = heisenberg(3)
    cov = Cover(L)
    u = ([0, 0, 1], [0, 0, 2])  # tz - t^2 z over F_3
    d2 = cov.dil(2, u)
    ok = cov.E(1, u) == [0, 0, 0] and d2 == ([0, 0, 2], [0, 0, 2]) and cov.E(1, d2) == [0, 0, 1]
    print("O5 Heisenberg F_3 example: E1(u)=0, delta_2(u)=2tz - t^2 z, E1(delta_2 u)=z :", ok)
    return out + (0 if ok else 1)


def O6():
    L = free23(5)
    cov = Cover(L)
    Gp = Group(L)
    f = CosetOracle(Gp, [])
    hl = cov.hlift_coords([])
    S = [1, 2]
    P2 = cov.pullback_coords([], S)
    u = cov.from_coords(P2[0])
    a = cov.random(rng)
    b = cov.mul(a, u)
    eq = tuple_oracle(cov, f, S, a) == tuple_oracle(cov, f, S, b)
    nonmem = not member(cov, cov.mul(cov.neg(a), b), hl)
    print("O6 negative control (2 points at class 3, H=1): dim P_2=%d, equal labels=%s, not in hlift=%s"
          % (len(P2), eq, nonmem))
    return 0 if (eq and nonmem) else 1


if __name__ == "__main__":
    tot = O1()
    for L in (heisenberg(5), heisenberg(7), free23(5), free23(7), free32(5), filiform(5, 5),
              dixmier_lister(5), dixmier_lister(7)):
        tot += O2_O3_O4(L)
        sys.stdout.flush()
    tot += O5()
    tot += O6()
    print("TOTAL FAILURES:", tot)
