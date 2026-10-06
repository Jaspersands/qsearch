from fractions import Fraction

import pytest

from dcp_physical_phase_noise import read
from dcp_noisy_completion import (
    _density_controls, basis_contamination_binary_density, commutator_squared_norm,
    known_basis_bias_filter, known_residue_classicalization_certificate, low_noise_clean_block_baseline,
    noise_promise_gate, phase_flip_binary_density, robust_full_candidate_verification,
)


def test_phase_noise_binary_experiment_has_exact_classical_reverse_channel():
    for e in (0, Fraction(1, 32), Fraction(1, 2)):
        row = known_residue_classicalization_certificate(128, e)
        assert row["measure_H_then_Z_is_lossless_for_declared_binary_experiment"]
        assert not row["coherent_label_or_example_oracle_granted"]
        assert not row["classical_polynomial_time_lpn_decoder_provided"]
        assert commutator_squared_norm(phase_flip_binary_density(0, e), phase_flip_binary_density(1, e)) == 0


def test_unbalanced_basis_failure_is_not_commuting_phase_noise():
    rows = _density_controls()
    assert len(rows) == 8
    a, b = (basis_contamination_binary_density(p, Fraction(1, 8), 0) for p in (0, 1))
    assert commutator_squared_norm(a, b) == Fraction(49, 2048)
    assert any(not row["X_twirl_is_lossless"] for row in rows)


def test_noise_promise_gate_rejects_unjustified_regev_to_phase_noise_transfer():
    kwargs = {"independent_registers": True, "uniform_native_labels": True,
              "independent_of_higher_labels": True, "independent_of_secret": True,
              "correct_residue_known": True}
    row = noise_promise_gate("arbitrary_basis_contamination", "native_iid_phase_moment", **kwargs)
    assert not row["transfer_obligations_satisfied_as_declared"]
    assert row["issues"]
    assert not noise_promise_gate("arbitrary_basis_contamination", "lossless_binary_classicalization", **kwargs)["transfer_obligations_satisfied_as_declared"]
    valid = noise_promise_gate("iid_physical_Z", "native_iid_phase_moment", **kwargs)
    assert valid["transfer_obligations_satisfied_as_declared"]
    assert not valid["declarations_programmatically_proven"]
    assert not valid["candidate_record_accepted"]


def test_correlated_phase_masks_classicalize_but_do_not_become_iid_lpn():
    kwargs = {"correct_residue_known": True}
    assert noise_promise_gate("classical_correlated_Z", "lossless_binary_classicalization", **kwargs)["transfer_obligations_satisfied_as_declared"]
    assert not noise_promise_gate("classical_correlated_Z", "iid_lpn_completion", **kwargs)["transfer_obligations_satisfied_as_declared"]
    assert not noise_promise_gate("iid_physical_Z", "lossless_binary_classicalization")["transfer_obligations_satisfied_as_declared"]


def test_low_noise_completion_has_a_legal_classical_clean_block_baseline():
    row = low_noise_clean_block_baseline(128, Fraction(1, 128**2))
    assert read(row["marginal_flip_bound_only_correct_completion_success_lower_bound"]) > Fraction(98, 100)
    assert read(row["iid_clean_block_correct_completion_success_lower_bound"]) > Fraction(98, 100)
    assert row["fresh_original_phase_states_per_trial"] == 168
    assert row["wrong_or_inconsistent_blocks_not_accepted_without_verification"]
    hard = low_noise_clean_block_baseline(128, Fraction(1, 8))
    assert read(hard["iid_clean_block_correct_completion_success_lower_bound"]) < Fraction(1, 10**9)
    assert not hard["noisy_constant_rate_polynomial_decoder_claim"]


def test_full_candidate_verifier_keeps_completeness_and_soundness_under_bounded_bad_states():
    row = robust_full_candidate_verification(256, Fraction(1, 16))
    assert row["projection_zero_votes_required"] == 192
    assert read(row["false_acceptance_probability_upper_bound"]) < Fraction(1, 10**7)
    assert read(row["false_rejection_probability_upper_bound"]) < Fraction(1, 10**20)
    assert row["bad_states_can_be_arbitrary_not_only_Z_flips"]
    assert row["conditional_bad_probability_bound_not_just_unconditional_marginals_required"]
    assert not row["conditional_source_promise_programmatically_verified"]


def test_missing_conditional_promise_or_invalid_models_are_not_silently_certified():
    with pytest.raises(ValueError):
        noise_promise_gate("made_up_noise", "iid_lpn_completion")
    with pytest.raises(ValueError):
        robust_full_candidate_verification(128, Fraction(1, 4))
    with pytest.raises(ValueError):
        low_noise_clean_block_baseline(0, 0)
    with pytest.raises(ValueError):
        phase_flip_binary_density(2, 0)


def test_public_bias_filter_and_reverse_preparation_are_symbolically_exact():
    import sympy as sp
    for gamma in (Fraction(1, 128), Fraction(1, 8)):
        g = sp.Rational(gamma.numerator, gamma.denominator)
        a = sp.sqrt((1 - g) / (1 + g))
        flip = (1 - a) / 2
        for bad in (0, 1):
            K = sp.diag(a, 1) if bad == 0 else sp.diag(1, a)
            for parity in (0, 1):
                rho = sp.Matrix(basis_contamination_binary_density(parity, gamma, bad))
                filtered = K * rho * K
                assert sp.simplify(sp.trace(filtered) - (1 - g)) == 0
                ideal = sp.Matrix([[sp.Rational(1, 2), (-1)**parity * a / 2],
                                   [(-1)**parity * a / 2, sp.Rational(1, 2)]])
                assert (filtered / (1 - g) - ideal).applyfunc(sp.simplify) == sp.zeros(2)
                def pure(y):
                    v = sp.Matrix([sp.sqrt((1 + g) / 2), (-1)**y * sp.sqrt((1 - g) / 2)])
                    if bad: v = sp.Matrix([v[1], v[0]])
                    return v * v.T
                recreated = (1 - flip) * pure(parity) + flip * pure(parity ^ 1)
                assert (rho - recreated).applyfunc(sp.simplify) == sp.zeros(2)
            row = known_basis_bias_filter(gamma, bad)
            assert read(row["success_probability"]) == 1 - gamma
            assert not row["one_copy_lossless_equivalence_claim"]
            assert not row["arbitrary_hidden_or_label_dependent_basis_bias_covered"]


def test_heralded_filter_requires_the_public_bias_not_the_general_failure_promise():
    row = noise_promise_gate("known_biased_basis_contamination", "heralded_binary_classicalization",
                            correct_residue_known=True, public_constant_basis_bias_known=True)
    assert row["transfer_obligations_satisfied_as_declared"]
    assert not noise_promise_gate("arbitrary_basis_contamination", "heralded_binary_classicalization",
                                 correct_residue_known=True)["transfer_obligations_satisfied_as_declared"]
    with pytest.raises(ValueError):
        known_basis_bias_filter(1, 0)
