"""Regenerate a scoped exact-arithmetic receipt, never a speedup verdict."""

import hashlib
import json
from pathlib import Path

from sympy import Matrix, eye

from kernel_output import (
    module_pairing, odd_maximal_order, odd_maximal_split,
    order_from_module, reconstruct,
)
from uniform_source_bound import smooth_denominator


def main():
    root = Path(__file__).resolve().parent
    rows = []
    for p, ell in [(3, 5), (7, 13), (11, 3), (19, 7), (11, 13)]:
        order = odd_maximal_order(p)
        kernel = Matrix([[1, 0], [1, 2], [0, 1], [2, 3]])
        out = reconstruct(order, odd_maximal_split(p, ell), kernel, ell)
        alternate = order_from_module(order, out.module_numerator, ell)
        gram = Matrix(8, 8, lambda i, j:
                      (order.traces*module_pairing(order, out.module_basis[:, i], out.module_basis[:, j], ell))[0])
        inclusion = ell*out.module_numerator.inv()
        checks = {
            "module_index": out.module_numerator.det() == ell**4,
            "order_index": out.order_numerator.det() == ell**16,
            "independent_order_agreement": alternate == out.order_numerator,
            "trace_gram_determinant": gram.det() == p**4,
            "positive_trace_gram": all(gram[:i, :i].det() > 0 for i in range(1, 9)),
            "integral_phi_module_inclusion": all(x.q == 1 for x in inclusion),
        }
        if not all(checks.values()):
            raise AssertionError(checks)
        rows.append({"p": p, "ell": ell, "checks": checks,
                     "module_numerator_hnf": [[int(x) for x in row] for row in out.module_numerator.tolist()],
                     "order_numerator_index": str(out.order_numerator.det()),
                     "trace_gram_determinant": int(gram.det())})
    sources = {}
    for name in ("kernel_output.py", "test_kernel_output.py", "replay_kernel_output.py", "KERNEL_TO_OUTPUT.md", "HANDOFF.md",
                 "uniform_source_bound.py", "test_uniform_source_bound.py", "UNIFORM_SOURCE_BOUND.md"):
        sources[name] = hashlib.sha256((root/name).read_bytes()).hexdigest()
    uniform = smooth_denominator(odd_maximal_order(11), 13, 11)
    record = {
        "schema": "isolated-exact-algebra-receipt-v1",
        "status": "CONDITIONAL_POSTPROCESSING_INDEPENDENT_REVIEW_PENDING",
        "input": "Correct abstract Lagrangian plus full source order and specified split",
        "kernel_recovery_executed": False,
        "geometric_backend_executed": False,
        "quantum_algorithm_executed": False,
        "speedup_admitted": False,
        "source_sha256": sources,
        "cases": rows,
        "uniform_source_bound": {
            "p": 11, "ell": 13,
            "physical_length_bound": uniform["physical_length_bound"],
            "quaternion_length_bound": uniform["quaternion_length_bound"],
            "trace_bound_bits": uniform["trace_bound"].bit_length(),
            "denominator_bits": uniform["denominator"].bit_length(),
            "largest_auxiliary_prime": max(uniform["primes"]),
            "auxiliary_prime_count": len(uniform["primes"]),
            "same_bound_for_all_queries": True,
            "geometric_cost_not_measured": True,
        },
    }
    destination = root/"kernel_output_receipt.json"
    destination.write_text(json.dumps(record, indent=2)+"\n")
    print(json.dumps({"receipt": str(destination), "cases": len(rows),
                      "checks_per_case": len(rows[0]["checks"]), "all_passed": True,
                      "speedup_admitted": False}, indent=2))


if __name__ == "__main__":
    main()
