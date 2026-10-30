"""Produce exact local affine-filter certificates, never speedup admissions."""

import argparse
from dataclasses import asdict
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import affine_converse as a

HERE = Path(__file__).resolve().parent


def encoded(value):
    return (json.dumps(value, sort_keys=True, indent=2, default=str)+"\n").encode("ascii")


def serialize(result):
    return {**result, "branches": [asdict(b) for b in result["branches"]]}


def report():
    cases = []
    for c in (F(0), F(1, 3), F(1, 2), F(13, 20), F(1)):
        q, effects = a.four_message(c)
        result = a.audit(q, effects)
        if result["mean_unresolved_bits"] != 4*c*c-c**4:
            raise ArithmeticError("four-message certificate mismatch")
        cases.append({"c": str(c), "spectrum": list(map(str, q)),
                      "result": serialize(result)})
    signed_q = (F(1, 10), F(3, 10), F(3, 10), F(3, 10))
    mixtures = [((0, 1, 2, 3), F(2, 5))]
    mixtures += [(pair, F(1, 5)) for pair in ((1, 2), (1, 3), (2, 3))]
    signed = a.audit(signed_q, a.mixture_effects(signed_q, mixtures))
    if signed["mean_unresolved_bits"] != F(3, 5):
        raise ArithmeticError("signed-overlap certificate mismatch")
    names = ("AFFINE_CONVERSE.md", "HANDOFF.md", "source_context.json",
             "affine_converse.py", "test_affine_converse.py", "make_receipt.py")
    return {"status": "local_unreviewed_link_from_known_measurement_cone_to_existing_classical_comparator",
            "source_sha256": {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                              for name in names},
            "four_message_cases": cases, "signed_overlap_case": serialize(signed),
            "fixed_sign_countercontrol": a.fixed_sign_countercontrol(),
            "theorem_scope": "covariant_unambiguous_binary_affine_filter_direction_laws",
            "random_sign_classical_bound": "E_b TV <= min(1,3*rank_failure_probability)",
            "fixed_instance_Gibbs_error_upper": None,
            "growing_block_mixture_complexity": "UNKNOWN_without_explicit_representation",
            "coherent_input_success": "requires_separate_reduction",
            "arbitrary_residual_quantum_processing_simulated": False,
            "new_quantum_algorithm": False,
            "decision": "do_not_treat_affine_filter_LP_as_escape_from_positive_mixture_baseline",
            "prior_art": "https://arxiv.org/html/2606.07852v2"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = report()
    if args.write:
        (HERE/"receipt.json").write_bytes(encoded(result))
    if args.output:
        args.output.write_bytes(encoded(result))
    print(json.dumps({"status": result["status"], "four_message_cases": 5,
                      "signed_overlap_unresolved_dimension": "3/5",
                      "fixed_instance_sampling": "UNKNOWN"}, sort_keys=True))
