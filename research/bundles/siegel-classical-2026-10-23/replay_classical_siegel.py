"""Count exact native-interface queries using explicitly scoped proof controls."""

import hashlib
import json
from pathlib import Path
from random import Random

from classical_siegel import recover, uniform_symplectic
from test_classical_siegel import hidden_plane_oracle, subspace_key


def main():
    root, rows = Path(__file__).resolve().parent, []
    for p in (3, 13, 101, 1009, 65537):
        for seed in (0, 1, 2):
            k = uniform_symplectic(p, Random(seed+80))[:, [0, 2]]
            oracle, calls = hidden_plane_oracle(k, p, seed+500)
            result = recover(oracle, p)
            correct = result["basis"] is not None and subspace_key(result["basis"], p) == subspace_key(k, p)
            if not correct or result["queries"] != len(calls):
                raise AssertionError(result)
            rows.append({"prime": p, "seed": seed, "correct": correct,
                         "queries": result["queries"], "query_bound": result["query_bound"],
                         "charts_tried": result["charts_tried"]})
    files = [root/name for name in ("classical_siegel.py", "test_classical_siegel.py",
                                   "replay_classical_siegel.py", "CLASSICAL_BASELINE.md", "HANDOFF.md")]
    files.append(root.parent/"prime-square-flags-2026-10-23"/"prime_square_flags.py")
    record = {
        "status": "PROPOSED_CLASSICAL_SQUARE_ROOT_BASELINE_REVIEW_PENDING",
        "input_contract": "Sp_4(F_p) exact LEFT stabilizer coset oracle at an odd prime",
        "fixture": "lazy opaque injective labels for exact subspace proof controls",
        "hidden_parameter_supplied_to_solver": False,
        "all_actual_oracle_calls_charged": True,
        "deterministic_eight_chart_cover": True,
        "geometric_source_executed": False,
        "geometric_oracle_cost_measured": False,
        "quantum_algorithm_executed": False,
        "polynomial_bit_time_dequantization": False,
        "speedup_admitted": False,
        "cases": rows,
        "source_sha256": {str(path.relative_to(root.parent)): hashlib.sha256(path.read_bytes()).hexdigest()
                          for path in files},
    }
    destination = root/"classical_siegel_receipt.json"
    destination.write_text(json.dumps(record, indent=2)+"\n")
    print(json.dumps({"receipt": str(destination), "cases": len(rows), "all_correct": True,
                      "largest_prime_cases": [r for r in rows if r["prime"] == 65537],
                      "geometric_source_executed": False}, indent=2))


if __name__ == "__main__":
    main()
