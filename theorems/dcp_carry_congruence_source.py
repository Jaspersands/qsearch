"""Exact higher-modulus native carry sources via integer congruence lattices.

Source conditioning and selection lineage are explicit assumptions. HNF
certificates replace exponentially large higher-label/state tables; they
do not produce an efficient unknown-copy decoder or a quantum circuit.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
from math import comb, gcd, prod
from pathlib import Path

from flint import fmpz_mat, fmpq_mat

from theorems.lattice_cube_coset_source import exact_int

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "research/DCP_CARRY_CONGRUENCE_SOURCE.md"
REPORT = ROOT / "research/phase_workbench/dcp_carry_congruence_source.json"
CONTRACT = ROOT / "research/hypotheses/dcp_carry_congruence_source_contract.json"
SELECTION = "low-bits-and-initial-syndrome-only"


@dataclass(frozen=True)
class SourcePolicy:
    max_intersection_states: int = 4096
    max_lattice_cells: int = 200000
    max_transform_cells: int = 500000
    max_modulus_bits: int = 1024

    def __post_init__(self):
        for x in (self.max_intersection_states, self.max_lattice_cells, self.max_transform_cells, self.max_modulus_bits):
            exact_int(x, "positive explicit source cap", 1)


def exact_json(value):
    """Bounded decimal display; large exact integers use signed hexadecimal."""
    if type(value) is int:
        return hex(value) if abs(value).bit_length() > 4096 else str(value) if abs(value) > 2**53-1 else value
    if isinstance(value, dict):
        return {k: exact_json(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [exact_json(v) for v in value]
    return value


def binary_probability(exponent, possible=True):
    return {"numerator_hex": "0x1" if possible else "0x0",
            "denominator_binary_exponent": exponent if possible else 0}


def overlap_closure(directions, t, cap):
    """Compress ALL mixed monomials by their nonzero physical intersection.

    Process fresh direction indices in order. For every intersection retain
    a smallest generating subset; extending it dominates extensions of any
    larger subset with the same intersection. Track mixed-degree witnesses
    separately, since a two-direction intersection can equal one generator.
    """
    meets, mixed, work = {}, {}, 0
    for j, u in enumerate(directions):
        previous = tuple(meets.items())
        for e, subset in previous:
            if len(subset) >= t:
                continue
            work += 1
            intersection, witness = e & u, subset + (j,)
            if not intersection:
                continue
            if intersection not in mixed or (len(witness), witness) < (len(mixed[intersection]), mixed[intersection]):
                mixed[intersection] = witness
            if intersection not in meets or (len(witness), witness) < (len(meets[intersection]), meets[intersection]):
                meets[intersection] = witness
        if u not in meets or len(meets[u]) > 1:
            meets[u] = (j,)
        if len(meets) > cap or len(mixed) > cap:
            raise ValueError("UNKNOWN_INTERSECTION_CLOSURE_CAP; no polynomial-size closure assumed")
    return tuple(sorted(((e, s) for e, s in mixed.items()), key=lambda x: (len(x[1]), x[1]))), {
        "distinct_nonzero_intersections": len(meets), "mixed_intersection_constraints": len(mixed),
        "pairwise_intersections_evaluated": work}


def int_matrix(A):
    return tuple(tuple(int(x) for x in row) for row in A.tolist())


def row_lattice_certificate(generators, policy):
    """Two integer containments prove exact lattice equality, not just a determinant."""
    r, d = len(generators), len(generators[0])
    if r * d > policy.max_lattice_cells or r * r > policy.max_transform_cells:
        raise ValueError("UNKNOWN_HNF_RESOURCE_CAP; not a source impossibility")
    G = fmpz_mat(generators)
    H, T = G.hnf(transform=True)
    if T * G != H or H.rank() != d:
        raise ArithmeticError("full-rank integer generator transform failed")
    basis = fmpz_mat(H.tolist()[:d])
    forward = fmpz_mat(T.tolist()[:d])
    inverse = fmpq_mat(basis).inv()
    coordinates = fmpq_mat(G) * inverse
    if any(x.denominator != 1 for row in coordinates.tolist() for x in row):
        raise ArithmeticError("integer generator containment failed")
    reverse = fmpz_mat([[int(x) for x in row] for row in coordinates.tolist()])
    if forward * G != basis or reverse * basis != G:
        raise ArithmeticError("two-way row-lattice equality failed")
    return {"generator_rows": int_matrix(G), "row_hnf_basis": int_matrix(basis),
            "basis_from_generator_coefficients": int_matrix(forward),
            "generators_from_basis_coefficients": int_matrix(reverse),
            "integer_lattice_index": abs(int(basis.det())),
            "HNF_rows": r, "HNF_columns": d, "internal_transform_cells": r * r,
            "largest_generator_entry_bits": max(abs(x).bit_length() for row in generators for x in row)}, basis, inverse, forward


def affine_congruence_source(R, moduli, J, Q, targets, offsets=None, *, policy=None):
    """Uniform Z_Q^m, constraints Rz=target mod D, output Jz+offset mod Q.

    Coordinates in the joint lattice are CONSTRAINTS FIRST. With FLINT's
    upper-triangular ROW HNF the bottom-right block is the output kernel
    lattice. Taking the leading block under the opposite convention is wrong.
    """
    policy = SourcePolicy() if policy is None else policy
    if not isinstance(policy, SourcePolicy):
        raise ValueError("typed source resource policy required")
    exact_int(Q, "dyadic input/output modulus", 2)
    if Q & (Q - 1) or Q.bit_length() - 1 > policy.max_modulus_bits:
        raise ValueError("UNKNOWN_MODULUS_CAP_OR_NON_DYADIC_SOURCE")
    R, J = tuple(map(tuple, R)), tuple(map(tuple, J))
    moduli, targets = tuple(moduli), tuple(map(tuple, targets))
    c, d = len(R), len(J)
    m = len(J[0]) if d else 0
    if not m or any(len(row) != m for row in R + J) or len(moduli) != c or not targets:
        raise ValueError("rectangular constraints/output and component targets required")
    for x in (x for row in R + J for x in row):
        exact_int(x, "signed integer linear-map entry")
    for x in moduli:
        exact_int(x, "positive divisor modulus", 1)
        if Q % x:
            raise ValueError("constraint periods must divide the uniform domain")
    if any(len(row) != c or any(type(x) is not int or not 0 <= x < moduli[i] for i, x in enumerate(row)) for row in targets):
        raise ValueError("canonical component targets required")
    offsets = tuple((0,) * d for _ in targets) if offsets is None else tuple(map(tuple, offsets))
    if len(offsets) != len(targets) or any(len(row) != d or any(type(x) is not int for x in row) for row in offsets):
        raise ValueError("integer output offset per component required")
    if c:
        constraints = [tuple(R[j][i] for j in range(c)) for i in range(m)]
        constraints += [tuple(moduli[i] if i == j else 0 for j in range(c)) for i in range(c)]
        rc, rb, ri, rf = row_lattice_certificate(constraints, policy)
        delta_R = rc["integer_lattice_index"]
    else:
        rc, rb, ri, rf, delta_R = None, None, None, None, 1
    joint = [tuple(R[j][i] for j in range(c)) + tuple(J[j][i] for j in range(d)) for i in range(m)]
    joint += [tuple((moduli[i] if i == j else 0) for j in range(c)) + (0,) * d for i in range(c)]
    joint += [(0,) * c + tuple(Q if i == j else 0 for j in range(d)) for i in range(d)]
    jc, jb, _, _ = row_lattice_certificate(joint, policy)
    rows = jb.tolist()
    if any(rows[i][j] != 0 for i in range(c, c + d) for j in range(c)):
        raise ArithmeticError("constraint-first row-HNF kernel block convention failed")
    output_basis = tuple(tuple(int(x) for x in row[c:]) for row in rows[c:])
    output_index = abs(int(fmpz_mat(output_basis).det()))
    if jc["integer_lattice_index"] != delta_R * output_index or Q**d % output_index:
        raise ArithmeticError("joint index/conditional output support identity failed")
    support = Q**d // output_index
    components = []
    for target, offset in zip(targets, offsets):
        coefficients = fmpq_mat([target]) * ri if c else None
        possible = not c or all(x.denominator == 1 for x in coefficients.tolist()[0])
        if not possible:
            components.append({"target": target, "acceptance_possible": False,
                "nonintegral_constraint_basis_coordinates": tuple(str(x) for x in coefficients.tolist()[0])})
            continue
        z = (0,) * m
        if c:
            expression = fmpz_mat([[int(x) for x in coefficients.tolist()[0]]]) * rf
            z = tuple(int(x) % Q for x in expression.tolist()[0][:m])
        if any(sum(a * b for a, b in zip(row, z)) % D != t for row, D, t in zip(R, moduli, target)):
            raise ArithmeticError("particular native higher-label witness failed")
        y = tuple((sum(a * b for a, b in zip(row, z)) + off) % Q for row, off in zip(J, offset))
        components.append({"target": target, "acceptance_possible": True,
                           "particular_higher_label_solution": z, "output_coset_representative": y})
    possible = all(row["acceptance_possible"] for row in components)
    image = prod(moduli) // delta_R
    if prod(moduli) % delta_R or image < 1 or image & (image - 1):
        raise ArithmeticError("constraint image cardinality failed")
    exponent = image.bit_length() - 1
    return {"input_modulus": Q, "input_width": m, "constraint_matrix": R, "constraint_moduli": moduli,
        "output_matrix": J, "component_output_offsets": offsets, "components": components,
        "constraint_lattice_certificate": rc, "joint_lattice_certificate": jc,
        "joint_coordinate_order": "CONSTRAINTS_FIRST_OUTPUTS_LAST_FLINT_ROW_HNF",
        "output_kernel_integer_basis": output_basis, "output_kernel_lattice_index": output_index,
        "output_support_size_per_accepted_component": support,
        "output_marginal_support_sizes": tuple(Q // gcd(Q, *(row[i] for row in output_basis)) for i in range(d)),
        "constraint_image_size": prod(moduli) // delta_R,
        "acceptance_possible": possible,
        "acceptance_probability_per_consistent_component": binary_probability(exponent),
        "joint_native_acceptance_probability": binary_probability(exponent * len(targets), possible),
        "expected_supplied_attempts_IF_fresh_batches_exist": {"power_of_two": exponent * len(targets)} if possible else None,
        "resupply_cost_model": "INDEPENDENT_SUPPLIED_BATCH_REJECTION; not a coherent-preparation lower bound",
        "conditional_output_uniform_on_reported_affine_cosets": possible,
        "conditional_joint_labels_IID_uniform_mod_Q": possible and output_index == 1,
        "particular_solution_is_not_unknown_quantum_state_preparation": True,
        "state_or_higher_label_enumeration_used": False}


def binary_rank(masks):
    pivots = {}
    for value in masks:
        while value:
            bit = value.bit_length() - 1
            if bit not in pivots:
                pivots[bit] = value
                break
            value ^= pivots[bit]
    return len(pivots)


def certify_native_source(low_labels, directions, t, background=0, *, selection_model, policy=None):
    policy = SourcePolicy() if policy is None else policy
    if not isinstance(policy, SourcePolicy) or selection_model != SELECTION:
        raise ValueError("typed policy and low-defined selection lineage required; no higher-label selector")
    exact_int(t, "phase-level exponent", 3)
    if t > policy.max_modulus_bits:
        raise ValueError("UNKNOWN_SOURCE_MODULUS_CAP")
    low, directions = tuple(map(tuple, low_labels)), tuple(directions)
    n, m, d = len(low), len(low[0]) if low else 0, len(directions)
    if not m or not d or any(len(row) != m or any(type(x) is not int or x not in (0, 1) for x in row) for row in low):
        raise ValueError("binary low-label matrix and nonempty retained directions required")
    if any(type(u) is not int or not 0 < u < 1 << m for u in directions) or binary_rank(directions) != d:
        raise ValueError("independent physical direction masks required")
    exact_int(background, "physical complement background", 0)
    if background >= 1 << m or any(sum(x for i, x in enumerate(row) if u >> i & 1) % 2 for row in low for u in directions):
        raise ValueError("background range and parity-kernel directions required")
    if (m + d)**2 > policy.max_transform_cells:
        raise ValueError("UNKNOWN_HNF_RESOURCE_CAP; no source impossibility")
    count = sum(comb(d, h) for h in range(2, min(d, t) + 1))
    overlaps, overlap_work = overlap_closure(directions, t, policy.max_intersection_states)
    signs = tuple(1 - 2 * (background >> i & 1) for i in range(m))
    common = {"phase_exponent": t, "modulus": 1 << t, "dimension": n, "physical_input_width": m,
        "retained_outputs": d, "low_label_matrix": low, "physical_directions_hex": tuple(hex(u) for u in directions),
        "physical_background_hex": hex(background), "monomial_expansion_terms": count,
        "overlap_closure_work": overlap_work,
        "selection_model_required": SELECTION, "selection_lineage_programmatically_verified": False,
        "native_law_conditioned_on_observed_B_and_initial_syndrome": True,
        "fixed_B_control_is_not_a_growing_native_success_rate": True,
        "reported_entropy_is_public_label_entropy_not_secret_information": True,
        "probability_of_this_fixed_B_under_IID_native_low_bits": binary_probability(n * m),
        "observed_B_is_not_automatically_a_rejection_filter": True,
        "quantum_product_extraction_circuit_compiled": False, "efficient_receiver_supplied": False,
        "input_noise_scope": "PURE_FLAT_NATIVE_PACKET; contaminated mixed-state outputs require a separate noise law",
        "fresh_native_batches_supplied_by_compiler": False,
        "coherent_native_parent_inverse_or_amplification_supplied": False,
        "accepted_speedup_candidate": False, "novelty_claim": False}
    R, moduli, targets, monomials, checked = [], [], [[] for _ in low], [], 0
    for overlap, subset in overlaps:
        h = len(subset)
        checked += 1
        row = tuple(signs[i] * ((overlap >> i) & 1) for i in range(m))
        totals = [sum(x * a for x, a in zip(row, b)) for b in low]
        if any(total % 2 for total in totals):
            return {**common, "acceptance_possible": False,
                "joint_native_acceptance_probability": binary_probability(0, False), "reason": "LOW_BIT_MIXED_MONOMIAL_OBSTRUCTION",
                "obstructing_subset": subset, "obstructing_overlap_hex": hex(overlap), "monomials_checked": checked}
        if h == t:
            continue
        D = 1 << (t - h)
        R.append(row);moduli.append(D);monomials.append({"degree": h, "subset": subset, "overlap_hex": hex(overlap)})
        for target, total in zip(targets, totals):
            target.append((-total // 2) % D)
    Q = 1 << (t - 1)
    J = tuple(tuple(signs[i] * ((u >> i) & 1) for i in range(m)) for u in directions)
    offsets = tuple(tuple(sum(signs[i] * b[i] for i in range(m) if u >> i & 1) // 2 % Q for u in directions) for b in low)
    law = affine_congruence_source(R, moduli, J, Q, targets, offsets, policy=policy)
    support = law["output_support_size_per_accepted_component"]
    if support & (support - 1) or support < 1 << d:
        raise ArithmeticError("dyadic support/top-output-bit source invariant failed")
    return {**common, "monomials_checked": checked, "higher_label_congruence_monomials": monomials, "source_law": law,
        "acceptance_possible": law["acceptance_possible"],
        "joint_native_acceptance_probability": law["joint_native_acceptance_probability"],
        "conditional_output_entropy_bits_IF_accepted": n * (support.bit_length() - 1) if law["acceptance_possible"] else None,
        "all_top_output_bits_jointly_uniform_IF_accepted": law["acceptance_possible"],
        "expected_original_phase_registers_IF_independent_fresh_batches": {
            "coefficient": m, "power_of_two": law["expected_supplied_attempts_IF_fresh_batches_exist"]["power_of_two"]
        } if law["acceptance_possible"] else None,
        "native_law_background_invariant_IF_selection_lineage_holds": True,
        "background_invariance_map": "Z'_li = (-1)^x_i Z_li - x_i B_li modulo Q; uniform bijection",
        "free_postselection_or_fresh_label_oracle_supplied": False}


def quadratic_inconsistency_control():
    points = [z for z in range(64) if sum(((z >> (2*j)) & 1) * ((z >> (2*j+1)) & 1) for j in range(3)) % 2 == 0]
    directions = tuple(sum(((z >> j) & 1) << i for i, z in enumerate(points)) for j in range(6))
    result = certify_native_source(((1,) * len(points),), directions, 3, selection_model=SELECTION)
    if result["acceptance_possible"] or "source_law" not in result:
        raise ArithmeticError("integer target-consistency counterexample was lost")
    return result


def build_report():
    strata = [(((1, 1, 1, 1),), (3, 12)), (((1, 1, 1, 1),), (3, 15)),
              (((0, 0, 0, 0),), (3, 5, 9))]
    controls = [certify_native_source(B, U, t, x, selection_model=SELECTION)
                for B, U in strata for t in (3, 4, 8, 64) for x in (0, 1)]
    large = certify_native_source(((0,) * 5,) * 16, (3, 5, 9, 17), 64,
                                   selection_model=SELECTION)
    disjoint = certify_native_source(((0,) * 128,), tuple(3 << (2*j) for j in range(64)),
                                      1024, selection_model=SELECTION)
    return {"status": "EXACT_HIGHER_MODULUS_CONDITIONAL_CARRY_SOURCE_REVIEW_PENDING",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "derivation_sha256": hashlib.sha256(DOC.read_bytes()).hexdigest(),
        "contract_sha256": hashlib.sha256(CONTRACT.read_bytes()).hexdigest(),
        "native_source_controls": controls, "large_exact_not_enumerated_control": large,
        "large_disjoint_compressed_control": disjoint,
        "parity_passes_but_integer_targets_inconsistent_control": quadratic_inconsistency_control(),
        "quantum_source_or_receiver_implemented": False,
        "hardness_or_quantum_speedup_demonstrated": False, "accepted_speedup_candidate": False,
        "new_active_negative_result_created": False, "novelty_claim": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2) + "\n")
    print(report["status"])
    print("Conditional source controls:", len(report["native_source_controls"]))


if __name__ == "__main__":
    main()
