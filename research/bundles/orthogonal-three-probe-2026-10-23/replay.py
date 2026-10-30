"""Generate finite oracle/QFT controls and separately labeled resource bounds."""

import hashlib
import json
from pathlib import Path

import orthogonal_probe as op


def run():
    cases = []
    for n, swap in ((3, False), (3, True), (4, True), (5, True)):
        hidden = op.eye(2*n)[:n]
        if swap:
            g = [list(row) for row in op.eye(2*n)]
            g[0], g[n] = g[n], g[0]
            hidden = op.image(g, hidden, 3)
        oracle = op.OpaqueFixtureOracle(hidden, 3)
        result = op.recover_reference(oracle, n, 3, seed=83, attempts=12,
                                      samples=22, dimension_cap=10000)
        if result["candidate"] != hidden:
            raise ArithmeticError("opaque reference recovered the wrong hidden space")
        result.update({"witt_rank": n, "prime": 3,
                       "actual_classical_oracle_queries": oracle.calls,
                       "hidden_fixture": hidden,
                       "execution": "dense classical simulation of coset preparation and Fourier sampling"})
        cases.append(result)
    here = Path(__file__).resolve().parent
    sources = [here / "orthogonal_probe.py", here / "test_orthogonal_probe.py", here / "replay.py",
               op.WORK / "central-rank-2026-10-23/central_rank.py"]
    return {
        "status": "proposed reduction, not independently reviewed or novelty certified",
        "problem": "full maximal-singular stabilizer HSP in split orthogonal groups",
        "oracle_labels_expose_hidden_coordinates": False,
        "depends_on_unreviewed_rees_theorem": False,
        "natural_non_oracle_application_established": False,
        "quantum_speedup_admitted": False,
        "moving_checkout_modified": False,
        "source_sha256": {str(path.relative_to(op.WORK)): hashlib.sha256(path.read_bytes()).hexdigest()
                          for path in sources},
        "reference_executions": cases,
        "proposed_scalable_budgets_not_simulator_costs": [
            op.recovery_budget(n, p, 40) for p, n in ((3, 3), (13, 8), (2**127-1, 64))],
    }


if __name__ == "__main__":
    output = Path(__file__).resolve().parent / "orthogonal_probe_receipt.json"
    result = run()
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"output": str(output), "cases": [
        {key: case[key] for key in ("witt_rank", "attempts", "actual_classical_oracle_queries",
                                    "certificate_passed")}
        for case in result["reference_executions"]]}, indent=2))
