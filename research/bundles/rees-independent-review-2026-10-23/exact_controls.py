"""Independent, bounded controls for the frozen Rees proof; no repository imports.

Arithmetic is exact in Q[w]/(w^2+w+1). Run with python3 -B exact_controls.py.
This program prints results and does not write files.
"""

from fractions import Fraction as F
from itertools import product
import json


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def mul(a, b):
    return (a[0] * b[0] - a[1] * b[1],
            a[0] * b[1] + a[1] * b[0] - a[1] * b[1])


def scale(a, x):
    return (a[0] * x, a[1] * x)


ZERO = (F(0), F(0))
ONE = (F(1), F(0))
ROOTS = (ONE, (F(0), F(1)), (F(-1), F(-1)))


def root(k):
    return ROOTS[k % 3]


def inv(a):
    return tuple(-x % 3 for x in a)


def convolution(a, b, group_mul):
    out = {}
    for x, cx in a.items():
        for y, cy in b.items():
            z = group_mul(x, y)
            out[z] = add(out.get(z, ZERO), mul(cx, cy))
    return {x: c for x, c in out.items() if c != ZERO}


def branch_states(elements, hidden, central, group_mul):
    identity = elements[0]
    size = len(elements)
    rho = {h: scale(ONE, F(1, size)) for h in hidden}
    rank = len(central[0][0])
    branches = {}
    masses = {}
    for label in product(range(3), repeat=rank):
        projector = {
            z: scale(root(-sum(a * b for a, b in zip(label, coord))),
                     F(1, len(central)))
            for coord, z in central
        }
        # Use the full two-sided measurement, not the proposed trace formula.
        projected = convolution(convolution(projector, rho, group_mul),
                                projector, group_mul)
        mass = scale(projected.get(identity, ZERO), size)
        assert mass[1] == 0 and mass[0] >= 0
        masses[label] = mass[0]
        if mass != ZERO:
            branches[label] = {
                g: scale(projected.get(inv(g), ZERO), size / mass[0])
                for g in elements
            }
        else:
            assert not projected
    assert sum(masses.values()) == 1
    return branches, masses


def all_record_control(elements, hidden, central, quotient, section,
                       group_mul, dilation, hidden_quotient):
    branches, masses = branch_states(elements, hidden, central, group_mul)
    k_size = sum(z in hidden for _, z in central)
    assert set(m for m in masses.values() if m) == {F(k_size, len(central))}
    hz = {group_mul(h, z) for h in hidden for _, z in central}
    rank = len(central[0][0])
    tuples_checked = witnesses_checked = moments_checked = entries_checked = 0
    first_output = None
    for labels in product(branches, repeat=3):
        tuples_checked += 1
        found = False
        for scales in product(range(3), repeat=3):
            if not any(scales):
                continue
            if any(sum(s * s * label[j] for s, label in zip(scales, labels)) % 3
                   for j in range(rank)):
                continue
            found = True
            witnesses_checked += 1
            moments = {}
            for g in elements:
                value = ONE
                for label, s in zip(labels, scales):
                    if s:
                        value = mul(value, branches[label][dilation(s, g)])
                assert value == (ONE if g in hz else ZERO)
                moments[g] = value
                moments_checked += 1
            output = {}
            for q in quotient:
                for r in quotient:
                    g = group_mul(inv(section(r)), section(q))
                    value = scale(moments[g], F(1, len(quotient)))
                    diff = tuple((a - b) % 3 for a, b in zip(q, r))
                    expected = scale(ONE, F(1, len(quotient))) if diff in hidden_quotient else ZERO
                    assert value == expected
                    output[q, r] = value
                    entries_checked += 1
            if first_output is None:
                first_output = output
            else:
                assert output == first_output
        assert found
    # The forbidden all-zero witness loses the support test.
    assert any(g not in hz for g in elements)
    return {
        "group_order": len(elements),
        "hidden_order": len(hidden),
        "central_order": len(central),
        "intersection_order": k_size,
        "positive_labels": len(branches),
        "forbidden_labels": len(masses) - len(branches),
        "complete_label_tuples": tuples_checked,
        "all_valid_witnesses": witnesses_checked,
        "exact_moment_checks": moments_checked,
        "exact_output_entry_checks": entries_checked,
        "zero_witness_negative_control": "fails as required",
    }, first_output


