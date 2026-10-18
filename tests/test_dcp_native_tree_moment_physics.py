"""Exact native moments, Z4 torsion and correlated-overflow falsifiers."""
from copy import deepcopy
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import subprocess
import sys

import pytest

from theorems.dcp_adaptive_direction_rank_gate import decode_dyadic
from theorems.dcp_native_tree_moment_audit import (
    CONTRACT,CONTRACT_ID,REPORT,build_report,dimensions,filtered_relation,moments,
    overflow_contract,pattern_census,pattern_constraints,unit_rank_mod4,
)
from theorems.dcp_vector_short_mask_join import resource

ROOT=Path(__file__).resolve().parents[1]
CHECKER=ROOT/"research/certificates/dcp_native_tree_moment_audit_crosscheck.js"


@pytest.fixture(scope="module")
def report():
    return build_report()


def test_every_small_Z4_matrix_unit_probability_and_nonunit_residual_fail_closed():
    certified=unknown=0
    for flat in product(range(4),repeat=4):
        A=(flat[:2],flat[2:])
        probability=Fraction(sum(all(sum(a*x for a,x in zip(row,z))%4==0 for row in A)
                                 for z in product(range(4),repeat=2)),16)
        try:
            r=unit_rank_mod4(A)
        except ValueError as error:
            assert "even residual" in str(error)
            unknown+=1
        else:
            assert probability==Fraction(1,4**r)
            certified+=1
    assert certified+unknown==256 and certified>0 and unknown>0
    for A in (((2,),),((1,0),(0,2)),((2,0),(0,2))):
        with pytest.raises(ValueError,match="even residual"):
            unit_rank_mod4(A)


def test_actual_Z4_constraint_probabilities_not_a_field_rank_approximation():
    for shared in range(4):
        for A in pattern_constraints(1,shared):
            count=sum(all(sum(a*x for a,x in zip(row,z))%4==0 for row in A)
                      for z in product(range(4),repeat=4))
            assert Fraction(count,256)==Fraction(1,4**unit_rank_mod4(A))
    # One even equation has probability1/2, not1 from its zero F2 rank.
    assert Fraction(sum(2*x%4==0 for x in range(4)),4)==Fraction(1,2)


def test_all_shared_support_patterns_recover_exact_source_moments(report):
    for C in report["complete_pattern_rank_censuses"]:
        a,b=C["depth"],C["chunk_components"]
        k,L,_=dimensions(a,b)
        assert len(C["patterns"])==1 << k
        assert sum(int(row["ordered_tuple_pair_count_hex"],16) for row in C["patterns"])==L**(2*k)
        total=Fraction(0)
        for row in C["patterns"]:
            s=int(row["shared_leaf_mask_hex"],16)
            ranks=[unit_rank_mod4(A) for A in pattern_constraints(a,s)]
            assert row["unit_constraint_ranks_by_chunk"]==ranks
            probability=Fraction(1,L**sum(ranks))
            count=L**k*(L-1)**(k-s.bit_count())
            assert decode_dyadic(row["joint_survival_probability"])==probability
            assert decode_dyadic(row["second_moment_term"])==count*probability
            total+=count*probability
        assert total==decode_dyadic(C["observed_second_moment"])
        assert total==decode_dyadic(moments(a,b)["second_degree_moment"])
        assert decode_dyadic(C["patterns"][-1]["second_moment_term"])==1


def test_two_list_boundary_matches_existing_vector_baseline_exactly():
    for b in range(1,9):
        L=4**b
        M=moments(1,b)
        C,_=resource(2*b,8*b)
        O=overflow_contract(1,b)
        assert decode_dyadic(M["second_degree_moment"])==2-Fraction(1,L*L)==C["degree_second_moment"]
        assert decode_dyadic(O["overflow_marked_mass_loss_upper_surrogate"])==0
        assert decode_dyadic(O["coarse_mass_lower_IF_clean_exact_receiver_contract"])==C["source_mass_lower"]


