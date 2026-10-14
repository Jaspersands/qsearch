"""Receipt-checked short-preimage to original noisy-linear recovery reduction.

No scalable helper is supplied. Bounded exhaustive controls are labelled as
such; a classical compilation oracle is not a free quantum ingredient.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
from itertools import product
import json
from pathlib import Path

from flint import fmpq

from native_known_seed_group_workbench import source_fixture
from native_noisy_phase_input import checked_source_bank
from known_preparation_coherent_reflection import checked_shape
from ternary_certified_noise_sampler import rational
from ternary_covariant_noise import root_digits
from ternary_measured_lattice_decoder import exact_json, integer
from ternary_noise_degradation import NoisyLinearRecord

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT/"research/NATIVE_SHORT_PREIMAGE_REDUCTION.md"
REPORT = ROOT/"research/reductions/native_short_preimage_reduction.json"
LABEL_ONLY = "LABEL_ONLY_HELPER_INDEPENDENT_ZERO_MEAN_ORIGINAL_ERRORS"
GLOBAL_MOMENT = "GLOBAL_ORIGINAL_MOMENT_BOUNDED_WORDS_DATA_DEPENDENCE_ALLOWED"


@dataclass(frozen=True)
class PublicWordFamily:
    modulus: int
    dimension: int
    cohorts: int
    sites: int
    paired_labels: tuple

    def __post_init__(self):
        root_digits(self.modulus)
        integer(self.dimension, "positive original dimension", 1)
        checked_shape(self.cohorts, self.sites)
        pairs = tuple(tuple(tuple(tuple(a) for a in pair) for pair in cohort) for cohort in self.paired_labels)
        if len(pairs) != self.cohorts or any(len(c) != self.sites for c in pairs):
            raise ValueError("complete public cohort labels required")
        if any(len(pair) != 2 or any(len(a) != self.dimension or any(type(x) is not int or not 0 <= x < self.modulus for x in a) for a in pair) for c in pairs for pair in c):
            raise ValueError("canonical original public label pairs required")
        object.__setattr__(self, "paired_labels", pairs)

    def record(self):
        return {"modulus": str(self.modulus), "dimension": self.dimension,
                "cohorts": self.cohorts, "sites": self.sites,
                "paired_labels": self.paired_labels,
                "responses_masks_source_IDs_and_errors_supplied": False}

    def fingerprint(self):
        return hashlib.sha256(json.dumps(exact_json(self.record()), sort_keys=True, separators=(",", ":")).encode()).hexdigest()

    def frequency(self, cohort, word):
        integer(cohort, "nonnegative public cohort index")
        word = tuple(word)
        if cohort >= self.cohorts or len(word) != self.sites or any(type(t) is not int or t not in (0, 1, 2) for t in word):
            raise ValueError("canonical cohort and ternary word required")
        out = [0]*self.dimension
        for pair, t in zip(self.paired_labels[cohort], word):
            a, c = pair
            for i, (x, y) in enumerate(zip(a, c)):
                out[i] = (out[i]+(x, y-x, -y)[t]) % self.modulus
        return tuple(out)


def public_family(records, cohorts, sites):
    records = tuple(records)
    if not records: raise ValueError("nonempty original data required")
    n = len(records[0].label)
    records, _, q, _ = checked_source_bank(records, (0,)*n)
    checked_shape(cohorts, sites)
    if len(records) != 2*cohorts*sites:
        raise ValueError("exact paid original pair count required")
    labels = tuple(tuple((records[2*(b*sites+j)].label, records[2*(b*sites+j)+1].label) for j in range(sites)) for b in range(cohorts))
    return PublicWordFamily(q, n, cohorts, sites, labels)


@dataclass(frozen=True)
class PreimageReceipt:
    public_family_sha256: str
    target: tuple[int, ...]
    cohort: int
    word: tuple[int, ...]


def verify_receipt(family, target, receipt):
    target = tuple(target)
    if len(target) != family.dimension or any(type(x) is not int or not 0 <= x < family.modulus for x in target):
        raise ValueError("canonical requested frequency required")
    if not isinstance(receipt, PreimageReceipt) or receipt.public_family_sha256 != family.fingerprint() or tuple(receipt.target) != target:
        raise ValueError("preimage receipt is not bound to this public family and target")
    if family.frequency(receipt.cohort, receipt.word) != target:
        raise ValueError("receipt word is not an actual requested preimage")
    return receipt


class BoundedExhaustiveLabelControl:
    """A finite proof fixture, not a proposed polynomial preimage algorithm."""
    def __init__(self, family, word_cap=512):
        integer(word_cap, "positive bounded enumeration cap", 1)
        count = family.cohorts*3**family.sites
        if count > word_cap:
            raise ValueError("exhaustive label control exceeds finite cap; no scalable helper is supplied")
        self.family_sha256 = family.fingerprint()
        self.table = {}
        self.words_evaluated, self.calls = count, 0
        for b in range(family.cohorts):
            for word in product(range(3), repeat=family.sites):
                target = family.frequency(b, word)
                self.table.setdefault(target, PreimageReceipt(self.family_sha256, target, b, word))

    def __call__(self, family, target):
        if family.fingerprint() != self.family_sha256:
            raise ValueError("bounded helper called with a different public family")
        self.calls += 1
        return self.table.get(tuple(target))

    def cost(self):
        return {"kind": "BOUNDED_EXHAUSTIVE_LABEL_ONLY_CONTROL", "word_evaluations": self.words_evaluated,
                "lookup_calls": self.calls, "public_frequency_support": len(self.table),
                "word_work_is_exponential_in_sites": True, "polynomial_scalable_helper_supplied": False}


def probe_plan(n, q):
    integer(n, "positive original dimension", 1)
    r = root_digits(q)
    return tuple({"coordinate": i, "digit": d, "frequency": tuple(3**(r-1-d) if j == i else 0 for j in range(n))}
                 for i in range(n) for d in range(r))


def evaluate_probe(records, mask, family, target, receipt):
    records, mask, _, _ = checked_source_bank(records, mask)
    if public_family(records, family.cohorts, family.sites) != family:
        raise ValueError("response records do not match the receipt's public label family")
    receipt = verify_receipt(family, target, receipt)
    q, eta, coefficients, sources = family.modulus, 0, [0]*len(records), []
    for j, t in enumerate(receipt.word):
        i = 2*(receipt.cohort*family.sites+j)
        weights = ((1, 0), (-1, 1), (0, -1))[t]
        for k, w in enumerate(weights):
            record = records[i+k]
            masked_value = (record.value+sum(a*m for a, m in zip(record.label, mask))) % q
            eta = (eta+w*masked_value) % q
            coefficients[i+k] = w
            if w: sources.append(record.source_id)
    squared = sum(w*w for w in coefficients)
    if squared > 2*family.sites:
        raise ArithmeticError("bounded word exceeded the short coefficient proof")
    return {"requested_frequency": tuple(target), "receipt": {"public_family_sha256": receipt.public_family_sha256,
             "target": receipt.target, "cohort": receipt.cohort, "word": receipt.word},
            "signed_original_coefficients": tuple(coefficients), "coefficient_squared_norm": squared,
            "derived_masked_response": eta, "active_original_source_IDs": tuple(sources),
            "fresh_original_errors_created": False}


def decode_probe_values(probes, n, q):
    plan, recovered, decisions = probe_plan(n, q), [0]*n, []
    if len(probes) != len(plan):
        raise ValueError("complete nonadaptive probe schedule required before decoding")
    for scheduled, probe in zip(plan, probes):
        if tuple(probe["requested_frequency"]) != scheduled["frequency"]:
            raise ValueError("random labels cannot be substituted for the chosen-frequency schedule")
        value = probe["derived_masked_response"]
        if type(value) is not int or not 0 <= value < q:
            raise ValueError("canonical exact observed response required")
        i, d = scheduled["coordinate"], scheduled["digit"]
        prefix = recovered[i]
        correction = scheduled["frequency"][i]*prefix % q
        residual = (value-correction) % q
        distances = tuple(min((residual-k*(q//3)) % q, (k*(q//3)-residual) % q) for k in range(3))
        selected = tuple(k for k, x in enumerate(distances) if x == min(distances))
        if len(selected) != 1:
            return {"status": "AMBIGUOUS_EXACT_TRIT_DISTANCE", "masked_secret": None, "decisions": decisions}
        trit = selected[0]
        recovered[i] += trit*3**d
        decisions.append({**scheduled, "lower_prefix_before": prefix, "known_phase_correction": correction,
                          "corrected_response": residual, "circular_integer_distances": distances,
                          "chosen_trit": trit, "lower_prefix_after": recovered[i]})
    return {"status": "COMPLETE_RECEIPT_CHECKED_CLASSICAL_RECONSTRUCTION", "masked_secret": tuple(recovered),
            "decisions": decisions, "correctness_requires_the_stated_noise_bound": True}


def recover_with_helper(records, mask, cohorts, sites, helper):
    records, mask, q, n = checked_source_bank(records, mask)
    family = public_family(records, cohorts, sites)
    plan, probes, missing = probe_plan(n, q), [], []
    # All helper targets are fixed and called before any response is evaluated.
    receipts = tuple(helper(family, p["frequency"]) for p in plan)
    for scheduled, receipt in zip(plan, receipts):
        if receipt is None:
            missing.append(scheduled)
        else:
            probes.append(evaluate_probe(records, mask, family, scheduled["frequency"], receipt))
    if missing:
        return {"status": "INCOMPLETE_SHORT_PREIMAGE_HELPER", "original_secret": None,
                "public_family": family.record(), "public_family_sha256": family.fingerprint(),
                "planned_probes": plan, "missing_probes": tuple(missing), "completed_probe_receipts": probes,
                "partial_batch_promoted_to_recovery": False,
                "original_records_paid_once": len(records), "helper_calls": len(receipts),
                "helper_classical_polynomial_runtime_proved_by_receipts": False,
                "helper_label_only_independence_proved_by_API": False,
                "new_quantum_algorithm_or_speedup": False}
    decoded = decode_probe_values(probes, n, q)
    result = {**decoded, "public_family": family.record(), "public_family_sha256": family.fingerprint(),
              "planned_probes": plan, "completed_probe_receipts": probes,
              "original_secret": None if decoded["masked_secret"] is None else tuple((x-y) % q for x, y in zip(decoded["masked_secret"], mask)),
              "original_records_paid_once": len(records), "helper_calls": len(receipts),
              "helper_classical_polynomial_runtime_proved_by_receipts": False,
              "helper_label_only_independence_proved_by_API": False,
              "new_quantum_algorithm_or_speedup": False}
    return result


def noise_ledger(n, q, cohorts, sites, moment, *, model, helper_failure_upper="0"):
    integer(n, "positive original dimension", 1)
    r = root_digits(q)
    checked_shape(cohorts, sites)
    V, helper_failure = rational(moment, "true original integer second moment"), rational(helper_failure_upper, "whole-batch helper failure promise")
    if V < 0 or not 0 <= helper_failure <= 1 or model not in (LABEL_ONLY, GLOBAL_MOMENT):
        raise ValueError("valid explicit source/helper model and nonnegative moment required")
    intrinsic = 72*n*r*sites*V/(q*q) if model == LABEL_ONLY else 144*cohorts*sites*sites*V/(q*q)
    total = min(fmpq(1), intrinsic+helper_failure)
    return {"dimension": n, "modulus": str(q), "root_digits": r, "cohorts": cohorts, "sites": sites,
            "nonadaptive_probe_count": n*r, "original_classical_record_count": 2*cohorts*sites,
            "true_original_second_moment_upper": str(V), "source_helper_model": model,
            "coefficient_squared_norm_upper": 2*sites, "whole_batch_helper_failure_upper": str(helper_failure),
            "source_failure_upper_unclipped": str(intrinsic), "complete_reconstruction_failure_upper": str(total),
            "full_recovery_lower_if_helper_is_supplied": str(1-total),
            "derived_probe_independence_required": False,
            "original_error_independence_and_zero_mean_required": model == LABEL_ONLY,
            "original_errors_independent_of_labels_and_helper_coins_required": model == LABEL_ONLY,
            "marginal_original_second_moments_suffice_for_global_bound": model == GLOBAL_MOMENT,
            "fresh_source_noise_per_helper_call_required": False,
            "source_moment_or_helper_access_established_from_small_receipts": False,
            "classical_polynomial_preimage_helper_supplied": False,
            "efficient_original_problem_decoder_supplied": False,
            "quantum_preimage_algorithms_excluded": False, "accepted_speedup_candidate": False}


def calibration_control(n, r, B, M, noisy, seed):
    recipe, truth, errors = source_fixture(n, r, B, M, noisy, seed)
    src = recipe["source_receipts"]
    raw = tuple(NoisyLinearRecord(tuple(row["label"]), row["value"], row["modulus"], row["source_id"]) for row in src["original_classical_records"])
    mask = tuple(src["preparation_random_mask"])
    family = public_family(raw, B, M)
    helper = BoundedExhaustiveLabelControl(family)
    result = recover_with_helper(raw, mask, B, M, helper)
    original = tuple((x-y) % family.modulus for x, y in zip(truth, mask))
    return {"original_records": tuple(row.public() for row in raw), "known_mask": mask,
            "truth_fixture_only": {"masked_secret": truth, "original_secret": original, "original_errors": errors},
            "helper_cost": helper.cost(), "result": result,
            "matches_truth_fixture": result["original_secret"] == original,
            "secret_or_errors_used_by_decoder": False, "bounded_control_is_a_scalable_solver": False}


def build_report():
    controls = [calibration_control(*p) for p in ((1, 1, 1, 3, False, 87001), (1, 2, 1, 4, False, 87002),
                                                (2, 2, 1, 4, False, 87003), (1, 2, 1, 4, True, 87004),
                                                (2, 2, 1, 1, False, 87005))]
    ledgers = []
    for n in (8, 32, 64, 128):
        q, M = 3**n, n*n+24
        V = fmpq(q*q, 3*n**6)+fmpq(1, 2)
        for model in (LABEL_ONLY, GLOBAL_MOMENT): ledgers.append(noise_ledger(n, q, 1, M, V, model=model))
    dependencies = ("native_known_seed_group_workbench.py", "native_noisy_phase_input.py", "known_preparation_coherent_reflection.py",
                    "ternary_certified_noise_sampler.py", "ternary_covariant_noise.py", "ternary_measured_lattice_decoder.py",
                    "ternary_noise_degradation.py")
    return {"status": "CONDITIONAL_CLASSICAL_SHORT_PREIMAGE_TO_ORIGINAL_LWE_REDUCTION_REVIEW_PENDING",
            "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "dependency_sha256": {f: hashlib.sha256((ROOT/"theorems"/f).read_bytes()).hexdigest() for f in dependencies},
            "bounded_original_data_controls": controls, "scalable_source_helper_ledgers": ledgers,
            "research_decision": "DO_NOT_GRANT_CLASSICAL_SHORT_PREIMAGE_COMPILATION_AS_A_FREE_QUANTUM_INGREDIENT",
            "classical_polynomial_short_preimage_solver_constructed": False,
            "general_quantum_fibre_processing_ruled_out": False,
            "accepted_speedup_candidate": False, "new_active_negative_result_created": False,
            "remaining_obligations": ["external proof review", "actual scalable preimage-helper algorithm or explicit oracle cost",
                                      "label-only versus data-dependent access provenance and original error law",
                                      "quantum frame/row access with absolute normalization and retained garbage",
                                      "production candidate/reduction/dequantization integration"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2)+"\n")
    print(json.dumps({"status": report["status"], "controls": [{"status": c["result"]["status"], "matches_truth": c["matches_truth_fixture"],
                       "enumerated_words": c["helper_cost"]["word_evaluations"]} for c in report["bounded_original_data_controls"]],
                      "scalable_ledgers": len(report["scalable_source_helper_ledgers"]), "accepted_speedup_candidate": False}, indent=2))


if __name__ == "__main__":
    main()
