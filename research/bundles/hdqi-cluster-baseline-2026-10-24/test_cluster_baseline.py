from fractions import Fraction as F
from itertools import combinations, product
import math
from pathlib import Path
import random
import sys

import numpy as np
import pytest
from scipy.linalg import expm

import cluster_baseline as c

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "hdqi-parent-gap-2026-10-23"))
from parent_gap import build_model


@pytest.mark.parametrize("n", (1, 2, 3, 4))
def test_complete_graph_tree_count_and_ursell(n):
    matrix = tuple(tuple(int(i != j) for j in range(n)) for i in range(n))
    assert c.tree_count(matrix) == (1 if n == 1 else n ** (n - 2))
    assert c.ursell(matrix) == (-1)**(n - 1) * math.factorial(n - 1)


def test_disconnected_graph_contributes_zero():
    adj = ((0, 1, 0), (1, 0, 0), (0, 0, 0))
    assert c.tree_count(adj) == c.ursell(adj) == 0


@pytest.mark.parametrize("edges", ((), ((0, 1),), ((0, 1), (1, 2)),
                                   ((0, 1), (0, 2), (1, 2))))
def test_primitive_sampler_is_exact_even_with_signed_activities(edges):
    host = c.Host.create(3, edges)
    activities = {s: F((-1)**sum(s), 100**len(s)) for s in c.connected_sets(host)}
    ref = c.Reference(host, activities.__getitem__)
    for v in range(3):
        for size in range(1, 4):
            for mode in ("root", "touch"):
                totals = {}
                for s, y, p in getattr(ref, mode + "_outcomes")(v, size):
                    totals[s] = totals.get(s, F(0)) + y * p
                expected = {s: w for s, w in activities.items() if len(s) == size and
                            (v in s if mode == "root" else host.touches((v,), s))}
                assert totals == expected


@pytest.mark.parametrize("edges", ((), ((0, 1),), ((0, 1), (1, 2)),
                                   ((0, 1), (0, 2), (1, 2))))
def test_full_cluster_draw_has_exact_expectation(edges):
    host = c.Host.create(3, edges)
    activities = {s: F((-1)**(sum(s) + 1), 128**len(s)) for s in c.connected_sets(host)}
    ref = c.Reference(host, activities.__getitem__)
    assert ref.exact_draw_mean(3) == c.direct_cluster_sum(host, activities, 3)


def test_repeated_polymers_and_factorials_are_not_dropped():
    host, w = c.Host.create(1, ()), F(1, 10)
    ref = c.Reference(host, lambda s: w)
    expected = sum((-1)**(k - 1) * w**k / k for k in range(1, 5))
    assert ref.exact_draw_mean(4) == expected
    assert expected != w


def test_host_triangle_embedding_multiplicity_is_not_one():
    host = c.Host.create(3, combinations(range(3), 2))
    ref = c.Reference(host, lambda s: F(1))
    vertices, weight, probability = ref.root_outcomes(0, 3)[0]
    assert vertices == (0, 1, 2)
    assert probability == F(2, 9)
    assert weight == F(9, 2)
    assert probability * weight == 1


def test_weighted_prufer_tree_mass_and_distribution():
    sizes = (1, 3, 2, 1)
    total = 0
    for seq in product(range(4), repeat=2):
        order = c.rooted_order(4, c.prufer_tree(4, seq))
        weight = math.prod(sizes[p] for p, _ in order)
        probability = math.prod(F(sizes[i], sum(sizes)) for i in seq)
        assert probability == F(weight, sizes[0] * sum(sizes)**2)
        total += weight
    assert total == sizes[0] * sum(sizes)**2


def test_tree_graph_bound_for_every_four_vertex_graph():
    pairs = tuple(combinations(range(4), 2))
    for bits in product((0, 1), repeat=len(pairs)):
        host = c.Host.create(4, [e for e, bit in zip(pairs, bits) if bit])
        matrix = host.induced(tuple(range(4)))
        assert abs(c.ursell(matrix)) <= c.tree_count(matrix)


