"""Costed partial-frequency phase echo on original native phase samples.

An actual orbit-coupling receiver and bounded-width likelihood evaluator.
No efficient unknown-secret decoder, novelty or speedup is asserted.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from itertools import product
import json
import math
from pathlib import Path
import random

import numpy as np
from flint import nmod_mat
from sympy import Matrix

from cyclotomic_fiber_receiver import inverse_frequency_coordinates, native_source
from ternary_covariant_noise import root_digits, phase, _word, _integer

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/phase_workbench/native_partial_phase_echo.json"
F3=np.array([[phase(-j*k,3)/math.sqrt(3) for k in range(3)] for j in range(3)])


@dataclass(frozen=True)
class EchoFamily:
    first: tuple
    second: tuple
    modulus: int
    mediator_width: int
    coupling: tuple
    local_settings: tuple = ()

    def __post_init__(self):
        root_digits(self.modulus)
        _integer(self.mediator_width,"mediator width",1)
        if len(self.first)<2 or len(self.first)!=len(self.second) or self.mediator_width>=len(self.first):
            raise ValueError("two nonempty original-source blocks required")
        n=len(self.first[0])
        for name in ("first","second"):
            object.__setattr__(self,name,tuple(_word(a,self.modulus,name,n) for a in getattr(self,name)))
        K=tuple(_word(row,self.modulus,"public coupling",n) for row in self.coupling)
        if len(K)!=n:
            raise ValueError("square public dimension-by-dimension coupling required")
        object.__setattr__(self,"coupling",K)
        settings=self.local_settings or ((0,0),)*len(self.first)
        if len(settings)!=len(self.first):
            raise ValueError("one public phase pair per original sample required")
        object.__setattr__(self,"local_settings",tuple(_word(a,self.modulus,"local setting",2) for a in settings))

    @property
    def dimension(self):
        return len(self.first[0])

    @property
    def copies(self):
        return len(self.first)

    @property
    def main_width(self):
        return self.copies-self.mediator_width

    def frequency(self,word,start=0):
        if len(word)+start>self.copies or any(type(j) is not int or j not in range(3) for j in word):
            raise ValueError("canonical word within original source rows required")
        return tuple(sum((self.first[start+i][l] if j==1 else self.second[start+i][l] if j==2 else 0)
                         for i,j in enumerate(word)) % self.modulus for l in range(self.dimension))

    def bilinear(self,a,b):
        return sum(a[i]*self.coupling[i][j]*b[j] for i in range(self.dimension) for j in range(self.dimension)) % self.modulus

    def setting_phase(self,word,start=0):
        return sum((self.local_settings[start+i][j-1] if j else 0) for i,j in enumerate(word)) % self.modulus

    def native_source(self):
        level=2*root_digits(self.modulus)
        labels=tuple(tuple(inverse_frequency_coordinates(a,c,level) for a,c in zip(first,second))
                     for first,second in zip(self.first,self.second))
        return native_source(labels,level)

    def recipe(self):
        r=root_digits(self.modulus)
        return {"original_native_source_copies":self.copies,"native_even_level":2*r,
                "main_block_qutrits":self.main_width,"mediator_qutrits":self.mediator_width,
                "frequency_scratch_trits":2*self.dimension*r,
                "modular_accumulator_trits":r,
                "modular_frequency_additions":4*self.dimension*self.main_width+2*self.dimension*self.mediator_width,
                "public_bilinear_multiplication_terms":2*self.dimension**2,
                "individual_inverse_F3_operations":self.copies,
                "program":["Apply the committed per-copy public diagonal settings.",
                           "Compute F_B and F_A into clean modular scratch.",
                           "Apply chi_q(F_A^T K F_B), then uncompute F_A.",
                           "Apply inverse_F3 to every A wire.",
                           "Compute F_A of the UPDATED A word.",
                           "Apply chi_q(-F_A^T K F_B), then uncompute BOTH frequency registers.",
                           "Apply inverse_F3 to every B wire; measure all original wires."],
                "public_arithmetic_workspace_and_gate_precision_still_to_be_compiled":True,
                "full_frequency_scratch_cleared_BEFORE_mediator_Fourier":True,
                "unknown_source_preparation_inverse_used":False,
                "fiber_count_rank_unrank_oracle_used":False,
                "source_states_reused_or_cloned":False,
                "hardware_gate_export_supplied":False}

    def amplitude(self,secret,outcome):
        """Streaming exact-form likelihood; numeric phases, no secret search."""
        secret=_word(secret,self.modulus,"verification secret",self.dimension)
        if len(outcome)!=self.copies or any(type(j) is not int or j not in range(3) for j in outcome):
            raise ValueError("one ternary outcome per original sample required")
        a,b=outcome[:self.main_width],outcome[self.main_width:]
        FA=self.frequency(a)
        correction=tuple(sum(FA[i]*self.coupling[i][l] for i in range(self.dimension)) % self.modulus for l in range(self.dimension))
        total=0j
        for y in product(range(3),repeat=self.mediator_width):
            FB=self.frequency(y,self.main_width)
            shifted=tuple((secret[i]+sum(self.coupling[i][l]*FB[l] for l in range(self.dimension))) % self.modulus for i in range(self.dimension))
            response=1+0j
            for i,digit in enumerate(a):
                f=sum(s*x for s,x in zip(shifted,self.first[i]))-self.local_settings[i][0]
                c=sum(s*x for s,x in zip(shifted,self.second[i]))-self.local_settings[i][1]
                response *= (1+phase(f,self.modulus)*phase(-digit,3)+phase(c,self.modulus)*phase(-2*digit,3))/3
            residual=sum((s-c)*z for s,c,z in zip(secret,correction,FB))-self.setting_phase(y,self.main_width)
            total += response*phase(residual,self.modulus)*phase(-sum(x*z for x,z in zip(b,y)),3)/3**self.mediator_width
        return total

    def dense_output(self,secret,word_budget=729):
        """Independent physical gate replay, capped; not a large-state solver."""
        secret=_word(secret,self.modulus,"verification secret",self.dimension)
        D=3**self.copies
        if D>word_budget:
            raise ValueError("complete native word reference exceeds its budget")
        words=tuple(product(range(3),repeat=self.copies))
        initial=np.array([phase(sum(s*f for s,f in zip(secret,self.frequency(w)))-self.setting_phase(w),self.modulus) for w in words])/np.sqrt(D)
        A=tuple(product(range(3),repeat=self.main_width))
        B=tuple(product(range(3),repeat=self.mediator_width))
        chirp=np.array([[phase(self.bilinear(self.frequency(a),self.frequency(b,self.main_width)),self.modulus) for b in B] for a in A])
        state=(initial.reshape(len(A),len(B))*chirp).reshape((3,)*self.copies)
        for wire in range(self.main_width):
            state=np.moveaxis(np.tensordot(F3,state,axes=(1,wire)),0,wire)
        state=(state.reshape(len(A),len(B))*chirp.conj()).reshape((3,)*self.copies)
        for wire in range(self.main_width,self.copies):
            state=np.moveaxis(np.tensordot(F3,state,axes=(1,wire)),0,wire)
        return state.ravel()

    def public(self):
        return {"first_frequencies":self.first,"second_frequencies":self.second,"modulus":self.modulus,
                "mediator_width":self.mediator_width,"public_coupling":self.coupling,"local_settings":self.local_settings}


def bounded_score(family,secret_budget=81,word_budget=729):
    G=family.modulus**family.dimension
    if G>secret_budget or 3**family.copies>word_budget:
        raise ValueError("complete prior/outcome reference exceeds budget; no partial score")
    secrets=tuple(product(range(family.modulus),repeat=family.dimension))
    P=np.array([abs(family.dense_output(s,word_budget))**2 for s in secrets])
    normalization=float(np.max(abs(P.sum(axis=1)-1)))
    if normalization>2e-11:
        raise ArithmeticError("raw echo output probability does not normalize")
    # Ties get a deterministic first index; exact checking is done separately.
    winners=[]
    for column in P.T:
        best=max(column)
        winners.append(next(i for i,p in enumerate(column) if best-p<2e-13))
    full=sum(P[s,j] for j,s in enumerate(winners))/G
    by_trit=np.array([P[[i for i,s in enumerate(secrets) if s[0] % 3 == t]].sum(axis=0) for t in range(3)])
    trit=float(by_trit.max(axis=0).sum()/G)
    counts=Counter(family.frequency(w) for w in product(range(3),repeat=family.copies))
    ideal=sum(math.sqrt(c) for c in counts.values())**2/(G*3**family.copies)
    if full>ideal+2e-11:
        raise ArithmeticError("basis receiver exceeds actual native ideal discrimination optimum")
    return {"full_uniform_secret_MAP_success_numeric_reference":float(full),
            "least_trit_MAP_success_numeric_reference":trit,"complete_probability_normalization_error":normalization,
            "ideal_native_PGM_success_information_only":ideal,"full_secret_count":G,
            "complete_word_outcomes":3**family.copies,"decoder_secret_hypotheses_enumerated":G,
            "full_secret_MAP_winner_indices_by_outcome":winners,
            "efficient_unknown_secret_decoder_supplied":False,"ideal_PGM_circuit_supplied":False}


def local_product_probabilities(family,secrets,start,width):
    outcomes=tuple(product(range(3),repeat=width))
    P=np.zeros((len(secrets),len(outcomes)))
    for isec,s in enumerate(secrets):
        probabilities=[]
        for i in range(start,start+width):
            f=sum(a*b for a,b in zip(s,family.first[i]))-family.local_settings[i][0]
            c=sum(a*b for a,b in zip(s,family.second[i]))-family.local_settings[i][1]
            probabilities.append([abs(1+phase(f,family.modulus)*phase(-z,3)+phase(c,family.modulus)*phase(-2*z,3))**2/9 for z in range(3)])
        P[isec]=[math.prod(probabilities[i][z] for i,z in enumerate(word)) for word in outcomes]
    return P


def randomized_local_baseline(family,secret_budget=81,word_budget=729):
    """Actual same-copy LOCC baseline; all exponential decoding is charged."""
    G=family.modulus**family.dimension
    if G>secret_budget or 3**family.copies>word_budget:
        raise ValueError("complete baseline prior/outcome reference exceeds budget")
    secrets=tuple(product(range(family.modulus),repeat=family.dimension))
    indices={s:i for i,s in enumerate(secrets)}
    PA=local_product_probabilities(family,secrets,0,family.main_width)
    PB=local_product_probabilities(family,secrets,family.main_width,family.mediator_width)
    W=3**family.mediator_width
    full=trit=0.
    dirty_A=np.zeros_like(PA)
    without_B=0.
    B_words=tuple(product(range(3),repeat=family.mediator_width))
    B_classes={}
    for y in B_words:
        B_classes.setdefault(family.frequency(y,family.main_width),[]).append(y)
    for y in product(range(3),repeat=family.mediator_width):
        FB=family.frequency(y,family.main_width)
        delta=tuple(sum(family.coupling[i][j]*FB[j] for j in range(family.dimension)) % family.modulus for i in range(family.dimension))
        shifted=[indices[tuple((s+d) % family.modulus for s,d in zip(secret,delta))] for secret in secrets]
        A=PA[shifted]
        dirty_A += A/W
        without_B += float(A.max(axis=0).sum()/(G*W))
        joint=A[:,:,None]*PB[:,None,:]/W
        full += float(joint.max(axis=0).sum()/G)
        by_trit=np.array([joint[[i for i,s in enumerate(secrets) if s[0] % 3 == t]].sum(axis=0) for t in range(3)])
        trit += float(by_trit.max(axis=0).sum()/G)
    dirty_FB=np.zeros((G,PA.shape[1],W))
    for FB,ys in B_classes.items():
        delta=tuple(sum(family.coupling[i][j]*FB[j] for j in range(family.dimension)) % family.modulus for i in range(family.dimension))
        shifted=[indices[tuple((s+d) % family.modulus for s,d in zip(secret,delta))] for secret in secrets]
        public_kernel=np.array([abs(sum(phase(-family.setting_phase(y,family.main_width),family.modulus)*phase(-sum(x*z for x,z in zip(b,y)),3) for y in ys))**2/W**2 for b in B_words])
        dirty_FB+=PA[shifted,:,None]*public_kernel[None,None,:]
    dirty_word_score=float(dirty_A.max(axis=0).sum()/G)
    dirty_score=float(dirty_FB.max(axis=0).sum()/G)
    if dirty_score>without_B+2e-11 or dirty_word_score>without_B+2e-11 or without_B>full+2e-11:
        raise ArithmeticError("discarding classical metadata or B data improves its optimal decision")
    return {"same_original_native_quantum_copies":family.copies,
            "public_random_word_width":family.mediator_width,
            "protocol":"Draw y uniformly; apply known +K F_B(y) phase to A, measure every copy with its committed product Fourier settings; retain y and all outputs.",
            "only_single_copy_quantum_gates_used":True,
            "full_uniform_secret_MAP_success_numeric_reference":full,
            "least_trit_MAP_success_numeric_reference":trit,
            "dirty_echo_with_unerased_F_B_scratch_MAP_success":dirty_score,
            "dirty_echo_with_a_full_B_WORD_tag_MAP_success":dirty_word_score,
            "distinct_B_frequency_classes":len(B_classes),
            "dirty_F_B_kernel_keeps_same_frequency_word_coherence":True,
            "pointwise_clean_to_dirty_F_B_likelihood_domination_factor":len(B_classes),
            "randomized_A_only_with_y_recorded_MAP_success":without_B,
            "classical_y_uses_no_unknown_secret":True,
            "decoder_secret_hypotheses_enumerated":G,
            "complete_classical_outcomes_including_y":3**(family.copies+family.mediator_width),
            "efficient_unknown_secret_decoder_supplied":False,
            "classical_dequantization_of_clean_echo_claimed":False}


def adapted_coupling(first,modulus,main_width):
    """Full-label calibration: first independent A rows, inverse over Z_q."""
    root_digits(modulus)
    _integer(main_width,"main width",1)
    if not first or main_width>len(first):
        raise ValueError("nonempty canonical A rows within the source required")
    n=len(first[0])
    first=tuple(_word(row,modulus,"calibration row",n) for row in first)
    pivots=[]
    for i in range(main_width):
        if nmod_mat([list(first[j]) for j in pivots+[i]],3).rank()>len(pivots):
            pivots.append(i)
        if len(pivots)==n:
            break
    if len(pivots)<n:
        return tuple((0,)*n for _ in range(n)),{"pivot_indices":pivots,"full_mod3_rank":False,
                  "rank_failure_returns_product_readout_without_source_rejection":True}
    V=Matrix([first[i] for i in pivots])
    determinant=int(V.det())
    inv=(pow(determinant % modulus,-1,modulus)*V.adjugate()).applyfunc(lambda x:int(x) % modulus)
    K=tuple(tuple(int(inv[i,j]) for j in range(n)) for i in range(n))
    if any(sum(first[pivots[i]][k]*K[k][j] for k in range(n)) % modulus != int(i==j) for i in range(n) for j in range(n)):
        raise ArithmeticError("actual native A calibration does not invert the selected frequency rows")
    return K,{"pivot_indices":pivots,"full_mod3_rank":True,"full_A_labels_used_in_coupling":True,
              "determinant_is_a_unit_modulo3":determinant % 3 != 0,
              "rank_failure_returns_product_readout_without_source_rejection":True,
              "shifted_probe_Gram_bound_for_A_independent_couplings_applies":False}


def generated_cohort(q,n,m,w,seed):
    rng=random.Random(seed)
    first=tuple(tuple(rng.randrange(q) for _ in range(n)) for _ in range(m))
    second=tuple(tuple(rng.randrange(q) for _ in range(n)) for _ in range(m))
    settings=tuple(tuple(rng.randrange(q) for _ in range(2)) for _ in range(m))
    zero=tuple((0,)*n for _ in range(n))
    calibrated,calibration=adapted_coupling(first,q,m-w)
    records=[]
    for basis in ("fixed","phase_randomized"):
        eta=((0,0),)*m if basis=="fixed" else settings
        for coupling_id in ("product","positive_echo","negative_echo","A_preconditioned_echo"):
            K=calibrated if coupling_id=="A_preconditioned_echo" else zero if coupling_id=="product" else tuple(tuple(((1 if coupling_id=="positive_echo" else q-1) if i==j else (1 if j==i+1 else 0)) for j in range(n)) for i in range(n))
            family=EchoFamily(first,second,q,w,K,eta)
            source=family.native_source()
            if source.frequencies != tuple(zip(first,second)):
                raise ArithmeticError("echo input frequencies do not reconstruct an actual even native source")
            score=bounded_score(family)
            local=randomized_local_baseline(family)
            records.append({"basis_policy":basis,"receiver_policy":coupling_id,"family":family.public(),
                            "score":score,"resource_recipe":family.recipe(),
                            "coupling_uses_full_A_frequency_labels":coupling_id=="A_preconditioned_echo",
                            "calibration":calibration if coupling_id=="A_preconditioned_echo" else None,
                            "matched_randomized_local_baseline":local,
                            "full_secret_echo_minus_OWN_matched_LOCC":score["full_uniform_secret_MAP_success_numeric_reference"]-local["full_uniform_secret_MAP_success_numeric_reference"],
                            "least_trit_echo_minus_OWN_matched_LOCC":score["least_trit_MAP_success_numeric_reference"]-local["least_trit_MAP_success_numeric_reference"]})
    baseline=max(r["score"]["full_uniform_secret_MAP_success_numeric_reference"] for r in records if r["receiver_policy"]=="product")
    echo=max(r["score"]["full_uniform_secret_MAP_success_numeric_reference"] for r in records if r["receiver_policy"]!="product")
    local=max(r["matched_randomized_local_baseline"]["full_uniform_secret_MAP_success_numeric_reference"] for r in records)
    fixed=max(r["score"]["full_uniform_secret_MAP_success_numeric_reference"] for r in records if r["receiver_policy"] in ("positive_echo","negative_echo"))
    adapted=max(r["score"]["full_uniform_secret_MAP_success_numeric_reference"] for r in records if r["receiver_policy"]=="A_preconditioned_echo")
    trit_key="least_trit_MAP_success_numeric_reference"
    trit_echo=max(r["score"][trit_key] for r in records if r["receiver_policy"]!="product")
    trit_product=max(r["score"][trit_key] for r in records if r["receiver_policy"]=="product")
    trit_local=max(r["matched_randomized_local_baseline"][trit_key] for r in records)
    return {"source_seed":seed,"full_uniform_IID_frequency_generation":True,"public_phase_settings_seeded_not_secret_selected":True,
            "receiver_records":records,"best_echo_minus_best_matched_product_score":echo-baseline,
            "best_echo_minus_best_stronger_LOCC_score":echo-local,
            "best_FIXED_echo_minus_best_product_score":fixed-baseline,
            "best_A_preconditioned_echo_minus_best_stronger_LOCC_score":adapted-local,
            "best_echo_minus_best_product_LEAST_TRIT_score":trit_echo-trit_product,
            "best_echo_minus_best_stronger_LOCC_LEAST_TRIT_score":trit_echo-trit_local,
            "best_policy_selection_uses_exponential_reference_not_an_algorithm":True,
            "numerical_conditional_cohort_difference_is_not_population_advantage":True,
            "new_speedup_or_candidate_acceptance_allowed":False}


def run_controls():
    return {"status":"NATIVE_PARTIAL_FREQUENCY_PHASE_ECHO_CONSTRUCTIVE_RECEIVER_REVIEW_PENDING",
            "cohort_controls":[generated_cohort(q,n,m,w,seed) for q,n,m,w in ((9,1,4,1),(9,2,6,2),(27,1,5,2),(81,1,6,2)) for seed in (58123,58124,58125)],
            "exact_checker_control":generated_cohort(9,1,3,1,58122),
            "classical_single_outcome_likelihood_complexity":"O(3^w*(n*M+n^2)) phase/arithmetic work; streaming workspace, not a q^n posterior table",
            "polynomial_likelihood_at_logarithmic_mediator_width":True,
            "polynomial_secret_search_follows_from_fast_likelihood":False,
            "cross_word_orbit_coherence_is_used":True,
            "initial_total_frequency_chirp_compiler_applies":False,
            "source_creation_inverse_or_fiber_oracle_supplied":False,
            "new_algorithmic_speedup_claimed":False,"novelty_claimed":False}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--write",action="store_true")
    args=p.parse_args()
    out=run_controls()
    if args.write:
        REPORT.write_text(json.dumps(out,indent=2,allow_nan=False)+"\n")
    differences=[x["best_echo_minus_best_matched_product_score"] for x in out["cohort_controls"]]
    print(json.dumps({"status":out["status"],"cohorts":len(differences),
                      "mean_conditional_echo_minus_product":float(np.mean(differences)),
                      "efficient_decoder_supplied":False}))


if __name__=="__main__":
    main()
