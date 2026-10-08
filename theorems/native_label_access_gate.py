"""Collective weak-trit gate for prefix-only quantum label access.

LOCAL DERIVATION / REVIEW PENDING. Full labels are free to the final classical
decoder. This is a copy/access tradeoff, not a polynomial-copy impossibility.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import product
import json
import math
from pathlib import Path
import random

from flint import fmpq, fmpq_poly
import numpy as np

from native_partial_phase_echo import EchoFamily
from ternary_covariant_noise import _integer, _word, root_digits

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/classical_baselines/native_label_access_gate.json"


def label_access_ledger(n,r,copies,read_digits,desired_advantage=Fraction(1,10)):
    for value,name,minimum in ((n,"dimension",1),(r,"root digits",1),(copies,"charged native copies",0),
                               (read_digits,"low label digits read by quantum control",0)):
        _integer(value,name,minimum)
    if read_digits>=r:
        raise ValueError("at least one unread label digit required; full quantum label access is outside this gate")
    if isinstance(desired_advantage,(float,bool)):
        raise ValueError("exact rational desired advantage required")
    eps=Fraction(desired_advantage)
    if not 0<=eps<=Fraction(2,3):
        raise ValueError("least-trit advantage is in [0,2/3]")
    V=n*(r-read_digits)
    denominator=3**(copies+V)
    variance_numerator=5**copies-3**copies
    rare_numerator=3**copies-1
    gap=eps.numerator*denominator-eps.denominator*rare_numerator
    possible=gap<=0 or variance_numerator*eps.denominator**2*denominator>=gap*gap
    if not copies:
        approximation=0.
    else:
        log_variance=copies*math.log(5/3)-V*math.log(3)+math.log1p(-(3/5)**copies)
        approximation=min(2/3,math.exp(min(log_variance/2,1))+math.exp(-V*math.log(3))*(-math.expm1(-copies*math.log(3))))
    return {"dimension":n,"root_digits":r,"original_even_native_level":2*r,
            "charged_native_copies":copies,"quantum_low_label_digits":read_digits,
            "unread_label_digits":r-read_digits,"nonzero_residue_covariance_block_size":{"coefficient":2,"base":3,"exponent":n*read_digits},
            "kernel_secret_prior_mass":{"base":3,"exponent":-V},
            "least_trit_advantage_upper":{"cap":"2/3",
                "nonkernel_squared":{"numerator":{"positive_base":5,"negative_base":3,"exponent":copies},"denominator":{"base":3,"exponent":copies+V}},
                "kernel_term":{"numerator":{"base":3,"exponent":copies,"subtract":1},"denominator":{"base":3,"exponent":copies+V}}},
            "approximate_advantage_upper_NOT_authoritative":approximation,
            "numerical_underflow_is_NOT_an_exact_zero_bound":True,
            "desired_advantage_exact":str(eps),"necessary_copy_access_gate_passed":possible,
            "arbitrary_collective_POVMs_and_outcome_feedback_covered":True,
            "unlimited_full_label_FINAL_classical_decoding_covered":True,
            "higher_label_digits_in_quantum_control_covered":False,
            "filtered_full_label_or_nonIID_source_covered":False,
            "all_polynomial_copy_receivers_ruled_out":False,
            "speedup_or_candidate_acceptance_allowed":False}


class CertificateField:
    """Finite Q(zeta_q) controls using FLINT's rational polynomial quotient."""
    def __init__(self,q):
        root_digits(q)
        if q>81:
            raise ValueError("finite certificate field capped at q81, not a scalable cyclotomic-field oracle")
        self.q=q
        coefficients=[0]*(2*q//3+1)
        for i in (0,q//3,2*q//3):
            coefficients[i]=1
        self.modulus=fmpq_poly(coefficients)
        self.zero=fmpq_poly([])
        self.one=fmpq_poly([1])
        z=fmpq_poly([0,1])
        self.roots=tuple(z**i % self.modulus for i in range(q))

    def times(self,a,b):
        return a*b % self.modulus

    def scale(self,a,value):
        value=Fraction(value)
        return a*fmpq(value.numerator,value.denominator)

    def conjugate(self,a):
        return sum((self.roots[-i % self.q]*c for i,c in enumerate(a)),self.zero)

    def encode(self,a):
        return [str(x) for x in reversed(list(a))]

    def rational(self,a):
        if len(a)>1:
            raise ArithmeticError("this finite control scalar is not certified rational")
        return Fraction(int(a[0].numerator),int(a[0].denominator)) if len(a) else Fraction()

    def number(self,a):
        return sum(float(c)*np.exp(2j*np.pi*i/self.q) for i,c in enumerate(a))


def collective_effects(field,name,lows):
    """Explicit positive rank-one factors; some effects have rank three."""
    D=9
    if name=="bell" or name=="coarse_bell":
        factors=[]
        for z in range(3):
            group=[]
            for p in range(3):
                vector=[field.zero for _ in range(D)]
                for j in range(3):
                    vector[3*j+(j+p) % 3]=field.roots[(field.q//3*z*j) % field.q]
                term=(Fraction(1,3),tuple(vector))
                if name=="bell":
                    factors.append((term,))
                else:
                    group.append(term)
            if name=="coarse_bell":
                factors.append(tuple(group))
    elif name in ("real_entangled","low_controlled_entangled","higher_prefix_entangled"):
        kappa=sum(sum(row) for pair in lows for row in pair) % 3 if name.startswith("low_") else (
            sum(x//3 for pair in lows for row in pair for x in row) % 3 if name.startswith("higher_") else 0)
        factors=[]
        for j in range(D):
            vector=tuple(field.scale(field.roots[(field.q//3*kappa*(i//3)*(i%3)) % field.q],Fraction(int(i==j))-Fraction(2,D)) for i in range(D))
            factors.append(((Fraction(1),vector),))
    elif name=="flat_real_product":
        signs=((1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1))
        factors=[((Fraction(1,16),tuple(field.scale(field.one,a*b) for a in left for b in right)),) for left,right in product(signs,repeat=2)]
    elif name=="adaptive_second_basis":
        factors=[]
        for z,j in product(range(3),repeat=2):
            left=tuple(field.roots[(field.q//3*z*i) % field.q] for i in range(3))
            if z==1:
                right=tuple(field.roots[(field.q//3*j*i) % field.q] for i in range(3))
                weight=Fraction(1,9)
            else:
                right=tuple(field.scale(field.one,Fraction(int(i==j))-Fraction(2,3)) for i in range(3))
                weight=Fraction(1,3)
            factors.append(((weight,tuple(field.times(a,b) for a in left for b in right)),))
    else:
        raise ValueError("named certified two-copy collective control required")
    effects=[]
    for terms in factors:
        effect=[[field.zero for _ in range(D)] for _ in range(D)]
        for weight,vector in terms:
            if weight<=0:
                raise ValueError("positive factor weights required")
            for i,j in product(range(D),repeat=2):
                effect[i][j]+=field.scale(field.times(vector[i],field.conjugate(vector[j])),weight)
        effects.append(effect)
    if any(sum((e[i][j] for e in effects),field.zero)!=(field.one if i==j else field.zero) for i,j in product(range(D),repeat=2)):
        raise ArithmeticError("factored PSD effects do not sum to identity")
    return tuple(effects),tuple(factors)


def conditional_gram_control(q,n,read_digits,name,first_low,second_low,census_budget=10000):
    r=root_digits(q)
    if not 0<=read_digits<r or n<1:
        raise ValueError("nontrivial unread high label modulus required")
    b=3**read_digits
    first_low=tuple(_word(row,b,"first low row",n) for row in first_low)
    second_low=tuple(_word(row,b,"second low row",n) for row in second_low)
    if len(first_low)!=2 or len(second_low)!=2:
        raise ValueError("finite exact collective controls use two original inputs")
    Q=q//b
    field=CertificateField(q)
    effects,factors=collective_effects(field,name,(first_low,second_low))
    words=tuple(product(range(3),repeat=2))
    secrets=tuple(product(range(q),repeat=n))
    if len(secrets)>81:
        raise ValueError("complete finite secret Gram exceeds81 hypotheses")
    retained=tuple(s for s in secrets if any(x % Q for x in s))
    reference=tuple(field.rational(sum((e[i][i] for i in range(9)),field.zero))/9 for e in effects)
    if any(x<=0 for x in reference) or sum(reference)!=1:
        raise ArithmeticError("positive complete measurement reference required")
    simplex=((0,0),(1,0),(0,1))
    low=lambda w:tuple(sum((first_low[i][l] if j==1 else second_low[i][l] if j==2 else 0) for i,j in enumerate(w)) for l in range(n))
    features=tuple(tuple(z for j in w for z in simplex[j]) for w in words)
    lows=tuple(low(w) for w in words)
    buckets=[]
    for e in effects:
        rows=[]
        for s in retained:
            row={}
            for i,j in product(range(9),repeat=2):
                if i==j or not e[j][i]:
                    continue
                key=tuple((features[i][a]-features[j][a])*v % Q for a in range(4) for v in s)
                exponent=sum(v*(x-y) for v,x,y in zip(s,lows[i],lows[j])) % q
                coefficient=field.scale(field.times(e[j][i],field.roots[exponent]),Fraction(1,9))
                row[key]=row.get(key,field.zero)+coefficient
            rows.append({key:value for key,value in row.items() if value})
        buckets.append(rows)
    gram=[]
    for i,s in enumerate(retained):
        row=[]
        for j,t in enumerate(retained):
            value=field.zero
            for rows,mass in zip(buckets,reference):
                value+=field.scale(sum((field.times(rows[i][key],field.conjugate(rows[j][key])) for key in rows[i].keys() & rows[j].keys()),field.zero),1/mass)
            if value!=field.conjugate(value):
                raise ArithmeticError("Born covariance is not a real scalar")
            allowed=tuple(x % Q for x in s) in (tuple(x % Q for x in t),tuple(-x % Q for x in t))
            if not allowed and value:
                raise ArithmeticError("covariance escaped the secret residue/sign block")
            row.append(value)
        gram.append(row)
    exact=tuple(tuple(field.rational(x) for x in row) for row in gram)
    variance=Fraction(5,3)**2-1
    if any(exact[i][i]>variance for i in range(len(retained))):
        raise ArithmeticError("collective covariance violates tensor fourth-moment bound")
    row_sum=max(sum(abs(x) for x in row) for row in exact)
    if row_sum>2*b**n*variance:
        raise ArithmeticError("finite collective Gram exceeds residue-block operator bound")
    control={"modulus":q,"dimension":n,"original_native_copies":2,"quantum_low_label_digits":read_digits,
             "fixed_first_low_rows":first_low,"fixed_second_low_rows":second_low,"measurement":name,
             "positive_effect_factors":[[{"positive_weight":str(weight),"vector":[field.encode(x) for x in vector]} for weight,vector in terms] for terms in factors],
             "effects":[[[field.encode(x) for x in row] for row in e] for e in effects],
             "reference_outcome_masses_exact":[str(x) for x in reference],
             "ALL_nonzero_high_residue_secrets":retained,
             "high_kernel_secret_count":b**n,"high_residue_sign_block_size_upper":2*b**n,
             "full_nonkernel_centered_Gram_exact_rationals":[[str(x) for x in row] for row in exact],
             "maximum_absolute_Gram_row_sum_exact":str(row_sum),
             "universal_nonkernel_operator_bound_exact":str(2*b**n*variance),
             "kernel_secret_removal_is_charged_in_gate_NOT_postselection":True,
             "conditional_high_lift_census_size":Q**(4*n),
             "conditional_high_lift_census_performed":Q**(4*n)<=census_budget}
    if control["conditional_high_lift_census_performed"]:
        numeric=np.array([[[field.number(x) for x in row] for row in e] for e in effects])
        actual=np.zeros((len(retained),len(retained)))
        actual_trit=0.
        complete=Q**(4*n)
        all_secrets=np.array(secrets)
        retained_indices=[secrets.index(s) for s in retained]
        for high in product(range(Q),repeat=4*n):
            first=[tuple(first_low[i][l]+b*high[i*n+l] for l in range(n)) for i in range(2)]
            second=[tuple(second_low[i][l]+b*high[(2+i)*n+l] for l in range(n)) for i in range(2)]
            frequency=np.array([tuple(sum((first[i][l] if j==1 else second[i][l] if j==2 else 0) for i,j in enumerate(w)) for l in range(n)) for w in words])
            state=np.exp(2j*np.pi*((all_secrets@frequency.T) % q)/q)/3
            born=np.einsum("si,yij,sj->sy",state.conj(),numeric,state).real
            relative=born[retained_indices]/np.array(reference,dtype=float)-1
            actual+=(relative*np.array(reference,dtype=float))@relative.T/complete
            grouped=np.array([born[all_secrets[:,0] % 3==t].sum(axis=0) for t in range(3)])
            actual_trit+=float(grouped.max(axis=0).sum()/(len(secrets)*complete))
        residual=float(np.max(abs(actual-np.array(exact,dtype=float))))
        if residual>3e-11:
            raise ArithmeticError("full original high-lift Born census contradicts exact character Gram")
        control.update({"full_conditional_Born_Gram_error":residual,
                        "all_secret_least_trit_MAP_including_kernel_numeric":actual_trit,
                        "decoded_using_all_full_labels_and_exponential_secret_enumeration":True})
    return control


def information_only_escape(r,seed):
    q=3**r
    rng=random.Random(seed)
    first=tuple((rng.randrange(q),) for _ in range(r))
    second=tuple((rng.randrange(q),) for _ in range(r))
    family=EchoFamily(first,second,q,1,((0,),))
    counts={}
    for w in product(range(3),repeat=r):
        y=family.frequency(w)[0]
        counts[y]=counts.get(y,0)+1
    by_residue={}
    for y,c in counts.items():
        by_residue[y % (q//3)]=by_residue.get(y % (q//3),0.)+math.sqrt(c)
    least=sum(x*x for x in by_residue.values())/(3*3**r)
    blind=label_access_ledger(1,r,r,0)["approximate_advantage_upper_NOT_authoritative"]+1/3
    return {"root_digits":r,"modulus":q,"original_native_copies":r,"source_seed":seed,
            "first_frequencies":first,"second_frequencies":second,"fiber_counts":[[y,c] for y,c in sorted(counts.items())],
            "dense_FULL_label_PGM_least_trit_success_information_only":least,
            "blind_collective_POPULATION_upper_numeric":blind,
            "conditional_cohort_is_NOT_a_population_bound_violation":True,
            "cube_words_enumerated":3**r,"efficient_PGM_compiler_or_fiber_oracle_supplied":False,
            "new_algorithm_or_speedup_claimed":False}


def run_controls():
    cases=[(3,1,0,"bell",((0,),(0,)),((0,),(0,))),
           (9,1,0,"real_entangled",((0,),(0,)),((0,),(0,))),
           (9,1,1,"low_controlled_entangled",((1,),(2,)),((2,),(2,))),
           (9,1,1,"coarse_bell",((1,),(0,)),((2,),(1,))),
           (27,1,1,"low_controlled_entangled",((2,),(1,)),((1,),(1,))),
           (3,2,0,"flat_real_product",((0,0),(0,0)),((0,0),(0,0))),
           (9,1,0,"adaptive_second_basis",((0,),(0,)),((0,),(0,))),
           (27,1,2,"higher_prefix_entangled",((3,),(0,)),((0,),(0,))),
           (81,1,0,"bell",((0,),(0,)),((0,),(0,)))]
    return {"status":"NATIVE_COLLECTIVE_PREFIX_LABEL_ACCESS_WEAK_TRIT_GATE_REVIEW_PENDING",
            "exact_collective_POVM_controls":[conditional_gram_control(*case) for case in cases],
            "scaling_ledgers":[label_access_ledger(n,r,M,ell) for n,r,M,ell in
                ((8,8,64,0),(8,8,64,1),(8,8,64,4),(8,8,64,5),(64,2,128,1),(128,2,256,1),
                 (32,32,1024,16),(32,32,1024,20),(128,128,16384,64),(128,128,16384,100))],
            "full_label_information_only_escapes":[information_only_escape(r,seed) for r in (4,5,6) for seed in (70321,70322,70323)],
            "single_site_fourth_moment_SOS":{
                "factor":"5/3","gap_monomials":["a^2","b^2","c^2","ab","ac","bc"],
                "gap_coefficients":["2/3","2/3","2/3","-2/3","-2/3","-2/3"],
                "positive_squared_terms":[{"weight":"1/3","difference":pair} for pair in (("a","b"),("a","c"),("b","c"))]},
            "unread_digit_residue_covariance_blocks_are_kept":True,
            "arbitrary_collective_measurements_WITH_LOW_PREFIX_control_covered":True,
            "full_frequency_classical_decoding_is_allowed":True,
            "full_label_quantum_measurements_or_all_polynomial_copies_ruled_out":False,
            "new_speedup_claimed":False,"novelty_claimed":False,"candidate_accepted":False}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write",action="store_true")
    args=parser.parse_args()
    out=run_controls()
    if args.write:
        REPORT.write_text(json.dumps(out,indent=2,allow_nan=False)+"\n")
    print(json.dumps({"status":out["status"],"exact_collective_controls":len(out["exact_collective_POVM_controls"]),
                      "copy_access_ledgers":len(out["scaling_ledgers"]),"new_algorithm":False}))


if __name__=="__main__":
    main()
