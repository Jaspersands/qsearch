"""Tests for multi-round interleaved syndrome-work circuits and response-call degree audit."""
from copy import deepcopy
from fractions import Fraction
import json
import subprocess

import pytest

from theorems import native_interleaved_syndrome_work_audit as I
from native_basis_lottery import _certificate_int


def stored():
    return json.loads(I.REPORT.read_text())


def node_check(payload):
    return subprocess.run(
        [
            "node",
            "-e",
            "const X=require('./research/certificates/native_interleaved_syndrome_work_audit_crosscheck.js');"
            "let s='';process.stdin.on('data',x=>s+=x);"
            "process.stdin.on('end',()=>console.log(JSON.stringify(X.verify(JSON.parse(s)))));",
        ],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        cwd=I.ROOT,
    )


def test_multi_round_interleaved_controls_conserve_parseval_ground_band_and_pinch_cross_fibres():
    rep = stored()
    ctrls = rep["multi_round_interleaved_controls"]
    assert len(ctrls) == 3
    for c in ctrls:
        assert c["multi_round_parseval_ground_band_conservation_holds"]
        assert c["multi_round_syndrome_weights"]["distinct_delta_weight_polynomial_count"] >= 2
        assert (
            c["sum_over_all_sectors_uniform_secret_overlap_root_polynomial"]
            == c["raw_gram_uniform_secret_overlap_root_polynomial"]
        )
        pinch = c["cross_fibre_word_effect_pinching"]
        assert pinch["off_fibre_nonzero_entries_in_E_cross"] > 0
        assert pinch["cross_fibre_entries_annihilated_exactly_by_secret_twirl"]
        assert pinch["complete_secret_sweep_mean_root_polynomial"] == pinch["pinched_fibre_diagonal_root_polynomial"]
    assert any(c["distinct_sector_overlap_polynomial_count"] >= 2 for c in ctrls)


def test_two_call_response_interleaving_matches_4tuple_additive_pinching():
    rep = stored()
    ctrls = rep["two_call_response_interleaving_controls"]
    assert len(ctrls) == 2
    for c in ctrls:
        assert c["two_call_pinching_theorem_verified"]
        assert c["nontrivial_additive_collisions_present"]
        assert c["nontrivial_cross_fibre_additive_collision_4tuples"] > 0
        assert (
            c["complete_secret_sweep_2call_root_polynomial"]
            == c["additive_4tuple_pinched_2call_root_polynomial"]
        )


@pytest.mark.parametrize("n,d,M", ((1, 1, 1), (1, 2, 1), (1, 2, 2), (2, 1, 2)))
def test_iid_two_call_additive_collision_census_matches_3adic_stratification(n, d, M):
    res = I.iid_additive_collision_census(n, d, M)
    q = 3 ** d
    N = q ** n
    assert res["stratum_zero_over_Z_15_pow_M"] == 15 ** M
    assert res["stratum_div3_nonzero_27_pow_M_minus_15_pow_M"] == 27 ** M - 15 ** M
    assert res["stratum_unit_81_pow_M_minus_27_pow_M"] == 81 ** M - 27 ** M
    prob_div3 = Fraction(1) if d == 1 else Fraction(3 ** n, N)
    expected = (
        Fraction(15 ** M, 81 ** M)
        + Fraction(27 ** M - 15 ** M, 81 ** M) * prob_div3
        + Fraction(81 ** M - 27 ** M, 81 ** M) * Fraction(1, N)
    )
    assert Fraction(res["exact_expected_2call_collision_density_E_A_C2"]) == expected
    if M == 1:
        assert res["complete_label_bank_enumeration_verified"]
    with pytest.raises(ValueError):
        I.iid_additive_collision_census(n, d, M, max_work=1)


def test_interleaved_scaling_ledgers_and_reflection_call_bounds():
    rep = stored()
    ledgers = rep["interleaved_scaling_ledgers"]
    assert [s["dimension_n"] for s in ledgers] == [8, 32, 64, 128]
    for s in ledgers:
        assert s["r_call_reflection_chebyshev_multiplier_2r_plus_1_sq"] == 81
        assert _certificate_int(s["necessary_reflection_calls_lower_for_target"]) > 0
        assert s["arbitrary_depth_label_only_syndrome_interleaving_bounded_by_fibre_pinching"]
        assert not s["universal_quantum_lower_bound_claimed"]
        assert not s["scalable_quantum_speedup_supplied"]


def test_independent_js_checker_verifies_stored_report():
    r = node_check(stored())
    assert r.returncode == 0, r.stderr
    out = json.loads(r.stdout)
    assert out["verified"] is True
    assert out["interleaved_controls"] == 3
    assert out["two_call_controls"] == 2
    assert out["iid_censuses"] == 4
    assert out["scalable_quantum_speedup_supplied"] is False


@pytest.mark.parametrize(
    "kind",
    (
        "q2-phase",
        "sector-poly",
        "total-band-poly",
        "cross-fibre-poly",
        "two-call-nontrivial",
        "two-call-poly",
        "census-zero4",
        "census-expected",
        "scaling-cheb",
        "scaling-calls",
        "speedup-claim",
        "lower-bound-claim",
        "dependency",
        "hash",
    ),
)
def test_independent_js_checker_rejects_interleaved_and_two_call_tampering(kind):
    p = deepcopy(stored())
    c0 = p["multi_round_interleaved_controls"][0]
    t0 = p["two_call_response_interleaving_controls"][0]
    cen0 = p["iid_two_call_additive_collision_censuses"][0]
    sc0 = p["interleaved_scaling_ledgers"][0]

    if kind == "q2-phase":
        c0["multi_round_syndrome_weights"]["Q2_phase_table"][0] ^= 1
    elif kind == "sector-poly":
        c0["sector_uniform_secret_overlaps"][0]["uniform_secret_mean_overlap_root_polynomial"] = ["0"]
    elif kind == "total-band-poly":
        c0["sum_over_all_sectors_uniform_secret_overlap_root_polynomial"] = ["0"]
    elif kind == "cross-fibre-poly":
        c0["cross_fibre_word_effect_pinching"]["complete_secret_sweep_mean_root_polynomial"] = ["0"]
    elif kind == "two-call-nontrivial":
        t0["nontrivial_cross_fibre_additive_collision_4tuples"] += 1
    elif kind == "two-call-poly":
        t0["complete_secret_sweep_2call_root_polynomial"] = ["0"]
    elif kind == "census-zero4":
        cen0["stratum_zero_over_Z_15_pow_M"] += 1
    elif kind == "census-expected":
        cen0["exact_expected_2call_collision_density_E_A_C2"] = "0"
    elif kind == "scaling-cheb":
        sc0["r_call_reflection_chebyshev_multiplier_2r_plus_1_sq"] = 1
    elif kind == "scaling-calls":
        sc0["necessary_reflection_calls_lower_for_target"] = 0
    elif kind == "speedup-claim":
        p["scalable_quantum_speedup_supplied"] = True
    elif kind == "lower-bound-claim":
        p["universal_quantum_lower_bound_claimed"] = True
    elif kind == "dependency":
        p["dependency_sha256"]["native_syndrome_dilation.py"] = "0" * 64
    else:
        p["producer_sha256"] = "0" * 64
    assert node_check(p).returncode != 0
