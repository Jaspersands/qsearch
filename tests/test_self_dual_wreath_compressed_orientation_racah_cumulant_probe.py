from self_dual_wreath_compressed_orientation_racah_cumulant_probe import (
    audit_s5_exact_amplitude_cross_check,
    compile_orientation_racah_channel,
    run_compressed_orientation_racah_cumulant_probe,
)


def test_compressed_orientation_amplitudes_match_exact_s5_channel_and_mass() -> None:
    cross_check, control = audit_s5_exact_amplitude_cross_check()
    assert cross_check.maximum_exact_amplitude_residual < 1e-8
    assert cross_check.physical_mass_formula_residual < 1e-8
    assert cross_check.exact_amplitude_and_mass_formula_verified
    assert control.compressed_orientation_channel_verified


def test_s6_repeated_orbit_has_low_mass_numerical_two_syndrome_spike() -> None:
    control = compile_orientation_racah_channel(
        "S6-TEST", ((3, 1, 1, 1),) * 6
    )
    assert control.numerically_nonzero_syndrome_count == 2
    assert control.irreducible_racah_cmi_bits > 0.99
    assert control.physical_sign_orbit_tuple_mass < 2e-4
    assert control.exact_zero_pattern_proved is False
    assert control.compressed_orientation_channel_verified


def test_high_mass_repeated_s7_sector_is_nearly_markov_not_one_bit() -> None:
    control = compile_orientation_racah_channel(
        "S7-TEST", ((3, 2, 1, 1),) * 6
    )
    assert control.physical_sign_orbit_tuple_mass > 0.01
    assert control.irreducible_racah_cmi_bits < 1e-4
    assert control.rank_profile_cmi_bits < 1e-10
    assert control.compressed_orientation_channel_verified


def test_report_blocks_scaling_and_speedup_claims() -> None:
    report = run_compressed_orientation_racah_cumulant_probe()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics["maximum_completed_n"] == 7
    assert report.claim_gate["repeated_orbit_sequence_supports_scaling_inference"] is False
    assert report.claim_gate["physical_average_orientation_cmi_positive_proved"] is False
    assert report.claim_gate["classical_separation_proved"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False
