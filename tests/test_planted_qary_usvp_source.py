"""Public-input, exact-field, uniqueness-scope and classical falsifier tests."""
from copy import deepcopy
from dataclasses import replace
from fractions import Fraction
from itertools import product
import json
from math import prod
import subprocess

import pytest
from flint import fmpz_mat, fmpz_mod_ctx, fmpz_mod_mat
from sympy import nextprime
from theorems import planted_qary_usvp_source as S


def small():
    return S.generate_source(4,2,257,2,4,plant_seed=99600,matrix_seed=99700)


@pytest.mark.parametrize("q", (3,257,int(nextprime(2**80))))
def test_exact_recursive_prime_certificates(q):
    certificate=S.prime_certificate(q).record()
    assert S.validate_prime_record(certificate)
    assert certificate["prime"]==q


@pytest.mark.parametrize("q", (9,15,341,561,1105))
def test_composite_fields_rejected(q):
    with pytest.raises(ValueError,match="prime"):
        S.PublicQaryLattice(q,((1,0,1,1),))


@pytest.mark.parametrize("kind", ("witness","factor","child","duplicate"))
def test_prime_certificate_tampering_rejected(kind):
    c=deepcopy(S.prime_certificate(257).record())
    if kind=="witness": c["witness"]=1
    elif kind=="factor": c["factors"][0]["exponent"]+=1
    elif kind=="child": c["factors"][0]["certificate"]["witness"]=2
    else: c["factors"]=c["factors"]*2
    with pytest.raises(ValueError): S.validate_prime_record(c)


@pytest.mark.parametrize("q", (257,int(nextprime(2**80))))
def test_full_kernel_basis_arbitrary_pivots_index_and_public_membership(q):
    p=S.PublicQaryLattice(q,((0,1,0,q-2,1),(0,0,1,1,2)))
    assert p.pivots==(1,2)
    assert p.free==(0,3,4)
    assert abs(int(fmpz_mat(p.basis).det()))==q**2
    assert all(p.member(row) for row in p.basis)
    for coeff in product((-1,0,1),repeat=5):
        v=tuple(sum(a*row[j] for a,row in zip(coeff,p.basis)) for j in range(5))
        assert p.member(v)


def test_solver_input_contains_neither_plant_nor_private_seeds():
    g=small();public=g.problem.public_record()
    assert public["solver_input_contains_plant_seed_or_solution"] is False
    assert not any("seed" in key or "plant" in key for key in public if key!="solver_input_contains_plant_seed_or_solution")
    for attack in (S.sparse_column_attack,S.public_LLL_attack,S.ternary_MITM_attack):
        with pytest.raises(ValueError,match="public lattice only"):attack(g)


def test_public_problem_digest_binds_every_basis_and_field_entry():
    g=small()
    p=g.problem.public_record()
    assert p["public_problem_sha256"]==g.problem.public_record()["public_problem_sha256"]
    H=[list(row) for row in g.problem.H];H[0][3]=(H[0][3]+1)%g.problem.prime
    altered=S.PublicQaryLattice(g.problem.prime,H).public_record()
    assert altered["public_problem_sha256"]!=p["public_problem_sha256"]


def test_small_exact_rank_conditioning_and_nonparallel_collision_probability():
    rows=tuple((a,b,c,(-a-b-c)%3) for a,b,c in product(range(3),repeat=3))
    full,annihilate=0,0
    v=(1,-1,0,0)
    for a,b in product(rows,repeat=2):
        if int(fmpz_mod_mat((a,b),fmpz_mod_ctx(3)).rank())==2:
            full+=1
            annihilate+=all(sum(x*y for x,y in zip(row,v))%3==0 for row in (a,b))
    rank=Fraction(full,len(rows)**2)
    assert rank==prod(1-Fraction(1,3**e) for e in (3,2))
    assert rank>=Fraction(5,6)
    assert Fraction(annihilate,full)<=Fraction(6,5*3**2)