def test_moment_growth_is_not_hidden_outside_the_constant_size_regime():
    assert decode_dyadic(moments(2,1)["second_degree_moment"])==Fraction(601,256)
    assert moments(2,1)["M_at_most_3_sufficient_size_condition"] is False
    assert moments(2,1)["M_actually_at_most_3"] is True
    assert moments(3,1)["M_actually_at_most_3"] is False
    for a in range(1,7):
        for b in (1,2,4,8):
            R=moments(a,b)
            k,L,_=dimensions(a,b)
            f=decode_dyadic(R["internal_weight_moment_recurrence"][-1])
            assert f<=(1+Fraction(1,L))**(k-1)
            if L>=2*(k-1):
                assert f<=2 and decode_dyadic(R["second_degree_moment"])<=3


def test_all_overflow_frontiers_charge_two_endpoints_without_independence(report):
    for C in report["conditional_overflow_frontiers"]:
        M=decode_dyadic(C["moment"]["second_degree_moment"])
        theta=decode_dyadic(C["affine_mark_probability"])
        cap=int(C["intermediate_list_capacity_hex"],16)
        k=C["moment"]["leaf_count"]
        L=int(C["moment"]["leaf_list_length_hex"],16)
        delta=Fraction((k-2)*L,cap+1)
        assert delta==Fraction(C["overflow_probability_upper_bound_exact_rational"])
        assert M*delta==Fraction(C["M_times_overflow_bound_exact_rational"])<Fraction(1,256)
        assert theta<=1/(4*(M-1))<2*theta
        original=theta**2-2*theta**3*(M-1)
        loss=decode_dyadic(C["overflow_marked_mass_loss_upper_surrogate"])
        lower=decode_dyadic(C["coarse_mass_lower_IF_clean_exact_receiver_contract"])
        assert lower==original-loss>=3*theta**2/8
        assert C["overflow_independent_of_degree_assumed"] is False
        assert C["overflow_detection_inspects_affine_mark_seed"] is False
        assert C["native_mean_is_before_label_or_syndrome_postselection"] is True
        assert C["clean_bounded_list_receiver_implemented"] is False
        if M<=3:
            assert theta>=Fraction(1,8) and lower>=Fraction(3,512)


def test_overflow_can_correlate_strongly_with_degree_and_cannot_use_mean_times_delta():
    # Abstract proof countercontrol, not a candidate oracle problem: a16-leaf
    # star plus15 isolates gives32 vertices and mean degree exactly1.
    adjacency=[set() for _ in range(32)]
    for leaf in range(1,17):
        adjacency[0].add(leaf)
        adjacency[leaf].add(0)
    D=[len(v) for v in adjacency]
    mu=Fraction(sum(D),32)
    M=Fraction(sum(d*d for d in D),32)
    delta=Fraction(1,32)
    incident=Fraction(D[0],32)
    assert mu==1 and incident>mu*delta
    assert incident**2<=M*delta
    endpoint_total=Fraction(sum((x==0 or y==0) for x,neighbors in enumerate(adjacency) for y in neighbors),32)
    assert endpoint_total==2*incident and endpoint_total>2*mu*delta


def test_tree_filters_are_partner_invariant_but_not_equivalent_to_only_the_final_sum():
    supports=(1,16,256,4096)
    A=[[0]*16 for _ in range(3)]
    for i,value in zip((0,4,8,12),(1,0,3,0)):
        A[0][i]=value
    assert sum(A[0][i] for i in (0,4,8,12))%4==0
    assert filtered_relation(A,0,supports,2,1) is False
    for i,value in zip((0,4,8,12),(1,3,2,2)):
        A[0][i]=value
    assert filtered_relation(A,0,supports,2,1) is True
    assert filtered_relation(A,sum(supports),supports,2,1) is True
    A[1][0]=1
    assert filtered_relation(A,0,supports,2,1) is False


def test_high_degree_coarse_zero_control_does_not_get_pointwise_mean_one_claim(report):
    C=report["native_edge_invariance_controls"][1]
    assert C["accepted_filtered_edges"]==C["tuple_tests"]==1536
    assert C["counts_are_native_probability_estimates"] is False
    assert C["accepted_filtered_edges"]//len(C["original_assignments"])==256


