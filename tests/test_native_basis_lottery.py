"""Original-data completion is not a producer, truth certificate or general no-go."""
from copy import deepcopy
from dataclasses import replace
from fractions import Fraction
import json
import subprocess

import pytest

from theorems import native_basis_lottery as B


def stored(): return json.loads(B.REPORT.read_text())


def records(control):
    return tuple(B.NoisyLinearRecord(tuple(B._certificate_int(a) for a in r["label"]),
        B._certificate_int(r["value"]),B._certificate_int(r["modulus"]),r["source_id"]) for r in control["original_records"])


def node_check(p):
    return subprocess.run(["node", "-e", "const C=require('./research/certificates/native_basis_lottery_crosscheck.js');let s='';process.stdin.on('data',x=>s+=x);process.stdin.on('end',()=>console.log(JSON.stringify(C.verify(JSON.parse(s)))));"],
        input=json.dumps(p), text=True, capture_output=True, cwd=B.ROOT)


@pytest.mark.parametrize("index", (0, 1, 2))
def test_actual_original_unit_bases_recover_without_cubic_features(index):
    c=stored()["actual_original_controls"][index];r=B.complete(records(c), B._certificate_int(c["coefficient"]),
        tuple(B._certificate_int(a) for a in c["multiple"]),B._certificate_int(c["radius"]))
    assert r["candidate_secret"] == tuple(B._certificate_int(a) for a in c["truth_fixture_only"]["original_secret"])
    assert r["cubic_features_compiled"] == 0
    assert r["original_candidate_verification_evaluations"] == len(records(c))*sum("public_basis_model" in t for t in r["trial_records"])
    assert r["original_response_rounding_evaluations"] == len(records(c)[0].label)*sum("public_basis_model" in t for t in r["trial_records"])
    assert not r["multiple_producer_supplied"] and not r["fixed_instance_radius_uniqueness_certified"]
    assert not r["actual_planted_secret_or_noise_law_certified"]
    if index == 2: assert records(c)[0].modulus > 2**53


def test_nonbasis_noise_does_not_require_full_bank_rounded_consistency():
    c=stored()["actual_original_controls"][0];raw=records(c);r=B.complete(raw,81,c["multiple"],c["radius"])
    assert [t["status"] for t in r["trial_records"]] == ["SINGULAR_UNIT_MINOR_NOT_NO_SECRET"]*2+["ORIGINAL_RADIUS_FIT"]
    g,Q=81,raw[0].modulus//81;x=r["quotient_model"]["known_quotient_IF_multiple_is_true"]
    h=r["trial_records"][-1]["missing_quotient_candidate"]
    rhs=B.nearest_odd_division((raw[0].value-sum(a*b for a,b in zip(raw[0].label,x))) % raw[0].modulus,Q) % g
    assert rhs != sum(a*b for a,b in zip(raw[0].label,h)) % g
    assert r["trial_records"][-1]["original_fit"]["original_records_checked"] == len(raw)


