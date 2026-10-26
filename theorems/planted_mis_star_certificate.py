"""Optimality certificate for protected planting with disjoint-star deletions.

Checks the actual graph against its structural witness. No clique-cover
preservation restriction. The graph-only solver is unchanged. Source-scope
interpretation remains separate from the combinatorial certificate.
"""
from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import random
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems import planted_mis_pair_closure as base

REPORT = ROOT / "research/classical_baselines/planted_mis_star_certificate.json"


def structural_certificate(rows, target, block_of, clique_of):
    """Certify UNIQUE maximum size using public graph/partition/set witnesses.

    This verifies optimality after recovery. The recovery algorithm receives
    none of target, block_of, or clique_of.
    """
    n = base.validate_graph(rows)
    if (len(block_of) != n or len(clique_of) != n
            or any(type(x) is not int or x < 0 for x in (*block_of, *clique_of))
            or any(type(v) is not int or not 0 <= v < n for v in target)
            or len(set(target)) != len(target)):
        raise ValueError("canonical target and one nonnegative block/clique ID per vertex required")
    target_set = set(target)
    if not base.independent(rows, sum(1 << v for v in target)):
        raise ValueError("target is not independent")
    clique_block, planted_cliques = {}, set()
    for v in range(n):
        clique = clique_of[v]
        if clique in clique_block and clique_block[clique] != block_of[v]:
            raise ValueError("clique crosses blocks")
        clique_block[clique] = block_of[v]
        if v in target_set:
            if clique in planted_cliques:
                raise ValueError("two target vertices occupy the same clique")
            planted_cliques.add(clique)
    counts = Counter(clique_block.values())
    if not counts:
        raise ValueError("nonempty structural instance required")
    max_cliques = max(counts.values())
    if len(target_set) <= max_cliques+1:
        raise ValueError("strict uniqueness margin |S| > max block clique count + 1 required")
    removed = [0]*n
    for u, v in combinations(range(n), 2):
        originally_edge = (clique_of[u] == clique_of[v] or block_of[u] != block_of[v])
        originally_edge &= not (u in target_set and v in target_set)
        edge = bool(rows[u] >> v & 1)
        if edge and not originally_edge:
            raise ValueError("graph adds an edge absent from the declared planted construction")
        if originally_edge and not edge:
            if u in target_set or v in target_set or block_of[u] == block_of[v]:
                raise ValueError("deletion damages a protected or within-clique edge")
            removed[u] |= 1 << v
            removed[v] |= 1 << u

    unseen = {v for v in range(n) if removed[v]}
    components = []
    while unseen:
        stack, component = [min(unseen)], set()
        while stack:
            v = stack.pop()
            if v not in component:
                component.add(v)
                stack.extend(base.vertices(removed[v]))
        unseen.difference_update(component)
        edges = sum(removed[v].bit_count() for v in component)//2
        centers = [v for v in component if removed[v].bit_count() == len(component)-1]
        if edges != len(component)-1 or not centers:
            raise ValueError("deleted-edge component is not a star")
        center = min(centers)
        components.append({"center": center, "leaves": tuple(sorted(component-{center}))})
    return {
        "vertices": n, "target_size": len(target_set),
        "block_clique_counts": dict(sorted(counts.items())),
        "single_block_independent_set_upper": max_cliques,
        "outside_target_independent_set_upper": max_cliques+1,
        "unique_maximum_independent_set_certified": True,
        "deleted_edge_count": sum(mask.bit_count() for mask in removed)//2,
        "deleted_star_components": components,
        "clique_cover_used": False,
    }


def unprotected_cover_fixture(spec, seed):
    """Implement single-participation anchored thinning without a cover guard."""
    fixture = base.make_fixture(spec, seed, thin=False)
    rows, planted = list(fixture["rows"]), set(fixture["planted"])
    cliques = fixture["clique_of"]
    anchor_at = {cliques[v]: v for v in planted}
    order = [v for v in range(len(rows)) if v not in planted and cliques[v] in anchor_at]
    rng = random.Random(seed+1)
    rng.shuffle(order)
    used, steps = set(), []
    for v in order:
        if v in used:
            continue
        anchor = anchor_at[cliques[v]]
        before, target = rows[v].bit_count(), rows[anchor].bit_count()
        count = before-target
        eligible = [u for u in base.vertices(rows[v] & rows[anchor])
                    if u not in planted and u not in used and cliques[u] != cliques[v]]
        rng.shuffle(eligible)
        edge = next(((u, w) for u, w in combinations(eligible, 2) if rows[u] >> w & 1), None)
        if count < 2 or len(eligible) < count or edge is None:
            continue
        deleted = list(edge)+[u for u in eligible if u not in edge][:count-2]
        for u in deleted:
            rows[v] &= ~(1 << u)
            rows[u] &= ~(1 << v)
        used.update([v, *deleted])
        steps.append({"center": v, "anchor": anchor, "removed": tuple(deleted),
                      "degree_before": before, "degree_after": target})
    old_cover = fixture.pop("cover")
    # Retain only the observed failure of the old extra restriction.
    broken = sum(not (rows[u] >> v & 1) for c in old_cover for u, v in combinations(c, 2))
    return {**fixture, "rows": tuple(rows), "thinning": steps,
            "old_cover_edges_deleted": broken}


