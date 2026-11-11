#!/usr/bin/env python
"""End-to-end classical simulation of the finite-index HSP reduction in UT_n(Z).

2026-11-12, Claude Code helper.  AI-checked, pending human review.
Run:  nice -n 19 /opt/anaconda3/bin/python utz_e2e_check.py [trials_per_config] [index_cap] [prod|lcm]

What it does, per random instance (n, M0):
  * Build a hidden H <= UT_n(Z) of finite index as the preimage of a random
    subgroup H0 = prod_q H0_q of UT_n(Z/M0), M0 = prod q^a.  The hiding function
    f(x) is a canonical left-coset label of (x mod M0) H0 (opaque to the
    algorithm, which never sees M0 or H0).
  * Run the reduction of the claim, with brute force in place of the quantum
    subroutines:
      1. periods e_ij = least t >= 1 with f(I + t E_ij) = f(I)  (stands in for Shor);
      2. N' = prod e_ij, M = (n-1)! N';
      3. CRT split of UT_n(Z/M); on each q^k factor, f_q(u) = f(lift(iota_q(u)));
         a coset-BFS + Schreier-generator solver (oracle-only, classical) stands
         in for Cor. cor:black-box-pe (q > n-1) / Imran-Ivanyos Thm 1 (q <= n-1);
      4. output = lifts of iota_q(gens of Hbar_q) together with I + M E_ij.
  * Check independently (with the hidden data, which the algorithm never uses):
      N | N', e_ij <= N, Gamma(M) <= H (generators and random elements),
      g^N in Core(H) (random g, all coset reps), output <= H, and
      [G : <output>] = [G : H] computed by a polycyclic sifting of the output mod
      lcm(M, M0); together these give <output> = H.
  * Control: M_ctrl = N' (no (n-1)!) and records how often Gamma(N') is NOT in H.

Self-test first: the sifting code (induced pcgs) is compared with brute-force
closure on small groups.  Finite checks only falsify (TRAPS 7).
"""
import itertools, math, random, sys
MODE = 'prod'
from collections import deque

# ---------------------------------------------------------------- matrices
# An element of UT_n(R) is a tuple of the m = n(n-1)/2 entries (i<j), row-major.

def idx_list(n):
    return [(i, j) for i in range(n) for j in range(i + 1, n)]

class UT:
    def __init__(self, n, mod):  # mod = None means Z
        self.n, self.mod = n, mod
        self.pos = idx_list(n)
        self.m = len(self.pos)
        self.ix = {p: k for k, p in enumerate(self.pos)}
        # Mal'cev order: by level j-i, then by i
        self.malcev = sorted(self.pos, key=lambda p: (p[1] - p[0], p[0]))
        self.one = tuple([0] * self.m)

    def red(self, a):
        return tuple(x % self.mod for x in a) if self.mod else tuple(a)

    def mul(self, a, b):
        n, ix = self.n, self.ix
        out = []
        for (i, j) in self.pos:
            s = a[ix[(i, j)]] + b[ix[(i, j)]]
            for k in range(i + 1, j):
                s += a[ix[(i, k)]] * b[ix[(k, j)]]
            out.append(s)
        return self.red(out)

    def inv(self, a):
        # solve a*b = I level by level: b_ij = -a_ij - sum_{i<k<j} a_ik b_kj
        n, ix = self.n, self.ix
        b = [0] * self.m
        for d in range(1, n):
            for i in range(n - d):
                j = i + d
                s = -a[ix[(i, j)]]
                for k in range(i + 1, j):
                    s -= a[ix[(i, k)]] * b[ix[(k, j)]]
                b[ix[(i, j)]] = s % self.mod if self.mod else s
        return tuple(b)

    def pw(self, a, e):
        if e < 0:
            a, e = self.inv(a), -e
        r, base = self.one, a
        while e:
            if e & 1:
                r = self.mul(r, base)
            base = self.mul(base, base)
            e >>= 1
        return r

    def elem(self, p, t):  # I + t E_p  = x_p^t
        a = [0] * self.m
        a[self.ix[p]] = t
        return self.red(a)

    def comm(self, a, b):
        return self.mul(self.mul(self.inv(a), self.inv(b)), self.mul(a, b))

    def malcev_coords(self, a):
        """t with a = prod_{p in malcev order} x_p^{t_p}."""
        t = {}
        cur = a
        for p in self.malcev:
            c = cur[self.ix[p]]
            if self.mod:
                c %= self.mod
            t[p] = c
            # cur <- x_p^{-c} * cur ; x_p^{-c} only changes entries at >= level
            cur = self.mul(self.elem(p, -c), cur)
        return [t[p] for p in self.malcev]

