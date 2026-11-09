"""Independent solvability checker for the diagonal SDE bank problem (written from
scratch; does NOT import sss.py).

Problem: columns lam_1..lam_M in F_p^a, kappa | p-1, P = (F_p^*)^kappa.
A solution is x in (P u {0})^M, x != 0, sum x_i lam_i = 0.

Method: a solution supported on S is a vector of K_S = ker(lam restricted to S) whose
coordinates all lie in P.  Up to a common scalar this is a vector of K_S whose coordinates
are nonzero and lie in ONE coset of P (then rescale by the inverse class).  We search
  * every subset S that is a circuit (dim K_S = 1, full support): exact test;
  * kernels of dim 2: scan all p+1 projective directions (exact for that S);
  * kernels of dim >= 3: scan many random 2-planes of K_S (sampled).
Subsets are enumerated exhaustively by size up to a cap, then sampled.
`exhaustive_small` decides solvability exactly by brute force over (P u {0})^M for tiny
instances (used only to cross-check this checker).
Returns a verified witness x or None.  None is NOT a proof of unsolvability unless the
function says so ('exact')."""
import itertools
import random
import numpy as np


class F:
    def __init__(self, p, k):
        assert (p - 1) % k == 0
        self.p, self.k = p, k
        # primitive root by brute force
        fac, n, d = [], p - 1, 2
        while d * d <= n:
            if n % d == 0:
                fac.append(d)
                while n % d == 0:
                    n //= d
            d += 1
        if n > 1:
            fac.append(n)
        g = 2
        while any(pow(g, (p - 1) // q, p) == 1 for q in fac):
            g += 1
        self.g = g
        # discrete log table -> class table
        cls = np.full(p, -1, dtype=np.int64)
        y = 1
        for e in range(p - 1):
            cls[y] = e % k
            y = y * g % p
        self.cls = cls

    def inP(self, y):
        return self.cls[y % self.p] == 0


def kernel(cols, S, p):
    """Basis of {y in F_p^S : sum_j y_j cols[S_j] = 0} (list of python int lists)."""
    a = len(cols[0])
    n = len(S)
    A = [[cols[S[j]][i] % p for j in range(n)] for i in range(a)]
    piv = []
    row = 0
    for c in range(n):
        r = next((t for t in range(row, a) if A[t][c]), None)
        if r is None:
            continue
        A[row], A[r] = A[r], A[row]
        iv = pow(A[row][c], p - 2, p)
        A[row] = [v * iv % p for v in A[row]]
        for t in range(a):
            if t != row and A[t][c]:
                f = A[t][c]
                A[t] = [(v - f * w) % p for v, w in zip(A[t], A[row])]
        piv.append(c)
        row += 1
        if row == a:
            break
    free = [c for c in range(n) if c not in piv]
    basis = []
    for fcol in free:
        y = [0] * n
        y[fcol] = 1
        for r, c in enumerate(piv):
            y[c] = (-A[r][fcol]) % p
        basis.append(y)
    return basis


def mono_scale(Fd, y):
    """If all coords of y are nonzero and in one class, return the rescaled vector in P^n."""
    p = Fd.p
    cl = Fd.cls[np.asarray(y, dtype=np.int64) % p]
    if (cl < 0).any() or (cl != cl[0]).any():
        return None
    c0 = int(cl[0])
    z = pow(Fd.g, (Fd.k - c0) % Fd.k, p)  # g^{-c0} mod P-classes
    return [v * z % p for v in y]


def scan_plane(Fd, u, w):
    """All directions u + t w (t in F_p) and w; return first monochromatic one or None."""
    p = Fd.p
    U = np.asarray(u, dtype=np.int64)
    W = np.asarray(w, dtype=np.int64)
    t = np.arange(p, dtype=np.int64)[:, None]
    V = (U[None, :] + t * W[None, :]) % p
    cl = Fd.cls[V]
    ok = (cl >= 0).all(axis=1) & (cl == cl[:, :1]).all(axis=1)
    idx = np.nonzero(ok)[0]
    if len(idx):
        return mono_scale(Fd, [int(v) for v in V[idx[0]]])
    return mono_scale(Fd, w)


def verify(Fd, cols, x):
    p = Fd.p
    if x is None or not any(v % p for v in x):
        return False
    if any(v % p and not Fd.inP(v) for v in x):
        return False
    a = len(cols[0])
    return all(sum(x[i] * cols[i][t] for i in range(len(cols))) % p == 0 for t in range(a))


def try_subset(Fd, cols, S, rng, planes=8):
    p = Fd.p
    K = kernel(cols, S, p)
    if not K:
        return None
    if len(K) == 1:
        y = mono_scale(Fd, K[0])
    elif len(K) == 2:
        y = scan_plane(Fd, K[0], K[1])
    else:
        y = None
        for _ in range(planes):
            c1 = [rng.randrange(p) for _ in K]
            c2 = [rng.randrange(p) for _ in K]
            u = [sum(c * v[j] for c, v in zip(c1, K)) % p for j in range(len(S))]
            w = [sum(c * v[j] for c, v in zip(c2, K)) % p for j in range(len(S))]
            y = scan_plane(Fd, u, w)
            if y:
                break
    if y is None:
        return None
    x = [0] * len(cols)
    for j, i in enumerate(S):
        x[i] = y[j]
    return x


def find_solution(Fd, cols, rng=None, exhaustive_upto=4, samples=4000, max_size=None):
    """Independent witness search.  Returns (x, how) with x verified, or (None, how)."""
    rng = rng or random.Random(1)
    p = Fd.p
    M = len(cols)
    for i, c in enumerate(cols):
        if not any(v % p for v in c):
            x = [0] * M
            x[i] = 1
            return x, "zero"
    max_size = max_size or M
    # exhaustive over small supports
    for s in range(2, min(exhaustive_upto, M) + 1):
        for S in itertools.combinations(range(M), s):
            x = try_subset(Fd, cols, list(S), rng)
            if x is not None and verify(Fd, cols, x):
                return x, "subset%d" % s
    # sampled larger supports (kernel dim 2-4 preferred)
    a = len(cols[0])
    for _ in range(samples):
        s = rng.randint(exhaustive_upto + 1, max(exhaustive_upto + 1, min(M, max_size)))
        S = sorted(rng.sample(range(M), s))
        x = try_subset(Fd, cols, S, rng)
        if x is not None and verify(Fd, cols, x):
            return x, "sample%d" % s
    return None, "notfound"


def exhaustive_small(Fd, cols):
    """Exact brute force over (P u {0})^M; only for tiny p and M."""
    p = Fd.p
    vals = [0] + [y for y in range(1, p) if Fd.inP(y)]
    for x in itertools.product(vals, repeat=len(cols)):
        if any(x) and verify(Fd, cols, list(x)):
            return list(x)
    return None


if __name__ == "__main__":
    # self-test against brute force on tiny instances
    rng = random.Random(5)
    for (p, k) in [(7, 2), (13, 3), (7, 3), (13, 2)]:
        Fd = F(p, k)
        agree = 0
        for t in range(150):
            a = rng.choice([1, 2])
            M = rng.randint(2, 5)
            cols = [[rng.randrange(p) for _ in range(a)] for _ in range(M)]
            ex = exhaustive_small(Fd, cols)
            x, how = find_solution(Fd, cols, rng, exhaustive_upto=M, samples=0)
            assert (x is None) == (ex is None), (p, k, cols, ex, x)
            agree += 1
        print("selftest p=%d k=%d: %d/150 agree with brute force" % (p, k, agree))
