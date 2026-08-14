import math

from self_dual_wreath_compressed_racah_coupling_probe import (
    build_complete_compressed_racah_coupling_report,
    compile_complete_racah_coupling,
)


def test_complete_s5_coupling_closes_every_rank_marginal() -> None:
    source = (3, 1, 1)
    record = compile_complete_racah_coupling((source,) * 4)
    assert record.block_count == 49
    assert record.total_multiplicity_dimension == 13
    assert record.total_block_mass_residual < 1e-10
    assert record.maximum_left_rank_marginal_residual < 1e-10
    assert record.maximum_right_rank_marginal_residual < 1e-10
    assert record.maximum_independent_finite_likelihood_mass_residual is not None
    assert record.maximum_independent_finite_likelihood_mass_residual < 1e-10
    assert record.exact_complete_coupling_verified


def test_complete_s6_coupling_reports_entropy_without_extrapolation() -> None:
    source = (3, 2, 1)
    record = compile_complete_racah_coupling((source,) * 4)
    assert record.block_count == 121
    assert record.total_multiplicity_dimension == 93
    assert record.total_block_mass_residual < 1e-9
    assert record.maximum_left_rank_marginal_residual < 1e-9
    assert record.maximum_right_rank_marginal_residual < 1e-9
    assert 0 <= record.conditional_racah_mutual_information_bits < math.log2(11)
    assert record.conditional_racah_mutual_information_bits < 0.01
    assert record.maximum_independent_finite_likelihood_mass_residual is None
    assert record.finite_representation_space_probe_only
    assert record.exact_complete_coupling_verified


def test_fractional_renyi_moments_upper_bound_conditional_mi() -> None:
    source = (3, 1, 1)
    record = compile_complete_racah_coupling((source,) * 4)
    for order in ("0.25", "0.5", "1.0"):
        assert record.fractional_dependence_moments[order] >= 1.0 - 1e-10
        assert (
            record.fractional_renyi_upper_bits[order]
            >= record.conditional_racah_mutual_information_bits - 1e-10
        )
    assert math.isclose(
        record.dependence_collision_moment,
        record.fractional_dependence_moments["1.0"],
        rel_tol=1e-14,
    )


def test_report_keeps_physical_average_and_speedup_gates_closed() -> None:
    report = build_complete_compressed_racah_coupling_report(n_values=(4, 5))
    assert report.headline_metrics["complete_conditional_coupling_failure_count"] == 0
    assert report.claim_gate["all_rank_marginal_checks_passed"] is True
    assert report.claim_gate["finite_conditional_mi_is_asymptotic_evidence"] is False
    assert report.claim_gate["physical_average_racah_mi_computed"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False