def native_control():
    k, seed = 7, 2026102051
    spec = ((4+4*k, 9, 2+2*k), (8+4*k, 6, 6+2*k), (3+2*k, 4, 2))
    start = time.perf_counter()
    fixture = unprotected_cover_fixture(spec, seed)
    generation_seconds = time.perf_counter()-start
    start = time.perf_counter()
    result = base.pair_closure(fixture["rows"])
    solver_seconds = time.perf_counter()-start
    start = time.perf_counter()
    certificate = structural_certificate(fixture["rows"], result["independent_set"],
                                         fixture["block_of"], fixture["clique_of"])
    certification_seconds = time.perf_counter()-start
    if (result["independent_set"] != fixture["planted"]
            or fixture["old_cover_edges_deleted"] == 0):
        raise ArithmeticError("control failed recovery or did not escape the prior cover restriction")
    return {
        "family_parameter": k, "seed": seed, "spec": spec,
        "adjacency_hex": [hex(row) for row in fixture["rows"]],
        "block_of": fixture["block_of"], "clique_of": fixture["clique_of"],
        "target_for_posthoc_check_only": fixture["planted"],
        "thinning": fixture["thinning"],
        "old_cover_edges_deleted": fixture["old_cover_edges_deleted"],
        "result": result, "certificate": certificate,
        "generation_seconds": generation_seconds, "graph_only_solver_seconds": solver_seconds,
        "posthoc_structural_certificate_seconds": certification_seconds,
        "author_benchmark_reproduction": False, "cross_paper_runtime_comparison": False,
    }


def report():
    return {
        "status": "EXACT_STRUCTURAL_CERTIFICATE_SOURCE_SCOPE_REVIEW_PENDING",
        "question": "Can the extra preserved clique cover be removed without assuming optimality?",
        "answer": "Yes, when removed edges form disjoint stars and |S| exceeds max block clique count by at least two.",
        "proof_summary": [
            "An independent set meeting S in two blocks is a subset of S.",
            "An independent set meeting S in one block lies entirely in that block.",
            "An outside-only independent set cannot occupy three blocks: that would require a deleted triangle.",
            "Across two blocks, two vertices on each side would require a deleted four-cycle.",
            "A star forest excludes both, so outside-only size is at most max block clique count plus one.",
        ],
        "broad_2025_gic_definition_covered": False,
        "formalization_scope": "The prior two recovery lemmas are Lean-checked; this optimality bound is not formalized.",
        "primary_source_audit": {
            "archive_url": "https://arxiv.org/src/2601.17686v1",
            "archive_sha256": "ade4650cd0b2dac01c4a8a14f2421afc3e2cb7acbcca67379594ef3ed46729c3",
            "archive_member_count": 30,
            "machine_readable_author_graph_files_found": False,
            "construction_member": "Results0123.tex",
            "construction_member_sha256": "6491a5f8c1672d7a8e43f0ded116d7defd3aaa9889f730024acb5e45079018db",
            "protected_edge_source_lines": [38, 42, 70, 76],
            "single_participation_source_lines": [80, 84],
            "parameter_source_line": 129,
            "broader_definition": "https://arxiv.org/html/2509.16263v1#S3.SS3",
            "broader_definition_implies_protected_edges": False,
            "independent_external_review_completed": False,
        },
        "native_control": native_control(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    result = report()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    native = result["native_control"]
    print(json.dumps({"output": str(args.output), "target_size": native["certificate"]["target_size"],
                      "unique_optimum": native["certificate"]["unique_maximum_independent_set_certified"],
                      "old_cover_edges_deleted": native["old_cover_edges_deleted"],
                      "solver_seconds": native["graph_only_solver_seconds"]}, indent=2))


if __name__ == "__main__":
    main()
