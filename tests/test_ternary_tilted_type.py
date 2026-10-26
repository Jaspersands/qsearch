from fractions import Fraction
from itertools import product

import numpy as np
import pytest

from theorems.ternary_tilted_type import (
    finite_coherent_control, local_receiver, projected_solution,
    receiver_unitary, relinearize, simplex_calibration, square_basis,
    tilt, tilted_budget, weighted_kernel_mass,
)
from theorems.ternary_type_transfer import (
    counts_from_profiles, rowspace_profiles, transfer_budget,
)


def rational(record):
    return Fraction(record["numerator"], record["denominator"])


@pytest.mark.parametrize("p", [Fraction(1, 8), Fraction(1, 3), Fraction(1, 2),
                              Fraction(2, 3), Fraction(7, 8)])
def test_local_receiver_is_unitary_completion_with_exact_outcome_law(p):
    receiver, unitary = local_receiver(p), receiver_unitary(p)
    np.testing.assert_allclose(receiver.conj().T @ receiver, np.eye(2), atol=1e-14)
    np.testing.assert_allclose(unitary.conj().T @ unitary, np.eye(4), atol=1e-14)
    np.testing.assert_allclose(unitary[:, :2], receiver, atol=1e-14)
    omega, q = np.exp(2j*np.pi/3), min(p, 1-p)
    for c in range(3):
        state = np.array([np.sqrt(float(p))*omega**c,
                          np.sqrt(float(1-p))*omega**(-c)])
        expected = [0 if a == c else float(q) for a in range(3)] + [float(1-2*q)]
        np.testing.assert_allclose(abs(receiver @ state)**2, expected, atol=1e-14)


@pytest.mark.parametrize("p", [0, 1, -1, 2])
def test_deterministic_or_invalid_tilts_are_not_quantum_candidates(p):
    with pytest.raises(ValueError):
        tilt(p)


def test_projected_uniqueness_does_not_require_auxiliary_uniqueness():
    result = projected_solution(((1, 0),), (2,), variables=2, projected=1)
    assert result["value"] == (2,)
    assert result["free_variables"] == 1
    assert result["projection_unique"]
    assert not projected_solution(((1, 1),), (2,), variables=2,
                                  projected=1)["projection_unique"]
    assert not projected_solution(((0, 0),), (1,), variables=2,
                                  projected=1)["consistent"]
    assert not projected_solution((), (), variables=2, projected=1)["projection_unique"]


def test_actual_schur_decoder_accepts_free_auxiliary_component():
    rows = ((1, 1, 0, 0, 1), (0, 0, 1, 1, 1))
    result = relinearize(rows, (1, 2, 1, 2, 3))
    assert len(square_basis(rows)) == 3
    assert result["projection_unique"] and result["value"] == (0, 0)
    assert result["free_variables"] == 1
    assert result["conclusive_coordinates"] == 4


@pytest.mark.parametrize("p", [Fraction(1, 4), Fraction(1, 3), Fraction(1, 2)])
def test_exact_repetition_decoder_census_keeps_erasure_cost(p):
    m, q = 4, min(p, 1-p)
    row = (1,)*m
    declared_failure = Fraction(0)
    for outcome in product((1, 2, 3), repeat=m):
        probability = q**(m-outcome.count(3))*(1-2*q)**outcome.count(3)
        result = relinearize((row,), outcome)
        if result["projection_unique"]:
            assert result["value"] == (0,)
        else:
            declared_failure += probability
    assert declared_failure == 2*(1-q)**m-(1-2*q)**m
    assert declared_failure <= 3**2*(1-q)**m
    assert not relinearize((row,), (3,)*m)["projection_unique"]
    if p != Fraction(1, 2):
        assert declared_failure > Fraction(2, 2**m)


def test_projected_linear_solver_matches_all_small_affine_systems():
    rows = tuple(product(range(3), repeat=2))
    for left in rows:
        for right in rows:
            for rhs in product(range(3), repeat=2):
                solutions = [x for x in rows
                             if all(sum(a*b for a, b in zip(row, x)) % 3 == v
                                    for row, v in zip((left, right), rhs))]
                result = projected_solution((left, right), rhs, variables=2, projected=1)
                projections = {x[0] for x in solutions}
                assert result["consistent"] == bool(solutions)
                assert result["projection_unique"] == (len(projections) == 1)
                if result["projection_unique"]:
                    assert result["value"] == (next(iter(projections)),)


@pytest.mark.parametrize("rows,outcomes", [
    ((), ()), (((0, 0),), (1, 2)), (((1, 2), (1, 2)), (1, 2)),
    (((1, 2),), (1,)), (((1, 2),), (1, 4)),
])
def test_decoder_rejects_missing_or_invalid_source_data(rows, outcomes):
    with pytest.raises(ValueError):
        relinearize(rows, outcomes)


