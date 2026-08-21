import json
from fractions import Fraction

import pytest

from self_dual_wreath_trace_biased_adaptive_walsh_no_go import (
    adaptive_walsh_scaling_record,
    audit_trace_biased_mixture,
    conditioned_collision_upper_bound,
    exact_block_autocorrelations,
    run_trace_biased_adaptive_walsh_no_go,
    trace_biased_adaptive_walsh_theorem,
    walsh_distribution_from_autocorrelations,
    write_trace_biased_adaptive_walsh_report,
)


def test_exact_block_autocorrelations_are_probabilistic() -> None:
    block = exact_block_autocorrelations(
        (2, 1),
        (((3,), (2, 1)),),
    )
    assert block is not None
    frame_trace, correlations = block
    probabilities = walsh_distribution_from_autocorrelations(correlations)
    assert frame_trace > 0
    assert correlations[0] == 1
    assert all(0 <= value <= 1 for value in correlations)
    assert sum(probabilities, Fraction()) == 1


def test_trace_biased_regular_first_moment_is_exact() -> None:
    control = audit_trace_biased_mixture(3, 1)
    assert control.exact_trace_biased_first_moment_verified
    assert control.unconditioned_expected_autocorrelations == ("1", "1/6")
    assert control.maximum_nonzero_first_moment_residual == 0
    assert control.exact_joint_trace_normalization == (
        control.predicted_joint_trace_normalization
    )


def test_joint_target_mixture_restores_plancherel_source_marginal() -> None:
    control = audit_trace_biased_mixture(4, 2)
    assert control.exact_source_marginal_plancherel_verified
    assert control.source_marginal_identity_failure_count == 0
    assert control.global_distinct_probability == "89/1536"
    assert control.direct_trace_biased_global_distinct_probability == "89/1536"


def test_second_moment_and_collision_contract_without_character_L4_bound() -> None:
    control = audit_trace_biased_mixture(4, 2)
    assert control.autocorrelation_unit_interval_verified
    assert control.second_moment_contraction_verified
    assert control.collision_and_adaptive_bounds_verified
    assert control.unconditioned_collision_probability <= (
        control.unconditioned_collision_upper_bound
    )
    assert control.globally_distinct_collision_probability is not None
    assert control.globally_distinct_collision_upper_bound is not None
    assert control.globally_distinct_collision_probability <= (
        control.globally_distinct_collision_upper_bound
    )


def test_conditioned_bound_and_asymptotic_sparse_no_go_scale() -> None:
    bound = conditioned_collision_upper_bound(24, 2, Fraction(89, 1536))
    assert float(bound) == pytest.approx(0.7893258426966292)
    small = adaptive_walsh_scaling_record(16)
    large = adaptive_walsh_scaling_record(128)
    assert large.adaptive_polynomial_retained_mass_upper_bound < (
        small.adaptive_polynomial_retained_mass_upper_bound
    )
    assert large.constant_retention_requires_linear_mode_count
    assert not large.finite_n_collision_free_lower_bound_certified


def test_report_closes_only_the_sparse_walsh_route() -> None:
    theorem = trace_biased_adaptive_walsh_theorem()
    report = run_trace_biased_adaptive_walsh_no_go()
    assert theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate[
        "source_and_target_label_adaptive_o_of_two_to_K_walsh_router_rejected"
    ]
    assert not report.claim_gate["non_walsh_adaptive_sparse_router_rejected"]
    assert not report.claim_gate["dense_structured_recoupling_rejected"]
    assert not report.claim_gate["complete_natural_orientation_polar_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_report_writer_preserves_claim_boundaries(tmp_path) -> None:
    path = tmp_path / "trace-biased-adaptive-walsh.json"
    payload = write_trace_biased_adaptive_walsh_report(path)
    loaded = json.loads(path.read_text())
    assert loaded == payload
    assert loaded["headline_metrics"]["source_adaptive_sparse_walsh_no_go_count"] == 1
    assert loaded["headline_metrics"]["non_walsh_sparse_router_no_go_count"] == 0
    assert loaded["headline_metrics"]["complete_orientation_polar_compiler_count"] == 0
    assert loaded["headline_metrics"]["new_quantum_algorithm_count"] == 0
