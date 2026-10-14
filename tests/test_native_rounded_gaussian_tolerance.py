"""Exact Gaussian-interface arithmetic, abort composition and source falsifiers."""
from fractions import Fraction
from itertools import product
import json
import math
import subprocess

import pytest

from theorems import native_rounded_gaussian_tolerance as G


@pytest.mark.parametrize("x", ("1", "2", "3/2", "8", "17/3", "1/100", "12345678901234567890/7"))
def test_hybrid_logarithm_is_exact_and_minimal(x):
    x = Fraction(x);t = G._ceil_log2_fraction(x)
    assert 2**t >= x
    if t: assert 2**(t-1) < x


@pytest.mark.parametrize("q,m,alpha,B", ((27, 1, "1/3", 1), (81, 4, "1/5", 2), (729, 12, "1/100", 3)))
def test_ideal_continuous_gaussian_TV_enclosed_with_correct_D_alpha_normalization(q, m, alpha, B):
    sigma = float(Fraction(alpha))*q/math.sqrt(2*math.pi)
    actual = math.erf(B*math.sqrt(m)/(2*math.sqrt(2)*sigma))
    square = G.translation_square(q, m, alpha, B)
    assert actual**2 <= float(square)+1e-14


def test_exact_integer_rounding_commutes_with_every_integer_shift_including_boundary():
    def rounding(x):
        x = x+Fraction(1, 2)
        return x.numerator//x.denominator
    for x, k in product((Fraction(i, 6) for i in range(-40, 41)), range(-8, 9)):
        assert rounding(x+k) == rounding(x)+k


@pytest.mark.parametrize("n", (8, 32, 64, 128))
def test_gaussian_source_compatibility_and_usable_valuation_are_separate(n):
    c = G.control(n);L = c["ideal_exact_rounding_budget"]
    eta, margin = Fraction(L["noise_tolerance_target"]), Fraction(L["ideal_tolerance_margin"])
    assert Fraction(L["terminal_hybrid_distance_squared_upper"]) <= Fraction(L["target_terminal_hybrid_distance_squared_upper"])
    assert Fraction(L["ideal_translation_TV_squared_upper"]) <= margin**2
    if n == 8:
        assert L["maximum_integer_shift_certified"] == 0 and c["published_size_ceiling_completion_gap"] is None
    else:
        assert L["maximum_integer_shift_certified"] > 0
        assert c["published_size_ceiling_completion_gap"]["worst_factor_local_source_event"]["original_error_event_failure_upper"] == "1"
    assert not L["published_discrete_Gaussian_corollary_imported"]
    assert not L["full_general_reduction_or_decision_algorithm_implemented"]
    assert Fraction(L["uniform_secret_nonprimitive_probability_IF_uniform"]) == Fraction(1, 3**n)
    assert c["adapter_budget_with_no_margin"]["maximum_integer_shift_certified"] == 0
    assert Fraction(c["containing_interval_precision_plan"]["whole_bank_unconditioned_abort_union_upper"]) <= eta/16


def test_actual_precision_adapter_loss_is_charged_twice_not_conditioned_away():
    q = 3**32;n = 32;m = 2*33**3
    ideal = G.tolerance_budget(q, n, m, "1/32768", "1/10")
    eta = Fraction(ideal["noise_tolerance_target"])
    adapted = G.tolerance_budget(q, n, m, "1/32768", "1/10", eta/16)
    assert adapted["two_adapter_losses"] == str(eta/8)
    assert adapted["ideal_tolerance_margin"] == str(7*eta/8)
    assert adapted["maximum_integer_shift_certified"] < ideal["maximum_integer_shift_certified"]
    assert not adapted["conditioning_on_adapter_success_erases_its_loss"]


def test_true_moment_upper_does_not_certify_gaussian_translation_smoothness():
    c = G.moment_countercontrol()
    assert c["heavy_tail_obeys_shared_moment_upper"]
    assert c["heavy_tail_integer_translation_TV"] == c["heavy_tail_modular_translation_TV"] == "1"
    assert Fraction(c["Gaussian_translation_TV_squared_upper_for_comparison"]) < Fraction(1, 10000)
    assert not c["Gaussian_smoothness_inferred_from_matching_moment_upper"]
    assert G.finite_translation_tv(((0, "1/2"), (1, "1/2")), 1) == Fraction(1, 2)
    assert G.finite_translation_tv(tuple((x, "1/3") for x in range(3)), 1, 3) == 0


def test_paid_known_mask_can_randomize_fixed_classical_secret_without_fresh_errors():
    q, n, original, labels, errors = 9, 2, (2, 3), ((1, 2), (3, 4)), (-1, 1)
    values = tuple((sum(a*s for a, s in zip(row, original))+e) % q for row, e in zip(labels, errors))
    secrets, nonprimitive = set(), 0
    for mask in product(range(q), repeat=n):
        masked = tuple((s+u) % q for s, u in zip(original, mask));secrets.add(masked)
        transformed = tuple((y+sum(a*u for a, u in zip(row, mask))) % q for row, y in zip(labels, values))
        assert transformed == tuple((sum(a*s for a, s in zip(row, masked))+e) % q for row, e in zip(labels, errors))
        assert tuple((s-u) % q for s, u in zip(masked, mask)) == original
        nonprimitive += all(s % 3 == 0 for s in masked)
    assert len(secrets) == q**n and Fraction(nonprimitive, q**n) == Fraction(1, 3**n)


