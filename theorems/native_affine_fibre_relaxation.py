"""Unit-minor affine parametrization, native selector filter and F3 countercontrol.

Exact public-coordinate recipes and bounded replay, not a physical compiler.
The filter cost is scoped to the unrestricted affine relaxation, not all rows.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
from itertools import product
import json
from pathlib import Path

from flint import fmpq, fmpz_mat, nmod_mat

from known_preparation_coherent_reflection import checked_shape
from native_known_seed_group_workbench import source_fixture
from native_short_preimage_reduction import PreimageReceipt, public_family, recover_with_helper
from ternary_covariant_noise import root_digits
from ternary_measured_lattice_decoder import exact_json, integer
from ternary_noise_degradation import NoisyLinearRecord

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT/"research/NATIVE_AFFINE_FIBRE_RELAXATION.md"
REPORT = ROOT/"research/reductions/native_affine_fibre_relaxation.json"


class NonFreeRank(ValueError):
    """This unit-minor recipe is unsupported; not a claim of no solutions."""


def matrix_product(A, B, q):
    product_matrix = fmpz_mat(A)*fmpz_mat(B)
    return tuple(tuple(int(product_matrix[i, j]) % q for j in range(product_matrix.ncols()))
                 for i in range(product_matrix.nrows()))


def unit_minor_inverse(S, q):
    """Prime-field start, verified Newton/Hensel lift; no composite-field inverse."""
    r = root_digits(q)
    n = len(S)
    if not n or any(len(row) != n for row in S): raise ValueError("nonempty square unit minor required")
    for row in S: canonical_vector(row, n, q)
    field = nmod_mat([[a % 3 for a in row] for row in S], 3)
    if int(field.rank()) != n: raise NonFreeRank("minor is not a unit; unsupported, not no solutions")
    initial = field.inv()
    X = tuple(tuple(int(initial[i, j]) for j in range(n)) for i in range(n))
    identity = tuple(tuple(int(i == j) for j in range(n)) for i in range(n))
    current, steps = 1, [1]
    while current < r:
        current = min(2*current, r)
        modulus = 3**current
        SX = matrix_product(S, X, modulus)
        correction = tuple(tuple((2*identity[i][j]-SX[i][j]) % modulus for j in range(n)) for i in range(n))
        X = matrix_product(X, correction, modulus)
        if matrix_product(S, X, modulus) != identity or matrix_product(X, S, modulus) != identity:
            raise ArithmeticError("unit-minor Hensel inverse failed both exact identities")
        steps.append(current)
    return X, tuple(steps)


@dataclass(frozen=True)
class AffineRecipe:
    modulus: int
    matrix: tuple
    pivot_columns: tuple
    free_columns: tuple
    pivot_inverse: tuple
    inverse_lift_digits: tuple

    def coordinates(self, z):
        z = canonical_vector(z, len(self.matrix[0]), self.modulus)
        target = tuple(sum(a*b for a, b in zip(row, z)) % self.modulus for row in self.matrix)
        return target, tuple(z[j] for j in self.free_columns)

    def solve(self, target, free):
        q, n = self.modulus, len(self.matrix)
        target = canonical_vector(target, n, q)
        free = canonical_vector(free, len(self.free_columns), q)
        rhs = tuple((target[i]-sum(self.matrix[i][j]*x for j, x in zip(self.free_columns, free))) % q for i in range(n))
        pivot = tuple(sum(a*b for a, b in zip(row, rhs)) % q for row in self.pivot_inverse)
        out = [0]*len(self.matrix[0])
        for j, x in zip(self.free_columns, free): out[j] = x
        for j, x in zip(self.pivot_columns, pivot): out[j] = x
        if self.coordinates(out) != (target, free): raise ArithmeticError("affine recipe did not invert actual public coordinates")
        return tuple(out)

    def record(self):
        n, d, r = len(self.matrix), len(self.matrix[0]), root_digits(self.modulus)
        return {"modulus": str(self.modulus), "matrix": self.matrix, "pivot_columns": self.pivot_columns,
                "free_columns": self.free_columns, "pivot_minor_inverse": self.pivot_inverse,
                "inverse_lift_digits": self.inverse_lift_digits,
                "free_registers": d-n, "free_fibre_size": {"base": str(self.modulus), "exponent": d-n},
                "coordinate_bijection": "z <-> (A*z,z_free)", "unit_minor_verified_modulo_full_root": True,
                "uses_composite_modulus_field_inverse": False,
                "classical_matrix_preprocessing_arithmetic_order": "O(n^2*d+n^3*log(r))",
                "reversible_affine_map_modular_multiply_add_order": "O(n*d+n^2)",
                "uniform_free_register_trits": (d-n)*r,
                "physical_gate_synthesis_and_precision_supplied": False}


def canonical_vector(values, width, q):
    values = tuple(values)
    if len(values) != width or any(type(x) is not int or not 0 <= x < q for x in values):
        raise ValueError("canonical exact modular vector required")
    return values


def affine_recipe(A, q):
    root_digits(q)
    A = tuple(tuple(row) for row in A)
    if not A or not A[0] or len(A) > len(A[0]) or any(len(row) != len(A[0]) for row in A):
        raise ValueError("nonempty wide public modular matrix required")
    for row in A: canonical_vector(row, len(A[0]), q)
    reduced, rank = nmod_mat([[a % 3 for a in row] for row in A], 3).rref()
    if rank != len(A): raise NonFreeRank("public rows are not full rank modulo3; unsupported, not no solutions")
    pivots = tuple(next(j for j in range(len(A[0])) if int(reduced[i, j])) for i in range(len(A)))
    free = tuple(j for j in range(len(A[0])) if j not in pivots)
    S = tuple(tuple(row[j] for j in pivots) for row in A)
    inverse, steps = unit_minor_inverse(S, q)
    return AffineRecipe(q, A, pivots, free, inverse, steps)


def family_matrix(family, cohort):
    integer(cohort, "nonnegative cohort")
    if cohort >= family.cohorts: raise ValueError("actual public cohort required")
    return tuple(tuple(a[i] for pair in family.paired_labels[cohort] for a in pair) for i in range(family.dimension))


def selector_word(coefficients, q):
    root_digits(q)
    coefficients = tuple(coefficients)
    if len(coefficients) % 2: raise ValueError("complete paired coefficient vector required")
    coefficients = canonical_vector(coefficients, len(coefficients), q)
    allowed = ((1, 0), (q-1, 1), (0, q-1))
    pairs = tuple(zip(coefficients[::2], coefficients[1::2]))
    return None if any(pair not in allowed for pair in pairs) else tuple(allowed.index(pair) for pair in pairs)


def selector_affine_certificate(q):
    root_digits(q)
    residual = (3 % q, -3 % q)
    closure = (-6 % q, 3 % q)
    return {"modulus": str(q), "third_selector_affine_extrapolation_defect": residual,
            "F3_slope_cyclic_closure_defect": closure,
            "native_selector_is_an_F3_affine_line_for_arbitrary_public_pairs": q == 3,
            "higher_root_carries_may_be_discarded": False}


def endpoint_recipes(family):
    if family.modulus != 3: raise ValueError("F3 endpoint linearization cannot be promoted to higher roots")
    out = []
    for b, pairs in enumerate(family.paired_labels):
        offset = tuple(sum(a[i] for a, _ in pairs) % 3 for i in range(family.dimension))
        slopes = tuple(tuple((a[i]+c[i]) % 3 for a, c in pairs) for i in range(family.dimension))
        try: recipe = affine_recipe(slopes, 3)
        except NonFreeRank: continue
        out.append((b, offset, recipe))
    if not out: raise NonFreeRank("no full-rank F3 endpoint cohort; unsupported, not no native solutions")
    return tuple(out)


class EndpointLabelHelper:
    """Polynomial known F3 endpoint, not a growing-root helper."""
    def __init__(self, family):
        self.fingerprint, self.recipes = family.fingerprint(), endpoint_recipes(family)
        self.calls = 0

    def __call__(self, family, target):
        if family.fingerprint() != self.fingerprint: raise ValueError("helper bound to a different public family")
        target = canonical_vector(target, family.dimension, 3)
        b, offset, recipe = self.recipes[0]
        word = recipe.solve(tuple((x-y) % 3 for x, y in zip(target, offset)), (0,)*len(recipe.free_columns))
        if family.frequency(b, word) != target: raise ArithmeticError("actual F3 native word map failed linearization")
        self.calls += 1
        return PreimageReceipt(self.fingerprint, target, b, word)


def filter_ledger(n, r, cohorts, sites):
    integer(n, "positive original dimension", 1)
    integer(r, "positive root exponent", 1)
    checked_shape(cohorts, sites)
    if 2*sites < n: raise ValueError("full-row-rank relaxation requires enough original coordinates")
    # Store exponents: growing-depth expansion would create millions of digits.
    E = r*(2*sites-n)-sites
    return {"dimension": n, "root_digits": r, "cohorts": cohorts, "sites": sites,
            "per_cohort_unrestricted_affine_fibre_trits": r*(2*sites-n),
            "per_target_filter_acceptance_upper": {"base": 3, "negative_exponent": max(0, E)},
            "uniform_target_mean_filter_acceptance": {"base": 3, "negative_exponent": (2*r-1)*sites},
            "half_success_requires_ordinary_amplification_multiplier_square_at_least":
                {"base": 3, "exponent": max(0, E), "denominator": 2},
            "full_row_rank_modulo3_in_every_cohort_is_an_assumption": True,
            "target_word_counts_or_population_balance_assumed": False,
            "bound_is_only_for_uniform_unrestricted_affine_fibre_filter": True,
            "arbitrary_coherent_fibre_algorithms_excluded": False,
            "endpoint_linear_bypass_excluded": False,
            "physical_gate_compiler_supplied": False, "accepted_speedup_candidate": False}


def finite_control(n, r, B, M, seed, cap=8192):
    source, _, _ = source_fixture(n, r, B, M, False, seed)
    raw = tuple(NoisyLinearRecord(tuple(s["label"]), s["value"], s["modulus"], s["source_id"])
                for s in source["source_receipts"]["original_classical_records"])
    family = public_family(raw, B, M)
    q = family.modulus
    integer(cap, "positive complete finite coordinate cap", 1)
    if B*q**(2*M) > cap: raise ValueError("complete affine coordinate replay exceeds finite cap")
    try: recipes = tuple(affine_recipe(family_matrix(family, b), q) for b in range(B))
    except NonFreeRank:
        return {"status": "NONFREE_RANK_UNSUPPORTED_NOT_NO_SOLUTIONS", "public_family": family.record(),
                "target_failure_or_general_no_go_inferred": False}
    targets = tuple(product(range(q), repeat=n))
    accepted, seen, word_counts = [], [], {}
    for b, recipe in enumerate(recipes):
        coordinates_seen = set()
        for target in targets:
            for free in product(range(q), repeat=2*M-n):
                z = recipe.solve(target, free)
                if recipe.coordinates(z) != (target, free): raise ArithmeticError("public coordinate inverse failed")
                coordinates_seen.add(z)
                word = selector_word(z, q)
                if word is not None:
                    if family.frequency(b, word) != target: raise ArithmeticError("relaxed coefficients disagree with actual selector map")
                    accepted.append({"cohort": b, "target": target, "free_coordinates": free, "coefficients": z, "word": word})
                    word_counts[target] = word_counts.get(target, 0)+1
        seen.append(len(coordinates_seen))
    if any(x != q**(2*M) for x in seen) or len(accepted) != B*3**M:
        raise ArithmeticError("complete affine bijection or native membership failed")
    K = q**(2*M-n)
    rows = tuple({"target": target, "native_word_count": word_counts.get(target, 0),
                  "raw_filter_acceptance": str(fmpq(word_counts.get(target, 0), B*K)),
                  "complete_failure_probability": str(1-fmpq(word_counts.get(target, 0), B*K)),
                  "conditional_word_probability": None if not word_counts.get(target, 0) else str(fmpq(1, word_counts[target]))}
                 for target in targets)
    return {"status": "COMPLETE_EXACT_PUBLIC_AFFINE_FILTER_CONTROL", "public_family": family.record(),
            "public_affine_recipes": tuple(p.record() for p in recipes), "all_target_filter_laws": rows,
            "accepted_word_receipts": tuple(accepted), "complete_coordinates_checked_per_cohort": tuple(seen),
            "complete_native_memberships_checked": len(accepted),
            "uniform_target_mean_acceptance_exact": str(fmpq(3**M, q**(2*M))),
            "source_values_mask_secret_and_errors_used_by_relaxation": False,
            "discarding_failure_is_free": False, "bounded_exhaustive_replay_is_polynomial_algorithm": False,
            "physical_uniform_affine_state_circuit_executed": False,
            "all_quantum_fibre_preparation_excluded": False}


def endpoint_control():
    # Deterministic actual original-data calibration; no fabricated oracle access.
    labels = ((1, 0), (1, 0), (0, 1), (0, 1), (1, 1), (2, 1))
    secret, mask = (2, 0), (1, 2)
    raw = tuple(NoisyLinearRecord(a, sum(x*y for x, y in zip(a, secret)) % 3, 3, f"affine-endpoint-{i}") for i, a in enumerate(labels))
    family = public_family(raw, 1, 3)
    helper = EndpointLabelHelper(family)
    result = recover_with_helper(raw, mask, 1, 3, helper)
    return {"original_records": tuple(s.public() for s in raw), "known_mask": mask,
            "public_endpoint_recipes": tuple({"cohort": b, "offset": offset, "affine_recipe": p.record()}
                                              for b, offset, p in helper.recipes),
            "actual_original_data_reconstruction": result,
            "truth_fixture_only": {"original_secret": secret},
            "matches_truth_fixture": result["original_secret"] == secret,
            "label_only_helper_calls": helper.calls,
            "growing_root_helper_or_new_quantum_algorithm": False}


def build_report():
    controls = [finite_control(*p) for p in ((1, 1, 1, 2, 90001), (1, 2, 1, 2, 90002),
                                           (2, 1, 1, 2, 90003), (1, 2, 2, 1, 90004),
                                           (2, 1, 1, 2, 90005), (1, 2, 2, 1, 90006))]
    dependencies = ("native_short_preimage_reduction.py", "native_known_seed_group_workbench.py", "known_preparation_coherent_reflection.py",
                    "ternary_covariant_noise.py", "ternary_measured_lattice_decoder.py", "ternary_noise_degradation.py")
    return {"status": "SCOPED_NATIVE_AFFINE_RELAXATION_FILTER_AND_ENDPOINT_COUNTERCONTROL_REVIEW_PENDING",
            "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "dependency_sha256": {f: hashlib.sha256((ROOT/"theorems"/f).read_bytes()).hexdigest() for f in dependencies},
            "bounded_filter_controls": controls, "actual_F3_endpoint_countercontrol": endpoint_control(),
            "selector_linearization_checks": tuple(selector_affine_certificate(3**r) for r in (1, 2, 16, 64)),
            "growing_relaxation_ledgers": tuple(filter_ledger(n, n, 1, n*n+24) for n in (8, 32, 64, 128)),
            "research_decision": "DEPRIORITIZE_UNRESTRICTED_AFFINE_RELAXATION_FILTER_NOT_STRUCTURED_ROW_CONSTRUCTIONS",
            "accepted_speedup_candidate": False, "new_active_negative_result_created": False,
            "general_quantum_fibre_lower_bound_proved": False,
            "remaining_obligations": ["external proof review", "actual physical affine/QFT/filter compiler and precision",
                                      "structured row preparation bypassing this uniform relaxation", "production admission wiring"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2)+"\n")
    print(json.dumps({"status": report["status"], "controls": [{"status": c["status"],
                      "coordinates": c.get("complete_coordinates_checked_per_cohort"),
                      "mean_acceptance": c.get("uniform_target_mean_acceptance_exact")} for c in report["bounded_filter_controls"]],
                      "endpoint_classical_reconstruction": report["actual_F3_endpoint_countercontrol"]["matches_truth_fixture"],
                      "accepted_speedup_candidate": False}, indent=2))


if __name__ == "__main__": main()
