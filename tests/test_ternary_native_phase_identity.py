from fractions import Fraction
from itertools import product
import json
import math
import subprocess

import pytest

from ternary_cubic_program_factory import relation, seeded_cohort
from ternary_native_phase_identity import (
    REPORT, RidgePhase, identity_budget, injection_control, lift_program,
    merge, test_identity as probe_identity,
)
from ternary_phase_depth import cyclic_difference


@pytest.fixture(scope="module")
def cohorts():
    base=seeded_cohort(2,3,88708);c,certificate=relation(base)
    outcomes=tuple(tuple((j+i+1) % 3 for i in range(3)) for j in certificate["selected_program_indices"])
    return {r:(tuple(lift_program(p,r,88800+r*100+j) for j,p in enumerate(base)),c,outcomes) for r in (1,2,3)}


@pytest.mark.parametrize("r",[1,2,3])
def test_compact_native_evaluator_equals_actual_original_root(cohorts,r):
    programs,_,_=cohorts[r]
    for p in programs:
        compact=p.compact()
        assert compact.modulus==3**r and compact.additive_degree_bound==2*r+1
        assert not compact.record()["high_degree_tensor_expanded"]
        for z in product(range(3),repeat=3): assert compact.value(z)==p.original_value(z)


@pytest.mark.parametrize("r",[1,2,3])
def test_signed_one_use_merge_preserves_full_root_and_all_source_costs(cohorts,r):
    programs,c,outcomes=cohorts[r];phase,record=merge(programs,c,outcomes)
    selected=record["selected_program_indices"]
    assert phase.modulus==3**r and len(selected)==4
    assert record["full_original_input_cap_charged"]==675
    assert not record["physical_IID_independence_certified_by_ids"]
    assert not record["efficient_search_for_useful_merge_rule_supplied"]
    assert not record["quantum_speedup_proved"]
    assert Fraction(record["conditional_injection_transcript_probability"])==Fraction(1,3**12)
    for z in product(range(3),repeat=3):
        expected=tuple(sum(programs[j].original_value(tuple((a+c[j]*b) % 3 for a,b in zip(m,z)))[l]-programs[j].original_value(m)[l] for j,m in zip(selected,outcomes)) % phase.modulus for l in range(2))
        assert phase.value(z)==expected
    if r>1:
        values=[a for z in product(range(3),repeat=3) for a in phase.value(z)]
        assert math.gcd(phase.modulus,*values)==1


def test_shared_denominator_carry_is_not_divided_locally():
    phase=RidgePhase(2,1,1,3,(((1,0),((0,1,2),)),((0,1),((0,1,2),)),((1,1),((0,8,7),))))
    assert phase.value((1,2))==(1,)
    assert phase.value((1,1))==(0,)
    assert any(row[1] % 3 for _,tables in phase.groups for row in tables)
    assert all(phase.value(z)==(int(sum(z)>=3),) for z in product(range(3),repeat=2))


@pytest.mark.parametrize("r",[1,2,3])
def test_local_valuation_degree_formula_matches_actual_cyclic_tables(r):
    N=3**(r+1)
    for a in range(N):
        for c in range(a % 3*2 % 3,N,3):
            table=(0,a,c);rows=[table]
            for _ in range(2*r+2):rows.append(cyclic_difference(rows[-1],1,N))
            actual=max((k for k in range(1,len(rows)) if any(rows[k])),default=0)
            def v(x):
                if not x:return r+1
                exponent=0
                while x % 3==0:exponent+=1;x//=3
                return exponent
            u,w=min(map(v,rows[1])),min(map(v,rows[2]))
            assert actual==max(0,2*(r+1-u)-1,2*(r+1-w))
            assert not any(rows[-1])


@pytest.mark.parametrize("r",[1,2,3])
def test_top_cancellation_exact_but_quadratic_transfer_fails_at_higher_roots(cohorts,r):
    programs,c,outcomes=cohorts[r];phase,_=merge(programs,c,outcomes)
    certificate=phase.degree_certificate()
    assert certificate["certified_global_degree_upper"]==2*r
    assert not certificate["upper_bound_is_exact_global_degree"]
    top=probe_identity(phase,2*r+1,seed=100)
    assert top["status"]=="EXACT_FACTORED_IDENTITY" and top["evaluations_used"]==0
    assert top["identity_algebraically_certified"]
    probe=probe_identity(phase,3,seed=88900+r)
    if r==1:assert probe["status"]=="EXACT_FACTORED_IDENTITY"
    else:
        assert probe["status"]=="EXPLICIT_COUNTEREXAMPLE"
        witness=probe["counterexample"];v=witness["directions"];base=witness["base"]
        # Independent finite-difference cube; the production evaluator does not build it.
        actual=[0,0]
        for bits in product(range(2),repeat=len(v)):
            z=tuple((base[i]+sum(b*h[i] for b,h in zip(bits,v))) % 3 for i in range(3))
            sign=(-1)**(len(v)-sum(bits))
            for l,x in enumerate(phase.value(z)):actual[l]+=sign*x
        assert tuple(x % phase.modulus for x in actual)==tuple(witness["component_derivative"])
        assert any(actual[l] % phase.modulus for l in range(2))


