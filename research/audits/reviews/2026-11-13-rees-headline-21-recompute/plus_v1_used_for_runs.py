"""Schedule 1H+ degrees e^+_kappa at a prime p, from fragment.tex (Def. def:schedule1hplus)
and the core (Def. def:schedule1h).  Availability of contractions: Lemma lem:sm thresholds
(verified in thresholds_check.py) or this checker's own search (rcsearch.c), never the
helper's tables.  Interpretation flags are explicit (see report)."""
from math import gcd
from fp import Field, t_pk, T_sets
T_EXIST = {"TL3": 430, "TL4": 9395, "TL5": 99745, "TW9": 1124521, "U7": 1995734}

def clog2(t): return (t - 1).bit_length()
def lift(Kp, Dp, D): return frozenset(x for x in range(D) if x % Dp in Kp)

class PlusDegrees:
    def __init__(self, S, tierB=lambda p: p <= 523, unknown_as=False, lift_variant=False,
                 exhaustive_pmax=600, ecap=3 * 10**6, rtrials=300, standard_extra=True):
        self.S = S; self.tierB = tierB; self.unknown_as = unknown_as
        self.lift_variant = lift_variant; self.exhaustive_pmax = exhaustive_pmax
        self.ecap = ecap; self.rtrials = rtrials
        self.unknowns = []

    def avail(self, p, D, R, K, std=None):
        if std is not None and p >= T_EXIST[std]: return True
        st, _ = self.S.status(p, D, sorted(R), sorted(K), rtrials=self.rtrials, ecap=self.ecap,
                              exhaustive=(p <= self.exhaustive_pmax))
        if st == "FOUND": return True
        if st == "NONE": return False
        self.unknowns.append((p, D, tuple(sorted(R)), tuple(sorted(K))))
        return self.unknown_as

    def degrees(self, p, F=None, want_trace=False):
        ks = [k for k in range(1, 10) if (p - 1) % k == 0]
        if F is None and any(p < 4 * k ** 4 for k in ks if k >= 2): F = Field(p)
        e = {1: 1}; how = {1: "GE"}
        tb = self.tierB(p)
        chain_nodes = {}   # (D, K) -> (deg, desc) best chain node at exact modulus D (tier B)
        for k in ks:
            if k == 1: continue
            cands = []
            t = t_pk(F, k) if (F is not None and p < 26244) else (2 if ((p - 1) // k) % 2 == 0 else 3)
            cands.append((k * clog2(t), f"S1(t={t})"))
            zeroK = frozenset({0})
            # standard chains (c), (d)
            if k in (3, 4, 5) and self.avail(p, k, range(k), [0], std=f"TL{k}"):
                cands.append((2, "TL"))
            if k == 9 and self.avail(p, 9, [0, 3, 6], [0], std="TW9"):
                cands.append((e[3] + 1, "TW/H3"))
            # tier B chains ending at modulus k
            nodes_k = {}
            if tb:
                nodes_k = self.tierB_chains(p, k, e)
                for (D, K), (dg, ds) in nodes_k.items():
                    if D == k and K == zeroK: cands.append((dg, "B:" + ds))
            # stage nodes {0,m} at modulus k
            stages = []
            if k % 2 == 0: stages.append((k // 2, e[k // 2], f"H{k//2}"))
            if k == 7:
                for m in range(1, 7):
                    if self.avail(p, 7, range(7), [0, m], std="U7"): stages.append((m, 2, f"U7m{m}"))
            for (D, K), (dg, ds) in nodes_k.items():
                if D == k and len(K) == 2: stages.append((max(K), dg, "B:" + ds))
            # finish K-nodes at modulus k
            fin = [(frozenset(range(k)), 1, "F1")]
            for Dp in ks:
                if 2 <= Dp < k and k % Dp == 0: fin.append((lift({0}, Dp, k), e[Dp], f"FH{Dp}"))
            for (D, K), (dg, ds) in nodes_k.items():
                if D == k: fin.append((K, dg, "FB:" + ds))
                elif self.lift_variant and k % D == 0: fin.append((lift(K, D, k), dg, "FBlift:" + ds))
            for (m, eN, nm) in stages:
                if p >= 4 * k ** 4:
                    cands.append((eN + 1, f"({nm})x1,F1")); continue
                T = T_sets(F, k, m, k + 2)
                for s in range(1, k + 3):
                    if T[s].zero: cands.append((s * eN, f"({nm})x{s},F0"))
                    for (Kf, eK, fn) in fin:
                        if any(all((u + x) % k in T[s].cls for x in Kf) for u in range(k)):
                            cands.append((s * eN + eK, f"({nm})x{s},{fn}"))
            best = min(cands, key=lambda c: c[0])
            e[k] = best[0]; how[k] = best[1]
        return (e, how) if want_trace else e

    def tierB_chains(self, p, k, e):
        """min degree e0+L (L<=3) of chain nodes with all moduli dividing k, |K_t|<=3."""
        divs = [D for D in range(2, k + 1) if k % D == 0]
        states = []
        from itertools import combinations
        for D in divs:
            others = [x for x in range(1, D)]
            for sz in range(0, 3):
                for c in combinations(others, sz): states.append((D, frozenset((0,) + c)))
        level = {(1, frozenset({0})): (1, "GE")}
        for D0 in divs:
            if D0 < k: level[(D0, frozenset({0}))] = (e[D0], f"H{D0}")
        best = {}
        for L in range(1, 4):
            new = {}
            for (Dp, Kp), (dg, ds) in level.items():
                for (D, K) in states:
                    if D % Dp: continue
                    R = lift(Kp, Dp, D)
                    if len(R) < 2: continue
                    cand = dg + 1
                    if (D, K) in new and new[(D, K)][0] <= cand: continue
                    if (D, K) in best and best[(D, K)][0] <= cand: continue
                    if self.avail(p, D, R, K):
                        new[(D, K)] = (cand, f"{ds}->({D},{sorted(K)})")
            for s, v in new.items():
                if s not in best or v[0] < best[s][0]: best[s] = v
            level = new
        return best

def grade_sum(p, e, c): return sum(e[gcd(d, p - 1)] for d in range(2, c + 1))