def rees_control():
    base = list(product(range(3), repeat=3))
    cover = list(product(range(3), repeat=4))

    def base_mul(a, b):
        x, y, z = a
        X, Y, Z = b
        return ((x + X) % 3, (y + Y) % 3,
                (z + Z + 2 * (x * Y - y * X)) % 3)

    def cover_mul(a, b):
        x, y, z, u = a
        X, Y, Z, U = b
        return ((x + X) % 3, (y + Y) % 3, (z + Z) % 3,
                (u + U + 2 * (x * Y - y * X)) % 3)

    def evaluate(s, a):
        x, y, z, u = a
        return (s * x % 3, s * y % 3, (s * z + s * s * u) % 3)

    hidden_base = {(a, 0, a) for a in range(3)}
    hidden_cover = {(a, 0, a, 0) for a in range(3)}
    labels = {g: min(base_mul(g, h) for h in hidden_base) for g in base}
    tuple_labels = {g: tuple(labels[evaluate(s, g)] for s in (1, 2)) for g in cover}
    for a in cover:
        for b in cover:
            delta = cover_mul(inv(b), a)
            equality = tuple_labels[a] == tuple_labels[b]
            assert equality == (delta in hidden_cover)
            # This is the independently evaluated copy-only overlap kernel.
            overlap = all(base_mul(inv(evaluate(s, b)), evaluate(s, a)) in hidden_base
                          for s in (1, 2))
            assert overlap == equality
            for s in (1, 2):
                assert evaluate(s, cover_mul(a, b)) == base_mul(evaluate(s, a), evaluate(s, b))
    assert any(base_mul(base_mul(g, h), inv(g)) not in hidden_base
               for g in base for h in hidden_base)
    # An intentionally nonhomomorphic public section.
    section = lambda q: (*q, (q[0] * q[1] + q[2]) % 3)
    central = [((u,), (0, 0, 0, u)) for u in range(3)]
    dilation = lambda s, g: (s * g[0] % 3, s * g[1] % 3, s * g[2] % 3, s * s * g[3] % 3)
    result, output = all_record_control(cover, hidden_cover, central, base, section,
                                        cover_mul, dilation, hidden_base)
    distribution = {}
    for freq in base:
        probability = ZERO
        for q in base:
            for r in base:
                exponent = sum(k * (b - a) for k, a, b in zip(freq, q, r))
                probability = add(probability, mul(root(exponent), output[q, r]))
        probability = scale(probability, F(1, len(base)))
        assert probability == (scale(ONE, F(1, 9)) if (freq[0] + freq[2]) % 3 == 0 else ZERO)
        distribution[freq] = probability
    recovered = [h for h in base if all(sum(a * b for a, b in zip(h, freq)) % 3 == 0
                                       for freq, mass in distribution.items() if mass != ZERO)]
    assert set(recovered) == hidden_base
    result.update({"tuple_fiber_and_copy_overlap_pairs": len(cover) ** 2,
                   "evaluation_homomorphism_checks": 2 * len(cover) ** 2,
                   "fourier_support_size": 9,
                   "recovered_hidden_elements": recovered})
    return result


def intersection_control():
    elements = list(product(range(3), repeat=4))

    def group_mul(a, b):
        x, y, z, w = a
        X, Y, Z, W = b
        return ((x + X) % 3, (y + Y) % 3,
                (z + Z + 2 * (x * Y - y * X)) % 3, (w + W) % 3)

    hidden = {(x, 0, z, z) for x in range(3) for z in range(3)}
    central = [((z, w), (0, 0, z, w)) for z in range(3) for w in range(3)]
    quotient = list(product(range(3), repeat=2))
    section = lambda q: (*q, q[0] * q[1] % 3, (q[0] + 2 * q[1]) % 3)
    dilation = lambda s, g: (s * g[0] % 3, s * g[1] % 3, s * s * g[2] % 3, s * s * g[3] % 3)
    assert any(group_mul(group_mul(g, h), inv(g)) not in hidden
               for g in elements for h in hidden)
    result, _ = all_record_control(elements, hidden, central, quotient, section,
                                   group_mul, dilation, {(x, 0) for x in range(3)})
    # H >= Z forces the zero label rather than a low acceptance probability.
    containing = {(x, 0, z, w) for x in range(3) for z in range(3) for w in range(3)}
    branches, masses = branch_states(elements, containing, central, group_mul)
    assert set(branches) == {(0, 0)} and masses[0, 0] == 1
    result["contains_center_control"] = "only zero label, mass one"
    return result


if __name__ == "__main__":
    print(json.dumps({"arithmetic": "exact rational cyclotomic Q[zeta_3]",
                      "rees_nonnormal_line": rees_control(),
                      "diagonal_central_intersection": intersection_control(),
                      "status": "all bounded controls passed; not a universal proof"}, indent=2))
