"""Exact law, actual original completion, split rank and honest source events."""
from copy import deepcopy
from fractions import Fraction
from itertools import product
import json
import subprocess

from flint import ctx, nmod_mat
import pytest

from theorems import native_gaussian_quotient_completion as G
from native_small_alphabet_decoder import features
from ternary_noise_degradation import NoisyLinearRecord


def stored(): return json.loads(G.REPORT.read_text())


def raw_control(index=0):
    c = stored()["actual_original_data_controls"][index]
    raw = tuple(NoisyLinearRecord(tuple(int(a) for a in r["label"]), int(r["value"]), int(r["modulus"]), r["source_id"]) for r in c["original_records"])
    return c, raw


@pytest.mark.parametrize("Q", (1, 3, 9, 27, 3**64))
def test_odd_double_rounding_identity_on_signed_rationals_and_boundaries(Q):
    for n in range(-8, 9):
        for delta in (Fraction(1, 2), Fraction(1, 2)-Fraction(1, 19), Fraction(1, 2)+Fraction(1, 19), Fraction(-1, 3)):
            x = Q*n+Q*delta
            assert G.nearest_odd_division(G.rounded_real(x), Q) == G.rounded_real(x/Q)


def test_even_divisor_cannot_inherit_the_exact_source_identity():
    x = Fraction(3, 5)
    assert G.rounded_real(Fraction(G.rounded_real(x), 2)) != G.rounded_real(x/2)
    with pytest.raises(ValueError): G.nearest_odd_division(1, 2)


