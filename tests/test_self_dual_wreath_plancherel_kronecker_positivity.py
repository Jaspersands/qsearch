import math
from fractions import Fraction

from self_dual_wreath_plancherel_kronecker_positivity import (
    audit_kronecker_positivity,
    centralizer_order,
    reciprocal_class_scaling_record,
    reciprocal_nonidentity_class_sum,
    run_plancherel_kronecker_positivity,
)


def test_centralizer_and_reciprocal_class_sum_controls() -> None:
    assert centralizer_order((1, 1, 1, 1)) == 24
    assert centralizer_order((2, 1, 1)) == 4
    assert centralizer_order((2, 2)) == 8
    assert reciprocal_nonidentity_class_sum(3) == Fraction(5, 6)
    assert reciprocal_nonidentity_class_sum(4) == Fraction(19, 24)


def test_exact_plancherel_variance_identity_through_s8() -> None:
    controls = [audit_kronecker_positivity(n) for n in range(3, 9)]
    assert all(record.exact_variance_identity_verified for record in controls)
    assert all(record.zero_probability_bound_verified for record in controls)
    assert all(record.exact_normalized_remainder_mean == "0" for record in controls)
    assert all(
        record.exact_normalized_remainder_second_moment
        == record.exact_reciprocal_nonidentity_class_sum
        for record in controls
    )


def test_actual_zero_probability_is_strictly_below_variance_bound() -> None:
    for n in range(3, 9):
        record = audit_kronecker_positivity(n)
        assert Fraction(record.exact_zero_probability) < Fraction(
            record.exact_reciprocal_nonidentity_class_sum
        )


def test_reciprocal_class_bound_decays_and_is_transposition_dominated() -> None:
    records = [reciprocal_class_scaling_record(n) for n in (10, 20, 30, 40, 50)]
    assert all(
        right.reciprocal_nonidentity_class_sum
        < left.reciprocal_nonidentity_class_sum
        for left, right in zip(records, records[1:])
    )
    assert records[-1].reciprocal_nonidentity_class_sum < 0.001
    assert records[-1].transposition_fraction_of_sum > 0.9
    assert all(record.asymptotic_bound_proved for record in records)


def test_report_scopes_the_new_positivity_theorem_correctly() -> None:
    report = run_plancherel_kronecker_positivity()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate[
        "independent_plancherel_ordinary_kronecker_positive_aas_proved"
    ]
    assert report.claim_gate["natural_hamming_three_common_support_aas_proved"]
    assert not report.claim_gate[
        "arbitrarily_coupled_plancherel_positivity_proved"
    ]
    assert not report.claim_gate["uniform_partition_positivity_proved"]
    assert not report.claim_gate["hamming_three_incidence_rank_or_edge_controlled"]
    assert not report.claim_gate["speedup_claim_allowed"]
