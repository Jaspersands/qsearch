import math

import numpy as np
import pytest

from dcp_pgm_garbage_bootstrap_reduction import (
    audit_pgm_garbage_bootstrap,
    bootstrap_scaling_record,
    covariant_pgm_success_from_counts,
    pgm_garbage_bootstrap_theorem,
    public_phase_state_in_fiber_basis,
    run_pgm_garbage_bootstrap_reduction,
)


def test_public_phase_state_is_normalized_on_legal_support() -> None:
    counts = (0, 1, 2, 1, 0, 2, 1, 1)
    support, state = public_phase_state_in_fiber_basis(counts, 5)
    assert support == (1, 2, 3, 5, 6, 7)
    assert np.linalg.norm(state) == pytest.approx(1.0)
    with pytest.raises(ValueError, match="positive"):
        public_phase_state_in_fiber_basis((0, 0), 0)


def test_matching_branch_amplitude_equals_root_pgm_success_for_every_d() -> None:
    control = audit_pgm_garbage_bootstrap(
        "bootstrap",
        (0, 1, 2, 1, 0, 2, 1, 1),
        garbage_dimension=5,
        seed=31,
    )
    assert control.minimum_matching_branch_amplitude == pytest.approx(
        math.sqrt(control.pgm_success_probability)
    )
    assert control.maximum_matching_branch_amplitude == pytest.approx(
        math.sqrt(control.pgm_success_probability)
    )
    assert control.matching_branch_amplitude_spread < 1e-10
    assert control.bootstrap_identity_verified


def test_garbage_cleanup_recovers_canonical_analysis_and_erasure() -> None:
    control = audit_pgm_garbage_bootstrap(
        "cleanup",
        (1, 1, 1, 1, 1, 1, 1, 1),
        garbage_dimension=3,
        seed=41,
    )
    assert covariant_pgm_success_from_counts((1,) * 8) == pytest.approx(1.0)
    assert control.dilation_isometry_residual < 1e-10
    assert control.garbage_preparation_isometry_residual < 1e-10
    assert control.garbage_cleanup_to_canonical_residual < 1e-10
    assert control.qft_erasure_residual_after_cleanup < 1e-10


def test_inverse_polynomial_success_has_polynomial_bootstrap_cost() -> None:
    row = bootstrap_scaling_record(
        n_bits=512,
        pgm_success_power=12,
        target_precision_power=8,
    )
    assert row.pgm_success_lower_bound == pytest.approx(512**-12)
    assert row.query_bound_polynomial
    assert row.phase_state_preparation_polynomial
    assert row.controlled_garbage_preparation_polynomial
    assert row.canonicalization_polynomial


def test_theorem_closes_accessible_exact_but_not_approximate_pgm() -> None:
    theorem = pgm_garbage_bootstrap_theorem()
    assert theorem.accessible_exact_pgm_reduced
    assert theorem.destructive_standard_circuit_loophole_closed
    assert not theorem.approximate_instrument_reduced
    assert not theorem.inaccessible_external_environment_recovered
    assert not theorem.arbitrary_collective_povm_reduced
    assert not theorem.polynomial_pgm_constructed


def test_report_keeps_speedup_gate_closed() -> None:
    report = run_pgm_garbage_bootstrap_reduction()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate[
        "accessible_exact_covariant_pgm_route_is_solver_equivalent"
    ]
    assert not report.claim_gate["standard_circuit_destructive_pgm_loophole_alive"]
    assert not report.claim_gate["orthogonal_outcome_garbage_loophole_alive"]
    assert not report.claim_gate["approximate_pgm_instrument_route_closed"]
    assert not report.claim_gate["non_pgm_collective_measurement_route_closed"]
    assert not report.claim_gate["speedup_claim_allowed"]