@pytest.mark.parametrize("index", (0, 1, 2))
def test_new_completion_recovers_actual_full_root_when_old_exact_quotient_fails(index):
    c, raw = raw_control(index)
    assert c["strict_zero_error_quotient_baseline"]["status"] == "INCONSISTENT_ROUNDED_MISSING_QUOTIENT"
    result = G.complete_alphabet_multiple(raw, c["signed_coefficient"], tuple(int(x) for x in c["supplied_multiple"]), int(c["alphabet_completion"]["verification_radius"]))
    assert result["candidate_secret"] == tuple(int(x) for x in c["truth_fixture_only"]["original_secret"])
    assert result["original_fit"]["fits_public_radius"] and result["multiple_equation_verified"]
    assert not result["actual_planted_secret_or_noise_law_certified"]
    assert not c["calibration_is_an_unbounded_Gaussian_source"]
    a = result["adapter"]
    assert tuple(r["source_id"] for r in a["derived_records"]) == tuple(r.source_id for r in raw)
    assert not a["new_independent_original_samples_created"]
    Q = a["model"]["remaining_modulus"];g = a["model"]["nonunit_factor"]
    x = a["model"]["known_quotient_IF_multiple_is_true"]
    truth = tuple(int(s) for s in c["truth_fixture_only"]["original_secret"])
    h = tuple((s-v)//Q for s, v in zip(truth, x))
    for r, child, error in zip(raw, a["derived_records"], c["truth_fixture_only"]["original_errors"]):
        assert child["value"] == (sum(u*v for u, v in zip(child["label"], h))+G.nearest_odd_division(int(error), Q)) % g


def test_false_original_noise_promise_can_have_a_good_fit_with_same_multiple():
    c, raw = raw_control()
    Q = c["alphabet_completion"]["adapter"]["model"]["remaining_modulus"]
    changed = tuple(NoisyLinearRecord(r.label, (r.value+Q*r.label[0]) % r.modulus, r.modulus, r.source_id) for r in raw)
    result = G.complete_alphabet_multiple(changed, c["signed_coefficient"], c["supplied_multiple"], c["alphabet_completion"]["verification_radius"])
    planted = tuple(c["truth_fixture_only"]["original_secret"])
    assert result["candidate_secret"] is not None and result["candidate_secret"] != planted
    assert result["multiple_equation_verified"] and result["original_fit"]["fits_public_radius"]
    assert not result["actual_planted_secret_or_noise_law_certified"]


def test_matrix_cap_is_not_silent_partial_completion():
    c, raw = raw_control()
    r = G.complete_alphabet_multiple(raw, c["signed_coefficient"], c["supplied_multiple"], c["alphabet_completion"]["verification_radius"], max_matrix_entries=1)
    assert r["candidate_secret"] is None and r["decoder"]["compiled_rows"] == 0
    assert r["decoder"]["status"] == "WHOLE_FEATURE_MATRIX_CAP_EXCEEDED_NOT_NO_SOLUTION"


def test_triplet_mod3_domain_is_correctly_unsupported_not_an_impossibility_claim():
    c, raw = raw_control();secret = tuple(c["truth_fixture_only"]["original_secret"])
    r = G.derive_quotient(raw, 3, tuple(3*s % raw[0].modulus for s in secret))
    assert r["status"] == "DERIVED_MODULUS_BELOW_DIVIDED_CUBIC_DOMAIN_NOT_NO_SECRET"
    assert not r["derived_records"]


@pytest.mark.parametrize("beta", ("1/2", "1/4", "1/6", "1/10000", "10000"))
def test_Arb_probability_boxes_are_directed_and_restore_precision(beta):
    old = ctx.prec;boxes = G.gaussian_alphabet_boxes(beta, 80)
    assert ctx.prec == old
    intervals = [boxes["zero"], boxes["each_signed_one"], boxes["outside_triplet"]]
    for b in intervals:
        assert 0 <= Fraction(b["lower"]) <= Fraction(b["upper"]) <= 1
        assert Fraction(b["upper"])-Fraction(b["lower"]) <= Fraction(2, 2**80)
    lo, hi = (sum(Fraction(b[k])*w for b, w in zip(intervals, (1, 2, 1))) for k in ("lower", "upper"))
    assert lo <= 1 <= hi
    assert not boxes["conditioning_erases_outside_triplet_mass"]


def test_tiny_probability_floors_do_not_become_fictitious_rank_certificates():
    b = G.gaussian_alphabet_boxes("1/10000", 64)
    assert b["each_signed_one"]["lower"] == "0"
    l = G.split_rank_ledger(4, 1000000, b["zero"]["lower"], 2*Fraction(b["each_signed_one"]["lower"]))
    assert l["conditional_rank_failure_upper"] == "1"


@pytest.mark.parametrize("n", (1, 2, 3))
def test_complete_zero_and_nonzero_structural_blocks_have_distinct_dimensions(n):
    g = G.structural_grid(n)
    assert g["zero_coefficient_rank"] == g["zero_base_coefficient_rank"] == G.feature_width(n)-n*(n+1)//2
    assert g["quadratic_rank"] == n*(n+1)//2


@pytest.mark.parametrize("secret", ((0, 0), (1, 2), (8, 8), (4, 7)))
def test_secret_translation_preserves_zero_error_rank_without_public_secret_access(secret):
    rows = [G.cubic_equation(a, sum(x*y for x, y in zip(a, secret)) % 9)[0] for a in product(range(9), repeat=2)]
    assert int(nmod_mat(rows, 3).rank()) == G.feature_width(2)-3
    assert stored()["actual_original_data_controls"][0]["alphabet_completion"]["adapter"]["truth_or_errors_entered_adapter"] is False


def test_secret_translation_carry_identity_on_every_canonical_variable_pair():
    secret, a = (4, 7), (8, 2)
    for noise in (-1, 0, 1):
        t = (sum(x*y for x, y in zip(a, secret))+noise) % 9
        row, rhs = G.cubic_equation(a, t);translated, translated_rhs = G.cubic_equation(a, noise % 9)
        for u in product(range(3), repeat=2):
            for v in product(range(3), repeat=2):
                original = tuple((s+x+3*y) % 9 for s, x, y in zip(secret, u, v))
                f = features(tuple(x % 3 for x in original), tuple(x//3 for x in original))
                assert (sum(x*y for x, y in zip(row, f))-rhs) % 3 == (sum(x*y for x, y in zip(translated, features(u, v)))-translated_rhs) % 3


def test_small_escape_uses_adaptive_power_block_not_a_zero_fixed16_decay():
    e = Fraction(1, 1000000)
    l = G.capture_budget(3, 1000000000, e)
    assert (1-e)**16 > Fraction(1, 2)
    assert l["power_block"] == 1000000 and l["block_times_escape"] == "1"
    assert Fraction(l["rank_failure_upper"]) <= Fraction(1, 2**64)


def test_split_rank_budget_beats_charging_rare_noise_on_all_cubic_features():
    source = stored()["conditional_Gaussian_source_profiles"][4]
    rank = source["valuation_terms"][0]["conditional_rank_ledger"]
    old_style = G.capture_budget(rank["feature_dimension"], int(source["original_rows"]), Fraction(rank["nonzero_probability_lower_IN_truncated_law"])/3)
    assert old_style["rank_failure_upper"] == "1"
    assert Fraction(rank["conditional_rank_failure_upper"]) <= Fraction(1, 2**63)


def test_source_event_keeps_tail_and_missing_coverage_and_huge_matrix_costs():
    p = stored()["conditional_Gaussian_source_profiles"][-1]
    assert int(p["original_rows"]) > 2**53
    assert int(p["logical_matrix_entries_for_each_decoder"]) > 2000000
    assert p["recovery_failure_upper_IF_coverage_and_source_laws_hold"] is None
    assert not p["source_law_or_multiple_producer_supplied"]
    assert p["all_valuations_union_before_external_data_selected_multiple"]
    assert not p["unit_parts_at_same_valuation_create_independent_source_banks"]


def test_constant_width_tail_event_eventually_becomes_vacuous():
    p = G.source_ledger(4, 16, 10**16, "1/162", (4,), (3**16)//16)
    assert p["valuation_terms"][0]["Gaussian_derived_error_law"]["continuous_Gaussian_width"] == "1/2"
    assert p["valuation_terms"][0]["whole_original_bank_outside_triplet_failure_upper"] == "1"
    assert p["uniform_local_failure_upper"] == "1"


def test_declared_multiple_valuations_are_unioned_without_unit_part_sample_multipliers():
    p = G.source_ledger(2, 8, 1000, "1/1000", (2, 3), (3**8)//8, coverage_failure="1/10")
    assert len(p["valuation_terms"]) == 2
    for t in p["valuation_terms"]: assert not t["conditioning_on_data_selected_multiple_truth"]
    assert Fraction(p["recovery_failure_upper_IF_coverage_and_source_laws_hold"]) >= Fraction(p["uniform_local_failure_upper"])


def test_Arb_probability_replay_rejects_mass_tampering_separately_from_algebra():
    p = stored();assert G.verify_probability_boxes(p)["verified"]
    p = deepcopy(p);p["conditional_Gaussian_source_profiles"][0]["valuation_terms"][0]["Gaussian_derived_error_law"]["each_signed_one"]["lower"] = "1/3"
    with pytest.raises(ValueError, match="probability box replay"): G.verify_probability_boxes(p)


def node_check(p):
    return subprocess.run(["node", "-e", "require('./research/certificates/native_gaussian_quotient_completion_crosscheck.js').verify(JSON.parse(require('fs').readFileSync(0,'utf8')));"],
                          input=json.dumps(p), text=True, cwd=G.ROOT, capture_output=True)


def test_independent_actual_record_and_conditional_budget_replay():
    r = node_check(stored());assert r.returncode == 0, r.stderr


@pytest.mark.parametrize("kind", ("child", "parent-hash", "noise-resampling", "truth", "rank", "block", "tail", "coverage", "matrix-cost", "hash"))
def test_independent_checker_rejects_false_research_claims(kind):
    p = deepcopy(stored());c = p["actual_original_data_controls"][0]["alphabet_completion"];s = p["conditional_Gaussian_source_profiles"][0]
    if kind == "child": c["adapter"]["derived_records"][0]["value"] = (c["adapter"]["derived_records"][0]["value"]+1) % 9
    elif kind == "parent-hash": c["adapter"]["record_receipts"][0]["parent_record_sha256"] = "0"*64
    elif kind == "noise-resampling": c["adapter"]["new_independent_original_samples_created"] = True
    elif kind == "truth": c["actual_planted_secret_or_noise_law_certified"] = True
    elif kind == "rank": s["valuation_terms"][0]["conditional_rank_ledger"]["base_feature_dimension"] += 1
    elif kind == "block": s["valuation_terms"][0]["conditional_rank_ledger"]["nonzero_row_quadratic_rank_budget"]["power_block"] = 16
    elif kind == "tail": s["valuation_terms"][0]["whole_original_bank_outside_triplet_failure_upper"] = "0"
    elif kind == "coverage": s["recovery_failure_upper_IF_coverage_and_source_laws_hold"] = "0"
    elif kind == "matrix-cost": s["logical_matrix_entries_for_each_decoder"] = 1
    else: p["producer_sha256"] = "0"*64
    assert node_check(p).returncode != 0
