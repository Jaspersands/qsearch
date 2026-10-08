from copy import deepcopy
from itertools import product
from math import comb

from flint import fmpq
import pytest

from ternary_proper_marginal_gap import (balanced_word_probability, word_probability, build_case,
    verify_case, verify_psd_template, parity_certificate, sign_matrix)
from ternary_moment_psd import verify_ldl


@pytest.mark.parametrize("M",[5,7,15,31])
def test_odd_gap_has_all_proper_genuine_projective_laws_and_exact_psd(M):
    record=build_case(M);checked=verify_case(record)
    assert checked["valid"] and checked["global_native_nonrealizability_proved"]
    assert record["maximum_marginal_size"]==M-1 and len(record["marginal_rows"])==M
    assert record["cost"]["native_words_enumerated"]==record["cost"]["LP_calls"]==0
    cert=record["global_record"]["parity_certificate"]
    assert fmpq(cert["exact_pair_moment_value"])==fmpq(-1,8)
    ldl=record["exact_sign_LDL_control"]["ldl"]
    assert verify_ldl(sign_matrix(M),ldl["lower"],ldl["diagonal"])["valid"]


@pytest.mark.parametrize("M",[4,6,16,32])
def test_even_balanced_controls_are_real_global_laws_not_fake_odd_gaps(M):
    record=build_case(M);checked=verify_case(record)
    assert checked["valid"] and not checked["global_native_nonrealizability_proved"]
    assert record["maximum_marginal_size"]==M
    full=record["marginal_rows"][-1]["classes"]
    assert all(fmpq(c["Hamming_class_mass"])==int(c["h"]==M//2) for c in full)
    assert not record["global_record"]["odd_parity_inequality_applicable"]
    with pytest.raises(ValueError):parity_certificate(M)


def test_per_word_and_class_probabilities_are_distinct_and_honest_native_counts_match():
    record=build_case(5);row=record["marginal_rows"][3]["classes"]
    assert [c["particular_word_probability"] for c in row]==["1/32","5/32","5/32","1/32"]
    assert [c["Hamming_class_mass"] for c in row]==["1/32","15/32","15/32","1/32"]
    even=build_case(6);counts={h:sum(sum(w)==h for w in product((0,1),repeat=3)) for h in range(4)}
    assert all(int(c["word_multiplicity"])==counts[c["h"]] for c in even["marginal_rows"][3]["classes"])


def test_marginal_formula_matches_explicit_small_balanced_word_distribution():
    N=6;words=[w for w in product((0,1),repeat=N) if sum(w)==N//2]
    for k in range(N+1):
        for prefix in product((0,1),repeat=k):
            observed=fmpq(sum(w[:k]==prefix for w in words),len(words))
            assert observed==balanced_word_probability(N,k,sum(prefix))


def test_native_parity_cut_checks_every_actual_five_event_word():
    cert=parity_certificate(5);constant=int(cert["integer_constant"]);single=int(cert["single_indicator_coefficient"])
    for word in product((0,1),repeat=5):
        h=sum(word);value=constant+single*h+comb(h,2)
        assert value>=0 and 8*value==(2*h-5)**2-1
        assert value==int(cert["all_native_hamming_weight_values"][h])


def test_wrong_word_mass_projection_omission_or_noncanonical_exact_values_fail():
    original=build_case(5)
    for mutate in (
        lambda r:r["marginal_rows"][2]["classes"][1].update(particular_word_probability="1/3"),
        lambda r:r["marginal_rows"][3]["classes"][1].update(Hamming_class_mass="5/32"),
        lambda r:r["marginal_rows"][0]["classes"][0].update(particular_word_probability="2/2"),
        lambda r:r["marginal_rows"].pop(),
        lambda r:r["marginal_rows"][2]["classes"].pop(),
        lambda r:r["marginal_rows"][0].update(k=False),
        lambda r:r["components"][0].update(mixture_weight="1/2"),
    ):
        bad=deepcopy(original);mutate(bad)
        with pytest.raises(ValueError):verify_case(bad)


def test_false_psd_flags_cannot_replace_the_full_exact_factor():
    record=build_case(5);record["exact_sign_LDL_control"]["ldl"]["diagonal"][0]="-1"
    record["exact_sign_LDL_control"]["ldl"]["valid"]=True
    with pytest.raises(ValueError,match="full factor"):verify_case(record)
    record=build_case(5);record["PSD_sum_of_squares_template"]["edge_square_weight"]="-1/4"
    with pytest.raises(ValueError):verify_case(record)


def test_false_odd_gap_cannot_be_transplanted_to_even_case_or_quantum_claim():
    odd=build_case(5);even=build_case(6)
    even["global_record"]=odd["global_record"]
    with pytest.raises(ValueError,match="even balanced"):verify_case(even)
    for key in ("is_algorithm_candidate","is_source_instance","quantum_speedup_proved","population_obstruction_proved"):
        bad=build_case(5);bad[key]=True
        with pytest.raises(ValueError):verify_case(bad)


def test_parity_and_ledger_tampering_fail_even_when_metadata_claims_valid():
    record=build_case(5);record["global_record"]["parity_certificate"]["exact_pair_moment_value"]="0"
    with pytest.raises(ValueError):verify_case(record)
    record=build_case(5);record["cost"]["maximum_probability_denominator_bits"]+=1
    with pytest.raises(ValueError,match="ledger"):verify_case(record)
    record=build_case(5);record["cost"]["LP_calls"]=False
    with pytest.raises(ValueError):verify_case(record)


def test_whole_preflight_guards_return_unknown_without_partial_proofs():
    for kw in ({"max_class_records":1},{"max_matrix_cells":1}):
        record=build_case(63,**kw)
        assert record["status"]=="PROPER_MARGINAL_CONTROL_PREFLIGHT_UNKNOWN"
        assert "marginal_rows" not in record and verify_case(record)["unknown_not_proof"]
        bad=deepcopy(record);bad["global_nonrealizability_proved"]=True
        with pytest.raises(ValueError):verify_case(bad)
    with pytest.raises(ValueError):build_case(5,max_class_records=0)


@pytest.mark.parametrize("M",[True,3,-1,5.0])
def test_invalid_native_sizes_fail_closed(M):
    with pytest.raises(ValueError):build_case(M)


def test_balanced_population_and_probability_indices_are_strict():
    for args in ((5,2,1),(6,7,1),(6,2,3),(6,True,1),(6,2,False)):
        with pytest.raises(ValueError):balanced_word_probability(*args)
    with pytest.raises(ValueError):word_probability(5,5,2)