@pytest.mark.parametrize("p", [Fraction(1, 3), Fraction(1, 2), Fraction(3, 4)])
def test_exact_tilted_character_sum_matches_direct_kernel_census(p):
    rows = ((1, 1, 2, 2), (0, 1, 0, 1))
    profiles = rowspace_profiles(rows)["profiles"]
    brute = sum((p**word.count(1)*(1-p)**word.count(-1)
                 for word in product((1, -1), repeat=4)
                 if all(sum(a*b for a, b in zip(row, word)) % 3 == 0 for row in rows)),
                Fraction(0))
    assert weighted_kernel_mass(profiles, p) == brute
    for h in range(5):
        count = counts_from_profiles(profiles, h)["fixed_type"]
        brute_type = sum(word.count(1) == h and
                         all(sum(a*b for a, b in zip(row, word)) % 3 == 0 for row in rows)
                         for word in product((1, -1), repeat=4))
        assert count == brute_type


def test_unequal_character_pair_bound_on_full_phase_grid():
    for p in (Fraction(1, 8), Fraction(1, 3), Fraction(1, 2), Fraction(4, 5)):
        for angle in np.linspace(0, 2*np.pi, 1001):
            factors = [abs(float(1-p)+float(p)*np.exp(1j*(angle+4*np.pi*a/3)))
                       for a in range(3)]
            for a in range(3):
                for b in range(a):
                    assert factors[a]*factors[b] <= float(1-p*(1-p))+1e-14


@pytest.mark.parametrize("decoder", ["relinearize", "zero"])
def test_executed_coherent_transfer_includes_workspace_and_failures(decoder):
    result = finite_coherent_control(decoder=decoder)
    assert result["physical_dimension_including_work"] == 256
    assert result["all_failure_and_workspace_branches_retained"]
    assert sum(result["actual_output_probabilities"]) == pytest.approx(1)
    assert result["actual_to_unnormalized_ideal_norm"] <= (
        2*np.sqrt(3*result["average_decoder_error"])+1e-12)
    if decoder == "zero":
        words = tuple(product((1, -1), repeat=4))
        product_law = [float(Fraction(1, 3)**w.count(1)*Fraction(2, 3)**w.count(-1))
                       for w in words]
        np.testing.assert_allclose(result["actual_output_probabilities"], product_law,
                                   atol=1e-14)
        assert result["actual_tv_to_weighted_kernel"] == pytest.approx(float(Fraction(16, 27)))


def test_balanced_case_recovers_previous_ledger_with_outward_rounding():
    previous = transfer_budget(728, 6, 21, 485)
    current = tilted_budget(728, 6, 21, 485, 364)
    assert current["base_sampler_call_cap"] == previous["bounded_base_sampler_calls"]
    assert rational(current["decoder_failure_upper"]) >= rational(
        previous["base_decoder_failure_upper"])
    assert abs(rational(current["ideal_acceptance_lower"]) -
               rational(previous["ideal_acceptance_lower"])) < Fraction(1, 2**180)


def test_native_rare_type_becomes_polynomial_mass_but_is_classically_easy():
    calibration = simplex_calibration()
    budget = calibration["budget"]
    assert rational(calibration["uniform_acceptance"]) < Fraction(1, 10**19)
    assert Fraction(3, 100) < rational(calibration["tilted_acceptance"]) < Fraction(4, 100)
    assert budget["base_sampler_call_cap"] == 1277
    assert budget["cap_failure_bound_applicable"]
    assert calibration["constant_constraint_rhs"] == 1
    assert calibration["homogeneous_constant_row_would_be_incompatible"]
    assert calibration["classical_syndrome_states"] == budget["length"]+1
    assert not calibration["native_quantum_circuit_executed"]
    assert not calibration["advantage_evidence"]
    assert rational(budget["verified_acceptance_lower"]) <= rational(
        calibration["tilted_acceptance"])
    assert rational(budget["verified_acceptance_lower"])*budget["base_sampler_call_cap"] >= 40


def test_extreme_tilt_and_large_circuit_error_do_not_get_unpaid_acceptance():
    extreme = tilted_budget(728, 6, 21, 485, 1)
    noisy = tilted_budget(728, 6, 21, 485, 243, circuit_tv_budget=1)
    for result in (extreme, noisy):
        assert result["base_sampler_call_cap"] is None
        assert not result["cap_failure_bound_applicable"]
        assert rational(result["verified_acceptance_lower"]) == 0


@pytest.mark.parametrize("args", [(8, 2, 3, 5, 0), (8, 2, 3, 5, 8),
                                 (8, 2, 3, 0, 3), (8, 2, 4, 5, 3)])
def test_budget_rejects_invalid_premises(args):
    with pytest.raises(ValueError):
        tilted_budget(*args)
