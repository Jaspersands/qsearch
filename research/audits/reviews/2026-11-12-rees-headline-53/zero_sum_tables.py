#!/opt/anaconda3/bin/python
"""Full-version numbers under the zero-sum-depth Schedule 1 (AI-run, pending human review).

Run from the repo root:
    nice -n 19 /opt/anaconda3/bin/python research/audits/reviews/2026-11-12-rees-headline-53/zero_sum_tables.py

Uses theorems/rees_hsp_reduction.py (zero_sum_length, schedule1_zero_sum_depth) for t(p, kappa).
  (1) E_1(c) = max_{p>c} 1 + sum_d kappa_d L_d (Schedule 1 alone) and E_W(c), the combined rule of
      main.tex rem:combined-schedule (linear at kappa_d = 1, Schedule 2 at p >= 16 kappa^(2kappa+2),
      else Schedule 1 at degree kappa_d), each at full depth (control: must reproduce the published
      5,11,23,38,56,77,109,145 and 5,11,23,38,56,77,107,143) and at zero-sum depth.
      For p >= 4c^4 the Schedule 1 depth depends only on p mod N; e_d is non-increasing in p inside a
      class (Schedule 2 grades only switch on), so the class maximum is at its least prime >= 4c^4.
  (2) The bb-envelope comparison numbers of main.tex (l. 1085: 2^2186, 2^1833, 2^603) under the new depth.
Finite computation only.
"""
import json
import math
import sys
from math import gcd, log2
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
from flint import fmpz  # noqa: E402
from theorems.rees_hsp_reduction import schedule1_zero_sum_depth  # noqa: E402

HERE = Path(__file__).resolve().parent


def is_prime(n):
    return n >= 2 and fmpz(n).is_prime()


def full_depth(k):
    return k.bit_length()  # ceil(log2(k+1))


def grade(rule, depth, p, d):
    """(kappa, exponent e_d, arity function a -> M_d)."""
    if rule == "S1pub":  # published thm:main: degree d, full depth, no reduction
        e = d * full_depth(d)
        return d, e, (lambda a, d=d: (d ** (d * (d - 1) // 2) * (a + 1) ** d) ** full_depth(d))
    k = gcd(d, p - 1)
    if k == 1:
        return 1, 1, (lambda a: a + 1)
    if rule == "W" and p >= 16 * k ** (2 * k + 2):
        return k, 2, (lambda a, k=k: (a + 1) * ((k - 1) * a + 1))
    L = full_depth(k) if depth == "full" else schedule1_zero_sum_depth(p, d)[1]
    return k, k * L, (lambda a, k=k, L=L: (k ** (k * (k - 1) // 2) * (a + 1) ** k) ** L)


def candidates(c):
    """Primes c < p < 4c^4, plus the least prime >= 4c^4 in every unit class mod N."""
    bound = 4 * c ** 4
    out = [p for p in range(c + 1, bound) if is_prime(p)]
    N = 1
    for d in range(2, c + 1):
        N = N * d // gcd(N, d)
    N = N * 2 ** c.bit_length() // gcd(N, 2 ** c.bit_length())
    for r in range(1, N + 1):
        if gcd(r, N) != 1:
            continue
        p = r + N * max(0, -(-(bound - r) // N))
        while not is_prime(p):
            p += N
        out.append(p)
    return sorted(set(out))


def E(rule, depth, c):
    best = (0, None)
    for p in candidates(c):
        v = 1 + sum(grade(rule, depth, p, d)[1] for d in range(2, c + 1))
        if v > best[0]:
            best = (v, p)
    return best


tables = {}
for rule, depth in (("S1", "full"), ("W", "full"), ("S1", "zero_sum"), ("W", "zero_sum")):
    tables[f"{rule}_{depth}"] = {c: E(rule, depth, c) for c in range(2, 10)}
assert [tables["S1_full"][c][0] for c in range(2, 10)] == [5, 11, 23, 38, 56, 77, 109, 145]
assert [tables["W_full"][c][0] for c in range(2, 10)] == [5, 11, 23, 38, 56, 77, 107, 143]
assert [tables["S1_zero_sum"][c][0] for c in range(2, 10)] == [5, 8, 16, 19, 35, 36, 44, 53]

# (2) bb-envelope comparison (cf. 2026-11-02-rees-bb-envelope/bb_envelope_check.py, section C)
EPS_INV = 3


def ceil_log(base, x):
    k, v = 0, 1
    while v < x:
        v *= base
        k += 1
    return k


def core_queries(rule, depth, p, grades, t):
    c, m = len(grades), grades[0]
    P = 1
    for d in range(2, c + 1):
        if grades[d - 1] == 0:
            continue
        P *= grade(rule, depth, p, d)[2](grades[d - 1])
    return c * (m + t) * P


def sylow_simple(rule, depth, p, n, c, t):
    return n * core_queries(rule, depth, p, (n,) * c, t)


def sylow_exact(rule, depth, p, n, c, t):
    return sum(core_queries(rule, depth, p, (n - j,) * c, t) for j in range(n))


b, c = 104, 9
slack = ceil_log(2, 12 * b * EPS_INV)
bb = {}
# reproduce the published figures first (controls)
q = sylow_simple("S1pub", "full", 43, b, c, slack)
bb["control_S1pub_p43_simple_log2"] = round(log2(q), 1)
assert abs(log2(q) - 2186.4) < 0.05
profile = (19, 17, 16, 14, 12, 9, 6, 3, 1)
t43 = ceil_log(43, 12 * 104 * EPS_INV)
bb["control_S1pub_p43_np19_exact_log2"] = round(log2(sylow_exact("S1pub", "full", 43, 19, 9, t43)), 1)
bb["control_W_full_p43_np19_exact_log2"] = round(log2(sylow_exact("W", "full", 43, 19, 9, t43)), 1)
assert bb["control_S1pub_p43_np19_exact_log2"] == 1832.8 and bb["control_W_full_p43_np19_exact_log2"] == 602.5
# new depth: at p = 43 and worst case over all p > 9 (candidates)
bb["S1t_p43_simple_log2"] = round(log2(sylow_simple("S1", "zero_sum", 43, b, c, slack)), 1)
worst = max(candidates(9), key=lambda p: sylow_simple("S1", "zero_sum", p, b, c, slack))
bb["S1t_worst_prime"] = worst
bb["S1t_worst_simple_log2"] = round(log2(sylow_simple("S1", "zero_sum", worst, b, c, slack)), 1)
bb["S1t_worst_exact_log2"] = round(log2(sylow_exact("S1", "zero_sum", worst, b, c, slack)), 1)
bb["S1t_p43_np19_exact_log2"] = round(log2(sylow_exact("S1", "zero_sum", 43, 19, 9, t43)), 1)
bb["Wt_p43_np19_exact_log2"] = round(log2(sylow_exact("W", "zero_sum", 43, 19, 9, t43)), 1)
bb["S1t_p43_profile_call_log2"] = round(log2(core_queries("S1", "zero_sum", 43, profile, t43)), 1)

out = {"exponent_tables": {k: {str(c): {"E": v[0], "attained_at": v[1]} for c, v in tab.items()}
                           for k, tab in tables.items()},
       "bb_envelope": bb}
(HERE / "zero_sum_tables.json").write_text(json.dumps(out, indent=1) + "\n")
print(json.dumps(out, indent=1))
