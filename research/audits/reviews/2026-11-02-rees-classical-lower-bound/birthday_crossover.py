"""Largest prime below which the proved birthday bound Q(1/3) is < the Schedule-1 count.

Also the line-case exact birthday constant: min Q with 1-prod(1-i/M) >= 2/3,
compared with sqrt(2 ln 3 M). Output birthday_crossover.json.
"""
import json, math
from pathlib import Path
import classical_lb as C

def closed_Q_int(p, m, eps_num=1, eps_den=3):
    # integer-safe version of closed_form_Q for huge p (t = 1 once p >= 6)
    t = 0
    while p ** t * eps_num < 2 * eps_den: t += 1
    ln = math.log(2 * eps_den / eps_num)
    # 8 ln 6 = 14.33... < 15; use the rational upper bound 15 (only enlarges Q)
    w = max(2 * (1 + t), 15)
    return 5 * (m + t) + 16 * math.ceil(ln) + C.isqrt_ceil(2 * w * p ** (m - 1))

fams = [("Heisenberg", 2, 3, [3, 1]), ("filiform class 3", 3, 4, [4, 2, 1]),
        ("free 2-generator class 3", 3, 5, [5, 3, 2]), ("Dixmier-Lister", 3, 8, [8, 4, 2]),
        ("class-9 profile", 9, 19, [19, 17, 16, 14, 12, 9, 6, 3, 1])]
out = []
for name, c, m, g in fams:
    Qq = C.quantum_schedule1(c, m, g, 11)
    lo, hi = 11, 11
    while closed_Q_int(hi, m) < Qq: hi *= 2
    while lo < hi:  # first p with closed_Q >= Qq
        mid = (lo + hi) // 2
        if closed_Q_int(mid, m) >= Qq: hi = mid
        else: lo = mid + 1
    out.append({"family": name, "log2_quantum": round(math.log2(Qq), 2),
                "birthday_beats_quantum_for_p_below_log2": round(math.log2(lo), 2),
                "birthday_beats_quantum_for_p_below": str(lo) if lo < 10 ** 12 else None})
def line_success_float(Q, p, m):
    """Birthday success for H of order p: sum_e Pr[E=e](1-p^-e), float DP."""
    M = p ** (m - 1)
    dist = [1.0] + [0.0] * Q  # dist[d] = Pr[d occupied]
    for j in range(Q):
        nd = [0.0] * (Q + 1)
        for d in range(j + 1):
            if dist[d]:
                nd[d] += dist[d] * d / M
                if d < M: nd[d + 1] += dist[d] * (M - d) / M
        dist = nd
    return sum(pr * (1 - p ** -(Q - d)) for d, pr in enumerate(dist) if pr)

lines = []
for p, m in [(3, 3), (5, 3), (7, 3), (5, 4), (101, 3), (1009, 3)]:
    Q = 1
    while line_success_float(Q, p, m) < 2 / 3: Q += 1
    M = p ** (m - 1)
    lines.append({"p": p, "m": m, "Q_min_line_H": Q, "ratio_to_sqrt(p^(m-1))": round(Q / math.sqrt(M), 4),
                  "q_lower_bound": C.q_union_bound((p ** m - 1) // (p - 1)),
                  "sqrt(2ln3)": round(math.sqrt(2 * math.log(3)), 4),
                  "sqrt(4/3)": round(math.sqrt(4 / 3), 4)})
res = {"crossover": out, "line_case_constant": lines}
Path("birthday_crossover.json").write_text(json.dumps(res, indent=1) + "\n")
print(json.dumps(res, indent=1))
