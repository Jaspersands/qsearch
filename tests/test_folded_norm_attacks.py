"""Same-input classical square completion and native polynomial verification."""

import hashlib
import json
from pathlib import Path
from fractions import Fraction
from itertools import combinations, product
import math

from flint import fq_default_ctx
import pytest

import theorems.folded_norm_attacks as module
from theorems.folded_norm_attacks import (REPORT, Problem, attack, fixed_input_fit_tail,
                                        instance, joint_acceptance_error, norm_line_polynomial,
                                        pencil_attack, pencil_pattern_certificate, population_tail)
from theorems.folded_norm_source import extension_model, fraction
from theorems.prime_character_opi import ring


def horner(p, coefficients, x):
    result = 0
    for a in reversed(coefficients):
        result = (result*x + a) % p
    return result


def independent_score(problem, coefficients, selected=()):
    spec = problem.specification()
    E = fq_default_ctx(modulus=ring(problem.p)(spec["field"]["modulus_coefficients"]))
    values = [horner(problem.p, coefficients, pow(problem.gamma, j, problem.p)) for j in range(problem.n*problem.m)]
    flags = []
    for i in range(problem.n):
        z = E(values[i*problem.m:(i + 1)*problem.m]) - E(list(problem.shifts[i]))
        chi = 0 if z == 0 else (1 if z.is_square() else -1)
        flags.append(chi == problem.signs[i] or (problem.include_zero and z == 0))
    assert all(flags[i] for i in selected)
    return flags


@pytest.mark.parametrize("strict", [True, False])
def test_every_small_proposal_fits_accepted_squares_without_altering_public_input(strict):
    problem = instance(127, 6, 3, 10, 3, 4891, include_zero=not strict)
    before = problem.specification()
    result = attack(problem, trials=8, repair_steps=12)
    assert before == problem.specification() == result["specification"]
    assert result["source_rerolls"] == 0
    assert result["complete_block_interpolation_guarantee"] == 3
    assert result["scalar_degrees_unused_by_anchor_rounding"] == 1
    for row in result["proposals"]:
        flags = independent_score(problem, row["polynomial_coefficients"], row["anchor_blocks"])
        assert row["score"] == sum(flags)
        assert row["accepted_blocks"] == [i for i, yes in enumerate(flags) if yes]
    count = len(result["proposals"])
    assert result["polynomial_interpolations_charged"] == count
    assert result["native_norm_character_evaluations_charged"] == count*problem.n
    assert result["native_scalar_values_evaluated_charged"] == count*problem.n*problem.m
    assert result["field_square_draws_charged"] >= 8*3
    assert result["public_base_field_nonsquare_tests_charged"] > 0
    assert not result["hidden_oracle_or_field_table_used"]


def test_model_rejects_even_degree_and_malformed_input_instead_of_importing_flatness():
    with pytest.raises(ValueError, match="odd m"):
        instance(127, 4, 2, 4, 3, 1)
    with pytest.raises(ValueError, match="distinct"):
        instance(127, 6, 3, 9, 1, 1)
    with pytest.raises(ValueError, match="canonical complete"):
        Problem(127, 4, 3, 6, 3, ((0, 0, 0),)*4, (1, 1, 1, 0))


