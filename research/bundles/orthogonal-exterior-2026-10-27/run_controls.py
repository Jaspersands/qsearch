"""Reproducible finite receipt; never presents simulation as quantum execution."""

import argparse
from fractions import Fraction
import json
from pathlib import Path

import exterior_probe as ep
from exterior_controls import native_fixture


def receipt():
    native = [native_fixture(n, k, 3, seed)
              for n, k, seed in ((3, 1, 81), (4, 1, 82), (4, 2, 83))]
    budgets = [ep.recovery_budget(4, 3, 40), ep.recovery_budget(64, 2**127-1, 80)]
    for item in budgets:
        epsilon = Fraction(item["error_target"])
        error = sum(Fraction(item[key]) for key in
                    ("geometry_failure_bound", "all_rank_failure_bound",
                     "row_sampler_failure_bound", "integer_sampler_failure_bound"))
        error += Fraction(item["error_per_complete_instrument"])*item["original_oracle_query_cap"]
        assert error <= epsilon
    return {"status": "finite_native_oracle_reference_and_analytic_budget_only",
            "quantum_algorithm_executed": False, "natural_input_speedup_established": False,
            "native_runs": native, "analytic_quantum_budgets": budgets,
            "boundary": "exterior receiver requires 1<=k<=n-2; higher ranks need existing receiver",
            "classical_lower_bound_scope": "proposed proof for opaque hidden lines only; not inferred from receipt"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", type=Path)
    group.add_argument("--check", type=Path)
    args = parser.parse_args()
    data = receipt()
    encoded = json.loads(json.dumps(data))
    if args.write:
        args.write.write_text(json.dumps(data, indent=2)+"\n", encoding="utf-8")
    else:
        if json.loads(args.check.read_text(encoding="utf-8")) != encoded:
            raise SystemExit("receipt differs from deterministic replay")
    print(json.dumps({"verified": True, "native_runs": len(data["native_runs"]),
                      "classical_calls": [r["classical_oracle_queries"] for r in data["native_runs"]],
                      "quantum_algorithm_executed": False}))


if __name__ == "__main__":
    main()