def test_missing_touch_divisor_and_conditioning_on_success_are_biased():
    host = c.Host.create(3, combinations(range(3), 2))
    activity = F(1, 100)
    ref = c.Reference(host, lambda s: activity)
    outcomes = ref.touch_outcomes(0, 2)
    expected = sum(y * p for _, y, p in outcomes)
    wrong = sum(y * p * len(set(s).intersection((0, 1, 2))) for s, y, p in outcomes)
    success = sum(p for _, _, p in outcomes)
    assert expected == 3 * activity
    assert wrong == 2 * expected
    assert 0 < success < 1
    assert expected / success != expected


@pytest.mark.parametrize("edges", ((), ((0, 1), (1, 2)), ((0, 1), (0, 2), (1, 2))))
def test_even_word_activity_matches_independent_dense_inclusion_exclusion(edges):
    host, beta, js = c.Host.create(3, edges), F(1, 8), (F(1), F(-1, 2), F(3, 4))
    for vertices in c.connected_sets(host):
        value, tail, _ = c.even_activity(host, vertices, beta, js)
        dense = 0.0
        for size in range(len(vertices) + 1):
            for subset in combinations(vertices, size):
                if not subset:
                    z = 1
                else:
                    local_edges = [(i, j) for i, j in combinations(range(size), 2)
                                   if subset[j] in host.neighbors[subset[i]]]
                    h = build_model(size, local_edges, [float(js[i]) for i in subset]).h
                    z = np.trace(expm(-float(beta) * h)) / (1 << size)
                dense += (-1)**(len(vertices) - size) * z
        assert abs(float(value) - dense) < 2e-14
        assert tail < F(1, 10**24)
        assert abs(value) <= (beta * max(map(abs, js)))**(2 * len(vertices))


def test_nonredundancy_is_a_real_assumption():
    z = np.diag([1, -1])
    identity = np.eye(2)
    ops = (np.kron(z, identity), np.kron(identity, z), np.kron(z, z))
    assert np.trace(ops[0] @ ops[1] @ ops[2]) / 4 == 1
    canonical = build_model(3, [])
    assert np.trace(canonical.operators[0] @ canonical.operators[1] @ canonical.operators[2]) == 0
    beta = 1 / 16
    w = 0.0
    for k in range(4):
        for subset in combinations(range(3), k):
            z_value = 1 if not subset else np.trace(expm(-beta * sum(ops[i] for i in subset))) / 4
            w += (-1)**(3-k) * z_value
    assert w < 0
    assert abs(w) > beta**6


@pytest.mark.parametrize("edges", ((), ((0, 1), (1, 2)), ((0, 1), (0, 2), (1, 2))))
def test_truncated_classical_estimate_matches_full_dense_partition(edges):
    host, beta = c.Host.create(3, edges), F(1, 16)
    js = (F(1), F(-1, 2), F(3, 4))
    activities = {s: c.even_activity(host, s, beta, js)[0] for s in c.connected_sets(host)}
    estimate = float(c.direct_cluster_sum(host, activities, 3))
    matrix = build_model(3, edges, [float(j) for j in js]).h
    actual = math.log(np.trace(expm(-float(beta) * matrix)) / 8)
    radius = 16 * host.slots * beta**2
    tail = F(host.m, 2 * host.slots) * radius**4 / (1-radius)
    assert abs(estimate - actual) <= float(tail) + 1e-14
    assert abs(estimate - actual) < 1e-9


