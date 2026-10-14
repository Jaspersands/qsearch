"""Actual classical first-carry diagonal restriction with paid MITM search.

Public labels only. Review pending; no full-root helper, uniform coherent
row sampler, generic no-go, or new quantum speedup is supplied.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, replace
import hashlib
from itertools import combinations, product
import json
from pathlib import Path

from flint import fmpq, nmod_mat

from native_prefix_carry_lift import PrefixCarryCircuit, compile_carry
from native_affine_fibre_relaxation import canonical_vector, matrix_product
from native_known_seed_group_workbench import source_fixture
from native_short_preimage_reduction import public_family
from native_choice_mitm import solve_choices
from ternary_measured_lattice_decoder import exact_json, integer
from ternary_noise_degradation import NoisyLinearRecord

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT/"research/NATIVE_CARRY_DIAGONAL_SLICE.md"
REPORT = ROOT/"research/classical_baselines/native_carry_diagonal_slice.json"


def fingerprint(record):
    return hashlib.sha256(json.dumps(exact_json(record), sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def left_apply(X, rows):
    if not rows[0]: return tuple(() for _ in X)
    return matrix_product(X, rows, 3)


@dataclass(frozen=True)
class NormalizedCarry:
    raw: PrefixCarryCircuit
    transformed: PrefixCarryCircuit
    output_inverse: tuple

    def evaluate(self, free): return self.transformed.evaluate(free)

    def record(self):
        c = self.transformed
        return {"raw_carry_sha256": fingerprint(self.raw.record()), "output_inverse": self.output_inverse,
                "F3_constants": c.constants, "F3_linear_coefficients": c.linear,
                "F3_diagonal_quadratic": c.diagonal_quadratic, "F3_pivot_weights": c.pivot_weights,
                "zero_set_is_preserved": True, "output_is_literal_native_digit_residual": False,
                "one_divided_cube_per_equation": True,
                "quadratic_terms_or_free_variables_are_independent": False,
                "uniform_fibre_sampler_or_solver_supplied_by_output_normalization": False}


def normalize(circuit):
    n, X = circuit.family.dimension, circuit.prefix_recipe.pivot_inverse
    cubic = tuple(tuple(circuit.pivot_weights[j][i]["cube"] for j in range(n)) for i in range(n))
    S = tuple(tuple(row[j] for j in circuit.prefix_recipe.pivot_columns) for row in circuit.prefix_recipe.matrix)
    I = tuple(tuple(int(i == j) for j in range(n)) for i in range(n))
    if cubic != S or matrix_product(X, cubic, 3) != I:
        raise ArithmeticError("actual cube coefficients do not equal the invertible prefix minor")
    constants = tuple(row[0] for row in left_apply(X, tuple((c,) for c in circuit.constants)))
    linear, diagonal = left_apply(X, circuit.linear), left_apply(X, circuit.diagonal_quadratic)
    weights = []
    for old in circuit.pivot_weights:
        square = tuple(sum(a*w["square"] for a, w in zip(row, old)) % 3 for row in X)
        cube = tuple(sum(a*w["cube"] for a, w in zip(row, old)) % 3 for row in X)
        weights.append(tuple({"square": a, "cube": b} for a, b in zip(square, cube)))
    transformed = replace(circuit, constants=constants, linear=linear, diagonal_quadratic=diagonal, pivot_weights=tuple(weights))
    return NormalizedCarry(circuit, transformed, X)


def divided_cube(b, u):
    b = canonical_vector(b, len(b), 3)
    u = canonical_vector(u, len(b), 3)
    numerator = sum(a*x for a, x in zip(b, u))**3-sum(a**3*x**3 for a, x in zip(b, u))
    if numerator % 3: raise ArithmeticError("divided cube has no integer quotient")
    return numerator//3 % 3


@dataclass(frozen=True)
class DiagonalSlice:
    normalized: NormalizedCarry
    directions: tuple
    blocks: tuple
    linear: tuple
    quadratic: tuple
    selection_is_known_low_only: bool = False

    def free(self, parameters):
        parameters = canonical_vector(parameters, len(self.directions), 3)
        k = len(self.normalized.raw.prefix_recipe.free_columns)
        return tuple(sum(v[l]*z for v, z in zip(self.directions, parameters)) % 3 for l in range(k))

    def evaluate(self, parameters):
        parameters = canonical_vector(parameters, len(self.directions), 3)
        return tuple((c+sum(a*z+b*z*z for a, b, z in zip(L, Q, parameters))) % 3
                     for c, L, Q in zip(self.normalized.transformed.constants, self.linear, self.quadratic))

    def record(self):
        raw, k, t = self.normalized.raw, len(self.normalized.raw.prefix_recipe.free_columns), len(self.directions)
        return {"normalized_carry_sha256": fingerprint(self.normalized.record()), "directions": self.directions,
                "blocks": self.blocks, "parameters": t, "free_prefix_trits": k,
                "F3_constants": self.normalized.transformed.constants,
                "F3_linear_columns": self.linear, "F3_quadratic_columns": self.quadratic,
                "uniform_prefix_projection_acceptance": {"base": 3, "negative_exponent": k-t},
                "support_disjointness_and_kernel_verified": True,
                "restricted_system_is_diagonal_quadratic_plus_linear": True,
                "full_prefix_zero_set_preserved": False,
                "full_coherent_fibre_or_full_root_helper_supplied": False,
                "slice_choice_uses_higher_labels": False if self.selection_is_known_low_only else None,
                "selection_policy": "LOW_SLOPE_DISJOINT_BLOCK_FIRST_NULLSPACE_VECTOR" if self.selection_is_known_low_only else "EXTERNAL_SELECTION_PROVENANCE_UNVERIFIED",
                "selection_provenance_inferred_from_kernel_validity": False}


def verify_directions(normalized, directions):
    k = len(normalized.raw.prefix_recipe.free_columns)
    B = tuple(form["coefficients"] for form in normalized.raw.pivot_forms)
    occupied = set()
    for v in directions:
        canonical_vector(v, k, 3)
        support = {i for i, x in enumerate(v) if x}
        if not support or occupied & support or any(sum(a*b for a, b in zip(row, v)) % 3 for row in B):
            raise ValueError("nonzero disjoint-support vectors in the actual pivot-form kernel required")
        occupied.update(support)


def restrict_diagonal(normalized, directions, blocks=()):
    directions = tuple(tuple(v) for v in directions)
    verify_directions(normalized, directions)
    c = normalized.transformed
    L, Q = [], []
    for i, b in enumerate(form["coefficients"] for form in c.pivot_forms):
        L.append(tuple((sum(a*x for a, x in zip(c.linear[i], v))+divided_cube(b, v)) % 3 for v in directions))
        Q.append(tuple(sum((a+x)*v_l*v_l for a, x, v_l in zip(c.diagonal_quadratic[i], b, v)) % 3 for v in directions))
    return DiagonalSlice(normalized, directions, tuple(blocks), tuple(L), tuple(Q))


def disjoint_kernel_slice(normalized):
    n, k = normalized.raw.family.dimension, len(normalized.raw.prefix_recipe.free_columns)
    B = tuple(form["coefficients"] for form in normalized.raw.pivot_forms)
    directions, blocks = [], []
    for start in range(0, k, n+1):
        end = min(k, start+n+1)
        kernel, nullity = nmod_mat([row[start:end] for row in B], 3).nullspace()
        if not nullity: continue
        v = [0]*k
        for l in range(start, end): v[l] = int(kernel[l-start, 0])
        scale = pow(next(x for x in v if x), -1, 3)
        v = tuple(x*scale % 3 for x in v)
        directions.append(v);blocks.append({"start": start, "end": end, "nullity": int(nullity)})
    if len(directions) < k//(n+1): raise ArithmeticError("full kernel blocks did not supply their guaranteed directions")
    return replace(restrict_diagonal(normalized, directions, blocks), selection_is_known_low_only=True)


def meet_in_middle(slice_, max_evaluations=100000, max_entries=100000):
    t, n = len(slice_.directions), slice_.normalized.raw.family.dimension
    choices = tuple(tuple(tuple((slice_.linear[i][j]*z+slice_.quadratic[i][j]*z*z) % 3 for i in range(n))
                          for z in range(3)) for j in range(t))
    target = tuple(-c % 3 for c in slice_.normalized.transformed.constants)
    result = solve_choices(choices, target, 3, max_evaluations, max_entries)
    if result["parameters"] is None:
        return {**result, "status": "SEARCH_CAP_EXCEEDED_NOT_NO_SOLUTION" if result["status"].startswith("SEARCH_CAP") else "COMPLETE_SEARCH_NO_SOLUTION_ON_THIS_SLICE",
                "whole_root_target_matched": False, "absence_of_full_prefix_or_root_solutions_inferred": False}
    parameters = result["parameters"]
    if any(slice_.evaluate(parameters)): raise ArithmeticError("MITM collision did not solve actual restricted equations")
    free = slice_.free(parameters);raw = slice_.normalized.raw
    word = raw.word(free);frequency = raw.family.frequency(raw.cohort, word)
    if any((x-y) % 9 for x, y in zip(frequency, raw.target)):
        raise ArithmeticError("restricted solver returned no actual mod9 word")
    return {**result, "status": "VERIFIED_CLASSICAL_FIRST_CARRY_WITNESS", "free_trits": free,
            "native_word": word, "actual_frequency": frequency, "whole_root_target_matched": frequency == raw.target}


def affine_mask_change(circuit, deltas):
    """Proof of conditional population map, NOT chosen access to original labels."""
    n, M, k = circuit.family.dimension, circuit.family.sites, len(circuit.prefix_recipe.free_columns)
    deltas = tuple(tuple(canonical_vector(a, n, 3) for a in pair) for pair in deltas)
    if len(deltas) != M or any(len(pair) != 2 for pair in deltas): raise ValueError("actual complete higher-label delta pairs required")
    constants, linear = [], []
    for i in range(n):
        d = tuple((a[i]+c[i]) % 3 for a, c in deltas)
        constants.append((sum(a[i] for a, _ in deltas)+sum(x*y for x, y in zip(d, circuit.offsets))) % 3)
        linear.append(tuple((d[site]+sum(d[form["site"]]*form["coefficients"][l] for form in circuit.pivot_forms)) % 3
                            for l, site in enumerate(circuit.prefix_recipe.free_columns)))
    return tuple(constants), tuple(linear)


def moment_ledger(n, k, t, cohorts=1):
    integer(n, "positive carry equation count", 1);integer(k, "nonnegative prefix free width");integer(t, "nonnegative injective slice width")
    integer(cohorts, "positive independent higher-label cohort count", 1)
    if t > k: raise ValueError("slice cannot exceed the prefix width")
    mu = fmpq(3**t, 3**n)
    lower = mu/(mu+1-fmpq(1, 3**n))
    return {"equations": n, "prefix_free_trits": k, "slice_parameters": t, "cohorts": cohorts,
            "single_slice_mean_solution_count": str(mu),
            "single_slice_solution_count_variance": str(mu*(1-fmpq(1, 3**n))),
            "single_slice_solution_existence_probability_lower": str(lower),
            "single_slice_solution_existence_probability_upper": str(min(fmpq(1), mu)),
            "full_prefix_no_solution_probability_upper_compact": {"numerator_base": 3, "numerator_exponent": n,
                "numerator_subtract": 1, "denominator_base": 3, "denominator_exponent": k, "denominator_multiplier": cohorts, "clipped_at_one": True},
            "IID_uniform_first_higher_labels_conditioned_on_low_labels_required": True,
            "full_low_prefix_rank_in_each_cohort_required": True,
            "target_basis_and_slice_fixed_before_higher_labels_required": True,
            "population_premises_established_by_artifact": False,
            "repeated_slices_on_same_data_are_independent": False,
            "existence_bound_constructs_witness_or_coherent_sampler": False,
            "later_carry_or_full_root_decoder_established": False, "accepted_speedup_candidate": False}


def degree3_probe_points(t):
    """Unisolvent grid for canonical F3 polynomials of total degree at most3."""
    integer(t, "nonnegative parameter width")
    points = {(0,)*t}
    for i in range(t):
        for a in (1, 2):
            point = [0]*t;point[i] = a;points.add(tuple(point))
    for i, j in combinations(range(t), 2):
        for a, b in ((1, 1), (1, 2), (2, 1)):
            point = [0]*t;point[i], point[j] = a, b;points.add(tuple(point))
    for i, j, h in combinations(range(t), 3):
        point = [0]*t;point[i] = point[j] = point[h] = 1;points.add(tuple(point))
    return tuple(sorted(points))


def control(n, r, M, seed, cap=729):
    source, _, _ = source_fixture(n, r, 1, M, False, seed)
    raw = tuple(NoisyLinearRecord(tuple(s["label"]), s["value"], s["modulus"], s["source_id"])
                for s in source["source_receipts"]["original_classical_records"])
    family = public_family(raw, 1, M)
    target = tuple((7+2*i) % family.modulus for i in range(n))
    circuit = compile_carry(family, 0, target)
    normalized = normalize(circuit);slice_ = disjoint_kernel_slice(normalized)
    t = len(slice_.directions)
    integer(cap, "positive diagnostic replay cap", 1)
    exhaustive = 3**t <= cap
    parameters_to_check = tuple(product(range(3), repeat=t)) if exhaustive else degree3_probe_points(t)
    if len(parameters_to_check) > cap: raise ValueError("degree3 diagonal slice grid exceeds finite cap")
    rows = []
    for parameters in parameters_to_check:
        free = slice_.free(parameters);restricted = slice_.evaluate(parameters)
        actual = normalized.evaluate(free)
        if restricted != actual: raise ArithmeticError("degree reduction changed actual carry on the slice")
        rows.append({"parameters": parameters, "free_trits": free, "normalized_carry": actual,
                     "is_mod9_solution": all(x == 0 for x in actual)})
    return {"raw_carry": circuit.record(), "output_normalization": normalized.record(), "diagonal_slice": slice_.record(),
            "slice_check_rows": rows, "slice_exhaustively_enumerated": exhaustive,
            "degree3_unisolvent_grid_used": not exhaustive,
            "solution_count": sum(row["is_mod9_solution"] for row in rows) if exhaustive else None,
            "diagnostic_points_are_a_uniform_solution_sampler": False,
            "solver": meet_in_middle(slice_), "conditional_population_ledger": moment_ledger(n, M-n, t),
            "full_prefix_enumerated": False, "new_quantum_algorithm_or_full_root_helper": False}


def build_report():
    controls = [control(*p) for p in ((2, 2, 12, 92001), (3, 3, 15, 92002), (4, 64, 20, 92003), (8, 8, 88, 92004))]
    deps = ("native_prefix_carry_lift.py", "native_affine_fibre_relaxation.py", "native_known_seed_group_workbench.py",
            "native_short_preimage_reduction.py", "native_choice_mitm.py", "ternary_measured_lattice_decoder.py", "ternary_noise_degradation.py")
    return {"status": "CONSTRUCTIVE_CLASSICAL_NATIVE_FIRST_CARRY_DIAGONAL_SLICE_REVIEW_PENDING",
            "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "dependency_sha256": {f: hashlib.sha256((ROOT/"theorems"/f).read_bytes()).hexdigest() for f in deps},
            "actual_native_slice_controls": controls,
            "growing_slice_population_ledgers": tuple(moment_ledger(n, n*n+24-n, (n*n+24-n)//(n+1)) for n in (8, 32, 64, 128)),
            "research_decision": "COMPARE_FIRST_CARRY_QUANTUM_PROPOSALS_WITH_PUBLIC_DIAGONAL_SLICE_MITM_AND_CHARGE_FULL_ROW_MASS",
            "accepted_speedup_candidate": False, "new_active_negative_result_created": False,
            "growing_root_classical_preimage_solver_or_uniform_coherent_row_sampler": False,
            "remaining_obligations": ["external degree-reduction and population proof review", "better public slice choices without fictitious independence",
                                      "classical simultaneous diagonal/quadratic methods and honest failure budgets", "later carries and full-row distribution",
                                      "production baseline/admission integration"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__);parser.add_argument("--write", action="store_true")
    args = parser.parse_args();report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True);REPORT.write_text(json.dumps(exact_json(report), indent=2)+"\n")
    print(json.dumps({"status": report["status"], "controls": [{"equations": c["raw_carry"]["next_digit_equations"],
                      "slice_parameters": c["diagonal_slice"]["parameters"], "solutions": c["solution_count"], "solver": c["solver"]["status"],
                      "whole_root_matched": c["solver"]["whole_root_target_matched"]} for c in report["actual_native_slice_controls"]],
                     "accepted_speedup_candidate": False}, indent=2))


if __name__ == "__main__": main()
