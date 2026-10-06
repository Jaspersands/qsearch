from fractions import Fraction
from itertools import combinations, product

from flint import nmod_mat
import pytest

from ternary_schur_closure import schur_admission
from ternary_schur_retention_bound import (
    certified_restriction, exact_kernel_certificate, exhaustive_source_control,
    iid_retention_envelope, projective_words, retention_bound, run_controls,
    short_word_union_bound,
)
from ternary_schur_tensor import combine


def subspace_frames(dimension):
    representatives, seen = projective_words(dimension), set()
    for k in range(1, dimension+1):
        for frame in combinations(representatives, k):
            rref, r = nmod_mat(frame, 3).rref()
            if r != k:
                continue
            key = tuple(tuple(int(rref[i, j]) for j in range(dimension)) for i in range(k))
            if key not in seen:
                seen.add(key)
                yield key


@pytest.mark.parametrize("low_rows", [((1, 1, 1),), ((1, 1, 1, 1),), ((0, 0, 0),),
    ((1, 0, 1, 1), (0, 1, 1, 2)), ((1, 0, 0, 2), (0, 1, 0, 2), (0, 0, 1, 2))])
def test_all_small_native_kernel_subspaces_obey_distance_retention_bound(low_rows):
    certificate = exact_kernel_certificate(low_rows)
    basis = certificate["physical_kernel_basis"]
    m, distance = len(low_rows[0]), certificate["minimum_distance"]
    tested = 0
    for logical in subspace_frames(len(basis)):
        physical = tuple(combine(basis, c, m) for c in logical)
        support = sum(any(c[i] for c in physical) for i in range(m))
        for degree in (1, 3, 5, 9):
            gate = schur_admission(low_rows, physical, degree)
            bound = retention_bound(support, degree, distance)
            if gate["higher_Schur_admission"]:
                assert len(physical) <= bound["maximum_admitted_frame_dimension"]
            tested += 1
    assert tested > 0


@pytest.mark.parametrize("support,degree,distance,ceiling", [(12, 3, 5, 3), (12, 3, 3, 4),
    (12, 9, 3, 4), (12, 1, 5, 8), (8, 3, 8, 1), (512, 19, 71, 24)])
def test_correct_product_singleton_branch_and_integer_rounding(support, degree, distance, ceiling):
    bound = retention_bound(support, degree, distance)
    assert bound["maximum_admitted_frame_dimension"] == ceiling
    assert bound["product_Singleton_power_used"] == min(degree, distance)
    assert bound["valid_for_source_adaptively_selected_linear_frames"]
    assert not bound["requires_projective_saturation"]
    assert not bound["distance_certified_by_this_arithmetic_ledger"]
    assert not bound["nonlinear_or_arbitrary_quantum_receiver_no_go"]


def test_exact_distance_certificate_matches_direct_all_ambient_words():
    rows = ((1, 0, 1, 1), (0, 1, 1, 2))
    certificate = exact_kernel_certificate(rows)
    actual = [w for w in projective_words(4) if all(sum(a*b for a, b in zip(row, w)) % 3 == 0 for row in rows)]
    assert certificate["minimum_distance"] == min(sum(bool(x) for x in w) for w in actual) == 3
    assert certificate["projective_kernel_words_enumerated"] == len(actual)
    assert certificate["bounded_exhaustive_certificate_not_scalable_distance_algorithm"]


def test_sharp_admitted_frame_and_excluded_full_kernel_have_actual_distance_certificate():
    report = run_controls()
    positive, negative = report["sharp_disjoint_restriction_control"], report["full_kernel_retention_countercontrol"]
    assert positive["restriction_admission"]["higher_Schur_admission"]
    assert positive["retention_bound"]["maximum_admitted_frame_dimension"] == 2
    assert positive["distance_certificate"]["minimum_distance"] == 2
    assert negative["high_retention_claim_excluded_by_bound"]
    assert not negative["restriction_admission"]["higher_Schur_admission"]
    assert negative["restriction_admission"]["mixed_failure_witness"]
    assert not positive["full_phase_instrument_or_decoder_supplied"]


@pytest.mark.parametrize("n", [1, 2])
def test_union_bound_upper_bounds_actual_complete_IID_source_failure(n):
    control = exhaustive_source_control(n, 3)
    assert control["all_source_matrices_enumerated"] == 3**(3*n)
    assert sum(control["minimum_distance_histogram"].values()) == 3**(3*n)
    for c in control["distance_checks"]:
        actual, upper = c["actual_failure_probability"], c["envelope"]["distance_failure_probability_upper_bound"]
        assert Fraction(int(actual["numerator"]), int(actual["denominator"])) <= Fraction(int(upper["numerator"]), int(upper["denominator"]))
    if n == 2:
        assert control["minimum_distance_histogram"] == {1: 217, 2: 320, 3: 192}


def test_projective_short_word_count_does_not_double_count_signs():
    bound = short_word_union_bound(4, 7, 3)
    assert bound["projective_short_words"] == str(7+2*21)
    assert bound["each_projective_word_kernel_probability_denominator"] == "81"
    assert bound["simultaneous_for_all_source_adaptive_frames"]
    assert not bound["certifies_this_particular_matrix"]
    assert not bound["conditions_on_full_row_rank"]


def test_statistical_distance_envelope_cannot_be_promoted_to_matrix_certificate():
    record = iid_retention_envelope(256, 512, 19)
    source = record["source_distance_envelope"]
    failure = source["distance_failure_probability_upper_bound"]
    assert Fraction(int(failure["numerator"]), int(failure["denominator"])) <= Fraction(1, 1000)
    assert source["kernel_distance_lower_bound"] > 19
    assert record["simultaneous_adaptive_frame_retention_bound"]["maximum_admitted_frame_dimension"] < 30
    assert not record["individual_matrix_distance_certificate_supplied"]
    assert not record["complete_algorithm_sample_complexity_bound"]
    assert not source["postselected_or_correlated_source_transfer_proved"]


def test_input_scope_rejects_invalid_distance_degrees_and_overlarge_calibrations():
    for values in ((0, 3, 1), (4, 2, 1), (4, 3, 5), (4, True, 1), (4, 513, 1)):
        with pytest.raises(ValueError):
            retention_bound(*values)
    for values in ((3, 3, 1), (1, 4, 5), (1, 4097, 2), (True, 3, 1)):
        with pytest.raises(ValueError):
            short_word_union_bound(*values)
    with pytest.raises(ValueError):
        exact_kernel_certificate(((0,)*9,))
    for rows in (((True, 1, 1),), ((3, 1, 1),), ((1, 1, 1), (1,))):
        with pytest.raises(ValueError):
            exact_kernel_certificate(rows)
    with pytest.raises(ValueError):
        exhaustive_source_control(3, 4)
    with pytest.raises(ValueError):
        iid_retention_envelope(2, 4, 3, 0)


def test_claim_gate_remains_closed():
    assert not any(run_controls()["claim_gate"].values())
