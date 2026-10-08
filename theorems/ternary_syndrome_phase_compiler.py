"""Constructive removal of initial polynomial frequency chirps for least trit.

LOCAL DERIVATION / REVIEW PENDING. Uniform-secret risk is preserved using
legal nuisance-syndrome measurement, not frequency-fiber inversion or a decoder.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path

import numpy as np

from cyclotomic_fiber_receiver import inverse_frequency_coordinates, native_source
from ternary_coherent_edge_receiver import NativeEdgeProgram
from ternary_covariant_noise import phase, root_digits
from ternary_cyclic_extractor import random_even_source

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/phase_workbench/ternary_syndrome_phase_compiler.json"


def _integer(x,name,minimum=0):
    if type(x) is not int or x<minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return x


def _vector(x,n,q):
    x=tuple(x)
    if len(x)!=n or any(type(a) is not int or not 0<=a<q for a in x):
        raise ValueError("canonical frequency vector required")
    return x


@dataclass(frozen=True)
class PolynomialPhase:
    dimension:int
    modulus:int
    terms:tuple

    def __post_init__(self):
        _integer(self.dimension,"dimension",1);root_digits(self.modulus)
        terms=tuple((c,tuple(e)) for c,e in self.terms)
        for c,e in terms:
            if type(c) is not int or not 0<=c<self.modulus or len(e)!=self.dimension or any(type(a) is not int or a<0 for a in e):
                raise ValueError("canonical modular coefficients and nonnegative integer powers required")
        object.__setattr__(self,"terms",terms)

    def value(self,f):
        f=_vector(f,self.dimension,self.modulus)
        return sum(c*prod_mod(f,e,self.modulus) for c,e in self.terms)%self.modulus

    def gradient_trit(self,f,j):
        f=_vector(f,self.dimension,self.modulus);_integer(j,"target coordinate")
        if j>=self.dimension:raise ValueError("target coordinate out of range")
        return sum(c*e[j]*prod_mod(f,tuple(a-int(k==j) for k,a in enumerate(e)),3)
                   for c,e in self.terms if e[j])%3

    def public(self):
        return {"family":"MODULAR_INTEGER_POLYNOMIAL","dimension":self.dimension,"modulus":str(self.modulus),
                "terms":[{"coefficient":str(c),"powers":tuple(map(str,e))} for c,e in self.terms]}


def prod_mod(values,powers,q):
    value=1
    for a,e in zip(values,powers):value=value*pow(a,e,q)%q
    return value


@dataclass(frozen=True)
class TopDigitQuadraticPhase:
    dimension:int
    modulus:int
    coordinate:int=0
    coefficient:int=1

    def __post_init__(self):
        _integer(self.dimension,"dimension",1)
        if root_digits(self.modulus)<2:raise ValueError("nonpolynomial top-digit countercontrol requires r>=2")
        _integer(self.coordinate,"phase coordinate");_integer(self.coefficient,"digit coefficient",1)
        if self.coordinate>=self.dimension or self.coefficient>2:raise ValueError("canonical coordinate and F3 coefficient required")

    def value(self,f):
        f=_vector(f,self.dimension,self.modulus);Q=self.modulus//3
        return Q*self.coefficient*(f[self.coordinate]//Q)**2%self.modulus

    def public(self):
        return {"family":"TOP_DIGIT_QUADRATIC_NON_POLYNOMIAL","dimension":self.dimension,"modulus":str(self.modulus),
                "coordinate":self.coordinate,"coefficient":self.coefficient}


def fiber_certificate(program,syndrome,coordinate=0):
    if type(program) not in (PolynomialPhase,TopDigitQuadraticPhase):raise ValueError("validated public phase program required")
    q,n=program.modulus,program.dimension;Q=q//3
    S=_vector(syndrome,n,q);_integer(coordinate,"target coordinate")
    if coordinate>=n or S[coordinate]>=Q:raise ValueError("canonical nuisance syndrome required")
    values=[]
    for h in range(3):
        f=list(S);f[coordinate]+=Q*h;values.append(program.value(f))
    delta=(values[1]-values[0])%q
    linear=delta%Q==0 and (values[2]-values[0]-2*delta)%q==0
    gradient=program.gradient_trit(S,coordinate) if type(program) is PolynomialPhase else None
    if type(program) is PolynomialPhase and q>=9 and (not linear or delta//Q!=gradient):
        raise ArithmeticError("square-zero Taylor identity failed")
    return {"program":program.public(),"syndrome":tuple(map(str,S)),"target_coordinate":coordinate,
            "phase_numerators_on_three_classes":list(map(str,values)),
            "phase_is_known_trit_translation":linear,"known_trit_translation":delta//Q if linear else None,
            "polynomial_derivative_trit":gradient,"square_zero_high_increment_theorem_applies":q>=9 and type(program) is PolynomialPhase,
            "root_one_or_nonpolynomial_exception_not_overridden":not(q>=9 and type(program) is PolynomialPhase)}


def syndrome_of(f,q,j):
    return tuple(a%(q//3) if k==j else a for k,a in enumerate(f))


def gradient_recipe(n,digits,inputs,coordinate=0):
    _integer(n,"dimension",1);_integer(digits,"root digits",2);_integer(inputs,"inputs",1)
    _integer(coordinate,"coordinate")
    if coordinate>=n:raise ValueError("target coordinate out of range")
    return {"dimension":n,"digits":digits,"original_qutrits":inputs,"target_coordinate":coordinate,
            "steps":["compute F(x) mod3 reversibly from public frequency rows mod3",
                     "evaluate and copy partial_j P(F mod3) into ONE gradient trit",
                     "UNCOMPUTE every low-frequency and derivative scratch register",
                     "measure ONLY the gradient trit",
                     "run the original remaining receiver on the original word registers",
                     "add polynomial derivative at the syndrome to the original trit prediction mod3"],
            "retained_measurement_register_trits":1,"low_frequency_scratch_trits":n,
            "frequency_row_evaluations_per_compute_or_uncompute":inputs,
            "phase_program_parameters_needed_only_mod3":True,
            "label_dependent_program_coefficients_may_still_depend_on_high_labels":True,
            "full_frequency_or_syndrome_register_required":False,
            "known_arithmetic_polynomial_in_public_input_size":True,"original_words_or_target_high_trit_measured":False,
            "extra_original_source_copies":0,"frequency_fiber_basis_or_inverse_supplied":False,
            "uniform_secret_mean_success_preserved":True,"pointwise_secret_success_preserved":False,
            "additional_same_secret_sources_or_query_access_covered":False,
            "interleaved_noncommuting_phase_operations_covered":False,"hardware_gate_export_implemented":False}


def exact_branch_law(words,high_trits,outputs,phase_trits,D):
    rows=[]
    for t in range(3):
        row=[]
        for output in outputs:
            counts=[0,0,0]
            exponents=[(t*h+p-sum(z*x for z,x in zip(output,w)))%3 for w,h,p in zip(words,high_trits,phase_trits)]
            for a,b in product(exponents,repeat=2):counts[(a-b)%3]+=1
            if counts[1]!=counts[2]:raise ArithmeticError("non-real exact branch probability")
            row.append(Fraction(counts[0]-counts[1],D*D))
        rows.append(row)
    return rows


def native_control(edge_program,phase_program):
    source=edge_program.source;q=source.modulus;n=source.dimension;j=edge_program.coordinate;D=edge_program.size
    if D>81:raise ValueError("complete native word/output calibration capped at81")
    if type(phase_program) is not PolynomialPhase or q<9:raise ValueError("native gradient compiler requires polynomial phase and r>=2")
    if phase_program.modulus!=q or phase_program.dimension!=n:raise ValueError("phase/source shape mismatch")
    words=tuple(product(range(3),repeat=source.inputs));frequencies=tuple(source.value(w) for w in words)
    groups={}
    for i,f in enumerate(frequencies):groups.setdefault(syndrome_of(f,q,j),[]).append(i)
    groups=dict(sorted(groups.items()));total=[[Fraction(0) for _ in words] for _ in range(3)]
    records=[];branch_laws=[]
    for S,indices in groups.items():
        cert=fiber_certificate(phase_program,S,j)
        if not cert["phase_is_known_trit_translation"]:raise ValueError("receiver compilation requires translated class phases")
        g=cert["known_trit_translation"];hs=[frequencies[i][j]//(q//3) for i in indices]
        base=exact_branch_law([words[i] for i in indices],hs,words,[0]*len(indices),D)
        chirped=exact_branch_law([words[i] for i in indices],hs,words,[(phase_program.value(frequencies[i])-phase_program.value(S))//(q//3)%3 for i in indices],D)
        if any(chirped[t]!=base[(t+g)%3] for t in range(3)):raise ArithmeticError("exact syndrome class-law translation mismatch")
        for t in range(3):
            if sum(base[t])!=Fraction(len(indices),D):raise ArithmeticError("wrong unconditioned Born branch mass")
            for o in range(D):total[t][o]+=chirped[t][o]
        records.append({"certificate":cert,"word_indices":indices,"high_trits":hs,"Born_mass":str(Fraction(len(indices),D))})
        branch_laws.append((S,indices,g,base,chirped))
    decoder=[max(range(3),key=lambda t:total[t][o]) for o in range(D)]
    score=sum(total[decoder[o]][o] for o in range(D))/3
    compiled=sum(base[t][o] for _,_,g,base,_ in branch_laws for t in range(3) for o in range(D) if (decoder[o]+g)%3==t)/3
    if score!=compiled:raise ArithmeticError("uniform-trit decoder risk was not preserved")
    constant_rule_baseline=[sum(Fraction(len(indices),D) for _,indices,g,_,_ in branch_laws if g==t) for t in range(3)]
    # Bounded physical replay of actual full-root phases, not only reduced class formulas.
    secret_controls=[(0,)*n,(1,)*n,(3,)*n,(q-1,)*n];residual=0.0;dirty_residual=0.0
    full_groups={}
    for i,f in enumerate(frequencies):full_groups.setdefault(f,[]).append(i)
    dirty_reference=np.zeros(D)
    for indices in full_groups.values():
        branch=np.zeros(D,dtype=complex);branch[indices]=1/np.sqrt(D)
        dirty_reference+=abs(np.fft.fftn(branch.reshape((3,)*source.inputs),norm="ortho").ravel())**2
    for secret in secret_controls:
        source_state=np.array([phase(sum(a*s for a,s in zip(f,secret)),q) for f in frequencies])/np.sqrt(D)
        chirp=np.array([phase(phase_program.value(f),q) for f in frequencies])
        for _,indices,_,_,law in branch_laws:
            branch=np.zeros(D,dtype=complex);branch[indices]=source_state[indices]*chirp[indices]
            output=np.fft.fftn(branch.reshape((3,)*source.inputs),norm="ortho").ravel()
            residual=max(residual,float(np.max(abs(abs(output)**2-np.array([float(p) for p in law[secret[j]%3]])))))
        dirty=np.zeros(D)
        for indices in full_groups.values():
            branch=np.zeros(D,dtype=complex);branch[indices]=source_state[indices]*chirp[indices]
            dirty+=abs(np.fft.fftn(branch.reshape((3,)*source.inputs),norm="ortho").ravel())**2
        dirty_residual=max(dirty_residual,float(np.max(abs(dirty-dirty_reference))))
    if max(residual,dirty_residual)>3e-12:raise ArithmeticError("actual full-root syndrome/readout or dirty-scratch control disagrees with class law")
    G=q**n
    if G>729:raise ValueError("complete gradient-only secret ensemble capped at729")
    secrets=np.array(tuple(product(range(q),repeat=n)),dtype=int)
    frequency_array=np.array(frequencies,dtype=int)
    ensemble=np.exp(2j*np.pi*(secrets @ frequency_array.T % q)/q)/np.sqrt(D)
    gradients=np.array([phase_program.gradient_trit(f,j) for f in frequencies])
    axes=tuple(range(1,source.inputs+1));shape=(G,)+(3,)*source.inputs
    gradient_score=0.0
    for g in range(3):
        branch=ensemble*(gradients==g)
        probabilities=abs(np.fft.fftn(branch.reshape(shape),axes=axes,norm="ortho").reshape(G,D))**2
        gradient_score+=float(np.sum(probabilities*((np.array(decoder)+g)%3==secrets[:,j,None]%3)))/G
    full_chirped=ensemble*np.array([phase(phase_program.value(f),q) for f in frequencies])
    probabilities=abs(np.fft.fftn(full_chirped.reshape(shape),axes=axes,norm="ortho").reshape(G,D))**2
    direct_score=float(np.sum(probabilities*(np.array(decoder)==secrets[:,j,None]%3)))/G
    gradient_residual=max(abs(gradient_score-float(compiled)),abs(direct_score-float(score)))
    if gradient_residual>3e-12:raise ArithmeticError("gradient-only measurement changed complete uniform-secret risk")
    return {"dimension":n,"root_digits":root_digits(q),"modulus":q,"target_coordinate":j,
            "native_labels":source.labels,"full_frequency_rows":source.frequencies,"words":words,
            "word_frequencies":frequencies,"occupied_syndrome_branches":records,
            "chirped_output_trit_laws_no_syndrome_reported":total,"original_chirped_MAP_decoder":decoder,
            "original_chirped_uniform_trit_success":str(score),"compiled_unchirped_uniform_trit_success":str(compiled),
            "actual_full_root_phase_Born_residual":residual,"calibration_secrets_only":secret_controls,
            "gradient_only_complete_uniform_secret_score_residual":gradient_residual,
            "complete_uniform_secrets_enumerated_for_gradient_calibration":G,
            "complete_ensemble_amplitude_cells_calibration_only":G*D,
            "constant_decision_pointwise_countercontrol":{"original_success_by_trit":["1","0","0"],
                                                          "compiled_success_by_trit":list(map(str,constant_rule_baseline)),
                                                          "uniform_mean_success_both":"1/3"},
            "dirty_full_frequency_scratch_or_measurement_trit_success":"1/3",
            "dirty_full_frequency_probability_residual":dirty_residual,
            "classical_word_and_output_enumerations_calibration_only":D,
            "efficient_MAP_decoder_or_fiber_transform_supplied":False,
            "uniform_mean_not_pointwise_secret_guarantee":True,"speedup_claim_allowed":False}


def report():
    certificates=[]
    for r,n,j in ((2,1,0),(16,2,0),(32,3,1),(64,2,1)):
        q=3**r
        terms=[((q+1)//2,tuple(2 if k==j else 0 for k in range(n))),
               (7%q,tuple(3 if k==j else 1 for k in range(n))),
               (2,tuple(1 for _ in range(n)))]
        P=PolynomialPhase(n,q,tuple(terms));S=tuple(((q//9+2)%(q//3) if k==j else q-2) for k in range(n))
        certificates.append(fiber_certificate(P,S,j))
    pairs=((1,2),(26,52));source=native_source([[inverse_frequency_coordinates(a,c,8)] for a,c in pairs],8)
    controls=[native_control(NativeEdgeProgram(source),PolynomialPhase(1,81,((41,(2,)),(7,(5,))))) ]
    random_source=random_even_source(1,12,4,99731)
    controls.append(native_control(NativeEdgeProgram(random_source),PolynomialPhase(1,729,((365,(2,)),(3,(3,)),(5,(1,))))))
    digit=fiber_certificate(TopDigitQuadraticPhase(1,81),(0,))
    root_one=fiber_certificate(PolynomialPhase(1,3,((1,(2,)),)),(0,))
    partial_values=[pow(2,-1,81)*a*a%81 for a in (0,1,2)]
    return {"status":"INITIAL_POLYNOMIAL_FREQUENCY_PHASE_COMPILATION_REVIEW_PENDING",
            "derivation_sha256":hashlib.sha256((ROOT/"research/TERNARY_SYNDROME_PHASE_COMPILER.md").read_bytes()).hexdigest(),
            "quantum_speedup_proved":False,"candidate_record_accepted":False,"novelty_claim":False,
            "every_fixed_native_label_matrix_uniform_secret_risk_scope":True,
            "pointwise_secret_success_or_general_measurement_no_go":False,
            "analytic_fiber_certificates":certificates,"native_receiver_controls":controls,
            "nonpolynomial_top_digit_countercontrol":digit,"root_one_countercontrol":root_one,
            "scalable_gradient_recipe":gradient_recipe(2,64,126,1),
            "partial_block_frequency_countercontrol":{"native_control_index":0,"words":[[0,0],[1,1],[2,2]],
                                                       "total_frequencies":[0,27,54],"common_total_nuisance_syndrome":[0],
                                                       "first_block_frequencies":[0,1,2],"partial_quadratic_phase_values":partial_values,
                                                       "known_total_trit_translation_available":False},
            "additional_same_secret_samples_or_query_access_covered":False,
            "native_source_supply_or_efficient_decoder_created":False,
            "falsifiers":["A modular integer polynomial violates its square-zero high-trit Taylor identity at r>=2.",
                          "A compiled receiver changes uniform-secret success after adding the known syndrome-dependent prediction shift.",
                          "The recipe retains or measures the target high-frequency trit and destroys the original useful phase.",
                          "A top-digit nonpolynomial phase or root-one case is falsely admitted as a polynomial translation."]}


def _json(x):
    if isinstance(x,Fraction):return str(x)
    raise TypeError(type(x).__name__)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--write",action="store_true");args=parser.parse_args()
    value=report();encoded=json.dumps(value,indent=2,default=_json,allow_nan=False)+"\n"
    if args.write:REPORT.write_text(encoded)
    print(json.dumps({"status":value["status"],"analytic_certificates":4,"native_controls":2,"speedup_claim_allowed":False}))


if __name__=="__main__":main()
