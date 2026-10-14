"""Coordinate uniqueness must replace neither nonlinear nor source verification."""
from copy import deepcopy
from dataclasses import replace
from fractions import Fraction
from itertools import product
import json
import subprocess

import pytest

from theorems import native_partial_coordinate_decoder as P
from native_small_alphabet_decoder import decode as full_decode, cubic_equation, features
from native_gaussian_quotient_completion import source_ledger, complete_alphabet_multiple, verify_probability_boxes


def stored(): return json.loads(P.REPORT.read_text())


def bank(n=4, r=16, pairs=90, errors=1, seed=103001):
    raw, mask, truth, _ = P.source_data(n, r, pairs, False, seed)
    q = 3**r
    raw = tuple(replace(s, value=(s.value+int(j<errors)) % q) for j, s in enumerate(raw))
    return raw, tuple((s-m) % q for s, m in zip(truth, mask))


def test_affine_pivots_with_free_dependence_do_not_certify_secret_values():
    a = P.affine_coordinates(((1, 0, 0), (0, 1, 2)), (2, 1), 3, (0, 1, 2))
    assert a["coefficient_rank"] == 2 and not a["all_requested_coordinates_fixed"]
    x, y, z = a["coordinate_certificates"]
    assert x["fixed"] and x["value"] == 2
    assert not y["fixed"] and y["free_variable_dependence"] == ((2, 2),) and y["value"] is None
    assert z["pivot_row"] is None and not z["fixed"] and not a["free_variables_assigned"]


def test_inconsistent_affine_system_cannot_certify_any_requested_coordinate():
    a = P.affine_coordinates(((1,), (1,)), (0, 1), 1, (0,))
    assert a["inconsistent"] and a["augmented_rank"] == 2
    assert not a["all_requested_coordinates_fixed"] and a["coordinate_certificates"][0]["value"] is None


@pytest.mark.parametrize("rows,rhs,coords", ((((1.0,),), (0,), (0,)), (((True,),), (0,), (0,)), (((3,),), (0,), (0,)), (((1,),), (0,), ()), (((1,),), (0,), (0, 0)), (((1,),), (0,), (True,))))
def test_noncanonical_or_vacuous_affine_inputs_rejected(rows, rhs, coords):
    with pytest.raises(ValueError): P.affine_coordinates(rows, rhs, 1, coords)


@pytest.mark.parametrize("n,r,pairs,rank,D", ((4, 16, 90, 25, 34), (8, 64, 220, 129, 164), (2, 4, 30, 7, 9)))
def test_partial_feature_rank_recovers_full_original_secret(n, r, pairs, rank, D):
    raw, truth = bank(n, r, pairs)
    result = P.decode(raw)
    assert result["candidate_secret"] == truth
    assert result["coefficient_rank"] == rank < D == result["feature_dimension"]
    assert result["low_coordinate_model"]["all_requested_coordinates_fixed"]
    assert result["next_coordinate_model"]["all_requested_coordinates_fixed"]
    assert not result["full_feature_rank_required"] and not result["free_feature_coordinates_guessed"]
    assert result["nonlinear_features_verified"] and result["fixed_instance_alphabet_uniqueness_certified"]
    assert not result["actual_planted_secret_or_noise_law_certified"]
    assert full_decode(raw)["status"] == "INSUFFICIENT_FEATURE_RANK_NOT_NO_SECRET"


def test_zero_noise_succeeds_without_nonzero_error_probability_floor():
    raw, truth = bank(n=2, r=4, pairs=30, errors=0, seed=103003)
    result = P.decode(raw)
    assert result["coefficient_rank"] == 6 < 9 and result["candidate_secret"] == truth
    assert not any(result["original_candidate_residuals"])


@pytest.mark.parametrize("n,errors", ((1, 0), (1, 1), (2, 0), (2, 1)))
def test_fixed_instance_uniqueness_matches_complete_small_original_secret_census(n, errors):
    raw, _ = bank(n=n, r=2, pairs=12, errors=errors, seed=103101+n)
    r = P.decode(raw)
    compatible = []
    for s in product(range(9), repeat=n):
        if all(((row.value-sum(a*x for a, x in zip(row.label, s))+4) % 9)-4 in (-1, 0, 1) for row in raw):
            compatible.append(s)
    assert compatible == [r["candidate_secret"]]
    assert r["fixed_instance_alphabet_uniqueness_certified"]
    assert r["classical_secret_hypotheses_enumerated"] == 0


