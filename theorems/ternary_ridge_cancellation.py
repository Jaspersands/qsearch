"""Depth-independent low-ridge cancellation on real native phase programs.

LOCAL DERIVATION / REVIEW PENDING. A source-accounted degree-drop factory,
not a full-root decoder or new speedup. IID input supply is an external premise.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import product
import json
import math
from pathlib import Path

from flint import nmod_mat

from cyclotomic_fiber_receiver import inverse_frequency_coordinates, native_source
from ternary_correlated_packet_acquisition import PacketAcquisition, integer
from ternary_cyclic_extractor import random_even_source
from ternary_native_phase_identity import NativeProgram, injection_control, merge, test_identity
from ternary_quadratic_program_receiver import nullspace

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/TERNARY_RIDGE_CANCELLATION.md"
REPORT = ROOT / "research/phase_workbench/ternary_ridge_cancellation.json"


def cohort_ledger(n,d):
    integer(n,"secret components",1);integer(d,"logical width",1)
    P = (3**d-1)//2;bound = n*(P-d);B = bound+1
    return {"components":n,"logical_width":d,"ambient_projective_forms":str(P),
            "signature_space_dimension_upper":str(bound),"guaranteed_cohort_programs":str(B),
            "original_inputs_per_program":(n+d)*(n+1)**2,
            "full_original_input_cap":str(B*(n+d)*(n+1)**2),
            "source_cap_depends_on_phase_depth":False,
            "ambient_width_dependence_exponential":True,
            "polynomial_when_width_O_log_n":True,"one_coordinate_stage_is_trivial":d==1,
            "decoder_or_full_depth_speedup_supplied":False}


def low_relation(programs):
    programs = tuple(programs)
    if not programs: raise ValueError("nonempty acquired native cohort required")
    phases = tuple(p.compact() for p in programs);first = phases[0]
    if any((p.width,p.components,p.phase_digits)!=(first.width,first.components,first.phase_digits) for p in phases):
        raise ValueError("same width, component count and retained modulus required")
    ids = [x for p in programs for x in p.source_ids]
    if len(set(ids)) != len(ids): raise ValueError("disjoint original source ancestry required")
    dictionaries = [{direction:tuple(row[1] % 3 for row in tables) for direction,tables in phase.groups
                     if any(row[1] % 3 for row in tables)} for phase in phases]
    keys = tuple(sorted({direction for dictionary in dictionaries for direction in dictionary}))
    n,d,B = first.components,first.width,len(programs)
    rows = [[dictionary.get(direction,(0,)*n)[l] for dictionary in dictionaries] for l in range(n) for direction in keys]
    span = int(nmod_mat([[direction[j] for direction in keys] for j in range(d)],3).rank()) if keys else 0
    signature_rank = int(nmod_mat(rows,3).rank()) if rows else 0
    observed_bound = n*(len(keys)-span)
    ambient_bound = n*((3**d-1)//2-d)
    if signature_rank > observed_bound or observed_bound > ambient_bound:
        raise ArithmeticError("native signatures violate global-kernel dimension bound")
    kernel = nullspace(rows,B)
    if not kernel: raise ValueError("no relation in supplied cohort; no unsupported sparse-dictionary promise")
    # More support exercises genuine combinations when already-restricted inputs
    # coexist; this policy still reads low signatures only.
    c = max(kernel,key=lambda v:sum(bool(x) for x in v))
    if not any(c) or any(sum(a*b for a,b in zip(row,c)) % 3 for row in rows):
        raise ArithmeticError("incorrect projective signature relation")
    record = {"coefficients":c,"selection_policy":"maximum-support-nullspace-basis-vector-low-only",
              "signature_rows":[{"component":l,"direction":direction,"program_coefficients":rows[l*len(keys)+k]}
                                for l in range(n) for k,direction in enumerate(keys)],
              "occupied_signature_directions":keys,"occupied_direction_span_rank":span,
              "signature_matrix_rank":signature_rank,"observed_signature_space_dimension_upper":observed_bound,
              "ambient_signature_space_dimension_upper":str(ambient_bound),
              "guaranteed_cohort_programs":str(ambient_bound+1),"cohort_programs_charged":B,
              "reads_only_native_low_signature_residues":True,
              "high_frequency_digits_or_measured_injection_words_read_for_selection":False,
              "sparse_occupied_bound_guarantees_future_cohorts":False,
              "all_ambient_projective_forms_materialized":False,
              "selected_inputs_include_nonzero_low_signature":any(dictionaries[j] for j,x in enumerate(c) if x)}
    return c,record


def cancel(programs,outcomes):
    programs = tuple(programs);c,relation = low_relation(programs)
    phase,record = merge(programs,c,outcomes)
    if any(x % 3 for _,tables in phase.groups for row in tables for x in row):
        raise ArithmeticError("low relation failed exact per-ridge divisibility for observed transcript")
    certificate = phase.degree_certificate()
    if certificate["certified_global_degree_upper"] > 2*phase.phase_digits:
        raise ArithmeticError("source-accounted degree-drop certificate failed")
    n,d = phase.components,phase.width
    record.update({"low_relation":relation,"degree_certificate":certificate,
                   "per_ridge_denominator_division_admitted":True,
                   "all_transcript_guarantee":"translated low coefficient is c_j*a_j independently of measurement",
                   "source_law_status":"LOCAL_DERIVATION_UNDER_IID_INPUT_PREMISE_REVIEW_PENDING",
                   "physical_source_IID_premise_verified":False,
                   "uniform_linear_coefficient_law_is_mod3_only":True,
                   "efficient_low_degree_drop_relation_search_supplied":True,
                   "conditional_full_phase_order_loss_upper":str(Fraction(1,3**(n*d))),
                   "full_phase_order_of_every_branch_guaranteed":False,
                   "full_root_secret_identifiability_proved":False,
                   "ordinary_field3_readout_or_phase_power_oracle_supplied":False})
    return phase,record


def native_cohort(n,d,r,seed,max_programs=1000):
    integer(r,"retained phase digits",1);integer(max_programs,"calibration program cap",1)
    ledger = cohort_ledger(n,d);B = int(ledger["guaranteed_cohort_programs"])
    if B > max_programs: raise ValueError("calibration preflight cap exceeded; no partial source returned")
    M = ledger["original_inputs_per_program"];programs = []
    for j in range(B):
        source = random_even_source(n,2*r+2,M,seed+j)
        acquisition = PacketAcquisition.from_source(source,n+d,
            tuple(f"ridge-cancel-{n}-{d}-{r}-{seed}-{j}-{i}" for i in range(M)),M)
        pointers = tuple((seed+j+i) % 3 for i in range(len(acquisition.pointers)))
        initial = acquisition.branch(pointers)
        syndrome = tuple((seed+j+i+1) % 3 for i in range(len(initial.packet.pivots)))
        branch = acquisition.branch(pointers,syndrome)
        complement = tuple((seed+j+i+2) % 3 for i in range(branch.packet.retained-d))
        programs.append(NativeProgram(branch,d,complement))
    return tuple(programs)


def linear_lift_census(programs,outcomes):
    """Vary one selected program's true original pivots, not an unknown state."""
    c,_ = low_relation(programs);j = next(i for i,x in enumerate(c) if x)
    program = programs[j];acquisition = program.branch.acquisition;source = acquisition.source
    K = len(acquisition.supports);d = program.width
    if K > 5: raise ValueError("complete original-pivot census capped at five odd inputs")
    baseline,_ = cancel(programs,outcomes);points = tuple(product(range(3),repeat=d))
    baseline_table = [baseline.value(z) for z in points]
    q = source.modulus;counts = Counter();records = []
    for increments in product(range(3),repeat=K):
        labels = [list(row) for row in source.labels]
        for support,h in zip(acquisition.supports,increments):
            i = support[0];a,b = (row[0] for row in source.frequencies[i])
            labels[i][0] = inverse_frequency_coordinates((a+3*h) % q,(b+6*h) % q,source.level)
        new_source = native_source(labels,source.level)
        new = PacketAcquisition.from_source(new_source,K,acquisition.source_ids,source.inputs)
        if new.supports != acquisition.supports: raise ArithmeticError("alpha lift changed low support selection")
        pointers = tuple(program.branch.anchor[i] for i in acquisition.pointers)
        branch = new.branch(pointers,program.branch.packet.syndrome)
        cohort = list(programs);cohort[j] = NativeProgram(branch,d,program.complement)
        actual,r = cancel(cohort,outcomes)
        if tuple(r["coefficients"]) != c: raise ArithmeticError("alpha altered low-only relation")
        differences = [tuple((a-b) % 3 for a,b in zip(actual.value(z),old)) for z,old in zip(points,baseline_table)]
        beta = tuple(differences[points.index(tuple(int(i==k) for i in range(d)))][0] for k in range(d))
        if any(delta != (sum(a*b for a,b in zip(beta,z)) % 3,)+(0,)*(actual.components-1) for z,delta in zip(points,differences)):
            raise ArithmeticError("native alpha variation is not purely linear modulo3")
        counts[beta] += 1
        records.append({"original_pivot_lifts":increments,"component_zero_linear_change_mod3":beta})
    if len(counts)!=3**d or set(counts.values())!={3**(K-d)}:
        raise ArithmeticError("native full-column-rank frame failed uniform linear coefficient law")
    return {"varied_program":j,"component":0,"retained_phase_digits":program.phase_digits,
            "complete_original_high_lifts":3**K,"width":d,"odd_inputs":K,
            "linear_change_multiplicity":3**(K-d),"records":records,
            "finite_census_certifies_physical_IID_premise":False,
            "virtual_lifts_are_additional_quantum_samples":False}


