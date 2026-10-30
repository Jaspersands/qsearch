from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
import math
from pathlib import Path
import random
import sys

import numpy as np
import pytest
from scipy.linalg import expm

import defect_observables as d

sys.path.insert(0, str(d.ROOT / "hdqi-parent-gap-2026-10-23"))
from parent_gap import build_model


def pauli_matrix(m, x, z, p=0):
    out = np.zeros((1 << m, 1 << m), dtype=complex)
    for y in range(1 << m):
        out[y ^ x, y] = 1j**p * (-1)**((z & y).bit_count() % 2)
    return out


def catalog(host, roots, twist=0, beta=F(1, 32), js=None):
    js = js or (F(1), F(-1, 2), F(3, 4))[:host.m]
    ordinary = {s: d.c.field_activity(host, s, beta, js,
                 tuple((-1)**(twist >> i & 1) for i in range(host.m)))[0]
                for s in d.c.connected_sets(host)}
    marked = {}
    for size in range(len(roots), host.m+1):
        for s in combinations(range(host.m), size):
            if set(roots).issubset(s) and d.forest_count(host, s, roots):
                marked[s] = d.marked_activity(host, s, roots, twist, beta, js)[0]
    return ordinary, marked


@pytest.mark.parametrize("h,r", [(h, n-h) for n in range(1, 5) for h in range(1, n+1)])
def test_complete_forest_count_and_wilson_support(h, r):
    exact = set(d.all_forests(h, r))
    assert len(exact) == d.complete_forest_count(h, r)
    for seed in range(30):
        forest = d.uniform_forest(h, r, random.Random(seed))
        assert forest in exact
        assert len(d.forest_order(h, forest)) == r


def test_wilson_small_distribution_and_explicit_budget_failure():
    rng = random.Random(241024)
    counts = Counter(d.uniform_forest(2, 1, rng) for _ in range(6000))
    assert set(counts) == {(0,), (1,)}
    assert abs(counts[(0,)]-3000) < 150

    class Loop:
        def randrange(self, stop):
            return stop-1

    with pytest.raises(d.ForestBudgetExceeded):
        d.uniform_forest(1, 2, Loop(), max_steps_per_walk=10)


@pytest.mark.parametrize("excess", range(6))
def test_marked_compositions_have_correct_count(excess):
    rows = list(d.root_compositions(excess))
    assert len(rows) == len(set(rows)) == 2**excess
    assert all(row[0] >= 0 and all(s > 0 for s in row[1:]) and sum(row) == excess for row in rows)


@pytest.mark.parametrize("edges,roots", [((), (0, 2)), (((0, 1), (1, 2)), (0, 2)),
                                         (((0, 1), (0, 2), (1, 2)), (0,)),
                                         (((0, 1), (1, 2)), (1,))])
def test_marked_forest_embedding_probabilities_exact(edges, roots):
    host = d.c.Host.create(3, edges)
    marked = lambda vertices: F((-1)**len(vertices), 7**len(vertices))
    ref = d.Reference(host, roots, lambda _: F(0), marked)
    for excess in range(4-len(roots)):
        out = ref.root_outcomes(excess)
        assert sum(p for _, _, p in out) <= 1
        expected = {s for s in combinations(range(3), len(roots)+excess)
                    if set(roots).issubset(s) and d.forest_count(host, s, roots)}
        assert {s for s, _, _ in out} == expected
        for vertices, weight, probability in out:
            assert probability*weight == marked(vertices)


@pytest.mark.parametrize("edges,roots,twist", [((), (0, 2), 0), (((0, 1), (1, 2)), (0, 2), 2),
                                               (((0, 1), (1, 2)), (1,), 5),
                                               (((0, 1), (0, 2), (1, 2)), (0, 1), 1)])
def test_exact_draw_equals_marked_ordered_tuple_expansion(edges, roots, twist):
    host = d.c.Host.create(3, edges)
    ordinary, marked = catalog(host, roots, twist)
    ref = d.Reference(host, roots, ordinary.__getitem__, marked.__getitem__)
    for limit in range(3):
        assert ref.exact_draw_mean(limit) == d.direct_sum(host, roots, ordinary, marked, limit)
    rng = random.Random(3401)
    assert all(abs(ref.draw(2, rng)) <= 2*8**len(roots) for _ in range(300))


