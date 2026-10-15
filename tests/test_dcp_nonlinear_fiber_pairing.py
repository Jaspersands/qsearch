"""Native fibre algebra, full-space reciprocal compiler and scaling falsifiers."""
from collections import Counter
from copy import deepcopy
from fractions import Fraction
from functools import lru_cache
from itertools import product
import json
import math
from pathlib import Path
from random import Random
import subprocess
import sys

import numpy as np
import pytest

from dcp_pairing_programs import mutual_circuit_maps
from theorems.dcp_adaptive_direction_rank_gate import decode_dyadic as probability
from theorems.dcp_nonlinear_fiber_pairing import (
    REPORT, augmentation_parity_certificate, build_report, compiler_certificate,
    exact_one_counting_reduction, exact_one_encoding, instance, lookup_program,
    native_bound, noise_frontier, phase_value, program_value, reference_program,
    useful_relation, wire_map,
    coarse_program,
)

ROOT=Path(__file__).resolve().parents[1]
CHECKER=ROOT/"research/certificates/dcp_nonlinear_fiber_pairing_crosscheck.js"


@pytest.fixture(scope="module")
def report(): return build_report()


def test_all_small_mod_four_matrices_against_augmentation_polynomial():
    checked=0
    for m in range(1,6):
        for row in product(range(4),repeat=m):
            c=augmentation_parity_certificate((row,),3,2)
            counts=Counter(sum(a*((x>>i)&1) for i,a in enumerate(row))%4 for x in range(1<<m))
            assert c["all_fibres_even"]==all(v%2==0 for v in counts.values())
            if m>3: assert c["all_fibres_even"] and not c["nonzero_Y_monomials"]
            checked+=1
    assert checked==1364


