import itertools

from self_dual_wreath_parity_projector_orbit_variance import (
    BITS,
    audit_orbit_variance,
    conditional_chi_square,
    inverse_walsh_transform,
    pairwise_flat_synergy_counterexample,
    run_parity_projector_orbit_variance,
    walsh_transform,
)


def test_walsh_transform_and_inverse_are_exact() -> None:
    values = tuple(float(index * index - 3 * index) for index in range(8))
    reconstructed = inverse_walsh_transform(walsh_transform(values))
    assert all(abs(left - right) < 1e-12 for left, right in zip(values, reconstructed))


def test_even_parity_counterexample_is_pairwise_flat_but_triple_nonuniform() -> None:
    control = pairwise_flat_synergy_counterexample()

    assert control.exact_pairwise_flat_triple_synergy_verified
    assert control.all_marginals_uniform
    assert control.all_pairs_uniform
    assert not control.triple_channel_uniform
    assert control.surviving_nonzero_walsh_modes == ((1, 1, 1),)
    assert abs(control.conditional_chi_square - 1.0) < 1e-12


def test_s5_paired_orbit_channels_are_positive_and_obey_parseval() -> None:
    for orbit_tuple in ((1,) * 6, (2,) * 6, (1, 2, 1, 2, 1, 2)):
        control = audit_orbit_variance("S5", 5, orbit_tuple)
        assert control.exact_orbit_variance_normal_form_verified
        assert control.minimum_unsigned_amplitude >= -1e-12
        assert control.probability_sum_residual < 1e-12
        assert control.conditional_chi_square_residual < 1e-12
        assert control.absolute_variance_residual < 1e-12


def test_conditional_chi_square_boundaries() -> None:
    uniform = (1.0 / 8.0,) * 8
    parity = tuple(0.25 if sum(point) % 2 == 0 else 0.0 for point in BITS)

    assert conditional_chi_square(uniform) == 0.0
    assert conditional_chi_square(parity) == 1.0


def test_report_requires_genuine_tetrahedral_control_and_keeps_gates_closed() -> None:
    report = run_parity_projector_orbit_variance()

    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["adaptive_channel_is_positive_projector_trace_law"]
    assert report.claim_gate["adaptive_chi_square_is_exact_channel_variance"]
    assert not report.claim_gate["marginal_rank_proof_strategy_sufficient"]
    assert not report.claim_gate["pairwise_angle_proof_strategy_sufficient"]
    assert report.claim_gate["genuine_tetrahedral_cumulant_required"]
    assert not report.claim_gate["canonical_adaptive_syndrome_decouples_proved"]
    assert not report.claim_gate["canonical_adaptive_syndrome_survives_proved"]
    assert not report.claim_gate["algorithm_claim_allowed"]
    assert not report.claim_gate["speedup_claim_allowed"]
