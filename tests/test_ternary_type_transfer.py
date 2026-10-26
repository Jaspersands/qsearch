from collections import Counter
from fractions import Fraction
from itertools import product
import json
from math import comb

import numpy as np
import pytest

from theorems import ternary_type_transfer as transfer


def fraction(record):
    return Fraction(record["numerator"], record["denominator"])


@pytest.mark.parametrize("counts", ((4, 0, 0), (1, 2, 2), (0, 4, 1), (2, 1, 3)))
def test_type_character_against_independent_enumeration(counts):
    labels = tuple(a for a, count in enumerate(counts) for _ in range(count))
    m = len(labels)
    for h in range(m+1):
        residues = Counter(sum(a*y for a, y in zip(labels, signs)) % 3
                           for signs in product((-1, 1), repeat=m) if signs.count(1) == h)
        expected = (residues[0]-residues[2], residues[1]-residues[2])
        assert transfer.type_character(counts, h) == expected


@pytest.mark.parametrize("rows", (((1, 1, 2, 2),),
                                 ((1, 0, 1, 2, 1, 0), (0, 1, 1, 1, 2, 2)),
                                 ((1, 1, 1, 1), (0, 1, 2, 1))))
def test_complete_code_counts_against_brute_force(rows):
    data = transfer.rowspace_profiles(rows)
    words = [s for s in product((1, 2), repeat=len(rows[0]))
             if all(sum(a*b for a, b in zip(row, s)) % 3 == 0 for row in rows)]
    for h in range(len(rows[0])+1):
        counts = transfer.counts_from_profiles(data["profiles"], h)
        assert counts == {"full_support": len(words), "fixed_type": sum(s.count(1) == h for s in words)}


def test_balanced_charge_makes_constant_codewords_indistinguishable():
    m = 6
    omega = np.exp(2j*np.pi/3)
    words = [y for y in product((-1, 1), repeat=m) if sum(y) == 0]
    c = (0, 1, 2, 0, 2, 1)
    original = np.asarray([omega**(sum(a*b for a, b in zip(c, y)) % 3) for y in words])
    for shift in (1, 2):
        changed = np.asarray([omega**(sum((a+shift)*b for a, b in zip(c, y)) % 3) for y in words])
        assert np.max(abs(original-changed)) < 1e-12
    # A decoder cannot identify three equiprobable identical states with success >1/3.
    assert Fraction(1, 3) < Fraction(2, 3)


def test_local_unambiguous_measurement_fails_on_type_state():
    # Two-coordinate balanced state, in the +/- basis. Each local marginal
    # is I/2, unlike the pure product state used by the published decoder.
    product_plus = np.ones(2)/np.sqrt(2)
    forbidden = np.asarray((1, -1))/np.sqrt(2)
    effect = Fraction(2, 3)*np.outer(forbidden, forbidden)
    assert abs(float(product_plus @ effect @ product_plus)) < 1e-12
    assert float(np.trace(np.eye(2)/2 @ effect)) == pytest.approx(1/3)


