r"""Independent recomputation of the S1H exponent (referee, 2026-11-12).

Written from the definitions only (Lemmas S, F, Corollary HCD of the k8-attack note,
and the Schedule 1 shortened-depth rule of the core Outlook); the attack's scripts were
NOT read before this file produced its numbers.

Rule S1H(kappa, p), kappa | p-1, as a degree in a:
  e(1) = 1                                   (Gaussian elimination)
  S1t(kappa) = kappa * ceil(log2 t(p,kappa))  (Schedule 1 at L = ceil(log2 t) rounds)
  HCD plans (kappa even, D = kappa/2, inner node = best D-solver, degree e(D)):
     s >= 1 stages, each degree e(D); type after s stages has Tn_s (P-invariant set);
     finish F0 (0 in Tn_s): +0;  F2(D') for D' | kappa, D' < kappa: +e(D') if some
     shift r has r + D'Z_kappa inside classes(Tn_s \ 0)  (D' = 1 is F1, Gaussian).
  e(kappa) = min(S1t, plans).
Exponent E(c, p) = 1 + sum_{d=2}^{c} e(gcd(d, p-1)).

Also computes S1t-only (the "53" rule) as a control, and a variant without F2 (only F0/F1).
Exact set arithmetic for p <= PMAX; for p > PMAX a residue-class formula mod 5040
justified by Weil (see report).
"""
import sys, math, json
import numpy as np

def primes_upto(n):
    s = np.ones(n + 1, dtype=bool); s[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]: s[i * i::i] = False
    return [int(x) for x in np.nonzero(s)[0]]

def prim_root(p):
    fac = [q for q in primes_upto(int(p ** 0.5) + 1) if (p - 1) % q == 0]
    m = p - 1
    for q in list(fac):
        while m % q == 0: m //= q
    if m > 1: fac.append(m)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fac):
            return g

class Field:
    def __init__(self, p):
        self.p = p
        g = prim_root(p); self.g = g
        self.log = np.zeros(p, dtype=np.int64)
        x = 1
        for k in range(p - 1):
            self.log[x] = k; x = x * g % p
        self.pw = np.array([pow(g, k, p) for k in range(p - 1)], dtype=np.int64)

    def member(self, kappa, cls, zero):
        """boolean array over F_p for the P_kappa-invariant set (cls subset of Z_kappa)."""
        p = self.p
        m = np.zeros(p, dtype=bool)
        cl = self.log[1:] % kappa
        m[1:] = np.isin(cl, list(cls)) if cls else False
        m[0] = zero
        return m

    def sumset(self, kappa, A, B):
        """A, B = (frozenset classes, zero flag), P_kappa-invariant. Return A+B."""
        p = self.p
        mA = self.member(kappa, *A); mB = self.member(kappa, *B)
        ar = np.arange(p)
        cls = set()
        for j in range(kappa):
            eta = int(self.pw[j])  # g^j has class j
            if np.any(mA & mB[(eta - ar) % p]): cls.add(j)
        zero = bool(np.any(mA & mB[(-ar) % p]))
        return (frozenset(cls), zero)

_TC = {}
def t_len(F, kappa):
    """least t>=1 with a zero sum of t nonzero kappa-th powers (t>=2)."""
    if kappa == 1: return 2
    if (F.p, kappa) in _TC: return _TC[(F.p, kappa)]
    _TC[(F.p, kappa)] = _t_len(F, kappa); return _TC[(F.p, kappa)]

def _t_len(F, kappa):
    P = (frozenset([0]), False)
    S = P; t = 1
    while True:
        S = F.sumset(kappa, S, P); t += 1
        if S[1]: return t
        if t > kappa + 1: raise RuntimeError("Chevalley-Warning violated?")

def S1t_deg(F, kappa):
    if kappa == 1: return 1
    return kappa * math.ceil(math.log2(t_len(F, kappa)))

def divisors(n): return [d for d in range(1, n + 1) if n % d == 0]

