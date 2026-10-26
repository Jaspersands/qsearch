"""Exact original-oracle equivalence controls, not a new oracle benchmark."""
from collections import defaultdict
from itertools import product
from math import comb, prod
import random

import pytest

from theorems.ambient_section_potential import polynomial_section_fixture, section_word_certificate
from theorems.jet_oracle_homogenization import (
    deterministic_resource_profile, lie_bch, make_oracle_plan, simplex_design, simplex_indices,
)
from theorems.nonabelian_jet_homogenization import FilteredEvaluation
from theorems.right_abelian_induced_source import upper_triangular_lie
from theorems.symbolic_scalar_phase_erasure import _fmpz_nullspace_basis, _fmpz_solve_coordinates
from theorems.ut5_matrix_phase_alignment import _identity, _rank
from tests.test_ambient_section_potential import _matrix_exp, _matrix_log, _matrix_multiply


@pytest.mark.parametrize("p,m,c", [(5, 2, 2), (5, 4, 4), (11, 4, 4), (43, 2, 9), (2**127-1, 3, 4)])
def test_simplex_is_exactly_unisolvent_without_randomness_or_field_scan(p, m, c):
    nodes = simplex_indices(m+1, c-1)
    points = simplex_design(p, m, c)
    assert len(points) == comb(m+c, m+1)
    newton = [[prod(comb(b, a) for b, a in zip(beta, alpha)) % p for alpha in nodes] for beta in nodes]
    assert all(row[i] == 1 and all(x == 0 for x in row[i+1:]) for i, row in enumerate(newton))
    raw = [[s*prod(pow(v, a, p) for v, a in zip((*u, s), alpha)) % p for alpha in nodes]
           for u, s in points]
    assert _rank(raw, p) == len(nodes)
    assert all(0 < s <= c and max(u) < c for u, s in points)
    if c > 1:
        wrong = [[prod(pow(v, a, p) for v, a in zip((*u, 1), alpha)) % p for alpha in nodes]
                 for u, _ in points]
        assert _rank(wrong, p) < len(nodes)


def fixture(size, p):
    algebra, slots = upper_triangular_lie(size, p)
    plan = make_oracle_plan(algebra, _identity(len(slots)))
    return algebra, slots, plan


def potential_fixture(algebra, plan, hidden_normal):
    """Hidden line projects to the FIRST public section basis vector."""
    section = plan.certificate.section_basis
    zero = (0,)*algebra.dimension
    inputs = ((zero, *section[1:]), (section[0], *(zero for _ in section[1:])),
              (hidden_normal, *(zero for _ in section[1:])))
    coefficients = polynomial_section_fixture(section_word_certificate(plan.group.class_bound), algebra, inputs)
    result = {}
    for alpha, value in coefficients.items():
        coords = _fmpz_solve_coordinates(plan.certificate.normal_basis, value, algebra.p)
        result.update({(i, alpha, 0): a for i, a in enumerate(coords) if a})
    return result


def encode(group, element):
    a, q = element
    return tuple(a.get(key, 0) for key in group.indices), q


def test_complete_lifted_oracle_partition_is_exactly_right_graph_action_cosets():
    p = 5
    algebra, slots, plan = fixture(3, p)
    group = plan.group
    assert plan.original_queries == 4 and group.dimension == 4
    hidden_normal = tuple(int(ij == (0, 2)) for ij in slots)
    potential = potential_fixture(algebra, plan, hidden_normal)
    hlog = tuple((x+y) % p for x, y in zip(plan.certificate.section_basis[0], hidden_normal))
    # Independently construct actual UT3 coset labels by matrix coordinates.
    def matrix(v):
        x, z, y = v
        return (x, y, (z+x*y*pow(2, -1, p)) % p)
    def multiply(a, b):
        x, y, z = a
        X, Y, Z = b
        return ((x+X) % p, (y+Y) % p, (z+Z+x*Y) % p)
    hidden = [matrix(tuple(t*x % p for x in hlog)) for t in range(p)]
    original_labels = {v: min(multiply(matrix(v), h) for h in hidden) for v in product(range(p), repeat=3)}
    buckets = defaultdict(set)
    representatives = {}
    for q in product(range(p), repeat=2):
        for coefficients in product(range(p), repeat=4):
            a = {key: value for key, value in zip(group.indices, coefficients) if value}
            element = a, q
            label = plan.evaluate_fixture(original_labels.__getitem__, element)
            buckets[label].add(encode(group, element))
            representatives.setdefault(label, element)
    assert len(buckets) == p**5
    assert {len(v) for v in buckets.values()} == {p}
    graph = [(group.normalized_curve_fixture(potential, (t, 0)), (t, 0)) for t in range(p)]
    for label, values in buckets.items():
        orbit = {encode(group, group.semidirect_multiply(representatives[label], h)) for h in graph}
        assert values == orbit
    # Every diagonal input is queried exactly once per fixed simplex point.
    queries = []
    plan.evaluate_fixture(lambda x: queries.append(x), ({}, (0, 0)))
    assert len(queries) == plan.original_queries


