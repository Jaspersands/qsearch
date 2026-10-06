import itertools
import random

import numpy as np
import pytest
import sympy as sp

from ternary_quotient_decoder import (
    Span, _annihilator, decode_ternary_binary_error, invariant_closure,
    monomial_dimension, monomials, run_controls, single_sample_image_certificate,
)


def roots(A, b):
    # Independent bounded verifier ONLY, never called by the decoder.
    return [s for s in itertools.product(range(3), repeat=len(A)) if all(
        (b[i]-sum(A[j][i]*s[j] for j in range(len(A)))) % 3 in (0,1) for i in range(len(b)))]


def test_complete_one_variable_sources_match_full_quotient_and_never_choose_arbitrary_root():
    for A in itertools.product(range(3), repeat=2):
        for b in itertools.product(range(3), repeat=2):
            for D in (2,3):
                result = decode_ternary_binary_error((A,),b,D)
                actual = roots((A,),b)
                if result["status"] == "LEADING_DEGREE_CERTIFICATE_FAILED":
                    assert result["secret"] is None
                    continue
                assert result["quotient_dimension"] == len(actual)
                assert result["secret"] == (actual[0] if len(actual) == 1 else None)


def test_random_two_variable_sources_match_complete_roots_at_different_degrees():
    rng = random.Random(9106)
    for _ in range(16):
        A = tuple(tuple(rng.randrange(3) for _ in range(4)) for _ in range(2))
        b = tuple(rng.randrange(3) for _ in range(4))
        actual = roots(A,b)
        for D in (2,3,5):
            result = decode_ternary_binary_error(A,b,D)
            if "quotient_dimension" in result:
                assert result["quotient_dimension"] == len(actual)
                assert result["secret"] == (actual[0] if len(actual) == 1 else None)


def test_leading_rank_alone_does_not_certify_secret_or_consistency():
    multiple = decode_ternary_binary_error(((1,),),(0,),2)
    assert multiple["leading_rank"] == 1
    assert multiple["status"] == "MULTIPLE_BINARY_ERROR_SECRETS"
    assert multiple["quotient_dimension"] == 2
    bad = decode_ternary_binary_error(((1,1,1),),(0,1,2),2)
    assert bad["leading_rank"] == 1
    assert bad["status"] == "INCONSISTENT_BINARY_ERROR_EQUATIONS"
    assert bad["quotient_dimension"] == 0


def test_missing_leading_certificate_fails_closed_even_with_a_true_root():
    result = decode_ternary_binary_error(((0,0),),(0,1),2)
    assert result["status"] == "LEADING_DEGREE_CERTIFICATE_FAILED"
    assert result["secret"] is None
    assert roots(((0,0),),(0,1)) == [(0,),(1,),(2,)]


def test_invariant_closure_processes_new_vectors_until_stability():
    X = np.asarray(((0,0,1),(1,0,0),(0,1,0)),dtype=np.int64)
    relations, initial, processed = invariant_closure(((1,0,0),),(X,))
    assert initial == 1 and processed == 3 and len(relations.rows) == 3
    assert all(not np.any(relations.reduce(X@v % 3)) for v in relations.rows.values())


def test_sympy_independently_verifies_actual_rewrites_and_multiplication_lifts():
    row = run_controls()["actual_fixed_source_decoder_trials"][0]
    A,b,result = row["labels"],row["observations"],row["result"]
    x = sp.symbols(f"x0:{len(A)}")
    equations = [sum(A[j][i]*x[j] for j in range(len(A)))-b[i] for i in range(len(b))]
    G = sp.groebner([z*(z+1) for z in equations]+[v**3-v for v in x],*x,modulus=3)
    certificate = result["algebra_certificate"]
    monomial = lambda alpha: sp.prod(v**e for v,e in zip(x,alpha))
    low = [monomial(alpha) for alpha in certificate["low_monomials"]]
    polynomial = lambda vector: sum(int(c)*v for c,v in zip(vector,low))
    for alpha, vector in zip(certificate["degree_monomials"],certificate["degree_rewrite_vectors"]):
        assert G.reduce(monomial(alpha)-polynomial(vector))[1] == 0
    for j, matrix in enumerate(certificate["provisional_variable_multiplication_matrices"]):
        for i, v in enumerate(low):
            assert G.reduce(x[j]*v-polynomial([row[i] for row in matrix]))[1] == 0
    for vector in certificate["stable_relation_basis"]:
        assert G.reduce(polynomial(vector))[1] == 0
    assert result["secret"] == row["planted_secret"]


