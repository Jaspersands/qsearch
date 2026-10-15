"""Tests for the certified public rounded-Gaussian dither and sign/mask batch sampler."""
from copy import deepcopy
from fractions import Fraction
import json
import subprocess

import pytest

from theorems import native_gaussian_dither_sampler as D
from native_basis_lottery import _certificate_int


def stored():
    return json.loads(D.REPORT.read_text())


def node_check(payload):
    return subprocess.run(
        [
            "node",
            "-e",
            "const X=require('./research/certificates/native_gaussian_dither_sampler_crosscheck.js');"
            "let s='';process.stdin.on('data',x=>s+=x);"
            "process.stdin.on('end',()=>console.log(JSON.stringify(X.verify(JSON.parse(s)))));",
        ],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        cwd=D.ROOT,
    )


@pytest.mark.parametrize("sigma,f", (("3/2", 1), ("5/2", 4), ("81", 8), (str(3 ** 40), 10)))
def test_adaptive_threshold_precision_union_and_per_draw_coupling_budget(sigma, f):
    p = D.dither_draw_parameters(sigma, f)
    B = _certificate_int(p["truncation_bound_B"])
    K = p["active_dyadic_bits_K"]
    assert p["total_binary_search_thresholds_2B_plus_2"] == 2 * B + 2
    assert Fraction(p["adaptive_all_threshold_precision_abort_upper"]) == Fraction(4 * (2 * B + 2), 2 ** K)
    assert Fraction(p["adaptive_all_threshold_precision_abort_upper"]) <= Fraction(1, 2 ** (f + 1))
    assert Fraction(p["per_draw_coupling_loss_upper"]) <= Fraction(1, 2 ** f)
    assert p["adaptive_union_strictly_exceeds_naive_for_positive_B"]
    assert Fraction(p["adaptive_all_threshold_precision_abort_upper"]) > Fraction(
        p["naive_query_count_precision_bound_DO_NOT_USE"]
    )


def test_complete_bounded_dyadic_prefix_censuses_match_cdf_quantile_brackets():
    rep = stored()
    for census in rep["bounded_dyadic_prefix_censuses"]:
        assert census["every_accepted_cell_verified_against_directed_cdf_brackets"]
        assert census["precision_abort_within_adaptive_union_bound"]
        assert not census["finite_census_is_an_oracle_or_speedup_candidate"]
        total = census["total_dyadic_cells_censused"]
        assert sum(census["status_counts"].values()) == total
        assert (
            Fraction(census["exact_accepted_mass"])
            + Fraction(census["exact_precision_abort_mass"])
            + Fraction(census["exact_tail_abort_mass"])
            == 1
        )
    with pytest.raises(ValueError):
        D.complete_dyadic_prefix_census("3/2", 1, 7, max_work=10)


def test_single_draw_controls_cover_negative_zero_positive_and_giant_widths():
    ctrls = stored()["single_draw_controls"]
    outcomes = [_certificate_int(c["draw"]["sampled_integer"]) for c in ctrls]
    assert outcomes[0] < 0
    assert outcomes[1] == 0
    assert outcomes[2] > 0
    assert abs(outcomes[3]) > 2 ** 53
    for c in ctrls:
        draw = c["draw"]
        assert draw["status"] == "CERTIFIED_ROUNDED_GAUSSIAN_SAMPLE"
        assert not draw["midpoint_or_floating_fallback_used"]
        assert not draw["silent_resampling_used"]
        assert not draw["independent_transcendental_certificate_supplied"]


def test_forced_tail_precision_numerical_cap_and_complete_batch_aborts():
    fals = stored()["abort_and_trap_falsifiers"]
    assert fals["forced_left_tail_abort"]["status"] == "TAIL_TRUNCATION_ABORT"
    assert fals["forced_left_tail_abort"]["tail_side"] == "LEFT_TAIL"
    assert fals["forced_right_tail_abort"]["status"] == "TAIL_TRUNCATION_ABORT"
    assert fals["forced_right_tail_abort"]["tail_side"] == "RIGHT_TAIL"
    assert fals["forced_uniform_prefix_precision_abort"]["status"] == "UNIFORM_PREFIX_PRECISION_ABORT"
    assert fals["forced_numerical_precision_cap_abort"]["status"] == "NUMERICAL_PRECISION_CAP_ABORT"

    batch_abort = fals["forced_complete_batch_abort_diagnostic"]
    assert batch_abort["status"] == "ABORTED_COMPLETE_REFRESH_BATCH_DIAGNOSTIC_ONLY"
    assert batch_abort["producer_input"] is None
    assert batch_abort["refresh_transform"] is None
    assert batch_abort["completed_dither_draws"] == 1
    assert not batch_abort["shortened_batch_emitted_as_valid_source"]


