"""Item C: free nilpotent Lie ring ranks (Witt) against Sage, and the outer-envelope arithmetic.

Run: /opt/anaconda3/envs/qsearch-cas/bin/python research/audits/reviews/2026-11-02-rees-extensions/C/rank_and_envelope_check.py
"""
import itertools, json, math
from sage.all import LieAlgebra, QQ, moebius, divisors


def witt_rank(s, c):
    return sum(sum(moebius(d) * s ** (k // d) for d in divisors(k)) // k for k in range(1, c + 1))


rows = []
for s, c in [(2, 2), (2, 3), (2, 4), (3, 3), (4, 3), (2, 5), (3, 4)]:
    L = LieAlgebra(QQ, s, step=c)  # free nilpotent Lie algebra
    rows.append((s, c, witt_rank(s, c), L.dimension(), sum(s ** j for j in range(1, c + 1))))
print("(s, c, Witt rank, Sage dim, T=sum s^j)")
for r in rows:
    print(r, "OK" if r[2] == r[3] <= r[4] else "MISMATCH")

# outer envelope arithmetic (rees_hsp_reduction.json, large_prime_outer_envelope)
env = json.load(open("research/reductions/rees_hsp_reduction.json"))["large_prime_outer_envelope"]
b, c = env["encoding_bits"], env["fixed_class_bound"]
S = sum(d * math.ceil(math.log2(d + 1)) for d in range(2, c + 1))
print("b(b+1) =", b * (b + 1), "json:", env["large_prime_call_cap"])
print("3 + sum d*ceil(log2(d+1)) =", 3 + S, "json:", env["large_prime_query_dimension_exponent"], "(core 1+sum =", 1 + S, ")")
# convexity: per-Sylow r_i(r_i+1) summed <= b(b+1) whenever sum r_i <= b
ok = all(sum(r * (r + 1) for r in parts) <= sum(parts) * (sum(parts) + 1)
         for n in range(1, 13) for k in range(1, 5)
         for parts in itertools.product(range(n + 1), repeat=k) if sum(parts) == n)
print("sum r_i(r_i+1) <= b(b+1) for all splits, b<=12, <=4 Sylows:", ok)
# free-route sizes vs b: composition length of the cover F_{s,c} over Z/p^e is e*d
for s_, c_, e_ in [(2, 3, 2), (4, 3, 2), (2, 9, 1), (4, 9, 1)]:
    d = witt_rank(s_, c_)
    print(f"free route s={s_} c={c_} e={e_}: d={d}, log_p|F|=e*d={e_*d}")
