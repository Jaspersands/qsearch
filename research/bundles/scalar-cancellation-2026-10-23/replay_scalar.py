"""Generate exact, replayable scalar/controller controls, not quantum claims."""

import argparse
from hashlib import sha256
import json
from math import gcd
from pathlib import Path
import random

from composer_bridge import COMPOSER_PATH, composer, solve_matrix
from scalar_cancellation import ScalarBackend


LARGE_PRIME = 170141183460469231731687303715884465961
ROOT = Path(__file__).resolve().parent


def report():
    cases = []
    settings = [
        (5, 2, 3), (13, 4, 3), (17, 8, 2), (13, 9, 2),
        (LARGE_PRIME, 2, 4), (LARGE_PRIME, 4, 3),
        (LARGE_PRIME, 6, 3), (LARGE_PRIME, 11, 2), (2**127-1, 4, 3),
    ]
    for prime, degree, rank in settings:
        reduced = gcd(degree, prime-1)
        count = composer.bank_arity(reduced, rank)
        rng = random.Random(456)
        matrix = [[rng.randrange(prime) for _ in range(count)] for _ in range(rank)]
        witness, metadata = solve_matrix(matrix, prime, degree, rank, rng=rng)
        cases.append({"public_matrix": matrix, "weights": witness.weights,
                      "replay_seed": 456, **metadata})
    sign_control = ScalarBackend(5, 4)
    sign_weights = sign_control((1, 1, 1, 1, 1), 4, 5)
    sources = [ROOT/name for name in (
        "scalar_cancellation.py", "composer_bridge.py", "test_scalar_cancellation.py",
        "replay_scalar.py", "SCALAR_CANCELLATION.md", "HANDOFF.md")]
    sources.append(COMPOSER_PATH)
    return {
        "status": "CONSTRUCTIVE_CLASSICAL_SCALAR_BACKEND_ONLY", "cases": cases,
        "even_power_sign_falsifier": {
            "prime": 5, "degree": 4, "coefficients": [1]*5,
            "weights": sign_weights, "all_five_scales_required": True,
            "minus_one_is_a_fourth_power": False,
        },
        "standalone_local_bundle_not_repo_integration": True,
        "whole_quantum_receiver_error_budget_allocated": False,
        "general_polynomial_in_rank_sde_backend_implemented": False,
        "quantum_source_executed": False, "quantum_receiver_executed": False,
        "independent_theorem_review_completed": False,
        "novel_algorithm_claim": False, "classical_hardness_claim": False,
        "speedup_claim_allowed": False,
        "sha256": {str(path): sha256(path.read_bytes()).hexdigest() for path in sources},
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    payload = report()
    if args.write:
        (ROOT/"scalar_cancellation_receipt.json").write_text(json.dumps(payload, indent=2)+"\n")
    print(json.dumps({
        "status": payload["status"],
        "cases": [{key: row[key] for key in (
            "prime", "requested_degree", "reduced_degree", "observed_rank",
            "acquired_columns", "original_matrix_moment_verified", "counters")}
            for row in payload["cases"]],
        "source_hashes": len(payload["sha256"]), "speedup_claim_allowed": False,
    }, indent=2))