@pytest.mark.parametrize("counts", ((2, 2, 2), (1, 4, 3), (6, 1, 1), (0, 5, 5)))
def test_uniform_type_character_bound(counts):
    m, r = sum(counts), min(sum(counts)//2, sum(counts)-max(counts))
    bound = 2**m*Fraction(3, 4)**r
    for h in range(m+1):
        a, b = transfer.type_character(counts, h)
        # |a+b omega|^2=a^2-a*b+b^2, exactly.
        assert a*a-a*b+b*b <= bound*bound


def test_simplex_profiles_distance_and_type_count():
    calibration = transfer.simplex_calibration(2)
    data = transfer.rowspace_profiles(calibration["quotient_rows"])
    assert data["profiles"] == {(8, 0, 0): 1, (2, 3, 3): 8}
    assert not data["constant_in_rowspace"]
    assert data["distance_to_constants"] == 5
    full_data = transfer.rowspace_profiles(calibration["full_constraint_matrix"])
    assert full_data["constant_in_rowspace"]
    assert full_data["distance_to_constants"] == 0
    # Balanced signs automatically satisfy the dropped all-ones constraint.
    assert transfer.counts_from_profiles(full_data["profiles"], 4)["fixed_type"] == calibration["exact_counts"]["fixed_type"]


def test_quotient_removes_actual_gram_degeneracy_not_just_a_label():
    data = transfer.simplex_calibration(2)
    signs = np.asarray([y for y in product((-1, 1), repeat=8) if sum(y) == 0])
    omega = np.exp(2j*np.pi/3)

    def gram(rows):
        coefficients = np.asarray(tuple(product(range(3), repeat=len(rows))))
        codewords = coefficients @ np.asarray(rows) % 3
        states = omega**(codewords @ signs.T % 3)/np.sqrt(len(signs))
        return states @ states.conj().T

    reduced = gram(data["quotient_rows"])
    expected = np.full((9, 9), -1/35)
    np.fill_diagonal(expected, 1)
    assert np.max(abs(reduced-expected)) < 1e-12
    assert np.linalg.matrix_rank(reduced, tol=1e-10) == 9
    full = gram(data["full_constraint_matrix"])
    assert full.shape == (27, 27)
    assert np.linalg.matrix_rank(full, tol=1e-10) == 9


def test_rejection_amplifies_distribution_error_and_all_calls_are_charged():
    # Uniform support of size 10, acceptance on first 2. Move eta=1/20
    # from one accepted outcome to a rejected outcome.
    ideal = [Fraction(1, 10)]*10
    actual = ideal.copy()
    actual[0] -= Fraction(1, 20)
    actual[-1] += Fraction(1, 20)
    eta = sum(abs(a-b) for a, b in zip(actual, ideal))/2
    p, observed = sum(ideal[:2]), sum(actual[:2])
    post_tv = sum(abs(actual[i]/observed-ideal[i]/p) for i in range(2))/2
    assert observed == p-eta
    assert post_tv > eta
    assert post_tv <= eta/(p-eta)


def test_executed_coherent_transfer_and_broken_decoder():
    valid = transfer.finite_erasure_control()
    broken = transfer.finite_erasure_control(decoder="zero")
    assert valid["all_failure_branches_retained"]
    assert valid["unnormalized_ideal_norm_squared"] == pytest.approx(9/8)
    assert valid["actual_output_tv_to_uniform_solutions"] < valid["tv_upper"] < 1
    assert valid["actual_verified_balanced_probability"] >= valid["ideal_balanced_probability"]-valid["tv_upper"]
    assert sum(valid["actual_output_probabilities"]) == pytest.approx(1)
    assert broken["actual_output_probabilities"] == pytest.approx([1/16]*16)
    assert broken["actual_output_tv_to_uniform_solutions"] == pytest.approx(5/8)
    assert broken["actual_verified_balanced_probability"] == pytest.approx(1/4)
    assert not valid["scalable_decoder_implemented"]


@pytest.mark.parametrize("value", (0, 1, Fraction(1, 9), Fraction(2, 7), Fraction(1, 2**500)))
def test_outward_square_root(value):
    upper = transfer.sqrt_upper(value)
    assert upper*upper >= value
    assert upper == 0 or (upper-Fraction(1, 2**256))**2 < value


def test_small_parameters_do_not_certify_a_sampler():
    budget = transfer.transfer_budget(8, 2, 3, 5)
    assert fraction(budget["verified_acceptance_lower"]) == 0
    assert budget["bounded_base_sampler_calls"] is None
    assert not budget["cap_failure_bound_applicable"]
    assert not budget["arbitrary_parameter_input_certifies_a_code"]


def test_circuit_error_is_charged_before_rejection():
    exact = transfer.transfer_budget(728, 6, 21, 485, circuit_tv_budget=0)
    noisy = transfer.transfer_budget(728, 6, 21, 485, circuit_tv_budget=Fraction(1, 100))
    blocked = transfer.transfer_budget(728, 6, 21, 485, circuit_tv_budget=Fraction(1, 10))
    assert fraction(exact["verified_acceptance_lower"])-fraction(noisy["verified_acceptance_lower"]) == Fraction(1, 100)
    assert noisy["bounded_base_sampler_calls"] > exact["bounded_base_sampler_calls"]
    assert not blocked["cap_failure_bound_applicable"]
    with pytest.raises(ValueError, match="TV budget"):
        transfer.transfer_budget(728, 6, 21, 485, circuit_tv_budget=-1)


@pytest.mark.parametrize("args", ((7, 2, 3, 4), (8, 0, 1, 4), (8, 2, 9, 4), (8, 2, 3, 6)))
def test_invalid_parameter_ledgers_rejected(args):
    with pytest.raises(ValueError):
        transfer.transfer_budget(*args)


def test_census_is_not_a_scalable_oracle():
    with pytest.raises(ValueError, match="cap"):
        transfer.rowspace_profiles(((1, 0, 1), (0, 1, 2)), cap=8)
    with pytest.raises(ValueError, match="independent"):
        transfer.rowspace_profiles(((1, 2), (2, 1)))


def test_matching_marginals_do_not_prove_rejection_success():
    # Negation-symmetric all-constant outputs have fair one-coordinate
    # marginals but never satisfy balance. A search witness is not a sampler.
    m = 8
    source = ((1,)*m, (2,)*m)
    assert all(sum(word[i] == 1 for word in source) == 1 for i in range(m))
    assert not any(word.count(1) == m//2 for word in source)
    assert Fraction(comb(m, m//2), 2**m) > 0


def test_rare_type_does_not_have_central_type_probability():
    m = 100
    assert Fraction(comb(m, 0), 2**m) == Fraction(1, 2**m)
    assert Fraction(comb(m, m//2), 2**m) > Fraction(1, 20)


def test_native_artifact_replay():
    if not transfer.REPORT.exists():
        pytest.skip("native report not generated")
    report = json.loads(transfer.REPORT.read_text())
    saved = report["calibration"]
    fresh = transfer.simplex_calibration(6)
    assert saved["exact_counts"] == fresh["exact_counts"]
    assert saved["budget"] == fresh["budget"]
    assert saved["full_constraint_matrix"] == [list(row) for row in fresh["full_constraint_matrix"]]
    probability = fraction(saved["exact_ideal_balanced_acceptance"])
    lower = fraction(saved["budget"]["verified_acceptance_lower"])
    assert 0 < lower <= probability
    assert lower*saved["budget"]["bounded_base_sampler_calls"] >= 40
    assert not saved["advantage_evidence"] and not saved["quantum_circuit_executed"]
    for key, mode in (("finite_coherent_erasure", "pgm"), ("broken_decoder_control", "zero")):
        actual = transfer.finite_erasure_control(decoder=mode)
        assert report[key]["actual_output_probabilities"] == pytest.approx(actual["actual_output_probabilities"])
