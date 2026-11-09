"""Falsifier hunt for research/REES_MIXED_SPECTRAL_SOURCE.md, sections 2-4, 6, 7.

Item 8 of REES_FULL_CAMPAIGN_2.md. Exact rational arithmetic where the claim is
combinatorial (grid, compression, margin, rank identity, tail bound); float checks
(numpy, tolerance 1e-9) where it needs eigenvalues, wedges or trace distances.
"""
import bisect, itertools, math, random
from fractions import Fraction as Fr
import numpy as np

rng = random.Random(20261102)
nrng = np.random.default_rng(20261102)
fails = 0
def check(cond, msg):
    global fails
    if not cond:
        fails += 1
        if fails < 20:
            print("FAIL", msg)

def floor_fr(x):
    return x.numerator // x.denominator

# ---------------------------------------------------------------- section 2 (exact)
def grid(delta, R, beta):
    w = delta / (16 * R)
    J = math.ceil(1 / w)
    M = 1
    while M < 8 * R / beta:
        M *= 2
    return w, J, M

def rand_spectrum(R):
    # rational spectrum, rank <= R, with deliberately tiny gaps and tails
    k = rng.randint(1, R)
    raw = [Fr(rng.randint(1, 50)) for _ in range(k)]
    if k >= 2 and rng.random() < 0.5:
        raw[1] = raw[0] + Fr(1, 2 ** 40)          # tiny internal gap
    if rng.random() < 0.3:
        raw[-1] = Fr(1, 2 ** 40)                   # tiny tail
    s = sum(raw)
    return [x / s for x in raw]

ncomp = 0
for trial in range(60):
    R = rng.randint(1, 4)
    lam = rand_spectrum(R)
    delta = Fr(rng.randint(25, 100), 100)
    beta = Fr(1, rng.choice([2, 8]))
    w, J, M = grid(delta, R, beta)
    for a in range(M):
        t = [w * (1 + Fr(a, M) + j) for j in range(J)]
        B = []
        for l in lam:
            b = w * bisect.bisect_right(t, l)
            b_formula = w * max(0, floor_fr(l / w - Fr(a, M)))
            check(b == b_formula, f"b formula lam={l} a={a}")
            check(0 <= l - b < 2 * w, f"compression lam={l}")
            B.append(b)
            ncomp += 1
        e = sum(l - b for l, b in zip(lam, B))
        check(0 <= e < 2 * R * w == delta / 8, "e bound")
print("sec 2: compression identities exact on", ncomp, "(eigenvalue, offset) pairs")

# ---------------------------------------------------------------- section 4 (exact)
nbad_max = 0
for trial in range(300):
    R = rng.randint(1, 8)
    lam = rand_spectrum(R)
    delta = Fr(rng.randint(5, 100), 100); beta = Fr(1, 8)
    w, J, M = grid(delta, R, beta)
    Delta = w / (4 * M)
    bad = set()
    for l in lam:
        hits = 0
        for a in range(M):
            j0 = floor_fr(l / w - 1 - Fr(a, M))
            if any(0 <= j < J and abs(l - w * (1 + Fr(a, M) + j)) < Delta for j in (j0, j0 + 1)):
                hits += 1; bad.add(a)
        check(hits <= 1, f"eigenvalue near thresholds for {hits} offsets")
    check(len(bad) <= R and Fr(len(bad), M) <= beta / 8, "bad offset fraction")
    nbad_max = max(nbad_max, len(bad))
print("sec 4: each eigenvalue spoils at most one offset; max bad offsets seen", nbad_max)

# ---------------------------------------------------------------- section 6 (exact)
for trial in range(300):
    R = rng.randint(1, 8)
    lam = rand_spectrum(R)
    for tt in [Fr(rng.randint(1, 999), 1000) for _ in range(5)]:
        E = sum(l * (1 / l if l >= tt else 0) for l in lam)
        check(E == sum(1 for l in lam if l >= tt), "rank identity")
# bias budget: h = min(Delta/2, w^2/128), kappa = zeta = w/128
for w in [Fr(1, k) for k in (2, 3, 16, 100, 2 ** 20)]:
    h = w * w / 128
    recip = 2 * h / w ** 2           # |1/Y - 1/lambda| <= h/(lambda (lambda-h)) <= 2h/w^2 when h <= w/2
    check(h <= w / 2 and recip + (w / 128 + w / 128) / w == Fr(1, 32), "bias 1/32")
    # Hoeffding: range 1/w, deviation 1/8 needs m >= 32 w^-2 ln(2J/beta); note uses 128 w^-2 ceil(log2(2J/beta))
    for beta in (Fr(1, 2), Fr(1, 16), Fr(1, 2 ** 20)):
        J = math.ceil(1 / w)
        m = math.ceil(128 / w ** 2 * math.ceil(math.log2(2 * J / beta)))
        # two-sided Hoeffding for J means of [0,1/w] variables at deviation 1/8, union over J
        check(2 * J * math.exp(-2 * m * (Fr(1, 8) * w) ** 2) <= beta, f"Hoeffding w={w} beta={beta}")
