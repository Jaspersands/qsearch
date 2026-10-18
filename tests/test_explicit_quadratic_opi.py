"""Native-field witnesses, exact score-law controls and random-subspace bound."""
from fractions import Fraction
import hashlib
from itertools import product
import json
from math import comb
from pathlib import Path

import pytest

from theorems.explicit_quadratic_opi import (
    OPIReferenceLimit, REPORT, QuadraticOPI, _affine_words, _accepted_message,
    affine_flat_attack, evaluation_masks,
    exact_small_filter_law, field, filter_bound, fixed_flat_attack, flat_rank_failure_bound,
    from_specification, instance, repair_flat_attack, restarted_flat_attack, smt_attack,
)
from theorems.bpqm_gibbs_frontier import affine_system
from theorems.linear_erasure_prange_duality import null_basis


@pytest.mark.parametrize("bits", [3, 5, 7])
def test_every_compact_predicate_is_balanced_with_maximal_quadratic_polar_rank(bits):
    problem = instance(bits, 3, 29)
    q = 1 << bits
    for position in (0, 1, problem.length-1):
        assert sum(problem.accepted(position, y) for y in range(q)) == q//2
        h = [int(not problem.accepted(position, y)) for y in range(q)]
        polar = tuple(sum((h[(1 << i) ^ (1 << j)] ^ h[1 << i] ^ h[1 << j] ^ h[0]) << j
                          for j in range(bits)) for i in range(bits))
        assert affine_system(tuple((row, 0) for row in polar), bits)["rank"] == bits-1


def test_binary_linear_forms_agree_with_independent_FLINT_Horner_evaluation():
    problem = instance(3, 3, 71)
    linear = evaluation_masks(3, 3)
    for word in range(512):
        values = problem.evaluations(word)
        for position, symbol in enumerate(values):
            predicted = sum(((mask & word).bit_count() % 2) << b for b, mask in enumerate(linear[position]))
            assert predicted == symbol
            z = [(mask & word).bit_count() % 2 for mask in problem.forms[position]]
            assert problem.accepted(position, symbol) == (z[0] ^ (z[1]*z[2]) ^ problem.offsets[position] == 0)
            assert _accepted_message(problem.forms[position], problem.offsets[position], word) == problem.accepted(position, symbol)


@pytest.mark.parametrize("seed", [29, 71])
def test_affine_attack_solutions_satisfy_the_native_not_a_relaxed_problem(seed):
    problem = instance(5, 9, seed)
    report = affine_flat_attack(problem, seed+10000)
    word = int(report["message_hex"], 16)
    assert report["score_count"] == problem.score_count(word)
    values = problem.evaluations(word)
    assert all(problem.accepted(i, values[i]) for i in report["forced_positions"])
    assert len(report["forced_positions"]) == 15
    assert report["linear_system_solves"] >= 15
    assert report["native_field_polynomial_evaluations"] == 31
    assert report["instance_rejected_or_resampled"] is False


def test_paid_restarts_charge_every_attempt_and_choose_using_full_native_score():
    problem = instance(3, 3, 29)
    report = restarted_flat_attack(problem, 997, restarts=8)
    assert len(report["trials"]) == 8
    assert report["score_count"] == max(t["score_count"] for t in report["trials"])
    assert report["total_native_field_polynomial_evaluations"] == 56
    assert report["total_linear_system_solves"] == sum(t["linear_system_solves"] for t in report["trials"])
    assert report["better_than_quantum_expected_score_proves_asymptotic_dequantization"] is False


def test_released_RREF_neighborhood_enumeration_is_complete_and_unique():
    equations = ((0b1011, 1), (0b0110, 0))
    system = affine_system(equations, 4)
    actual = list(_affine_words(system, 4, 4))
    expected = [x for x in range(16) if all((x & h).bit_count() % 2 == b for h, b in equations)]
    assert len(actual) == len(set(actual)) == 1 << len(system["free"])
    assert sorted(actual) == expected
    with pytest.raises(OPIReferenceLimit, match="UNKNOWN"):
        list(_affine_words(system, 4, 1))


