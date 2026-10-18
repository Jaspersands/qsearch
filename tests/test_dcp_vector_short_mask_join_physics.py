"""Vector group, native law, physical phase and cost falsifiers. Preserve this suite."""
from collections import Counter
from copy import deepcopy
from fractions import Fraction
from itertools import combinations, product
import json
import math
from pathlib import Path
from random import Random
import subprocess
import sys

import numpy as np
import pytest

from dcp_affine_marked_pairing import affine_hash
from dcp_balanced_pairing import BalancedPairingProgram, evaluate_record_join
from theorems.dcp_adaptive_direction_rank_gate import decode_dyadic
from theorems.dcp_nonlinear_fiber_pairing import compiler_certificate, phase_value, program_value, wire_map
from theorems.dcp_vector_short_mask_join import (
    CONTRACT, CONTRACT_ID, REPORT, build_report, evaluate_xor, exact_source_census,
    frontier, make_program, packed_group_value, propose, resource, validate_program,
)

ROOT=Path(__file__).resolve().parents[1]
CHECKER=ROOT/"research/certificates/dcp_vector_short_mask_join_crosscheck.js"


@pytest.fixture(scope="module")
def report():
    return build_report()


def test_packed_key_addition_has_both_false_negatives_and_false_positives():
    a,b=(1,1),(3,3)
    assert tuple((x+y)%4 for x,y in zip(a,b))==(0,0)
    assert (packed_group_value(a)+packed_group_value(b))%16==4
    A=((1,3),(1,3))
    P=make_program(A,0,1,1)
    assert propose(P,0)==3
    a,b=(3,0),(1,3)
    assert (packed_group_value(a)+packed_group_value(b))%16==0
    assert tuple((x+y)%4 for x,y in zip(a,b))==(0,3)
    assert propose(make_program(((3,1),(0,3)),0,1,1),0) is None


def test_all_distinct_signed_support_pairs_have_uniform_vector_joint_sums():
    for n,m in ((1,3),(2,2)):
        for x in range(1 << m):
            for u,v in combinations(range(1,1 << m),2):
                for second_origin in (x,x^u):
                    H=Counter()
                    for flat in product(range(4),repeat=n*m):
                        A=tuple(flat[l*m:(l+1)*m] for l in range(n))
                        def signed(mask,origin):
                            return tuple(sum(a*(1-2*(origin >> i & 1)) for i,a in enumerate(row) if mask >> i & 1)%4 for row in A)
                        H[signed(u,x),signed(v,second_origin)]+=1
                    assert len(H)==4**(2*n)
                    assert set(H.values())=={4**(n*m-2*n)}


def test_all_affine_seeds_not_only_full_rank_seeds_give_three_wise_vertex_marking():
    m,g=3,2
    for vertices in combinations(range(1 << m),3):
        H=Counter()
        for seed in range(1 << (g*(m+1))):
            rows=tuple((seed >> (j*m))&((1 << m)-1) for j in range(g))
            c=seed >> (g*m)
            H[tuple(affine_hash(x,rows,c) for x in vertices)]+=1
        assert len(H)==1 << (3*g)
        assert len(set(H.values()))==1
    P=make_program(((1,1,1,1),),0)
    assert P["hash_rows_hex"]==["0x0","0x0"]
    assert P["hash_offset_hex"]=="0x0"


def test_degree_one_at_one_endpoint_is_not_reciprocal_or_a_useful_accepted_pair():
    A=((5,1,1,1),)
    P=make_program(A,2)
    assert propose(P,9)==12 and propose(P,12) is None
    assert (phase_value(A,12,8)[0]-phase_value(A,9,8)[0])%8==4
    certificate=compiler_certificate(A,3,2,P)
    assert 9 not in certificate["accepted_assignments"]
    assert 12 not in certificate["accepted_assignments"]


