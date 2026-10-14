"""Disjoint original-basis completion, full-radius verification and source events.

External multiples and IID source laws are not supplied or certified. A fitted
candidate is not a planted-secret certificate. No cubic features are compiled.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path

from flint import nmod_mat

from native_affine_fibre_relaxation import canonical_vector, unit_minor_inverse
from native_small_multiple_completion import _rational, multiple_quotient, separation_ledger
from native_classical_modulus_descent import digest
from native_gaussian_quotient_completion import nearest_odd_division, gaussian_alphabet_boxes, gaussian_radius_box
from native_full_root_slice import source_data
from ternary_covariant_noise import root_digits
from ternary_noise_degradation import NoisyLinearRecord
from ternary_measured_lattice_decoder import integer, exact_json

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/NATIVE_BASIS_LOTTERY.md"
REPORT = ROOT / "research/classical_baselines/native_basis_lottery.json"
MAX_BLOCKS, MAX_MINOR_ENTRIES = 10000, 65536


def original_bank(records):
    """Classical linear observations need not come in quantum-qutrit pairs."""
    records = tuple(records)
    if not records or any(not isinstance(r, NoisyLinearRecord) for r in records):
        raise ValueError("nonempty typed original classical records required")
    q, n = records[0].modulus, len(records[0].label)
    if any(r.modulus != q or len(r.label) != n for r in records) or len({r.source_id for r in records}) != len(records):
        raise ValueError("consistent original shape and distinct original IDs required")
    return records


def original_fit(records, candidate, radius):
    records = original_bank(records);q, n = records[0].modulus, len(records[0].label)
    integer(radius, "public original radius")
    if 4*radius >= q: raise ValueError("original radius requires4R<q")
    candidate = canonical_vector(candidate, n, q)
    distances = tuple(min(e, q-e) for r in records for e in ((r.value-sum(a*x for a, x in zip(r.label, candidate))) % q,))
    return {"radius": radius, "original_circular_error_distances": distances,
        "original_records_checked": len(records), "fits_public_radius": max(distances) <= radius,
        "fit_certifies_planted_truth_or_source_law": False}


class BasisBank:
    """Fixed disjoint blocks; only labels enter rank and inverse preprocessing."""
    def __init__(self, records, max_blocks=MAX_BLOCKS, max_minor_entries=MAX_MINOR_ENTRIES):
        self.records = original_bank(records);self.q, self.n = self.records[0].modulus, len(self.records[0].label)
        integer(max_blocks, "positive complete block cap", 1);integer(max_minor_entries, "positive minor matrix cap", 1)
        self.planned = len(self.records)//self.n
        self.cap_exceeded = self.planned > max_blocks or self.n*self.n > max_minor_entries
        self.label_sha256 = digest({"modulus": self.q, "labels": tuple(r.label for r in self.records),
            "source_ids": tuple(r.source_id for r in self.records)})
        self.ranks, self.inverses = {}, {}
        self.rank_calls, self.inverse_calls = 0, 0

    def block(self, index):
        integer(index, "nonnegative original block index")
        if index >= self.planned: raise ValueError("whole declared original block required")
        return self.records[index*self.n:(index+1)*self.n]

    def rank(self, index):
        self.block(index)
        if index not in self.ranks:
            self.ranks[index] = int(nmod_mat([[a % 3 for a in r.label] for r in self.block(index)], 3).rank())
            self.rank_calls += 1
        return self.ranks[index]

    def inverse(self, index, g):
        self.block(index);root_digits(g)
        key = (index, g)
        if key not in self.inverses:
            S = tuple(tuple(a % g for a in r.label) for r in self.block(index))
            X, steps = unit_minor_inverse(S, g)
            self.inverses[key] = {"modulus": g, "minor": S, "inverse": X, "inverse_lift_digits": steps,
                "response_values_entered_basis_selection": False, "composite_field_inverse_used": False}
            self.inverse_calls += 1
        return self.inverses[key]


def complete(records, coefficient, multiple, radius, max_blocks=MAX_BLOCKS, max_minor_entries=MAX_MINOR_ENTRIES, bank=None):
    records = original_bank(records);q, n = records[0].modulus, len(records[0].label)
    integer(radius, "public original verification radius")
    integer(max_blocks, "positive complete block cap", 1);integer(max_minor_entries, "positive minor matrix cap", 1)
    if 4*radius >= q: raise ValueError("original radius requires4R<q")
    multiple = canonical_vector(multiple, n, q);model = multiple_quotient(q, coefficient, multiple)
    result = {"signed_coefficient": coefficient, "supplied_multiple": multiple,
        "candidate_secret": None, "original_records_paid_once": len(records), "verification_radius": radius,
        "original_records_sha256": digest(tuple(r.public() for r in records)),
        "trial_records": (), "blocks_attempted": 0, "original_candidate_verification_evaluations": 0,
        "original_response_rounding_evaluations": 0,
        "cubic_features_compiled": 0, "new_independent_original_samples_created": False,
        "actual_planted_secret_or_noise_law_certified": False,
        "fixed_instance_radius_uniqueness_certified": False, "multiple_producer_supplied": False,
        "max_blocks": max_blocks, "max_minor_entries": max_minor_entries,
        "minor_cap_includes_inverse_certificate_or_interpreter_overhead": False,
        "paired_original_records_required": False, "schedule_orbits_are_new_IID_samples": False}
    if model is None: return {**result, "status": "EXACT_NONUNIT_IMAGE_INCOMPATIBILITY"}
    result["quotient_model"] = model.record()
    if model.factor == 1:
        fit = original_fit(records, model.quotient_secret, radius)
        return {**result, "status": "UNIT_PREIMAGE_ORIGINAL_RADIUS_FIT_NOT_TRUTH" if fit["fits_public_radius"] else "UNIT_PREIMAGE_ORIGINAL_RADIUS_FIT_FAILED",
            "candidate_secret": model.quotient_secret if fit["fits_public_radius"] else None,
            "unit_fit": fit, "original_candidate_verification_evaluations": len(records),
            "complete_schedule_or_original_fit_found": True}
    if bank is None: bank = BasisBank(records, max_blocks, max_minor_entries)
    if bank.records != records: raise ValueError("basis cache must bind the same original bank")
    result.update({"planned_disjoint_blocks": bank.planned, "block_width": n,
        "unused_tail_original_IDs": tuple(r.source_id for r in records[bank.planned*n:]),
        "public_label_bank_sha256": bank.label_sha256,
        "public_rank_or_inverse_preprocessing_free": False,
        "arithmetic_order": "O(T*n^3*log(d+1)+T*m*n) on O(log(q))-bit operands; cached label-only bases",
        "certificate_storage_order": "O(m*n+attempted_blocks*n^2)"})
    if bank.cap_exceeded or bank.planned > max_blocks or n*n > max_minor_entries:
        return {**result, "status": "COMPLETE_BLOCK_SCHEDULE_CAP_EXCEEDED_NOT_NO_SECRET",
            "complete_schedule_or_original_fit_found": False}
    if not bank.planned:
        return {**result, "status": "INSUFFICIENT_ORIGINAL_ROWS_NOT_NO_SECRET", "complete_schedule_or_original_fit_found": True}
    trials = []
    for index in range(bank.planned):
        block = bank.block(index);rank = bank.rank(index)
        trial = {"block_index": index, "original_indices": tuple(range(index*n, (index+1)*n)),
            "original_source_IDs": tuple(r.source_id for r in block), "label_rank_mod3": rank}
        if rank < n:
            trials.append({**trial, "status": "SINGULAR_UNIT_MINOR_NOT_NO_SECRET"});continue
        basis = bank.inverse(index, model.factor);receipts = []
        for row in block:
            residual = (row.value-sum(a*x for a, x in zip(row.label, model.quotient_secret))) % q
            rhs = nearest_odd_division(residual, model.remaining_modulus) % model.factor
            receipts.append({"source_id": row.source_id, "parent_record_sha256": digest(row.public()),
                "corrected_original_response": residual, "rounded_missing_quotient_equation": rhs})
        h = tuple(sum(a*r["rounded_missing_quotient_equation"] for a, r in zip(row, receipts)) % model.factor for row in basis["inverse"])
        candidate = tuple(x+model.remaining_modulus*y for x, y in zip(model.quotient_secret, h))
        if tuple(coefficient*x % q for x in candidate) != multiple: raise ArithmeticError("candidate escaped the actual supplied multiple")
        fit = original_fit(records, candidate, radius)
        trials.append({**trial, "status": "ORIGINAL_RADIUS_FIT" if fit["fits_public_radius"] else "ORIGINAL_RADIUS_FIT_FAILED",
            "public_basis_model": basis, "response_receipts": tuple(receipts),
            "missing_quotient_candidate": h, "candidate_secret": candidate,
            "multiple_equation_verified": True, "original_fit": fit})
        result["original_candidate_verification_evaluations"] += len(records)
        result["original_response_rounding_evaluations"] += n
        if fit["fits_public_radius"]:
            return {**result, "status": "ONE_ORIGINAL_RADIUS_FIT_SOURCE_CERTIFICATION_REQUIRED",
                "candidate_secret": candidate, "trial_records": tuple(trials), "blocks_attempted": len(trials),
                "complete_schedule_or_original_fit_found": True}
    return {**result, "status": "NO_RADIUS_FIT_IN_DECLARED_BLOCKS_NOT_NO_SECRET", "trial_records": tuple(trials),
        "blocks_attempted": len(trials), "complete_schedule_or_original_fit_found": True}


def scan(records, multiples, coefficient_bound, radius, maximum_valuation, max_pair_trials=10000, max_blocks=MAX_BLOCKS):
    records = original_bank(records);q, n = records[0].modulus, len(records[0].label)
    integer(coefficient_bound, "positive coefficient bound", 1);integer(maximum_valuation, "nonnegative supported valuation")
    integer(max_pair_trials, "positive whole coefficient scan cap", 1)
    integer(radius, "public original verification radius");integer(max_blocks, "positive complete block cap", 1)
    if 4*radius >= q: raise ValueError("original radius requires4R<q")
    if maximum_valuation >= root_digits(q): raise ValueError("nonzero multiple valuations required")
    multiples = tuple(canonical_vector(w, n, q) for w in multiples)
    if not multiples: raise ValueError("nonempty external multiple list required")
    C = min(coefficient_bound, q//2);planned = 2*C*len(multiples)
    base = {"declared_coefficient_bound": coefficient_bound, "effective_centered_coefficient_bound": C,
        "maximum_supported_valuation": maximum_valuation, "supplied_multiples": multiples,
        "planned_coefficient_trials": planned, "trials_evaluated": 0, "candidate_secret": None,
        "original_records_paid_once": len(records), "multiple_list_coverage_supplied": False,
        "new_original_samples_created": False, "actual_planted_truth_certified": False,
        "original_candidate_verification_evaluations": 0, "block_attempts": 0,
        "original_response_rounding_evaluations": 0,
        "public_label_preprocessing_is_free": False,
        "first_fit_requires_global_original_code_and_noise_events": True}
    base.update({"verification_radius": radius, "max_pair_trials": max_pair_trials, "max_blocks": max_blocks})
    if planned > max_pair_trials:
        return {**base, "status": "COMPLETE_COEFFICIENT_SCAN_CAP_EXCEEDED_NOT_NO_CANDIDATE", "trial_records": (),
            "complete_scan_or_original_fit_found": False}
    bank = BasisBank(records, max_blocks) if maximum_valuation else None
    if bank is not None and bank.cap_exceeded:
        return {**base, "status": "COMPLETE_BASIS_SCHEDULE_CAP_EXCEEDED_NOT_NO_CANDIDATE", "trial_records": (),
            "complete_scan_or_original_fit_found": False}
    trials = []
    for w in multiples:
        for c in (*range(-C, 0), *range(1, C+1)):
            a, d = c, 0
            while a % 3 == 0: a, d = a//3, d+1
            if d > maximum_valuation:
                trials.append({"coefficient": c, "multiple": w, "status": "OUTSIDE_DECLARED_VALUATION_SCOPE"});continue
            trial = complete(records, c, w, radius, max_blocks=max_blocks, bank=bank)
            base["original_candidate_verification_evaluations"] += trial["original_candidate_verification_evaluations"]
            base["original_response_rounding_evaluations"] += trial["original_response_rounding_evaluations"]
            base["block_attempts"] += trial["blocks_attempted"]
            trials.append({"coefficient": c, "multiple": w, "completion": trial})
            if trial["candidate_secret"] is not None:
                return {**base, "status": "FIRST_RADIUS_FIT_SOURCE_CERTIFICATION_REQUIRED", "candidate_secret": trial["candidate_secret"],
                    "trial_records": tuple(trials), "trials_evaluated": len(trials), "complete_scan_or_original_fit_found": True,
                    "public_basis_rank_calls": bank.rank_calls if bank else 0, "public_basis_inverse_calls": bank.inverse_calls if bank else 0}
    return {**base, "status": "NO_RADIUS_FIT_IN_COMPLETE_DECLARED_SCAN_NOT_NO_SECRET",
        "trial_records": tuple(trials), "trials_evaluated": len(trials), "complete_scan_or_original_fit_found": True,
        "public_basis_rank_calls": bank.rank_calls if bank else 0, "public_basis_inverse_calls": bank.inverse_calls if bank else 0}


def _certificate_int(value):
    if type(value) is int: return value
    if type(value) is str:
        n = int(value)
        if str(n) == value and abs(n) > 2**53-1: return n
    raise ValueError("canonical exact certificate integer required")


def verify_probability_boxes(report):
    bases = [p["maximum_valuation_basis_event"] for p in report["Gaussian_source_profiles"] if p["maximum_valuation_basis_event"] is not None]
    bases.append(report["constant_width_large_dimension_countercontrol"])
    for base in bases:
        z, wrap = base["Gaussian_derived_error_law"], base["nonzero_ring_wrap_tail"]
        if gaussian_alphabet_boxes(z["continuous_Gaussian_width"], z["enclosure_bits"]) != z:
            raise ValueError("Gaussian zero mass probability replay failed")
        expected = gaussian_radius_box(wrap["continuous_Gaussian_width"], _certificate_int(wrap["integer_error_radius"]), wrap["enclosure_bits"])
        if exact_json(expected) != wrap: raise ValueError("wrapped ring error probability replay failed")
    for p in report["Gaussian_source_profiles"]:
        b = p["original_radius_Gaussian_law"]
        expected = gaussian_radius_box(b["continuous_Gaussian_width"], _certificate_int(b["integer_error_radius"]), b["enclosure_bits"])
        if exact_json(expected) != b: raise ValueError("original radius probability replay failed")
    return {"verified": True, "Gaussian_laws_replayed": len(bases)+len(report["Gaussian_source_profiles"]),
        "same_trusted_Arb_special_functions_reused": True, "independent_transcendental_certificate_supplied": False}


def power_box(base, exponent, bits=128, max_bit_work=524288):
    base = _rational(base);integer(exponent, "nonnegative probability power")
    integer(bits, "positive probability bits", 1);integer(max_bit_work, "positive exact power bit cap", 1)
    if not 0 <= base <= 1: raise ValueError("probability base required")
    required = exponent*max(base.numerator.bit_length(), base.denominator.bit_length())
    model = {"base": str(base), "exponent": exponent, "bits": bits, "required_operand_bits_upper": required,
        "max_bit_work": max_bit_work}
    if required > max_bit_work:
        return {**model, "status": "UNKNOWN_EXACT_POWER_CAP", "lower": "0", "upper": "1"}
    a, b, scale = base.numerator**exponent, base.denominator**exponent, 2**bits
    return {**model, "status": "CERTIFIED_INTEGER_DYADIC_POWER", "lower": str(Fraction(a*scale//b, scale)),
        "upper": str(Fraction((a*scale+b-1)//b, scale))}


def basis_probability_ledger(n, trials, beta, g, bits=128):
    integer(n, "positive dimension", 1);integer(trials, "nonnegative disjoint trials")
    root_digits(g);beta = _rational(beta)
    zero = gaussian_alphabet_boxes(beta, bits);wrap = gaussian_radius_box(beta, g-1, bits)
    clean = power_box(zero["zero"]["lower"], n, bits)
    success = Fraction(clean["lower"])/2
    exact_failure = power_box(1-success, trials, bits)
    block = (success.denominator+success.numerator-1)//success.numerator if success else None
    half = Fraction(1, 2**min(64, trials//block)) if block else Fraction(1)
    failure = min(Fraction(exact_failure["upper"]), half)
    ring_zero_upper = min(Fraction(1), Fraction(zero["zero"]["upper"])+Fraction(wrap["upper"]))
    correct_upper = power_box(ring_zero_upper, n, bits)
    any_correct_upper = min(Fraction(1), trials*Fraction(correct_upper["upper"]))
    return {"dimension": n, "disjoint_original_trials": trials, "derived_modulus": g,
        "Gaussian_derived_error_law": zero, "nonzero_ring_wrap_tail": wrap,
        "unit_minor_probability_lower": "1/2", "unwrapped_clean_basis_probability_box": clean,
        "one_trial_success_probability_lower": str(success), "all_trials_fail_power_box": exact_failure,
        "reciprocal_Bernoulli_half_block": block, "half_block_failure_upper": str(half),
        "all_trials_fail_probability_upper": str(failure),
        "one_row_ring_zero_probability_upper": str(ring_zero_upper), "all_selected_ring_errors_zero_power_box": correct_upper,
        "any_correct_basis_probability_upper": str(any_correct_upper),
        "no_correct_basis_probability_lower": str(1-any_correct_upper),
        "IID_uniform_original_labels_and_independent_Gaussian_errors_required": True,
        "source_IDs_establish_independence": False, "reused_blocks_count_as_independent_trials": False,
        "unwrapped_clean_event_is_necessary_for_correctness": False,
        "correctness_upper_bound_includes_nonzero_wrapped_errors": True,
        "general_decoder_lower_bound_proved": False}


def source_ledger(n, r, rows, alpha, maximum_valuation, radius, bits=128, coverage_failure=None):
    integer(n, "positive dimension", 1);integer(r, "positive original root", 1);integer(rows, "positive original count", 1)
    integer(maximum_valuation, "nonnegative maximum supported valuation")
    if maximum_valuation >= r: raise ValueError("nonzero original multiple required")
    q, alpha = 3**r, _rational(alpha)
    if not 0 < alpha < 1: raise ValueError("positive subunit original Gaussian width required")
    code = separation_ledger(q, n, rows, radius)
    original = gaussian_radius_box(alpha*q, radius, bits)
    original_failure = min(Fraction(1), rows*Fraction(original["upper"]))
    basis = basis_probability_ledger(n, rows//n, alpha*3**maximum_valuation, 3**maximum_valuation, bits) if maximum_valuation else None
    failure = min(Fraction(1), original_failure+Fraction(code["global_code_separation_failure_upper_used"])+(Fraction(basis["all_trials_fail_probability_upper"]) if basis else 0))
    coverage = None if coverage_failure is None else _rational(coverage_failure)
    if coverage is not None and not 0 <= coverage <= 1: raise ValueError("valid external coverage bound required")
    return {"dimension": n, "root_digits": r, "original_rows": rows, "original_Gaussian_width": str(alpha),
        "maximum_supported_valuation": maximum_valuation, "maximum_valuation_basis_event": basis,
        "original_radius_Gaussian_law": original, "whole_original_radius_failure_upper": str(original_failure),
        "global_original_code_separation_ledger": code, "uniform_local_failure_upper": str(failure),
        "external_true_usable_pair_or_complete_scan_coverage_failure_upper": None if coverage is None else str(coverage),
        "recovery_failure_upper_IF_source_coverage_and_complete_work_hold": None if coverage is None else str(min(Fraction(1), failure+coverage)),
        "maximum_valuation_clean_event_covers_all_smaller_true_quotients": True,
        "valuation_or_unit_part_union_multiplier_required": False,
        "conditioning_on_data_selected_multiple_truth_used": False,
        "whole_derived_bank_triplet_truncation_required": False,
        "original_rows_need_not_be_paired": True,
        "source_alpha_q_at_least_2_sqrt_n": (alpha*q)**2 >= 4*n,
        "worst_case_lattice_reduction_compatibility_established": False,
        "default_complete_schedule_cap_feasible": rows//n <= MAX_BLOCKS and n*n <= MAX_MINOR_ENTRIES,
        "source_laws_or_multiple_producer_supplied": False}


def control(n, r, g, pairs, seed, error_index=0):
    raw, mask, truth, _ = source_data(n, r, pairs, False, seed)
    q = 3**r;Q = q//g;secret = tuple((s-m) % q for s, m in zip(truth, mask))
    E = Q if g >= 9 else (Q//2+1 if g == 3 else q//8)
    errors = tuple(E*int(j == error_index) for j in range(len(raw)))
    raw = tuple(NoisyLinearRecord(s.label, (s.value+e) % q, q, s.source_id) for s, e in zip(raw, errors))
    w = tuple(g*s % q for s in secret);result = complete(raw, g, w, E)
    return {"original_records": tuple(r.public() for r in raw), "coefficient": g, "multiple": w, "radius": E,
        "truth_fixture_only": {"original_secret": secret, "original_errors": errors}, "completion": result,
        "matches_truth_fixture": result["candidate_secret"] == secret,
        "external_multiple_prepared_from_truth_FOR_CALIBRATION_ONLY": True,
        "calibration_is_unbounded_Gaussian_source": False}


def falsifiers():
    controls = []
    # Both combined label directions are present, but no scheduled block is a basis.
    for kind, labels, secret, errors, radius in (
        ("full_bank_rank_but_every_fixed_block_singular", ((1, 0), (1, 0), (0, 1), (0, 1)), (5, 7), (0, 0, 0, 0), 0),
        ("wrong_planted_secret_with_an_original_radius_fit", ((1, 0), (0, 1), (1, 0), (0, 1)), (5, 7), (9, 0, 0, 0), 9),
        ("nonzero_unwrapped_error_is_harmless_modulo_missing_ring", ((1,), (1,), (1,)), (5,), (81, 0, 0), 0),
    ):
        raw = tuple(NoisyLinearRecord(a, (sum(x*y for x, y in zip(a, secret))+e) % 81, 81, f"{kind}:{j}")
            for j, (a, e) in enumerate(zip(labels, errors)))
        w = tuple(9*s % 81 for s in secret);result = complete(raw, 9, w, radius)
        controls.append({"kind": kind, "original_records": tuple(r.public() for r in raw),
            "coefficient": 9, "multiple": w, "radius": radius,
            "truth_fixture_only": {"original_secret": secret, "original_errors": errors},
            "completion": result, "matches_truth_fixture": result["candidate_secret"] == secret,
            "external_multiple_prepared_from_truth_FOR_CALIBRATION_ONLY": True,
            "calibration_is_unbounded_Gaussian_source": False})
    return controls


def build_report():
    profiles = []
    for n, beta in ((8, Fraction(1, 4)), (32, Fraction(1, 6)), (128, Fraction(1, 6))):
        d = 1
        while 3**(d+1) <= n**3 and d+1 < n: d += 1
        profiles.append(source_ledger(n, n, n*max(128, 2*n), beta/3**d, d, (3**n)//n))
    controls = [control(*x) for x in ((4, 16, 81, 90, 103001), (3, 8, 3, 30, 104002), (8, 64, 729, 220, 104003))]
    first = controls[0];raw = tuple(NoisyLinearRecord(**r) for r in first["original_records"])
    scanned = scan(raw, (first["multiple"],), 81, first["radius"], 4)
    deps = ("native_affine_fibre_relaxation.py", "native_small_multiple_completion.py", "native_classical_modulus_descent.py",
        "native_gaussian_quotient_completion.py", "native_full_root_slice.py", "ternary_covariant_noise.py",
        "ternary_noise_degradation.py", "ternary_measured_lattice_decoder.py")
    return {"status": "DISJOINT_CLEAN_BASIS_CLASSICAL_COMPLETION_AND_MONOTONE_SOURCE_EVENT_REVIEW_PENDING",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
        "dependency_sha256": {f: hashlib.sha256((ROOT/"theorems"/f).read_bytes()).hexdigest() for f in deps},
        "actual_original_controls": controls, "actual_unknown_coefficient_scan": scanned,
        "actual_original_falsifiers": falsifiers(),
        "Gaussian_source_profiles": profiles,
        "constant_width_large_dimension_countercontrol": basis_probability_ledger(1024, 2048, "1/2", 3**18),
        "accepted_speedup_candidate": False, "new_active_negative_result_created": False,
        "Gaussian_LWE_solver_or_new_quantum_algorithm": False, "novelty_claim": False,
        "research_decision": "PAY_SOURCE_AWARE_CLEAN_BASIS_COMPARISON_BEFORE_CUBIC_MATRICES_OR_QUANTUM_SIGNAL"}


def main():
    parser = argparse.ArgumentParser(description=__doc__);parser.add_argument("--write", action="store_true");parser.add_argument("--check-probabilities", action="store_true")
    args = parser.parse_args()
    if args.check_probabilities:
        print(json.dumps(verify_probability_boxes(json.loads(REPORT.read_text())), indent=2));return
    p = build_report()
    if args.write: REPORT.write_text(json.dumps(exact_json(p), indent=2)+"\n")
    print(json.dumps({"status": p["status"], "actual_control_matches": [c["matches_truth_fixture"] for c in p["actual_original_controls"]],
        "source_rows": [s["original_rows"] for s in p["Gaussian_source_profiles"]],
        "cubic_features_compiled": 0, "multiple_producer_supplied": False}, indent=2))


if __name__ == "__main__": main()
