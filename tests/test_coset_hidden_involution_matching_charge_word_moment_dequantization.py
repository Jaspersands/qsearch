import math

from coset_hidden_involution_matching_charge_orbit_recoupling_reduction import (
    reference_hidden_involution,
)
from coset_hidden_involution_matching_charge_word_moment_dequantization import (
    Hoeffding_sample_bound,
    build_word_moment_dequantization_report,
    estimate_charge_word_returns,
    exact_charge_word_returns,
    exact_word_moment_control,
    identity_permutation,
    word_moment_scaling_record,
    write_word_moment_dequantization_report,
)


def test_exact_degree_two_return_probability_is_inverse_orbit_size():
    half_degree = 4
    identity = identity_permutation(2 * half_degree)
    tuples, identity_returns, hidden_returns = exact_charge_word_returns(
        half_degree,
        (identity, identity),
    )
    assert tuples == 192**2
    assert identity_returns == 192
    assert hidden_returns >= 0
    assert identity_returns / tuples == 1 / 192


def test_Monte_Carlo_estimates_regular_and_h_even_returns():
    row = exact_word_moment_control(4)
    assert row.return_probability_identity_verified
    assert row.regular_estimate_within_bound
    assert row.hidden_even_estimate_within_bound
    assert row.exact_hidden_even_trace >= row.exact_regular_trace


def test_Hoeffding_bound_has_inverse_square_accuracy_scaling():
    failure = 0.01
    coarse = Hoeffding_sample_bound(0.1, failure)
    fine = Hoeffding_sample_bound(0.01, failure)
    assert 99 <= fine / coarse <= 101


def test_inverse_polynomial_signals_have_polynomial_classical_bounds():
    rows = [
        word_moment_scaling_record(value, max(4, int(math.log2(value))))
        for value in (8, 16, 32, 64)
    ]
    assert all(row.inverse_polynomial_signal_classically_estimable for row in rows)
    assert all(
        not row.quantum_amplitude_estimation_exponential_advantage_possible
        for row in rows
    )
    # Epsilon=Theta(m^-9), so Hoeffding samples scale as Theta(m^18).
    normalized = [
        row.Hoeffding_sample_upper_bound / row.half_degree**18 for row in rows
    ]
    assert max(normalized) / min(normalized) < 1.01


def test_report_closes_scalar_moments_but_not_conditioned_matrix_data():
    report = build_word_moment_dequantization_report()
    theorem = report.theorem
    assert theorem.exact_all_degree_return_probability_reduction_proved
    assert theorem.inverse_polynomial_scalar_word_moments_classically_estimable
    assert theorem.polynomial_signed_moment_combinations_classically_estimable
    assert theorem.scalar_commutator_moment_advantage_ruled_out
    assert not theorem.conditioned_matrix_transition_dequantized
    assert not theorem.spectral_projector_transition_dequantized
    assert not theorem.all_copy_target_interference_dequantized
    assert not theorem.speedup_claim_allowed
    assert theorem.theorem_verified


def test_live_word_moment_report_is_json_serializable(tmp_path):
    output = tmp_path / "word-moments.json"
    payload = write_word_moment_dequantization_report(output)
    assert output.exists()
    assert payload["status"] == (
        "all-degree-scalar-charge-word-moments-dequantized-matrix-data-open"
    )
    assert payload["claim_gate"]["scalar_charge_word_moments_classically_estimable"]
    assert not payload["claim_gate"]["conditioned_matrix_transition_dequantized"]
    assert not payload["claim_gate"]["speedup_claim_allowed"]
