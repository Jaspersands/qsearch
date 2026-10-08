from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import subprocess

import pytest

from cyclotomic_fiber_receiver import inverse_frequency_coordinates,native_source
from ternary_coherent_edge_receiver import NativeEdgeProgram
from ternary_cyclic_extractor import random_even_source
from ternary_syndrome_phase_compiler import (
    PolynomialPhase,TopDigitQuadraticPhase,fiber_certificate,gradient_recipe,native_control,
)


def correlation_source():
    return NativeEdgeProgram(native_source([[inverse_frequency_coordinates(a,c,8)] for a,c in ((1,2),(26,52))],8))


@pytest.mark.parametrize("r",[2,3,4])
def test_entire_small_syndrome_domain_has_exact_polynomial_phase_translation(r):
    q=3**r;P=PolynomialPhase(1,q,(((q+1)//2,(2,)),(7%q,(5,)),(3,(7,))))
    for S in range(q//3):
        c=fiber_certificate(P,(S,))
        assert c["phase_is_known_trit_translation"] and c["square_zero_high_increment_theorem_applies"]
        g=c["known_trit_translation"]
        for h in range(3):
            assert (P.value((S+q//3*h,))-P.value((S,)))%q==(q//3*h*g)%q
        assert g==P.gradient_trit((S,),0)


def test_multivariate_composite_ring_taylor_and_only_low_gradient_not_field_substitution():
    P=PolynomialPhase(2,9,((1,(1,2)),(5,(2,5)),(2,(4,0))))
    for a,b in product(range(9),range(3)):
        c=fiber_certificate(P,(a,b),1)
        assert c["known_trit_translation"]==P.gradient_trit((a,b),1)
        for h in range(3):assert P.gradient_trit((a,b+3*h),1)==P.gradient_trit((a,b),1)


@pytest.mark.parametrize("r",[16,32,64])
def test_large_root_and_large_degree_certificate_needs_no_quantum_word_enumeration(r):
    q=3**r;degree=10**30+2
    P=PolynomialPhase(2,q,((q-1,(degree,2)),((q+1)//2,(2,0))))
    c=fiber_certificate(P,(q//9+2,q-2))
    assert c["phase_is_known_trit_translation"] and c["known_trit_translation"]==P.gradient_trit((q//9+2,q-2),0)
    assert P.public()["terms"][0]["powers"][0]==str(degree)


def test_root_one_and_nonsmooth_top_digit_phases_are_not_falsely_removed():
    root=fiber_certificate(PolynomialPhase(1,3,((1,(2,)),)),(0,))
    digit=fiber_certificate(TopDigitQuadraticPhase(1,81),(0,))
    for c in (root,digit):
        assert not c["phase_is_known_trit_translation"] and c["known_trit_translation"] is None
        assert not c["square_zero_high_increment_theorem_applies"]
    assert root["phase_numerators_on_three_classes"]==["0","1","1"]
    assert digit["phase_numerators_on_three_classes"]==["0","27","27"]
    with pytest.raises(ValueError):TopDigitQuadraticPhase(1,3)
    with pytest.raises(ValueError):TopDigitQuadraticPhase(1,9,coefficient=0)


def test_native_chirp_and_unchirped_compiled_rule_have_identical_exact_raw_risk():
    c=native_control(correlation_source(),PolynomialPhase(1,81,((41,(2,)),(7,(5,)))))
    assert c["original_chirped_uniform_trit_success"]==c["compiled_unchirped_uniform_trit_success"]
    assert c["actual_full_root_phase_Born_residual"]<3e-12
    assert c["gradient_only_complete_uniform_secret_score_residual"]<3e-12
    assert c["complete_uniform_secrets_enumerated_for_gradient_calibration"]==81
    assert sum(Fraction(b["Born_mass"]) for b in c["occupied_syndrome_branches"])==1
    assert c["uniform_mean_not_pointwise_secret_guarantee"] and not c["efficient_MAP_decoder_or_fiber_transform_supplied"]


def test_uniform_mean_compilation_must_not_be_promoted_to_pointwise_guarantee():
    c=native_control(correlation_source(),PolynomialPhase(1,81,((41,(2,)),(7,(5,)))))
    counter=c["constant_decision_pointwise_countercontrol"]
    assert counter["original_success_by_trit"]!=counter["compiled_success_by_trit"]
    assert sum(map(Fraction,counter["compiled_success_by_trit"]))/3==Fraction(1,3)
    assert counter["uniform_mean_success_both"]=="1/3"


def test_multivariate_physical_source_keeps_other_coordinates_in_nuisance_ensemble():
    edge=NativeEdgeProgram(random_even_source(2,6,4,99735),1)
    P=PolynomialPhase(2,27,((14,(0,2)),(2,(1,1)),(5,(2,3))))
    c=native_control(edge,P)
    assert c["target_coordinate"]==1 and c["dimension"]==2
    assert c["complete_uniform_secrets_enumerated_for_gradient_calibration"]==729
    assert c["gradient_only_complete_uniform_secret_score_residual"]<3e-12
    assert c["original_chirped_uniform_trit_success"]==c["compiled_unchirped_uniform_trit_success"]


def test_dirty_full_frequency_scratch_or_measurement_removes_useful_phase():
    c=native_control(correlation_source(),PolynomialPhase(1,81,((41,(2,)),)))
    assert c["dirty_full_frequency_scratch_or_measurement_trit_success"]=="1/3"
    assert c["dirty_full_frequency_probability_residual"]<3e-12


def test_minimal_gradient_recipe_keeps_one_trit_and_erases_scratch_without_extra_sources():
    c=gradient_recipe(2,64,126,1)
    assert c["retained_measurement_register_trits"]==1 and c["low_frequency_scratch_trits"]==2
    assert not c["full_frequency_or_syndrome_register_required"]
    assert not c["original_words_or_target_high_trit_measured"] and c["extra_original_source_copies"]==0
    assert not c["additional_same_secret_sources_or_query_access_covered"]
    assert not c["interleaved_noncommuting_phase_operations_covered"]
    assert c["uniform_secret_mean_success_preserved"] and not c["pointwise_secret_success_preserved"]


def test_partial_block_quadratic_is_a_real_exception_not_a_total_frequency_chirp():
    source=correlation_source().source;words=((0,0),(1,1),(2,2))
    total=[source.value(w)[0] for w in words]
    partial=[(0,source.frequencies[0][0][0],source.frequencies[0][1][0])[w[0]] for w in words]
    values=[41*f*f%81 for f in partial]
    assert total==[0,27,54] and partial==[0,1,2] and values==[0,41,2]
    assert (values[1]-values[0])%27!=0


def test_shapes_programs_and_calibration_limits_fail_closed():
    with pytest.raises(ValueError):PolynomialPhase(1,9,((-1,(2,)),))
    with pytest.raises(ValueError):PolynomialPhase(1,9,((1,(-1,)),))
    with pytest.raises(ValueError):PolynomialPhase(1,9,((True,(2,)),))
    with pytest.raises(ValueError):fiber_certificate(PolynomialPhase(1,9,((1,(2,)),)),(3,))
    with pytest.raises(ValueError):gradient_recipe(1,1,1)
    with pytest.raises(ValueError):native_control(correlation_source(),TopDigitQuadraticPhase(1,81))
    with pytest.raises(ValueError):native_control(NativeEdgeProgram(random_even_source(1,16,6,17)),PolynomialPhase(1,6561,((1,(2,)),)))


def test_standalone_checker_accepts_the_complete_live_native_report():
    root=Path(__file__).resolve().parents[1]
    result=subprocess.run(["node",str(root/"research/certificates/ternary_syndrome_phase_compiler_crosscheck.js")],capture_output=True,text=True)
    assert result.returncode==0,result.stderr
    assert json.loads(result.stdout)["nativeBranches"]>0


@pytest.mark.parametrize("mutation",["Taylor","risk","prior","exception","recipe","partial","source","native","Born","decoder"])
def test_standalone_checker_rejects_invalid_translation_and_claim_scope(tmp_path,mutation):
    root=Path(__file__).resolve().parents[1]
    record=json.loads((root/"research/phase_workbench/ternary_syndrome_phase_compiler.json").read_text())
    if mutation=="Taylor":record["analytic_fiber_certificates"][0]["known_trit_translation"]=0
    if mutation=="risk":record["native_receiver_controls"][0]["compiled_unchirped_uniform_trit_success"]="1"
    if mutation=="prior":record["pointwise_secret_success_or_general_measurement_no_go"]=True
    if mutation=="exception":record["nonpolynomial_top_digit_countercontrol"]["phase_is_known_trit_translation"]=True
    if mutation=="recipe":record["scalable_gradient_recipe"]["original_words_or_target_high_trit_measured"]=True
    if mutation=="partial":record["partial_block_frequency_countercontrol"]["known_total_trit_translation_available"]=True
    if mutation=="source":record["additional_same_secret_samples_or_query_access_covered"]=True
    if mutation=="native":record["native_receiver_controls"][0]["native_labels"][0][0][0]+=1
    if mutation=="Born":record["native_receiver_controls"][0]["occupied_syndrome_branches"][0]["Born_mass"]="1"
    if mutation=="decoder":record["native_receiver_controls"][0]["original_chirped_MAP_decoder"][0]=(record["native_receiver_controls"][0]["original_chirped_MAP_decoder"][0]+1)%3
    target=tmp_path/"mutant.json";target.write_text(json.dumps(record))
    result=subprocess.run(["node",str(root/"research/certificates/ternary_syndrome_phase_compiler_crosscheck.js"),str(target)],capture_output=True,text=True)
    assert result.returncode!=0,result.stdout
