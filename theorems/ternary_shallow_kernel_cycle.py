"""Known shallow sieve as a polynomial nonlinear cycle; exact unseen-prefix gate.

LOCAL DERIVATION / REVIEW PENDING. No new algorithm or full-depth supply gain.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path
import random

import numpy as np

from ternary_affine_line_extractor import from_quadratic,quadratic_rows,rank
from ternary_batch_fiber_compiler import BatchFiberProgram,integer,pointed_minor
from ternary_cyclic_extractor import kernel_relation,random_even_source,throughput_ledger,zero_sum_support
from ternary_nonlinear_cycle_compiler import canonical_word,cyclic_coordinates,reconstruct

ROOT=Path(__file__).resolve().parents[1]
NOTE=ROOT/"research/TERNARY_SHALLOW_KERNEL_CYCLE.md"
REPORT=ROOT/"research/phase_workbench/ternary_shallow_kernel_cycle.json"


@dataclass(frozen=True)
class ShallowKernelCycle:
    dimension:int
    width:int
    A:tuple
    B:tuple
    supports:tuple
    mask_policy:str="provided-validated-disjoint-masks"

    def __post_init__(self):
        integer(self.dimension,"dimension",1);integer(self.width,"original width",1)
        for matrix in (self.A,self.B):
            if len(matrix)!=self.dimension or any(len(row)!=self.width or any(type(a) is not int or a not in range(3) for a in row) for row in matrix):raise ValueError("canonical low quadratic matrices required")
        if len(self.supports)!=self.dimension+1:raise ValueError("n+1 nonempty disjoint curvature supports required")
        flattened=[]
        for support in self.supports:
            if not support or tuple(sorted(set(support)))!=support or any(type(i) is not int or i<0 or i>=self.width for i in support):raise ValueError("canonical disjoint support indices required")
            if any(sum(row[i] for i in support)%3 for row in self.B):raise ValueError("support does not cancel true low curvature")
            flattened.extend(support)
        if len(set(flattened))!=len(flattened):raise ValueError("overlapping masks invalidate the invariant-tangent proof")
        if self.mask_policy not in ("known-disjoint-SDE-windows","provided-validated-disjoint-masks"):raise ValueError("unreviewed mask acquisition policy")

    @classmethod
    def from_source(cls,source):
        A,B=quadratic_rows(source);n=source.dimension;W=(n+1)**2
        if source.inputs<(n+1)*W:raise ValueError("known guaranteed shallow construction needs(n+1)^3 original inputs")
        supports=[]
        for j in range(n+1):
            indices=tuple(range(j*W,(j+1)*W));vectors=[tuple(row[i] for row in B) for i in indices]
            certificate=zero_sum_support(vectors);supports.append(tuple(indices[i] for i in certificate["support"]))
        return cls(n,source.inputs,A,B,tuple(supports),"known-disjoint-SDE-windows")

    def control(self,word):
        word=canonical_word(word,self.width)
        tangents=tuple(tuple(sum(self.A[j][i]+2*self.B[j][i]*word[i] for i in support)%3 for j in range(self.dimension)) for support in self.supports)
        coefficients=kernel_relation(tangents)
        if not any(coefficients) or any(sum(column[j]*c for column,c in zip(tangents,coefficients))%3 for j in range(self.dimension)):raise ArithmeticError("invalid tangent-kernel relation")
        shift=[0]*self.width
        for support,c in zip(self.supports,coefficients):
            for i in support:shift[i]=c
        return tangents,coefficients,tuple(shift)

    def __call__(self,word):
        word=canonical_word(word,self.width);_,_,v=self.control(word)
        return tuple((x+a)%3 for x,a in zip(word,v))

    def metadata(self):
        return {"dimension":self.dimension,"original_qutrits":self.width,"A":self.A,"B":self.B,"disjoint_masks":self.supports,
                "mask_support_ranks":[rank([[row[i] for i in support] for row in self.B]) for support in self.supports],
                "word_evaluation_arithmetic_cost":"O(n*M+n^3)","mask_policy":self.mask_policy,
                "guaranteed_mask_preprocessing_polynomial":self.mask_policy=="known-disjoint-SDE-windows",
                "policy_stores_or_reads_high_frequency_rows":False,"word_cube_table_or_rank_oracle_loaded":False,
                "explicit_polynomial_word_algorithm_supplied":True,"native_quantum_gate_synthesis_supplied":False,
                "whole_instrument_hardware_error_bound_supplied":False,"acceptance_for_all_low_matrices":"1",
                "one_step_polynomial_original_supply_supplied":True,"full_depth_polynomial_supply_supplied":False}


def unseen_prefix_gate(n,r,e,d):
    integer(n,"dimension",1);integer(r,"parent root digits",2);integer(e,"available prefix digits",1);integer(d,"requested prefix digits",1)
    if not e<=d<r:raise ValueError("available prefix <= requested proper prefix < parent root required")
    J=3**(d-e);child=3**(r-e)
    return {"dimension":n,"parent_root_digits":r,"available_prefix_digits":e,"requested_prefix_digits":d,
            "extra_prefix_modulus":J,"conditional_child_modulus":child,
            "per_coordinate_uniform_child_pair_count":child**2,"per_coordinate_extra_prefix_match_count":(child//J)**2,
            "mean_extra_prefix_survival_factor":str(Fraction(1,J**(2*n))),
            "cycle_policy_is_unchanged_and_reads_only_available_prefix":True,
            "full_high_label_instance_success_equal_to_population_factor_claimed":False,
            "higher_prefix_informed_actions_or_secret_digit_correction_excluded":False,"quantum_speedup_proved":False}


def selected_child(source,policy,tag):
    triple=tuple(reconstruct(tag,k,policy) for k in range(3));f=tuple(source.value(w) for w in triple);q=source.modulus;child=q//3
    rows=tuple(tuple((a-b)%q//3 for a,b in zip(row,f[0])) for row in f[1:]);minor=pointed_minor(triple);a,b=minor["columns"];R=minor["coefficient_rows"]
    images={((R[0][a]*u+R[0][b]*v)%child,(R[1][a]*u+R[1][b]*v)%child) for u,v in product(range(child),repeat=2)}
    if len(images)!=child*child:raise ArithmeticError("pointed conditional high-lift map is not bijective")
    success=[]
    for coordinate in range(source.dimension):
        physical_pairs=set()
        for u,v in product(range(child),repeat=2):
            altered=[(row[coordinate]+3*u*int(word[a//2]==a%2+1)+3*v*int(word[b//2]==b%2+1))%q for row,word in zip(f,triple)]
            physical_pairs.add(tuple((value-altered[0])%q//3 for value in altered[1:]))
        if len(physical_pairs)!=child**2:raise ArithmeticError("actual two-column source-frequency lifts did not give every child pair")
        success.append(sum(u%3==0 and v%3==0 for u,v in physical_pairs))
    census={"per_coordinate_complete_two_column_lifts":child**2,
            "actual_source_frequency_lift_census_coordinates":source.dimension,
            "per_coordinate_child_pairs_divisible_by_three":success,
            "joint_prefix9_survival_factor_from_independent_coordinates":str(Fraction(1,9**source.dimension)),
            "whole_joint_high_lift_cartesian_cube_enumerated":False}
    secrets=[(0,)*source.dimension,(1,)*source.dimension,(q-1,)*source.dimension];residual=0.0
    for secret in secrets:
        actual=np.exp(2j*np.pi*np.array([sum(a*b for a,b in zip(row,secret))%q for row in f])/q)/np.sqrt(3)
        expected=actual[0]*np.exp(2j*np.pi*np.array([0]+[sum(a*b for a,b in zip(row,secret))%child for row in rows])/child)
        residual=max(residual,float(np.max(abs(actual-expected))))
    if residual>3e-12:raise ArithmeticError("physical child phase failed")
    return {"tag_word":tag,"original_words":triple,"full_frequencies":f,"child_rows":rows,"pointed_unit_minor":minor,
            "raw_tag_probability_exponent_base_three":1-source.inputs,"conditional_lift_census":census,
            "calibration_secrets":secrets,"physical_phase_residual":residual}


def control_record(n,r,seed,complete=False):
    M=(n+1)**3;source=random_even_source(n,2*r,M,seed);policy=ShallowKernelCycle.from_source(source)
    if complete:
        if M>8:raise ValueError("whole shallow cube capped at eight original qutrits")
        words=tuple(product(range(3),repeat=M))
    else:
        rng=random.Random(seed+1);words=tuple(tuple(rng.randrange(3) for _ in range(M)) for _ in range(48))
    coordinates=[];directions=set();tags=set();prefix9_good=0
    for word in words:
        tangents,coefficients,v=policy.control(word);directions.add(v)
        first=policy(word);second=policy(first)
        if policy(second)!=word or word==first or policy.control(first)!=policy.control(word) or policy.control(second)!=policy.control(word):raise ArithmeticError("nonlinear direction is not invariant on a three-cycle")
        if any(source.value(first)[j]%3!=source.value(word)[j]%3 for j in range(n)):raise ArithmeticError("actual native first prefix changed")
        u,t,flag=cyclic_coordinates(word,policy)
        if not flag or reconstruct(u,t,policy)!=word:raise ArithmeticError("canonical coordinates failed to erase original word")
        coordinates.append((u,t));tags.add(u)
        prefix9_good+=int(len({tuple(a%9 for a in source.value(w)) for w in (word,first,second)})==1)
    if len(set(coordinates))!=len(set(words)):raise ArithmeticError("word coordinates are not injective")
    if complete and (len(tags)!=3**(M-1) or len(words)!=3**M):raise ArithmeticError("complete source mass was not retained")
    selected=sorted(tags);pick=sorted(set((0,len(selected)//2,len(selected)-1)))
    return {"dimension":n,"parent_root_digits":r,"parent_modulus":3**r,"original_qutrits":M,
            "native_labels":source.labels,"full_frequency_rows":source.frequencies,"policy":policy.metadata(),
            "source_cube_enumerated_completely":complete,"original_words_audited":len(words),
            "audited_words":None if complete else words,
            "complete_or_sample_coordinate_sha256":hashlib.sha256(json.dumps(coordinates,separators=(",",":")).encode()).hexdigest(),
            "distinct_direction_values_on_audited_words":len(directions),"distinct_tags_on_audited_words":len(tags),
            "raw_first_prefix_acceptance":"1","unchanged_cycles_with_prefix9_match_on_audited_words":prefix9_good,
            "sample_fraction_is_population_survival_factor_claimed":False,
            "selected_child_controls":[selected_child(source,policy,selected[k]) for k in pick],
            "one_output_per_actual_batch":True,"all_orbit_tags_counted_as_separate_outputs":False,
            "novel_shallow_algorithm_claimed":False,"full_depth_polynomial_supply_supplied":False}


def report():
    controls=[control_record(1,3,88114,True),control_record(2,3,88102),control_record(3,3,88103)]
    return {"status":"KNOWN_SHALLOW_NONLINEAR_CYCLE_VERIFIED_FULL_DEPTH_LIFT_BLOCKED_REVIEW_PENDING",
            "derivation_sha256":hashlib.sha256(NOTE.read_bytes()).hexdigest(),"candidate_record_accepted":False,"quantum_speedup_proved":False,"novelty_claim":False,
            "complete_n1_seed_selected_for_nonconstant_direction_control":True,
            "native_controls":controls,"implicit_exponential_menu_control":implicit_menu_control(),
            "unseen_prefix_population_gates":[unseen_prefix_gate(n,r,e,d) for n,r,e,d in ((1,3,1,2),(2,3,1,2),(8,5,1,4),(32,6,2,5),(128,7,1,6))],
            "known_full_depth_supply_controls":[throughput_ledger(3**r,r) for r in (2,3,4,5)],
            "all_polynomial_cycle_programs_are_polynomial_explicit_menus_claimed":False,
            "full_depth_polynomial_time_and_supply_algorithm_supplied":False,"source_preparation_inverse_granted":False}


def implicit_menu_control():
    n=2;M=(n+1)**2;A=tuple((0,)*M for _ in range(n));B=tuple(tuple((int(i%(n+1)==j)-int(i%(n+1)==n))%3 for i in range(M)) for j in range(n))
    source=from_quadratic(A,B);supports=tuple(tuple(range(j*(n+1),(j+1)*(n+1))) for j in range(n+1));policy=ShallowKernelCycle(n,M,*quadratic_rows(source),supports)
    rows=[]
    for c in product(range(3),repeat=n):
        targets=tuple(tuple(int(i==j) for i in range(n)) for j in range(n))+ (tuple(-x%3 for x in c),)
        word=tuple(a for column in targets for a in (*tuple(2*x%3 for x in column),0))
        tangents,coefficients,v=policy.control(word)
        if tangents!=targets or coefficients!=c+(1,):raise ArithmeticError("implicit exponential menu construction failed its actual tangent equations")
        rows.append({"chosen_c":c,"original_word":word,"actual_tangents":tangents,"kernel_coefficients":coefficients,"word_direction":v})
    if len({row["word_direction"] for row in rows})!=3**n:raise ArithmeticError("exponentially many coefficient values did not give distinct word directions")
    return {"dimension":n,"original_qutrits":M,"parent_root_digits":3,"native_labels":source.labels,"full_frequency_rows":source.frequencies,
            "policy":policy.metadata(),"all_c_vectors_controls":rows,"distinct_direction_count":3**n,
            "provided_full_rank_masks_are_guaranteed_on_IID_labels_claimed":False,"algorithm_candidate_record_accepted":False}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--write",action="store_true");args=parser.parse_args();value=report()
    if args.write:REPORT.write_text(json.dumps(value,indent=2,allow_nan=False)+"\n")
    print(json.dumps({"status":value["status"],"original_words_audited":sum(c["original_words_audited"] for c in value["native_controls"]),"full_depth_algorithm_supplied":False}))


if __name__=="__main__":main()
