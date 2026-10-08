"""Exact finite gaps after ALL represented complete cyclic positivity cuts.

Saved numerical solutions propose witnesses only. Dyadic PSD certificates and
rational bounds must prove every cyclic law and a gap above every character.
This is not a population, asymptotic, copy-complexity or speedup theorem.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path

import numpy as np

from ternary_character_cyclic_decoder import (
    DERIVATION as CYCLIC_DERIVATION, REPORT as CYCLIC_REPORT,
    _bounded_product, complete_cyclic_groups,
)
from ternary_character_sdp_decoder import REPORT as SOURCE_REPORT, compile_model
from ternary_character_sdp_gap_certificate import (
    DERIVATION as PSD_DERIVATION, REPORT as ORIGINAL_GAP_REPORT,
    objective_lower, quantized_witness, root_intervals,
)
from ternary_covariant_noise import CovariantRecord

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/classical_baselines/ternary_character_cyclic_gap_certificate.json"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_cyclic_feasibility(nodes, q, witness):
    """Check ALL compiled laws; paired moments also prove exact reality."""
    description = complete_cyclic_groups(nodes, q)
    if description["status"] != "ALL_REPRESENTED_COMPLETE_CYCLIC_GROUPS":
        return {"status": "CYCLIC_COMPILATION_FAILED", "all_complete_cyclic_laws_exactly_nonnegative": False}
    K, S = len(nodes), witness["moment_scale"]
    re, im = witness["matrix_real_integer"], witness["matrix_imag_integer"]
    if type(S) is not int or S <= 0 or any(
            len(matrix) != K or any(len(row) != K or any(type(x) is not int for x in row) for row in matrix)
            for matrix in (re, im)):
        raise ValueError("complete exact integer moments and positive scale required")
    least, location, count, reality = None, None, 0, True
    for gi, group in enumerate(description["groups"]):
        m = group["order"]
        values = [divmod(entry, K) for entry in group["power_entries"]]
        i, j = values[0]
        reality = reality and re[i][j] == S and im[i][j] == 0
        for k, (i, j) in enumerate(values):
            a, b = values[-k % m]
            reality = reality and re[i][j] == re[a][b] and im[i][j] == -im[a][b]
        roots = root_intervals(m)
        for t in range(m):
            lower = 0
            for k, (i, j) in enumerate(values):
                # Re(exp(-i theta)*(x+i y)) = cos(theta)*x+sin(theta)*y.
                lower += _bounded_product(re[i][j], roots[k*t % m], "cos", True)
                lower += _bounded_product(im[i][j], roots[k*t % m], "sin", True)
            probability = Fraction(lower, S*2**48*m)
            if least is None or probability < least:
                least, location = probability, {"group_index": gi, "sector": t, "order": m}
            count += 1
    # An empty collection is vacuously feasible, not evidence of realizability.
    positive = reality and (least is None or least >= 0)
    return {"status": "ALL_COMPLETE_CYCLIC_LAWS_EXACTLY_FEASIBLE" if positive else "EXACT_CYCLIC_FEASIBILITY_FAILED",
            "description": description, "complete_cyclic_probabilities_exact_lower_checked": count,
            "minimum_complete_cyclic_probability_lower_exact": str(least) if least is not None else None,
            "minimum_lower_location": location, "all_complete_cyclic_laws_exactly_nonnegative": positive,
            "exact_reality_and_normalization_from_conjugate_powers": reality,
            "global_cross_cycle_character_realizability_certified": False}


def certify_survivor(control, original, old_certificate):
    if control["seed"] != original["seed"] or control["seed"] != old_certificate["seed"]:
        raise ValueError("same pinned training cohort required")
    records = tuple(CovariantRecord(tuple(r["first"]), tuple(r["second"]), tuple(r["outcome"]), r["modulus"])
                    for r in original["training_records"])
    model = compile_model(records, max_matrix_nodes=control["model"]["matrix_nodes"])
    for field in ("nodes", "native_nodes"):
        if json.dumps(model[field]) != json.dumps(old_certificate[field]) or json.dumps(model[field]) != json.dumps(control["model"][field]):
            raise ValueError("unchanged public moment model and score linkage required")
    matrix = np.array(control["solver"]["matrix_real"])+1j*np.array(control["solver"]["matrix_imag"])
    witness = quantized_witness(model, matrix)
    if not witness["PSD_certified"]:
        return {"seed": control["seed"], **witness}
    cyclic = exact_cyclic_feasibility(model["nodes"], model["modulus"], witness)
    if json.dumps(cyclic["description"]) != json.dumps(control["model"]["cyclic_description"]):
        raise ValueError("ALL strengthened constraints must be retained")
    roots = root_intervals(model["modulus"])
    if json.dumps(roots) != json.dumps(old_certificate["root_intervals"]):
        raise ValueError("unchanged independently verifiable root intervals required")
    census = old_certificate["character_census"]
    if census["status"] != "ALL_FULL_ROOT_SECRETS_EXACT_INTERVAL_BOUNDED" or census["secrets_checked"] != model["modulus"]**model["dimension"]:
        raise ValueError("complete original all-character upper certificate required")
    lower = objective_lower(records, model["native_nodes"], witness, roots)
    upper = int(census["global_character_score_upper_numerator"])*witness["moment_scale"]
    gap = lower-upper
    status = "EXACT_FINITE_SDP_CHARACTER_GAP" if cyclic["all_complete_cyclic_laws_exactly_nonnegative"] and gap > 0 else "NO_STRENGTHENED_GAP_CERTIFIED"
    return {"status": status, "seed": control["seed"], "dimension": model["dimension"], "modulus": model["modulus"],
            "nodes": model["nodes"], "native_nodes": model["native_nodes"], "witness": witness,
            "root_interval_denominator": str(2**48), "root_intervals": roots, "character_census": census,
            "cyclic_feasibility": cyclic, "strengthening": "ALL_REPRESENTED_COMPLETE_CYCLIC_POSITIVITY",
            "SDP_feasible_score_lower_numerator": str(lower), "all_character_score_upper_same_scale_numerator": str(upper),
            "strict_gap_lower_numerator": str(gap), "score_common_denominator": str(2**72),
            "strict_gap_per_qutrit_approximation_NOT_certificate": gap/2**72/len(records),
            "exact_SDP_optimum_or_dual_certificate_required": False,
            "finite_counterexample_is_population_or_asymptotic_failure": False,
            "certification_uses_truth_or_holdout": False,
            "cached_census_requires_independent_verifier_replay": True}


def build_report():
    source = json.loads(SOURCE_REPORT.read_text())
    cyclic = json.loads(CYCLIC_REPORT.read_text())
    old = json.loads(ORIGINAL_GAP_REPORT.read_text())
    if cyclic["source_report_sha256"] != sha256(SOURCE_REPORT) or old["source_report_sha256"] != sha256(SOURCE_REPORT) or cyclic["gap_report_sha256"] != sha256(ORIGINAL_GAP_REPORT):
        raise ValueError("cached numerical matrices and census require unchanged source ancestry")
    if cyclic["derivation_sha256"] != sha256(CYCLIC_DERIVATION) or old["derivation_sha256"] != sha256(PSD_DERIVATION):
        raise ValueError("unchanged proof derivations required")
    originals = {c["seed"]: c for c in source["native_controls"]}
    old_certificates = {c["seed"]: c for c in old["certificates"]}
    controls = {c["seed"]: c for c in cyclic["controls"]}
    return {"status": "EXACT_FINITE_NATIVE_CHARACTER_SDP_GAP_RESEARCH_ONLY",
            "strengthening": "ALL_REPRESENTED_COMPLETE_CYCLIC_POSITIVITY",
            "source_report_sha256": sha256(SOURCE_REPORT), "derivation_sha256": sha256(PSD_DERIVATION),
            "cyclic_decoder_report_sha256": sha256(CYCLIC_REPORT), "original_gap_report_sha256": sha256(ORIGINAL_GAP_REPORT),
            "cyclic_derivation_sha256": sha256(CYCLIC_DERIVATION),
            "certificates": [certify_survivor(controls[s], originals[s], old_certificates[s]) for s in (93017, 93018)],
            "numerical_solver_status_used_as_proof": False, "asymptotic_impossibility_or_speedup_claim": False,
            "numerical_optimizer_reexecuted": False, "new_independent_experiment": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": report["status"], "certificates": [
        {"seed": c["seed"], "status": c["status"], "gap_per_qutrit": c.get("strict_gap_per_qutrit_approximation_NOT_certificate"),
         "cyclic_laws": c.get("cyclic_feasibility", {}).get("complete_cyclic_probabilities_exact_lower_checked"),
         "minimum_cyclic_probability_lower": c.get("cyclic_feasibility", {}).get("minimum_complete_cyclic_probability_lower_exact")}
        for c in report["certificates"]]}, indent=2))


if __name__ == "__main__":
    main()
