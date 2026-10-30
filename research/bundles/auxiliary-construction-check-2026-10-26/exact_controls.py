"""Exact controls, not a curve implementation or an asymptotic proof."""

from fractions import Fraction as F
from itertools import product
from math import isqrt, prod
from random import Random
import json
from pathlib import Path

from sympy import Matrix, eye
from sympy.matrices.normalforms import hermite_normal_form


def binary_solve(rows, width, rhs=None):
    """Return one solution and a kernel basis over F_2, or None."""
    rhs = [0] * len(rows) if rhs is None else rhs
    work = [[int(x) & 1 for x in row] + [int(y) & 1]
            for row, y in zip(rows, rhs)]
    pivots = []
    for col in range(width):
        pivot = next((i for i in range(len(pivots), len(work))
                      if work[i][col]), None)
        if pivot is None:
            continue
        r = len(pivots)
        work[r], work[pivot] = work[pivot], work[r]
        for i in range(len(work)):
            if i != r and work[i][col]:
                work[i] = [a ^ b for a, b in zip(work[i], work[r])]
        pivots.append(col)
    if any(not any(row[:width]) and row[width] for row in work):
        return None
    particular = [0] * width
    for r, col in enumerate(pivots):
        particular[col] = work[r][width]
    basis = []
    for free in sorted(set(range(width)) - set(pivots)):
        v = [0] * width
        v[free] = 1
        for r, col in enumerate(pivots):
            v[col] = work[r][free]
        basis.append(v)
    return particular, basis


