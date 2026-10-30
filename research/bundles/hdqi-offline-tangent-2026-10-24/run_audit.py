"""Replay bounded tangent controls and ledgers; no quantum circuit is executed."""

import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import numpy as np

import offline_tangent as t


def receipt():
    terms = [(1., "XIII"), (-.7, "ZXII")]
    initial = np.eye(4).reshape(-1) / 2
    full = [t.dense_schedule_control(terms, initial, .4, steps, [(0, 1, 2, 3)] * 2)
            for steps in (8, 16, 32)]
    restricted = t.dense_schedule_control(terms, initial, .8, 32, [(0, 2), (0, 1, 2, 3)])
    opposite = []
    for sign in (-1, 1):
        rho = np.eye(4) / 4
        rho[0, 2] = rho[2, 0] = .2
        rho[1, 3] = rho[3, 1] = sign * 1e-12
        opposite.append((rho, t.polar_tangent(rho, t.pauli("ZI"))))
    discontinuity = {
        "density_trace_change": t.trace_norm(opposite[0][0] - opposite[1][0]),
        "generator_operator_change": float(np.linalg.norm(
            opposite[0][1].generator - opposite[1][1].generator, 2)),
        "cross_objective_excess": t.tangent_loss(opposite[0][0], t.pauli("ZI"),
                                                 opposite[1][1].generator) - opposite[0][1].loss}
    root = Path(__file__).resolve().parent.parent
    here = Path(__file__).resolve().parent
    local = ["offline_tangent.py", "test_offline_tangent.py", "run_audit.py",
             "OFFLINE_TANGENT.md", "HANDOFF.md"]
    paths = [here / name for name in local]
    paths += [root / folder / name for folder, names in {
        "hdqi-defect-observables-2026-10-24": ["DEFECT_OBSERVABLES.md", "defect_observables.py",
                                             "linear_pullback.py"],
        "hdqi-cluster-baseline-2026-10-24": ["CLUSTER_BASELINE.md", "cluster_baseline.py"]}.items()
        for name in names]
    symbolic = t.tfd_pauli_pullback(128, [(i, i + 1) for i in range(127)], "X" + "I" * 255)
    return {
        "status": "local_unreviewed_offline_compiler_lemma",
        "full_patch_dense_controls": full, "restricted_patch_dense_control": restricted,
        "polar_discontinuity": discontinuity,
        "symbolic_128_vertex_pullback": {"sign": symbolic[0], "pilot_word": symbolic[1],
                                         "density_table_constructed": False},
        "illustrative_cost_plan": t.endpoint_plan(128, F(1, 8), 128, F(1, 100), 20),
        "ball_growth_ledgers": [t.ball_ledger(10**6, degree, 8) for degree in (2, 4, 16)],
        "correlation_theorem_verified": False, "production_observable_estimator_executed": False,
        "main_repository_modified": False, "independently_reviewed": False,
        "quantum_execution": False, "new_polynomial_preparation_theorem": False,
        "novelty_certified": False, "quantum_advantage_established": False,
        "hashes": {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
                   for path in paths}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("receipt.json"))
    args = parser.parse_args()
    data = receipt()
    args.output.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(args.output.resolve()),
                      "full_patch_errors": [row["vector_error"] for row in data["full_patch_dense_controls"]],
                      "restricted_patch_error": data["restricted_patch_dense_control"]["vector_error"],
                      "quantum_executed": False}, sort_keys=True))
