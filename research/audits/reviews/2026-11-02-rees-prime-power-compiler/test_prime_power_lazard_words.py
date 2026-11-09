"""Tests for the mod-p^e inverse-BCH evaluator and the free pullback (campaign item 6)."""
import re
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import prime_power_lazard_words as ppw  # noqa: E402


def witt(s, k):
    mu = {1: 1, 2: -1, 3: -1, 4: 0, 5: -1, 6: 1, 7: -1, 8: 0}
    return sum(mu[d]*s**(k//d) for d in range(1, k+1) if k % d == 0)//k


@pytest.mark.parametrize("s,c", [(2, 5), (2, 6), (3, 5), (4, 4)])
def test_lyndon_basis_has_witt_rank(s, c):
    assert len(ppw.lyndon_words(s, c)) == sum(witt(s, k) for k in range(1, c+1))
    ppw.FreeNilpotentLieRing(s, c, 7, 49)   # constructor asserts Lyndon triangularity


def test_exponent_p_evaluator_fails_and_prime_power_evaluator_succeeds():
    r = ppw.exponent_p_evaluator_failure(3, 2)
    assert not r["mod_p_correct"] and r["mod_p^e_correct"] and not r["mod_p_inverse_of_x_correct"]


@pytest.mark.parametrize("p,e,c", [(7, 2, 5), (11, 2, 5), (7, 2, 6), (11, 2, 6), (5, 3, 4), (3, 2, 2)])
def test_words_match_matrix_log_exp(p, e, c):
    assert ppw.check_ut_operations(p, e, c, 4, p+e+c)["ok"]


@pytest.mark.parametrize("p,c,s", [(7, 5, 2), (11, 6, 2), (7, 5, 3)])
def test_pullback_by_words_equals_direct_and_is_homomorphism(p, c, s):
    r = ppw.check_ut_pullback(p, 2, c, s, 2, 3*p+c)
    assert r["ok"] and r["mean_multiplications_per_Phi"] <= r["Phi_evaluation_cap"]


def test_loose_annihilator():
    assert ppw.check_ut_pullback(7, 2, 5, 2, 2, 11, modulus=7**4)["ok"]


def test_negative_controls_fail():
    r = ppw.negative_controls()
    assert r["mod_p_evaluator_add_failures_of_10_at_p7_e2_c5"] == 10
    assert r["class4_words_add_failures_of_10_on_UT6_Z49"] >= 8   # a random pair can hit a zero degree-5 error
    assert r["mod_p_pullback_homomorphism_holds"] is False


@pytest.mark.parametrize("args", [(7, 48, 5), (7, 49, 7), (7, 98, 5), (4, 16, 2)])
def test_rejects_bad_parameters(args):
    p, M, c = args
    with pytest.raises(ValueError):
        ppw.PrimePowerLazardWords(p, M, c, None, lambda a, b: a)


def test_recorded_gap_checks_if_present():
    outs = sorted(HERE.glob("gap_check_p*_c*.out"))
    results = [line for f in outs for line in f.read_text().splitlines() if line.startswith("RESULT")]
    if not results:
        pytest.skip("GAP outputs not recorded")
    for line in results:
        fields = dict(re.findall(r"(\S+)=(\S+)", line))
        assert fields["order_is_M^d"] == "true" and fields["generators_ok"] == "true"
        assert fields["hom_mod_p^e"] == "true" and fields["quotient_hom_mod_p^e"] == "true"
        assert fields["hom_mod_p_control"] == "false"