def test_mask_rejection_sampling_abort_aborts_complete_refresh_batch():
    ctrl = stored()["integrated_source_refresh"]["complete_batch_control"]
    raw = tuple(
        D.NoisyLinearRecord(
            tuple(_certificate_int(a) for a in r["label"]),
            _certificate_int(r["value"]),
            _certificate_int(r["modulus"]),
            r["source_id"],
        )
        for r in ctrl["original_records"]
    )
    # All-ones bits force candidate_integer = 127 >= 81 on every mask trial
    all_ones = (1,) * 256
    res = D.certified_refresh_batch(raw, 81, (0, 0), "3/2", 2, 2, 2, all_ones)
    assert res["status"] == "ABORTED_COMPLETE_REFRESH_BATCH_DIAGNOSTIC_ONLY"
    assert res["abort_reason"] == "MASK_REJECTION_SAMPLING_ABORT"
    assert res["producer_input"] is None
    assert res["completed_dither_draws"] == 0


def test_complete_batch_integration_and_coupled_source_refresh_ledger():
    integ = stored()["integrated_source_refresh"]
    batch = integ["complete_batch_control"]["batch_result"]
    assert batch["status"] == "CERTIFIED_COMPLETE_REFRESH_BATCH_READY_FOR_EXTERNAL_PRODUCER"
    assert batch["completed_dither_draws"] == 3
    assert batch["producer_input"] == batch["refresh_transform"]["producer_input"]
    assert not batch["fresh_public_randomness_is_a_fresh_original_sample"]

    for prof in integ["coupled_source_refresh_profiles"]:
        b_loss = Fraction(prof["batch_sampler_budget"]["certified_complete_dither_sampler_TV_loss"])
        s_led = prof["coupled_source_refresh_ledger"]
        assert Fraction(s_led["certified_complete_dither_sampler_TV_loss_EXTERNAL"]) == b_loss
        assert Fraction(s_led["one_refresh_coverage_lower_IF_quality_and_external_contracts_hold"]) > 0


def test_arb_probability_box_replay_and_independent_js_crosscheck():
    rep = stored()
    arb_res = D.verify_probability_boxes(rep)
    assert arb_res["verified"] is True
    assert arb_res["Arb_tail_boxes_replayed"] == 141
    assert arb_res["independent_transcendental_certificate_supplied"] is False

    js_res = node_check(rep)
    assert js_res.returncode == 0, js_res.stderr
    out = json.loads(js_res.stdout)
    assert out["verified"] is True
    assert out["single_draw_controls"] == 4
    assert out["censused_dyadic_cells"] == 384
    assert out["coupled_refresh_profiles"] == 3
    assert out["actual_quantum_producer_supplied"] is False


@pytest.mark.parametrize(
    "kind",
    (
        "draw-sigma",
        "draw-threshold",
        "draw-cdf-lower",
        "draw-integer",
        "draw-adaptive-union",
        "census-hist",
        "census-precision-mass",
        "abort-batch-producer-input",
        "batch-sign",
        "batch-mask",
        "batch-dither",
        "coupled-sampler-loss",
        "transcendental-claim",
        "producer-claim",
        "dependency",
        "hash",
    ),
)
def test_independent_js_checker_rejects_sampler_transcript_and_budget_tampering(kind):
    p = deepcopy(stored())
    d0 = p["single_draw_controls"][0]["draw"]
    c0 = p["bounded_dyadic_prefix_censuses"][0]
    ba = p["abort_and_trap_falsifiers"]["forced_complete_batch_abort_diagnostic"]
    br = p["integrated_source_refresh"]["complete_batch_control"]["batch_result"]
    cp = p["integrated_source_refresh"]["coupled_source_refresh_profiles"][0]

    if kind == "draw-sigma":
        d0["draw_parameters"]["sigma"] = "7/2"
    elif kind == "draw-threshold":
        d0["threshold_comparisons"][0]["threshold_t"] += 1
    elif kind == "draw-cdf-lower":
        d0["threshold_comparisons"][0]["cdf_box"]["lower"] = "1/2"
    elif kind == "draw-integer":
        d0["sampled_integer"] += 1
    elif kind == "draw-adaptive-union":
        d0["draw_parameters"]["adaptive_all_threshold_precision_abort_upper"] = d0["draw_parameters"][
            "naive_query_count_precision_bound_DO_NOT_USE"
        ]
    elif kind == "census-hist":
        c0["sampled_integer_histogram"]["0"] += 1
    elif kind == "census-precision-mass":
        c0["exact_precision_abort_mass"] = "0"
    elif kind == "abort-batch-producer-input":
        ba["producer_input"] = {"modulus": 81, "labels": [], "responses": []}
    elif kind == "batch-sign":
        br["signs_and_mask_sampling"]["sign_rows"][0][0] *= -1
    elif kind == "batch-mask":
        br["signs_and_mask_sampling"]["secret_mask"][0] = (br["signs_and_mask_sampling"]["secret_mask"][0] + 1) % 81
    elif kind == "batch-dither":
        br["dither_draw_receipts"][0]["sampled_integer"] += 1
    elif kind == "coupled-sampler-loss":
        cp["batch_sampler_budget"]["certified_complete_dither_sampler_TV_loss"] = "0"
    elif kind == "transcendental-claim":
        p["independent_transcendental_certificate_supplied"] = True
    elif kind == "producer-claim":
        p["actual_quantum_decision_or_multiple_producer_supplied"] = True
    elif kind == "dependency":
        p["dependency_sha256"]["native_source_refresh.py"] = "0" * 64
    else:
        p["producer_sha256"] = "0" * 64
    assert node_check(p).returncode != 0
