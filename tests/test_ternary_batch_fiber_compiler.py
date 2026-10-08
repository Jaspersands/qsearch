from fractions import Fraction
from itertools import combinations,product
import json
from pathlib import Path
import subprocess

import numpy as np
import pytest

from cyclotomic_fiber_receiver import inverse_frequency_coordinates,native_source
from ternary_cyclic_extractor import random_even_source
from ternary_batch_fiber_compiler import BatchFiberProgram,batch_ledger,cnf_value,gated_cnf,lex_rank_reduction,lucas,pointed_minor


@pytest.mark.parametrize("d",[1,2,3])
def test_carry_coefficient_identity_matches_every_ternary_integer_digit(d):
    for n in range(3**(d+1)):
        assert lucas(n,3**d)==n//3**d%3
    assert lucas(0,0)==1 and lucas(2,3)==0


@pytest.mark.parametrize("n,r,d,M,seed",[(1,3,2,3,99934),(2,4,3,3,99935)])
def test_native_ring_generating_circuit_and_reduced_polynomials_match_all_words(n,r,d,M,seed):
    p=BatchFiberProgram(random_even_source(n,2*r,M,seed),d)
    for coordinate in range(n):
        for digit in range(d):
            poly=p.reduced_polynomial(coordinate,digit)
            assert poly["degree"]<=2*3**digit
            for word in product(range(3),repeat=M):
                actual=p.low_frequency(word)[coordinate]//3**digit%3
                observed=sum(t["coefficient"]*np.prod([x**e for x,e in zip(word,t["powers"])]) for t in poly["terms"])%3
                assert int(observed)==actual==p.coefficient_digit(word,coordinate,digit)


def test_high_carry_contains_mixed_terms_not_a_diagonal_solver_instance():
    p=BatchFiberProgram(random_even_source(1,6,3,99934),2)
    poly=p.reduced_polynomial(0,1)
    assert poly["contains_mixed_variable_terms"]
    assert not poly["constant_degree_diagonal_solver_premise_certified"]