@pytest.mark.parametrize("n,R", ((1,0),(2,1),(3,2),(4,3),(6,2)))
def test_integer_volume_bound_dominates_complete_sphere_count(n,R):
    bound=S.lattice_ball_count_bound(n,R)
    points=sum(sum(x*x for x in v)<=R*R for v in product(range(-R,R+1),repeat=n))
    assert points<=bound["selected_count_base"]**n
    c=bound["ceil_radius_over_sqrt_dimension"]
    assert n*c*c>=R*R
    if c: assert n*(c-1)*(c-1)<R*R


def test_prime_selection_and_failure_exponents_are_exact_integer_inequalities():
    g=S.generate_source(12,plant_seed=4,matrix_seed=5)
    L=g.private.ledger;F=L["conditional_failure_bound_factors"]
    num=6*F["count_base"]**F["count_exponent"];den=5*F["prime"]**F["prime_exponent"]
    k=L["conditional_failure_upper_dyadic"]["negative_exponent"]
    assert num*2**k<=den<num*2**(k+1)
    assert k>=16
    assert L["prime_selection"]["chosen_before_classical_attack_outcomes"]
    assert L["generator_rejects_on_classical_attack_or_uniqueness_outcome"] is False
    assert L["individual_instance_uniqueness_certified"] is False
    assert L["computational_hardness_proved"] is False


@pytest.mark.parametrize("q,R,G,support", ((7,4,2,4),(257,1,2,4)))
def test_invalid_uniqueness_scope_has_no_bound(q,R,G,support):
    L=S.uniqueness_ledger(4,2,q,R,G,support)
    assert L["status"]=="UNKNOWN_UNIQUENESS_SCOPE"
    assert L["conditional_failure_upper_dyadic"] is None
    assert L["bound_is_nonvacuous"] is False


def test_generator_rank_rejections_are_charged_and_reproducible():
    chosen=next(seed for seed in range(100) if len(S.generate_source(
        4,2,3,2,4,plant_seed=3,matrix_seed=seed).private.attempted_matrices)>1)
    g=S.generate_source(4,2,3,2,4,plant_seed=3,matrix_seed=chosen)
    h=S.generate_source(4,2,3,2,4,plant_seed=3,matrix_seed=chosen)
    assert g==h
    assert all(a["rank"]<2 for a in g.private.attempted_matrices[:-1])
    assert g.private.attempted_matrices[-1]["rank"]==2
    assert g.private.ledger["seeded_PRNG_fixture_is_not_a_formal_IID_sampler"]
    with pytest.raises(ValueError,match="UNKNOWN_GENERATOR_RANK_CAP"):
        S.generate_source(4,2,3,2,4,plant_seed=3,matrix_seed=chosen,max_attempts=1)


@pytest.mark.parametrize("H", (((1,0,1,2),),((1,1,2,3),),((1,4,2,3),)))
def test_sparse_columns_are_legal_public_negative_controls(H):
    p=S.PublicQaryLattice(5,H)
    attack=S.sparse_column_attack(p)
    assert p.member(attack["vector"])
    assert attack["squared_norm"]<=2


def test_complete_MITM_minimum_agrees_with_whole_ternary_census_and_zero_exception():
    p=S.PublicQaryLattice(5,((1,2,1,2),))
    vectors=tuple(v for v in product((-1,0,1),repeat=4) if any(v) and p.member(v))
    attack=S.ternary_MITM_attack(p)
    assert attack["squared_norm"]==min(S.norm_squared(v) for v in vectors)
    assert p.member(attack["vector"])
    # Left zero-syndrome bucket includes zero and must retain a nonzero option.
    p=S.PublicQaryLattice(5,((0,0,1,2),))
    assert S.ternary_MITM_attack(p)["squared_norm"]==1


def test_MITM_and_radius_caps_never_certify_absence():
    g=small()
    attack=S.ternary_MITM_attack(g.problem,max_states=1)
    census=S.complete_radius_audit(g,max_states=1)
    assert attack["status"]=="UNKNOWN_COMPLETE_MITM_CAP"
    assert attack["cap_failure_proves_hardness"] is False
    assert census["status"]=="UNKNOWN_COMPLETE_RADIUS_CAP"
    assert census["individual_uniqueness_certified"] is False
    assert census["truncated_search_certifies_absence"] is False


