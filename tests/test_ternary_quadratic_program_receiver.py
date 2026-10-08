from fractions import Fraction
from itertools import product
import json
import math
import random
import subprocess

import numpy as np
import pytest

from cyclotomic_fiber_receiver import inverse_frequency_coordinates, native_source
from ternary_correlated_packet_acquisition import PacketAcquisition
from ternary_quadratic_program_receiver import (
    DERIVATION, REPORT, QuadraticFamily, apply_chart, combination,
    engineered_native_program, equation_sample_ledger, isotropic_direction,
    linear_chart, linear_offset_census, native_quadratic_program, physical_receiver, teleport_tensor,
)


@pytest.fixture(scope="module")
def native():
    return [engineered_native_program(n,seed) for n,seed in ((1,88601),(2,88602))]


@pytest.mark.parametrize("index",[0,1])
def test_native_program_uses_actual_original_ancestry_and_quadratic_restriction(native,index):
    family,record=native[index];n=index+1
    source=record["original_source"]
    assert source["acquired_original_native_inputs"]==27*(n+1)**2
    assert source["active_original_inputs"]==27
    assert source["untouched_original_inputs"]==27*((n+1)**2-1)
    assert len(set(source["original_source_ids"]))==source["acquired_original_native_inputs"]
    assert Fraction(record["raw_program_branch_probability"])==Fraction(1,3**24)
    assert not record["source_is_IID_population_control"]
    assert not record["IID_original_source_program_factory_proved"]
    assert not record["identical_program_factory_supplied"]
    assert record["all_restriction_outcomes_accepted"]
    assert record["mixed_cubic_admission"]["classical_quadratic_restriction_admitted"]
    assert [family.value(z) for z in product(range(3),repeat=3)]==[tuple(row) for row in record["complete_native_program_frequency_table"]]


def test_gate_recipe_is_a_complete_invertible_chart_not_only_a_phase_table():
    frame=((1,1,0),(0,1,1));columns,gates=linear_chart(frame,3)
    assert len(columns)==3
    outputs=set()
    for coordinate in product(range(3),repeat=3):
        original=combination(columns,coordinate,3)
        assert apply_chart(gates,original)==coordinate
        outputs.add(original)
    assert len(outputs)==27


