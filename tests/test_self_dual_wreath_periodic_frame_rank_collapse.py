import math

import pytest

from self_dual_wreath_periodic_frame_rank_collapse import (
    audit_periodic_fiber_closed_form,
    audit_periodic_suffix_branch_certificate,
    periodic_rank_collapse_scaling_records,
    periodic_same_fiber_closed_form,
    run_periodic_frame_rank_collapse,
)


def test_neutral_block_suffix_witnesses_prove_three_generator_bound():
    certificate = audit_periodic_suffix_branch_certificate()
    assert certificate.neutral_block_state == certificate.zero_neutral_block_state
    assert certificate.first_neutral_block_unresolved_coordinates == (1, 2, 5)
    assert certificate.repeated_neutral_block_branch_coordinates == tuple(
        range(1, 31)
    )
    assert certificate.terminal_block_branch_coordinates == tuple(range(1, 6))
    assert certificate.single_terminal_same_fiber_branch_coordinates == (4,)
    assert certificate.single_terminal_exception_branch_coordinates == (5,)
    assert certificate.universal_finite_group_frame_generator_upper_bound == 3
    assert certificate.exact_suffix_branch_elimination_lemma_applied
    assert certificate.neutral_concatenation_induction_verified
    assert all(
        witness.bit_flipped
        and witness.strict_suffix_agreement
        and witness.witness_state_verified
        for witness in (
            *certificate.first_neutral_block_witnesses,
            *certificate.repeated_neutral_block_witnesses,
            *certificate.terminal_block_witnesses,
            *certificate.single_terminal_witnesses,
        )
    )


def test_transfer_annihilator_gives_exact_subsequence_fiber_formula():
    certificate = audit_periodic_fiber_closed_form()
    assert certificate.recurrence_roots == (2**30, 2**24, 2**6, 1)
    assert certificate.transfer_fiber_sizes == certificate.closed_form_fiber_sizes
    assert certificate.transfer_fiber_sizes[:3] == (
        2,
        1923787406,
        2049888430391468942,
    )
    assert periodic_same_fiber_closed_form(0) == 2
    assert certificate.initial_values_determine_closed_form
    assert certificate.closed_form_verified
    assert certificate.uniform_density_bound_verified


def test_rank_collapse_gives_uniform_positive_scalar_pressure_margin():
    records = periodic_rank_collapse_scaling_records(8)
    lower_bound = 1.0 - 0.5 * math.log2(3.0 / 2.0)
    assert all(row.frame_generator_upper_bound == 3 for row in records)
    assert all(
        row.full_solution_exponent_before_conjugacy_classes == 4
        for row in records
    )
    assert all(row.scalar_crossing_pressure_margin > 0 for row in records)
    assert min(row.scalar_crossing_pressure_margin for row in records) == pytest.approx(
        lower_bound
    )
    assert records[-1].scalar_crossing_pressure_margin == pytest.approx(
        math.log2(18) - 3,
        rel=1e-12,
    )


def test_report_falsifies_periodic_family_without_claiming_algorithm():
    report = run_periodic_frame_rank_collapse()
    assert report.headline_metrics["all_period_suffix_branch_rank_theorem_count"] == 1
    assert report.headline_metrics["periodic_family_leading_Sn_mass_count"] == 0
    assert report.claim_gate["periodic_frame_rank_collapse_proved"]
    assert report.claim_gate["periodic_family_uniformly_subleading_in_Sn"]
    assert not report.claim_gate["periodic_family_survives"]
    assert not report.claim_gate["speedup_claim_allowed"]
    assert all(row["resolved"] for row in report.proof_obligations)
