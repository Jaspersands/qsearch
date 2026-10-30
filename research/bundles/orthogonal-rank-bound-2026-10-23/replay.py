"""Produce exact lower-bound deductions and finite controls, not timing fits."""

import hashlib
import json
from pathlib import Path

import rank_bound as rb


def main():
    here = Path(__file__).resolve().parent
    files = [here / name for name in ("rank_bound.py", "test_rank_bound.py", "replay.py",
                                      "RANK_DEPENDENT_COMPARISON.md")]
    files += [Path(rb.op.__file__), rb.WORK / "central-rank-2026-10-23/central_rank.py"]
    scalings = []
    for n, q in ((8, 3), (16, 3), (32, 3), (64, 3), (128, 3), (8, 127), (8, 2**127-1)):
        scalings.append({"rank": n, "field_order": q,
                         "classical_queries_necessary_for_two_thirds": rb.necessary_queries(n, q),
                         "fixed_point_bound": str(rb.fixed_point_bound(n, q)),
                         "root_fixed_point_ratio": str(rb.root_fixed_point_ratio(n, q)),
                         "proposed_quantum_query_schedule": rb.op.recovery_budget(n, q),
                         "deduced_not_measured": True})
    report = {
        "status": "published-bound application with local derivation; independent review pending",
        "primary_source": "https://pages.uoregon.edu/kantor/PAPERS/gkfinal.pdf",
        "source_locator": "Section 3.2 pp753-754; Lemma 3.14 pp756-758",
        "assumptions": ["odd effective finite field", "Witt rank at least three",
                        "full maximal-singular stabilizer", "random opaque injective coset names",
                        "uniform hidden space in one known component"],
        "quantum_algorithm_executed": False,
        "natural_source_hardness_established": False,
        "novelty_established": False,
        "finite_controls": [rb.finite_control(n, p) for n, p in ((3, 3), (3, 5), (4, 3))],
        "scaling_deductions": scalings,
        "source_hashes": {str(path.relative_to(rb.WORK)): hashlib.sha256(path.read_bytes()).hexdigest()
                          for path in files},
    }
    destination = here / "rank_bound_receipt.json"
    destination.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"receipt": str(destination), "finite_spaces_checked": 2632,
                      "scaling_deductions": len(scalings)}, indent=2))


if __name__ == "__main__":
    main()
