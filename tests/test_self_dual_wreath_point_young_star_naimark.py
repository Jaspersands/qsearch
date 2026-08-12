from __future__ import annotations

import pytest

from coset_jucys_murphy_label_transform import standard_young_tableaux
from self_dual_wreath_point_young_star_naimark import (
    audit_young_star_naimark,
    run_young_star_naimark,
    tableau_child,
    young_star_naimark_scaling_record,
)


THRESHOLD_LABELS = (
    ((3,), (2, 1)),
    ((3,), (1, 1, 1)),
    ((2, 1), (1, 1, 1)),
)


def test_tableau_child_matches_branching_shape_and_tableau() -> None:
    for parent in ((4, 2), (3, 2, 1), (2, 2, 2)):
        for tableau in standard_young_tableaux(parent):
            child, reduced = tableau_child(tableau)
            assert sum(child) == sum(parent) - 1
            assert reduced in standard_young_tableaux(child)
    with pytest.raises(ValueError, match="at least two"):
        tableau_child(((1,),))


def test_young_star_seed_and_square_root_factorization_are_exact() -> None:
    control = audit_young_star_naimark(
        3,
        THRESHOLD_LABELS,
        control_id="threshold",
    )
    assert control.exact_young_star_seed_factorization_verified
    assert control.maximum_seed_young_star_factorization_residual < 1e-9
    assert control.maximum_seed_square_root_factorization_residual < 1e-9
    assert control.child_partition_count == 2
    assert control.maximum_parent_count_per_child == 2
    assert control.centered_child_star_has_both_signs
    assert control.centered_child_star_rank_one_factorization_falsified


def test_width_n_covariant_naimark_isometry_reproduces_born_probabilities() -> None:
    for n, labels in (
        (3, (((3,), (2, 1)),)),
        (3, THRESHOLD_LABELS),
        (4, (((4,), (3, 1)), ((2, 2), (2, 1, 1)))),
    ):
        control = audit_young_star_naimark(n, labels, control_id=str(n))
        assert control.exact_width_n_covariant_naimark_verified
        assert control.covariant_effect_orbit_residual < 1e-9
        assert control.naimark_isometry_residual < 1e-9
        assert control.naimark_born_probability_residual < 1e-9
        assert control.point_outcome_count == n


def test_s4_centered_child_star_is_high_rank_and_signed() -> None:
    control = audit_young_star_naimark(
        4,
        (((4,), (3, 1)), ((2, 2), (2, 1, 1))),
        control_id="w4-rank",
    )
    assert control.maximum_centered_child_star_rank == 19
    assert control.maximum_centered_child_star_rank_fraction > 0.59
    assert control.centered_child_star_has_both_signs
    assert control.centered_child_star_rank_one_factorization_falsified


def test_scaling_exposes_orientation_multiplicity_not_parent_graph() -> None:
    record = young_star_naimark_scaling_record(64)
    assert record.maximum_parent_count_per_child <= record.maximum_parent_count_upper_bound
    assert record.child_star_parent_graph_polynomial_degree
    assert record.subgroup_chain_young_label_transform_polynomial
    assert record.coset_outcome_width_polynomial
    assert not record.explicit_orientation_multiplicity_polynomial
    assert not record.implicit_child_star_block_transform_proved
    assert not record.child_star_spectrum_bound_proved
    assert not record.direct_point_naimark_compiled


def test_report_records_direct_escape_without_calling_it_a_circuit() -> None:
    report = run_young_star_naimark()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["point_outcome_orbit_compressed_to_n"]
    assert report.claim_gate["young_star_seed_factorization_proved"]
    assert report.claim_gate["young_star_square_root_factorization_proved"]
    assert not report.claim_gate["orientation_multiplicity_removed"]
    assert not report.claim_gate[
        "centered_child_star_rank_one_factorization_valid"
    ]
    assert not report.claim_gate["implicit_child_star_block_transform_proved"]
    assert not report.claim_gate["direct_covariant_point_naimark_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]
