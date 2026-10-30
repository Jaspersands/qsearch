"""Generate classical native witnesses for a rejected source extension."""

import argparse
from dataclasses import asdict
from fractions import Fraction as F
import hashlib
from itertools import product
import json
from pathlib import Path

import bent_classical as b


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def receipt():
    here = Path(__file__).resolve().parent
    rows = []
    for p, width in ((13, 3), (31, 5), (43, 7), (941, 5)):
        g, forms, allowed = b.instance(p, width, 271024)
        input_record = {"geometry": asdict(g), "forms": [asdict(f) for f in forms], "halfsets": allowed}
        rows.append({"p": p, "width": width, "M": len(forms), "dimension": g.dimension,
                     "rate": str(F(g.dimension, width*len(forms))), "input_seed": 271024,
                     "algorithm_seed": 271025, "input_sha256": digest(input_record),
                     "result": b.solve(g, forms, allowed, 271025)})
    g, forms, allowed = b.instance(7, 3, 1)
    failures = sum(b.linear_attempt(g, forms, allowed, ((a,), (c,)))["status"] == "RETRY_SINGULAR"
                   for a, c in product(range(7), repeat=2))
    dependencies = {
        "../orbit-residual-decoder-2026-10-24/orbit_decoder.py": None,
        "../orbit-residual-decoder-2026-10-24/ORBIT_DECODER.md": None,
        "../orbit-residual-decoder-2026-10-24/source_context.json": None}
    return {"status": "CLASSICAL_FALSIFIER_OF_COORDINATE_MM_PERFECT_SEARCH_EXTENSION",
            "native_classical_runs": rows,
            "exhaustive_singularity_control": {"p": 7, "choices": 49, "singular": failures,
                                               "fraction": str(F(failures, 49)), "bound": "2/7"},
            "scope": {"fixed_input_theorem": "LOCAL_UNREVIEWED",
                      "anisotropic_cubic_problem_solved": False, "all_bent_functions_dequantized": False,
                      "quantum_algorithm_executed": False, "new_candidate_admitted": False,
                      "novelty_or_independent_review_claimed": False},
            "source_sha256": {name: hashlib.sha256((here/name).read_bytes()).hexdigest()
                              for name in ("bent_classical.py", "test_bent_classical.py", "make_receipt.py",
                                           "BENT_CLASSICAL.md", *dependencies)}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(receipt(), indent=2, sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")
