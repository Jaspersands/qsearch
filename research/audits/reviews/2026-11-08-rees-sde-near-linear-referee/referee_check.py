"""Independent referee checks for 2026-11-08-rees-sde-near-linear.md (Theorem H etc.).
Written from scratch; shares no code with the author's scripts. Exact integer arithmetic.

A. Wrong-key statistics (step (v)): for random theta, i.i.d. uniform queries c_1..c_m, list
   EVERY (K, sigma) consistent with the pattern by scanning all K in F_p.  By the
   parametrisation, these are exactly the keys any SDE solver can hand back, so the
   frequency of "some wrong K consistent" is the exact failure event of Theorem H.
   Compared with the union bound kappa(p-1)(1/kappa+1/(p-1))^m.
B. Column-language construction + own nullspace + full kernel enumeration on tiny
   instances; exact count of P0-solutions vs. the count predicted from A's (K, sigma) list;
   dead pairs unused; negative control with a LIVE pair (-c in P).
C. Shift symmetry (Corollary H2): bank built from pattern eps and from eps+tau have the
   same kernel; at p >= m^2 kappa^(2m) both sigma = 0 and sigma != 0 solution sets are
   nonempty, so a worst-case solver may always return a shifted solution.
D. kappa = 3 dead weight above density 2 at a small prime: exhaustive search for a
   5-column bank in F_7^2 with no nonzero P0-solution (paper states N(3,2,7) = 5).
"""
import random, itertools, math, sys

