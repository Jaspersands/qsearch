"""Bounded public controls and parameter ledgers, not a quantum HSP run."""

import hashlib
import json
from pathlib import Path

from modular_lazard import compile_word, instruction_cap
from terminal_reduction import finite_omega_recovery, terminal_plan
from test_terminal_fpt import Matrices, coset_oracle, cyclic, heisenberg_times_c9


def build_report():
    words = []
    for p, e, c in ((3, 2, 2), (5, 3, 4), (7, 1, 6), (2**127-1, 2, 3)):
        matrices = Matrices(c+1, p**e)
        X, Y = matrices.random_lie(105), matrices.random_lie(506)
        x, y, identity = [matrices.encode(a) for a in (matrices.exp(X), matrices.exp(Y), matrices.one)]
        targets = {"add": matrices.exp(matrices.add(X, Y)),
                   "bracket": matrices.exp(matrices.add(matrices.mul(X, Y), matrices.mul(Y, X), -1))}
        for operation in ("add", "bracket"):
            cert = compile_word(p, c, operation, e)
            actual, calls = cert.evaluate(x, y, identity, matrices.opaque_multiply)
            if matrices.decode_map[actual] != targets[operation]:
                raise ArithmeticError("independent matrix control failed")
            words.append({"residue_prime": p, "exponent_bound": e, "class": c,
                          "operation": operation, "verified_all_formal_coefficients": True,
                          "independent_matrix_control": True,
                          "instructions": len(cert.instructions),
                          "instruction_cap": instruction_cap(c),
                          "public_multiplications": calls,
                          "multiplication_cap": cert.multiplication_cap()})
    finite = []
    groups = [("C_81_hidden_whole_group", cyclic(81), (1,)),
              ("Heisenberg_F3_times_C9", heisenberg_times_c9(), ((1, 0, 0, 0), (0, 0, 0, 1)))]
    for name, group, generators in groups:
        hidden = group.subgroup(generators)
        result = finite_omega_recovery(group, 3, coset_oracle(group, hidden))
        if result["recovered"] != hidden:
            raise ArithmeticError("finite recovery control failed")
        finite.append({"name": name, "ambient_order": len(group.elements),
                       "recovered_order": len(result["recovered"]),
                       "verified_exact_recovery": True, "stages": result["stages"],
                       "enumeration_queries": result["oracle_queries"],
                       "enumerated_control": True})
    plans = [terminal_plan(3, 6, 4, 3), terminal_plan(5, 6, 4, 3),
             terminal_plan(2**127-1, 78, 23, 12)]
    root = Path(__file__).resolve().parent
    return {
        "status": "conditional_uniform_terminal_bound_independent_review_pending",
        "bound": "2^O(k^2 log(k+2)) * poly(input_size,log(p),log(1/error))",
        "compiler_is_existing_inverse_BCH_construction": True,
        "bounded_word_controls": words, "finite_reduction_controls": finite,
        "formal_parameter_ledgers_not_asserted_real_terminal_families": plans,
        "quantum_receiver_executed": False,
        "opaque_group_preprocessing_implemented": False,
        "general_scalar_solver_implemented": False,
        "speedup_claim": False, "novelty_established": False,
        "source_repository_or_staging_modified": False,
        "source_hashes": {name: hashlib.sha256((root/name).read_bytes()).hexdigest()
                          for name in ("modular_lazard.py", "terminal_reduction.py", "test_terminal_fpt.py",
                                       "replay.py", "TERMINAL_FPT.md")},
    }


if __name__ == "__main__":
    report = build_report()
    output = Path(__file__).with_name("terminal_fpt_receipt.json")
    output.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"receipt": str(output), "word_controls": len(report["bounded_word_controls"]),
                      "finite_reduction_controls": len(report["finite_reduction_controls"]),
                      "quantum_receiver_executed": False, "speedup_claim": False}, indent=2))