def cancellation_phase():
    # A polynomial identity calibration, never an algorithm candidate.
    return RidgePhase(2,1,1,3,(((1,0),((0,3,6),)),((0,1),((0,3,6),)),((1,1),((0,6,3),))))


def test_fresh_random_points_have_conditional_soundness_not_exact_proof():
    phase=cancellation_phase()
    assert phase.degree_certificate()["certified_global_degree_upper"]==1
    assert all(phase.value(z)==(0,) for z in product(range(3),repeat=2))
    result=probe_identity(phase,0,kappa=3)
    assert result["status"]=="RANDOMIZED_IDENTITY_EVIDENCE"
    assert result["soundness_bound_applicable_to_this_run"]
    assert result["evaluations_used"]==6
    assert not result["exact_identity_proved_by_random_testing"]
    assert not result["identity_algebraically_certified"]


@pytest.mark.parametrize("seed,cap",[(100,100),(None,1)])
def test_seeded_or_underbudget_no_witness_is_never_certified(seed,cap):
    result=probe_identity(cancellation_phase(),0,kappa=3,max_evaluations=cap,seed=seed)
    assert result["status"]=="UNCERTIFIED_NO_WITNESS"
    assert not result["soundness_bound_applicable_to_this_run"]
    assert not result["deterministic_seed_is_mathematical_randomness_certificate"]


@pytest.mark.parametrize("r",[1,2,4,8,16,32])
def test_dimension_independent_budget_is_polynomial_in_q_not_log_q(r):
    budget=identity_budget(2*r+1,32)
    assert budget["independent_uniform_tests_required"]==64*4**r
    assert Fraction(budget["nonzero_relative_support_lower"])==Fraction(1,2**(2*r+1))
    assert Fraction(budget["conditional_false_accept_probability_upper"])==Fraction(1,2**32)
    assert budget["dimension_independent"] and budget["fresh_points_after_candidate_commit_required"]


@pytest.mark.parametrize("r",[1,2,3])
def test_physical_native_injection_is_uniform_with_full_modulus_secret(cohorts,r):
    programs,c,_=cohorts[r];j=next(i for i,x in enumerate(c) if x==2)
    result=injection_control(programs[j],2,(3**r-1,2))
    assert result["all_injection_outcomes"]==27
    assert result["reference_dimension"]==27
    assert result["arbitrary_reference_entangled_max_error"]<1e-12


def test_invalid_class_membership_and_source_reuse_rejected(cohorts):
    with pytest.raises(ValueError,match="low linearity"):
        RidgePhase(1,1,1,3,(((1,),((0,1,1),)),))
    with pytest.raises(ValueError,match="kernel"):
        RidgePhase(1,1,1,3,(((1,),((0,1,2),)),))
    with pytest.raises(ValueError,match="degree"):
        RidgePhase(1,1,1,1,())
    programs,_,_=cohorts[1]
    with pytest.raises(ValueError,match="ancestry"):merge((programs[0],programs[0]),(1,1),((0,0,0),(0,0,0)))
    with pytest.raises(ValueError,match="signs"):merge(programs,(3,)*len(programs),())
    with pytest.raises(ValueError,match="measured word"):merge(programs,(1,)*len(programs),())


def test_live_independent_checker():
    result=subprocess.run(["node","research/certificates/ternary_native_phase_identity_crosscheck.js",str(REPORT)],capture_output=True,text=True)
    assert result.returncode==0,result.stderr


@pytest.mark.parametrize("mutation",["table","counterexample","root","cost","proof","degree","budget"])
def test_independent_checker_rejects_false_phase_or_proof_claims(tmp_path,mutation):
    report=json.loads(REPORT.read_text());c=report["native_controls"][1]
    if mutation=="table":c["merged_phase"]["projective_ridge_groups"][0]["component_tables"][0][1]=(c["merged_phase"]["projective_ridge_groups"][0]["component_tables"][0][1]+3)%27
    elif mutation=="counterexample":c["degree_two_probe"]["counterexample"]["component_derivative"]=[0,0]
    elif mutation=="root":c["merged_phase"]["phase_modulus"]="3"
    elif mutation=="cost":c["full_original_input_cap_charged"]-=1
    elif mutation=="proof":c["degree_two_probe"]["exact_identity_proved_by_random_testing"]=True
    elif mutation=="degree":c["top_degree_probe"]["degree_certificate"]["certified_global_degree_upper"]-=1
    else:report["identity_budgets"][0]["independent_uniform_tests_required"]-=1
    p=tmp_path/"mutation.json";p.write_text(json.dumps(report))
    result=subprocess.run(["node","research/certificates/ternary_native_phase_identity_crosscheck.js",str(p)],capture_output=True,text=True)
    assert result.returncode!=0