# ---------------------------------------------------------------- pcgs sifting
class PcgsTable:
    """Induced polycyclic sequence of a subgroup K of UT_n(Z/q^k), in echelon form
    along the Mal'cev series (coordinate i, then q-adic valuation)."""

    def __init__(self, G, q, k):
        self.G, self.q, self.k, self.Q = G, q, k, q ** k
        self.tab = {}  # coordinate index -> (element, valuation)

    def val(self, c):
        v = 0
        while c % self.q == 0 and v < self.k:
            c //= self.q
            v += 1
        return v

    def lead(self, g):
        t = self.G.malcev_coords(g)
        for i, c in enumerate(t):
            if c % self.Q:
                return i, c % self.Q
        return None, 0

    def normalize(self, g, i, c):
        v = self.val(c)
        u = c // self.q ** v
        uinv = pow(u, -1, self.Q)
        return self.G.pw(g, uinv), v

    def sift(self, g):
        """Right-multiply by table elements to clear leading coordinates.
        Returns residue (identity iff g in <table>, once the table is closed)."""
        G = self.G
        while True:
            i, c = self.lead(g)
            if i is None:
                return g
            if i not in self.tab:
                return g
            T, v = self.tab[i]
            if c % self.q ** v:
                return g
            g = G.mul(g, G.pw(T, -(c // self.q ** v)))

    def add_gens(self, gens):
        G, q = self.G, self.q
        queue = deque(gens)
        while queue:
            g = self.sift(queue.popleft())
            i, c = self.lead(g)
            if i is None:
                continue
            g, v = self.normalize(g, i, c)
            if i in self.tab:
                old, vo = self.tab[i]
                assert v < vo
                self.tab[i] = (g, v)
                queue.append(old)
            else:
                self.tab[i] = (g, v)
            # refined pcgs: g, g^q, ..., g^(q^(k-v-1)); the power leaving G_i must sift,
            # and commutators of all refined elements must sift.
            queue.append(G.pw(g, q ** (self.k - v)))
            gpows = [G.pw(g, q ** a) for a in range(self.k - v)]
            for (T, vt) in list(self.tab.values()):
                tpows = [G.pw(T, q ** b) for b in range(self.k - vt)]
                for u in gpows:
                    for w in tpows:
                        queue.append(G.comm(u, w))
        return self

    def log_order(self):  # log_q |K|
        return sum(self.k - v for (_, v) in self.tab.values())

    def log_index(self):  # log_q [UT_n(Z/q^k) : K]
        return self.G.m * self.k - self.log_order()

    def canon_left_coset(self, x):
        """Canonical representative of x K: clear coordinate i to [0, q^v)."""
        G = self.G
        g = x
        t = G.malcev_coords(g)
        for i in range(G.m):
            t = G.malcev_coords(g)
            c = t[i]
            if i in self.tab:
                T, v = self.tab[i]
                s = c // self.q ** v
                if s:
                    g = G.mul(g, G.pw(T, -s))
        return g

    def member(self, x):
        return self.sift(x) == self.G.one

# ---------------------------------------------------------------- helpers
def factor(N):
    f, d = {}, 2
    while d * d <= N:
        while N % d == 0:
            f[d] = f.get(d, 0) + 1
            N //= d
        d += 1
    if N > 1:
        f[N] = f.get(N, 0) + 1
    return f

def crt_embed(a_mod_qk, qk, M):
    """iota_q: UT(Z/q^k) -> UT(Z/M), entries == a mod q^k and == 0 (identity) mod M/q^k."""
    R = M // qk
    # x == a (mod qk), x == 0 (mod R)
    inv = pow(R, -1, qk)
    return tuple((a * R * inv) % M for a in a_mod_qk)

def closure_size(G, gens):
    seen = {G.one}
    frontier = [G.one]
    while frontier:
        new = []
        for x in frontier:
            for g in gens:
                y = G.mul(x, g)
                if y not in seen:
                    seen.add(y)
                    new.append(y)
        frontier = new
    return len(seen), seen

# ---------------------------------------------------------------- self test
def self_test(rng):
    bad = 0
    tests = 0
    for (n, q, k) in [(4, 2, 2), (4, 3, 1), (3, 2, 3), (4, 2, 1), (3, 5, 1), (3, 3, 2), (5, 2, 1), (4, 3, 2), (5, 3, 1)]:
        G = UT(n, q ** k)
        for _ in range(6):
            gens = [tuple(rng.randrange(q ** k) * (q ** rng.randrange(k + 1) if rng.random() < .5 else 1) % q ** k
                          for _ in range(G.m)) for _ in range(rng.randint(1, 3))]
            size, S = closure_size(G, gens)
            T = PcgsTable(G, q, k).add_gens(gens)
            tests += 1
            if q ** T.log_order() != size:
                bad += 1
                continue
            # canonical coset reps: equal iff same coset (sample)
            elems = list(S)
            for _ in range(40):
                x = tuple(rng.randrange(q ** k) for _ in range(G.m))
                h = rng.choice(elems)
                if T.canon_left_coset(x) != T.canon_left_coset(G.mul(x, h)):
                    bad += 1
                    break
                y = tuple(rng.randrange(q ** k) for _ in range(G.m))
                same = G.mul(G.inv(x), y) in S
                if (T.canon_left_coset(x) == T.canon_left_coset(y)) != same:
                    bad += 1
                    break
    return tests, bad

# ---------------------------------------------------------------- instance
class Instance:
    def __init__(self, n, M0, rng):
        self.n, self.M0 = n, M0
        self.GZ = UT(n, None)
        self.parts = []  # (q, a, G_q, table)
        logN = 0
        self.N = 1
        for q, a in factor(M0).items():
            Gq = UT(n, q ** a)
            gens = []
            for _ in range(rng.randint(2, 5)):
                g = [rng.randrange(q ** a) for _ in range(Gq.m)]
                if rng.random() < 0.3:  # thin it out to get non-trivial index
                    g = [(x * q ** rng.randrange(a + 1)) % q ** a for x in g]
                gens.append(tuple(g))
            T = PcgsTable(Gq, q, a).add_gens(gens)
            self.parts.append((q, a, Gq, T))
            self.N *= q ** T.log_index()
        self.queries = 0

    def f(self, x):  # x: integer matrix (tuple); label of left coset x H
        self.queries += 1
        lab = []
        for (q, a, Gq, T) in self.parts:
            lab.append(T.canon_left_coset(Gq.red(x)))
        return tuple(lab)

# ---------------------------------------------------------------- the reduction
def run_reduction(inst, use_factorial=True, rng=None):
    n, GZ = inst.n, inst.GZ
    fI = inst.f(GZ.one)
    # 1. periods (brute force stands in for Shor; bound N <= 2^b is not used here)
    per = {}
    for p in GZ.pos:
        t = 1
        while inst.f(GZ.elem(p, t)) != fI:
            t += 1
        per[p] = t
    Np = math.prod(per.values())
    if MODE == 'lcm':  # simplified reduction: Gamma(M) = <x_ij^M>, so M = lcm(e_ij) suffices
        M = math.lcm(*per.values())
    else:              # the claim as stated in application-search-3: M = (n-1)! prod e_ij
        M = (math.factorial(n - 1) if use_factorial else 1) * Np
    # 2-3. CRT split and per-prime solver
    out = []
    for q, k in factor(M).items():
        qk = q ** k
        Gq = UT(n, qk)
        def fq(u):
            return inst.f(crt_embed(u, qk, M))  # lift: entries in [0, M)
        base = fq(Gq.one)
        gens = [Gq.elem(p, 1) for p in GZ.pos]
        # coset BFS: reps[label] = representative
        reps = {base: Gq.one}
        dq = deque([Gq.one])
        schreier = []
        while dq:
            r = dq.popleft()
            for s in gens:
                rs = Gq.mul(r, s)
                lab = fq(rs)
                if lab not in reps:
                    reps[lab] = rs
                    dq.append(rs)
                else:
                    schreier.append(Gq.mul(Gq.inv(reps[lab]), rs))
        # the Schreier generators generate Hbar_q (Schreier's lemma)
        Hq = PcgsTable(Gq, q, k).add_gens(schreier)
        assert q ** Hq.log_index() == len(reps), "BFS index != pcgs index"
        for (T, _) in Hq.tab.values():
            out.append(crt_embed(T, qk, M))
    out += [GZ.elem(p, M) for p in GZ.pos]
    return per, Np, M, out

def check_instance(inst, per, Np, M, out, rng):
    GZ, n = inst.GZ, inst.n
    fI = inst.f(GZ.one)
    res = {}
    res['N|Np'] = (Np % inst.N == 0)
    res['Gamma(lcm e)<=H'] = gamma_in_H(inst, math.lcm(*per.values()), rng)
    res['e<=N'] = all(e <= inst.N for e in per.values())
    # Gamma(M) <= H
    ok = all(inst.f(GZ.elem(p, M)) == fI for p in GZ.pos)
    for _ in range(30):
        A = [M * rng.randrange(-50, 50) for _ in range(GZ.m)]
        ok &= inst.f(tuple(A)) == fI
    res['Gamma(M)<=H'] = ok
    # N1: g^N in Core(H): g^N fixes every coset y H (y over all coset reps of H)
    reps = []
    for (q, a, Gq, T) in inst.parts:
        pass
    ok = True
    for _ in range(10):
        g = tuple(rng.randrange(-5, 6) for _ in range(GZ.m))
        gN = GZ.pw(g, inst.N)
        for _ in range(15):
            y = tuple(rng.randrange(-20, 21) for _ in range(GZ.m))
            ok &= inst.f(GZ.mul(y, gN)) == inst.f(y)
    res['g^N in Core'] = ok
    # output <= H
    res['out<=H'] = all(inst.f(g) == fI for g in out)
    # index of <out> via sifting mod L = lcm(M, M0)
    L = M * inst.M0 // math.gcd(M, inst.M0)
    logidx = 1
    for q, k in factor(L).items():
        Gq = UT(n, q ** k)
        T = PcgsTable(Gq, q, k).add_gens([Gq.red(g) for g in out])
        logidx *= q ** T.log_index()
    res['[G:<out>]=N'] = (logidx == inst.N)
    return res

def gamma_in_H(inst, M, rng):
    GZ = inst.GZ
    fI = inst.f(GZ.one)
    if not all(inst.f(GZ.elem(p, M)) == fI for p in GZ.pos):
        return False
    for _ in range(30):
        A = [M * rng.randrange(-50, 50) for _ in range(GZ.m)]
        if inst.f(tuple(A)) != fI:
            return False
    return True

def main():
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    global NCAP, MODE
    NCAP = int(sys.argv[2]) if len(sys.argv) > 2 else 1500
    MODE = sys.argv[3] if len(sys.argv) > 3 else 'prod'
    print(f"mode: {MODE} (prod: M = (n-1)! prod e_ij; lcm: M = lcm e_ij)", flush=True)
    rng = random.Random(20261112)
    t, b = self_test(rng)
    print(f"self-test (pcgs order vs closure, canonical cosets): {t} subgroups, {b} failures", flush=True)
    configs = [(3, 4), (3, 6), (3, 12), (4, 4), (4, 6), (4, 8), (4, 9), (4, 10), (4, 12), (4, 30),
               (4, 15), (4, 25), (5, 6), (5, 10), (5, 4)]
    tot = 0
    fails = {}
    ctrl_bad = 0
    ctrl_tot = 0
    nontriv = 0
    maxM = 0
    for (n, M0) in configs:
        cfails = 0
        for _ in range(trials):
            for _att in range(200):
                inst = Instance(n, M0, rng)
                if 1 < inst.N <= NCAP:
                    break
            else:
                continue
            nontriv += 1
            per, Np, M, out = run_reduction(inst, True, rng)
            maxM = max(maxM, M)
            res = check_instance(inst, per, Np, M, out, rng)
            tot += 1
            for kk, v in res.items():
                if not v:
                    fails[kk] = fails.get(kk, 0) + 1
                    cfails += 1
            ctrl_tot += 1
            if not gamma_in_H(inst, Np, rng):
                ctrl_bad += 1
        print(f"n={n} M0={M0}: done, failures in this config: {cfails}", flush=True)
    print(f"instances with N>1: {tot}; check failures: {fails if fails else 0}")
    print(f"largest M used (mode {MODE}): {maxM}")
    print(f"control M_ctrl = N' (no (n-1)!): Gamma(N') not inside H in {ctrl_bad}/{ctrl_tot} instances")

if __name__ == '__main__':
    main()