def test_distinguished_factorial_and_repeated_polymers_are_necessary():
    host = d.c.Host.create(1, ())
    ordinary, marked = {(0,): F(1, 7)}, {(0,): F(-2, 9)}
    ref = d.Reference(host, (0,), ordinary.__getitem__, marked.__getitem__)
    expected = F(-2, 9)*sum((-F(1, 7))**k for k in range(4))
    assert ref.exact_draw_mean(3) == expected
    wrong = F(-2, 9)*sum((-F(1, 7))**k/F(k+1) for k in range(4))
    assert wrong != expected
    assert expected != marked[(0,)]


def test_forest_and_contact_corrections_cannot_be_dropped():
    host = d.c.Host.create(3, ((0, 1), (0, 2), (1, 2)))
    ref = d.Reference(host, (0,), lambda _: F(1, 100), lambda _: F(1, 100))
    vertices, weight, probability = ref.root_outcomes(2)[0]
    assert d.forest_count(host, vertices, (0,)) == 3
    assert weight*probability == F(1, 100)
    assert weight*3*probability != F(1, 100)
    sets = {0: (0, 1), 1: (2,)}
    corrected = ref.value(2, 2, (2, 1), ((0, 1),), sets, {0: F(1, 100), 1: F(1, 100)})
    assert corrected != 2*corrected


@pytest.mark.parametrize("edges", [(), ((0, 1), (1, 2)), ((0, 1), (0, 2), (1, 2))])
def test_every_twisted_insertion_matches_independent_dense_trace(edges):
    host = d.c.Host.create(3, edges)
    js, beta = (F(1), F(-1, 2), F(3, 4)), F(1, 16)
    model = build_model(3, edges, tuple(map(float, js)))
    s = expm(-float(beta)*model.h/2)
    pilot, z = s[:, 0], np.trace(s@s)/8
    for u, twist in product(range(8), repeat=2):
        roots = tuple(i for i in range(3) if u >> i & 1)
        value, error = d.inserted_partition(host, (0, 1, 2), roots, twist, beta, js)
        ordered = np.eye(8)
        for i in roots:
            ordered = ordered @ model.operators[i]
        zz = pauli_matrix(3, 0, twist)
        dense = np.trace(s @ ordered @ zz @ s @ zz)/8
        assert abs(float(value)-dense) <= float(error)+2e-14
        w = twist ^ d.ell(host, u)
        assert np.max(np.abs(ordered-pauli_matrix(3, u, d.ell(host, u)))) < 1e-14
        expect = pilot @ pauli_matrix(3, u, w) @ pilot / z
        assert abs(expect-dense/z) < 2e-14


@pytest.mark.parametrize("edges,roots,twist", [(((0, 1), (1, 2)), (0, 2), 0),
                                               (((0, 1), (1, 2)), (1,), 3),
                                               ((), (0, 2), 7)])
def test_marked_polymer_factorization_and_cluster_tail(edges, roots, twist):
    host = d.c.Host.create(3, edges)
    js, beta = (F(1), F(-1, 2), F(3, 4)), F(1, 32)
    ordinary, marked = catalog(host, roots, twist, beta, js)
    fields = tuple((-1)**(twist >> i & 1) for i in range(3))
    total = F(0)
    for first, value in marked.items():
        available = tuple(i for i in range(3) if not host.touches((i,), first))
        partition, _ = d.c.field_partition(host, available, beta, js, fields)
        total += value*partition
    exact, error = d.inserted_partition(host, (0, 1, 2), roots, twist, beta, js)
    assert abs(float(total-exact)) < 1e-18+float(error)
    z, _ = d.c.field_partition(host, (0, 1, 2), beta, js, fields)
    for limit in range(3):
        approx = d.direct_sum(host, roots, ordinary, marked, limit)
        tighter_tail = F(8**len(roots))*(16*host.slots*beta*beta)**(limit+1)/(1-16*host.slots*beta*beta)
        assert abs(float(approx-exact/z)) <= float(tighter_tail)+1e-18
    for s, value in ordinary.items():
        assert abs(value) <= beta**(2*len(s))+F(1, 10**20)
    for s, value in marked.items():
        assert abs(value) <= (2*beta)**len(roots)*beta**(2*(len(s)-len(roots)))+F(1, 10**20)


