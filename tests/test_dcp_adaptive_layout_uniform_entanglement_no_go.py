import math

import pytest

from dcp_adaptive_layout_uniform_entanglement_no_go import (
    adaptive_layout_moment_order,
    all_layout_entanglement_scaling_record,
    all_layout_side_cap_failure_log2_upper_bound,
    build_dcp_adaptive_layout_uniform_entanglement_report,
    side_multiplicity_cap_log2,
    simultaneous_schmidt_rank_log2_lower_bound,
    write_dcp_adaptive_layout_uniform_entanglement_report,
)


def test_sub_cube_root_schedule_and_all_layout_union_bound():
    q = 1 << 24
    m = 2 * q + 4
    order = adaptive_layout_moment_order(q)
    assert order >= 2
    assert order < (q / math.log2(q)) ** (1 / 3)
    cap_log = side_multiplicity_cap_log2(q, m, order)
    failure_log = all_layout_side_cap_failure_log2_upper_bound(
        q, m, order, cap_log
    )
    assert failure_log <= -q
    assert cap_log / q < 0.5


def test_deterministic_side_cap_to_schmidt_rank_formula():
    lower = simultaneous_schmidt_rank_log2_lower_bound(
        full_fiber_mean_log2=100.0,
        side_cap_log2=7.0,
        requested_mass=0.5,
    )
    assert lower == pytest.approx(84.0)
    with pytest.raises(ValueError, match="requested_mass"):
        simultaneous_schmidt_rank_log2_lower_bound(10.0, 2.0, 0.0)


def test_scaling_certifies_all_adaptive_balanced_coordinate_cuts():
    row = all_layout_entanglement_scaling_record(1 << 24)
    assert row.moment_schedule_condition_ratio < 1.0
    assert row.side_multiplicity_cap_subexponential
    assert row.all_layout_side_cap_failure_log2_upper_bound <= -row.modulus_bits
    assert row.simultaneous_schmidt_rank_log2_lower_bound > (
        row.polynomial_bond_benchmark_log2
    )
    assert row.every_balanced_coordinate_layout_exponential_rank_certified


def test_finite_controls_enumerate_every_balanced_layout():
    report = build_dcp_adaptive_layout_uniform_entanglement_report(
        finite_specs=((3, 0),),
        finite_trials=1,
        scaling_modulus_bits=(1 << 24,),
    )
    row = report.finite_controls[0]
    assert row.balanced_layout_count == math.comb(6, 3)
    assert row.every_layout_fiber_size_consistent
    assert row.every_layout_rank_bound_verified


def test_report_closes_adaptive_coordinate_mps_only(tmp_path):
    report = build_dcp_adaptive_layout_uniform_entanglement_report()
    assert report.theorem.theorem_verified
    assert report.theorem.all_balanced_coordinate_side_caps_proved
    assert report.theorem.every_balanced_coordinate_cut_exp_rank_proved
    assert not report.theorem.adaptive_coordinate_mps_polynomial_bond_possible
    assert not report.theorem.inverse_polynomial_easy_source_subset_for_coordinate_mps_possible
    assert not report.theorem.noncoordinate_tensor_network_ruled_out
    assert not report.theorem.general_quantum_circuit_lower_bound_proved
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_dcp_adaptive_layout_uniform_entanglement_report(
        tmp_path / "report.json"
    )
    assert payload["status"] == (
        "adaptive-coordinate-tensor-route-closed-"
        "noncoordinate-coisometry-open"
    )
