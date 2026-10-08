"""Multi-round native echo with explicit mediator-history contraction.

Original native sample access only. Conditional simulation is not an
unknown-secret decoder or classical dequantization of the input states.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, replace
from itertools import product
import json
from pathlib import Path
import random

import numpy as np

from native_partial_phase_echo import (
    EchoFamily, F3, adapted_coupling, bounded_score, local_product_probabilities,
)
from ternary_covariant_noise import _word, _integer, phase

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/phase_workbench/native_echo_history_receiver.json"


@dataclass(frozen=True)
class EchoSchedule:
    source: EchoFamily
    couplings: tuple

    def __post_init__(self):
        if not isinstance(self.source,EchoFamily):
            raise ValueError("actual native source and nonempty public echo schedule required")
        couplings=tuple(replace(self.source,coupling=K).coupling for K in self.couplings)
        if not couplings:
            raise ValueError("actual native source and nonempty public echo schedule required")
        object.__setattr__(self,"couplings",couplings)

    @property
    def rounds(self):
        return len(self.couplings)

    @property
    def modulus(self):
        return self.source.modulus

    @property
    def dimension(self):
        return self.source.dimension

    @property
    def copies(self):
        return self.source.copies

    def frequency(self,word):
        return self.source.frequency(word)

    @property
    def histories(self):
        return 3**(self.source.mediator_width*self.rounds)

    def recipe(self):
        ledger=self.source.recipe()
        for key in ("modular_frequency_additions","public_bilinear_multiplication_terms","individual_inverse_F3_operations"):
            ledger[key]*=self.rounds
        ledger.update({"echo_rounds":self.rounds,"original_native_source_copies":self.source.copies,
                       "initial_local_settings_applied_once":True,
                       "frequency_scratch_cleared_before_EVERY_mediator_Fourier":True,
                       "same_batch_is_evolved_NOT_reprepared":True,
                       "mediator_history_count":self.histories,
                       "conditional_streaming_likelihood_work":"O(3^(w*d)*d*m*n^2) arithmetic/phase work; no q^n secret search included",
                       "polynomial_contraction_requires_w_times_d_logarithmic":True,
                       "has_single_echo_architecture":self.rounds==1,
                       "A_independence_of_coupling_is_NOT_inferred_from_schedule":True,
                       "program":["Apply initial public per-copy diagonal settings once.",
                                  "For each public K: compute frequencies, phase, clear A, Fourier A, recompute UPDATED A, undo phase, clear BOTH, Fourier B.",
                                  "Do not measure or reprepare original inputs between rounds; measure all original wires at the end."]})
        return ledger

    def public(self):
        return {"source":self.source.public(),"round_couplings":self.couplings,"recipe":self.recipe()}

    def local_history_unitaries(self,history):
        f=self.source
        if len(history)!=self.rounds:
            raise ValueError("one full mediator word per round required")
        history=tuple(_word(y,3,"mediator history word",f.mediator_width) for y in history)
        unitaries=np.array([np.eye(3,dtype=complex) for _ in range(f.main_width)])
        for y,K in zip(history,self.couplings):
            FB=f.frequency(y,f.main_width)
            delta=tuple(sum(K[i][j]*FB[j] for j in range(f.dimension)) % f.modulus for i in range(f.dimension))
            for i in range(f.main_width):
                exponents=(0,sum(x*z for x,z in zip(f.first[i],delta)),sum(x*z for x,z in zip(f.second[i],delta)))
                diagonal=np.array([phase(x,f.modulus) for x in exponents])
                U=diagonal.conj()[:,None]*F3*diagonal[None,:]
                unitaries[i]=U@unitaries[i]
        return unitaries

    def amplitude(self,secret,outcome,history_budget=59049):
        f=self.source
        secret=_word(secret,f.modulus,"verification secret",f.dimension)
        if len(outcome)!=f.copies or any(type(x) is not int or x not in range(3) for x in outcome):
            raise ValueError("one canonical original-wire output word required")
        _integer(history_budget,"complete mediator history budget",1)
        if self.histories>history_budget:
            raise ValueError("complete mediator history contraction exceeds budget; no truncation")
        a,b=outcome[:f.main_width],outcome[f.main_width:]
        initial=initial_local_states(f,(secret,),0,f.main_width)[0]
        B=tuple(product(range(3),repeat=f.mediator_width))
        total=0j
        for history in product(B,repeat=self.rounds):
            y0=history[0]
            exponent=sum(s*z for s,z in zip(secret,f.frequency(y0,f.main_width)))-f.setting_phase(y0,f.main_width)
            response=phase(exponent,f.modulus)
            for before,after in zip(history,history[1:]+(b,)):
                response*=phase(-sum(x*y for x,y in zip(before,after)),3)
            U=self.local_history_unitaries(history)
            response*=np.prod([(U[i]@initial[i])[digit] for i,digit in enumerate(a)])
            total+=response
        return total/3**(f.mediator_width*(self.rounds+1)/2)

    def dense_output(self,secret,word_budget=729):
        """Physical full-batch replay, independent of the history formula."""
        f=self.source
        secret=_word(secret,f.modulus,"verification secret",f.dimension)
        D=3**f.copies
        if D>word_budget:
            raise ValueError("complete original-word replay exceeds budget")
        words=tuple(product(range(3),repeat=f.copies))
        state=np.array([phase(sum(s*z for s,z in zip(secret,f.frequency(x)))-f.setting_phase(x),f.modulus) for x in words])/np.sqrt(D)
        A=tuple(product(range(3),repeat=f.main_width))
        B=tuple(product(range(3),repeat=f.mediator_width))
        for K in self.couplings:
            lens=replace(f,coupling=K)
            chirp=np.array([[phase(lens.bilinear(f.frequency(a),f.frequency(b,f.main_width)),f.modulus) for b in B] for a in A])
            state=(state.reshape(len(A),len(B))*chirp).reshape((3,)*f.copies)
            for i in range(f.main_width):
                state=np.moveaxis(np.tensordot(F3,state,axes=(1,i)),0,i)
            state=(state.reshape(len(A),len(B))*chirp.conj()).reshape((3,)*f.copies)
            for i in range(f.main_width,f.copies):
                state=np.moveaxis(np.tensordot(F3,state,axes=(1,i)),0,i)
            state=state.ravel()
        return state


def initial_local_states(f,secrets,start,width):
    return np.array([[[phase(sum(s*z for s,z in zip(secret,row))-eta,f.modulus)/np.sqrt(3)
                       for row,eta in (((0,)*f.dimension,0),(f.first[i],f.local_settings[i][0]),(f.second[i],f.local_settings[i][1]))]
                      for i in range(start,start+width)] for secret in secrets])


def history_baseline(schedule,secret_budget=81,word_budget=729,history_budget=59049):
    """Same-copy LOCC: public random history, local A unitaries, B Fourier."""
    f=schedule.source
    G=f.modulus**f.dimension
    if G>secret_budget or 3**f.copies>word_budget or schedule.histories>history_budget:
        raise ValueError("complete original prior/word/history baseline exceeds budget")
    secrets=tuple(product(range(f.modulus),repeat=f.dimension))
    A=tuple(product(range(3),repeat=f.main_width))
    B=tuple(product(range(3),repeat=f.mediator_width))
    initial=initial_local_states(f,secrets,0,f.main_width)
    PB=local_product_probabilities(f,secrets,f.main_width,f.mediator_width)
    dirty_A=np.zeros((G,len(A)))
    full=trit=without_B=0.
    for history in product(B,repeat=schedule.rounds):
        U=schedule.local_history_unitaries(history)
        states=np.einsum("ijk,sik->sij",U,initial)
        probabilities=abs(states)**2
        PA=np.ones((G,len(A)))
        for i in range(f.main_width):
            PA*=probabilities[:,i,[word[i] for word in A]]
        if np.max(abs(PA.sum(axis=1)-1))>2e-11:
            raise ArithmeticError("local history output does not normalize")
        dirty_A+=PA/schedule.histories
        without_B+=float(PA.max(axis=0).sum()/(G*schedule.histories))
        joint=PA[:,:,None]*PB[:,None,:]/schedule.histories
        full+=float(joint.max(axis=0).sum()/G)
        grouped=np.array([joint[[i for i,s in enumerate(secrets) if s[0] % 3==t]].sum(axis=0) for t in range(3)])
        trit+=float(grouped.max(axis=0).sum()/G)
    dirty=np.repeat(dirty_A[:,:,None]/len(B),len(B),axis=2).reshape(G,-1)
    P=np.array([abs(schedule.dense_output(s,word_budget))**2 for s in secrets])
    violation=float(np.max(P-schedule.histories*dirty))
    if violation>2e-11:
        raise ArithmeticError("coherent history sum exceeds exact Cauchy domination factor")
    return {"full_uniform_secret_MAP_success_numeric_reference":full,
            "least_trit_MAP_success_numeric_reference":trit,
            "A_only_random_history_recorded_MAP_success":without_B,
            "dephased_full_B_WORD_history_MAP_success":float(dirty.max(axis=0).sum()/G),
            "pointwise_coherent_to_dephased_domination_factor":schedule.histories,
            "maximum_pointwise_domination_residual":violation,
            "complete_histories_enumerated":schedule.histories,
            "decoder_secret_hypotheses_enumerated":G,
            "same_original_native_copies":f.copies,"single_copy_quantum_gates_only":True,
            "protocol":"Draw every mediator history word uniformly; apply its known local A unitary products; Fourier-measure original B separately; retain history and every outcome.",
            "classical_simulation_without_unknown_input_states_claimed":False,
            "efficient_unknown_secret_decoder_supplied":False},dirty


def cohort(q,n,M,w,seed):
    rng=random.Random(seed)
    first=tuple(tuple(rng.randrange(q) for _ in range(n)) for _ in range(M))
    second=tuple(tuple(rng.randrange(q) for _ in range(n)) for _ in range(M))
    settings=tuple(tuple(rng.randrange(q) for _ in range(2)) for _ in range(M))
    zero=tuple((0,)*n for _ in range(n))
    identity=tuple(tuple(int(i==j) for j in range(n)) for i in range(n))
    calibrated,calibration=adapted_coupling(first,q,M-w)
    negate=lambda K:tuple(tuple(-x % q for x in row) for row in K)
    policies={"product_three_rounds":(zero,zero,zero),"fixed_same_lens":(identity,identity,identity),
              "fixed_alternating_lens":(identity,negate(identity),identity),
              "calibrated_alternating_lens":(calibrated,negate(calibrated),calibrated),
              "calibrated_two_rounds_then_product":(calibrated,negate(calibrated),zero)}
    records=[]
    for basis,eta in (("fixed",((0,0),)*M),("initial_randomized",settings)):
        for name,Ks in policies.items():
            f=EchoFamily(first,second,q,w,zero,eta)
            schedule=EchoSchedule(f,Ks)
            score=bounded_score(schedule)
            baseline,_=history_baseline(schedule)
            records.append({"receiver_policy":name,"basis_policy":basis,"schedule":schedule.public(),
                            "score":score,"matched_history_LOCC":baseline,
                            "full_MAP_minus_OWN_LOCC":score["full_uniform_secret_MAP_success_numeric_reference"]-baseline["full_uniform_secret_MAP_success_numeric_reference"],
                            "least_trit_MAP_minus_OWN_LOCC":score["least_trit_MAP_success_numeric_reference"]-baseline["least_trit_MAP_success_numeric_reference"],
                            "coupling_uses_full_A_labels":name.startswith("calibrated"),
                            "calibration":calibration if name.startswith("calibrated") else None})
    return {"modulus":q,"dimension":n,"original_native_copies":M,"mediator_width":w,
            "source_seed":seed,"full_IID_source_no_rejection":True,"records":records,
            "conditional_reference_policy_selection_is_NOT_an_algorithm":True}


def run_controls():
    cohorts=[cohort(q,n,M,w,seed) for q,n,M,w in ((9,1,4,1),(9,2,4,2),(27,1,5,1),(81,1,6,1)) for seed in (61911,61912,61913)]
    return {"status":"NATIVE_MULTIROUND_ECHO_HISTORY_RECEIVER_REVIEW_PENDING","cohorts":cohorts,
            "exact_checker_control":cohort(9,1,3,1,61910),
            "contraction_exponent_is_mediator_width_TIMES_echo_rounds":True,
            "fast_conditional_likelihood_is_NOT_unknown_secret_inference":True,
            "one_echo_obstruction_does_NOT_cover_multiple_rounds":True,
            "new_speedup_claimed":False,"novelty_claimed":False,"candidate_accepted":False}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write",action="store_true")
    args=parser.parse_args()
    out=run_controls()
    if args.write:
        REPORT.write_text(json.dumps(out,indent=2,allow_nan=False)+"\n")
    records=[r for c in out["cohorts"] for r in c["records"] if r["receiver_policy"]!="product_three_rounds"]
    print(json.dumps({"status":out["status"],"nonproduct_controls":len(records),
                      "maximum_full_MAP_minus_OWN_LOCC":max(r["full_MAP_minus_OWN_LOCC"] for r in records),
                      "maximum_least_trit_MAP_minus_OWN_LOCC":max(r["least_trit_MAP_minus_OWN_LOCC"] for r in records)}))


if __name__=="__main__":
    main()
