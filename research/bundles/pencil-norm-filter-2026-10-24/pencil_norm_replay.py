"""Reproduce exact classical answers without expanding any large norm."""

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path

import sympy as sp

from pencil_norm import solve_ut_pencil_norm, transformed
from power_product_replay import mersenne_127_certificate


def audit():
    p, controls = 2**127-1, []
    for d in (3, 6, 10):
        variables = sp.symbols(f"x:{d}")
        answer = solve_ut_pencil_norm(variables[0]+variables[1]**2, variables[1], p, variables)
        assert answer.status == "CLASSICALLY_SOLVED"
        assert len(answer.lie_basis) == 1+(d-2)*(d-3)//2
        assert sum(bool(t) for t in answer.translation_coefficients) == 1
        assert all(not A[1][j] for A in answer.lie_basis for j in range(d))
        assert all(not A[0][j] for A in answer.lie_basis for j in range(2, d))
        row = asdict(answer)
        row.update({"exact_formal_degree_for_this_family": 2*p,
                    "old_small_factor_support_guard": False,
                    "old_raw_degree_guard": p > (d-1)*2*p,
                    "exposed_mixed_frobenius_degree": p+1,
                    "old_no_carry_guard": False,
                    "orbit_module_rank_lower_bound": p,
                    "orbit_rank_evidence": "written coefficient projection and Vandermonde proof; not enumerated",
                    "finite_pencil_generators_verified": len(answer.group_generators),
                    "large_norm_expanded": False})
        controls.append(row)
    counterexamples = []
    x, z, y = sp.symbols("x z y")
    for prime in (3, 5):
        P, Q = x**prime-x*z**(prime-1), y**prime-y*z**(prime-1)
        norm = sp.Poly(P**prime-P*Q**(prime-1), x, z, y, modulus=prime)
        g = sp.Matrix([[1, 0, 0], [0, 1, 1], [0, 0, 1]])
        assert transformed(norm, g) == norm
        assert transformed(sp.Poly(Q, x, z, y, modulus=prime), g) != sp.Poly(Q, x, z, y, modulus=prime)
        answer = solve_ut_pencil_norm(P, Q, prime, (x, z, y))
        assert answer.status == "OUT_OF_SCOPE"
        counterexamples.append({"prime": prime, "norm_preserved": True, "denominator_preserved": False,
                                "filter_status": answer.status, "reason": answer.reason})
    return {"status": "COPRIME_SMALL_ATOM_PENCIL_NORMS_CLASSICALLY_SOLVED",
            "theorem_status": "LOCAL_WRITTEN_PROOF_NOT_INDEPENDENTLY_REVIEWED",
            "prime_certificate": mersenne_127_certificate(), "controls": controls,
            "nested_norm_counterexamples": counterexamples,
            "original_problem": "formal polynomial stabilizer with public exposed P,Q",
            "general_matrix_group_backend_implemented": False,
            "arbitrary_circuit_decomposition_implemented": False,
            "quantum_algorithm_executed": False, "speedup_claim": False,
            "classical_novelty_claim": False, "guard_failure_means": "OUT_OF_SCOPE_NOT_HARDNESS"}


def record():
    result = audit()
    root = Path(__file__).resolve().parent
    names = ["pencil_norm.py", "test_pencil_norm.py", "pencil_norm_replay.py", "RESULT.md", "HANDOFF.md",
             "../power-product-filter-2026-10-24/power_product.py",
             "../power-product-filter-2026-10-24/power_product_replay.py"]
    result["source_sha256"] = {name: hashlib.sha256((root/name).read_bytes()).hexdigest() for name in names}
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = record()
    payload = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(payload)
    print(json.dumps({"status": result["status"],
                      "controls": [{"D": row["dimension"], "lie_dimension": len(row["lie_basis"])}
                                   for row in result["controls"]],
                      "counterexamples": result["nested_norm_counterexamples"]}, indent=2))
