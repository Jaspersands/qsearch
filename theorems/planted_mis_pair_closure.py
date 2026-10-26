"""Graph-only recovery of a planted independent set with a two-seed separator.

Application to the construction stated in arXiv:2601.17686v1 Section 2.1,
pending independent source-scope review. Not a general MIS algorithm, a
quantum dynamics simulator, or a reproduction of the author's input files.
"""
from __future__ import annotations

import argparse
from itertools import combinations
import json
from pathlib import Path
import random
import time

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/classical_baselines/planted_mis_pair_closure.json"


def vertices(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length()-1
        mask ^= bit


def validate_graph(rows):
    if type(rows) is not tuple:
        raise ValueError("immutable tuple of adjacency bit masks required")
    n = len(rows)
    for u, mask in enumerate(rows):
        if type(mask) is not int or mask < 0 or mask >> n or mask >> u & 1:
            raise ValueError("simple loop-free graph with canonical integer masks required")
    for u, mask in enumerate(rows):
        if any(not (rows[v] >> u & 1) for v in vertices(mask)):
            raise ValueError("undirected symmetric adjacency required")
    return n


def independent(rows, mask):
    return all(rows[u] & mask == 0 for u in vertices(mask))


def pair_closure(rows):
    """Only the public graph is accepted; no planted set, blocks or target size."""
    n = validate_graph(rows)
    full = (1 << n)-1
    best, seed, examined, accepted = (1 if n else 0), (), 0, 0
    for u in range(n):
        for v in range(u+1, n):
            if rows[u] >> v & 1:
                continue
            examined += 1
            pair = (1 << u) | (1 << v)
            if best.bit_count() < 2:
                best, seed = pair, ()
            closed = full & ~(rows[u] | rows[v])
            if independent(rows, closed):
                accepted += 1
                if closed.bit_count() > best.bit_count() or (
                        closed.bit_count() == best.bit_count() and not seed):
                    best, seed = closed, (u, v)
    return {
        "independent_set": tuple(vertices(best)), "seed_pair": seed,
        "nonedge_pairs_examined": examined, "independent_closures": accepted,
        "generic_optimality_claim": False,
    }


def certify_cover(rows, candidate, cover):
    """Independent public upper bound: a partition into |candidate| cliques."""
    n = validate_graph(rows)
    if (any(type(u) is not int or not 0 <= u < n for u in candidate)
            or len(set(candidate)) != len(candidate)):
        raise ValueError("distinct valid candidate vertices required")
    mask = sum(1 << u for u in candidate)
    if not independent(rows, mask):
        raise ValueError("candidate contains an edge")
    seen = set()
    for clique in cover:
        if (not clique or any(type(u) is not int or not 0 <= u < n for u in clique)
                or len(set(clique)) != len(clique) or seen.intersection(clique)):
            raise ValueError("clique cover must be a nonempty-part vertex partition")
        seen.update(clique)
        if any(not (rows[u] >> v & 1) for u, v in combinations(clique, 2)):
            raise ValueError("purported cover part is not a clique")
    if seen != set(range(n)):
        raise ValueError("cover does not contain every vertex")
    return {"lower_bound": len(candidate), "upper_bound": len(cover),
            "optimality_certified": len(candidate) == len(cover)}


def make_fixture(spec, seed, *, thin=True):
    """Independent synthetic construction, with an explicitly preserved cover.

    Each (clique_count, clique_size, planted_count) describes one block.
    The cover restriction is extra: it lets the control certify optimality
    without trusting planting or reproducing a claimed uniqueness safeguard.
    """
    if (len(spec) < 2 or any(len(row) != 3 for row in spec)
            or any(type(x) is not int or x < 1 for row in spec for x in row)
            or any(g > m for m, _, g in spec)):
        raise ValueError("at least two positive block triples with planted_count<=count required")
    total_planted = sum(g for _, _, g in spec)
    if max(m for m, _, _ in spec) > total_planted:
        raise ValueError("fixture's explicit clique cover needs enough planted colors")
    rng = random.Random(seed)
    cliques, block_of, clique_of, planted, anchor_of = [], [], [], [], {}
    next_vertex = 0
    for block, (count, size, g) in enumerate(spec):
        selected = set(rng.sample(range(count), g))
        for j in range(count):
            clique = tuple(range(next_vertex, next_vertex+size))
            next_vertex += size
            index = len(cliques)
            cliques.append(clique)
            block_of.extend([block]*size)
            clique_of.extend([index]*size)
            if j in selected:
                anchor = rng.choice(clique)
                planted.append(anchor)
                anchor_of.update({v: anchor for v in clique if v != anchor})
    n, planted_set = next_vertex, set(planted)
    rows = [0]*n
    for u, v in combinations(range(n), 2):
        edge = clique_of[u] == clique_of[v] or block_of[u] != block_of[v]
        if edge and not (u in planted_set and v in planted_set):
            rows[u] |= 1 << v
            rows[v] |= 1 << u

    # One color per planted vertex, used at most once in each block.
    color_of, cover = {}, [[] for _ in planted]
    for block in range(len(spec)):
        local = [c for c in cliques if block_of[c[0]] == block]
        assigned = {}
        for c in local:
            for anchor in c:
                if anchor in planted_set:
                    assigned[c] = planted.index(anchor)
        unused = iter(j for j in range(total_planted) if j not in assigned.values())
        for c in local:
            color = assigned[c] if c in assigned else next(unused)
            cover[color].extend(c)
            color_of.update({v: color for v in c})

    records, used = [], set()
    order = list(anchor_of)
    rng.shuffle(order)
    if thin:
        for v in order:
            if v in used:
                continue
            anchor = anchor_of[v]
            degree_before, target_degree = rows[v].bit_count(), rows[anchor].bit_count()
            count = degree_before-target_degree
            eligible = [u for u in vertices(rows[v] & rows[anchor])
                        if u not in planted_set and u not in used
                        and clique_of[u] != clique_of[v] and color_of[u] != color_of[v]]
            rng.shuffle(eligible)
            edge = next(((u, w) for u, w in combinations(eligible, 2)
                         if rows[u] >> w & 1), None)
            if count < 2 or len(eligible) < count or edge is None:
                continue
            removed = list(edge)+[u for u in eligible if u not in edge][:count-2]
            for u in removed:
                rows[v] &= ~(1 << u)
                rows[u] &= ~(1 << v)
            used.update([v, *removed])
            records.append({"center": v, "anchor": anchor, "removed": tuple(removed),
                            "degree_before": degree_before, "degree_after": target_degree})
    rows = tuple(rows)
    validate_graph(rows)
    certify_cover(rows, tuple(planted), tuple(map(tuple, cover)))

    # Solver-facing labels cannot disclose the generating blocks or anchors.
    permutation = list(range(n))
    rng.shuffle(permutation)
    shuffled = [0]*n
    for u, mask in enumerate(rows):
        shuffled[permutation[u]] = sum(1 << permutation[v] for v in vertices(mask))
    return {
        "rows": tuple(shuffled), "planted": tuple(sorted(permutation[u] for u in planted)),
        "cover": tuple(tuple(permutation[u] for u in c) for c in cover),
        "block_of": tuple(block_of[permutation.index(u)] for u in range(n)),
        "clique_of": tuple(clique_of[permutation.index(u)] for u in range(n)),
        "thinning": tuple({**record, "center": permutation[record["center"]],
                           "anchor": permutation[record["anchor"]],
                           "removed": tuple(permutation[u] for u in record["removed"])}
                          for record in records),
        "seed": seed, "spec": tuple(map(tuple, spec)),
        "author_input_files_reproduced": False, "uniqueness_certified": False,
    }


def check_fixture(fixture):
    """Review the generator premises separately; never used by the solver."""
    rows, planted = fixture["rows"], set(fixture["planted"])
    n = validate_graph(rows)
    blocks, cliques, used = fixture["block_of"], fixture["clique_of"], set()
    if len(blocks) != n or len(cliques) != n or not independent(
            rows, sum(1 << u for u in planted)):
        raise ArithmeticError("invalid planted independent set or metadata")
    for v in range(n):
        if v not in planted:
            for s in planted:
                if blocks[s] != blocks[v] and not (rows[v] >> s & 1):
                    raise ArithmeticError("outside vertex lost a cross-block planted neighbor")
    for record in fixture["thinning"]:
        v, anchor, removed = record["center"], record["anchor"], record["removed"]
        if (v in planted or anchor not in planted or cliques[v] != cliques[anchor]
                or used.intersection([v, *removed]) or len(set(removed)) != len(removed)
                or v in removed or not removed):
            raise ArithmeticError("invalid thinning participation")
        if any(u in planted or cliques[u] == cliques[v]
               or rows[v] >> u & 1 or not rows[anchor] >> u & 1 for u in removed):
            raise ArithmeticError("thinning removed an ineligible edge")
        if independent(rows, sum(1 << u for u in removed)):
            raise ArithmeticError("removed neighbors are independent")
        if not (rows[v].bit_count() == rows[anchor].bit_count() == record["degree_after"]
                == record["degree_before"]-len(removed)):
            raise ArithmeticError("anchor degree equality failed")
        used.update([v, *removed])
    certificate = certify_cover(rows, tuple(planted), fixture["cover"])
    if not certificate["optimality_certified"]:
        raise ArithmeticError("fixture lacks its promised exact cover certificate")
    return certificate


def native_control():
    k, seed = 7, 2026102047
    spec = ((4+4*k, 9, 2+2*k), (8+4*k, 6, 6+2*k), (3+2*k, 4, 2))
    start = time.perf_counter()
    fixture = make_fixture(spec, seed)
    check_fixture(fixture)
    setup_seconds = time.perf_counter()-start
    start = time.perf_counter()
    result = pair_closure(fixture["rows"])
    solver_seconds = time.perf_counter()-start
    start = time.perf_counter()
    certificate = certify_cover(fixture["rows"], result["independent_set"], fixture["cover"])
    verification_seconds = time.perf_counter()-start
    if (not certificate["optimality_certified"]
            or result["independent_set"] != fixture["planted"]):
        raise ArithmeticError("native graph-only recovery did not recover the planted optimum")
    if not fixture["thinning"]:
        raise ArithmeticError("native control did not exercise degree thinning")
    return {
        "family_parameter": k, "vertices": len(fixture["rows"]), "seed": seed,
        "spec": fixture["spec"], "adjacency_hex": [hex(row) for row in fixture["rows"]],
        "block_of": fixture["block_of"], "clique_of": fixture["clique_of"],
        "planted_for_posthoc_check_only": fixture["planted"],
        "clique_cover_for_posthoc_check_only": fixture["cover"],
        "thinning": fixture["thinning"], "result": result, "certificate": certificate,
        "setup_and_premise_checks_seconds": setup_seconds,
        "graph_only_solver_seconds": solver_seconds,
        "public_certificate_verification_seconds": verification_seconds,
        "author_input_files_reproduced": False, "unique_optimum_claim": False,
        "timing_comparison_to_paper_valid": False,
    }


def report():
    return {
        "status": "CLASSICAL_STRUCTURAL_RECOVERY_SOURCE_SCOPE_REVIEW_PENDING",
        "scientific_question": "Does protected cross-block planting survive graph-only pair closure?",
        "answer": "No: two planted vertices in different blocks isolate the entire planted set.",
        "algorithm": "Enumerate all nonedges; keep the largest independent common closed antineighborhood.",
        "input": "Explicit simple undirected graph only; no planting metadata, seed oracle or target size.",
        "proof": "Every outside vertex is adjacent to at least one of two cross-block planted seeds.",
        "scope": "Any independent target with such a seed pair; optimality requires the target be maximum.",
        "classical_worst_case_boolean_operation_bound": "O(n^4)",
        "classical_graph_storage_bits": "O(n^2)",
        "generic_mis_solver": False, "quantum_dynamics_simulated": False,
        "sources": [
            {"url": "https://arxiv.org/html/2601.17686v1", "location": "Section 2.1 and Table 1",
             "use": "Graph construction and restriction of thinning to non-planted endpoints."},
            {"url": "https://drops.dagstuhl.de/storage/00lipics/lipics-vol168-icalp2020/LIPIcs.ICALP.2020.44/LIPIcs.ICALP.2020.44.pdf",
             "use": "General planted-clique seed/common-neighborhood technique is established; not a novelty claim."},
        ],
        "native_control": native_control(),
        "remaining_debt": [
            "Independent review of the written graph theorem and match to the paper's intended inputs.",
            "Original author graph files were not supplied or reproduced.",
            "No statement about quantum dynamics, general MIS, or changes deleting planted-outside edges.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    result = report()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    native = result["native_control"]
    print(json.dumps({"output": str(args.output), "vertices": native["vertices"],
                      "optimal_size": native["certificate"]["lower_bound"],
                      "solver_seconds": native["graph_only_solver_seconds"],
                      "thinning_operations": len(native["thinning"]),
                      "certificate": native["certificate"]}, indent=2))


if __name__ == "__main__":
    main()
