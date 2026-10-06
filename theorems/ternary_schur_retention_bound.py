"""Known product-Singleton bounds applied to native adaptive phase restrictions.

LOCAL APPLICATION / REVIEW PENDING. Bounds linear top-degree cancellation,
not arbitrary quantum instruments or complete secret-decoder complexity.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from itertools import product
import json
import math
from pathlib import Path

from dhsp_codomain_instrument import _integer
from ternary_carry_packets import compile_packet
from ternary_schur_closure import frame_columns, schur_admission
from ternary_schur_tensor import canonical, combine

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/ternary_schur_retention_bound.json"


def exact(value):
    value = Fraction(value)
    return {"numerator": str(value.numerator), "denominator": str(value.denominator)}


def retention_bound(support_size, degree, distance_lower_bound):
    for value in (support_size, degree, distance_lower_bound):
        _integer(value, "positive retention parameter")
    if degree % 2 != 1 or degree > 512 or distance_lower_bound > support_size:
        raise ValueError("odd degree<=512 and distance<=nonzero support required")
    t = min(degree, distance_lower_bound)
    ceiling = 1+(support_size-distance_lower_bound)//t
    return {"nonzero_physical_support": support_size, "required_odd_Schur_degree": degree,
            "kernel_distance_lower_bound": distance_lower_bound,
            "product_Singleton_power_used": t,
            "maximum_admitted_frame_dimension": ceiling,
            "maximum_retained_support_fraction": exact(Fraction(ceiling, support_size)),
            "requires_certified_kernel_distance_and_all_mixed_admission": True,
            "valid_for_source_adaptively_selected_linear_frames": True,
            "requires_projective_saturation": False,
            "distance_certified_by_this_arithmetic_ledger": False,
            "nonlinear_or_arbitrary_quantum_receiver_no_go": False}


def projective_words(width):
    return tuple(word for word in product(range(3), repeat=width)
                 if any(word) and next(x for x in word if x) == 1)


def exact_kernel_certificate(low_rows):
    if not low_rows or not low_rows[0]:
        raise ValueError("nonempty low matrix required")
    m = len(low_rows[0])
    low_rows = tuple(canonical(row, m) for row in low_rows)
    packet = compile_packet([[(row[i], 0) for row in low_rows] for i in range(m)], 3)
    if not packet.retained or packet.retained > 8:
        raise ValueError("nonzero exact kernel calibration with dimension<=8 required")
    physical = tuple(tuple(packet.assignment(tuple(int(i == j) for i in range(packet.retained)))[a]
                           for a in range(m)) for j in range(packet.retained))
    histogram, witness, distance = Counter(), None, m+1
    for coefficients in projective_words(packet.retained):
        word = combine(physical, coefficients, m)
        weight = sum(bool(x) for x in word)
        histogram[weight] += 1
        if weight < distance:
            distance, witness = weight, word
    return {"native_low_rows": tuple(tuple(row) for row in low_rows), "physical_kernel_basis": physical,
            "kernel_dimension": packet.retained, "minimum_distance": distance,
            "minimum_weight_witness": witness, "projective_weight_histogram": dict(sorted(histogram.items())),
            "projective_kernel_words_enumerated": (3**packet.retained-1)//2,
            "bounded_exhaustive_certificate_not_scalable_distance_algorithm": True}


def certified_restriction(low_rows, columns, degree):
    columns = frame_columns(columns)
    certificate = exact_kernel_certificate(low_rows)
    admission = schur_admission(low_rows, columns, degree)
    support = sum(any(c[i] for c in columns) for i in range(len(columns[0])))
    distance = certificate["minimum_distance"]
    if support < distance:
        raise AssertionError("nonzero native kernel frame violates exact distance")
    bound = retention_bound(support, degree, distance)
    if admission["higher_Schur_admission"]:
        assert len(columns) <= bound["maximum_admitted_frame_dimension"]
    return {"distance_certificate": certificate, "restriction_admission": admission, "retention_bound": bound,
            "exact_source_distance_certificate_supplied": True,
            "high_retention_claim_excluded_by_bound": len(columns) > bound["maximum_admitted_frame_dimension"],
            "full_phase_instrument_or_decoder_supplied": False}


def short_word_union_bound(secret_dimension, width, distance):
    for value in (secret_dimension, width, distance):
        _integer(value, "positive IID distance parameter")
    if secret_dimension >= width or distance > width or width > 4096:
        raise ValueError("nonzero random kernel with n<m<=4096 and distance<=m required")
    count = sum(math.comb(width, w)*2**(w-1) for w in range(1, distance))
    denominator = 3**secret_dimension
    return {"secret_dimension": secret_dimension, "physical_width": width,
            "kernel_distance_lower_bound": distance,
            "projective_short_words": str(count), "each_projective_word_kernel_probability_denominator": str(denominator),
            "distance_failure_probability_upper_bound": exact(min(Fraction(1), Fraction(count, denominator))),
            "distance_success_probability_lower_bound": exact(max(Fraction(0), 1-Fraction(count, denominator))),
            "IID_uniform_low_native_A_required": True,
            "conditions_on_full_row_rank": False,
            "simultaneous_for_all_source_adaptive_frames": True,
            "certifies_this_particular_matrix": False,
            "postselected_or_correlated_source_transfer_proved": False}


def iid_retention_envelope(secret_dimension, width, degree, failure_budget=Fraction(1, 1000)):
    failure_budget = Fraction(failure_budget)
    if not 0 < failure_budget < 1:
        raise ValueError("strict probability failure budget required")
    short_word_union_bound(secret_dimension, width, 1)
    denominator, count, distance = 3**secret_dimension, 0, 1
    for weight in range(1, min(width, secret_dimension+1)):
        count += math.comb(width, weight)*2**(weight-1)
        if Fraction(count, denominator) > failure_budget:
            break
        distance = weight+1
    source = short_word_union_bound(secret_dimension, width, distance)
    return {"source_distance_envelope": source, "required_failure_budget": exact(failure_budget),
            "simultaneous_adaptive_frame_retention_bound": retention_bound(width, degree, distance),
            "individual_matrix_distance_certificate_supplied": False,
            "complete_algorithm_sample_complexity_bound": False}


def exhaustive_source_control(secret_dimension=2, width=3):
    short_word_union_bound(secret_dimension, width, 1)
    if 3**(secret_dimension*width) > 10000:
        raise ValueError("complete source calibration capped at10000 low matrices")
    words = projective_words(width)
    words = sorted(words, key=lambda w: sum(bool(x) for x in w))
    histogram = Counter()
    for flat in product(range(3), repeat=secret_dimension*width):
        rows = tuple(flat[width*i:width*i+width] for i in range(secret_dimension))
        word = next(w for w in words if all(sum(a*b for a, b in zip(row, w)) % 3 == 0 for row in rows))
        histogram[sum(bool(x) for x in word)] += 1
    total = 3**(secret_dimension*width)
    checks = []
    for distance in range(1, width+1):
        failed = sum(c for w, c in histogram.items() if w < distance)
        envelope = short_word_union_bound(secret_dimension, width, distance)
        upper = envelope["distance_failure_probability_upper_bound"]
        assert Fraction(failed, total) <= Fraction(int(upper["numerator"]), int(upper["denominator"]))
        checks.append({"distance": distance, "actual_failure_probability": exact(Fraction(failed, total)), "envelope": envelope})
    return {"secret_dimension": secret_dimension, "physical_width": width, "all_source_matrices_enumerated": total,
            "minimum_distance_histogram": dict(sorted(histogram.items())), "distance_checks": checks}


def run_controls():
    low = ((1, 1, 1, 1),)
    positive = certified_restriction(low, ((1, 2, 0, 0), (0, 0, 1, 2)), 3)
    negative = certified_restriction(low, exact_kernel_certificate(low)["physical_kernel_basis"], 3)
    return {"status": "NATIVE_ADAPTIVE_LINEAR_RETENTION_BOUND_VERIFIED_REVIEW_PENDING",
            "sharp_disjoint_restriction_control": positive,
            "full_kernel_retention_countercontrol": negative,
            "complete_IID_source_controls": [exhaustive_source_control(n, 3) for n in (1, 2)],
            "growing_source_retention_envelopes": [iid_retention_envelope(n, 2*n, L) for n in (16, 32, 64, 128, 256) for L in (3, 9, 19, 39, 79)],
            "claim_gate": {"new_algorithm": False, "candidate_accepted": False,
                "generic_quantum_decoder_lower_bound": False, "complete_source_recursion_bound": False,
                "independent_human_review": False}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    report = run_controls()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"report": str(args.output), "adaptive_linear_retention_gate_verified": True, "new_algorithm": False}))


if __name__ == "__main__":
    main()