def test_repair_moves_preserve_the_actual_nonlinear_prefix_and_charge_enumeration():
    problem = instance(3, 3, 29)
    initial = affine_flat_attack(problem, 10029)
    report = repair_flat_attack(problem, int(initial["message_hex"], 16), tuple(initial["forced_positions"]), 30029)
    word = int(report["message_hex"], 16)
    assert report["score_count"] >= initial["score_count"]
    assert report["score_count"] == problem.score_count(word)
    assert report["candidate_words_enumerated"] > 0
    assert report["linear_neighborhood_solves"] > 0
    values = problem.evaluations(word)
    assert all(problem.accepted(i, values[i]) for i in initial["forced_positions"])
    previous = initial["score_count"]
    for move in report["improvement_trace"]:
        assert move["score_count"] > previous
        assert problem.score_count(int(move["message_hex"], 16)) == move["score_count"]
        previous = move["score_count"]
    assert report["global_optimum_or_polynomial_success_guaranteed"] is False
    assert report["uncapped_local_fixed_point_reached"] is True
    assert report["passes_executed"] <= problem.length-report["initial_score_count"]+1


def test_large_neighborhood_is_UNKNOWN_not_a_classical_hardness_result():
    problem = instance(3, 1, 29)
    initial = next(word for word in range(8) if problem.accepted(0, problem.evaluations(word)[0]))
    report = repair_flat_attack(problem, initial, (0,), 29, max_free_bits=1)
    assert report["skipped_UNKNOWN_dimension_caps"] == 1
    assert report["uncapped_local_fixed_point_reached"] is False
    assert int(report["message_hex"], 16) == initial
    assert report["global_optimum_or_polynomial_success_guaranteed"] is False
    with pytest.raises(ValueError):
        repair_flat_attack(problem, initial, (0, 0), 29)


@pytest.mark.parametrize("seed", [29, 71])
def test_ideal_small_filter_normalization_and_mean_match_the_strict_DQI_score_law(seed):
    problem = instance(3, 3, seed)
    report, law = filter_bound(problem), exact_small_filter_law(problem)
    assert report["degree"] == 1
    assert sum(law["message_score_histogram"]) == 512
    assert law["normalization"] == pytest.approx(1, abs=2e-12)
    assert float(Fraction(report["expected_score_lower"]))-2e-12 <= law["mean_score"]
    assert law["mean_score"] <= float(Fraction(report["expected_score_upper"]))+2e-12
    assert Fraction(report["expected_score_upper"])-Fraction(report["expected_score_lower"]) < Fraction(1, 1 << 70)
    assert report["coherent_RS_decoder_and_filter_circuit_executed"] is False
    assert report["oracle_classical_lower_bound_transferred_to_explicit_predicates"] is False


def test_distance_condition_is_strict_not_an_off_by_one_decoding_claim():
    with pytest.raises(ValueError, match="strict"):
        filter_bound(instance(3, 2, 29), degree=1)
    with pytest.raises(OPIReferenceLimit, match="UNKNOWN"):
        exact_small_filter_law(instance(5, 9, 29))


def test_MDS_rank_union_bound_covers_exact_enumeration_of_all_small_subspaces():
    # All seven 2D subspaces of F2^3, independently at three RS positions.
    spaces = [null_basis((normal,), 3) for normal in range(1, 8)]
    evaluations = evaluation_masks(3, 2)
    failures = 0
    for choices in product(spaces, repeat=3):
        rows = []
        for position, local in enumerate(choices):
            for vector in local:
                mask = 0
                for bit in range(3):
                    if (vector >> bit) & 1:
                        mask ^= evaluations[position][bit]
                rows.append((mask, 0))
        failures += affine_system(tuple(rows), 6)["rank"] < 6
    assert Fraction(failures, 343) == Fraction(175, 343)
    bound = flat_rank_failure_bound(3, 2, 3)
    assert Fraction(bound["raw_MDS_union_bound"]) == Fraction(27, 49)
    assert Fraction(failures, 343) <= Fraction(bound["rank_failure_probability_upper"])


def test_high_rate_perfect_flat_solutions_have_a_scoped_probability_bound():
    report = flat_rank_failure_bound(7, 90)
    assert Fraction(report["rank_failure_probability_upper"]) < Fraction(1, 1 << 100)
    assert report["rank_failure_probability_power_two_upper_exponent"] >= 100
    assert report["requires_independent_uniform_GL_predicate_transforms"] is True
    assert report["seeded_trials_are_not_an_IID_probability_certificate"] is True
    assert report["proves_classical_ease_for_every_OPI_family"] is False
    assert flat_rank_failure_bound(3, 3, 3)["rank_failure_probability_upper"] == "0"


