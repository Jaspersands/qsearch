import math

import pytest

from self_dual_wreath_parity_racah_information_projection import (
    audit_information_projection,
    audit_information_projection_aggregate,
    conditional_independence_minor_residual,
    kl_divergence_bits,
    markov_information_projection,
    run_parity_racah_information_projection,
    write_parity_racah_information_projection_report,
)


def test_markov_projection_preserves_k_and_conditional_one_bit_marginals() -> None:
    probabilities = (0.30, 0.05, 0.05, 0.10, 0.05, 0.10, 0.10, 0.25)
    projected = markov_information_projection(probabilities)

    assert sum(projected) == pytest.approx(1.0)
    assert conditional_independence_minor_residual(projected) < 1e-15
    for k in (0, 1):
        assert sum(projected[4 * g + 2 * h + k] for g in (0, 1) for h in (0, 1)) == pytest.approx(
            sum(probabilities[4 * g + 2 * h + k] for g in (0, 1) for h in (0, 1))
        )
        for g in (0, 1):
            assert sum(projected[4 * g + 2 * h + k] for h in (0, 1)) == pytest.approx(
                sum(probabilities[4 * g + 2 * h + k] for h in (0, 1))
            )
        for h in (0, 1):
            assert sum(projected[4 * g + 2 * h + k] for g in (0, 1)) == pytest.approx(
                sum(probabilities[4 * g + 2 * h + k] for g in (0, 1))
            )


def test_information_projection_gives_exact_positive_kl_split() -> None:
    control = audit_information_projection(
        "S5-WITNESS", 5, (1, 2, 1, 2, 2, 2)
    )

    assert control.exact_information_projection_verified
    assert control.irreducible_racah_conditional_mutual_information_bits > 0.2
    assert control.markov_projection_kl_to_uniform_bits > 0.08
    assert control.uniform_pythagorean_residual_bits < 1e-12
    assert control.rank_profile_pythagorean_residual_bits is not None
    assert control.rank_profile_pythagorean_residual_bits < 1e-12
    assert control.maximum_markov_projection_conditional_minor < 1e-15


def test_flat_s4_channel_has_zero_irreducible_and_compatible_information() -> None:
    control = audit_information_projection("S4-FLAT", 4, (1,) * 6)

    assert control.adaptive_kl_to_uniform_bits < 1e-12
    assert control.irreducible_racah_conditional_mutual_information_bits < 1e-12
    assert control.markov_projection_kl_to_uniform_bits < 1e-12


def test_kl_rejects_reference_support_mismatch() -> None:
    p = (0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    q = (1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

    assert math.isinf(kl_divergence_bits(p, q))


def test_s5_nontrivial_paired_sector_has_positive_aggregate_racah_cmi() -> None:
    s4 = audit_information_projection_aggregate(4)
    s5 = audit_information_projection_aggregate(5)

    assert s4.physical_mass_weighted_irreducible_racah_cmi_bits < 1e-12
    assert s5.retained_physical_mass == pytest.approx(0.10354861111111108)
    assert s5.physical_mass_weighted_irreducible_racah_cmi_bits == pytest.approx(
        0.0028430220697473665
    )
    assert s5.physical_mass_weighted_adaptive_kl_bits == pytest.approx(
        0.11525262182668568
    )
    assert s5.irreducible_fraction_of_adaptive_kl == pytest.approx(
        0.02466774312538104
    )
    assert s5.aggregate_pythagorean_residual_bits < 1e-12
    assert s5.all_orbit_projections_verified


def test_report_keeps_asymptotic_and_algorithmic_claims_closed(tmp_path) -> None:
    report = run_parity_racah_information_projection()

    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate[
        "racah_cmi_is_exact_distance_to_all_rank_profile_models"
    ]
    assert report.claim_gate["adaptive_kl_has_positive_rank_racah_decomposition"]
    assert report.claim_gate["finite_physical_racah_cmi_positive"]
    assert not report.claim_gate["asymptotic_racah_cmi_vanishes_proved"]
    assert not report.claim_gate["asymptotic_racah_cmi_survives_proved"]
    assert not report.claim_gate["classical_separation_proved"]
    assert not report.claim_gate["algorithm_claim_allowed"]
    assert not report.claim_gate["speedup_claim_allowed"]

    path = tmp_path / "information-projection.json"
    payload = write_parity_racah_information_projection_report(path)
    assert path.exists()
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0
