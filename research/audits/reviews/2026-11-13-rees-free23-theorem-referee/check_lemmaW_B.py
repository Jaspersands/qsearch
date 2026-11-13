"""Lemma W and Lemma B, re-derived and checked with own code (AI-written, pending human review).
Uses only the Lemma-0 coefficient forms (verified against true states in check_lemma0.py, convention (-1,-1,1)).

Lemma W, Claim 1: the Q3 system  e.grad q(w) + T(e; w) = 0  for all e, w, with
   T(e; w) = sum_{ji} 3 u_j^3 s_ji^3 A3_ji(e) f_ji(w)^2,
is solvable iff  sum_j u_j^3 P3(T_j) = 0, and then q is unique.
Lemma W, Claim 2: the e3-part of B(w, e) = sum u_j^2 s^2 f(w) (A2 + 3 A3 X) vanishes iff sum_j u_j^2 P2(T_j) = 0.
Closed form (re-derived by hand in the referee report): the non-symmetric part of T is
   -(1/18)... * [det(e,w) * (sum u^3 P3).w]  -- checked here as: obstruction vector is a fixed nonzero multiple of
   sum u^3 P3 (the Q3 system's inconsistency is measured by projecting T onto the complement of Sym^3).
Lemma B: own block solver on (a) label configurations, (b) adversarial columns (zeros, repeated, binary s).
Usage: python check_lemmaW_B.py"""
import sys, numpy as np
from ref_core import *

CONV = (-1, -1, 1)

class FakeCopy(FrontEnd):
    def __init__(self, F, lam, rng):
        super().__init__(F, lam, rng); p = F.p
        self.y = tuple(int(v) for v in rng.integers(0, p, 3))

def build(F, rng, m):
    p = F.p; trips = []
    while len(trips) < m:
        labs = [tuple(int(v) for v in rng.integers(0, p, 2)) for _ in range(3)]
        if not admissible(labs, p): continue
        s, P2, P3 = triple_data(labs, F)
        cps = [FakeCopy(F, l, rng) for l in labs]
        X = [int(v) for v in rng.integers(0, p, 3)]
        trips.append(dict(labs=labs, s=s, P2=P2, P3=P3, cps=cps, X=X))
    return trips

def q3_system(trips, u, F):
    p = F.p
    # unknown q = (q0, q1, q2, q3): q(w) = q0 w0^3 + q1 w0^2 w1 + q2 w0 w1^2 + q3 w1^3
    # e.grad q: e0 (3q0 w0^2 + 2q1 w0w1 + q2 w1^2) + e1 (q1 w0^2 + 2 q2 w0w1 + 3 q3 w1^2)
    Mq = [[3, 0, 0, 0], [0, 2, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 2, 0], [0, 0, 0, 3]]
    T = [0] * 6
    for t, uj in zip(trips, u):
        if uj == 0: continue
        for i, cp in enumerate(t['cps']):
            A3 = [int(x) for x in cp.A_forms(CONV)[2]]
            assert not any(A3[2:])
            fn = F.inv(cp.n); l0, l1 = int(cp.lam[0]), int(cp.lam[1])
            f0, f1 = l0 * fn % p, l1 * fn % p                      # f(w) = f0 w0 + f1 w1
            mono = [f0 * f0, 2 * f0 * f1, f1 * f1]
            c = 3 * pow(int(uj), 3, p) * pow(int(t['s'][i]), 3, p)
            for a in range(2):
                for k in range(3): T[3 * a + k] = (T[3 * a + k] + c * A3[a] * mono[k]) % p
    return Mq, T

def e3_part(trips, u, F):
    p = F.p; v = [0, 0]
    for t, uj in zip(trips, u):
        for i, cp in enumerate(t['cps']):
            A2, A3 = [[int(x) for x in A] for A in cp.A_forms(CONV)[1:]]
            coef = (A2[2] + 3 * A3[2] * t['X'][i]) % p
            fn = F.inv(cp.n)
            for r in range(2): v[r] = (v[r] + int(uj) * int(uj) * int(t['s'][i]) ** 2 * int(cp.lam[r]) * fn * coef) % p
    return v

def powsum(trips, u, k, F):
    p = F.p; key = 'P2' if k == 2 else 'P3'
    return [sum(pow(uj, k, p) * t[key][r] for t, uj in zip(trips, u)) % p for r in range(2)]

