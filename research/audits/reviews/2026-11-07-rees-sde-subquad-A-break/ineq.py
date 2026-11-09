"""Exact check of the count lemmas of subquad-A section 3 with my own D_J (brute force from the
definition), J = 2..12, r <= RMAX, and the least slack of each.  Also the T_m(c) inequality
F(r) - F(r-m) > r - 1 for m >= J - 1, and the variant C = max(2, J - 3).  Usage: ineq.py RMAX"""
import sys

from algt import DJ

RMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 400


def F(r, J, C):
    return DJ(r, J) + C * r if r > 0 else 0


def run(J, C, label, tsmax):
    c = 2 * (J - 1)
    least = {}
    bad = []

    def rec(name, val, ctx):
        if name not in least or val < least[name][0]:
            least[name] = (val, ctx)
        if val < 0 and len(bad) < 5:
            bad.append((name, val, ctx))
    for r in range(1, RMAX + 1):
        rec("F_increasing", F(r, J, C) - F(r - 1, J, C) - 1, (r,))
        # (C1)
        for m in range(0, r + 1):
            t = m // (J - 1)
            rec("C1", DJ(r, J) - DJ(r - m, J) - (t * (r + 1) - (J - 1) * t * (t - 1) // 2), (r, m))
        for q in range(1, (r - 2) // 2 + 1):
            # (Y): 1 <= b <= q, r >= q + b
            for b in range(1, min(q, r - q) + 1):
                rec("Y", b + (C - 1) * r + DJ(q, J) - q - F(b, J, C), (r, q, b))
            # (I1): c+1 <= m <= q, r >= 2q+2
            for m in range(c + 1, q + 1):
                lhs = (m - 1) + ((m - 1) // c) * (r + 1 - c) + (r - 1)
                rec("I1", F(r, J, C) - F(r - m, J, C) - lhs, (r, q, m))
        for m in range(2 * (J - 1), (r - 2) // 2 + 1):
            rec("I2", F(r, J, C) - F(r - m, J, C) - (r - 1), (r, m))
        for m in range(1, tsmax + 1):
            if 2 * m + 2 > r:
                break
            for mp in range(1, m + 1):
                rec("TS", F(r, J, C) - F(r - mp, J, C) - (m + mp), (r, m, mp))
        for m in range(J - 1, (r - 2) // 2 + 1):
            rec("Tmc", F(r, J, C) - F(r - m, J, C) - r, (r, m))
    print(label, "J=%d C=%d c=%d" % (J, C, c),
          {k: v[0] for k, v in sorted(least.items())}, "BAD" if bad else "", bad[:3], flush=True)


for J in range(2, 13):
    run(J, max(2, 2 * J - 4), "theorem", 2 * J - 3)
for J in range(4, 13):
    run(J, max(2, J - 3), "sideC", J - 2)
