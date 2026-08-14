import math

import pytest

from self_dual_wreath_parity_racah_rank_residual_decomposition import (
    audit_axis_mapping_support,
    audit_racah_rank_residual,
    centered_cross_energy,
    centered_energy,
    haar_block_mass_variance,
    run_parity_racah_rank_residual_decomposition,
    write_parity_racah_rank_residual_report,
)


def test_direct_physical_axis_mapping_has_no_forbidden_positive_blocks() -> None:
    for n in (3, 4):
        control = audit_axis_mapping_support(n)
        assert control.positive_likelihood_entry_count > 0
        assert control.direct_mapping_unsupported_positive_count == 0
        assert control.maximum_direct_mapping_unsupported_likelihood == 0.0
        assert control.direct_coefficient_axis_mapping_verified
        assert control.dual_geometric_mapping_unsupported_positive_count > 0
        assert control.competing_dual_mapping_rejected


def test_orientation_fibers_preserve_profiles_and_normalized_block_mass() -> None:
    control = audit_racah_rank_residual("S5-MIXED", 5, (1, 2, 1, 2, 1, 2))

    assert control.all_orientation_fusion_profiles_invariant
    assert control.all_fusion_associativity_identities_verified
    assert control.maximum_orientation_fiber_amplitude_residual < 1e-12
    assert control.maximum_forbidden_support_amplitude_residual < 1e-12
    assert all(row.orientation_fiber_profile_invariant for row in control.channels)
    assert any(row.left_block_rank * row.right_block_rank == 0 for row in control.channels)


def test_centered_energy_decomposition_and_minkowski_are_exact() -> None:
    control = audit_racah_rank_residual("S5-ALL-FIVE", 5, (2,) * 6)
    natural = tuple(row.natural_normalized_block_mass for row in control.channels)
    haar = tuple(row.haar_rank_profile_benchmark for row in control.channels)
    residual = tuple(row.nonhaar_arithmetic_residual for row in control.channels)

    assert centered_energy(natural) == pytest.approx(
        centered_energy(haar)
        + centered_energy(residual)
        + 2.0 * centered_cross_energy(haar, residual),
        abs=1e-12,
    )
    assert control.variance_decomposition_residual < 1e-12
    assert control.minkowski_violation == 0.0
    assert control.minkowski_lower_bound <= math.sqrt(control.natural_centered_energy)
    assert math.sqrt(control.natural_centered_energy) <= control.minkowski_upper_bound
    assert control.exact_rank_residual_decomposition_verified


def test_s4_rank_nonuniformity_is_exactly_cancelled_by_racah_arithmetic() -> None:
    control = audit_racah_rank_residual("S4-CANCELLATION", 4, (1,) * 6)

    assert control.natural_centered_energy < 1e-12
    assert control.haar_rank_profile_centered_energy > 1e-6
    assert control.nonhaar_residual_centered_energy == pytest.approx(
        control.haar_rank_profile_centered_energy,
        abs=1e-12,
    )
    assert control.centered_alignment_cosine == pytest.approx(-1.0, abs=1e-12)
    assert control.finite_mechanism_diagnosis == (
        "rank-profile-nonuniformity-exactly-cancelled-by-racah-arithmetic"
    )


def test_s5_contains_an_arithmetic_dominated_finite_control() -> None:
    control = audit_racah_rank_residual("S5-ARITHMETIC", 5, (2,) * 6)

    assert control.nonhaar_residual_centered_energy > (
        10.0 * control.haar_rank_profile_centered_energy
    )
    assert control.finite_mechanism_diagnosis == (
        "nonhaar-racah-arithmetic-dominates-finite-centered-energy"
    )


def test_haar_block_variance_has_correct_boundaries_and_o2_value() -> None:
    assert haar_block_mass_variance(1, 1, 1) == 0.0
    assert haar_block_mass_variance(5, 0, 3) == 0.0
    assert haar_block_mass_variance(5, 5, 3) == 0.0
    assert haar_block_mass_variance(2, 1, 1) == pytest.approx(1.0 / 8.0)
    assert haar_block_mass_variance(7, 2, 3) == pytest.approx(
        haar_block_mass_variance(7, 3, 2)
    )
    with pytest.raises(ValueError):
        haar_block_mass_variance(3, 4, 1)


def test_report_keeps_all_canonical_and_algorithmic_gates_closed(tmp_path) -> None:
    report = run_parity_racah_rank_residual_decomposition()

    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics[
        "exact_rank_arithmetic_cancellation_control_count"
    ] >= 1
    assert report.headline_metrics["finite_arithmetic_dominated_control_count"] >= 1
    assert report.claim_gate["physical_coefficient_axis_mapping_verified"]
    assert report.claim_gate["positive_channels_are_normalized_racah_block_masses"]
    assert report.claim_gate["rank_arithmetic_alignment_decomposition_proved"]
    assert not report.claim_gate[
        "haar_rank_profile_alone_determines_natural_channel"
    ]
    assert not report.claim_gate["canonical_kronecker_rank_profile_mixes_proved"]
    assert not report.claim_gate["canonical_nonhaar_racah_residual_vanishes_proved"]
    assert not report.claim_gate["canonical_adaptive_syndrome_survives_proved"]
    assert not report.claim_gate["algorithm_claim_allowed"]
    assert not report.claim_gate["speedup_claim_allowed"]

    path = tmp_path / "rank-residual.json"
    payload = write_parity_racah_rank_residual_report(path)
    assert path.exists()
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0
