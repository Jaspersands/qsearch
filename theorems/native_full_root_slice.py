"""Exact original-label all-root block problem and costed classical reconstruction.

Search is exponential and restricted to a low-only slice. No polynomial
preimage helper, uniform coherent full row or new quantum speedup is claimed.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
from itertools import product
import json
from pathlib import Path

from flint import fmpq

from native_affine_fibre_relaxation import canonical_vector, NonFreeRank
from native_carry_diagonal_slice import disjoint_kernel_slice, normalize, fingerprint, verify_directions
from native_choice_mitm import solve_choices
from native_known_seed_group_workbench import source_fixture
from native_prefix_carry_lift import compile_carry
from native_short_preimage_reduction import LABEL_ONLY, PreimageReceipt, noise_ledger, public_family, recover_with_helper
from ternary_covariant_noise import root_digits
from ternary_measured_lattice_decoder import exact_json, integer
from ternary_noise_degradation import NoisyLinearRecord

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT/"research/NATIVE_FULL_ROOT_SLICE.md"
REPORT = ROOT/"research/classical_baselines/native_full_root_slice.json"


@dataclass(frozen=True)
class FullRootProblem:
    slice: object
    base_frequency: tuple
    remaining_target: tuple
    choices: tuple

    @property
    def modulus(self): return self.slice.normalized.raw.family.modulus//3

    def frequency(self, parameters):
        parameters = canonical_vector(parameters, len(self.choices), 3)
        q = 3*self.modulus
        return tuple((a+3*sum(column[z][i] for column, z in zip(self.choices, parameters))) % q
                     for i, a in enumerate(self.base_frequency))

    def record(self):
        raw = self.slice.normalized.raw
        return {"diagonal_slice_sha256": fingerprint(self.slice.record()), "original_modulus": str(raw.family.modulus),
                "remaining_modulus": str(self.modulus), "original_target": raw.target,
                "base_frequency": self.base_frequency, "remaining_target": self.remaining_target,
                "remaining_choices": self.choices, "parameters": len(self.choices),
                "active_block_original_a_sums": tuple(tuple(sum(raw.family.paired_labels[raw.cohort][site][0][i]
                    for l, site in enumerate(raw.prefix_recipe.free_columns) if v[l]) % self.modulus for i in range(raw.family.dimension))
                    for v in self.slice.directions),
                "paired_choice_sum_is_minus_original_a_sum": True,
                "independent_ring_choice_distribution_assumed": False,
                "actual_original_word_map_used": True, "later_unrestricted_carries_assumed_cubic": False,
                "full_normalized_row_is_supplied": False}


def full_root_problem(slice_):
    verify_directions(slice_.normalized, slice_.directions)
    raw, q = slice_.normalized.raw, slice_.normalized.raw.family.modulus
    k, n = len(raw.prefix_recipe.free_columns), raw.family.dimension
    base = raw.family.frequency(raw.cohort, raw.word((0,)*k))
    residual = tuple((a-b) % q for a, b in zip(raw.target, base))
    if any(x % 3 for x in residual): raise ArithmeticError("base word missed actual target's low prefix")
    columns = []
    for v in slice_.directions:
        column = [(0,)*n]
        for z in (1, 2):
            delta = [0]*n
            for l, site in enumerate(raw.prefix_recipe.free_columns):
                t = v[l]*z % 3
                if not t: continue
                a, c = raw.family.paired_labels[raw.cohort][site]
                for i in range(n): delta[i] += (c[i]-2*a[i]) if t == 1 else -c[i]-a[i]
            delta = tuple(x % q for x in delta)
            if any(x % 3 for x in delta): raise ArithmeticError("native block did not preserve its low prefix")
            column.append(tuple(x//3 for x in delta))
        columns.append(tuple(column))
    problem = FullRootProblem(slice_, base, tuple(x//3 for x in residual), tuple(columns))
    for column, a_sum in zip(problem.choices, problem.record()["active_block_original_a_sums"]):
        if tuple((x+y) % problem.modulus for x, y in zip(column[1], column[2])) != tuple(-a % problem.modulus for a in a_sum):
            raise ArithmeticError("paired block choices violate original source correlation")
    return problem


def search(problem, max_evaluations=100000, max_entries=100000):
    result = solve_choices(problem.choices, problem.remaining_target, problem.modulus, max_evaluations, max_entries)
    if result["parameters"] is None:
        return {**result, "status": "SEARCH_CAP_EXCEEDED_NOT_NO_SOLUTION" if result["status"].startswith("SEARCH_CAP") else "COMPLETE_SEARCH_NO_FULL_ROOT_SOLUTION_ON_THIS_SLICE",
                "whole_root_target_matched": False, "absence_of_other_original_preimages_inferred": False}
    parameters = result["parameters"];raw = problem.slice.normalized.raw
    free = problem.slice.free(parameters);word = raw.word(free)
    actual = raw.family.frequency(raw.cohort, word)
    if actual != raw.target or actual != problem.frequency(parameters):
        raise ArithmeticError("ring solution is not an actual entire-root native preimage")
    return {**result, "status": "VERIFIED_CLASSICAL_WHOLE_ROOT_SLICE_WITNESS", "free_trits": free,
            "native_word": word, "actual_frequency": actual, "whole_root_target_matched": True,
            "coherent_uniform_full_row_sampler": False}


def root_moments(n, r, k, t):
    integer(n, "positive original dimension", 1);integer(r, "root exponent at least2", 2)
    integer(k, "nonnegative free-prefix width");integer(t, "nonnegative slice width")
    if t > k: raise ValueError("injective slice cannot exceed prefix width")
    E, surplus = n*(r-1), t-n*(r-1)
    short = abs(surplus) <= 512
    mu = fmpq(3**max(0, surplus), 3**max(0, -surplus)) if short else None
    return {"dimension": n, "root_digits": r, "prefix_free_trits": k, "slice_parameters": t,
            "remaining_group_trits": E, "slice_entropy_surplus": surplus,
            "mean_whole_root_solution_count": {"base": 3, "exponent": surplus},
            "variance_factor": {"one_minus_base": 3, "negative_exponent": E},
            "solution_existence_upper": {"base": 3, "exponent": min(0, surplus)},
            "no_solution_upper": {"base": 3, "exponent": min(0, -surplus)},
            "solution_existence_lower_formula": "mu/(mu+1)",
            "solution_existence_lower_if_short": str(mu/(mu+1)) if short else None,
            "word_pair_unit_minor": "actual distinct selector coefficient pairs have determinant +/-1",
            "IID_uniform_entire_higher_original_label_vectors_conditioned_on_low_labels_required": True,
            "full_low_prefix_rank_and_fixed_low_only_target_slice_required": True,
            "derived_choices_assumed_independent": False,
            "population_promises_established_by_artifact": False,
            "repeated_slices_or_queries_on_same_data_assumed_independent": False,
            "statistics_construct_a_polynomial_solver_or_coherent_row": False}


class FullRootSliceHelper:
    """Explicit exponential label-only helper, with actual incomplete receipts."""
    def __init__(self, family, max_evaluations=100000, max_entries=100000):
        if root_digits(family.modulus) < 2: raise ValueError("whole-root slice helper requires root at least9")
        integer(max_evaluations, "positive search cap", 1);integer(max_entries, "positive left storage cap", 1)
        self.family_sha256 = family.fingerprint()
        self.dimension, self.sites = family.dimension, family.sites
        self.max_evaluations, self.max_entries = max_evaluations, max_entries
        self.calls = []

    def __call__(self, family, target):
        if family.fingerprint() != self.family_sha256: raise ValueError("helper called on a different actual label family")
        target = canonical_vector(target, family.dimension, family.modulus)
        try: slice_ = disjoint_kernel_slice(normalize(compile_carry(family, 0, target)))
        except NonFreeRank:
            self.calls.append({"target": target, "status": "LOW_PREFIX_RANK_UNSUPPORTED_NOT_NO_PREIMAGES"});return None
        problem = full_root_problem(slice_)
        result = search(problem, self.max_evaluations, self.max_entries)
        self.calls.append({"target": target, "status": result["status"], "parameters": len(slice_.directions),
                           "assignments_evaluated": result["assignments_evaluated"], "stored_entries": result["stored_entries"],
                           "cost": result["cost"], "whole_root_target_matched": result["whole_root_target_matched"],
                           "slice_model": {"raw_carry": slice_.normalized.raw.record(), "output_normalization": slice_.normalized.record(),
                                           "diagonal_slice": slice_.record(), "whole_root_problem": problem.record()}})
        if result["parameters"] is None: return None
        return PreimageReceipt(self.family_sha256, target, 0, result["native_word"])

    def cost(self):
        return {"calls": tuple(self.calls), "total_assignments_evaluated": sum(c.get("assignments_evaluated", 0) for c in self.calls),
                "peak_stored_entries": max((c.get("stored_entries", 0) for c in self.calls), default=0),
                "preprocessing_or_search_is_free": False, "search_is_exponential": True,
                "polynomial_classical_helper_supplied": False, "coherent_uniform_full_row_sampler_supplied": False,
                "left_table_is_rebuilt_and_charged_per_query": True,
                "public_label_elements_per_query": 2*self.dimension*self.sites,
                "prefix_matrix_dimensions_per_query": (self.dimension, self.sites),
                "matrix_and_block_preprocessing_arithmetic_order": "O(n^2*M+n^3) per query with O(log(q))-bit operands",
                "matrix_preprocessing_is_free": False,
                "best_classical_runtime_bound_proved": False}


def ceil_log3(x):
    integer(x, "positive count", 1)
    e, power = 0, 1
    while power < x: e, power = e+1, power*3
    return e


def bank_tradeoff(n, r, failure_trits=6):
    integer(n, "positive original dimension", 1);integer(r, "root exponent at least2", 2)
    integer(failure_trits, "positive helper failure trits", 1)
    E, s = n*(r-1), ceil_log3(n*r+1)+failure_trits
    t = E+s;M = (n+1)*t+n
    absence_failure, rank_failure = fmpq(n*r, 3**s), fmpq(1, 3**s)
    helper_failure = absence_failure+rank_failure
    q = 3**r;V = fmpq(q*q, 3*n**6)+fmpq(1, 2)
    return {"dimension": n, "root_digits": r, "sites": M, "original_classical_records": 2*M,
            "guaranteed_slice_parameters": t, "entropy_surplus": s, "nonadaptive_original_probes": n*r,
            "conditional_batch_absence_probability_upper_if_complete_search": str(absence_failure),
            "rank_failure_upper_compact": {"hyperplanes_numerator_base": 3, "hyperplanes_numerator_exponent": n,
                "hyperplanes_numerator_subtract": 1, "hyperplanes_denominator": 2,
                "single_hyperplane_probability_base": 3, "single_hyperplane_probability_negative_exponent": M},
            "rank_failure_upper_used_in_budget": str(rank_failure),
            "whole_batch_helper_failure_upper_if_complete_search": str(helper_failure),
            "meet_in_middle_left_assignment_trits": t//2, "meet_in_middle_right_assignment_trits": t-t//2,
            "full_prefix_projection_loss_trits": M-n-t,
            "whole_root_population": root_moments(n, r, M-n, t),
            "original_secret_noise_ledger_if_complete_helper": noise_ledger(n, q, 1, M, V, model=LABEL_ONLY, helper_failure_upper=helper_failure),
            "complete_exponential_search_is_assumed_low_rank_failure_is_charged": True,
            "IID_uniform_original_low_and_higher_labels_required": True,
            "live_caps_proved_sufficient_for_scalable_search": False,
            "true_original_noise_model_established_by_artifact": False,
            "statistical_or_noise_feasibility_is_polynomial_runtime": False}


def source_data(n, r, M, noisy, seed):
    source, truth, errors = source_fixture(n, r, 1, M, noisy, seed)
    src = source["source_receipts"]
    raw = tuple(NoisyLinearRecord(tuple(s["label"]), s["value"], s["modulus"], s["source_id"])
                for s in src["original_classical_records"])
    return raw, tuple(src["preparation_random_mask"]), truth, errors


def control(n, r, M, seed, cap=729):
    raw, _, _, _ = source_data(n, r, M, False, seed);family = public_family(raw, 1, M)
    target = tuple((7+2*i) % family.modulus for i in range(n))
    slice_ = disjoint_kernel_slice(normalize(compile_carry(family, 0, target)));problem = full_root_problem(slice_)
    t = len(problem.choices)
    if 3**t <= cap: points = tuple(product(range(3), repeat=t));complete = True
    else:
        # Full frequency is a sum of one-parameter functions, so bases suffice.
        points = [(0,)*t]
        for j in range(t):
            for z in (1, 2):
                p = [0]*t;p[j] = z;points.append(tuple(p))
        points.extend((tuple(j % 3 for j in range(t)), tuple(2 for _ in range(t))))
        points = tuple(sorted(set(points)));complete = False
    if len(points) > cap: raise ValueError("whole-root diagnostic point cap exceeded")
    rows = []
    for parameters in points:
        word = slice_.normalized.raw.word(slice_.free(parameters));actual = family.frequency(0, word)
        if problem.frequency(parameters) != actual: raise ArithmeticError("all-root block model changed the actual native word frequency")
        rows.append({"parameters": parameters, "actual_frequency": actual, "is_whole_root_solution": actual == target})
    return {"raw_carry": slice_.normalized.raw.record(), "output_normalization": slice_.normalized.record(),
            "diagonal_slice": slice_.record(), "whole_root_problem": problem.record(), "native_word_checks": rows,
            "slice_exhaustively_enumerated": complete,
            "whole_root_solution_count": sum(row["is_whole_root_solution"] for row in rows) if complete else None,
            "solver": search(problem), "population_ledger": root_moments(n, r, M-n, t),
            "whole_root_model_is_an_unrestricted_row": False}


def reconstruction_control(n, r, M, noisy, seed):
    raw, mask, truth, errors = source_data(n, r, M, noisy, seed)
    family = public_family(raw, 1, M);helper = FullRootSliceHelper(family)
    result = recover_with_helper(raw, mask, 1, M, helper)
    original = tuple((x-y) % family.modulus for x, y in zip(truth, mask))
    return {"original_records": tuple(s.public() for s in raw), "known_mask": mask,
            "truth_fixture_only": {"original_secret": original, "original_errors": errors},
            "result": result, "helper_cost": helper.cost(), "matches_truth_fixture": result["original_secret"] == original,
            "secret_or_errors_used_by_helper_or_decoder": False, "noise_correctness_inferred_from_small_outputs": False}


def build_report():
    controls = [control(*p) for p in ((2, 2, 12, 92001), (3, 3, 15, 92002), (4, 64, 20, 92003),
                                     (8, 8, 88, 92004), (2, 3, 20, 93001))]
    reconstructions = [reconstruction_control(*p) for p in ((2, 3, 20, False, 93002), (2, 3, 20, True, 93003), (2, 6, 44, True, 93004))]
    deps = ("native_carry_diagonal_slice.py", "native_choice_mitm.py", "native_prefix_carry_lift.py", "native_affine_fibre_relaxation.py",
            "native_known_seed_group_workbench.py", "native_short_preimage_reduction.py", "ternary_covariant_noise.py",
            "ternary_measured_lattice_decoder.py", "ternary_noise_degradation.py")
    return {"status": "EXACT_ALL_ROOT_NATIVE_SLICE_AND_EXPONENTIAL_ORIGINAL_DATA_BASELINE_REVIEW_PENDING",
            "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "dependency_sha256": {f: hashlib.sha256((ROOT/"theorems"/f).read_bytes()).hexdigest() for f in deps},
            "whole_root_slice_controls": controls, "original_data_reconstruction_controls": reconstructions,
            "quadratic_bank_whole_root_ledgers": tuple(root_moments(n, n, n*n+24-n, (n*n+24-n)//(n+1)) for n in (8, 32, 64, 128)),
            "larger_bank_tradeoffs": tuple(bank_tradeoff(n, n) for n in (8, 32, 64, 128)),
            "research_decision": "DO_NOT_CONFUSE_FIRST_CARRY_WITNESSES_WITH_FULL_PREIMAGES_OR_EXPONENTIAL_COMPILATION_WITH_QUANTUM_ADVANTAGE",
            "accepted_speedup_candidate": False, "new_active_negative_result_created": False,
            "polynomial_full_root_preimage_helper_or_uniform_coherent_row_supplied": False,
            "remaining_obligations": ["external all-root additivity and original-frequency population review", "stronger actual-source classical algorithms",
                                      "coherent uniform rows with honest mass/compilation", "large-bank source and noise premises", "production integration"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__);parser.add_argument("--write", action="store_true")
    args = parser.parse_args();report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True);REPORT.write_text(json.dumps(exact_json(report), indent=2)+"\n")
    print(json.dumps({"status": report["status"], "whole_root_searches": [c["solver"]["status"] for c in report["whole_root_slice_controls"]],
                     "original_data_reconstructions": [{"status": c["result"]["status"], "matches_truth": c["matches_truth_fixture"],
                         "helper_assignments": c["helper_cost"]["total_assignments_evaluated"]} for c in report["original_data_reconstruction_controls"]],
                     "accepted_speedup_candidate": False}, indent=2))


if __name__ == "__main__": main()