def test_higher_degree_recovers_below_quadratic_feature_sample_count_without_enumeration():
    row = run_controls()["actual_fixed_source_decoder_trials"][-1]
    result = row["result"]
    assert row["fewer_samples_than_degree_two_feature_dimension"]
    assert result["samples"] == 30 and row["degree_two_feature_dimension"] == 36
    assert result["low_monomial_dimension"] == 45
    assert result["leading_rank"] == result["leading_monomial_dimension"] == 112
    assert result["secret"] == row["planted_secret"]
    assert result["quotient_dimension"] == 1
    assert not result["secret_assignments_enumerated_by_decoder"]
    assert not result["asymptotic_source_probability_proved_by_these_trials"]
    quadratic = decode_ternary_binary_error(row["labels"], row["observations"], 2)
    assert quadratic["status"] == "LEADING_DEGREE_CERTIFICATE_FAILED"


def test_multiple_live_secrets_are_recorded_not_hidden_by_rerolling():
    rows = run_controls()["actual_fixed_source_decoder_trials"]
    for row in rows[1:3]:
        assert row["result"]["status"] == "MULTIPLE_BINARY_ERROR_SECRETS"
        actual = roots(row["labels"],row["observations"])
        assert len(actual) == row["result"]["quotient_dimension"] > 1


def test_monomials_use_bounded_degree_not_entire_field_assignment_grid():
    assert len(monomials(8,3)) == 112
    assert len(monomials(32,2)) == 528
    assert all(sum(alpha) == 2 and max(alpha) <= 2 for alpha in monomials(32,2))


def test_exact_single_sample_rank_with_nilpotent_leading_field_reduction():
    rng = random.Random(4309)
    for n,D in ((2,3),(4,3),(4,4),(8,3)):
        top = monomials(n,D)
        index = {alpha:i for i,alpha in enumerate(top)}
        for _ in range(4):
            a = tuple(rng.randrange(3) for _ in range(n))
            if not any(a):
                a = (1, *a[1:])
            span = Span(len(top))
            for mu in monomials(n,D-2):
                vector = np.zeros(len(top), dtype=np.int64)
                for alpha,c in _annihilator(a,0).items():
                    beta = tuple(x+y for x,y in zip(alpha,mu))
                    # Leading associated graded algebra has x_j^3=0, NOT x_j^3=x_j.
                    if sum(alpha) == 2 and max(beta) <= 2:
                        vector[index[beta]] = (vector[index[beta]]+c) % 3
                span.add(vector)
            assert len(span.rows) == single_sample_image_certificate(n,D)["nonzero_sample_image_rank"]


def test_dimension_counter_and_necessary_sample_count_are_not_sufficiency_claims():
    for n in range(7):
        for D in range(2*n+2):
            assert monomial_dimension(n,D) == len(monomials(n,D))
    certificate = single_sample_image_certificate(8,3)
    assert certificate["nonzero_sample_image_rank"] == 7
    assert certificate["necessary_nonzero_samples"] == 16
    assert not certificate["counting_condition_is_sufficient"]
    assert monomial_dimension(500,2) == 125250


@pytest.mark.parametrize("A,b,D", [((),(),2), (((True,),),(0,),2), (((3,),),(0,),2),
                                 (((1,),),(3,),2), (((1,),),(0,),1), (((1,),),(0,),4),
                                 (((1,2),),(0,),2)])
def test_malformed_field_inputs_and_wrong_degrees_rejected(A,b,D):
    with pytest.raises(ValueError):
        decode_ternary_binary_error(A,b,D)
