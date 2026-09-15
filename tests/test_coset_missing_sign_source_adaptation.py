import json
from fractions import Fraction

import numpy as np
import pytest

from coset_missing_sign_source_adaptation import (
    SOURCE_ADAPTIVE_SCOPE, build_source_adaptive_audit, exact_source_census,
    physical_source_adaptive_control, regular_source_rank_control, source_adaptive_query_contract,
)


def rational(record):
    return Fraction(int(record["numerator_hex"], 16), int(record["denominator_hex"], 16))


@pytest.mark.parametrize("spec,expected,count", (
    ((3, 1, 3), Fraction(119, 216), 189),
    ((4, 1, 2), Fraction(23, 192), 75),
    ((4, 1, 3), Fraction(2819, 13824), 875),
    ((6, 3, 2), Fraction(719, 172800), 363),
))
def test_all_source_subsets_obey_exact_rank_bound(spec, expected, count):
    row = exact_source_census(*spec)
    assert row["verified"]
    assert row["conditional_sector_count"] == count
    assert rational(row["mean_best_subset_probability"]) == expected
    assert expected <= rational(row["dimension_cap"])
    if spec[0] == 6:
        assert rational(row["source_score_second_moment"]) == Fraction(1, 15)
        assert rational(row["inverse_dimension_mean"]) == Fraction(11, 720)


@pytest.mark.parametrize("n", (3, 4))
def test_character_ranks_and_both_priors_match_regular_physics(n):
    row = regular_source_rank_control(n, 2)
    assert row["verified"]
    assert row["maximum_rank_residual"] < 1e-9
    assert row["maximum_source_prior_residual"] < 1e-9
    assert row["per_hidden_source_prior_check_count"] == (9 if n == 3 else 30)


@pytest.mark.parametrize("spec", ((3, 1, 2, 0), (3, 1, 3, 2), (4, 1, 2, 1)))
def test_source_adaptive_physical_program_and_hidden_member_laws(spec):
    row = physical_source_adaptive_control(*spec)
    assert row["verified"]
    assert row["max_hidden_baseline_residual"] < 1e-9
    assert row["max_state_normalization_residual"] < 1e-9
    assert np.ptp(row["per_hidden_full_output_trace_distances"]) < 1e-9
    assert row["classical_baseline_includes_quantum_weak_label_frontend"]
    assert not row["optimal_ancilla_readout_compiler_supplied"]
    if spec[-1] == 0:
        assert rational(row["exact_source_prior_tv"]) == Fraction(11, 36)
        assert row["per_hidden_full_output_trace_distances"][0] == pytest.approx(11/36)
        assert row["null_to_identity_query_ancilla_distance"] < 1e-9
        assert not row["contract"]["one_sided_query_only_bound_available"]
    if spec[-1] == 1:
        assert row["null_to_identity_query_ancilla_distance"] == pytest.approx(row["mean_best_subset_probability"])
        assert row["finite_information_gain_over_weak_labels"][0] == pytest.approx(1/144)


@pytest.mark.parametrize("key", SOURCE_ADAPTIVE_SCOPE)
@pytest.mark.parametrize("wrong", (False, 1))
def test_source_scope_does_not_cover_other_data_operations(key, wrong):
    scope = {name: True for name in SOURCE_ADAPTIVE_SCOPE}
    scope[key] = wrong
    row = source_adaptive_query_contract(6, 3, 36, 36, scope=scope)
    assert not row["applicable"]
    assert key in row["scope_issues"]
    assert "output_trace_distance_squared_upper_bound" not in row


@pytest.mark.parametrize("n", (6, 10, 34, 66, 258, 1026, 4098))
def test_scalable_contract_uses_exact_arithmetic_and_keeps_weak_source_term(n):
    scope = {name: True for name in SOURCE_ADAPTIVE_SCOPE}
    row = source_adaptive_query_contract(n, n//2, n*n, n*n, scope=scope)
    zero = source_adaptive_query_contract(n, n//2, n*n, 0, scope=scope)
    assert row["applicable"]
    assert rational(zero["output_trace_distance_squared_upper_bound"]) > 0
    assert rational(zero["query_hybrid_distance_squared_upper_bound"]) == 0
    assert not row["general_circuit_lower_bound"]
    assert not row["arbitrary_program_scope_verified"]
    if n >= 66:
        assert row["output_trace_distance_upper_bound_power_of_two"] < -20
    json.dumps(row)


def test_invalid_scope_and_missing_sign_premises_are_rejected():
    scope = {name: True for name in SOURCE_ADAPTIVE_SCOPE}
    for args in ((4, 2, 16, 2), (6, 3, True, 1), (6, 3, 36, True), (6, 3, 36, -1)):
        with pytest.raises(ValueError):
            source_adaptive_query_contract(*args, scope=scope)
    assert not source_adaptive_query_contract(6, 3, 36, 1, scope={})["applicable"]
    assert not source_adaptive_query_contract(6, 3, 36, 1, scope={**scope, "extra": True})["applicable"]
    with pytest.raises(ValueError, match="budget"):
        exact_source_census(4, 1, 100)
    with pytest.raises(ValueError, match="budget"):
        exact_source_census(8, 1, 4)
    with pytest.raises(ValueError, match="transpositions"):
        exact_source_census(4, True, 2)
    with pytest.raises(ValueError, match="declared"):
        physical_source_adaptive_control(6, 3, 2, 1)


def test_report_gates_require_physical_and_exact_evidence(monkeypatch):
    report = build_source_adaptive_audit()
    assert report["verified"]
    assert sum(row["conditional_sector_count"] for row in report["censuses"]) == 1502
    assert sum(row["sector_comparison_count"] for row in report["regular_controls"]) == 102
    assert not report["independent_review"]
    assert not report["formal_verification"]
    assert not report["novelty_established"]
    assert not report["speedup_claim_allowed"]
    assert not build_source_adaptive_audit(physical_specs=())["verified"]
    import coset_missing_sign_source_adaptation as module
    from coset_missing_harmonic_detector import build_missing_harmonic_report
    report["verified"] = False
    monkeypatch.setattr(module, "build_source_adaptive_audit", lambda **kwargs: report)
    combined = build_missing_harmonic_report(finite_specs=((3, 1, 1),), query_specs=((3, 2, 1),), scaling_n_values=(6,))
    assert not combined["claim_gate"]["source_adaptive_query_bound_derived"]
    assert not combined["claim_gate"]["finite_physical_controls_verified"]
    assert combined["status"] == "control-failure"
