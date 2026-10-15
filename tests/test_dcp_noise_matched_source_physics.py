"""Research-critical physics/lineage checks, separate from integration smoke tests."""
from collections import Counter
from copy import deepcopy
from fractions import Fraction
from itertools import product
import json
import math
from pathlib import Path
import subprocess
import sys

import numpy as np
import pytest

from theorems.dcp_adaptive_direction_rank_gate import decode_dyadic
from theorems.dcp_noise_matched_source import (
    CONTRACT, CONTRACT_ID, PREMISES, REPORT, build_report, first_level_census,
    product_source_certificate, replacement_actions, require_premises, second_level_census,
)

ROOT=Path(__file__).resolve().parents[1]
CHECKER=ROOT/"research/certificates/dcp_noise_matched_source_crosscheck.js"


@pytest.fixture(scope="module")
def report():
    return build_report()


def density(label,secret,R,v):
    angle=2*math.pi*(sum(a*b for a,b in zip(label,secret))%R)/R
    return np.array([[1,float(v)*np.exp(-1j*angle)],[float(v)*np.exp(1j*angle),1]])/2


@pytest.mark.parametrize("components,R",[(1,2),(1,8),(2,4)])
def test_actual_CPTP_actions_restore_all_CQ_blocks_for_unknown_secret(components,R):
    labels=list(product(range(R),repeat=components))
    N=len(labels)
    plus=np.ones((2,2))/2
    minus=np.array([[1,-1],[-1,1]])/2
    tags=((Fraction(0),Fraction(1,4)),(Fraction(9,16),Fraction(1,2)),(Fraction(1),Fraction(1,4)))
    for secret in (tuple(0 for _ in range(components)),tuple(2*j+1 for j in range(components))):
        total=0
        for v,pi in tags:
            recipe=replacement_actions(v,R.bit_length()-1,components,premises=PREMISES)
            pkeep=decode_dyadic(recipe["keep_paid_nonzero_qubit_probability"])
            pplus=decode_dyadic(recipe["replacement_plus_probability_including_zero_coin"])
            pminus=decode_dyadic(recipe["replacement_minus_probability_including_zero_coin"])
            for label in labels:
                target=float(pi/N)*density(label,secret,R,v)
                if any(label):
                    actual=float(pi/(N-1)*pkeep)*density(label,secret,R,v)
                else:
                    actual=sum(float(pi/(N-1))*(float(pplus)*plus+float(pminus)*minus)
                               for candidate in labels if any(candidate))
                assert np.allclose(actual,target,atol=2e-14)
                assert np.linalg.eigvalsh(actual).min()>=-1e-14
                total+=np.trace(actual).real
        assert total==pytest.approx(1)


def test_pure_injection_fails_and_matching_public_dephasing_repairs_it():
    R,v=8,Fraction(9,16)
    desired=density((0,),(3,),R,v)/R
    pure=np.ones((2,2))/(2*R)
    distance=sum(abs(np.linalg.eigvalsh(desired-pure)))/2
    assert distance==pytest.approx(float((1-v)/(2*R))) and distance>0
    recipe=replacement_actions(v,3,1,premises=PREMISES)
    p=decode_dyadic(recipe["conditional_Z_flip_probability"])
    plus=np.ones((2,2))/2
    Z=np.diag([1,-1])
    matched=(float(1-p)*plus+float(p)*(Z@plus@Z))/R
    assert np.allclose(matched,desired,atol=1e-15)


def test_complete_first_level_has_correct_paid_failure_and_public_tag_independence(report):
    C=report["two_level_exact_censuses"][0]
    assert C["raw_census_total"]==8**4*8
    histogram=Counter()
    for row in C["joint_label_visibility_rows"]:
        histogram[row["visibility_exponent"]]+=row["raw_count"]
    assert Fraction(histogram[2],C["raw_census_total"])==Fraction(3,4)
    assert Fraction(histogram[4],C["raw_census_total"])==Fraction(1,4)
    assert C["charged_nonzero_admission_probability"]=="7/8"
    assert C["pure_replacement_matches_noisy_zero_blocks"] is False
    assert first_level_census()==Counter({(row["label"],row["visibility_exponent"]):row["raw_count"]
                                         for row in C["joint_label_visibility_rows"]})


def test_complete_second_level_uses_restored_IID_source_and_pays_retries(report):
    C=report["two_level_exact_censuses"][1]
    assert C["raw_census_total"]==8**4*4**4*8
    assert C["charged_nonzero_admission_probability"]=="1/2"
    assert all(row["target_probability"]==row["restored_probability"] for row in C["joint_label_visibility_rows"])
    assert {row["visibility_exponent"] for row in C["joint_label_visibility_rows"]}==set(range(2,17,2))
    assert second_level_census()==Counter({(row["label"],row["visibility_exponent"]):row["raw_count"]
                                          for row in C["joint_label_visibility_rows"]})
    cost=report["implemented_wrapper_supply"]
    assert Fraction(cost["first_level_original_qubits_per_restored_output"])*Fraction(cost["first_level_outputs_per_second_level_restored_output"])==Fraction(256,7)
    assert cost["these_costs_are_universal_lower_bounds"] is False


