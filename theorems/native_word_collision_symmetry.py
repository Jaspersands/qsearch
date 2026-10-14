"""Costed two-word collision/swap observable on known original-data preparations.

All branches are retained. A large conditional signal is not a free collision
sampler, nor is one-pass classical readout simulation a general quantum no-go.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
from itertools import product
import json
from math import isqrt
from pathlib import Path

import numpy as np

from native_full_root_slice import source_data
from native_word_spectral_filter_audit import finite_control
from native_word_span_decision import root_polynomial
from native_small_multiple_completion import _rational
from ternary_measured_lattice_decoder import exact_json, integer

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/NATIVE_WORD_COLLISION_SYMMETRY.md"
REPORT = ROOT / "research/reductions/native_word_collision_symmetry.json"


def combine_root(polynomial, q, constant, multiplier):
    asc = list(map(Fraction, reversed(polynomial)))
    coefficients = [Fraction(0)] * q
    for j, c in enumerate(asc):
        coefficients[j] = multiplier * c
    coefficients[0] += constant
    return root_polynomial(coefficients, q)


def literal_branches(rows, q):
    D = len(rows)
    if D > 256:
        raise ValueError("whole two-word reference state cap exceeded")
    psi = np.exp(2j * np.pi * np.asarray([row["known_phase"] for row in rows]) / q) / np.sqrt(D)
    initial = np.outer(psi, np.ones(D) / np.sqrt(D))
    # Literal H--controlled SWAP--H on the two actual word registers.
    plus, minus = (initial + initial.T) / 2, (initial - initial.T) / 2
    equal = np.asarray([[a["frequency"] == b["frequency"] for b in rows] for a in rows])
    return {
        "equal_plus": float(np.sum(abs(plus[equal]) ** 2)),
        "equal_minus": float(np.sum(abs(minus[equal]) ** 2)),
        "unequal_plus": float(np.sum(abs(plus[~equal]) ** 2)),
        "unequal_minus": float(np.sum(abs(minus[~equal]) ** 2)),
        "complete_mass": float(np.sum(abs(plus) ** 2) + np.sum(abs(minus) ** 2)),
        "whole_joint_amplitudes_evaluated": 2 * D * D,
        "branch_discarded_for_free": False,
    }


def control(raw, mask):
    base = finite_control(raw, mask, (("GEOMETRIC", 1),))
    D, q = base["word_dimension"], raw[0].modulus
    collision = Fraction(base["collision_probability"])
    raw_filter = base["spectral_filter_controls"][0]
    raw_acceptance = raw_filter["exact_source_acceptance_root_polynomial"]
    branches = literal_branches(base["actual_native_word_rows"], q)
    raw_float = raw_filter["diagnostic_source_acceptance_probability"]
    if abs(branches["equal_plus"] - (float(collision) + raw_float) / 2) > 1e-10 or abs(branches["equal_minus"] - (float(collision) - raw_float) / 2) > 1e-10:
        raise ArithmeticError("literal joint circuit disagrees with collision/swap effect")
    return {
        "native_spectral_reference": base, "literal_joint_branches": branches,
        "exact_equal_plus_root_polynomial": combine_root(raw_acceptance, q, collision / 2, Fraction(1, 2)),
        "exact_equal_minus_root_polynomial": combine_root(raw_acceptance, q, collision / 2, Fraction(-1, 2)),
        "exact_equal_total_probability": str(collision),
        "IID_null_equal_plus_probability": str((collision + Fraction(1, D)) / 2),
        "IID_null_equal_minus_probability": str((collision - Fraction(1, D)) / 2),
        "effective_original_word_effect_commutes_with_raw_Gram": True,
        "phase_independent_diagonal_term_cancels_source_vs_IID_null": True,
        "classical_full_measured_readout_identity": {
            "word_pair_probability": str(Fraction(1, D * D)),
            "conditional_plus_probability": "(1+cos(2*pi*(phase_w-phase_v)/q))/2",
            "conditional_minus_probability": "(1-cos(2*pi*(phase_w-phase_v)/q))/2",
            "predicate": "f_A(w)==f_A(v)",
            "original_phase_evaluator_and_frequency_work_paid": True,
            "entire_measured_word_pair_and_flag_law_matched": True,
            "finite_precision_classical_sampler_implemented_here": False,
            "coherent_amplification_or_retained_unmeasured_output_simulated": False,
        },
        "scalable_logical_recipe": {
            "original_records_paid_once": len(raw), "uniform_qutrits": 2 * len(raw) // 2,
            "original_response_phase_gates": len(raw) // 2,
            "controlled_qutrit_swaps": len(raw) // 2,
            "forward_and_uncompute_label_coordinate_accumulations": 4 * (len(raw) // 2) * len(raw[0].label),
            "frequency_comparison_coordinates": len(raw[0].label),
            "known_initial_preparation_inverse_available_on_this_source": True,
            "normalized_fibre_preparation_required_by_one_pass": False,
            "full_word_table_required_by_logical_recipe": False,
            "physical_gate_compilation_and_precision_certified": False,
        },
        "accepted_speedup_candidate": False,
    }


def ensemble_ledger(n, r, surplus, normalized_error_second_moment, target_equal_mass="1/2"):
    for x in (n, r, surplus):
        integer(x, "positive ensemble scope", 1)
    if n * r > 4096:
        raise ValueError("exact conditional probability certificate bit cap exceeded")
    V = _rational(normalized_error_second_moment)
    target = _rational(target_equal_mass)
    if V < 0 or not 0 < target <= 1:
        raise ValueError("valid true source moment and target mass required")
    N, D, M = 3 ** (n * r), 3 ** (n * r + surplus), n * r + surplus
    den = 1 + Fraction(N - 1, D)
    mean_equal = den / N
    loss = min(Fraction(1), 80 * M * V)
    source_anti = min(Fraction(1, 2), loss / (2 * den))
    null_anti = (1 - Fraction(1, D)) / (2 * den)
    squared = target / mean_equal
    d = isqrt(squared.numerator // squared.denominator)
    if d * d * squared.denominator < squared.numerator:
        d += 1
    return {
        "dimension": n, "root_digits": r, "word_surplus": surplus, "word_sites": M,
        "true_original_error_second_moment_over_q_squared_upper": str(V),
        "mean_equality_probability": str(mean_equal),
        "conditional_IID_null_antisymmetric_probability": str(null_anti),
        "conditional_source_antisymmetric_probability_upper": str(source_anti),
        "conditional_antisymmetric_gap_lower": str(max(Fraction(0), null_anti - source_anti)),
        "target_mean_amplified_equality_probability": str(target),
        "necessary_standard_amplification_iterations_lower": d // 2,
        "original_errors_independent_of_full_root_original_labels_required": True,
        "IID_uniform_full_root_original_labels_and_IID_uniform_null_values_required": True,
        "conditional_bounds_are_unamplified_source_and_branch_ensemble_bounds": True,
        "amplified_ensemble_source_gap_certified": False,
        "generic_trace_error_safe_after_rare_branch_conditioning": False,
        "arbitrary_nonstandard_quantum_algorithm_lower_bound": False,
    }


def label_noise_census(label_dependent_errors=False):
    """Complete real mod3 source census; truth only generates calibrations."""
    words = tuple(product(range(3), repeat=2))
    beta = tuple(tuple(c for t in w for c in ((1, 0), (-1, 1), (0, -1))[t]) for w in words)
    total_collision = total_raw = total_error_fidelity = Fraction(0)
    for labels in product(range(3), repeat=4):
        errors = tuple(-a for a in labels) if label_dependent_errors else (1, 0, 0, 0)
        values = tuple((a + e) % 3 for a, e in zip(labels, errors))
        frequencies = tuple(sum(b * a for b, a in zip(v, labels)) % 3 for v in beta)
        phases = tuple(sum(b * y for b, y in zip(v, values)) % 3 for v in beta)
        error_phases = tuple(sum(b * e for b, e in zip(v, errors)) % 3 for v in beta)
        for i in range(9):
            for j in range(9):
                cosine = Fraction(1) if (phases[j] - phases[i]) % 3 == 0 else Fraction(-1, 2)
                err_cosine = Fraction(1) if (error_phases[j] - error_phases[i]) % 3 == 0 else Fraction(-1, 2)
                total_error_fidelity += err_cosine / 81
                if frequencies[i] == frequencies[j]:
                    total_collision += Fraction(1, 81)
                    total_raw += cosine / 81
    C, R, f = total_collision / 81, total_raw / 81, total_error_fidelity / 81
    return {
        "complete_original_label_banks": 81, "words_per_bank": 9,
        "original_secret_USED_ONLY_TO_GENERATE_CONTROL": 1,
        "original_error_recipe": "e_i=-a_i" if label_dependent_errors else "(1,0,0,0)",
        "errors_independent_of_labels": not label_dependent_errors,
        "exact_mean_collision": str(C), "exact_mean_raw_acceptance": str(R),
        "exact_mean_error_fidelity": str(f), "exact_mean_C_minus_R": str(C - R),
        "one_over_N_times_mean_one_minus_error_fidelity": str((1 - f) / 3),
        "independent_error_averaging_identity_holds": C - R == (1 - f) / 3,
        "is_hard_source_or_algorithm_candidate": False,
    }


def build_report():
    controls = []
    for args in ((1, 1, 3, False, 99001), (1, 2, 4, False, 99002), (1, 3, 5, True, 99003), (2, 1, 3, False, 99004)):
        raw, mask, _, _ = source_data(*args)
        controls.append(control(raw, mask))
    deps = ("native_word_spectral_filter_audit.py", "native_word_span_decision.py", "native_full_root_slice.py",
            "native_small_multiple_completion.py", "ternary_measured_lattice_decoder.py")
    return {
        "status": "ACTUAL_TWO_WORD_COLLISION_SYMMETRY_REFERENCE_MEASURED_LAW_CLASSICAL_RARE_BRANCH_PAID",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
        "dependency_sha256": {f: hashlib.sha256((ROOT / "theorems" / f).read_bytes()).hexdigest() for f in deps},
        "actual_source_controls": tuple(controls),
        "independent_error_label_census": label_noise_census(),
        "label_dependent_error_countercensus": label_noise_census(True),
        "scaling_ensemble_ledgers": tuple(ensemble_ledger(n, n, 12, Fraction(1, 3 * n ** 6) + Fraction(1, 2 * 3 ** (2 * n))) for n in (8, 32, 64)),
        "accepted_speedup_candidate": False, "new_active_negative_result_created": False,
        "research_decision": "KEEP_AS_CONSTRUCTIVE_COLLECTIVE_BASELINE_NOT_A_NEW_SPEEDUP_OR_FREE_FIBRE_NORMALIZER",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.write_text(json.dumps(exact_json(report), indent=2) + "\n")
    print(json.dumps({"status": report["status"],
        "complete_masses": [c["literal_joint_branches"]["complete_mass"] for c in report["actual_source_controls"]],
        "diagnostic_conditional_gaps": [float(Fraction(p["conditional_antisymmetric_gap_lower"])) for p in report["scaling_ensemble_ledgers"]],
        "efficient_quantum_speedup_claimed": False}, indent=2))


if __name__ == "__main__":
    main()