def test_live_best_words_are_independently_valid_at_every_scaling_size():
    report = json.loads(REPORT.read_text())
    for control in report["controls"]:
        classical = control["classical"]
        spec = classical["specification"]
        problem = Problem(int(spec["p_decimal"]), spec["n_blocks"], spec["m_fold"],
                          spec["ORIGINAL_scalar_dimension_K"], spec["gamma"],
                          tuple(map(tuple, spec["shifts"])), tuple(spec["signs"]), spec["include_zero"])
        flags = independent_score(problem, classical["best_polynomial_coefficients"])
        assert sum(flags) == classical["best_score"]
        assert [i for i, yes in enumerate(flags) if yes] == classical["best_accepted_blocks"]
        assert classical["polynomial_interpolations_charged"] == len(classical["proposals"]) == 96
        assert not control["matched_runtime_advantage_or_candidate_accepted"]
        assert not control["exceeding_a_mean_lower_bound_refutes_quantum_algorithm_or_proves_dequantization"]
        quantum = control["conditional_quantum_reference"]
        assert quantum["source"]["scalar_rank_K"] == problem.K
        assert quantum["source"]["n_blocks"] == problem.n
        assert fraction(quantum["bounded_decoder_loss"]["per_attempt_expected_normalized_score_lower_exact"]) <= fraction(quantum["heralded_mean_lower_exact"])
        fit_bound = control["fixed_input_fresh_full_fit_sampling_bound"]
        assert quantum["tails"][-1]["accepted_count"] == fit_bound["target_accepted_count"]
        assert fraction(quantum["tails"][-1]["bounded_pruning_one_attempt_lower_exact"]) > 0
        pencil = control["native_norm_pencil_attack"]
        assert pencil["input_sha256"] == classical["input_sha256"]
        final_flags = independent_score(problem, pencil["best_polynomial_coefficients"])
        assert sum(final_flags) == pencil["best_score"] >= classical["best_score"]
        assert [i for i, yes in enumerate(final_flags) if yes] == pencil["best_accepted_blocks"]
        assert len(pencil["pencils"]) == pencil["rounds_requested"] == 4
        previous = classical["best_score"]
        for row in pencil["pencils"]:
            assert len(row["parameter_values"]) == len(row["scores"]) == 2048
            assert len(set(row["parameter_values"])) == 2048
            assert row["starting_score"] == row["scores"][0] == previous
            assert row["best_score"] == max(row["scores"]) >= previous
            assert row["winner_parameter"] in row["parameter_values"]
            pattern = row["fixed_line_character_pattern_certificate"]
            assert not pattern["failed_constant_blocks"]
            assert not pattern["conflicting_duplicate_square_class_blocks"]
            assert pattern["positive_count_is_not_an_efficient_finding_algorithm"]
            assert not pattern["independent_predicate_or_IID_public_input_assumption"]
            previous = row["best_score"]
        assert previous == pencil["best_score"]
        assert not pencil["fresh_full_fit_bound_applies_to_this_attack"]
        assert not pencil["finite_search_failure_is_a_hardness_certificate"]
        first_line = pencil["pencils"][0]
        assert first_line["fixed_line_character_pattern_certificate"] == pencil_pattern_certificate(
            problem.p, problem.m, first_line["norm_polynomials"], problem.signs,
            include_zero=problem.include_zero)
        if problem.n == 25:
            assert first_line["fixed_line_character_pattern_certificate"]["all_variable_nonzero_and_all_blocks_accepted_parameters_lower"] > 0


def test_source_provenance_and_same_input_replay_on_small_problems():
    report = json.loads(REPORT.read_text())
    assert report["source_sha256"] == hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()
    for name, digest in report["dependency_sha256"].items():
        assert digest == hashlib.sha256((module.ROOT / "theorems" / name).read_bytes()).hexdigest()
    p = instance(127, 6, 3, 9, 3, 13)
    assert attack(p, trials=4, repair_steps=3) == attack(p, trials=4, repair_steps=3)


def test_frobenius_norm_polynomials_descend_and_match_all_base_field_parameters():
    model = extension_model(7, 3)
    E = model["field"]
    pairs = [(E(0), E(0)), (E(0), E([1, 2, 3])), (E(2), E(3)),
             (E([1, 2, 3]), E([3, 1, 6])), (E([0, 0, 1]), E(0))]
    for a, b in pairs:
        poly, costs = norm_line_polynomial(model, a, b)
        for parameter in range(7):
            z = a*E(parameter) + b
            # Compute the determinant of multiplication-by-z independently of
            # the Frobenius product and the field's norm implementation.
            columns = [list(map(int, (z*E.gen() ** j).to_list())) for j in range(3)]
            matrix = [[(columns[j] + [0]*3)[i] for j in range(3)] for i in range(3)]
            determinant = sum((1 if permutation in ((0, 1, 2), (1, 2, 0), (2, 0, 1)) else -1)
                              * math.prod(matrix[i][permutation[i]] for i in range(3))
                              for permutation in product(range(3), repeat=3) if len(set(permutation)) == 3) % 7
            assert horner(7, list(map(int, poly.coeffs())), parameter) == determinant
            assert determinant == int(z.norm())
        assert costs["extension_frobenius_maps"] == (6 if a != 0 else 0)
        assert costs["extension_polynomial_products"] == (2 if a != 0 else 0)
    # Base-field a,b produce a repeated polynomial, not a squarefree one.
    repeated, _ = norm_line_polynomial(model, E(2), E(3))
    assert repeated == ring(7)([3, 2]) ** 3