@pytest.mark.parametrize("q,B,d", ((81, 1, 2), (729, 1, 2), (729, 3, 1)))
def test_censored_threshold_covariance_is_exact_but_primitive_characters_vanish(q, B, d):
    c = G.threshold_censoring(q, B, d);g, Q = 3**d, q//3**d
    f = [int(min(t, q-t) <= B) for t in range(q)]
    h = [int(min(t % Q, (-t) % Q) <= B) for t in range(q)]
    p, coarse, joint = Fraction(sum(f), q), Fraction(sum(h), q), Fraction(sum(a*b for a, b in zip(f, h)), q)
    assert str(joint-p*coarse) == c["centered_covariance"]
    assert all(h[t] == h[(t+Q) % q] for t in range(q))
    # Literal finite Fourier check supplements the exact geometric cancellation.
    for k in (1, 2, 4, 5):
        real = sum(a*math.cos(2*math.pi*k*t/q) for t, a in enumerate(h))/q
        imag = sum(a*math.sin(2*math.pi*k*t/q) for t, a in enumerate(h))/q
        assert abs(real)+abs(imag) < 1e-12
    assert c["all_primitive_character_coefficients_zero"]
    assert not c["scalar_inner_product_available_to_real_original_source_receiver"]


def test_growing_source_window_can_be_strongly_correlated_without_usable_coefficient():
    c = G.control(64);F = c["nonprimitive_threshold_correlation_countercontrol"]
    assert Fraction(F["fraction_of_uncensored_covariance_preserved"]) > Fraction(99, 100)
    assert c["coarse_predictor_original_completion_budget"]["original_error_event_failure_upper"] == "1"
    assert F["this_is_a_counterexample_to_correlation_implying_primitive_support_not_a_decision_algorithm"]


@pytest.mark.parametrize("bad", ("root", "width", "advantage", "adapter", "float", "negative_shift", "odd_bank", "law"))
def test_unproved_or_malformed_source_parameters_do_not_enter_the_budget(bad):
    with pytest.raises(ValueError):
        if bad == "root": G.tolerance_budget(3, 1, 2, "1/2", "1/10")
        elif bad == "width": G.tolerance_budget(9, 1, 2, "1", "1/10")
        elif bad == "advantage": G.tolerance_budget(9, 1, 2, "1/2", "0")
        elif bad == "adapter": G.tolerance_budget(9, 1, 2, "1/2", "1/10", "-1")
        elif bad == "float": G.tolerance_budget(9, 1, 2, 0.1, "1/10")
        elif bad == "negative_shift": G.translation_square(9, 1, "1/2", -1)
        elif bad == "odd_bank": G.precision_plan(9, 3, "1/2", "1/10", 12)
        elif bad == "law": G.finite_translation_tv(((0, "1/4"),), 1)


def test_live_noise_artifact_and_independent_checker():
    p = json.loads(G.REPORT.read_text())
    assert not p["accepted_speedup_candidate"] and not p["new_active_negative_result_created"]
    result = subprocess.run(["node", "research/certificates/native_rounded_gaussian_tolerance_crosscheck.js"], cwd=G.ROOT, capture_output=True, text=True, check=True)
    assert json.loads(result.stdout)["verified"]


@pytest.mark.parametrize("tamper", ("rounding_loss", "primitive", "advantage", "coefficient", "source", "countercontrol"))
def test_independent_checker_rejects_false_noise_interfaces(tamper):
    p = json.loads(G.REPORT.read_text());c = p["scaling_controls"][1]
    if tamper == "rounding_loss": c["charged_adapter_budget"]["two_adapter_losses"] = "0"
    elif tamper == "primitive": c["ideal_exact_rounding_budget"]["coprime_secret_required_for_terminal_hybrid_argument"] = False
    elif tamper == "advantage": c["decision_advantage_assumed_not_measured"] = False
    elif tamper == "coefficient": c["ideal_exact_rounding_budget"]["coefficient_size_ceiling_IF_published_reduction_contract_is_met"] = 1
    elif tamper == "source": c["ideal_exact_rounding_budget"]["actual_Gaussian_law_or_adapter_failure_established"] = True
    elif tamper == "countercontrol": p["moment_only_smoothness_countercontrol"]["heavy_tail_modular_translation_TV"] = "0"
    result = subprocess.run(["node", "-e", "require('./research/certificates/native_rounded_gaussian_tolerance_crosscheck.js').verify(JSON.parse(require('fs').readFileSync(0,'utf8')))"],
        input=json.dumps(p), cwd=G.ROOT, capture_output=True, text=True)
    assert result.returncode != 0
