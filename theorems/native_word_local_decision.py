"""Actual paired-word heat bath, ground-space decision and local classical test.

Finite kernels are references. Small exact moves need not connect fibres;
the one-block statistic has a paid classical rational-precision counterpart.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path

import numpy as np

from native_short_preimage_reduction import public_family, PublicWordFamily
from native_word_frame_access import preparation_contract, finite_frame, word_error_second_moment
from native_full_root_slice import source_data
from native_word_span_decision import root_polynomial
from ternary_certified_noise_sampler import cosine_box
from ternary_native_block_walk import NativeBlockHeatbath, signature_count, transition_reference, complete_signature_audit
from ternary_covariant_noise import root_digits
from ternary_measured_lattice_decoder import exact_json, integer

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/NATIVE_WORD_LOCAL_DECISION.md"
REPORT = ROOT / "research/reductions/native_word_local_decision.json"


@dataclass(frozen=True)
class PairedWordSource:
    family: PublicWordFamily

    def __post_init__(self):
        if not isinstance(self.family, PublicWordFamily) or self.family.cohorts != 1:
            raise ValueError("one actual original word cohort required")

    @property
    def inputs(self): return self.family.sites

    @property
    def modulus(self): return self.family.modulus

    @property
    def dimension(self): return self.family.dimension

    @property
    def frequencies(self):
        # Subtract each site's base a: (0,c-2a,-c-a). This map has determinant3.
        q = self.modulus
        return tuple((tuple((c-2*a) % q for a, c in zip(x, y)),
                      tuple((-c-a) % q for a, c in zip(x, y))) for x, y in self.family.paired_labels[0])

    def value(self, word): return self.family.frequency(0, word)


@dataclass(frozen=True)
class PairedWordHeatbath(NativeBlockHeatbath):
    def __post_init__(self):
        if not isinstance(self.source, PairedWordSource): raise ValueError("actual paired-label source required")
        H = self.source.modulus if self.prefix is None else self.prefix
        root_digits(H)
        if self.source.modulus % H: raise ValueError("prefix must divide actual full root")
        object.__setattr__(self, "prefix", H)


def paired_collision_ledger(n, r, M, support):
    integer(n, "positive original dimension", 1);integer(r, "positive original digits", 1)
    count = signature_count(M, support)
    group = 3**(n*r)
    # Keep large-root certificates factored; an upper bound must round UP.
    bits = min(128, max(0, group.bit_length()-count.bit_length()-1))
    bound = Fraction(1, 2**bits)
    if count*2**bits > group and bits:
        raise ArithmeticError("dyadic collision bound rounded in the wrong direction")
    return {"dimension": n, "root_digits": r, "original_pairs": M, "support": support,
        "unoriented_difference_signatures": str(count), "probability_any_exact_full_root_local_collision_upper": str(bound),
        "exact_uncapped_union_ratio": {"numerator": str(count), "denominator_base": 3, "denominator_exponent": n*r},
        "conservative_probability_budget_bits": bits,
        "probability_ground_effect_is_identity_lower": str(1-bound),
        "original_paired_labels_IID_uniform_required": True,
        "independent_offset_frequency_columns_assumed": False,
        "nonunit_offset_chart_determinant": 3,
        "label_and_word_adaptive_exact_local_policies_covered": True,
        "every_signature_has_a_unit_in_original_pair_coefficients": True,
        "temporary_syndrome_violations_or_collective_macros_excluded": False,
        "generic_quantum_decoder_lower_bound_proved": False}


def local_acceptance_interval(records, mask, block, prefix=None, bits=64, max_local_words=729):
    """Classical expectation of one local quantum heat-bath projection."""
    records = tuple(records)
    if not records or len(records) % 2: raise ValueError("complete original pairs required")
    family = public_family(records, 1, len(records)//2)
    walk = PairedWordHeatbath(PairedWordSource(family), prefix)
    block = walk._block(block)
    integer(bits, "positive rational enclosure bits", 1);integer(max_local_words, "whole local table cap", 1)
    D = 3**len(block)
    if D > max_local_words: raise ValueError("whole local phase table cap exceeded; no partial estimator")
    phases = preparation_contract(records, mask, 1, family.sites)["known_word_phases_by_cohort"][0]
    groups = {}
    for digits in product(range(3), repeat=len(block)):
        value = walk.local_frequency(block, digits)
        phase = sum(phases[j][t] for j, t in zip(block, digits)) % family.modulus
        groups.setdefault(value, []).append(phase)
    lower, upper, pairs = Fraction(0), Fraction(0), 0
    for values in groups.values():
        denominator = D*len(values)
        lower += Fraction(len(values), denominator);upper += Fraction(len(values), denominator)
        for i, a in enumerate(values):
            for b in values[i+1:]:
                lo, hi = cosine_box(family.modulus, b-a, bits)
                lower += Fraction(str(lo))*2/denominator;upper += Fraction(str(hi))*2/denominator;pairs += 1
    return {"block": block, "original_modulus": family.modulus, "committed_prefix": walk.prefix,
        "local_words_evaluated": D, "cosine_pair_evaluations": pairs,
        "acceptance_lower": str(max(Fraction(0), lower)), "acceptance_upper": str(min(Fraction(1), upper)),
        "enclosure_bits": bits, "exact_IID_raw_null_acceptance": str(Fraction(len(groups), D)),
        "null_trace_is_for_fixed_mask_IID_original_values": True,
        "uses_actual_original_values_and_known_mask": True,
        "all_blocks_or_whole_words_enumerated": False,
        "unknown_quantum_only_phases_allowed": False,
        "ground_space_projection_or_long_time_walk_simulated": False,
        "classical_local_work_bound": "O(n*k*3^k + 9^k*poly(bits,log(q)) + n*M*poly(log(q)))"}


def expectation_polynomial(phases, rows, q):
    D = len(phases);coefficients = [Fraction(0)]*q
    for i, entries in enumerate(rows):
        for j, weight in entries:
            coefficients[(phases[j]-phases[i]) % q] += Fraction(weight)/D
    return root_polynomial(coefficients, q)


def component_rows(components, D):
    rows = [None]*D
    for component in components:
        for i in component: rows[i] = tuple((j, str(Fraction(1, len(component)))) for j in component)
    if any(row is None for row in rows): raise ValueError("whole component partition required")
    return tuple(rows)


def control(n, r, M, support, prefix, noisy, seed):
    raw, mask, truth, errors = source_data(n, r, M, noisy, seed)
    frame = finite_frame(raw, mask, 1, M)
    walk = PairedWordHeatbath(PairedWordSource(frame["family"]), prefix)
    reference = transition_reference(walk, support, max_words=256)
    signature_audit = complete_signature_audit(walk, support)
    D = 3**M;phases = tuple(row["known_phase"] for row in frame["rows"])
    transitions, components = reference["conditional_transition_rows"], reference["connected_components"]
    ground = component_rows(components, D)
    gap_bounds = []
    for C in components:
        if len(C) > 1:
            edge_min = min(Fraction(w) for i in C for j, w in transitions[i] if i != j)
            gap_bounds.append(Fraction(1) if support == M else 2*edge_min/(len(C)*(len(C)-1)))
    projector = np.zeros((D, D))
    for i, row in enumerate(ground):
        for j, w in row: projector[i, j] = float(Fraction(w))
    ideal = np.exp(2j*np.pi*np.asarray([sum(a*t for a, t in zip(row["frequency"], truth)) % (3**r)
                                       for row in frame["rows"]])/(3**r))/np.sqrt(D)
    state = frame["state"]
    source_membership = float(np.vdot(ideal, projector@ideal).real)
    rejection_bound = min(Fraction(1), 40*Fraction(str(word_error_second_moment(errors, 1, M)))/(3**(2*r)))
    actual_ground = float(np.vdot(state, projector@state).real)
    preserves = reference["full_native_source_family_stationary_certified"]
    if preserves and (abs(source_membership-1)>1e-10 or actual_ground<1-float(rejection_bound)-1e-10):
        raise ArithmeticError("full-root component projection lost source membership/noise bound")
    return {"original_records": tuple(s.public() for s in raw), "known_mask": mask,
        "truth_fixture_only": {"masked_secret": truth, "original_errors": errors},
        "preparation_contract": frame["spec"], "actual_word_rows": frame["rows"],
        "heatbath_reference": reference, "whole_small_signature_audit": signature_audit,
        "exact_ground_acceptance_polynomial": expectation_polynomial(phases, ground, 3**r),
        "exact_one_random_block_acceptance_polynomial": expectation_polynomial(phases, transitions, 3**r),
        "exact_ground_IID_null_acceptance": str(Fraction(len(components), D)),
        "null_trace_is_for_fixed_mask_IID_original_values": True,
        "exact_one_random_block_IID_null_acceptance": str(sum((Fraction(w) for i, row in enumerate(transitions) for j, w in row if i == j), Fraction(0))/D),
        "positive_Hamiltonian_gap_lower": str(min(gap_bounds)) if gap_bounds else None,
        "Hamiltonian_identically_zero": not gap_bounds,
        "ground_rank": len(components), "full_fibre_span_rank": int(sum(frame["counts"] > 0)),
        "diagnostic_actual_ground_acceptance": actual_ground,
        "diagnostic_ideal_source_ground_acceptance": source_membership,
        "full_root_source_moment_bound_applicable": preserves,
        "conditional_pathwise_ground_rejection_upper": str(rejection_bound) if preserves else None,
        "classical_first_block_expectation": local_acceptance_interval(raw, mask, tuple(range(support)), prefix),
        "dense_kernel_is_an_efficient_ground_effect": False,
        "coherent_walk_gate_export_supplied": False,
        "unknown_phase_measurement_access_granted": False,
        "new_speedup_claim": False}


def build_report():
    controls = [control(*p) for p in ((1, 2, 4, 1, None, False, 101001), (1, 2, 4, 2, None, True, 101001),
                                    (1, 2, 4, 4, None, False, 101001), (1, 2, 4, 2, 3, False, 101001))]
    deps = ("native_short_preimage_reduction.py", "native_word_frame_access.py", "native_full_root_slice.py",
            "native_word_span_decision.py", "ternary_native_block_walk.py", "ternary_certified_noise_sampler.py",
            "ternary_covariant_noise.py", "ternary_measured_lattice_decoder.py")
    return {"status": "PAIRED_WORD_LOCAL_GROUND_TEST_AND_CLASSICAL_ONE_BLOCK_COUNTERPART_REVIEW_PENDING",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
        "dependency_sha256": {f: hashlib.sha256((ROOT/"theorems"/f).read_bytes()).hexdigest() for f in deps},
        "actual_paired_source_controls": controls,
        "growing_root_local_move_ledgers": [paired_collision_ledger(n, n, n*n+12, (n+1).bit_length()) for n in (8, 32, 64, 128)],
        "offset_chart_joint_law_is_IID": False,
        "research_decision": "DEPRIORITIZE_EXACT_SMALL_MOVE_GROUND_TEST; SEARCH_COSTED_COLLECTIVE_MACROS_OR_OTHER_ENSEMBLE_EFFECTS",
        "all_efficient_span_tests_excluded": False,
        "accepted_speedup_candidate": False, "new_active_negative_result_created": False,
        "remaining_obligations": ["constructive collective/nonlocal mechanism without granted fibre oracle",
            "external proof review", "precision/source audit of any future coherent walk", "production integration"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__);parser.add_argument("--write", action="store_true")
    args = parser.parse_args();report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True);REPORT.write_text(json.dumps(exact_json(report), indent=2)+"\n")
    print(json.dumps({"status": report["status"], "controls": [{"ground_rank": c["ground_rank"], "span_rank": c["full_fibre_span_rank"],
        "ground_null": c["exact_ground_IID_null_acceptance"], "source_bound_legal": c["full_root_source_moment_bound_applicable"]}
        for c in report["actual_paired_source_controls"]], "efficient_ground_effect_supplied": False}, indent=2))


if __name__ == "__main__": main()
