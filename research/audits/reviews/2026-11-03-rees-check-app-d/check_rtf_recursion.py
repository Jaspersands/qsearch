"""Exact simulation of Algorithm RtF (Prop. tb-recursion) on small mixed-order rings.

Truth solver: returns exactly (h/K) cap M[p]. Adversarial solver: returns a
random additive subgroup between K and the socle preimage P (possibly not a
subalgebra, possibly not containing the truth). Checks, on every branch:
  * at most b calls, none on a trivial section;
  * truth solver returns h; normalizer invariant K <= h <= S;
  * socle class <= min(c, R+1), derived rank of every section <= R;
  * the appendix sentence "log_p|H| enlarging calls plus one final call when
    H != G" (expected to FAIL as an equality; only the <= b total is claimed);
  * sum of socle dimensions vs b (relevant to thm:bb-envelope's accounting).
"""
import random, sys
from lazard_small import Ring, logp

random.seed(20261103)

def rings():
    R = []
    R.append(("Z/27", Ring(3, [3], {}, 1)))
    R.append(("Z/25+Z/5 abelian", Ring(5, [2, 1], {}, 1)))
    R.append(("(Z/9)^2 [x,y]=3y", Ring(3, [2, 2], {(0, 1): (0, 3)}, 2)))
    R.append(("Z/9+Z/3+Z/3 [e2,e3]=3e1", Ring(3, [2, 1, 1], {(1, 2): (3, 0, 0)}, 2)))
    R.append(("Heis(Z/9)", Ring(3, [2, 2, 2], {(0, 1): (0, 0, 1)}, 2)))
    R.append(("Z/25+Z/5 [e1,e2]=5e1", Ring(5, [2, 1], {(0, 1): (5, 0)}, 2)))
    R.append(("Z/25+Z/5+Z/5 [e0,e1]=e2,[e0,e2]=5e0 class3", Ring(5, [2, 1, 1], {(0, 1): (0, 0, 1), (0, 2): (5, 0, 0)}, 3)))
    R.append(("Z/5^2+Z/5^2 [x,y]=5y class2", Ring(5, [2, 2], {(0, 1): (0, 5)}, 2)))
    return R


def agens(L, S):
    """Greedy additive generators of an additive subgroup S."""
    span, out = {L.zero}, []
    for x in sorted(S):
        if x not in span:
            out.append(x)
            new, m = set(span), x
            while m != L.zero:
                new |= {L.add(s, m) for s in span}
                m = L.add(m, x)
            span = new
    assert span == set(S)
    return out


def bspan(L, A, B, extra=()):
    return L.additive_span({L.br(a, b) for a in agens(L, A) for b in agens(L, B)} | set(extra))


def socle_pre(L, K, S):
    return frozenset(x for x in S if L.smul(L.p, x) in K)


def idealizer(L, S, Kp):
    gens = agens(L, Kp)
    return frozenset(x for x in S if all(L.br(x, k) in Kp for k in gens))


def section_class(L, P, K):
    """class of the F_p algebra P/K."""
    cls, cur = 0, P
    while not cur <= K:
        cls += 1
        cur = bspan(L, P, cur, agens(L, K))
    return cls


def section_derived_rank(L, S, K):
    D = bspan(L, S, S, agens(L, K))
    # d((D)/K): number of cyclic factors of D/K = dim of (D/K)[p]
    pts = sum(1 for x in D if L.smul(L.p, x) in K)
    return logp(pts // len(K), L.p)


def rtf(L, h, solver, R, stats):
    K, S = frozenset([L.zero]), frozenset(L.elements())
    b = sum(L.exps)
    calls = 0
    while True:
        if S == K:
            return K, calls
        P = socle_pre(L, K, S)
        assert len(P) > len(K)
        stats["socle_dims"].append(logp(len(P) // len(K), L.p))
        assert section_class(L, P, K) <= min(L.cls, R + 1), "socle class"
        assert section_derived_rank(L, S, K) <= R, "section derived rank"
        calls += 1
        assert calls <= b, "call cap"
        Kp = solver(L, h, K, S, P)
        g = agens(L, Kp)
        if Kp == K or not all(L.br(a, b) in Kp for a in g for b in g):
            return K, calls
        stats["enlarging"] += 1
        Sp = idealizer(L, S, Kp)
        assert Kp <= Sp and all(L.br(s, k) in Kp for s in agens(L, Sp) for k in agens(L, Kp))
        K, S = Kp, Sp


def truth(L, h, K, S, P):
    assert K <= h <= S, "invariant K<=h<=S"
    return frozenset(h & P)


def adversary(L, h, K, S, P):
    r = random.random()
    if r < 0.3:
        return truth(L, h, K, S, P) if K <= h <= S else K
    if r < 0.4:
        return K
    extra = random.sample(sorted(P - K), min(len(P - K), random.randint(1, 2)))
    return L.additive_span(set(K) | set(extra))


def hidden_subrings(L, count):
    els = L.elements()
    seen = {frozenset([L.zero]), frozenset(els)}
    for _ in range(count):
        g = random.sample(els, random.randint(1, 2))
        seen.add(L.subring(g))
    return sorted(seen, key=len)


def main():
    total_cases = fail_eq = 0
    worst_ratio = (0, None)
    smallest_eq_cex = None
    for name, L in rings():
        b = sum(L.exps)
        basis = [tuple(int(i == j) for j in range(L.n)) for i in range(L.n)]
        for x in basis:
            for y in basis:
                for z in basis:
                    j = L.add(L.add(L.br(x, L.br(y, z)), L.br(y, L.br(z, x))), L.br(z, L.br(x, y)))
                    assert j == L.zero, (name, "Jacobi")
        assert len(L.lcs_dims(frozenset(L.elements()))) == L.cls, (name, "declared class")
        assert L.p > L.cls
        Lset = frozenset(L.elements())
        R = L.cyc_rank(bspan(L, Lset, Lset))
        Hs = hidden_subrings(L, 60)
        for h in Hs:
            stats = {"socle_dims": [], "enlarging": 0}
            out, calls = rtf(L, h, truth, R, stats)
            assert out == h, (name, "wrong output")
            total_cases += 1
            lh = logp(len(h), L.p)
            claimed = lh + (0 if len(h) == len(L.elements()) else 1)
            if calls != claimed:
                fail_eq += 1
                cand = (len(L.elements()), name, lh, calls, claimed, stats["enlarging"])
                if smallest_eq_cex is None or cand < smallest_eq_cex:
                    smallest_eq_cex = cand
            ratio = sum(stats["socle_dims"]) / b
            if ratio > worst_ratio[0]:
                worst_ratio = (ratio, (name, lh, stats["socle_dims"], b))
            for _ in range(15):
                st2 = {"socle_dims": [], "enlarging": 0}
                rtf(L, h, adversary, R, st2)
        print(f"{name}: b={b} R={R} class={L.cls} subrings tested={len(Hs)}", flush=True)
    print("truth-solver cases:", total_cases, "all returned h within b calls")
    print("adversarial branches: 15 per case, call cap <= b and invariants held")
    print("cases where calls != log_p|H| + [H!=G]:", fail_eq)
    print("smallest such case (|L|, ring, log_p|H|, calls, claimed, enlarging):", smallest_eq_cex)
    print("max (sum of socle dims)/b:", worst_ratio)


if __name__ == "__main__":
    main()