def test_fixed_flat_failure_does_not_claim_OPI_unsatisfiability():
    problem = instance(3, 3, 29)
    report = fixed_flat_attack(problem)
    assert report["linear_system_solves"] == 1
    assert report["original_OPI_unsatisfiable_claimed"] is False
    assert report["status"] == "THIS_FIXED_FLAT_IS_INCONSISTENT"
    assert any(problem.score_count(word) == 7 for word in range(512))
    if report["message_hex"] is not None:
        assert problem.score_count(int(report["message_hex"], 16)) == 7


def test_dense_symmetric_cubic_is_not_an_automatic_escape_from_affine_flats():
    # In the Boolean quotient, e3=e1*e2, so the parity-zero hyperplane kills it.
    for width in (4, 6, 8):
        for word in range(1 << width):
            weight = word.bit_count()
            e1 = weight % 2
            e2 = comb(weight, 2) % 2 if weight >= 2 else 0
            e3 = comb(weight, 3) % 2 if weight >= 3 else 0
            assert e3 == e1*e2
            if e1 == 0:
                assert e3 == 0


def test_optional_SMT_witness_is_checked_and_limits_do_not_mean_hardness():
    problem = instance(3, 3, 29)
    report = smt_attack(problem)
    assert report["hardness_evidence"] is False
    if report["status"] == "SAT":
        assert problem.score_count(int(report["message_hex"], 16)) == 7
    else:
        assert report["status"] in ("UNKNOWN", "UNKNOWN_SOLVER_UNAVAILABLE")


def test_canonical_inputs_and_saved_field_basis_are_enforced():
    problem = instance(3, 3, 29)
    spec = problem.specification()
    assert from_specification(spec) == problem
    spec["field_modulus_coefficients"] = [1, 1, 1, 1]
    with pytest.raises(ValueError, match="basis changed"):
        from_specification(spec)
    for bad in (True, 2, 4, 3.0):
        with pytest.raises(ValueError):
            instance(bad, 3, 29)
    with pytest.raises(ValueError):
        affine_flat_attack(problem, True)


def test_live_artifact_source_deterministic_baselines_and_all_saved_witnesses():
    artifact = json.loads(REPORT.read_text())
    assert artifact["source_sha256"] == hashlib.sha256(Path("theorems/explicit_quadratic_opi.py").read_bytes()).hexdigest()
    for name, digest in artifact["dependency_sha256"].items():
        assert digest == hashlib.sha256((Path("theorems")/name).read_bytes()).hexdigest()
    assert artifact["oracle_problem_generated"] is False
    assert artifact["retracted_max_QUADSAT_state_preparation_used"] is False
    assert artifact["accepted_speedup_candidate"] is False
    assert len(artifact["instances"]) == 8
    for row in artifact["instances"]:
        problem = from_specification(row["specification"])
        assert affine_flat_attack(problem, row["public_seed"]+10000) == row["affine_flat_attack"]
        assert filter_bound(problem) == row["known_quantum_filter_bound"]
        assert fixed_flat_attack(problem) == row["fixed_zero_flat_attack"]
        for trial in row["restarted_affine_flat_attack"]["trials"]:
            assert problem.score_count(int(trial["message_hex"], 16)) == trial["score_count"]
        initial = row["restarted_affine_flat_attack"]
        forced = tuple(initial["trials"][initial["best_trial_index"]]["forced_positions"])
        repaired = repair_flat_attack(problem, int(initial["message_hex"], 16), forced, row["public_seed"]+30000)
        assert repaired == row["repaired_affine_flat_attack"]
        assert problem.score_count(int(repaired["message_hex"], 16)) == repaired["score_count"]
        for move in repaired["improvement_trace"]:
            assert problem.score_count(int(move["message_hex"], 16)) == move["score_count"]
        smt = row["SMT_all_constraints_attack"]
        assert smt["hardness_evidence"] is False
        if smt["status"] == "SAT":
            assert problem.score_count(int(smt["message_hex"], 16)) == problem.length
    control = artifact["predeclared_high_rate_control"]
    problem = from_specification(control["specification"])
    report = fixed_flat_attack(problem)
    assert report == control["fixed_zero_flat_attack"]
    assert report["full_row_rank"] is True
    assert problem.score_count(int(report["message_hex"], 16)) == 127
