import json
from fractions import Fraction

from self_dual_wreath_trace_biased_coefficient_rank_no_go import (
    audit_trace_biased_coefficient_purity,
    coefficient_rank_scaling_record,
    exact_block_output_density,
    output_density_purity,
    pointwise_purity_upper_bound,
    run_trace_biased_coefficient_rank_no_go,
    trace_biased_coefficient_rank_theorem,
    write_trace_biased_coefficient_rank_report,
)


def test_exact_native_output_density_is_positive_and_normalized() -> None:
    block = exact_block_output_density(
        (2, 1),
        (((3,), (2, 1)),),
    )
    assert block is not None
    frame_trace, density = block
    assert frame_trace > 0
    assert sum(density[index][index] for index in range(len(density))) == 1
    assert output_density_purity(density) <= pointwise_purity_upper_bound(density)


def test_regular_master_total_coherence_is_recovered_exactly() -> None:
    control = audit_trace_biased_coefficient_purity(3, 1)
    assert control.trace_biased_total_coherence_identity_verified
    assert control.average_total_coherence == "7/6"
    assert control.regular_master_total_coherence == "7/6"
    assert control.exact_joint_trace_normalization == (
        control.predicted_joint_trace_normalization
    )


def test_joint_trace_bias_keeps_product_plancherel_source_marginal() -> None:
    control = audit_trace_biased_coefficient_purity(4, 2)
    assert control.exact_source_marginal_plancherel_verified
    assert control.source_marginal_identity_failure_count == 0
    assert control.global_distinct_probability == "89/1536"
    assert control.direct_trace_biased_global_distinct_probability == "89/1536"


def test_pointwise_purity_and_arbitrary_rank_bounds_hold() -> None:
    control = audit_trace_biased_coefficient_purity(4, 2)
    assert control.output_density_identity_verified
    assert control.projector_entry_and_purity_inequality_verified
    assert control.adaptive_rank_bound_verified
    assert control.maximum_pointwise_purity_inequality_residual <= 0
    assert control.average_best_adaptive_rank_mass <= (
        control.average_hilbert_schmidt_rank_bound
    )
    assert control.globally_distinct_average_best_adaptive_rank_mass is not None
    assert control.globally_distinct_hilbert_schmidt_rank_bound is not None
    assert control.globally_distinct_average_best_adaptive_rank_mass <= (
        control.globally_distinct_hilbert_schmidt_rank_bound
    )


def test_uniform_rank_failure_is_below_inverse_orientation_width() -> None:
    small = coefficient_rank_scaling_record(16)
    large = coefficient_rank_scaling_record(128)
    assert large.log2_orientation_count_times_rank_failure_upper_bound < 0
    assert large.adaptive_polynomial_retained_mass_upper_bound < (
        small.adaptive_polynomial_retained_mass_upper_bound
    )
    assert large.half_mass_required_rank_fraction_lower_bound > 0
    assert large.arbitrary_basis_sublinear_rank_no_go_applies_once_mass_bound_holds
    assert not large.finite_n_global_distinct_lower_bound_certified


def test_report_closes_low_rank_but_not_dense_transforms() -> None:
    theorem = trace_biased_coefficient_rank_theorem()
    report = run_trace_biased_coefficient_rank_no_go()
    assert theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate[
        "source_and_target_adaptive_arbitrary_basis_o_of_two_to_K_rank_rejected"
    ]
    assert not report.claim_gate["dense_structured_transform_rejected"]
    assert not report.claim_gate["direct_rectangular_cs_polar_compiled"]
    assert not report.claim_gate["complete_natural_orientation_polar_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_report_writer_preserves_dense_route_boundary(tmp_path) -> None:
    path = tmp_path / "trace-biased-coefficient-rank.json"
    payload = write_trace_biased_coefficient_rank_report(path)
    loaded = json.loads(path.read_text())
    assert loaded == payload
    assert loaded["headline_metrics"][
        "arbitrary_basis_adaptive_sublinear_rank_no_go_count"
    ] == 1
    assert loaded["headline_metrics"]["dense_structured_transform_no_go_count"] == 0
    assert loaded["headline_metrics"]["complete_orientation_polar_compiler_count"] == 0
    assert loaded["headline_metrics"]["new_quantum_algorithm_count"] == 0
