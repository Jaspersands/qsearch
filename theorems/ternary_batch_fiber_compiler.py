"""Balanced native low-frequency fibers and a COSTED batch extractor reference.

LOCAL DERIVATION / REVIEW PENDING. Correct child law does not implement the
missing efficient coherent fiber partition. One batch produces one child.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from itertools import combinations,product
import json
from pathlib import Path

import numpy as np
from flint import nmod_mat

from cyclotomic_fiber_receiver import inverse_frequency_coordinates,native_source
from ternary_covariant_noise import phase,root_digits
from ternary_cyclic_extractor import random_even_source

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/phase_workbench/ternary_batch_fiber_compiler.json"
DERIVATION=ROOT/"research/TERNARY_BATCH_FIBER_COMPILER.md"


def integer(x,name,minimum=0):
    if type(x) is not int or x<minimum:raise ValueError(f"{name} must be an integer >= {minimum}")
    return x


def lucas(n,k):
    integer(n,"nonnegative exponent");integer(k,"coefficient degree")
    value=1
    while n or k:
        a,b=n%3,k%3
        if b>a:return 0
        value=value*(2 if (a,b)==(2,1) else 1)%3;n//=3;k//=3
    return value


def batch_ledger(n,r,d):
    integer(n,"dimension",1);integer(r,"root digits",2);integer(d,"prefix digits",1)
    if d>=r:raise ValueError("retain a nontrivial child root")
    H=3**d;M=n*(H-1)+1
    return {"dimension":n,"parent_root_digits":r,"prefix_digits":d,"parent_modulus":str(3**r),"child_modulus":str(3**(r-d)),
            "per_coordinate_digit_degree_bounds":[2*3**j for j in range(d)],"total_constraint_degree_upper":n*(H-1),
            "minimum_original_qutrits_for_all_fibers_divisible_by_three":M,
            "word_cube_exponent_base_three":M,"possible_measurement_tags_exponent_base_three":M-1,
            "output_qutrits_per_actual_input_batch":1,
            "batch_supply_polynomial_in_n_only_if_q_polynomial_in_n":True,
            "batch_supply_polynomial_in_log_q_claimed":False,
            "generating_coefficient_circuit_scalar_operation_upper":n*M*(H+1)**2,
            "known_integer_frequency_evaluation_is_a_fiber_inverse":False,
            "efficient_coherent_partition_implemented":False,
            "independent_child_law_requires_low_only_partition_and_fresh_batches":True,
            "quantum_speedup_proved":False}


def pointed_minor(words):
    words=tuple(tuple(w) for w in words)
    if len(words)!=3 or not words[0] or any(len(w)!=len(words[0]) or any(type(a) is not int or a not in range(3) for a in w) for w in words) or len(set(words))!=3:
        raise ValueError("three distinct canonical original words required")
    basis=((0,0),(1,0),(0,1))
    rows=[tuple(basis[w][k]-basis[b][k] for b,w in zip(words[0],target) for k in range(2)) for target in words[1:]]
    for a,b in combinations(range(len(rows[0])),2):
        determinant=rows[0][a]*rows[1][b]-rows[0][b]*rows[1][a]
        if abs(determinant)==1:return {"coefficient_rows":rows,"columns":(a,b),"determinant":determinant}
    raise ArithmeticError("native pointed triple has no unit minor")


def gated_cnf(variables,clauses):
    """Parsimonious OR gadgets supply a known satisfying gated assignment."""
    integer(variables,"Boolean variables",1);clauses=tuple(tuple(c) for c in clauses)
    if any(not 1<=len(c)<=3 or any(type(a) is not int or not 1<=abs(a)<=variables for a in c) for c in clauses):
        raise ValueError("canonical nonempty clauses of at most three literals required")
    gate=variables+1;new_variables=gate;new=[]
    for clause in clauses:
        if len(clause)<3:new.append((gate,)+clause)
        else:
            a,b,c=clause;new_variables+=1;y=new_variables
            new.extend(((-gate,y),(-a,y),(gate,a,-y),(y,b,c)))
    return new_variables,tuple(new),(0,)*variables+(1,)*(new_variables-variables)


def cnf_value(word,clauses):
    return all(any(bool(word[abs(a)-1])==(a>0) for a in clause) for clause in clauses)


def lex_rank_reduction(variables,clauses):
    """Native worst-case compiler countercontrol; NOT an algorithm candidate."""
    V,C,known=gated_cnf(variables,clauses);n=V+len(C);real_width=n
    if variables>6 or real_width>8:raise ValueError("entire real-variable reduction calibration capped at eight qutrits")
    q,H=27,9;rows=[]
    for variable in range(V):
        a=[0]*n;c=[0]*n;c[variable]=1
        for j,clause in enumerate(C):a[V+j]=sum(1 if literal>0 else -1 for literal in clause if abs(literal)==variable+1)%q
        rows.append((tuple(a),tuple(c)))
    for j in range(len(C)):
        a=[0]*n;c=[0]*n;a[V+j]=1;c[V+j]=2;rows.append((tuple(a),tuple(c)))
    target=(0,)*V+tuple((3-sum(a<0 for a in clause))%H for clause in C)
    M=n*(H-1)+1;dummy=M-real_width;zero=((0,)*n,(0,)*n);full_rows=[zero]*dummy+rows
    labels=[[inverse_frequency_coordinates(a,c,6) for a,c in zip(pair[0],pair[1])] for pair in full_rows]
    source=native_source(labels,6);p=BatchFiberProgram(source,2)
    real_words=tuple(product(range(3),repeat=real_width));solutions=[]
    for word in real_words:
        frequency=tuple(sum(rows[i][x-1][j] if x else 0 for i,x in enumerate(word))%H for j in range(n))
        if frequency==target:solutions.append(word)
    real_known=known+tuple(3-sum(bool(known[abs(a)-1])==(a>0) for a in clause) for clause in C)
    if real_known not in solutions:raise ArithmeticError("gated known assignment did not give its native target word")
    original_count=sum(cnf_value(w,clauses) for w in product(range(2),repeat=variables))
    if len(solutions)!=original_count+2**variables:raise ArithmeticError("native fiber does not parsimoniously count gated CNF solutions")
    rank=solutions.index(real_known);first=(0,)*dummy+real_known;second=(0,)*(dummy-1)+(1,)+real_known
    if p.low_frequency(first)!=target or p.low_frequency(second)!=target:raise ArithmeticError("promised basis-query words left their target fiber")
    trits=(rank%3,(rank+len(solutions))%3)
    recovered=(trits[1]-trits[0]-2**variables)%3
    if recovered!=original_count%3:raise ArithmeticError("lexicographic logical digit did not reveal model count modulo3")
    return {"original_boolean_variables":variables,"original_clauses":clauses,"gated_boolean_variables":V,"gated_clauses":C,
            "known_satisfying_gated_assignment":known,"native_dimension":n,"parent_modulus":q,"prefix_modulus":H,
            "original_qutrits":M,"zero_frequency_dummy_prefix_width":dummy,"real_frequency_rows":rows,
            "native_full_rows":source.frequencies,"native_labels":source.labels,"target_native_prefix":target,
            "whole_real_words_enumerated_calibration_only":3**real_width,"real_fiber_count":len(solutions),
            "original_CNF_satisfying_assignment_count_calibration_only":original_count,
            "first_promised_native_word":first,"second_promised_native_word":second,
            "lex_logical_trits_from_exact_rank_formula_not_compiler":trits,"recovered_original_model_count_mod_three":recovered,
            "whole_padded_source_words_enumerated":False,"actual_coherent_basis_compiler_supplied":False,
            "hard_labels_are_worst_case_not_IID_average_case":True,
            "nonlexicographic_or_source_state_only_compilers_ruled_out":False}


@dataclass(frozen=True)
class BatchFiberProgram:
    source:object
    prefix_digits:int

    def __post_init__(self):
        s=self.source
        if s.level%2 or s.modulus!=3**(s.level//2) or native_source(s.labels,s.level).frequencies!=s.frequencies:
            raise ValueError("canonical original even native source required")
        integer(self.prefix_digits,"prefix digits",1)
        if self.prefix_digits>=s.level//2:raise ValueError("proper nontrivial prefix only")

    @property
    def prefix_modulus(self):return 3**self.prefix_digits

    @property
    def low_rows(self):return tuple(tuple(tuple(a%self.prefix_modulus for a in row) for row in pair) for pair in self.source.frequencies)

    def low_frequency(self,word):
        word=tuple(word)
        if len(word)!=self.source.inputs or any(type(a) is not int or a not in range(3) for a in word):raise ValueError("one canonical original trit per input required")
        rows=self.low_rows
        return tuple(sum(rows[i][a-1][j] if a else 0 for i,a in enumerate(word))%self.prefix_modulus for j in range(self.source.dimension))

    def coefficient_digit(self,word,coordinate,digit):
        """Fixed-loop algebraic circuit, not a full word truth-table lookup."""
        self.low_frequency(word);integer(coordinate,"coordinate");integer(digit,"digit")
        if coordinate>=self.source.dimension or digit>=self.prefix_digits:raise ValueError("digit or coordinate outside prefix")
        L=3**digit
        if L>243:raise ValueError("coefficient-circuit replay capped at degree243; symbolic degree ledger remains valid")
        accumulator=[1]+[0]*L
        for pair,x in zip(self.low_rows,word):
            local=[]
            for k in range(L+1):
                zero=int(k==0);a=lucas(pair[0][coordinate],k);c=lucas(pair[1][coordinate],k)
                local.append((zero+(2*a+c)*x+(2*a+2*c+2*zero)*x*x)%3)
            accumulator=[sum(accumulator[j]*local[k-j] for j in range(k+1))%3 for k in range(L+1)]
        return accumulator[L]

    def reduced_polynomial(self,coordinate,digit):
        integer(coordinate,"coordinate");integer(digit,"digit")
        if coordinate>=self.source.dimension or digit>=self.prefix_digits:raise ValueError("digit/coordinate outside prefix")
        M=self.source.inputs
        if M>6:raise ValueError("entire reduced-polynomial calibration capped at six word variables")
        ws=tuple(product(range(3),repeat=M));table=np.array([self.low_frequency(w)[coordinate]//3**digit%3 for w in ws],dtype=np.int64).reshape((3,)*M)
        inverse=nmod_mat([[1,x,x*x%3] for x in range(3)],3).inv();inv=np.array([[int(inverse[i,j]) for j in range(3)] for i in range(3)])
        for axis in range(M):
            table=np.moveaxis(table,axis,0);shape=table.shape;table=(inv@table.reshape(3,-1)%3).reshape(shape);table=np.moveaxis(table,0,axis)
        terms=[{"powers":w,"coefficient":int(table[w])} for w in ws if table[w]]
        degree=max((sum(t["powers"]) for t in terms),default=0);bound=min(2*M,2*3**digit)
        if degree>bound:raise ArithmeticError("native carry degree exceeded generating-function bound")
        return {"coordinate":coordinate,"digit":digit,"terms":terms,"degree":degree,"degree_upper":bound,
                "contains_mixed_variable_terms":any(sum(e!=0 for e in t["powers"])>1 for t in terms),
                "constant_degree_diagonal_solver_premise_certified":False,
                "entire_words_enumerated_calibration_only":3**M}

    def reference(self,max_words=19683):
        integer(max_words,"whole reference budget",1);D=3**self.source.inputs
        if D>max_words:raise ValueError("whole partition preflight exceeded; no partial map returned")
        ledger=batch_ledger(self.source.dimension,self.source.level//2,self.prefix_digits)
        if self.source.inputs<ledger["minimum_original_qutrits_for_all_fibers_divisible_by_three"]:
            raise ValueError("batch below the ALL-LABEL Chevalley-Warning threshold")
        ws=tuple(product(range(3),repeat=self.source.inputs));groups={}
        for i,w in enumerate(ws):groups.setdefault(self.low_frequency(w),[]).append(i)
        groups=dict(sorted(groups.items()));mapping=[]
        for indices in groups.values():
            if len(indices)%3:raise ArithmeticError("above-threshold occupied native fiber is not divisible by three")
            mapping.extend(indices)
        inverse=[0]*D
        for packed,original in enumerate(mapping):inverse[original]=packed
        return FiberReference(self,ws,groups,tuple(mapping),tuple(inverse))


@dataclass(frozen=True)
class FiberReference:
    program:BatchFiberProgram
    words:tuple
    groups:dict
    packed_to_original:tuple
    original_to_packed:tuple

    def forward(self,index):
        integer(index,"source basis index")
        if index>=len(self.words):raise ValueError("source index outside cube")
        return self.original_to_packed[index]

    def inverse(self,index):
        integer(index,"packed basis index")
        if index>=len(self.words):raise ValueError("packed index outside cube")
        return self.packed_to_original[index]

    def triple(self,tag):
        integer(tag,"physical measurement tag")
        if tag>=len(self.words)//3:raise ValueError("tag outside complete partition")
        return tuple(self.words[i] for i in self.packed_to_original[3*tag:3*tag+3])

    def child(self,tag):
        words=self.triple(tag);s=self.program.source;H=self.program.prefix_modulus;q=s.modulus
        f=[s.value(w) for w in words]
        if any(tuple(a%H for a in v)!=tuple(a%H for a in f[0]) for v in f[1:]):raise ArithmeticError("triple left its actual native fiber")
        rows=tuple(tuple((a-b)%q//H for a,b in zip(v,f[0])) for v in f[1:])
        return words,f,rows,pointed_minor(words)

    def report(self):
        p=self.program;s=p.source;D=len(self.words);H=p.prefix_modulus;q=s.modulus;child_q=q//H
        tags=D//3;selected=(0,tags//2,tags-1);controls=[];residual=0.0;child_rows=[]
        secrets=[(0,)*s.dimension,(1,)*s.dimension,(3,)*s.dimension,(q-1,)*s.dimension]
        for tag in range(tags):
            words,f,rows,minor=self.child(tag)
            child_rows.append(rows)
            for coordinate in range(s.dimension):
                for endpoint in range(2):
                    if (f[endpoint+1][coordinate]-f[0][coordinate]-H*rows[endpoint][coordinate])%q:raise ArithmeticError("symbolic child phase coefficient failed")
            for secret in secrets:
                actual=np.array([phase(sum(a*b for a,b in zip(v,secret)),q) for v in f])/np.sqrt(D)
                common=phase(sum(a*b for a,b in zip(f[0],secret)),q)/np.sqrt(D)
                predicted=common*np.array([1]+[phase(sum(a*b for a,b in zip(row,secret)),child_q) for row in rows])
                residual=max(residual,float(np.max(abs(actual-predicted))))
            if tag in selected:
                a,b=minor["columns"];R=minor["coefficient_rows"]
                images={((R[0][a]*u+R[0][b]*v)%child_q,(R[1][a]*u+R[1][b]*v)%child_q) for u,v in product(range(child_q),repeat=2)}
                if len(images)!=child_q**2:raise ArithmeticError("conditional high-lift pair map is not bijective")
                controls.append({"tag":tag,"original_words":words,"full_frequencies":f,"child_frequency_rows":rows,
                                 "pointed_unit_minor":minor,"actual_branch_Born_probability":str(Fraction(3,D)),
                                 "complete_two_high_column_lift_cases":child_q**2,
                                 "distinct_child_frequency_pairs_for_each_coordinate":len(images)})
        frequencies=np.array([s.value(w) for w in self.words],dtype=int);mapping=np.array(self.packed_to_original)
        children=np.array(child_rows,dtype=int);mass_residual=0.0
        for secret in secrets:
            state=np.exp(2j*np.pi*(frequencies@secret%q)/q)/np.sqrt(D)
            mapped=state[mapping].reshape(tags,3)
            expected=np.empty_like(mapped);expected[:,0]=state[mapping[::3]]
            expected[:,1:]=expected[:,0,None]*np.exp(2j*np.pi*(children@secret%child_q)/child_q)
            residual=max(residual,float(np.max(abs(mapped-expected))))
            mass_residual=max(mass_residual,float(np.max(abs((abs(mapped)**2).sum(axis=1)-3/D))))
        if max(residual,mass_residual)>3e-12:raise ArithmeticError("full-root physical permutation differs from child phase or Born law")
        digest=hashlib.sha256(json.dumps(self.packed_to_original,separators=(",",":")).encode()).hexdigest()
        return {"dimension":s.dimension,"parent_root_digits":s.level//2,"prefix_digits":p.prefix_digits,"modulus":q,
                "child_modulus":child_q,"original_qutrits":s.inputs,"native_labels":s.labels,"full_frequency_rows":s.frequencies,
                "occupied_fiber_counts":[{"syndrome":S,"count":len(indices)} for S,indices in self.groups.items()],
                "whole_word_reference_count":D,"complete_measurement_tag_count":tags,"complete_partition_sha256":digest,
                "pointed_unit_minors_checked_for_all_tags":tags,"all_original_basis_words_covered_exactly_once":True,
                "output_qutrits_per_input_batch":1,"all_measurement_tags_are_simultaneously_available_child_samples":False,
                "calibration_secrets_only":secrets,"physical_all_tag_phase_residual":residual,
                "complete_permutation_state_replayed":True,"physical_all_tag_Born_mass_residual":mass_residual,
                "selected_tag_controls":controls,"partition_reads_high_frequency_lifts":False,
                "conditional_IID_child_law_is_population_not_fixed_label_histogram":True,
                "independence_between_outputs_from_reused_original_batches_claimed":False,
                "efficient_coherent_partition_implemented":False,"reference_time_and_memory_exponential_in_original_qutrits":True,
                "source_preparation_inverse_or_free_QRAM_supplied":False,"quantum_speedup_proved":False}


def report():
    controls=[]
    for n,r,d,M,seed in ((1,3,2,9,99931),(2,2,1,5,99932),(3,4,1,7,99933)):
        controls.append(BatchFiberProgram(random_even_source(n,2*r,M,seed),d).reference().report())
    polynomial=BatchFiberProgram(random_even_source(1,6,3,99934),2)
    circuit_cases=0
    for word in product(range(3),repeat=3):
        for j in range(2):
            if polynomial.coefficient_digit(word,0,j)!=polynomial.low_frequency(word)[0]//3**j%3:raise ArithmeticError("fixed-loop coefficient circuit differs from actual ring digit")
            circuit_cases+=1
    return {"status":"BATCH_NATIVE_FIBER_EXTRACTION_ARCHITECTURE_REVIEW_PENDING_COMPILER_MISSING",
            "derivation_sha256":hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "candidate_record_accepted":False,"quantum_speedup_proved":False,"novelty_claim":False,
            "efficient_coherent_partition_implemented":False,
            "all_fiber_divisibility_is_existence_not_algorithm":True,
            "polynomial_supply_controls":[batch_ledger(3**r,r,r-1) for r in (2,3,4,5)],
            "native_complete_partition_controls":controls,
            "true_ring_digit_polynomial_controls":[polynomial.reduced_polynomial(0,j) for j in (0,1)],
            "digit_polynomial_control_full_rows":polynomial.source.frequencies,
            "digit_polynomial_control_native_labels":polynomial.source.labels,
            "complete_coefficient_circuit_identity_cases":circuit_cases,
            "lexicographic_basis_compiler_counting_reduction_controls":[lex_rank_reduction(v,clauses) for v,clauses in ((1,((1,),(-1,))),(2,((1,2),)),(1,((1,1,1),)))],
            "falsifiers":["A generated digit polynomial differs from its true native ring digit or exceeds its degree bound.",
                          "An above-threshold occupied fiber is not divisible by3.",
                          "A complete basis permutation duplicates or drops a source word or retains original-index garbage.",
                          "The conditional high-lift minor is nonunit or its source choice uses high lifts.",
                          "An exponential fiber reference is called polynomial-time or possible tags are counted as cloned children."]}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--write",action="store_true");args=parser.parse_args()
    value=report()
    if args.write:REPORT.write_text(json.dumps(value,indent=2,allow_nan=False)+"\n")
    print(json.dumps({"status":value["status"],"complete_native_partitions":3,"output_qutrits_per_batch":1,"efficient_compiler_supplied":False}))


if __name__=="__main__":main()
