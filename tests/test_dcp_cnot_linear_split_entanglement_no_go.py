import pytest

from dcp_cnot_linear_split_entanglement_no_go import (
    audit_linear_split_schmidt_control,
    audit_offset_moment_domination,
    build_cnot_linear_split_entanglement_report,
    cnot_circuit_family_log2_upper_bound,
    cnot_linear_split_scaling_record,
    selected_factorial_moment_order,
    side_cap_log2,
    write_cnot_linear_split_entanglement_report,
)


def test_arbitrary_offsets_do_not_increase_factorial_moments():
    quadratic = tuple(
        2 * (((value >> 0) & 1) * ((value >> 1) & 1))
        for value in range(8)
    )
    nonlinear = tuple((value * value + 3 * value) % 8 for value in range(8))
    for order, offsets, name in (
        (2, quadratic, "quadratic"),
        (3, nonlinear, "nonlinear"),
    ):
        row = audit_offset_moment_domination(3, order, offsets, name)
        assert row.offset_moment_dominated
        assert row.domination_residual == pytest.approx(0.0)
        assert row.offset_average_factorial_moment <= (
            row.homogeneous_average_factorial_moment + 1e-12
        )


@pytest.mark.parametrize(
    ("bits", "labels", "gates"),
    (
        (3, (1, 3, 5, 7, 2, 6), ((0, 3), (1, 4), (5, 2), (3, 1))),
        (
            4,
            (1, 3, 5, 7, 9, 11, 13, 15),
            ((0, 4), (1, 5), (2, 6), (7, 3), (4, 2)),
        ),
    ),
)
def test_linear_split_rank_bound_allows_matrix_cancellation(bits, labels, gates):
    row = audit_linear_split_schmidt_control(bits, labels, gates)
    assert row.cancellation_aware_rank_bound_verified
    assert row.schmidt_mass_residual < 1e-10
    assert row.rank_for_requested_mass >= row.deterministic_rank_lower_bound
    assert row.maximum_row_occupancy >= 1
    assert row.maximum_column_occupancy >= 1


def test_circuit_count_and_cap_charge_adaptive_selection():
    q = 1 << 40
    m = 2 * q + 4
    order = selected_factorial_moment_order(q)
    circuit_log = cnot_circuit_family_log2_upper_bound(m, q)
    cap = side_cap_log2(q, m, q, order)
    assert circuit_log > 2 * q * 39
    assert cap < q // 4
    with pytest.raises(ValueError, match="planted"):
        side_cap_log2(q, m, q, order, independent_failure_exponent=q - 1)


def test_scaling_closes_compact_but_not_dense_linear_transforms():
    rows = [
        cnot_linear_split_scaling_record(bits)
        for bits in (1 << 40, 1 << 48, 1 << 56)
    ]
    assert all(
        row.compact_cnot_family_exponential_rank_certified for row in rows
    )
    assert all(row.maximum_side_register_excess == 2 for row in rows)
    assert all(
        row.averaged_side_factorial_moment_log2_upper_bound
        == 2 * row.selected_factorial_moment_order + 1
        for row in rows
    )
    assert all(
        row.inherited_factorial_moment_envelope_certified for row in rows
    )
    assert all(row.inherited_bad_moment_log2_upper_bound < 0 for row in rows)
    assert all(not row.dense_quadratic_cnot_family_ruled_out for row in rows)
    assert all(row.schmidt_rank_exponent_fraction > 0.4 for row in rows)
    assert all(
        row.planted_target_failure_log2_upper_bound
        == 2 * row.independent_target_failure_log2_upper_bound / 3
        for row in rows
    )


def test_report_keeps_dense_and_nonlinear_routes_open(tmp_path):
    report = build_cnot_linear_split_entanglement_report(
        scaling_modulus_bits=(1 << 40, 1 << 48),
    )
    assert report.theorem.theorem_verified
    assert report.theorem.arbitrary_offset_moment_domination_proved
    assert report.theorem.compact_cnot_family_exponential_rank_proved
    assert report.theorem.approximate_rank_with_matrix_cancellation_proved
    assert not report.theorem.dense_quadratic_cnot_transforms_ruled_out
    assert not report.theorem.nonlinear_tensorization_ruled_out
    assert not report.claim_gate["compact_adaptive_cnot_mps_route_alive"]
    assert report.claim_gate["dense_quadratic_cnot_transform_route_alive"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_cnot_linear_split_entanglement_report(
        tmp_path / "cnot-linear.json",
        scaling_modulus_bits=(1 << 40, 1 << 48),
    )
    assert payload["status"] == (
        "sub-q-four-thirds-cnot-linear-tensor-route-closed-dense-and-"
        "nonlinear-routes-open"
    )
