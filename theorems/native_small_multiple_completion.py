"""Conditional completion of actual secret multiples over ternary prime powers.

No decision solver or multiple-producing oracle is supplied. Local algebra,
original-record verification and source-wide event budgets stay separate.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path

from flint import nmod_mat

from native_affine_fibre_relaxation import canonical_vector, unit_minor_inverse, NonFreeRank
from native_classical_modulus_descent import digest, originals
from ternary_covariant_noise import root_digits
from ternary_measured_lattice_decoder import exact_json, integer

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/NATIVE_SMALL_MULTIPLE_COMPLETION.md"
REPORT = ROOT / "research/classical_baselines/native_small_multiple_completion.json"


def _records(records):
    pairs = originals(records)
    return tuple(s for p in pairs for s in (p.a, p.c))


def _rational(x):
    if type(x) not in (int, str, Fraction):
        raise ValueError("exact integer, rational string or Fraction required")
    return Fraction(x)


@dataclass(frozen=True)
class MultipleQuotient:
    modulus: int
    coefficient: int
    multiple: tuple
    factor: int
    valuation: int
    remaining_modulus: int
    unit_coefficient: int
    quotient_secret: tuple

    def record(self):
        return {"original_modulus": self.modulus, "signed_coefficient": self.coefficient,
            "multiple": self.multiple, "nonunit_factor": self.factor, "valuation": self.valuation,
            "remaining_modulus": self.remaining_modulus, "unit_coefficient": self.unit_coefficient,
            "known_quotient_IF_multiple_is_true": self.quotient_secret,
            "lost_secret_trits_per_coordinate": self.valuation,
            "multiple_membership_in_original_secret_orbit_established": False,
            "free_multiple_producer_or_decision_oracle_supplied": False}


def multiple_quotient(q, coefficient, multiple):
    root_digits(q)
    if type(coefficient) is not int or coefficient % q == 0:
        raise ValueError("nonzero modulo-q exact signed coefficient required")
    multiple = tuple(multiple)
    canonical_vector(multiple, len(multiple), q)
    if not multiple: raise ValueError("nonempty original-secret multiple vector required")
    a, g, d = coefficient % q, 1, 0
    while a % 3 == 0: a, g, d = a//3, 3*g, d+1
    if any(x % g for x in multiple): return None
    Q, u = q//g, (coefficient//g) % (q//g)
    inverse = pow(u, -1, Q)
    lower = tuple((x//g)*inverse % Q for x in multiple)
    if tuple(coefficient*x % q for x in lower) != multiple:
        raise ArithmeticError("unit-part extraction did not match the actual full-root multiple")
    return MultipleQuotient(q, coefficient, multiple, g, d, Q, u, lower)


class PublicBasisCache:
    """Only label matrices enter the cache; every inverse is replayed at its ring."""
    def __init__(self, records):
        records = _records(records)
        self.q, self.labels = records[0].modulus, tuple(s.label for s in records)
        self.n, self.models = len(self.labels[0]), {}
        field = nmod_mat([[a[i] % 3 for a in self.labels] for i in range(self.n)], 3)
        reduced, rank = field.rref()
        self.rank = int(rank)
        self.pivots = tuple(next(j for j in range(len(self.labels)) if reduced[i, j]) for i in range(self.rank))
        self.fingerprint = digest({"modulus": self.q, "labels": self.labels})

    def inverse(self, g):
        if self.rank != self.n: raise NonFreeRank("actual original row basis is rank deficient modulo3")
        if g not in self.models:
            S = tuple(tuple(x % g for x in self.labels[j]) for j in self.pivots)
            inverse, steps = unit_minor_inverse(S, g)
            self.models[g] = {"modulus": g, "label_only_basis_rows": self.pivots, "minor": S,
                "inverse": inverse, "inverse_lift_digits": steps, "public_label_sha256": self.fingerprint,
                "composite_field_inverse_used": False, "response_values_entered_basis_selection": False}
        return self.models[g]


def complete_multiple(records, coefficient, multiple, cache=None):
    records = _records(records);q, n = records[0].modulus, len(records[0].label)
    multiple = canonical_vector(multiple, n, q)
    quotient = multiple_quotient(q, coefficient, multiple)
    base = {"signed_coefficient": coefficient, "multiple": multiple, "candidate_secret": None,
        "original_response_residual_evaluations": 0, "multiple_truth_premise_verified": False,
        "rounded_consistency_is_an_original_secret_certificate": False}
    if quotient is None:
        return {**base, "status": "EXACT_NONUNIT_IMAGE_INCOMPATIBILITY"}
    base["quotient_model"] = quotient.record()
    if quotient.factor == 1:
        return {**base, "status": "UNIT_MULTIPLE_ALGEBRAIC_PREIMAGE_NOT_TRUTH_CERTIFICATE",
                "candidate_secret": quotient.quotient_secret, "rounding_transcript": ()}
    if cache is None: cache = PublicBasisCache(records)
    if cache.q != q or cache.labels != tuple(s.label for s in records):
        raise ValueError("basis cache must bind the same actual original public labels")
    try: model = cache.inverse(quotient.factor)
    except NonFreeRank:
        return {**base, "status": "ORIGINAL_LOW_LABEL_RANK_UNSUPPORTED_NOT_NO_SOLUTION"}
    Q, g, lower = quotient.remaining_modulus, quotient.factor, quotient.quotient_secret
    transcript = []
    for s in records:
        residual = (s.value-sum(a*b for a, b in zip(s.label, lower))) % q
        rounded = ((residual+Q//2)//Q) % g
        distance = min((residual-Q*rounded) % q, (Q*rounded-residual) % q)
        transcript.append({"source_id": s.source_id, "corrected_original_response": residual,
            "rounded_missing_quotient_equation": rounded, "distance_to_nearest_center": distance})
    rhs = tuple(transcript[j]["rounded_missing_quotient_equation"] for j in cache.pivots)
    h = tuple(sum(a*b for a, b in zip(row, rhs)) % g for row in model["inverse"])
    consistent = all(sum(a*b for a, b in zip(s.label, h)) % g == t["rounded_missing_quotient_equation"] for s, t in zip(records, transcript))
    candidate = tuple(a+Q*b for a, b in zip(lower, h)) if consistent else None
    if candidate is not None and tuple(coefficient*x % q for x in candidate) != multiple:
        raise ArithmeticError("completed candidate escaped the given multiple")
    return {**base, "status": "CONDITIONAL_ORIGINAL_BANK_MULTIPLE_COMPLETION" if consistent else "INCONSISTENT_ROUNDED_MISSING_QUOTIENT",
        "candidate_secret": candidate, "missing_quotient_solution": h if consistent else None,
        "public_basis_model": model, "rounding_transcript": tuple(transcript),
        "original_response_residual_evaluations": len(records)}


def bounded_fit(records, candidate, radius):
    records = _records(records);q, n = records[0].modulus, len(records[0].label)
    integer(radius, "public bounded-error radius")
    if 4*radius >= q: raise ValueError("verification radius must satisfy4R<q")
    candidate = canonical_vector(candidate, n, q)
    distances = []
    for s in records:
        e = (s.value-sum(a*b for a, b in zip(s.label, candidate))) % q
        distances.append(min(e, q-e))
    return {"fits_public_radius": max(distances) <= radius, "radius": radius,
        "original_circular_error_distances": tuple(distances), "original_records_checked": len(records),
        "bounded_fit_alone_certifies_truth": False}


def scan_list(records, multiples, coefficient_bound, radius, max_trials=10000):
    records = _records(records);q, n = records[0].modulus, len(records[0].label)
    multiples = tuple(canonical_vector(w, n, q) for w in multiples)
    integer(coefficient_bound, "positive declared coefficient bound", 1);integer(max_trials, "positive complete scan budget", 1)
    integer(radius, "public verification radius")
    if not multiples or 4*radius >= q: raise ValueError("nonempty supplied list and radius4R<q required")
    C = min(coefficient_bound, q//2)
    trials = len(multiples)*2*C
    scope = {"declared_coefficient_bound": coefficient_bound, "effective_centered_coefficient_bound": C,
        "supplied_multiples": multiples, "public_verification_radius": radius,
        "planned_coefficient_trials": trials, "original_records_paid_once": len(records),
        "public_matrix_preprocessing_is_free": False,
        "public_matrix_preprocessing_arithmetic_order": "O(n^2*m) field RREF once; O(n^3*log(d+1)) modular arithmetic per cached3^d inverse",
        "list_coverage_or_decision_solver_supplied": False, "new_independent_original_samples_created": False,
        "unconditional_secret_recovery_claim": False}
    if trials > max_trials:
        return {**scope, "status": "COMPLETE_SCAN_CAP_EXCEEDED_NOT_NO_CANDIDATES", "trials_evaluated": 0,
            "bounded_fit_candidates": (), "trial_records": (), "public_basis_inversions": (),
            "public_basis_rref_calls": 0, "public_basis_inversion_calls": 0,
            "original_response_residual_evaluations": 0, "original_candidate_verification_evaluations": 0}
    cache = PublicBasisCache(records);attempts, fits = [], {}
    for w in multiples:
        for c in tuple(range(-C, 0))+tuple(range(1, C+1)):
            result = complete_multiple(records, c, w, cache)
            candidate = result["candidate_secret"]
            if candidate is not None and candidate not in fits:
                fits[candidate] = bounded_fit(records, candidate, radius)
            attempts.append(result)
    survivors = tuple({"candidate_secret": s, "fit": fit} for s, fit in sorted(fits.items()) if fit["fits_public_radius"])
    status = "ONE_BOUNDED_FIT_CANDIDATE_SOURCE_CERTIFICATION_REQUIRED" if len(survivors) == 1 else (
        "AMBIGUOUS_BOUNDED_FIT_CANDIDATES" if survivors else "NO_BOUNDED_FIT_CANDIDATE_NOT_NO_SECRET")
    return {**scope, "status": status, "trials_evaluated": len(attempts), "trial_records": tuple(attempts),
        "bounded_fit_candidates": survivors, "public_basis_inversions": tuple(cache.models[g] for g in sorted(cache.models)),
        "public_basis_rref_calls": 1, "public_basis_inversion_calls": len(cache.models),
        "original_response_residual_evaluations": sum(a["original_response_residual_evaluations"] for a in attempts),
        "original_candidate_verification_evaluations": len(records)*len(fits)}


def separation_ledger(q, n, m, radius, block=16):
    """A public code-distance union event covers EVERY adaptive candidate."""
    r = root_digits(q);integer(n, "positive source dimension", 1);integer(m, "positive original rows", 1)
    integer(radius, "public verifier radius");integer(block, "positive exact power certificate block", 1)
    if 4*radius >= q: raise ValueError("verification radius4R<q required")
    rows, exact = [], Fraction(0)
    short = r*m <= 2048
    for d in range(r):
        g, L = 3**d, 3**(r-d)
        numerator = 2*((2*radius)//g)+1
        D, N = L**block, numerator**block
        k = (D//N).bit_length()-1
        population_exponent = (r-d)*n
        bits = (3**population_exponent-1).bit_length()
        e = bits-k*(m//block)
        rows.append({"difference_valuation": d, "subgroup_order": L, "small_ball_numerator": numerator,
            "small_ball_denominator": L, "difference_population_base3_exponent": population_exponent,
            "population_upper_ceil_log2": bits, "exact_probability_power_block": block,
            "power_negative_log2_floor": k, "complete_power_blocks": m//block, "term_upper_power2_exponent": e})
        if short: exact += (3**population_exponent-3**((r-d-1)*n))*Fraction(numerator, L)**m
    exponent = max(row["term_upper_power2_exponent"] for row in rows)+(r-1).bit_length()
    budget = Fraction(1, 2**min(64, max(0, -exponent)))
    if short: budget = min(budget, exact, Fraction(1))
    return {"original_modulus": q, "dimension": n, "original_rows": m, "verification_radius": radius,
        "valuation_small_ball_certificates": tuple(rows), "dyadic_union_upper_exponent": exponent,
        "exact_union_upper_if_short": str(min(Fraction(1), exact)) if short else None,
        "global_code_separation_failure_upper_used": str(budget),
        "IID_uniform_original_label_rows_required": True,
        "separation_event_covers_all_secrets_and_adaptive_candidates": True,
        "candidate_count_union_multiplier_required": False, "fixed_instance_distance_certified": False}


def source_event_ledger(q, n, m, radius, max_valuation, moment, coverage_failure=None):
    r = root_digits(q);integer(max_valuation, "nonnegative maximum supported multiple valuation")
    if max_valuation >= r: raise ValueError("nonzero supported multiple required")
    V = _rational(moment)
    if V < 0: raise ValueError("true nonnegative original error moment upper required")
    separation = separation_ledger(q, n, m, radius)
    spacing = q//3**max_valuation
    T = min(radius, spacing//2)
    errors = min(Fraction(1), m*V/(T+1)**2)
    local = min(Fraction(1), errors+Fraction(separation["global_code_separation_failure_upper_used"]))
    total = None
    if coverage_failure is not None:
        coverage_failure = _rational(coverage_failure)
        if not 0 <= coverage_failure <= 1: raise ValueError("valid external list-coverage failure upper required")
        total = min(Fraction(1), local+coverage_failure)
    return {"original_modulus": q, "dimension": n, "original_rows": m, "public_radius": radius,
        "maximum_supported_valuation": max_valuation, "minimum_original_center_spacing": spacing,
        "uniform_good_original_error_threshold": T, "true_original_second_moment_upper": str(V),
        "original_error_event_failure_upper": str(errors), "code_separation_ledger": separation,
        "uniform_local_event_failure_upper": str(local),
        "external_covered_usable_multiple_list_failure_upper": None if coverage_failure is None else str(coverage_failure),
        "composed_recovery_failure_upper_IF_external_coverage_is_proved": None if total is None else str(total),
        "complete_declared_coefficient_scan_without_caps_is_required": True,
        "conditioning_on_data_selected_multiple_truth_used": False,
        "original_errors_assumed_independent": False,
        "arbitrary_correlations_between_coverage_noise_and_labels_allowed_by_union": True,
        "source_promises_or_published_reduction_applicability_established": False,
        "decision_algorithm_supplied": False}


def coefficient_size_gap(q, n, m, radius, moment, bound):
    integer(bound, "positive declared coefficient bound", 1)
    effective = min(bound, q//2);g, d = 1, 0
    while 3*g <= effective: g, d = 3*g, d+1
    return {"coefficient_size_bound": bound, "largest_allowed_ternary_factor": g,
        "worst_allowed_valuation": d,
        "worst_factor_local_source_event": source_event_ledger(q, n, m, radius, d, moment),
        "small_integer_coefficient_bound_guarantees_a_safe_valuation": False,
        "bound_is_derived_from_an_implemented_decision_reduction": False}


def code_census(q, m, radius):
    root_digits(q);integer(m, "positive original-label census row count", 1)
    integer(radius, "public original-code radius")
    if 4*radius >= q: raise ValueError("census radius4R<q required")
    if q**m > 10000: raise ValueError("complete original-label census cap exceeded")
    collisions = 0
    for labels in product(range(q), repeat=m):
        if any(all(min(a*h % q, (-a*h) % q) <= 2*radius for a in labels) for h in range(1, q)):
            collisions += 1
    return {"modulus": q, "dimension": 1, "original_rows": m, "radius": radius,
        "original_label_banks_checked": q**m, "banks_with_nonzero_close_codeword": collisions,
        "exact_separation_failure_probability": str(Fraction(collisions, q**m)),
        "ledger": separation_ledger(q, 1, m, radius)}


def control(n, r, M, noisy, seed, coefficients):
    from native_full_root_slice import source_data
    raw, mask, truth, errors = source_data(n, r, M, noisy, seed)
    q = 3**r;secret = tuple((a-b) % q for a, b in zip(truth, mask))
    attempts = []
    for c in coefficients:
        w = tuple(c*s % q for s in secret)
        result = complete_multiple(raw, c, w)
        attempts.append({"supplied_multiple": w, "signed_coefficient": c, "completion": result,
                         "matches_truth_fixture": result["candidate_secret"] == secret})
    scan = scan_list(raw, (tuple(3*s % q for s in secret), (0,)*n), 3, max(1, q//32))
    return {"original_records": tuple(s.public() for s in raw),
        "truth_fixture_only": {"original_secret": secret, "original_errors": errors},
        "multiple_inputs_prepared_from_truth_FOR_CALIBRATION_ONLY": True,
        "known_coefficient_completions": tuple(attempts), "unknown_coefficient_list_scan": scan,
        "secret_or_errors_entered_completion": False}


def build_report():
    deps = ("native_affine_fibre_relaxation.py", "native_classical_modulus_descent.py",
            "native_full_root_slice.py", "ternary_covariant_noise.py", "ternary_measured_lattice_decoder.py")
    grids = []
    for n in (8, 32, 64, 128):
        q, m, R = 3**n, 2*(n+1)**3, (3**n)//n
        V = Fraction(q*q, 3*n**6)+Fraction(1, 2)
        d = 0
        while 3**(d+1) <= n: d += 1
        grids.append({"dimension": n, "usable_valuation_budget": d,
            "safe_valuation_source_ledger": source_event_ledger(q, n, m, R, d, V),
            "declared_size_only_gap": coefficient_size_gap(q, n, m, R, V, n**9)})
    return {"status": "ORIGINAL_BANK_SMALL_MULTIPLE_COMPLETION_AND_UNIFORM_VERIFICATION_REVIEW_PENDING",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
        "dependency_sha256": {f: hashlib.sha256((ROOT/"theorems"/f).read_bytes()).hexdigest() for f in deps},
        "original_data_controls": [control(*args) for args in ((2, 3, 12, False, 96001, (1, -2, 3, -3, 9)),
            (2, 6, 20, True, 96002, (1, -2, 3, 9)), (3, 64, 16, True, 96003, (3, 9, -27)))],
        "complete_original_code_censuses": [code_census(9, 4, R) for R in (0, 1)],
        "scaling_source_events_and_size_gaps": grids,
        "accepted_speedup_candidate": False, "new_active_negative_result_created": False,
        "research_decision": "REQUIRE_USABLE_VALUATION_COVERAGE_OR_PRIMITIVE_CHARACTER_MECHANISM_NOT_JUST_SMALL_MULTIPLES",
        "remaining_obligations": ["external algebra and source-event review", "actual classical/quantum decision mechanism",
            "usable coefficient-valuation coverage", "actual error-law compatibility with published reductions",
            "production registry/CLI integration"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__);parser.add_argument("--write", action="store_true")
    args = parser.parse_args();report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2)+"\n")
    print(json.dumps({"status": report["status"], "original_data_controls": len(report["original_data_controls"]),
        "known_multiple_calibrations": sum(len(c["known_coefficient_completions"]) for c in report["original_data_controls"]),
        "calibrations_matching_truth": sum(a["matches_truth_fixture"] for c in report["original_data_controls"] for a in c["known_coefficient_completions"]),
        "list_scan_statuses": [c["unknown_coefficient_list_scan"]["status"] for c in report["original_data_controls"]],
        "decision_algorithm_supplied": False}, indent=2))


if __name__ == "__main__": main()
