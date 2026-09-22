from fractions import Fraction
from itertools import permutations, product

import numpy as np
import pytest

from dcp_pairing_programs import (
    build_pairing_controls, canonical_proposal, correlated_fault_source, correlated_noise_controls, dephased_source,
    evaluate_flagged_permutation, evaluate_mutual_program, gauge_control,
    local_mass_bound, matching_profile, mutual_circuit_maps, physical_pair_isometry,
    noise_mass_envelope, reference_matching_proposal, subset_residues,
)


def test_all_four_input_partial_functions_have_physical_clean_six_call_maps():
    for table in product((None, 0, 1, 2, 3), repeat=4):
        _, checks = physical_pair_isometry((1, 2), 4, table)
        assert all(checks.values())
    assert mutual_circuit_maps((1, 2), 4, (None, 3, 0, 1))["oracle_calls"] == 6


def test_canonical_witness_success_is_not_matching_coverage():
    labels = (1, 2, 4, 3, 5, 6, 7, 1)
    profile = matching_profile(labels, 8, canonical_proposal(labels, 8))
    assert profile["valid_proposal_fraction"] == 1
    assert profile["heralded_success_fraction"] == 8/256
    assert profile["mutual_assignment_count"] == 2*len(profile["pairs"])


def test_input_dependent_pairing_escapes_canonical_density_loss_but_is_not_efficient():
    labels = (1, 2, 4, 3, 5, 6, 7, 1)
    sorted_pairs = reference_matching_proposal(labels, 8)
    optimized = reference_matching_proposal(labels, 8, .75, True)
    left = matching_profile(labels, 8, sorted_pairs)
    right = matching_profile(labels, 8, optimized)
    assert left["heralded_success_fraction"] == right["heralded_success_fraction"] == 1
    from dcp_pairing_programs import hamming_visibility
    assert hamming_visibility(right["accepted_hamming_histogram"], 256, .75) >= hamming_visibility(left["accepted_hamming_histogram"], 256, .75)-1e-12


def test_low_sum_measurement_preserves_only_the_relevant_pair_signal():
    labels, modulus, table = (1, 2, 5), 8, tuple(b ^ 7 for b in range(8))
    matrix, _ = physical_pair_isometry(labels, modulus, table)
    observable = np.kron(np.eye(8), [[0, 1], [1, 0]])
    for secret in range(modulus):
        before = matrix@dephased_source(labels, modulus, secret, .8)@matrix.T
        after = matrix@dephased_source(labels, modulus, secret, .8, True)@matrix.T
        assert np.trace(observable@before) == pytest.approx(np.trace(observable@after), abs=1e-13)
        assert np.trace(before) == pytest.approx(np.trace(after), abs=1e-13)


def test_four_cycles_are_not_incorrectly_excluded_as_quantum_readouts():
    table = (1, 2, 3, 0)
    mutual = evaluate_mutual_program((2, 0), 4, table)
    general = evaluate_flagged_permutation((2, 0), 4, table)
    assert mutual["profile"]["heralded_success_fraction"] == 0
    assert general["valid_edge_fraction"] == 1
    assert general["maximum_residual"] < 1e-12
    assert not general["mutuality_required"]


def test_colliding_proposal_cannot_be_promoted_to_a_clean_permutation():
    with pytest.raises(ValueError, match="clean permutation"):
        evaluate_flagged_permutation((1, 2), 4, (1, 1, 3, 3))


@pytest.mark.parametrize("labels", [(1, 2, 5), (0, 4, 7)])
@pytest.mark.parametrize("secret", [0, 3, 7])
def test_prelabel_basis_faults_and_gauge_equal_product_dephasing(labels, secret):
    m, modulus, epsilon = len(labels), 8, .2
    size = 1 << m
    bad_bits = 5
    actual = np.zeros((size, size), complex)
    for faults in range(size):
        probability = epsilon**faults.bit_count()*(1-epsilon)**(m-faults.bit_count())
        for flips in range(size):
            old = [(-a if (flips >> j) & 1 else a) % modulus for j, a in enumerate(labels)]
            vector = np.zeros(size, complex)
            for b in range(size):
                if (b ^ bad_bits) & faults:
                    continue
                phase = sum(a*((b >> j) & 1) for j, a in enumerate(old) if not (faults >> j) & 1)
                vector[b ^ flips] = np.exp(2j*np.pi*secret*phase/modulus)/np.sqrt(1 << (m-faults.bit_count()))
            actual += probability*np.outer(vector, vector.conj())/size
    np.testing.assert_allclose(actual, dephased_source(labels, modulus, secret, 1-epsilon), atol=1e-14)
    assert np.trace(actual).real == pytest.approx(1)


def test_gauge_scope_fails_for_postlabel_adversarial_basis_bits():
    report = gauge_control()
    assert report["maximum_good_state_residual"] < 1e-12
    assert report["maximum_prelabel_bad_bit_residual"] == 0
    assert report["postlabel_adversarial_bit_counterexample_gap"] == .5


@pytest.mark.parametrize("secret", [0, 1, 5])
@pytest.mark.parametrize("law", [{0: Fraction(3, 4), 7: Fraction(1, 4)},
                                 {1: Fraction(1, 3), 2: Fraction(1, 3), 4: Fraction(1, 3)}])
