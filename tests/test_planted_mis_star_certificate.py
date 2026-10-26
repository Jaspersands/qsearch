from itertools import combinations
import json

import pytest

from theorems import planted_mis_pair_closure as base
from theorems import planted_mis_star_certificate as star


def graph(n, edges):
    rows = [0]*n
    for u, v in edges:
        rows[u] |= 1 << v
        rows[v] |= 1 << u
    return tuple(rows)


def test_recovery_does_not_prove_optimality_without_promise():
    # Join a three-vertex planted set to C10. Recovery finds the planted
    # set, but the true optimum lies entirely outside it.
    edges = [(3+j, 3+(j+1) % 10) for j in range(10)]
    edges.extend((s, v) for s in range(3) for v in range(3, 13))
    rows = graph(13, edges)
    assert base.pair_closure(rows)["independent_set"] == (0, 1, 2)
    actual = (3, 5, 7, 9, 11)
    cover = ((0, 3, 4), (1, 5, 6), (2, 7, 8), (9, 10), (11, 12))
    assert base.certify_cover(rows, actual, cover)["optimality_certified"]


@pytest.mark.parametrize("seed", range(10))
def test_no_cover_guard_and_uniqueness(seed):
    fixture = star.unprotected_cover_fixture(((2, 2, 2), (2, 2, 2), (1, 2, 1)), seed)
    rows = fixture["rows"]
    result = base.pair_closure(rows)
    cert = star.structural_certificate(rows, result["independent_set"],
                                      fixture["block_of"], fixture["clique_of"])
    assert cert["unique_maximum_independent_set_certified"]
    assert not cert["clique_cover_used"]
    # Independent exhaustive optimum and uniqueness, not generator self-check.
    candidates = [s for size in range(len(rows)+1) for s in combinations(range(len(rows)), size)
                  if all(not (rows[u] >> v & 1) for u, v in combinations(s, 2))]
    size = max(map(len, candidates))
    optima = [s for s in candidates if len(s) == size]
    assert optima == [fixture["planted"]]


def simple_base():
    # Three single-clique blocks. Each clique consists of target+outside.
    target, blocks, cliques = (0, 2, 4), (0, 0, 1, 1, 2, 2), (0, 0, 1, 1, 2, 2)
    rows = graph(6, [(u, v) for u, v in combinations(range(6), 2)
                     if not (u in target and v in target)])
    return rows, target, blocks, cliques


def test_all_eligible_small_star_patterns():
    rows, target, blocks, cliques = simple_base()
    possible = ((1, 3), (1, 5), (3, 5))
    for mask in range(7):  # All proper subsets of the triangle are star forests.
        changed = list(rows)
        for i, (u, v) in enumerate(possible):
            if mask >> i & 1:
                changed[u] &= ~(1 << v)
                changed[v] &= ~(1 << u)
        cert = star.structural_certificate(tuple(changed), target, blocks, cliques)
        assert cert["target_size"] == 3
        assert cert["outside_target_independent_set_upper"] == 2


def test_triangle_is_not_a_star_and_breaks_uniqueness():
    rows, target, blocks, cliques = simple_base()
    changed = list(rows)
    for u, v in combinations((1, 3, 5), 2):
        changed[u] &= ~(1 << v)
        changed[v] &= ~(1 << u)
    rows = tuple(changed)
    assert base.independent(rows, sum(1 << u for u in (1, 3, 5)))
    with pytest.raises(ValueError, match="not a star"):
        star.structural_certificate(rows, target, blocks, cliques)


def test_four_cycle_is_not_a_star_and_breaks_uniqueness():
    target, blocks, cliques = (0, 2, 4, 6), (0, 0, 0, 0, 1, 1, 1, 1), (0, 0, 1, 1, 2, 2, 3, 3)
    edges = [(u, v) for u, v in combinations(range(8), 2)
             if (blocks[u] != blocks[v] or cliques[u] == cliques[v])
             and not (u in target and v in target)
             and not (u in (1, 3) and v in (5, 7))]
    rows = graph(8, edges)
    assert base.independent(rows, sum(1 << u for u in (1, 3, 5, 7)))
    with pytest.raises(ValueError, match="not a star"):
        star.structural_certificate(rows, target, blocks, cliques)


def test_strict_margin_is_needed_for_unique_optimum():
    target, blocks, cliques = (0, 2, 4), (0, 0, 0, 0, 1, 1), (0, 0, 1, 1, 2, 2)
    edges = [(u, v) for u, v in combinations(range(6), 2)
             if (blocks[u] != blocks[v] or cliques[u] == cliques[v])
             and not (u in target and v in target) and (u, v) not in ((1, 5), (3, 5))]
    rows = graph(6, edges)
    assert base.independent(rows, sum(1 << u for u in (1, 3, 5)))
    with pytest.raises(ValueError, match="strict uniqueness margin"):
        star.structural_certificate(rows, target, blocks, cliques)


@pytest.mark.parametrize("damage", ("protected", "clique", "added", "wrong_partition", "bad_target"))
def test_corrupted_structural_certificates_rejected(damage):
    rows, target, blocks, cliques = simple_base()
    rows = list(rows)
    if damage in ("protected", "clique"):
        u, v = (0, 3) if damage == "protected" else (0, 1)
        rows[u] &= ~(1 << v)
        rows[v] &= ~(1 << u)
    elif damage == "added":
        rows[0] |= 1 << 2
        rows[2] |= 1
    elif damage == "wrong_partition":
        blocks = (0, 1, 1, 1, 2, 2)
    else:
        target = (0, 0, 4)
    with pytest.raises(ValueError):
        star.structural_certificate(tuple(rows), target, blocks, cliques)


def test_native_replay_and_actual_thinning_rules():
    if not star.REPORT.exists():
        pytest.skip("native report not generated")
    data = json.loads(star.REPORT.read_text())
    native = data["native_control"]
    rows = tuple(int(row, 16) for row in native["adjacency_hex"])
    result = base.pair_closure(rows)
    assert len(result["independent_set"]) == 38
    assert tuple(native["target_for_posthoc_check_only"]) == result["independent_set"]
    cert = star.structural_certificate(rows, result["independent_set"],
                                      native["block_of"], native["clique_of"])
    assert cert["unique_maximum_independent_set_certified"]
    assert cert["single_block_independent_set_upper"] == 36
    assert cert["outside_target_independent_set_upper"] == 37
    assert native["old_cover_edges_deleted"] > 0
    target, used = set(result["independent_set"]), set()
    for step in native["thinning"]:
        v, anchor, removed = step["center"], step["anchor"], step["removed"]
        assert v not in target and anchor in target
        assert native["clique_of"][v] == native["clique_of"][anchor]
        assert not used.intersection([v, *removed])
        used.update([v, *removed])
        assert all(u not in target and native["clique_of"][u] != native["clique_of"][v]
                   and not (rows[v] >> u & 1) and rows[anchor] >> u & 1 for u in removed)
        assert not base.independent(rows, sum(1 << u for u in removed))
        assert rows[v].bit_count() == rows[anchor].bit_count() == step["degree_after"]
        assert step["degree_before"]-len(removed) == step["degree_after"]
    assert not data["broad_2025_gic_definition_covered"]
    assert not data["primary_source_audit"]["independent_external_review_completed"]
