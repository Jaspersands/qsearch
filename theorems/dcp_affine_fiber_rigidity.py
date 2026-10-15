"""Global Boolean-affine mod-4 fibre rigidity; local derivation, review pending.

This does not exclude affine proposals accepted only on part of the cube,
adaptive measurement trees, nonlinear involutions, or general receivers.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import product
import json
from math import comb
from pathlib import Path
from random import Random

from theorems.dcp_adaptive_direction_rank_gate import binary_basis, binary_map, dyadic, integer


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/dcp_affine_fiber_rigidity.json"
CONTRACT = ROOT / "research/hypotheses/dcp_affine_fiber_rigidity_contract.json"
CONTRACT_ID = "global_affine_mod4_fibre_signature_rigidity_v1"


def matrix(labels):
    A = tuple(tuple(row) for row in labels)
    if not A or not A[0] or any(len(row) != len(A[0]) for row in A):
        raise ValueError("nonempty rectangular public label matrix required")
    n, m = len(A), len(A[0])
    if max(n, m) > 4096 or n * m > 2000000:
        raise ValueError("UNKNOWN: polynomial certificate work cap")
    for row in A:
        for a in row:
            integer(a, "nonnegative integer public label", 0)
    return A


def signatures(labels):
    A = matrix(labels)
    return tuple(sum((row[i] & 1) << j for j, row in enumerate(A)) for i in range(len(A[0])))


def separating_covector(output_signature, input_signature):
    """u.output=1, u.input=0 when output is nonzero and unequal to input."""
    integer(output_signature, "output signature")
    integer(input_signature, "input signature")
    a, b = output_signature, input_signature
    if not a or a == b:
        return None
    outside = a & ~b
    if outside:
        return outside & -outside
    # Here nonzero a is a STRICT subset of b. Two coordinates separate them.
    inside, difference = a & -a, b & ~a
    return inside | (difference & -difference)


def signature_certificate(labels):
    A = matrix(labels)
    p = signatures(A)
    zero = [i for i, value in enumerate(p) if value == 0]
    repeats = [[j, i] for i in range(len(p)) for j in range(i) if p[i] == p[j]]
    rigid = not zero and not repeats
    return {
        "public_labels_hex": [[hex(a) for a in row] for row in A],
        "secret_vector_components": len(A), "original_registers": len(p),
        "low_column_signatures_hex": [hex(value) for value in p],
        "zero_signature_coordinates": zero, "repeated_signature_pairs": repeats,
        "nonzero_distinct_signatures": rigid,
        "global_affine_mod4_automorphism_classification": "IDENTITY_ONLY" if rigid else "UNKNOWN",
        "failure_of_gate_proves_a_nonidentity_automorphism": False,
        "all_binary_combinations_of_diagonal_forms_used": True,
        "full_label_adaptive_global_affine_selectors_covered": True,
        "partial_affine_proposals_excluded": False,
        "adaptive_affine_measurement_trees_excluded": False,
        "scalar_DHSP_lower_bound": False,
    }


def affine_coefficients(labels, linear_rows, offset):
    """Unique multilinear coefficients of A(Lx XOR c)-Ax modulo4.

    Output coordinate i of Lx is parity(linear_rows[i] & x).
    Degrees >=3 vanish modulo4. No source state or secret enters this test.
    """
    A = matrix(labels)
    n, m = len(A), len(A[0])
    if n * m**3 > 2000000:
        raise ValueError("UNKNOWN: affine coefficient work cap")
    rows = tuple(linear_rows)
    if len(rows) != m:
        raise ValueError("square binary linear map required")
    for row in rows:
        integer(row, "binary linear row", 0, (1 << m) - 1)
    integer(offset, "binary affine offset", 0, (1 << m) - 1)
    cols = tuple(sum(((row >> j) & 1) << i for i, row in enumerate(rows)) for j in range(m))
    signs = tuple(-1 if offset >> i & 1 else 1 for i in range(m))
    constant = [sum(a for i, a in enumerate(row) if offset >> i & 1) % 4 for row in A]
    linear = [[(sum(signs[i] * a for i, a in enumerate(row) if cols[j] >> i & 1) - row[j]) % 4
               for j in range(m)] for row in A]
    quadratic = [[(-2 * sum(signs[i] * a for i, a in enumerate(row)
                              if (cols[j] & cols[k]) >> i & 1)) % 4 for row in A]
                 for j in range(m) for k in range(j + 1, m)]
    zero = (not any(constant) and not any(any(row) for row in linear)
            and not any(any(row) for row in quadratic))
    invertible = len(binary_basis(rows, m)) == m
    p = signatures(A)
    violations = [[i, j] for i in range(m) for j in range(m)
                  if rows[i] >> j & 1 and p[i] and p[i] != p[j]]
    return {
        "linear_rows_hex": [hex(row) for row in rows], "affine_offset_hex": hex(offset),
        "constant_mod4": constant, "linear_mod4_by_component": linear,
        "quadratic_mod4_by_lexicographic_input_pair": quadratic,
        "linear_map_invertible": invertible, "preserves_all_original_assignments_mod4": zero,
        "is_global_affine_fibre_automorphism": invertible and zero,
        "simultaneous_form_forbidden_entries": violations,
        "all_coefficients_are_exact_integers": True,
    }


def native_bound(n, copies):
    integer(n, "native vector dimension", 1, 4096)
    integer(copies, "original registers", 1, 1000000)
    # Zero signature plus birthday collision union, not coordinate containment.
    zero = Fraction(copies, 1 << n)
    repeated = Fraction(comb(copies, 2), 1 << n)
    bad = min(Fraction(1), zero + repeated)
    exact_good = None
    if copies <= 1024:
        # Sequentially exclude zero and all earlier signatures. A pigeonhole
        # failure must remain zero, not a product of negative factors.
        exact_good = Fraction(1)
        if copies >= 1 << n:
            exact_good = Fraction(0)
        else:
            for j in range(copies):
                exact_good *= Fraction((1 << n) - 1 - j, 1 << n)
    return {
        "secret_vector_components": n, "original_registers": copies,
        "native_low_labels": "IID uniform column signatures in F2^n BEFORE postselection",
        "zero_signature_union_upper_bound_uncapped": dyadic(zero),
        "repeated_signature_union_upper_bound_uncapped": dyadic(repeated),
        "rigidity_gate_failure_probability_upper_bound": dyadic(bad),
        "identity_only_probability_lower_bound": dyadic(1 - bad),
        "exact_signature_gate_probability": dyadic(exact_good) if exact_good is not None else None,
        "exact_probability_omitted_due_to_work_cap": exact_good is None,
        "bound_vacuous": bad == 1,
        "all_full_label_selected_global_affine_bijections_covered": True,
        "gate_failure_probability_is_probability_of_nontrivial_automorphism": False,
        "postselected_low_label_laws_inherit_native_probability": False,
        "partial_affine_acceptance_probability_bounded_here": False,
        "general_quantum_lower_bound": False,
    }


def affine_group(width):
    integer(width, "complete affine census width", 1)
    if width > 3:
        raise ValueError("UNKNOWN: complete affine census work cap")
    for rows in product(range(1 << width), repeat=width):
        if len(binary_basis(rows, width)) == width:
            for offset in range(1 << width):
                yield rows, offset


def finite_control(name, labels, phase_bits=3, proposal=None):
    A = matrix(labels)
    integer(phase_bits, "full phase bits", 3, 4096)
    n, m, q = len(A), len(A[0]), 1 << phase_bits
    if m > 3 or any(a >= q for row in A for a in row):
        raise ValueError("UNKNOWN: finite full-assignment census cap or noncanonical labels")
    global_maps, tested = [], 0
    for rows, offset in affine_group(m):
        coeff = affine_coefficients(A, rows, offset)
        direct = all(all(sum(a * (((binary_map(rows, x) ^ offset) >> i & 1) - (x >> i & 1))
                                   for i, a in enumerate(row)) % 4 == 0 for row in A)
                     for x in range(1 << m))
        if direct != coeff["preserves_all_original_assignments_mod4"]:
            raise ArithmeticError("multilinear test disagrees with original subset sums")
        if direct:
            if coeff["simultaneous_form_forbidden_entries"]:
                raise ArithmeticError("simultaneous diagonal form support theorem violated")
            global_maps.append(coeff)
        tested += 1
    identity = tuple(1 << i for i in range(m))
    cert = signature_certificate(A)
    if cert["nonzero_distinct_signatures"] and not (
        len(global_maps) == 1 and global_maps[0]["linear_rows_hex"] == [hex(r) for r in identity]
        and global_maps[0]["affine_offset_hex"] == "0x0"
    ):
        raise ArithmeticError("signature rigidity theorem violated")
    result = {
        "control_id": name, "signature_certificate": cert, "phase_bits": phase_bits,
        "complete_affine_bijections_tested": tested,
        "global_mod4_automorphisms": global_maps,
    }
    if proposal is not None:
        rows, offset = proposal
        coeff = affine_coefficients(A, rows, offset)
        accepted, fixed, nonreciprocal = [], [], []
        for x in range(1 << m):
            y = binary_map(rows, x) ^ offset
            if y == x:
                fixed.append(hex(x))
                continue
            if binary_map(rows, y) ^ offset != x:
                nonreciprocal.append(hex(x))
                continue
            delta = [sum(a * ((y >> i & 1) - (x >> i & 1)) for i, a in enumerate(row)) % q for row in A]
            if all(d % 4 == 0 for d in delta) and any(delta):
                accepted.append({"x_hex": hex(x), "partner_hex": hex(y),
                                 "output_label_hex": [hex(d // 4) for d in delta]})
        result["partial_proposal_control"] = {
            "coefficients": coeff, "useful_reciprocal_assignments": accepted,
            "fixed_assignments_hex": fixed, "nonreciprocal_assignments_hex": nonreciprocal,
            "paid_input_useful_acceptance_probability": dyadic(Fraction(len(accepted), 1 << m)),
            "complete_assignment_census_is_a_scalable_algorithm": False,
        }
    return result


def build_report():
    controls = [
        finite_control("nonzero-antichain", ((1, 1, 0), (1, 0, 1), (0, 1, 1))),
        finite_control("comparable-BUT-distinct-signatures-partial-success", ((1, 0, 5), (0, 1, 1)),
                       proposal=((1, 2, 4), 7)),
        finite_control("repeated-low-signatures-useful-swap", ((1, 5), (2, 2)), proposal=((2, 1), 0)),
        finite_control("zero-signature-useful-translation", ((1, 4),), proposal=((1, 2), 2)),
        finite_control("duplicate-signatures-are-NOT-sufficient", ((1, 1), (0, 2))),
        finite_control("one-nonzero-column", ((3,),)),
    ]
    samples = []
    for n in (32, 64, 128):
        rng = Random(3217 + n)
        # Deterministic UNFILTERED controls, not a probability estimate or a
        # natural hard-instance source. The native theorem is separate.
        A = tuple(tuple(rng.randrange(16) for _ in range(3*n)) for _ in range(n))
        samples.append({"seed": 3217 + n, "sampling": "unfiltered pseudorandom finite control, NOT source theorem",
                        "certificate": signature_certificate(A)})
    return {
        "contract_id": CONTRACT_ID, "status": "LOCAL_DERIVATION_EXTERNAL_REVIEW_PENDING",
        "accepted_speedup_candidate": False, "novelty_claim": False,
        "external_theorem_review_complete": False, "source_quantum_preparations_executed": 0,
        "finite_controls": controls, "polynomial_signature_controls": samples,
        "native_probability_frontiers": [native_bound(n, 3*n + extra)
                                          for n in (1, 8, 32, 64, 128, 256, 512)
                                          for extra in (0, 1)],
        "scope": {
            "relation": "A P(x) = A x mod4 for EVERY original Boolean assignment",
            "map_class": "globally Boolean-affine bijections P(x)=Lx XOR c",
            "higher_descent_moduli_inherit_necessary_mod4_obstruction": True,
            "one_bit_mod2_descent_covered": False,
            "full_public_label_adaptive_choice_of_L_and_c_allowed": True,
            "partial_proposals_excluded": False, "adaptive_measurement_trees_excluded": False,
            "nonlinear_pairing_excluded": False, "general_quantum_lower_bound": False,
            "efficient_coarse_only_pairing_program_supplied": False,
            "source_joint_noise_or_growing_level_composition_resolved": False,
        },
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args(argv)
    report = build_report()
    if not args.no_write:
        REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": report["status"], "finite_controls": len(report["finite_controls"]),
                      "native_frontiers": len(report["native_probability_frontiers"]),
                      "artifact": str(REPORT), "accepted_speedup_candidate": False}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
