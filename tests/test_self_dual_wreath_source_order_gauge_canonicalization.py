import json

from self_dual_wreath_source_order_gauge_canonicalization import (
    audit_source_order_gauge,
    canonicalize_source_order,
    diagonal_branch_orbit,
    run_source_order_gauge_canonicalization,
    selected_label_pattern,
    source_order_gauge_scaling_record,
    write_source_order_gauge_canonicalization_report,
)


S6_LABELS = (
    ((6,), (4, 2)),
    ((5, 1), (2, 2, 2)),
    ((3, 3), (2, 1, 1, 1, 1)),
    ((2, 2, 1, 1), (1, 1, 1, 1, 1, 1)),
)


def test_selected_pattern_is_invariant_under_diagonal_branch_action() -> None:
    orbit = diagonal_branch_orbit(0b101, 0b011, 3)
    selected = {selected_label_pattern(order, orientation) for order, orientation in orbit}
    assert selected == {0b110}
    assert len(set(orbit)) == 8


def test_canonical_sort_retains_reversible_gauge_and_selected_pattern() -> None:
    canonical_order, canonical_orientation, gauge = canonicalize_source_order(
        0b1010,
        0b1100,
    )
    assert canonical_order == 0
    assert canonical_orientation == 0b0110
    assert gauge == 0b1010


def test_s4_all_order_gauges_match_canonical_selected_pattern_rank() -> None:
    control = audit_source_order_gauge(
        "S4-GAUGE",
        (2, 2),
        (((4,), (3, 1)), ((2, 2), (2, 1, 1))),
    )
    assert control.source_order_orientation_pair_count == 16
    assert control.diagonal_branch_orbit_count == 4
    assert control.diagonal_branch_orbit_size == 4
    assert control.maximum_order_gauge_rank_residual == 0
    assert control.maximum_selected_pattern_invariance_residual == 0
    assert control.selected_pattern_is_complete_orbit_invariant
    assert control.exact_source_order_gauge_reduction_verified


def test_s6_sorting_preserves_nonuniform_selected_rank_profile() -> None:
    control = audit_source_order_gauge(
        "S6-GAUGE",
        (6,),
        S6_LABELS,
    )
    assert control.selected_pattern_count == 16
    assert control.distinct_selected_pattern_rank_count == 5
    assert control.minimum_selected_pattern_leaf_rank == 0
    assert control.maximum_selected_pattern_leaf_rank == 2025
    assert control.selected_pattern_rank_profile_nonuniform


def test_scaling_compiles_sorting_but_not_selected_pattern_polar() -> None:
    record = source_order_gauge_scaling_record(16)
    assert record.coherent_partition_pair_sort_polynomial
    assert record.coherent_carrier_swap_polynomial
    assert record.branch_fourier_transform_polynomial
    assert not record.branch_operations_mix_selected_patterns
    assert not record.source_order_sorting_compiles_rectangular_cs_polar
    assert not record.complete_orientation_polar_compiled


def test_report_records_gauge_reduction_without_polar_claim() -> None:
    report = run_source_order_gauge_canonicalization()
    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_count"] == 4
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics["maximum_order_gauge_rank_residual"] == 0
    assert report.headline_metrics["nonuniform_selected_pattern_rank_control_count"] == 4
    assert report.claim_gate["source_order_gauge_quotient_proved"]
    assert report.claim_gate["coherent_source_pair_sorting_polynomial"]
    assert report.claim_gate["selected_pattern_complete_branch_orbit_invariant"]
    assert not report.claim_gate["branch_gauge_operations_mix_selected_patterns"]
    assert not report.claim_gate[
        "source_order_sorting_compiles_rectangular_cs_polar"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_report_writer_records_selected_pattern_frontier(tmp_path) -> None:
    path = tmp_path / "source_order_gauge.json"
    payload = write_source_order_gauge_canonicalization_report(path)
    stored = json.loads(path.read_text())
    assert stored["status"] == payload["status"]
    assert stored["status"] == (
        "source-order-gauge-quotient-proved-selected-pattern-polar-open"
    )
    assert stored["headline_metrics"]["source_order_gauge_quotient_theorem_count"] == 1
    assert stored["headline_metrics"]["selected_pattern_rectangular_cs_compiler_count"] == 0
    assert stored["headline_metrics"]["new_quantum_algorithm_count"] == 0
    assert not stored["claim_gate"]["speedup_claim_allowed"]
