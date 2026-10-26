"""Matched graph-only controls; small exhaustive tests are theorem regressions."""
from itertools import combinations
import json
import random

import pytest

from theorems import planted_mis_pair_closure as p


def graph(n, edges):
    rows = [0]*n
    for u, v in edges:
        rows[u] |= 1 << v
        rows[v] |= 1 << u
    return tuple(rows)


def brute_mis(rows):
    """Independent list-based exhaustive oracle, capped to control sizes."""
    n = len(rows)
    assert n <= 12
    for size in range(n, -1, -1):
        for subset in combinations(range(n), size):
            if all(not rows[u] >> v & 1 for u, v in combinations(subset, 2)):
                return subset


def test_all_outside_edge_deletions():
    # Three public blocks, three vertices each; no planting given to solver.
    n, planted = 9, {0, 3, 6}
    fixed, deletable = [], []
    for u, v in combinations(range(n), 2):
        if u in planted and v in planted:
            continue
        if u//3 != v//3 and u not in planted and v not in planted:
            deletable.append((u, v))
        else:
            fixed.append((u, v))
    assert len(deletable) == 12
    for mask in range(1 << len(deletable)):
        rows = graph(n, fixed+[edge for i, edge in enumerate(deletable) if mask >> i & 1])
        result = p.pair_closure(rows)
        assert len(result["independent_set"]) == 3
        certificate = p.certify_cover(rows, result["independent_set"],
                                      ((0, 1, 2), (3, 4, 5), (6, 7, 8)))
        assert certificate["optimality_certified"]
        if mask % 127 == 0:
            assert len(brute_mis(rows)) == 3


@pytest.mark.parametrize("seed", range(8))
@pytest.mark.parametrize("thin", (False, True))
def test_shuffled_graph_only_solver(seed, thin):
    fixture = p.make_fixture(((3, 3, 2), (4, 2, 2), (2, 4, 1)), seed, thin=thin)
    p.check_fixture(fixture)
    result = p.pair_closure(fixture["rows"])
    assert len(result["independent_set"]) == len(fixture["planted"])
    assert p.certify_cover(fixture["rows"], result["independent_set"],
                           fixture["cover"])["optimality_certified"]
    # Explicitly exercise the written separating-pair identity.
    full = (1 << len(fixture["rows"]))-1
    target = sum(1 << v for v in fixture["planted"])
    for u, v in combinations(fixture["planted"], 2):
        if fixture["block_of"][u] != fixture["block_of"][v]:
            assert full & ~(fixture["rows"][u] | fixture["rows"][v]) == target


def test_independent_of_metadata_and_size():
    fixture = p.make_fixture(((2, 3, 1), (2, 3, 1), (2, 3, 1)), 87)
    rows = tuple(int(hex(v), 16) for v in fixture["rows"])
    fixture.clear()
    result = p.pair_closure(rows)
    assert len(result["independent_set"]) == 3
    assert not result["generic_optimality_claim"]


def test_arbitrary_graph_does_not_get_a_general_mis_claim():
    rows = graph(10, tuple((u, (u+1) % 10) for u in range(10)))
    result = p.pair_closure(rows)
    assert len(brute_mis(rows)) == 5
    assert len(result["independent_set"]) == 2
    assert result["seed_pair"] == ()
    assert not result["generic_optimality_claim"]
    assert p.independent(rows, sum(1 << u for u in result["independent_set"]))


def test_deleting_target_outside_edges_breaks_the_premise():
    # Independent target 0,1,2. Each of 3,4,5 sees only one target, and
    # 6 sees two. No target pair excludes all outsiders.
    rows = graph(7, ((0, 3), (1, 4), (2, 5), (0, 6), (1, 6),
                     (3, 4), (3, 5), (4, 5), (3, 6), (4, 6), (5, 6)))
    full, target = (1 << 7)-1, (1 << 3)-1
    for u, v in combinations(range(3), 2):
        assert full & ~(rows[u] | rows[v]) != target
    assert not p.pair_closure(rows)["generic_optimality_claim"]


def test_finite_random_graphs_against_exhaustive_oracle():
    rng = random.Random(876)
    for n in range(1, 10):
        for _ in range(10):
            rows = graph(n, tuple(e for e in combinations(range(n), 2) if rng.randrange(2)))
            result = p.pair_closure(rows)
            candidate = result["independent_set"]
            assert all(not rows[u] >> v & 1 for u, v in combinations(candidate, 2))
            optimum = brute_mis(rows)
            assert len(candidate) <= len(optimum)
            # When an optimal set has a separating pair, recovery is guaranteed.
            target = sum(1 << u for u in optimum)
            if any(((1 << n)-1) & ~(rows[u] | rows[v]) == target
                   for u, v in combinations(optimum, 2)):
                assert len(candidate) == len(optimum)


@pytest.mark.parametrize("rows", ([0], (True,), (-1,), (1,), (2,), (2, 0), (2, "x")))
def test_bad_graphs_rejected(rows):
    with pytest.raises(ValueError):
        p.pair_closure(rows)


def test_degenerate_graphs():
    assert p.pair_closure(())["independent_set"] == ()
    assert p.pair_closure((0,))["independent_set"] == (0,)
    assert p.pair_closure((0, 0, 0))["independent_set"] == (0, 1, 2)
    rows = graph(4, tuple(combinations(range(4), 2)))
    assert len(p.pair_closure(rows)["independent_set"]) == 1


@pytest.mark.parametrize("candidate,cover", (
    ((0, 1), ((0, 1), (2,))),
    ((0, 0), ((0, 1), (2,))),
    ((0,), ((0, 1),)),
    ((0,), ((0, 1), (1, 2))),
    ((0,), ((0, 2), (1,))),
    ((0,), ((), (0, 1), (2,))),
    ((False,), ((0, 1), (2,))),
))
def test_forged_certificates_rejected(candidate, cover):
    rows = graph(3, ((0, 1),))
    with pytest.raises(ValueError):
        p.certify_cover(rows, candidate, cover)


def test_upper_bound_is_not_automatically_equality():
    rows = graph(3, ((0, 1),))
    certificate = p.certify_cover(rows, (0,), ((0, 1), (2,)))
    assert certificate == {"lower_bound": 1, "upper_bound": 2, "optimality_certified": False}


def test_native_artifact_replay():
    if not p.REPORT.exists():
        pytest.skip("native artifact has not been generated")
    report = json.loads(p.REPORT.read_text())
    native = report["native_control"]
    rows = tuple(int(row, 16) for row in native["adjacency_hex"])
    result = p.pair_closure(rows)
    assert len(rows) == 572
    assert result["independent_set"] == tuple(native["result"]["independent_set"])
    assert len(result["independent_set"]) == 38
    assert p.certify_cover(rows, result["independent_set"],
                           native["clique_cover_for_posthoc_check_only"])["optimality_certified"]
    fixture = {"rows": rows, "planted": native["planted_for_posthoc_check_only"],
               "cover": native["clique_cover_for_posthoc_check_only"],
               "block_of": native["block_of"], "clique_of": native["clique_of"],
               "thinning": native["thinning"]}
    p.check_fixture(fixture)
    assert native["thinning"]
    assert not native["author_input_files_reproduced"]
    assert not native["timing_comparison_to_paper_valid"]
    assert not native["unique_optimum_claim"]
