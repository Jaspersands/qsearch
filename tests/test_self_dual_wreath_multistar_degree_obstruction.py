from fractions import Fraction

import pytest

from self_dual_wreath_multistar_degree_obstruction import (
    GERSHGORIN_DEGREE_BUDGET,
    _laplacian_controls,
    audit_finite_merge_degree,
    live_crossing_edges,
    natural_threshold_portfolio,
    off_common_star_weight,
    run_multistar_degree_obstruction,
    sample_natural_merge_degree,
    sign_blind_weighted_degrees,
)


D5_LABELS = (
    ((6,), (2, 2, 2)),
    ((5, 1), (4, 1, 1)),
    ((4, 2), (3, 1, 1, 1)),
    ((3, 3), (1, 1, 1, 1, 1, 1)),
)


def test_natural_portfolio_reaches_the_information_threshold_where_possible() -> None:
    labels, copy_count, threshold, target = natural_threshold_portfolio(12)

    assert copy_count == min(threshold, 77 // 2)
    assert len(labels) == copy_count
    sources = [partition for label in labels for partition in label]
    assert len(set(sources)) == len(sources)
    assert sum(target) == 12


def test_off_common_star_weight_is_an_exact_rational() -> None:
    weight = off_common_star_weight((6,), D5_LABELS, 14, 0, 7)

    assert isinstance(weight, Fraction)
    assert weight == Fraction(1, 5)


def test_live_crossing_edges_need_disjoint_children() -> None:
    with pytest.raises(ValueError):
        live_crossing_edges((6,), D5_LABELS, (0, 1), (1, 2))


def test_finite_merge_degrees_still_fit_the_gershgorin_budget() -> None:
    record = audit_finite_merge_degree("W6-D5-SPLIT-3", (6,), D5_LABELS, 3)

    assert record.child_size == 8
    assert record.crossing_pair_count == 64
    assert record.gershgorin_budget == GERSHGORIN_DEGREE_BUDGET
    assert record.sign_blind_certificate_available
    assert record.maximum_weighted_degree < GERSHGORIN_DEGREE_BUDGET
    degrees = sign_blind_weighted_degrees(
        (6,),
        D5_LABELS,
        tuple(mask for mask in range(16) if not (mask >> 3) & 1),
        tuple(mask for mask in range(16) if (mask >> 3) & 1),
    )
    assert len(degrees) == record.live_crossing_edge_count
    assert all(isinstance(value, Fraction) for value in degrees.values())


def test_natural_degree_is_within_budget_at_seven_and_vacuous_at_ten() -> None:
    small = sample_natural_merge_degree(7, sample_count=24)
    large = sample_natural_merge_degree(10, sample_count=24)

    assert small.sign_blind_certificate_available
    assert not large.sign_blind_certificate_available
    assert large.projected_weighted_degree > GERSHGORIN_DEGREE_BUDGET
    assert large.adjacent_crossing_edge_count == 2 * ((1 << (large.label_count - 1)) - 1)
    assert large.live_star_wilson_lower_bound > 0.5


def test_off_common_weight_saturates_toward_the_minimal_irrep_reciprocal() -> None:
    early = sample_natural_merge_degree(7, sample_count=24)
    late = sample_natural_merge_degree(12, sample_count=24)

    assert (
        late.saturation_ratio_against_inverse_n_minus_one
        > early.saturation_ratio_against_inverse_n_minus_one
    )
    assert late.saturation_ratio_against_inverse_n_minus_one > 0.5
    assert late.one_dimensional_carrier_star_count > (
        early.one_dimensional_carrier_star_count
    )


def test_relation_gram_equals_the_subspace_graph_laplacian() -> None:
    controls = _laplacian_controls()

    assert controls
    assert all(control.verified for control in controls)
    assert all(
        control.incidence_reconstruction_residual < 1e-8 for control in controls
    )
    assert all(
        control.maximum_positive_spectrum_residual < 1e-8 for control in controls
    )
    assert all(control.positive_spectrum_size > 0 for control in controls)


def test_report_kills_the_sign_blind_route_and_keeps_the_gap_open() -> None:
    report = run_multistar_degree_obstruction(
        sampled_degrees=(7, 10),
        sample_count=16,
    )

    assert report.claim_gate["exact_absolute_weight_law_available"]
    assert report.claim_gate[
        "sign_blind_multistar_certificate_dead_at_natural_depth"
    ]
    assert report.claim_gate["subspace_graph_laplacian_equivalence_verified"]
    assert not report.claim_gate["phase_sensitive_quotient_gap_proved"]
    assert not report.claim_gate["all_depth_multistar_conditioning_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
    assert report.headline_metrics["laplacian_equivalence_failure_count"] == 0
    assert report.headline_metrics["new_quantum_algorithm_count"] == 0
    assert all(
        row["phase_sensitive_bound_required"] for row in report.scaling_records
    )
    assert not any(
        row["sign_blind_certificate_possible"]
        for row in report.scaling_records
    )


def test_report_writer_can_skip_the_registry(tmp_path) -> None:
    from self_dual_wreath_multistar_degree_obstruction import (
        write_multistar_degree_obstruction_report,
    )

    path = tmp_path / "multistar.json"
    payload = write_multistar_degree_obstruction_report(
        path=path,
        write_registry=False,
        sampled_degrees=(7, 10),
        sample_count=8,
    )

    assert path.exists()
    assert payload["claim_gate"]["speedup_claim_allowed"] is False
    assert payload["headline_metrics"][
        "laplacian_equivalence_failure_count"
    ] == 0

