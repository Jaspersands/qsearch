from collections import Counter
from fractions import Fraction
from itertools import product
import random
import sys

import pytest

import isotropic_birthday as ib

sys.path.insert(0, str(ib.WORK / "orthogonal-rank-bound-2026-10-23"))
import rank_bound as rb
from test_orthogonal_probe import all_maximal, expected_kernel, standard


@pytest.mark.parametrize("n,p", [(3, 3), (4, 5), (5, 7), (8, 2**127-1)])
def test_complement_frame_has_no_secret_and_is_public_hyperbolic(n, p):
    rng = random.Random(125)
    for _ in range(4):
        probe = ib.op.make_probe(ib.op.random_singular(n, p, rng), p)
        frame = ib.complement_frame(probe)
        assert len(frame) == 2*n-2
        assert all(ib.op.polar(probe.e, v, p) == ib.op.polar(probe.dual, v, p) == 0 for v in frame)
        rows = ib.restriction(probe, rng)
        actual = [ib.op.span_coordinates(row, probe.complement, p) for row in rows]
        assert len(rows) == n-1
        assert all(ib.op.quadratic(v, p) == 0 for v in actual)
        assert all(ib.op.polar(v, w, p) == 0 for v in actual for w in actual)


def test_uniform_sampler_incidence_weights_exact_not_histogram():
    # Exhaust the recursion at rank two, not pseudo-random frequency bins.
    p, rank = 3, 2
    counts = Counter()
    for e in product(range(p), repeat=2*rank):
        if not any(e) or ib.op.quadratic(e, p):
            continue
        probe = ib.op.make_probe(e, p)
        frame = ib.complement_frame(probe)
        for lower in (((1, 0),), ((0, 1),)):
            subspace = ib.op.basis((e,)+tuple(ib.op.span_coordinates(v, frame, p) for v in lower), p)
            counts[subspace] += 1
    assert len(counts) == 8
    assert set(counts.values()) == {p**rank-1}
    assert set(counts) == set(all_maximal(rank, p))


@pytest.mark.parametrize("rank,p", [(2, 3), (3, 3), (3, 5)])
def test_at_least_half_restrictions_intersect_nontrivially(rank, p):
    spaces = all_maximal(rank, p)
    hidden = standard(rank)
    histogram = Counter(len(ib.op.intersection(hidden, space, 2*rank, p)) for space in spaces)
    assert sum(count for dimension, count in histogram.items() if dimension % 2 == 1) == len(spaces)//2
    assert sum(count for dimension, count in histogram.items() if dimension) >= len(spaces)//2


@pytest.mark.parametrize("n,p", [(3, 3), (4, 3), (4, 5), (5, 3)])
def test_real_opaque_queries_recover_complete_probe_kernel(n, p):
    hidden = standard(n)
    probe = ib.op.make_probe(ib.op.eye(2*n)[n], p)
    oracle = ib.op.OpaqueFixtureOracle(hidden, p)
    kernel, report = ib.learn_probe(probe, oracle, random.Random(169), error_bits=16)
    assert kernel == expected_kernel(probe, hidden)
    assert oracle.calls == report["actual_queries"]
    assert oracle.calls <= report["schedule"]["probe_query_cap"]
    assert all(row["queries"] <= report["schedule"]["query_cap_per_round"] for row in report["rounds"])


@pytest.mark.parametrize("n,p", [(3, 3), (3, 5), (4, 3), (5, 3)])
def test_end_to_end_classical_recovery_same_oracle_with_exact_certificate(n, p):
    hidden = ib.op.image(rb.swap_pair(n, 0), standard(n), p)
    oracle = ib.op.OpaqueFixtureOracle(hidden, p)
    result = ib.recover(oracle, n, p, seed=402)
    assert result["candidate"] == hidden
    assert result["certificate_passed"] and not result["quantum"]
    assert not result["dense_table_constructed"]
    assert result["actual_queries"] == oracle.calls


def test_distinct_parameters_never_manufacture_zero_collision():
    p, n = 3, 3
    probe = ib.op.make_probe(ib.op.eye(6)[3], p)
    rows = ib.restriction(probe, random.Random(6))
    calls = []

    def injective(matrix):
        calls.append(matrix)
        return matrix

    vector, receipt = ib.collision_round(probe, rows, injective, random.Random(12), p**(n-1))
    assert vector is None and not receipt["collision"]
    assert len(set(calls)) == len(calls) == p**(n-1)


def test_singleton_fiber_has_no_collision_and_constant_fiber_has_one():
    probe = ib.op.make_probe(ib.op.eye(6)[3], 3)
    rows = ib.restriction(probe, random.Random(7))
    vector, receipt = ib.collision_round(probe, rows, lambda _: 0, random.Random(12), 7)
    assert any(vector) and receipt["queries"] == 2


@pytest.mark.parametrize("n,p", [(3, 3), (8, 127), (64, 3)])
def test_exact_schedule_and_memory_have_matching_field_exponent(n, p):
    report = ib.query_schedule(n, p)
    assert Fraction(report["conditional_rank_failure_bound"]) <= Fraction(1, 2**20)
    assert report["probe_query_cap"] == report["query_cap_per_round"]*report["round_cap"]
    assert report["memory_labels_cap"] == report["query_cap_per_round"]
    assert (report["query_cap_per_round"]-1)**2 >= 9*p**(n-2)


def test_exponential_classical_work_cannot_silently_start():
    probe = ib.op.make_probe(ib.op.eye(16)[8], 127)
    with pytest.raises(ValueError, match="safety limit"):
        ib.learn_probe(probe, lambda _: 0, random.Random(1))


def test_incomplete_probe_retains_cost_and_does_not_become_a_neighbor(monkeypatch):
    def no_collision(probe, rows, oracle, rng, query_cap):
        oracle(probe.matrix((0,)*probe.width))
        return None, {"queries": 1, "parameter_draws": 1,
                      "labels_stored": 1, "collision": False}

    monkeypatch.setattr(ib, "collision_round", no_collision)
    oracle = ib.op.OpaqueFixtureOracle(standard(3), 3)
    result = ib.recover(oracle, 3, 3, attempts=2, error_bits=1)
    assert result["candidate"] is None and not result["certificate_passed"]
    assert result["actual_queries"] == oracle.calls
    assert len(result["records"]) == 2
    assert all(not attempt[0]["complete_rank"] for attempt in result["records"])