@pytest.mark.parametrize("include_zero", [True, False])
def test_every_parameter_of_native_retained_value_pencils_is_independently_scored(include_zero):
    problem = instance(31, 8, 3, 10, 3, 5101, include_zero=include_zero)
    before = problem.specification()
    initial = attack(problem, trials=3, repair_steps=2)
    result = pencil_attack(problem, initial["best_polynomial_coefficients"], rounds=3, parameters=31)
    assert before == problem.specification()
    assert result == pencil_attack(problem, initial["best_polynomial_coefficients"], rounds=3, parameters=31)
    previous = initial["best_score"]
    for row in result["pencils"]:
        assert row["parameter_values"] == list(range(31))
        assert len(row["retained_scalar_indices"]) == problem.K - 1
        assert len(set(row["retained_scalar_indices"])) == problem.K - 1
        direction, base = row["direction_polynomial_coefficients"], row["base_polynomial_coefficients"]
        assert len(direction) == problem.K and direction[-1] == 1
        assert all(horner(problem.p, direction, problem.points[j]) == 0 for j in row["retained_scalar_indices"])
        for j, parameter in enumerate(row["parameter_values"]):
            coefficients = [((base[r] if r < len(base) else 0) + parameter*direction[r]) % problem.p
                            for r in range(problem.K)]
            flags = independent_score(problem, coefficients, row["retained_accepted_blocks"])
            assert sum(flags) == row["scores"][j]
            for record in row["norm_polynomials"]:
                value = horner(problem.p, record["norm_polynomial_coefficients"], parameter)
                hit = (pow(value, 15, 31) == (problem.signs[record["block"]] % 31)
                       or (include_zero and value == 0))
                assert hit == flags[record["block"]]
        assert row["starting_score"] == previous
        assert row["best_score"] == max(row["scores"]) >= previous
        previous = row["best_score"]
        constants = sum(record["constant_on_pencil"] for record in row["norm_polynomials"])
        costs = row["precomputation_and_evaluation_costs"]
        assert costs["base_field_Legendre_evaluations"] == constants + (problem.n - constants)*31
        assert costs["extension_norm_checks"] == constants + 2*(problem.n - constants)
        assert costs["extension_frobenius_maps"] == 2*problem.m*(problem.n - constants)
    assert not result["fresh_full_fit_bound_applies_to_this_attack"]
    assert not result["full_extension_field_table_or_extension_coefficient_relaxation"]
    assert not result["finite_search_failure_is_a_hardness_certificate"]
    assert not result["general_quadratic_system_solver_implemented"]
    assert result["source_rerolls"] == 0


@pytest.mark.parametrize("include_zero", [True, False])
def test_fixed_line_Weil_count_bound_against_full_parameter_enumeration(include_zero):
    model = extension_model(127, 3)
    E = model["field"]
    polynomials = [norm_line_polynomial(model, a, b)[0] for a, b in
                   ((E([1, 2, 3]), E([2, 0, 4])), (E(2), E(3)))]
    for count in (1, 2):
        rows = [{"norm_polynomial_coefficients": list(map(int, poly.coeffs()))}
                for poly in polynomials[:count]]
        for signs in product((-1, 1), repeat=count):
            certificate = pencil_pattern_certificate(127, 3, rows, signs, include_zero=include_zero)
            nonzero_good = 0
            for parameter in range(127):
                values = [horner(127, row["norm_polynomial_coefficients"], parameter) for row in rows]
                nonzero_good += all(value and (1 if pow(value, 63, 127) == 1 else -1) == sign
                                    for value, sign in zip(values, signs))
            lower = certificate["all_variable_nonzero_and_all_blocks_accepted_parameters_lower"]
            assert 0 < lower <= nonzero_good
            assert fraction(certificate["one_fresh_uniform_base_field_parameter_success_lower_exact"]) == Fraction(lower, 127)
            assert certificate["distinct_base_field_roots_subtracted"] == count - 1
            assert not certificate["independent_predicate_or_IID_public_input_assumption"]


