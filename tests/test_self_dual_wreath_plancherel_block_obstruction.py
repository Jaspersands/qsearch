import pytest

from self_dual_wreath_plancherel_block_obstruction import (
    SELLKE_PAPER_URL,
    bad_block_density_certificate,
    build_plancherel_block_obstruction_report,
    residual_target_certificate,
)


def test_rate_free_markov_certificate_has_exponential_common_family() -> None:
    certificate = bad_block_density_certificate(
        copy_count=640,
        covering_block_size=8,
        single_block_failure_probability_upper_bound=0.01,
        bad_fraction_threshold=0.1,
    )
    assert certificate.complete_block_count == 80
    assert certificate.probability_bad_fraction_reaches_threshold_upper_bound == pytest.approx(
        0.1
    )
    assert certificate.good_block_count_lower_bound_off_failure_event == 72
    assert certificate.common_orientation_family_size_lower_bound == 2**72
    assert certificate.ratio_to_two_to_one_minus_k == 2**71


def test_residual_target_lemma_matches_exact_kronecker_multiplicity() -> None:
    certificate = residual_target_certificate(
        5,
        ((4, 1), (3, 2)),
    )
    assert certificate.target_multiplicity_in_residual > 0
    assert (
        certificate.trivial_multiplicity_in_target_tensor_residual
        == certificate.target_multiplicity_in_residual
    )
    assert certificate.residual_target_lemma_verified


def test_report_falsifies_only_the_uniform_frame_norm_route() -> None:
    report = build_plancherel_block_obstruction_report()
    assert report.literature["url"] == SELLKE_PAPER_URL
    assert all(step.proved for step in report.proof_steps)
    assert report.claim_gate[
        "typical_exponential_common_orientation_family_proved"
    ]
    assert report.claim_gate[
        "uniform_collision_free_polynomial_factor_norm_bound_falsified"
    ]
    assert not report.claim_gate["uniform_orientation_frame_norm_route_viable"]
    assert not report.claim_gate["all_collective_measurements_ruled_out"]
    assert not report.claim_gate[
        "alternative_measurement_or_whitening_ruled_out"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]
    unresolved = [
        item for item in report.adversarial_audit if not item["resolved"]
    ]
    assert len(unresolved) == 3
    assert any("fixed-target" in item["resolution"] for item in unresolved)


def test_markov_certificate_rejects_invalid_probabilities() -> None:
    with pytest.raises(ValueError):
        bad_block_density_certificate(100, 8, -0.1, 0.2)
    with pytest.raises(ValueError):
        bad_block_density_certificate(100, 8, 0.1, 0.0)
