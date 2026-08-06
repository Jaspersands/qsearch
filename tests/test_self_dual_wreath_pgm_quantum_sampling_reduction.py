import math

import numpy as np

from self_dual_wreath_pgm_quantum_sampling_reduction import (
    _explicit_fiber_controls,
    audit_carrier_polar_identity,
    quantum_sampling_scaling_record,
    run_pgm_quantum_sampling_reduction,
)


def test_carrier_analysis_gram_is_partial_trace_and_polar_isometry():
    bell = np.asarray([1.0, 0.0, 0.0, 1.0]) / math.sqrt(2)
    record = audit_carrier_polar_identity(
        "bell",
        np.outer(bell, bell),
        row_dimension=2,
        multiplicity_dimension=2,
    )

    assert record.exact_carrier_polar_identity_verified
    assert record.carrier_support_rank == 2
    assert abs(record.minimum_positive_carrier_eigenvalue - 0.5) < 1e-10
    assert record.analysis_gram_residual < 1e-10
    assert record.polar_support_isometry_residual < 1e-10


def test_known_small_fiber_bypasses_tiny_normalized_singular_value():
    singleton, overlapping = _explicit_fiber_controls()

    assert singleton.direct_fiber_sampler_available
    assert abs(singleton.normalized_analysis_minimum_positive_singular_value - 0.25) < 1e-12
    assert abs(singleton.inverse_singular_value_cost - 4.0) < 1e-12
    assert not singleton.factorial_scale_alone_implies_hardness
    assert overlapping.direct_fiber_sampler_available
    assert overlapping.maximum_pair_commutator_norm < 1e-12


def test_actual_wreath_orientation_blocks_require_nonorthogonal_sampling():
    report = run_pgm_quantum_sampling_reduction()
    metrics = report.headline_metrics

    assert metrics["carrier_validation_failure_count"] == 0
    assert metrics["explicit_fiber_validation_failure_count"] == 0
    assert metrics["wreath_orientation_validation_failure_count"] == 0
    assert metrics["noncommuting_wreath_sector_count"] > 0
    assert metrics["maximum_wreath_pair_commutator_norm"] > 0.4
    assert not report.claim_gate[
        "ordinary_commuting_fiber_sampler_applies_generically"
    ]
    assert not report.claim_gate["structured_nonorthogonal_sampler_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_black_box_polar_cost_is_factorial_at_information_threshold():
    record = quantum_sampling_scaling_record(128)

    assert record.black_box_polar_query_cost_log2_lower > 10 * math.log2(128)
    assert not record.polynomial_black_box_polar
    assert not record.direct_structured_nonorthogonal_sampler_proved
