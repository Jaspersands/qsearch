"""Corollary tb-correspondence (a)-(c), brute force on small mixed-order rings.

(a) group closure under BCH of any 1-2 elements == Lie subring they generate;
(b) normalizer of K in (S,*) == idealizer I_S(K), for S = L and S = a subring;
(c) for ideals K of S: x*K == x+K for all x in S.
"""
import random
from lazard_small import Ring

random.seed(11)
rings = [
    ("(Z/9)^2 [x,y]=3y", Ring(3, [2, 2], {(0, 1): (0, 3)}, 2)),
    ("Heis(Z/9)", Ring(3, [2, 2, 2], {(0, 1): (0, 0, 1)}, 2)),
    ("Z/25+Z/5 [e1,e2]=5e1", Ring(5, [2, 1], {(0, 1): (5, 0)}, 2)),
    ("Z/25+Z/5+Z/5 class3", Ring(5, [2, 1, 1], {(0, 1): (0, 0, 1), (0, 2): (5, 0, 0)}, 3)),
    ("F_5^4 filiform class3", Ring(5, [1, 1, 1, 1], {(0, 1): (0, 0, 1, 0), (0, 2): (0, 0, 0, 1)}, 3)),
]
for name, L in rings:
    els = L.elements()
    subs = set()
    for _ in range(80):
        g = random.sample(els, random.randint(1, 2))
        G = L.group_closure(g)
        R = L.subring(g)
        assert G == R, (name, "(a)")
        subs.add(R)
    nb = ni = 0
    subs = sorted(subs, key=len)
    for S in [frozenset(els)] + random.sample(subs, min(4, len(subs))):
        for K in subs:
            if not K <= S:
                continue
            gensK = list(K)
            norm = frozenset(x for x in S
                             if {L.bch(L.bch(x, k), L.neg(x)) for k in gensK} <= K)
            ideal = frozenset(x for x in S if all(L.br(x, k) in K for k in gensK))
            assert norm == ideal, (name, "(b)")
            nb += 1
            if ideal == S:
                for x in random.sample(sorted(S), min(40, len(S))):
                    assert {L.bch(x, k) for k in K} == {L.add(x, k) for k in K}, (name, "(c)")
                ni += 1
    print(f"{name}: (a) 80 generating sets; (b) {nb} pairs (K,S); (c) {ni} ideal pairs: all hold")
