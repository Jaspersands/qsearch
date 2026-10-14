"""Actual-ring carry decoding, nonlinear checks, source confidence and falsifiers."""
from dataclasses import replace
from fractions import Fraction
from itertools import product
import json
import subprocess

import pytest
from flint import nmod_mat

from theorems import native_small_alphabet_decoder as C
from native_full_root_slice import source_data
from ternary_noise_degradation import NoisyLinearRecord


def bank(n=2, r=3, M=20, seed=98001):
    raw, mask, truth, errors = source_data(n, r, M, True, seed)
    return raw, tuple((x-y) % (3**r) for x, y in zip(truth, mask)), errors


@pytest.mark.parametrize("n", (1, 2, 3, 4, 8))
def test_feature_width_and_layout_are_fixed_canonical_ternary_monomials(n):
    assert len(C.feature_layout(n)) == C.feature_width(n)
    assert len(set(C.feature_layout(n))) == C.feature_width(n)
    assert len(C.feature_layout(n, "quadratic")) == C.feature_width(n, "quadratic")
    u, v = tuple(i % 3 for i in range(n)), tuple((i+1) % 3 for i in range(n))
    features = C.features(u, v)
    assert features[:n] == u and features[-n:] == v


@pytest.mark.parametrize("a,t", (((0, 0), 0), ((1, 2), 8), ((8, 7), 2), ((4, 3, 8), 7)))
def test_divided_cubic_equals_original_integer_carry_for_every_canonical_trit(a, t):
    row, rhs = C.cubic_equation(a, t);n = len(a)
    for u in product(range(3), repeat=n):
        x = t-sum(x*y for x, y in zip(a, u))
        original = (x**3-x)//3 % 3
        polynomial = (sum(x*y for x, y in zip(row, C.features(u, (0,)*n)))-rhs) % 3
        assert polynomial == original
    assert any((x**3-x)//3 % 3 for x in range(9))
    assert all((x**3-x) % 3 == 0 for x in range(3))  # Reducing first loses the signal.


@pytest.mark.parametrize("q", (9, 27, 3**16, 3**64))
def test_actual_full_root_recovery_uses_no_preimage_helper_or_secret_input(q):
    raw, truth, _ = bank(r=C.root_digits(q))
    result = C.decode(raw)
    assert result["candidate_secret"] == truth
    assert result["fixed_instance_alphabet_uniqueness_certified"]
    assert not result["actual_planted_secret_or_noise_law_certified"]
    assert result["classical_secret_hypotheses_enumerated"] == 0
    assert all(e in (-1, 0, 1) for e in result["original_candidate_residuals"])
    if q > 9:
        assert result["full_root_lift"]["public_basis_model"]["composite_field_inverse_used"] is False
        assert result["full_root_lift"]["all_original_higher_equations_consistent"]
    else: assert not result["full_root_lift"]["applied"]


@pytest.mark.parametrize("n,r", ((1, 1), (2, 2), (4, 16), (8, 64)))
def test_faster_quadratic_signed_only_baseline_recovers_actual_originals(n, r):
    raw, truth, _ = bank(n=n, r=r, M=max(24, 2*C.feature_width(n, "quadratic")))
    result = C.decode(raw, "quadratic")
    assert result["candidate_secret"] == truth
    assert result["feature_dimension"] < C.feature_width(n)
    assert result["required_canonical_original_error_alphabet"] == (-1, 1)
    assert not result["new_quantum_algorithm_or_general_Gaussian_solver"]


def test_mixed_alphabet_with_zero_noise_scales_beyond_small_sample_controls():
    c = C.control(8, 64, 688, "mixed", "cubic", 97004)
    assert c["matches_truth_fixture"]
    assert set(c["truth_fixture_only"]["original_errors"]) == {-1, 0, 1}
    assert c["decoder"]["feature_dimension"] == 164
    assert Fraction(c["cubic_source_rank_budget"]["rank_failure_upper_used"]) < Fraction(1, 100000)
    assert not c["unbounded_Gaussian_noise_is_represented_by_this_calibration"]


def test_false_alphabet_can_have_unique_compatible_secret_but_wrong_planted_secret():
    cases = {c["kind"]: c for c in C.falsifiers()}
    c = cases["wrong_planted_secret_with_unique_alphabet_fit"]
    assert c["decoder"]["fixed_instance_alphabet_uniqueness_certified"]
    assert c["decoder"]["candidate_secret"] is not None and not c["matches_planted_truth"]
    assert not c["decoder"]["actual_planted_secret_or_noise_law_certified"]
    assert any(e not in (-1, 0, 1) for e in c["truth_fixture_only"]["original_errors"])


def test_caps_failed_rank_and_corrupted_equations_are_not_secret_guesses():
    cases = {c["kind"]: c for c in C.falsifiers()}
    capped = cases["preflight_cap"]["decoder"]
    assert capped["compiled_rows"] == capped["field_elimination_calls"] == 0
    assert capped["status"] == "WHOLE_FEATURE_MATRIX_CAP_EXCEEDED_NOT_NO_SOLUTION"
    rankless = cases["rankless_source"]["decoder"]
    assert rankless["coefficient_rank"] == 0 and rankless["candidate_secret"] is None
    assert rankless["status"] == "INSUFFICIENT_FEATURE_RANK_NOT_NO_SECRET"
    corrupt = cases["corrupted_carry_equation"]["decoder"]
    assert corrupt["status"] == "INCONSISTENT_SMALL_ALPHABET_EQUATIONS" and corrupt["candidate_secret"] is None
    nonphysical = cases["full_rank_nonphysical_feature_lift"]["decoder"]
    assert nonphysical["coefficient_rank"] == nonphysical["feature_dimension"] == 3
    assert nonphysical["linearized_solution"] == (0, 1, 0)
    assert nonphysical["status"] == "INVALID_NONLINEAR_FEATURE_LIFT" and nonphysical["candidate_secret"] is None


def test_signed_quadratic_method_does_not_silently_ignore_zero_errors():
    raw = (NoisyLinearRecord((0,), 0, 9, "zero-0"), NoisyLinearRecord((1,), 1, 9, "zero-1"))
    result = C.decode(raw, "quadratic")
    assert result["status"] == "INCONSISTENT_SMALL_ALPHABET_EQUATIONS"
    assert result["candidate_secret"] is None


def test_nonlinear_features_are_not_read_out_from_an_arbitrary_linear_solution(monkeypatch):
    raw, _, _ = bank()
    fake = list(C.features((1, 2), (0, 0)));fake[2] = (fake[2]+1) % 3
    monkeypatch.setattr(C, "solve_full_rank_f3", lambda *args: tuple(fake))
    result = C.decode(raw)
    assert result["status"] == "INVALID_NONLINEAR_FEATURE_LIFT" and result["candidate_secret"] is None


@pytest.mark.parametrize("n", (1, 2, 3))
def test_complete_public_coefficient_grid_has_full_feature_span(n):
    grid = C.coefficient_grid(n)
    assert grid["coefficient_rank_mod3"] == grid["feature_dimension"]
    assert grid["full_public_parameter_grid_rows"] == 3**(2*n+1)
    assert grid["these_rows_are_not_new_oracle_samples"]


@pytest.mark.parametrize("support,p", (((-1, 1), "1/2"), ((-1, 0, 1), "1/3"), ((0, 1), "1/4")))
def test_source_probability_floor_and_power_bound_are_exact_and_distinct(support, p):
    L = C.cubic_rank_ledger(4, 400, p, support)
    escape = 2*Fraction(p)/3 if len(support) == 3 else Fraction(p)/3
    assert Fraction(L["row_escape_probability_lower"]) == escape
    k, block = L["capture_power_negative_log2_floor"], L["capture_power_block"]
    power = (1-escape)**block
    assert 2**k*power.numerator <= power.denominator < 2**(k+1)*power.numerator
    exact = min(Fraction(1), Fraction(3**L["feature_dimension"]-1, 2)*(1-escape)**400)
    assert Fraction(L["rank_failure_upper_used"]) >= exact
    assert not L["actual_source_promise_or_probability_floor_established"]


def test_tiny_noise_floor_does_not_require_an_astronomical_loop_or_fake_confidence():
    L = C.cubic_rank_ledger(4, 400, Fraction(1, 10**100), (-1, 1))
    assert L["rank_failure_upper_used"] == "1"
    assert L["capture_power_block"] == 16


def test_complete_source_aware_scalar_escape_censuses_cover_two_and_three_supports():
    for u, support in product(range(3), ((-1, 1), (-1, 0, 1), (0, 1))):
        c = C.scalar_escape_control(u, support)
        assert Fraction(c["minimum_actual_escape_probability"]) >= Fraction(c["claimed_escape_lower"])
        assert c["nonzero_duals_checked"] == 26


def test_actual_uniqueness_agrees_with_exhaustive_small_source_verification():
    raw, truth, _ = bank(n=1, r=2, M=20)
    result = C.decode(raw)
    compatible = [s for s in range(9) if all(((r.value-r.label[0]*s+4) % 9)-4 in (-1, 0, 1) for r in raw)]
    assert compatible == [truth[0]] == [result["candidate_secret"][0]]


@pytest.mark.parametrize("secret", (0, 3, 9))
def test_decoder_handles_zero_and_nonprimitive_original_secret(secret):
    raw, _, errors = bank(n=1)
    changed = tuple(replace(s, value=(s.label[0]*secret+e) % s.modulus) for s, e in zip(raw, errors))
    assert C.decode(changed)["candidate_secret"] == (secret,)


@pytest.mark.parametrize("bad", ("root", "method", "reuse", "feature", "cap", "noise_floor", "support", "probability", "derived", "grid"))
def test_invalid_or_unpaid_source_models_are_rejected(bad):
    raw, _, _ = bank()
    with pytest.raises(ValueError):
        if bad == "root": C.decode(tuple(NoisyLinearRecord(tuple(x % 3 for x in s.label), s.value % 3, 3, s.source_id) for s in raw))
        elif bad == "method": C.decode(raw, "Gaussian")
        elif bad == "reuse": C.decode((raw[0], raw[0]))
        elif bad == "feature": C.features((1, 2), (True, 0))
        elif bad == "cap": C.decode(raw, max_matrix_entries=0)
        elif bad == "noise_floor": C.cubic_rank_ledger(2, 40, 0, (-1, 1))
        elif bad == "support": C.cubic_rank_ledger(2, 40, "1/2", (0,))
        elif bad == "probability": C.cubic_rank_ledger(2, 40, "1/2", (-1, 0, 1))
        elif bad == "derived": C.decode(({"label": (1,), "value": 0},)*2)
        elif bad == "grid": C.coefficient_grid(8)


def test_live_artifact_and_independent_checker():
    report = json.loads(C.REPORT.read_text())
    assert not report["general_Gaussian_LWE_solver_or_new_quantum_algorithm"]
    checked = subprocess.run(["node", "research/certificates/native_small_alphabet_decoder_crosscheck.js"], cwd=C.ROOT, capture_output=True, text=True, check=True)
    assert json.loads(checked.stdout)["verified"]


@pytest.mark.parametrize("tamper", ("coefficient", "low_prefix", "inverse", "source", "confidence", "novelty", "planted"))
def test_independent_checker_rejects_algebra_or_claim_inflation(tamper):
    p = json.loads(C.REPORT.read_text());c = p["original_data_controls"][0]
    if tamper == "coefficient": c["decoder"]["compiled_system_sha256"] = "0"*64
    elif tamper == "low_prefix": c["decoder"]["low_secret"][0] = (c["decoder"]["low_secret"][0]+1) % 9
    elif tamper == "inverse": c["decoder"]["full_root_lift"]["public_basis_model"]["inverse"][0][0] = 0
    elif tamper == "source": c["decoder"]["actual_planted_secret_or_noise_law_certified"] = True
    elif tamper == "confidence": c["cubic_source_rank_budget"]["capture_power_negative_log2_floor"] += 1
    elif tamper == "novelty": p["novelty_claim"] = True
    elif tamper == "planted": p["falsifier_controls"][3]["matches_planted_truth"] = True
    result = subprocess.run(["node", "-e", "require('./research/certificates/native_small_alphabet_decoder_crosscheck.js').verify(JSON.parse(require('fs').readFileSync(0,'utf8')))"],
        input=json.dumps(p), cwd=C.ROOT, capture_output=True, text=True)
    assert result.returncode != 0
