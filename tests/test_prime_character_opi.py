"""Universal small-input power completion, native witnesses and coset escape guards."""
from dataclasses import replace
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path
import random

import pytest

from theorems.prime_character_opi import (
    REPORT, PrimeCharacterOPI, attack, complete_positions, from_specification, generator_valid,
    diagonal_system, instance, interpolate, quadratic_jet_attack, quantum_reference, repair_quadratic_jet,
    ring, root_at_infinity, strict_completion_controls, strict_root_zero_trap, verify_projective_witness,
)


@pytest.mark.parametrize("p,r,N,K", [(5, 2, 4, 2), (7, 3, 3, 2), (5, 4, 4, 3)])
def test_every_small_shift_vector_has_a_perfect_native_completion_at_the_proved_threshold(p, r, N, K):
    base = instance(p, N, K, r, 29, mode="global")
    for shifts in product(range(p), repeat=N):
        problem = replace(base, shifts=shifts)
        row = complete_positions(problem, tuple(range(N)))
        coefficients = tuple(map(int, row["polynomial_coefficients_decimal"]))
        assert row["status"] == "NATIVE_COMPLETION_WITNESS"
        assert problem.score_count(coefficients) == N
        assert row["degree"] < K
        assert row["formal_root_certificate"] is not None


@pytest.mark.parametrize("N,K,r,p", [(5, 3, 2, 101), (7, 4, 2, 101), (8, 6, 3, 103), (10, 9, 4, 101)])
def test_odd_lengths_padding_nontrivial_cosets_and_nonunit_leading_roots(N, K, r, p):
    problem = instance(p, N, K, r, 71, mode="global")
    for orientation in range(r):
        problem = replace(problem, orientations=(orientation,)*N)
        row = complete_positions(problem, tuple(range(N)), leading=7)
        coefficients = tuple(map(int, row["polynomial_coefficients_decimal"]))
        assert problem.score_count(coefficients) == N
        assert row["degree"] < (r-1)*((N+r-1)//r)
        assert row["formal_root_certificate"]["common_coset_orientation"] == orientation


def test_formal_square_root_matches_independent_FLINT_series_primitive():
    p, C, rng = 101, ring(101), random.Random(29)
    for D in (1, 2, 5, 12):
        F = C([rng.randrange(p) for _ in range(2*D)]+[1])
        R, record = root_at_infinity(p, F, 2, D)
        expected = F.reverse(degree=2*D).sqrt_trunc(D+1).reverse(degree=D)
        assert R == expected
        assert (R**2-F).degree() < D
        assert record["series_inverse_calls"] == len(record["truncation_precisions"])
    with pytest.raises(ValueError, match="invertible"):
        root_at_infinity(3, ring(3)([1, 0, 0, 1]), 3, 1)


def test_strict_common_cosets_solve_every_small_shift_vector_with_one_degree_slack():
    base = instance(5, 4, 3, 2, 29, mode="global", include_zero=False)
    for shifts in product(range(5), repeat=4):
        problem = replace(base, shifts=shifts)
        row = complete_positions(problem, (0, 1, 2, 3))
        coefficients = tuple(map(int, row["polynomial_coefficients_decimal"]))
        values = problem.evaluations(coefficients)
        assert problem.score_count(coefficients) == 4
        assert all(y != t for y, t in zip(values, shifts))
        assert row["degree"] < 3
        assert row["proved_degree_dimension_threshold"] == 3


@pytest.mark.parametrize("p,N,r", [(5, 4, 2), (7, 6, 3), (13, 8, 4), (17, 16, 8)])
def test_adversarial_exact_power_controls_need_an_actual_nonzero_root_shift(p, N, r):
    problem = strict_root_zero_trap(p, N, r)
    row = complete_positions(problem, tuple(range(N)))
    certificate, C = row["formal_root_certificate"], ring(p)
    base = C(list(map(int, certificate["base_root_polynomial_coefficients_decimal"])))
    final = C(list(map(int, certificate["root_polynomial_coefficients_decimal"])))
    shift = int(certificate["zero_avoidance_shift_decimal"])
    assert any(int(base(i+1)) == 0 for i in range(N))
    assert shift > 0
    assert final == base+shift
    assert all(int(final(i+1)) != 0 for i in range(N))
    assert certificate["zero_avoidance_root_evaluations_charged"] == N
    assert certificate["zero_avoidance_candidate_shifts_tested"] <= N+1
    assert certificate["series_congruence_applies_to_base_root"]
    assert certificate["candidate_shift_search_bounded_by_selected_points_plus_one"]
    assert not certificate["field_size_scan_required_for_zero_avoidance"]
    assert problem.score_count(tuple(map(int, row["polynomial_coefficients_decimal"]))) == N


@pytest.mark.parametrize("p,N,K,r", [(101, 5, 4, 2), (103, 8, 7, 3), (101, 11, 10, 4)])
def test_strict_padding_and_arbitrary_cosets_or_direct_nonzero_interpolation(p, N, K, r):
    base = instance(p, N, K, r, 71, mode="global", include_zero=False)
    for orientation in range(r):
        problem = replace(base, orientations=(orientation,)*N)
        row = complete_positions(problem, tuple(range(N)), leading=7)
        coefficients = tuple(map(int, row["polynomial_coefficients_decimal"]))
        assert problem.score_count(coefficients) == N
    arbitrary = replace(base, dimension=N, orientations=tuple(i % r for i in range(N)))
    row = complete_positions(arbitrary, tuple(range(N)))
    values = arbitrary.evaluations(tuple(map(int, row["polynomial_coefficients_decimal"])))
    assert values == tuple((t+arbitrary.multiplier(i)) % p for i, t in enumerate(arbitrary.shifts))
    assert row["score_count"] == N


def test_tight_strict_boundary_is_not_silently_claimed_universally_solvable():
    problem = replace(instance(5, 4, 2, 2, 29, mode="global", include_zero=False), shifts=(0, 0, 0, 1))
    scores = [problem.score_count(coefficients) for coefficients in product(range(5), repeat=2)]
    assert len(scores) == 25
    assert max(scores) < 4  # Complete native proof for THIS small boundary instance.
    result = complete_positions(problem, (0, 1, 2, 3))
    assert result["status"] == "NOT_APPLICABLE_DEGREE_BUDGET"
    assert not result["original_problem_unsatisfiable"]
    slack = replace(problem, dimension=3)
    assert complete_positions(slack, (0, 1, 2, 3))["score_count"] == 4
    with pytest.raises(ValueError, match="zero-including"):
        quadratic_jet_attack(problem, 29)
    # Strict generic attacks use the charged completion/direct baseline, not an invalid conic shortcut.
    row = attack(problem, 29, trials=2)
    assert len(row["trials"]) == 2
    assert row["adaptive_quadratic_jet_repair"] is None
    assert row["best_score_count"] < 4


def test_strict_density_input_conventions_and_quantum_reference_cannot_include_zero():
    base = instance(13, 4, 2, 2, 29, include_zero=False)
    for orientation in range(2):
        problem = replace(base, orientations=(orientation,)*4)
        assert sum(problem.accepted(0, x) for x in range(13)) == 6
        assert not problem.accepted(0, problem.shifts[0])
    assert base.density == Fraction(6, 13)
    assert quantum_reference(base)["density_lower"] == "6/13"
    assert from_specification(base.specification()) == base
    with pytest.raises(ValueError, match="Boolean"):
        replace(base, include_zero=0)
    with pytest.raises(ValueError, match="noncanonical"):
        from_specification(dict(base.specification(), include_zero=True))


@pytest.mark.parametrize("p,r", [(13, 2), (13, 3), (13, 4), (17, 8)])
def test_every_native_coset_list_has_the_exact_claimed_density(p, r):
    problem = instance(p, 4, 2, r, 29)
    for orientation in range(r):
        changed = replace(problem, orientations=(orientation,)*4)
        for i in range(4):
            assert sum(changed.accepted(i, y) for y in range(p)) == 1+(p-1)//r
            assert changed.accepted(i, changed.shifts[i])
    assert problem.density == Fraction(1+(p-1)//r, p)


def test_interpolation_and_native_integer_Horner_agree_on_arbitrary_selected_positions():
    p, positions, values = (1 << 61)-1, (2, 5, 9, 16), (7, 8, 99, 12345)
    T, V = interpolate(p, positions, values)
    assert T.degree() < len(positions)
    assert tuple(int(T(x)) for x in positions) == values
    assert all(int(V(x)) == 0 for x in positions)
    problem = instance(p, 16, 5, 2, 29)
    coefficients = tuple(map(int, T.coeffs()))
    assert problem.evaluations(coefficients) == tuple(int(T(x)) for x in range(1, 17))


def test_mixed_cosets_are_not_a_global_power_lift_or_a_hardness_certificate():
    base = instance(5, 4, 2, 2, 29)
    problem = replace(base, shifts=(0, 0, 0, 0), orientations=(0, 1, 0, 1))
    row = complete_positions(problem, (0, 1, 2, 3))
    assert row["status"] == "NOT_APPLICABLE_MIXED_POWER_COSETS"
    assert not row["original_problem_unsatisfiable"]
    # Different orientations do NOT establish hardness: zero residual is accepted.
    assert problem.score_count((0,)) == 4
    assert attack(problem, 29, trials=2)["best_score_count"] == 4
    row = complete_positions(replace(problem, orientations=(0,)*4, dimension=1), (0, 1, 2, 3))
    assert row["status"] == "NOT_APPLICABLE_DEGREE_BUDGET"
    assert not row["original_problem_unsatisfiable"]


def test_mixed_versus_global_sources_keep_identical_shifts_and_charge_every_restart():
    global_source = instance(65537, 16, 8, 2, 29, mode="global")
    mixed = instance(65537, 16, 8, 2, 29, mode="mixed")
    assert global_source.shifts == mixed.shifts
    assert global_source.coset_generator == mixed.coset_generator
    row = attack(mixed, 10029, trials=8)
    assert len(row["trials"]) == 16
    repair = row["adaptive_quadratic_jet_repair"]
    assert row["best_score_count"] == max(row["linear_interpolation_baseline"]["score_count"],
                                           max(t["score_count"] for t in row["trials"]), repair["score_count"])
    assert row["total_native_Horner_evaluations"] == 272+repair["native_Horner_evaluations"]
    assert not row["classical_hardness_inferred"]
    for trial in row["trials"]:
        coefficients = tuple(map(int, trial["polynomial_coefficients_decimal"]))
        values = mixed.evaluations(coefficients)
        assert trial["score_count"] == mixed.score_count(coefficients)
        assert all(mixed.accepted(i, values[i]) for i in trial["forced_positions"])


def test_full_dimension_direct_interpolation_handles_arbitrary_orientations():
    problem = instance(101, 7, 7, 2, 29, mode="mixed")
    row = attack(problem, 29, trials=2)
    assert row["best_score_count"] == 7
    assert all(t["formal_root_certificate"] is None for t in row["trials"] if t["mechanism"] == "power_completion")
    for trial in row["trials"]:
        assert trial["score_count"] == problem.length


def test_native_prime_field_and_specification_contracts_cannot_be_silently_relaxed():
    with pytest.raises(ValueError, match="prime field"):
        instance(9, 4, 2, 2, 29)
    with pytest.raises(ValueError, match="dividing"):
        instance(101, 4, 2, 3, 29)
    with pytest.raises(ValueError):
        instance(101, 4, 2, True, 29)
    problem = instance(101, 4, 2, 2, 29)
    assert generator_valid(101, 2, problem.coset_generator)
    assert from_specification(problem.specification()) == problem
    bad = problem.specification()
    bad["input_set_density"] = "1/2"
    with pytest.raises(ValueError, match="noncanonical"):
        from_specification(bad)
    reference = quantum_reference(problem)
    assert not reference["finite_success_probability_or_score_certificate_supplied"]
    assert not reference["coherent_capacity_list_decoder_compiled"]


def test_free_quadratic_jet_forces_both_cosets_without_changing_protected_degree():
    problem = instance((1 << 61)-1, 127, 77, 2, 29)
    row = quadratic_jet_attack(problem, 19029)
    coefficients = tuple(map(int, row["polynomial_coefficients_decimal"]))
    values = problem.evaluations(coefficients)
    assert row["extra_interpolated_positions"]
    assert not row["UNKNOWN_local_search_caps"]
    assert len(row["extra_interpolated_positions"]) == row["free_root_coefficients"]
    assert len(row["forced_positions"]) > problem.dimension
    assert row["degree"] < problem.dimension
    assert all(problem.accepted(i, values[i]) for i in row["forced_positions"])
    assert row["score_count"] == problem.score_count(coefficients)
    assert not row["source_rejected_or_resampled"]
    assert Fraction(row["IID_uniform_proposal_cap_union_bound"]) < Fraction(1, 10**30)
    assert row["native_membership_tests_including_forced_checks"] == (
        problem.length+len(row["forced_positions"])+row["local_random_root_proposals"])


def test_every_small_mixed_source_keeps_all_forced_constraints_and_native_degree():
    base = replace(instance(5, 4, 3, 2, 29), orientations=(0, 1, 0, 1))
    for shifts in product(range(5), repeat=4):
        problem = replace(base, shifts=shifts)
        row = quadratic_jet_attack(problem, 71)
        coefficients = tuple(map(int, row["polynomial_coefficients_decimal"]))
        values = problem.evaluations(coefficients)
        assert row["degree"] < 3
        assert not row["UNKNOWN_local_search_caps"]
        assert row["protected_high_root_coefficients"] == 0
        assert row["free_root_coefficients"] == 2
        assert all(problem.accepted(i, values[i]) for i in row["forced_positions"])
        assert row["score_count"] == problem.score_count(coefficients)


def test_even_root_degree_cancellation_and_odd_free_leading_coefficient_are_independent():
    for N in range(1, 9):
        for K in range(1, N+1):
            problem = instance(101, N, K, 2, 29)
            row = quadratic_jet_attack(problem, 71)
            p, C = problem.prime, ring(problem.prime)
            R0 = C(list(map(int, row["base_root_coefficients_decimal"])))
            L = C(list(map(int, row["root_perturbation_coefficients_decimal"])))
            assert L.degree() < row["free_root_coefficients"]
            assert ((R0+L)**2-R0**2).degree() < K
            assert problem.score_count(tuple(map(int, row["polynomial_coefficients_decimal"]))) == row["score_count"]


def test_local_quadratic_value_search_has_a_counting_guarantee_not_a_full_field_oracle():
    p = 13
    problem = instance(p, 3, 2, 2, 29)
    for orientation in range(2):
        changed = replace(problem, shifts=(0, 0, 0), orientations=(orientation,)*3)
        for beta in (1, problem.coset_generator):
            for a in range(1, p):
                assert sum(changed.accepted(0, (a+beta*z*z) % p) for z in range(p)) >= (p-1)//2


def test_jet_search_caps_are_unknown_and_do_not_reject_the_source_or_native_witness():
    problem = instance(65537, 16, 8, 2, 29)
    row = quadratic_jet_attack(problem, 29, max_root_trials=0)
    assert row["UNKNOWN_local_search_caps"]
    assert Fraction(row["IID_uniform_proposal_cap_union_bound"]) == 1
    assert not row["classical_hardness_inferred"]
    coefficients = tuple(map(int, row["polynomial_coefficients_decimal"]))
    assert row["score_count"] == problem.score_count(coefficients)
    with pytest.raises(ValueError, match="only for quadratic"):
        quadratic_jet_attack(instance(103, 8, 6, 3, 29), 29)


def test_diagonal_export_matches_native_polynomial_degree_for_all_small_root_vectors():
    problem = instance(7, 3, 2, 2, 29, mode="mixed")
    rows, targets = diagonal_system(problem)
    assert len(rows) == 1
    for roots in product(range(7), repeat=3):
        values = tuple((t+problem.multiplier(i)*z*z) % 7 for i, (t, z) in enumerate(zip(problem.shifts, roots)))
        Q, _ = interpolate(7, (1, 2, 3), values)
        equations_hold = all(sum(a*z*z for a, z in zip(row, roots)) % 7 == b for row, b in zip(rows, targets))
        assert equations_hold == (Q.degree() < problem.dimension)
        converted = verify_projective_witness(problem, roots)
        assert converted["native_solution"] == equations_hold


def test_adaptive_jet_repair_is_monotone_preserves_forced_constraints_and_charges_rejections():
    problem = instance(65537, 16, 8, 2, 29)
    initial = quadratic_jet_attack(problem, 10029)
    row = repair_quadratic_jet(problem, initial, 71, proposals_per_coordinate=8)
    assert row["score_count"] >= initial["score_count"]
    assert row["all_proposals_retained"]
    scores = [initial["score_count"]]
    for move in row["accepted_moves"]:
        coefficients = tuple(map(int, move["polynomial_coefficients_decimal"]))
        values = problem.evaluations(coefficients)
        assert all(problem.accepted(i, values[i]) for i in row["forced_positions"])
        assert problem.score_count(coefficients) == move["score_count"]
        assert move["score_count"] > scores[-1]
        scores.append(move["score_count"])
    assert row["score_count"] == scores[-1]
    feasible = sum(p["released_predicate_accepted"] for p in row["proposals"])
    assert row["native_Horner_evaluations"] == problem.length*(1+feasible)
    assert row["native_membership_tests"] == row["native_Horner_evaluations"]+len(row["proposals"])
    assert row == repair_quadratic_jet(problem, initial, 71, proposals_per_coordinate=8)


def test_adaptive_repair_transcript_replays_every_proposal_not_only_successful_moves():
    problem = instance(101, 8, 5, 2, 71)
    initial = quadratic_jet_attack(problem, 29)
    row = repair_quadratic_jet(problem, initial, 29, proposals_per_coordinate=4)
    C, p = ring(problem.prime), problem.prime
    positions, extras = tuple(initial["common_coset_positions"]), tuple(initial["extra_interpolated_positions"])
    T, V = interpolate(p, tuple(i+1 for i in positions), tuple(problem.shifts[i] for i in positions))
    leading = int(initial["base_formal_root_certificate"]["leading_root_decimal"])
    W = C.gen()**(2*initial["root_degree"]-len(positions))*V*(leading*leading % p)
    beta = problem.multiplier(positions[0])
    root = C(list(map(int, initial["base_root_coefficients_decimal"])))+C(list(map(int, initial["root_perturbation_coefficients_decimal"])))
    score = initial["score_count"]
    for proposal in row["proposals"]:
        e, delta = proposal["released_position"], int(proposal["delta_decimal"])
        basis, _ = interpolate(p, tuple(i+1 for i in extras), tuple(int(i == e) for i in extras))
        new_root = root+delta*basis
        Q = T+beta*(new_root**2-W)
        coefficients = tuple(map(int, Q.coeffs()))
        values = problem.evaluations(coefficients)
        accepted = tuple(problem.accepted(i, y) for i, y in enumerate(values))
        assert accepted[e] == proposal["released_predicate_accepted"]
        if not accepted[e]:
            assert proposal["proposed_score"] is None
        else:
            assert sum(accepted) == proposal["proposed_score"]
            assert all(accepted[i] for i in row["forced_positions"])
        improves = accepted[e] and sum(accepted) > score
        assert improves == proposal["strict_improvement_accepted"]
        if improves:
            root, score = new_root, sum(accepted)
    assert score == row["score_count"]
    assert list(map(str, root.coeffs())) == row["final_root_coefficients_decimal"]


def test_empty_proposal_pool_and_pass_caps_do_not_certify_a_local_optimum():
    problem = instance((1 << 61)-1, 127, 77, 2, 29)
    initial = quadratic_jet_attack(problem, 29)
    assert initial["score_count"] < problem.length
    empty = repair_quadratic_jet(problem, initial, 29, proposals_per_coordinate=0)
    assert empty["termination"] == "NO_SAMPLED_IMPROVEMENT"
    assert not empty["local_or_global_optimality_proved"]
    capped = repair_quadratic_jet(problem, initial, 29, max_passes=0)
    assert capped["termination"] == "UNKNOWN_PASS_CAP"
    assert not capped["local_or_global_optimality_proved"]
    assert capped["score_count"] == initial["score_count"]
    bad = dict(initial, polynomial_coefficients_decimal=["0"])
    with pytest.raises(ValueError, match="reconstruct"):
        repair_quadratic_jet(problem, bad, 29)
    with pytest.raises(ValueError, match="native score"):
        repair_quadratic_jet(problem, dict(initial, score_count=0), 29)


def test_chevalley_warning_homogenization_cannot_silently_return_a_point_at_infinity():
    problem = replace(instance(7, 3, 2, 2, 29), shifts=(0, 0, 1))
    # Homogeneous zero always passes equations; it must NOT become an affine witness.
    row = verify_projective_witness(problem, (0, 0, 0), homogenizer=0)
    assert row["status"] == "ZERO_VECTOR_IS_NOT_A_PROJECTIVE_POINT"
    assert not row["native_solution"]
    # A nonzero point at infinity also exists; its guarantee is still insufficient.
    point = next(z for z in product(range(7), repeat=3) if any(z)
                 and verify_projective_witness(problem, z, 0)["status"] == "POINT_AT_INFINITY_NOT_A_NATIVE_OPI_SOLUTION")
    assert any(point)


def test_projective_normalization_of_a_true_affine_solution_preserves_native_witness():
    problem = instance(7, 3, 2, 2, 29)
    roots = next(z for z in product(range(7), repeat=3) if verify_projective_witness(problem, z)["native_solution"])
    expected = verify_projective_witness(problem, roots)
    scaled = tuple(3*x % 7 for x in roots)
    assert verify_projective_witness(problem, scaled, homogenizer=3) == expected


def test_strict_diagonal_equations_also_require_nonzero_affine_roots():
    problem = replace(instance(7, 3, 2, 2, 29, mode="global", include_zero=False), shifts=(0, 0, 0))
    rows, targets = diagonal_system(problem)
    for roots in product(range(7), repeat=3):
        equations_hold = all(sum(a*z*z for a, z in zip(row, roots)) % 7 == b for row, b in zip(rows, targets))
        native = verify_projective_witness(problem, roots)
        assert native["native_solution"] == (equations_hold and all(roots))
        if equations_hold and not all(roots):
            assert native["status"] == "ZERO_AFFINE_ROOT_EXCLUDED_BY_STRICT_LISTS"


def test_artifact_keeps_all_sources_paid_trials_native_witnesses_and_exact_replay():
    if not REPORT.exists():
        pytest.fail("required native witness artifact has not been generated")
    report = json.loads(REPORT.read_text())
    assert report["source_sha256"] == hashlib.sha256(Path("theorems/prime_character_opi.py").read_bytes()).hexdigest()
    for name, digest in report["dependency_sha256"].items():
        assert digest == hashlib.sha256((Path("theorems")/name).read_bytes()).hexdigest()
    assert not report["accepted_speedup_candidate"]
    assert not report["mixed_cosets_proved_classically_hard"]
    assert len(report["instances"]) == 24
    assert report["strict_common_coset_controls"] == strict_completion_controls()
    assert len(report["strict_common_coset_controls"]) == 10
    for row in report["strict_common_coset_controls"]:
        problem = from_specification(row["specification"])
        assert not problem.include_zero
        assert problem.score_count(tuple(map(int, row["completion"]["polynomial_coefficients_decimal"]))) == problem.length
    for row in report["instances"]:
        problem = from_specification(row["specification"])
        assert attack(problem, row["public_seed"]+10000) == row["paid_power_completion"]
        assert quantum_reference(problem) == row["published_quantum_reference_not_finite_certificate"]
