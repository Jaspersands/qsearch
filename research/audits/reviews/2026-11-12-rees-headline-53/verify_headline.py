#!/opt/anaconda3/bin/python
"""Independent check of the Schedule 1 zero-sum-depth headline (AI-run, pending human review).

Run from the repo root:
    nice -n 19 /opt/anaconda3/bin/python research/audits/reviews/2026-11-12-rees-headline-53/verify_headline.py

Code path independent of theorems/rees_hsp_reduction.py (no import of it):
  * t(p, kappa) by sumset iteration over the kappa-th power subgroup built from a primitive root,
    with NO Weil shortcut, for every prime p < 4*9^4 = 26244 and every kappa | p-1, kappa <= 9;
  * the Weil claim "t <= 3 for p >= 4 kappa^4" spot-checked exactly on every prime in [26244, 40000];
  * the worst case over p > c of 1 + sum_d kappa_d ceil(log2 t_d), c = 2..9, from the exhaustive range
    plus every unit residue class mod 5040 (pattern depends only on p mod 5040 above 26244);
  * the same maximization for the class-nine profile product (g_d) and the b = 104 envelope;
  * the crossover table of tab:query-crossover with the new p-uniform count (functions of
    2026-11-02-rees-classical-lower-bound/classical_lb.py imported read-only).
Finite computation: it can falsify, it proves nothing asymptotic by itself.
"""
import importlib.util
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
C9 = 9
SMALL = 4 * C9 ** 4  # 26244


def sieve(n):
    s = bytearray([1]) * (n + 1)
    s[0] = s[1] = 0
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return [i for i in range(n + 1) if s[i]]


PRIMES = sieve(200000)
PSET = set(PRIMES)


def is_prime(n):
    if n <= 200000:
        return n in PSET
    if n % 2 == 0:
        return False
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def primitive_root(p):
    if p == 2:
        return 1
    n, fac, q = p - 1, [], 2
    while q * q <= n:
        if n % q == 0:
            fac.append(q)
            while n % q == 0:
                n //= q
        q += 1
    if n > 1:
        fac.append(n)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fac):
            return g