@pytest.mark.parametrize("beta", [F(0), F(1, 16), F(1, 2), F(2)])
def test_all_pauli_flip_bounds_without_degree_or_independence_assumptions(beta):
    edges = ((0, 1), (1, 2))
    js = (1, -0.5, 0.75)
    model = build_model(3, edges, js)
    pilot = expm(-float(beta)*model.h/2)[:, 0]
    pilot /= np.linalg.norm(pilot)
    for u, w in product(range(8), repeat=2):
        p = (u & w).bit_count() % 2
        value = pilot @ pauli_matrix(3, u, w, p) @ pilot
        bound = math.prod(min(1, float(beta)*abs(j)) for i, j in enumerate(js) if u >> i & 1)
        assert abs(value) <= bound+2e-14
        if p:
            assert abs(value) < 2e-14


def test_plans_do_not_promote_theorem_or_resource_ledger_to_execution():
    host = d.c.Host.create(100, [(i, i+1) for i in range(99)])
    out = d.pauli_plan(host, [1]*100, F(1, 16), (1, 0, 0), F(1, 10000))
    assert out["status"] == "marked_cluster_comparator"
    assert not out["production_estimator_executed"]
    assert not out["quantum_gap_certified"] and not out["full_output_sampling"]
    assert out["bound_B"] < 40000
    assert d.pauli_plan(host, [1]*100, 1, (1, 0, 0))["status"].startswith("inconclusive")
    assert d.pauli_plan(host, [1]*100, F(1, 16), (1, 1, 1))["status"] == "exact_zero_real_state"
    assert d.pauli_plan(host, [1]*100, F(1, 16), (15, 0, 0))["status"] == "zero_with_flip_bound"
    assert d.pauli_plan(host, [1]*100, F(1, 16), (0, 15, 0))["status"] == "existing_parity_cluster_comparator"


def test_small_coupling_precision_zero_couplings_and_guards():
    host = d.c.Host.create(2, ((0, 1),))
    value, error = d.marked_activity(host, (0, 1), (0,), 0, F(1, 10**100), (F(1), F(-1)))
    assert abs(value) <= F(2, 10**300)+error
    value, error = d.marked_activity(host, (0, 1), (0,), 0, F(1, 16), (0, 1))
    assert value == 0
    with pytest.raises(ValueError, match="Hermitian"):
        d.pauli_plan(host, [1, 1], F(1, 16), (1, 0, 1))
    with pytest.raises(ValueError):
        d.Reference(host, (), lambda _: 0, lambda _: 0)
    with pytest.raises(ValueError):
        d.restricted_coefficients(host, tuple(range(5)), 0, [1]*5, F(1, 100))
    with pytest.raises(ValueError):
        list(d.all_forests(2, 3))


def test_activity_precision_can_be_relative_to_a_tiny_root_envelope():
    host = d.c.Host.create(2, ((0, 1),))
    beta = F(1, 10**25)
    value, error = d.marked_activity(host, (0, 1), (0,), 0, beta, (1, 1), beta**3/10**12)
    assert error <= beta**3/10**12
    assert abs(value/beta**3+F(1, 6)) <= F(1, 10**10)


def test_all_sign_flip_twist_has_identity_partition_and_zero_nonempty_insertions():
    host = d.c.Host.create(3, ((0, 1), (1, 2)))
    beta, js = F(1, 16), (1, F(-1, 2), F(3, 4))
    for mask in range(1, 8):
        roots = tuple(i for i in range(3) if mask >> i & 1)
        value, error = d.inserted_partition(host, (0, 1, 2), roots, 7, beta, js)
        assert abs(value) <= error


@pytest.mark.parametrize("k", [2, 4, 16, 128, 1024])
def test_connected_growing_degree_family_has_actual_exponential_sign_cost_bound(k):
    row = d.separated_family(k)
    assert F(row["D_lambda"]) <= F(1, 64)
    assert F(row["log_C_lower"]) == F(k**4, 40*16**4)
    assert row["connected"] and row["all_couplings_nonzero"]
    assert not row["graph_constructed"] and not row["classical_hardness_claimed"]
    a, g = 1/16, k*k
    clique_log_c = g*math.log1p(2*math.sinh(a/(2*k))**2)-math.log1p(2*math.sinh(a/2)**2)
    assert clique_log_c >= a**4/20
    assert k**4*clique_log_c-float(F(1, 16*k)*(k**4-1)*F(1, 80*16**3)) >= float(F(row["log_C_lower"]))