def e_table(F, kmax=9, allow_F2=True, hcd=True, smax=4, prefer_hcd=False):
    p = F.p
    e = {}; plan = {}
    for kappa in range(1, kmax + 1):
        if (p - 1) % kappa: continue
        if kappa == 1:
            e[1] = 1; plan[1] = 'GE'; continue
        best = S1t_deg(F, kappa); bp = 'S1t'
        if hcd and kappa % 2 == 0:
            D = kappa // 2
            cl_m1 = ((p - 1) // 2) % kappa
            cl_eps = (cl_m1 - D) % kappa   # eps = -1/q, q in Q_D
            Tn = (frozenset([0]), False)   # columns: Tn = P
            for s in range(1, smax + 1):
                shifted = (frozenset((c + cl_eps) % kappa for c in Tn[0]), Tn[1])
                ss = F.sumset(kappa, Tn, shifted)
                Tn = (Tn[0] | shifted[0] | ss[0], Tn[1] or shifted[1] or ss[1])
                base = s * e[D]
                if base > best or (base == best and not prefer_hcd): break
                cands = []
                if Tn[1]: cands.append((base, f'{s}xHCD+F0'))
                for Dp in divisors(kappa):
                    if Dp == kappa: continue
                    if Dp > 1 and not allow_F2: continue
                    sub = set(range(0, kappa, Dp))
                    if any(all(((x + r) % kappa) in Tn[0] for x in sub) for r in range(kappa)):
                        cands.append((base + e[Dp], f'{s}xHCD+F{"1" if Dp==1 else "2(%d)"%Dp}'))
                for c, name in cands:
                    if c < best or (prefer_hcd and c == best and bp == 'S1t'): best, bp = c, name
        e[kappa] = best; plan[kappa] = bp
    return e, plan

def exponents(p, e, cmax=9):
    out = {}
    for c in range(2, cmax + 1):
        if p <= c: continue
        out[c] = 1 + sum(e[math.gcd(d, p - 1)] for d in range(2, c + 1))
    return out

def large_p_formula(r):
    """e table at a prime p > PMAX with p = r mod 5040 (Weil regime)."""
    pm1 = (r - 1) % 5040  # p-1 mod 5040; 2^4 | 5040 suffices for parities of (p-1)/kappa, kappa<=9
    e = {}
    for kappa in range(1, 10):
        if pm1 % kappa: continue
        if kappa == 1: e[1] = 1; continue
        t = 2 if ((pm1 // kappa) % 2 == 0) else 3
        s1t = kappa * math.ceil(math.log2(t))
        best = s1t
        if kappa % 2 == 0: best = min(best, e[kappa // 2] + 1)
        e[kappa] = best
    return e

if __name__ == '__main__':
    PMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 30000
    res = {'S1H': {}, 'S1t': {}, 'S1H_noF2': {}}
    worst = {k: {} for k in res}
    disagree = []
    for p in primes_upto(PMAX):
        if p < 3: continue
        F = Field(p)
        eH, plH = e_table(F)
        eT, _ = e_table(F, hcd=False)
        eN, _ = e_table(F, allow_F2=False)
        for name, ee in (('S1H', eH), ('S1t', eT), ('S1H_noF2', eN)):
            ex = exponents(p, ee)
            for c, v in ex.items():
                w = worst[name].get(c)
                if w is None or v > w[0]: worst[name][c] = [v, [p]]
                elif v == w[0] and len(w[1]) < 8: w[1].append(p)
        # consistency with the large-p formula where Weil thresholds hold
        if p > 26244:
            ef = large_p_formula(p % 5040)
            if any(ef[k] != eH[k] for k in eH): disagree.append((p, eH, ef))
        if p in (41, 2521, 1801, 13, 17, 73, 37):
            print(p, 'S1H e:', eH, plH, 'S1t e:', eT, flush=True)
    print('exact-range worst (p <= %d):' % PMAX)
    for name in worst:
        print(' ', name, {c: worst[name][c] for c in sorted(worst[name])})
    print('formula/exact disagreements above 26244:', len(disagree), disagree[:3])
    # residue classes mod 5040 for p > PMAX
    tail = {}
    for r in range(1, 5040):
        if math.gcd(r, 5040) != 1: continue
        ef = large_p_formula(r)
        for c in range(2, 10):
            v = 1 + sum(ef[math.gcd(d, (r - 1) % 5040 or 5040)] for d in range(2, c + 1))
            if c not in tail or v > tail[c][0]: tail[c] = [v, [r]]
            elif v == tail[c][0]: tail[c][1].append(r)
    print('tail (all units mod 5040):', {c: (tail[c][0], tail[c][1][:4], len(tail[c][1])) for c in tail})
    json.dump({'worst': worst, 'tail': {c: [tail[c][0], tail[c][1]] for c in tail}},
              open(__file__.replace('.py', '.json'), 'w'), indent=1)
