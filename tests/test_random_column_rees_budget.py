"""Exact forest/error checks; no source or whole-HSP correctness claim."""
from fractions import Fraction
from hashlib import sha256
from math import gcd
from pathlib import Path

import pytest

from theorems.random_column_rees_budget import random_column_tree_budget, report


def _logceil(value):
    exponent = 0
    while 2**exponent < value:
        exponent += 1
    return exponent


@pytest.mark.parametrize("u", range(2, 13))
def test_global_bank_and_tree_bounds_through_class_twelve(u):
    profile = (u+1,)+tuple(range(u-1, 0, -1))
    p = 65537
    result = random_column_tree_budget(profile, prime=p,
                                      uniform_parameter=u, intrinsic_rank_bound=u-1)
    width, c = 4*u, len(profile)
    P = width**(c-1)
    nodes = sum(width**j for j in range(c-1))
    B = _logceil(64*P)
    assert result["leaves_per_tree"] == P
    assert result["merges_per_tree"] == nodes == (P-1)//(width-1)
    assert result["classical_failure_bits_per_node"] == B
    bank_total = failure = Fraction(0)
    trial_total = fair_total = bracket_total = qft_per_tree = 0
    for stage in reversed(result["stages_top_down"]):
        d = stage["grade"]
        degree = gcd(d, p-1)
        a = min(profile[d-1], u-1)
        h = (p-1)//degree
        vectors, calls = (h+1)**width-1, width**(d-2)
        mean = Fraction(vectors//h, p**a)
        bad = min(Fraction(1), 4/mean+Fraction(2, p**(width-a)))
        assert mean >= 2**(8*u+1)*u**(2*u+1)
        assert stage["projective_count_mean_lower_bound"] == mean
        assert stage["iid_bad_bank_bound"] == bad
        assert stage["conversions_per_tree"] == calls
        assert stage["good_bank_power_kernel_density_lower_bound"] >= Fraction(1, 4*degree**width)
        bank_total += calls*bad
        if degree > 1:
            trials = 4*degree**width*B
            root_cap = 3*(B+_logceil(width*(degree-1))+2)
            draws = trials*width+width*degree*(degree-1)*root_cap
            rejection = B+1+_logceil(draws)
            roots_fail = width*(degree-1)*Fraction(2, 3)**root_cap
            bits_fail = Fraction(draws, 2**rejection)
            fail = bad+Fraction(1, 2**B)+roots_fail+bits_fail
            assert stage["kernel_trial_cap"] == trials
            assert stage["root_split_attempt_cap"] == root_cap
            assert stage["uniform_field_draw_cap"] == draws
            assert stage["integer_rejection_cap"] == rejection
            assert stage["fair_bit_cap"] == draws*rejection*17
        else:
            trials = draws = rejection = 0
            roots_fail = bits_fail = fail = Fraction(0)
            assert stage["root_call_cap"] == stage["kernel_trial_cap"] == 0
        assert stage["root_failure_bound"] == roots_fail
        assert stage["integer_rejection_bound"] == bits_fail
        assert stage["node_abort_bound"] == fail
        failure += calls*fail
        trial_total += calls*trials
        fair_total += calls*draws*rejection*(p-1).bit_length()
        bracket_total += calls*4*width*((d-1)*d*(d+1)*(d+2)//6)
        qft_per_tree += calls*(2*width*profile[d-1]+sum(profile[:d-1]))
    assert bank_total <= Fraction(1, 64)
    assert failure == result["tree_abort_bound"] <= Fraction(1, 16)
    assert result["tree_abort_bound_used_for_restart"] == Fraction(1, 4)
    m = result["desired_terminal_samples"]
    attempts = 4*m
    assert result["whole_tree_attempt_cap"] == attempts
    assert result["lifted_source_cap"] == attempts*P
    assert result["original_oracle_query_cap"] == c*attempts*P
    assert result["classical_kernel_trial_cap"] == attempts*trial_total
    assert result["classical_fair_bit_cap"] == attempts*fair_total
    assert result["compiled_bracket_call_cap"] == attempts*bracket_total
    assert result["single_coordinate_qft_call_cap"] == attempts*(P*sum(profile)+qft_per_tree)+m*profile[0]


@pytest.mark.parametrize("error", [Fraction(1, 3), Fraction(1, 2**100)])
def test_restart_precision_and_all_error_shares(error):
    result = random_column_tree_budget((6, 3, 1), prime=1009,
                                      uniform_parameter=4, intrinsic_rank_bound=3, error=error)
    m = 6+_logceil(3/error)
    assert result["desired_terminal_samples"] == m
    assert result["leaves_per_tree"] == 16**2
    assert result["original_oracle_query_cap"] == 3*4*m*16**2
    rank = Fraction(1, 1008*1009**(m-6))
    fewer = Fraction(1, 2**(2*m))
    assert result["final_rank_failure_bound"] == rank <= error/3
    assert result["fewer_successes_failure_bound"] == fewer <= error/3
    assert result["complete_quantum_error_bound"] <= error/3
    assert result["total_error_bound"] == rank+fewer+result["complete_quantum_error_bound"] <= error
    eta, bits = result["qft_isometry_error_per_call"], result["qft_precision_bits"]
    assert Fraction(1, 2**bits) <= eta < Fraction(1, 2**(bits-1))
    assert result["all_failed_trees_charged"] is True
    assert result["labels_resampled_inside_kernel_trials"] is False
    assert result["successful_outputs_required_to_decouple_from_records"] is True


def test_intrinsic_codimension_bound_is_not_ambient_or_cover_rank():
    result = random_column_tree_budget((6, 4, 3, 2, 1), prime=577,
                                      uniform_parameter=6, intrinsic_rank_bound=3)
    stages = list(reversed(result["stages_top_down"]))
    assert [s["ambient_label_dimension"] for s in stages] == [4, 3, 2, 1]
    assert [s["intrinsic_rank_upper_bound"] for s in stages] == [3, 3, 2, 1]
    assert result["field_threshold"] == 64*3**2
    assert result["width_per_grade"] == 8*3
    assert result["intrinsic_rank_promise_verified"] is False
    assert result["observed_bank_rank_certifies_intrinsic_rank"] is False


def test_zero_intrinsic_rank_needs_no_stochastic_solver():
    result = random_column_tree_budget((6, 3, 1), prime=1009,
                                      uniform_parameter=3, intrinsic_rank_bound=0)
    assert result["tree_abort_bound"] == 0
    assert result["classical_kernel_trial_cap"] == result["classical_fair_bit_cap"] == 0
    assert result["original_oracle_query_cap"] > 0


@pytest.mark.parametrize("changes", [
    {"prime": 5}, {"prime": None}, {"prime": True},
    {"uniform_parameter": 1}, {"uniform_parameter": True}, {"uniform_parameter": 3.0},
    {"uniform_parameter": 2}, {"intrinsic_rank_bound": 4},
    {"intrinsic_rank_bound": -1}, {"intrinsic_rank_bound": True},
    {"error": 0.1}, {"error": Fraction(0)}, {"error": Fraction(1)},
])
def test_reject_unpaid_regimes_and_malformed_inputs(changes):
    args = dict(prime=1009, uniform_parameter=4, intrinsic_rank_bound=3)
    args.update(changes)
    with pytest.raises(ValueError):
        random_column_tree_budget((6, 3, 1), **args)


def test_report_runs_only_bounded_classical_controls_and_binds_sources():
    payload = report()
    root = Path(__file__).resolve().parents[1]
    for path, digest in payload["source_sha256"].items():
        assert sha256((root/path).read_bytes()).hexdigest() == digest
    assert len(payload["source_sha256"]) == 7
    assert [r["attempts"] for r in payload["arithmetic_controls"]] == [403, 62]
    assert all(r["status"] == "VERIFIED" and r["exact_verified"] for r in payload["arithmetic_controls"])
    assert payload["adversarial_bank_control"]["status"] == "ABORT"
    assert payload["adversarial_bank_control"]["reason"] == "ATTEMPT_CAP"
    for key in ("source_hashes_certify_proof", "quantum_receiver_implemented", "novelty_established",
                "candidate_promotion", "proof_promotion", "speedup_claim_allowed",
                "arithmetic_controls_certify_iid_source"):
        assert payload[key] is False
    for row in payload["cases"]:
        assert row["oracle_queries_executed"] == 0
        assert row["iid_intrinsic_label_law_required"]
        assert not row["joint_source_law_verified"]
        assert not row["fixed_bank_success_guaranteed"]
        assert row["total_error_bound"] <= row["error_target"]
