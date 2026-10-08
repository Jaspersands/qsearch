from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import subprocess

import pytest

from ternary_affine_line_extractor import from_quadratic
from ternary_batch_fiber_compiler import BatchFiberProgram
from cyclotomic_fiber_receiver import inverse_frequency_coordinates,native_source
from ternary_cyclic_extractor import random_even_source
from ternary_nonlinear_cycle_compiler import affine_step,audit,cyclic_coordinates,reconstruct,reference_step


@pytest.mark.parametrize("n,r,d,M",[(1,3,1,3),(2,2,1,5),(1,3,2,9)])
def test_every_native_reference_word_has_clean_canonical_cycle_coordinates(n,r,d,M):
    p=BatchFiberProgram(random_even_source(n,2*r,M,88030+n),d);step=reference_step(p);outputs=[]
    for word in product(range(3),repeat=M):
        u,t,success=cyclic_coordinates(word,step)
        assert success and u==min(word,step(word),step(step(word)))
        assert reconstruct(u,t,step)==word
        assert p.low_frequency(word)==p.low_frequency(step(word))
        assert all((a-b)%3==0 for a,b in zip(word,reconstruct(u,t,step)))
        outputs.append((u,t,success))
    assert len(set(outputs))==3**M


def test_partial_affine_cycles_have_fixed_failure_words_and_raw_not_conditional_success():
    s=from_quadratic([[0,0,1,0],[1,2,0,1]],[[1,2,0,1],[0,0,1,1]])
    step=affine_step(s,(1,1,0,0));success=0
    for word in product(range(3),repeat=4):
        u,t,flag=cyclic_coordinates(word,step)
        assert reconstruct(u,t,step)==word
        if not flag:assert u==word and t==0
        success+=flag
    assert Fraction(success,81)==Fraction(1,3)
    value=audit(BatchFiberProgram(s,1),"supplied-low-affine-direction",(1,1,0,0))
    assert value["original_word_scratch_erasure_failures"]==0
    assert not value["global_fiber_rank_or_unrank_called"]
    assert value["canonical_tag_register_trits"]==4
    assert value["raw_success_probability"]=="1/3"
    assert value["output_qutrits_per_accepted_batch"]==1


def test_three_cycle_orientation_is_not_global_lexicographic_fiber_rank():
    orbit=((0,1),(2,0),(1,2));table={orbit[i]:orbit[(i+1)%3] for i in range(3)}
    for index,w in enumerate(orbit):
        u,t,flag=cyclic_coordinates(w,table.__getitem__)
        assert u==orbit[0] and t==index and flag
        assert reconstruct(u,t,table.__getitem__)==w


def test_cycle_policy_does_not_change_when_actual_high_native_labels_change():
    source=random_even_source(1,6,3,88035);p=BatchFiberProgram(source,1);first=audit(p,"exponential-low-fiber-atlas")
    q=source.modulus
    rows=[tuple(tuple((a+3*(i+k+1))%q for a in row) for k,row in enumerate(pair)) for i,pair in enumerate(source.frequencies)]
    labels=[[inverse_frequency_coordinates(a,c,source.level) for a,c in zip(pair[0],pair[1])] for pair in rows]
    changed=native_source(labels,source.level);second=audit(BatchFiberProgram(changed,1),"exponential-low-fiber-atlas")
    assert first["complete_coordinate_map_sha256"]==second["complete_coordinate_map_sha256"]
    assert first["raw_success_probability"]==second["raw_success_probability"]
    assert first["selected_child_controls"]!=second["selected_child_controls"]


def test_forward_and_reconstruction_use_constant_not_fiber_size_evaluator_calls():
    table={(0,0):(1,2),(1,2):(2,1),(2,1):(0,0)};calls=[]
    def step(w):calls.append(w);return table[w]
    u,t,success=cyclic_coordinates((2,1),step)
    assert success and len(calls)==3
    reconstruct(u,t,step)
    assert len(calls)<=5


def test_opaque_callbacks_cannot_be_declared_costed_low_only_audit_policies():
    p=BatchFiberProgram(random_even_source(1,4,3,14),1)
    with pytest.raises(ValueError):audit(p,"unreviewed-black-box")
    with pytest.raises(ValueError):audit(p,"exponential-low-fiber-atlas",(1,0,0))


@pytest.mark.parametrize("word,step",[((0,),lambda w:(1-w[0],)),((0,),lambda w:(True,)),((0,1),lambda w:(0,))])
def test_invalid_orbits_do_not_silently_become_logical_children(word,step):
    with pytest.raises(ValueError):cyclic_coordinates(word,step)


def test_complete_audit_budget_and_prefix_domain_fail_closed():
    p=BatchFiberProgram(random_even_source(1,6,9,14),2)
    with pytest.raises(ValueError):audit(p,"exponential-low-fiber-atlas",max_words=729)
    with pytest.raises(ValueError):audit(p,"supplied-low-affine-direction",(1,)*9)
    with pytest.raises(ValueError):reconstruct((0,),3,lambda w:w)


def test_live_independent_verifier_reconstructs_the_entire_isometry():
    root=Path(__file__).resolve().parents[1]
    result=subprocess.run(["node",str(root/"research/certificates/ternary_nonlinear_cycle_compiler_crosscheck.js")],capture_output=True,text=True)
    assert result.returncode==0,result.stderr
    value=json.loads(result.stdout)
    assert value["wholeOriginalWords"]==value["erasedOriginalWords"]==20007
    assert value["nonaffineCycles"]>0
    assert not value["fastNonlinearActionSupplied"]


@pytest.mark.parametrize("mutation",["rank-demand","map","erasure","phase","coverage","tag-size","fast-action","calls","scope","depth","shallow","baseline-scope"])
def test_verifier_rejects_unclean_maps_bad_phases_and_fake_efficient_cycle_actions(tmp_path,mutation):
    root=Path(__file__).resolve().parents[1];record=json.loads((root/"research/phase_workbench/ternary_nonlinear_cycle_compiler.json").read_text());c=record["native_complete_controls"][0]
    if mutation=="rank-demand":record["tag_compression_or_global_ranking_required"]=True
    if mutation=="map":c["complete_coordinate_map_sha256"]="0"*64
    if mutation=="erasure":c["original_word_scratch_erasure_failures"]=1
    if mutation=="phase":c["selected_child_controls"][0]["child_rows"][0][0]=(c["selected_child_controls"][0]["child_rows"][0][0]+1)%3
    if mutation=="coverage":record["native_complete_controls"][-1]["raw_success_probability"]="1"
    if mutation=="tag-size":c["canonical_tag_register_trits"]-=1
    if mutation=="fast-action":record["efficient_constant_coverage_nonlinear_action_supplied"]=True
    if mutation=="calls":c["clean_evaluator_compute_uncompute_call_upper"]=0
    if mutation=="scope":record["all_quantum_receivers_equivalent_to_cycle_actions_claimed"]=True
    comparison=record["full_depth_supply_comparisons"][-1]
    if mutation=="depth":comparison["existing_sieve"]["fresh_batch_protocol_copies_for_one_final_field_qutrit"]="1"
    if mutation=="shallow":comparison["shallow_perfect_acceptance_is_already_known"]=False
    if mutation=="baseline-scope":comparison["existing_sieve"]["lower_bound_scope"]="all quantum receivers"
    target=tmp_path/"mutant.json";target.write_text(json.dumps(record))
    result=subprocess.run(["node",str(root/"research/certificates/ternary_nonlinear_cycle_compiler_crosscheck.js"),str(target)],capture_output=True,text=True)
    assert result.returncode!=0,result.stdout
