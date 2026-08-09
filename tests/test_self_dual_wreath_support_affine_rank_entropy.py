import itertools

from self_dual_wreath_support_affine_rank_entropy import (
    affine_dimension,
    audit_support_affine_rank,
    relation_exponent_matrix,
    run_support_affine_rank_entropy,
)


def test_cube_support_affine_dimension_pays_logarithmic_size():
    cube3 = tuple(itertools.product((0, 1), repeat=3))
    even3 = tuple(row for row in cube3 if sum(row) % 2 == 0)
    assert affine_dimension(((0, 0, 0),)) == 0
    assert affine_dimension(cube3) == 3
    assert affine_dimension(even3) == 3


def test_singleton_support_exposes_exactly_one_crossing_exponent_debt():
    control = audit_support_affine_rank(
        "SINGLETON",
        ("A",),
        ((0,),),
        ((0,),),
    )
    assert control.relation_exponent_matrix_rank == 2
    assert control.support_entropy_bits == 0
    assert control.rank_margin_above_entropy_bound == 0
    assert control.crossing_extra_exponent_debt_upper_bound == 1
    assert control.exact_rank_entropy_inequality_verified


def test_full_cube_support_rank_dominates_support_entropy():
    cube4 = tuple(itertools.product((0, 1), repeat=4))
    control = audit_support_affine_rank(
        "FULL-CUBE",
        ("A", "B", "A", "B"),
        cube4,
        cube4,
    )
    assert control.support_entropy_bits == 4
    assert control.relation_exponent_matrix_rank >= 6
    assert control.rank_margin_above_entropy_bound >= 0
    assert control.crossing_extra_exponent_debt_upper_bound <= 1


def test_relation_matrix_keeps_the_EF_offset_and_all_ones_independent():
    matrix = relation_exponent_matrix(
        ("A", "B"),
        ((0, 0), (1, 1)),
        ((0, 1), (1, 0)),
        crossing=True,
    )
    assert matrix[0] == (1, 1, 1, 1, 1, 1)
    assert matrix[1] == (0, 0, 0, 0, 0, 1)
    assert any(row[:4] == (0, 1, 0, 1) for row in matrix)


def test_report_does_not_promote_abelian_rank_to_an_Sn_theorem():
    report = run_support_affine_rank_entropy()
    assert report.headline_metrics["checked_support_profile_count"] == 918
    assert report.headline_metrics["rank_entropy_failure_count"] == 0
    assert report.claim_gate["support_entropy_paid_in_abelian_rank"]
    assert report.claim_gate[
        "unpaid_crossing_debt_at_most_one_exponent"
    ]
    assert not report.claim_gate["symmetric_group_rank_lift_proved"]
    assert not report.claim_gate["growing_degree_pressure_separation_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
