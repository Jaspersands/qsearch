"""Replay finite algebra controls and exact bounds, not a quantum algorithm."""

import argparse
from fractions import Fraction as F
import hashlib
from itertools import product
import json
from pathlib import Path
import random

import orbit_decoder as o


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def rank_control(right):
    g = o.geometry(19, 3, 4)
    columns = [[tuple(sum(e*pow(x, j, 19) for e, x in zip((u, w, v), points)) % 19
                      for j in range(3)) for u, w in product(range(19), repeat=2)]
               for points, v in zip(g.points[:2], right)]
    failures = sum(all((x[i]*y[j]-x[j]*y[i]) % 19 == 0
                       for i, j in ((0, 1), (0, 2), (1, 2)))
                   for x in columns[0] for y in columns[1])
    return {"fixed_last_frequencies": right, "free_assignments": 19**4,
            "rank_deficient": failures, "exact_fraction": str(F(failures, 19**4)),
            "valid_source_contract": all(right),
            "valid_contract_bound": str(o.rank_failure_bound(19, 3, 12, 2, 3))}


def receipt():
    here = Path(__file__).resolve().parent
    g, rng = o.geometry(2053, 3, 68), random.Random(261024)
    errors = [[0]*3 for _ in g.representatives]
    for j, i in enumerate(rng.sample(range(len(g.representatives)), 50)):
        errors[i] = [rng.randrange(g.p), rng.randrange(g.p), j+1]
    rows = o.syndrome(g, errors)
    result = o.decode(g, 51, rows)
    basis = {k: v for k, v in result.items() if k not in ("errors", "locator", "support")}
    basis.update({"p": g.p, "M": len(g.representatives), "dimension": g.dimension,
                  "degree": 50, "seed": 261024, "exact_recovery": result.get("errors") == errors,
                  "syndrome_sha256": digest(rows), "errors_sha256": digest(errors),
                  "kind": "one_classical_basis_label_not_a_quantum_state",
                  "halfset_fourier_last_frequencies_sampled": False})
    return {
        "status": "LOCAL_UNREVIEWED_ALGORITHM_DERIVATION_WITH_FINITE_CONTROLS",
        "basis_decoder_run": basis,
        "exhaustive_fixed_frequency_rank_controls": [rank_control(v) for v in ((1, 1), (2, 7), (0, 0))],
        "ideal_perfect_search_bound": o.perfect_search_certificate(),
        "classical_control": {
            "width3_split_form_flat": "(t,t,last_constant) for x^2-y^2",
            "width3_anisotropic_form": "x^2-3*y^2 over F7 has no nonzero isotropic vector",
            "width4_local_flat_direction_F7": o.isotropic_ternary(7, (1, 2, 3)),
            "global_classical_algorithm_excluded": False,
            "matched_classical_campaign_run": False},
        "admission": {"speedup": False, "novelty": False, "independent_review": False,
                      "quantum_execution": False, "native_witness": False,
                      "natural_problem_reduction": False, "main_registry_integrated": False},
        "source_sha256": {name: hashlib.sha256((here/name).read_bytes()).hexdigest()
                          for name in ("orbit_decoder.py", "test_orbit_decoder.py", "make_receipt.py",
                                       "ORBIT_DECODER.md", "HANDOFF.md", "source_context.json")}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(receipt(), indent=2, sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")