@pytest.mark.parametrize("index",[0,1])
def test_complete_choi_bell_receiver_yields_exact_equations_and_uniform_labels(native,index):
    family,record=native[index];s=tuple(range(1,index+2))
    replay=physical_receiver(family,s,record["receiver"]["direction"])
    assert replay["total_raw_Bell_probability"]==pytest.approx(1)
    assert replay["arbitrary_entangled_data_maximum_amplitude_error"]<1e-12
    assert len(replay["all_Bell_branches"])==729
    for branch in replay["all_Bell_branches"]:
        assert Fraction(branch["raw_Bell_probability"])==Fraction(1,729)
        assert branch["answer"]==sum(a*b for a,b in zip(s,branch["public_equation_label"])) % 3
        assert branch["all_Fourier_probabilities"][branch["answer"]]==pytest.approx(1)
    assert len(replay["public_label_histogram"])==3**family.components
    assert {row["count"] for row in replay["public_label_histogram"]}=={729//3**family.components}
    assert not replay["unknown_gate_inverse_or_Clifford_byproduct_correction_used"]
    assert not replay["virtual_calibration_branches_are_source_copies"]


def test_zero_secret_is_also_decoded_and_not_excluded_as_in_pauli_signal_gate(native):
    family,record=native[0]
    replay=physical_receiver(family,(0,),record["receiver"]["direction"])
    assert all(branch["answer"]==0 for branch in replay["all_Bell_branches"])


def test_basis_copy_is_entangled_choi_program_not_cloning(native):
    family,_=native[0];D=3**family.width
    phase=np.array([np.exp(2j*np.pi*family.value(z)[0]/3) for z in product(range(3),repeat=family.width)])
    choi=np.diag(phase)/math.sqrt(D)
    assert np.allclose(choi @ choi.conj().T,np.eye(D)/D)
    rho=choi @ choi.conj().T
    assert np.trace(rho @ rho).real==pytest.approx(1/D)
    supplied=phase/math.sqrt(D)
    assert np.trace(np.outer(supplied,supplied.conj()) @ np.outer(supplied,supplied.conj())).real==pytest.approx(1)


def test_anisotropic_line_does_not_yield_a_deterministic_fourier_equation(native):
    family,_=native[0];v=(0,1,0)
    assert family.quadratic(v)==(1,)
    with pytest.raises(ValueError,match="isotropic"): family.receiver(v)
    data=np.zeros(27,complex)
    for j in range(3):data[3*j]=1/math.sqrt(3)
    tensor,_=teleport_tensor(family,(1,),data)
    line=np.array([tensor[0,0,0,3*j] for j in range(3)])*27
    probability=abs(np.fft.fft(line)/math.sqrt(3))**2
    assert np.allclose(probability,[1/3]*3)


@pytest.mark.parametrize("n",[1,2,3])
def test_wide_common_isotropy_is_guaranteed_without_exponential_search(n):
    d=(n+1)**3-n;rng=random.Random(88670+n);matrices=[]
    for _ in range(n):
        M=[[0]*d for _ in range(d)]
        for i in range(d):
            for j in range(i,d):M[i][j]=M[j][i]=rng.randrange(3)
        matrices.append(tuple(tuple(row) for row in M))
    family=QuadraticFamily(tuple(matrices),((0,)*d,)*n)
    v,record=isotropic_direction(family)
    assert any(v) and family.quadratic(v)==(0,)*n
    assert record["scalable_search_claimed"]
    assert record["orthogonal_basis_size"]==(n+1)**2
    assert not record["full_gradient_rank_guaranteed"]


def test_gradient_deficiency_is_not_promoted_to_full_uniform_secret_labels():
    M=((0,0),(0,0));family=QuadraticFamily((M,M),((1,0),(0,1)))
    record=family.receiver((1,0))
    assert record["gradient_rank"]==0
    assert record["label_offset"]==(1,0)
    assert not record["uniform_full_secret_label_law_certified"]


def test_matrix_only_isotropic_selection_preserves_uniform_fresh_linear_offsets():
    census=linear_offset_census()
    assert census["gradient_rank"]==0
    assert census["complete_independent_linear_offsets"]==81
    assert len(census["public_label_histogram"])==9
    assert {row["count"] for row in census["public_label_histogram"]}=={9}
    assert not census["direction_selection_reads_linear_coefficients"]
    assert not census["unconditional_native_factory_proved_by_this_census"]


def test_linear_offset_adaptive_isotropic_choice_can_destroy_the_uniform_label_law():
    labels=[]
    for beta in product(range(3),repeat=2):
        v=(beta[1],-beta[0] % 3) if any(beta) else (1,0)
        labels.append(sum(a*b for a,b in zip(beta,v)) % 3)
    assert labels==[0]*9


def test_native_cubic_packet_and_higher_root_are_rejected_as_quadratic_programs():
    labels=[]
    for _ in range(3):
        labels.append([inverse_frequency_coordinates(1,2,4)])
        labels.extend([[(0,0)]]*3)
    source=native_source(labels,4)
    acq=PacketAcquisition.from_source(source,3,tuple(f"cubic-{i}" for i in range(12)),12)
    branch=acq.branch((0,)*len(acq.pointers))
    with pytest.raises(ValueError,match="mixed cubic"):
        native_quadratic_program(branch,((1,0),(0,1)),())
    high=native_source(labels,6)
    high_acq=PacketAcquisition.from_source(high,3,tuple(f"high-{i}" for i in range(12)),12)
    high_branch=high_acq.branch((0,)*len(high_acq.pointers))
    with pytest.raises(ValueError,match="level3"):
        native_quadratic_program(high_branch,((1,0),),(0,))


def test_nonzero_logical_complements_still_have_actual_native_quadratic_phases(native):
    family,record=native[1];source=native_source(record["original_labels"],4)
    acq=PacketAcquisition.from_source(source,27,tuple(record["original_source"]["original_source_ids"]),243)
    branch=acq.branch((0,)*len(acq.pointers),(1,2))
    frame=tuple(tuple(column) for column in record["logical_frame"])
    for value in (1,2):
        new,new_record=native_quadratic_program(branch,frame,(value,)*(branch.packet.retained-3))
        assert len(new_record["complete_native_program_frequency_table"])==27
        assert [new.value(z) for z in product(range(3),repeat=3)]==[tuple(row) for row in new_record["complete_native_program_frequency_table"]]


@pytest.mark.parametrize("n",[1,2,8,32,128])
def test_equation_rank_ledger_is_conditional_not_a_supplied_source_factory(n):
    record=equation_sample_ledger(n,8)
    assert record["independent_supplied_programs_required"]==n+8
    assert Fraction(record["field_equation_rank_failure_upper"])==Fraction(3**n-1,2*3**(n+8))
    assert not record["availability_of_these_programs_proved"]
    assert not record["original_full_modulus_secret_recovery_proved"]


def test_invalid_data_frames_families_and_zero_direction_are_rejected(native):
    family,_=native[0]
    for v in ((0,0,0),(True,0,0),(3,0,0),(1,0)):
        with pytest.raises(ValueError): family.receiver(v)
    with pytest.raises(ValueError): linear_chart(((1,0),(2,0)),2)
    with pytest.raises(ValueError): QuadraticFamily((((0,1),(0,0)),),((0,0),))
    with pytest.raises(ValueError): teleport_tensor(family,(1,),np.zeros(27))
    low=QuadraticFamily((((1,0),(0,1)),),((0,0),))
    with pytest.raises(ValueError,match="no common isotropic"):isotropic_direction(low)


def test_independent_live_native_receiver_certificate():
    import hashlib
    report=json.loads(REPORT.read_text())
    assert report["derivation_sha256"]==hashlib.sha256(DERIVATION.read_bytes()).hexdigest()
    checker=DERIVATION.parent/"certificates/ternary_quadratic_program_receiver_crosscheck.js"
    result=subprocess.run(["node",str(checker),str(REPORT)],capture_output=True,text=True)
    assert result.returncode==0,result.stderr
    assert json.loads(result.stdout)["allBellBranches"]==1458


@pytest.mark.parametrize("mutation",["source","quadratic","gradient","label","probability","factory","missing"])
def test_independent_checker_rejects_false_receiver_or_source_claims(tmp_path,mutation):
    report=json.loads(REPORT.read_text());c=report["native_calibration_controls"][0]
    if mutation=="source":c["original_source"]["acquired_original_native_inputs"]-=1
    elif mutation=="quadratic":c["component_matrices"][0][0][0]=(c["component_matrices"][0][0][0]+1)%3
    elif mutation=="gradient":c["receiver"]["gradient_rows"][0][0]=(c["receiver"]["gradient_rows"][0][0]+1)%3
    elif mutation=="label":c["physical_receiver"]["all_Bell_branches"][0]["public_equation_label"][0]=(c["physical_receiver"]["all_Bell_branches"][0]["public_equation_label"][0]+1)%3
    elif mutation=="probability":c["physical_receiver"]["all_Bell_branches"][0]["raw_Bell_probability"]="1"
    elif mutation=="factory":report["unconditional_IID_native_program_factory_supplied"]=True
    elif mutation=="missing":c["physical_receiver"]["all_Bell_branches"].pop()
    target=tmp_path/"mutated.json";target.write_text(json.dumps(report))
    checker=DERIVATION.parent/"certificates/ternary_quadratic_program_receiver_crosscheck.js"
    result=subprocess.run(["node",str(checker),str(target)],capture_output=True,text=True)
    assert result.returncode!=0
