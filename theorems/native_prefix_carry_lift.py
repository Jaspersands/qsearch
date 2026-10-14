"""Exact prefix-native word parametrization and compact first carry equations.

Local derivation, review pending. No cubic solver, physical row compiler or
growing-root speedup is supplied; mod9 matching is not full-root matching.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
from itertools import combinations, product
import json
from pathlib import Path

from flint import fmpq

from native_affine_fibre_relaxation import affine_recipe, canonical_vector, NonFreeRank
from native_known_seed_group_workbench import source_fixture
from native_short_preimage_reduction import public_family
from known_preparation_coherent_reflection import checked_shape
from ternary_covariant_noise import root_digits
from ternary_measured_lattice_decoder import exact_json, integer
from ternary_noise_degradation import NoisyLinearRecord

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT/"research/NATIVE_PREFIX_CARRY_LIFT.md"
REPORT = ROOT/"research/reductions/native_prefix_carry_lift.json"


@dataclass(frozen=True)
class PrefixCarryCircuit:
    family: object
    cohort: int
    target: tuple
    prefix_recipe: object
    offsets: tuple
    pivot_forms: tuple
    constants: tuple
    linear: tuple
    diagonal_quadratic: tuple
    pivot_weights: tuple

    def word(self, free):
        free = canonical_vector(free, len(self.prefix_recipe.free_columns), 3)
        offset = tuple(sum(a[i] for a, _ in self.family.paired_labels[self.cohort]) % 3 for i in range(self.family.dimension))
        rhs = tuple((s-a) % 3 for s, a in zip(self.target, offset))
        return self.prefix_recipe.solve(rhs, free)

    def evaluate(self, free):
        free = canonical_vector(free, len(self.prefix_recipe.free_columns), 3)
        out = [c+sum(a*u for a, u in zip(row, free))+sum(a*u*u for a, u in zip(diag, free))
               for c, row, diag in zip(self.constants, self.linear, self.diagonal_quadratic)]
        for form, weights in zip(self.pivot_forms, self.pivot_weights):
            b = form["coefficients"]
            L = sum(a*u for a, u in zip(b, free))
            numerator = L**3-sum(a**3*u**3 for a, u in zip(b, free))
            if numerator % 3: raise ArithmeticError("divided cube numerator is not divisible over integers")
            divided, square_term = numerator//3, sum(a*u*u for a, u in zip(b, free))
            for i, weight in enumerate(weights):
                out[i] += weight["square"]*L*L+weight["cube"]*(square_term+divided)
        return tuple(x % 3 for x in out)

    def record(self):
        k = len(self.prefix_recipe.free_columns)
        return {"public_family": self.family.record(), "cohort": self.cohort, "target": self.target,
                "prefix_recipe": self.prefix_recipe.record(), "word_offsets": self.offsets,
                "pivot_affine_forms": self.pivot_forms, "F3_constants": self.constants,
                "F3_linear_coefficients": self.linear, "F3_diagonal_quadratic": self.diagonal_quadratic,
                "F3_pivot_weights": self.pivot_weights, "free_trits": k,
                "next_digit_equations": self.family.dimension, "total_degree_upper": 3,
                "dense_divided_cube_forms_upper": len(self.pivot_forms),
                "expanded_cubic_tensor_materialized": False,
                "divided_cubes_are_ordinary_rank_one_F3_cubes": False,
                "coefficient_division_by3_is_verified_integer_division": True,
                "source_values_mask_secret_or_errors_supplied": False,
                "matching_mod9_implies_full_root_matching": self.family.modulus == 9,
                "polynomial_cubic_solver_or_uniform_row_sampler_supplied": False,
                "physical_row_preparation_circuit_executed": False}

    def expanded_polynomial(self, cap=100000):
        """Capped canonical F3 expansion; never the scalable representation."""
        k, n = len(self.prefix_recipe.free_columns), self.family.dimension
        integer(cap, "positive canonical polynomial expansion cap", 1)
        possible = 1+2*k+k*(k-1)//2+k*(k-1)+k*(k-1)*(k-2)//6
        if n*possible > cap: raise ValueError("canonical cubic expansion exceeds cap; use compact carry circuit")
        polys = [dict() for _ in range(n)]
        def add(i, powers, coefficient):
            powers = tuple(powers)
            polys[i][powers] = (polys[i].get(powers, 0)+coefficient) % 3
        for i in range(n):
            add(i, [0]*k, self.constants[i])
            for l in range(k):
                powers = [0]*k; powers[l] = 1; add(i, powers, self.linear[i][l])
                powers[l] = 2; add(i, powers, self.diagonal_quadratic[i][l])
        for form, weights in zip(self.pivot_forms, self.pivot_weights):
            b = form["coefficients"]
            for i, weight in enumerate(weights):
                square, cube = weight["square"], weight["cube"]
                for l in range(k):
                    powers = [0]*k; powers[l] = 2; add(i, powers, square*b[l]**2+cube*b[l])
                    for m in range(k):
                        if m == l: continue
                        powers = [0]*k; powers[l], powers[m] = 2, 1
                        add(i, powers, cube*b[l]**2*b[m])
                for l, m in combinations(range(k), 2):
                    powers = [0]*k; powers[l] = powers[m] = 1
                    add(i, powers, 2*square*b[l]*b[m])
                for l, m, h in combinations(range(k), 3):
                    powers = [0]*k; powers[l] = powers[m] = powers[h] = 1
                    add(i, powers, 2*cube*b[l]*b[m]*b[h])
        return tuple(tuple({"powers": powers, "coefficient": coefficient}
                           for powers, coefficient in sorted(p.items()) if coefficient) for p in polys)


def compile_carry(family, cohort, target):
    if root_digits(family.modulus) < 2: raise ValueError("first nontrivial carry requires root at least9")
    integer(cohort, "nonnegative actual cohort")
    if cohort >= family.cohorts: raise ValueError("actual public cohort required")
    target = canonical_vector(target, family.dimension, family.modulus)
    pairs, n = family.paired_labels[cohort], family.dimension
    slopes = tuple(tuple((a[i]+c[i]) % 3 for a, c in pairs) for i in range(n))
    offset = tuple(sum(a[i] for a, _ in pairs) % 3 for i in range(n))
    recipe = affine_recipe(slopes, 3)
    rhs = tuple((s-a) % 3 for s, a in zip(target, offset))
    k = len(recipe.free_columns)
    word_offsets = recipe.solve(rhs, (0,)*k)
    coefficients = tuple(tuple(-sum(row[j]*slopes[j][site] for j in range(n)) % 3 for site in recipe.free_columns)
                         for row in recipe.pivot_inverse)
    forms = tuple({"site": site, "offset": word_offsets[site], "coefficients": row}
                  for site, row in zip(recipe.pivot_columns, coefficients))
    constants, linear, diagonals = [], [], []
    weights = [[] for _ in forms]
    for i in range(n):
        constant = sum(a[i] for a, _ in pairs)-target[i]
        lin = [0]*k
        for form, entries in zip(forms, weights):
            site, t0, b = form["site"], form["offset"], form["coefficients"]
            a, c = pairs[site][0][i], pairs[site][1][i]
            w = c-2*a
            constant += w*t0**3+3*a*t0*(t0-1)
            for l in range(k): lin[l] += w*(3*t0*t0*b[l]-2*b[l]**3)+3*a*(2*t0-1)*b[l]
            entries.append({"square": (w*t0+a) % 3, "cube": w % 3})
        diag = []
        for l, site in enumerate(recipe.free_columns):
            a, c = pairs[site][0][i], pairs[site][1][i]
            w = c-2*a
            lin[l] += -2*w-3*a
            diag.append((w+a) % 3)
        if constant % 3 or any(x % 3 for x in lin):
            raise ArithmeticError("prefix correctness did not imply coefficientwise divisibility")
        constants.append((constant % 9)//3)
        linear.append(tuple((x % 9)//3 for x in lin))
        diagonals.append(tuple(diag))
    return PrefixCarryCircuit(family, cohort, target, recipe, word_offsets, forms,
                              tuple(constants), tuple(linear), tuple(diagonals), tuple(tuple(x) for x in weights))


def finite_control(n, r, B, M, seed, cap=4096):
    recipe, _, _ = source_fixture(n, r, B, M, False, seed)
    raw = tuple(NoisyLinearRecord(tuple(s["label"]), s["value"], s["modulus"], s["source_id"])
                for s in recipe["source_receipts"]["original_classical_records"])
    family = public_family(raw, B, M)
    target = tuple((7+2*i) % family.modulus for i in range(n))
    try: circuits = tuple(compile_carry(family, b, target) for b in range(B))
    except NonFreeRank:
        return {"status": "PREFIX_RANK_UNSUPPORTED_NOT_NO_WORDS", "public_family": family.record(),
                "source_impossibility_or_general_no_go_inferred": False}
    integer(cap, "positive complete finite prefix replay cap", 1)
    count = B*3**(M-n)
    if count > cap: raise ValueError("complete prefix-word replay exceeds finite cap")
    controls = []
    for circuit in circuits:
        rows = []
        for free in product(range(3), repeat=M-n):
            word = circuit.word(free)
            sigma = family.frequency(circuit.cohort, word)
            residual = tuple((x-y) % 9 for x, y in zip(sigma, target))
            if any(x % 3 for x in residual): raise ArithmeticError("native word missed its low prefix")
            expected = tuple(x//3 for x in residual)
            computed = circuit.evaluate(free)
            if computed != expected: raise ArithmeticError("compact cubic carry disagrees with actual original label map")
            rows.append({"free_trits": free, "native_word": word, "actual_frequency": sigma,
                         "next_digit_residual": computed, "matches_mod9_target": all(x == 0 for x in computed),
                         "matches_entire_root_target": sigma == target})
        controls.append({"compact_circuit": circuit.record(), "canonical_polynomials": circuit.expanded_polynomial(),
                         "complete_prefix_word_rows": rows,
                         "mod9_filter_acceptance": str(fmpq(sum(row["matches_mod9_target"] for row in rows), len(rows))),
                         "entire_root_filter_acceptance": str(fmpq(sum(row["matches_entire_root_target"] for row in rows), len(rows)))})
    return {"status": "EXACT_COMPACT_MOD9_CARRY_AND_COMPLETE_PREFIX_WORD_CONTROL", "public_family": family.record(),
            "target": target, "cohort_controls": controls, "complete_prefix_words_checked": count,
            "new_cubic_solver_or_full_root_row_circuit": False}


def prefix_filter_ledger(n, r, cohorts, sites):
    integer(n, "positive original dimension", 1);integer(r, "positive root exponent", 1)
    checked_shape(cohorts, sites)
    if sites < n: raise ValueError("full prefix rank requires at least n native sites")
    return {"dimension": n, "root_digits": r, "cohorts": cohorts, "sites": sites,
            "free_native_word_trits_per_cohort": sites-n,
            "uniform_higher_target_mean_acceptance": {"base": 3, "negative_exponent": n*(r-1)},
            "prescribed_target_ensemble_mean_under_uniform_higher_labels": {"base": 3, "negative_exponent": n*(r-1)},
            "ordinary_amplification_mean_acceptance_upper": "min(1,(2j+1)^2*3^[-n(r-1)])",
            "full_prefix_rank_in_each_cohort_required": True,
            "IID_uniform_higher_original_labels_conditioned_on_low_labels_required_for_prescribed_target_mean": True,
            "prescribed_target_fixed_conditioned_on_low_labels_before_higher_labels_required": True,
            "prefix_basis_and_cohort_weights_depend_only_on_low_labels_required": True,
            "uniform_target_mean_is_a_per_dataset_prescribed_target_promise": False,
            "population_law_established_by_finite_artifact": False,
            "later_digit_equations_proved_degree3": False,
            "generic_carry_solvers_excluded": False, "accepted_speedup_candidate": False}


def build_report():
    controls = [finite_control(*p) for p in ((1, 2, 1, 3, 91001), (2, 2, 1, 4, 91002),
                                           (2, 3, 2, 4, 91003), (3, 64, 1, 6, 91004),
                                           (1, 2, 1, 3, 91005))]
    deps = ("native_affine_fibre_relaxation.py", "native_known_seed_group_workbench.py", "native_short_preimage_reduction.py",
            "known_preparation_coherent_reflection.py", "ternary_covariant_noise.py", "ternary_measured_lattice_decoder.py", "ternary_noise_degradation.py")
    return {"status": "COMPACT_NATIVE_FIRST_CARRY_EQUATIONS_AND_PREFIX_ROW_REFERENCE_REVIEW_PENDING",
            "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "dependency_sha256": {f: hashlib.sha256((ROOT/"theorems"/f).read_bytes()).hexdigest() for f in deps},
            "bounded_carry_controls": controls,
            "growing_prefix_filter_ledgers": tuple(prefix_filter_ledger(n, n, 1, n*n+24) for n in (8, 32, 64, 128)),
            "research_decision": "SEARCH_STRUCTURED_CARRY_SYSTEMS_NOT_FREE_HIGHER_ROOT_LINEARIZATION",
            "polynomial_cubic_solver_or_full_root_row_circuit": False,
            "accepted_speedup_candidate": False, "new_active_negative_result_created": False,
            "remaining_obligations": ["external polynomial identity and access review", "known underdetermined polynomial-system algorithm comparison",
                                      "uniform coherent solution sampler versus one-witness search", "later digits and complete row normalization",
                                      "physical prefix/filter/compiler precision", "production admission integration"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__);parser.add_argument("--write", action="store_true")
    args = parser.parse_args();report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True);REPORT.write_text(json.dumps(exact_json(report), indent=2)+"\n")
    print(json.dumps({"status": report["status"], "controls": [{"status": c["status"],
                      "prefix_words": c.get("complete_prefix_words_checked")} for c in report["bounded_carry_controls"]],
                     "accepted_speedup_candidate": False}, indent=2))


if __name__ == "__main__": main()
