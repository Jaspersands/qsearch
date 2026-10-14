"""Recursion must not manufacture independent sources or certified producer branches."""
from copy import deepcopy
from fractions import Fraction
import json
import subprocess

import pytest

from theorems import native_recursive_quotient_audit as R
from native_basis_lottery import _certificate_int


def stored(): return json.loads(R.REPORT.read_text())


def records(rows):
    return tuple(R.NoisyLinearRecord(tuple(_certificate_int(a) for a in r["label"]),
        _certificate_int(r["value"]),_certificate_int(r["modulus"]),r["source_id"]) for r in rows)


def hypotheses(raw,target,coefficients):
    q=raw[0].modulus;s=tuple(target);output=[]
    for c in coefficients:
        w=tuple(c*x % q for x in s);output.append((c,w));m=R.multiple_quotient(q,c,w)
        if m.factor==1: break
        s=tuple(x//m.remaining_modulus for x in s);q=m.factor
    return tuple(output)


def node_check(p):
    return subprocess.run(["node","-e","const C=require('./research/certificates/native_recursive_quotient_crosscheck.js');let s='';process.stdin.on('data',x=>s+=x);process.stdin.on('end',()=>console.log(JSON.stringify(C.verify(JSON.parse(s)))));"],
        input=json.dumps(p),text=True,capture_output=True,cwd=R.ROOT)


@pytest.mark.parametrize("index", (0,1))
def test_actual_odd_original_chain_preserves_every_record_and_fits_full_root(index):
    c=stored()["actual_chain_calibrations"][index];raw=records(c["original_records"])
    pairs=tuple((_certificate_int(a),tuple(_certificate_int(x) for x in w)) for a,w in c["supplied_hypotheses_FOR_CALIBRATION_ONLY"])
    r=R.adapt_chain(raw,pairs,_certificate_int(c["chain"]["verification_radius"]))
    assert r["candidate_secret"] == tuple(_certificate_int(x) for x in c["original_secret_FOR_CALIBRATION_ONLY"])
    assert len(raw) % 2 and r["original_fit"]["original_records_checked"] == len(raw)
    assert all(r["supplied_multiple_chain_equations_verified"])
    assert r["sequential_response_rounding_evaluations"] == len(raw)*(len(r["steps"])-1)
    assert r["canonical_composition_rounding_evaluations"] == r["sequential_response_rounding_evaluations"]
    assert not r["true_prefix_or_Gaussian_law_certified"] and not r["planted_truth_or_uniqueness_certified"]
    for step in r["steps"][:-1]:
        assert step["source_IDs_preserved"] and step["composition_verified_on_every_original"]
        assert tuple(x["source_id"] for x in step["derived_records"]) == tuple(s.source_id for s in raw)
        assert step["canonical_node"]["modulus"] < step["parent_modulus"]


@pytest.mark.parametrize("target", ((425,211),(17,341),(0,0)))
def test_different_compatible_paths_with_same_prefix_merge_even_when_the_prefix_is_false(target):
    c=R.control(729,(425,211),(9,),(-151,180,1,-1,5));raw=records(c["original_records"])
    a=R.adapt_chain(raw,hypotheses(raw,target,(9,)),180)
    b=R.adapt_chain(raw,hypotheses(raw,target,(81,9)),180)
    assert a["final_canonical_node"] == b["final_canonical_node"]
    assert a["steps"][-1]["derived_records"] == b["steps"][-1]["derived_records"]
    assert a["steps"][-1]["canonical_node_sha256"] == b["steps"][-1]["canonical_node_sha256"]
    assert not a["true_prefix_or_Gaussian_law_certified"]
    # Sharing a root without sharing an original prefix does NOT license a merge.
    if target != (425,211):
        good=R.adapt_chain(raw,hypotheses(raw,(425,211),(9,)),180)
        assert a["final_canonical_node"] != good["final_canonical_node"]


def test_exact_nested_odd_rounding_including_negative_integers_and_wraps():
    for L in (1,3,9,27):
        for Q in (1,3,9):
            for e in range(-500,501):
                assert R.nearest_odd_division(R.nearest_odd_division(e,L),Q) == R.nearest_odd_division(e,L*Q)


def test_true_quotient_retains_same_gaussian_variable_not_new_error_samples():
    q=729;s=425;nearest=lambda x:(2*x.numerator+x.denominator)//(2*x.denominator)
    for j in range(-60,61):
        X=Fraction(j,70);e=nearest(q*X)
        raw=tuple(R.NoisyLinearRecord((a,), (a*s+e) % q,q,f"original:{a}") for a in (1,17,311))
        chain=R.adapt_chain(raw,hypotheses(raw,(s,),(81,9)),0)
        for step in chain["steps"]:
            g=step["canonical_node"]["modulus"];L=q//g;h=s//L
            for row in step["derived_records"]:
                assert (row["value"]-row["label"][0]*h) % g == nearest(g*X) % g
    assert not chain["new_independent_original_samples_created"]


def test_false_prefix_is_not_automatically_the_standard_full_uniform_null():
    w=R.wrong_prefix_census()
    assert w["conditional_TV_from_full_uniform"] == ("2/3",)*9
    assert all(sorted(row)==[0]*6+[3]*3 for row in w["conditional_child_value_counts_by_child_label"])
    assert not w["wrong_prefix_implies_full_uniform_child"] and not w["candidate_or_decision_oracle_created"]


def test_path_cap_and_incompatibility_do_not_guess_or_claim_no_original_secret():
    raw=(R.NoisyLinearRecord((1,),5,81,"x"),)
    r=R.adapt_chain(raw,((9,(45,)),(1,(0,))),0,max_steps=1)
    assert r["steps"] == () and r["sequential_response_rounding_evaluations"] == 0
    assert not r["complete_declared_path_or_terminal_preimage"]
    r=R.adapt_chain(raw,((9,(1,)),),0)
    assert r["status"] == "INCOMPATIBLE_SUPPLIED_PATH_NOT_NO_ORIGINAL_SECRET"
    assert r["candidate_secret"] is None
    with pytest.raises(ValueError): R.adapt_chain(raw,((81,(0,)),),0)
    with pytest.raises(ValueError): R.adapt_chain(raw,(),0)
    with pytest.raises(ValueError): R.adapt_chain(raw,((1,(5,)),),True)


def test_unit_termination_verifies_originals_and_reports_unconsumed_supplied_path():
    raw=(R.NoisyLinearRecord((1,),5,81,"x"),)
    r=R.adapt_chain(raw,((-2,(71,)),(1,(0,))),0)
    assert r["candidate_secret"] == (5,) and r["unconsumed_supplied_hypotheses"] == 1
    assert r["original_fit"]["original_records_checked"] == 1
    wrong=R.adapt_chain(raw,((1,(6,)),),0)
    assert wrong["candidate_secret"] is None and wrong["terminal_original_algebraic_preimage"] == (6,)
    assert wrong["status"] == "TERMINAL_PREIMAGE_ORIGINAL_RADIUS_FIT_FAILED"


def test_complete_tree_cost_and_random_path_loss_are_not_free_polynomial_work():
    c=R.recursion_cost(16,4,"1/8")
    assert c["complete_tree_leaves_upper"] == 65536 and c["complete_tree_nodes_upper"] == 69905
    assert c["random_one_branch_success_IF_every_visited_true_list_covers"] == "1/65536"
    assert c["all_required_fixed_root_events_Frechet_lower"] == "0"
    assert c["all_levels_coverage_lower_IF_conditional_contract_proved"] is None
    assert not c["polynomial_branch_budget_implies_polynomial_total_work"]
    assert not c["tree_bound_is_a_general_reduction_lower_bound"]
    one=R.recursion_cost(1,8,"1")
    assert one["complete_tree_nodes_upper"] == 9 and one["complete_tree_leaves_upper"] == 1
    with pytest.raises(ValueError): R.recursion_cost(2,100000,"1/8")


def test_source_marginals_do_not_multiply_but_external_conditional_contract_can():
    c=R.recursion_cost(2,2,"1/2")
    assert c["all_required_fixed_root_events_Frechet_lower"] == "0"
    assert not c["marginal_success_product_is_justified"] and not c["same_bank_repetition_amplifies_source_good_fraction"]
    assert not c["fixed_root_Frechet_bound_covers_unknown_adaptive_root_selection"]
    c=R.recursion_cost(2,4,"1/8","7/8")
    assert c["all_levels_coverage_lower_IF_conditional_contract_proved"] == "2401/4096"
    assert not c["actual_coverage_or_producer_contract_established"]


@pytest.mark.parametrize("r,C,d", ((1,100,0),(8,1,0),(8,2,0),(8,3,1),(8,80,3),(8,81,4),(8,1000000,7)))
def test_nonzero_modulus_and_centered_size_bound_strictly_limit_first_child(r,C,d):
    c=R.fixed_root_source_contract(3,r,"1/100",C)
    assert c["first_nonunit_child_root_digits_upper"] == d
    assert c["first_nonunit_child_modulus_upper"] == 3**d
    assert c["nonunit_child_possible_within_declared_bound"] == (r>1 and C>=3)
    assert not c["same_normalized_width_guarantees_a_distinguisher_at_every_root"]


def test_primitive_original_does_not_certify_primitive_high_quotient():
    assert 4 % 3 != 0 and (4//9) % 3 == 0
    c=R.fixed_root_source_contract(3,8,"1/100",81)
    assert Fraction(c["all_proper_fixed_true_root_primitive_failure_union_upper_IF_original_secret_uniform"]) == Fraction(7,27)
    assert not c["original_primitive_secret_implies_every_high_quotient_primitive"]
    assert not c["adaptively_selected_root_has_unconditioned_Gaussian_law_certified"]
    assert not c["published_rounded_Gaussian_reduction_applicable_at_all_roots"]


def test_independent_same_original_composition_and_cost_replay():
    r=node_check(stored());assert r.returncode == 0,r.stderr
    p=json.loads(r.stdout);assert p["actual_original_composition_equations"] == 112
    assert not p["recursive_producer_or_reduction_supplied"]


@pytest.mark.parametrize("kind", ("prefix","scale","parent-hash","original-hash","response","child-ID","candidate","source-truth","cost","success","conditional","adaptive","same-noise","primitive","root-limit","wrong-prefix-null","paper-promise","reduction","dependency","hash"))
def test_independent_checker_rejects_algebra_cost_source_and_reduction_tampering(kind):
    p=deepcopy(stored());c=p["actual_chain_calibrations"][0]["chain"];s=c["steps"][0];a=p["ambiguity_profiles"][0];source=p["source_contract_profiles"][0]
    if kind == "prefix": s["canonical_node"]["known_original_lower_prefix_IF_path_true"][0] += 1
    elif kind == "scale": s["canonical_node"]["original_scale"] = 1
    elif kind == "parent-hash": s["record_receipts"][0]["parent_record_sha256"] = "0"*64
    elif kind == "original-hash": s["record_receipts"][0]["original_record_sha256"] = "0"*64
    elif kind == "response": s["derived_records"][0]["value"] = (s["derived_records"][0]["value"]+1) % s["derived_records"][0]["modulus"]
    elif kind == "child-ID": s["derived_records"][0]["source_id"] = "new-independent-sample"
    elif kind == "candidate": c["candidate_secret"][0] += 1
    elif kind == "source-truth": c["true_prefix_or_Gaussian_law_certified"] = True
    elif kind == "cost": a["complete_tree_nodes_upper"] = 1
    elif kind == "success": a["all_required_fixed_root_events_Frechet_lower"] = "1/8"
    elif kind == "conditional": a["all_levels_coverage_lower_IF_conditional_contract_proved"] = "1/8"
    elif kind == "adaptive": a["fixed_root_Frechet_bound_covers_unknown_adaptive_root_selection"] = True
    elif kind == "same-noise": source["fixed_true_quotient_laws_share_original_noise_and_are_not_independent"] = False
    elif kind == "primitive": source["original_primitive_secret_implies_every_high_quotient_primitive"] = True
    elif kind == "root-limit": source["first_nonunit_child_root_digits_upper"] += 1
    elif kind == "wrong-prefix-null": p["wrong_prefix_subgroup_countercontrol"]["conditional_TV_from_full_uniform"][0] = "0"
    elif kind == "paper-promise": p["published_interface_scope"]["list_outputs_are_certified_true_pairs"] = True
    elif kind == "reduction": p["complete_recursive_search_to_decision_reduction_established"] = True
    elif kind == "dependency": p["dependency_sha256"]["native_basis_lottery.py"] = "0"*64
    else: p["producer_sha256"] = "0"*64
    assert node_check(p).returncode != 0
