"""Exact nine-sector joint-law probes on represented order-three planes.

No new moments, optimizer, secret census or population recovery claim. The
public compiler checks every complete rank-two subgroup in represented G[3].
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
from itertools import combinations
import json
from pathlib import Path

from ternary_character_cyclic_decoder import _bounded_product, represented_differences
from ternary_character_cyclic_gap_certificate import REPORT as SOURCE_REPORT
from ternary_character_cyclic_gap_certificate import exact_cyclic_feasibility
from ternary_character_sdp_decoder import REPORT as NATIVE_REPORT
from ternary_character_sdp_gap_certificate import objective_lower, root_intervals
from ternary_covariant_noise import CovariantRecord

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/classical_baselines/ternary_character_joint_plane.json"
DERIVATION = ROOT / "research/TERNARY_CHARACTER_JOINT_PLANE.md"


def complete_order_three_planes(nodes, q, max_pairs=1000000, max_planes=100000):
    if any(type(x) is not int or x < 1 for x in (max_pairs, max_planes)):
        raise ValueError("positive whole-scan pair and plane caps required")
    differences = represented_differences(nodes, q)
    zero = (0,)*len(nodes[0])
    lines = sorted({min(d, tuple(-x % q for x in d)) for d in differences
                    if d != zero and all(3*x % q == 0 for x in d)})
    pair_count = len(lines)*(len(lines)-1)//2
    if pair_count > max_pairs:
        return {"status": "ORDER_THREE_PLANE_PAIR_CAP_EXHAUSTED", "required_pairs": pair_count,
                "partial_joint_scan_certifies_closure": False}
    seen, planes = set(), []
    for a, b in combinations(lines, 2):
        vectors = tuple(sorted(tuple((x*u+y*v) % q for u, v in zip(a, b))
                               for x in range(3) for y in range(3)))
        if len(set(vectors)) != 9 or vectors in seen:
            continue
        seen.add(vectors)
        if all(d in differences for d in vectors):
            first = next(d for d in vectors if d != zero)
            first_line = {zero, first, tuple(2*x % q for x in first)}
            second = next(d for d in vectors if d not in first_line)
            powers = tuple(tuple((x*u+y*v) % q for u, v in zip(first, second))
                           for x in range(3) for y in range(3))
            planes.append({"generators": (first, second), "group_order": 9,
                           "power_entries": tuple(differences[d] for d in powers)})
            if len(planes) > max_planes:
                return {"status": "ORDER_THREE_PLANE_COUNT_CAP_EXHAUSTED", "partial_joint_scan_certifies_closure": False}
    planes.sort(key=lambda p: p["generators"])
    return {"status": "ALL_REPRESENTED_COMPLETE_ORDER_THREE_PLANES", "planes": planes,
            "represented_order_three_lines": len(lines), "line_pairs_checked": pair_count,
            "distinct_spanned_planes_checked": len(seen), "complete_planes": len(planes),
            "incomplete_spanned_planes": len(seen)-len(planes), "joint_laws_checked": 9*len(planes),
            "unrepresented_moments_added": False, "full_secret_enumeration_used": False,
            "compilation_reads_truth_outcomes_or_witness": False}


def audit_joint_planes(certificate):
    nodes, q, witness = certificate["nodes"], certificate["modulus"], certificate["witness"]
    description = complete_order_three_planes(nodes, q)
    if description["status"] != "ALL_REPRESENTED_COMPLETE_ORDER_THREE_PLANES":
        return {"seed": certificate["seed"], "status": "NO_COMPLETE_JOINT_AUDIT", "description": description}
    re, im = witness["matrix_real_integer"], witness["matrix_imag_integer"]
    K, S, roots = len(nodes), witness["moment_scale"], root_intervals(3)
    negative, smallest, smallest_lower, reality = [], None, None, True
    for pi, plane in enumerate(description["planes"]):
        values = tuple(divmod(entry, K) for entry in plane["power_entries"])
        i, j = values[0]
        reality = reality and re[i][j] == S and im[i][j] == 0
        for x in range(3):
            for y in range(3):
                i, j = values[3*x+y]
                a, b = values[3*(-x % 3)+(-y % 3)]
                reality = reality and re[i][j] == re[a][b] and im[i][j] == -im[a][b]
        for u in range(3):
            for v in range(3):
                upper, lower = 0, 0
                for x in range(3):
                    for y in range(3):
                        i, j = values[3*x+y]
                        interval = roots[(x*u+y*v) % 3]
                        upper += _bounded_product(re[i][j], interval, "cos", False)+_bounded_product(im[i][j], interval, "sin", False)
                        lower += _bounded_product(re[i][j], interval, "cos", True)+_bounded_product(im[i][j], interval, "sin", True)
                den = 9*S*2**48
                value, lo = Fraction(upper, den), Fraction(lower, den)
                smallest = value if smallest is None or value < smallest else smallest
                smallest_lower = lo if smallest_lower is None or lo < smallest_lower else smallest_lower
                if upper < 0:
                    negative.append({"plane_index": pi, "sectors": (u, v), "generators": plane["generators"],
                                     "joint_probability_upper_numerator": str(upper), "joint_probability_upper_denominator": str(den)})
    return {"seed": certificate["seed"], "status": "EXACT_JOINT_PLANE_VIOLATIONS" if reality and negative else "NO_EXACT_JOINT_VIOLATION",
            "description": description, "negative_joint_laws": negative,
            "negative_joint_laws_certified": len(negative) if reality else 0,
            "minimum_joint_probability_upper_exact": str(smallest) if smallest is not None else None,
            "minimum_joint_probability_lower_exact": str(smallest_lower) if smallest_lower is not None else None,
            "exact_reality_and_normalization": reality,
            "all_separate_cyclic_laws_pass_exactly": certificate["cyclic_feasibility"]["all_complete_cyclic_laws_exactly_nonnegative"],
            "all_joint_laws_or_global_realizability_certified": False}


def mix_with_identity(certificate, numerator=1, denominator=4):
    """Exact convex repair, with no optimizer/rounding or untrusted new PSD test."""
    if type(numerator) is not int or type(denominator) is not int or not 0 < numerator < denominator <= 65536:
        raise ValueError("strict convex rational weight with bounded exact JSON integers required")
    parent = certificate["witness"]
    if not parent["PSD_certified"]:
        raise ValueError("certified PSD parent required")
    K, S = len(certificate["nodes"]), parent["moment_scale"]
    re = [[(denominator-numerator)*parent["matrix_real_integer"][i][j]+(numerator*S if i == j else 0)
           for j in range(K)] for i in range(K)]
    im = [[(denominator-numerator)*parent["matrix_imag_integer"][i][j] for j in range(K)] for i in range(K)]
    return {"status": "EXACT_CONVEX_PARENT_IDENTITY_MOMENT_POINT", "moment_scale": denominator*S,
            "matrix_real_integer": re, "matrix_imag_integer": im, "PSD_certified": True,
            "PSD_certificate_kind": "EXACT_CONVEXITY_FROM_INDEPENDENTLY_CERTIFIED_PARENT",
            "identity_weight_numerator": numerator, "identity_weight_denominator": denominator,
            "parent_seed": certificate["seed"], "new_numerical_factor_or_solver_used": False}


def certify_joint_cut_survivor(certificate, original):
    if certificate["seed"] != original["seed"]:
        raise ValueError("same pinned native training cohort required")
    witness = mix_with_identity(certificate)
    nodes, q = certificate["nodes"], certificate["modulus"]
    cyclic = exact_cyclic_feasibility(nodes, q, witness)
    joint = audit_joint_planes({**certificate, "witness": witness, "cyclic_feasibility": cyclic})
    records = tuple(CovariantRecord(tuple(r["first"]), tuple(r["second"]), tuple(r["outcome"]), r["modulus"])
                    for r in original["training_records"])
    lower = objective_lower(records, certificate["native_nodes"], witness, root_intervals(q))
    upper = int(certificate["character_census"]["global_character_score_upper_numerator"])*witness["moment_scale"]
    gap, den = lower-upper, witness["moment_scale"]*2**48
    least = joint["minimum_joint_probability_lower_exact"]
    positive = cyclic["all_complete_cyclic_laws_exactly_nonnegative"] and joint["exact_reality_and_normalization"] and joint["negative_joint_laws_certified"] == 0 and (least is None or Fraction(least) >= 0)
    return {"seed": certificate["seed"], "status": "EXACT_ALL_JOINT_PLANE_CUTS_CHARACTER_GAP" if positive and gap > 0 else "NO_JOINT_REPAIR_GAP_CERTIFIED",
            "witness": witness, "cyclic_feasibility": cyclic, "joint_feasibility": joint,
            "all_complete_joint_planes_exactly_nonnegative": positive,
            "SDP_feasible_score_lower_numerator": str(lower), "all_character_score_upper_same_scale_numerator": str(upper),
            "strict_gap_lower_numerator": str(gap), "score_common_denominator": str(den),
            "strict_gap_per_record_approximation_NOT_certificate": gap/den/len(records),
            "parent_census_reused_only_under_independently_verified_unchanged_records": True,
            "all_secrets_enumerated_to_construct_mixed_point": False,
            "population_or_asymptotic_failure_claim": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    source = json.loads(SOURCE_REPORT.read_text())
    native = json.loads(NATIVE_REPORT.read_text())
    if source["source_report_sha256"] != hashlib.sha256(NATIVE_REPORT.read_bytes()).hexdigest():
        raise ValueError("unchanged native training records required for exact score bounds")
    originals = {c["seed"]: c for c in native["native_controls"]}
    report = {"status": "EXACT_FINITE_JOINT_PLANE_OBSTRUCTION_REVIEW_PENDING",
              "source_report_sha256": hashlib.sha256(SOURCE_REPORT.read_bytes()).hexdigest(),
              "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
              "controls": [audit_joint_planes(c) for c in source["certificates"]],
              "all_joint_cuts_survivors": [certify_joint_cut_survivor(c, originals[c["seed"]]) for c in source["certificates"]],
              "new_optimizer_or_source_experiment": False, "population_or_asymptotic_failure_claim": False,
              "accepted_speedup_candidate": False}
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": report["status"], "controls": [
        {"seed": c["seed"], "complete_planes": c["description"].get("complete_planes"),
         "negative_joint_laws": c.get("negative_joint_laws_certified"),
         "minimum_probability_upper": c.get("minimum_joint_probability_upper_exact")}
        for c in report["controls"]], "all_joint_cuts_survivors": [
            {"seed": c["seed"], "status": c["status"], "gap_per_record": c["strict_gap_per_record_approximation_NOT_certificate"],
             "minimum_joint_lower": c["joint_feasibility"]["minimum_joint_probability_lower_exact"]}
            for c in report["all_joint_cuts_survivors"]]}, indent=2))


if __name__ == "__main__":
    main()
