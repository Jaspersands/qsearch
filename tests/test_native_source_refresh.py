"""Conditional source refresh must not turn algebra/calibration into an oracle."""
from copy import deepcopy
from fractions import Fraction
from itertools import product
import json
import subprocess

import pytest

from theorems import native_source_refresh as S
from native_basis_lottery import _certificate_int


def stored(): return json.loads(S.REPORT.read_text())


def records(rows):
    return tuple(S.NoisyLinearRecord(tuple(_certificate_int(a) for a in r["label"]),
        _certificate_int(r["value"]),_certificate_int(r["modulus"]),r["source_id"]) for r in rows)


def node_check(p):
    return subprocess.run(["node","-e","const C=require('./research/certificates/native_source_refresh_crosscheck.js');let s='';process.stdin.on('data',x=>s+=x);process.stdin.on('end',()=>console.log(JSON.stringify(C.verify(JSON.parse(s)))));"],
        input=json.dumps(p),text=True,capture_output=True,cwd=S.ROOT)


@pytest.mark.parametrize("n,d,m", ((1,1,1),(1,1,3),(1,2,3),(2,1,3)))
def test_complete_original_matrix_sign_census_matches_exact_composite_collision_identity(n,d,m):
    c=S.sign_census(n,d,m)
    assert Fraction(c["exact_mean_chi_square"]) == Fraction(3**(n*d)-1,2**m)
    assert c["original_matrices_checked"] == 3**(n*d*m)
    assert sum(c["conditional_TV_histogram"].values()) == c["original_matrices_checked"]
    assert Fraction(c["zero_matrix_conditional_TV"]) == 1-Fraction(1,3**(n*d))
    assert Fraction(c["exact_mean_conditional_label_TV"])**2 <= Fraction(c["exact_mean_chi_square"])/4
    assert not c["all_source_matrices_individually_uniform_claimed"]
    with pytest.raises(ValueError): S.sign_census(n,d,m,max_work=1)


def test_full_rank_does_not_certify_a_conditionally_uniform_sign_sum_source():
    labels=(1,0,0);q=9;values=[sum(t*a for t,a in zip(row,labels)) % q for row in product((-1,1),repeat=3)]
    assert len(set(values)) == 2 and labels[0] % 3 != 0
    TV=sum(abs(Fraction(values.count(x),8)-Fraction(1,q)) for x in range(q))/2
    assert TV == Fraction(7,9)


def test_exact_label_failure_bound_is_conservative_and_does_not_expand_large_denominators():
    for n,d,m,k in ((1,1,10,1),(2,2,30,3),(3,3,50,5)):
        b=S.label_quality_ledger(n,d,m,k,"1/8")
        exact=Fraction(k*k,4)*64*Fraction(3**(n*d)-1,2**m)
        assert Fraction(b["label_quality_failure_upper"]) >= min(1,exact)
        assert Fraction(b["exact_expected_chi_square_IF_small"]) == Fraction(3**(n*d)-1,2**m)
    b=S.label_quality_ledger(128,39,128**3,9216,"1/2097152")
    assert b["exact_expected_chi_square_IF_small"] is None
    assert b["label_quality_failure_upper"] == str(Fraction(1,2**64))
    assert not b["one_observed_full_rank_bank_quality_certified"]
    with pytest.raises(ValueError): S.label_quality_ledger(1024,128,10,1,"1/8")


