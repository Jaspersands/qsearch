from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import subprocess
import random

import pytest

from cyclotomic_fiber_receiver import native_source
from ternary_coherent_edge_receiver import NativeEdgeProgram
from ternary_cyclic_extractor import random_even_source
from ternary_prefix_schmidt import branch_record,classical_prefix_sample,low_label_census,physical_control,prefix_control,purity_certificate


@pytest.mark.parametrize("r",[16,32,64])
def test_exact_middle_scale_purity_bound_decays_exponentially_not_a_quantum_no_go(r):
    split=(r-2)//2;H=3**split;c=purity_certificate(1,r,split,split,r*r)
    assert c["mean_uniform_target_fiber_size"]==H
    assert c["mean_Born_weighted_Schmidt_purity_upper"]<Fraction(10,H)
    assert c["mean_squared_overlap_upper_squared"]==min(1,r*r*c["mean_Born_weighted_Schmidt_purity_upper"])
    assert not c["general_tensor_network_or_quantum_no_go"] and not c["quantum_speedup_proved"]
    assert not c["adaptive_label_partition_covered"] and not c["large_word_space_executed"]
    assert c["mean_bond_budget"]==r*r and c["label_outcome_dependent_bond_allocation_covered_by_mean_cost_bound"]


def test_large_root_polynomial_bond_cannot_have_high_average_full_state_fidelity():
    c=purity_certificate(1,64,31,31,4096)
    assert c["mean_squared_overlap_upper_squared"]<Fraction(1,10**8)
    assert int(c["necessary_bond_for_mean_squared_overlap_ge_nine_tenths"])>10**12


@pytest.mark.parametrize("n,r,d,split",[(1,6,2,2),(2,4,1,3)])
def test_actual_native_phase_matrix_schmidt_spectra_are_independent_of_all_secret_types(n,r,d,split):
    p=NativeEdgeProgram(random_even_source(n,2*r,n*r-2,99503))
    for target,secret in product(((0,)*n,(1,)*n,(3**d-1,)*n),((0,)*n,(3,)*n,(p.source.modulus-1,)*n)):
        c=physical_control(p,d,split,target,secret)
        if c["status"]=="EMPTY_PHYSICAL_BRANCH":assert c["Born_probability"]=="0"
        else:
            assert c["spectrum_residual"]<2e-12 and c["matrix_norm_residual"]<2e-12
            assert not c["unknown_secret_used_in_receiver_recipe"]


def test_branch_distribution_is_born_weighted_not_uniform_targets_and_keeps_empties():
    p=NativeEdgeProgram(random_even_source(1,12,4,99501));c=prefix_control(p,3,2,2)
    rows=c["complete_branches"]
    assert len(rows)==27 and c["Born_probability_sum"]==1
    assert sum(int(row["fiber_size"]) for row in rows)==81
    assert c["full_native_words_enumerated_for_counts"]==0 and c["half_words_enumerated"]==18
    assert c["Born_weighted_best_rank_chi_squared_overlap"]**2<=2*c["Born_weighted_purity"]


def test_population_bound_must_not_be_promoted_to_a_pointwise_label_guarantee():
    p=NativeEdgeProgram(native_source([[(0,0)]]*6,16))
    c=prefix_control(p,3,3)
    assert c["Born_weighted_purity"]==1
    assert sum(row["status"]=="EMPTY_PHYSICAL_BRANCH" for row in c["complete_branches"])==26
    assert purity_certificate(1,8,3,3)["mean_Born_weighted_Schmidt_purity_upper"]<1


def test_no_prefix_measurement_retains_product_state_and_rank_one():
    p=NativeEdgeProgram(random_even_source(1,12,4,99501));c=prefix_control(p,0,2)
    assert c["Born_weighted_purity"]==1 and c["Born_weighted_best_rank_chi_squared_overlap"]==1
    assert c["complete_branches"][0]["Schmidt_rank"]==1


