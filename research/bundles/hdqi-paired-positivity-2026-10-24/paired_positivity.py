"""Exact paired-support falsifiers, not a pilot sampler or hardness test."""

from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import math


@dataclass(frozen=True)
class Graph:
    vertices: int
    edges: tuple
    lower: tuple

    @classmethod
    def create(cls, vertices, edges):
        if type(vertices) is not int or not 1 <= vertices <= 4096:
            raise ValueError("explicit graph must have 1 through 4096 vertices")
        normalized = set()
        for edge in edges:
            if (len(edge) != 2 or any(type(v) is not int or not 0 <= v < vertices for v in edge)
                    or edge[0] == edge[1]):
                raise ValueError("simple graph edge required")
            pair = tuple(sorted(edge))
            if pair in normalized:
                raise ValueError("duplicate edge")
            normalized.add(pair)
        normalized = tuple(sorted(normalized))
        lower = [0] * vertices
        for j, i in normalized:
            lower[i] |= 1 << j
        return cls(vertices, normalized, tuple(lower))

    @property
    def full(self):
        return (1 << self.vertices) - 1

    @property
    def degree(self):
        degrees = [0] * self.vertices
        for a, b in self.edges:
            degrees[a] += 1
            degrees[b] += 1
        return max(degrees)

    def mask(self, mask):
        if type(mask) is not int or not 0 <= mask <= self.full:
            raise ValueError("mask outside graph register")
        return mask


def witness_graph():
    return Graph.create(6, [(0, 1), (0, 2), (1, 3), (2, 4), (2, 5), (3, 5)])


def extended_witness(vertices):
    """Connected arbitrarily extendible family; the fixed leaf carries a tail."""
    if type(vertices) is not int or not 6 <= vertices <= 4096:
        raise ValueError("extension size must be in 6..4096")
    edges = list(witness_graph().edges)
    if vertices > 6:
        edges += [(4, 6)] + [(i, i + 1) for i in range(6, vertices - 1)]
    permutation = (5, 3, 2, 1, 4, 0) + tuple(range(6, vertices))
    return Graph.create(vertices, edges), permutation


def power_coefficients(graph, active, label, order):
    """Integers <label|H_active^k|0>, with unit couplings, 0<=k<=order."""
    graph.mask(active)
    graph.mask(label)
    if graph.vertices > 8:
        raise ValueError("dense exact powers limited to eight vertices")
    if type(order) is not int or not 0 <= order <= 64:
        raise ValueError("power reference order must be in 0..64")
    vector = [0] * (1 << graph.vertices)
    vector[0] = 1
    coefficients = []
    generators = [i for i in range(graph.vertices) if active >> i & 1]
    for _ in range(order + 1):
        coefficients.append(vector[label])
        following = [0] * len(vector)
        for mask, value in enumerate(vector):
            if value:
                for i in generators:
                    following[mask ^ (1 << i)] += (-1)**((graph.lower[i] & mask).bit_count()) * value
        vector = following
    return tuple(coefficients)


@dataclass(frozen=True)
class Interval:
    lower: F
    upper: F

    def square(self):
        a, b = self.lower**2, self.upper**2
        return Interval(F(0) if self.lower <= 0 <= self.upper else min(a, b), max(a, b))


def amplitude_interval(graph, active, label, time, order=20):
    """Certified Taylor interval for <label|exp(-time H_active)|0>."""
    graph.mask(active)
    graph.mask(label)
    time = F(time)
    if time < 0:
        raise ValueError("nonnegative imaginary time required")
    coefficients = power_coefficients(graph, active, label, order)
    center = sum((F(value) * (-time)**k / math.factorial(k)
                  for k, value in enumerate(coefficients)), F(0))
    norm_time = active.bit_count() * time
    ratio = norm_time / (order + 2)
    if ratio >= 1:
        raise ValueError("Taylor tail ratio is not contractive; raise the capped order")
    tail = norm_time**(order + 1) / math.factorial(order + 1) / (1 - ratio)
    return Interval(center - tail, center + tail)


def paired_activity_interval(graph, support, label, time, order=20):
    """Moebius sum of squared restricted amplitudes, with rational endpoints."""
    graph.mask(support)
    graph.mask(label)
    if label & ~support:
        raise ValueError("label must be contained in visit support")
    free = support ^ label
    lower, upper, subset = F(0), F(0), free
    while True:
        active = subset | label
        square = amplitude_interval(graph, active, label, time, order).square()
        if (support ^ active).bit_count() % 2:
            lower -= square.upper
            upper -= square.lower
        else:
            lower += square.lower
            upper += square.upper
        if subset == 0:
            break
        subset = (subset - 1) & free
    return Interval(lower, upper)