def primroot(p):
    n, fac, q = p - 1, [], 2
    while q * q <= n:
        if n % q == 0:
            fac.append(q)
            while n % q == 0: n //= q
        q += 1
    if n > 1: fac.append(n)
    return next(g for g in range(2, p) if all(pow(g, (p - 1) // f, p) != 1 for f in fac))

def coset_table(p, kap):
    g = primroot(p); t = [None] * p; y = 1
    for e in range(p - 1):
        t[y] = e % kap; y = y * g % p
    return g, t

def is_prime(n):
    return n > 1 and all(n % q for q in range(2, int(n ** .5) + 1))

def next_prime_1mod(n, kap):
    while not (is_prime(n) and n % kap == 1): n += 1
    return n

def consistent_keys(p, kap, cos, c, eps):
    """all (K, sigma): for every i, K == -c_i or cos(K+c_i) - eps_i == -sigma (mod kap)."""
    out = []
    for K in range(p):
        sig = None; ok = True
        for ci, ei in zip(c, eps):
            y = (K + ci) % p
            if y == 0: continue
            s = (ei - cos[y]) % kap
            if sig is None: sig = s
            elif s != sig: ok = False; break
        if ok: out.append((K, sig))
    return out

# ---------------- A ----------------
def part_A(rng):
    print("== A: exact wrong-key frequency vs union bound ==")
    for kap, p0, lam, trials in [(2, 2000, 1, 400), (2, 2000, 3, 400), (3, 3000, 1, 300),
                                 (3, 3000, 2, 300), (4, 3000, 1, 300), (2, 20000, 2, 150)]:
        p = next_prime_1mod(p0, kap); g, cos = coset_table(p, kap)
        m = math.ceil(math.log(p, kap) - 1e-12) + lam
        bad = 0; zero_hit = 0; allequal = 0; n = 0
        for _ in range(trials):
            th = rng.randrange(p); c = [rng.randrange(p) for _ in range(m)]
            if any((th + ci) % p == 0 for ci in c): zero_hit += 1; continue
            n += 1
            eps = [cos[(th + ci) % p] for ci in c]
            if len(set(eps)) == 1: allequal += 1
            keys = consistent_keys(p, kap, cos, c, eps)
            assert (th, 0) in keys
            if any(K != th for K, _ in keys): bad += 1
        ub = kap * (p - 1) * (1 / kap + 1 / (p - 1)) ** m
        print(f"kap={kap} p={p} lam={lam} m={m}: trials={n} zero_hits={zero_hit} "
              f"Pr[wrong key consistent]={bad / n:.4f} union_bound={ub:.4f} 2kap^(1-lam)={2 * kap ** (1 - lam):.4f} "
              f"Pr[all eps equal]={allequal / n:.4f} exact={kap ** (1 - m):.2e}")

# ---------------- linear algebra ----------------
def rref_null(rows, p, n):
    """basis of {x in F_p^n : R x = 0}."""
    R = [r[:] for r in rows]; piv = []; r = 0
    for col in range(n):
        pr = next((i for i in range(r, len(R)) if R[i][col] % p), None)
        if pr is None: continue
        R[r], R[pr] = R[pr], R[r]
        inv = pow(R[r][col], p - 2, p); R[r] = [v * inv % p for v in R[r]]
        for i in range(len(R)):
            if i != r and R[i][col] % p:
                f = R[i][col]; R[i] = [(a - f * b) % p for a, b in zip(R[i], R[r])]
        piv.append(col); r += 1
        if r == len(R): break
    free = [j for j in range(n) if j not in piv]; basis = []
    for f in free:
        v = [0] * n; v[f] = 1
        for i, pc in enumerate(piv): v[pc] = (-R[i][f]) % p
        basis.append(v)
    return basis

# ---------------- B ----------------
def build_bank(p, kap, g, cos, c, eps, k, live=False):
    """columns: hard block in F_p^{m-2} with relation space span(u, w); k pairs (e_j, c_pair e_j)."""
    m = len(c)
    u = [pow(g, (kap - e) % kap, p) for e in eps]          # u_i in g^{-eps_i} P
    w = [ui * ci % p for ui, ci in zip(u, c)]
    H = rref_null([u, w], p, m)                            # rows of H: basis of span(u,w)^perp
    assert len(H) == m - 2
    a = m - 2 + k; M = m + 2 * k
    # pair ratio: column (mu, cp*mu); dead iff -cp notin P.  pick cp = -g (dead) or -1 (live: -cp=1 in P)
    cp = (-g) % p if not live else p - 1
    Lam = [[0] * M for _ in range(a)]
    for r in range(m - 2):
        for i in range(m): Lam[r][i] = H[r][i]
    for j in range(k):
        Lam[m - 2 + j][m + 2 * j] = 1; Lam[m - 2 + j][m + 2 * j + 1] = cp
    return Lam, a, M

def part_B(rng):
    print("== B: column-language bank, own nullspace, full kernel enumeration ==")
    for kap, p, m, k, reps in [(2, 29, 6, 2, 3), (2, 41, 7, 1, 3), (3, 37, 5, 2, 3), (4, 37, 5, 2, 2), (6, 37, 4, 2, 2)]:
        g, cos = coset_table(p, kap)
        P0 = set(y for y in range(1, p) if cos[y] == 0) | {0}
        for live in (False, True):
            for _ in range(reps):
                while True:
                    th = rng.randrange(p); c = [rng.randrange(p) for _ in range(m)]
                    if all((th + ci) % p for ci in c) and len(set(c)) > 1: break
                eps = [cos[(th + ci) % p] for ci in c]
                Lam, a, M = build_bank(p, kap, g, cos, c, eps, k, live)
                B = rref_null(Lam, p, M); assert len(B) == M - a == k + 2
                sols = 0; uses_pair = 0
                for coef in itertools.product(range(p), repeat=len(B)):
                    if not any(coef): continue
                    x = [sum(cf * b[i] for cf, b in zip(coef, B)) % p for i in range(M)]
                    if all(xi in P0 for xi in x):
                        assert all(sum(Lam[r][i] * x[i] for i in range(M)) % p == 0 for r in range(a))
                        sols += 1
                        if any(x[m:]): uses_pair += 1
                keys = consistent_keys(p, kap, cos, c, eps)
                pred = len(keys) * (p - 1) // kap + ((p - 1) // kap if len(set(eps)) == 1 else 0)
                tag = "LIVE-pair control" if live else "dead pairs"
                print(f"kap={kap} p={p} m={m} k={k} a={a} M={M} {tag}: P0-solutions={sols} "
                      f"using_pairs={uses_pair} predicted_block_only={pred} keys={sorted(K for K,_ in keys)} theta={th}")
                if not live: assert uses_pair == 0 and sols == pred
                else: assert uses_pair > 0

# ---------------- C ----------------
def part_C(rng):
    print("== C: shift symmetry of the bank (Corollary H2) ==")
    for kap, m in [(2, 6), (3, 4)]:
        p = next_prime_1mod(m * m * kap ** (2 * m) + 1, kap); g, cos = coset_table(p, kap)
        for _ in range(3):
            c = [rng.randrange(p) for _ in range(m)]; eps = [rng.randrange(kap) for _ in range(m)]
            ks = consistent_keys(p, kap, cos, c, eps)
            by = [sum(1 for _, s in ks if s == t) for t in range(kap)]
            # same kernel for eps and eps+1: u' = g^{-1} u, w' = g^{-1} w
            u = [pow(g, (kap - e) % kap, p) for e in eps]; u2 = [pow(g, (kap - (e + 1) % kap) % kap, p) for e in eps]
            ratio = set(u2[i] * pow(u[i], p - 2, p) % p for i in range(m))
            same = len(set(cos[r] for r in ratio)) == 1   # all ratios in one coset g^{-1}P
            print(f"kap={kap} m={m} p={p}: #K by shift sigma=0..{kap-1}: {by}; "
                  f"u(eps+1)/u(eps) in a single coset (banks equal after P-rescaling of columns): {same}")

# ---------------- D ----------------
def part_D():
    print("== D: kappa=3 dead weight of density 5/2 at p=7 ==")
    p, kap = 7, 3; g, cos = coset_table(p, kap)
    P = [y for y in range(1, p) if cos[y] == 0]; P0 = [0] + P
    vecs = [(x, y) for x in range(p) for y in range(p) if (x, y) != (0, 0)]
    # classes up to scaling by P
    reps = []; seen = set()
    for v in vecs:
        if v in seen: continue
        reps.append(v)
        for s in P: seen.add((v[0] * s % p, v[1] * s % p))
    sums = {}
    def dead(bank):
        for x in itertools.product(P0, repeat=len(bank)):
            if not any(x): continue
            if all(sum(xi * b[j] for xi, b in zip(x, bank)) % p == 0 for j in range(2)): return False
        return True
    found = None; count = 0
    for bank in itertools.combinations_with_replacement(reps, 5):
        if dead(bank):
            count += 1
            if found is None: found = bank
    print(f"p=7 kappa=3: #dead 5-column banks in F_7^2 (columns up to P-scaling, multisets) = {count}; example {found}")

if __name__ == "__main__":
    rng = random.Random(20261108)
    part = sys.argv[1] if len(sys.argv) > 1 else "ABCD"
    if "A" in part: part_A(rng)
    if "B" in part: part_B(rng)
    if "C" in part: part_C(rng)
    if "D" in part: part_D()
