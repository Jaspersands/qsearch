"""Write exact negative-result and symbolic-extension receipts."""

import argparse
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path

import paired_positivity as p


def receipt():
    root = Path(__file__).resolve().parent.parent
    here = Path(__file__).resolve().parent
    certificates = [p.witness_certificate(time) for time in (F(1, 64), F(1, 128), F(1, 1024))]
    extensions = []
    for vertices in (128, 1024):
        graph, permutation = p.extended_witness(vertices)
        extensions.append({"vertices": vertices, "edges": graph.edges,
                           "maximum_degree": graph.degree,
                           "symmetry": p.symmetry_zero_certificate(graph, permutation, 30),
                           "statevector_constructed": False, "amplitudes_evaluated": False})
    time = F(1, 64)
    lower = (F(7, 8) * time**6 / 45)**2
    local = ["paired_positivity.py", "test_paired_positivity.py", "run_audit.py",
             "PAIRED_POSITIVITY.md", "HANDOFF.md"]
    paths = [here / name for name in local]
    paths += [root / folder / name for folder, names in {
        "hdqi-cluster-baseline-2026-10-24": ["CLUSTER_BASELINE.md", "cluster_baseline.py"],
        "hdqi-offline-tangent-2026-10-24": ["OFFLINE_TANGENT.md", "offline_tangent.py"]}.items()
        for name in names]
    return {"status": "locally_certified_negative_result_for_specific_representation",
            "certificates": certificates, "connected_extensions": extensions,
            "clipping_amplification_ledger": {"one_block_bad_event_probability_lower": str(lower),
                "disjoint_blocks_sufficient_for_tv_at_least_one_minus_exp_minus_one": math.ceil(1 / lower),
                "large_instance_executed": False, "connected_amplification_claimed": False},
            "independently_reviewed": False, "novelty_certified": False,
            "quantum_execution": False, "generic_classical_hardness": False,
            "main_repository_modified": False,
            "hashes": {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
                       for path in paths}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("receipt.json"))
    args = parser.parse_args()
    data = receipt()
    args.output.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(args.output.resolve()),
                      "all_negative_intervals": all(row["negative_activity_certified"] for row in data["certificates"]),
                      "symbolic_extension_sizes": [row["vertices"] for row in data["connected_extensions"]],
                      "generic_classical_hardness": False}, sort_keys=True))
