"""Exact small-instance controls for the signed cluster comparator.

No circuit search, thermal oracle, or scalable implementation is claimed.
The randomized draw is explicit; exhaustive expectations are guarded controls.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache
import hashlib
from itertools import combinations, product
import json
import math
from pathlib import Path
import random


@dataclass(frozen=True)
class Host:
    neighbors: tuple[tuple[int, ...], ...]

    @classmethod
    def create(cls, m, edges):
        if type(m) is not int or m < 1:
            raise ValueError("positive integer vertex count required")
        adj = [set() for _ in range(m)]
        for i, j in edges:
            if any(type(v) is not int or not 0 <= v < m for v in (i, j)) or i == j:
                raise ValueError("invalid edge")
            if j in adj[i]:
                raise ValueError("duplicate edge")
            adj[i].add(j)
            adj[j].add(i)
        return cls(tuple(tuple(sorted(a)) for a in adj))

    @property
    def m(self):
        return len(self.neighbors)

    @property
    def slots(self):
        return 1 + max(map(len, self.neighbors))

    def touches(self, left, right):
        return any(v in right or any(u in right for u in self.neighbors[v]) for v in left)

    def induced(self, vertices):
        return tuple(tuple(int(j in self.neighbors[i]) for j in vertices) for i in vertices)


def determinant(matrix):
    """Fraction-free elimination, with exact row pivoting."""
    a = [list(row) for row in matrix]
    n = len(a)
    if n == 0:
        return 1
    sign, previous = 1, 1
    for k in range(n - 1):
        if a[k][k] == 0:
            pivot = next((r for r in range(k + 1, n) if a[r][k]), None)
            if pivot is None:
                return 0
            a[k], a[pivot] = a[pivot], a[k]
            sign *= -1
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = a[i][j] * a[k][k] - a[i][k] * a[k][j]
                quotient, remainder = divmod(numerator, previous)
                if remainder:
                    raise ArithmeticError("non-exact Bareiss division")
                a[i][j] = quotient
        previous = a[k][k]
        for i in range(k + 1, n):
            a[i][k] = 0
    return sign * a[-1][-1]


@lru_cache(None)
def tree_count(adjacency):
    k = len(adjacency)
    if k == 0:
        return 0
    lap = [[sum(adjacency[i]) if i == j else -adjacency[i][j]
            for j in range(k - 1)] for i in range(k - 1)]
    return determinant(lap)


@lru_cache(None)
def ursell(adjacency):
    k = len(adjacency)
    if k == 0:
        return 0
    independent, phi = [1] * (1 << k), [0] * (1 << k)
    for mask in range(1, 1 << k):
        vertices = [i for i in range(k) if mask >> i & 1]
        independent[mask] = int(not any(adjacency[i][j] for i, j in combinations(vertices, 2)))
        anchor = mask & -mask
        value, part = independent[mask], (mask - 1) & mask
        while part:
            if part & anchor:
                value -= phi[part] * independent[mask ^ part]
            part = (part - 1) & mask
        phi[mask] = value
    return phi[-1]


def prufer_tree(size, sequence):
    if size == 1:
        return ()
    degree = [1] * size
    for v in sequence:
        degree[v] += 1
    edges = []
    for v in sequence:
        leaf = next(i for i, x in enumerate(degree) if x == 1)
        edges.append((leaf, v))
        degree[leaf] -= 1
        degree[v] -= 1
    edges.append(tuple(i for i, x in enumerate(degree) if x == 1))
    return tuple(edges)


def rooted_order(size, edges):
    visited, order = {0}, []
    while len(visited) < size:
        changed = False
        for u, v in edges:
            if (u in visited) != (v in visited):
                if v in visited:
                    u, v = v, u
                order.append((u, v))
                visited.add(v)
                changed = True
        if not changed:
            raise ValueError("tree is disconnected")
    return tuple(order)


def compositions(total):
    for cuts in product((0, 1), repeat=total - 1):
        sizes = [1]
        for cut in cuts:
            if cut:
                sizes.append(1)
            else:
                sizes[-1] += 1
        yield tuple(sizes)


def block_graph(host, sets):
    return tuple(tuple(int(i != j and host.touches(left, right))
                       for j, right in enumerate(sets)) for i, left in enumerate(sets))


class Reference:
    def __init__(self, host, activity):
        self.host, self.activity = host, activity

    def root_weight(self, vertices):
        size = len(vertices)
        trees = tree_count(self.host.induced(vertices))
        if trees == 0:
            raise ValueError("rooted polymer must be connected")
        cayley = 1 if size == 1 else size ** (size - 2)
        return self.activity(vertices) * F(cayley * self.host.slots ** (size - 1),
                                          math.factorial(size - 1) * trees)

    def draw_root(self, root, size, rng):
        if size > self.host.m:
            return None
        sequence = [rng.randrange(size) for _ in range(max(0, size - 2))]
        order = rooted_order(size, prufer_tree(size, sequence))
        labels, used = {0: root}, {root}
        for parent, child in order:
            neighbors = self.host.neighbors[labels[parent]]
            slot = rng.randrange(self.host.slots)
            if slot >= len(neighbors) or neighbors[slot] in used:
                return None
            labels[child] = neighbors[slot]
            used.add(neighbors[slot])
        vertices = tuple(sorted(used))
        return vertices, self.root_weight(vertices)

    def draw_touch(self, vertex, size, rng):
        closed = (vertex,) + self.host.neighbors[vertex]
        slot = rng.randrange(self.host.slots)
        if slot >= len(closed):
            return None
        out = self.draw_root(closed[slot], size, rng)
        if out is None:
            return None
        vertices, weight = out
        count = len(set(closed).intersection(vertices))
        return vertices, weight * F(self.host.slots, count)

    def draw(self, limit, rng):
        if type(limit) is not int or limit < 1:
            raise ValueError("positive truncation required")
        draw, h = rng.randrange((1 << limit) - 1), 1
        while draw >= 1 << (limit - h):
            draw -= 1 << (limit - h)
            h += 1
        sizes = [1]
        for _ in range(h - 1):
            if rng.randrange(2):
                sizes.append(1)
            else:
                sizes[-1] += 1
        k = len(sizes)
        sequence = []
        for _ in range(max(0, k - 2)):
            pick = rng.randrange(h)
            for i, size in enumerate(sizes):
                if pick < size:
                    sequence.append(i)
                    break
                pick -= size
        order = rooted_order(k, prufer_tree(k, sequence))
        root = self.draw_root(rng.randrange(self.host.m), sizes[0], rng)
        if root is None:
            return F(0)
        sets, weights = {0: root[0]}, {0: root[1]}
        for parent, child in order:
            v = rng.choice(sets[parent])
            out = self.draw_touch(v, sizes[child], rng)
            if out is None:
                return F(0)
            sets[child], weights[child] = out
        return self.value(h, limit, sizes, order, sets, weights)

    def value(self, h, limit, sizes, order, sets, weights):
        k = len(sizes)
        matrix = block_graph(self.host, [sets[i] for i in range(k)])
        mass = 1 if k == 1 else sizes[0] * h ** (k - 2)
        p_h = F(1 << (limit - h), (1 << limit) - 1)
        value = F(self.host.m * (1 << (h - 1)) * mass,
                  math.factorial(k) * sizes[0]) / p_h
        value *= F(ursell(matrix), tree_count(matrix))
        for parent, child in order:
            contacts = sum(self.host.touches((v,), sets[child]) for v in sets[parent])
            value /= contacts
        return value * math.prod(weights.values())

    @lru_cache(None)
    def root_outcomes(self, root, size):
        if self.host.m > 4 or size > 4:
            raise ValueError("exhaustive reference limited to four vertices/order")
        if size > self.host.m:
            return ()
        counts = defaultdict(int)
        cayley = 1 if size == 1 else size ** (size - 2)
        for sequence in product(range(size), repeat=max(0, size - 2)):
            order = rooted_order(size, prufer_tree(size, sequence))
            for slots in product(range(self.host.slots), repeat=size - 1):
                labels, used = {0: root}, {root}
                for (parent, child), slot in zip(order, slots):
                    neighbors = self.host.neighbors[labels[parent]]
                    if slot >= len(neighbors) or neighbors[slot] in used:
                        break
                    labels[child] = neighbors[slot]
                    used.add(neighbors[slot])
                else:
                    counts[tuple(sorted(used))] += 1
        denominator = cayley * self.host.slots ** (size - 1)
        return tuple((s, self.root_weight(s), F(count, denominator))
                     for s, count in sorted(counts.items()))

    @lru_cache(None)
    def touch_outcomes(self, vertex, size):
        closed = (vertex,) + self.host.neighbors[vertex]
        rows = []
        for root in closed:
            for vertices, weight, probability in self.root_outcomes(root, size):
                count = len(set(closed).intersection(vertices))
                rows.append((vertices, weight * F(self.host.slots, count),
                             probability / self.host.slots))
        return tuple(rows)

    def exact_draw_mean(self, limit):
        if not 1 <= limit <= 4 or self.host.m > 4:
            raise ValueError("exhaustive reference limited to four vertices/order")
        answer = F(0)
        for h in range(1, limit + 1):
            p_h = F(1 << (limit - h), (1 << limit) - 1)
            for sizes in compositions(h):
                k = len(sizes)
                for seq in product(range(k), repeat=max(0, k - 2)):
                    order = rooted_order(k, prufer_tree(k, seq))
                    p_tree = math.prod((F(sizes[i], h) for i in seq), start=F(1))
                    base_p = p_h * p_tree / ((1 << (h - 1)) * self.host.m)

                    def descend(position, sets, weights, probability):
                        if position == len(order):
                            return probability * self.value(h, limit, sizes, order, sets, weights)
                        parent, child = order[position]
                        total = F(0)
                        for vertex in sets[parent]:
                            for s, y, p in self.touch_outcomes(vertex, sizes[child]):
                                total += descend(position + 1, {**sets, child: s},
                                                 {**weights, child: y},
                                                 probability * p / sizes[parent])
                        return total

                    for root in range(self.host.m):
                        for s, y, p in self.root_outcomes(root, sizes[0]):
                            answer += descend(0, {0: s}, {0: y}, base_p * p)
        return answer


def connected_sets(host):
    if host.m > 4:
        raise ValueError("catalog is a four-vertex reference, not the scalable sampler")
    return [s for k in range(1, host.m + 1) for s in combinations(range(host.m), k)
            if tree_count(host.induced(s))]


def direct_cluster_sum(host, activities, limit):
    """Independent ordered-tuple definition, no tree-sampling weights."""
    answer = F(0)
    for k in range(1, limit + 1):
        for sets in product(activities, repeat=k):
            if sum(map(len, sets)) <= limit:
                answer += F(ursell(block_graph(host, sets)), math.factorial(k)) * math.prod(
                    activities[s] for s in sets)
    return answer


def even_activity(host, vertices, beta, couplings, tolerance=F(1, 10**24)):
    """Rational word-series reference, with an absolute analytic tail bound."""
    if not 1 <= len(vertices) <= 4 or tolerance <= 0:
        raise ValueError("small positive-precision reference required")
    beta = F(beta)
    js = tuple(F(couplings[i]) for i in vertices)
    if beta < 0:
        raise ValueError("beta must be nonnegative")
    masks = [sum(1 << j for j in range(i) if vertices[j] in host.neighbors[vertices[i]])
             for i in range(len(vertices))]
    scale = beta * sum(map(abs, js))
    if scale == 0:
        return F(0), F(0), 0
    state, value, majorant = {(0, 0): F(1)}, F(0), F(1)
    full = (1 << len(vertices)) - 1
    for order in range(1, 200):
        following = defaultdict(F)
        for (seen, parity), coefficient in state.items():
            for i, ji in enumerate(js):
                sign = -1 if (parity & masks[i]).bit_count() % 2 else 1
                following[seen | (1 << i), parity ^ (1 << i)] += (
                    -beta * ji * sign * coefficient / order)
        state = following
        value += state.get((full, 0), F(0))
        majorant *= scale / order
        if order + 2 > scale:
            tail = majorant * scale / (order + 1) / (1 - scale / (order + 2))
            if tail <= tolerance:
                return value, tail, order
    raise ValueError("reference Taylor cap reached; no result admitted")


def field_partition(host, vertices, beta, couplings, fields, tolerance=F(1, 10**24)):
    """Restricted doubled-word reference; rational Taylor approximation + tail."""
    if len(vertices) > 4 or tolerance <= 0:
        raise ValueError("small positive-precision reference required")
    beta = F(beta)
    if beta < 0 or any(not -1 <= F(t) <= 1 for t in fields):
        raise ValueError("nonnegative beta and fields in [-1,1] required")
    if not vertices:
        return F(1), F(0)
    js = tuple(F(couplings[i]) for i in vertices)
    masks = [sum(1 << j for j in range(i) if vertices[j] in host.neighbors[vertices[i]])
             for i in range(len(vertices))]
    scale = beta * sum(map(abs, js)) / 2
    if scale == 0:
        return F(1), F(0)
    state = [F(0)] * (1 << len(vertices))
    state[0] = F(1)
    coefficients, majorant = state[:], F(1)
    norm_upper = 3**math.ceil(scale)
    for order in range(1, 200):
        following = [F(0)] * len(state)
        for parity, coefficient in enumerate(state):
            for i, ji in enumerate(js):
                sign = -1 if (parity & masks[i]).bit_count() % 2 else 1
                following[parity ^ (1 << i)] += -beta * ji * sign * coefficient / (2 * order)
        state = following
        coefficients = [a + b for a, b in zip(coefficients, state)]
        majorant *= scale / order
        if order + 2 > scale:
            tail = majorant * scale / (order + 1) / (1 - scale / (order + 2))
            error = tail * (2 * norm_upper + tail)
            if error <= tolerance:
                value = sum(a*a * math.prod(F(fields[v]) for i, v in enumerate(vertices)
                                            if parity >> i & 1)
                            for parity, a in enumerate(coefficients))
                return value, error
    raise ValueError("reference Taylor cap reached; no result admitted")


def field_activity(host, vertices, beta, couplings, fields, tolerance=F(1, 10**24)):
    value, error = F(0), F(0)
    for size in range(len(vertices) + 1):
        for subset in combinations(vertices, size):
            term, bound = field_partition(host, subset, beta, couplings, fields,
                                          tolerance / (1 << len(vertices)))
            value += (-1)**(len(vertices) - size) * term
            error += bound
    return value, error


def parameter_ledger(m, degree, beta, jmax=F(1), epsilon=F(1, 100), delta=F(1, 100)):
    if type(m) is not int or type(degree) is not int or not 0 <= degree < m:
        raise ValueError("invalid graph parameters")
    beta, jmax, epsilon, delta = map(F, (beta, jmax, epsilon, delta))
    if beta < 0 or not 0 <= jmax <= 1 or not 0 < epsilon < 1 or not 0 < delta < 1:
        raise ValueError("invalid temperature/coupling/error parameters")
    lam, slots = (beta * jmax)**2, degree + 1
    admitted = slots * lam <= F(1, 64)
    limit = max(1, math.ceil(math.log(4 * m / float(epsilon), 4)))
    return {"m": m, "degree": degree, "lambda": str(lam),
            "D_lambda": str(slots * lam), "local_theorem_regime": admitted,
            "tail_bound": float(F(m) * (16 * slots * lam)**(limit + 1) /
                                (2 * slots * (1 - 16 * slots * lam))) if admitted else None,
            "truncation": limit, "quantum_gap_certified": False,
            "pilot_sampling_dequantized": False, "independently_reviewed": False,
            "production_fpras_implemented": False}


def receipt():
    controls = []
    for name, edges in (("commuting", ()), ("path", ((0, 1), (1, 2))),
                        ("triangle", ((0, 1), (0, 2), (1, 2)))):
        host = Host.create(3, edges)
        beta, js = F(1, 16), (F(1), F(-1, 2), F(3, 4))
        activities, tails = {}, []
        for s in connected_sets(host):
            activities[s], tail, _ = even_activity(host, s, beta, js)
            tails.append(tail)
        ref = Reference(host, activities.__getitem__)
        exact = ref.exact_draw_mean(3)
        direct = direct_cluster_sum(host, activities, 3)
        rng = random.Random(24024)
        draws = [float(ref.draw(3, rng)) for _ in range(4000)]
        controls.append({"name": name, "exact_unbiasedness": exact == direct,
                         "truncated_log_z": float(direct),
                         "maximum_activity_tail": float(max(tails)),
                         "diagnostic_draws": len(draws),
                         "diagnostic_sample_mean": math.fsum(draws) / len(draws),
                         "diagnostic_max_abs_draw": max(map(abs, draws)),
                         "sample_mean_is_not_a_proof": True})
    field_controls = []
    host = Host.create(3, ((0, 1), (1, 2)))
    beta, js = F(1, 16), (F(1), F(-1, 2), F(3, 4))
    for name, fields in (("zero_pins", (0, 1, 0)), ("parity", (-1, 1, -1)),
                         ("total_parity", (-1, -1, -1)), ("fractional", (F(1, 3), F(-2, 3), 0))):
        activities = {s: field_activity(host, s, beta, js, fields)[0] for s in connected_sets(host)}
        exact_mean = Reference(host, activities.__getitem__).exact_draw_mean(3)
        direct = direct_cluster_sum(host, activities, 3)
        z, error = field_partition(host, (0, 1, 2), beta, js, fields)
        field_controls.append({"name": name, "fields": list(map(str, fields)),
                               "exact_unbiasedness": exact_mean == direct,
                               "partition_reference": float(z), "reference_error": float(error),
                               "truncated_log_partition": float(direct),
                               "log_reference_residual": abs(float(direct) - math.log(float(z))),
                               "full_pilot_sampler_implemented": False})
    here = Path(__file__).resolve().parent
    return {"status": "local_unreviewed_classical_comparator", "controls": controls,
            "field_controls": field_controls,
            "parameter_ledgers": [parameter_ledger(10**6, d, F(1, b))
                                  for d, b in ((1, 16), (99, 128), (9999, 1024), (9999, 128))],
            "hashes": {name: hashlib.sha256((here / name).read_bytes()).hexdigest()
                       for name in ("cluster_baseline.py", "test_cluster_baseline.py",
                                    "CLUSTER_BASELINE.md", "HANDOFF.md")}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("receipt.json"))
    args = parser.parse_args()
    data = receipt()
    args.output.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"controls": len(data["controls"]),
                      "all_exact_unbiasedness": all(r["exact_unbiasedness"] for r in data["controls"]),
                      "output": str(args.output.resolve())}))