def test_threshold_is_sharp_and_even_fibres_do_not_imply_useful_labels():
    for n in (1,2,3):
        A=tuple(tuple(int(i//3==j) for i in range(3*n)) for j in range(n))
        c=augmentation_parity_certificate(A,4,2)
        assert len(c["odd_coarse_fibres"])==4**n
        assert c["nonzero_Y_monomials"]==[[3]*n]
        extra=tuple(row+(j+1,) for j,row in enumerate(A))
        assert augmentation_parity_certificate(extra,4,2)["all_fibres_even"]
        if n<=2:
            # This exceptional FULL A has no higher lifts: coarse agreement
            # already forces identical full sums. Mean bounds are not pointwise.
            assert probability(compiler_certificate(A,4,2,reference_program(A))["useful_descent_probability"])==0
    # All counts can be even while every possible pair has zero full label.
    A=((0,)*5,)
    assert augmentation_parity_certificate(A,4,2)["all_fibres_even"]
    c=compiler_certificate(A,4,2,reference_program(A))
    assert probability(c["useful_descent_probability"])==0


def optimal_pair_weight(A,t,h,visibility):
    """Independent exhaustive matching DP on original assignments."""
    M=1<<len(A[0])
    @lru_cache(None)
    def search(vertices):
        if not vertices: return Fraction(0)
        x,*rest=vertices
        best=search(tuple(rest))
        for y in rest:
            a=tuple(sum(row[i]*((x>>i)&1) for i in range(len(row)))%(1<<t) for row in A)
            b=tuple(sum(row[i]*((y>>i)&1) for i in range(len(row)))%(1<<t) for row in A)
            if a!=b and all((v-u)%(1<<h)==0 for u,v in zip(a,b)):
                best=max(best,visibility**((x^y).bit_count())+search(tuple(z for z in rest if z!=y)))
        return best
    return Fraction(2,M)*search(tuple(range(M)))


@pytest.mark.parametrize("visibility",[Fraction(1),Fraction(1,4),Fraction(3,4)])
def test_native_mean_coverage_and_noise_bounds_against_every_small_full_label_matrix(visibility):
    mean=Fraction(0)
    for row in product(range(8),repeat=2):
        mean+=optimal_pair_weight((row,),3,1,visibility)/64
    bound=noise_frontier(1,3,1,2,visibility)
    assert probability(bound["native_mean_optimal_useful_visibility_lower_bound"])<=mean
    assert mean<=probability(bound["native_mean_any_pairing_visibility_upper_bound"])


def test_all_625_partial_programs_keep_only_reciprocal_useful_pairs():
    A=((4,0),(0,4))
    for values in product((None,0,1,2,3),repeat=4):
        program=lookup_program(values,2)
        c=compiler_certificate(A,3,2,program)
        expected=[x for x,y in enumerate(values) if y is not None and y!=x and values[y]==x]
        assert c["accepted_assignments"]==expected
        assert probability(c["useful_descent_probability"])==Fraction(len(expected),4)


@pytest.mark.parametrize("values",[(1,0,3,2),(1,0,1,0),(None,)*4,(0,1,2,3)])
def test_both_compiler_stages_are_permutations_on_every_dirty_workspace_value(values):
    program=lookup_program(values,2)
    A=((4,0),(0,4))
    for stage in ("accept","order"):
        outputs=[wire_map(w,program,A,3,2,stage) for w in range(1<<10)]
        assert sorted(outputs)==list(range(1<<10))
        assert all(wire_map(out,program,A,3,2,stage,inverse=True)==w for w,out in enumerate(outputs))


def test_vector_compiler_matches_existing_six_call_scalar_construction_on_its_special_case():
    values=(1,0,3,2)
    old=mutual_circuit_maps((4,0),8,values)
    program=lookup_program(values,2)
    for name,new in (("accept","accept"),("ordered","order")):
        assert [wire_map(w,program,((4,0),),3,2,new) for w in range(1<<10)]==old[name].tolist()


@pytest.mark.parametrize("visibility",[1,Fraction(3,4)])
def test_original_unknown_phase_density_through_compiled_isometry_every_outcome(report,visibility):
    for C in report["nonlinear_reference_controls"]:
        A=tuple(tuple(int(a,16) for a in row) for row in C["public_labels_hex"])
        m,n=len(A[0]),len(A)
        secret=tuple(1+2*j for j in range(n))
        rho=np.ones((1,1),complex)
        for i in reversed(range(m)):
            angle=2*math.pi*(sum(s*row[i] for s,row in zip(secret,A))%16)/16
            off=float(visibility)*np.exp(-1j*angle)
            rho=np.kron(rho,np.array([[1,off],[off.conjugate(),1]])/2)
        M=1<<m
        K=np.zeros((2*M,M),int)
        for x in C["accepted_assignments"]:
            accepted=wire_map(x,C["program"],A,4,2,"accept")
            ordered=wire_map(accepted,C["program"],A,4,2,"order")
            r,e=ordered&(M-1),(ordered>>(3*m+3))&1
            K[2*r+e,x]=1
        expected_projector=np.zeros(M,int)
        expected_projector[C["accepted_assignments"]]=1
        assert np.array_equal(K.T@K,np.diag(expected_projector))
        transformed=K@rho@K.T
        assert np.trace(transformed).real==pytest.approx(float(probability(C["useful_descent_probability"])))
        total=0.0
        for pair in C["pairs"]:
            r=pair["first"]
            block=transformed[2*r:2*r+2,2*r:2*r+2]
            mass=np.trace(block).real
            assert mass==pytest.approx(2/M)
            label=tuple(int(a,16) for a in pair["descended_label_hex"])
            assert any(label)
            angle=2*math.pi*(sum(s*a for s,a in zip(secret,label))%4)/4
            v=float(visibility)**pair["physical_Hamming_width"]
            off=v*np.exp(-1j*angle)
            assert np.allclose(block/mass,np.array([[1,off],[off.conjugate(),1]])/2,atol=2e-14)
            total+=mass
        assert total==pytest.approx(float(probability(C["useful_descent_probability"])))


def test_reference_really_closes_the_finite_affine_gap_but_charges_exponential_program(report):
    C=report["nonlinear_reference_controls"][2]
    assert C["source_control"].startswith("SELECTED-")
    assert probability(C["useful_descent_probability"])==Fraction(11,16)
    assert probability(C["source_affine_useful_descent_probability"])==Fraction(9,16)
    assert C["program"]["row_address_comparisons_per_XOR_F"]==64
    assert C["program"]["uniform_efficient_program_supplied"] is False
    assert C["accepted_XOR_F_calls"]==6 and C["failed_XOR_F_calls"]==4
    assert C["fresh_descended_labels_IID_certified"] is False


def test_near_unit_native_existence_is_not_a_compiler_and_constant_noise_is_not_inverse_dimension_noise(report):
    row=report["one_extra_copy_parity_frontiers"][1]
    assert row["secret_vector_components"]==64 and row["original_copies"]==193
    assert row["every_coarse_fibre_even_for_every_A"] is True
    assert probability(row["native_mean_optimal_useful_pairing_coverage_lower_bound"])>1-Fraction(1,1<<3903)
    assert row["efficient_pairing_program_constructed_by_bound"] is False
    assert row["naive_reference_table_rows"]=={"power_of_two":193}
    assert row["reference_table_cost_is_not_a_lower_bound_on_structured_programs"] is True
    for row in report["native_growing_parameter_frontiers"]:
        if probability(row["visibility"])==Fraction(1,4):
            assert probability(row["native_mean_any_pairing_visibility_upper_bound"])<Fraction(1,1<<row["secret_vector_components"])
    for row in report["joint_growing_parameter_frontiers"]:
        assert row["phase_bits"]==row["secret_vector_components"]
        assert probability(row["native_mean_optimal_useful_visibility_lower_bound"])>Fraction(1,25)
    assert 32**32 < 2**16*31**31  # Fixed exact constant in the documented entropy-free tail proof.


def test_coarse_only_pairing_has_an_exact_higher_label_law_not_a_full_A_conditional_claim(report):
    for control in report["coarse_only_higher_label_source_controls"]:
        B=tuple(tuple(row) for row in control["coarse_labels"])
        t,h=control["phase_bits"],control["descent_bits"]
        n,m=len(B),len(B[0]);R=1<<(t-h);K=1<<h
        program=control["program_fixed_before_higher_lifts"]
        for seed in range(8):
            rng=Random(seed)
            full=tuple(tuple(a+K*rng.randrange(R) for a in row) for row in B)
            assert coarse_program(full,t,h)==program
        for record in control["per_pair_output_histograms"]:
            assert len(record["counts"])==R**n
            assert {row["count"] for row in record["counts"]}=={R**(n*(m-1))}
        p=probability(control["coarse_admission_probability"])
        assert probability(control["joint_coarse_admission_and_nonzero_label_probability"])==p*(1-Fraction(1,R**n))
        assert control["uniformity_is_conditioned_on_old_full_A"] is False
        assert control["native_output_interface_discards_original_higher_label_transcript"] is True
        assert control["full_label_dependent_programs_inherit_this_law"] is False
    row=native_bound(64,64,2,193)
    exact=probability(row["coarse_only_maximal_pairing_exact_mean_IF_even_fibres"])
    assert exact==1-Fraction(1,1<<3968)


def test_coarse_selector_zero_filter_is_paid_on_every_higher_label_lift():
    B=((1,1,1,1),);program=coarse_program(B,3,2)
    total=Fraction(0)
    for z in product(range(2),repeat=4):
        A=(tuple(b+4*h for b,h in zip(B[0],z)),)
        certificate=compiler_certificate(A,3,2,program)
        total+=probability(certificate["useful_descent_probability"])/16
    assert total==Fraction(1,2)


def test_public_zero_injection_restores_pure_uniform_source_but_not_automatically_noisy_source():
    R=4;secret=3;visibility=0.75
    pure=np.zeros((2*R,2*R),complex)
    nonzero=np.zeros_like(pure)
    noisy=np.zeros_like(pure)
    for label in range(R):
        angle=2*math.pi*(secret*label%R)/R
        off=np.exp(-1j*angle)
        block=np.array([[1,off],[off.conjugate(),1]])/2
        pure[2*label:2*label+2,2*label:2*label+2]=block/R
        noisy[2*label:2*label+2,2*label:2*label+2]=np.array([[1,visibility*off],[visibility*off.conjugate(),1]])/(2*R)
        if label: nonzero[2*label:2*label+2,2*label:2*label+2]=block/(R-1)
    restored=(1-1/R)*nonzero
    restored[:2,:2]=np.ones((2,2))/(2*R)
    assert np.allclose(restored,pure)
    mixed_restoration=noisy.copy();mixed_restoration[:2,:2]=np.ones((2,2))/(2*R)
    distance=sum(abs(np.linalg.eigvalsh(mixed_restoration-noisy)))/2
    assert distance==pytest.approx((1-visibility)/(2*R))


def test_counting_reduction_and_simple_pairing_are_different_tasks(report):
    for C in report["counting_route_falsifiers"]:
        assert C["coarse_target_fibre_count"]==C["exact_one_satisfying_assignments"]*C["known_count_multiplier"]
        assert probability(C["simple_useful_pairing"]["useful_descent_probability"])==1
        assert C["counting_hardness_implies_general_pairing_hardness"] is False
        assert C["pairing_solves_exact_one_counting"] is False
    # Even an unsatisfiable original constraint system has the trivial useful
    # padded-coordinate pairing. Its existence is not a SAT/counting answer.
    C=exact_one_counting_reduction(((0,0,0),),1)
    assert C["coarse_target_fibre_count"]==0
    assert probability(C["simple_useful_pairing"]["useful_descent_probability"])==1


def test_polynomial_encoding_and_known_program_work_without_large_truth_tables():
    clauses=tuple((i,(i+1)%64,(i+2)%64) for i in range(64))
    encoding=exact_one_encoding(clauses,64)
    A,P=encoding["labels"],encoding["program"]
    assert P["width"]==193 and "table" not in P
    assert P["CNOT_gates_per_XOR_F"]==193 and P["X_gates_per_XOR_F"]==2
    rng=Random(101506)
    for _ in range(8):
        x=rng.getrandbits(193)
        y=program_value(P,x)
        assert program_value(P,y)==x and useful_relation(A,3,2,x,y)
        w=wire_map(x,P,A,3,2,"accept")
        assert w==x|(1<<(3*193+2))
        assert wire_map(w,P,A,3,2,"accept",inverse=True)==x


def test_free_lookup_and_missing_schema_fail_closed():
    program=lookup_program((1,0,3,2),2)
    program["table_lookup_is_a_free_coherent_oracle"]=True
    with pytest.raises(ValueError,match="free"): compiler_certificate(((4,0),),3,2,program)
    with pytest.raises(ValueError,match="UNKNOWN"): reference_program(((1,)*10,))
    with pytest.raises(ValueError): instance(((True,),),3,2)
    with pytest.raises(ValueError): native_bound(2,3,3,6)
    with pytest.raises(ValueError): noise_frontier(2,4,2,6,0.5)


def js_check(record,tmp_path):
    target=tmp_path/"certificate.json"
    target.write_text(json.dumps(record))
    return subprocess.run(["node",str(CHECKER),str(target)],capture_output=True,text=True)


def test_current_artifact_and_independent_source_algebra_wire_replay(report,tmp_path):
    assert json.loads(REPORT.read_text())==report
    done=js_check(report,tmp_path)
    assert done.returncode==0,done.stderr
    assert json.loads(done.stdout)["native_frontiers"]==28


@pytest.mark.parametrize("mutation",["label","table","calls","oracle","mean","parity","noise","counting","scope","provenance","higher_hist","higher_scope"])
def test_forged_claims_and_favorable_source_relabeling_rejected(report,tmp_path,mutation):
    bad=deepcopy(report)
    C=bad["nonlinear_reference_controls"][2]
    if mutation=="label": C["pairs"][0]["descended_label_hex"]=["0x0","0x0"]
    elif mutation=="table": C["program"]["table"][C["accepted_assignments"][0]]=None
    elif mutation=="calls": C["failed_XOR_F_calls"]=0
    elif mutation=="oracle": C["program"]["row_address_comparisons_per_XOR_F"]=1
    elif mutation=="mean": bad["native_growing_parameter_frontiers"][0]["native_mean_optimal_useful_pairing_coverage_lower_bound"]["numerator_hex"]="0x1"
    elif mutation=="parity": bad["augmentation_parity_controls"][0]["all_fibres_even"]=True
    elif mutation=="noise": bad["native_growing_parameter_frontiers"][0]["native_mean_any_pairing_visibility_upper_bound"]["numerator_hex"]="0x0"
    elif mutation=="counting": bad["counting_route_falsifiers"][1]["coarse_target_fibre_count"]+=1
    elif mutation=="scope": bad["scope"]["worst_case_fibre_counting_hardness_is_pairing_hardness"]=True
    elif mutation=="higher_hist": bad["coarse_only_higher_label_source_controls"][0]["per_pair_output_histograms"][0]["counts"][0]["count"]+=1
    elif mutation=="higher_scope": bad["coarse_only_higher_label_source_controls"][0]["uniformity_is_conditioned_on_old_full_A"]=True
    else: bad["source_affine_sha256"]="0"*64
    assert js_check(bad,tmp_path).returncode!=0


def test_read_only_cli_preserves_artifact():
    before=REPORT.read_bytes()
    done=subprocess.run([sys.executable,"qsearch.py","dcp-nonlinear-fiber-pairing","--no-write"],cwd=ROOT,capture_output=True,text=True)
    assert done.returncode==0,done.stderr
    assert json.loads(done.stdout)["efficient_native_receiver_supplied"] is False
    assert REPORT.read_bytes()==before
