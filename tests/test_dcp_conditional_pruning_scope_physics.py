from copy import deepcopy
import json
from pathlib import Path
import subprocess

import pytest

from theorems.dcp_interleaved_tree_merge_syndrome_pruning_audit import (
    DEFAULT_ARTIFACT_PATH, build_dcp_interleaved_tree_merge_syndrome_pruning_audit,
    evaluate_syndrome_pruning_case,
)

ROOT=Path(__file__).resolve().parents[1]
CHECKER=ROOT/"research/certificates/dcp_interleaved_tree_merge_syndrome_pruning_audit_crosscheck.js"


def test_q3_critical_visibility_and_both_proxies_are_exact_zero_not_float_residuals():
    C=evaluate_syndrome_pruning_case(case_id="exact-tie",q=3,p_err_num=2,p_err_den=3,max_depth=8)
    assert C["baseline_lambda_1"]==0
    assert C["theorem3_verified"] is True  # ONLY the proxy upper bound.
    assert C["direct_leaf_dominance_is_a_universal_theorem"] is False
    assert C["strict_direct_leaf_dominance_in_this_finite_case"] is False
    for row in C["depth_rows"]:
        assert row["conditional_root_visibility"]==0
        assert row["throughput_adjusted_pruned_snr"]==row["classical_k_leaf_snr"]==0
        assert row["direct_leaf_comparison"]=="EXACT_ZERO_TIE"
        assert row["pruned_to_leaf_snr_ratio"] is None


@pytest.mark.parametrize("q,p",[(3,0),(3,1),(4,0),(4,1),(8,0),(8,1)])
def test_degenerate_probability_endpoints_are_neutral_not_strictly_purifying_or_degrading(q,p):
    C=evaluate_syndrome_pruning_case(case_id="endpoint",q=q,p_err_num=p,p_err_den=1,max_depth=3)
    assert C["expected_purification_regime"]=="ENDPOINT_NEUTRAL"
    assert abs(C["step1_visibility_gain"])<1e-12
    assert C["all_theorems_verified"] is True
    assert C["physical_equality_instrument_supplied"] is False


def test_physics_access_receipt_rejects_three_state_equality_and_no_CNOT_error_law_is_claimed():
    C=evaluate_syndrome_pruning_case(case_id="no-oracle",q=4,p_err_num=1,p_err_den=2,max_depth=2)
    assert C["analysis_model"]=="CONDITIONAL_CLASSICAL_LATENT_ERROR_RETAIN_ONE_LEAF"
    assert C["source_access_receipt"]["latent_error_equality_available"] is False
    assert C["source_access_receipt"]["extra_source_access_proved"] is False
    assert C["physical_equality_instrument_supplied"] is False
    assert C["CNOT_sum_merge_error_law_claimed"] is False


def test_live_artifact_guardrails_and_independent_replay():
    payload=build_dcp_interleaved_tree_merge_syndrome_pruning_audit()
    assert json.loads(DEFAULT_ARTIFACT_PATH.read_text())==payload
    assert payload["status"]=="CONDITIONAL_CLASSICAL_IDENTITIES_PHYSICAL_ACCESS_NOT_SUPPLIED"
    assert all(value is False for value in payload["guardrails"].values())
    result=subprocess.run(["node",str(CHECKER)],capture_output=True,text=True,check=True)
    assert json.loads(result.stdout)["case_count"]==8


def test_checker_rejects_promotion_back_to_a_physical_filter(tmp_path):
    payload=build_dcp_interleaved_tree_merge_syndrome_pruning_audit()
    payload["cases"][0]["physical_equality_instrument_supplied"]=True
    path=tmp_path/"forged.json"
    path.write_text(json.dumps(payload))
    result=subprocess.run(["node",str(CHECKER),str(path)],capture_output=True,text=True)
    assert result.returncode!=0


@pytest.mark.parametrize("q,num,den,depth",[(2,1,2,1),(3,2,1,1),(3,1,0,1),(3,-1,2,1),(3,1,2,0)])
def test_malformed_conditional_calculations_fail_closed(q,num,den,depth):
    with pytest.raises(ValueError):
        evaluate_syndrome_pruning_case(case_id="invalid",q=q,p_err_num=num,p_err_den=den,max_depth=depth)
