"""Replay finite exact marked-cluster checks and an explicit 128-qubit pullback."""

import argparse
from fractions import Fraction as F
import hashlib
from itertools import combinations
import json
import math
from pathlib import Path
import random

import defect_observables as d
import linear_pullback as lp


def receipt():
    controls = []
    for name, edges, roots, twist in (
        ("nonadjacent_marked_roots", ((0, 1), (1, 2)), (0, 2), 0),
        ("signed_single_insertion", ((0, 1), (1, 2)), (1,), 5),
        ("nonzero_antihermitian_word", ((0, 1), (0, 2), (1, 2)), (0, 1), 1),
    ):
        host = d.c.Host.create(3, edges)
        js, beta, limit = (F(1), F(-1, 2), F(3, 4)), F(1, 32), 2
        fields = tuple((-1)**(twist >> i & 1) for i in range(3))
        ordinary = {s: d.c.field_activity(host, s, beta, js, fields)[0]
                    for s in d.c.connected_sets(host)}
        marked = {}
        for size in range(len(roots), 4):
            for vertices in combinations(range(3), size):
                if set(roots).issubset(vertices) and d.forest_count(host, vertices, roots):
                    marked[vertices] = d.marked_activity(host, vertices, roots, twist, beta, js)[0]
        ref = d.Reference(host, roots, ordinary.__getitem__, marked.__getitem__)
        exact_mean = ref.exact_draw_mean(limit)
        direct = d.direct_sum(host, roots, ordinary, marked, limit)
        numerator, n_error = d.inserted_partition(host, (0, 1, 2), roots, twist, beta, js)
        z, z_error = d.c.field_partition(host, (0, 1, 2), beta, js, fields)
        rng = random.Random(241025+twist)
        draws = [ref.draw(limit, rng) for _ in range(2048)]
        controls.append({"name": name, "roots": roots, "twist": twist,
                         "exact_rational_unbiasedness": exact_mean == direct,
                         "excess_limit": limit, "truncated_ratio": float(exact_mean),
                         "restricted_ratio": float(numerator/z),
                         "ratio_residual": abs(float(exact_mean-numerator/z)),
                         "numerator_taylor_error": str(n_error), "denominator_taylor_error": str(z_error),
                         "diagnostic_draws": len(draws),
                         "diagnostic_mean": math.fsum(map(float, draws))/len(draws),
                         "diagnostic_max_abs_draw": float(max(map(abs, draws))),
                         "diagnostic_is_certified_estimate": False})
    n = 128
    paulis = [(1 << i, (1 << (i-1)) if i else 0, 0) for i in range(n)]
    physical = lp.d.Physical.create(n, paulis, [1]*n, F(1, 32))
    decoder = lp.linear.build_linear_decoder(physical)
    pulled = lp.pullback(physical, decoder, paulis[64])
    host = d.c.Host.create(n, physical.pilot.edges)
    plan = d.pauli_plan(host, [1]*n, F(1, 32), pulled, F(1, 4096))
    here = Path(__file__).resolve().parent
    paths = [here/name for name in ("defect_observables.py", "linear_pullback.py", "make_receipt.py",
                                    "test_defect_observables.py", "test_linear_pullback.py",
                                    "DEFECT_OBSERVABLES.md", "HANDOFF.md")]
    dependencies = {
        "hdqi-cluster-baseline-2026-10-24": ("cluster_baseline.py", "CLUSTER_BASELINE.md"),
        "hdqi-output-sampling-2026-10-24": ("output_sampling.py", "commuting_linear.py", "OUTPUT_SAMPLING.md"),
        "hdqi-decoded-observables-2026-10-24": ("decoded_observables.py", "DECODED_OBSERVABLES.md"),
        "hdqi-coherent-sign-2026-10-24": ("coherent_sign.py",),
        "hdqi-sign-sampler-2026-10-24": ("sign_sampler.py",),
        "central-rank-2026-10-23": ("central_rank.py",),
    }
    paths += [d.ROOT/folder/name for folder, names in dependencies.items() for name in names]
    return {"status": "local_unreviewed_degree_scale_pauli_comparator", "controls": controls,
            "large_explicit_pullback": {"physical_qubits": n, "generators": n,
                                        "noncommuting_edges": len(physical.pilot.edges),
                                        "pulled_pauli": pulled, "plan": plan,
                                        "statevector_constructed": False, "estimate_executed": False},
            "strict_sign_cost_separation_ledgers": [d.separated_family(k) for k in (2, 16, 128, 1024)],
            "main_repository_modified": False, "independently_reviewed": False,
            "quantum_execution": False, "full_output_sampler": False,
            "hashes": {str(p.relative_to(d.ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("receipt.json"))
    args = parser.parse_args()
    data = receipt()
    args.output.write_text(json.dumps(data, indent=2, sort_keys=True)+"\n")
    print(json.dumps({"output": str(args.output.resolve()),
                      "all_exact_unbiasedness": all(row["exact_rational_unbiasedness"] for row in data["controls"]),
                      "diagnostic_draws": sum(row["diagnostic_draws"] for row in data["controls"]),
                      "production_estimate_executed": False}))