def test_default_weights_counts_and_noise_parameters_are_vector_not_scalar_bits(report):
    for n in (2,3,8,16,64,128):
        C,R=resource(n,4*n)
        assert C["each_list_length"]==1 << n
        assert C["supports"]==4**n
        assert R["hash_bits"]==2 and R["physical_mask_width"]<=2*n
        assert decode_dyadic(R["native_mean_coarse_coverage_lower_bound"])==Fraction(1,32)+Fraction(1,32*4**n)
        assert "joint_fault_signal_lower" not in R and "independent_fault_signal_lower" not in R
        assert R["group_cardinality_binary_exponent"]==2*n
        assert int(R["counts_hex"]["persistent_workspace_bits"],16)>2*(1 << n)
    for F in report["native_short_mask_frontiers"]:
        n=F["resource_ledger"]["secret_vector_components"]
        assert decode_dyadic(F["original_visibility"])==1-Fraction(1,n)
        assert decode_dyadic(F["native_mean_useful_visibility_lower_bound"])>=Fraction(1,1536)
        assert F["exponential_recursive_supply_removed"] is False


def test_elementary_constant_noise_lower_bound_is_valid_beyond_the_saved_grid():
    for n in range(2,129):
        C,_=resource(n,4*n)
        v=1-Fraction(1,n)
        assert v**(n-1)>Fraction(1,3)
        assert v**(2*n)>Fraction(1,36)
        assert C["source_mass_lower"]*Fraction(3,4)*v**C["radius"]>Fraction(1,1536)


def test_join_padding_reverse_scan_record_cleanup_and_arbitrary_xor_target_are_paid():
    A=((1,2,3,0,1,2,3,0),(2,3,1,0,3,2,0,1))
    P=make_program(A,71,1,3)
    _,C,_,_=validate_program(P)
    assert C["padded_records"]==8>6
    for x in range(256):
        row=evaluate_xor(P,x,output=217)
        clean=evaluate_xor(P,x)
        assert row["output"]==217^clean["output"]
        assert row["workspace_clean"] is True
        assert row["comparators"]==C["one_xor_comparators"]
        assert row["record_evaluations"]==12
        assert row["scan_steps"]==16
        assert row["persistent_workspace_bits"]==C["persistent_workspace_bits"]


def test_vector_join_uses_lexicographic_supports_not_numeric_bitmask_order():
    A=((0,1,2,3,2,0,1,3),(1,3,0,2,1,2,3,0))
    P=make_program(A,17,2,3)
    left=[sum(1 << i for i in c) for c in list(combinations(range(4),2))[:3]]
    assert left==[3,5,9]
    _,_,H,c=validate_program(P)
    for x in range(256):
        neighbors=[x^u^(v<<4) for u in left for v in left
                   if affine_hash(x,H,c)==0 and affine_hash(x^u^(v<<4),H,c)==0
                   and phase_value(A,x,4)==phase_value(A,x^u^(v<<4),4)]
        assert propose(P,x)==(neighbors[0] if len(neighbors)==1 else None)