def lowest_digit_readout(phase,max_words=729):
    """Ideal program-only optimum with uniform unknown higher secret digits."""
    integer(max_words,"coarse-fiber calibration cap",1);D = 3**phase.width
    if D > max_words: raise ValueError("coarse readout is a bounded reference, not an efficient fiber compiler")
    q,H,g = phase.modulus,phase.modulus//3,3**phase.components
    fibers = {}
    for z in product(range(3),repeat=phase.width):
        value = phase.value(z);key = tuple(x % H for x in value)
        fibers.setdefault(key,[]).append((z,value))
    records = [];numerator = 0.;collisions = 0
    for key,words in sorted(fibers.items()):
        base = words[0][1];counts = Counter(tuple(((x-b) % q)//H for x,b in zip(value,base)) for _,value in words)
        radical_sum = sum(math.sqrt(count) for count in counts.values());numerator += radical_sum**2
        k = len(words);collisions += k*(k-1)
        records.append({"coarse_frequency":key,"fiber_words":tuple(z for z,_ in words),
                        "fine_label_counts":[{"label":label,"count":count} for label,count in sorted(counts.items())]})
    return {"secret_prior":"uniform s0 in F3^n and shared higher digits in Z_(q/3)^n",
            "program_dimension":D,"coarse_modulus":str(H),"secret_digit_outcomes":str(g),
            "coarse_fibers":records,"ordered_distinct_coarse_collisions":collisions,
            "ideal_optimal_lowest_digit_success":numerator/(g*D),
            "chance_success":str(Fraction(1,g)),
            "fixed_instance_success_advantage_upper":str(min(Fraction(g-1,g),Fraction(collisions,g*D))),
            "reference_only_not_efficient_measurement_implementation":True,
            "other_live_original_registers_excluded":True,
            "high_secret_twirl_not_tensor_of_independent_per_program_twirls":True}


def program_only_population_bound(n,d,r,copies=1):
    integer(n,"components",1);integer(d,"width",1);integer(r,"phase digits",1);integer(copies,"outputs",0)
    D,g,q = 3**(d*copies),3**n,3**r
    return {"components":n,"width":d,"phase_digits":r,"independent_original_cohorts":copies,
            "joint_program_dimension":str(D),"chance_success":str(Fraction(1,g)),
            "mean_optimal_lowest_digit_advantage_upper":str(min(Fraction(g-1,g),Fraction(D-1,q**n))),
            "population_bound_applies_to_each_fixed_instance":False,
            "same_shared_higher_secret_across_outputs":True,
            "original_IID_and_low_only_policy_premise_required":True,
            "all_collective_measurements_on_the_stated_outputs_covered":True,
            "unused_original_registers_or_additional_outputs_covered":False,
            "efficient_collective_receiver_supplied":False}


def run_controls():
    controls = []
    for n,d,r,seed in ((1,1,1,89001),(1,2,1,89128),(1,2,2,89128),(2,3,3,89031)):
        programs = native_cohort(n,d,r,seed);c,_ = low_relation(programs)
        selected = tuple(j for j,x in enumerate(c) if x)
        outcomes = tuple(tuple((seed+j+i) % 3 for i in range(d)) for j in selected)
        phase,record = cancel(programs,outcomes);points = tuple(product(range(3),repeat=d))
        table = [phase.value(z) for z in points]
        for j,p in enumerate(programs):
            if any(p.compact().value(z)!=p.original_value(z) for z in points): raise ArithmeticError("original phase mismatch")
        family_gcd = math.gcd(phase.modulus,*(x for row in table for x in row))
        unit = next(({"word":z,"component":l,"frequency":x} for z,row in zip(points,table) for l,x in enumerate(row) if x % 3),None)
        record.update({"seed":seed,"calibration_kind":"prespecified-native-cohort-not-population-estimate",
                       "ledger":cohort_ledger(n,d),"complete_frequency_table":table,
                       "complete_original_word_checks":len(programs)*len(points),
                       "component_frequency_family_order":str(phase.modulus//family_gcd),
                       "unit_frequency_word_witness":unit,
                       "one_coordinate_control_is_trivial":d==1,
                       "top_degree_identity":test_identity(phase,2*r+1,seed=seed),
                       "quadratic_transfer_probe":test_identity(phase,3,seed=seed+100),
                       "program_only_lowest_digit_readout":lowest_digit_readout(phase),
                       "program_only_population_bound":program_only_population_bound(n,d,r),
                       "physical_injection_controls":[injection_control(programs[j],c[j],tuple((phase.modulus-1-l) % phase.modulus for l in range(n))) for j in selected]})
        if n==1 and d==2 and r==2: record["original_linear_source_census"] = linear_lift_census(programs,outcomes)
        controls.append(record)
    return {"status":"DEPTH_INDEPENDENT_LOW_RIDGE_CANCELLATION_FACTORY_REVIEW_PENDING",
            "derivation_sha256":hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "native_controls":controls,"cohort_ledgers":[cohort_ledger(n,d) for n,d in ((1,1),(8,2),(32,3),(32,8),(32,16),(32,32))],
            "candidate_record_accepted":False,"full_root_decoder_supplied":False,
            "quantum_speedup_proved":False,"routine_wiring_owner":"Gemini or Antigravity"}


def main():
    parser = argparse.ArgumentParser(description=__doc__);parser.add_argument("--write",action="store_true");args=parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.parent.mkdir(parents=True,exist_ok=True);REPORT.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"],"report":str(REPORT) if args.write else None,
                      "control_selected_programs":[len(c["selected_program_indices"]) for c in report["native_controls"]]},indent=2))


if __name__=="__main__":main()
