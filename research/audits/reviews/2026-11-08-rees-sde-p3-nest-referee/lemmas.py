"""Referee checks of Lemma G, Lemma P, Lemma M, Lemma D (exact, independent code)."""
import itertools, math, sys
from fractions import Fraction
import numpy as np
from f3 import rank, nullspace, normalize

rng = np.random.default_rng(20261108)
CL = [(a, b) for a in (1, 2) for b in range(3)]          # the six classes P_ab

# ------------------------------------------------------------------ Lemma G (gadget)
print("== Lemma G ==")
rel1 = np.array([1 if a == 1 else 2 for (a, b) in CL])    # w_1. - w_2.
rel2 = np.array([{(1, 1): 1, (2, 1): 1, (1, 2): 2, (2, 2): 2}.get(c, 0) for c in CL])
# derive the relations from scratch: delta = sum a w_a. = 0, delta' = sum b w_.b = 0
d1 = np.array([a for (a, b) in CL]); d2 = np.array([b for (a, b) in CL])
R = np.vstack([d1, d2]) % 3
assert rank(np.vstack([R, rel1, rel2])) == 2, "note's relations = span of delta, delta'"
h1 = np.array([1 if c in [(1, 0), (1, 1), (2, 0)] else 0 for c in CL])
h2 = np.array([1 if c in [(1, 1), (1, 2), (2, 2)] else 0 for c in CL])
print("h1,h2 independent mod relations:", rank(np.vstack([R, h1, h2])) == 4)
# for each alpha find ALL class unions U with 1_U = alpha.h mod <R>
alphas = [a for a in itertools.product(range(3), repeat=2) if a != (0, 0)]
found = {}
for al in alphas:
    tgt = (al[0] * h1 + al[1] * h2) % 3
    sols = []
    for bits in itertools.product((0, 1), repeat=6):
        u = np.array(bits)
        if rank(np.vstack([R, (u - tgt) % 3])) == 2:
            sols.append(frozenset(c for c, bb in zip(CL, bits) if bb))
    found[al] = sols
    print(" alpha", al, "unions:", [sorted(s) for s in sols])
NOTE = {(0, 1): [(1, 1), (1, 2), (2, 2)], (0, 2): [(1, 2), (2, 1), (2, 2)],
        (1, 0): [(1, 0), (1, 1), (2, 0)], (1, 1): [(1, 0), (2, 0), (2, 1)],
        (1, 2): [(1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)],
        (2, 0): [(1, 1), (2, 0), (2, 2)], (2, 1): [(2, 0), (2, 1), (2, 2)],
        (2, 2): [(1, 0), (1, 2), (2, 1)]}
print("note's UNIONS table among the derived solutions:",
      all(frozenset(NOTE[a]) in found[a] for a in alphas))
UNION = {a: frozenset(NOTE[a]) for a in alphas}
# degenerate emptiness: E = set of nonempty classes; delta full support; delta' not in <delta>
bad = []
nondeg = 0
for r in range(1, 7):
    for E in itertools.combinations(CL, r):
        E = set(E)
        prop = any(all(b == (c * a) % 3 for (a, b) in E) for c in range(3))
        if prop:
            continue
        nondeg += 1
        for al in alphas:
            al2 = tuple((2 * x) % 3 for x in al)
            if not (UNION[al] & E) and not (UNION[al2] & E):
                bad.append((sorted(E), al))
print(f"nonempty-class patterns with delta' not in <delta>: {nondeg}; "
      f"(alpha, 2alpha) pairs with both unions empty: {len(bad)}")
# also: whenever some listed union is empty, which E?  (referee's 16)
emp = sum(1 for r in range(1, 7) for E in itertools.combinations(CL, r)
          if not any(all(b == (c * a) % 3 for (a, b) in E) for c in range(3))
          and any(not (UNION[a] & set(E)) for a in alphas))