def test_LLL_public_transform_and_matched_classical_recovery():
    g=small();attack=S.public_LLL_attack(g.problem)
    T=fmpz_mat(attack["unimodular_row_transform"])
    assert abs(int(T.det()))==1
    assert T*fmpz_mat(g.problem.basis)==fmpz_mat(attack["reduced_row_basis"])
    assert S.audit_attacks(g,{"LLL":attack})["tested_instance_classically_recovers_planted_direction"]
    assert attack["plant_or_private_seed_used"] is False


def test_complete_radius_census_certifies_only_this_instance_and_finds_bad_instance():
    census=S.complete_radius_audit(small())
    assert census["status"]=="COMPLETE_FINITE_RADIUS_CENSUS"
    assert census["individual_uniqueness_certified"]
    assert census["growing_family_hardness_or_quantum_advantage_certified"] is False
    g=S.generate_source(4,2,3,2,4,plant_seed=3,matrix_seed=2)
    c=S.complete_radius_audit(g)
    assert c["PRIVATE_AUDIT_ONLY_nonparallel_kernel_vectors"]
    assert c["individual_uniqueness_certified"] is False


def test_private_radius_ledger_is_bound_before_calibration():
    g=small();L=deepcopy(g.private.ledger);L["prime"]+=2
    altered=replace(g,private=replace(g.private,ledger=L))
    for f in (S.complete_radius_audit,lambda x:S.audit_attacks(x,{})):
        with pytest.raises(ValueError,match="not bound"):f(altered)


def test_attack_calibration_uses_only_legal_public_primitive_normalization():
    g=small();v=tuple(2*x for x in g.private.plant)
    assert S.audit_attacks(g,{"multiple":{"vector":v}})["tested_instance_classically_recovers_planted_direction"]
    q_basis=(g.problem.prime,0,0,0)
    assert g.problem.member(q_basis)
    if not g.problem.member((1,0,0,0)):
        C=S.audit_attacks(g,{"basis":{"vector":q_basis}})["PRIVATE_AUDIT_ONLY_attack_calibrations"][0]
        assert C["public_membership_checked_normalized_vector"]==q_basis
    with pytest.raises(ValueError,match="invalid/zero"):S.audit_attacks(g,{"zero":{"vector":(0,0,0,0)}})


def node_check(payload):
    return subprocess.run(["node","-e",
        "const X=require('./research/certificates/planted_qary_usvp_source_crosscheck.js');"
        "let s='';process.stdin.on('data',x=>s+=x);"
        "process.stdin.on('end',()=>console.log(JSON.stringify(X.verify(JSON.parse(s)))));"],
        input=json.dumps(payload),text=True,capture_output=True,cwd=S.ROOT)


def test_independent_source_and_classical_certificate_replay():
    result=node_check(json.loads(S.REPORT.read_text()))
    assert result.returncode==0,result.stderr
    output=json.loads(result.stdout)
    assert output["source_controls"]==8
    assert output["verified"] is True


@pytest.mark.parametrize("kind", ("basis","prime","rank","private","dyadic","LLL","MITM","scope","hash"))
def test_independent_checker_rejects_tampering(kind):
    report=json.loads(S.REPORT.read_text());C=report["source_controls"][0]
    if kind=="basis": C["public_problem"]["row_basis"][0][0]+=1
    elif kind=="prime": C["public_problem"]["prime_certificate"]["witness"]=1
    elif kind=="rank": C["PRIVATE_AUDIT_ONLY_generation"]["attempted_matrices"][0]["rank"]-=1
    elif kind=="private": C["PRIVATE_AUDIT_ONLY_generation"]["plant"][0]=0
    elif kind=="dyadic": C["distributional_uniqueness_ledger"]["conditional_failure_upper_dyadic"]["negative_exponent"]+=1
    elif kind=="LLL": C["public_classical_attacks"]["public_LLL"]["unimodular_row_transform"][0][0]+=1
    elif kind=="MITM": C["public_classical_attacks"]["complete_ternary_MITM"]["squared_norm"]+=1
    elif kind=="scope": report["source_distribution_is_proved_computationally_hard"]=True
    else: report["producer_sha256"]="0"*64
    assert node_check(report).returncode!=0
