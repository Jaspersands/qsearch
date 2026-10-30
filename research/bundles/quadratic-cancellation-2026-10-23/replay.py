"""Generate exact, seeded arithmetic receipts; no quantum experiment runs."""

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import random

from quadratic_cancellation import WORK, SmoothPowerRoots, quadratic_arity, quadratic_witness


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    cases = []
    primes = (3, 5, 7, 13, 43, 257, 263, 2**64-2**32+1,
              2**127-295, 2**127-39, 2**127-1)
    for prime in primes:
        for rank in (1, 2, 4, 8, 16):
            size = quadratic_arity(rank)
            rng = random.Random(61)
            matrix = tuple(tuple(int(i == j) if j < rank else rng.randrange(prime)
                                 for j in range(size)) for i in range(rank))
            witness = quadratic_witness(matrix, prime, rank,
                                        rng=random.Random(415), security_bits=40)
            assert all(sum(a*x*x for a, x in zip(row, witness.weights)) % prime == 0
                       for row in matrix)
            cases.append({"control": "full_rank", "matrix": matrix,
                          "witness": asdict(witness)})
    for prime in primes:
        zeta = SmoothPowerRoots(prime, 2, rng=random.Random(81), attempt_cap=41).generator
        matrix = ((1, -zeta % prime, -zeta % prime, zeta*zeta % prime),)
        witness = quadratic_witness(matrix, prime, 1, rng=random.Random(81), security_bits=40)
        assert witness.method == "four_cell_scalar"
        cases.append({"control": "four_nonempty_cells", "matrix": matrix,
                      "witness": asdict(witness)})
    here = Path(__file__).resolve().parent
    sources = (here / "quadratic_cancellation.py", here / "replay.py",
               here / "test_quadratic_cancellation.py",
               WORK / "central-rank-2026-10-23/central_rank.py",
               WORK / "scalar-cancellation-2026-10-23/scalar_cancellation.py")
    return {
        "scope": "published classical quadratic SDE primitive, prime fields only",
        "new_coverage": "p=1 mod4; an existing specialized p=3 mod4 polynomial-bank solver already exists",
        "reference": "https://arxiv.org/html/1503.09016#S2.SS1",
        "quantum_source_executed": False,
        "complete_hsp_reduction_validated": False,
        "independent_proof_review_completed": False,
        "seeded_controls_certify_abort_probability": False,
        "input_oracle_candidates_created": False,
        "moving_repository_modified": False,
        "sources_sha256": {str(path.relative_to(WORK)): digest(path) for path in sources},
        "arity_comparison": [{"rank": rank, "quadratic_bank": quadratic_arity(rank),
                              "scalar_recursive_bank": 3**rank}
                             for rank in (1, 2, 4, 8, 16, 32, 64)],
        "cases": cases,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    receipt = run()
    args.output.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"output": str(args.output), "exact_witnesses": len(receipt["cases"]),
                      "four_cell_controls": sum(case["control"] == "four_nonempty_cells"
                                                for case in receipt["cases"]),
                      "largest_prime_bits": 127, "largest_rank": 16}, indent=2))
