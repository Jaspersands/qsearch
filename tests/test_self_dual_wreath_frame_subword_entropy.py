import itertools
import math

import pytest

from self_dual_wreath_frame_subword_entropy import (
    audit_frame_subword_entropy,
    frame_subword_entropy_induction_certificate,
    frame_subword_reduction,
    frame_subword_relations,
    frame_subword_rerooting_certificate,
    frame_subword_suffix_branch_certificate,
    reroot_frame_subword_support,
    run_frame_subword_entropy,
)
from self_dual_wreath_marked_relation_topology import presentation_solution_count


def test_frame_relations_are_ordered_support_subwords():
    support = ((0, 0, 0), (1, 0, 1), (0, 1, 1))
    assert frame_subword_relations(support) == ((-3, -2), (-3, -1))


def test_triangular_automorphism_implements_xor_rerooting_exactly():
    certificate = frame_subword_rerooting_certificate((1, 0, 1))
    assert certificate.generator_images == (
        (-1,),
        (1, 2, -1),
        (1, -3, -1),
    )
    assert certificate.checked_cube_vertex_count == 8
    assert certificate.every_subword_identity_verified
    assert certificate.triangular_automorphism_verified
    assert certificate.exact_rerooting_isomorphism_verified
    for width in range(7):
        for base in itertools.product((0, 1), repeat=width):
            assert frame_subword_rerooting_certificate(
                base
            ).exact_rerooting_isomorphism_verified


def test_entropy_induction_reroots_the_larger_upper_half():
    support = (
        (0, 0, 0),
        (0, 0, 1),
        (0, 1, 1),
        (1, 0, 0),
        (1, 1, 1),
    )
    rerooted = reroot_frame_subword_support(support, (0, 0, 1))
    assert sum(row[-1] == 0 for row in rerooted) == 3
    certificate = frame_subword_entropy_induction_certificate(support)
    assert certificate.exact_induction_verified
    assert certificate.rerooting_step_count == 2
    assert certificate.induction_steps[0].rerooted
    assert certificate.induction_steps[0].zero_half_size == 3
    assert certificate.induction_steps[0].one_half_size == 2
    assert certificate.universal_finite_group_solution_exponent_upper_bound == (
        pytest.approx(3 - math.log2(5))
    )


def test_universal_bound_dominates_exact_S3_counts_through_width_three():
    order = 6
    for width in range(1, 4):
        cube = tuple(itertools.product((0, 1), repeat=width))
        for mask in range(1 << (len(cube) - 1)):
            support = (
                cube[0],
                *(
                    row
                    for index, row in enumerate(cube[1:])
                    if mask >> index & 1
                ),
            )
            certificate = frame_subword_entropy_induction_certificate(support)
            exact_count = presentation_solution_count(
                3,
                range(1, width + 1),
                frame_subword_relations(support),
            )
            bound = order ** (
                certificate.universal_finite_group_solution_exponent_upper_bound
            )
            assert exact_count <= bound + 1e-12


def test_suffix_branch_entropy_gives_explicit_integer_generator_bound():
    support = (
        (0, 0, 0),
        (0, 0, 1),
        (0, 1, 0),
        (1, 0, 0),
        (1, 1, 1),
    )
    certificate = frame_subword_suffix_branch_certificate(support)
    assert certificate.entropy_codimension == pytest.approx(3 - math.log2(5))
    assert certificate.universal_finite_group_generator_upper_bound == 0
    assert not certificate.suffix_forced_coordinates
    assert certificate.suffix_branch_coordinates == (1, 2, 3)
    assert certificate.entropy_chain_rule_verified
    assert certificate.average_forced_bound_verified
    assert certificate.explicit_anchor_bound_verified
    assert certificate.exact_suffix_branch_elimination_verified