print("sec 6: rank identity E[1(lam>=t)/lam] = rank(P_t) exact; bias 1/32 and Hoeffding constants check")

# ---------------------------------------------------------------- sections 2-3 with real group actions (float)
def td(A, B):
    return 0.5 * np.abs(np.linalg.eigvalsh(A - B)).sum()

def proj_ge(rho, t):
    ev, V = np.linalg.eigh(rho)
    cols = V[:, ev >= t - 1e-13]
    return cols @ cols.conj().T, cols

def wedge_overlap(cols, U):
    # |<Omega_V | U^{tensor r} | Omega_V>| = |det(cols^dag U cols)|
    return abs(np.linalg.det(cols.conj().T @ U @ cols)) if cols.shape[1] else 1.0

def perm_matrices(n, gens):
    # closure of a permutation group given by generators, as matrices
    elems = {tuple(range(n))}
    frontier = list(elems)
    while frontier:
        new = []
        for g in frontier:
            for s in gens:
                h = tuple(g[s[i]] for i in range(n))
                if h not in elems:
                    elems.add(h); new.append(h)
        frontier = new
    mats = []
    for g in elems:
        P = np.zeros((n, n))
        for i in range(n):
            P[g[i], i] = 1
        mats.append(P)
    return mats

groups = {
    "S4 on C^4": perm_matrices(4, [(1, 0, 2, 3), (1, 2, 3, 0)]),
    "C5 on C^5": perm_matrices(5, [(1, 2, 3, 4, 0)]),
    "D4 on C^4": perm_matrices(4, [(1, 2, 3, 0), (3, 2, 1, 0)]),
    "S3xC2 on C^6": perm_matrices(6, [(1, 0, 2, 4, 3, 5), (1, 2, 0, 4, 5, 3), (3, 4, 5, 0, 1, 2)]),
}
ninst = 0; min_margin = 1e9
for name, G in groups.items():
    n = G[0].shape[0]
    for trial in range(60):
        R = rng.randint(1, n)
        # build rho with some symmetry: average a random low-rank state over a random subgroup sometimes
        X = nrng.normal(size=(n, R)) + 1j * nrng.normal(size=(n, R))
        rho = X @ X.conj().T
        if rng.random() < 0.6:
            sub = rng.sample(G, rng.randint(1, len(G)))
            rho = sum(U @ rho @ U.T for U in sub)
        rho = rho / np.trace(rho).real
        # truncate to rank <= R by eigen-threshold, keep exact rank info
        ev, V = np.linalg.eigh(rho)
        ev[ev < 1e-12] = 0
        rho = (V * ev) @ V.conj().T
        rank = int((ev > 1e-12).sum())
        Rb = max(rank, R)
        tds = [td(rho, U @ rho @ U.T) for U in G]
        H = [i for i, d in enumerate(tds) if d < 1e-9]
        outside = [d for d in tds if d >= 1e-9]
        if not outside:
            continue
        delta = min(outside)
        w = delta / (16 * Rb); J = math.ceil(1 / w); M = 8
        for a in range(M):
            ts = [w * (1 + a / M + j) for j in range(J)]
            # distinct positive-rank projectors
            flags = {}
            for t in ts:
                P, cols = proj_ge(rho, t)
                if cols.shape[1]:
                    flags[cols.shape[1]] = cols
            ranks = sorted(flags)
            check(sum(ranks) <= min(Rb * (Rb + 1) // 2, 1 / w + 1e-9), "register count")
            stab = []
            for i, U in enumerate(G):
                ov = 1.0
                for r_, cols in flags.items():
                    ov *= wedge_overlap(cols, U)
                if ov > 1 - 1e-9:
                    stab.append(i)
                else:
                    check(ov <= 1 - delta ** 2 / 8 + 1e-12, f"{name} joint gap ov={ov} delta={delta}")
                    min_margin = min(min_margin, (1 - ov) / (delta ** 2 / 8))
            check(stab == H, f"{name} stabilizer mismatch {stab} vs {H}")
            ninst += 1
print(f"sec 2-3 group controls: {ninst} (state, offset) instances over {list(groups)}; "
      f"stabilizer of the flag product = H in all; min (1-overlap)/(delta^2/8) = {min_margin:.3f}")

# false-global-gap control: overstating delta can invent symmetries
# eigenvalues 0.4 +- 1e-6 share one band of the grid built from the false delta = 0.5
lam = np.array([0.4 + 1e-6, 0.4 - 1e-6, 0.2, 0])
rho = np.diag(lam); swap = np.eye(4)[[1, 0, 2, 3]]
true_delta = td(rho, swap @ rho @ swap.T)
fake = 0.5
w = fake / (16 * 3); ts = [w * (1 + j) for j in range(math.ceil(1 / w))]
fixed = all(np.allclose(swap @ proj_ge(rho, t)[0] @ swap.T, proj_ge(rho, t)[0]) for t in ts)
check(fixed, "false-gap control")
print(f"false-gap control: true delta={true_delta:.1e}, supplied 0.5 -> swap (not in H) fixes every flag: {fixed}; the global-gap promise is necessary")

# ---------------------------------------------------------------- section 3 overlap lemma (float)
worst = 0
for trial in range(4000):
    n = rng.randint(2, 7); r = rng.randint(1, n - 1)
    A = np.linalg.qr(nrng.normal(size=(n, r)) + 1j * nrng.normal(size=(n, r)))[0]
    if rng.random() < 0.5:
        # near-identical subspace: small rotation
        Z = nrng.normal(size=(n, r)) * 10 ** rng.uniform(-6, 0)
        Bm = np.linalg.qr(A + Z)[0]
    else:
        Bm = np.linalg.qr(nrng.normal(size=(n, r)) + 1j * nrng.normal(size=(n, r)))[0]
    T = td(A @ A.conj().T / r, Bm @ Bm.conj().T / r)
    ov = abs(np.linalg.det(A.conj().T @ Bm))
    check(ov ** 2 <= 1 - T ** 2 + 1e-10, f"overlap^2 <= 1 - TD^2  ov={ov} T={T}")
    check(ov <= 1 - T ** 2 / 2 + 1e-10, "overlap <= 1 - TD^2/2")
    worst = max(worst, ov ** 2 + T ** 2)
print(f"sec 3 lemma: |<Omega_A|Omega_B>|^2 <= 1 - TD(A/r,B/r)^2 on 4000 pairs (max lhs+TD^2 = {worst:.6f})")

# ---------------------------------------------------------------- section 7 growth step (float + exact DP)
def antisym_proj(n, k):
    # projector onto wedge^k C^n inside (C^n)^{tensor k}
    dim = n ** k
    P = np.zeros((dim, dim))
    for perm in itertools.permutations(range(k)):
        sign = np.linalg.det(np.eye(k)[list(perm)])
        Pm = np.zeros((dim, dim))
        for idx in itertools.product(range(n), repeat=k):
            src = int(np.ravel_multi_index(idx, [n] * k))
            dst = int(np.ravel_multi_index(tuple(idx[perm[i]] for i in range(k)), [n] * k))
            Pm[dst, src] = 1
        P += sign * Pm
    return P / math.factorial(k)

for n, k in [(3, 1), (3, 2), (4, 2), (4, 3)]:
    Pk = antisym_proj(n, k); Pk1 = antisym_proj(n, k + 1)
    for trial in range(40):
        r = rng.randint(k + 1, n)
        Vb = np.linalg.qr(nrng.normal(size=(n, n)) + 1j * nrng.normal(size=(n, n)))[0][:, :r]
        evs = nrng.uniform(0.05, 1, size=r); evs /= evs.sum()
        rho = (Vb * evs) @ Vb.conj().T
        wmin = evs.min()
        # random pure psi in wedge^k(V): antisymmetrize a random vector of V^{tensor k}
        v = nrng.normal(size=r ** k) + 1j * nrng.normal(size=r ** k)
        emb = Vb
        for _ in range(k - 1):
            emb = np.kron(emb, Vb)
        psi = Pk @ (emb @ v)
        psi /= np.linalg.norm(psi)
        acc = np.real(np.trace(Pk1 @ np.kron(np.outer(psi, psi.conj()), rho)))
        # one-body reduced density of psi (normalised, trace 1)
        Psi = psi.reshape(n, n ** (k - 1))
        gam = Psi @ Psi.conj().T
        pred = (1 - k * np.real(np.trace(rho @ gam))) / (k + 1)
        check(abs(acc - pred) < 1e-9, f"acceptance formula n={n} k={k}")
        check(acc >= wmin * (r - k) / (k + 1) - 1e-9, "acceptance >= w(r-k)/(k+1)")
print("sec 7: acceptance of one growth step = (1 - k Tr(rho gamma_psi))/(k+1) >= w(r-k)/(k+1) for every pure psi in wedge^k V (float)")

def tail_exact(qs, N):
    # P[sum of independent geometrics with success probs qs > N], exact rationals
    dist = {0: Fr(1)}
    for q in qs:
        new = {}
        for s, pr in dist.items():
            for g in range(1, N - s + 1):
                new[s + g] = new.get(s + g, 0) + pr * (1 - q) ** (g - 1) * q
        dist = new
    return 1 - sum(dist.values())

for r in range(2, 7):
    for wden in [r, 2 * r, 4 * r]:
        w = Fr(1, wden)
        if w * r > 1:
            continue
        for b in [1, 2, 3]:
            N = math.ceil(r / w) * b
            if N > 400:
                continue
            qs = [w * (r - k) / (k + 1) for k in range(1, r)]   # worst admissible acceptance
            tail = tail_exact(qs, N)
            bound = r * math.exp(-N * w / r)
            check(float(tail) <= bound, f"tail r={r} w={w} b={b}: {float(tail)} > {bound}")
print("sec 7: exact tail of the growth clock <= r exp(-N w / r) for r<=6, w in {1/r,1/2r,1/4r}, b<=3")
print("TOTAL FAILURES:", fails)
