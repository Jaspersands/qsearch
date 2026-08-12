from __future__ import annotations

import numpy as np

from self_dual_wreath_joint_character_multiplicity_gram import (
    audit_joint_multiplicity_gram,
    joint_multiplicity_gram_scaling_record,
    matrix_valued_projection_gram,
    orientation_overlap_kernel,
    predicted_joint_multiplicity_operator,
    projection_gram_factor,
    run_joint_multiplicity_gram,
)
from self_dual_wreath_orientation_fourier_reduction import (
    _w4_collision_free_labels,
)


THRESHOLD_LABELS = (
    ((3,), (2, 1)),
    ((3,), (1, 1, 1)),
    ((2, 1), (1, 1, 1)),
)


def _random_projection(
    rng: np.random.Generator,
    dimension: int,
    rank: int,
) -> np.ndarray:
    matrix = rng.normal(size=(dimension, rank)) + 1j * rng.normal(
        size=(dimension, rank)
    )
    basis, _ = np.linalg.qr(matrix)
    return basis @ basis.conj().T


def test_matrix_valued_gram_is_positive_and_has_explicit_factor() -> None:
    rng = np.random.default_rng(20260811)
    for irrep_dimension, carrier_dimension, count in ((1, 5, 4), (2, 3, 5), (3, 2, 6)):
        projectors = tuple(
            _random_projection(
                rng,
                irrep_dimension * carrier_dimension,
                1 + index % (irrep_dimension * carrier_dimension - 1),
            )
            for index in range(count)
        )
        gram = matrix_valued_projection_gram(
            projectors,
            irrep_dimension,
            carrier_dimension,
        )
        factor = projection_gram_factor(
            projectors,
            irrep_dimension,
            carrier_dimension,
        )
        assert np.allclose(gram, factor.conj().T @ factor, atol=1e-10)
        assert np.linalg.eigvalsh((gram + gram.conj().T) / 2)[0] > -1e-10


def test_universal_projection_gram_moment_bound_survives_random_attacks() -> None:
    rng = np.random.default_rng(8112026)
    for _ in range(80):
        irrep_dimension = int(rng.integers(1, 5))
        carrier_dimension = int(rng.integers(2, 7))
        count = int(rng.integers(2, 9))
        ambient = irrep_dimension * carrier_dimension
        projectors = tuple(
            _random_projection(rng, ambient, int(rng.integers(1, ambient + 1)))
            for _ in range(count)
        )
        gram = matrix_valued_projection_gram(
            projectors,
            irrep_dimension,
            carrier_dimension,
        )
        frame_sum = sum(projectors)
        np.testing.assert_allclose(
            np.trace(gram),
            np.trace(frame_sum),
            atol=1e-9,
        )
        assert np.trace(gram @ gram).real <= (
            carrier_dimension * np.trace(frame_sum @ frame_sum).real + 1e-8
        )


def test_exact_w3_projection_gram_matches_joint_multiplicity_blocks() -> None:
    control = audit_joint_multiplicity_gram(
        3,
        THRESHOLD_LABELS,
        control_id="threshold",
    )
    assert control.exact_projection_gram_theorem_verified
    assert control.active_sector_count == 3
    assert control.maximum_exact_multiplicity_formula_residual < 1e-9
    assert control.maximum_gram_factorization_residual < 1e-9
    assert control.maximum_scalar_block_residual < 1e-9
    assert control.maximum_orientation_kernel_factorization_residual < 1e-9
    assert control.maximum_trace_identity_residual < 1e-9
    assert control.maximum_walsh_spectrum_residual < 1e-9
    assert control.maximum_moment_bound_violation == 0
    assert control.maximum_character_offdiagonal_norm > 0


def test_w4_projection_gram_identity_is_not_a_tiny_s3_accident() -> None:
    control = audit_joint_multiplicity_gram(
        4,
        _w4_collision_free_labels()[0],
        control_id="w4",
    )
    assert control.exact_projection_gram_theorem_verified
    assert control.active_sector_count >= 3
    assert control.maximum_exact_multiplicity_formula_residual < 1e-9
    assert control.maximum_nonzero_condition_number > 1


def test_predicted_operator_is_psd_but_not_character_diagonal() -> None:
    operator, gram, _ = predicted_joint_multiplicity_operator(
        (2, 1),
        THRESHOLD_LABELS,
    )
    assert np.linalg.eigvalsh((operator + operator.conj().T) / 2)[0] > -1e-10
    assert np.linalg.eigvalsh((gram + gram.conj().T) / 2)[0] > -1e-10
    tensor = operator.reshape(2, 8, 2, 8).copy()
    for character in range(8):
        tensor[:, character, :, character] = 0
    assert np.linalg.norm(tensor) > 0.1


def test_physical_orientation_gram_factors_as_column_identity() -> None:
    operator, gram, projectors = predicted_joint_multiplicity_operator(
        (2, 1),
        THRESHOLD_LABELS,
    )
    kernel = orientation_overlap_kernel(projectors, 2)
    assert np.allclose(gram, np.kron(np.eye(2), kernel), atol=1e-10)
    assert np.linalg.eigvalsh((kernel + kernel.conj().T) / 2)[0] > -1e-10
    assert operator.shape == (16, 16)


def test_scaling_and_report_keep_access_and_hard_edge_open() -> None:
    scaling = joint_multiplicity_gram_scaling_record(128)
    assert scaling.controlled_invariant_projector_schema_polynomial
    assert scaling.branch_walsh_polynomial
    assert not scaling.explicit_orientation_enumeration_required
    assert not scaling.coherent_projection_gram_block_encoding_proved
    assert not scaling.inverse_polynomial_bulk_window_proved

    report = run_joint_multiplicity_gram()
    assert report.headline_metrics["finite_control_count"] == 3
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate[
        "joint_multiplicity_equals_walsh_rotated_projection_gram"
    ]
    assert report.claim_gate[
        "projection_gram_psd_and_trace_moment_bounds_proved"
    ]
    assert report.claim_gate["fourier_column_factors_from_joint_multiplicity"]
    assert report.claim_gate["orientation_kernel_entries_equal_pair_overlaps"]
    assert not report.claim_gate["walsh_diagonalizes_projection_gram"]
    assert not report.claim_gate[
        "coherent_projection_gram_block_encoding_proved"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]
