"""Causal public-phase feedback compiler and costed fixed-trine emulation.

LOCAL DERIVATION / REVIEW PENDING. Supplied covariant records are NOT a
classical simulator for the original DCP inputs or their unknown phase states.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path
import random

import numpy as np

from ternary_covariant_noise import CovariantRecord, phase, root_digits, simulated_record
from ternary_posterior_dual import solve_least_trit
from ternary_product_trine import F3, randomized_outcome

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT/"research/classical_baselines/ternary_phase_feedback.json"


def _integer(x, name, minimum=0):
    if type(x) is not int or x < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return x


def _pair(x, q):
    x = tuple(x)
    if len(x) != 2 or any(type(a) is not int or not 0 <= a < q for a in x):
        raise ValueError("canonical public phase pair required")
    return x


def _batch(records, original_ids):
    records, ids = tuple(records), tuple(original_ids)
    if not records or any(not isinstance(r, CovariantRecord) for r in records):
        raise ValueError("nonempty supplied covariant-record stream required")
    q, n = records[0].modulus, len(records[0].first)
    if any(r.modulus != q or len(r.first) != n for r in records):
        raise ValueError("one source modulus and dimension required")
    if len(ids) != len(records) or any(type(i) is not int or i < 0 for i in ids) or len(set(ids)) != len(ids):
        raise ValueError("distinct original source IDs required")
    return records, ids, q, n


@dataclass(frozen=True)
class PublicPhasePolicy:
    """Auditable examples; no callbacks carrying hidden/future input data."""

    kind: str = "zero"
    known_offset: tuple = ()

    def __post_init__(self):
        if self.kind not in ("zero", "known_offset", "quadratic_feedback"):
            raise ValueError("unsupported public phase policy")
        object.__setattr__(self, "known_offset", tuple(self.known_offset))
        if (self.kind == "known_offset") != bool(self.known_offset):
            raise ValueError("only known-offset policy takes a nonempty public offset")

    def choose(self, first, second, q, prior_reported_outcomes):
        # Only current labels and PAST reported outcomes enter phase selection.
        CovariantRecord(first, second, (0, 0), q)
        history = tuple(_pair(x, q) for x in prior_reported_outcomes)
        if self.kind == "zero":
            return (0, 0)
        if self.kind == "known_offset":
            if len(self.known_offset) != len(first) or any(type(x) is not int or not 0 <= x < q for x in self.known_offset):
                raise ValueError("canonical public known offset of source dimension required")
            return tuple(sum(a*x for a, x in zip(row, self.known_offset)) % q for row in (first, second))
        feedback = sum(a+2*b for a, b in history) % q
        alpha = (sum(a*a+c for a, c in zip(first, second))+feedback+len(history)) % q
        beta = (sum(a*c for a, c in zip(first, second))+pow(feedback, 3, q)-len(history)) % q
        return (alpha, beta)


def compile_covariant_feedback(records, original_ids, policy):
    """Exact causal transcript coupling, without new measurements or copies."""
    records, ids, q, _ = _batch(records, original_ids)
    if type(policy) is not PublicPhasePolicy:
        raise ValueError("auditable public policy required")
    history, steps = [], []
    for original, original_id in zip(records, ids):
        phases = policy.choose(original.first, original.second, q, history)
        shifted = tuple((y-a) % q for y, a in zip(original.outcome, phases))
        steps.append({"original_id": original_id, "first": original.first, "second": original.second,
                      "phase_pair": phases, "reported_outcome": shifted, "modulus": q})
        history.append(shifted)
    return {"status": "EXACT_CLASSICAL_COVARIANT_FEEDBACK_TRANSCRIPT",
            "policy": {"kind": policy.kind, "known_offset": policy.known_offset}, "steps": steps,
            "cost_ledger": {"supplied_covariant_records_consumed": len(records), "distinct_original_ids": ids,
                            "new_source_records_or_unknown_phase_states_created": 0,
                            "classical_modular_subtractions": 2*len(records),
                            "public_policy_evaluation_calls": len(records),
                            "policy_computation_is_classical_and_must_be_charged": True,
                            "quantum_phase_gates_needed_after_records_supplied": 0},
            "readout_model": "FULL_ROOT_COVARIANT",
            "source_independence_not_proved_by_unique_IDs": True,
            "general_causal_public_phase_equivalence_derived": True,
            "original_unknown_states_or_DCP_classically_simulated": False,
            "arbitrary_non_diagonal_or_collective_operations_covered": False,
            "speedup_claim_allowed": False}


def recover_raw_records(transcript):
    """Inverse map also checks the causal policy and every ancestor ID."""
    if transcript.get("readout_model") != "FULL_ROOT_COVARIANT":
        raise ValueError("fixed trine or other measurements are not a covariant relabeling")
    policy = PublicPhasePolicy(**transcript["policy"])
    records, ids, history = [], [], []
    for step in transcript["steps"]:
        q = step["modulus"]
        phases = _pair(step["phase_pair"], q)
        reported = _pair(step["reported_outcome"], q)
        if phases != policy.choose(step["first"], step["second"], q, history):
            raise ValueError("transcript phase disagrees with causal public policy")
        outcome = tuple((y+a) % q for y, a in zip(reported, phases))
        records.append(CovariantRecord(step["first"], step["second"], outcome, q))
        ids.append(step["original_id"]); history.append(reported)
    records, ids, _, _ = _batch(records, ids)
    if transcript["cost_ledger"]["supplied_covariant_records_consumed"] != len(records):
        raise ValueError("feedback stream cost ledger mismatch")
    if tuple(transcript["cost_ledger"]["distinct_original_ids"]) != ids:
        raise ValueError("feedback ancestor ledger mismatch")
    return records, ids


def feedback_posterior(transcript, **budgets):
    records, ids = recover_raw_records(transcript)
    result = solve_least_trit(records, ids, **budgets)
    result.update({"feedback_removed_by_exact_classical_inverse": True,
                   "feedback_adds_information_about_secret": False,
                   "physical_covariant_record_source_still_required": True})
    return result


def filter_trine_orbit(record, phase_pair):
    """One supplied record is consumed even when its fixed-basis filter fails."""
    if not isinstance(record, CovariantRecord):
        raise ValueError("supplied covariant record required")
    q = record.modulus
    alpha, beta = _pair(phase_pair, q)
    first = (record.outcome[0]-alpha) % q
    if first % (q//3):
        return None
    z = first//(q//3)
    if record.outcome[1] != (beta+2*q//3*z) % q:
        return None
    return {"digit": z, "phase_pair": (alpha, beta), "first": record.first,
            "second": record.second, "modulus": q,
            "fixed_trine_phases_are_not_paired_covariant_outcomes": True}


def trine_resampling_budget(digits, target_records, maximum_source_records):
    _integer(digits, "root digits", 1); _integer(target_records, "target records")
    _integer(maximum_source_records, "source cap")
    q = 3**digits; p = Fraction(3, q*q)
    # This bound is necessary for success >=1/2, not a sufficient algorithm.
    return {"digits": digits, "modulus": str(q), "target_fixed_basis_records": target_records,
            "maximum_covariant_source_records": maximum_source_records,
            "acceptance_probability_per_consumed_record": str(p),
            "uncapped_expected_covariant_records": str(target_records/p),
            "expected_accepted_records_under_cap": str(maximum_source_records*p),
            "probability_of_filling_target_upper_by_Markov": str(min(Fraction(1), maximum_source_records*p/target_records)) if target_records else "1",
            "cost_polynomial_in_q_not_log_q": True,
            "polynomial_in_n_only_if_q_is_polynomial_and_source_supply_permits": True,
            "batch_label_lookahead_fixed_trine_compilation_covered": False,
            "same_record_can_be_retried_as_fresh_source": False,
            "input_states_classically_simulated": False}


def run_trine_resampling(records, original_ids, target_records, policy):
    """Finite supplied stream; stop at a declared target or report shortage."""
    records, ids, q, _ = _batch(records, original_ids)
    _integer(target_records, "target records")
    if type(policy) is not PublicPhasePolicy:
        raise ValueError("auditable causal public phase policy required")
    history, accepted, rejected, consumed = [], [], [], 0
    if target_records:
        for record, source_id in zip(records, ids):
            phases = policy.choose(record.first, record.second, q, history)
            sample = filter_trine_orbit(record, phases)
            consumed += 1
            if sample is None:
                rejected.append(source_id)
            else:
                accepted.append({**sample, "original_id": source_id})
                # Match the post-correction output convention of feedback policies.
                history.append(randomized_outcome(q, 0, 0, sample["digit"]))
            if len(accepted) == target_records:
                break
    return {"status": "TARGET_FIXED_TRINE_STREAM_FILLED" if len(accepted) == target_records else "SOURCE_CAP_EXHAUSTED_NO_COMPLETE_FIXED_TRINE_STREAM",
            "accepted_records": accepted, "rejected_original_ids": rejected,
            "consumed_original_ids": ids[:consumed], "unused_original_ids": ids[consumed:],
            "cost_ledger": {"supplied_covariant_records_consumed": consumed,
                            "source_cap": len(records), "target_records": target_records,
                            "conditional_success_not_treated_as_unconditional": True},
            "source_law_contract": "fresh IID full native labels and covariant observations; policy set before seeing each observation",
            "retained_label_IID_claim_conditional_on_source_contract": True,
            "batch_label_lookahead_fixed_trine_compilation_covered": False,
            "quantum_unknown_states_classically_simulated": False, "speedup_claim_allowed": False}


def physical_phase_control(q, first, second, secret, phase_pair):
    """All outcomes on actual native phases; arbitrary public phase settings."""
    root_digits(q)
    if q > 27:
        raise ValueError("dense phase control capped at q27")
    validate = CovariantRecord(first, second, (0, 0), q)
    first, second = validate.first, validate.second
    if len(secret) != len(first) or any(type(s) is not int or not 0 <= s < q for s in secret):
        raise ValueError("canonical calibration secret required")
    alpha, beta = _pair(phase_pair, q)
    a, c = (sum(x*s for x, s in zip(row, secret)) % q for row in (first, second))
    state = np.array([1, phase(a, q), phase(c, q)])/np.sqrt(3)
    corrected = state*np.array([1, phase(-alpha, q), phase(-beta, q)])
    fixed = abs(F3 @ corrected)**2
    accepted = np.zeros(3); relabel_residual = 0.0
    for y1, y2 in product(range(q), repeat=2):
        p = abs(corrected[0]+corrected[1]*phase(-y1, q)+corrected[2]*phase(-y2, q))**2/(q*q)
        recovered = CovariantRecord(first, second, ((y1+alpha) % q, (y2+beta) % q), q)
        relabel_residual = max(relabel_residual, abs(p-recovered.probability(secret)))
        raw = CovariantRecord(first, second, (y1, y2), q)
        filtered = filter_trine_orbit(raw, (alpha, beta))
        if filtered:
            accepted[filtered["digit"]] += raw.probability(secret)
    expected_acceptance = Fraction(3, q*q)
    accept_residual = abs(float(accepted.sum())-float(expected_acceptance))
    conditional_residual = float(np.max(abs(accepted/float(expected_acceptance)-fixed)))
    if max(relabel_residual, accept_residual, conditional_residual) > 3e-12:
        raise ArithmeticError("public phase covariance/orbit law mismatch")
    return {"modulus": q, "first": first, "second": second, "calibration_secret": secret,
            "public_phase_pair": (alpha, beta), "covariant_output_relabel_residual": relabel_residual,
            "orbit_acceptance_probability": str(expected_acceptance), "orbit_acceptance_residual": accept_residual,
            "fixed_trine_conditional_Born_residual": conditional_residual,
            "all_covariant_outcomes_kept_in_control": q*q,
            "calibration_secret_not_an_input_to_policy_or_decoder": True}


def report():
    cases = []
    for q in (3, 9, 27):
        for s, settings in product((0, 3 % q, q-1), ((0, 0), (1, q-1), (q-1, 1))):
            cases.append(physical_phase_control(q, (1,), (q-1,), (s,), settings))
    rng = random.Random(99681)
    records = tuple(simulated_record((i+1,), ((2*i+3) % 9,), (4,), 9, rng)[0] for i in range(4))
    transcripts = []
    for policy in (PublicPhasePolicy(), PublicPhasePolicy("known_offset", (2,)), PublicPhasePolicy("quadratic_feedback")):
        transcript = compile_covariant_feedback(records, range(4), policy)
        recovered, ids = recover_raw_records(transcript)
        if recovered != records or ids != tuple(range(4)):
            raise ArithmeticError("causal feedback is not invertible")
        transcript["original_supplied_records_calibration_only"] = [r.public() for r in records]
        transcript["prespecified_frequency_rows_not_IID_population_evidence"] = True
        transcript["exact_feedback_removed_posterior"] = feedback_posterior(transcript)
        transcripts.append(transcript)
    return {"status": "COSTED_PUBLIC_PHASE_FEEDBACK_ACCESS_AUDIT_REVIEW_PENDING",
            "derivation_sha256": hashlib.sha256((ROOT/"research/TERNARY_PHASE_FEEDBACK.md").read_bytes()).hexdigest(),
            "quantum_speedup_proved": False, "candidate_record_accepted": False, "novelty_claim": False,
            "original_DCP_inputs_classically_simulated": False,
            "physical_phase_and_filter_controls": cases, "causal_feedback_controls": transcripts,
            "scaling_resampling_ledgers": [trine_resampling_budget(r, r-2, (r-2)*r*r) for r in (4, 8, 16, 32, 64)],
            "finite_shortage_control": run_trine_resampling(records, range(4), 4, PublicPhasePolicy()),
            "falsifiers": ["Causal public phase feedback changes the full-covariant raw-record posterior.",
                           "A fixed-trine orbit has input-dependent acceptance or a different conditional Born law.",
                           "A resampling emulator fills its stream by silently reusing rejected records or ignoring source shortage."],
            "arbitrary_non_covariant_or_collective_readouts_covered": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = report()
    encoded = json.dumps(result, indent=2, allow_nan=False)+"\n"
    if args.write:
        REPORT.write_text(encoded)
    print(json.dumps({"status": result["status"], "physical_controls": len(result["physical_phase_and_filter_controls"]),
                      "causal_feedback_controls": len(result["causal_feedback_controls"]), "speedup_claim_allowed": False}))


if __name__ == "__main__":
    main()