@pytest.mark.parametrize("p", [5, 17, 2**127-1])
def test_nonabelian_normal_public_queries_match_independent_matrices_and_cosets(p):
    algebra, slots, plan = fixture(5, p)
    group = plan.group
    assert any(group.tensor.values())
    hidden_normal = tuple(int(ij == (2, 4)) for ij in slots)
    potential = potential_fixture(algebra, plan, hidden_normal)
    hidden_log = tuple((a+b) % p for a, b in zip(plan.certificate.section_basis[0], hidden_normal))
    rng = random.Random(314)
    def matrix(v):
        return [[v[slots.index((i, j))] if (i, j) in slots else 0 for j in range(5)] for i in range(5)]
    a = {key: v for key in group.indices if (v := rng.randrange(p))}
    q = tuple(x % p for x in (3, 4, 5, 6))
    u = (2, 0, 0, 0)
    moved = group.semidirect_multiply((a, q), (group.normalized_curve_fixture(potential, u), u))
    for i in (0, 1, 5, plan.original_queries-1):
        left = plan.input_at((a, q), i)
        right = plan.input_at(moved, i)
        difference = _matrix_log(_matrix_multiply(_matrix_exp(matrix(tuple(-x % p for x in left)), p),
                                                  _matrix_exp(matrix(right), p), p), p)
        scale = plan.points[i][1]
        assert tuple(difference[r][c] for r, c in slots) == tuple(2*scale*x % p for x in hidden_log)
        y, s = plan.points[i]
        normal = group.evaluate(a, y, s)
        nlog = tuple(sum(x*v[k] for x, v in zip(normal, plan.certificate.normal_basis)) % p for k in range(len(slots)))
        slog = tuple(sum((yi+s*qi)*v[k] for yi, qi, v in zip(y, q, plan.certificate.section_basis)) % p
                     for k in range(len(slots)))
        product_matrix = _matrix_multiply(_matrix_exp(matrix(nlog), p), _matrix_exp(matrix(slog), p), p)
        assert _matrix_exp(matrix(left), p) == product_matrix
        # Reversing the normal-first order changes at least some query inputs.
    assert any(lie_bch(algebra, nlog, slog, 4)[k] != lie_bch(algebra, slog, nlog, 4)[k] for k in range(len(slots)))
    assert FilteredEvaluation(group, plan.points).spectator_dimension >= 0


def test_transversality_cannot_be_silently_omitted():
    algebra, slots, plan = fixture(3, 5)
    group = plan.group
    # H=N. This original oracle hides the normal subgroup, not a transverse H.
    original = lambda log: (log[slots.index((0, 1))], log[slots.index((1, 2))])
    zero = ({}, (0, 0))
    nonzero = ({group.indices[0]: 1}, (0, 0))
    assert plan.evaluate_fixture(original, zero) == plan.evaluate_fixture(original, nonzero)
    # Its image U is zero, so the proposed graph H_F would be trivial.
    # The extra collision invalidates that conclusion until H intersect N is removed.
    assert encode(group, zero) != encode(group, nonzero)


def test_omitting_one_point_creates_false_collisions_even_for_trivial_hidden_subgroup():
    _, _, plan = fixture(3, 5)
    group = plan.group
    rows = [[s**d*prod(pow(v, e, 5) for v, e in zip(y, alpha)) % 5
             for _, alpha, d in group.indices] for y, s in plan.points[:-1]]
    kernel = _fmpz_nullspace_basis(rows, group.dimension, 5)
    assert len(kernel) == 1
    nonzero = {key: x for key, x in zip(group.indices, kernel[0]) if x}
    left = plan.evaluate_fixture(lambda x: x, ({}, (0, 0)))
    right = plan.evaluate_fixture(lambda x: x, (nonzero, (0, 0)))
    assert left[:-1] == right[:-1]
    assert left[-1] != right[-1]


def test_query_compiler_never_calls_hidden_potential_and_rejects_bad_coordinates(monkeypatch):
    _, _, plan = fixture(3, 5)
    def forbidden(*args, **kwargs):
        raise AssertionError("hidden fixture leaked into public compiler")
    monkeypatch.setattr(type(plan.group), "normalized_curve_fixture", forbidden)
    assert len(plan.inputs(({}, (1, 2)))) == 4
    with pytest.raises(ValueError, match="support"):
        plan.inputs(({(0, (0, 0), 0): 1}, (1, 2)))
    with pytest.raises(ValueError, match="index"):
        plan.input_at(({}, (1, 2)), -1)
    with pytest.raises(ValueError, match="p>degree"):
        simplex_design(5, 2, 5)


def test_resource_profile_removes_alignment_not_the_remaining_quantum_tree():
    weights = (6, 5, 4, 4, 3, 3, 2, 9, 8, 8, 7, 7, 7, 6, 6, 5, 5)
    profile = deterministic_resource_profile(weights, 2, 43)
    assert profile["queries_per_lifted_oracle"] == 165
    assert profile["alignment_retries"] == profile["spectator_measurements"] == 0
    assert profile["original_queries_ceil_log2"] > 1700
    assert profile["coherent_circuit_implemented"] is False
    assert "not source-only" in profile["access"]
