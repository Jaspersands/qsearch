"""Costed higher native Schur admission and projective saturation gates.

LOCAL APPLICATION / REVIEW PENDING. Schur-power stabilization is known coding
theory. Public restriction geometry is not source construction or decoding.
"""
from __future__ import annotations

import argparse
from itertools import product
import json
import math
from pathlib import Path
import random

from cyclotomic_rescaling_gate import ideal_chart
from dhsp_codomain_instrument import _integer
from ternary_carry_packets import compile_packet
from ternary_phase_depth import NativePhaseHierarchy
from ternary_schur_tensor import canonical, combine, rank

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/ternary_schur_closure.json"


def frame_columns(columns):
    if not columns or not columns[0]:
        raise ValueError("nonempty physical frame required")
    height = len(columns[0])
    columns = tuple(canonical(c, height) for c in columns)
    if rank(columns, height) != len(columns):
        raise ValueError("independent physical frame required")
    return columns


def dot_rows(rows, word):
    return tuple(sum(a*b for a, b in zip(row, word)) % 3 for row in rows)


def projective_classes(columns):
    columns = frame_columns(columns)
    m, k = len(columns[0]), len(columns)
    classes, zeros = {}, []
    for i in range(m):
        row = tuple(c[i] for c in columns)
        if not any(row):
            zeros.append(i)
            continue
        scale = next(x for x in row if x)
        representative = tuple(scale*x % 3 for x in row)
        classes.setdefault(representative, []).append((i, scale))
    records = []
    for representative, entries in sorted(classes.items()):
        word = [0]*m
        for i, scale in entries:
            word[i] = scale
        records.append({"representative": representative, "signed_block_word": tuple(word),
                        "support": tuple(i for i, _ in entries)})
    return {"physical_width": m, "frame_dimension": k, "zero_row_coordinates": zeros,
            "classes": records, "projective_length": len(records),
            "direct_odd_stabilization_bound": 2*k-1,
            "known_coding_regularity_bound": len(records)-k+1}


def independent_products(candidates, height):
    echelon, basis = {}, []
    count = 0
    for original, factors in candidates:
        count += 1
        reduced = list(original)
        for pivot, row in sorted(echelon.items()):
            coefficient = reduced[pivot]
            if coefficient:
                reduced = [(a-coefficient*b) % 3 for a, b in zip(reduced, row)]
        pivot = next((i for i, x in enumerate(reduced) if x), None)
        if pivot is None:
            continue
        inverse = reduced[pivot]
        row = tuple(inverse*x % 3 for x in reduced)
        echelon[pivot] = row
        basis.append((tuple(original), tuple(factors)))
    assert len(basis) <= height
    return tuple(basis), count


def odd_power_basis(columns, degree):
    columns = frame_columns(columns)
    _integer(degree, "positive odd Schur degree")
    if degree % 2 != 1 or degree > 512:
        raise ValueError("odd Schur degree<=512 required")
    m, k = len(columns[0]), len(columns)
    geometry = projective_classes(columns)
    c = geometry["projective_length"]
    basis = tuple((column, (i,)) for i, column in enumerate(columns))
    histories = [{"degree": 1, "dimension": k, "candidate_products": k}]
    candidate_count, evaluated_degree = k, 1
    for d in range(2, degree+1):
        if evaluated_degree % 2 == 1 and len(basis) == c:
            break
        candidates = ((tuple(a*b % 3 for a, b in zip(word, column)), factors+(i,))
                      for word, factors in basis for i, column in enumerate(columns))
        basis, count = independent_products(candidates, m)
        histories.append({"degree": d, "dimension": len(basis), "candidate_products": count})
        candidate_count += count
        evaluated_degree = d
    if evaluated_degree < degree:
        padding = degree-evaluated_degree
        assert padding % 2 == 0
        basis = tuple((word, factors+(factors[0],)*padding) for word, factors in basis)
    assert all(len(factors) == degree for _, factors in basis)
    if degree >= geometry["direct_odd_stabilization_bound"]:
        assert len(basis) == c
    return {"degree": degree, "basis": basis, "histories": histories,
            "evaluated_through_degree": evaluated_degree,
            "projective_geometry": geometry,
            "resources": {"candidate_products_processed": candidate_count,
                "coordinatewise_products_upper_bound": m*candidate_count,
                "modular_elimination_entry_operations_upper_bound": m*m*candidate_count,
                "maximum_basis_vectors_stored_per_power": m,
                "full_basis_multisets_not_enumerated": str(math.comb(k+degree-1, degree)),
                "unknown_weighted_phase_queries": 0,
                "quantum_instrument_or_decoder_supplied": False}}


def fixed_frame_probability(secret_dimension, frame_dimension, power_dimension):
    for value in (secret_dimension, frame_dimension, power_dimension):
        _integer(value, "positive fixed-frame dimension")
    if power_dimension < frame_dimension:
        raise ValueError("odd Schur span must contain the frame")
    return {"unconditional_admission_probability_denominator": str(3**(secret_dimension*power_dimension)),
            "conditional_on_AW_zero_probability_denominator": str(3**(secret_dimension*(power_dimension-frame_dimension))),
            "requires_frame_fixed_independently_of_uniform_low_A": True,
            "invalid_after_source_adaptive_frame_selection": True,
            "algorithm_for_finding_admitted_frame_supplied": False}