def test_affine_result_is_invariant_under_row_order_and_extra_redundant_rows():
    rows, rhs = ((1, 0, 1), (0, 1, 0)), (2, 1)
    a = P.affine_coordinates(rows, rhs, 3, (0, 1))
    b = P.affine_coordinates(tuple(reversed(rows))+(rows[0],), tuple(reversed(rhs))+(rhs[0],), 3, (0, 1))
    assert a["reduced_nonzero_rows"] == b["reduced_nonzero_rows"]
    assert a["coordinate_certificates"] == b["coordinate_certificates"]


def test_full_matrix_cap_precedes_compilation_and_secret_guessing():
    raw, _ = bank()
    result = P.decode(raw, max_matrix_entries=1)
    assert result["compiled_rows"] == result["field_elimination_calls"] == 0
    assert result["candidate_secret"] is None and result["coefficient_rank"] is None
    assert result["status"] == "WHOLE_FEATURE_MATRIX_CAP_EXCEEDED_NOT_NO_SOLUTION"


@pytest.mark.parametrize("secret", tuple(product(range(9), repeat=1))+((4, 7), (8, 8), (0, 2)))
def test_zero_row_base_fixes_secret_coordinates_for_nontrivial_secret_translations(secret):
    n = len(secret)
    equations = [cubic_equation(a, sum(x*y for x, y in zip(a, secret)) % 9) for a in product(range(9), repeat=n)]
    rows, rhs = tuple(x[0] for x in equations), tuple(x[1] for x in equations)
    low = P.affine_coordinates(rows, rhs, P.C.feature_width(n), tuple(range(n)))
    assert low["coefficient_rank"] == P.C.feature_width(n)-n*(n+1)//2
    u = tuple(c["value"] for c in low["coordinate_certificates"])
    assert low["all_requested_coordinates_fixed"] and u == tuple(x % 3 for x in secret)
    phi = features(u, (0,)*n)
    v = P.affine_coordinates(tuple(r[-n:] for r in rows), tuple((b-sum(x*y for x, y in zip(r, phi))) % 3 for r, b in zip(rows, rhs)), n, tuple(range(n)))
    assert v["all_requested_coordinates_fixed"]
    assert tuple(c["value"] for c in v["coordinate_certificates"]) == tuple(x//3 for x in secret)


def test_signed_quadratic_method_enforces_actual_squares_and_strict_signed_alphabet():
    c = stored()["actual_original_data_controls"][3]
    assert c["partial_decoder"]["method"] == "quadratic"
    assert c["partial_decoder"]["field_elimination_calls"] == 1
    assert c["matches_truth_fixture"] and c["partial_decoder"]["required_original_error_alphabet"] == [-1, 1]


def test_unfixed_zero_label_source_is_not_repaired_by_a_free_assignment():
    raw, _ = bank(n=2, r=3, pairs=12)
    raw = tuple(replace(s, label=(0, 0), value=1) for s in raw)
    result = P.decode(raw)
    assert result["status"] == "SECRET_COORDINATES_NOT_LINEARLY_UNIQUE_NOT_NO_SECRET"
    assert result["candidate_secret"] is None
    assert not result["low_coordinate_model"]["all_requested_coordinates_fixed"]


def test_full_rank_nonphysical_auxiliary_solution_still_rejected():
    f = {x["kind"]: x for x in P.falsifiers()}
    r = f["full_rank_nonphysical_feature_lift"]["partial_decoder"]
    assert r["coefficient_rank"] == r["feature_dimension"] == 3
    assert r["low_coordinate_model"]["all_requested_coordinates_fixed"]
    assert r["status"] == "INCONSISTENT_CANONICAL_FEATURE_SUBSTITUTION"
    assert r["candidate_secret"] is None


def test_corrupted_higher_root_equation_is_not_hidden_by_mod9_coordinate_success():
    raw, _ = bank()
    changed = (*raw[:-1], replace(raw[-1], value=(raw[-1].value+9) % raw[-1].modulus))
    r = P.decode(changed)
    assert r["low_coordinate_model"]["all_requested_coordinates_fixed"]
    assert r["next_coordinate_model"]["all_requested_coordinates_fixed"]
    assert r["nonlinear_features_verified"]
    assert r["status"] == "INCONSISTENT_OR_UNSUPPORTED_ORIGINAL_HIGHER_ROOT_LIFT"
    assert r["candidate_secret"] is None


def test_wrong_planted_source_can_have_unique_fit_without_truth_certificate():
    f = {x["kind"]: x for x in P.falsifiers()}
    r = f["wrong_planted_secret_with_unique_alphabet_fit"]["partial_decoder"]
    assert r["candidate_secret"] is not None and r["fixed_instance_alphabet_uniqueness_certified"]
    assert not f["wrong_planted_secret_with_unique_alphabet_fit"]["matches_planted_truth"]
    assert not r["actual_planted_secret_or_noise_law_certified"]


def test_base_only_source_budget_survives_zero_rare_noise_probability_floor():
    p = P.base_only_source_ledger(2, 16, 500, "1/90000", (2,), (3**16)//32)
    reference = p["full_feature_reference_same_source"]
    assert reference["valuation_terms"][0]["Gaussian_derived_error_law"]["each_signed_one"]["lower"] == "0"
    assert reference["valuation_terms"][0]["conditional_rank_ledger"]["conditional_rank_failure_upper"] == "1"
    assert Fraction(p["uniform_local_secret_recovery_failure_upper"]) < Fraction(1, 1000000)
    assert not p["secret_coordinate_valuation_terms"][0]["nonzero_noise_probability_floor_required"]
    assert not p["actual_source_or_multiple_producer_supplied"]


def test_Gaussian_sample_reduction_retains_caps_tails_and_missing_coverage():
    s = stored()["base_only_Gaussian_source_profiles"][-1]
    old = int(s["full_feature_rank_sufficient_original_rows_reference"])
    rows = int(s["full_feature_reference_same_source"]["original_rows"])
    assert old > 10**11*rows
    assert not s["default_matrix_cap_feasible"]
    assert not s["recovery_with_missing_external_coverage_claimed"]
    assert s["all_original_radius_separation_truncation_and_valuation_events_retained"]
    assert Fraction(s["uniform_local_secret_recovery_failure_upper"]) < Fraction(1, 1000000)


def test_quotient_completion_default_uses_certified_coordinates():
    raw, truth = bank(n=4, r=16, pairs=90, errors=1)
    q, g = 3**16, 3**4;Q = q//g
    # A single nonzero DERIVED error, with no free original-secret argument.
    errors = tuple(Q*int(j==0) for j in range(len(raw)))
    raw = tuple(replace(s, value=(sum(a*t for a, t in zip(s.label, truth))+e) % q) for s, e in zip(raw, errors))
    w = tuple(g*s % q for s in truth)
    r = complete_alphabet_multiple(raw, g, w, Q)
    assert r["candidate_secret"] == truth
    assert r["decoder"]["algorithm"] == "CERTIFIED_AFFINE_SECRET_COORDINATES_AND_CANONICAL_SUBSTITUTION"
    assert r["decoder"]["coefficient_rank"] < r["decoder"]["feature_dimension"]


def test_current_Gaussian_probability_boxes_have_the_separate_replay_gate():
    profiles = [s["full_feature_reference_same_source"] for s in stored()["base_only_Gaussian_source_profiles"]]
    assert verify_probability_boxes({"conditional_Gaussian_source_profiles": profiles})["verified"]


def node_check(p):
    return subprocess.run(["node", "-e", "require('./research/certificates/native_partial_coordinate_decoder_crosscheck.js').verify(JSON.parse(require('fs').readFileSync(0,'utf8')));"],
        input=json.dumps(p), text=True, cwd=P.ROOT, capture_output=True)


def test_independent_live_coordinate_and_source_budget_replay():
    r = node_check(stored());assert r.returncode == 0, r.stderr


@pytest.mark.parametrize("kind", ("RREF", "free-coefficient", "pivot", "coordinate", "physical-features", "next-system", "source-rank", "tail", "source-truth", "hash"))
def test_independent_checker_rejects_tampered_coordinate_or_advantage_claims(kind):
    p = deepcopy(stored());r = p["actual_original_data_controls"][0]["partial_decoder"];s = p["base_only_Gaussian_source_profiles"][0]
    if kind == "RREF": r["low_coordinate_model"]["reduced_nonzero_rows"][0][0] = 0
    elif kind == "free-coefficient": r["low_coordinate_model"]["coordinate_certificates"][0]["free_variable_dependence"] = [[r["low_coordinate_model"]["free_columns"][0], 1]]
    elif kind == "pivot": r["low_coordinate_model"]["pivot_columns"][0] = 33
    elif kind == "coordinate": r["low_coordinate_model"]["coordinate_certificates"][0]["value"] = (r["low_coordinate_model"]["coordinate_certificates"][0]["value"]+1) % 3
    elif kind == "physical-features": r["canonical_feature_vector"][4] = (r["canonical_feature_vector"][4]+1) % 3
    elif kind == "next-system": r["next_coordinate_model"]["input_system_sha256"] = "0"*64
    elif kind == "source-rank": s["secret_coordinate_valuation_terms"][0]["zero_error_base_coordinate_budget"]["rank_failure_upper"] = "0"
    elif kind == "tail": s["secret_coordinate_valuation_terms"][0]["whole_bank_outside_triplet_failure_upper"] = "0"
    elif kind == "source-truth": r["actual_planted_secret_or_noise_law_certified"] = True
    else: p["producer_sha256"] = "0"*64
    assert node_check(p).returncode != 0
