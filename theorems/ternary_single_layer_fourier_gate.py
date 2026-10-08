"""Native offset-energy obstruction for ONE word-diagonal/Fourier layer.

LOCAL DERIVATION / REVIEW PENDING. Collective full-label phases are allowed;
multiple layers, pre-Fourier permutations and other source laws are not.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
from collections import Counter
from itertools import product
import json
from math import comb
from pathlib import Path

import numpy as np

from cyclotomic_fiber_receiver import inverse_frequency_coordinates, native_source
from ternary_covariant_noise import root_digits
from ternary_cyclic_extractor import random_even_source

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/classical_baselines/ternary_single_layer_fourier_gate.json"
DERIVATION=ROOT/"research/TERNARY_SINGLE_LAYER_FOURIER_GATE.md"
MACROS=("zero","total_quadratic","partial_quadratic","cross_quadratic","top_digit","word_label_coupled")
TRANSITIONS=(((1,0),(-1,1),(0,-1)),((0,1),(-1,0),(1,-1)))


def integer(x,name,minimum=1):
    if type(x) is not int or x<minimum:raise ValueError(f"{name} must be an integer >= {minimum}")
    return x


def population_certificate(n,r,M=None):
    integer(n,"dimension");integer(r,"root digits")
    M=n*r-2 if M is None else M;integer(M,"original source qutrits")
    D=3**M;G=3**(n*r);A=Fraction(5,3)**M
    moments=[{"support":k,"offsets":str(comb(M,k)*2**k),
              "second_moment_per_oriented_high_class":str(Fraction(D*D,3**k*G)+Fraction(D*D*(3**k-1),3**k*G*G))}
             for k in range(1,M+1)]
    expected=2*D*D*((A-1)/G+(D-A)/(G*G))
    if expected!=2*sum(int(row["offsets"])*Fraction(row["second_moment_per_oriented_high_class"]) for row in moments):
        raise ArithmeticError("support sum and closed population moment disagree")
    squared=min(Fraction(4,9),2*expected/(9*D*D))
    return {"dimension":n,"root_digits":r,"original_qutrits":M,"native_words":str(D),"secret_group_size":str(G),
            "support_moments":moments,"expected_phase_independent_offset_energy":str(expected),
            "mean_raw_trit_advantage_upper_squared":str(squared),
            "label_dependent_collective_initial_diagonal_covered":True,
            "all_classical_postprocessing_covered":True,"uniform_full_secret_prior_required":True,
            "word_Fourier_readout_fixed":True,"IID_original_full_native_frequency_rows_required":True,
            "earlier_noncommuting_mixing_or_word_permutation_covered":False,
            "label_independent_word_permutations_covered":True,
            "label_dependent_invertible_affine_word_maps_covered":True,
            "generic_quantum_lower_bound":False,"large_word_space_executed":False,
            "polynomial_surplus_copies_excluded":False}


def routing_requirement(n,r,advantage,M=None):
    """Necessary costed target for a label-adaptive nonlinear word routing."""
    integer(n,"dimension");integer(r,"root digits");M=n*r-2 if M is None else M;integer(M,"qutrits")
    if type(advantage) is not Fraction or not 0<advantage<=Fraction(2,3):raise ValueError("exact positive rational raw advantage <=2/3 required")
    D=3**M;G=3**(n*r);required=Fraction(9,2)*advantage**2*D*D
    required_cap=Fraction(9*D*G,4*(D-1))*advantage**2
    return {"dimension":n,"root_digits":r,"original_qutrits":M,"target_mean_raw_trit_advantage":str(advantage),
            "required_mean_phase_weighted_offset_energy_at_least":str(required),
            "required_mean_phase_independent_offset_energy_at_least":str(required),
            "necessary_uniform_worst_case_offset_multiplicity_cap_at_least":str((required_cap.numerator+required_cap.denominator-1)//required_cap.denominator),
            "expected_total_informative_directed_edges_invariant_under_word_permutation":str(Fraction(2*D*(D-1),G)),
            "uniform_worst_case_cap_not_unproved_independent_average_cap":True,
            "energy_is_necessary_not_sufficient_for_efficient_readout_or_decoder":True,
            "label_dependent_nonlinear_route_or_its_computation_supplied":False}


def _native(source,j):
    if source.level%2 or source.modulus!=3**(source.level//2):raise ValueError("even native source required")
    if native_source(source.labels,source.level).frequencies!=source.frequencies:raise ValueError("native chart must agree")
    integer(j,"target coordinate",0)
    if j>=source.dimension:raise ValueError("target coordinate outside source")
    D=3**source.inputs;G=source.modulus**source.dimension
    if D>81 or G>729:raise ValueError("complete word and uniform-secret replay capped at81 words/729 secrets")
    ws=tuple(product(range(3),repeat=source.inputs))
    f=tuple(source.value(w) for w in ws)
    return ws,f,D,G


def offset_counts(source,j=0):
    ws,fs,D,_=_native(source,j);q=source.modulus;Q=q//3;lookup={w:i for i,w in enumerate(ws)};records=[]
    for delta in ws[1:]:
        edges=[[],[]]
        for x,w in enumerate(ws):
            y=lookup[tuple((a+b)%3 for a,b in zip(w,delta))]
            difference=tuple((b-a)%q for a,b in zip(fs[x],fs[y]))
            for h in (1,2):
                if difference==tuple(Q*h if k==j else 0 for k in range(source.dimension)):edges[h-1].append((x,y))
        records.append({"delta":delta,"positive_count":len(edges[0]),"negative_count":len(edges[1]),"edges":edges})
    return ws,fs,records


def phase_values(source,j,kind):
    if kind not in MACROS:raise ValueError("audited public phase macro required, not a secret-bearing callback")
    ws,fs,_,_=_native(source,j);q=source.modulus;cut=max(1,source.inputs//2);inv2=pow(2,-1,q)
    values=[]
    for w,f in zip(ws,fs):
        a=sum(source.frequencies[i][d-1][j] if d else 0 for i,d in enumerate(w[:cut]))%q
        b=(f[j]-a)%q
        if kind=="zero":p=0
        elif kind=="total_quadratic":p=inv2*f[j]**2
        elif kind=="partial_quadratic":p=inv2*a*a
        elif kind=="cross_quadratic":p=a*b
        elif kind=="top_digit":p=(q//3)*(f[j]//(q//3))**2
        else:p=5*a*a+sum((row[0][j]+2*row[1][j])*d*d for row,d in zip(source.frequencies,w))
        values.append(p%q)
    return values


def native_control(source,j=0):
    ws,fs,records=offset_counts(source,j);D=len(ws);q=source.modulus;G=q**source.dimension
    E=sum(row["positive_count"]**2+row["negative_count"]**2 for row in records)
    squared=min(Fraction(4,9),Fraction(2*E,9*D*D))
    secrets=np.array(tuple(product(range(q),repeat=source.dimension)),dtype=int)
    ensemble=np.exp(2j*np.pi*(secrets@np.array(fs,dtype=int).T%q)/q)/np.sqrt(D)
    shape=(G,)+(3,)*source.inputs;axes=tuple(range(1,source.inputs+1));controls=[]
    for kind in MACROS:
        ps=phase_values(source,j,kind);phases=np.exp(2j*np.pi*np.array(ps)/q)
        physical=abs(np.fft.fftn((ensemble*phases).reshape(shape),axes=axes,norm="ortho").reshape(G,D))**2
        laws=np.stack([physical[secrets[:,j]%3==t].mean(axis=0) for t in range(3)])
        score=float(laws.max(axis=0).sum()/3);adv=score-1/3
        C=sum(abs(sum(phases[x]*phases[y].conjugate() for x,y in edges))**2 for row in records for edges in row["edges"])
        lhs=float(((laws-laws.mean(axis=0))**2).sum());rhs=3*C/D**3
        residual=abs(lhs-rhs)
        normalization=float(np.max(abs(physical.sum(axis=1)-1)))
        if residual>3e-12 or normalization>3e-12 or C>E+3e-10 or adv*adv>float(squared)+3e-12:raise ArithmeticError("physical score violates exact phase-independent envelope or Parseval")
        controls.append({"macro":kind,"public_phase_numerators":ps,"physical_uniform_prior_raw_MAP_success":score,
                         "physical_advantage_squared":adv*adv,"phase_weighted_offset_energy":C,
                         "actual_Parseval_left":lhs,"predicted_Parseval_right":rhs,"Parseval_residual":residual,
                         "Born_normalization_residual":normalization,
                         "efficient_classical_decoder_supplied":False})
    return {"dimension":source.dimension,"root_digits":root_digits(q),"modulus":q,"original_qutrits":source.inputs,"target_coordinate":j,
            "native_labels":source.labels,"full_frequency_rows":source.frequencies,
            "words":ws,"word_frequencies":fs,"offset_counts":[{k:v for k,v in row.items() if k!="edges"} for row in records],
            "exact_phase_independent_offset_energy":str(E),"every_phase_raw_advantage_squared_upper":str(squared),
            "complete_uniform_secret_count_calibration_only":G,"complete_amplitude_cells_calibration_only":G*D,
            "phase_controls":controls,"selected_or_prespecified_labels_not_population_evidence":True,
            "quantum_speedup_proved":False}


def census(q,M):
    root_digits(q);integer(M,"census width")
    if q**(2*M)>6561:raise ValueError("entire source census cap exceeded")
    ws=tuple(product(range(3),repeat=M));indices={w:i for i,w in enumerate(ws)}
    totals={k:0 for k in range(1,M+1)};numbers={k:comb(M,k)*2**k for k in totals};energy=0
    for flat in product(range(q),repeat=2*M):
        f=[sum(flat[2*i+d-1] if d else 0 for i,d in enumerate(w))%q for w in ws]
        for delta in ws[1:]:
            count=[0,0]
            for x,w in enumerate(ws):
                y=indices[tuple((a+b)%3 for a,b in zip(w,delta))];difference=(f[y]-f[x])%q
                if difference==q//3:count[0]+=1
                elif difference==2*q//3:count[1]+=1
            totals[sum(d!=0 for d in delta)]+=count[0]**2
            energy+=sum(a*a for a in count)
    cases=q**(2*M);r=root_digits(q);expected=population_certificate(1,r,M)
    mean=Fraction(energy,cases)
    if str(mean)!=expected["expected_phase_independent_offset_energy"]:raise ArithmeticError("complete IID source census disagrees with closed moment")
    moments=[{"support":k,"actual_second_moment_per_positive_class":str(Fraction(totals[k],cases*numbers[k]))} for k in totals]
    if any(a["actual_second_moment_per_positive_class"]!=b["second_moment_per_oriented_high_class"] for a,b in zip(moments,expected["support_moments"])):
        raise ArithmeticError("inactive-coordinate multiplicity or pairwise native moment failed")
    return {"modulus":q,"width":M,"entire_IID_frequency_cases":cases,"support_moments":moments,
            "actual_mean_offset_energy":str(mean),"calibration_not_a_new_oracle_problem":True}


def permutation_moment(q,images):
    """Exact signature routing, not source enumeration or a label-chosen map."""
    root_digits(q);images=tuple(tuple(w) for w in images);D=len(images)
    if not D:raise ValueError("nonempty word permutation required")
    M=len(images[0]);integer(M,"width")
    if D!=3**M or D>81 or any(len(w)!=M or any(type(a) is not int or a not in range(3) for a in w) for w in images) or len(set(images))!=D:
        raise ValueError("complete canonical bijection, at most81 words")
    ws=tuple(product(range(3),repeat=M));basis=((0,0),(1,0),(0,1));buckets={}
    for x in range(D):
        for y in range(D):
            if x==y:continue
            delta=tuple((b-a)%3 for a,b in zip(images[x],images[y]))
            signature=tuple(basis[b][k]-basis[a][k] for a,b in zip(ws[x],ws[y]) for k in range(2))
            buckets.setdefault(delta,Counter())[signature]+=1
    concentration=sum(c*c for bucket in buckets.values() for c in bucket.values())
    opposite=sum(c*bucket.get(tuple(-a for a in sig),0) for bucket in buckets.values() for sig,c in bucket.items())
    identity=D*D*((Fraction(5,3)**M)-1)
    if any(sum(bucket.values())!=D for bucket in buckets.values()) or concentration>identity:
        raise ArithmeticError("permutation signature routing violated mass or concentration")
    expected=2*(Fraction((D-1)*D*D,q*q)+(Fraction(1,q)-Fraction(1,q*q))*concentration-Fraction(opposite,q*q))
    if expected>Fraction(population_certificate(1,root_digits(q),M)["expected_phase_independent_offset_energy"]):
        raise ArithmeticError("label-independent routing exceeded original native population envelope")
    return {"modulus":q,"width":M,"permutation_images":images,"signature_bucket_square_sum":str(concentration),
            "opposite_signature_bucket_product_sum":str(opposite),"identity_signature_concentration_upper":str(identity),
            "exact_expected_offset_energy_after_permutation":str(expected),
            "permutation_fixed_independently_of_native_labels_required":True,
            "arbitrary_label_dependent_nonlinear_permutation_covered":False}


def report():
    source=native_source([[inverse_frequency_coordinates(a,c,8)] for a,c in ((1,2),(26,52))],8)
    controls=[native_control(source),native_control(random_even_source(1,12,4,99821)),native_control(random_even_source(2,6,4,99822),1)]
    tight=controls[0];zero=tight["phase_controls"][0]
    if tight["exact_phase_independent_offset_energy"]!="50" or abs(zero["physical_uniform_prior_raw_MAP_success"]-19/27)>3e-12:
        raise ArithmeticError("selected legal bound-saturating source control failed")
    ws=tuple(product(range(3),repeat=3));toffoli=tuple((a,b,(c+a*b)%3) for a,b,c in ws)
    return {"status":"LABEL_AWARE_SINGLE_DIAGONAL_FOURIER_LAYER_GATE_REVIEW_PENDING",
            "derivation_sha256":hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "candidate_record_accepted":False,"quantum_speedup_proved":False,"novelty_claim":False,"generic_quantum_lower_bound":False,
            "label_dependent_collective_initial_phases_covered":True,
            "partial_block_and_top_digit_initial_phases_covered":True,
            "multiple_noncommuting_layers_or_word_permutations_covered":False,
            "label_independent_word_permutations_covered":True,
            "label_dependent_affine_word_permutations_covered":True,
            "label_dependent_nonlinear_word_permutations_covered":False,
            "source_law":"ALL_IID_ORIGINAL_FULL_NATIVE_FREQUENCY_ROWS; UNIFORM_FULL_SECRET_PRIOR",
            "transition_rows":TRANSITIONS,
            "population_certificates":[population_certificate(n,r) for n,r in ((1,8),(1,16),(1,32),(1,64),(2,16))],
            "copy_surplus_control":population_certificate(1,4,16),
            "nonlinear_routing_requirements":[routing_requirement(n,r,Fraction(1,(n*r)**2)) for n,r in ((1,16),(1,32),(1,64),(2,16))],
            "complete_source_censuses":[census(3,2),census(9,2)],
            "fixed_permutation_signature_controls":[permutation_moment(9,ws),permutation_moment(9,toffoli)],
            "native_controls":controls,
            "tight_selected_control":{"exact_MAP_success":"19/27","exact_advantage_squared":"100/729","IID_population_algorithm":False},
            "falsifiers":["A native transition unit minor fails over a composite root.",
                          "The complete source census disagrees with support moments including inactive coordinates.",
                          "A complete uniform-secret physical score exceeds the phase-independent envelope.",
                          "This scoped receiver gate is extended to earlier word permutations, multiple mixers or a changed source law."]}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--write",action="store_true");args=parser.parse_args()
    value=report()
    if args.write:REPORT.write_text(json.dumps(value,indent=2,allow_nan=False)+"\n")
    print(json.dumps({"status":value["status"],"native_controls":3,"phase_controls":18,"complete_source_cases":6642,"speedup_claim_allowed":False}))


if __name__=="__main__":main()