@pytest.mark.parametrize("n,r,d,M,seed",[(1,3,1,3,99940),(2,3,1,5,99941),(1,3,2,9,99931)])
def test_all_occupied_native_fibers_divisible_and_whole_basis_map_is_bijective(n,r,d,M,seed):
    p=BatchFiberProgram(random_even_source(n,2*r,M,seed),d);ref=p.reference()
    assert sum(map(len,ref.groups.values()))==3**M
    assert all(len(indices)%3==0 for indices in ref.groups.values())
    assert sorted(ref.packed_to_original)==list(range(3**M))
    for i in range(3**M):assert ref.inverse(ref.forward(i))==i
    for tag in range(3**M//3):
        words,_,rows,minor=ref.child(tag)
        assert len(set(p.low_frequency(w) for w in words))==1
        assert abs(minor["determinant"])==1
        assert all(0<=a<3**(r-d) for row in rows for a in row)


@pytest.mark.parametrize("M",[1,2,3])
def test_every_distinct_pointed_native_word_triple_has_unit_minor(M):
    for words in combinations(product(range(3),repeat=M),3):
        proof=pointed_minor(words);a,b=proof["columns"];R=proof["coefficient_rows"]
        assert R[0][a]*R[1][b]-R[0][b]*R[1][a]==proof["determinant"]
        assert abs(proof["determinant"])==1


def source_from_rows(rows,r):
    return native_source([[inverse_frequency_coordinates(a,c,2*r) for a,c in zip(pair[0],pair[1])] for pair in rows],2*r)


@pytest.mark.parametrize("r",[2,3])
def test_fixed_low_partition_is_invariant_and_conditional_child_pair_law_is_uniform(r):
    source=random_even_source(1,2*r,3,99945+r);p=BatchFiberProgram(source,1);ref=p.reference();H=3;q=3**r;qchild=q//H
    _,_,_,minor=ref.child(0);a,b=minor["columns"];pairs=[]
    for u,v in product(range(qchild),repeat=2):
        rows=[[list(row) for row in pair] for pair in p.low_rows]
        rows[a//2][a%2][0]+=H*u;rows[b//2][b%2][0]+=H*v
        changed=BatchFiberProgram(source_from_rows(rows,r),1).reference()
        assert changed.packed_to_original==ref.packed_to_original
        _,_,child,_=changed.child(0)
        pairs.append((child[0][0],child[1][0]))
    assert len(set(pairs))==qchild*qchild


def test_physical_all_tag_reference_charges_one_child_and_no_postselection():
    ref=BatchFiberProgram(random_even_source(2,4,5,99932),1).reference();report=ref.report()
    assert report["output_qutrits_per_input_batch"]==1
    assert not report["all_measurement_tags_are_simultaneously_available_child_samples"]
    assert report["physical_all_tag_phase_residual"]<3e-12
    assert report["reference_time_and_memory_exponential_in_original_qutrits"]
    assert not report["efficient_coherent_partition_implemented"]
    assert sum(Fraction(3,len(ref.words)) for _ in range(len(ref.words)//3))==1


def test_polynomial_sample_regime_is_explicit_not_polynomial_in_log_modulus():
    for r in (2,3,4,5):
        n=q=3**r;row=batch_ledger(n,r,r-1)
        assert row["minimum_original_qutrits_for_all_fibers_divisible_by_three"]==n*(q//3-1)+1
        assert row["output_qutrits_per_actual_input_batch"]==1
        assert not row["batch_supply_polynomial_in_log_q_claimed"]
        assert not row["known_integer_frequency_evaluation_is_a_fiber_inverse"]


def test_budget_and_threshold_domains_fail_without_partial_maps():
    with pytest.raises(ValueError):batch_ledger(True,3,1)
    with pytest.raises(ValueError):batch_ledger(1,3,3)
    with pytest.raises(ValueError):BatchFiberProgram(random_even_source(1,6,2,17),1).reference()
    with pytest.raises(ValueError):BatchFiberProgram(random_even_source(1,6,9,17),2).reference(max_words=729)
    with pytest.raises(ValueError):pointed_minor(((0,),(0,),(1,)))
    with pytest.raises(ValueError):BatchFiberProgram(random_even_source(1,6,3,17),1).coefficient_digit((0,0,0),0,1)


@pytest.mark.parametrize("variables,clauses",[(1,((1,),(-1,))),(2,((1,2),)),(1,((1,1,1),)),(2,((-1,2,-2),))])
def test_gated_cnf_has_exactly_one_auxiliary_extension_per_satisfying_original_or_gate(variables,clauses):
    V,C,known=gated_cnf(variables,clauses)
    assert cnf_value(known,C)
    for base in product(range(2),repeat=variables+1):
        extensions=[base+aux for aux in product(range(2),repeat=V-variables-1) if cnf_value(base+aux,C)]
        assert len(extensions)==int(bool(base[-1]) or cnf_value(base[:-1],clauses))


@pytest.mark.parametrize("variables,clauses,count",[(1,((1,),(-1,)),0),(2,((1,2),),3),(1,((1,1,1),),1)])
def test_native_lexical_compiler_reduction_counts_models_without_enumerating_padded_cube(variables,clauses,count):
    c=lex_rank_reduction(variables,clauses)
    assert c["real_fiber_count"]==count+2**variables
    assert c["recovered_original_model_count_mod_three"]==count%3
    assert c["hard_labels_are_worst_case_not_IID_average_case"]
    assert not c["nonlexicographic_or_source_state_only_compilers_ruled_out"]
    assert not c["actual_coherent_basis_compiler_supplied"]
    assert not c["whole_padded_source_words_enumerated"]
    assert c["original_qutrits"]==8*c["native_dimension"]+1
    rows=c["native_full_rows"]
    p=BatchFiberProgram(source_from_rows(rows,3),2)
    assert p.low_frequency(c["first_promised_native_word"])==p.low_frequency(c["second_promised_native_word"])==tuple(c["target_native_prefix"])


@pytest.mark.parametrize("variables,clauses",[(True,((1,),)),(1,((2,),)),(1,((0,),)),(1,((),)),(1,((1,1,1,1),)),(7,((1,),))])
def test_counting_reduction_rejects_invalid_formulas_or_excess_calibration(variables,clauses):
    with pytest.raises(ValueError):lex_rank_reduction(variables,clauses)


def test_strict_chevalley_warning_threshold_cannot_be_replaced_by_equality():
    p=BatchFiberProgram(source_from_rows([((1,),(1,)),((1,),(1,))],2),1)
    counts=[sum(p.low_frequency(w)==(S,) for w in product(range(3),repeat=2)) for S in range(3)]
    assert counts==[1,4,4]
    with pytest.raises(ValueError):p.reference()


def test_independent_checker_accepts_live_complete_reference():
    root=Path(__file__).resolve().parents[1]
    result=subprocess.run(["node",str(root/"research/certificates/ternary_batch_fiber_compiler_crosscheck.js")],capture_output=True,text=True)
    assert result.returncode==0,result.stderr
    assert json.loads(result.stdout)["completeNativePartitions"]==3


@pytest.mark.parametrize("mutation",["compiler","clones","threshold","count","digest","minor","child","high","degree","circuit","model-count","query-word","gate","counting-scope","counting-rows"])
def test_standalone_verifier_rejects_uncharged_compilers_bad_maps_and_wrong_ring_math(tmp_path,mutation):
    root=Path(__file__).resolve().parents[1]
    record=json.loads((root/"research/phase_workbench/ternary_batch_fiber_compiler.json").read_text());c=record["native_complete_partition_controls"][0]
    if mutation=="compiler":record["efficient_coherent_partition_implemented"]=True
    if mutation=="clones":c["output_qutrits_per_input_batch"]=c["complete_measurement_tag_count"]
    if mutation=="threshold":record["polynomial_supply_controls"][0]["minimum_original_qutrits_for_all_fibers_divisible_by_three"]=1
    if mutation=="count":c["occupied_fiber_counts"][0]["count"]+=1
    if mutation=="digest":c["complete_partition_sha256"]="0"*64
    if mutation=="minor":c["selected_tag_controls"][0]["pointed_unit_minor"]["determinant"]=0
    if mutation=="child":c["selected_tag_controls"][0]["child_frequency_rows"][0][0]=(c["selected_tag_controls"][0]["child_frequency_rows"][0][0]+1)%c["child_modulus"]
    if mutation=="high":c["partition_reads_high_frequency_lifts"]=True
    if mutation=="degree":record["true_ring_digit_polynomial_controls"][1]["degree"]=0
    if mutation=="circuit":record["complete_coefficient_circuit_identity_cases"]=1
    reduction=record["lexicographic_basis_compiler_counting_reduction_controls"][0]
    if mutation=="model-count":reduction["recovered_original_model_count_mod_three"]=1
    if mutation=="query-word":reduction["second_promised_native_word"][0]=2
    if mutation=="gate":reduction["gated_clauses"][0][0]=-reduction["gated_clauses"][0][0]
    if mutation=="counting-scope":reduction["nonlexicographic_or_source_state_only_compilers_ruled_out"]=True
    if mutation=="counting-rows":reduction["real_frequency_rows"][0][0][0]=1
    target=tmp_path/"mutant.json";target.write_text(json.dumps(record))
    result=subprocess.run(["node",str(root/"research/certificates/ternary_batch_fiber_compiler_crosscheck.js"),str(target)],capture_output=True,text=True)
    assert result.returncode!=0,result.stdout
