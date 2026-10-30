"""Record exact identities and resource debt, not geometric success."""

import hashlib
import json
from pathlib import Path

from sympy import Poly

from smooth_sos import X, certify, shared_denominator, uniform_bounds


def main():
    root = Path(__file__).resolve().parent
    bounds = uniform_bounds(3, 7)
    denominator = shared_denominator(bounds, (11, 13))
    cases = []
    for f in (X-1, X**2-3*X+1, X**2-7*X+1, X**3-6*X**2+5*X-1):
        result = certify(f, degree_bound=3, height_bound=7,
                         forbidden=(11, 13), denominator=denominator)
        exact = {
            "denominator_hex": hex(result.denominator),
            "weights_hex": [hex(w) for w in result.weights],
            "polynomials_hex": [[hex(int(Poly(p, X).nth(i))) for i in range(result.polynomial.degree())]
                                for p in result.polynomials],
        }
        cases.append({
            "polynomial": str(f), "exact_weighted_identity": result.verify(),
            "weight_count": len(result.weights),
            "largest_weight_bits": max(w.bit_length() for w in result.weights),
            "certificate_sha256": hashlib.sha256(json.dumps(exact, sort_keys=True).encode()).hexdigest(),
        })
    receipt = {
        "status": "PROPOSED_GENERAL_ALGEBRAIC_SOURCE_LEMMA_REVIEW_PENDING",
        "same_denominator_for_all_cases": True,
        "denominator_bits": denominator[0].bit_length(),
        "auxiliary_prime_count": len(denominator[1]),
        "largest_auxiliary_prime": max(denominator[1]),
        "uniform_degree_bound": 3, "uniform_height_bound": 7,
        "padded_unweighted_square_count_bound": 32,
        "stabilization_copy_count_bound": str(2**31),
        "four_square_expansion_executed": False,
        "geometric_quotient_executed": False,
        "quantum_algorithm_executed": False,
        "speedup_admitted": False,
        "cases": cases,
        "source_sha256": {name: hashlib.sha256((root/name).read_bytes()).hexdigest() for name in
                          ("smooth_sos.py", "test_smooth_sos.py", "replay_smooth_sos.py",
                           "GENERAL_SMOOTH_SOS.md", "HANDOFF.md")},
        "dependency_sha256": {"../kernel-output-2026-10-23/kernel_output.py":
                              hashlib.sha256((root.parent/"kernel-output-2026-10-23"/"kernel_output.py").read_bytes()).hexdigest()},
    }
    if not all(row["exact_weighted_identity"] for row in cases):
        raise AssertionError("exact certificate failed")
    destination = root/"smooth_sos_receipt.json"
    destination.write_text(json.dumps(receipt, indent=2)+"\n")
    print(json.dumps({"receipt": str(destination), "cases": len(cases),
                      "all_passed": True, "denominator_bits": receipt["denominator_bits"],
                      "largest_auxiliary_prime": receipt["largest_auxiliary_prime"],
                      "stabilization_copy_count_bound": receipt["stabilization_copy_count_bound"],
                      "speedup_admitted": False}, indent=2))


if __name__ == "__main__":
    main()
