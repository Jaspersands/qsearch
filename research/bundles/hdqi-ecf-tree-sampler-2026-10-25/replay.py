"""Deterministic exact finite-product replay, not a thermal execution claim."""

from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
from random import Random
import hashlib
import json
import sys

from tree_controls import direct_output_masses, small_ecf_check
from tree_sampler import Decomposition, TreeSampler
from thermal_scope import conditional_thermal_plan


ROOT = Path(__file__).resolve().parent


def fixtures():
    cycle = Decomposition(5, [(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)],
                          [{0, 1, 2}, {0, 2, 3}, {0, 3, 4}], [(0, 1), (1, 2)])
    branching = Decomposition(6, [(0, 1), (0, 2), (1, 2), (0, 3), (1, 4), (2, 5)],
                              [{0, 1, 2}, {0, 3}, {1, 4}, {2, 5}], [(0, 1), (0, 2), (0, 3)])
    path_power = Decomposition(7, [(a, b) for a, b in combinations(range(7), 2) if b-a <= 2],
                               [{i, i+1, i+2} for i in range(5)], [(i, i+1) for i in range(4)])
    # A growing branching line-graph family with an explicit clique bag tree.
    root_edges = [((v-1)//2, v) for v in range(1, 31)]
    bags = [{i for i, edge in enumerate(root_edges) if v in edge} for v in range(31)]
    edges = [(i, j) for i, j in combinations(range(30), 2) if set(root_edges[i]) & set(root_edges[j])]
    large = Decomposition(30, edges, bags, root_edges, independence_bound=1)
    return [("odd-cycle", cycle), ("branching-cliques", branching),
            ("non-line-path-power", path_power), ("binary-tree-line-graph", large)]


def build():
    sources = ("tree_sampler.py", "tree_controls.py", "thermal_scope.py", "test_tree_sampler.py",
               "replay.py", "ECF_TREE_SAMPLING.md")
    context = ("hdqi-rational-transfer-2026-10-25/rational_thermal.py",
               "hdqi-rational-transfer-2026-10-25/RATIONAL_TRANSFER.md",
               "hdqi-transfer-word-sampler-2026-10-25/word_sampler.py")
    result = {"schema": "signed-ecf-tree-sampling-v1",
              "source_sha256": {f: hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in sources},
              "context_sha256": {f: hashlib.sha256((ROOT.parent/f).read_bytes()).hexdigest() for f in context},
              "claim_status": "exact finite-product executable; unreviewed general thermal upper-bound argument",
              "full_thermal_sampler_executed": False, "quantum_advantage_claim": False,
              "independent_review_performed": False, "cases": {}}
    for name, d in fixtures():
        couplings = [Q((-1)**i, 1+i % 3) for i in range(d.size)]
        parameters = [(Q(1, 3), Q(1, 7)), (Q(-1, 5), Q(2, 9))]
        bases = tuple("XZ"[i % 2] for i in range(d.size))
        sampler = TreeSampler(d, couplings, parameters, bases=bases)
        words = [sampler.sample(Random(seed), order=reversed(range(d.size))) for seed in (17, 23)]
        if d.size <= 9:
            expected = direct_output_masses(couplings, d.edges, parameters, bases)
            assert sampler.norm_squared == sum(expected)
            for word in range(1 << d.size):
                pins = {i: word >> i & 1 for i in range(d.size)}
                assert sampler.mass(pins) == expected[word]
            assert small_ecf_check(d.size, d.edges)
        plan = conditional_thermal_plan(d, couplings, 1, Q(1, 100))
        # Preserve the approximation parameters/budgets; avoid duplicating large moments.
        scalar = plan.pop("scalar_approximation")
        plan["scalar_summary"] = {key: value for key, value in scalar.items() if key != "blocks"}
        result["cases"][name] = {"graph_edges": d.edges, "bags": [sorted(b) for b in d.bags],
                                 "tree_edges": d.tree_edges, "couplings": couplings,
                                 "parameters": parameters, "bases": bases,
                                 "norm_squared": sampler.norm_squared, "samples": words,
                                 "sample_probabilities": [sampler.probability(w) for w in words],
                                 "resource_record": sampler.resources,
                                 "direct_all_output_check": d.size <= 9,
                                 "conditional_thermal_plan": plan}
        print(name, "m", d.size, "pair states/contract",
              sampler.resources["total_bag_pair_states_per_contraction"],
              "thermal degree <=", plan["factors_upper"],
              "thermal log2(pair states) <=", plan["max_pair_states_log2_upper"], flush=True)
    return json.loads(json.dumps(result, default=str))


def main():
    if sys.argv[1:] not in (["write"], ["check"]):
        raise SystemExit("usage: replay.py write|check")
    result = build()
    destination = ROOT/"receipt.json"
    if sys.argv[1] == "write":
        destination.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    elif result != json.loads(destination.read_text()):
        raise SystemExit("receipt mismatch")
    print(sys.argv[1], "PASS; receipt sha256", hashlib.sha256(destination.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
