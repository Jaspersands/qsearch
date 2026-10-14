"""Certified secret-coordinate recovery from possibly rank-deficient F3 features.

No free coordinates are guessed. Actual nonlinear substitution and full-root
original-value verification are mandatory. Source promises remain conditional.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path

from flint import nmod_mat

import native_small_alphabet_decoder as C
from native_small_multiple_completion import _records
from native_classical_modulus_descent import digest
from native_full_root_slice import source_data
from ternary_measured_lattice_decoder import integer, exact_json
from ternary_covariant_noise import root_digits
from ternary_noise_degradation import NoisyLinearRecord

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/NATIVE_PARTIAL_COORDINATE_DECODER.md"
REPORT = ROOT / "research/classical_baselines/native_partial_coordinate_decoder.json"


def affine_coordinates(rows, rhs, dimension, coordinates, max_entries=2000000):
    integer(dimension, "positive affine feature dimension", 1);integer(max_entries, "positive full-matrix cap", 1)
    rows, rhs, coordinates = tuple(tuple(r) for r in rows), tuple(rhs), tuple(coordinates)
    if not rows or not coordinates or len(rhs) != len(rows) or len(set(coordinates)) != len(coordinates):
        raise ValueError("whole nonempty affine system and distinct requested coordinates required")
    if any(type(j) is not int or not 0 <= j < dimension for j in coordinates): raise ValueError("canonical coordinate indices required")
    if len(rows)*(dimension+1) > max_entries: raise ValueError("whole affine matrix cap exceeded")
    if any(len(r) != dimension or any(type(a) is not int or a not in (0, 1, 2) for a in r) for r in rows) or any(type(b) is not int or b not in (0, 1, 2) for b in rhs):
        raise ValueError("canonical exact F3 rows and right-hand side required")
    reduced, augmented_rank = nmod_mat([list(r)+[b] for r, b in zip(rows, rhs)], 3).rref()
    reduced = tuple(tuple(int(reduced[i, j]) for j in range(dimension+1)) for i in range(int(augmented_rank)))
    inconsistent = any(not any(r[:dimension]) and r[dimension] for r in reduced)
    pivots = tuple(next(j for j, a in enumerate(row[:dimension]) if a) for row in reduced if any(row[:dimension]))
    free = tuple(j for j in range(dimension) if j not in pivots)
    certs = []
    for j in coordinates:
        pivot = pivots.index(j) if j in pivots else None
        dependence = tuple((k, reduced[pivot][k]) for k in free if reduced[pivot][k]) if pivot is not None else ()
        fixed = not inconsistent and pivot is not None and not dependence
        certs.append({"column": j, "pivot_row": pivot, "free_variable_dependence": dependence,
            "fixed": fixed, "value": reduced[pivot][dimension] if fixed else None})
    return {"feature_dimension": dimension, "equations": len(rows), "augmented_rank": int(augmented_rank),
        "coefficient_rank": len(pivots), "inconsistent": inconsistent,
        "pivot_columns": pivots, "free_columns": free, "reduced_nonzero_rows": reduced,
        "coordinate_certificates": tuple(certs), "all_requested_coordinates_fixed": all(c["fixed"] for c in certs),
        "input_system_sha256": digest({"rows": rows, "rhs": rhs}), "free_variables_assigned": False}


def decode(records, method="cubic", max_matrix_entries=2000000):
    records = _records(records);q, n, m = records[0].modulus, len(records[0].label), len(records)
    D = C.feature_width(n, method)
    if method == "cubic" and root_digits(q) < 2: raise ValueError("divided-cubic source requires modulus at least9")
    integer(max_matrix_entries, "positive whole-matrix preflight cap", 1)
    entries = m*(D+1)
    base = {"algorithm": "CERTIFIED_AFFINE_SECRET_COORDINATES_AND_CANONICAL_SUBSTITUTION",
        "original_modulus": q, "dimension": n, "method": method, "original_records_paid_once": m,
        "feature_dimension": D, "logical_augmented_matrix_entries": entries,
        "max_matrix_entries": max_matrix_entries, "matrix_cap_includes_Python_and_FLINT_overhead": False,
        "candidate_secret": None, "fixed_instance_alphabet_uniqueness_certified": False,
        "actual_planted_secret_or_noise_law_certified": False, "full_feature_rank_required": False,
        "free_feature_coordinates_guessed": False, "truth_or_error_input_used": False,
        "required_original_error_alphabet": (-1, 0, 1) if method == "cubic" else (-1, 1),
        "classical_secret_hypotheses_enumerated": 0, "new_quantum_algorithm_or_general_Gaussian_solver": False,
        "field_elimination_calls": 0, "coefficient_rank": None,
        "polynomial_work_order": "O(m*D^2 + m*n^2 + n^3*log(r+1)) on O(log(q))-bit original operands",
        "certificate_storage_order": "O(D^2+n^2); whole solve storage O(m*D)"}
    if entries > max_matrix_entries:
        return {**base, "status": "WHOLE_FEATURE_MATRIX_CAP_EXCEEDED_NOT_NO_SOLUTION", "compiled_rows": 0}
    rows, rhs = C.compile_equations(records, method)
    columns = tuple(range(n)) if method == "cubic" else tuple(range(D-n, D))
    low = affine_coordinates(rows, rhs, D, columns, max_matrix_entries)
    base.update({"compiled_rows": m, "field_elimination_calls": 1, "coefficient_rank": low["coefficient_rank"],
        "original_records_sha256": digest(tuple(r.public() for r in records)),
        "compiled_system_sha256": digest({"basis": C.feature_layout(n, method), "rows": rows, "rhs": rhs}),
        "low_coordinate_model": low})
    if low["inconsistent"]: return {**base, "status": "INCONSISTENT_SMALL_ALPHABET_EQUATIONS"}
    if not low["all_requested_coordinates_fixed"]:
        return {**base, "status": "SECRET_COORDINATES_NOT_LINEARLY_UNIQUE_NOT_NO_SECRET"}
    u = tuple(c["value"] for c in low["coordinate_certificates"])
    base["low_trit_coordinates"] = u
    if method == "cubic":
        initial = C.features(u, (0,)*n)
        next_rows = tuple(row[-n:] for row in rows)
        next_rhs = tuple((b-sum(a*f for a, f in zip(row, initial))) % 3 for row, b in zip(rows, rhs))
        higher = affine_coordinates(next_rows, next_rhs, n, tuple(range(n)), max_matrix_entries)
        base.update({"field_elimination_calls": 2, "next_coordinate_model": higher})
        if higher["inconsistent"]: return {**base, "status": "INCONSISTENT_CANONICAL_FEATURE_SUBSTITUTION"}
        if not higher["all_requested_coordinates_fixed"]:
            return {**base, "status": "NEXT_SECRET_COORDINATES_NOT_LINEARLY_UNIQUE_NOT_NO_SECRET"}
        v = tuple(c["value"] for c in higher["coordinate_certificates"])
        lower, prefix, physical = tuple(a+3*b for a, b in zip(u, v)), 9, C.features(u, v)
    else:
        lower, prefix, physical = u, 3, C.features(u, method=method)
    if any((sum(a*f for a, f in zip(row, physical))-b) % 3 for row, b in zip(rows, rhs)):
        return {**base, "status": "CANONICAL_FEATURES_FAIL_COMPILED_EQUATIONS"}
    base.update({"canonical_feature_vector": physical, "nonlinear_features_verified": True,
        "low_secret": lower, "prefix_modulus": prefix})
    candidate, lift = C.high_root_lift(records, lower, prefix);base["full_root_lift"] = lift
    if candidate is None: return {**base, "status": "INCONSISTENT_OR_UNSUPPORTED_ORIGINAL_HIGHER_ROOT_LIFT"}
    residuals = tuple(((r.value-sum(a*s for a, s in zip(r.label, candidate))+q//2) % q)-q//2 for r in records)
    base["original_candidate_residuals"] = residuals
    if any(e not in base["required_original_error_alphabet"] for e in residuals):
        return {**base, "status": "FULL_ROOT_ALPHABET_FIT_FAILED"}
    return {**base, "status": "UNIQUE_ALPHABET_COMPATIBLE_FULL_ROOT_SECRET_FROM_FIXED_COORDINATES",
        "candidate_secret": candidate, "fixed_instance_alphabet_uniqueness_certified": True,
        "planted_secret_recovery_requires_true_alphabet_promise": True}


def base_only_source_ledger(n, r, rows, alpha, valuations, radius, bits=128):
    import native_gaussian_quotient_completion as G
    reference = G.source_ledger(n, r, rows, alpha, valuations, radius, bits)
    terms = []
    for t in reference["valuation_terms"]:
        base = t["conditional_rank_ledger"]["zero_row_base_rank_budget"]
        failure = min(Fraction(1), Fraction(t["whole_original_bank_outside_triplet_failure_upper"])+Fraction(base["rank_failure_upper"]))
        terms.append({"valuation": t["valuation"], "Gaussian_derived_error_law": t["Gaussian_derived_error_law"],
            "zero_error_base_coordinate_budget": base,
            "whole_bank_outside_triplet_failure_upper": t["whole_original_bank_outside_triplet_failure_upper"],
            "fixed_valuation_secret_recovery_failure_upper": str(failure),
            "nonzero_noise_probability_floor_required": False,
            "secret_translation_is_only_a_proof_operation": True})
    union = min(Fraction(1), Fraction(reference["original_radius_event_failure_upper"])+Fraction(reference["original_code_separation_ledger"]["global_code_separation_failure_upper_used"])+
                sum(Fraction(t["fixed_valuation_secret_recovery_failure_upper"]) for t in terms))
    return {"full_feature_reference_same_source": reference, "secret_coordinate_valuation_terms": tuple(terms),
        "uniform_local_secret_recovery_failure_upper": str(union),
        "actual_source_or_multiple_producer_supplied": False,
        "recovery_with_missing_external_coverage_claimed": False,
        "all_original_radius_separation_truncation_and_valuation_events_retained": True,
        "default_matrix_cap_feasible": rows*(C.feature_width(n)+1) <= 2000000}


def control(n, r, pairs, nonzero_errors, seed, method="cubic"):
    raw, mask, truth, errors = source_data(n, r, pairs, method == "quadratic", seed)
    q = 3**r;secret = tuple((x-y) % q for x, y in zip(truth, mask))
    if method == "cubic":
        errors = tuple(int(j < nonzero_errors) for j in range(len(raw)))
        raw = tuple(NoisyLinearRecord(s.label, (s.value+e) % q, q, s.source_id) for s, e in zip(raw, errors))
    result = decode(raw, method)
    return {"original_records": tuple(r.public() for r in raw), "truth_fixture_only": {"original_secret": secret, "original_errors": errors},
        "partial_decoder": result, "full_feature_reference": C.decode(raw, method),
        "matches_truth_fixture": result["candidate_secret"] == secret,
        "calibration_is_unbounded_Gaussian_source": False}


def falsifiers():
    output = []
    for case in C.falsifiers():
        raw = tuple(NoisyLinearRecord(**r) for r in case["original_records"])
        result = decode(raw, max_matrix_entries=case["max_matrix_entries"])
        output.append({"kind": case["kind"], "original_records": case["original_records"],
            "truth_fixture_only": case["truth_fixture_only"], "partial_decoder": result,
            "matches_planted_truth": result["candidate_secret"] == case["truth_fixture_only"]["original_secret"],
            "false_source_promise_repaired_by_truth": False})
    return tuple(output)


def build_report():
    import native_gaussian_quotient_completion as G
    controls = [control(*p) for p in ((4, 16, 90, 1, 103001), (8, 64, 220, 1, 103002),
                                    (2, 4, 30, 0, 103003), (4, 16, 60, 0, 103004, "quadratic"))]
    profiles = []
    for n in (8, 32, 128):
        d = 2
        while 3**(d+1) <= n**3 and d+1 < n: d += 1
        beta = Fraction(1, 2*(math.isqrt((n-1).bit_length()-1)+1))
        boxes = G.gaussian_alphabet_boxes(beta)
        prelim = G.split_rank_ledger(n, 2, boxes["zero"]["lower"], 2*Fraction(boxes["each_signed_one"]["lower"]))
        b = prelim["zero_row_base_rank_budget"]
        required = b["power_block"]*(2*b["feature_block_dimension"]+66)
        rows = 2*((required+1)//2)
        old_required = max(t["power_block"]*(2*t["feature_block_dimension"]+66) for t in
            (prelim["zero_row_base_rank_budget"], prelim["nonzero_row_quadratic_rank_budget"]))
        p = base_only_source_ledger(n, n, rows, beta/3**d, (d,), (3**n)//n)
        p["full_feature_rank_sufficient_original_rows_reference"] = 2*((old_required+1)//2)
        profiles.append(p)
    deps = ("native_small_alphabet_decoder.py", "native_small_multiple_completion.py", "native_classical_modulus_descent.py",
            "native_full_root_slice.py", "native_gaussian_quotient_completion.py", "ternary_covariant_noise.py",
            "ternary_measured_lattice_decoder.py", "ternary_noise_degradation.py")
    return {"status": "CERTIFIED_PARTIAL_SECRET_COORDINATES_AND_BASE_ONLY_GAUSSIAN_COMPLETION_REVIEW_PENDING",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
        "dependency_sha256": {f: hashlib.sha256((ROOT/"theorems"/f).read_bytes()).hexdigest() for f in deps},
        "actual_original_data_controls": controls, "base_only_Gaussian_source_profiles": profiles,
        "falsifier_controls": falsifiers(),
        "accepted_speedup_candidate": False, "new_active_negative_result_created": False,
        "Gaussian_LWE_solver_or_new_quantum_algorithm": False, "novelty_claim": False,
        "research_decision": "REQUIRE_SECRET_COORDINATE_UNIQUENESS_NOT_FULL_AUXILIARY_FEATURE_RANK"}


def main():
    parser = argparse.ArgumentParser(description=__doc__);parser.add_argument("--write", action="store_true");parser.add_argument("--check-probabilities", action="store_true")
    args = parser.parse_args()
    if args.check_probabilities:
        import native_gaussian_quotient_completion as G
        p = json.loads(REPORT.read_text())
        print(json.dumps(G.verify_probability_boxes({"conditional_Gaussian_source_profiles": [s["full_feature_reference_same_source"] for s in p["base_only_Gaussian_source_profiles"]]}), indent=2));return
    p = build_report()
    if args.write: REPORT.write_text(json.dumps(exact_json(p), indent=2)+"\n")
    print(json.dumps({"status": p["status"], "controls": [{"rank": c["partial_decoder"]["coefficient_rank"], "features": c["partial_decoder"]["feature_dimension"],
        "matches_truth": c["matches_truth_fixture"]} for c in p["actual_original_data_controls"]],
        "base_only_original_rows": [x["full_feature_reference_same_source"]["original_rows"] for x in p["base_only_Gaussian_source_profiles"]]}, indent=2))


if __name__ == "__main__": main()