print("patterns emptying at least one listed union:", emp)
# numeric check: random X with delta of full support and delta' nested, in F_3^q
ok = 0
for trial in range(300):
    q = int(rng.integers(3, 9)); s = q + 2 + int(rng.integers(0, 3))
    while True:
        M = rng.integers(0, 3, size=(q, s))
        B = nullspace(M)
        if len(B) < 2:
            continue
        x = rng.integers(0, 3, size=len(B)); dl = (x @ B) % 3
        if np.all(dl != 0):
            break
    dp = None
    for b in B:
        if rank(np.vstack([dl, b])) == 2:
            dp = b; break
    w = {c: np.zeros(q, dtype=np.int64) for c in CL}
    for i in range(s):
        w[(int(dl[i]), int(dp[i]))] += M[:, i]
    H1 = sum(w[c] for c in UNION[(1, 0)]) % 3; H2 = sum(w[c] for c in UNION[(0, 1)]) % 3
    for al in alphas:
        S = sum(w[c] for c in UNION[al]) % 3
        assert np.array_equal(S, (al[0] * H1 + al[1] * H2) % 3)
    ok += 1
print("numeric gadget identities on", ok, "random nested pairs: all hold")

# ------------------------------------------------------------------ Lemma P (series classes)
print("== Lemma P ==")
def classes(B):
    """proportionality classes of the columns of the k x N basis matrix B (no zero columns)."""
    cls = {}
    for i in range(B.shape[1]):
        cls.setdefault(normalize(B[:, i]), []).append(i)
    return list(cls.values())
cnt = 0; tight = 0; maxa = 0
for trial in range(4000):
    q = int(rng.integers(2, 7)); N = int(rng.integers(q + 1, q + 7))
    # mixture: random, low-rank, with planted chains
    mode = trial % 3
    if mode == 0:
        M = rng.integers(0, 3, size=(q, N))
    elif mode == 1:
        k = int(rng.integers(1, q + 1)); M = (rng.integers(0, 3, size=(q, k)) @ rng.integers(0, 3, size=(k, N))) % 3
    else:
        L = int(rng.integers(2, min(q, N - 1) + 1))
        U = rng.integers(0, 3, size=(q, L - 1))
        chain = np.hstack([U, (-(U @ rng.integers(1, 3, size=L - 1))[:, None]) % 3])
        M = np.hstack([chain, rng.integers(0, 3, size=(q, N - L))]) % 3
    M = M[:, np.any(M != 0, axis=0)]
    if M.shape[1] == 0:
        continue
    B = nullspace(M)
    if len(B) == 0 or np.any(np.all(B == 0, axis=0)):
        continue                                 # need: no coloop
    r = rank(M)
    for A in classes(B):
        rest = [j for j in range(M.shape[1]) if j not in A]
        rr = rank(M[:, rest]) if rest else 0
        assert r - rr >= len(A) - 1, (M, A)
        cnt += 1; tight += (r - rr == len(A) - 1); maxa = max(maxa, len(A))
        # exactness: drop is exactly a-1 (images of A span a-1 dims, and r-rr cannot exceed a)
        assert r - rr <= len(A)
print(f"classes tested {cnt}, drop == a-1 in {tight}, max class size {maxa}; no violation")

# ------------------------------------------------------------------ Lemma M (second moment)
print("== Lemma M ==")
mcnt = 0
for trial in range(600):
    q = int(rng.integers(1, 5)); N = int(rng.integers(q + 1, q + 6))
    M = rng.integers(0, 3, size=(q, N))
    if trial % 2:   # plant duplicates / negatives -> larger classes
        j = int(rng.integers(0, N)); k = int(rng.integers(0, N)); M[:, k] = (2 * M[:, j]) % 3
    B = nullspace(M)
    if len(B) == 0 or np.any(np.all(B == 0, axis=0)) or len(B) > 7:
        continue
    ws = [int(np.count_nonzero((np.array(x) @ B) % 3)) for x in itertools.product(range(3), repeat=len(B))]
    T = len(ws)
    mean = Fraction(sum(ws), T); var = Fraction(sum(w * w for w in ws), T) - mean * mean
    a = [len(c) for c in classes(B)]
    assert mean == Fraction(2 * N, 3), (mean, N)
    assert var == Fraction(2, 9) * sum(x * x for x in a), (var, a)
    mcnt += 1
