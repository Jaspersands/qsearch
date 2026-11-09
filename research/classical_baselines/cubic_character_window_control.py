"""Exact, finite falsifier for a cubic character interpolation attack.

Run with /opt/anaconda3/envs/qsearch-cas/bin/python.  The attack receives
only p queried character values. Secret coefficients are confined to the
test harness. This control makes no asymptotic rank or speedup claim.
"""
import json
from collections import Counter
from pathlib import Path

from sage.all import GF, PolynomialRing, matrix, vector


def attack(field, answers):
    p = field.order()
    h = (p - 1) // 2
    ring = PolynomialRing(field, "x")
    poly = ring.lagrange_polynomial([(field(a), answers[a]) for a in range(p)])
    rows, rhs = [], []
    for n in range(h + 3, p - 1):
        rows.append([(n - 1 - 2 * h) * poly[n - 1],
                     (n - h) * poly[n], (n + 1) * poly[n + 1]])
        rhs.append(-(n - 2 - 3 * h) * poly[n - 2])
    mat = matrix(field, rows)
    rank = mat.rank()
    solution = mat.solve_right(vector(field, rhs))
    return rank, solution, poly, mat, vector(field, rhs)


def run(p):
    field = GF(p)
    ring = PolynomialRing(field, "x")
    x = ring.gen()
    h = (p - 1) // 2
    counts = Counter()
    examples = []
    checked = 0
    for b in field:
        for c in field:
            for d in field:
                q = x**3 + b*x**2 + c*x + d
                if not q.is_irreducible():
                    continue
                answers = [q(field(a))**h for a in range(p)]
                rank, solution, poly, mat, rhs = attack(field, answers)
                counts[rank] += 1
                power = q**h
                assert all(poly[j] == power[j] for j in range(h + 1, p))
                assert mat * vector(field, [b, c, d]) == rhs
                if rank == 3:
                    assert solution == vector(field, [b, c, d])
                elif len(examples) < 3:
                    examples.append({"bcd": [int(b), int(c), int(d)],
                                     "rank": int(rank),
                                     "kernel": [[int(v) for v in row]
                                                for row in mat.right_kernel().basis()]})
                checked += 1
    assert checked == (p**3-p)//3
    return {"p": p, "checked_irreducibles": checked,
            "oracle_queries_per_input": p,
            "rank_counts": {str(k): v for k, v in sorted(counts.items())},
            "deficient_examples": examples}


if __name__ == "__main__":
    result = {"scope": "Exact finite control only; no uniform rank theorem",
              "interpolation": "Sage Lagrange; no fast-runtime claim",
              "results": []}
    for p in (13, 17, 19):
        row = run(p)
        result["results"].append(row)
        print(json.dumps(row), flush=True)
    Path(__file__).with_suffix(".json").write_text(json.dumps(result, indent=2) + "\n")
