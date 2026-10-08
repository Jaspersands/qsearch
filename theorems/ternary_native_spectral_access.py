"""Source-native access audit for proposed secret-phase spectral generators.

LOCAL DERIVATION / REVIEW PENDING. A restricted nondemolition-generator
boundary, not a lower bound against collective receivers or a speedup.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import product
import json
import math
from pathlib import Path

import numpy as np

from cyclotomic_fiber_receiver import inverse_frequency_coordinates, native_source
from ternary_covariant_noise import phase, root_digits
from ternary_cyclic_extractor import random_even_source

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/TERNARY_NATIVE_SPECTRAL_ACCESS.md"
REPORT = ROOT / "research/phase_workbench/ternary_native_spectral_access.json"


def _integer(value, name, minimum=1):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} requires an integer >= {minimum}")
    return value


def _offset(value, n, q):
    value = tuple(value)
    if len(value) != n or any(type(x) is not int or not 0 <= x < q for x in value):
        raise ValueError("full-root canonical fixed frequency offset required")
    return value


def sqrt_integer_interval(value, bits=40):
    _integer(value, "integer square-root argument", 0)
    _integer(bits, "square-root precision bits")
    scale = 1 << bits
    lower = math.isqrt(value*scale*scale)
    upper = lower if lower*lower == value*scale*scale else lower+1
    return Fraction(lower, scale), Fraction(upper, scale)


def bounded_fibers(source, max_words=4096, max_group=4096):
    _integer(max_words, "whole word-table cap")
    _integer(max_group, "whole frequency-group cap")
    if 3**source.inputs > max_words or source.modulus**source.dimension > max_group:
        raise ValueError("complete native calibration table exceeds cap; no partial certificate")
    words = tuple(product(range(3), repeat=source.inputs))
    values = tuple(source.value(word) for word in words)
    group = tuple(product(range(source.modulus), repeat=source.dimension))
    counts = Counter(values)
    return words, values, group, counts


def translation_certificate(counts, group, d, q, bits=40):
    root_digits(q)
    if not group:
        raise ValueError("nonempty complete retained-root group required")
    n = len(group[0])
    d = _offset(d, n, q)
    D = sum(counts.values())
    if D < 1 or any(type(c) is not int or c < 0 for c in counts.values()):
        raise ValueError("exact nonnegative native fiber counts required")
    if len(group) != q**n or set(group) != set(product(range(q), repeat=n)) or not set(counts).issubset(group):
        raise ValueError("complete retained-root group required")
    terms = []
    lower = upper = Fraction(0)
    matched = edge_pairs = 0
    for y in group:
        z = tuple((a+b) % q for a, b in zip(y, d))
        a, b = counts.get(y, 0), counts.get(z, 0)
        if a*b:
            lo, hi = sqrt_integer_interval(a*b, bits)
            terms.append({"source_frequency": y, "target_frequency": z,
                          "source_fiber_count": a, "target_fiber_count": b,
                          "sqrt_product_lower": str(lo), "sqrt_product_upper": str(hi)})
            lower += lo/D
            upper += hi/D
        matched += min(a, b)
        edge_pairs += a*b
    exact_permutation = matched == D
    return {"fixed_frequency_offset": d, "native_words": D,
            "all_nonzero_radical_terms": terms, "sqrt_interval_bits": bits,
            "optimal_arbitrary_public_unitary_mean_overlap_lower": str(lower),
            "optimal_arbitrary_public_unitary_mean_overlap_upper": str(min(Fraction(1), upper)),
            "optimal_public_permutation_mean_overlap_exact": str(Fraction(matched, D)),
            "minimum_arbitrary_unitary_mean_squared_phase_error_lower": str(max(Fraction(0), 2-2*upper)),
            "minimum_arbitrary_unitary_mean_squared_phase_error_upper": str(2-2*lower),
            "ordered_frequency_shift_pair_count": edge_pairs,
            "integer_collision_overlap_upper": str(min(Fraction(1), Fraction(edge_pairs, D))),
            "exact_frequency_translation_permutation_exists": exact_permutation,
            "unitary_optimized_without_cost_or_q_order_constraints": True,
            "full_secret_recovery_or_general_receiver_lower_bound": False,
            "efficient_fiber_transform_supplied": False}


def fixed_offset_population_bound(n, q, inputs):
    _integer(n, "native dimension")
    root_digits(q)
    _integer(inputs, "original source inputs")
    D, G = 3**inputs, q**n
    overlap = min(Fraction(1), Fraction(D-1, G))
    dense_error = min(Fraction(2), Fraction(4*(G-1), D))
    return {"dimension": n, "modulus": str(q), "original_source_qutrits": inputs,
            "native_word_dimension": str(D), "full_frequency_group": str(G),
            "mean_optimal_arbitrary_unitary_phase_overlap_upper": str(overlap),
            "mean_minimum_squared_nondemolition_phase_error_lower": str(2*(1-overlap)),
            "mean_minimum_squared_nondemolition_phase_error_upper": str(dense_error),
            "expected_chi_squared_frequency_nonuniformity_exact": str(Fraction(G-1, D)),
            "offset_must_be_fixed_nonzero_before_random_labels": True,
            "public_unitary_may_depend_on_all_labels": True,
            "requires_all_IID_uniform_full_native_frequency_rows": True,
            "scope": "ONE_PUBLIC_UNITARY_APPROXIMATING_KNOWN_CHARACTER_PHASE_ON_UNALTERED_NATIVE_STATE",
            "general_receiver_lower_bound": False, "efficient_unitary_construction_supplied": False}


def complete_permutation(values, d, q):
    """Exponential calibration: maximize exact frequency-shift word matches."""
    by_frequency = {}
    for i, y in enumerate(values):
        by_frequency.setdefault(y, []).append(i)
    result = [None]*len(values)
    used = set()
    for y, indices in by_frequency.items():
        z = tuple((a+b) % q for a, b in zip(y, d))
        for i, j in zip(indices, by_frequency.get(z, [])):
            result[i] = j
            used.add(j)
    available = iter(i for i in range(len(values)) if i not in used)
    for i in range(len(result)):
        if result[i] is None:
            result[i] = next(available)
    if sorted(result) != list(range(len(values))):
        raise ArithmeticError("reference translation is not a complete word permutation")
    return tuple(result)


def dense_optimal_unitary(values, group, d, q):
    """Reference-only partial frequency shift plus orthonormal completion."""
    D = len(values)
    fibers = {y: [i for i, v in enumerate(values) if v == y] for y in group}
    basis, index = [], {}
    for y, indices in fibers.items():
        if not indices:
            continue
        uniform = np.zeros(D, dtype=complex)
        uniform[indices] = 1/math.sqrt(len(indices))
        index[y] = len(basis)
        basis.append(uniform)
    # The Householder basis within each fiber is reproducible and complete.
    for indices in fibers.values():
        if len(indices) < 2:
            continue
        k = len(indices)
        v = np.zeros(k); v[0] = 1
        v -= np.ones(k)/math.sqrt(k)
        H = np.eye(k)-2*np.outer(v,v)/(v@v)
        for j in range(1, k):
            column = np.zeros(D, dtype=complex)
            column[indices] = H[:, j]
            basis.append(column)
    B = np.column_stack(basis)
    image = [None]*D
    used = set()
    for y, i in index.items():
        z = tuple((a+b) % q for a, b in zip(y, d))
        if z in index:
            image[i] = index[z]
            used.add(index[z])
    remaining = iter(j for j in range(D) if j not in used)
    for i in range(D):
        if image[i] is None:
            image[i] = next(remaining)
    U = B[:, image]@B.conj().T
    return U


def dense_phase_error(U, values, group, d, q):
    errors = []
    for secret in group:
        psi = np.array([phase(sum(a*s for a, s in zip(y, secret)), q) for y in values])/math.sqrt(len(values))
        target = phase(-sum(a*s for a, s in zip(d, secret)), q)*psi
        errors.append(float(np.linalg.norm(U@psi-target)**2))
    return sum(errors)/len(errors)


def calibration(n, q, inputs, seed):
    source = random_even_source(n, 2*root_digits(q), inputs, seed)
    words, values, group, counts = bounded_fibers(source)
    offsets = [tuple(1 if i == j else 0 for i in range(n)) for j in range(n)]
    offsets += [tuple(q//3 if i == j else 0 for i in range(n)) for j in range(n)] if q > 3 else []
    offsets = list(dict.fromkeys(offsets))
    translations = []
    for d in offsets:
        cert = translation_certificate(counts, group, d, q)
        permutation = complete_permutation(values, d, q)
        matched = sum(tuple((a+b) % q for a, b in zip(values[i], d)) == values[j] for i, j in enumerate(permutation))
        if Fraction(matched, len(values)) != Fraction(cert["optimal_public_permutation_mean_overlap_exact"]):
            raise ArithmeticError("permutation reference fails the exact matching optimum")
        U = dense_optimal_unitary(values, group, d, q)
        error = dense_phase_error(U, values, group, d, q)
        defect = float(np.linalg.norm(U.conj().T@U-np.eye(len(values)), ord=2))
        lo, hi = (float(Fraction(cert[key])) for key in ("minimum_arbitrary_unitary_mean_squared_phase_error_lower", "minimum_arbitrary_unitary_mean_squared_phase_error_upper"))
        if defect > 1e-10 or not lo-1e-10 <= error <= hi+1e-10:
            raise ArithmeticError("dense reference fails the exact radical envelope")
        translations.append({"certificate": cert, "reference_word_permutation": permutation,
                             "reference_matched_word_count": matched,
                             "dense_arbitrary_unitary_mean_squared_phase_error": error,
                             "dense_unitarity_operator_norm_defect": defect,
                             "floating_reference_is_exact_proof": False,
                             "dense_reference_is_efficient_compiler": False})
    # Source-native diagonal operators always commute with ALL secret encodings.
    diagonal = np.diag([phase((i*i+2*i) % q, q) for i in range(len(values))])
    probabilities = []
    for secret in group:
        psi = np.array([phase(sum(a*s for a, s in zip(y, secret)), q) for y in values])/math.sqrt(len(values))
        probabilities.append(np.abs(diagonal@psi)**2)
    if max(float(np.max(np.abs(p-probabilities[0]))) for p in probabilities) > 1e-12:
        raise ArithmeticError("commuting diagonal control spuriously changed native secret information")
    return {"seed": seed, "dimension": n, "modulus": q, "source_inputs": inputs,
            "native_level": source.level, "original_ring_labels": source.labels,
            "native_frequencies": source.frequencies, "complete_words": words,
            "complete_frequency_values": values,
            "complete_fiber_counts": [{"frequency": y, "count": counts.get(y, 0)} for y in group],
            "translations": translations,
            "diagonal_computational_readout_secret_independent": True,
            "commutant_projective_readout_information_exact": "0",
            "source_has_IID_population_law_from_calibration_seed": False}


def adaptive_offset_countercontrol():
    source = random_even_source(1, 6, 1, 89815)
    words, values, group, counts = bounded_fibers(source)
    d = next(tuple((b-a) % source.modulus for a, b in zip(values[0], y))
             for y in values[1:] if y != values[0])
    cert = translation_certificate(counts, group, d, source.modulus)
    fixed = fixed_offset_population_bound(1, source.modulus, 1)
    if Fraction(cert["optimal_arbitrary_public_unitary_mean_overlap_lower"]) <= Fraction(fixed["mean_optimal_arbitrary_unitary_phase_overlap_upper"]):
        raise ArithmeticError("adaptive-offset countercontrol did not expose the missing independence")
    return {"seed": 89815, "native_level": 6, "original_ring_labels": source.labels,
            "native_frequencies": source.frequencies, "complete_words": words, "complete_frequency_values": values,
            "certificate": cert, "fixed_offset_population_ledger": fixed,
            "offset_was_chosen_from_labels": True,
            "fixed_offset_population_bound_applies_to_this_selected_offset": False,
            "one_instance_is_an_ensemble_refutation": False}


def population_reference(q, inputs, max_label_matrices=128):
    root_digits(q)
    _integer(inputs, "native population inputs")
    _integer(max_label_matrices, "whole native population cap")
    total = q**(2*inputs)
    if total > max_label_matrices:
        raise ValueError("complete label ensemble exceeds cap; no partial population assertion")
    edge_mean = chi2_mean = lower = upper = Fraction(0)
    for flat in product(range(q), repeat=2*inputs):
        labels = tuple((inverse_frequency_coordinates(flat[2*i], flat[2*i+1], 2*root_digits(q)),)
                       for i in range(inputs))
        source = native_source(labels, 2*root_digits(q))
        _, _, group, counts = bounded_fibers(source)
        cert = translation_certificate(counts, group, (1,), q)
        D = 3**inputs
        edge_mean += Fraction(cert["ordered_frequency_shift_pair_count"], D*total)
        chi2_mean += Fraction(q*sum(c*c for c in counts.values()), D*D*total)-Fraction(1, total)
        lower += Fraction(cert["optimal_arbitrary_public_unitary_mean_overlap_lower"])/total
        upper += Fraction(cert["optimal_arbitrary_public_unitary_mean_overlap_upper"])/total
    ledger = fixed_offset_population_bound(1, q, inputs)
    if edge_mean != Fraction(3**inputs-1, q) or chi2_mean != Fraction(q-1, 3**inputs):
        raise ArithmeticError("native complete population violates the exact ordered-pair law")
    if lower > Fraction(ledger["mean_optimal_arbitrary_unitary_phase_overlap_upper"]):
        raise ArithmeticError("exact mean unitary overlap exceeds the fixed-offset envelope")
    return {"dimension": 1, "modulus": q, "original_source_inputs": inputs,
            "entire_native_label_matrices_checked": total, "fixed_offset": (1,),
            "mean_ordered_pair_over_word_dimension_exact": str(edge_mean),
            "mean_frequency_chi_squared_exact": str(chi2_mean),
            "mean_optimal_unitary_overlap_lower": str(lower), "mean_optimal_unitary_overlap_upper": str(upper),
            "complete_native_chart_replayed": True, "finite_population_check_is_asymptotic_proof": False}


def run_controls():
    specs = ((2, 9, 2, 89811), (3, 3, 1, 89813), (1, 9, 3, 89821), (1, 3, 3, 89823))
    return {"status": "NATIVE_NONDEMOLITION_SPECTRAL_ACCESS_BOUNDARY_REVIEW_PENDING",
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "native_controls": [calibration(*spec) for spec in specs],
            "adaptive_offset_scope_countercontrol": adaptive_offset_countercontrol(),
            "complete_small_native_populations": [population_reference(q, m) for q, m in ((3, 1), (3, 2), (9, 1))],
            "underfull_population_ledgers": [fixed_offset_population_bound(n, q, n*root_digits(q)-2)
                                            for n, q in ((8, 9), (12, 9), (8, 27), (128, 243))],
            "overfull_population_ledgers": [fixed_offset_population_bound(n, q, n*root_digits(q)+k)
                                           for n, q, k in ((8, 9, 8), (32, 81, 16))],
            "generic_quantum_receiver_lower_bound": False,
            "native_spectral_generator_compiler_supplied": False,
            "quantum_speedup_proved": False, "candidate_record_accepted": False, "novelty_claim": False,
            "routine_wiring_owner": "Gemini or Antigravity"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": report["status"], "report": str(REPORT) if args.write else None,
                      "native_calibrations": len(report["native_controls"]),
                      "native_spectral_generator_compiler_supplied": False}, indent=2))


if __name__ == "__main__":
    main()
