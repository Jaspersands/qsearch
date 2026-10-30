"""Reproduce arithmetic evidence without promoting a geometric claim."""

import hashlib
import json
from pathlib import Path

from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_form

from smooth_repolarization import certificate, evaluate, resource_plan, verify_certificate


def evidence():
    sample = resource_plan(3723, 61, 103)
    proof = certificate(3723, sample["denominator"])
    checks = verify_certificate(proof)
    if not all(checks.values()):
        raise AssertionError(checks)
    h = ((1,0,1,-2), (0,1,2,1), (1,2,6,0), (-2,1,0,6))
    e = Matrix(evaluate(certificate(7,30)["E"], h))
    snf = smith_normal_form(e, domain=ZZ)
    return {
        "status": "PROPOSED_SOURCE_LEMMA_REVIEW_PENDING",
        "input_scope": "dimension_two_common_unit_weak_isogeny_with_prime_square_access",
        "coefficient_certificate": {key: proof[key] for key in (
            "trace", "denominator", "coin_x", "coin_y", "four_squares_x", "four_squares_y")},
        "ring_identity_checks": checks,
        "sample_resource_plan": sample,
        "nonfree_kernel_smith_invariants": [abs(int(snf[i,i])) for i in range(32)],
        "resource_sweep": [resource_plan(2**bits+3,2**127-1,103) for bits in (8,32,128,256,1024)],
        "quotient_strategy": "direct_A26_at_each_small_prime_square_not_unmodified_Algorithm_1",
        "formal_proof_assistant_used": False,
        "geometric_backend_executed": False,
        "quantum_receiver_executed": False,
        "new_speedup_admitted": False,
        "novelty_established": False,
        "classical_comparators": ["weak_scalar_sign_enumeration",
                                  "polarized_descent_membership",
                                  "scaled_polarized_endomorphism_transport"],
    }


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    result = evidence()
    paper_hash = hashlib.sha256((root/"robert-2024-406.pdf").read_bytes()).hexdigest()
    if paper_hash != "84a16373a8d7da78cf990511d5232e976b65996adf76e4f878cf24973793edf5":
        raise ValueError("Robert source differs from the reviewed version")
    conversion_hash = hashlib.sha256((root/"page-robert-soumier-2026-276.pdf").read_bytes()).hexdigest()
    if conversion_hash != "7c5bf9474b8e2589ffb84b089320790f83a8bc4c14aa3d1e4f7ed64a29033486":
        raise ValueError("Module-conversion source differs from the reviewed version")
    result["literature"] = {
        "robert": {"url": "https://eprint.iacr.org/2024/406", "sha256": paper_hash,
                   "pages": 128, "date_on_pdf": "2024-03-05", "license": "CC BY",
                   "pages_read": [9,10,11,12,14,15,16,17,18], "visually_checked": 17},
        "ppav_framework": {"url": "https://eprint.iacr.org/2026/1142",
                           "additional_pages_read": [16,17],
                           "source_receipt": "../ppav-source-2026-10-23/source_receipt.json"},
        "four_squares": "https://math.colgate.edu/~integers/sjs15/sjs15.pdf",
        "module_conversion": {"url": "https://eprint.iacr.org/2026/276", "sha256": conversion_hash,
                              "pages": 48, "pages_read": [1,2,3,4,24,25,26,31,32,33],
                              "visually_checked": 33, "license": "CC BY"},
        "surface_equivalences": {"url": "https://arxiv.org/html/2601.18050",
                                 "sections_checked": ["1.1", "1.2"]},
    }
    result["sha256"] = {name: hashlib.sha256((root/name).read_bytes()).hexdigest() for name in (
        "smooth_repolarization.py", "test_smooth_repolarization.py", "SMOOTH_REPOLARIZATION.md",
        "HANDOFF.md", "VERIFICATION.md", "replay_smooth_repolarization.py")}
    (root/"smooth_repolarization_receipt.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status": result["status"], "checks": result["ring_identity_checks"],
                      "receipt": str(root/"smooth_repolarization_receipt.json")}, indent=2))
