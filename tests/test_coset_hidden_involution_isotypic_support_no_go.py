from fractions import Fraction

import pytest

from coset_hidden_involution_isotypic_support_no_go import (
    audit_isotypic_law_control,
    build_isotypic_support_no_go_report,
    character_total_variation_upper_bound,
    diagonal_isotypic_label_laws,
    elementary_isotypic_tv_upper_bound,
    fixed_point_class_count,
    fixed_point_free_threshold_copy_count,
    isotypic_support_scaling_record,
    isotypic_total_variation,
    permutation_of_cycle_type,
    write_isotypic_support_no_go_report,
)


def test_cycle_representatives_and_fixed_point_counts_are_exact():
    permutation = permutation_of_cycle_type((3, 1))
    assert permutation == (1, 2, 0, 3)
    assert fixed_point_class_count(4, 2, (4,)) == 1
    assert fixed_point_class_count(4, 2, (3, 1)) == 3
    assert fixed_point_class_count(4, 2, (2, 2)) == 2
    assert fixed_point_class_count(4, 2, (1, 1, 1, 1)) == 0

    with pytest.raises(ValueError, match="nonempty"):
        permutation_of_cycle_type(())
    with pytest.raises(ValueError, match="wrong degree"):
        fixed_point_class_count(4, 2, (3,))


@pytest.mark.parametrize(
    ("n", "transpositions", "copies", "expected_tv"),
    (
        (3, 1, 1, Fraction(0)),
        (3, 1, 2, Fraction(0)),
        (3, 1, 3, Fraction(0)),
        (4, 2, 2, Fraction(1, 6)),
    ),
)
def test_exact_class_law_matches_direct_fixed_point_trace(
    n, transpositions, copies, expected_tv
):
    laws, _ = diagonal_isotypic_label_laws(n, transpositions, copies)
    assert sum(row[1] for row in laws) == 1
    assert sum(row[2] for row in laws) == 1
    assert isotypic_total_variation(n, transpositions, copies) == expected_tv

    row = audit_isotypic_law_control(n, transpositions, copies)
    assert row.finite_control_verified
    assert row.exact_direct_law_residual == 0
    assert row.exact_isotypic_total_variation == float(expected_tv)
    assert row.character_bound_respected


def test_odd_perfect_matching_parity_makes_s6_label_law_identical():
    # Fixed-point-free involutions in S_6 are odd.  Multiplication changes
    # parity, so gh cannot be conjugate to g and every z_K vanishes.
    laws, fixed_counts = diagonal_isotypic_label_laws(6, 3, 6)
    assert all(value == 0 for value in fixed_counts.values())
    assert all(null == alternative for _, null, alternative in laws)
    assert isotypic_total_variation(6, 3, 6) == 0


def test_all_n_threshold_bound_forces_proper_multiplicity_support():
    rows = [
        isotypic_support_scaling_record(n)
        for n in (6, 8, 16, 32, 64, 128)
    ]
    assert all(row.copy_count >= row.n for row in rows)
    assert all(
        row.class_count_total_variation_upper_bound
        <= row.elementary_total_variation_upper_bound
        for row in rows
    )
    assert rows[0].elementary_total_variation_upper_bound == pytest.approx(1 / 9)
    assert all(
        row.elementary_total_variation_upper_bound <= 1 / 9 for row in rows
    )
    assert all(
        row.whole_isotypic_support_required_total_variation >= 3 / 4
        for row in rows
    )
    assert all(row.proper_multiplicity_support_forced for row in rows)
    assert all(
        not row.diagonal_group_algebra_support_compiler_possible for row in rows
    )
    assert all(not row.commutant_side_support_compiler_ruled_out for row in rows)

    assert fixed_point_free_threshold_copy_count(6) == 6
    assert elementary_isotypic_tv_upper_bound(6) == Fraction(1, 9)
    with pytest.raises(ValueError, match="even"):
        elementary_isotypic_tv_upper_bound(7)


def test_character_bound_dominates_exact_finite_signal():
    exact = isotypic_total_variation(4, 2, 2)
    bound = character_total_variation_upper_bound(4, 2, 2)
    assert exact == Fraction(1, 6)
    assert bound == Fraction(11, 16)
    assert exact <= bound


def test_report_upgrades_finite_witness_but_keeps_commutant_route_open(tmp_path):
    report = build_isotypic_support_no_go_report(
        finite_specs=((3, 1, 2), (4, 2, 2)),
        scaling_n_values=(6, 8, 16, 32),
    )
    assert report.theorem.theorem_verified
    assert report.theorem.exact_isotypic_law_proved
    assert report.theorem.all_n_total_variation_bound_proved
    assert report.theorem.all_n_proper_multiplicity_support_proved
    assert report.theorem.diagonal_group_action_compiler_refuted
    assert not report.theorem.commutant_side_compiler_refuted
    assert not report.theorem.arbitrary_circuit_lower_bound_proved
    assert report.claim_gate["all_n_proper_multiplicity_support_proved"]
    assert not report.claim_gate["commutant_side_support_compiler_refuted"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_isotypic_support_no_go_report(
        tmp_path / "isotypic-support.json",
        finite_specs=((3, 1, 2),),
        scaling_n_values=(6, 8),
    )
    assert payload["status"] == (
        "all-n-diagonal-isotypic-support-compiler-refuted-commutant-route-open"
    )
    assert payload["headline_metrics"][
        "all_n_proper_multiplicity_support_theorem_count"
    ] == 1