def test_entire_iid_low_label_law_has_exact_uniform_target_and_collision_moments():
    c=low_label_census()
    assert c["complete_IID_low_label_cases"]==81
    assert c["uniform_target_variance"]==2 and c["independent_half_collision_product_mean"]==25
    assert 0<c["Born_weighted_purity_mean"]<=1


def test_empty_schmidt_branch_cannot_have_fake_conditional_purity_or_fidelity():
    c=branch_record({(0,):1},{(0,):1},(1,),3,1,1)
    assert c["status"]=="EMPTY_PHYSICAL_BRANCH" and c["conditional_purity"] is None
    assert c["conditional_best_rank_chi_squared_overlap"] is None


def test_classical_basis_word_sampling_exactly_reproduces_secret_independent_prefix_born_law():
    p=NativeEdgeProgram(random_even_source(1,8,2,99601));counts={}
    for word in product(range(3),repeat=2):
        target=(p.source.value(word)[0]%3,);counts[target]=counts.get(target,0)+1
    c=prefix_control(p,1,1)
    for branch in c["complete_branches"]:
        assert Fraction(branch["Born_probability"])==Fraction(counts.get(branch["target"],0),9)
    sampled=classical_prefix_sample(p,1,random.Random(1))
    assert sampled["known_native_rows_evaluated"]==2
    assert not sampled["unknown_secret_used"] and not sampled["coherent_conditioned_phase_state_produced"]


def test_classical_prefix_sampler_at_high_root_is_polynomial_public_arithmetic_not_a_phase_decoder():
    p=NativeEdgeProgram(random_even_source(1,128,62,99602))
    c=classical_prefix_sample(p,31,random.Random(1))
    assert c["known_native_rows_evaluated"]==62 and 0<=c["prefix_outcome"][0]<3**31
    assert c["reproduces_prefix_outcome_law_only"]


def test_whole_preflight_and_illegal_shapes_fail_closed():
    p=NativeEdgeProgram(random_even_source(1,16,6,99501))
    with pytest.raises(ValueError,match="preflight"):prefix_control(p,7,3)
    with pytest.raises(ValueError,match="nontrivial"):purity_certificate(1,8,3,6)
    with pytest.raises(ValueError,match="bond cap"):purity_certificate(1,8,3,3,True)
    with pytest.raises(ValueError,match="secret"):physical_control(p,3,3,(0,),(-1,))


@pytest.mark.parametrize("mutation",["population","scope","Born","Schmidt","norm","unknown"])
def test_independent_checker_rejects_corrupted_mean_claims_and_conditional_certificates(tmp_path,mutation):
    root=Path(__file__).resolve().parents[1]
    record=json.loads((root/"research/phase_workbench/ternary_prefix_schmidt.json").read_text())
    if mutation=="population":record["population_certificates"][-1]["mean_Born_weighted_Schmidt_purity_upper"]="1"
    elif mutation=="scope":record["generic_quantum_or_tensor_network_lower_bound"]=True
    elif mutation=="Born":record["prespecified_native_cases"][0]["count_controls"][1]["complete_branches"][0]["Born_probability"]="1"
    elif mutation=="Schmidt":record["prespecified_native_cases"][0]["count_controls"][1]["complete_branches"][0]["Schmidt_integer_weights"][0]["integer_weight"]="999"
    elif mutation=="norm":record["prespecified_native_cases"][0]["physical_controls"][0]["observed_squared_singular_values"][0]=1.25
    else:record["prespecified_native_cases"][0]["count_controls"][-1]["classification_complete"]=True
    p=tmp_path/"bad.json";p.write_text(json.dumps(record))
    result=subprocess.run(["node",str(root/"research/certificates/ternary_prefix_schmidt_crosscheck.js"),str(p)],capture_output=True,text=True)
    assert result.returncode!=0 and "Error:" in result.stderr
