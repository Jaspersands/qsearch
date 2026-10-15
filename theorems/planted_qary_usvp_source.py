"""Planted modular-kernel lattice sources and public-data classical falsifiers.

Distributional uniqueness is not instance certification or computational
hardness. Private plants/seeds never enter basis construction or attacks.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
import hashlib
from itertools import product
import json
from math import gcd, isqrt, prod
from pathlib import Path
import random
import time

from flint import fmpz_mat, fmpz_mod_ctx, fmpz_mod_mat
from sympy import factorint, integer_nthroot, isprime, nextprime

from ternary_measured_lattice_decoder import exact_json

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/reductions/planted_qary_usvp_source.json"
DERIVATION=ROOT/"research/PLANTED_QARY_USVP_SOURCE.md"
CONTRACT=ROOT/"research/hypotheses/planted_qary_usvp_source_contract.json"


def integer(x,name,minimum=0):
    if type(x) is not int or x<minimum:
        raise ValueError("exact "+name+" required")
    return x


def matrix_rows(matrix):
    return tuple(tuple(int(x) for x in row) for row in matrix.tolist())


def ceil_sqrt(x):
    integer(x,"nonnegative square root argument")
    r=isqrt(x)
    return r+int(r*r<x)


def lattice_ball_count_bound(n,radius):
    """Disjoint unit cubes + Gaussian volume bound sqrt(2*pi*e)<5."""
    integer(n,"positive count dimension",1);integer(radius,"nonnegative count radius")
    c=isqrt(radius*radius//n)
    if n*c*c<radius*radius: c+=1
    box=2*radius+1
    ball=5*c+3
    return {"containing_box_side":box,"Gaussian_volume_side_upper":ball,
            "ceil_radius_over_sqrt_dimension":c,"selected_count_base":min(box,ball),
            "selected_count_exponent":n,
            "proof":"DISJOINT_UNIT_CUBES_IN_RADIUS_R_PLUS_SQRT_N_OVER2; sqrt(2*pi*e)<5"}


def select_prime(n,m,radius,failure_bits=16):
    integer(n,"dimension",3);integer(m,"rows",1)
    integer(failure_bits,"positive uniqueness failure bits",1)
    if not m<n-1: raise ValueError("rank-conditioned prime selection requires m<n-1")
    bound=lattice_ball_count_bound(n,radius)
    count=bound["selected_count_base"]**n
    target=(6*count*(1<<failure_bits)+4)//5
    root,exact=integer_nthroot(target,m)
    lower=max(3,2*radius+1,int(root)+int(not exact))
    prime=int(nextprime(lower-1))
    if 5*prime**m<6*count*(1<<failure_bits):
        raise ArithmeticError("selected prime does not satisfy conditional failure target")
    return prime,{"failure_bits_target":failure_bits,"integer_prime_lower_bound":lower,
                  "selected_prime":prime,"chosen_before_classical_attack_outcomes":True,
                  "q_to_m_times5_at_least6_count_times2_to_failure_bits":True}


def canonical_sign(v):
    v=tuple(v)
    first=next((x for x in v if x),0)
    return tuple(-x for x in v) if first<0 else v


def norm_squared(v):
    return sum(x*x for x in v)


@dataclass(frozen=True)
class PrimeCertificate:
    prime: int
    witness: int
    factors: tuple

    def record(self):
        return {"prime":self.prime,"witness":self.witness,
            "factors":tuple({"prime":p,"exponent":e,"certificate":c.record()} for p,e,c in self.factors),
            "method":"LUCAS_FULL_N_MINUS_ONE_ORDER_CERTIFICATE"}


@lru_cache(maxsize=1024)
def prime_certificate(q):
    """Exact Lucas certificate; probable primality is only a rejection filter."""
    integer(q,"prime certificate integer",2)
    if q==2: return PrimeCertificate(2,1,())
    if not isprime(q): raise ValueError("prime field required")
    factors=tuple((int(p),int(e),prime_certificate(int(p))) for p,e in sorted(factorint(q-1).items()))
    if prod(p**e for p,e,_ in factors)!=q-1:
        raise ArithmeticError("complete q-1 factorization required")
    for witness in range(2,min(q,514)):
        if pow(witness,q-1,q)==1 and all(gcd(pow(witness,(q-1)//p,q)-1,q)==1 for p,_,_ in factors):
            return PrimeCertificate(q,witness,factors)
    raise ValueError("UNKNOWN_PRIME_CERTIFICATE_WITNESS_CAP; not a composite or hardness claim")


def validate_prime_record(record):
    """Check only exact integer arithmetic, no probable-prime oracle."""
    q=integer(record["prime"],"certificate prime",2)
    witness=integer(record["witness"],"order witness",1)
    factors=record["factors"]
    if record["method"]!="LUCAS_FULL_N_MINUS_ONE_ORDER_CERTIFICATE":
        raise ValueError("Lucas order certificate required")
    if q==2:
        if witness!=1 or factors: raise ValueError("invalid base-prime certificate")
        return True
    seen=set();value=1
    for factor in factors:
        p=integer(factor["prime"],"factor prime",2);e=integer(factor["exponent"],"factor exponent",1)
        if p>=q or p in seen or factor["certificate"]["prime"]!=p:
            raise ValueError("distinct bound prime factors required")
        seen.add(p);validate_prime_record(factor["certificate"]);value*=p**e
    if value!=q-1 or not 1<witness<q or pow(witness,q-1,q)!=1 or any(
            gcd(pow(witness,(q-1)//p,q)-1,q)!=1 for p in seen):
        raise ValueError("invalid prime order certificate")
    return True


@dataclass(frozen=True)
class PublicQaryLattice:
    prime: int
    H: tuple

    def __post_init__(self):
        integer(self.prime,"odd prime",3)
        certificate=prime_certificate(self.prime)
        H=tuple(tuple(row) for row in self.H)
        m=len(H)
        n=len(H[0]) if m else 0
        if not 1<=m<n-1 or any(len(row)!=n for row in H):
            raise ValueError("full row rank rectangular kernel with m<n-1 required")
        for row in H:
            for x in row:
                integer(x,"canonical field entry")
                if x>=self.prime:
                    raise ValueError("canonical modular matrix required")
        rref,rank=fmpz_mod_mat(H,fmpz_mod_ctx(self.prime)).rref()
        if rank!=m:
            raise ValueError("full row rank public matrix required")
        reduced=tuple(tuple(int(rref[i,j]) for j in range(n)) for i in range(m))
        pivots=tuple(next(j for j,x in enumerate(row) if x) for row in reduced)
        free=tuple(j for j in range(n) if j not in pivots)
        basis=[]
        for pivot in pivots:
            row=[0]*n;row[pivot]=self.prime;basis.append(tuple(row))
        for column in free:
            row=[0]*n;row[column]=1
            for i,pivot in enumerate(pivots):
                c=reduced[i][column]
                c=c-self.prime if c>self.prime//2 else c
                row[pivot]=-c
            basis.append(tuple(row))
        basis=tuple(basis)
        if abs(int(fmpz_mat(basis).det()))!=self.prime**m:
            raise ArithmeticError("public kernel basis index mismatch")
        object.__setattr__(self,"H",H)
        object.__setattr__(self,"rref",reduced)
        object.__setattr__(self,"pivots",pivots)
        object.__setattr__(self,"free",free)
        object.__setattr__(self,"basis",basis)
        object.__setattr__(self,"prime_certificate",certificate)
        if any(not self.member(row) for row in basis):
            raise ArithmeticError("basis row is not in public modular kernel")

    @property
    def dimension(self): return len(self.H[0])

    @property
    def rows(self): return len(self.H)

    def member(self,v):
        v=tuple(v)
        if len(v)!=self.dimension or any(type(x) is not int for x in v):
            raise ValueError("exact full ambient integer vector required")
        return all(sum(a*x for a,x in zip(row,v))%self.prime==0 for row in self.H)

    def public_record(self):
        payload={"prime":self.prime,"dimension":self.dimension,"constraint_rows":self.rows,
                 "H":self.H,"row_basis":self.basis,"public_modular_rref":self.rref,
                 "pivot_columns":self.pivots,"free_columns":self.free,
                 "lattice_index":{"prime":self.prime,"exponent":self.rows},
                 "prime_certificate":self.prime_certificate.record(),
                 "solver_input_contains_plant_seed_or_solution":False}
        payload["public_problem_sha256"]=hashlib.sha256(json.dumps(exact_json(payload),sort_keys=True,separators=(",",":")).encode()).hexdigest()
        return payload


def rank_probability_factors(n,m,q):
    for value,name,lower in ((n,"dimension",3),(m,"rows",1),(q,"odd prime",3)):
        integer(value,name,lower)
    if not m<n-1 or not isprime(q):
        raise ValueError("rank lower bound needs odd prime and m<n-1")
    prime_certificate(q)
    return {"prime":q,"orthogonal_space_dimension":n-1,
            "failure_exponents":tuple(n-1-i for i in range(m)),
            "exact_full_rank_probability":"PRODUCT(1-q^(-exponent))",
            "uniform_certified_rank_probability_lower":"5/6"}


def uniqueness_ledger(n,m,q,radius,gap,support):
    for x,name,minimum in ((n,"dimension",3),(m,"rows",1),(q,"prime",3),(radius,"radius",1),(gap,"gap",2),(support,"support",1)):
        integer(x,name,minimum)
    if not m<n-1 or support>n or not isprime(q):
        raise ValueError("valid primitive ternary source/rank parameters required")
    factors=rank_probability_factors(n,m,q)
    valid=2*radius<q and radius*radius>=gap*gap*support
    count_bound=lattice_ball_count_bound(n,radius)
    base=count_bound["selected_count_base"]
    numerator=6*base**n
    denominator=5*q**m
    k=0
    if valid and numerator<=denominator:
        k=max(0,denominator.bit_length()-numerator.bit_length())
        while numerator*(1<<k)>denominator: k-=1
        while numerator*(1<<(k+1))<=denominator: k+=1
    return {"dimension":n,"constraint_rows":m,"prime":q,"radius":radius,"promised_relative_gap":gap,
            "PRIVATE_AUDIT_ONLY_plant_support":support,"rank_conditioning":factors,
            "integer_ball_count_bound":count_bound,
            "radius_strictly_below_q_over2":2*radius<q,
            "radius_covers_gap_times_plant_norm":radius*radius>=gap*gap*support,
            "status":"DISTRIBUTIONAL_UNIQUENESS_BOUND" if valid else "UNKNOWN_UNIQUENESS_SCOPE",
            "conditional_failure_bound_factors":{"numerator_multiplier":6,"denominator_multiplier":5,
                "count_base":base,"count_exponent":n,"prime":q,"prime_exponent":m},
            "conditional_failure_upper_dyadic":None if not valid else {"base":2,"negative_exponent":k},
            "bound_is_nonvacuous":valid and numerator<denominator,
            "individual_instance_uniqueness_certified":False,"computational_hardness_proved":False,
            "rank_conditioned_rows_assumed_IID_unconditioned":False,
            "probability_bound_assumes_ideal_independent_uniform_rows":True,
            "seeded_PRNG_fixture_is_not_a_formal_IID_sampler":True}


@dataclass(frozen=True)
class PrivatePlantAudit:
    plant: tuple
    plant_seed: int
    matrix_seed: int
    attempted_matrices: tuple
    ledger: dict


@dataclass(frozen=True)
class GeneratedQarySource:
    problem: PublicQaryLattice
    private: PrivatePlantAudit


def generate_source(n,m=None,q=None,gap=None,support=None,*,plant_seed=0,matrix_seed=1,max_attempts=32,failure_bits=16):
    integer(n,"dimension",4)
    m=n//2 if m is None else integer(m,"rows",1)
    support=n if support is None else integer(support,"dense support",1)
    gap=n**3 if gap is None else integer(gap,"relative gap",2)
    if not 1<=m<n-1 or not (n+2)//3<=support<=n:
        raise ValueError("valid dense primitive ternary/full-rank family required")
    radius=ceil_sqrt(gap*gap*support)
    if q is None:
        q,prime_choice=select_prime(n,m,radius,failure_bits)
    else:
        q=integer(q,"odd prime",3)
        prime_choice={"selected_prime":q,"explicit_prime_supplied":True,
                      "chosen_before_classical_attack_outcomes":True}
    integer(max_attempts,"rank attempt cap",1)
    if not 1<=m<n-1 or not (n+2)//3<=support<=n or not isprime(q):
        raise ValueError("valid dense primitive ternary/full-rank family required")
    for seed in (plant_seed,matrix_seed): integer(seed,"private reproducibility seed")
    rng=random.Random(plant_seed)
    locations=rng.sample(range(n),support)
    plant=[0]*n
    for i in locations: plant[i]=rng.choice((-1,1))
    pivot=locations[0]
    matrix_rng=random.Random(matrix_seed)
    attempts=[]
    for attempt in range(max_attempts):
        H=[]
        for _ in range(m):
            row=[matrix_rng.randrange(q) for _ in range(n)]
            row[pivot]=(-sum(row[i]*plant[i] for i in range(n) if i!=pivot)*plant[pivot])%q
            H.append(tuple(row))
        H=tuple(H)
        rank=int(fmpz_mod_mat(H,fmpz_mod_ctx(q)).rank())
        attempts.append({"H":H,"rank":rank,"accepted_full_row_rank":rank==m})
        if rank==m:
            problem=PublicQaryLattice(q,H)
            ledger=uniqueness_ledger(n,m,q,radius,gap,support)
            ledger["prime_selection"]=prime_choice
            ledger["rank_attempt_cap"]=max_attempts
            ledger["actual_rank_sampling_attempts"]=attempt+1
            ledger["rank_sampling_abort_probability_upper"]={"base":6,"negative_exponent":max_attempts}
            ledger["generator_rejects_on_classical_attack_or_uniqueness_outcome"]=False
            if not problem.member(tuple(plant)):
                raise ArithmeticError("planted vector not in public kernel")
            return GeneratedQarySource(problem,PrivatePlantAudit(tuple(plant),plant_seed,matrix_seed,tuple(attempts),ledger))
    raise ValueError("UNKNOWN_GENERATOR_RANK_CAP; no hardness or source-failure conclusion")


def checked_public(problem):
    if not isinstance(problem,PublicQaryLattice):
        raise ValueError("public lattice only; private generator records are not solver inputs")
    return problem


def checked_private(generated):
    if not isinstance(generated,GeneratedQarySource): raise ValueError("private calibration context required")
    p,a=generated.problem,generated.private
    if not any(a.plant) or any(type(x) is not int or x not in (-1,0,1) for x in a.plant) or not p.member(a.plant):
        raise ValueError("private plant must be a primitive ternary lattice member")
    if (a.ledger["dimension"],a.ledger["constraint_rows"],a.ledger["prime"])!=(p.dimension,p.rows,p.prime):
        raise ValueError("private radius ledger is not bound to public problem")
    if a.ledger["PRIVATE_AUDIT_ONLY_plant_support"]!=norm_squared(a.plant):
        raise ValueError("private support ledger does not match plant")
    integer(a.ledger["radius"],"private audit radius",1)
    integer(a.ledger["promised_relative_gap"],"private audit gap",2)
    if a.ledger["radius"]**2<a.ledger["promised_relative_gap"]**2*norm_squared(a.plant):
        raise ValueError("radius does not cover promised uniqueness gap")
    return p,a


def sparse_column_attack(problem):
    problem=checked_public(problem)
    n,m,q=problem.dimension,problem.rows,problem.prime
    columns=[tuple(problem.H[i][j] for i in range(m)) for j in range(n)]
    seen={}
    checked=0
    for j,column in enumerate(columns):
        checked+=m
        if not any(column):
            v=tuple(int(i==j) for i in range(n))
            return {"status":"RECOVERED_PUBLIC_SPARSE_KERNEL_VECTOR","vector":v,"squared_norm":1,"modular_entries_processed":checked}
        for sign in (1,-1):
            key=tuple((sign*x)%q for x in column)
            if key in seen:
                i=seen[key];v=[0]*n;v[i]=1;v[j]=-sign
                return {"status":"RECOVERED_PUBLIC_SPARSE_KERNEL_VECTOR","vector":canonical_sign(v),
                        "squared_norm":2,"modular_entries_processed":checked}
        seen[column]=j
    return {"status":"NO_UNIT_OR_COLUMN_PAIR_RELATION","vector":None,"squared_norm":None,
            "modular_entries_processed":checked,"absence_proves_hardness":False}


def public_LLL_attack(problem):
    problem=checked_public(problem)
    start=time.perf_counter()
    B=fmpz_mat(problem.basis)
    reduced,transform=B.lll(transform=True,gram="exact")
    if transform*B!=reduced or abs(int(transform.det()))!=1:
        raise ArithmeticError("LLL public unimodular transformation failed")
    rows=matrix_rows(reduced)
    if any(not problem.member(row) for row in rows):
        raise ArithmeticError("LLL returned an invalid kernel vector")
    vector=canonical_sign(min(rows,key=lambda r:(norm_squared(r),r)))
    return {"status":"RECOVERED_PUBLIC_REDUCED_ROW","vector":vector,"squared_norm":norm_squared(vector),
            "reduced_row_basis":rows,"unimodular_row_transform":matrix_rows(transform),
            "library":"FLINT fmpz_mat.lll with exact Gram mode",
            "elapsed_seconds":time.perf_counter()-start,
            "input_basis_rows":problem.dimension,"input_basis_entries":problem.dimension**2,
            "delta_squared_power_factors":{"row_squared_norm":norm_squared(vector),"norm_exponent":problem.dimension,
                "determinant_prime":problem.prime,"determinant_exponent":2*problem.rows},
            "empirical_quality_is_a_general_LLL_guarantee":False,
            "plant_or_private_seed_used":False}


def ternary_MITM_attack(problem,max_states=20000):
    problem=checked_public(problem)
    integer(max_states,"complete MITM state cap",1)
    n,m,q=problem.dimension,problem.rows,problem.prime
    split=n//2
    states=3**split+3**(n-split)
    if states>max_states:
        return {"status":"UNKNOWN_COMPLETE_MITM_CAP","vector":None,"squared_norm":None,
                "required_complete_half_states":states,"max_states":max_states,"cap_failure_proves_hardness":False}
    start=time.perf_counter()
    left={}
    for v in product((-1,0,1),repeat=split):
        key=tuple(sum(a*x for a,x in zip(row[:split],v))%q for row in problem.H)
        bucket=left.setdefault(key,[]);bucket.append((norm_squared(v),v));bucket.sort();del bucket[2:]
    best=None
    for v in product((-1,0,1),repeat=n-split):
        key=tuple(-sum(a*x for a,x in zip(row[split:],v))%q for row in problem.H)
        for left_norm,u in left.get(key,()):
            candidate=u+v
            if not any(candidate): continue
            value=(left_norm+norm_squared(v),canonical_sign(candidate))
            if best is None or value<best: best=value
    vector=None if best is None else best[1]
    if vector is not None and not problem.member(vector):
        raise ArithmeticError("MITM collision is not a kernel vector")
    return {"status":"RECOVERED_MINIMUM_TERNARY_KERNEL_VECTOR" if best else "NO_TERNARY_VECTOR_IN_COMPLETE_SEARCH",
            "vector":vector,"squared_norm":None if best is None else best[0],
            "complete_half_states_processed":states,"maximum_retained_vectors_per_syndrome":2,
            "modular_dot_product_terms":m*(split*3**split+(n-split)*3**(n-split)),
            "elapsed_seconds":time.perf_counter()-start,"family_low_alphabet_prior_exploited":True,
            "plant_or_private_seed_used":False,"failure_proves_hardness":False}


def complete_radius_audit(generated,max_states=200000):
    p,a=checked_private(generated)
    integer(max_states,"complete radius state cap",1)
    R=a.ledger["radius"];states=(2*R+1)**p.dimension
    if states>max_states:
        return {"status":"UNKNOWN_COMPLETE_RADIUS_CAP","required_box_states":states,
                "individual_uniqueness_certified":False,"truncated_search_certifies_absence":False}
    pivot=next(i for i,x in enumerate(a.plant) if x)
    failures=[];checked=0
    for v in product(range(-R,R+1),repeat=p.dimension):
        if norm_squared(v)>R*R: continue
        checked+=1
        if p.member(v):
            factor=v[pivot]*a.plant[pivot]
            if any(x!=factor*u for x,u in zip(v,a.plant)): failures.append(v)
    return {"status":"COMPLETE_FINITE_RADIUS_CENSUS","complete_box_states":states,
            "sphere_points_checked":checked,"PRIVATE_AUDIT_ONLY_nonparallel_kernel_vectors":tuple(failures),
            "individual_uniqueness_certified":not failures,
            "growing_family_hardness_or_quantum_advantage_certified":False}


def audit_attacks(generated,attacks):
    p,a=checked_private(generated)
    plant=canonical_sign(a.plant)
    outcomes=[]
    for name,attack in attacks.items():
        v=attack.get("vector")
        if v is not None and (not any(v) or not p.member(v)):
            raise ValueError("an invalid/zero attack output is not a source falsifier")
        # Integer gcd division is legal only if the public kernel confirms it.
        if v is not None:
            divisor=gcd(*v)
            primitive=tuple(x//divisor for x in v)
            if p.member(primitive): v=primitive
        success=v is not None and canonical_sign(v)==plant
        pivot=next(i for i,x in enumerate(plant) if x)
        nonparallel=v is not None and any(x!=(v[pivot]*plant[pivot])*u for x,u in zip(v,plant))
        false_instance=nonparallel and norm_squared(v)<=a.ledger["radius"]**2
        outcomes.append({"attack":name,"planted_direction_recovered_up_to_sign":success,
                         "private_uniqueness_event_falsified_for_this_instance":false_instance,
                         "public_membership_checked_normalized_vector":v})
    recovered=any(o["planted_direction_recovered_up_to_sign"] for o in outcomes)
    return {"PRIVATE_AUDIT_ONLY_attack_calibrations":tuple(outcomes),
            "tested_instance_classically_recovers_planted_direction":recovered,
            "research_decision":"FINITE_REGIME_CLASSICALLY_RECOVERED_NO_QUANTUM_SIGNAL" if recovered else "UNRESOLVED_IMPLEMENTED_ATTACKS_NOT_HARDNESS",
            "full_unique_SVP_or_all_classical_algorithms_ruled_out":False}


def build_report():
    controls=[]
    params=((4,2,257,2,4),(8,4,None,None,8),(12,6,None,None,12),(16,8,None,None,16),(32,16,None,None,32),
            (8,4,int(nextprime(2**80)),None,8),(64,32,None,None,64),(128,64,None,None,128))
    for i,(n,m,q,gap,support) in enumerate(params):
        g=generate_source(n,m,q,gap,support,plant_seed=99600+i,matrix_seed=99700+i)
        attacks={"sparse_columns":sparse_column_attack(g.problem),"public_LLL":public_LLL_attack(g.problem),
                 "complete_ternary_MITM":ternary_MITM_attack(g.problem)}
        controls.append({"public_problem":g.problem.public_record(),
            "PRIVATE_AUDIT_ONLY_generation":{"plant":g.private.plant,"plant_seed":g.private.plant_seed,
                "matrix_seed":g.private.matrix_seed,"attempted_matrices":g.private.attempted_matrices},
            "distributional_uniqueness_ledger":g.private.ledger,"public_classical_attacks":attacks,
            "matched_attack_calibration":audit_attacks(g,attacks),"complete_radius_audit":complete_radius_audit(g),
            "BKZ_status":"NOT_RUN_DEPENDENCY_FPYLLL_UNAVAILABLE",
            "MILP_and_general_SIS_search_status":"NOT_IMPLEMENTED_NOT_A_NEGATIVE_RESULT",
            "quantum_source_or_receiver_has_been_benchmarked":False})
    return {"status":"PLANTED_QARY_USVP_PUBLIC_SOURCE_AND_CLASSICAL_FALSIFICATION_REVIEW_PENDING",
            "producer_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "derivation_sha256":hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "contract_sha256":hashlib.sha256(CONTRACT.read_bytes()).hexdigest(),
            "source_controls":tuple(controls),"accepted_speedup_candidate":False,
            "source_distribution_is_proved_computationally_hard":False,
            "new_active_negative_result_created":False,"novelty_claim":False}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write",action="store_true")
    args=parser.parse_args();report=build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True,exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report),indent=2)+"\n")
    print(json.dumps({"status":report["status"],"source_controls":len(report["source_controls"]),
        "classically_recovered_controls":sum(c["matched_attack_calibration"]["tested_instance_classically_recovers_planted_direction"] for c in report["source_controls"]),
        "accepted_speedup_candidate":False},indent=2))


if __name__=="__main__": main()