def test_actual_original_sign_mask_transform_pays_full_ancestry_and_hidden_advice_separation():
    c=S.control();raw=records(c["original_records"]);f=c["transform"]
    assert f["sign_label_accumulation_terms"] == 30 and f["sign_response_accumulation_terms"] == 15
    assert f["mask_dot_product_terms"] == 6 and f["original_response_rounding_evaluations"] == 5
    assert f["derived_original_record_count"] == f["original_records_paid_once"] == 5
    assert set(f["producer_input"]) == {"modulus","labels","responses"}
    assert not f["producer_input_contains_signs_mask_prefix_or_source_metadata"]
    for output in f["output_receipts"]:
        assert output["ALL_original_source_IDs"] == tuple(r.source_id for r in raw)
    truth=c["secret_AND_original_errors_FOR_CALIBRATION_ONLY"];g=f["modulus"];L=f["original_scale"]
    h=tuple(s//L for s in truth["secret"]);shifted=tuple((x-z) % g for x,z in zip(h,f["supplied_secret_mask"]))
    derived_errors=tuple(S.nearest_odd_division(e,L) for e in truth["errors"])
    assert any(h) and derived_errors == (1,-1,0,0,0)
    for t,a,y,dither in zip(f["supplied_sign_rows"],f["producer_input"]["labels"],f["producer_input"]["responses"],f["supplied_integer_dithers"]):
        assert (y-sum(x*z for x,z in zip(a,shifted))) % g == (sum(x*e for x,e in zip(t,derived_errors))+dither) % g
    assert not f["supplied_dithers_certified_Gaussian"] and not f["signs_and_mask_certified_IID_uniform"]


def test_transform_handles_original_root_and_high_root_without_float_or_even_record_assumptions():
    q=3**64;raw=(S.NoisyLinearRecord((q-2,),123,q,"high"),)
    r=S.refresh_node(raw,q,(0,),((-1,),),(17,),(-q+11,))
    assert r["original_scale"] == 1 and r["original_response_rounding_evaluations"] == 1
    assert r["producer_input"]["responses"] == ((-123+11-2*17) % q,)
    assert not r["source_quality_or_true_prefix_established"]


def test_false_prefix_does_not_receive_a_source_certificate():
    c=S.control();f=c["transform"];wrong=tuple((x+1) % f["original_scale"] for x in f["known_original_lower_prefix_IF_true"])
    r=S.refresh_node(records(c["original_records"]),81,wrong,f["supplied_sign_rows"],f["supplied_secret_mask"],f["supplied_integer_dithers"])
    assert r["producer_input"] == f["producer_input"]
    assert r["known_original_lower_prefix_IF_true"] != f["known_original_lower_prefix_IF_true"]
    assert r["original_quotient_receipts"] != f["original_quotient_receipts"]
    assert not r["source_quality_or_true_prefix_established"]


def test_whole_transform_cap_is_zero_work_not_no_source():
    c=S.control();f=c["transform"]
    r=S.refresh_node(records(c["original_records"]),81,f["known_original_lower_prefix_IF_true"],f["supplied_sign_rows"],f["supplied_secret_mask"],f["supplied_integer_dithers"],max_entries=1)
    assert r["status"] == "WHOLE_REFRESH_TRANSFORM_CAP_EXCEEDED_NOT_SOURCE_FAILURE"
    assert r["producer_input"] is None
    assert r["derived_original_record_count"] == r["sign_label_accumulation_terms"] == r["original_response_rounding_evaluations"] == 0


def test_shared_canonical_node_replays_the_same_original_quotient_without_truth_certificate():
    c=S.control();raw=records(c["original_records"]);f=c["transform"]
    node=S.canonical_quotient_node(raw,f["original_scale"],f["known_original_lower_prefix_IF_true"])
    assert node["record_receipts"] == f["original_quotient_receipts"]
    assert node["original_response_rounding_evaluations"] == len(raw)
    assert not node["true_prefix_or_noise_law_certified"]
    root=S.canonical_quotient_node(raw,1,(0,0))
    assert root["derived_records"] == tuple(r.public() for r in raw)
    with pytest.raises(ValueError): S.canonical_quotient_node(raw,raw[0].modulus,(0,0))
    with pytest.raises(ValueError): S.canonical_quotient_node(raw,True,(0,0))


@pytest.mark.parametrize("kind", ("sign","mask","prefix","dither","root","duplicate","shape"))
def test_transform_rejects_noncanonical_or_incomplete_inputs(kind):
    c=S.control();f=c["transform"];args={"records":records(c["original_records"]),"g":81,"prefix":f["known_original_lower_prefix_IF_true"],
        "signs":f["supplied_sign_rows"],"mask":f["supplied_secret_mask"],"dithers":f["supplied_integer_dithers"]}
    if kind == "sign": args["signs"] = ((True,)*5,)*3
    elif kind == "mask": args["mask"] = (81,0)
    elif kind == "prefix": args["prefix"] = (-1,0)
    elif kind == "dither": args["dithers"] = (1.0,0,0)
    elif kind == "root": args["g"] = 5
    elif kind == "duplicate": args["records"] = (args["records"][0],)*5
    else: args["signs"] = ((1,1),)
    with pytest.raises(ValueError): S.refresh_node(**args)


def test_common_energy_couples_all_true_root_rounding_without_independence_assumptions():
    X=(Fraction(-17,20),Fraction(4,9),Fraction(1,2));nearest=lambda x:(2*x.numerator+x.denominator)//(2*x.denominator)
    norm=sum(x*x for x in X)
    for dmin in (1,2,3):
        for d in range(dmin,6):
            g=3**d;e=tuple(nearest(g*x) for x in X)
            assert Fraction(sum(x*x for x in e),g*g) <= 2*norm+Fraction(len(X),2*3**(2*dmin))
    s=stored()["width_and_root_scope_profiles"][-1]
    assert not s["original_noise_independence_required_for_energy_Markov_bound"]
    assert not s["sign_sum_error_and_label_independence_assumed"]


def test_width_sweeps_do_not_inherit_advantage_or_hide_vacuous_energy_profiles():
    profiles=stored()["width_and_root_scope_profiles"]
    assert profiles[0]["status"] == "NO_DECLARED_ROOT_INTERVAL_ABOVE_ROUNDING_FLOOR"
    assert len(profiles) == 7
    for s in profiles[1:]:
        assert s["one_refresh_coverage_lower_IF_quality_and_external_contracts_hold"] is None
        assert s["one_refresh_unconditional_coverage_lower_IF_source_and_external_contracts_hold"] is None
        assert not s["same_narrow_width_producer_advantage_inherited"]
        assert not s["actual_source_law_quality_sampler_or_producer_certified"]
    assert profiles[1]["common_original_energy_failure_upper"] == profiles[4]["common_original_energy_failure_upper"] == "1"
    assert profiles[3]["common_energy_event_is_nonvacuous"] and profiles[6]["common_energy_event_is_nonvacuous"]
    assert profiles[3]["target_width_multiplier"] == str(32**15)


def test_conditional_coverage_requires_new_width_producer_sampler_and_primitive_secret_loss():
    args=(32,32,32**3,1728,23,28,Fraction(1,32**16),Fraction(1,32),Fraction(1,32**3),Fraction(1,32**3))
    missing=S.source_ledger(*args,ideal_producer_success="1/8")
    assert missing["one_refresh_coverage_lower_IF_quality_and_external_contracts_hold"] is None
    actual=S.source_ledger(*args,ideal_producer_success="1/8",sampler_TV_loss="1/1024")
    success=Fraction(1,8)-Fraction(2,32**3)-Fraction(1,3**32)-Fraction(1,1024)
    assert Fraction(actual["one_refresh_coverage_lower_IF_quality_and_external_contracts_hold"]) == success > 0
    source_failure=Fraction(actual["all_reachable_source_quality_failure_upper"])
    assert Fraction(actual["one_refresh_unconditional_coverage_lower_IF_source_and_external_contracts_hold"]) == (1-source_failure)*success
    impossible=S.source_ledger(2,8,100,10,1,2,"1/10","1/8","1/16","1/16",ideal_producer_success="1/2",sampler_TV_loss="0")
    assert not impossible["common_energy_event_is_nonvacuous"]
    assert impossible["one_refresh_unconditional_coverage_lower_IF_source_and_external_contracts_hold"] == "0"


def test_independent_entropy_transform_and_common_energy_replay():
    r=node_check(stored());assert r.returncode == 0,r.stderr
    p=json.loads(r.stdout);assert p["complete_original_matrices_censused"] == 1458
    assert not p["Gaussian_sampler_or_producer_supplied"]


@pytest.mark.parametrize("kind", ("label","response","original-hash","source-ID","work","metadata","Gaussian","uniform","chi-square","census-count","zero-source","label-exponent","label-bound","rounding-floor","energy","energy-failure","root-union","coverage","noise-correlation","advantage","invalid-producer-promise","alias-truth","sampler","producer","dependency","hash"))
def test_independent_checker_rejects_algebra_entropy_source_and_claim_tampering(kind):
    p=deepcopy(stored());f=p["actual_supplied_dither_control"]["transform"];s=p["width_and_root_scope_profiles"][-1];l=s["maximum_root_label_quality_ledger"];c=p["complete_sign_collision_censuses"][0]
    if kind == "label": f["producer_input"]["labels"][0][0] = (f["producer_input"]["labels"][0][0]+1) % 81
    elif kind == "response": f["producer_input"]["responses"][0] = (f["producer_input"]["responses"][0]+1) % 81
    elif kind == "original-hash": f["original_quotient_receipts"][0]["original_record_sha256"] = "0"*64
    elif kind == "source-ID": f["output_receipts"][0]["ALL_original_source_IDs"][0] = "fresh-original"
    elif kind == "work": f["sign_response_accumulation_terms"] = 0
    elif kind == "metadata": f["producer_input"]["mask"] = f["supplied_secret_mask"]
    elif kind == "Gaussian": f["supplied_dithers_certified_Gaussian"] = True
    elif kind == "uniform": f["signs_and_mask_certified_IID_uniform"] = True
    elif kind == "chi-square": c["exact_mean_chi_square"] = "0"
    elif kind == "census-count": c["original_matrices_checked"] = 1
    elif kind == "zero-source": c["zero_matrix_conditional_TV"] = "0"
    elif kind == "label-exponent": l["label_quality_failure_power2_exponent_upper"] -= 1
    elif kind == "label-bound": l["label_quality_failure_upper"] = "0"
    elif kind == "rounding-floor": s["normalized_rounding_energy_floor_upper"] = "0"
    elif kind == "energy": s["common_continuous_original_energy_threshold"] = "1"
    elif kind == "energy-failure": s["common_original_energy_failure_upper"] = "0"
    elif kind == "root-union": s["reachable_fixed_roots_covered"] = 1
    elif kind == "coverage": s["one_refresh_unconditional_coverage_lower_IF_source_and_external_contracts_hold"] = "1/8"
    elif kind == "noise-correlation": s["sign_sum_error_and_label_independence_assumed"] = True
    elif kind == "advantage": s["same_narrow_width_producer_advantage_inherited"] = True
    elif kind == "invalid-producer-promise": s["ideal_target_source_producer_success_lower_EXTERNAL"] = "2"
    elif kind == "alias-truth": p["false_prefix_calibration_alias"]["same_input_certifies_true_prefix"] = True
    elif kind == "sampler": p["source_refresh_sampler_implemented"] = True
    elif kind == "producer": p["source_conditioned_producer_amplification_established"] = True
    elif kind == "dependency": p["dependency_sha256"]["native_basis_lottery.py"] = "0"*64
    else: p["producer_sha256"] = "0"*64
    assert node_check(p).returncode != 0
