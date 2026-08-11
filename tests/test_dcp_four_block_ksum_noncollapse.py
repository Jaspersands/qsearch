from fractions import Fraction

import pytest

from dcp_four_block_ksum_noncollapse import (
    four_block_template_certificate,
    marked_vertex_union_control,
    published_ksum_exponent,
    published_resource_record,
    residue_class_exponent_proofs,
    run_four_block_ksum_noncollapse,
    uniform_legal_multiplicity_scaling_record,
)


def test_source_recovers_seven_sum_and_two_sevenths_block_exponent() -> None:
    assert published_ksum_exponent(7) == 2
    row = published_resource_record(7)
    assert row.ksum_time_exponent_exact == "2"
    assert row.sample_exponent_exact == "2"
    assert row.subset_sum_certified_time_exponent == pytest.approx(2 / 7)
    assert row.subset_sum_dictionary_exponent == pytest.approx(2 / 7)


def test_all_published_fixed_k_rows_remain_exponential() -> None:
    rows = [published_resource_record(k) for k in range(4, 201)]
    assert all(row.two_sevenths_time_floor_verified for row in rows)
    assert all(row.one_fifth_dictionary_floor_verified for row in rows)
    assert min(row.subset_sum_certified_time_exponent for row in rows) == pytest.approx(2 / 7)
    assert min(row.subset_sum_dictionary_exponent for row in rows) == pytest.approx(1 / 5)
    assert not any(row.polynomial_resource_certificate for row in rows)


def test_seven_residue_classes_prove_all_k_exponent_floors() -> None:
    rows = residue_class_exponent_proofs()
    assert {row.residue_class_mod_seven for row in rows} == set(range(7))
    assert all(
        row.two_sevenths_time_floor_for_all_valid_quotients for row in rows
    )
    assert all(
        row.one_fifth_dictionary_floor_for_all_valid_quotients for row in rows
    )
    assert next(
        row for row in rows if row.residue_class_mod_seven == 5
    ).five_r_minus_k_at_minimum_quotient_exact == "0"


@pytest.mark.parametrize(
    ("block_count", "walk_total", "sample"),
    [
        (7, Fraction(4), Fraction(2)),
        (7, Fraction(3), Fraction(3, 2)),
        (14, Fraction(8), Fraction(4)),
        (21, Fraction(9), Fraction(3)),
        (21, Fraction(14), Fraction(11, 2)),
    ],
)
def test_four_block_template_has_exact_two_sevenths_floor(
    block_count: int,
    walk_total: Fraction,
    sample: Fraction,
) -> None:
    certificate = four_block_template_certificate(
        block_count,
        walk_total,
        sample,
    )
    assert certificate.two_sevenths_floor_verified
    assert Fraction(certificate.charged_exponent_exact) >= Fraction(
        2 * block_count, 7
    )


def test_template_equality_occurs_at_four_sevenths_two_sevenths_split() -> None:
    certificate = four_block_template_certificate(35, 20, 10)
    assert Fraction(certificate.charged_exponent_exact) == 10
    assert certificate.nonnegative_margin_exact == "0"


def test_uniform_legal_exponential_multiplicity_has_exponential_tail() -> None:
    row = uniform_legal_multiplicity_scaling_record(512, 0.25, 0.1)
    assert row.witness_threshold_log2 == pytest.approx(51.2)
    assert row.conditional_tail_log2_upper_bound <= -49
    assert row.exponential_tail_bound
    assert row.subexponential_multiplicity_is_typical
    assert not row.polynomial_resource_collapse_proved


def test_marked_vertex_union_bound_survives_overlapping_witness_pairs() -> None:
    control = marked_vertex_union_control(
        6,
        7,
        3,
        2,
        [(0, 0), (0, 1), (1, 0), (5, 6)],
    )
    assert control.union_bound_verified
    assert control.exact_marked_fraction <= control.witness_union_upper_bound


def test_report_keeps_all_algorithm_and_lower_bound_gates_closed() -> None:
    report = run_four_block_ksum_noncollapse()
    assert report.headline_metrics["published_exponent_certificate_failure_count"] == 0
    assert report.headline_metrics["polynomial_dcp_witness_solver_count"] == 0
    assert report.theorem.density_one_multiplicity_collapse_excluded
    assert not report.theorem.general_quantum_subset_sum_lower_bound_proved
    assert not report.claim_gate["implicit_list_free_density_one_route_closed"]
    assert not report.claim_gate["speedup_claim_allowed"]
