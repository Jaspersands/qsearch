"""Costed collective frequency evaluation with exact character feedforward.

LOCAL DERIVATION / REVIEW PENDING. A concrete, falsified receiver route, not
a general decoding lower bound. Original physical IID supply is a premise.
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
import numpy as np

from ternary_correlated_packet_acquisition import integer
from ternary_quadratic_program_receiver import nullspace
from ternary_ridge_cancellation import cancel, cohort_ledger, low_relation, native_cohort

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/TERNARY_COLLECTIVE_CHARACTER_RECEIVER.md"
REPORT = ROOT / "research/phase_workbench/ternary_collective_character_receiver.json"


def rank(rows, columns):
    return int(nmod_mat(rows, 3).rank()) if rows and columns else 0


def _family(phases):
    phases = tuple(phases)
    if not phases:
        raise ValueError("nonempty phase family required")
    p = phases[0]
    if any((x.width, x.components, x.modulus) != (p.width, p.components, p.modulus) for x in phases):
        raise ValueError("equal widths, secret dimensions and retained roots required")
    return phases, p.width, p.components, p.modulus


def character_corrections(phases, max_words_per_program=729):
    """Complete correction image if public frequencies span the full ring.

    This enumerates each LOCAL alphabet, not the collective product alphabet.
    At width O(log n), its table/rank work is polynomial in the supplied data.
    Completeness additionally needs the verified mod3 quadratic phase class.
    """
    phases, d, n, q = _family(phases)
    integer(max_words_per_program, "local table cap", 1)
    if 3**d > max_words_per_program:
        raise ValueError("local character audit cap exceeded")
    words = tuple(product(range(3), repeat=d))
    points = tuple(tuple(int(i == j) for i in range(d)) for j in range(d))
    tables, matrices, linears, rows = [], [], [], []
    for phase in phases:
        table = {z: phase.value(z) for z in words}
        if table[(0,)*d] != (0,)*n:
            raise ValueError("normalized phase at the zero word required")
        linear, diagonal, cross = [], [], []
        for l in range(n):
            squares = tuple(2*(table[tuple(2*x for x in e)][l]-2*table[e][l]) % 3 for e in points)
            beta = tuple((table[e][l]-a) % 3 for e, a in zip(points, squares))
            mixed = {(i, j): (table[tuple(a+b for a,b in zip(points[i],points[j]))][l]
                     -table[points[i]][l]-table[points[j]][l]) % 3 for i in range(d) for j in range(i+1,d)}
            for z, value in table.items():
                fitted = sum(b*x+a*x*x for x,b,a in zip(z,beta,squares))
                fitted += sum(a*z[i]*z[j] for (i,j),a in mixed.items())
                if fitted % 3 != value[l] % 3:
                    raise ValueError("mod3 phase is not ordinary quadratic; class certificate rejected")
            linear.append(beta); diagonal.append(squares); cross.append(mixed)
        quadratic_rows = [tuple(diagonal[l][i] for l in range(n)) for i in range(d)]
        quadratic_rows += [tuple(cross[l][i,j] for l in range(n)) for i in range(d) for j in range(i+1,d)]
        matrices.append(quadratic_rows); linears.append(tuple(linear)); rows.extend(quadratic_rows)
        tables.append(tuple(table[z] for z in words))
    frequencies = [tuple(x % 3 for x in value) for table in tables for value in table]
    span = rank(frequencies, n)
    kernel = nullspace(rows, n)
    characters = [tuple(sum(a[l]*linear[l][j] for l in range(n)) % 3
                        for linear in linears for j in range(d)) for a in kernel]
    image_rank = rank(characters, d*len(phases))
    complete = span == n
    if complete and image_rank != len(kernel):
        raise ArithmeticError("full-frequency-span character map must be injective")
    image_basis, correction_basis = [], []
    for a, t in zip(kernel, characters):
        if rank(image_basis+[t], d*len(phases)) > len(image_basis):
            image_basis.append(t); correction_basis.append(a)
    return {"public_frequency_span_rank_mod3": span, "secret_components": n,
            "complete_correction_image_certified": complete,
            "full_ring_span_follows_from_mod3_span": complete,
            "mod3_quadratic_class_exhaustively_checked_locally": True,
            "program_quadratic_rows": matrices, "program_linear_rows": linears,
            "order_three_secret_correction_basis": kernel,
            "word_character_basis": image_basis, "word_character_image_rank": image_rank,
            "implemented_rescuable_erasure_outcomes": str(3**image_rank),
            "all_exact_rescuable_erasure_outcomes": str(3**image_rank) if complete else None,
            "full_root_secret_corrections": [tuple((q//3)*x for x in a) for a in correction_basis],
            "joint_correct_and_accepted_probability": str(Fraction(3**image_rank, q**n)),
            "universal_exact_character_feedforward_ceiling": str(Fraction(3**n, q**n)),
            "incomplete_span_case_is_not_reported_as_complete": True,
            "approximate_or_noncharacter_outcome_corrections_ruled_out": False,
            "local_words_evaluated": len(phases)*3**d,
            "joint_word_table_used_for_character_search": False,
            "complete_frequency_tables": tables}


def joint_fiber_reference(phases, max_joint_words=729):
    """Bounded exact joint reference, with one SHARED higher secret."""
    phases, d, n, q = _family(phases)
    integer(max_joint_words, "joint reference cap", 1)
    D = 3**(d*len(phases)); G = q**n; H = q//3; g = 3**n
    if D > max_joint_words:
        raise ValueError("joint reference is exponential; calibration cap exceeded")
    words = tuple(product(range(3), repeat=d*len(phases)))
    values = []
    for z in words:
        blocks = [p.value(z[i*d:(i+1)*d]) for i,p in enumerate(phases)]
        values.append(tuple(sum(v[l] for v in blocks) % q for l in range(n)))
    counts = Counter(values)
    coarse = {}
    for z,v in zip(words,values):
        coarse.setdefault(tuple(x % H for x in v), []).append((z,v))
    records = []; digit_numerator = 0.
    for key, entries in sorted(coarse.items()):
        base = entries[0][1]
        fine = Counter(tuple(((a-b) % q)//H for a,b in zip(v,base)) for _,v in entries)
        digit_numerator += sum(math.sqrt(k) for k in fine.values())**2
        records.append({"coarse_frequency":key, "fine_counts":[{"label":k,"count":v} for k,v in sorted(fine.items())]})
    sum_squares = sum(c*c for c in counts.values())
    chi2 = Fraction(G*sum_squares, D*D)-1
    herald = Fraction(sum_squares, D*D)
    return {"programs":len(phases), "width_per_program":d, "components":n,
            "phase_modulus":str(q), "joint_words":words, "joint_frequencies":values,
            "joint_dimension":D, "full_secret_count":str(G),
            "frequency_counts":[{"frequency":v,"count":c} for v,c in sorted(counts.items())],
            "coarse_fibers":records, "frequency_chi_square_from_uniform":str(chi2),
            "ideal_full_secret_PGM_success":sum(math.sqrt(c) for c in counts.values())**2/(G*D),
            "ideal_lowest_digit_success_shared_high_secret":digit_numerator/(g*D),
            "zero_erasure_herald_probability":str(herald),
            "zero_erasure_conditional_correct_probability":str(1/(G*herald)),
            "zero_erasure_joint_correct_probability":str(Fraction(1,G)),
            "exact_reference_not_efficient_fiber_compiler":True,
            "independent_high_secret_twirl_per_program_used":False}


def instrument_replay(reference, corrections, secret):
    """Actually execute erasure amplitudes, not only the count formula."""
    n = reference["components"]; q = int(reference["phase_modulus"])
    if len(secret) != n or any(type(x) is not int or not 0 <= x < q for x in secret):
        raise ValueError("canonical full-root secret required")
    words = reference["joint_words"]; values = reference["joint_frequencies"]
    D = len(words); G = q**n
    pairs = [((0,)*len(words[0]), (0,)*n)]
    pairs += list(zip(corrections["word_character_basis"], corrections["full_root_secret_corrections"]))
    branches = []
    for t, delta in pairs:
        amplitudes = {}
        for z,v in zip(words,values):
            angle = sum(a*b for a,b in zip(secret,v))/q-sum(a*b for a,b in zip(t,z))/3
            amplitudes[v] = amplitudes.get(v, 0j)+np.exp(2j*math.pi*angle)/D
        mass = sum(abs(a)**2 for a in amplitudes.values())
        output = tuple((a-b) % q for a,b in zip(secret,delta))
        amplitude = sum(a*np.exp(-2j*math.pi*sum(x*y for x,y in zip(output,v))/q)
                        for v,a in amplitudes.items())/math.sqrt(G)
        correct = abs(amplitude)**2
        if abs(mass-float(Fraction(reference["zero_erasure_herald_probability"]))) > 2e-10 or abs(correct-1/G) > 2e-10:
            raise ArithmeticError("actual erasure/Fourier branch disagrees with exact character law")
        branches.append({"erasure_word":t,"secret_correction":delta,"group_Fourier_output":output,
                         "herald_probability":mass,"joint_correct_probability":correct})
    return {"full_root_secret":secret,"branches":branches,
            "nonbasis_character_combinations_checked_by_linear_character_identity":True,
            "unknown_state_preparation_inverse_used":False,
            "reference_only_not_scalable_statevector_implementation":True}


def all_outcome_likelihood_reference(phases, max_entries=1_000_000):
    """Exact product-Fourier measurement with exponential classical MAP.

    Keeping every (frequency Fourier, word Fourier) outcome avoids the herald
    cost. A shared public frequency shift just translates the secret prior;
    the same mean MAP success is attained by plain local word Fourier readout.
    No polynomial-time likelihood maximizer is provided.
    """
    phases,d,n,q = _family(phases);integer(max_entries,"likelihood reference cap",1)
    D = 3**(d*len(phases));G=q**n
    if D*G > max_entries:
        raise ValueError("classical MAP enumerates all secrets and joint outcomes; reference cap exceeded")
    local_words = np.array(tuple(product(range(3),repeat=d)),dtype=np.int64)
    secrets = tuple(product(range(q),repeat=n)); secret_array=np.array(secrets,dtype=np.int64)
    word_fourier=np.exp(-2j*math.pi*(local_words@local_words.T % 3)/3)
    distributions=[]
    for phase in phases:
        table=np.array([phase.value(tuple(map(int,z))) for z in local_words],dtype=np.int64)
        states=np.exp(2j*math.pi*(secret_array@table.T % q)/q)
        probability=abs(states@word_fourier.T/len(local_words))**2
        if not np.allclose(probability.sum(axis=1),1,atol=2e-10):
            raise ArithmeticError("local Fourier likelihood failed normalization")
        distributions.append(probability)
    outcomes=tuple(product(range(len(local_words)),repeat=len(phases)))
    maxima=[]; total=0.
    for t in outcomes:
        likelihood=np.ones(G)
        for j,outcome in enumerate(t):likelihood*=distributions[j][:,outcome]
        arg=int(np.argmax(likelihood)); p=float(likelihood[arg]);total+=p
        maxima.append({"local_word_Fourier_outcomes":[tuple(map(int,local_words[i])) for i in t],
                       "maximizing_shifted_secret":secrets[arg],"maximum_likelihood":p})
    return {"mean_all_outcome_classical_MAP_success":total/G,
            "secret_prior":"uniform full-root secret",
            "local_Fourier_measurement_is_efficient":True,
            "public_shared_frequency_shift_changes_uniform_prior_MAP_success":False,
            "all_erasure_outcomes_used_not_only_exact_characters":True,
            "classical_maximization_enumerates_all_secrets":True,
            "polynomial_time_classical_likelihood_optimizer_supplied":False,
            "secret_hypotheses_enumerated":str(G),"joint_outcomes_enumerated":D,
            "local_likelihood_probability_tables":len(phases)*G*3**d,
            "MAP_witnesses":maxima,"measurement_reference_not_candidate":True}


def scaling_ledger(n,d,r,outputs):
    for x,name in ((n,"components"),(d,"width"),(r,"phase digits"),(outputs,"outputs")):
        integer(x,name,1)
    G = 3**(n*r); D = 3**(d*outputs)
    source = int(cohort_ledger(n,d)["full_original_input_cap"])*outputs
    return {"components":n,"width":d,"phase_digits":r,"outputs":outputs,
            "joint_dimension":str(D),"full_secret_count":str(G),
            "provided_original_inputs_per_attempt":str(source),
            "mean_ideal_PGM_failure_upper_under_IID_source":str(min(Fraction(1),Fraction(G-1,D))),
            "population_bound_is_fixed_instance_certificate":False,
            "uncorrected_erasure_joint_success":str(Fraction(1,G)),
            "uncorrected_expected_fresh_original_inputs_per_correct_readout":str(source*G),
            "reciprocal_yield_is_a_correctness_flag_or_stopping_rule":False,
            "best_exact_character_feedforward_joint_success_ceiling":str(Fraction(3**n,G)),
            "ideal_PGM_is_an_implemented_efficient_receiver":False,
            "one_use_unknown_source_reflection_or_inverse_granted":False,
            "all_outcome_classical_inference_ruled_out_by_character_ceiling":False}


def run_controls():
    controls = []
    for n,d,r,seeds in ((1,1,1,(89000,)),(1,1,2,(89000,)),
                        (1,1,2,(89001,89002)),(1,2,2,(89128,89131)),(2,3,3,(89031,89103))):
        phases = []; sources = []; all_ids = []
        for seed in seeds:
            programs = native_cohort(n,d,r,seed); c,_ = low_relation(programs)
            outcomes = tuple(tuple((seed+j+i) % 3 for i in range(d)) for j,x in enumerate(c) if x)
            phase, record = cancel(programs,outcomes); phases.append(phase)
            all_ids += [x for p in programs for x in p.source_ids]
            sources.append({"seed":seed,"source_cap":record["full_original_input_cap_charged"],
                            "original_ancestry_ids":[x for p in programs for x in p.source_ids],
                            "public_phase":phase.record(),"source_premise_physically_certified":False})
        if len(set(all_ids)) != len(all_ids):
            raise ArithmeticError("independent cohort control reused known original ancestry")
        correction = character_corrections(phases); reference = joint_fiber_reference(phases)
        likelihood=all_outcome_likelihood_reference(phases)
        if likelihood["mean_all_outcome_classical_MAP_success"] > reference["ideal_full_secret_PGM_success"]+2e-10:
            raise ArithmeticError("classical measurement MAP cannot beat optimal collective PGM")
        controls.append({"source_cohorts":sources,"corrections":correction,"joint_reference":reference,
                         "all_outcome_likelihood_reference":likelihood,
                         "instrument_replay":instrument_replay(reference,correction,tuple((3**r-1-i) % 3**r for i in range(n))),
                         "ledger":scaling_ledger(n,d,r,len(seeds))})
    return {"status":"COLLECTIVE_CHARACTER_FEEDFORWARD_COSTED_NEGATIVE_REVIEW_PENDING",
            "derivation_sha256":hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "native_controls":controls,
            "scaling_ledgers":[scaling_ledger(n,d,r,B) for n,d,r,B in ((8,2,3,15),(32,3,4,45),(128,5,5,130),(256,6,8,345))],
            "exact_character_feedforward_subsystem_implemented":True,
            "general_collective_receiver_ruled_out":False,"quantum_speedup_proved":False,
            "candidate_record_accepted":False,"routine_wiring_owner":"Gemini or Antigravity"}


def main():
    parser = argparse.ArgumentParser(description=__doc__);parser.add_argument("--write",action="store_true")
    args = parser.parse_args(); report = run_controls()
    if args.write:
        REPORT.parent.mkdir(parents=True,exist_ok=True);REPORT.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"],"report":str(REPORT) if args.write else None,
                      "native_control_character_ranks":[x["corrections"]["word_character_image_rank"] for x in report["native_controls"]]},indent=2))


if __name__ == "__main__": main()
