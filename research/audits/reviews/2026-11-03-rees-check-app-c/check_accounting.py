"""Item 3 (campaign 4): Proposition app-sub-stream tails and the copy-cost accounting.

1. Exact Fraction tails P(sum_{k=1}^{r-1} Geom(p_k) > r^2 B), p_k = (r-k)/(r(k+1)),
   against r 2^{-B}, for r = 2..10, B = 1..8; also the product of p_k equals r^{-r}
   (the one-shot projection probability quoted in Theorem subspace-source(ii)).
2. The parameters of Theorem app-sub-hsp and Remark app-sub-profile, recomputed
   from scratch with exact integers from the profile's lower-central dimensions,
   and compared with research/reductions/rees_subspace_source.json.
3. Remark app-sub-multiple-p numbers.
Run: /opt/anaconda3/bin/python check_accounting.py
"""
import json
import math
import os
from fractions import Fraction as F


def tail(r, N):
    """P(attempts > N) for the level chain 1 -> r with exact success probabilities."""
    dist = {1: F(1)}
    for _ in range(N):
        new = {}
        for k, pr in dist.items():
            if k == r:
                new[k] = new.get(k, 0) + pr
                continue
            pk = F(r - k, r * (k + 1))
            new[k + 1] = new.get(k + 1, 0) + pr * pk
            new[k] = new.get(k, 0) + pr * (1 - pk)
        dist = new
    return 1 - dist.get(r, F(0))


def part1():
    worst = 0
    for r in range(2, 11):
        prod = F(1)
        for k in range(1, r):
            prod *= F(r - k, r * (k + 1))
        assert prod == F(1, r ** r)
        for B in range(1, 9):
            N = r * r * B
            t = tail(r, N)
            bound = F(r, 2 ** B)
            assert t <= bound, (r, B)
            worst = max(worst, t / bound)
    print(f"1. tails exact for r = 2..10, B = 1..8: P(timeout) <= r 2^-B everywhere; "
          f"largest ratio {float(worst):.3f}; prod p_k = r^-r exactly")


def B_d(d, a):
    return (d ** (d * (d - 1) // 2) * (a + 1) ** d) ** math.ceil(math.log2(d + 1))


def ceil_log2_frac(x):
    """ceil(log2 x) for a positive Fraction x, exactly."""
    k = x.numerator.bit_length() - x.denominator.bit_length() - 1
    while F(2) ** k < x:
        k += 1
    while F(2) ** (k - 1) >= x:
        k -= 1
    return k


def log2(x):
    return math.log2(x) if x < 2 ** 1000 else (x.bit_length() - 1000) + math.log2(x >> (x.bit_length() - 1000))


def part2():
    here = os.path.dirname(os.path.abspath(__file__))
    js = json.load(open(os.path.join(here, "..", "..", "..", "reductions", "rees_subspace_source.json")))
    prof = js["public_group_profile"]
    p, c, n = prof["p"], prof["class"], prof["rees_dimension"]
    lcs = prof["original_lcs_dimensions"]
    m = lcs[0]
    g = {d: lcs[d - 1] for d in range(1, c + 1)}
    assert sum(g.values()) == n
    eps = F(1, 3)
    delta = F(1, 10)
    eps0 = eps / 4
    t = 0
    while F(p) ** t < 3 / eps0:
        t += 1
    prodM = 1
    for d in range(2, c + 1):
        prodM *= B_d(d, g[d])
    Bleaf = (m + t) * prodM
    gamma = delta ** 2 / 2
    # floor(n log2 p): exact via integer comparison
    fl = (p ** n).bit_length() - 1
    b = fl + 1 + ceil_log2_frac(8 * F(Bleaf) / eps)
    ell = math.ceil(F(b) / gamma)
    M = len(prof["design_points"])
    T = M * ell * Bleaf
    print(f"2. profile p={p}, c={c}, m={m}, n={n}: t={t}, log2 B_leaf = {log2(Bleaf):.2f}, b = {b}, "
          f"ell = {ell}, M = {M}, log2 T = {log2(T):.2f}")
    assert (t, b, ell, M) == (1, 2102, 420400, 14)
    rows = {}
    for prf in js["profiles"]:
        rows[prf["rank"]] = prf["budget"]
    for r in (1, 2, 8, 32):
        if r == 1:
            N = 0
            B = None
        else:
            B = ceil_log2_frac(8 * r * F(T) / eps)
            N = r * r * B
        raw = T * (N + 1)
        line = f"   r={r}: B={B}, N={N}, raw copies T(N+1) ~ 2^{log2(raw):.4f}, rT controlled R calls ~ 2^{log2(r*T):.2f}"
        if r in rows:
            jr = rows[r]
            ok_raw = int(jr['raw_copy_cap']) == raw
            ok_n = int(jr['growth_attempts_per_output']) == N and int(jr['growth_attempt_cap']) == T * N
            assert ok_raw and ok_n and (B is None or int(jr['tail_bits']) == B)
            line += "; json: raw_copy_cap == T(N+1), per-output cap == N, growth cap == TN, tail_bits == B"
        print(line)
    return p, c, ell, M, Bleaf, T


def part3(p, c, ell, M):
    ell_p = p * math.ceil(ell / p)
    print(f"3. Remark multiple-p: ell = {ell} -> {ell_p} (multiple of {p}); c*ell' = {c * ell_p:,}; M*ell = {M * ell:,}; "
          f"c(ell+p) = {c * (ell + p):,}")
    assert ell_p == 420411 and c * ell_p == 3783699 and M * ell == 5885600


if __name__ == "__main__":
    part1()
    p, c, ell, M, Bleaf, T = part2()
    part3(p, c, ell, M)