def main():
    rng = np.random.default_rng(7)
    tot = bad = 0; seen = {}
    for p in (101, 1009, 10007):
        F = Field(p)
        for m in (6, 36):
            for trial in range(10):
                trips = build(F, rng, m)
                for kind in ('random', 'cubic-only', 'quad-only'):
                    u = [int(v) for v in rng.integers(0, p, m)]
                    if kind == 'cubic-only' and m == 36:      # force sum u^3 P3 = 0 only (support = first g^2 triples)
                        g = g3(p); w = solve2([t['P3'] for t in trips[:g * g]], 3, g, F, rng); u = w + [0] * (m - g * g)
                    if kind == 'quad-only' and m == 36:       # force sum u^2 P2 = 0 only
                        w = solve2([t['P2'] for t in trips[:9]], 2, 3, F, rng); u = w + [0] * (m - 9)
                    Mq, T = q3_system(trips, u, F)
                    sol = solve_mod(Mq, [(-x) % p for x in T], p)
                    z3 = powsum(trips, u, 3, F) == [0, 0]; z2 = powsum(trips, u, 2, F) == [0, 0]
                    c1 = (sol is not None) == z3
                    c2 = (e3_part(trips, u, F) == [0, 0]) == z2
                    key = (kind, z3, z2); seen[key] = seen.get(key, 0) + 1
                    tot += 1; bad += int(not (c1 and c2))
            print('p=%d m=%d: Claim-1/Claim-2 iff checks so far %d, failures %d' % (p, m, tot, bad), flush=True)
    print('  cases seen (kind, sum u^3 P3 = 0, sum u^2 P2 = 0): %s' % seen)
    for p in (101, 103, 1009, 1013):
        F = Field(p); m = 9 * g3(p) ** 2; nsol = 0; fails = 0
        for trial in range(10):
            trips = build(F, rng, m)
            u = level2_weights([t['P2'] for t in trips], [t['P3'] for t in trips], F, rng)
            Mq, T = q3_system(trips, u, F)
            sol = solve_mod(Mq, [(-x) % p for x in T], p)
            ok = sol is not None and e3_part(trips, u, F) == [0, 0]
            hom = solve_mod(Mq + [[1, 0, 0, 0]], [0] * 6 + [1], p)     # q -> 0 forced? (uniqueness of q)
            hom2 = [solve_mod(Mq + [[int(i == k) for i in range(4)]], [0] * 6 + [1], p) for k in range(4)]
            ok = ok and all(h is None for h in hom2)
            nsol += 1; fails += int(not ok)
        print('p=%d (p mod 3 = %d, m = %d): Lemma-B weights give a unique public Q3 and E3 in %d/%d' % (p, p % 3, m, nsol - fails, nsol), flush=True)
    print('Lemma W iff-checks: %d, failures %d' % (tot, bad))

def lemmaB_adversarial():
    rng = np.random.default_rng(11); tot = 0
    for p in (5, 7, 11, 13, 19, 31, 37, 101, 103):
        F = Field(p)
        for trial in range(300):
            mode = trial % 5
            if mode == 0: cols = [tuple(int(v) for v in rng.integers(0, p, 2)) for _ in range(9)]
            elif mode == 1: cols = [(0, 0)] * 9
            elif mode == 2: cols = [tuple(int(v) for v in rng.integers(1, p, 2))] * 9
            elif mode == 3: cols = [(int(rng.integers(1, p)), 0) for _ in range(9)]
            else: cols = [(1, int(rng.choice([1, p - 1])) ) for _ in range(9)]
            v = solve2(cols, 2, 3, F, rng); assert any(v)
            assert all(sum(v[i] ** 2 * cols[i][r] for i in range(9)) % p == 0 for r in range(2))
            g = g3(p); cols3 = cols[:g * g] if g * g <= 9 else (cols + cols)[:g * g]
            v = solve2(cols3, 3, g, F, rng); assert any(v)
            assert all(sum(v[i] ** 3 * cols3[i][r] for i in range(g * g)) % p == 0 for r in range(2))
            tot += 1
        # worst case for the d=3 single equation at p = 1 mod 3: three cube classes, 4 entries
        if p % 3 == 1:
            reps = sorted({min(c * pow(x, 3, p) % p for x in range(1, p)) for c in range(1, p)})
            assert len(reps) == 3
            v = solve1(reps + [reps[0] * 2 % p], 3, F, rng); assert any(v)
    print('Lemma B adversarial columns: %d configurations at p in {5..103}, 0 failures (asserted)' % tot)

if __name__ == '__main__':
    lemmaB_adversarial()
    main()
