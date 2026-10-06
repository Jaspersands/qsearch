"""Exact native source law for low-label-selected q=8 carry extraction.

LOCAL DERIVATION / REVIEW PENDING. Conditional circuit identities alone do
not establish the native acceptance rate or fresh independent output labels.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

from sympy import GF
from sympy.polys.matrices import DomainMatrix

from dcp_carry_packets import binary_rank


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/dcp_carry_source_law.json"
SELECTION = "low-bits-and-initial-syndrome-only"


def _matrix(rows, width):
    return DomainMatrix.from_list_sympy(len(rows), width,
        [[row >> j & 1 for j in range(width)] for row in rows]).convert_to(GF(2))


def _independent_indices(vectors, width):
    if not vectors:
        return ()
    return _matrix(vectors, width).transpose().rref()[1]


def _relations(vectors, width):
    """Relations among physical vectors; elimination over GF(2), not rationals."""
    matrix = _matrix(vectors, width).transpose()
    rref, pivots = matrix.rref()
    rref = rref.to_Matrix()
    return tuple((1 << f) | sum((int(rref[i, f]) & 1) << p
                               for i, p in enumerate(pivots))
                 for f in range(len(vectors)) if f not in pivots)


def _validate(low_labels, directions, background):
    low = tuple(tuple(row) for row in low_labels)
    if not low or not low[0] or any(len(row) != len(low[0]) for row in low):
        raise ValueError("nonempty rectangular low-label matrix required")
    if any(a not in (0, 1) for row in low for a in row):
        raise ValueError("low-label source certificate accepts binary residues only")
    directions = tuple(directions)
    m = len(low[0])
    if not directions or any(not 0 < u < 1 << m for u in directions):
        raise ValueError("nonempty physical direction basis required")
    if not 0 <= background < 1 << m:
        raise ValueError("physical background out of range")
    if binary_rank(directions, m) != len(directions):
        raise ValueError("independent physical directions required")
    parity = tuple(sum(a << i for i, a in enumerate(row)) for row in low)
    if any((row & u).bit_count() & 1 for row in parity for u in directions):
        raise ValueError("physical directions must lie in the public parity kernel")
    return low, directions, parity


def _carry(row, mask, background):
    value = sum((1 - 2 * (background >> i & 1)) * a for i, a in enumerate(row)
                if mask >> i & 1)
    if value & 1:
        raise ValueError("carry numerator is odd")
    return value // 2 & 1


def certify_q8_source(low_labels, directions, background=0, *, selection_model):
    """Caller must establish selection lineage; this cannot inspect an algorithm."""
    if selection_model != SELECTION:
        raise ValueError("higher-label/outcome-adaptive selection needs a different source theorem")
    low, directions, parity = _validate(low_labels, directions, background)
    n, m, d = len(low), len(low[0]), len(directions)
    pairs = tuple(u & v for u, v in itertools.combinations(directions, 2))
    common = {"status": "LOCAL_DERIVATION_REVIEW_PENDING", "dimension": n,
              "input_qubits": m, "retained_product_outputs_if_accepted": d,
              "modulus": 8, "selection_model_required": SELECTION,
              "selection_lineage_programmatically_verified": False,
              "unknown_secret_or_gate_oracle_used": False,
              "background_is_physical_not_logical": True,
              "native_average_not_fixed_high_labels": True,
              "source_conditioning": "B, selected directions, initial syndrome, acceptance",
              "unconditional_mixture_over_low_labels_or_changed_bases_classified": False,
              "free_postselection": False, "speedup_claim_allowed": False}
    zero = {"numerator_hex": "0x0", "denominator_binary_exponent": 0}
    if any((row & e).bit_count() & 1 for row in parity for e in pairs):
        return {**common, "acceptance_possible": False, "reason": "quadratic parity obstruction",
                "native_acceptance_probability": zero}
    if any((row & e & u).bit_count() & 1 for row in parity for e in pairs for u in directions):
        return {**common, "acceptance_possible": False, "reason": "cubic interaction",
                "native_acceptance_probability": zero}
    indices = _independent_indices(pairs, m)
    overlap_basis = tuple(pairs[i] for i in indices)
    e = len(overlap_basis)
    targets = [[_carry(row, mask, background) for mask in pairs] for row in low]
    if any(binary_rank([mask | (target << m) for mask, target in zip(pairs, values)], m + 1) != e
           for values in targets):
        return {**common, "acceptance_possible": False, "reason": "inconsistent middle-label constraints",
                "native_acceptance_probability": zero,
                "overlap_span_dimension": e}
    relations = _relations(overlap_basis + directions, m)
    intersection = len(relations)
    assert intersection == e + d - binary_rank(overlap_basis + directions, m)
    constraints = []
    for relation in relations:
        output_mask = relation >> e
        assert output_mask
        component_targets = []
        for l, row in enumerate(low):
            value = sum(targets[l][indices[i]] for i in range(e) if relation >> i & 1)
            value += sum(_carry(row, u, background) for j, u in enumerate(directions)
                         if output_mask >> j & 1)
            component_targets.append(value & 1)
        constraints.append({"output_low_bit_parity_mask": output_mask,
                            "target_by_component": component_targets})
    return {**common, "acceptance_possible": True,
            "overlap_span_dimension": e, "retained_overlap_intersection_dimension": intersection,
            "native_acceptance_probability": {"numerator_hex": "0x1",
                                                "denominator_binary_exponent": n * e},
            "inverse_acceptance_batch_exponent": n * e,
            "conditional_output_entropy_bits": n * (2 * d - intersection),
            "conditional_output_min_entropy_bits": n * (2 * d - intersection),
            "full_iid_output_entropy_bits": 2 * n * d,
            "conditional_output_labels_jointly_iid_uniform_mod_four": intersection == 0,
            "conditional_top_output_bits_jointly_uniform": True,
            "conditional_low_output_constraints": constraints,
            "law_independent_of_complement_outcome": True,
            "overlap_basis_physical_masks": list(overlap_basis),
            "middle_bit_constraint_targets_by_component":
                [[values[i] for i in indices] for values in targets],
            "not_a_claim_that_entropy_deficit_makes_decoding_hard": True}


def overlapping_menu_bound(n, menu_size, attempts=1, *, modulus=8):
    """Select BEFORE complement measurement among low-label-defined bases."""
    if n < 1 or menu_size < 1 or attempts < 1:
        raise ValueError("positive dimension, menu size and attempts required")
    if modulus < 8 or modulus & (modulus - 1):
        raise ValueError("power-of-two modulus >=8 required")
    exponent = n * (modulus.bit_length() - 3)
    bound = min(Fraction(1), Fraction(menu_size * attempts, 1 << exponent))
    return {"dimension": n, "modulus": modulus,
            "single_option_native_acceptance_probability_upper_bound": {
                "numerator_hex": "0x1", "denominator_binary_exponent": exponent},
            "low_label_defined_overlapping_options": menu_size,
            "supplied_packet_attempts": attempts,
            "native_probability_any_accepted_overlapping_packet_upper_bound": {
                "numerator_hex": hex(bound.numerator),
                "denominator_binary_exponent": bound.denominator.bit_length() - 1},
            "selection_can_use_middle_and_top_public_label_bits": True,
            "selection_before_complement_measurement": True,
            "low_defined_menu_membership_programmatically_verified": False,
            "all_options_must_have_nonzero_overlap": True,
            "one_high_bit_synthesized_option_is_not_a_low_defined_menu": True,
            "outcome_adaptive_retained_subspaces_covered": False,
            "arbitrary_polynomial_subspace_synthesis_covered": False,
            "partial_secret_side_information_covered": False,
            "bound_vacuous": bound == 1}


def quadratic_variety_inconsistency_control():
    """A divisibility falsifier, not a proposed oracle/problem family."""
    points = [z for z in range(64)
              if sum((z >> (2 * j) & 1) * (z >> (2 * j + 1) & 1) for j in range(3)) % 2 == 0]
    directions = tuple(sum((z >> j & 1) << i for i, z in enumerate(points)) for j in range(6))
    for order in (1, 2, 3):
        for indices in itertools.combinations(range(6), order):
            overlap = (1 << len(points)) - 1
            for index in indices:
                overlap &= directions[index]
            assert overlap.bit_count() % 2 == 0
    special_pairs = tuple(directions[2 * j] & directions[2 * j + 1] for j in range(3))
    assert special_pairs[0] ^ special_pairs[1] ^ special_pairs[2] == 0
    assert all(mask.bit_count() == 6 for mask in special_pairs)
    result = certify_q8_source([[1] * len(points)], directions, selection_model=SELECTION)
    assert not result["acceptance_possible"]
    assert result["reason"] == "inconsistent middle-label constraints"
    return {"physical_coordinates": len(points), "retained_direction_count": len(directions),
            "all_degree_one_two_three_parity_checks_pass": True,
            "special_pair_overlap_weights": [mask.bit_count() for mask in special_pairs],
            "special_pair_xor_is_zero": True,
            "middle_constraint_target_xor": 1,
            "certificate": result,
            "bounded_identity_counterexample_not_algorithm_candidate": True}


def _source_rows(low_labels, directions):
    """Exhaust independent higher bits per component, without secret simulation."""
    certificate = certify_q8_source(low_labels, directions, selection_model=SELECTION)
    assert certificate["acceptance_possible"]
    m, d = len(low_labels[0]), len(directions)
    if m > 8:
        raise ValueError("exhaustive source control requires m<=8")
    histograms = []
    accepted_counts = []
    for component, low in enumerate(low_labels):
        histogram = Counter()
        accepted_middle = 0
        pairs = tuple(u & v for u, v in itertools.combinations(directions, 2))
        for middle in range(1 << m):
            if any((middle & mask).bit_count() % 2 != _carry(low, mask, 0) for mask in pairs):
                continue
            accepted_middle += 1
            for top in range(1 << m):
                A = [b + 2 * (middle >> i & 1) + 4 * (top >> i & 1) for i, b in enumerate(low)]
                output = tuple(sum(a for i, a in enumerate(A) if u >> i & 1) // 2 % 4
                               for u in directions)
                histogram[output] += 1
                for constraint in certificate["conditional_low_output_constraints"]:
                    assert sum(value & 1 for j, value in enumerate(output)
                               if constraint["output_low_bit_parity_mask"] >> j & 1) % 2 == \
                           constraint["target_by_component"][component]
        assert accepted_middle == 1 << (m - certificate["overlap_span_dimension"])
        assert len(histogram) == 1 << (2 * d - certificate["retained_overlap_intersection_dimension"])
        assert len(set(histogram.values())) == 1
        histograms.append(histogram)
        accepted_counts.append(accepted_middle)
    return {"low_labels_fixed_for_source_identity_control_only": True,
            "certificate": certificate,
            "higher_bit_tables_exhausted_per_component": 1 << (2 * m),
            "accepted_middle_bit_tables_per_component": accepted_counts,
            "observed_output_support_per_component": [len(h) for h in histograms],
            "joint_law_uses_proved_component_factorization_not_full_tensor_enumeration": True}


def run_controls():
    strata = [
        ([[1, 1, 1, 1]], (3, 12)),
        ([[1, 1, 1, 1, 1, 1]], (15, 51)),
        ([[1, 1, 1, 1]], (3, 15)),
        ([[1, 1, 0, 0, 1, 1], [0, 0, 1, 1, 1, 1]], (15, 51)),
        ([[1, 1, 1, 1], [1, 1, 0, 0]], (3, 15)),
    ]
    rows = [_source_rows(low, directions) for low, directions in strata]
    background_checks = 0
    for low, directions in strata:
        base = certify_q8_source(low, directions, selection_model=SELECTION)
        for x in range(1 << len(low[0])):
            current = certify_q8_source(low, directions, x, selection_model=SELECTION)
            assert current["native_acceptance_probability"] == base["native_acceptance_probability"]
            assert current["conditional_low_output_constraints"] == base["conditional_low_output_constraints"]
            background_checks += 1
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING", "source_controls": rows,
            "physical_background_invariance_checks": background_checks,
            "quadratic_variety_inconsistency_control": quadratic_variety_inconsistency_control(),
            "overlapping_menu_bounds": [overlapping_menu_bound(n, n * n, n * n)
                                        for n in (16, 32, 64, 128)],
            "growing_modulus_menu_bounds": [overlapping_menu_bound(n, n * n, n * n, modulus=n)
                                            for n in (16, 32, 64, 128)],
            "claim_gate": {"source_selection_lineage_verified_for_external_candidates": False,
                           "general_outcome_adaptive_no_go": False,
                           "independent_theorem_review": False,
                           "new_decoder": False, "speedup_claim_allowed": False},
            "dependency_sha256": {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                                  for path in (Path(__file__), ROOT / "theorems/dcp_carry_packets.py")}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.save:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"status": report["status"], "source_strata": len(report["source_controls"]),
                      "background_checks": report["physical_background_invariance_checks"],
                      "claim_gate": report["claim_gate"]}, indent=2))


if __name__ == "__main__":
    main()
