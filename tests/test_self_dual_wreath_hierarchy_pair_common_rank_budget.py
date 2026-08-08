import math
from fractions import Fraction

from self_dual_wreath_hierarchy_pair_common_rank_budget import (
    audit_exact_pair_common_mass,
    audit_hierarchy_pair_incidence,
    hierarchy_pair_common_rank_scaling_record,
    hierarchy_pair_incidence_formula,
    run_hierarchy_pair_common_rank_budget,
)


def test_exact_hierarchy_pair_incidence_formula_through_seven_copies() -> None:
    for copy_count in range(1, 8):
        record = audit_hierarchy_pair_incidence(copy_count)
        orientation_count = 1 << copy_count
        lower, root_nonantipodal, root_antipodal = (
            hierarchy_pair_incidence_formula(copy_count)
        )
        assert lower == orientation_count * (
            orientation_count - copy_count - 1
        ) // 2
        assert root_nonantipodal == orientation_count * (
            orientation_count - 2
        ) // 2
        assert root_antipodal == orientation_count // 2
        assert record.exact_hierarchy_pair_count_verified
        assert (
            record.predicted_total_nonantipodal_pair_incidence_count
            == orientation_count * (2 * orientation_count - copy_count - 3) // 2
        )


def test_nonantipodal_pair_common_mass_is_two_over_group_order_cubed() -> None:
    controls = (
        audit_exact_pair_common_mass(3, (3,)),
        audit_exact_pair_common_mass(3, (2, 1)),
        audit_exact_pair_common_mass(4, (1, 1, 1, 1), 2),
        audit_exact_pair_common_mass(4, (2, 2), 2),
    )
    for record in controls:
        order = math.factorial(record.n)
        assert (
            Fraction(record.observed_nonantipodal_expected_relative_common_rank)
            == Fraction(2, order**3)
        )
        assert record.exact_nonantipodal_mass_verified


def test_root_antipodal_exception_occurs_only_for_one_dimensional_targets() -> None:
    trivial = audit_exact_pair_common_mass(4, (4,), 2)
    sign = audit_exact_pair_common_mass(4, (1, 1, 1, 1), 2)
    higher = audit_exact_pair_common_mass(4, (2, 2), 2)
    for record in (trivial, sign):
        assert record.target_dimension == 1
        assert Fraction(
            record.observed_root_antipodal_expected_relative_common_rank
        ) == Fraction(1, math.factorial(4) ** 2)
        assert record.exact_root_antipodal_mass_verified
    assert higher.target_dimension > 1
    assert Fraction(
        higher.observed_root_antipodal_expected_relative_common_rank
    ) == 0
    assert higher.exact_root_antipodal_mass_verified


def test_scaling_uses_exact_target_union_formula_and_conditioning() -> None:
    record = hierarchy_pair_common_rank_scaling_record(32)
    order = math.factorial(record.n)
    orientation_count = int(record.orientation_count_decimal)
    copy_count = record.selected_copy_count
    nonantipodal_count = (
        orientation_count * (2 * orientation_count - copy_count - 3) // 2
    )
    predicted = (
        Fraction(2 * record.partition_count * nonantipodal_count, order**3)
        + Fraction(orientation_count, order**2)
    )
    assert math.isclose(
        record.unconditioned_all_target_union_expected_rank_upper_bound,
        float(predicted),
        rel_tol=1e-12,
    )
    assert math.isclose(
        record.conditioned_all_target_union_expected_rank_upper_bound,
        float(predicted) / record.global_distinct_probability,
        rel_tol=1e-12,
    )
    assert record.finite_simultaneous_rank_trim_certified
    assert not record.full_noncommon_frame_edge_proved


def test_report_proves_only_exact_common_rank_trim() -> None:
    report = run_hierarchy_pair_common_rank_budget()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate[
        "arbitrarily_coherent_exact_common_span_rank_bounded"
    ]
    assert report.claim_gate[
        "collision_free_all_target_exact_common_rank_trim_proved"
    ]
    assert not report.claim_gate["arbitrary_source_coupling_covered"]
    assert not report.claim_gate[
        "noncommon_collision_free_return_bound_proved"
    ]
    assert not report.claim_gate["near_outlier_accumulation_controlled"]
    assert not report.claim_gate["natural_complete_node_frame_edge_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
    tail = report.scaling_records[-1]
    assert tail.conditioned_all_target_union_bound_log2 < -100
    assert tail.finite_simultaneous_rank_trim_certified
