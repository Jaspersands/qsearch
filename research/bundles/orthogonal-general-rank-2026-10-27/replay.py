"""Deterministic finite controls and analytic budget, never a quantum run."""

import argparse
import json
from pathlib import Path

import general_rank as gr
from controls import changed_frame, expected_kernel, kernel_fiber_control

op = gr.op


def build_receipt():
    cases = [kernel_fiber_control(4, 3, 3, op.eye(8)[i]) for i in (0, 3, 4)]
    runs = []
    for k in (3, 4):
        hidden = op.image(changed_frame(4, 3), op.eye(8)[:k], 3)
        oracle = op.OpaqueFixtureOracle(hidden, 3)
        result = gr.recover_reference(oracle, 4, 3, seed=91)
        assert result["candidate"] == hidden
        runs.append({"n": 4, "p": 3, "hidden_rank_for_verification_only": k,
                     "inferred_rank": result["inferred_rank"], "attempts": result["attempts"],
                     "classical_oracle_calls": oracle.calls,
                     "dense_table_queries": sum(r["classical_table_queries"]
                                                for t in result["records"] for r in t),
                     "candidate": result["candidate"], "matches_fixture_secret": True,
                     "hidden_rank_supplied_to_controller": False})
    n, k, p = 8, 5, 2**127-1
    frame = changed_frame(n, p)
    hidden = op.image(frame, op.eye(2*n)[:k], p)
    neighbors = []
    for i in range(3):
        probe = op.make_probe(op.mv(frame, op.eye(2*n)[n+i], p), p)
        kernel, kind = expected_kernel(probe, hidden)
        assert kind == "good"
        neighbors.append(gr.neighbor(probe, kernel))
    candidate = gr.reconstruct(neighbors, n, p)
    assert candidate == hidden
    assert all(op.image(g, hidden, p) == hidden for g in gr.certificate_matrices(candidate, p))
    return {"schema": "orthogonal_unknown_rank_control_v1", "kernel_controls": cases,
            "opaque_oracle_dense_runs": runs,
            "large_prime_control": {"n": n, "k": k, "p": p,
                                    "supplied_secret_algebra_control_only": True,
                                    "three_probe_reconstruction_matches": True},
            "proposed_quantum_budget": gr.recovery_budget(64, 2**127-1, 64),
            "quantum_algorithm_executed": False, "natural_application_established": False,
            "literature_novelty_certified": False,
            "general_rank_classical_lower_bound_proved": False,
            "reflection_probability_n8_k3_q3": str(gr.reflection_hit_probability(8, 3, 3)),
            "reflection_probability_maximal": str(gr.reflection_hit_probability(8, 8, 3))}


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    receipt = Path(__file__).with_name("receipt.json")
    encoded = json.dumps(build_receipt(), indent=2, sort_keys=True)+"\n"
    if args.write:
        receipt.write_text(encoded)
        print("Wrote deterministic finite-control receipt; no quantum algorithm executed.")
    else:
        if receipt.read_text() != encoded:
            raise SystemExit("Receipt mismatch")
        print("Receipt matches fresh finite controls and analytic budget.")


if __name__ == "__main__":
    main()
