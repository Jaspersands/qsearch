"""Replay finite native-fiber controls and fingerprint their true scope."""

import hashlib
import json
from pathlib import Path
from random import Random

import qiskit
from sympy import eye

from chirp_receiver import recover
from classical_siegel import uniform_symplectic
from quantum_controls import NativeFiberControl
from test_classical_siegel import hidden_plane_oracle, subspace_key


def main():
    root, rows = Path(__file__).resolve().parent, []
    for p, seed in ((3, 0), (3, 7), (5, 1), (5, 9), (3, 42)):
        k = eye(4)[:, [0, 2]] if seed == 42 else uniform_symplectic(p, Random(seed+200))[:, [0, 2]]
        oracle, calls = hidden_plane_oracle(k, p, seed+700)
        backend = NativeFiberControl(oracle, p, seed)
        result = recover(backend.prepare, backend.measure_pair, oracle, p, block_pairs=48)
        correct = result["basis"] is not None and subspace_key(result["basis"], p) == subspace_key(k, p)
        if not correct or result["source_copies"] != backend.prepared_copies:
            raise AssertionError("native-fiber receiver failed")
        if len(calls) != backend.reference_table_queries+result["verification_queries"]:
            raise AssertionError("actual fixture query accounting failed")
        rows.append({"receiver_prime": p, "seed": seed, "correct": correct,
                     "ideal_protocol_source_copies": result["source_copies"],
                     "verification_queries": result["verification_queries"],
                     "actual_classical_fiber_table_queries": backend.reference_table_queries,
                     "pair_measurements": backend.pair_measurements,
                     "chart_outcomes": [c["status"] for c in result["charts"]],
                     "source_copy_bound": result["source_copy_bound"]})
    files = [root/name for name in ("chirp_receiver.py", "quantum_controls.py",
                                   "test_chirp_receiver.py", "replay_chirp_receiver.py",
                                   "EXPLICIT_CHIRP_RECEIVER.md", "HANDOFF.md")]
    files.extend(root.parent/"siegel-classical-2026-10-23"/name
                 for name in ("classical_siegel.py", "test_classical_siegel.py"))
    files.append(root.parent/"prime-square-flags-2026-10-23"/"prime_square_flags.py")
    record = {
        "status": "EXPLICIT_RECEIVER_PROTOCOL_WITH_FINITE_QUANTUM_CONTROLS_REVIEW_PENDING",
        "qiskit_version": qiskit.__version__,
        "decoder_supplied_secret_coefficients": False,
        "quantum_post_query_decoder_simulated": True,
        "coherent_oracle_circuit_executed": False,
        "geometric_source_executed": False,
        "scalable_prime_fourier_compiler_implemented": False,
        "quantum_hardware_used": False,
        "speedup_admitted": False,
        "cases": rows,
        "source_sha256": {str(path.relative_to(root.parent)): hashlib.sha256(path.read_bytes()).hexdigest()
                          for path in files},
    }
    destination = root/"chirp_receiver_receipt.json"
    destination.write_text(json.dumps(record, indent=2)+"\n")
    print(json.dumps({"receipt": str(destination), "all_correct": True, "cases": rows,
                      "geometric_source_executed": False}, indent=2))


if __name__ == "__main__":
    main()