def _amplitude_recurrence(graph):
    @lru_cache(None)
    def coefficient(count):
        degree = sum(count)
        if degree == 0:
            return F(1)
        label = sum((k % 2) << i for i, k in enumerate(count))
        answer = F(0)
        for i, multiplicity in enumerate(count):
            if multiplicity:
                previous = list(count)
                previous[i] -= 1
                answer -= (-1)**((graph.lower[i] & label).bit_count()) * coefficient(tuple(previous)) / degree
        return answer
    return coefficient


def multivariate_amplitude(graph, cap):
    """Coefficient of prod_i z_i^cap_i in exp(-sum z_i O_i)|0>.

    Its only possible label is cap modulo two. Complexity is exponential
    in the supplied caps, guarded before populating the recurrence cache.
    """
    cap = tuple(cap)
    if (len(cap) != graph.vertices or any(type(k) is not int or k < 0 for k in cap)
            or math.prod(k + 1 for k in cap) > 100000 or sum(cap) > 64):
        raise ValueError("multivariate coefficient exceeds exact reference budget")
    return _amplitude_recurrence(graph)(cap)


def leading_paired_coefficients(graph):
    """Coefficient at total multiplicity two at every vertex, for all labels."""
    if graph.vertices > 8:
        raise ValueError("leading paired coefficient census limited to eight vertices")
    a = _amplitude_recurrence(graph)
    answers = [F(0) for _ in range(1 << graph.vertices)]
    for count in product(range(3), repeat=graph.vertices):
        label = sum((k % 2) << i for i, k in enumerate(count))
        answers[label] += a(count) * a(tuple(2 - k for k in count))
    return tuple(answers)


def symmetry_image(graph, permutation, label):
    """Exact ordered-word image under a supplied graph automorphism.

    This checks a supplied unit-coupling symmetry, not graph isomorphism.
    Returns the new label and its sign from reordering generator images.
    """
    graph.mask(label)
    permutation = tuple(permutation)
    if any(type(v) is not int for v in permutation) or sorted(permutation) != list(range(graph.vertices)):
        raise ValueError("permutation of graph vertices required")
    image_edges = {tuple(sorted((permutation[i], permutation[j]))) for i, j in graph.edges}
    if image_edges != set(graph.edges):
        raise ValueError("supplied permutation does not preserve the graph")
    images = [permutation[i] for i in range(graph.vertices) if label >> i & 1]
    inversions = sum(a > b and tuple(sorted((a, b))) in graph.edges
                     for k, a in enumerate(images) for b in images[k + 1:])
    return sum(1 << i for i in images), (-1)**inversions


def symmetry_zero_certificate(graph, permutation, label):
    image, sign = symmetry_image(graph, permutation, label)
    return {"label": label, "image": image, "image_sign": sign,
            "identically_zero_for_unit_couplings": image == label and sign == -1,
            "coupling_scope": "all unit couplings only; weighted symmetries must be rechecked"}


def witness_certificate(time=F(1, 64)):
    graph, label = witness_graph(), 30
    time = F(time)
    if not 0 < time <= F(1, 64):
        raise ValueError("analytic witness range is 0 < beta/2 <= 1/64")
    symmetry = symmetry_zero_certificate(graph, (5, 3, 2, 1, 4, 0), label)
    interval = paired_activity_interval(graph, graph.full, label, time)
    leading = leading_paired_coefficients(graph)[label]
    ratio = F(45 * 5**8, math.factorial(8) * 64**2) * F(64, 59)
    amplitude_lower = F(7, 8) * time**6 / 45
    analytic_upper = -2 * amplitude_lower**2
    if not (symmetry["identically_zero_for_unit_couplings"] and leading == -F(2, 2025)
            and ratio < F(1, 8) and interval.upper < 0):
        raise AssertionError("paired-support witness did not certify")
    return {"vertices": graph.vertices, "edges": graph.edges, "couplings": [1] * graph.vertices,
            "label": label, "occupied_vertices": [1, 2, 3, 4], "visit_support": graph.full,
            "beta": str(2 * time), "time_beta_over_two": str(time),
            "degree_scale": str((graph.degree + 1) * (2 * time)**2),
            "analytic_beta_range": "0 < beta <= 1/32",
            "symmetry": symmetry, "leading_time_power": 12,
            "leading_time_coefficient": str(leading),
            "uniform_remainder_ratio_upper": str(ratio),
            "analytic_activity_upper": str(analytic_upper),
            "taylor_order": 20,
            "activity_interval": {"lower": str(interval.lower), "upper": str(interval.upper)},
            "negative_activity_certified": True,
            "decision": "reject_direct_nonnegative_paired_visit_support_sampler",
            "generic_classical_sampling_ruled_out": False,
            "quantum_advantage_established": False}
