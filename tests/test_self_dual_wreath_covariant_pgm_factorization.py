import numpy as np
import pytest

from representation_obstruction import hook_length_dimension, integer_partitions
from self_dual_wreath_covariant_pgm_factorization import (
    audit_covariant_factorization,
    covariant_factorization_scaling_record,
    run_covariant_pgm_factorization,
)


def _regular_multiplicities(n: int) -> dict[tuple[int, ...], int]:
    return {
        partition: hook_length_dimension(partition)
        for partition in integer_partitions(n)
    }


def test_full_rank_covariant_factorization_is_exact() -> None:
    dimension = 6
    raw = np.arange(1, dimension * dimension + 1, dtype=float).reshape(dimension, dimension)
    positive = raw @ raw.T + np.eye(dimension)
    state = positive / np.trace(positive)
    record = audit_covariant_factorization(
        "full-rank",
        3,
        _regular_multiplicities(3),
        state,
    )

    assert record.exact_covariant_factorization_verified
    assert record.fourier_factorization_residual < 1e-9
    assert record.compressed_isometry_support_residual < 1e-9
    assert record.maximum_average_block_formula_residual < 1e-9


def test_projector_rank_normalization_cancels() -> None:
    projector = np.diag([1.0, 1.0, 0.0, 0.0, 0.0, 0.0])
    record = audit_covariant_factorization(
        "projector",
        3,
        _regular_multiplicities(3),
        projector / 2,
        projector=projector,
    )

    assert record.exact_covariant_factorization_verified
    assert record.projector_rank_cancellation_residual is not None
    assert record.projector_rank_cancellation_residual < 1e-9


def test_scaling_removes_explicit_group_factor_but_not_inverse() -> None:
    record = covariant_factorization_scaling_record(512)

    assert record.generic_petz_environment_sqrt_log2_charge > 1900
    assert record.explicit_group_size_factor_after_covariant_fourier_reduction == 1
    assert record.efficient_symmetric_group_qft_available
    assert not record.controlled_multiplicity_inverse_block_encoding_proved
    assert not record.polynomial_covariant_pgm_circuit_proved


def test_report_is_proof_gated() -> None:
    report = run_covariant_pgm_factorization()

    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["covariance_compressed_stinespring_factorization_proved"]
    assert not report.claim_gate["explicit_sqrt_group_environment_charge_survives"]
    assert not report.claim_gate["controlled_multiplicity_inverse_block_encoding_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_invalid_degree_is_rejected() -> None:
    with pytest.raises(ValueError, match="at least two"):
        covariant_factorization_scaling_record(1)
