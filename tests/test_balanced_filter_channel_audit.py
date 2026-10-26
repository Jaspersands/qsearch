from fractions import Fraction as Q
import hashlib
from itertools import product
import json

import pytest

import theorems.balanced_filter_channel_audit as channel_audit
from theorems.balanced_filter_channel_audit import (
    NOTE, REPORT, ROOT, _fixture, _fwht, audit_instance, list_projection_budget,
    projection_size, report,
)


@pytest.mark.parametrize("params", [(2, 3, 2, 1), (3, 4, 1, 2), (4, 3, 1, 1)])
def test_every_target_preserves_stage_ledger_and_exact_which_message_penalty(params):
    heralds = set()
    for targets in product((0, 1), repeat=params[1]):
        row = audit_instance(*params, targets)
        clean = row["channels"]["clean"]
        dirty = row["channels"]["which_message"]
        herald = Q(*clean["herald_probability"])
        heralds.add(herald)
        messages = row["enumerated_messages"]
        assert Q(*clean["parity_valid_probability_per_attempt"]) == herald
        assert Q(*dirty["parity_valid_probability_per_attempt"])*messages == herald
        assert Q(*dirty["native_valid_probability_per_attempt"])*messages == Q(*clean["native_valid_probability_per_attempt"])
        assert 0 <= Q(*clean["native_valid_probability_per_attempt"]) <= herald <= 1
        for mode in ("which_message", "exact_weight", "exact_support", "phase_stripped"):
            assert row["channels"][mode]["herald_probability"] == clean["herald_probability"]
        assert row["which_codeword_probability_penalty_exact"] == messages
        assert row["code_projection_from_clean_register_operations_checked"]
        assert row["within_strict_gs_radius"]
        assert not row["native_large_receiver_executed"]
        assert not row["reference_has_polynomial_complexity"]
        projected = row["channels"]["padded_list_projection"]
        probability = Q(*projected["herald_probability"])
        assert probability == Q(*projected["parity_valid_probability_per_attempt"])
        assert probability+Q(*projected["projection_rejected_probability"])+Q(*projected["weight_rejected_probability"]) == 1
        assert Q(*projected["unpaid_coalesced_ball_norm_squared"]) == probability*projected["public_padding"]
        assert projected["all_projection_outcomes_accounted"]
        if not row["native_witness_count"]:
            assert all(Q(*c["native_valid_probability_per_attempt"]) == 0 for c in row["channels"].values())
    assert len(heralds) == 1


def test_equal_herald_statistics_hide_four_distinct_physical_faults():
    row = audit_instance(3, 4, 1, 2, (0, 1, 0, 1))
    expected = {"clean": Q(377, 1024), "which_message": Q(377, 8192),
                "exact_weight": Q(157, 1024), "exact_support": Q(43, 1024),
                "phase_stripped": Q(41, 1024)}
    for mode, probability in expected.items():
        assert Q(*row["channels"][mode]["herald_probability"]) == Q(19, 32)
        assert Q(*row["channels"][mode]["native_valid_probability_per_attempt"]) == probability


def test_false_singleton_may_improve_a_score_without_cleaning_original_message():
    row = audit_instance(3, 4, 1, 2, (0, 1, 0, 1))
    assert row["maximum_complete_list_size"] == 2
    assert Q(*row["incomplete_list_nonzero_message_residual_mass"]) == Q(3, 64)
    false_score = Q(*row["channels"]["incomplete_list"]["native_valid_probability_per_attempt"])
    assert false_score > Q(*row["channels"]["clean"]["native_valid_probability_per_attempt"])
    assert false_score == Q(1955, 4096)


def test_zero_herald_is_not_renormalized_or_treated_as_success():
    row = audit_instance(2, 3, 2, 2, (0, 1, 0))
    clean = row["channels"]["clean"]
    assert clean["herald_probability"] == [0, 1]
    assert clean["native_valid_probability_per_attempt"] == [0, 1]
    assert clean["conditional_native_probability"] is None
    assert not row["within_strict_gs_radius"]


def test_full_list_projection_retains_collisions_and_pays_the_normalizer():
    row = audit_instance(2, 3, 2, 2, (0, 0, 0))
    assert row["channels"]["clean"]["herald_probability"] == [0, 1]
    projected = row["channels"]["padded_list_projection"]
    assert projected["public_padding"] == 16
    assert Q(*projected["unpaid_coalesced_ball_norm_squared"]) == Q(13, 8)
    assert Q(*projected["herald_probability"]) == Q(13, 128)
    assert Q(*projected["native_valid_probability_per_attempt"]) == Q(49, 512)
    assert not row["within_strict_gs_radius"]


def test_public_padding_rounds_three_to_four_not_branch_dependent_list_length():
    row = audit_instance(2, 3, 2, 1, (0, 1, 0))
    assert row["maximum_complete_list_size"] == 3
    assert row["channels"]["padded_list_projection"]["public_padding"] == 4
    assert projection_size(3, 2, 1, 16) == 4
    with pytest.raises(ValueError):
        projection_size(3, 2, 1, 3)


