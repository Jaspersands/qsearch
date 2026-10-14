"""Original-record quotient completion and source-correct Gaussian rank budgets.

Multiples are external inputs, not certified truth. Gaussian probability boxes
use FLINT/Arb; algebra/rank certificates have separate independent replay.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
from itertools import product
import json
import math
from pathlib import Path

from flint import arb, ctx, fmpq, nmod_mat

from native_small_multiple_completion import _records, _rational, multiple_quotient, complete_multiple, bounded_fit, separation_ledger
from native_small_alphabet_decoder import feature_width, cubic_equation, feature_layout
from native_classical_modulus_descent import digest
from native_full_root_slice import source_data
from ternary_covariant_noise import root_digits
from ternary_noise_degradation import NoisyLinearRecord
from ternary_measured_lattice_decoder import integer, exact_json

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/NATIVE_GAUSSIAN_QUOTIENT_COMPLETION.md"
REPORT = ROOT / "research/classical_baselines/native_gaussian_quotient_completion.json"


def nearest_odd_division(value, divisor):
    integer(divisor, "positive odd divisor", 1)
    if type(value) is not int or divisor % 2 != 1: raise ValueError("exact integer and odd divisor required")
    return (value+divisor//2)//divisor


def rounded_real(value):
    value = _rational(value)+Fraction(1, 2)
    return value.numerator//value.denominator


def derive_quotient(records, coefficient, multiple):
    raw = _records(records);q, n = raw[0].modulus, len(raw[0].label)
    multiple = tuple(multiple)
    if len(multiple) != n: raise ValueError("complete original-secret multiple required")
    model = multiple_quotient(q, coefficient, multiple)
    if model is None: return {"status": "EXACT_NONUNIT_IMAGE_INCOMPATIBILITY", "derived_records": (), "model": None}
    if model.factor < 9:
        return {"status": "DERIVED_MODULUS_BELOW_DIVIDED_CUBIC_DOMAIN_NOT_NO_SECRET", "derived_records": (), "model": model.record()}
    derived, receipts = [], []
    for row in raw:
        residual = (row.value-sum(a*x for a, x in zip(row.label, model.quotient_secret))) % q
        value = nearest_odd_division(residual, model.remaining_modulus) % model.factor
        child = NoisyLinearRecord(tuple(a % model.factor for a in row.label), value, model.factor, row.source_id)
        derived.append(child)
        receipts.append({"source_id": row.source_id, "parent_record_sha256": digest(row.public()),
            "corrected_original_response": residual, "derived_record": child.public()})
    return {"status": "ONE_TO_ONE_ORIGINAL_QUOTIENT_RECORDS", "model": model.record(),
        "original_records_sha256": digest(tuple(s.public() for s in raw)),
        "derived_records": tuple(s.public() for s in derived), "record_receipts": tuple(receipts),
        "original_records_paid_once": len(raw), "new_independent_original_samples_created": False,
        "multiple_truth_or_Gaussian_law_certified": False,
        "parent_source_IDs_preserved": True, "truth_or_errors_entered_adapter": False}


def complete_alphabet_multiple(records, coefficient, multiple, radius, max_matrix_entries=2000000):
    raw = _records(records);q = raw[0].modulus
    integer(radius, "public original verification radius")
    if 4*radius >= q: raise ValueError("public original verifier requires4R<q")
    adapted = derive_quotient(raw, coefficient, multiple)
    base = {"adapter": adapted, "candidate_secret": None, "multiple_membership_in_planted_orbit_certified": False,
        "actual_planted_secret_or_noise_law_certified": False, "free_multiple_producer_supplied": False,
        "max_matrix_entries": max_matrix_entries, "verification_radius": radius}
    if adapted["status"] != "ONE_TO_ONE_ORIGINAL_QUOTIENT_RECORDS":
        return {**base, "status": adapted["status"], "decoder": None}
    children = tuple(NoisyLinearRecord(**r) for r in adapted["derived_records"])
    from native_partial_coordinate_decoder import decode as decode_coordinates
    result = decode_coordinates(children, max_matrix_entries=max_matrix_entries)
    if result["candidate_secret"] is None:
        return {**base, "status": "QUOTIENT_DECODER_INCOMPLETE_NOT_NO_ORIGINAL_SECRET", "decoder": result}
    model = adapted["model"];Q = model["remaining_modulus"]
    candidate = tuple(x+Q*h for x, h in zip(model["known_quotient_IF_multiple_is_true"], result["candidate_secret"]))
    matches = tuple(coefficient*s % q for s in candidate) == tuple(multiple)
    fit = bounded_fit(raw, candidate, radius)
    if not matches: raise ArithmeticError("completed candidate escaped the supplied multiple")
    return {**base, "status": "ONE_ALPHABET_COMPATIBLE_ORIGINAL_RADIUS_FIT_SOURCE_PREMISES_REQUIRED" if fit["fits_public_radius"] else "ORIGINAL_RADIUS_FIT_FAILED",
        "candidate_secret": candidate if fit["fits_public_radius"] else None, "decoder": result,
        "multiple_equation_verified": matches, "original_fit": fit}


def dyadic_probability_box(value, bits):
    scaled = value*2**bits
    lo = int(scaled.lower().floor().fmpz());hi = -int((-scaled.upper()).floor().fmpz())
    return {"lower": str(Fraction(max(0, lo), 2**bits)), "upper": str(Fraction(min(2**bits, hi), 2**bits))}


def gaussian_alphabet_boxes(width, bits=128):
    width = _rational(width);integer(bits, "positive probability enclosure bits", 1)
    if width <= 0: raise ValueError("positive continuous Gaussian width required")
    with ctx.workprec(bits+48):
        a = arb.const_sqrt_pi()/(2*arb(fmpq(width.numerator, width.denominator)))
        boxes = {"zero": dyadic_probability_box(a.erf(), bits),
            "each_signed_one": dyadic_probability_box((a.erfc()-(3*a).erfc())/2, bits),
            "outside_triplet": dyadic_probability_box((3*a).erfc(), bits)}
    return {"continuous_Gaussian_width": str(width), "enclosure_bits": bits, **boxes,
        "primitive": "FLINT/Arb erf/erfc on exact rational inputs with directed dyadic endpoints",
        "independent_transcendental_certificate_supplied": False,
        "conditioning_erases_outside_triplet_mass": False}


def gaussian_radius_box(width, radius, bits=128):
    width = _rational(width);integer(radius, "nonnegative original error radius")
    integer(bits, "positive probability enclosure bits", 1)
    if width <= 0: raise ValueError("positive continuous Gaussian width required")
    with ctx.workprec(bits+48):
        a = arb.const_sqrt_pi()*arb(fmpq(2*radius+1, 2))/arb(fmpq(width.numerator, width.denominator))
        return {"continuous_Gaussian_width": str(width), "integer_error_radius": radius,
            "enclosure_bits": bits, **dyadic_probability_box(a.erfc(), bits)}


def capture_budget(dimension, rows, escape):
    escape = _rational(escape)
    integer(dimension, "positive feature block dimension", 1);integer(rows, "positive original rows", 1)
    if not 0 <= escape <= 1: raise ValueError("valid row escape floor required")
    block = (escape.denominator+escape.numerator-1)//escape.numerator if escape else None
    exponent = 2*dimension-rows//block if block else None
    budget = Fraction(1, 2**min(64, max(0, -exponent))) if block else Fraction(1)
    return {"feature_block_dimension": dimension, "original_rows": rows,
        "row_escape_probability_lower": str(escape), "power_block": block,
        "block_times_escape": str(block*escape) if block else None,
        "complete_power_blocks": rows//block if block else 0,
        "union_power2_exponent": exponent, "rank_failure_upper": str(budget),
        "power_half_bound_uses_reciprocal_Bernoulli_inequality": True}


def split_rank_ledger(n, rows, zero_floor, nonzero_floor):
    z, t = _rational(zero_floor), _rational(nonzero_floor)
    if z < 0 or t < 0 or z+t > 1: raise ValueError("valid zero/nonzero probability lower bounds required")
    D, Q = feature_width(n), n*(n+1)//2
    base, quadratic = capture_budget(D-Q, rows, 2*z/9), capture_budget(Q, rows, t/3)
    return {"dimension": n, "feature_dimension": D, "base_feature_dimension": D-Q, "quadratic_feature_dimension": Q,
        "zero_probability_lower_IN_truncated_law": str(z), "nonzero_probability_lower_IN_truncated_law": str(t),
        "zero_row_base_rank_budget": base, "nonzero_row_quadratic_rank_budget": quadratic,
        "conditional_rank_failure_upper": str(min(Fraction(1), Fraction(base["rank_failure_upper"])+Fraction(quadratic["rank_failure_upper"]))),
        "secret_translation_used_only_in_rank_proof_not_decoder": True,
        "fixed_secret_original_uniform_labels_and_independent_noise_required": True,
        "full_rank_established_by_source_promise_not_small_fixtures": False}


def structural_grid(n):
    D, Q = feature_width(n), n*(n+1)//2
    if 9**n*D > 100000: raise ValueError("whole zero-row structural grid cap exceeded")
    layouts = feature_layout(n)
    base_indices = tuple(i for i, (kind, _) in enumerate(layouts) if kind not in ("u2", "uij"))
    zero = tuple(cubic_equation(a, 0)[0] for a in product(range(9), repeat=n))
    quad = tuple(tuple(a[i]*a[j] % 3 for i in range(n) for j in range(i, n)) for a in product(range(3), repeat=n))
    return {"dimension": n, "full_feature_dimension": D, "quadratic_dimension": Q, "zero_label_grid_rows": 9**n,
        "zero_coefficient_rank": int(nmod_mat(zero, 3).rank()),
        "zero_base_coefficient_rank": int(nmod_mat([[r[i] for i in base_indices] for r in zero], 3).rank()),
        "zero_coefficient_sha256": digest(zero), "base_column_indices": base_indices,
        "quadratic_label_grid_rows": 3**n, "quadratic_rank": int(nmod_mat(quad, 3).rank()), "quadratic_sha256": digest(quad)}


def source_ledger(n, r, rows, alpha, valuations, radius, bits=128, coverage_failure=None):
    integer(n, "positive dimension", 1);integer(r, "positive root digits", 1);integer(rows, "positive original rows", 1)
    q, alpha = 3**r, _rational(alpha)
    if not 0 < alpha < 1: raise ValueError("positive subunit source width required")
    valuations = tuple(valuations)
    if not valuations or valuations != tuple(sorted(set(valuations))) or any(type(d) is not int or not 2 <= d < r for d in valuations):
        raise ValueError("complete distinct declared divided-cubic valuations required")
    terms = []
    for d in valuations:
        boxes = gaussian_alphabet_boxes(alpha*3**d, bits)
        rank = split_rank_ledger(n, rows, boxes["zero"]["lower"], 2*Fraction(boxes["each_signed_one"]["lower"]))
        tail = min(Fraction(1), rows*Fraction(boxes["outside_triplet"]["upper"]))
        terms.append({"valuation": d, "Gaussian_derived_error_law": boxes, "conditional_rank_ledger": rank,
            "whole_original_bank_outside_triplet_failure_upper": str(tail),
            "fixed_valuation_failure_upper": str(min(Fraction(1), tail+Fraction(rank["conditional_rank_failure_upper"]))),
            "conditioning_on_data_selected_multiple_truth": False})
    original = gaussian_radius_box(alpha*q, radius, bits)
    original_tail = min(Fraction(1), rows*Fraction(original["upper"]))
    separation = separation_ledger(q, n, rows, radius)
    union = min(Fraction(1), original_tail+Fraction(separation["global_code_separation_failure_upper_used"])+sum(Fraction(t["fixed_valuation_failure_upper"]) for t in terms))
    coverage = None if coverage_failure is None else _rational(coverage_failure)
    if coverage is not None and not 0 <= coverage <= 1: raise ValueError("valid external coverage failure required")
    return {"dimension": n, "root_digits": r, "original_rows": rows, "continuous_D_alpha_width": str(alpha),
        "original_Gaussian_radius_law": original, "original_radius_event_failure_upper": str(original_tail),
        "original_code_separation_ledger": separation, "valuation_terms": tuple(terms),
        "uniform_local_failure_upper": str(union), "external_true_usable_multiple_coverage_failure_upper": None if coverage is None else str(coverage),
        "recovery_failure_upper_IF_coverage_and_source_laws_hold": None if coverage is None else str(min(Fraction(1), union+coverage)),
        "external_coverage_is_for_known_coefficient_and_multiple_pairs": True,
        "unknown_coefficient_list_scan_implemented_in_this_module": False,
        "source_alpha_q_at_least_2_sqrt_n": (alpha*q)**2 >= 4*n,
        "source_law_or_multiple_producer_supplied": False,
        "all_valuations_union_before_external_data_selected_multiple": True,
        "unit_parts_at_same_valuation_create_independent_source_banks": False,
        "logical_matrix_entries_for_each_decoder": rows*(feature_width(n)+1),
        "full_declared_matrix_and_uncapped_multiple_coverage_required": True}


def control(n, r, d, pairs, coefficient_unit, seed):
    raw, mask, truth, _ = source_data(n, r, pairs, False, seed)
    q, g = 3**r, 3**d;Q = q//g;secret = tuple((s-m) % q for s, m in zip(truth, mask))
    # Bounded forward calibration, NOT samples from an unbounded Gaussian source.
    errors = tuple(Q*((j*7+seed) % 3-1)+((-1)**j)*(Q//5) for j in range(len(raw)))
    raw = tuple(NoisyLinearRecord(s.label, (sum(a*b for a, b in zip(s.label, secret))+e) % q, q, s.source_id) for s, e in zip(raw, errors))
    c = coefficient_unit*g;w = tuple(c*s % q for s in secret);R = max(abs(e) for e in errors)
    result = complete_alphabet_multiple(raw, c, w, R)
    return {"original_records": tuple(s.public() for s in raw), "signed_coefficient": c, "supplied_multiple": w,
        "truth_fixture_only": {"original_secret": secret, "original_errors": errors},
        "multiple_inputs_generated_from_truth_FOR_CALIBRATION_ONLY": True,
        "calibration_is_an_unbounded_Gaussian_source": False,
        "strict_zero_error_quotient_baseline": complete_multiple(raw, c, w),
        "alphabet_completion": result, "completion_matches_truth_fixture": result["candidate_secret"] == secret}


def build_report():
    profiles = []
    for n in (8, 32, 128):
        d = 2
        while 3**(d+1) <= n**3 and d+1 < n: d += 1
        for beta in (Fraction(1, 2), Fraction(1, 2*(math.isqrt((n-1).bit_length()-1)+1))):
            boxes = gaussian_alphabet_boxes(beta)
            prelim = split_rank_ledger(n, 2, boxes["zero"]["lower"], 2*Fraction(boxes["each_signed_one"]["lower"]))
            budgets = (prelim["zero_row_base_rank_budget"], prelim["nonzero_row_quadratic_rank_budget"])
            needed = max(t["power_block"]*(2*t["feature_block_dimension"]+66) for t in budgets)
            rows = 2*((needed+1)//2)
            profiles.append(source_ledger(n, n, rows, beta/3**d, (d,), (3**n)//n))
    dependencies = ("native_small_multiple_completion.py", "native_small_alphabet_decoder.py", "native_classical_modulus_descent.py",
                    "native_full_root_slice.py", "native_partial_coordinate_decoder.py", "ternary_covariant_noise.py", "ternary_noise_degradation.py", "ternary_measured_lattice_decoder.py")
    return {"status": "SOURCE_CORRECT_GAUSSIAN_QUOTIENT_COMPLETION_AND_SPLIT_RANK_REVIEW_PENDING",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
        "dependency_sha256": {f: hashlib.sha256((ROOT/"theorems"/f).read_bytes()).hexdigest() for f in dependencies},
        "actual_original_data_controls": [control(*p) for p in ((2, 6, 2, 60, -2, 102001), (4, 16, 4, 180, 2, 102002), (8, 64, 6, 600, -1, 102003))],
        "zero_quadratic_structural_grids": [structural_grid(n) for n in (1, 2, 3)], "conditional_Gaussian_source_profiles": profiles,
        "accepted_speedup_candidate": False, "new_active_negative_result_created": False,
        "Gaussian_LWE_solver_or_new_quantum_algorithm": False, "novelty_claim": False,
        "research_decision": "USE_SOURCE_CORRECT_COMPLETION_AND_SPLIT_RANK; MULTIPLE_OR_DECISION_PRODUCER_STILL_MISSING"}


def verify_probability_boxes(report):
    for profile in report["conditional_Gaussian_source_profiles"]:
        for term in profile["valuation_terms"]:
            box = term["Gaussian_derived_error_law"]
            if gaussian_alphabet_boxes(box["continuous_Gaussian_width"], box["enclosure_bits"]) != box:
                raise ValueError("Gaussian alphabet probability box replay failed")
        box = profile["original_Gaussian_radius_law"]
        radius = box["integer_error_radius"]
        if type(radius) is str:
            value = int(radius)
            if str(value) != radius or abs(value) <= 2**53-1: raise ValueError("noncanonical exact radius transport")
            radius = value
        if exact_json(gaussian_radius_box(box["continuous_Gaussian_width"], radius, box["enclosure_bits"])) != box:
            raise ValueError("original radius probability box replay failed")
    return {"verified": True, "Gaussian_profiles_replayed": len(report["conditional_Gaussian_source_profiles"]),
        "replay_uses_same_trusted_Arb_special_function_primitive": True, "independent_transcendental_proof_supplied": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__);parser.add_argument("--write", action="store_true");parser.add_argument("--check-probabilities", action="store_true")
    args = parser.parse_args()
    if args.check_probabilities:
        print(json.dumps(verify_probability_boxes(json.loads(REPORT.read_text())), indent=2));return
    report = build_report()
    if args.write: REPORT.write_text(json.dumps(exact_json(report), indent=2)+"\n")
    print(json.dumps({"status": report["status"], "original_data_controls_match": [c["completion_matches_truth_fixture"] for c in report["actual_original_data_controls"]],
        "Gaussian_local_failure_upper_diagnostics": [float(Fraction(p["uniform_local_failure_upper"])) for p in report["conditional_Gaussian_source_profiles"]],
        "multiple_producer_supplied": False}, indent=2))


if __name__ == "__main__": main()
