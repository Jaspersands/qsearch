"""Original-data ternary descent, correlated noise and compressed-only information.

This is a classical transformation, not a quantum-only phase operation.
Exact lost-secret digits are scoped to receivers that discard parent values,
value-dependent hashes and every other secret-dependent side channel.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path

from flint import nmod_mat

from ternary_covariant_noise import root_digits
from ternary_measured_lattice_decoder import exact_json, integer
from ternary_noise_degradation import NoisyLinearRecord

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/NATIVE_CLASSICAL_MODULUS_DESCENT.md"
REPORT = ROOT / "research/classical_baselines/native_classical_modulus_descent.json"


def digest(value):
    return hashlib.sha256(json.dumps(exact_json(value), sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def nearest_third(x):
    if type(x) is not int:
        raise ValueError("exact signed integer response required")
    return (x+1)//3


def _label_shape(labels, q):
    if root_digits(q) < 2:
        raise ValueError("descent requires an original modulus at least9")
    labels = tuple(tuple(tuple(a) for a in pair) for pair in labels)
    if not labels or any(len(pair) != 2 for pair in labels):
        raise ValueError("nonempty paired public labels required")
    n = len(labels[0][0])
    if not n or any(len(a) != n or any(type(x) is not int or not 0 <= x < q for x in a)
                    for pair in labels for a in pair):
        raise ValueError("canonical consistent original label vectors required")
    return labels, n


def low_direction(labels, q):
    labels, n = _label_shape(labels, q)
    if len(labels) != n+1:
        raise ValueError("each deterministic block needs exactly n+1 input pairs")
    slopes = [[(a[i]+c[i]) % 3 for a, c in labels] for i in range(n)]
    kernel, nullity = nmod_mat(slopes, 3).nullspace()
    if not nullity:
        raise ArithmeticError("an n by n+1 slope matrix must have a kernel")
    v = tuple(int(kernel[j, 0]) for j in range(n+1))
    scale = pow(next(x for x in v if x), -1, 3)
    return tuple(x*scale % 3 for x in v)


def branch_map(labels, direction, q):
    labels, n = _label_shape(labels, q)
    direction = tuple(direction)
    if len(direction) != len(labels) or not any(direction) or any(type(x) is not int or x not in (0, 1, 2) for x in direction):
        raise ValueError("nonzero canonical block direction required")
    if any(sum((a[i]+c[i])*v for (a, c), v in zip(labels, direction)) % 3 for i in range(n)):
        raise ValueError("direction must annihilate the actual low slopes")
    weights, reduced = [], []
    for z in (1, 2):
        row = tuple((0, 0) if not v else ((-2, 1) if v*z % 3 == 1 else (-1, -1)) for v in direction)
        delta = tuple(sum(w[0]*a[i]+w[1]*c[i] for (a, c), w in zip(labels, row)) % q for i in range(n))
        if any(x % 3 for x in delta):
            raise ArithmeticError("original label combination is not divisible by3")
        weights.append(row);reduced.append(tuple(x//3 for x in delta))
    return tuple(weights), tuple(reduced)


@dataclass(frozen=True)
class OriginalPair:
    a: NoisyLinearRecord
    c: NoisyLinearRecord

    def __post_init__(self):
        if not isinstance(self.a, NoisyLinearRecord) or not isinstance(self.c, NoisyLinearRecord):
            raise ValueError("actual original classical records required")
        if self.a.modulus != self.c.modulus or len(self.a.label) != len(self.c.label) or self.a.source_id == self.c.source_id:
            raise ValueError("consistent pair with distinct original ancestors required")

    @property
    def modulus(self): return self.a.modulus
    @property
    def labels(self): return self.a.label, self.c.label
    @property
    def values(self): return self.a.value, self.c.value
    @property
    def original_ids(self): return self.a.source_id, self.c.source_id
    @property
    def level(self): return 0

    def observation(self):
        return {"modulus": self.modulus, "labels": self.labels, "values": self.values}

    def record(self):
        return {**self.observation(), "kind": "ORIGINAL_CLASSICAL_PAIR", "level": 0,
                "original_source_ids": self.original_ids}


def _check_pairs(pairs):
    pairs = tuple(pairs)
    if not pairs or any(not isinstance(p, (OriginalPair, DescendedPair)) for p in pairs):
        raise ValueError("nonempty typed original or lineage-preserving derived pairs required")
    first = pairs[0]
    if any(p.modulus != first.modulus or p.level != first.level or len(p.labels[0]) != len(first.labels[0]) for p in pairs):
        raise ValueError("consistent dimension, level and modulus required")
    ids = tuple(x for p in pairs for x in p.original_ids)
    if len(set(ids)) != len(ids):
        raise ValueError("original ancestors cannot be reused as independent blocks")
    return pairs


@dataclass(frozen=True)
class DescendedPair:
    parents: tuple
    direction: tuple
    labels: tuple
    values: tuple

    def __post_init__(self):
        parents = _check_pairs(self.parents)
        object.__setattr__(self, "parents", parents)
        direction = low_direction(tuple(p.labels for p in parents), parents[0].modulus)
        if tuple(self.direction) != direction:
            raise ValueError("only the replayable low-slope-only selection policy is admitted")
        object.__setattr__(self, "direction", direction)
        weights, labels = branch_map(tuple(p.labels for p in parents), direction, parents[0].modulus)
        values = tuple(nearest_third(sum(w[0]*p.values[0]+w[1]*p.values[1] for p, w in zip(parents, row))) % self.modulus for row in weights)
        if tuple(tuple(a) for a in self.labels) != labels or tuple(self.values) != values:
            raise ValueError("derived labels and values must replay from the actual parents")
        object.__setattr__(self, "labels", labels);object.__setattr__(self, "values", values)

    @property
    def modulus(self): return self.parents[0].modulus//3
    @property
    def level(self): return self.parents[0].level+1
    @property
    def original_ids(self): return tuple(x for p in self.parents for x in p.original_ids)

    def observation(self):
        return {"modulus": self.modulus, "labels": self.labels, "values": self.values}

    def record(self):
        weights, _ = branch_map(tuple(p.labels for p in self.parents), self.direction, 3*self.modulus)
        return {**self.observation(), "kind": "DESCENDED_CORRELATED_CLASSICAL_PAIR", "level": self.level,
                "original_source_ids": self.original_ids, "direction": self.direction,
                "branch_weights": weights, "parent_record_sha256": tuple(digest(p.record()) for p in self.parents),
                "fresh_original_errors_created": False, "pair_errors_assumed_independent": False,
                "receipt_hashes_are_excluded_from_compressed_only_receiver": True}


def originals(records):
    records = tuple(records)
    if not records or len(records) % 2:
        raise ValueError("nonempty complete original record pairs required")
    return _check_pairs(tuple(OriginalPair(a, c) for a, c in zip(records[::2], records[1::2])))


def descend(pairs):
    pairs = _check_pairs(pairs)
    q, n = pairs[0].modulus, len(pairs[0].labels[0])
    if root_digits(q) < 2:
        raise ValueError("cannot descend below modulus3")
    width, outputs = n+1, []
    used = len(pairs)//width*width
    for start in range(0, used, width):
        parents = pairs[start:start+width]
        labels = tuple(p.labels for p in parents)
        v = low_direction(labels, q);weights, reduced = branch_map(labels, v, q)
        values = tuple(nearest_third(sum(w[0]*p.values[0]+w[1]*p.values[1] for p, w in zip(parents, row))) % (q//3) for row in weights)
        outputs.append(DescendedPair(parents, v, reduced, values))
    return tuple(outputs), {"input_pairs": len(pairs), "output_pairs": len(outputs), "input_modulus": q,
        "output_modulus": q//3, "block_width": width, "pairs_used": used,
        "unused_original_source_ids": tuple(x for p in pairs[used:] for x in p.original_ids),
        "original_ancestors_paid_once": sum(len(p.original_ids) for p in pairs),
        "label_preprocessing_arithmetic_order_per_block": "O(n^3) over F3 and O(n^2) log(q)-bit arithmetic",
        "quantum_only_unknown_phases_are_an_input": False, "retained_parent_values_are_part_of_observation": False}


def noise_ledger(q, active_sites, moment, independent_original_scalars):
    if root_digits(q) < 2: raise ValueError("descent root at least9 required")
    integer(active_sites, "positive active sites", 1)
    if type(independent_original_scalars) is not bool: raise ValueError("explicit independence premise required")
    V = Fraction(moment)
    if V < 0: raise ValueError("nonnegative true conditional moment bound required")
    factor = 5 if independent_original_scalars else 9
    before = factor*active_sites*V
    after = Fraction(2, 9)*before+Fraction(1, 2)
    return {"input_modulus": q, "output_modulus": q//3, "active_sites": active_sites,
        "true_input_marginal_second_moment_upper": str(V), "pre_rounding_branch_second_moment_upper": str(before),
        "rounded_output_marginal_second_moment_upper": str(after),
        "normalized_output_moment_upper": str(after/(q//3)**2),
        "independent_original_scalars_required": independent_original_scalars,
        "independent_input_pairs_and_conditional_joint_sign_symmetry_required": True,
        "within_pair_covariance_before_rounding_upper_if_original_independent": str(2*active_sites*V) if independent_original_scalars else None,
        "within_pair_covariance_if_identical_scalar_variance_formula": "m * actual common variance",
        "output_pair_errors_independent": False, "moments_infer_maximum_noise_atom": False,
        "upper_bound_growth_is_a_noise_lower_bound_or_no_go": False, "source_premises_established_by_API": False}


def joint_noise_law(direction, error_law, q, max_assignments=100000):
    if root_digits(q) < 2: raise ValueError("descent root at least9 required")
    integer(max_assignments, "positive exact population budget", 1)
    direction = tuple(direction)
    if not direction or not any(direction) or any(type(v) is not int or v not in (0, 1, 2) for v in direction):
        raise ValueError("nonzero canonical error-combination direction required")
    law = tuple((e, Fraction(p)) for e, p in error_law)
    if not law or len({e for e, _ in law}) != len(law) or any(type(e) is not int or p <= 0 for e, p in law) or sum(p for _, p in law) != 1:
        raise ValueError("distinct exact signed errors with a normalized positive rational law required")
    active = tuple(v for v in direction if v)
    assignments = len(law)**(2*len(active))
    if assignments > max_assignments:
        return {"status": "NOISE_POPULATION_CAP_EXCEEDED_NOT_A_NOISE_BOUND", "assignments_evaluated": 0,
                "assignments_required": assignments, "input_modulus": q, "direction": direction,
                "pair_max_atom": None, "law": None}
    counts = Counter()
    for samples in product(law, repeat=2*len(active)):
        delta = [0, 0];probability = Fraction(1)
        for j, v in enumerate(active):
            a, c = samples[2*j][0], samples[2*j+1][0]
            probability *= samples[2*j][1]*samples[2*j+1][1]
            d = (c-2*a, -c-a)
            delta[0] += d[v-1];delta[1] += d[2-v]
        counts[tuple(nearest_third(x) % (q//3) for x in delta)] += probability
    return {"status": "EXACT_DECLARED_ORIGINAL_ERROR_LAW_PUSHFORWARD", "assignments_evaluated": assignments,
            "input_modulus": q, "direction": direction,
            "pair_max_atom": str(max(counts.values())),
            "law": tuple({"errors": e, "probability": str(p)} for e, p in sorted(counts.items())),
            "original_error_law": tuple((e, str(p)) for e, p in law),
            "law_inferred_from_observed_responses": False, "scalar_product_law_assumed": False}


def guessing_bound(original_q, n, levels, pairs, pair_max_atom=None):
    r = root_digits(original_q)
    integer(n, "positive secret dimension", 1);integer(levels, "positive descent levels", 1)
    integer(pairs, "nonnegative final paired observations")
    if levels >= r: raise ValueError("remaining modulus at least3 required")
    q = original_q//3**levels
    alias = Fraction(1, 3**(n*levels))
    power = 2*pairs-n
    exponent = -n*levels+min(0, (r-levels)*power)
    bound = Fraction(1, 3**(-exponent))
    if pair_max_atom is not None:
        beta = Fraction(pair_max_atom)
        if not Fraction(1, q*q) <= beta <= 1: raise ValueError("valid true conditional joint-noise maximum-atom upper required")
        alphabet_ratio = Fraction(q**max(0, power), q**max(0, -power))
        residual = min(Fraction(1), alphabet_ratio*beta**pairs)
        bound = alias*residual
    return {"original_modulus": original_q, "remaining_modulus": q, "dimension": n, "levels": levels,
        "final_pairs": pairs, "erased_secret_trits": n*levels, "alias_only_full_secret_success_upper": str(alias),
        "observation_alphabet_bound_applied": True,
        "true_conditional_pair_max_atom_upper": None if pair_max_atom is None else str(Fraction(pair_max_atom)),
        "full_original_secret_guessing_success_upper": str(bound) if max(bound.numerator.bit_length(), bound.denominator.bit_length()) <= 12000 else None,
        "full_original_secret_guessing_success_upper_power3_without_atom": {"base": 3, "exponent": exponent} if pair_max_atom is None else None,
        "uniform_original_secret_and_secret_independent_labels_errors_required": True,
        "independent_final_noise_pairs_given_labels_required_for_atom_bound": pair_max_atom is not None,
        "receiver_input": "ONLY final labels/values and secret-independent label-only metadata",
        "excluded_inputs": ["original or intermediate responses", "value-dependent hashes/receipts", "truth/noise fixtures", "quantum-only source states"],
        "repeated_preparation_from_same_compressed_records_adds_information": False,
        "all_original_data_algorithms_or_quantum_LWE_are_ruled_out": False}


def lift_original_top_digit(records, known_lower):
    """Conditional classical lift using retained ORIGINAL values, not descended ones."""
    pairs = originals(records)
    records = tuple(s for p in pairs for s in (p.a, p.c))
    q, n = records[0].modulus, len(records[0].label)
    if root_digits(q) < 2: raise ValueError("quotient lift requires modulus at least9")
    lower = tuple(known_lower)
    if len(lower) != n or any(type(x) is not int or not 0 <= x < q//3 for x in lower):
        raise ValueError("explicit canonical known lower-quotient vector required")
    # Fix the row basis before any response processing; only invert over F3.
    reduced, rank = nmod_mat([[s.label[i] % 3 for s in records] for i in range(n)], 3).rref()
    base = {"original_modulus": q, "known_lower_input": lower, "original_records_read": len(records),
        "known_lower_correctness_established": False, "row_basis_selected_from_labels_only": True,
        "all_rounding_equations_are_conditional_on_original_error_bound": True,
        "complete_original_secret_solver_supplied": False}
    if rank != n:
        return {**base, "status": "ORIGINAL_LOW_LABEL_RANK_INSUFFICIENT", "rank_mod3": int(rank),
                "recovered_secret": None, "rounding_transcript": ()}
    pivots = tuple(next(j for j in range(len(records)) if reduced[i, j]) for i in range(n))
    transcript = []
    for s in records:
        residual = (s.value-sum(a*b for a, b in zip(s.label, lower))) % q
        distances = tuple(min((residual-t*(q//3)) % q, (t*(q//3)-residual) % q) for t in range(3))
        chosen = min(range(3), key=lambda t: distances[t])
        transcript.append({"source_id": s.source_id, "corrected_original_response": residual,
            "circular_distances": distances, "rounded_top_equation": chosen})
    inverse = nmod_mat([[x % 3 for x in records[j].label] for j in pivots], 3).inv()
    top = tuple(sum(int(inverse[i, j])*transcript[pivots[j]]["rounded_top_equation"] for j in range(n)) % 3 for i in range(n))
    consistent = all(sum(a*b for a, b in zip(s.label, top)) % 3 == t["rounded_top_equation"] for s, t in zip(records, transcript))
    return {**base, "status": "CONDITIONAL_ORIGINAL_BANK_TOP_DIGIT_LIFT" if consistent else "INCONSISTENT_ROUNDED_ORIGINAL_EQUATIONS",
        "rank_mod3": n, "label_only_basis_rows": pivots, "rounding_transcript": tuple(transcript),
        "recovered_top_digits": top if consistent else None,
        "recovered_secret": tuple(a+(q//3)*b for a, b in zip(lower, top)) if consistent else None,
        "rounding_consistency_proves_lower_input_or_noise_promise": False}


def original_lift_ledger(n, q, count, moment):
    integer(n, "positive dimension", 1);integer(count, "positive paid original count", 1)
    if count < n or root_digits(q) < 2: raise ValueError("enough original rows at root at least9 required")
    V = Fraction(moment)
    if V < 0: raise ValueError("nonnegative true original error moment required")
    # Keep the exponentially small hyperplane bound symbolic; charge a looser
    # exact capped-trit budget instead of expanding millions of denominator digits.
    rank = Fraction(1, 3**min(64, count-n))
    loss = min(Fraction(1), 36*count*V/(q*q))
    return {"dimension": n, "original_modulus": q, "original_records": count,
        "true_original_second_moment_upper": str(V), "conditional_rounding_failure_union_upper": str(loss),
        "IID_uniform_original_low_labels_rank_failure_upper_compact": {"numerator": "3^n-1", "denominator": "2*3^m", "n": n, "m": count},
        "rank_failure_upper_used_in_budget": str(rank),
        "conditional_lift_failure_upper_given_correct_lower": str(min(Fraction(1), loss+rank)),
        "known_lower_correctness_is_an_external_premise": True,
        "original_noise_moments_and_label_source_promises_verified": False,
        "returned_consistent_solution_is_a_correctness_certificate": False,
        "original_bank_retention_is_charged_not_forbidden": True}


def source_law_control(q, slopes):
    labels = tuple(((0,), (b,)) for b in slopes)
    v = low_direction(labels, q);site = next(j for j, x in enumerate(v) if x)
    counts, fixed_low = Counter(), Counter()
    for a, h in product(range(q), range(q//3)):
        changed = list(labels);changed[site] = ((a,), (((slopes[site]-a) % 3)+3*h,))
        _, reduced = branch_map(changed, v, q)
        key = tuple(row[0] for row in reduced);counts[key] += 1
        if a % 3 == 0: fixed_low[key] += 1
    return {"original_modulus": q, "fixed_low_slopes": slopes, "direction": v, "varied_active_site": site,
        "conditional_on_slopes_outputs": len(counts), "conditional_on_slopes_multiplicities": sorted(set(counts.values())),
        "conditional_on_all_low_labels_outputs": len(fixed_low), "conditional_on_all_low_labels_multiplicities": sorted(set(fixed_low.values())),
        "assignments_checked": q*(q//3), "remaining_pair_space": (q//3)**2,
        "all_low_labels_may_be_conditioned_without_changing_the_law": False}


def control(n, r, M, noisy, seed, levels):
    from native_full_root_slice import source_data
    raw, mask, truth, errors = source_data(n, r, M, noisy, seed)
    secret = tuple((a-b) % (3**r) for a, b in zip(truth, mask))
    pairs, histories = originals(raw), []
    for _ in range(levels):
        inputs = tuple(p.record() for p in pairs)
        pairs, cost = descend(pairs)
        histories.append({"inputs": inputs, "outputs": tuple(p.record() for p in pairs), "cost": cost})
        if not pairs: break
    actual_levels = len(histories)
    if not pairs: raise ValueError("live control requires nonempty final data")
    q = 3**r;remaining = q//3**actual_levels
    aliases = (secret, tuple((a+remaining) % q for a in secret), tuple((a+2*remaining) % q for a in secret))
    observations = tuple(p.observation() for p in pairs)
    replays = []
    for other in aliases:
        changed = tuple(NoisyLinearRecord(s.label, (sum(a*b for a, b in zip(s.label, other))+e) % q, q, s.source_id) for s, e in zip(raw, errors))
        current = originals(changed)
        for _ in range(actual_levels): current, _ = descend(current)
        replays.append({"secret_fixture_only": other, "final_observations_equal": tuple(p.observation() for p in current) == observations,
            "first_parent_receipt_equal": digest(current[0].record()) == digest(pairs[0].record())})
    lifted = lift_original_top_digit(raw, tuple(x % (q//3) for x in secret))
    return {"fixture_parameters": {"dimension": n, "root_digits": r, "original_pairs": M, "noisy": noisy, "seed": seed, "requested_levels": levels},
        "histories": histories, "truth_fixture_only": {"original_secret": secret, "original_errors": errors},
        "alias_replays": replays, "original_values_verified": all((sum(a*b for a, b in zip(s.label, secret))+e) % q == s.value for s, e in zip(raw, errors)),
        "full_secret_bound_for_compressed_only_receiver": guessing_bound(q, n, actual_levels, len(pairs)),
        "conditional_original_bank_lift": lifted, "conditional_lift_matches_truth": lifted["recovered_secret"] == secret,
        "lower_prefix_supplied_from_truth_FOR_CONTROL_ONLY": True,
        "secret_or_errors_read_by_transformation": False, "a_working_secret_decoder_is_supplied": False}


def scaling(n, r, M, levels):
    integer(n, "positive dimension", 1);integer(M, "positive original pairs", 1)
    q = 3**r;V = Fraction(q*q, 3*n**6)+Fraction(1, 2)
    rows = []
    for depth in range(1, min(levels, r-1)+1):
        count = M//(n+1)**depth
        L = noise_ledger(q, n+1, V, depth == 1)
        q //= 3;V = Fraction(L["rounded_output_marginal_second_moment_upper"])
        rows.append({"level": depth, "remaining_pairs": count, "worst_support_noise_ledger": L,
                     "compressed_only_full_secret_bound": guessing_bound(3**r, n, depth, count)})
    required = (n+1)**(r-1)
    return {"dimension": n, "root_digits": r, "original_pairs": M, "levels": rows,
            "full_depth_levels_to_modulus3": r-1,
            "original_pairs_required_for_one_terminal_pair_under_this_policy": str(required),
            "terminal_pairs_available_under_same_bank_full_depth_policy": M//required,
            "this_fixed_policy_resource_recurrence_is_a_universal_receiver_lower_bound": False,
            "true_source_moment_and_conditional_pair_independence_established": False,
            "noise_upper_bound_is_a_general_obstruction": False}


def build_report():
    controls = [control(*args) for args in ((2, 3, 12, False, 94001, 1), (2, 3, 12, True, 94002, 2), (3, 8, 64, True, 94003, 2))]
    deps = ("ternary_covariant_noise.py", "ternary_measured_lattice_decoder.py", "ternary_noise_degradation.py", "native_full_root_slice.py")
    return {"status": "SOURCE_CORRECT_CLASSICAL_DESCENT_AND_COMPRESSED_ONLY_INFORMATION_AUDIT_REVIEW_PENDING",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
        "dependency_sha256": {f: hashlib.sha256((ROOT/"theorems"/f).read_bytes()).hexdigest() for f in deps},
        "source_law_controls": [source_law_control(q, s) for q in (9, 27, 81) for s in ((0, 0), (1, 2), (1, 1))],
        "original_data_controls": controls,
        "declared_noise_controls": [joint_noise_law(v, ((-1, "1/3"), (0, "1/3"), (1, "1/3")), 27) for v in ((1,), (2,), (1, 2))],
        "scaling": [scaling(n, n, (n+1)**3, 3) for n in (8, 32, 64, 128)],
        "retained_original_bank_conditional_lift_ledgers": [original_lift_ledger(n, 3**n, 2*(n+1)**3, Fraction(3**(2*n), 3*n**6)+Fraction(1, 2)) for n in (8, 32, 64, 128)],
        "research_decision": "RETAIN_LOST_SECRET_INFORMATION_OR_LIMIT_TASK_TO_REMAINING_QUOTIENT; NO FREE QUANTUM_INFORMATION_FROM_REPREPARATION",
        "accepted_speedup_candidate": False, "new_active_negative_result_created": False,
        "remaining_obligations": ["external source-law/rounding/information review", "retained-complement or original-bank decoder",
            "source-specific correlated-noise maximum-atom bounds", "comparison to known modulus switching and BKW", "production integration"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__);parser.add_argument("--write", action="store_true")
    args = parser.parse_args();report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2)+"\n")
    print(json.dumps({"status": report["status"], "source_populations": len(report["source_law_controls"]),
        "original_data_controls": len(report["original_data_controls"]),
        "alias_replays_equal": all(a["final_observations_equal"] for c in report["original_data_controls"] for a in c["alias_replays"]),
        "accepted_speedup_candidate": False}, indent=2))


if __name__ == "__main__": main()
