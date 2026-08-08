import math

import numpy as np

from self_dual_wreath_signed_steiner_incidence_boundary import (
    audit_signed_steiner_kernel,
    audit_unsigned_steiner_incidence,
    projective_points,
    projective_steiner_lines,
    run_signed_steiner_incidence_boundary,
    signed_steiner_incidence_with_quotient_kernel,
)


def test_projective_lines_form_the_expected_steiner_triple_system() -> None:
    for copy_count in range(2, 8):
        points = projective_points(copy_count)
        lines = projective_steiner_lines(copy_count)
        orientation_count = 1 << copy_count
        assert len(points) == orientation_count - 1
        assert len(lines) == (
            (orientation_count - 1) * (orientation_count - 2) // 6
        )
        pair_counts: dict[tuple[int, int], int] = {}
        for line in lines:
            assert len(set(line)) == 3
            assert line[0] ^ line[1] ^ line[2] == 0
            for first_index in range(3):
                for second_index in range(first_index + 1, 3):
                    pair = tuple(
                        sorted((line[first_index], line[second_index]))
                    )
                    pair_counts[pair] = pair_counts.get(pair, 0) + 1
        assert len(pair_counts) == len(points) * (len(points) - 1) // 2
        assert set(pair_counts.values()) == {1}


def test_unsigned_steiner_incidence_has_exact_two_eigenvalue_gram() -> None:
    for copy_count in range(3, 8):
        record = audit_unsigned_steiner_incidence(copy_count)
        orientation_count = 1 << copy_count
        assert record.exact_unsigned_gram_verified
        assert math.isclose(
            record.predicted_small_eigenvalue,
            (orientation_count - 4) / 2,
        )
        assert math.isclose(
            record.predicted_large_eigenvalue,
            3 * (orientation_count - 2) / 2,
        )
        assert math.isclose(
            record.predicted_condition_number,
            3 * (orientation_count - 2) / (orientation_count - 4),
        )


def test_positive_line_holonomy_allows_exact_two_dimensional_kernel() -> None:
    for copy_count in range(2, 8):
        incidence, witness = signed_steiner_incidence_with_quotient_kernel(
            copy_count
        )
        record = audit_signed_steiner_kernel(copy_count)
        assert np.array_equal(incidence.T @ witness, np.zeros((incidence.shape[1], 2)))
        assert np.linalg.matrix_rank(witness) == 2
        assert record.signed_incidence_nullity >= 2
        assert record.kernel_residual == 0
        assert record.maximum_line_sign_product_residual == 0
        assert record.maximum_triangle_holonomy_residual == 0
        assert record.two_dimensional_exact_kernel_verified
        assert record.local_positive_holonomy_verified


def test_report_rejects_local_holonomy_as_a_global_edge_certificate() -> None:
    report = run_signed_steiner_incidence_boundary()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics["minimum_signed_incidence_nullity"] >= 2
    assert report.claim_gate[
        "unsigned_steiner_surrogate_uniformly_conditioned"
    ]
    assert report.claim_gate[
        "positive_local_holonomy_can_have_global_kernel"
    ]
    assert not report.claim_gate[
        "local_positive_holonomy_sufficient_for_frame_edge"
    ]
    assert not report.claim_gate["natural_recoupling_realizes_adversarial_signing"]
    assert not report.claim_gate["natural_inter_plane_gauge_controlled"]
    assert not report.claim_gate["matrix_valued_overlap_traffic_controlled"]
    assert not report.claim_gate["speedup_claim_allowed"]