def test_character_certificate_checks_duplicate_square_classes_conflicts_and_fixed_bad_blocks():
    R = ring(7)
    cube = R([1, 1]) ** 3
    rows = [{"norm_polynomial_coefficients": list(map(int, poly.coeffs()))}
            for poly in (cube, 3*cube)]
    consistent = pencil_pattern_certificate(7, 3, rows, (1, -1))
    assert consistent["number_of_distinct_variable_square_classes"] == 1
    assert not consistent["conflicting_duplicate_square_class_blocks"]
    assert consistent["all_variable_nonzero_and_all_blocks_accepted_parameters_lower"] == 3
    conflicting = pencil_pattern_certificate(7, 3, rows, (1, 1))
    assert conflicting["conflicting_duplicate_square_class_blocks"] == [1]
    assert conflicting["all_variable_nonzero_and_all_blocks_accepted_parameters_lower"] == 0
    constants = [{"norm_polynomial_coefficients": []}, {"norm_polynomial_coefficients": [3]}]
    assert pencil_pattern_certificate(7, 3, constants, (1, -1))["all_variable_nonzero_and_all_blocks_accepted_parameters_lower"] == 7
    strict = pencil_pattern_certificate(7, 3, constants, (1, -1), include_zero=False)
    assert strict["failed_constant_blocks"] == [0]
    assert strict["all_variable_nonzero_and_all_blocks_accepted_parameters_lower"] == 0
    with pytest.raises(ValueError, match="verified odd power"):
        pencil_pattern_certificate(7, 3, [{"norm_polynomial_coefficients": [0, 1, 0, 1]}], (1,))
    with pytest.raises(ValueError, match="odd norm degree"):
        pencil_pattern_certificate(7, 7, rows, (1, -1))


def test_pencil_budget_one_and_noncanonical_input_are_not_silently_relaxed():
    problem = instance(127, 6, 3, 10, 3, 5103)
    coefficients = [0]*problem.K
    result = pencil_attack(problem, coefficients, rounds=1, parameters=1)
    row = result["pencils"][0]
    assert row["parameter_values"] == [0]
    assert row["winner_polynomial_coefficients"] == coefficients
    assert row["starting_score"] == row["best_score"]
    with pytest.raises(ValueError, match="canonical polynomial"):
        pencil_attack(problem, [0]*(problem.K + 1))
    with pytest.raises(ValueError):
        pencil_attack(problem, coefficients, parameters=0)


@pytest.mark.parametrize("include_zero,expected", [(True, Fraction(16, 49)), (False, Fraction(9, 49))])
def test_population_law_matches_all_shift_pairs_but_never_becomes_a_restart_certificate(include_zero, expected):
    # A constant P=1 fits an anchored positive square at shift0. The other
    # TWO shifts, not algorithm restarts on a fixed source, vary independently.
    success = 0
    for t1, t2 in product(range(7), repeat=2):
        flags = []
        for shift, sign in ((t1, 1), (t2, -1)):
            z = (1 - shift) % 7
            symbol = 0 if z == 0 else (1 if pow(z, 3, 7) == 1 else -1)
            flags.append(symbol == sign or (include_zero and z == 0))
        success += all(flags)
    assert Fraction(success, 49) == expected
    result = population_tail(7, 3, 1, 1, 3, include_zero=include_zero, nonadaptive_trials=2)
    assert expected <= fraction(result["single_trial_tail_upper_128bit_dyadic"]) <= expected + Fraction(1, 1 << 128)
    assert 2*expected <= fraction(result["nonadaptive_union_upper_128bit_dyadic"])
    assert not result["fixed_input_or_independent_restarts_law"]
    assert not result["adaptive_block_exchange_covered"]


@pytest.mark.parametrize("include_zero", [True, False])
def test_fixed_input_joint_moments_and_actual_root_sampler_by_full_polynomial_enumeration(include_zero):
    p, n, K = 7, 6, 3
    points = [pow(3, j, p) for j in range(n)]
    shifts, signs, anchors = [0, 2, 3, 1, 5, 4], [1, -1, 1, -1, 1, -1], (0, 2, 4)
    rho = Fraction(p + (1 if include_zero else -1), 2*p)
    words, flags_by_coeff, anchor_values = {}, {}, {}
    for coefficients in product(range(p), repeat=K):
        values = [horner(p, coefficients, x) for x in points]
        flags = []
        for value, shift, sign in zip(values, shifts, signs):
            z = (value - shift) % p
            symbol = 0 if not z else (1 if pow(z, 3, p) == 1 else -1)
            flags.append(symbol == sign or (include_zero and not z))
        words[coefficients], flags_by_coeff[coefficients] = values, flags
        anchor_values[tuple(values[i] for i in anchors)] = coefficients
    assert len(anchor_values) == p ** K
    for size in range(n + 1):
        error = joint_acceptance_error(p, 1, K, size, include_zero=include_zero)
        for selected in combinations(range(n), size):
            actual = Fraction(sum(all(flags[i] for i in selected) for flags in flags_by_coeff.values()), p ** K)
            assert abs(actual - rho ** size) <= error
    accepted = [c for c, flags in flags_by_coeff.items() if all(flags[i] for i in anchors)]
    assert Fraction(len(accepted), p ** K) == rho ** len(anchors)
    free = [i for i in range(n) if i not in anchors]
    for r in range(1, len(free) + 1):
        actual_moment = Fraction(sum(math.comb(sum(flags_by_coeff[c][i] for i in free), r) for c in accepted), len(accepted))
        upper = math.comb(len(free), r)*(rho ** r + joint_acceptance_error(p, 1, K, len(anchors) + r, include_zero=include_zero)/rho ** len(anchors))
        assert actual_moment <= upper
    # Enumerate the IMPLEMENTED square-root sampler; do not silently treat
    # including-zero squares as uniform over the accepted set.
    counts = {c: 0 for c in words}
    roots = range(p) if include_zero else range(1, p)
    for chosen in product(roots, repeat=len(anchors)):
        targets = tuple((shifts[i] + (1 if signs[i] == 1 else 3)*root*root) % p
                        for i, root in zip(anchors, chosen))
        counts[anchor_values[targets]] += 1
    total = len(roots) ** len(anchors)
    tv = sum(abs(Fraction(counts[c], total) - (Fraction(1, len(accepted)) if c in accepted else 0)) for c in words) / 2
    certificate = fixed_input_fit_tail(p, n, 1, K, n, include_zero=include_zero)
    bias = fraction(certificate["root_square_sampler_TV_from_uniform_anchor_conditioning_upper_exact"])
    assert tv <= bias
    assert (tv > 0) == include_zero
    actual_tail = Fraction(sum(counts[c] for c, flags in flags_by_coeff.items() if all(flags)), total)
    assert actual_tail <= fraction(certificate["one_fresh_fit_success_upper_128bit_dyadic"])


