"""Try to kill the cheap linear-decoder replacement for coherent filtering."""
from fractions import Fraction
from itertools import product

import numpy as np
import pytest

from ternary_decoder_filter import (
    audit_filter, linear_erasure_right_inverse, linear_erasure_classical_output,
    linear_erasure_reference,
)


def test_every_full_rank_one_row_source_and_every_right_inverse_matches_full_physics():
    checked = 0
    for row in product(range(3),repeat=3):
        if not any(row):
            continue
        for r in product(range(3),repeat=3):
            if sum(x*y for x,y in zip(row,r)) % 3 != 1:
                continue
            R = tuple((x,) for x in r)
            result = audit_filter((row,),decoder_mode="linear-right-inverse",linear_right_inverse=R)
            comparison = result["linear_erasure_classical_comparison"]
            assert comparison["actual_full_output_distribution_max_error"] < 1e-12
            assert not result["failure_branches_discarded_or_renormalized"]
            assert abs(result["unheralded_state_norm_squared"]-1) < 1e-12
            checked += 1
    assert checked == 26*9


@pytest.mark.parametrize("A", [
    ((1,0,1,2),(0,1,2,2)),
    ((1,2,0,1,1),(2,1,1,0,2)),
    ((1,0),(0,1)),
])
def test_vector_sources_whole_distribution_not_just_success(A):
    result = audit_filter(A,3,decoder_mode="linear-right-inverse")
    comparison = result["linear_erasure_classical_comparison"]
    exact = [Fraction(x["numerator"],x["denominator"])
             for x in comparison["all_classical_output_probabilities"]]
    assert sum(exact) == 1
    np.testing.assert_allclose(comparison["actual_quantum_output_probabilities"],
                               [float(x) for x in exact],atol=1e-12)
    assert not comparison["new_algorithmic_advantage"]


def test_systematic_inverse_is_random_free_assignment_not_a_hard_decoder():
    A = ((1,0,1,2,0),(0,1,2,1,1))
    reference = linear_erasure_reference(A)
    for word,count in reference["all_output_counts"].items():
        assert all(x in (1,2) for x in word[2:])
        assert count == 2**2  # Original pivot signs are completely projected out.
        assert all(sum(x*y for x,y in zip(row,word)) % 3 == 0 for row in A)
    valid = sum(all(word) for word in reference["all_output_counts"])
    assert reference["all_nonzero_success"] == Fraction(valid,2**3)


def test_residual_global_translation_does_not_change_linear_classical_equivalence():
    A = ((1,1,2,0),)
    for offset in ((0,),(1,),(2,)):
        result = audit_filter(A,decoder_mode="linear-right-inverse",decoder_offset=offset)
        assert result["linear_erasure_classical_comparison"]["actual_full_output_distribution_max_error"] < 1e-12


def test_complete_systematic_matrix_census_has_exponential_dimension_penalty():
    # For H=[I|C], every fixed nonzero free sign word gives uniform -C e.
    # Averaging ALL C, not favorable rerolls, gives exactly (2/3)^n.
    n,k = 2,2
    mean = Fraction()
    for flat in product(range(3),repeat=n*k):
        C = [flat[i*k:(i+1)*k] for i in range(n)]
        A = tuple(tuple(int(i == j) for j in range(n))+C[i] for i in range(n))
        reference = linear_erasure_reference(A)
        mean += reference["all_nonzero_success"]
        # At every C it is exactly uniform free-assignment Gaussian elimination.
        for e in product((1,2),repeat=k):
            expected = tuple(-sum(x*y for x,y in zip(row,e)) % 3 for row in C)+e
            assert expected in reference["all_output_counts"]
    assert mean/3**(n*k) == Fraction(2,3)**n


def test_sampler_is_polynomial_and_never_calls_the_binary_error_decoder(monkeypatch):
    import ternary_decoder_filter as module
    def forbidden(*args,**kwargs):
        raise AssertionError("hidden solver or exponential enumeration called")
    n,m = 32,96
    A = tuple(tuple(int(i == j) if j < n else (i*j+i+j) % 3 for j in range(m))
              for i in range(n))
    signs = tuple(1+i % 2 for i in range(m))
    monkeypatch.setattr(module,"decode_ternary_binary_error",forbidden)
    monkeypatch.setattr(module.itertools,"product",forbidden)
    word = linear_erasure_classical_output(A,signs)
    assert len(word) == m
    assert all(sum(x*y for x,y in zip(row,word)) % 3 == 0 for row in A)


@pytest.mark.parametrize("A", [(),((1,),(2,)),((3,),),((True,),),((1,2),(0,))])
def test_bad_or_rank_deficient_source_cannot_gain_free_inverse(A):
    with pytest.raises(ValueError):
        linear_erasure_right_inverse(A)


def test_wrong_inverse_invalid_coins_and_exponential_reference_budget_rejected():
    A = ((1,0,1),(0,1,1))
    with pytest.raises(ValueError):
        linear_erasure_classical_output(A,(1,1,1),right_inverse=((0,0),)*3)
    with pytest.raises(ValueError):
        linear_erasure_classical_output(A,(1,0,2))
    with pytest.raises(ValueError):
        audit_filter(A,linear_right_inverse=linear_erasure_right_inverse(A))
    with pytest.raises(ValueError,match="verification cap"):
        linear_erasure_reference(A,cap=4)