def test_every_recorded_CQ_phase_block_is_positive_and_normalized_for_all_secrets(report):
    for C in report["two_level_exact_censuses"]:
        R=C["output_modulus"]
        for secret in range(R):
            total=0
            for row in C["joint_label_visibility_rows"]:
                v=Fraction(3,4)**row["visibility_exponent"]
                mass=Fraction(row["restored_probability"])
                block=float(mass)*density((row["label"],),(secret,),R,v)
                assert np.allclose(block,block.conj().T)
                assert np.linalg.eigvalsh(block).min()>=-1e-15
                total+=np.trace(block).real
            assert total==pytest.approx(1)


def test_uniform_label_marginals_do_not_prove_visibility_independence():
    bad=Counter({(0,1):1,(1,2):1,(2,1):1,(3,2):1})
    assert {sum(c for (l,_),c in bad.items() if l==label) for label in range(4)}=={1}
    with pytest.raises(ValueError,match="correlated"):
        product_source_certificate(bad,4,Fraction(3,4),premises=PREMISES)


@pytest.mark.parametrize("premise",list(PREMISES))
def test_unverified_source_premises_cannot_inherit_inductive_closure(premise):
    bad=dict(PREMISES)
    bad[premise]="correlated-or-unverified" if isinstance(bad[premise],str) else False
    with pytest.raises(ValueError,match="UNRESOLVED"):
        replacement_actions(Fraction(3,4),2,1,premises=bad)
    del bad[premise]
    with pytest.raises(ValueError,match="UNRESOLVED"):
        require_premises(bad)


def test_integer_flags_cannot_be_promoted_to_an_assumption_receipt():
    bad=dict(PREMISES)
    bad["fresh_independent_batches_per_attempt"]=1
    with pytest.raises(ValueError):
        require_premises(bad)


@pytest.mark.parametrize("visibility",[True,0.5,Fraction(-1,4),Fraction(5,4),Fraction(1,3)])
def test_invalid_or_rounded_visibility_is_rejected(visibility):
    with pytest.raises(ValueError):
        replacement_actions(visibility,2,1,premises=PREMISES)


def test_visibility_boundaries_and_large_exact_zero_coin_need_no_unknown_inverse():
    for v in (0,1):
        R=replacement_actions(v,64,64,premises=PREMISES)
        assert decode_dyadic(R["zero_label_coin_probability"])==Fraction(1,1 << 4096)
        assert decode_dyadic(R["conditional_Z_flip_probability"])==Fraction(1-v,2)
        assert R["unknown_preparation_inverse_used"] is False
    with pytest.raises(ValueError,match="UNKNOWN"):
        replacement_actions(1,4096,4096,premises=PREMISES)


def test_reused_batch_marginals_are_not_an_IID_two_input_source():
    R=4
    iid_equal=Fraction(sum(a==b for a,b in product(range(R),repeat=2)),R*R)
    reused_equal=Fraction(sum(a==a for a in range(R)),R)
    assert iid_equal==Fraction(1,4) and reused_equal==1


def js_check(R,tmp_path):
    target=tmp_path/"certificate.json"
    target.write_text(json.dumps(R))
    return subprocess.run(["node",str(CHECKER),str(target)],capture_output=True,text=True)


def test_live_provenance_and_independent_complete_censuses(report,tmp_path):
    assert json.loads(REPORT.read_text())==report
    assert json.loads(CONTRACT.read_text())["contract_id"]==CONTRACT_ID
    checked=js_check(report,tmp_path)
    assert checked.returncode==0,checked.stderr
    assert json.loads(checked.stdout)["exact_source_levels"]==2


@pytest.mark.parametrize("mutation",["raw_count","conditional_mass","restored_mass","pure_zero","visibility","cost","premise","scope","promotion"])
def test_checker_rejects_false_channel_noise_supply_and_scope_claims(report,tmp_path,mutation):
    R=deepcopy(report)
    C=R["two_level_exact_censuses"][0]
    if mutation=="raw_count":
        C["joint_label_visibility_rows"][0]["raw_count"]+=1
    elif mutation=="conditional_mass":
        C["accepted_nonzero_input_rows"][0]["conditional_probability"]="1"
    elif mutation=="restored_mass":
        C["joint_label_visibility_rows"][0]["restored_probability"]="0"
    elif mutation=="pure_zero":
        C["replacement_recipes_by_exponent"][0]["recipe"]["conditional_Z_flip_probability"]={"numerator_hex":"0x0","denominator_binary_exponent":0}
    elif mutation=="visibility":
        C["replacement_recipes_by_exponent"][0]["recipe"]["visibility"]={"numerator_hex":"0x1","denominator_binary_exponent":0}
    elif mutation=="cost":
        R["implemented_wrapper_supply"]["original_qubits_per_second_level_restored_output"]="16"
    elif mutation=="premise":
        R["assumed_not_inferred_premises"]["original_higher_label_transcript_discarded"]=False
    elif mutation=="scope":
        R["scope"]["all_joint_natural_lattice_noise_models_covered"]=True
    else:
        R["accepted_speedup_candidate"]=True
    assert js_check(R,tmp_path).returncode!=0


def test_read_only_CLI_does_not_mutate_live_artifact():
    before=REPORT.read_bytes()
    result=subprocess.run([sys.executable,"qsearch.py","dcp-noise-matched-source","--no-write"],
                          cwd=ROOT,capture_output=True,text=True)
    assert result.returncode==0,result.stderr
    assert json.loads(result.stdout)["actual_natural_source_certified"] is False
    assert REPORT.read_bytes()==before
