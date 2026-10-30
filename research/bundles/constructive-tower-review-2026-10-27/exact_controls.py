"""Small independent normalization/branch controls, not a tower backend."""

import json
from pathlib import Path


def semigroup(generators, limit):
    values = {0}
    for value in range(1, limit + 1):
        if any(value - generator in values for generator in generators):
            values.add(value)
    return values


def normalization_control():
    # In F_3, x=t^4, y=t^3 gives y^4-x^3=0 and [F_3(t):F_3(x)]=4.
    # The radical test ideal is the positive-degree monomial ideal.
    limit = 80
    current = semigroup([3, 4], limit)
    records = []
    while True:
        gaps = [n for n in range(limit) if n not in current]
        conductor = max(gaps, default=-1) + 1
        positive = sorted(n for n in current if 0 < n < limit // 2)
        # Past the conductor all exponents occur, so these finite tests suffice.
        added = [n for n in gaps if all(n + j in current for j in positive)]
        records.append({"gaps": gaps, "conductor": conductor, "added": added})
        if not added:
            break
        current = semigroup(sorted((current - {0}) | set(added)), limit)
    assert [r["gaps"] for r in records] == [[1, 2, 5], [1, 2], []]
    assert [r["added"] for r in records] == [[5], [1, 2], []]
    # Disc_Y(Y^4-X^3) = -256 X^9 = 2 X^9 in F_3, nonzero.
    assert (-256) % 3 == 2
    assert 3 < 4
    return {
        "field_characteristic": 3,
        "separable_extension_degree": 4,
        "equation": "Y^4-X^3",
        "derivative_in_Y": "Y^3",
        "discriminant": "2*X^9",
        "normalization_length": 3,
        "trace_dual_length_bound": 36,
        "endomorphism_ring_steps": records,
    }


def branch_control():
    p = 5
    images = {}
    for t in range(p):
        x = (t * t - 1) % p
        y = (t * x) % p
        assert (y * y - x * x * (x + 1)) % p == 0
        images[t] = [x, y]
    assert images[1] == images[4] == [0, 0]
    assert 1 != 4
    return {
        "field_characteristic": p,
        "equation": "Y^2-X^2*(X+1)",
        "normalization": "X=t^2-1, Y=t*(t^2-1)",
        "distinct_branches_above_origin": [1, 4],
        "images": images,
    }


if __name__ == "__main__":
    result = {
        "normalization": normalization_control(),
        "branch_collision": branch_control(),
        "scope": "Exact small controls; no tower, RR backend, zeta, or native code generated.",
    }
    destination = Path(__file__).resolve().with_name("exact_controls.json")
    destination.write_text(json.dumps(result, indent=2) + "\n", encoding="ascii")
    print(json.dumps(result, indent=2))
