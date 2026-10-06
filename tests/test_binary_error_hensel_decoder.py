import itertools
import random
from fractions import Fraction

import pytest

from binary_error_hensel_decoder import (
    _coefficient_and_translation_controls, _pointwise_small_source_control,
    _row_function_controls, decode_binary_error, feature_dimension,
    lowbit_equation, parity_feature_word, pointwise_rank_source_certificate,
    translated_feature_map,
)
from dcp_physical_phase_noise import read


def test_complete_polynomial_and_affine_secret_translation_identities():
    row=_coefficient_and_translation_controls()
    assert row["complete_mod_four_polynomial_evaluations"] == 17472
    assert row["secret_error_affine_feature_source_translations"] == 768


def test_feature_coordinates_must_include_binary_addition_carry():
    T,c=translated_feature_map((1,3))
    for low,high in itertools.product(range(4),repeat=2):
        y=parity_feature_word(low,high,2)
        transformed=c ^ sum(((row&y).bit_count()%2)<<j for j,row in enumerate(T))
        x=tuple((s+(low>>j&1)+2*(high>>j&1))%4 for j,s in enumerate((1,3)))
        xl=sum((v&1)<<j for j,v in enumerate(x))
        xh=sum((v>>1&1)<<j for j,v in enumerate(x))
        assert transformed == parity_feature_word(xl,xh,2)
    assert T[2] & 1  # Carry from the low bit changes the lift coordinate.


def test_native_feature_rows_are_not_assumed_uniform_unstructured_bits():
    rows=_row_function_controls()
    assert [read(r["minimum_nonzero_row_function_mass"]) for r in rows] == [Fraction(1,2),Fraction(1,4),Fraction(1,4)]
    assert [r["all_nonzero_feature_functions"] for r in rows] == [3,31,511]
    certificate=pointwise_rank_source_certificate(8,132,33)
    assert not certificate["coefficient_matrix_is_an_IID_unstructured_d_bit_matrix"]
    assert certificate["conservative_rank_failure_dyadic_exponent"] == 8


def test_complete_pointwise_source_census_has_same_rank_law_for_all_secrets_errors():
    row=_pointwise_small_source_control()
    assert row["every_fixed_secret_and_error_law_controls"] == 32
    assert row["common_rank_histogram"][2] == 42
    assert read(row["exact_pointwise_success_probability"]) == Fraction(21,32)


@pytest.mark.parametrize("n,L",[(1,2),(2,3),(4,17),(8,33),(16,65)])
def test_actual_growing_modulus_decoder_recovers_arbitrary_fixed_error_patterns(n,L):
    rng=random.Random(800+17*n+L)
    q=1<<L
    m=3*feature_dimension(n)
    A=tuple(tuple(rng.randrange(q) for _ in range(m)) for _ in range(n))
    secret=tuple(rng.randrange(q) for _ in range(n))
    for errors in ((0,)*m,(1,)*m,tuple(i%2 for i in range(m))):
        b=tuple((sum(A[j][i]*secret[j] for j in range(n))+errors[i])%q for i in range(m))
        result=decode_binary_error(A,b,q)
        assert result["status"] == "CERTIFIED_UNIQUE_BINARY_ERROR_SECRET"
        assert result["secret"] == secret
        assert result["verified_errors"] == errors
        assert result["feature_rank"] == feature_dimension(n)
        assert len(result["hensel_lifts"]) == L-2
        assert not result["secret_assignments_or_target_fibers_enumerated"]
        assert not result["native_subset_sum_witness_finder_supplied"]


def test_certified_small_decoding_agrees_with_complete_binary_error_root_set():
    rng=random.Random(915)
    for _ in range(24):
        n,q,m=2,8,15
        A=tuple(tuple(rng.randrange(q) for _ in range(m)) for _ in range(n))
        secret=tuple(rng.randrange(q) for _ in range(n))
        errors=tuple(rng.randrange(2) for _ in range(m))
        b=tuple((sum(A[j][i]*secret[j] for j in range(n))+errors[i])%q for i in range(m))
        result=decode_binary_error(A,b,q)
        roots=[s for s in itertools.product(range(q),repeat=n) if all(
            (b[i]-sum(A[j][i]*s[j] for j in range(n)))%q in (0,1) for i in range(m))]
        if result["secret"] is not None:
            assert roots == [result["secret"]]
        else:
            assert result["status"] == "LOWBIT_FEATURE_RANK_DEFICIENT"


def test_nonbinary_source_is_not_promoted_from_annihilator_congruences():
    A=((1,2,3,0,1,2),)
    result=decode_binary_error(A,(0,0,0,0,2,0),8)
    assert result["secret"] is None
    assert result["status"] != "CERTIFIED_UNIQUE_BINARY_ERROR_SECRET"
    deficient=decode_binary_error(((0,0),),(0,1),4)
    assert deficient["status"] == "LOWBIT_FEATURE_RANK_DEFICIENT"


def test_polynomial_zero_does_not_mean_general_ring_square_free_or_field_algorithms():
    # Consecutive factors over2^L are special: one is an invertible odd number.
    for L in range(2,7):
        q=1<<L
        roots=[z for z in range(q) if z*(z+1)%q == 0]
        assert roots == [0,q-1]
    certificate=pointwise_rank_source_certificate(16,456,65)
    assert certificate["conservative_rank_failure_dyadic_exponent"] == 30
    assert not certificate["label_dependent_error_vector_allowed"]
    assert not certificate["native_boolean_subset_sum_or_general_LWE_solved"]


def test_rejects_wrong_modulus_and_malformed_input():
    for q in (2,3,6,7):
        with pytest.raises(ValueError):
            decode_binary_error(((1,2),),(0,1),q)
    for A,b in (((),()),(((1,),()),(0,)),(((1,2),),(0,)),(((True,2),),(0,1)),(((1,2),),(0,8))):
        with pytest.raises(ValueError):
            decode_binary_error(A,b,8)
    with pytest.raises(ValueError):
        pointwise_rank_source_certificate(1,1,1)
    with pytest.raises(ValueError):
        translated_feature_map((4,))
    with pytest.raises(ValueError):
        parity_feature_word(4,0,2)