def test_missing_candidate_is_rejected_instead_of_silently_projected_away(monkeypatch):
    fixture = dict(_fixture(3, 4, 1, 2))
    lists = list(fixture["lists"])
    z = next(z for z, candidates in enumerate(lists) if len(candidates) > 1)
    lists[z] = lists[z][:1]
    fixture["lists"] = tuple(lists)
    monkeypatch.setattr(channel_audit, "_fixture", lambda *_: fixture)
    with pytest.raises(ArithmeticError, match="omitted original"):
        audit_instance(3, 4, 1, 2, (0, 1, 0, 1))


@pytest.mark.parametrize("n", [17, 31, 61])
def test_full_list_native_budget_has_constant_paid_success_without_ambiguity(n):
    row = list_projection_budget(n, n*n, n*n//8, 3*n*n//5)
    assert row["padding"] == 8
    assert Q(1, 9) < row["native_success_per_attempt_lower"] < Q(1, 8)
    assert row["ideal_output_conditioned_on_native_success_is_uniform"]
    assert not row["uses_unique_decoding_assumption"]
    assert not row["uses_nonzero_symbol_point_mass_assumption"]
    assert row["invalid_success_per_attempt_upper"] < Q(1, 1000)


def test_vacuous_coherence_or_unsupported_radius_never_yields_a_native_success_claim():
    row = list_projection_budget(2, 3, 2, 1)
    assert row["eta"] >= 1
    assert row["native_success_per_attempt_lower"] == 0
    with pytest.raises(ValueError):
        list_projection_budget(2, 3, 2, 2)


def test_independent_register_protocol_reproduces_old_coalescence_controls():
    old = json.loads((ROOT / "research/reductions/balanced_codeword_filter.json").read_text())
    assert old["source_sha256"] == hashlib.sha256((ROOT / "theorems/balanced_codeword_filter.py").read_bytes()).hexdigest()
    assert old["proof_sha256"] == hashlib.sha256((ROOT / "research/BALANCED_CODEWORD_FILTER.md").read_bytes()).hexdigest()

    def rational(record):
        return Q(int(record["numerator_hex"], 16), int(record["denominator_hex"], 16))

    for control in old["finite_controls"]:
        row = audit_instance(*(control[k] for k in ("bits", "length", "dimension", "radius")), control["targets"])
        assert row["field_modulus_coefficients"] == control["field_modulus_coefficients"]
        assert row["evaluation_points"] == control["evaluation_points"]
        assert row["native_witness_count"] == control["valid_native_witness_count"]
        clean = row["channels"]["clean"]
        assert Q(*clean["herald_probability"]) == rational(control["herald_probability"])
        assert Q(*clean["native_valid_probability_per_attempt"]) == rational(control["valid_output_probability_per_attempt"])
        assert Q(*clean["conditional_native_probability"]) == rational(control["conditional_valid_probability"])


def test_cached_fixture_validation_does_not_accept_bool_as_dimension():
    _fixture(3, 4, 1, 2)
    with pytest.raises(ValueError):
        _fixture(3, 4, True, 2)


@pytest.mark.parametrize("params,targets", [
    ((5, 3, 1, 1), (0, 0, 0)),
    ((4, 4, 1, 1), (0, 0, 0, 0)),
    ((4, 3, 2, 1), (0, 0, 0)),
    ((3, 4, 0, 2), (0, 0, 0, 0)),
    ((3, 4, 1, 4), (0, 0, 0, 0)),
    ((3, 4, 1, 2), (True, 0, 0, 0)),
    ((3, 4, 1, 2), (0, 0, 0)),
])
def test_exponential_caps_and_native_input_contract(params, targets):
    with pytest.raises(ValueError):
        audit_instance(*params, targets)


def test_hadamard_integer_scaling_and_report_scope():
    values = [3, -4, 0, 2, 7, -1, 2, -5]
    assert _fwht(_fwht(values)) == [len(values)*v for v in values]
    data = report()
    assert data["all_target_inputs_checked"] == 32
    assert not data["independent_external_proof_review_complete"]
    assert not data["classical_hardness_established"]
    assert not data["scalable_receiver_implemented"]
    assert all(row["failure_after_128_fresh_attempts_power2_upper"] <= -11
               for row in data["full_list_native_budgets"])


def test_live_artifact_exact_replay_and_both_proof_bindings():
    data = json.loads(REPORT.read_text())
    assert data == report()
    assert data["proof_sha256"] == hashlib.sha256(NOTE.read_bytes()).hexdigest()
    assert data["upstream_proof_sha256"] == hashlib.sha256(
        (ROOT / "research/BALANCED_CODEWORD_FILTER.md").read_bytes()).hexdigest()
    assert data["mds_bound_source_sha256"] == hashlib.sha256(
        (ROOT / "theorems/inverse_trace_gibbs_target.py").read_bytes()).hexdigest()