def test_fixed_input_bound_uses_the_effective_fitted_dimension_and_handles_impossible_targets():
    left = fixed_input_fit_tail(19, 4, 3, 7, 4)
    right = fixed_input_fit_tail(19, 4, 3, 8, 4)
    assert left["effective_uniform_polynomial_dimension"] == right["effective_uniform_polynomial_dimension"] == 6
    assert left["scalar_degrees_unused"] == 1 and right["scalar_degrees_unused"] == 2
    assert left["checked_factorial_moment_bounds"] == right["checked_factorial_moment_bounds"]
    impossible = fixed_input_fit_tail(19, 4, 3, 7, 5)
    assert impossible["one_fresh_fit_success_upper_128bit_dyadic"] == "0"
    assert impossible["necessary_fits_for_half_success_in_this_sampling_class"] is None
    certain = fixed_input_fit_tail(19, 4, 3, 7, 2)
    assert certain["one_fresh_fit_success_upper_128bit_dyadic"] == "1"
    with pytest.raises(ValueError, match="distinct scalar"):
        fixed_input_fit_tail(7, 3, 3, 6, 3)
    with pytest.raises(ValueError, match="flat odd"):
        fixed_input_fit_tail(19, 4, 2, 4, 4)


def test_large_fixed_input_sampling_class_certificate_replays_without_IID_input_or_binomial_assumptions():
    record = json.loads(REPORT.read_text())["controls"][-1]["fixed_input_fresh_full_fit_sampling_bound"]
    assert record == fixed_input_fit_tail((1 << 61) - 1, 127, 31, 1550, 114)
    assert record["factorial_moment_witness"] == 49
    bound = fraction(record["one_fresh_fit_success_upper_128bit_dyadic"])
    assert 0 < bound < Fraction(9, 10 ** 9)
    count = record["necessary_fits_for_half_success_in_this_sampling_class"]
    assert count == 57356397
    assert (count - 1)*bound < Fraction(1, 2) <= count*bound
    assert fraction(record["union_success_upper_128bit_dyadic"]) >= min(1, 32*bound)
    # Reconstruct the SELECTED bound from its Fourier error, independently
    # of the implementation's search over candidate moment orders.
    Q, b, r, free, needed = ((1 << 61) - 1) ** 31, 50, 49, 77, 64
    rho = Fraction(Q + 1, 2*Q)
    H = math.isqrt(Q + 1) + int(math.isqrt(Q + 1) ** 2 != Q + 1)
    error = (rho + Fraction(H, 2)) ** (b + r) / Q ** b
    bias = Fraction(b*(Q - 1), Q*(Q + 1))
    exact = Fraction(math.comb(free, r), math.comb(needed, r))*(rho ** r + error/rho ** b) + bias
    assert exact <= bound <= exact + Fraction(1, 1 << 128)
    assert record["no_IID_public_shift_or_independent_restart_assumption"]
    assert not record["retained_anchor_block_exchange_or_other_adaptive_repairs_covered"]
    assert not record["all_classical_algorithms_or_general_norm_solvers_bounded"]
