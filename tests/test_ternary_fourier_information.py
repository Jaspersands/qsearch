from collections import Counter
from fractions import Fraction
import hashlib
from itertools import product
import json
import math
from pathlib import Path
import subprocess

import numpy as np
import pytest

from ternary_fourier_information import (
    DERIVATION, REPORT, code_energy, information_bound, original_high_chart_census,
    physical_directions,
)
from ternary_ridge_cancellation import low_relation, native_cohort


def projective(d):
    return tuple(z for z in product(range(3),repeat=d) if any(z) and next(x for x in z if x)==1)


def direct_energy(d,directions):
    ws=tuple(product(range(3),repeat=d))
    code=[tuple(sum(a*b for a,b in zip(row,z)) % 3 for row in directions) for z in ws]
    counts=Counter(tuple(tuple(sorted((a,b))) for a,b in zip(x,y)) for x in code for y in code)
    return sum(x*x for x in counts.values())


@pytest.mark.parametrize("d",[1,2,3,4])
def test_square_span_proves_global_unordered_pair_separation(d):
    directions=projective(d);x=code_energy(d,directions);D=3**d
    assert x["unordered_pair_separation_certified_by_square_span"]
    assert int(x["ordered_balanced_quadruples"])==2*D*D-D
    assert direct_energy(d,directions)==2*D*D-D
    assert Fraction(x["conditional_mean_local_Fourier_collision_nonzero_secret"])==Fraction(2,D)-Fraction(1,D*D)
    assert x["entropy_deficit_upper_nats"]<math.log(2)


@pytest.mark.parametrize("d",[2,3,4])
def test_coordinate_only_code_has_extra_balanced_quadruples_and_does_not_get_one_bit_certificate(d):
    axes=tuple(tuple(int(i==j) for i in range(d)) for j in range(d));x=code_energy(d,axes)
    assert not x["unordered_pair_separation_certified_by_square_span"]
    assert int(x["ordered_balanced_quadruples"])==15**d
    assert not x["full_square_rank_bound_less_than_one_bit"]
    assert x["energy_method"]=="exact-coordinatewise-unordered-pair-census"


@pytest.mark.parametrize("n,d,r,seed",[(1,1,2,89000),(1,2,2,89128),(2,3,3,89031)])
def test_actual_selected_native_physical_shapes_get_certificates(n,d,r,seed):
    programs=native_cohort(n,d,r,seed);c,_=low_relation(programs)
    directions,frames=physical_directions(programs,c);x=code_energy(d,directions)
    assert x["unordered_pair_separation_certified_by_square_span"]
    assert len(frames)==sum(bool(a) for a in c)
    assert x["physical_frame_rank"]==d
    assert not x["physical_IID_source_premise_certified"]
    assert direct_energy(d,directions)==int(x["ordered_balanced_quadruples"])


def test_true_original_alpha_delta_chart_matches_fourth_moment():
    x=original_high_chart_census()
    assert x["complete_original_high_chart_words"]==81
    assert len(x["frequency_pair_counts"])==9
    assert all(row["count"]==9 for row in x["frequency_pair_counts"])
    assert x["mean_Fourier_collision_by_secret"]==pytest.approx([1,5/9,5/9])
    assert not x["virtual_chart_lifts_are_additional_supplied_states"]
    assert not x["finite_chart_proves_physical_IID_source_premise"]


@pytest.mark.parametrize("q",[3,9,27])
def test_alpha_delta_fourth_moment_necessity_includes_divisible_secrets(q):
    # Exact coordinate condition uses effective order, not a unit-secret assumption.
    for effective in (3,q):
        for a,b,c,d in product(range(3),repeat=4):
            indicator=int(a==2)-int(b==2)+int(c==2)-int(d==2)
            phase=a-b+c-d
            survives=indicator % effective==0 and phase % effective==0
            assert survives==(sorted((a,c))==sorted((b,d)))


