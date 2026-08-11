import math

import pytest

from dcp_linear_reparameterization_affine_flat_no_go import (
    affine_flat_scaling_record,
    affine_flat_union_log2_upper_bound,
    audit_parity_feature_kernel,
    build_linear_reparameterization_affine_flat_report,
    excluded_affine_dimension,
    log2_general_linear_group_order,
    parity_evaluation_matrix,
    write_linear_reparameterization_affine_flat_report,
)


def test_distinct_parity_features_have_full_rational_rank():
    matrix = parity_evaluation_matrix(3, (1, 2, 3, 4, 7))
    assert matrix.shape == (8, 5)
    assert round(float(__import__("numpy").linalg.matrix_rank(matrix))) == 5

    with pytest.raises(ValueError, match="distinct"):
        parity_evaluation_matrix(3, (1, 1))
    with pytest.raises(ValueError, match="nonzero"):
        parity_evaluation_matrix(3, (0, 1))


@pytest.mark.parametrize(
    ("dimension", "types", "modulus"),
    ((2, (1, 2, 3), 4), (3, (1, 2, 4), 8), (3, (1, 2, 3, 4), 8)),
)
def test_exact_modular_kernels_obey_smith_hadamard_bound(
    dimension, types, modulus
):
    row = audit_parity_feature_kernel(dimension, types, modulus)
    assert row.kernel_bound_verified
    assert row.rational_evaluation_rank == len(types)
    assert row.exact_kernel_probability <= (
        row.smith_hadamard_probability_upper_bound + 1e-12
    )


def test_gl_order_and_union_bound_include_all_affine_cosets():
    assert log2_general_linear_group_order(2) == pytest.approx(math.log2(6))
    total, maximum, dimension, types = affine_flat_union_log2_upper_bound(
        16, 36, 32
    )
    assert total < -300
    assert maximum <= total
    assert 32 <= dimension <= 36
    assert dimension <= types <= 36


def test_scaling_excludes_large_flats_but_not_arbitrary_linear_mps():
    rows = [affine_flat_scaling_record(bits) for bits in (64, 128, 256)]
    assert all(row.every_large_affine_flat_excluded for row in rows)
    assert all(
        row.planted_target_failure_log2_upper_bound
        == pytest.approx(
            row.union_failure_probability_log2_upper_bound + row.modulus_bits
        )
        for row in rows
    )
    assert all(row.polynomial_affine_cover_excluded for row in rows)
    assert all(not row.arbitrary_linear_tensor_rank_excluded for row in rows)
    assert all(
        row.excluded_affine_dimension == excluded_affine_dimension(row.modulus_bits)
        for row in rows
    )
    assert all(
        later.cancellation_free_affine_cover_log2_lower_bound
        > earlier.cancellation_free_affine_cover_log2_lower_bound
        for earlier, later in zip(rows, rows[1:])
    )


def test_report_preserves_cancellation_and_nonlinear_escapes(tmp_path):
    report = build_linear_reparameterization_affine_flat_report(
        scaling_modulus_bits=(64, 128),
    )
    assert report.theorem.theorem_verified
    assert report.theorem.every_gl_reparameterization_large_flat_excluded
    assert report.theorem.planted_target_large_flat_excluded
    assert not report.theorem.cancellation_free_polynomial_affine_cover_possible
    assert not report.theorem.arbitrary_linear_reparameterized_mps_ruled_out
    assert not report.theorem.nonlinear_tensorization_ruled_out
    assert not report.claim_gate["adaptive_gl_large_affine_component_route_alive"]
    assert report.claim_gate["arbitrary_linear_reparameterized_mps_route_alive"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_linear_reparameterization_affine_flat_report(
        tmp_path / "affine-flat.json",
        scaling_modulus_bits=(64, 128),
    )
    assert payload["status"] == (
        "adaptive-linear-affine-product-route-closed-cancellation-and-"
        "nonlinear-routes-open"
    )
