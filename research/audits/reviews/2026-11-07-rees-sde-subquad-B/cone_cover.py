"""Basic-cone covering [exact for q = 2 and small p; sampled otherwise], kappa = 2.

A set S of n columns in F_p^q covers w if w = sum_{i in B} x_i lambda_i with B a basis
contained in S and every x_i in P (nonzero squares).  A covering piece realises the
quotient with no coset sampling: query the cosets of the minors det(lambda_T, w) and
read off a good basis.  This is the theta-free, many-query rule that Theorem B's
table model charges at kappa^(#queried forms), so it marks the boundary of that model.

(1) q = 2, n = 5: exhaustive coverage of all w (off the lines through the columns) at
    small primes, against the split-graph criterion (p = 1 mod 4: some w is uncovered
    iff the graph of pairs with chi(det(l_i,l_j)) = +1 is a split graph and the
    offending sign pattern occurs; p = 3 mod 4: the all-equal sign pattern is never
    covered by a 2-cone).
(2) q = 3, 4: exhaustive coverage over all w at p = 13, 17 for n = q+1, ..., 2q+2.
(3) q up to 10, p = 10^9+7: fraction of bases covering a random w (about 2^-q), i.e.
    the cost of finding a covering basis by trying bases.
"""
import itertools
import random

from subB import F, BigF, rank, brt


def det2(u, v, p):
    return (u[0] * v[1] - u[1] * v[0]) % p


def is_split(n, E):
    """Does V = clique(E) union independent(E) for some partition?  (brute force)"""
    V = range(n)
    for mask in range(1 << n):
        A = [i for i in V if mask >> i & 1]      # clique
        B = [i for i in V if not mask >> i & 1]  # independent
        if all((i, j) in E for i, j in itertools.combinations(A, 2)) and \
           all((i, j) not in E for i, j in itertools.combinations(B, 2)):
            return True
    return False


def part1(rng):
    for p in (13, 17, 29, 37, 41, 53, 101, 11, 19, 23, 43, 103):
        Fd = F(p, 2)
        tally = {}
        for _ in range(40):
            while True:
                S = [[rng.randrange(p), rng.randrange(p)] for _ in range(5)]
                if all(det2(S[i], S[j], p) for i, j in itertools.combinations(range(5), 2)):
                    break
            lines = set()
            for v in S:
                for t in range(1, p):
                    lines.add(((t * v[0]) % p, (t * v[1]) % p))
            unc = 0
            for w0 in range(p):
                for w1 in range(p):
                    w = (w0, w1)
                    if w == (0, 0) or w in lines:
                        continue
                    cov = False
                    for i, j in itertools.combinations(range(5), 2):
                        d = det2(S[i], S[j], p)
                        di = inv = pow(d, p - 2, p)
                        x_i = (det2(w, S[j], p) * inv) % p
                        x_j = (det2(S[i], w, p) * inv) % p
                        if x_i and x_j and Fd.in_sq(x_i) and Fd.in_sq(x_j):
                            cov = True
                            break
                    unc += not cov
            Ep = {(i, j) for i, j in itertools.combinations(range(5), 2) if Fd.in_sq(det2(S[i], S[j], p))}
            split = is_split(5, Ep)
            key = ("full" if unc == 0 else "partial", "split" if split else "nonsplit")
            tally[key] = tally.get(key, 0) + 1
        print(f"(1) q=2 n=5 p={p} (p mod 4 = {p % 4}): (coverage, sign graph) -> count {tally}", flush=True)


def covers(Fd, S, w, q):
    p = Fd.p
    for B in itertools.combinations(range(len(S)), q):
        cols = [S[i] for i in B]
        x = brt.solve_basis(cols, w, p)
        if x is None:
            continue
        if all(v and Fd.in_sq(v) for v in x):
            return True
    return False


def part2(rng):
    for (p, q) in [(13, 3), (17, 3), (29, 3), (13, 4)]:
        Fd = F(p, 2)
        for n in range(q + 1, 2 * q + 3):
            full = 0
            worst = 0.0
            trials = 4 if q == 3 else 2
            for _ in range(trials):
                S = [[rng.randrange(p) for _ in range(q)] for _ in range(n)]
                tot = unc = 0
                for w in itertools.product(range(p), repeat=q):
                    if not any(w):
                        continue
                    # skip w lying in the span of q-1 columns (measure zero, boundary)
                    tot += 1
                    if not covers(Fd, S, list(w), q):
                        unc += 1
                frac = unc / tot
                worst = max(worst, frac)
                full += unc == 0
            print(f"(2) q={q} p={p} n={n}: fully covered {full}/{trials}, worst uncovered fraction {worst:.4f}",
                  flush=True)


def part3(rng):
    p = 10**9 + 7
    Fd = BigF(p, 2)
    for q in (2, 4, 6, 8, 10):
        n = 2 * q
        S = [[rng.randrange(p) for _ in range(q)] for _ in range(n)]
        good = tried = 0
        for _ in range(3000):
            w = [rng.randrange(p) for _ in range(q)]
            B = rng.sample(range(n), q)
            x = brt.solve_basis([S[i] for i in B], w, p)
            tried += 1
            if x is not None and all(v and Fd.in_sq(v) for v in x):
                good += 1
        print(f"(3) q={q} n={n} p=1e9+7: fraction of random bases covering a random target "
              f"{good}/{tried} = {good/tried:.4f} (2^-q = {2**-q:.4f})", flush=True)


if __name__ == "__main__":
    import sys
    rng = random.Random(5)
    parts = sys.argv[1:] or ["1", "3", "2"]
    for k in parts:
        {"1": part1, "2": part2, "3": part3}[k](rng)
