import numpy as np

from self_dual_wreath_polar_factor_transfer import (
    audit_equal_gram_transfer,
    polar_transfer_scaling_record,
    run_polar_factor_transfer,
)


def _isometry(rows: int, columns: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    basis, _ = np.linalg.qr(
        rng.normal(size=(rows, columns))
        + 1j * rng.normal(size=(rows, columns))
    )
    return basis


def test_known_output_isometry_transfers_equal_gram_polar_exactly():
    rng = np.random.default_rng(17)
    orientation = rng.normal(size=(5, 3)) + 1j * rng.normal(size=(5, 3))
    output_isometry = _isometry(8, 5, 23)

    record = audit_equal_gram_transfer(
        "known-output",
        orientation,
        output_isometry @ orientation,
        output_intertwiner_given_independently=True,
    )

    assert record.exact_equal_gram_transfer_verified
    assert record.gram_support_rank == 3
    assert record.output_intertwiner_given_independently
    assert record.polar_transfer_residual < 1e-9


def test_rank_deficiency_does_not_break_partial_isometry_transfer():
    orientation = np.asarray(
        [
            [1.0, 0.0, 1.0, 0.0],
            [0.0, 1.0, 1.0, 0.0],
            [1.0, -1.0, 0.0, 0.0],
        ],
        dtype=complex,
    )
    hidden_output = _isometry(7, 3, 41)

    record = audit_equal_gram_transfer(
        "rank-deficient",
        orientation,
        hidden_output @ orientation,
        output_intertwiner_given_independently=False,
    )

    assert record.exact_equal_gram_transfer_verified
    assert record.gram_support_rank < orientation.shape[1]
    assert not record.output_intertwiner_given_independently
    assert record.status == "exact-equal-gram-transfer-exists-intertwiner-not-compiled"


def test_generic_nonimplication_is_preserved_but_wreath_transfer_is_compiled():
    report = run_polar_factor_transfer()

    assert report.headline_metrics["finite_validation_failure_count"] == 0
    assert report.claim_gate["equal_gram_transfer_exists_algebraically"]
    assert not report.claim_gate[
        "orientation_polar_circuit_implies_physical_pgm_without_intertwiner"
    ]
    assert report.claim_gate[
        "structured_covariant_row_copy_is_full_polar_transfer"
    ]
    assert report.claim_gate["physical_output_intertwiner_compiled"]
    assert report.claim_gate["coherent_cross_sector_transfer_proved"]
    assert not report.claim_gate["polynomial_physical_pgm_circuit_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_scaling_record_keeps_both_implementation_gates_open():
    record = polar_transfer_scaling_record(128)

    assert record.orientation_gram_factorization_available
    assert record.physical_pgm_polar_target_specified
    assert not record.hierarchical_orientation_polar_proved
    assert record.full_output_intertwiner_compiled
    assert not record.selected_trace_transfer_is_full_polar_transfer
    assert not record.polynomial_physical_pgm_circuit_proved
