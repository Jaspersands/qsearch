"""Rank-compressed arithmetic receipts; no quantum source is executed."""

import argparse
import hashlib
import json
from pathlib import Path

from central_rank import compressed_witness, terminal_envelope
from test_central_rank import capped_quadratic, rank_matrix, tiny_scalar


def run():
    root = Path(__file__).resolve().parent
    controls = []
    for prime, degree, ambient, rank, cap, width, solver in (
        (17, 4, 12, 2, 2, 25, tiny_scalar),
        (7, 3, 8, 1, 2, 16, tiny_scalar),
        (2**127-1, 2, 17, 3, 3, 27, capped_quadratic),
    ):
        matrix = rank_matrix(ambient, rank, width, prime, 2310)
        result = compressed_witness(matrix, prime, degree, cap, solver)
        moments = [sum(a*pow(x, degree, prime) for a, x in zip(row, result.weights)) % prime
                   for row in matrix]
        assert not any(moments) and any(result.weights)
        controls.append({
            "prime": prime, "degree": degree, "ambient_label_dimension": ambient,
            "observed_rank": result.observed_rank, "public_rank_cap": cap,
            "acquired_columns": width, "used_prefix_columns": result.used_prefix_columns,
            "scalar_calls": result.scalar_calls,
            "verified_original_moments": moments,
            "witness": result.weights,
            "backend": solver.__name__,
            "quantum_source_executed": False,
            "general_scalar_solver": False,
        })
    envelopes = []
    for k in (3, 5, 8, 12):
        c, m = 2*k-1, k*(k+1)//2
        ranks = tuple(range(m-2, m-c-1, -1))
        envelope = terminal_envelope(k, ranks, 127, terminal_samples=20)
        envelope["kind"] = "formal upper-envelope profile, not an asserted Lie family"
        envelope["old_multiplier_ceil_log2"] = (envelope["old_scalar_line_multiplier"]-1).bit_length()
        envelope["new_multiplier_ceil_log2"] = (envelope["compressed_multiplier"]-1).bit_length()
        envelopes.append(envelope)
    return {
        "status": "PROPOSED_PARAMETER_BOUND_WITH_EXACT_ARITHMETIC_CONTROLS",
        "old_uniform_exponent": "O(k^3 log(k+2))",
        "new_uniform_exponent": "O(k^2 log(k+2))",
        "conditional_on_whole_rees_and_outer_proof": True,
        "independently_reviewed": False,
        "quantum_receiver_executed": False,
        "speedup_claim": False,
        "arithmetic_controls": controls,
        "actual_class_three_profile_budget": terminal_envelope(3, (3, 2), 7, 5),
        "upper_envelope_profiles": envelopes,
        "source_sha256": {name: hashlib.sha256((root/name).read_bytes()).hexdigest()
                          for name in ("central_rank.py", "test_central_rank.py", "replay.py")},
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="ascii")
        print(json.dumps({"artifact": str(args.output.resolve()),
                          "controls": len(result["arithmetic_controls"]),
                          "claims": result["status"],
                          "envelope_bits_old_new": [
                              [x["k"], x["old_multiplier_ceil_log2"], x["new_multiplier_ceil_log2"]]
                              for x in result["upper_envelope_profiles"]]}))
    else:
        print(encoded)