def test_coarse_only_program_and_full_uniform_higher_label_law():
    B=((1,3),(1,3))
    P=make_program(B,0,1,1)
    hist=Counter()
    mass=Fraction(0)
    for z in product(range(2),repeat=4):
        A=tuple(tuple(a+4*z[l*2+i] for i,a in enumerate(row)) for l,row in enumerate(B))
        assert make_program(A,0,1,1)==P
        hist[tuple(sum(a for a in row)//4%2 for row in A)]+=1
        mass+=decode_dyadic(compiler_certificate(A,3,2,P)["useful_descent_probability"])/16
    assert hist=={(0,0):4,(0,1):4,(1,0):4,(1,1):4}
    assert mass==Fraction(3,8)


def test_actual_unknown_vector_phase_and_original_product_noise_not_search_depth():
    A=((1,3),(1,3))
    P=make_program(A,0,1,1)
    K=compiler_certificate(A,3,2,P)
    assert len(K["pairs"])==1
    pair=K["pairs"][0]
    x,y=pair["first"],pair["second"]
    label=tuple(int(a,16) for a in pair["descended_label_hex"])
    for secret in product(range(8),repeat=2):
        def amplitude(z):
            phase=sum(s*a for s,a in zip(secret,phase_value(A,z,8)))%8
            return np.exp(2j*math.pi*phase/8)/2
        raw=np.outer([amplitude(x),amplitude(y)],np.conj([amplitude(x),amplitude(y)]))
        v=Fraction(3,4)**2
        raw[0,1]*=float(v)
        raw[1,0]*=float(v)
        mass=np.trace(raw).real
        angle=math.pi*(sum(s*a for s,a in zip(secret,label))%2)
        target=np.array([[1,float(v)*np.exp(-1j*angle)],[float(v)*np.exp(1j*angle),1]])/2
        assert mass==pytest.approx(1/2)
        assert np.allclose(raw/mass,target,atol=2e-14)


def test_actual_six_call_instrument_all_recorded_pairs_and_signed_higher_labels(report):
    for F in report["finite_controls"]:
        K,P=F["compiler"],F["program"]
        A=tuple(tuple(int(a,16) for a in row) for row in K["public_labels_hex"])
        m,t=P["width"],K["phase_bits"]
        q,R=1 << t,1 << (t-2)
        for pair in K["pairs"]:
            x,y=pair["first"],pair["second"]
            for endpoint,orientation in ((x,0),(y,1)):
                accepted=wire_map(endpoint,P,A,t,2,"accept")
                output=wire_map(accepted,P,A,t,2,"order")
                assert output==x | (1 << (3*m+2)) | (orientation << (3*m+3))
            label=[int(a,16) for a in pair["descended_label_hex"]]
            for secret in (tuple(1+l for l in range(len(A))),tuple(3-l for l in range(len(A)))):
                phases=[sum(s*a for s,a in zip(secret,phase_value(A,z,q)))%q for z in (x,y)]
                amplitudes=np.exp(2j*math.pi*np.array(phases)/q)/math.sqrt(1 << m)
                density=np.outer(amplitudes,np.conj(amplitudes))
                v=float(Fraction(3,4)**((x^y).bit_count()))
                density[0,1]*=v
                density[1,0]*=v
                mass=np.trace(density).real
                angle=2*math.pi*(sum(s*a for s,a in zip(secret,label))%R)/R
                expected=np.array([[1,v*np.exp(-1j*angle)],[v*np.exp(1j*angle),1]])/2
                assert mass==pytest.approx(2/(1 << m))
                assert np.allclose(density/mass,expected,atol=2e-14)


def test_complete_native_censuses_verify_counts_moments_and_coverage(report):
    for C in report["complete_source_censuses"]:
        R=C["resource_ledger"]
        n,m=C["components"],C["width"]
        population=4**(n*m)*(1 << m)
        assert Fraction(C["sum_unmarked_degrees"],population)==decode_dyadic(R["mean_degree"])
        assert Fraction(C["sum_squared_unmarked_degrees"],population)==decode_dyadic(R["degree_second_moment"])
        p=Fraction(C["mutual_unique_marked_assignments"],C["all_label_seed_assignments_enumerated"])
        assert p==decode_dyadic(C["observed_coarse_acceptance_probability"])
        assert p>=decode_dyadic(R["native_mean_coarse_coverage_lower_bound"])
    assert report["complete_source_censuses"][0]["all_label_seed_assignments_enumerated"]==4194304


def test_shared_join_validates_inputs_before_any_records_or_marks_are_evaluated():
    def should_not_run():
        raise AssertionError("invalid x must be rejected before evaluating input-dependent records")
    with pytest.raises(ValueError):
        evaluate_record_join(4,0.5,0,should_not_run,should_not_run,{},(0,0,0))
    P=BalancedPairingProgram((1,2,3,0),2,1,(),0)
    with pytest.raises(ValueError):
        P.evaluate_xor(0.5)


@pytest.mark.parametrize("mutation",["free","space","seed","group","bits","size","noise_model"])
def test_programs_cannot_erase_costs_or_change_the_group_and_source_model(mutation):
    P=make_program(((1,3),(1,3)),0,1,1)
    if mutation=="free":
        P["table_lookup_is_a_free_coherent_oracle"]=True
    elif mutation=="space":
        P["resource_ledger"]["counts_hex"]["persistent_workspace_bits"]="0x0"
    elif mutation=="seed":
        P["seed_has_been_conditioned_on_success"]=True
    elif mutation=="group":
        P["resource_ledger"]["group"]="cyclic Z16"
    elif mutation=="bits":
        P["components"]=True
    elif mutation=="size":
        P["coarse_labels"][0][0]=5
    else:
        P["resource_ledger"]["independent_fault_signal_lower"]=1
    with pytest.raises(ValueError):
        evaluate_xor(P,0)


def test_exponential_work_caps_do_not_allocate_a_large_list_or_report_a_negative(monkeypatch):
    import theorems.dcp_vector_short_mask_join as module
    P=make_program(tuple((1,)*128 for _ in range(32)),0)
    def no_enumeration(*args):
        raise AssertionError("exponential list must not be built before the cap")
    monkeypatch.setattr(module,"block_masks",no_enumeration)
    with pytest.raises(ValueError,match="UNKNOWN"):
        propose(P,0)
    with pytest.raises(ValueError,match="UNKNOWN"):
        exact_source_census(2,8,1,4)


def js_check(R,tmp_path):
    target=tmp_path/"certificate.json"
    target.write_text(json.dumps(R))
    return subprocess.run(["node",str(CHECKER),str(target)],capture_output=True,text=True)


def test_live_provenance_and_independent_vector_census_replay(report,tmp_path):
    assert json.loads(REPORT.read_text())==report
    assert json.loads(CONTRACT.read_text())["contract_id"]==CONTRACT_ID
    checked=js_check(report,tmp_path)
    assert checked.returncode==0,checked.stderr
    assert json.loads(checked.stdout)["complete_source_censuses"]==2


@pytest.mark.parametrize("mutation",["proposal","zero","mask","cost","coverage","census","signal","seed","scope","admit"])
def test_independent_checker_rejects_forged_research_claims(report,tmp_path,mutation):
    R=deepcopy(report)
    F=R["finite_controls"][0]
    if mutation=="proposal":
        F["diagnostic_proposal_table_NOT_free_oracle"][0]=None
    elif mutation=="zero":
        F["compiler"]["pairs"][0]["descended_label_hex"]=["0x0","0x0"]
    elif mutation=="mask":
        F["compiler"]["pairs"][0]["physical_Hamming_width"]=1
    elif mutation=="cost":
        R["native_short_mask_frontiers"][-1]["resource_ledger"]["counts_hex"]["persistent_workspace_bits"]="0x1"
    elif mutation=="coverage":
        R["native_short_mask_frontiers"][0]["resource_ledger"]["native_mean_coarse_coverage_lower_bound"]["numerator_hex"]="0x0"
    elif mutation=="census":
        R["complete_source_censuses"][0]["mutual_unique_marked_assignments"]+=1
    elif mutation=="signal":
        R["native_short_mask_frontiers"][0]["native_mean_useful_visibility_lower_bound"]["numerator_hex"]="0x1"
    elif mutation=="seed":
        F["program"]["seed_has_been_conditioned_on_success"]=True
    elif mutation=="scope":
        R["scope"]["polynomial_time_or_coherent_space_claimed"]=True
    else:
        R["accepted_speedup_candidate"]=True
    assert js_check(R,tmp_path).returncode!=0


def test_read_only_CLI_keeps_live_artifact_unchanged():
    before=REPORT.read_bytes()
    proc=subprocess.run([sys.executable,"qsearch.py","dcp-vector-short-mask-join","--no-write"],
                        cwd=ROOT,capture_output=True,text=True)
    assert proc.returncode==0,proc.stderr
    assert json.loads(proc.stdout)["polynomial_time_claimed"] is False
    assert REPORT.read_bytes()==before
