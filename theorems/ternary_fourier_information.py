"""Source-aware information cost of local Fourier reads of ridge outputs.

LOCAL DERIVATION / REVIEW PENDING. A measurement-specific information bound,
not a classical simulation, computational lower bound or collective no-go.
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

from cyclotomic_fiber_receiver import inverse_frequency_coordinates, native_source
from ternary_correlated_packet_acquisition import PacketAcquisition, integer
from ternary_native_phase_identity import NativeProgram
from ternary_ridge_cancellation import cancel, low_relation, native_cohort

ROOT=Path(__file__).resolve().parents[1]
DERIVATION=ROOT/"research/TERNARY_FOURIER_INFORMATION.md"
REPORT=ROOT/"research/phase_workbench/ternary_fourier_information.json"


def physical_directions(programs, coefficients):
    if len(programs)!=len(coefficients) or not any(coefficients):
        raise ValueError("nonempty matched selected native cohort required")
    d=programs[0].width;keys=set();frames=[]
    for p,c in zip(programs,coefficients):
        if c not in (0,1,2) or p.width!=d:raise ValueError("canonical native domain signs and equal widths required")
        if not c:continue
        packet=p.branch.packet;base=packet.assignment((0,)*d+p.complement)
        columns=[tuple((a-b) % 3 for a,b in zip(packet.assignment(tuple(int(i==j) for i in range(d))+p.complement),base)) for j in range(d)]
        rows=tuple(tuple(col[i] for col in columns) for i in range(len(base)))
        for row in rows:
            if any(row):keys.add(tuple(next(x for x in row if x)*x % 3 for x in row))
        frames.append({"domain_sign":c,"physical_frame_rows":rows,"physical_base":base})
    return tuple(sorted(keys)),frames


def code_energy(d,directions,max_pairs=1_000_000):
    integer(d,"logical width",1);integer(max_pairs,"unordered-pair calibration cap",1)
    directions=tuple(tuple(row) for row in directions)
    if not directions or any(len(row)!=d or not any(row) or any(type(x) is not int or x not in (0,1,2) for x in row) for row in directions):
        raise ValueError("nonzero canonical-width ternary directions required")
    span=int(nmod_mat(list(directions),3).rank())
    if span!=d:raise ValueError("injective physical frame required")
    pairs=[(i,j) for i in range(d) for j in range(i,d)]
    features=[[row[i]*row[j] % 3 for i,j in pairs] for row in directions]
    feature_rank=int(nmod_mat(features,3).rank());D=3**d
    certificate=feature_rank==len(pairs)
    if certificate:
        E=2*D*D-D;method="full-symmetric-square-rank-certificate"
    else:
        if D*D>max_pairs:raise ValueError("no square-rank certificate; exact pair census exceeds cap")
        words=tuple(product(range(3),repeat=d));code=[tuple(sum(a*b for a,b in zip(row,z)) % 3 for row in directions) for z in words]
        counts=Counter(tuple(tuple(sorted((a,b))) for a,b in zip(x,y)) for x in code for y in code)
        E=sum(c*c for c in counts.values());method="exact-coordinatewise-unordered-pair-census"
    return {"width":d,"program_dimension":D,"directions":directions,"physical_frame_rank":span,
            "symmetric_square_feature_rank":feature_rank,"symmetric_square_dimension":len(pairs),
            "unordered_pair_separation_certified_by_square_span":certificate,
            "ordered_balanced_quadruples":str(E),"energy_method":method,
            "conditional_mean_local_Fourier_collision_nonzero_secret":str(Fraction(E,D**3)),
            "entropy_deficit_upper_nats":math.log(E/(D*D)),
            "full_square_rank_bound_less_than_one_bit":certificate,
            "physical_IID_source_premise_certified":False}


def information_bound(energy,n,r,outputs=1,target_error=0.1):
    for x,name in ((n,"components"),(r,"phase digits"),(outputs,"outputs")):
        integer(x,name,1)
    if not 0<target_error<0.5:raise ValueError("target error must lie strictly between zero and one half")
    D=energy["program_dimension"];G=3**(n*r);deficit=energy["entropy_deficit_upper_nats"]
    zero_mass=Fraction(1,G)
    per_output=deficit+(math.log(D)-deficit)*float(zero_mass)
    h=-target_error*math.log(target_error)-(1-target_error)*math.log(1-target_error)
    required=max(0.,((1-target_error)*math.log(G)-h)/per_output)
    return {"components":n,"phase_digits":r,"outputs":outputs,"secret_count":str(G),
            "exact_zero_secret_prior_mass":str(zero_mass),
            "exact_information_bound_formula":"log(E/D^2)+(log(D)-log(E/D^2))/G",
            "numeric_entropy_and_Fano_values_are_estimates":True,
            "mean_mutual_information_per_output_upper_nats":per_output,
            "mean_mutual_information_per_output_upper_bits":per_output/math.log(2),
            "mean_joint_information_upper_nats":outputs*per_output,
            "target_mean_full_secret_error":target_error,
            "Fano_required_outputs_lower_real":required,
            "conditional_low_frame_and_physical_IID_premise_required":True,
            "public_full_labels_conditioned_in_mutual_information":True,
            "shared_public_secret_shift_allowed":True,
            "label_or_outcome_adaptive_measurement_bases_covered":False,
            "collective_nonproduct_measurements_covered":False,
            "computational_cost_of_classical_inference_lower_bounded":False,
            "source_realization_pointwise_information_bound":False}


def original_high_chart_census():
    """Complete alpha/delta chart on actual original pivot labels, at q3."""
    programs=native_cohort(1,1,1,89000);p=programs[0];acq=p.branch.acquisition;source=acq.source
    K=len(acq.supports)
    if K!=2:raise AssertionError("fixed original chart calibration requires two odd inputs")
    ws=tuple(product(range(3),repeat=1));W=np.exp(-2j*math.pi*np.array([[a[0]*b[0] % 3 for b in ws] for a in ws])/3)
    counts=Counter();collision_sums=[0.,0.,0.];source_controls=[]
    for chart in product(range(3),repeat=2*K):
        labels=[list(row) for row in source.labels]
        for j,support in enumerate(acq.supports):
            i=support[0];a,c=(row[0] for row in source.frequencies[i]);h,k=chart[2*j:2*j+2]
            labels[i][0]=inverse_frequency_coordinates((a+3*h) % 9,(c+6*h+3*k) % 9,source.level)
        new_source=native_source(labels,source.level)
        new=PacketAcquisition.from_source(new_source,K,acq.source_ids,source.inputs)
        if new.supports!=acq.supports:raise ArithmeticError("high chart changed low support selection")
        pointers=tuple(p.branch.anchor[i] for i in acq.pointers)
        branch=new.branch(pointers,p.branch.packet.syndrome);cohort=(NativeProgram(branch,1,p.complement),)
        if any(branch.packet.assignment(z+p.complement)!=p.branch.packet.assignment(z+p.complement) for z in ws):
            raise ArithmeticError("high chart changed the conditional physical frame")
        phase,_=cancel(cohort,((2,),));table=tuple(phase.value(z)[0] for z in ws);counts[table[1:]]+=1
        for s in range(3):
            states=np.exp(2j*math.pi*s*np.array(table)/3);prob=abs(W@states/3)**2
            collision_sums[s]+=float(sum(prob*prob))
        source_controls.append({"original_pivot_alpha_delta_lifts":chart,"actual_phase_values":table})
    if len(counts)!=9 or set(counts.values())!={9}:raise ArithmeticError("true source chart failed uniform two-frequency law")
    if not np.allclose(np.array(collision_sums)/81,[1,5/9,5/9],atol=2e-10):
        raise ArithmeticError("source fourth moment disagrees with physical-word energy")
    return {"complete_original_high_chart_words":81,"original_program":p.record(),
            "original_source_supports_unchanged":True,"records":source_controls,
            "frequency_pair_counts":[{"pair":pair,"count":count} for pair,count in sorted(counts.items())],
            "mean_Fourier_collision_by_secret":[x/81 for x in collision_sums],
            "virtual_chart_lifts_are_additional_supplied_states":False,
            "finite_chart_proves_physical_IID_source_premise":False}


def run_controls():
    controls=[]
    for n,d,r,seed in ((1,1,2,89000),(1,2,2,89128),(2,3,3,89031)):
        programs=native_cohort(n,d,r,seed);c,_=low_relation(programs)
        directions,frames=physical_directions(programs,c);energy=code_energy(d,directions)
        controls.append({"seed":seed,"components":n,"phase_digits":r,
                         "selected_source_frames":frames,"selected_coefficients":c,
                         "physical_source_shape_selection_is_low_only":True,
                         "energy":energy,"information_bound":information_bound(energy,n,r)})
    dense=code_energy(3,tuple(z for z in product(range(3),repeat=3) if any(z) and next(x for x in z if x)==1))
    return {"status":"SOURCE_LOCAL_FOURIER_INFORMATION_CEILING_REVIEW_PENDING",
            "derivation_sha256":hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "native_controls":controls,"original_high_chart_census":original_high_chart_census(),
            "growing_dimension_information_ledgers":[information_bound(dense,n,r,B) for n,r,B in ((32,4,45),(128,5,130),(256,8,345))],
            "general_collective_receiver_ruled_out":False,"quantum_speedup_proved":False,
            "candidate_record_accepted":False,"routine_wiring_owner":"Gemini or Antigravity"}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--write",action="store_true");args=parser.parse_args()
    report=run_controls()
    if args.write:
        REPORT.parent.mkdir(parents=True,exist_ok=True);REPORT.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"],"report":str(REPORT) if args.write else None,
                      "native_square_feature_ranks":[x["energy"]["symmetric_square_feature_rank"] for x in report["native_controls"]]},indent=2))


if __name__=="__main__":main()
