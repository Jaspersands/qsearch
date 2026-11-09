"""Run the classical part (N2)-(N5) of the Schedule-3 node exactly, as written in Appendix B.

Banks are drawn as Lambda = E X with E a random injective g x a matrix and X uniform a x M
(the law of Lemma s3-law in intrinsic coordinates). Field elements come from fair bits by
rejection with the appendix's attempt cap; roots by the splitting procedure of Lemma s3-root
with round cap R; the witness is s_i = t_i^alpha (Bezout). Every accepted witness is verified
exactly against sum_i s_i^d lambda_i = 0. Also checks that a bank of rank > u-1 aborts in (N2).
Each run is exact; the reported trial counts are sample statistics (not a proof).

Run: /opt/anaconda3/bin/python -I node_sim.py
"""
import random
import sys
from math import gcd

sys.setrecursionlimit(10000)


# helpers copied verbatim from root_bezout_check.py (python -I cannot import siblings)
# polynomial helpers over F_p, coefficient lists low -> high
def trim(a):
    while a and a[-1] == 0:
        a.pop()
    return a


def pmod(a, b, p):
    a = a[:]
    inv = pow(b[-1], p - 2, p)
    while len(a) >= len(b):
        f = a[-1] * inv % p
        s = len(a) - len(b)
        for i, bi in enumerate(b):
            a[s + i] = (a[s + i] - f * bi) % p
        trim(a)
    return a


def pmul(a, b, p):
    if not a or not b:
        return []
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i + j] = (r[i + j] + x * y) % p
    return trim(r)


def pdivexact(a, b, p):
    a = a[:]
    q = [0] * (len(a) - len(b) + 1)
    inv = pow(b[-1], p - 2, p)
    while len(a) >= len(b) and a:
        f = a[-1] * inv % p
        s = len(a) - len(b)
        q[s] = f
        for i, bi in enumerate(b):
            a[s + i] = (a[s + i] - f * bi) % p
        trim(a)
    assert not a
    return trim(q)


def pgcd(a, b, p):
    a, b = trim(a[:]), trim(b[:])
    while b:
        a, b = b, pmod(a, b, p)
    inv = pow(a[-1], p - 2, p)
    return [x * inv % p for x in a]


def ppowmod(base, e, m, p):
    r = [1]
    base = pmod(base, m, p)
    while e:
        if e & 1:
            r = pmod(pmul(r, base, p), m, p)
        base = pmod(pmul(base, base, p), m, p)
        e >>= 1
    return r


