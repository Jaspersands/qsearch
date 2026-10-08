from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import subprocess

import pytest

from ternary_affine_line_extractor import best_menu_bound,coordinate_inverse,coordinate_map,direction,from_quadratic,good,line_control,line_ledger,menu_bound,quadratic_rows,rank
from ternary_cyclic_extractor import random_even_source


@pytest.mark.parametrize("n,M",[(1,2),(2,3)])
def test_rank_matches_complete_column_span_for_every_small_native_matrix(n,M):
    for entries in product(range(3),repeat=n*M):
        B=[list(entries[j*M:(j+1)*M]) for j in range(n)]
        image={tuple(sum(a*x for a,x in zip(row,w))%3 for row in B) for w in product(range(3),repeat=M)}
        assert len(image)==3**rank(B)


@pytest.mark.parametrize("r",[2,3,4])
def test_true_native_prefix_is_the_claimed_quadratic_not_an_arbitrary_oracle(r):
    source=random_even_source(3,2*r,4,88010+r);A,B=quadratic_rows(source)
    for word in product(range(3),repeat=4):
        actual=source.value(word)
        assert tuple(a%3 for a in actual)==tuple(sum(a*x+b*x*x for a,b,x in zip(arow,brow,word))%3 for arow,brow in zip(A,B))


def test_affine_basis_coordinates_are_reversible_for_every_direction_and_word():
    words=tuple(product(range(3),repeat=3))
    for v in words:
        if not any(v):continue
        for w in words:
            u,t=coordinate_map(w,v)
            assert coordinate_inverse(u,t,v)==w


@pytest.mark.parametrize("n,M",[(1,3),(2,4)])
def test_all_directions_and_all_original_words_obey_exact_coverage_and_rank_implication(n,M):
    source=random_even_source(n,6,M,88013+n);A,B=quadratic_rows(source);words=tuple(product(range(3),repeat=M))
    smallest=min((sum(bool(x) for x in w) for w in words if any(w) and all(sum(a*x for a,x in zip(row,w))%3==0 for row in B)),default=M+1)
    for v in words:
        if not any(v) or v!=direction(v,M)[0]:continue
        ledger=line_ledger(source,v);count=0
        for w in words:
            u,t=coordinate_map(w,v)
            values=[tuple(a%3 for a in source.value(coordinate_inverse(u,k,v))) for k in range(3)]
            assert good(u,ledger)==(len(set(values))==1)
            count+=good(u,ledger)
        assert Fraction(count,3**M)==Fraction(ledger["exact_raw_success_probability"])
        if ledger["predicate_consistent"]:assert ledger["support_rank"]>=smallest-1


def test_easy_low_curvature_positive_control_is_not_typical_random_source_evidence():
    source=from_quadratic([[1,2,0],[0,0,1]],[[0,0,0],[0,0,0]])
    c=line_control(source,(1,1,0))
    assert c["support_rank"]==0 and c["exact_raw_success_probability"]=="1"
    assert not c["quantum_speedup_proved"]
    assert not c["all_potential_tags_counted_as_outputs"]
    assert not c["efficient_direction_finder_supplied"]


def test_even_a_quadratic_zero_direction_can_have_no_valid_affine_lines():
    source=from_quadratic([[0,0],[1,0]],[[1,2],[0,0]])
    c=line_control(source,(1,1))
    assert c["curvature"]==(0,0) and c["support_rank"]==1
    assert not c["predicate_consistent"] and c["accepted_tag_count"]==0


