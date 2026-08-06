from self_dual_wreath_orientation_fourier_reduction import (
    _w4_collision_free_labels,
)
from self_dual_wreath_orientation_retention_theorem import (
    exact_retention_control,
    expected_rejection_fraction_log2,
    plancherel_character_control,
    retention_scaling_record,
    run_orientation_retention_theorem,
)


def test_exact_character_formula_matches_direct_physical_filter() -> None:
    labels = _w4_collision_free_labels()[0]
    for generators in ((1, 2), (3,)):
        control = exact_retention_control(
            4,
            labels,
            generators,
            "finite",
        )
        assert control.exact_rejection_formula_verified
        assert control.rejection_formula_residual < 1e-12


def test_plancherel_normalized_character_expectation_is_delta_identity() -> None:
    for n in range(3, 9):
        control = plancherel_character_control(n)
        assert control.exact_plancherel_delta_identity_verified
        assert control.maximum_expected_normalized_character_residual == 0


def test_expected_rejection_has_inverse_subspace_size_exponent() -> None:
    log_loss = expected_rejection_fraction_log2(4000.0, 500)
    assert -501 < log_loss < -499


def test_scaling_certifies_gentle_constant_information_retention() -> None:
    record = retention_scaling_record(512)
    assert record.expected_rejection_fraction_log2 < -480
    assert record.markov_failure_probability_log2_upper_bound < -380
    assert record.high_probability_polynomial_retention_certified
    assert record.filtered_identification_success_lower_bound > 0.06


def test_report_opens_information_gate_but_not_decoder_gate() -> None:
    report = run_orientation_retention_theorem()
    assert report.claim_gate[
        "typical_natural_filter_acceptance_one_minus_inverse_polynomial"
    ]
    assert report.claim_gate["constant_identification_information_retained"]
    assert not report.claim_gate["postfilter_polynomial_frame_norm_proved"]
    assert not report.claim_gate["efficient_filtered_povm_constructed"]
    assert not report.claim_gate["polynomial_hidden_permutation_decoder_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