def test_suffix_branch_generator_bound_holds_for_every_support_through_width_three():
    for width in range(1, 4):
        cube = tuple(itertools.product((0, 1), repeat=width))
        for mask in range(1, 1 << len(cube)):
            support = tuple(
                row for index, row in enumerate(cube) if mask >> index & 1
            )
            certificate = frame_subword_suffix_branch_certificate(support)
            expected = width - (len(support) - 1).bit_length()
            assert certificate.universal_finite_group_generator_upper_bound == expected
            assert len(certificate.suffix_forced_coordinates) <= expected
            assert certificate.exact_suffix_branch_elimination_verified


def test_monotone_chain_tietze_eliminates_every_frame():
    width = 9
    support = tuple(
        tuple(int(index >= width - weight) for index in range(width))
        for weight in range(width + 1)
    )
    reduction = frame_subword_reduction(support)
    assert len(reduction.elimination_steps) == width
    assert not reduction.remaining_generators
    control = audit_frame_subword_entropy("CHAIN", support)
    assert control.frame_solution_exponent_upper_bound == 0
    assert control.pressure_inequality_certified


def test_even_parity_code_leaves_only_an_involution():
    width = 5
    support = tuple(
        row
        for row in itertools.product((0, 1), repeat=width)
        if sum(row) % 2 == 0
    )
    control = audit_frame_subword_entropy("PARITY", support)
    assert control.frame_solution_exponent_upper_bound == pytest.approx(0.5)
    assert control.exponent_certificate_source == "single-nonorientable-surface-genus-1"
    assert control.entropy_margin == pytest.approx(0.5)


def test_nested_blocks_falsify_edge_pivots_but_pass_full_subword_bound():
    support = (
        (0, 0, 0, 0),
        (1, 1, 0, 0),
        (1, 1, 1, 1),
    )
    reduction = frame_subword_reduction(support)
    assert len(reduction.elimination_steps) == 2
    assert len(reduction.remaining_generators) == 2
    control = audit_frame_subword_entropy("NESTED", support)
    assert control.frame_solution_exponent_upper_bound == 2
    assert control.entropy_margin > 0


def test_torsion_residual_uses_exact_coprime_power_collapse():
    support = (
        (0, 0, 0, 0),
        (0, 0, 1, 1),
        (0, 1, 0, 1),
        (0, 1, 1, 0),
        (1, 0, 0, 1),
        (1, 0, 1, 0),
        (1, 1, 0, 0),
        (1, 1, 1, 0),
        (1, 1, 1, 1),
    )
    control = audit_frame_subword_entropy("TORSION", support)
    assert control.residual_relations == ((-4, -4), (-4, -4, -4))
    assert control.frame_solution_exponent_upper_bound == 0
    assert control.exponent_certificate_source == (
        "multi-relator-coprime-pure-power-collapse"
    )
    assert control.pressure_inequality_certified


def test_nonzero_base_support_is_rejected_by_the_scope_gate():
    with pytest.raises(ValueError, match="zero assignment"):
        audit_frame_subword_entropy("NO-ZERO", ((1, 0), (0, 1)))


def test_report_separates_all_width_proof_from_finite_controls():
    report = run_frame_subword_entropy()
    metrics = report.headline_metrics
    assert metrics[
        "exhaustively_checked_zero_support_count_through_width_four"
    ] == 32906
    assert metrics["exhaustive_pressure_failure_count_through_width_four"] == 0
    assert metrics["width_five_stress_failure_count"] == 0
    assert metrics["complete_width_four_zero_based_pressure_theorem_count"] == 1
    assert metrics["growing_width_frame_subword_entropy_theorem_count"] == 1
    assert metrics["growing_width_suffix_branch_generator_theorem_count"] == 1
    assert report.claim_gate["all_zero_based_supports_through_width_four_certified"]
    assert report.claim_gate["growing_width_frame_subword_entropy_proved"]
    assert report.claim_gate[
        "growing_width_suffix_branch_generator_bound_proved"
    ]
    assert not report.claim_gate["nonzero_base_assignments_certified"]
    assert not report.claim_gate["speedup_claim_allowed"]
