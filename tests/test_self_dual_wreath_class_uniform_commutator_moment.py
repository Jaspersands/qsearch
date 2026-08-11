from fractions import Fraction
from functools import lru_cache

import pytest

from self_dual_wreath_class_uniform_commutator_moment import (
    class_uniform_commutator_theorem,
    conjugate_partition,
    direct_plancherel_moment_average,
    extremal_character_moment_control,
    irrep_class_moment,
    plancherel_moment_control,
    reciprocal_class_average,
    run_class_uniform_commutator_moment,
)


@lru_cache(maxsize=1)
def _report():
    return run_class_uniform_commutator_moment(maximum_extremal_degree=14)


def test_standard_s3_moment_matches_translated_parity_control():
    moment = irrep_class_moment((2, 1))
    assert moment.dimension == 2
    assert moment.class_second_moment_sum == 5
    assert Fraction(moment.exact_normalized_moment) == Fraction(5, 12)


@pytest.mark.parametrize(
    "partition",
    ((4, 1), (3, 2), (3, 1, 1), (2, 2, 1)),
)
def test_sign_twist_preserves_squared_class_moment(partition):
    conjugate = conjugate_partition(partition)
    left = irrep_class_moment(partition)
    right = irrep_class_moment(conjugate)
    assert left.conjugate_partition == conjugate
    assert left.dimension == right.dimension
    assert left.exact_normalized_moment == right.exact_normalized_moment


@pytest.mark.parametrize("degree", range(5, 11))
def test_column_orthogonality_matches_reciprocal_class_identity(degree):
    assert direct_plancherel_moment_average(degree) == reciprocal_class_average(degree)
    control = plancherel_moment_control(degree, verify_irrep_side=True)
    assert control.column_orthogonality_identity_verified


@pytest.mark.parametrize("degree", range(5, 21))
def test_symmetric_group_class_size_and_natural_source_bound(degree):
    control = plancherel_moment_control(degree)
    assert control.smallest_nonidentity_class_size >= control.transposition_class_size
    assert control.class_size_lemma_verified
    assert control.theorem_bound_verified
    assert control.reciprocal_class_average <= control.theorem_upper_bound


def test_finite_extremal_scan_preserves_small_degree_counterexamples():
    n4 = extremal_character_moment_control(4)
    assert n4.maximizing_partitions == ((2, 2),)
    assert Fraction(n4.maximum_exact_moment) == Fraction(9, 20)
    assert not n4.standard_and_sign_twist_are_only_maximizers
    assert n4.known_small_degree_exception_or_tie

    n6 = extremal_character_moment_control(6)
    assert set(n6.maximizing_partitions) == {
        (5, 1),
        (3, 3),
        (2, 2, 2),
        (2, 1, 1, 1, 1),
    }
    assert n6.known_small_degree_exception_or_tie


@pytest.mark.parametrize("degree", range(7, 15))
def test_standard_and_sign_twist_are_finite_extremizers_from_seven(degree):
    control = extremal_character_moment_control(degree)
    assert set(control.maximizing_partitions) == {
        (degree - 1, 1),
        (2, *((1,) * (degree - 2))),
    }
    assert control.standard_and_sign_twist_are_only_maximizers
    assert control.exhaustive_finite_control_verified


def test_theorem_is_natural_source_not_worst_case_claim():
    theorem = class_uniform_commutator_theorem()
    assert theorem.arbitrary_finite_group_identity
    assert theorem.all_n_symmetric_group_bound_from_degree_five
    assert theorem.natural_source_obstruction_verified
    assert not theorem.worst_case_irrep_bound_proved
    assert not theorem.standard_extremality_proved_for_all_n


def test_inverse_n_signal_has_vanishing_plancherel_tail_bound():
    small = plancherel_moment_control(10)
    large = plancherel_moment_control(30)
    assert large.inverse_n_threshold_tail_bound < small.inverse_n_threshold_tail_bound
    assert large.inverse_n_threshold_tail_bound < 0.006


def test_report_blocks_speedup_and_global_extremality_claims():
    report = _report()
    assert report.headline_metrics["exact_natural_source_no_go_theorem_count"] == 1
    assert report.headline_metrics["finite_extremal_control_failure_count"] == 0
    assert report.headline_metrics["plancherel_control_failure_count"] == 0
    assert report.headline_metrics["all_n_standard_extremality_theorem_count"] == 0
    assert not report.claim_gate["natural_plancherel_source_signal_survives"]
    assert report.claim_gate["rare_low_dimensional_signal_exists"]
    assert not report.claim_gate["rare_sector_preparation_is_free"]
    assert not report.claim_gate["standard_irrep_globally_extremal"]
    assert not report.claim_gate["speedup_claim_allowed"]