def t_bruteforce(p, k, g=None):
    """Least t with a sum of t elements of P_k equal to 0 (sumset iteration, no shortcut)."""
    if k == 1:
        return 2
    g = g or primitive_root(p)
    gk, x, P = pow(g, k, p), 1, []
    for _ in range((p - 1) // k):
        P.append(x)
        x = x * gk % p
    assert x == 1 and len(set(P)) == len(P)
    Ps = set(P)
    # By homogeneity (P is a group): t = 2 iff -1 in P; t <= 3 iff -1 = u + v with u, v in P.
    # These are the definitions, not the parity rule or the Weil bound.
    if (p - 1) in Ps:
        return 2
    if any((p - 1 - u) % p in Ps for u in P):
        return 3
    S, t = set(Ps), 1   # sumset iteration (only reached when t >= 4, i.e. small p)
    while 0 not in S:
        S = {(a + b) % p for a in S for b in P}
        t += 1
        assert t <= k + 1, (p, k)
    return t


def ceil_log2(t):
    return (t - 1).bit_length()


T = {}  # (p, kappa) -> t, exhaustive range
for p in PRIMES:
    if p >= SMALL:
        break
    g = primitive_root(p)
    for k in range(1, C9 + 1):
        if (p - 1) % k == 0:
            T[(p, k)] = t_bruteforce(p, k, g)

checks = {}
# Parity rule and Chevalley-Warning on the exhaustive range.
checks["t2_iff_even_index"] = all((t == 2) == (((p - 1) // k) % 2 == 0) for (p, k), t in T.items())
checks["chevalley_warning_t_le_k_plus_1"] = all(t <= k + 1 for (p, k), t in T.items())
checks["weil_t_le_3_on_range_p_ge_4k4"] = all(t <= 3 for (p, k), t in T.items() if p >= 4 * k ** 4)
checks["t(41,8)"] = T[(41, 8)]
checks["t(2521,8)"] = T[(2521, 8)]
checks["t_ge_4_cases"] = sorted((p, k, t) for (p, k), t in T.items() if t >= 4 and p > 9)[:12]
checks["max_p_with_t_ge_4"] = max(p for (p, k), t in T.items() if t >= 4)
# Weil spot check above the exhaustive range: only the t <= 3 question matters there.
viol = []
for p in PRIMES:
    if p < SMALL:
        continue
    if p > 40000:
        break
    g = primitive_root(p)
    for k in range(2, C9 + 1):
        if (p - 1) % k == 0 and ((p - 1) // k) % 2 == 1:
            gk, x, P = pow(g, k, p), 1, set()
            for _ in range((p - 1) // k):
                P.add(x)
                x = x * gk % p
            if not any((-1 - y) % p in P for y in P):
                viol.append((p, k))
checks["weil_spotcheck_26244_40000_violations"] = viol


def pattern_small(p, c):
    out = []
    for d in range(2, c + 1):
        k = math.gcd(d, p - 1)
        out.append((k, ceil_log2(T[(p, k)])))
    return tuple(out)


def pattern_residue(r, c):
    out = []
    for d in range(2, c + 1):
        k = math.gcd(d, r - 1)
        out.append((k, 1 if _even(r, k) else 2))
    return tuple(out)


def _even(r, k):
    # (p-1)/k even  <=>  v2(p-1) > v2(k); p-1 = r-1 mod 16 determines v2(p-1) up to >= 4 > v2(k).
    v = 4 if (r - 1) % 16 == 0 else ((r - 1) % 16 & -((r - 1) % 16)).bit_length() - 1
    return v > (k & -k).bit_length() - 1


def split_patterns(c):
    small, res = {}, {}
    for p in PRIMES:
        if p <= c:
            continue
        if p >= SMALL:
            break
        small.setdefault(pattern_small(p, c), p)
    for r in range(1, 5040):
        if math.gcd(r, 5040) == 1:
            res.setdefault(pattern_residue(r, c), ("residue", r))
    return small, res


def all_patterns(c):
    small, res = split_patterns(c)
    pats = dict(res)
    pats.update(small)  # prefer an explicit prime as witness
    return pats


def exponent(pat):
    return 1 + sum(k * L for k, L in pat)


table = {}
for c in range(2, C9 + 1):
    pats = all_patterns(c)
    best = max(pats, key=lambda q: (exponent(q), -(pats[q] if isinstance(pats[q], int) else 10 ** 9)))
    sp, rp = split_patterns(c)
    big = max(exponent(q) for q in rp)
    small = max(exponent(q) for q in sp)
    table[c] = {"E1": exponent(best), "attained_at": pats[best], "pattern": best,
                "max_over_exhaustive_range": small, "max_over_residue_classes_p_ge_26244": big,
                "published_1+sum d*ceil(log2(d+1))": 1 + sum(d * (d).bit_length() for d in range(2, c + 1))}


def G(k, a):
    return k ** (k * (k - 1) // 2) * (a + 1) ** k


def arity(pat_entry, a):
    k, L = pat_entry
    return a + 1 if k == 1 else G(k, a) ** L


def worst_product(c, g_by_d, pmin):
    pats = {}
    for p in PRIMES:
        if p >= SMALL:
            break
        if p > c and p >= pmin:
            pats.setdefault(pattern_small(p, c), p)
    for pat, w in split_patterns(c)[1].items():
        pats.setdefault(pat, w)
    best = None
    for pat, w in pats.items():
        prod = 1
        for d, e in zip(range(2, c + 1), pat):
            prod *= arity(e, g_by_d[d])
        if best is None or prod > best[0]:
            best = (prod, w, pat)
    return best


profile_g = {2: 17, 3: 16, 4: 14, 5: 12, 6: 9, 7: 6, 8: 3, 9: 1}
prod9, w9, pat9 = worst_product(9, profile_g, 11)
Q9 = 9 * 20 * prod9
# p = 43 instance
pat43 = pattern_small(43, 9)
prod43 = 1
for d, e in zip(range(2, 10), pat43):
    prod43 *= arity(e, profile_g[d])
# published
pub = 1
for d in range(2, 10):
    pub *= G(d, profile_g[d]) ** d.bit_length()
profile = {"worst_prime_or_class": w9, "worst_pattern": pat9,
           "log2_Q_new": math.log2(Q9), "original_queries_ceil_log2_new": (Q9 - 1).bit_length(),
           "log2_Q_p43": math.log2(9 * 20 * prod43), "p43_pattern": pat43,
           "log2_Q_published": math.log2(9 * 20 * pub), "original_queries_ceil_log2_published": (9 * 20 * pub - 1).bit_length()}
# solver calls and attempts under the generator's randomized-restart model (eps = 1/3)
def tree(arities_top_down):
    counts, leaves = [], 1
    for a in reversed(arities_top_down):
        counts.append(leaves)
        leaves *= a
    return leaves, sum(counts)


ar_top = [arity(e, profile_g[d]) for d, e in reversed(list(zip(range(2, 10), pat9)))]
leaves, stage = tree(ar_top)
samples = 20
solvers = samples * stage
instruments = samples * leaves + solvers + samples
solver_error = Fraction(1, 3) / (3 * solvers)
restarts = 0
while Fraction(1, 2 ** restarts) > solver_error:
    restarts += 1
profile["sde_attempts_per_call_new"] = restarts
profile["instrument_calls_ceil_log2_new"] = (instruments - 1).bit_length()
# envelope at b = 104
b = 104
envg = {d: b for d in range(2, 10)}
prodE, wE, patE = worst_product(9, envg, 10)
cap = b * (b + 1)
slack = 0
while 2 ** slack < Fraction(12 * cap, 1) / Fraction(1, 3):
    slack += 1
qE = cap * 9 * (b + slack) * prodE
envelope = {"worst": wE, "pattern": patE, "large_prime_original_queries_ceil_log2_new": (qE - 1).bit_length(),
            "large_prime_query_dimension_exponent_new": 2 + table[9]["E1"]}

# crossover table, read-only import of the 2026-11-02 script
spec = importlib.util.spec_from_file_location(
    "classical_lb", ROOT / "research/audits/reviews/2026-11-02-rees-classical-lower-bound/classical_lb.py")
CL = importlib.util.module_from_spec(spec)
sys.path.insert(0, str(spec.origin and Path(spec.origin).parent))
spec.loader.exec_module(CL)


def closed_Q_int(p, m, eps_num=1, eps_den=3):  # copy of birthday_crossover.closed_Q_int
    t = 0
    while p ** t * eps_num < 2 * eps_den:
        t += 1
    ln = math.log(2 * eps_den / eps_num)
    w = max(2 * (1 + t), 15)
    return 5 * (m + t) + 16 * math.ceil(ln) + CL.isqrt_ceil(2 * w * p ** (m - 1))


fams = [("Heisenberg", 2, 3, {2: 1}), ("filiform", 3, 4, {2: 2, 3: 1}),
        ("free, two generators", 3, 5, {2: 3, 3: 2}), ("Dixmier--Lister", 3, 8, {2: 4, 3: 2}),
        ("class-9 profile", 9, 19, profile_g)]
cross = []
for name, c, m, g in fams:
    prod, w, pat = worst_product(c, g, 11)
    Qq = c * (m + 1) * prod  # tau = 1 for p >= 11 at eps = 1/3
    old = CL.quantum_schedule1(c, m, [None] + [g[d] for d in range(2, c + 1)], 11)
    # crossover(): smallest prime with classical LB > Qq (same predicate as classical_lb.crossover)
    def ok(x):
        return CL.classical_lb(x, m) > Qq
    hi = 11
    while not ok(hi):
        hi *= 2
    lo = 11
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid + 1
    px = lo
    while not CL.is_prime(px):
        px += 1
    lo2, hi2 = 11, 11
    while closed_Q_int(hi2, m) < Qq:
        hi2 *= 2
    while lo2 < hi2:
        mid = (lo2 + hi2) // 2
        if closed_Q_int(mid, m) >= Qq:
            hi2 = mid
        else:
            lo2 = mid + 1
    row = {"family": name, "worst": w, "pattern": pat, "log2_Q_old": round(math.log2(old), 2),
           "log2_Q_new": round(math.log2(Qq), 2), "Q_new": str(Qq),
           "LB_crossover_prime": str(px) if px < 10 ** 12 else None, "log2_LB_crossover": round(math.log2(px), 2),
           "birthday_below": str(lo2) if lo2 < 10 ** 12 else None, "log2_birthday_below": round(math.log2(lo2), 2)}
    if m <= 8 or px < 2 ** 200:
        row["ehk_copies_at_crossover"] = CL.ehk_copies(px, m)
    cross.append(row)

out = {"checks": checks, "E1_table": {str(k): {kk: (list(vv) if isinstance(vv, tuple) else vv) for kk, vv in v.items()}
                                     for k, v in table.items()},
       "profile": profile, "envelope_b104": envelope, "crossover": cross}
(HERE / "verify_headline.json").write_text(json.dumps(out, indent=1, default=str) + "\n")
print(json.dumps(out, indent=1, default=str))
