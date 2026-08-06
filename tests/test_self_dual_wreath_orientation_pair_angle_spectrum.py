import numpy as np

from self_dual_wreath_orientation_fourier_reduction import (
    orientation_invariant_projector,
)
from self_dual_wreath_orientation_pair_angle_spectrum import (
    exact_pair_principal_angle_spectrum,
    run_orientation_pair_angle_spectrum,
)


W5_LABELS = (
    ((5,), (4, 1)),
    ((2, 1, 1, 1), (1, 1, 1, 1, 1)),
)


def _basis(projector: np.ndarray) -> np.ndarray:
    eigenvalues, eigenvectors = np.linalg.eigh(projector)
    return eigenvectors[:, eigenvalues > 1 - 1e-8]


def test_exact_pair_angle_spectrum_matches_s5_projectors() -> None:
    target = (3, 1, 1)
    left_mask = 0
    right_mask = 3
    left = _basis(
        orientation_invariant_projector(
            target,
            W5_LABELS,
            left_mask,
        )
    )
    right = _basis(
        orientation_invariant_projector(
            target,
            W5_LABELS,
            right_mask,
        )
    )
    actual = np.sort(
        np.linalg.svd(left.T @ right, compute_uv=False)
    )[::-1]
    actual = actual[actual > 1e-8]
    predicted = np.array(
        sorted(
            (
                float(value)
                for value, multiplicity, _ in exact_pair_principal_angle_spectrum(
                    target,
                    W5_LABELS,
                    left_mask,
                    right_mask,
                )
                for _ in range(multiplicity)
            ),
            reverse=True,
        )
    )
    assert len(actual) == len(predicted)
    assert np.max(np.abs(actual - predicted), initial=0) < 1e-10


def test_pair_hilbert_schmidt_overlap_is_spectrum_square_sum() -> None:
    target = (2, 1, 1, 1)
    rows = exact_pair_principal_angle_spectrum(
        target,
        W5_LABELS,
        0,
        3,
    )
    predicted_overlap = sum(
        multiplicity * float(value) ** 2
        for value, multiplicity, _ in rows
    )
    left = orientation_invariant_projector(target, W5_LABELS, 0)
    right = orientation_invariant_projector(target, W5_LABELS, 3)
    assert abs(predicted_overlap - np.trace(left @ right)) < 1e-10


def test_report_proves_inverse_dimension_pair_contraction_only() -> None:
    report = run_orientation_pair_angle_spectrum()
    metrics = report.headline_metrics
    assert metrics["complete_w4_pair_angle_validation_count"] == 15
    assert metrics["w5_pair_angle_control_count"] == 3
    assert metrics["finite_pair_angle_validation_failure_count"] == 0
    assert metrics["maximum_w4_noncommon_principal_correlation"] < 0.51
    assert metrics["maximum_w5_noncommon_principal_correlation"] < 0.251
    assert report.claim_gate[
        "exact_pair_principal_angle_spectrum_proved"
    ]
    assert report.claim_gate[
        "noncommon_inverse_n_minus_one_contraction_proved"
    ]
    assert not report.claim_gate["uniform_projector_sum_norm_bound_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