class TwoGroup:
    def __init__(self, moduli):
        self.moduli = moduli
        self.order = prod(moduli)
        self.s = self.order.bit_length() - 1
        assert self.order == 2 ** self.s
        self.zero = tuple(0 for _ in moduli)
        self.rng = Random(20261026)
        self.pair_calls = 0

    def combine(self, generators, coefficients):
        return tuple(sum(int(a) * v[j] for a, v in zip(coefficients, generators)) % m
                     for j, m in enumerate(self.moduli))

    def sample(self):
        return tuple(self.rng.randrange(m) for m in self.moduli)

    def pair(self, torsion, point):
        self.pair_calls += 1
        assert all(2 * t % m == 0 for t, m in zip(torsion, self.moduli))
        return sum((t // (m // 2)) * (y % 2)
                   for t, y, m in zip(torsion, point, self.moduli)) % 2

    def verified_relations(self, torsion):
        rows = []
        for _ in range(256):
            kernel = binary_solve(rows, len(torsion))[1]
            if all(self.combine(torsion, v) == self.zero for v in kernel):
                return kernel
            y = self.sample()
            rows.append([self.pair(t, y) for t in torsion])
        raise AssertionError("Control-only guard exceeded")


def relation_lattice(group, generators):
    t = len(generators)
    lattice = (2 ** group.s) * eye(t)
    steps = 0
    while True:
        # B*u is even precisely when B*u/2 represents an element of (Z^t/L)[2].
        binary_kernel = binary_solve(lattice.tolist(), t)[1]
        lifts = [lattice * Matrix(u) / 2 for u in binary_kernel]
        assert all(x.q == 1 for v in lifts for x in v)
        lifts = [Matrix(v.rows, 1, [int(x) for x in v]) for v in lifts]
        torsion = [group.combine(generators, v) for v in lifts]
        kernel = group.verified_relations(torsion)
        if not kernel:
            break
        additions = [sum((a * v for a, v in zip(u, lifts)), Matrix.zeros(t, 1))
                     for u in kernel]
        old_det = int(lattice.det())
        lattice = hermite_normal_form(Matrix.hstack(lattice, *additions))
        assert 0 < int(lattice.det()) < old_det
        assert all(group.combine(generators, lattice[:, j]) == group.zero
                   for j in range(t))
        steps += 1
        assert steps <= group.s * t
    return lattice, steps


def exact_generated_subgroup(group, generators):
    found = {group.zero}
    todo = [group.zero]
    while todo:
        point = todo.pop()
        for generator in generators:
            new = group.combine([point, generator], [1, 1])
            if new not in found:
                found.add(new)
                todo.append(new)
    return found


def lattice_controls():
    fixtures = [
        ([2], [(1,), (0,)]),
        ([4], [(1,), (3,)]),
        ([4, 2], [(1, 1), (2, 1), (3, 0)]),
        ([8, 4], [(1, 1), (2, 1), (3, 2)]),
        ([4, 2, 2], [(1, 1, 0), (0, 1, 1), (0, 0, 1), (1, 0, 0)]),
        ([8, 4], [(2, 2), (4, 0), (0, 2)]),
    ]
    results = []
    for moduli, generators in fixtures:
        group = TwoGroup(moduli)
        expected = exact_generated_subgroup(group, generators)
        lattice, steps = relation_lattice(group, generators)
        assert int(lattice.det()) == len(expected)
        tested = 0
        if len(expected) == group.order:
            for x in product(*(range(m) for m in moduli)):
                extended = generators + [x]
                relations, _ = relation_lattice(group, extended)
                unit = [0] * len(generators) + [1]
                solved = binary_solve(relations.tolist(), len(extended), unit)
                halves = [y for y in expected if group.combine([y], [2]) == x]
                assert (solved is not None) == bool(halves)
                if solved is not None:
                    v = (Matrix(unit) + relations * Matrix(solved[0])) / 2
                    assert all(a.q == 1 for a in v)
                    half = group.combine(extended, v)
                    assert group.combine([half], [2]) == x
                tested += 1
        results.append({"moduli": moduli, "generated_order": len(expected),
                        "lattice_index": int(lattice.det()), "strict_stages": steps,
                        "targets_checked": tested, "pair_calls": group.pair_calls})

    # Restricting the second pairing argument to the current subgroup can fail.
    c4 = TwoGroup([4])
    assert c4.pair((2,), (0,)) == c4.pair((2,), (2,)) == 0
    assert c4.pair((2,), (1,)) == 1
    c4c2 = TwoGroup([4, 2])
    assert all(c4c2.combine([x], [4]) == c4c2.zero
               for x in product(range(4), range(2)))
    # The target can have a half in H but not in its own cyclic subgroup.
    assert c4.combine([(1,)], [2]) == (2,)
    assert all(c4.combine([x], [2]) != (2,) for x in [(0,), (2,)])

    # Check the odd-part recombination formula in C_4 x C_6, of order 24=8*3.
    moduli, M = [4, 6], 3
    combine = lambda a, x: tuple(a * v % m for v, m in zip(x, moduli))
    points = list(product(range(4), range(6)))
    primary = [x for x in points if combine(8, x) == (0, 0)]
    for x in points:
        us = [u for u in primary if combine(2, u) == combine(M, x)]
        assert bool(us) == any(combine(2, y) == x for y in points)
        for u in us:
            y = tuple((v - ((M - 1) // 2) * w) % m
                      for v, w, m in zip(u, x, moduli))
            assert combine(2, y) == x
    return {"fixtures": results, "countercontrols": 3, "mixed_order_targets": 24}


def birthday_controls():
    results = []
    for n in [4, 16, 64]:
        length = isqrt(n)
        epsilon = F(1, 4 * length)
        mu = [F(1, n) * (1 - epsilon) + (epsilon if x == 0 else 0)
              for x in range(n)]
        for character in range(1, n):
            coefficient = sum(p * (-1) ** ((x & character).bit_count())
                              for x, p in enumerate(mu))
            assert coefficient == epsilon
        ratios = []
        success = []
        for target in range(n):
            p = sum(mu[x] * mu[target ^ x] for x in range(n))
            sx = sum(mu[x] * mu[target ^ x] ** 2 for x in range(n))
            sy = sum(mu[x] ** 2 * mu[target ^ x] for x in range(n))
            ez = length ** 2 * p
            ez2 = (ez + length ** 2 * (length - 1) ** 2 * p ** 2
                   + length ** 2 * (length - 1) * (sx + sy))
            claimed = ez + ez ** 2 + length ** 3 * p * (F(2, n) + 2 * epsilon)
            assert p >= F(15, 16 * n)
            assert ez2 <= claimed
            assert ez2 / ez ** 2 < 5
            ratios.append(ez2 / ez ** 2)
            if n == 4:
                probability = F(0)
                enumerated_ez = F(0)
                enumerated_ez2 = F(0)
                for entries in product(range(n), repeat=2 * length):
                    weight = prod(mu[x] for x in entries)
                    z = sum((x ^ y) == target for x in entries[:length]
                            for y in entries[length:])
                    probability += weight * bool(z)
                    enumerated_ez += weight * z
                    enumerated_ez2 += weight * z * z
                assert enumerated_ez == ez and enumerated_ez2 == ez2
                assert probability >= ez ** 2 / ez2 > F(1, 5)
                success.append(str(probability))
        results.append({"N": n, "L": length, "epsilon": str(epsilon),
                        "max_exact_second_moment_ratio": str(max(ratios)),
                        "exhaustive_success_probabilities": success})
    return results


def cutoff_controls():
    q = 100003
    rows = []
    for e in [8, 16, 32, 64]:
        g, a = 5 * e + 1, 2 * e - 9
        n = 2 ** (2 * g)
        constant = lambda degree: (g + 1) * (degree + 6)
        single = F(q ** a, (2 * n * constant(a)) ** 2)
        birthday = [F(q ** degree, 64 * constant(degree) ** 2 * n)
                    for degree in [a // 2, (a + 1) // 2]]
        rows.append({"e": e, "single_pass": single > 1,
                     "single_ratio_floor": single.numerator // single.denominator,
                     "birthday_pass": [x > 1 for x in birthday],
                     "birthday_ratio_floors": [x.numerator // x.denominator
                                               for x in birthday]})
    assert rows[1]["single_pass"] and all(rows[2]["birthday_pass"])
    return rows


if __name__ == "__main__":
    report = {"status": "passed", "cutoffs": cutoff_controls(),
              "birthday": birthday_controls(), "lattice": lattice_controls()}
    destination = Path(__file__).resolve().parent / "exact_controls.json"
    destination.write_text(json.dumps(report, indent=2) + "\n", encoding="ascii")
    print(json.dumps(report, indent=2))