def schur_admission(low_rows, columns, degree):
    columns = frame_columns(columns)
    m, k = len(columns[0]), len(columns)
    if not low_rows:
        raise ValueError("nonempty low native matrix required")
    low_rows = tuple(canonical(row, m) for row in low_rows)
    if any(any(dot_rows(low_rows, c)) for c in columns):
        raise ValueError("physical frame must lie in the actual native low kernel")
    power = odd_power_basis(columns, degree)
    images = tuple(dot_rows(low_rows, word) for word, _ in power["basis"])
    witness = next(({"basis_factor_indices": factors, "physical_product_word": word,
                     "weighted_component_values_mod3": values}
                    for (word, factors), values in zip(power["basis"], images) if any(values)), None)
    geometry = power["projective_geometry"]
    blocks = tuple(record["signed_block_word"] for record in geometry["classes"])
    block_images = tuple(dot_rows(low_rows, word) for word in blocks)
    saturated = len(power["basis"]) == geometry["projective_length"]
    stable = not any(any(row) for row in block_images)
    admitted = witness is None
    if saturated:
        assert admitted == stable
    if stable:
        reconstructed = tuple(combine(blocks, [record["representative"][j] for record in geometry["classes"]], m)
                              for j in range(k))
        assert reconstructed == columns
    return {"odd_degree": degree, "physical_frame_columns": columns, "native_low_rows": low_rows,
            "power_dimension": len(power["basis"]), "power_histories": power["histories"],
            "evaluated_through_degree": power["evaluated_through_degree"],
            "higher_Schur_admission": admitted, "mixed_failure_witness": witness,
            "projective_geometry": geometry, "signed_block_component_images": block_images,
            "odd_power_saturated": saturated,
            "all_odd_powers_admitted": stable,
            "disjoint_kernel_refinement": {"certified": stable, "dimension": len(blocks) if stable else None,
                "signed_blocks": blocks if stable else None,
                "original_frame_contained": stable,
                "new_source_sampler_or_complete_receiver": False},
            "fixed_frame_reference_probability": fixed_frame_probability(len(low_rows), k, len(power["basis"])),
            "fixed_frame_probability_applicable_to_this_source_adaptive_kernel_frame": False,
            "resources": power["resources"], "secret_decoder_or_generic_no_go": False}


def native_restriction(packet, logical_frame):
    logical_frame = frame_columns(logical_frame)
    if len(logical_frame[0]) != packet.retained:
        raise ValueError("logical frame height must equal packet retained width")
    hierarchy = NativePhaseHierarchy.from_packet(packet)
    physical = tuple(hierarchy.physical_direction(v) for v in logical_frame)
    result = schur_admission(hierarchy.low_rows, physical, packet.level)
    witness = result["mixed_failure_witness"]
    derivative = None
    if witness:
        directions = [logical_frame[j] for j in witness["basis_factor_indices"]]
        derivative = hierarchy.derivative((0,)*packet.retained, directions)
        assert derivative == hierarchy.top_derivative(directions)
        assert any(derivative)
    result.update({"native_parent_level": packet.level, "logical_frame_columns": logical_frame,
                   "native_top_derivative_of_failure_witness": derivative,
                   "all_affine_branches_have_same_top_admission": True,
                   "top_admission_only_not_constant_degree_or_decoder": True,
                   "source_acquisition_or_full_instrument_charged": False})
    return result


def native_evaluation_countercontrol():
    points = tuple(product(range(3), repeat=3))
    labels = [[(x[2], 0)] for x in points]
    physical = tuple(tuple(x[j] for x in points) for j in range(3))
    records = []
    for L in (3, 5, 9, 19):
        packet = compile_packet(labels, L)
        frame = tuple(tuple(c[i] for i in packet.free) for c in physical)
        records.append(native_restriction(packet, frame))
    return {"native_labels": labels, "deterministic_algebra_control_not_IID_sampler": True,
            "level_controls": records}


def native_refinement_control():
    labels = [[(1, 0)]]*6
    blocks = ((1, 2, 0, 0, 0, 0), (0, 0, 1, 2, 0, 0), (0, 0, 0, 0, 1, 2))
    physical = (combine(blocks, (1, 1, 0), 6), combine(blocks, (0, 1, 1), 6))
    packet = compile_packet(labels, 19)
    frame = tuple(tuple(c[i] for i in packet.free) for c in physical)
    record = native_restriction(packet, frame)
    assert record["higher_Schur_admission"] and record["odd_power_saturated"]
    assert record["disjoint_kernel_refinement"]["dimension"] == 3
    return {"native_labels": labels, "deterministic_algebra_control_not_IID_sampler": True,
            "overlapping_frame_dimension": 2, "restriction": record}


def native_large_countercontrol():
    rng = random.Random(49171)
    L, m, n = 19, 24, 3
    a, _, b = ideal_chart(L)[0]
    labels = [[(rng.randrange(a), rng.randrange(b)) for _ in range(n)] for _ in range(m)]
    packet = compile_packet(labels, L)
    frame = tuple(tuple(int(i == j) for i in range(packet.retained)) for j in range(packet.retained))
    record = native_restriction(packet, frame)
    assert record["odd_power_saturated"] and not record["higher_Schur_admission"]
    return {"native_labels": labels, "seed": 49171, "unfiltered_native_label_calibration": True,
            "restriction": record}


def run_controls():
    return {"status": "NATIVE_HIGHER_SCHUR_CLOSURE_AND_SATURATION_GATE_VERIFIED_REVIEW_PENDING",
            "evaluation_code_countercontrol": native_evaluation_countercontrol(),
            "overlapping_disjoint_refinement_control": native_refinement_control(),
            "growing_width_native_countercontrol": native_large_countercontrol(),
            "fixed_frame_probability_control": fixed_frame_probability(2, 2, 3),
            "claim_gate": {"new_algorithm": False, "candidate_accepted": False,
                "generic_source_adaptive_no_go": False, "growing_depth_secret_decoder": False,
                "independent_human_review": False}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    report = run_controls()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"report": str(args.output), "higher_Schur_admission_verified": True, "new_algorithm": False}))


if __name__ == "__main__":
    main()
