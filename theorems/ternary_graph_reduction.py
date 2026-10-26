"""Graph-coloring test of two-fold ternary decoding and edge subdivision.

Written structural arguments pending review. Exact classical sampling is
implemented; no native quantum circuit or general coloring no-go is claimed.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
from itertools import product
import json
from math import comb
from pathlib import Path
import random
import time

import networkx as nx
import numpy as np

from theorems.ternary_coloring_bpqm import graph_code
from theorems.ternary_tilted_type import local_receiver, relinearize, square_basis
from theorems.ternary_type_transfer import exact, sqrt_upper

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/reductions/ternary_graph_reduction.json"


def graph_from_code(code):
    graph = nx.Graph()
    graph.add_nodes_from(range(code["vertices"]))
    graph.add_edges_from(code["edges"])
    return graph


def series_profile(vertices, edges):
    """Independent graph-code construction and actual Schur-square rank."""
    code = graph_code(vertices, edges)
    classes, bridges = defaultdict(list), []
    for i in range(len(code["edges"])):
        column = tuple(row[i] for row in code["cycles"])
        leading = next((a for a in column if a), None)
        if leading is None:
            bridges.append(i)
        else:
            classes[tuple(a*leading % 3 for a in column)].append(i)
    square = square_basis(code["cycles"]) if code["cycles"] else ()
    if len(square) != len(classes):
        raise ArithmeticError("counterexample to the written series-class square formula")
    return {
        "code": code, "bridge_edge_indices": bridges,
        "series_classes": list(classes.values()), "square_dimension": len(square),
        "full_square": len(square) == len(code["edges"]),
        "square_equals_series_class_count": True,
    }


def core_edge_witnesses(code):
    """Two edge-disjoint detours give an explicit unit vector in D*D."""
    graph = graph_from_code(code)
    if nx.edge_connectivity(graph) < 3:
        raise ValueError("this witness constructor requires a three-edge-connected core")
    edges = code["edges"]
    index = {edge: i for i, edge in enumerate(edges)}
    witnesses = []
    for j, (u, v) in enumerate(edges):
        remainder = graph.copy()
        remainder.remove_edge(u, v)
        paths = list(nx.edge_disjoint_paths(remainder, u, v, cutoff=2))
        if len(paths) != 2:
            raise ArithmeticError("missing edge-disjoint detours")
        cycles = []
        for path in paths:
            vector = [0]*len(edges)
            vector[j] = 1
            for a, b in zip(path, path[1:]):
                vector[index[tuple(sorted((a, b)))]] = 2 if a < b else 1
            if any(sum(a*b for a, b in zip(check, vector)) % 3
                   for check in code["incidence"]):
                raise ArithmeticError("witness is not a circulation")
            cycles.append(vector)
        if tuple(a*b % 3 for a, b in zip(*cycles)) != tuple(
                int(i == j) for i in range(len(edges))):
            raise ArithmeticError("cycle product is not the claimed unit vector")
        witnesses.append({"edge_index": j, "detours": paths})
    return witnesses


def path_counts(length):
    """Number of proper three-color walks with a prescribed endpoint residue."""
    if type(length) is not int or not 0 <= length <= 4096:
        raise ValueError("integer path length in [0,4096] required")
    power, sign = 2**length, (-1)**length
    return ((power+2*sign)//3, (power-sign)//3, (power-sign)//3)


def sample_path(length, start, end, rng):
    if (type(start) is not int or type(end) is not int
            or start not in range(3) or end not in range(3)):
        raise ValueError("canonical endpoint colors required")
    counts = [path_counts(t) for t in range(length+1)]
    if not counts[-1][(end-start) % 3]:
        raise ValueError("no proper path with these endpoints")
    colors = [start]
    for remaining in range(length-1, -1, -1):
        options = [(c, counts[remaining][(end-c) % 3])
                   for c in range(3) if c != colors[-1]]
        total = sum(weight for _, weight in options)
        ticket = rng.randrange(total)
        for c, weight in options:
            if ticket < weight:
                colors.append(c)
                break
            ticket -= weight
    if colors[-1] != end or any(a == b for a, b in zip(colors, colors[1:])):
        raise ArithmeticError("path bridge sampler produced an invalid path")
    return tuple(colors)


def subdivision_budget(vertices, edges, length, *, trial_cap=16):
    """Charged classical rejection and conditional quantum erasure estimates."""
    code = graph_code(vertices, edges)
    if type(length) is not int or not 2 <= length <= 4096:
        raise ValueError("subdivision length at least two required")
    if type(trial_cap) is not int or trial_cap < 1:
        raise ValueError("positive trial cap required")
    m, k = len(code["edges"]), code["code_dimension"]
    counts = path_counts(length)
    rejection = min(Fraction(1), Fraction(m, max(counts)))
    # On a simple core, an unresolved cycle requires at least three erasures.
    erasure = Fraction(1, 2**(length-1))
    decoder_failure = min(Fraction(1), comb(m, 3)*erasure**3) if k else Fraction(0)
    quantum_tv = min(Fraction(1), 4*sqrt_upper(3**k*decoder_failure)
                     + Fraction(1, 2**64))
    return {
        "core_vertices": vertices, "core_edges": m, "cycle_dimension": k,
        "path_length": length, "expanded_vertices": vertices+m*(length-1),
        "expanded_edges": m*length,
        "classical_trial_acceptance_lower": exact(1-rejection),
        "classical_trial_cap": trial_cap,
        "classical_abort_probability_upper": exact(rejection**trial_cap),
        "classical_conditional_output_exactly_uniform": True,
        "path_erasure_probability": exact(erasure),
        "conditional_quantum_decoder_failure_upper": exact(decoder_failure),
        "conditional_quantum_output_tv_upper": exact(quantum_tv),
        "quantum_circuit_tv_compilation_requirement": exact(Fraction(1, 2**64)),
        "forest_failure_bound_sufficient_for_any_simple_core": True,
        "forest_criterion_necessary_only_when_core_square_full": True,
        "native_quantum_circuit_executed": False,
    }


def sample_subdivision(vertices, edges, length, *, seed, trial_cap=16):
    """Bounded exact uniform sampler, conditional on declared non-abort.

    Input is only the public core and path length. It does not receive a
    coloring, planted witness, count oracle, or quantum-generated sample.
    """
    code = graph_code(vertices, edges)
    budget = subdivision_budget(vertices, edges, length, trial_cap=trial_cap)
    counts, rng = path_counts(length), random.Random(seed)
    maximum = max(counts)
    start_time = time.perf_counter()
    for attempt in range(1, trial_cap+1):
        core_colors = (0, *(rng.randrange(3) for _ in range(vertices-1)))
        accepted = True
        for u, v in code["edges"]:
            if rng.randrange(maximum) >= counts[(core_colors[v]-core_colors[u]) % 3]:
                accepted = False
                break
        if not accepted:
            continue
        paths = [sample_path(length, core_colors[u], core_colors[v], rng)
                 for u, v in code["edges"]]
        return {
            "status": "EXACT_UNIFORM_SUBDIVISION_COLORING", "seed": seed,
            "core_colors": core_colors, "path_colors": paths, "attempts": attempt,
            "core_coloring_is_proper": all(core_colors[u] != core_colors[v]
                                           for u, v in code["edges"]),
            "every_expanded_edge_verified": all(
                len(path) == length+1 and path[0] == core_colors[u]
                and path[-1] == core_colors[v]
                and all(a != b for a, b in zip(path, path[1:]))
                for (u, v), path in zip(code["edges"], paths)),
            "elapsed_seconds": time.perf_counter()-start_time,
            "seeded_replay_not_a_distributional_certificate": True,
            "budget": budget,
        }
    return {"status": "DECLARED_ABORT", "seed": seed, "attempts": trial_cap,
            "budget": budget, "elapsed_seconds": time.perf_counter()-start_time}


def restored_block_control(length):
    """Reimposing a nonzero endpoint difference restores the original trine."""
    if type(length) is not int or not 1 <= length <= 10:
        raise ValueError("bounded block identity control requires 1<=length<=10")
    words = tuple(product((1, -1), repeat=length))
    residues = np.asarray([sum(word) % 3 for word in words])
    allowed = residues != 0
    omega = np.exp(2j*np.pi/3)
    fibers = np.column_stack([(residues == a)/np.sqrt(np.sum(residues == a))
                              for a in (1, 2)])
    trines = np.asarray([[omega**c, omega**(-c)] for c in range(3)]).T/np.sqrt(2)
    signals = np.column_stack([allowed*omega**(c*residues)/np.sqrt(allowed.sum())
                               for c in range(3)])
    gram = signals.conj().T @ signals
    expected = np.full((3, 3), -0.5)
    np.fill_diagonal(expected, 1)
    false_exclusions = []
    for c in range(3):
        state = signals[:, c].reshape(2, -1)
        false_exclusions.append(float(np.sum(abs(local_receiver(Fraction(1, 2))[c]
                                                @ state)**2)))
    b = path_counts(length)[1]
    wrong_pair = Fraction(1, 3)*(1-Fraction(path_counts(length-1)[0], b))
    if (np.max(abs(gram-expected)) > 2e-12
            or np.max(abs(fibers @ trines-signals)) > 2e-12
            or max(abs(x-float(wrong_pair)) for x in false_exclusions) > 2e-12):
        raise ArithmeticError("restored source contradicts the written identity")
    return {
        "length": length, "logical_spectrum": [0, 0.5, 0.5],
        "gram_real": gram.real.tolist(),
        "gram_max_imaginary_residual": float(np.max(abs(gram.imag))),
        "isometry_max_residual": float(np.max(abs(fibers @ trines-signals))),
        "unrestricted_product_off_diagonal_overlap": exact(Fraction(-1, 2)**length),
        "restored_off_diagonal_overlap": exact(Fraction(-1, 2)),
        "invalid_local_pair_probability": exact(wrong_pair),
        "measured_false_exclusion_probabilities": false_exclusions,
        "extra_logical_discrimination_information": False,
    }


def exact_core_law(vertices, edges, length):
    """Small exact normalization control, not the scalable sampler."""
    code = graph_code(vertices, edges)
    if vertices > 8:
        raise ValueError("exponential core-law control cap exceeded")
    counts = path_counts(length)
    rows, total = [], 0
    for tail in product(range(3), repeat=vertices-1):
        colors, weight = (0, *tail), 1
        for u, v in code["edges"]:
            weight *= counts[(colors[v]-colors[u]) % 3]
        total += weight
        rows.append((colors, weight))
    proper_weight = sum(weight for colors, weight in rows
                        if all(colors[u] != colors[v] for u, v in code["edges"]))
    return {"normalizer": total, "rows": rows,
            "original_endpoint_constraints_probability": exact(Fraction(proper_weight, total)),
            "proposal_acceptance": exact(Fraction(total, 3**(vertices-1)*max(counts)**len(edges)))}


def atlas_control():
    tested = 0
    for graph in nx.graph_atlas_g():
        n = len(graph)
        if not 2 <= n <= 6 or not nx.is_connected(graph):
            continue
        profile = series_profile(n, tuple(sorted(graph.edges())))
        expected_bridges = {tuple(sorted(e)) for e in nx.bridges(graph)}
        actual_bridges = {profile["code"]["edges"][i] for i in profile["bridge_edge_indices"]}
        if actual_bridges != expected_bridges:
            raise ArithmeticError("cycle-column bridges disagree with graph bridges")
        tested += 1
    return {"connected_simple_graphs_checked": tested, "maximum_vertices": 6,
            "all_series_square_ranks_match": True,
            "census_is_not_a_proof_for_arbitrary_graphs": True}


def report():
    graph = nx.random_regular_graph(4, 40, seed=2026102061)
    edges = tuple(sorted(tuple(sorted(e)) for e in graph.edges()))
    profile = series_profile(40, edges)
    witnesses = core_edge_witnesses(profile["code"])
    # Actual RLS on a legal outcome transcript: full square leaves all v free.
    codeword = profile["code"]["cycles"][0]
    decoder = relinearize(profile["code"]["cycles"],
                          tuple((c+1) % 3 for c in codeword))
    if decoder["projection_unique"] or decoder["free_variables"] != profile["code"]["code_dimension"]:
        raise ArithmeticError("full-square RLS did not retain every codeword degree of freedom")
    sample = sample_subdivision(40, edges, 64, seed=2026102062)
    complete4 = tuple((u, v) for u in range(4) for v in range(u+1, 4))
    return {
        "status": "SCOPED_GRAPH_REDUCTION_FALSIFIED_WRITTEN_REVIEW_PENDING",
        "sources": ["https://arxiv.org/html/2610.00502v1",
                    "https://webspace.maths.qmul.ac.uk/p.j.cameron/preprints/bcc20_cjr.pdf"],
        "core": profile, "unit_square_witnesses": witnesses,
        "actual_core_relinearization": decoder,
        "classical_subdivision_sample": sample,
        "atlas": atlas_control(),
        "restored_source_controls": [restored_block_control(t) for t in (1, 2, 3, 6)],
        "incompatible_original_k4": exact_core_law(4, complete4, 2),
        "rare_endpoint_control": {
            "core_family": "Complete tripartite K_(t,t,t), t=10",
            "vertices": 30, "edges": 300, "proper_colorings": 6,
            "any_even_subdivision_length_at_least_two": True,
            "restored_constraints_acceptance_upper": exact(Fraction(6, 3**30)),
            "core_family_itself_is_classically_easy": True,
        },
        "claim_gate": {
            "native_quantum_circuit_executed": False, "novelty_established": False,
            "general_coloring_or_quantum_decoding_no_go": False,
            "independent_mathematical_review_complete": False,
            "speedup_claim_allowed": False,
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    result = report()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+"\n")
    sample = result["classical_subdivision_sample"]
    print(json.dumps({"status": result["status"], "core_square_dimension": result["core"]["square_dimension"],
                      "core_cycle_dimension": result["core"]["code"]["code_dimension"],
                      "classical_status": sample["status"], "expanded_edges": sample["budget"]["expanded_edges"],
                      "classical_seconds": sample["elapsed_seconds"], "atlas": result["atlas"],
                      "speedup_claim_allowed": False}, indent=2))


if __name__ == "__main__":
    main()
