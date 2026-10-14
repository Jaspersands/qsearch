"""Conditional Gaussian prefix budgets must not cut the full-value source."""
from copy import deepcopy
from fractions import Fraction
import json
import subprocess

import pytest

from theorems import native_gaussian_prefix_information as G


@pytest.mark.parametrize("n", (32, 64, 128))
def test_original_mod9_is_negligibly_informative_only_under_Gaussian_source(n):
    p = G.prefix_ledger(n, n, 2, 2*(n*n+12), Fraction(1, n**3))
    assert p["conservative_bank_TV_budget_bits"] == 128
    assert not p["source_Gaussian_law_established_by_calibration"]
    assert p["public_labels_can_be_kept_at_the_full_original_modulus"]
    assert not p["general_LWE_or_quantum_decoder_lower_bound_proved"]


def test_small_profile_and_full_root_countercontrol_are_correctly_vacuous():
    assert G.prefix_ledger(8, 8, 2, 152, "1/512")["whole_prefix_bank_to_secret_independent_uniform_TV_upper"] == "1"
    full = G.prefix_ledger(32, 32, 32, 2072, "1/32768")
    assert full["whole_prefix_bank_to_secret_independent_uniform_TV_upper"] == "1"
    assert not full["true_quotient_side_information_or_other_coherent_access_excluded"]


def test_shared_Gaussian_error_marginals_can_leave_the_secret_prefix_exactly_visible():
    for secret in range(9):
        for error in range(-30, 31):
            assert ((error+secret) % 9-error % 9) % 9 == secret
        uniform_event_count = sum((b-a) % 9 == secret for a in range(9) for b in range(9))
        assert Fraction(uniform_event_count, 81) == Fraction(1, 9)
    c = json.loads(G.REPORT.read_text())["correlated_Gaussian_marginal_countercontrol"]
    assert not c["errors_are_IID"] and c["whole_bank_TV_from_IID_null_lower"] == "8/9"
    assert not c["marginal_Gaussian_laws_suffice_for_bank_bound"]


@pytest.mark.parametrize("alpha,m", (("1/3", 1), ("2/3", 12), ("1/9", 20), ("1/27", 2)))
def test_conservative_bound_is_never_smaller_than_its_justified_Gaussian_envelope(alpha, m):
    p = G.prefix_ledger(1, 3, 1, m, alpha, bits=32)
    K = p["Gaussian_decay_floor"]
    justified = min(1, Fraction(8*m, 7*2**K)) if K else 1
    assert Fraction(p["whole_prefix_bank_to_secret_independent_uniform_TV_upper"]) >= justified
    assert Fraction(p["Gaussian_width_in_prefix_periods_squared"]) == Fraction(alpha)**2*81


def test_decay_exponent_is_factored_instead_of_allocating_its_denominator():
    p = G.prefix_ledger(128, 128, 2, 32792, "1/2097152")
    assert p["Gaussian_decay_floor"] > 10**100
    assert len(json.dumps(G.exact_json(p))) < 2500


@pytest.mark.parametrize("args", ((0, 2, 1, 4, "1/9"), (2, 2, 3, 4, "1/9"), (2, 2, 1, 4, 0), (2, 2, 1, 4, .1), (2, True, 1, 4, "1/9")))
def test_invalid_or_inexact_source_promises_rejected(args):
    with pytest.raises(ValueError): G.prefix_ledger(*args)


def run_checker(p):
    return subprocess.run(["node", "-e", "require('./research/certificates/native_gaussian_prefix_information_crosscheck.js').verify(JSON.parse(require('fs').readFileSync(0,'utf8')));"],
                          input=json.dumps(p), text=True, cwd=G.ROOT, capture_output=True)


def test_independent_live_ledger_replay():
    r = run_checker(json.loads(G.REPORT.read_text()))
    assert r.returncode == 0, r.stderr


@pytest.mark.parametrize("kind", ("decay", "TV", "law", "full-value-cut", "side-information"))
def test_checker_rejects_tampered_source_and_scope(kind):
    p = deepcopy(json.loads(G.REPORT.read_text()));x = p["original_mod9_profiles"][0]
    if kind == "decay": x["Gaussian_decay_floor"] = 0
    elif kind == "TV": x["whole_prefix_bank_to_secret_independent_uniform_TV_upper"] = "0"
    elif kind == "law": x["source_Gaussian_law_established_by_calibration"] = True
    elif kind == "full-value-cut": p["full_original_root_outside_the_cut"]["whole_prefix_bank_to_secret_independent_uniform_TV_upper"] = "0"
    else: x["true_quotient_side_information_or_other_coherent_access_excluded"] = True
    assert run_checker(p).returncode != 0
