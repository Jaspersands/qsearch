"""Conditional scaling test for target-blind candidate lists, not CVP hardness."""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems import integer_character_babai as babai
from theorems import integer_character_near_vector as near

REPORT = ROOT / "research/classical_baselines/integer_character_readset.json"


def uniform_residue_mean(order):
    if type(order) is not int or order < 2 or order % 2:
        raise ValueError("an even integer order is required")
    return Q(1, 12)+Q(1, 6*order*order)


def readset_bound(length, blind_count, order, pool_size, threshold=Q(13, 200)):
    """Requires an entire conditional pool independent of the blind centers.

    The returned bound is conditional mathematics, not an information-flow
    audit. Reading all centers to rank a pre-existing pool is allowed.
    """
    mean = uniform_residue_mean(order)
    if (type(length) is not int or length < 1
            or type(blind_count) is not int or not 0 <= blind_count <= length
            or type(pool_size) is not int or pool_size < 1
            or not isinstance(threshold, Q) or not 0 <= threshold <= Q(1, 4)):
        raise ValueError("valid integer dimensions/pool size and rational threshold required")
    gap = mean-Q(length, blind_count)*threshold if blind_count else Q(0)
    exponent = 32*blind_count*gap*gap if gap > 0 else Q(0)
    # e^x >= 1+x and e > 2 give exact rational upper bounds.
    # Capping an exponent weakens the upper bound; it never underflows to zero.
    dyadic_exponent = min(4096, exponent.numerator//exponent.denominator)
    upper = min(Q(1), Q(pool_size, 1+exponent), Q(pool_size, 2**dyadic_exponent))
    return {
        "length": length, "blind_count": blind_count, "pool_size": pool_size,
        "threshold": str(threshold), "residue_mean_square": str(mean),
        "positive_gap": gap > 0, "gap": str(gap),
        "hoeffding_exponent": str(exponent),
        "dyadic_exponent_used": dyadic_exponent, "dyadic_exponent_cap": 4096,
        "success_probability_upper": str(upper),
        "preconditions": [
            "centers are mutually independent and uniform modulo the even order",
            "the blind coordinate set is fixed independently of those centers",
            "conditional on other centers and independent random coins, the entire pool has at most pool_size scalars and does not depend on blind centers",
        ],
        "ranking_may_read_all_centers": True,
        "adaptive_visited_count_is_not_a_pool_bound": True,
        "information_flow_automatically_verified": False,
        "bound_depends_on_input_dependence_not_computation_model": True,
        "unrestricted_classical_lower_bound": False,
    }


def uniform_certificate():
    blind_fraction, threshold = Q(19, 20), Q(13, 200)
    gap = Q(1, 12)-threshold/blind_fraction
    rate = 32*blind_fraction*gap*gap
    if rate <= Q(1, 150):
        raise ArithmeticError("uniform exponential-rate inequality failed")
    # For m in [20000*2^h,40000*2^h), m^4 < 2^(64+4h).
    # 64+4h <= (200/3)*(h+1) <= (200/3)*2^h <= m/300.
    if not (64 <= Q(200, 3) and 4 <= Q(200, 3)):
        raise ArithmeticError("dyadic-block polynomial-budget domination failed")
    return {
        "status": "written_conditional_argument_with_exact_constant_checks",
        "minimum_length": 20000, "minimum_blind_fraction": str(blind_fraction),
        "pool_size_at_most": "m^4", "threshold": str(threshold),
        "gap_lower": str(gap), "exponent_rate_lower": str(rate),
        "simplified_rate_lower": "1/150",
        "success_probability_upper": "2^(-m/300)",
        "integer_dyadic_exponent_at_minimum_length": 66,
        "asymptotic_read_fraction_necessary_for_polynomial_pools": str(1-12*threshold),
        "native_lll_profile_scales_as_assumed": False,
        "kernel_checked": False,
        "unrestricted_classical_lower_bound": False,
    }


def scope_counterexamples():
    adaptive = readset_bound(1, 1, 2, 1, Q(0))
    # The adaptive solver x=c inspects the nominally blind coordinate.
    adaptive_success = Q(sum(near.witness([1], [c], 2, c)["mean_square"] == 0
                             for c in range(2)), 2)
    correlated = readset_bound(10, 10, 2, 1, Q(0))
    correlated_success = Q(sum(near.witness([1]*10, [c]*10, 2, 0)["mean_square"] == 0
                               for c in range(2)), 2)
    if (adaptive_success <= Q(adaptive["success_probability_upper"])
            or correlated_success <= Q(correlated["success_probability_upper"])):
        raise ArithmeticError("scope controls did not invalidate the misapplied bound")
    return {
        "adaptive_one_visited_candidate": {
            "actual_success": str(adaptive_success),
            "incorrect_blind_list_bound": adaptive["success_probability_upper"],
            "violated_condition": "x=c reads the nominally blind center",
            "true_pre_existing_pool_size": 2,
            "bound_charging_that_pool": readset_bound(1, 1, 2, 2, Q(0))["success_probability_upper"],
        },
        "uniform_marginals_but_correlated_centers": {
            "actual_success": str(correlated_success),
            "incorrect_independence_bound": correlated["success_probability_upper"],
            "violated_condition": "all ten coordinates equal one uniform bit",
        },
    }


def exact_control_probability(order, labels, read_indices, factory, threshold):
    """Exponential finite identity control only, never a native attack."""
    if order**len(labels) > 100000:
        raise ValueError("exhaustive control would exceed the declared state cap")
    hits = 0
    for centers in itertools.product(range(order), repeat=len(labels)):
        pool = factory(tuple(centers[i] for i in read_indices))
        hits += any(near.witness(labels, list(centers), order, x)["mean_square"] <= threshold
                    for x in pool)
    return Q(hits, order**len(labels))


def native_report():
    attack_bytes = babai.REPORT.read_bytes()
    attack = json.loads(attack_bytes)
    if attack["producer_sha256"] != hashlib.sha256(Path(babai.__file__).read_bytes()).hexdigest():
        raise ValueError("native Babai producer provenance is stale")
    source_bytes = near.REPORT.read_bytes()
    if attack["input_artifact_sha256"] != hashlib.sha256(source_bytes).hexdigest():
        raise ValueError("native input provenance is stale")
    input_report = json.loads(source_bytes)
    if input_report["producer_sha256"] != hashlib.sha256(Path(near.__file__).read_bytes()).hexdigest():
        raise ValueError("native input producer provenance is stale")
    source = input_report["native"]
    labels, order = list(map(int, source["public_labels_decimal"])), int(source["cyclic_order_decimal"])
    basis_path = ROOT/attack["basis_artifact"]
    if hashlib.sha256(basis_path.read_bytes()).hexdigest() != attack["basis_artifact_sha256"]:
        raise ValueError("native basis provenance is stale")
    rows = babai.read_basis(basis_path)
    blind, prefix_open = [], True
    for row in rows:
        near.recover_assignment(labels, order, row)
        support = [j for j, v in enumerate(row) if v]
        if prefix_open and len(support) == 1 and abs(row[support[0]]) == order:
            if support[0] in blind:
                raise ValueError("coordinate prefix is singular")
            blind.append(support[0])
        else:
            prefix_open = False
    if len(blind) != attack["exact_arithmetic"]["orthogonal_integer_prefix_rank"]:
        raise ValueError("native coordinate prefix does not match the artifact")
    branch = attack["bounded_last_plane_search"]
    witness = near.witness(labels, list(map(int, source["centers_decimal"])), order,
                           int(branch["best"]["assignment_decimal"]))
    if (str(witness["mean_square"]) != branch["best"]["mean_square"]
            or witness["accepted"] != branch["best"]["threshold_met"]):
        raise ValueError("saved native witness failed exact replay")
    bound = readset_bound(len(labels), len(blind), order, branch["trials_evaluated"])
    return {
        "schema": "integer_character_readset_v1",
        "status": "conditional_scope_and_scaling_certificate_not_a_new_speedup",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "babai_artifact_sha256": hashlib.sha256(attack_bytes).hexdigest(),
        "input_artifact_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "native": {
            "dimension": len(labels), "center_seed": source["center_seed"],
            "blind_coordinate_indices": blind,
            "read_coordinate_indices": [i for i in range(len(labels)) if i not in blind],
            "candidate_pool_size": branch["trials_evaluated"],
            "conditional_random_center_bound": bound,
            "bound_informative_at_native_parameters": Q(bound["success_probability_upper"]) < 1,
            "verified_frozen_witness_mean_square": branch["best"]["mean_square"],
            "frozen_witness_threshold_met": branch["best"]["threshold_met"],
            "bound_is_a_probability_for_this_fixed_seed": False,
            "information_flow_evidence": "written inspection of exact_normalized_babai and _round_profile: the core uses only retained target coordinates; prefix rows change the point by multiples of N, not the scalar assignment",
        },
        "uniform_conditional_certificate": uniform_certificate(),
        "scope_counterexamples": scope_counterexamples(),
        "decision": "keep the finite classical falsifier; measure profile scaling and test genuinely full-target-aware attacks; do not infer either full dequantization or hardness from this conditional bound",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    report = native_report()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"output": str(args.output),
                      "native_bound": report["native"]["conditional_random_center_bound"]["success_probability_upper"],
                      "native_falsifier_retained": report["native"]["frozen_witness_threshold_met"],
                      "unrestricted_classical_lower_bound": False}))


if __name__ == "__main__":
    main()
