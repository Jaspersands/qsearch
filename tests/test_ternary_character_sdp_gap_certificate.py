import copy
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import subprocess

import numpy as np
import pytest

from ternary_character_sdp_decoder import character_matrix, compile_model
from ternary_character_sdp_gap_certificate import (
    DERIVATION, REPORT, SOURCE_REPORT, ceil_rational, exact_psd_residual,
    exhaustive_character_bounds, floor_rational, objective_lower, pi_interval,
    quantized_witness, root_intervals,
)
from ternary_covariant_noise import CovariantRecord, heldout_score


@pytest.mark.parametrize("value", [Fraction(5, 3), Fraction(-5, 3), Fraction(2), Fraction(-2)])
def test_outward_integer_rounding_including_negative_values(value):
    assert floor_rational(value) <= value <= ceil_rational(value)
    assert ceil_rational(value)-floor_rational(value) in (0, 1)


@pytest.mark.parametrize("q", [3, 9, 27])
def test_rational_root_intervals_have_exact_zero_and_conjugation(q):
    intervals = root_intervals(q)
    S = 2**48
    assert intervals[0] == {"cos_lower": S, "cos_upper": S, "sin_lower": 0, "sin_upper": 0}
    for e, r in enumerate(intervals):
        opposite = intervals[-e % q]
        assert r["cos_lower"] == opposite["cos_lower"] and r["cos_upper"] == opposite["cos_upper"]
        assert r["sin_lower"] == -opposite["sin_upper"] and r["sin_upper"] == -opposite["sin_lower"]
        assert r["cos_lower"]/S-1e-15 <= math.cos(2*math.pi*e/q) <= r["cos_upper"]/S+1e-15
    assert intervals[q//3]["cos_lower"] <= -S//2 <= intervals[q//3]["cos_upper"]
    lo, hi = pi_interval()
    assert 3 < lo < hi < Fraction(22, 7) and hi-lo == Fraction(1, 2**64)


def test_exact_PSD_residual_checks_integer_dominance_not_numeric_eigenvalues():
    A = np.eye(2, dtype=np.int64)*16
    L = np.eye(2, dtype=np.int64)*15
    assert exact_psd_residual(A, L, 16)["PSD_certified"]
    L[0, 0] = 32
    assert not exact_psd_residual(A, L, 16)["PSD_certified"]
    with pytest.raises(ValueError, match="int64 square"):
        exact_psd_residual(A.astype(float), L, 16)
    with pytest.raises(ValueError, match="int64 scope"):
        exact_psd_residual(A, np.eye(2, dtype=np.int64)*2**32, 16)


def test_quantized_primal_is_exactly_feasible_and_never_fakes_a_full_group_gap():
    records = (CovariantRecord((1,), (2,), (1, 2), 3),)
    model = compile_model(records)
    witness = quantized_witness(model, character_matrix(model, (1,)))
    assert witness["PSD_certified"]
    re = np.asarray(witness["matrix_real_integer"])
    im = np.asarray(witness["matrix_imag_integer"])
    assert np.all(np.diag(re) == 2**24) and np.all(np.diag(im) == 0)
    assert np.array_equal(re, re.T) and np.array_equal(im, -im.T)
    assert np.all(model["difference_operator"] @ re.reshape(-1) == 0)
    assert np.all(model["difference_operator"] @ im.reshape(-1) == 0)
    roots = root_intervals(3)
    upper = exhaustive_character_bounds(records, roots)
    lower = objective_lower(records, model["native_nodes"], witness, roots)
    assert lower <= int(upper["global_character_score_upper_numerator"])*2**24


def test_all_secrets_including_divisible_values_and_reference_cap_are_charged():
    records = (CovariantRecord((1,), (3,), (1, 4), 9), CovariantRecord((2,), (5,), (3, 7), 9))
    roots = root_intervals(9)
    census = exhaustive_character_bounds(records, roots, max_secrets=9, batch_size=2)
    assert census["secrets_checked"] == 9 and census["paired_score_features_checked"] == 54
    upper = Fraction(int(census["global_character_score_upper_numerator"]), 2**48)
    assert max(len(records)*heldout_score(records, (s,)) for s in range(9)) <= float(upper)+1e-13
    skipped = exhaustive_character_bounds(records, roots, max_secrets=8)
    assert skipped["status"] == "COMPLETE_SECRET_CENSUS_CAP_EXHAUSTED"
    assert not skipped["partial_census_certifies_global_upper"]


def test_live_exact_gaps_pin_source_and_do_not_claim_population_failure():
    report = json.loads(REPORT.read_text())
    assert report["source_report_sha256"] == hashlib.sha256(SOURCE_REPORT.read_bytes()).hexdigest()
    assert report["derivation_sha256"] == hashlib.sha256(DERIVATION.read_bytes()).hexdigest()
    assert not report["numerical_solver_status_used_as_proof"]
    assert not report["asymptotic_impossibility_or_speedup_claim"]
    assert len(report["certificates"]) == 2
    assert sum(c["character_census"]["secrets_checked"] for c in report["certificates"]) == 590490
    for c in report["certificates"]:
        assert c["status"] == "EXACT_FINITE_SDP_CHARACTER_GAP"
        assert int(c["strict_gap_lower_numerator"]) > 0
        assert not c["finite_counterexample_is_population_or_asymptotic_failure"]
        assert not c["certification_uses_truth_or_holdout"]


CHECKER = Path(__file__).resolve().parents[1]/"research/certificates/ternary_character_sdp_gap_certificate_crosscheck.js"


def test_independent_exact_integer_interval_and_complete_secret_replay():
    output = subprocess.run(["node", str(CHECKER)], check=True, capture_output=True, text=True)
    result = json.loads(output.stdout)
    assert result["status"] == "PASS" and result["exact_finite_gaps"] == 2
    assert result["full_root_secrets_checked"] == 590490
    assert result["exact_score_features_checked"] == 56687040
    assert not result["numerical_eigenvalues_or_solver_status_trusted"]


@pytest.mark.parametrize("mutation", ["scope", "source", "root", "factor", "census", "gap"])
def test_tampered_finite_certificates_are_rejected(tmp_path, mutation):
    report = copy.deepcopy(json.loads(REPORT.read_text()))
    c = report["certificates"][0]
    if mutation == "scope":
        report["asymptotic_impossibility_or_speedup_claim"] = True
    elif mutation == "source":
        report["source_report_sha256"] = "0"*64
    elif mutation == "root":
        c["root_intervals"][1]["cos_upper"] += 1
    elif mutation == "factor":
        c["witness"]["factor_lower_triangle_integer"][0][0] = 2**25
    elif mutation == "census":
        c["character_census"]["secrets_checked"] -= 1
    else:
        c["strict_gap_lower_numerator"] = str(int(c["strict_gap_lower_numerator"])+1)
    target = tmp_path/"tampered.json"
    target.write_text(json.dumps(report))
    output = subprocess.run(["node", str(CHECKER), str(target)], capture_output=True, text=True)
    assert output.returncode != 0