def test_noise_is_physical_width_and_higher_zero_filter_is_explicit(report):
    for C in report["conditional_overflow_frontiers"]:
        n=C["moment"]["secret_vector_components"]
        v=decode_dyadic(C["dyadic_original_visibility_lower_promise"])
        assert v<=1-Fraction(1,n)
        assert Fraction(C["ideal_inverse_dimension_visibility_exact_rational"])==1-Fraction(1,n)
        factors=C["conditional_mean_useful_visibility_lower_factors_IF_receiver_contract"]
        p=decode_dyadic(factors[0])
        vis=decode_dyadic(factors[1])
        assert vis==v**C["default_full_physical_mask_width"]
        assert factors[2]=={"one_minus_two_to_negative":n*n}
        assert C["input_phase_bits_for_higher_label_factor"]==n+2
        assert decode_dyadic(C["conditional_mean_unfiltered_visibility_lower_IF_receiver_contract"])==p*vis
        assert C["classical_Wagner_expected_kL_bound_used_as_quantum_gate_count"] is False
        cap=int(C["intermediate_list_capacity_hex"],16)
        assert int(C["naive_nonroot_candidate_cell_upper_bound_hex"],16)==C["nonroot_internal_nodes"]*cap*cap


def test_work_caps_and_missing_leaf_lineage_return_unknown_not_a_negative():
    with pytest.raises(ValueError,match="UNKNOWN"):
        pattern_census(4,1)
    with pytest.raises(ValueError,match="UNKNOWN"):
        overflow_contract(8,64)
    A=((0,)*16,)*3
    with pytest.raises(ValueError,match="disjoint"):
        filtered_relation(A,0,(1,1,256,4096),2,1)
    for args in ((True,1),(0,1),(2,0),(9,1)):
        with pytest.raises(ValueError):
            moments(*args)


def js_check(R,tmp_path):
    target=tmp_path/"certificate.json"
    target.write_text(json.dumps(R))
    return subprocess.run(["node",str(CHECKER),str(target)],capture_output=True,text=True)


def test_live_provenance_and_independent_native_graph_rank_resource_replay(report,tmp_path):
    assert json.loads(REPORT.read_text())==report
    assert json.loads(CONTRACT.read_text())["contract_id"]==CONTRACT_ID
    result=js_check(report,tmp_path)
    assert result.returncode==0,result.stderr
    assert json.loads(result.stdout)["complete_equality_patterns"]==276


@pytest.mark.parametrize("mutation",["rank","pattern","moment","overflow","mark","cap","noise","source","edge","seed","receiver","scope"])
def test_forged_moments_overflow_noise_and_receiver_claims_are_rejected(report,tmp_path,mutation):
    R=deepcopy(report)
    C=R["conditional_overflow_frontiers"][1]
    if mutation=="rank":
        R["complete_pattern_rank_censuses"][1]["patterns"][0]["unit_constraint_ranks_by_chunk"][0]-=1
    elif mutation=="pattern":
        R["complete_pattern_rank_censuses"][0]["patterns"].pop()
    elif mutation=="moment":
        C["moment"]["second_degree_moment"]["numerator_hex"]="0x1"
    elif mutation=="overflow":
        C["overflow_probability_upper_bound_exact_rational"]="0"
    elif mutation=="mark":
        C["hash_bits"]-=1
    elif mutation=="cap":
        C["intermediate_list_capacity_hex"]="0x1"
    elif mutation=="noise":
        C["default_full_physical_mask_width"]-=1
    elif mutation=="source":
        C["conditional_mean_useful_visibility_lower_factors_IF_receiver_contract"][2]["one_minus_two_to_negative"]-=1
    elif mutation=="edge":
        R["native_edge_invariance_controls"][1]["accepted_filtered_edges"]-=1
    elif mutation=="seed":
        C["overflow_detection_inspects_affine_mark_seed"]=True
    elif mutation=="receiver":
        C["clean_bounded_list_receiver_implemented"]=True
    else:
        R["scope"]["silent_truncation_inherits_this_contract"]=True
    assert js_check(R,tmp_path).returncode!=0


def test_read_only_CLI_does_not_replace_a_graph_contract_by_a_receiver():
    before=REPORT.read_bytes()
    result=subprocess.run([sys.executable,"qsearch.py","dcp-native-tree-moment-audit","--no-write"],
                          cwd=ROOT,capture_output=True,text=True)
    assert result.returncode==0,result.stderr
    assert json.loads(result.stdout)["coherent_receiver_implemented"] is False
    assert REPORT.read_bytes()==before