def test_correlated_fault_formula_from_independent_prelabel_gauge_enumeration(secret, law):
    labels, modulus, m, bad_bits = (1, 2, 5), 8, 3, 5
    actual = np.zeros((8, 8), complex)
    for faults, probability in law.items():
        for flips in range(8):
            old = [(-a if (flips >> j) & 1 else a) % modulus for j, a in enumerate(labels)]
            vector = np.zeros(8, complex)
            for b in range(8):
                if (b ^ bad_bits) & faults:
                    continue
                phase = sum(a*((b >> j) & 1) for j, a in enumerate(old) if not (faults >> j) & 1)
                vector[b ^ flips] = np.exp(2j*np.pi*secret*phase/modulus)/np.sqrt(1 << (m-faults.bit_count()))
            actual += float(probability)*np.outer(vector, vector.conj())/8
    np.testing.assert_allclose(actual, correlated_fault_source(labels, modulus, secret, law), atol=1e-14)


def test_correlations_can_improve_or_worsen_signal_relative_to_product_formula():
    rows = correlated_noise_controls()
    assert all(row["maximum_residual"] < 1e-12 for row in rows)
    assert rows[0]["weighted_signal"] > rows[0]["incorrect_independent_model_signal"]
    assert rows[1]["weighted_signal"] < rows[1]["incorrect_independent_model_signal"]
    assert rows[2]["weighted_signal"] == rows[2]["marginal_union_lower"]
    # All-or-none faults retain constant coherence at every nonempty width:
    # the independent constant-noise envelope cannot be generalized to this law.
    source = correlated_fault_source((1, 2, 5), 8, 0, {0: Fraction(3, 4), 7: Fraction(1, 4)})
    assert source[0, 7].real == pytest.approx(.75/8)
    assert source[0, 1].real == pytest.approx(.75/8)
    with pytest.raises(ValueError, match="probability"):
        correlated_fault_source((1,), 4, 0, {0: Fraction(1, 2)})


def test_heralded_probability_and_noise_bias_charge_different_quantities():
    report = evaluate_mutual_program((1, 3), 4, (3, 2, 1, 0))
    assert all(report["physical_checks"].values())
    assert report["maximum_residual"] < 1e-12
    for row in report["rows"]:
        assert row["accepted_mass"] == pytest.approx(report["profile"]["heralded_success_fraction"])
        if row["eta"] == 0:
            assert abs(row["signed_output_bias"]) < 1e-12


def test_adaptive_short_moves_obey_natural_label_average_mass_bound():
    modulus, m = 8, 2
    total = Fraction(0)
    for labels in product(range(modulus), repeat=m):
        residues = subset_residues(labels, modulus)
        accepted = 0
        for b in range(1 << m):
            # Allow an all-powerful input/label-adaptive selector, not a fixed move.
            accepted += any((int(residues[b ^ (1 << i)])-int(residues[b])) % modulus == modulus//2
                            for i in range(m))
        total += Fraction(accepted, (1 << m)*modulus**m)
    assert total == 1-Fraction(modulus-1, modulus)**m
    assert total <= local_mass_bound(3, m, 1)
    assert local_mass_bound(256, 256**2, 8) < Fraction(1, 1 << 140)


def test_label_independent_complement_has_exactly_inverse_modulus_average_mass():
    total = Fraction(0)
    for labels in product(range(4), repeat=3):
        profile = matching_profile(labels, 4, tuple(b ^ 7 for b in range(8)))
        total += Fraction(profile["mutual_assignment_count"], 8*4**3)
    assert total == Fraction(1, 4)


def test_noise_envelope_bounds_even_per_label_optimal_permutations():
    eta, average = Fraction(3, 4), Fraction(0)
    for labels in product(range(4), repeat=2):
        residues = subset_residues(labels, 4)
        best = max(sum((eta**((b ^ c).bit_count()) for b, c in enumerate(table)
                        if (int(residues[c])-int(residues[b])) % 4 == 2), Fraction(0))/4
                   for table in permutations(range(4)))
        average += best/16
    report = noise_mass_envelope(2, 2, eta)
    assert average > 0
    assert average <= report["upper"]
    assert report["upper"] == Fraction(33, 64)
    assert report["unallocated_mass"] == Fraction(1, 4)


def test_envelope_is_exact_capacity_relaxation_not_an_achievable_matching():
    from scipy.optimize import linprog
    from math import comb
    n, m, eta = 6, 9, Fraction(4, 5)
    result = linprog([-float(eta**w) for w in range(1, m+1)],
                     A_ub=[[1]*m], b_ub=[1],
                     bounds=[(0, comb(m, w)/2**n) for w in range(1, m+1)], method="highs")
    assert result.success
    assert float(noise_mass_envelope(n, m, eta)["upper"]) == pytest.approx(-result.fun)
    assert noise_mass_envelope(n, m, Fraction(0))["upper"] == 0
    assert noise_mass_envelope(n, m, Fraction(1))["upper"] == 1
    assert noise_mass_envelope(4096, 4096**2, Fraction(3, 4))["upper"] < Fraction(1, 2**50)
    assert noise_mass_envelope(4096, 4096**2, Fraction(4095, 4096))["upper"] > Fraction(9, 10)
    with pytest.raises(ValueError, match="Fraction"):
        noise_mass_envelope(n, m, .8)


@pytest.mark.parametrize("modulus,labels,table", [(3, (1,), (1, 0)), (4, (), (0,)),
                                                   (4, (True,), (1, 0)), (4, (1,), (1, 3))])
def test_invalid_physical_models_are_rejected(modulus, labels, table):
    with pytest.raises(ValueError):
        matching_profile(labels, modulus, table)


def test_report_does_not_promote_reference_tables_or_conditional_visibility():
    report = build_pairing_controls()
    assert report["control_failures"] == 0
    assert len(report["mutual_controls"]) == 9
    assert all(row["mean_heralded_mass"] <= row["canonical_mass_upper_bound"]
               for row in report["canonical_density_controls"])
    assert not report["contract"]["gate_export_implemented"]
    assert not report["contract"]["polynomial_decoder_constructed"]
    assert not report["contract"]["novelty_established"]
