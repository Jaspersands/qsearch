"""Referee check: Theorem 2(b) stall inequality, B basis/disjointness invariants,
GP => no true pool, and per-pass backward failure counts (hidden by sss_theorem retries)."""
import sys, random, itertools
sys.path.insert(0, "..")
sys.setrecursionlimit(10000)
from sss import Field, forward_swap, backward, rank, solve_in_span, worst_forward_cost, check
from run_adversarial import fam_lines, fam_subspace, fam_flag, fam_sparse

def reserve_of(cols, p):
    res, bas = [], []
    for i in range(len(cols)):
        if solve_in_span(bas, cols[i], p) is None:
            bas.append(cols[i]); res.append(i)
    return res

rng = random.Random(123)
viol = 0; nstall = 0; nstall_nopool_big = 0; tot = 0
for (p, k) in [(1009, 2), (1009, 3), (10007, 2)]:
    Fd = Field(p, k)
    for a in (3, 4, 5, 6):
        for M in range(a + 1, worst_forward_cost(a, 3, {}) + a + 4):
            for fam in range(5):
                for t in range(3):
                    if fam == 0: cols = fam_lines(rng, p, a, M, a + 1)
                    elif fam == 1: cols = fam_subspace(rng, p, a, M, a - 1, 0.8)
                    elif fam == 2: cols = fam_flag(rng, p, a, M)
                    elif fam == 3: cols = fam_sparse(rng, p, a, M)
                    else: cols = [[rng.randrange(p) for _ in range(a)] for _ in range(M)]
                    if any(not any(c) for c in cols): continue
                    r = rank(cols, p)[0]
                    res = forward_swap(Fd, cols, 3, rng, reserve_of(cols, p), "random")
                    tot += 1
                    if res["status"] == "direct": continue
                    B = res["B"]
                    used = [i for R in res["rounds"] for i in R.S]
                    # invariants
                    assert rank([cols[i] for i in B], p)[0] == r == len(B)
                    assert not (set(B) & set(used)) and not (set(B) & set(res["pool"])) and not (set(used) & set(res["pool"]))
                    if res["status"] == "stall":
                        nstall += 1
                        D = lambda q: worst_forward_cost(q, 3, {})
                        q = r - len(res["U"]); pi = len(res["pool"])
                        if not (M <= D(r) - D(q) + r + pi + q):
                            viol += 1; print("VIOL", p, k, a, M, fam, q, pi)
                        if M >= D(r) + r and pi == 0:
                            nstall_nopool_big += 1; print("stall with no pool above budget!", p, k, a, M)
print("banks", tot, "stalls", nstall, "inequality violations", viol, "no-pool stalls at budget", nstall_nopool_big)

# per-pass failures on GP banks at small admissible primes
def is_gp(cols, p):
    r = rank(cols, p)[0]
    return all(rank([cols[i] for i in S], p)[0] == r for S in itertools.combinations(range(len(cols)), r))
for (p, k, a, n) in [(307, 3, 2, 40), (307, 3, 3, 40), (2791, 3, 3, 30), (257, 2, 4, 30), (31, 2, 3, 40), (11, 2, 2, 40)]:
    Fd = Field(p, k)
    M = worst_forward_cost(a, 3, {}) + a
    fails = passes = pools = 0; minG = None
    for t in range(n):
        while True:
            cols = [[rng.randrange(p) for _ in range(a)] for _ in range(M)]
            if all(any(c) for c in cols) and is_gp(cols, p): break
        res = forward_swap(Fd, cols, 3, rng, reserve_of(cols, p), "random")
        if res["status"] != "ok":
            if res["status"] == "stall": print("GP STALL", p, k, a)
            continue
        pools += len(res["pool"])
        for _ in range(20):
            x, st = backward(Fd, cols, res["rounds"], res["U"], res["B"], rng)
            passes += 1
            if x is None: fails += 1
            else: assert check(Fd, cols, x)
    print("GP p=%d k=%d a=%d M=%d: passes %d, per-pass failures %d, true pool %d" % (p, k, a, M, passes, fails, pools))