print(f"{mcnt} coloop-free codes: mean = 2N/3 and Var = (2/9) sum a_j^2 exactly in all")

# ------------------------------------------------------------------ Lemma D (conditional expectations)
print("== Lemma D ==")
def phi27(B, prefix):
    """27 * E[(wt - 2N/3)^2 | x_1..x_j = prefix] via the note's class formula (integer)."""
    k, N = B.shape; j = len(prefix)
    c = (np.array(prefix, dtype=np.int64) @ B[:j]) % 3 if j else np.zeros(N, dtype=np.int64)
    G = B[j:]
    const = 0; groups = {}
    for i in range(N):
        g = G[:, i] % 3
        if not np.any(g):
            const += 3 * (c[i] != 0) - 2
        else:
            nz = np.nonzero(g)[0][0]; s = int(g[nz])
            key = normalize(g)
            groups.setdefault(key, []).append((int(c[i]), s))
    tot = 27 * const * const   # (3Y)^2 -> 9 Y^2 ... scale: 27*Phi = 3*(sum 3Y)^2 + sum_cls sum_t (sum 3Y)^2
    tot = 3 * const * const
    for key, lst in groups.items():
        for t in range(3):
            ssum = sum(3 * ((ci + si * t) % 3 != 0) - 2 for ci, si in lst)
            tot += ssum * ssum
    return tot
def phi27_brute(B, prefix):
    k, N = B.shape; j = len(prefix); tot = Fraction(0); cntx = 0
    for rest in itertools.product(range(3), repeat=k - j):
        x = np.array(list(prefix) + list(rest), dtype=np.int64)
        w = int(np.count_nonzero((x @ B) % 3)); tot += (Fraction(w) - Fraction(2 * N, 3)) ** 2; cntx += 1
    return 27 * tot / cntx
def pick(B):
    pre = []
    for j in range(B.shape[0]):
        vals = [phi27(B, pre + [v]) for v in range(3)]
        pre.append(int(np.argmin(vals)))
    return (np.array(pre) @ B) % 3
dcnt = 0
for trial in range(300):
    q = int(rng.integers(1, 6)); N = int(rng.integers(q + 2, q + 8))
    M = rng.integers(0, 3, size=(q, N))
    B = nullspace(M)
    if len(B) == 0 or np.any(np.all(B == 0, axis=0)) or len(B) > 6:
        continue
    for j in range(len(B) + 1):
        for pre in itertools.product(range(3), repeat=j):
            assert Fraction(phi27(B, list(pre))) == phi27_brute(B, list(pre))
    d = pick(B); w = int(np.count_nonzero(d))
    a = [len(c) for c in classes(B)]
    assert (3 * w - 2 * N) ** 2 <= 2 * sum(x * x for x in a)        # 9(wt-mu)^2 <= 9 Var
    assert w > 0
    dcnt += 1
print(f"{dcnt} codes: class formula == brute-force conditional expectation at every prefix; "
      f"selected codeword within one sigma and nonzero")

# ------------------------------------------------------------------ pool size, sums
print("== N(q) and the closed-form sums ==")
def Nq(q):
    N = 1
    while N - 1.5 * q < 3 + math.sqrt(N):
        N += 1
    return N
print("N(q) <= 1.5q+2sqrt(q)+6 for 4<=q<20000:",
      all(Nq(q) <= 1.5 * q + 2 * math.sqrt(q) + 6 for q in range(4, 20000)))
print("N(q) nondecreasing on 1..20000:", all(Nq(q) <= Nq(q + 1) for q in range(1, 20000)))
okS = all(sum(q for q in range(n, 3, -2)) <= n * n / 4 + n / 2 and
          sum(math.sqrt(q) for q in range(n, 3, -2)) <= (n + 2) ** 1.5 / 3 and
          len(range(n, 3, -2)) <= n / 2 for n in range(4, 5000))
print("sum q <= n^2/4+n/2, sum sqrt q <= (n+2)^1.5/3, #stages <= n/2 for 4<=n<5000:", okS)
