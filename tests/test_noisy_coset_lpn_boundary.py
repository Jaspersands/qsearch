from fractions import Fraction

import numpy as np
import pytest

from theorems.noisy_coset_lpn_boundary import (
    CosetNoiseContract, FlatSpectrum, build_report,
    coherent_example_countercontrol, dense_reduction_control, error_mass,
    sample_to_fourier_label, secret_from_line,
)


@pytest.mark.parametrize("p,secret", [(2, (1, 0, 1)), (3, (1, 2)),
                                      (5, (2, 4)), (3, (0, 0))])
@pytest.mark.parametrize("visibility", [Fraction(0), Fraction(3, 4), Fraction(1)])
def test_actual_regular_source_equals_prepared_classical_sample_mixture(p, secret, visibility):
    record = dense_reduction_control(p, secret, visibility)
    for key in ("density_identity_max_error", "fourier_diagonal_max_error",
                "pairwise_commutator_max_error", "trace_distance_error"):
        assert record[key] < 2e-12
    assert record["every_nonzero_line_generator_decoded"]
    expected_rank = record["clean_rank"] if visibility else record["group_order"]
    assert record["actual_top_multiplicity"] == expected_rank


def test_binary_parameter_map_and_odd_prime_noise_law():
    tau = Fraction(1, 8)
    assert error_mass(2, 1-2*tau, 1) == tau
    assert error_mass(2, 1-2*tau, 0) == 1-tau
    assert [error_mass(3, Fraction(3, 4), e) for e in range(3)] == [
        Fraction(5, 6), Fraction(1, 12), Fraction(1, 12)]


def test_conversion_needs_no_secret_or_purity_flag():
    assert sample_to_fourier_label(43, (17, 31), 12) == (17, 31, 12)
    for scale in range(1, 43):
        assert secret_from_line(43, (17*scale % 43, 31*scale % 43, -scale % 43)) == (17, 31)
    p = 2**127-1
    assert secret_from_line(p, (p-6, p-9, 3)) == (2, 3)


@pytest.mark.parametrize("args", [(4, 2, Fraction(1, 2)), (2, 0, Fraction(1, 2)),
                                 (2, 2, .5), (2, 2, Fraction(-1, 2))])
def test_invalid_contracts_fail_closed(args):
    with pytest.raises(ValueError):
        CosetNoiseContract(*args)


def test_invalid_coordinates_and_dense_cap():
    for call in (lambda: sample_to_fourier_label(5, (5,), 1),
                 lambda: secret_from_line(5, (1, 0)),
                 lambda: dense_reduction_control(5, (1, 2, 3), Fraction(1, 2))):
        with pytest.raises(ValueError):
            call()


def test_symmetric_formula_against_actual_projector_and_partial_trace():
    spectrum = FlatSpectrum(2, 4, Fraction(1, 8))
    eigenvalues = [spectrum.top_eigenvalue]*2+[spectrum.bottom_eigenvalue]*2
    rho = np.diag([float(x) for x in eigenvalues])
    swap = np.zeros((16, 16))
    for i in range(4):
        for j in range(4):
            swap[4*j+i, 4*i+j] = 1
    symmetric = (np.eye(16)+swap)/2
    joint = symmetric@np.kron(rho, rho)@symmetric
    success = float(np.trace(joint))
    actual = np.trace((joint/success).reshape(4, 4, 4, 4), axis1=1, axis2=3)
    following, probability = spectrum.symmetric_step()
    assert abs(success-float(probability)) < 1e-14
    expected = np.diag([float(following.top_eigenvalue)]*2+
                       [float(following.bottom_eigenvalue)]*2)
    assert np.max(np.abs(actual-expected)) < 1e-14


@pytest.mark.parametrize("rank,dimension", [(1, 2), (2, 4), (8, 16), (9, 27)])
def test_exact_odds_contraction_and_necessary_level_bound(rank, dimension):
    start = FlatSpectrum(rank, dimension, Fraction(1, 8))
    target = Fraction(1, 16)
    lower = start.necessary_levels(target)
    current = start
    for levels in range(1, 7):
        following, probability = current.symmetric_step()
        ratio = (following.error/(1-following.error))/(current.error/(1-current.error))
        assert ratio >= Fraction(rank, rank+1)
        assert Fraction(1, 2) <= probability <= 1
        current = following
        if levels < lower:
            assert current.error > target
        if current.error <= target:
            assert levels >= lower
            break


def test_large_rank_cost_is_symbolic_not_exponentially_allocated():
    spectrum = CosetNoiseContract(2, 64, Fraction(3, 4)).spectrum()
    assert spectrum.rank == 2**64
    assert spectrum.necessary_levels(Fraction(1, 16)) == (8*2**64+14)//15
    collision = spectrum.equal_label_collision(2)
    assert collision["output_error"] == Fraction(1, 50)
    assert collision["success_probability"] == Fraction(25, 32*2**64)
    assert collision["expected_raw_copies"] == Fraction(64*2**64, 25)


def test_collision_law_by_explicit_classical_enumeration():
    spectrum = FlatSpectrum(2, 6, Fraction(1, 6))
    probabilities = [spectrum.top_eigenvalue]*2+[spectrum.bottom_eigenvalue]*4
    accepted = [sum(a*b for i, a in enumerate(probabilities)
                    for j, b in enumerate(probabilities) if i == j == k)
                for k in range(6)]
    result = spectrum.equal_label_collision(2)
    assert sum(accepted) == result["success_probability"]
    assert sum(accepted[2:])/sum(accepted) == result["output_error"]


def test_uniform_state_does_not_purify_and_zero_error_is_not_finite():
    uniform = FlatSpectrum(2, 4, Fraction(1, 2))
    assert uniform.symmetric_step()[0] == uniform
    with pytest.raises(ValueError):
        uniform.necessary_levels(Fraction(1, 8))
    with pytest.raises(ValueError):
        FlatSpectrum(2, 4, Fraction(1, 8)).necessary_levels(Fraction(0))
    assert FlatSpectrum(2, 4, Fraction(0)).necessary_levels(Fraction(0)) == 0


def test_coherent_examples_are_a_different_resource():
    record = coherent_example_countercontrol()
    assert record["same_classical_sample_diagonal"]
    assert abs(record["coherent_secret_and_label_one_probability"]-1/2) < 1e-14
    assert abs(record["dephased_secret_and_label_one_probability"]-1/8) < 1e-14
    assert record["dephased_fourier_uniform_max_error"] < 1e-14


def test_report_keeps_scope_and_hardness_claims_separate():
    report = build_report()
    assert report["binary_lpn_equivalence_is_known"]
    assert report["classical_sample_simulation"]
    for flag in ("classical_polynomial_decoder_implied", "quantum_polynomial_decoder_implemented",
                 "gaussian_lwe_reduction_established", "all_purification_protocols_ruled_out",
                 "noiseless_rees_claim_refuted", "independent_review", "novelty_established",
                 "speedup_claim_allowed"):
        assert report[flag] is False