def test_entropy_bound_keeps_zero_secret_and_not_pointwise_or_adaptive_claim():
    x=code_energy(1,((1,),));y=information_bound(x,1,1,3)
    c=math.log(5/3)
    assert y["mean_mutual_information_per_output_upper_nats"]==pytest.approx(c+(math.log(3)-c)/3)
    assert y["exact_zero_secret_prior_mass"]=="1/3"
    assert not y["source_realization_pointwise_information_bound"]
    assert not y["label_or_outcome_adaptive_measurement_bases_covered"]
    assert not y["collective_nonproduct_measurements_covered"]
    assert not y["computational_cost_of_classical_inference_lower_bounded"]


def test_large_root_information_is_not_lost_to_float_overflow_or_false_exactness():
    x=information_bound(code_energy(3,projective(3)),256,8,345)
    assert Fraction(x["exact_zero_secret_prior_mass"])==Fraction(1,3**2048)
    assert math.isfinite(x["mean_mutual_information_per_output_upper_nats"])
    assert x["numeric_entropy_and_Fano_values_are_estimates"]
    assert x["Fano_required_outputs_lower_real"]>2500


def test_reference_cap_and_injective_source_frame_are_enforced():
    with pytest.raises(ValueError,match="census exceeds cap"):
        code_energy(4,tuple(tuple(int(i==j) for i in range(4)) for j in range(4)),max_pairs=100)
    with pytest.raises(ValueError,match="injective physical frame"):
        code_energy(2,((1,0),))
    with pytest.raises(ValueError,match="nonempty matched"):
        physical_directions((),())


def test_shannon_entropy_jensen_step_matches_explicit_source_census():
    # Uniform independent qutrit phases give a finite check on the entropy step.
    entropies=[];collisions=[]
    for a,b in product(range(3),repeat=2):
        amplitudes=np.exp(2j*math.pi*np.array([0,a,b])/3)
        prob=abs(np.fft.fft(amplitudes)/3)**2
        entropies.append(-sum(p*math.log(p) for p in prob if p>1e-14))
        collisions.append(float(sum(prob*prob)))
    assert sum(collisions)/9==pytest.approx(5/9)
    assert sum(entropies)/9>=-math.log(sum(collisions)/9)-1e-12


def test_curvature_filtered_source_is_explicit_counterexample_to_overbroad_moment_claim():
    # A later delta-dependent stage is not the original low-ell-only factory.
    for a in range(3):
        state=np.exp(2j*math.pi*np.array([0,a,2*a])/3)
        probability=abs(np.fft.fft(state)/3)**2
        assert sum(probability*probability)==pytest.approx(1)
        assert sum(probability*probability)>5/9


def test_live_artifact_pins_derivation_and_preserves_scope():
    x=json.loads(REPORT.read_text())
    assert x["derivation_sha256"]==hashlib.sha256(DERIVATION.read_bytes()).hexdigest()
    assert not x["general_collective_receiver_ruled_out"]
    assert not x["candidate_record_accepted"] and not x["quantum_speedup_proved"]


CHECKER=Path(__file__).resolve().parents[1]/"research/certificates/ternary_fourier_information_crosscheck.js"


def test_independent_information_checker_passes_live_artifact():
    result=subprocess.run(["node",str(CHECKER)],capture_output=True,text=True,check=True)
    x=json.loads(result.stdout)
    assert x["status"]=="PASS" and x["true_original_chart_words"]==81
    assert not x["external_IID_supply_certified"]


@pytest.mark.parametrize("mutation",["energy","scope","chart","rank","Fano"])
def test_independent_information_checker_rejects_false_evidence(tmp_path,mutation):
    x=json.loads(REPORT.read_text())
    if mutation=="energy":x["native_controls"][1]["energy"]["ordered_balanced_quadruples"]="81"
    elif mutation=="scope":x["native_controls"][0]["information_bound"]["collective_nonproduct_measurements_covered"]=True
    elif mutation=="chart":x["original_high_chart_census"]["records"][0]["actual_phase_values"][1]+=1
    elif mutation=="rank":x["native_controls"][2]["energy"]["symmetric_square_feature_rank"]=1
    elif mutation=="Fano":x["growing_dimension_information_ledgers"][0]["Fano_required_outputs_lower_real"]=1
    path=tmp_path/"mutated.json";path.write_text(json.dumps(x))
    result=subprocess.run(["node",str(CHECKER),str(path)],capture_output=True,text=True)
    assert result.returncode!=0 and result.stderr
