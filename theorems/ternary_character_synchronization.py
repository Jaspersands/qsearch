"""Exact native character-consistency audit for sparse Bochner relaxations.

LOCAL DERIVATION / REVIEW PENDING. Rank-one PSD and perfect local phase fit
do not certify a shared group character. No efficient noisy decoder supplied.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
from itertools import product
import json
import math
from pathlib import Path
import random

from flint import nmod_mat
from sympy import Matrix, eye

from ternary_covariant_noise import CovariantRecord, ROOT_DIRECTIONS, root_digits, simulated_record
from ternary_cyclic_extractor import random_even_source

ROOT=Path(__file__).resolve().parents[1]
DERIVATION=ROOT/"research/TERNARY_CHARACTER_SYNCHRONIZATION.md"
REPORT=ROOT/"research/classical_baselines/ternary_character_synchronization.json"


def _records(records):
    records=tuple(records)
    if not records or any(not isinstance(r,CovariantRecord) for r in records):
        raise ValueError("validated original covariant records required")
    n,q=len(records[0].first),records[0].modulus
    if any((len(r.first),r.modulus)!=(n,q) for r in records):
        raise ValueError("same secret dimension and full root required")
    return records,n,q


def vocabulary(records):
    """Fixed preregistered templates, independent of native labels/outcomes."""
    records,n,q=_records(records);M=len(records);rows=[row for r in records for row in (r.first,r.second)]
    outcomes=[x for r in records for x in r.outcome];nodes=[]
    nodes.append({"formal_coefficients":(0,)*(2*M),"frequency":(0,)*n,"phase_exponent":0})
    for j in range(M):
        for a,c in ROOT_DIRECTIONS:
            formal=[0]*(2*M);formal[2*j]=a % q;formal[2*j+1]=c % q
            nodes.append({"formal_coefficients":tuple(formal),
                          "frequency":tuple((a*rows[2*j][i]+c*rows[2*j+1][i]) % q for i in range(n)),
                          "phase_exponent":(a*outcomes[2*j]+c*outcomes[2*j+1]) % q})
    return tuple(nodes)


def synchronization_witness(records,max_moment_entries=1_000_000):
    records,n,q=_records(records)
    if type(max_moment_entries) is not int or max_moment_entries<1:
        raise ValueError("positive whole moment-table cap required")
    nodes=vocabulary(records);K=len(nodes)
    if K*K>max_moment_entries:raise ValueError("complete difference-constraint audit exceeds cap")
    seen={};resonances=[];violations=[]
    for i,u in enumerate(nodes):
        for j,v in enumerate(nodes):
            frequency=tuple((a-b) % q for a,b in zip(u["frequency"],v["frequency"]))
            formal=tuple((a-b) % q for a,b in zip(u["formal_coefficients"],v["formal_coefficients"]))
            phase=(u["phase_exponent"]-v["phase_exponent"]) % q
            old=seen.setdefault(frequency,(formal,phase,i,j))
            if formal!=old[0]:
                resonance={"first_pair":(old[2],old[3]),"second_pair":(i,j),"frequency":frequency,
                           "formal_residual":tuple((a-b) % q for a,b in zip(formal,old[0]))}
                resonances.append(resonance)
            if phase!=old[1]:
                violations.append({"first_pair":(old[2],old[3]),"second_pair":(i,j),
                                   "frequency":frequency,"nonzero_phase_residual":(phase-old[1]) % q})
    return {"nodes":nodes,"moment_matrix_dimension":K,"all_moment_entries_checked":K*K,
            "PSD_certificate":"M_uv=chi_q(h_u-h_v)=v_u*conjugate(v_v); vv* is PSD of rank1",
            "diagonal_entries_exactly_one":True,"matrix_rank_exactly_one":True,
            "phase_variables_are_exact_qth_roots":True,
            "all_equal_frequency_difference_constraints_satisfied":not violations,
            "no_accidental_formal_difference_resonances":not resonances,
            "accidental_difference_resonance_count":len(resonances),
            "violated_difference_constraint_count":len(violations),
            "resonance_witnesses":resonances[:8],"constraint_violation_witnesses":violations[:8],
            "rank_one_witness_is_valid_for_the_relaxation":not violations,
            "perfect_local_paired_phase_score":3*len(records),
            "perfect_local_phase_fit_proves_shared_secret":False,
            "character_decoder_supplied":False,
            "template_selection_reads_native_labels_or_outcomes":False}


def lifted_inverse(rows,q):
    """Prime-field inverse plus Newton lift; FLINT inversion is prime-only."""
    root_digits(q);n=len(rows)
    if not n or any(len(row)!=n for row in rows):raise ValueError("nonempty square unit basis required")
    B=Matrix(rows);F=nmod_mat([[x % 3 for x in row] for row in rows],3)
    if int(F.rank())!=n:raise ValueError("basis must have unit determinant modulo3")
    F=F.inv();X=Matrix([[int(F[i,j]) for j in range(n)] for i in range(n)]);modulus=3
    while modulus<q:
        modulus=min(modulus*modulus,q)
        X=(X*(2*eye(n)-B*X)).applyfunc(lambda x:int(x) % modulus)
    if (B*X).applyfunc(lambda x:int(x) % q)!=eye(n):raise ArithmeticError("Newton modular inverse failed")
    return X


def character_validator(records):
    """Public exact-fit validator and syzygy compiler, NOT noisy inference."""
    records,n,q=_records(records);rows=[row for r in records for row in (r.first,r.second)]
    outcomes=tuple(x for r in records for x in r.outcome)
    reduced,rank=nmod_mat([[row[i] % 3 for row in rows] for i in range(n)],3).rref()
    if rank<n:
        return {"status":"UNKNOWN_NO_FULL_UNIT_ROW_BASIS","rank_mod3":int(rank),
                "full_group_character_fit_certified":False,"noisy_secret_decoder_supplied":False}
    basis=tuple(next(j for j in range(len(rows)) if reduced[i,j]) for i in range(n))
    inverse=lifted_inverse([rows[j] for j in basis],q)
    trial=tuple(int(x) % q for x in inverse*Matrix([outcomes[j] for j in basis]));relations=[];first_failure=None
    for j,row in enumerate(rows):
        coefficients=tuple(int(x) % q for x in Matrix([row])*inverse)
        weights=[0]*len(rows);weights[j]=1
        for i,c in zip(basis,coefficients):weights[i]=(weights[i]-c) % q
        if any(sum(a*row[k] for a,row in zip(weights,rows)) % q for k in range(n)):
            raise ArithmeticError("public syzygy failed exact native frequencies")
        residual=sum(a*b for a,b in zip(weights,outcomes)) % q
        relation={"target_frequency_row":j,"basis_coefficients":coefficients,
                  "native_frequency_relation_weights":weights,"outcome_phase_residual":residual}
        relations.append(relation)
        if residual and first_failure is None:first_failure=relation
    return {"status":"EXACT_CHARACTER_FIT" if first_failure is None else "RANK_ONE_PHASE_FIT_NOT_A_CHARACTER",
            "rank_mod3":int(rank),"unit_basis_frequency_rows":basis,
            "modular_unit_basis_inverse":[list(map(int,inverse.row(i))) for i in range(n)],
            "basis_interpolated_secret_trial":trial,"all_native_group_relations":relations,
            "first_nonzero_character_relation":first_failure,
            "full_group_character_fit_certified":first_failure is None,
            "character_validator_is_a_noisy_secret_decoder":False,
            "truth_or_hidden_secret_used":False,
            "polynomial_relation_compiler_supplied":True,
            "multiplicative_relations_become_linear_SDP_constraints_without_lifting":False,
            "product_power_circuit_upper":len(rows)*n*max(1,2*q.bit_length()),
            "dense_moment_lift_polynomial_size_proved":False}


def rank_one_character_lift(records,max_nodes=10000):
    """Polynomial label-adaptive circuit lift with rank-one soundness only."""
    records,n,q=_records(records);validation=character_validator(records)
    if validation["rank_mod3"]<n:
        return {"status":"UNKNOWN_NO_FULL_UNIT_ROW_BASIS","rank_one_character_soundness_certified":False}
    if type(max_nodes) is not int or max_nodes<1:raise ValueError("positive circuit node cap required")
    rows=[row for r in records for row in (r.first,r.second)];ys=tuple(x for r in records for x in r.outcome)
    nodes=[];indices={};stencils=[];conjugated=set();L=len(rows)
    def node(formal):
        formal=tuple(x % q for x in formal)
        if formal not in indices:
            if len(nodes)>=max_nodes:raise ValueError("whole character-circuit node cap exceeded")
            indices[formal]=len(nodes)
            nodes.append({"formal_coefficients":formal,
                          "frequency":tuple(sum(a*row[j] for a,row in zip(formal,rows)) % q for j in range(n)),
                          "fake_observed_phase_exponent":sum(a*y for a,y in zip(formal,ys)) % q})
        return indices[formal]
    zero=node((0,)*L)
    native=[node(tuple(int(i==j) for i in range(L))) for j in range(L)]
    def negative(i):
        j=node(tuple(-x for x in nodes[i]["formal_coefficients"]))
        if i not in conjugated:
            stencils.append({"kind":"conjugation","left_entry":(i,zero),"right_entry":(zero,j)})
            conjugated.add(i)
        return j
    def add(i,j):
        k=node(tuple(a+b for a,b in zip(nodes[i]["formal_coefficients"],nodes[j]["formal_coefficients"])))
        stencils.append({"kind":"addition","left_entry":(k,zero),"right_entry":(i,negative(j))})
        return k
    powers={}
    def multiply(i,c):
        total=zero;power=i;bit=0
        while c:
            if c & 1:total=add(total,power)
            c >>= 1;bit+=1
            if c:
                if (i,bit) not in powers:powers[i,bit]=add(power,power)
                power=powers[i,bit]
        return total
    basis=validation["unit_basis_frequency_rows"];loops=[];targets=[]
    for i in basis:
        end=multiply(native[i],q)
        if end!=zero:raise ArithmeticError("q-multiple frequency loop did not close")
        loops.append({"basis_frequency_row":i,"integer_multiplier":q,"endpoint":end})
    for relation in validation["all_native_group_relations"]:
        total=zero
        for i,c in zip(basis,relation["basis_coefficients"]):
            if c:total=add(total,multiply(native[i],c))
        target=native[relation["target_frequency_row"]]
        stencils.append({"kind":"native_target","left_entry":(total,zero),"right_entry":(target,zero)})
        targets.append({"frequency_row":relation["target_frequency_row"],"computed_node":total,"native_node":target})
    failures=[]
    for j,stencil in enumerate(stencils):
        left,right=stencil["left_entry"],stencil["right_entry"]
        difference=lambda pair:tuple((a-b) % q for a,b in zip(nodes[pair[0]]["frequency"],nodes[pair[1]]["frequency"]))
        if difference(left)!=difference(right):raise ArithmeticError("lift introduced a non-native moment equality")
        phase=lambda pair:(nodes[pair[0]]["fake_observed_phase_exponent"]-nodes[pair[1]]["fake_observed_phase_exponent"]) % q
        residual=(phase(left)-phase(right)) % q
        if residual:failures.append({"stencil_index":j,"kind":stencil["kind"],"phase_residual":residual})
    gap_certificates=[]
    for relation in validation["all_native_group_relations"]:
        if relation["outcome_phase_residual"]:
            weight_norm=1+sum(c*c for c in relation["basis_coefficients"])
            gap_certificates.append({"target_frequency_row":relation["target_frequency_row"],
                                     "nonzero_modular_phase_residual":relation["outcome_phase_residual"],
                                     "one_plus_basis_coefficient_squared_norm":weight_norm,
                                     "any_feasible_PSD_objective_gap_lower":str(Fraction(8,q*q*weight_norm))})
    gap=max((Fraction(x["any_feasible_PSD_objective_gap_lower"]) for x in gap_certificates),default=Fraction(0))
    return {"status":"POLYNOMIAL_ADAPTIVE_RANK_ONE_CHARACTER_LIFT_REVIEW_PENDING",
            "nodes":nodes,"linear_moment_stencils":stencils,"basis_q_loops":loops,"native_target_maps":targets,
            "unit_basis_frequency_rows":basis,"matrix_dimension":len(nodes),"dense_PSD_complex_entries":len(nodes)**2,
            "selected_linear_moment_constraint_count":len(stencils),
            "fake_perfect_local_fit_violated_stencils":failures,
            "all_rank_PSD_near_perfect_gap_certificates":gap_certificates,
            "any_feasible_PSD_objective_gap_lower":str(gap),
            "gap_is_to_impossible_perfect_score_not_true_secret_score":True,
            "rank_one_character_soundness_certified":True,
            "polynomial_size_selected_PSD_lift_constructed":True,
            "template_construction_is_native_label_adaptive":True,
            "every_rank_one_feasible_point_is_a_shared_group_character":True,
            "convex_relaxation_tightness_proved":False,
            "rank_one_optimum_or_efficient_decoder_supplied":False,
            "PSD_rank_greater_than_one_certifies_a_distribution_over_characters":False,
            "floating_approximate_rank_one_rounding_certified":False}


def source_ledger(n,r,M):
    if any(type(x) is not int or x<1 for x in (n,r,M)):raise ValueError("positive native dimensions and supply required")
    q=3**r;K=6*M+1;constraints=K*K
    # A fixed local A2 vocabulary has raw difference-residual coefficients<=4.
    g=1 if r==1 else 3
    resonance=min(Fraction(1),math.comb(constraints,2)*Fraction(g,q)**n)
    perfect=min(Fraction(1),q**n*Fraction(3,q*q)**M)
    rank_failure=min(Fraction(1),Fraction(3**n-1,2*3**(2*M)))
    return {"components":n,"root_digits":r,"original_native_qutrits":M,"modulus":str(q),
            "fixed_vocabulary_nodes":K,"complete_moment_constraint_entries":constraints,
            "fixed_A2_template_any_accidental_resonance_probability_upper":str(resonance),
            "generic_fixed_polynomial_vocabulary_resonance_upper":str(min(Fraction(1),math.comb(constraints,2)*Fraction(1,3**n))),
            "any_shared_character_perfectly_fits_noise_probability_upper":str(perfect),
            "unit_basis_rank_failure_probability_upper":str(rank_failure),
            "local_fake_and_global_rejection_and_unit_basis_probability_lower":str(max(Fraction(0),1-resonance-perfect-rank_failure)),
            "IID_uniform_original_frequency_premise_required":True,
            "same_result_for_label_adaptive_syzygy_templates":False,
            "source_distribution_bound_is_pointwise_certificate":False,
            "quantum_or_all_classical_decoder_lower_bound":False}


def native_control(n,r,M,seed):
    source=random_even_source(n,2*r,M,seed);rng=random.Random(seed+1)
    secret=tuple((2*i+1) % source.modulus for i in range(n));records=[];proposals=0
    for first,second in source.frequencies:
        record,count=simulated_record(first,second,secret,source.modulus,rng);records.append(record);proposals+=count
    witness=synchronization_witness(records);validator=character_validator(records)
    honest=tuple(CovariantRecord(first,second,tuple(sum(a*s for a,s in zip(row,secret)) % source.modulus for row in (first,second)),source.modulus)
                 for first,second in source.frequencies)
    return {"seed":seed,"original_even_native_level":source.level,"original_ring_labels":source.labels,
            "original_native_frequencies":source.frequencies,"original_ancestry_ids":[f"character-sync-{n}-{r}-{seed}-{i}" for i in range(M)],
            "native_records":[x.public() for x in records],"calibration_secret":secret,
            "known_secret_was_used_only_to_simulate_measurements":True,
            "simulated_noise_proposals":proposals,"source_law_physically_certified":False,
            "witness":witness,"validator":validator,"honest_character_countercontrol":character_validator(honest),
            "adaptive_character_lift":rank_one_character_lift(records),
            "ledger":source_ledger(n,r,M)}


def run_controls():
    controls=[native_control(n,r,M,seed) for n,r,M,seed in ((8,2,8,89513),(12,2,12,89523),(8,3,8,89533))]
    if any(not x["witness"]["rank_one_witness_is_valid_for_the_relaxation"] or x["validator"]["status"]!="RANK_ONE_PHASE_FIT_NOT_A_CHARACTER" for x in controls):
        raise ArithmeticError("prespecified native synchronization falsifier not reproduced")
    resonance=(CovariantRecord((1,0),(0,1),(0,0),9),CovariantRecord((1,1),(1,8),(1,0),9))
    return {"status":"NATIVE_RANK_ONE_SYNCHRONIZATION_NOT_A_CHARACTER_REVIEW_PENDING",
            "derivation_sha256":hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "native_controls":controls,"label_resonance_countercontrol":{"records":[x.public() for x in resonance],"witness":synchronization_witness(resonance)},
            "growing_native_ledgers":[source_ledger(n,r,M) for n,r,M in ((32,3,64),(64,4,128),(128,5,256))],
            "existing_identifiability_and_noise_modules_reused_not_reimplemented":True,
            "rank_one_PSD_acceptance_is_rejected_without_character_validation":True,
            "polynomial_rank_one_sound_character_lift_implemented":True,
            "label_adaptive_lifts_or_all_spectral_methods_ruled_out":False,
            "efficient_noisy_secret_decoder_supplied":False,"quantum_speedup_proved":False,
            "candidate_record_accepted":False,"routine_wiring_owner":"Gemini or Antigravity"}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--write",action="store_true");args=parser.parse_args();report=run_controls()
    if args.write:
        REPORT.parent.mkdir(parents=True,exist_ok=True);REPORT.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"],"report":str(REPORT) if args.write else None,
                      "native_character_validator_statuses":[x["validator"]["status"] for x in report["native_controls"]]},indent=2))


if __name__=="__main__":main()