def splits(g, delta, p):
    w = ppowmod([delta % p, 1], (p - 1) // 2, g, p)
    w = trim([(w[0] - 1) % p] + w[1:]) if w else [p - 1]
    g1 = pgcd(g, w, p) if w else g[:]
    return 0 < len(g1) - 1 < len(g) - 1, g1


def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y




def clog2(n):
    return (n - 1).bit_length() if n > 1 else 0


class Coins:
    def __init__(self, seed, cap):
        self.rng = random.Random(seed)
        self.cap = cap
        self.draws = 0

    def field(self, p):
        ell = clog2(p)
        self.draws += 1
        for _ in range(self.cap):
            v = self.rng.getrandbits(ell)
            if v < p:
                return v
        raise TimeoutError("draw")


def kernel_basis(Lam, p):
    """Lam: list of g rows, M columns. Returns rank r and a basis of the right kernel."""
    A = [r[:] for r in Lam]
    g, M = len(A), len(A[0])
    pivcols, r = [], 0
    for c in range(M):
        piv = next((i for i in range(r, g) if A[i][c]), None)
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        inv = pow(A[r][c], p - 2, p)
        A[r] = [x * inv % p for x in A[r]]
        for i in range(g):
            if i != r and A[i][c]:
                f = A[i][c]
                A[i] = [(x - f * y) % p for x, y in zip(A[i], A[r])]
        pivcols.append(c)
        r += 1
    free = [c for c in range(M) if c not in pivcols]
    basis = []
    for fc in free:
        v = [0] * M
        v[fc] = 1
        for i, pc in enumerate(pivcols):
            v[pc] = (-A[i][fc]) % p
        basis.append(v)
    return r, basis


def root(y, kappa, p, coins, R):
    g = [(-y) % p] + [0] * (kappa - 1) + [1]
    while len(g) - 1 >= 2:
        for _ in range(R):
            ok, g1 = splits(g, coins.field(p), p)
            if ok:
                break
        else:
            raise TimeoutError("root")
        g2 = pdivexact(g, g1, p)
        g = g1 if len(g1) <= len(g2) else g2
    return (-g[0]) % p


def node(Lam, p, d, u, B, seed):
    M = len(Lam[0])
    kappa = gcd(d, p - 1)
    h = (p - 1) // kappa
    _, alpha, _ = egcd(d, p - 1)
    K = 4 * kappa ** M * B
    L = max(1, clog2(kappa))
    R = 2 * (B + clog2(M * L))
    F = K * M + M * L * R
    coins = Coins(seed, B + clog2(F))
    r, ker = kernel_basis(Lam, p)
    if r > u - 1:
        return "abort-rank", None, 0
    try:
        for trial in range(1, K + 1):
            cs = [coins.field(p) for _ in ker]
            w = [sum(c * k[i] for c, k in zip(cs, ker)) % p for i in range(M)]
            if any(w) and all(pow(x, h, p) == 1 for x in w if x):
                break
        else:
            return "abort-trials", None, K
        s = []
        for yi in w:
            if yi == 0:
                s.append(0)
            else:
                t = yi if kappa == 1 else root(yi, kappa, p, coins, R)
                assert pow(t, kappa, p) == yi
                s.append(pow(t, alpha % (p - 1), p))
    except TimeoutError as e:
        return "abort-" + str(e), None, 0
    g = len(Lam)
    ok = any(s) and all(sum(pow(si, d, p) * Lam[row][i] for i, si in enumerate(s)) % p == 0
                        for row in range(g))
    return ("accept" if ok else "N5-FAIL"), s, trial


def random_bank(p, g, a, M, rng):
    if a == 0:
        return [[0] * M for _ in range(g)]
    while True:
        E = [[rng.randrange(p) for _ in range(a)] for _ in range(g)]
        if kernel_basis([list(col) for col in zip(*E)], p)[0] == a:  # E injective
            break
    X = [[rng.randrange(p) for _ in range(M)] for _ in range(a)]
    return [[sum(E[i][k] * X[k][j] for k in range(a)) % p for j in range(M)] for i in range(g)]


CASES = [  # (u, p, d, a, g, runs): kappa = gcd(d, p-1) noted
    (2, 67, 2, 1, 3, 40),    # kappa 2
    (2, 67, 2, 0, 2, 5),     # a = 0: labels all zero
    (3, 149, 3, 2, 4, 10),   # kappa 1 (Bezout only)
    (3, 151, 2, 2, 3, 6),    # kappa 2
    (3, 151, 3, 1, 3, 3),    # kappa 3
    (4, 263, 4, 1, 3, 4),    # kappa 2 < d = 4: roots plus Bezout
    (4, 257, 3, 3, 5, 6),    # kappa 1, d = 3
]
rng = random.Random(1103)
bad = []
for (u, p, d, a, g, runs) in CASES:
    M = 4 * u
    B = clog2(64 * M)  # c = 2 tree depth is irrelevant to the node; B >= 1
    res = []
    for k in range(runs):
        Lam = random_bank(p, g, a, M, rng)
        status, s, trials = node(Lam, p, d, u, B, seed=rng.getrandbits(64))
        res.append((status, trials))
        if status != "accept":
            bad.append((u, p, d, a, status))
    trials = [t for st, t in res if st == "accept"]
    print(f"u={u} p={p} d={d} kappa={gcd(d, p - 1)} a={a}: {sum(st == 'accept' for st, _ in res)}/{runs} accepted;"
          f" trials max {max(trials) if trials else None}, cap K={4 * gcd(d, p - 1) ** M * B}")
# rank guard: a bank of rank u (> u-1) must abort in (N2)
u, p, d = 2, 67, 2
Lam = random_bank(p, 3, 2, 8, rng)
st, _, _ = node(Lam, p, d, u, 5, seed=7)
print("rank-2 bank at u=2:", st)
if st != "abort-rank":
    bad.append("rank guard")
print("non-accepting runs:", bad)
