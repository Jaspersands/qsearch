from functools import lru_cache

import pytest

from self_dual_wreath_same_support_triangle_target_no_go import (
    audit_missing_triangle_edge_countercontrol,
    audit_translated_triangle_countercontrol,
    audit_triangle_target_certificate,
    exhaustive_triangle_pattern_census,
    run_same_support_triangle_target_no_go,
    triangle_assignments,
    triangle_target_all_depth_certificate,
)


@lru_cache(maxsize=1)
def _report():
    return run_same_support_triangle_target_no_go()


@pytest.mark.parametrize(
    ("pattern", "triple"),
    (
        ("EFEFABA", (0, 1, 2)),
        ("EFEBFAB", (0, 1, 2)),
        ("ABEFBAEABF", (0, 2, 5)),
        ("EAABFEBAFBA", (1, 3, 6)),
    ),
)
def test_arbitrary_coefficient_blocks_preserve_the_target_certificate(pattern, triple):
    certificate = audit_triangle_target_certificate("TEST", pattern, triple)
    assert certificate.exact_common_involution_certificate_verified
    assert certificate.exact_block_factorization_verified
    assert certificate.exact_pair_deleted_factorization_verified
    assert certificate.target_normal_closure_factorization == (
        certificate.factorized_target_word
    )
    assert certificate.exact_target_normal_closure_certificate_verified
    assert certificate.all_group_target_identity_proved


def test_triangle_rows_are_zero_based_weight_two_clique_edges():
    rows = triangle_assignments(7, (1, 3, 6))
    assert rows == (
        (0, 1, 0, 1, 0, 0, 0),
        (0, 1, 0, 0, 0, 0, 1),
        (0, 0, 0, 1, 0, 0, 1),
    )
    assert all(sum(row) == 2 for row in rows)


@pytest.mark.parametrize(
    ("width", "patterns", "triangles"),
    ((3, 280, 280), (4, 1120, 4480)),
)
def test_exhaustive_small_width_pattern_census_has_no_certificate_failure(
    width, patterns, triangles
):
    census = exhaustive_triangle_pattern_census(width)
    assert census.checked_pattern_count == patterns
    assert census.checked_triangle_count == triangles
    assert census.certificate_failure_count == 0
    assert census.exhaustive_at_width


def test_removing_one_triangle_edge_really_can_preserve_target_mass():
    control = audit_missing_triangle_edge_countercontrol()
    assert control.pattern == "EFEBFAB"
    assert len(control.same_support) == 2
    assert control.missing_triangle_assignment == (0, 1, 1)
    assert control.solution_count == 108
    assert control.nonidentity_target_count == 42
    assert control.target_survival_verified


def test_affine_translation_can_preserve_target_but_not_scalar_pressure():
    control = audit_translated_triangle_countercontrol()
    assert control.pattern == "EFEAAABFB"
    assert control.translation == (0, 0, 0, 1, 1)
    assert control.solution_count == 432
    assert control.nonidentity_target_count == 168
    assert control.finite_target_survival_verified
    assert control.solution_exponent_upper_bound == 3.0
    assert control.scalar_crossing_pressure_margin == pytest.approx(2.0)
    assert not control.scalar_pressure_survival_verified
    assert control.exact_countercontrol_verified


def test_all_depth_scope_is_symbolic_not_a_finite_pattern_claim():
    theorem = triangle_target_all_depth_certificate()
    assert theorem.arbitrary_frame_width
    assert theorem.arbitrary_leaf_placement
    assert theorem.arbitrary_frame_types
    assert theorem.arbitrary_additional_support_rows
    assert theorem.arbitrary_different_support
    assert theorem.exact_target_identity
    assert theorem.universal_triangle_target_no_go_verified


def test_report_closes_even_parity_patterns_but_keeps_translated_frontier_open():
    report = _report()
    assert report.headline_metrics["all_depth_triangle_target_no_go_theorem_count"] == 1
    assert report.headline_metrics["exhaustive_pattern_count"] == 1400
    assert report.headline_metrics["exhaustive_triangle_certificate_count"] == 4760
    assert report.headline_metrics["exhaustive_certificate_failure_count"] == 0
    assert report.headline_metrics["missing_edge_S3_nonidentity_target_count"] == 42
    assert report.headline_metrics[
        "translated_triangle_S3_nonidentity_target_count"
    ] == 168
    assert report.headline_metrics["translated_triangle_pressure_survival_count"] == 0
    assert report.claim_gate[
        "same_support_weight_two_triangle_forces_target_identity"
    ]
    assert report.claim_gate["all_even_parity_interleaved_targets_controlled"]
    assert not report.claim_gate["two_edge_path_forces_target_identity"]
    assert not report.claim_gate["affine_translated_triangles_controlled"]
    assert not report.claim_gate["all_triangle_free_supports_controlled"]
    assert not report.claim_gate["speedup_claim_allowed"]
