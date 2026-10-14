"""Bounded raw-frame spectral filters: exact controls and a scoped degree price.

Not a lower bound on arbitrary quantum algorithms or data-dependent effects.
No efficient normalized fibre access is granted by this diagnostic.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
import hashlib
from itertools import product
import json
from math import comb, cos, isqrt, pi
from pathlib import Path

from native_basis_lottery import original_bank
from native_full_root_slice import source_data
from native_small_multiple_completion import _rational
from native_word_span_decision import root_polynomial
from ternary_measured_lattice_decoder import exact_json, integer
from ternary_noise_degradation import NoisyLinearRecord

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/NATIVE_WORD_SPECTRAL_FILTER_AUDIT.md"
REPORT = ROOT / "research/reductions/native_word_spectral_filter_audit.json"


def polynomial_value(coefficients, x):
    x = _rational(x)
    value = Fraction(0)
    for c in reversed(coefficients):
        value = value * x + _rational(c)
    return value


def certified_filter(family, degree):
    integer(degree, "nonnegative filter degree")
    if degree > 32:
        raise ValueError("whole finite polynomial construction cap exceeded")
    if family == "GEOMETRIC" and degree >= 1:
        coefficients = (Fraction(0),) + tuple(Fraction((-1) ** (j + 1) * comb(degree, j)) for j in range(1, degree + 1))
        reason = "1-(1-x)^d belongs to [0,1] on [0,1]"
    elif family == "CHEBYSHEV_ENDPOINT" and degree >= 1:
        prev, cur = [Fraction(1)], [Fraction(-1), Fraction(2)]
        for _ in range(1, degree):
            nxt = [Fraction(0)] * (len(cur) + 1)
            for i, c in enumerate(cur):
                nxt[i] -= 2 * c
                nxt[i + 1] += 4 * c
            for i, c in enumerate(prev):
                nxt[i] -= c
            prev, cur = cur, nxt
        coefficients = tuple(-Fraction((-1) ** degree, 2) * c for c in cur)
        coefficients = (coefficients[0] + Fraction(1, 2),) + coefficients[1:]
        reason = "(1-(-1)^d*T_d(2x-1))/2 belongs to [0,1] on [0,1]"
    elif family == "NONZERO_KERNEL_BIAS" and degree == 1:
        coefficients = (Fraction(1, 3), Fraction(2, 3))
        reason = "1/3+2*x/3 belongs to [0,1] on [0,1]"
    elif family == "CONSTANT" and degree == 0:
        coefficients = (Fraction(1, 3),)
        reason = "constant 1/3"
    else:
        raise ValueError("analytically globally bounded filter family required")
    return {
        "family": family, "degree": degree, "ascending_coefficients": tuple(str(c) for c in coefficients),
        "global_effect_range": "[0,1] on ALL x in [0,1]", "global_range_certificate": reason,
        "polynomial_selected_independently_of_original_values": True,
        "filter_physical_QSVT_implementation_supplied": False,
    }


def finite_control(records, mask, specs):
    raw = original_bank(records)
    q, n = raw[0].modulus, len(raw[0].label)
    if len(raw) % 2 or q > 81 or 3 ** (len(raw) // 2) > 256:
        raise ValueError("complete finite native paired-word diagnostic cap exceeded")
    mask = tuple(mask)
    if len(mask) != n or any(type(x) is not int or not 0 <= x < q for x in mask):
        raise ValueError("canonical known mask required")
    sites = len(raw) // 2
    rows, groups = [], defaultdict(list)
    for word in product(range(3), repeat=sites):
        frequency, phase = [0] * n, 0
        for j, t in enumerate(word):
            left, right = raw[2 * j:2 * j + 2]
            ca, cc = ((1, 0), (-1, 1), (0, -1))[t]
            frequency = [(s + ca * a + cc * c) % q for s, a, c in zip(frequency, left.label, right.label)]
            y1 = left.value + sum(a * z for a, z in zip(left.label, mask))
            y2 = right.value + sum(a * z for a, z in zip(right.label, mask))
            phase = (phase + ca * y1 + cc * y2) % q
        row = {"word": word, "frequency": tuple(frequency), "known_phase": phase}
        rows.append(row)
        groups[tuple(frequency)].append(phase)
    D = len(rows)
    collision = sum(Fraction(len(phases) ** 2, D * D) for phases in groups.values())
    filters = []
    for family, degree in specs:
        spec = certified_filter(family, degree)
        coefficients = spec["ascending_coefficients"]
        p0 = polynomial_value(coefficients, 0)
        weights = [Fraction(0)] * q
        weights[0] = p0
        null = p0
        ideal = Fraction(0)
        for phases in groups.values():
            count = len(phases)
            p = Fraction(count, D)
            value = polynomial_value(coefficients, p)
            null += (value - p0) / D
            ideal += p * value
            weight = (value - p0) / (D * count)
            for a in phases:
                for b in phases:
                    weights[(b - a) % q] += weight
        gap_weights = weights.copy()
        gap_weights[0] -= null
        probability = sum(float(c) * cos(2 * pi * j / q) for j, c in enumerate(weights))
        bound = min(Fraction(1), degree * degree * (collision + Fraction(1, D)))
        if abs(probability - float(null)) > float(bound) + 1e-9:
            raise ArithmeticError("native spectral gap violates scoped Markov bound")
        filters.append({
            "filter": spec, "exact_source_acceptance_root_polynomial": root_polynomial(weights, q),
            "exact_source_minus_IID_null_root_polynomial": root_polynomial(gap_weights, q),
            "IID_null_acceptance": str(null), "ideal_source_acceptance_IF_codeword": str(ideal),
            "absolute_source_null_gap_upper": str(bound),
            "diagnostic_source_acceptance_probability": probability,
            "matched_classical_monomial_estimator": {
                "coefficient_l1_norm": str(sum(abs(_rational(c)) for c in coefficients)),
                "maximum_words_per_monomial_shot": degree + 1,
                "identity": "E[all k+1 frequencies equal * exp(i*(phase_last-phase_first))] = <psi,K^k psi> for k>=1",
                "coefficient_norm_and_inverse_precision_are_not_free": True,
                "polynomial_time_classical_dequantization_established": False,
            },
        })
    return {
        "original_records": tuple(row.public() for row in raw), "known_mask": mask,
        "actual_native_word_rows": tuple(rows), "word_dimension": D,
        "supported_frequency_count": len(groups), "collision_probability": str(collision),
        "spectral_filter_controls": tuple(filters), "dense_control_is_scalable_circuit": False,
        "IID_label_source_law_established_by_this_fixture": False,
    }


def degree_ledger(n, r, surplus, gap="1/4", effect_error="0", preparation_error="0"):
    for x, name in ((n, "dimension"), (r, "root digits"), (surplus, "word surplus")):
        integer(x, "positive " + name, 1)
    if n * r > 16384:
        raise ValueError("exact scalable degree certificate bit scope exceeded")
    gamma, eps, delta = map(_rational, (gap, effect_error, preparation_error))
    if not 0 < gamma <= 1 or not all(0 <= x <= 1 for x in (eps, delta)):
        raise ValueError("valid required gap and two-ensemble implementation losses")
    residual = max(Fraction(0), gamma - 2 * eps - 2 * delta)
    factor = 1 + Fraction(2, 3 ** surplus)
    squared = residual * 3 ** (n * r) / factor
    degree = isqrt(squared.numerator // squared.denominator)
    if degree * degree * squared.denominator < squared.numerator:
        degree += 1
    return {
        "dimension": n, "root_digits": r, "word_sites": n * r + surplus,
        "frequency_population_base3_exponent": n * r, "word_surplus": surplus,
        "required_decision_gap": str(gamma), "uniform_effect_error_each_ensemble": str(eps),
        "preparation_trace_error_each_ensemble": str(delta), "residual_exact_filter_gap_required": str(residual),
        "expected_collision_plus_inverse_word_dimension_upper": {
            "coefficient": str(factor), "base": 3, "exponent": -n * r,
        },
        "minimum_acceptance_polynomial_degree_under_scoped_model": degree,
        "degree_lower_bound_bit_length": degree.bit_length(),
        "label_only_globally_bounded_raw_Gram_filter_required": True,
        "IID_full_root_original_labels_and_IID_uniform_null_values_required": True,
        "arbitrary_original_source_phase_noise_is_allowed_in_upper_bound": True,
        "balanced_fibres_or_per_matrix_uniformity_assumed": False,
        "mask_may_depend_on_original_values_IF_fibre_constant": True,
        "coefficients_may_depend_on_original_values": False,
        "degree_bound_is_a_general_quantum_query_lower_bound": False,
        "efficient_different_preconditioner_or_noncommuting_measurement_excluded": False,
        "actual_quantum_decision_algorithm_supplied": False,
    }


def collision_census(n, r, sites, max_work=10000):
    for x in (n, r, sites, max_work):
        integer(x, "positive complete census parameter", 1)
    q, D = 3 ** r, 3 ** sites
    banks = q ** (2 * sites * n)
    work = banks * D * sites * n
    if work > max_work:
        raise ValueError("whole source-label/word census cap exceeded")
    total = Fraction(0)
    words = tuple(product(range(3), repeat=sites))
    for labels in product(range(q), repeat=2 * sites * n):
        counts = defaultdict(int)
        for word in words:
            frequency = [0] * n
            for j, t in enumerate(word):
                a, c = ((1, 0), (-1, 1), (0, -1))[t]
                for i in range(n):
                    frequency[i] = (frequency[i] + a * labels[2 * j * n + i] + c * labels[(2 * j + 1) * n + i]) % q
            counts[tuple(frequency)] += 1
        total += sum(Fraction(c * c, D * D) for c in counts.values())
    mean = total / banks
    theoretical = Fraction(1, q ** n) + (1 - Fraction(1, q ** n)) / D
    if mean != theoretical:
        raise ArithmeticError("exact label-source collision identity failed")
    return {"dimension": n, "root_digits": r, "word_sites": sites,
            "complete_original_label_banks": banks, "complete_coordinate_accumulation_terms": work,
            "exact_mean_collision_probability": str(mean), "theoretical_collision_probability": str(theoretical),
            "census_is_new_oracle_problem_or_algorithm_candidate": False}


def build_report():
    specs = (("CONSTANT", 0), ("NONZERO_KERNEL_BIAS", 1)) + tuple(
        (family, d) for family in ("GEOMETRIC", "CHEBYSHEV_ENDPOINT") for d in (1, 2, 4, 8))
    controls = []
    for n, r, sites, noisy, seed in ((1, 1, 3, False, 99001), (1, 2, 4, False, 99002),
                                    (1, 3, 5, True, 99003), (2, 1, 3, False, 99004)):
        raw, mask, _, _ = source_data(n, r, sites, noisy, seed)
        controls.append(finite_control(raw, mask, specs))
    concentrated = tuple(NoisyLinearRecord((0,), 0, 3, f"spectral-concentrated:{j}") for j in range(4))
    deps = ("native_basis_lottery.py", "native_full_root_slice.py", "native_word_span_decision.py",
            "native_small_multiple_completion.py", "ternary_measured_lattice_decoder.py", "ternary_noise_degradation.py")
    return {
        "status": "RAW_WORD_GRAM_BOUNDED_SPECTRAL_FILTER_DEGREE_AND_ENSEMBLE_SCOPE_AUDIT",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
        "dependency_sha256": {f: hashlib.sha256((ROOT / "theorems" / f).read_bytes()).hexdigest() for f in deps},
        "actual_native_source_controls": tuple(controls),
        "complete_label_source_collision_censuses": tuple(collision_census(*args) for args in ((1, 1, 2), (1, 2, 1), (2, 1, 1))),
        "scaling_degree_ledgers": tuple(degree_ledger(n, n, 12, effect_error="1/64", preparation_error="1/64") for n in (8, 32, 64, 128)),
        "concentrated_labels_countercontrol": finite_control(concentrated, (0,), (("GEOMETRIC", 1),)),
        "unbounded_rescaling_countercontrol": {
            "balanced_supported_eigenvalue": "1/81", "candidate_degree1_polynomial": "81*x",
            "value_at_supported_eigenvalue": "1", "value_at_x1": "81",
            "valid_globally_bounded_filter": False, "cheap_normalized_block_encoding_supplied": False,
        },
        "data_dependent_coefficients_countercontrol": {
            "effect": "P_y(x)=1 if ALL original values are0, else0",
            "polynomial_degree": 0, "fixed_zero_secret_noiseless_calibration_acceptance": "1",
            "IID_uniform_null_acceptance_with4_original_values_mod3": "1/81",
            "original_values_enter_effect_selection": True, "label_only_filter_model_applies": False,
            "is_hard_source_or_algorithm_candidate": False,
        },
        "accepted_speedup_candidate": False, "new_active_negative_result_created": False,
        "all_quantum_measurements_or_preconditioners_excluded": False,
        "research_decision": "DO_NOT_TREAT_RAW_FRAME_QSVT_AS_FREE_NORMALIZATION_SEARCH_STRUCTURAL_PRECONDITIONERS_OR_NONCOMMUTING_TESTS",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.write_text(json.dumps(exact_json(report), indent=2) + "\n")
    print(json.dumps({"status": report["status"],
        "native_controls": len(report["actual_native_source_controls"]),
        "minimum_degree_bit_lengths": [p["degree_lower_bound_bit_length"] for p in report["scaling_degree_ledgers"]],
        "universal_quantum_no_go": False, "actual_quantum_algorithm_supplied": False}, indent=2))


if __name__ == "__main__":
    main()