def test_exact_draw_bound_and_no_quantum_promotion():
    host = c.Host.create(3, ((0, 1), (1, 2)))
    lam = F(1, 256)
    ref = c.Reference(host, lambda s: (-1)**len(s) * lam**len(s))
    rng = random.Random(2026)
    for _ in range(500):
        assert abs(ref.draw(4, rng)) <= host.m
    ledger = c.parameter_ledger(10**6, 9999, F(1, 1024))
    assert ledger["local_theorem_regime"]
    assert not ledger["quantum_gap_certified"]
    assert not ledger["pilot_sampling_dequantized"]
    assert not ledger["production_fpras_implemented"]


def test_outside_regime_does_not_get_a_certificate():
    assert not c.parameter_ledger(100, 99, F(1, 2))["local_theorem_regime"]
    assert c.parameter_ledger(100, 99, F(1, 2))["tail_bound"] is None
    assert c.parameter_ledger(100, 99, F(0))["tail_bound"] == 0


def test_reference_guards_fail_instead_of_truncating_silently():
    with pytest.raises(ValueError):
        c.connected_sets(c.Host.create(5, ()))
    with pytest.raises(ValueError):
        c.Reference(c.Host.create(1, ()), lambda s: F(1)).exact_draw_mean(5)
    with pytest.raises(ValueError):
        c.Host.create(2, ((0, 1), (0, 1)))


@pytest.mark.parametrize("fields", ((1, 1, 1), (0, 1, 0), (-1, 1, -1),
                                    (-1, -1, -1), (F(1, 3), F(-2, 3), 0)))
def test_generating_function_matches_dense_pilot_and_cluster_draw(fields):
    host, beta, js = c.Host.create(3, ((0, 1), (1, 2))), F(1, 16), (F(1), F(-1, 2), F(3, 4))
    matrix = build_model(3, ((0, 1), (1, 2)), [float(j) for j in js]).h
    amplitudes = expm(-float(beta) * matrix / 2)[:, 0]
    dense = sum(a*a * math.prod(float(fields[i]) for i in range(3) if y >> i & 1)
                for y, a in enumerate(amplitudes))
    exact, error = c.field_partition(host, (0, 1, 2), beta, js, fields)
    assert abs(float(exact) - dense) < 1e-14
    assert error < F(1, 10**24)
    activities = {}
    for s in c.connected_sets(host):
        value, bound = c.field_activity(host, s, beta, js, fields)
        assert abs(value) <= beta**(2 * len(s)) + bound
        activities[s] = value
    ref = c.Reference(host, activities.__getitem__)
    assert ref.exact_draw_mean(3) == c.direct_cluster_sum(host, activities, 3)
    assert abs(float(ref.exact_draw_mean(3)) - math.log(dense)) < 1e-9


def test_all_negative_fields_have_exact_unit_partition():
    host = c.Host.create(3, ((0, 1), (1, 2)))
    value, error = c.field_partition(host, (0, 1, 2), F(1, 8), (1, 1, 1), (-1, -1, -1))
    assert abs(value - 1) <= error
    for s in c.connected_sets(host):
        value, error = c.field_activity(host, s, F(1, 8), (1, 1, 1), (-1, -1, -1))
        assert abs(value) <= error


def test_mixed_positive_pins_cancel_exactly_on_an_edge():
    host, beta = c.Host.create(2, ((0, 1),)), F(1, 8)
    partitions = [c.field_partition(host, (0, 1), beta, (1, 1), fields)
                  for fields in ((1, 1), (0, 1), (1, 0), (0, 0))]
    cancellation = sum(sign * value for sign, (value, _) in zip((1, -1, -1, 1), partitions))
    assert abs(cancellation) <= sum(error for _, error in partitions)
    assert all(value > F(9, 10) for value, _ in partitions)
    matrix = build_model(2, ((0, 1),)).h
    assert abs(expm(-float(beta) * matrix / 2)[3, 0]) < 1e-16


def test_fields_outside_unit_interval_are_not_silently_admitted():
    host = c.Host.create(1, ())
    with pytest.raises(ValueError):
        c.field_partition(host, (0,), F(1, 8), (1,), (2,))