def test_odd_dimension_and_odd_original_count_require_no_padded_copies():
    c=stored()["actual_original_controls"][1];raw=records(c)[:-1];r=B.complete(raw,3,c["multiple"],c["radius"])
    assert len(raw) % 2 and len(raw[0].label) % 2
    assert r["candidate_secret"] == tuple(c["truth_fixture_only"]["original_secret"])
    assert r["unused_tail_original_IDs"] == tuple(s.source_id for s in raw[(len(raw)//3)*3:])
    assert not r["paired_original_records_required"] and not r["new_independent_original_samples_created"]


def test_unit_multiple_preimage_bypasses_irrelevant_basis_caps_but_checks_every_original():
    c=stored()["actual_original_controls"][0];raw=records(c);truth=tuple(c["truth_fixture_only"]["original_secret"])
    w=tuple(-2*s % raw[0].modulus for s in truth)
    r=B.complete(raw,-2,w,c["radius"],max_blocks=1,max_minor_entries=1)
    assert r["candidate_secret"] == truth and r["blocks_attempted"] == 0
    assert r["original_candidate_verification_evaluations"] == len(raw)
    wrong=tuple((s+1) % raw[0].modulus for s in truth)
    r=B.complete(raw,1,wrong,0)
    assert r["candidate_secret"] is None and r["unit_fit"]["original_records_checked"] == len(raw)


def test_exact_nonunit_image_failure_does_not_execute_any_block():
    c=stored()["actual_original_controls"][0];r=B.complete(records(c),81,(1,)*4,0)
    assert r["status"] == "EXACT_NONUNIT_IMAGE_INCOMPATIBILITY"
    assert r["blocks_attempted"] == r["original_candidate_verification_evaluations"] == 0


@pytest.mark.parametrize("caps", ({"max_blocks":1},{"max_minor_entries":1}))
def test_complete_schedule_caps_abort_before_any_execution_even_with_permissive_cache(caps):
    c=stored()["actual_original_controls"][0];raw=records(c);cache=B.BasisBank(raw)
    r=B.complete(raw,81,c["multiple"],c["radius"],bank=cache,**caps)
    assert r["status"] == "COMPLETE_BLOCK_SCHEDULE_CAP_EXCEEDED_NOT_NO_SECRET"
    assert r["blocks_attempted"] == cache.rank_calls == cache.inverse_calls == 0
    assert not r["complete_schedule_or_original_fit_found"]


def test_too_few_rows_and_singular_schedule_are_not_no_secret_certificates():
    c=stored()["actual_original_controls"][0];r=B.complete(records(c)[:3],81,c["multiple"],c["radius"])
    assert r["status"] == "INSUFFICIENT_ORIGINAL_ROWS_NOT_NO_SECRET" and r["candidate_secret"] is None
    f=B.falsifiers()[0];raw=records(f)
    assert int(B.nmod_mat([list(s.label) for s in raw],3).rank()) == 2
    assert f["completion"]["status"] == "NO_RADIUS_FIT_IN_DECLARED_BLOCKS_NOT_NO_SECRET"
    assert len(f["completion"]["trial_records"]) == 2


def test_false_radius_fit_and_harmless_wrapped_error_countercontrols():
    wrong,wrapped=B.falsifiers()[1:]
    assert wrong["completion"]["candidate_secret"] == (14,7) != wrong["truth_fixture_only"]["original_secret"]
    assert not wrong["completion"]["actual_planted_secret_or_noise_law_certified"]
    assert not wrong["completion"]["fixed_instance_radius_uniqueness_certified"]
    assert wrapped["truth_fixture_only"]["original_errors"][0] == 81
    assert wrapped["matches_truth_fixture"] and wrapped["completion"]["candidate_secret"] == (5,)


def test_label_cache_is_not_new_IID_trials_and_never_binds_different_responses():
    c=stored()["actual_original_controls"][0];raw=records(c);cache=B.BasisBank(raw)
    a=B.complete(raw,81,c["multiple"],c["radius"],bank=cache);counts=cache.rank_calls,cache.inverse_calls
    b=B.complete(raw,81,c["multiple"],c["radius"],bank=cache)
    assert a == b and counts == (cache.rank_calls,cache.inverse_calls) == (3,1)
    assert not b["schedule_orbits_are_new_IID_samples"]
    altered=(*raw[:-1],replace(raw[-1],value=(raw[-1].value+1) % raw[-1].modulus))
    with pytest.raises(ValueError): B.complete(altered,81,c["multiple"],c["radius"],bank=cache)
    assert B.BasisBank(altered).label_sha256 == cache.label_sha256
    with pytest.raises(ValueError): cache.rank(True)
    with pytest.raises(ValueError): cache.inverse(True,81)


@pytest.mark.parametrize("bad", ((),(object(),)))
def test_original_bank_requires_typed_nonempty_originals(bad):
    with pytest.raises(ValueError): B.original_bank(bad)


def test_duplicate_ids_inconsistent_shape_and_nonexact_parameters_rejected():
    c=stored()["actual_original_controls"][0];raw=records(c)
    with pytest.raises(ValueError): B.original_bank((raw[0],raw[0]))
    with pytest.raises(ValueError): B.original_bank((raw[0],B.NoisyLinearRecord((0,),0,81,"other")))
    for kw in ({"radius":True},{"radius":raw[0].modulus//4+1},{"max_blocks":0},{"max_minor_entries":1.0},{"coefficient":0}):
        args={"coefficient":81,"multiple":c["multiple"],"radius":c["radius"],**kw}
        with pytest.raises(ValueError): B.complete(raw,**args)


def test_unknown_coefficient_workflow_completely_scans_and_pays_cached_bases():
    c=stored()["actual_original_controls"][0];raw=records(c);s=B.scan(raw,(c["multiple"],),81,c["radius"],4)
    assert s["trials_evaluated"] == s["planned_coefficient_trials"] == 162
    assert s["candidate_secret"] == tuple(c["truth_fixture_only"]["original_secret"])
    assert s["public_basis_rank_calls"] == 45 and s["public_basis_inverse_calls"] == 112
    assert s["original_response_rounding_evaluations"] == sum(t.get("completion",{}).get("original_response_rounding_evaluations",0) for t in s["trial_records"])
    assert s["original_candidate_verification_evaluations"] == sum(t.get("completion",{}).get("original_candidate_verification_evaluations",0) for t in s["trial_records"])
    assert not s["multiple_list_coverage_supplied"] and not s["actual_planted_truth_certified"]


def test_scan_valuation_filter_unit_only_early_fit_and_preflight_caps():
    c=stored()["actual_original_controls"][0];raw=records(c);truth=c["truth_fixture_only"]["original_secret"]
    negative=tuple(-s % raw[0].modulus for s in truth)
    s=B.scan(raw,(negative,),3,c["radius"],0,max_blocks=1)
    assert s["trials_evaluated"] == 3 < s["planned_coefficient_trials"]
    assert s["trial_records"][0]["status"] == "OUTSIDE_DECLARED_VALUATION_SCOPE"
    assert s["candidate_secret"] == tuple(truth) and s["public_basis_rank_calls"] == 0
    for kw in ({"max_pair_trials":1},{"max_blocks":1}):
        a=B.scan(raw,(c["multiple"],),81,c["radius"],4,**kw)
        assert a["trials_evaluated"] == a["block_attempts"] == a["original_response_rounding_evaluations"] == 0
        assert not a["complete_scan_or_original_fit_found"]


def test_maximum_valuation_clean_event_couples_every_smaller_true_quotient():
    q,gmax=3**6,3**3
    nearest=lambda x:(2*x.numerator+x.denominator)//(2*x.denominator)
    # Include negative and exact tie boundaries under the declared floor(x+1/2) convention.
    for j in range(-100,101):
        X=Fraction(j,200*gmax);e=nearest(q*X)
        if nearest(gmax*X) != 0: continue
        for d in range(4):
            g=3**d;Q=q//g
            assert B.nearest_odd_division(e,Q) == nearest(g*X) == 0
            secret=(311,607);lower=tuple(s % Q for s in secret)
            for u in (-4,-2,-1,1,2,4):
                c=g*u;w=tuple(c*s % q for s in secret)
                model=B.multiple_quotient(q,c,w)
                assert model.quotient_secret == lower
                a=(56,173);y=(sum(x*z for x,z in zip(a,secret))+e) % q
                residual=(y-sum(x*z for x,z in zip(a,lower))) % q
                assert B.nearest_odd_division(residual,Q) % g == sum(x*(z//Q) for x,z in zip(a,secret)) % g


@pytest.mark.parametrize("base,n", (("0",0),("0",4),("1",12),("1/3",15),("7/8",32)))
def test_probability_power_is_exactly_outward_not_float_fitted(base,n):
    box=B.power_box(base,n,bits=10);true=Fraction(base)**n
    assert Fraction(box["lower"]) <= true <= Fraction(box["upper"])
    assert Fraction(box["upper"])-Fraction(box["lower"]) <= Fraction(1,2**10)
    if n == 0: assert box["lower"] == box["upper"] == "1"


def test_probability_cap_is_unknown_not_zero_failure_and_zero_trials_fail_certainly():
    b=B.power_box("1/2",100,max_bit_work=10)
    assert b["status"] == "UNKNOWN_EXACT_POWER_CAP" and b["lower"] == "0" and b["upper"] == "1"
    s=B.basis_probability_ledger(4,0,"1/4",9)
    assert s["all_trials_fail_probability_upper"] == "1" and s["any_correct_basis_probability_upper"] == "0"


def test_constant_width_countercontrol_charges_ring_wraps_and_is_not_general_lower_bound():
    s=stored()["constant_width_large_dimension_countercontrol"]
    assert Fraction(s["no_correct_basis_probability_lower"]) > Fraction(99,100)
    assert s["correctness_upper_bound_includes_nonzero_wrapped_errors"]
    assert not s["general_decoder_lower_bound_proved"] and not s["unwrapped_clean_event_is_necessary_for_correctness"]
    wide=B.basis_probability_ledger(2,2,"3",3)
    assert Fraction(wide["one_row_ring_zero_probability_upper"]) > Fraction(wide["Gaussian_derived_error_law"]["zero"]["upper"])


def test_source_ledger_couples_noise_rank_radius_and_separation_without_coverage_or_conditioning():
    for s in stored()["Gaussian_source_profiles"]:
        assert Fraction(s["uniform_local_failure_upper"]) < Fraction(1,10**6)
        assert s["recovery_failure_upper_IF_source_coverage_and_complete_work_hold"] is None
        assert s["maximum_valuation_clean_event_covers_all_smaller_true_quotients"]
        assert not s["valuation_or_unit_part_union_multiplier_required"]
        assert not s["worst_case_lattice_reduction_compatibility_established"]
        assert not s["source_laws_or_multiple_producer_supplied"]
        assert s["default_complete_schedule_cap_feasible"]
    s=B.source_ledger(3,8,59,"1/100",0,20,coverage_failure="1/8")
    assert s["maximum_valuation_basis_event"] is None and s["original_rows_need_not_be_paired"]
    assert Fraction(s["recovery_failure_upper_IF_source_coverage_and_complete_work_hold"]) == min(1,Fraction(s["uniform_local_failure_upper"])+Fraction(1,8))
    with pytest.raises(ValueError): B.source_ledger(3,8,59,"1/100",8,20)
    with pytest.raises(ValueError): B.source_ledger(3,8,59,"1/100",0,20,coverage_failure="2")


def test_separate_trusted_Arb_probability_replay_and_tamper_rejection():
    p=stored();r=B.verify_probability_boxes(p)
    assert r["verified"] and r["Gaussian_laws_replayed"] == 7
    assert not r["independent_transcendental_certificate_supplied"]
    p["constant_width_large_dimension_countercontrol"]["nonzero_ring_wrap_tail"]["upper"] = "0"
    with pytest.raises(ValueError): B.verify_probability_boxes(p)


def test_independent_original_ring_and_source_event_replay():
    r=node_check(stored());assert r.returncode == 0,r.stderr
    result=json.loads(r.stdout);assert result["coefficient_trials_replayed"] == 162
    assert not result["Gaussian_transcendental_endpoints_independently_verified"]


@pytest.mark.parametrize("kind", ("inverse","minor","original-ID","parent-hash","rounding","candidate","fit-distance","verification-work","rounding-work","cache-work","scan-order","clean-power","failure-power","wrap-tail","source-width","source-count","conditioning","valuation-union","truth","Gaussian-solver","dependency","hash"))
def test_independent_checker_rejects_tampered_transcripts_probabilities_and_claims(kind):
    p=deepcopy(stored());r=p["actual_original_controls"][0]["completion"];t=r["trial_records"][-1]
    s=p["Gaussian_source_profiles"][0];b=s["maximum_valuation_basis_event"];scan=p["actual_unknown_coefficient_scan"]
    if kind == "inverse": t["public_basis_model"]["inverse"][0][0] = (t["public_basis_model"]["inverse"][0][0]+1) % 81
    elif kind == "minor": t["public_basis_model"]["minor"][0][0] = (t["public_basis_model"]["minor"][0][0]+1) % 81
    elif kind == "original-ID": t["original_source_IDs"][0] = "fabricated"
    elif kind == "parent-hash": t["response_receipts"][0]["parent_record_sha256"] = "0"*64
    elif kind == "rounding": t["response_receipts"][0]["rounded_missing_quotient_equation"] = 100
    elif kind == "candidate": r["candidate_secret"][0] += 1
    elif kind == "fit-distance": t["original_fit"]["original_circular_error_distances"][0] = 0
    elif kind == "verification-work": r["original_candidate_verification_evaluations"] = 0
    elif kind == "rounding-work": scan["original_response_rounding_evaluations"] = 0
    elif kind == "cache-work": scan["public_basis_inverse_calls"] = 0
    elif kind == "scan-order": scan["trial_records"][0]["coefficient"] = 81
    elif kind == "clean-power": b["unwrapped_clean_basis_probability_box"]["lower"] = "1"
    elif kind == "failure-power": b["all_trials_fail_power_box"]["upper"] = "0"
    elif kind == "wrap-tail": b["nonzero_ring_wrap_tail"]["integer_error_radius"] = 0
    elif kind == "source-width": s["original_Gaussian_width"] = "1/2"
    elif kind == "source-count": b["disjoint_original_trials"] += 1
    elif kind == "conditioning": s["conditioning_on_data_selected_multiple_truth_used"] = True
    elif kind == "valuation-union": s["valuation_or_unit_part_union_multiplier_required"] = True
    elif kind == "truth": r["actual_planted_secret_or_noise_law_certified"] = True
    elif kind == "Gaussian-solver": p["Gaussian_LWE_solver_or_new_quantum_algorithm"] = True
    elif kind == "dependency": p["dependency_sha256"]["native_full_root_slice.py"] = "0"*64
    else: p["producer_sha256"] = "0"*64
    assert node_check(p).returncode != 0