def test_exact_population_union_bound_covers_every_small_label_adaptive_best_direction():
    n,M=2,2;total=Fraction(0)
    for entries in product(range(3),repeat=2*n*M):
        A=[list(entries[j*M:(j+1)*M]) for j in range(n)]
        B=[list(entries[(n+j)*M:(n+j+1)*M]) for j in range(n)]
        # Use the exact public-prefix law; no source states or inverse are fabricated.
        best=Fraction(0)
        for v in ((1,0),(0,1),(1,1),(1,2)):
            curvature=[sum(a*x*x for a,x in zip(row,v))%3 for row in B]
            if any(curvature):continue
            C=[[a*x%3 for a,x in zip(row,v)] for row in B]
            b=[sum(a*x for a,x in zip(row,v))%3 for row in A];R=rank(C)
            if rank([row+[offset] for row,offset in zip(C,b)])==R:best=max(best,Fraction(1,3**R))
        total+=best
    actual=total/3**(2*n*M)
    assert 0<actual<=Fraction(menu_bound(n,M,1,1)["mean_raw_menu_success_probability_upper"])<1


def test_population_gate_records_superpolynomial_not_fitted_success_for_polynomial_menus():
    values=[best_menu_bound(n,n*n,n*n) for n in (128,256,512,1024)]
    assert all(Fraction(a["mean_raw_menu_success_probability_upper"])>Fraction(b["mean_raw_menu_success_probability_upper"]) for a,b in zip(values,values[1:]))
    assert values[-1]["sparse_kernel_cutoff"]==94
    assert Fraction(1,10**40)<Fraction(values[-1]["mean_raw_menu_success_probability_upper"])<Fraction(1,10**38)
    assert all(c["directions_may_depend_on_all_low_labels"] and not c["coherent_direction_interference_or_nonlinear_partitions_excluded"] for c in values)


@pytest.mark.parametrize("operation",[lambda:direction((0,0),2),lambda:direction((True,1),2),lambda:coordinate_inverse((1,0),0,(1,0)),lambda:menu_bound(2,3,1,3),lambda:menu_bound(True,3,1,1),lambda:line_control(random_even_source(1,4,7,2),(1,0,0,0,0,0,0),729)])
def test_domain_failures_do_not_return_partial_source_certificates(operation):
    with pytest.raises(ValueError):operation()


def test_independent_checker_accepts_live_native_and_big_integer_certificates():
    root=Path(__file__).resolve().parents[1]
    result=subprocess.run(["node",str(root/"research/certificates/ternary_affine_line_extractor_crosscheck.js")],capture_output=True,text=True)
    assert result.returncode==0,result.stderr
    assert json.loads(result.stdout)["completeProjectiveDirections"]==121


@pytest.mark.parametrize("mutation",["phase","rank","coverage","curvature","bijection","cloning","sparse-weight","menu-census","bound","exception","scope"])
def test_independent_checker_rejects_false_coverage_bad_native_math_and_overscoped_gates(tmp_path,mutation):
    root=Path(__file__).resolve().parents[1];record=json.loads((root/"research/phase_workbench/ternary_affine_line_extractor.json").read_text());c=record["native_full_cube_controls"][0]
    if mutation=="phase":c["accepted_tags"][0]["child_rows"][0][0]=(c["accepted_tags"][0]["child_rows"][0][0]+1)%9
    if mutation=="rank":c["support_rank"]=0
    if mutation=="coverage":c["exact_raw_success_probability"]="1"
    if mutation=="curvature":c["curvature"][0]=1
    if mutation=="bijection":c["coordinate_map_sha256"]="0"*64
    if mutation=="cloning":c["logical_output_qutrits_per_successful_batch"]=c["accepted_tag_count"]
    if mutation=="sparse-weight":record["complete_low_label_direction_census"]["smallest_nonzero_kernel_weight"]=0
    if mutation=="menu-census":record["complete_low_label_direction_census"]["menu"].pop()
    if mutation=="bound":record["polynomial_menu_population_bounds"][-1]["mean_raw_menu_success_probability_upper"]="0"
    if mutation=="exception":record["polynomial_menu_population_bounds"][-1]["exceptional_label_probability_upper"]="0"
    if mutation=="scope":record["nonlinear_or_coherent_direction_compilers_ruled_out"]=True
    target=tmp_path/"mutant.json";target.write_text(json.dumps(record))
    result=subprocess.run(["node",str(root/"research/certificates/ternary_affine_line_extractor_crosscheck.js"),str(target)],capture_output=True,text=True)
    assert result.returncode!=0,result.stdout
