import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

from coset_missing_harmonic_detector import (
    DEFAULT_EXPERIMENT_ID, SELECTOR_ONLY_SCOPE, amplification_contract, audit_selector_only_queries, build_missing_harmonic_report,
    finite_control, finite_subset_projectors, frame_moments, grover_response,
    scaling_control, schedule_null_upper_bound, selector_only_query_contract, write_missing_harmonic_report,
)


def rational(record):
    return Fraction(int(record["numerator_hex"], 16), int(record["denominator_hex"], 16))


@pytest.mark.parametrize("spec", ((3, 1, 1), (3, 1, 2), (3, 1, 3), (4, 1, 2)))
def test_complete_physical_projectors_and_walks(spec):
    row = finite_control(*spec)
    assert row["verified"]
    assert max(row["residuals"].values()) < 1e-9
    assert row["null_acceptance"] >= row["certified_null_acceptance_lower_bound"]
    assert row["individual_subset_null_acceptance"] == pytest.approx(1 / math.factorial(spec[0]))
    if spec == (3, 1, 3):
        assert row["max_subset_commutator_frobenius_norm"] > 0.1
        assert row["null_acceptance"] > row["individual_subset_null_acceptance"]


def test_sign_premise_is_not_silently_extended_to_even_involutions():
    with pytest.raises(ValueError, match="not a missing harmonic"):
        finite_control(4, 2, 2)
    with pytest.raises(ValueError, match="2 mod 4"):
        scaling_control(128)
    from coset_hidden_involution_binary_decision_reduction import dense_hidden_coset_state
    projectors, _ = finite_subset_projectors(4, 1)
    invalid_alternative = dense_hidden_coset_state(4, (1, 0, 3, 2), 1)
    assert np.trace(projectors[0] @ invalid_alternative) == pytest.approx(2 / 24)


@pytest.mark.parametrize("n,copies", ((5, 1), (4, 3), (100, 1), (3, 100)))
def test_no_factorial_calibration_allocation(n, copies):
    with pytest.raises(ValueError, match="budget"):
        finite_subset_projectors(n, copies)


def test_nonuniform_weights_and_uniform_second_moment_optimality():
    ps, _ = finite_subset_projectors(3, 2)
    weights = (Fraction(1, 2), Fraction(1, 3), Fraction(1, 6))
    mean, second = frame_moments(6, weights)
    frame = sum(float(w) * p for w, p in zip(weights, ps))
    assert np.trace(frame) / 36 == pytest.approx(float(mean))
    assert np.trace(frame @ frame) / 36 == pytest.approx(float(second))
    assert second > frame_moments(6, (Fraction(1, 3),) * 3)[1]
    assert frame_moments(6, (1, 0, 0)) == (Fraction(1, 6), Fraction(1, 6))


@pytest.mark.parametrize("weights", ((), (0.5, 0.5), (Fraction(1, 3),), (2, -1), (True,)))
def test_invalid_weight_certificates(weights):
    with pytest.raises(ValueError):
        frame_moments(6, weights)


@pytest.mark.parametrize("order", (2, 6, 24, 720, 10000))
def test_randomized_response_including_near_one_and_arbitrarily_small_values(order):
    steps = math.isqrt(order) + (math.isqrt(order)**2 < order)
    values = np.unique(np.concatenate((np.linspace(1 / (2 * order), 1, 1001), [0, 1e-40, 1-1e-12, 1])))
    response = grover_response(values, steps)
    assert response[0] == 0
    assert response[-1] == pytest.approx(1)
    assert np.min(response[values >= 1 / (2 * order)]) >= 1 / 8 - 1e-12
    assert np.all(response <= (2 * steps**2 + 1) / 3 * values + 1e-12)


@pytest.mark.parametrize("n", (6, 10, 66, 258, 1026, 4098))
def test_exact_scaling_has_constant_bias_but_no_polynomial_compiler(n):
    row = scaling_control(n)
    certificate = row["certificate"]
    assert certificate["constant_bias_certified"]
    assert rational(certificate["detector_null_acceptance_lower_bound"]) >= Fraction(1, 64)
    assert not certificate["requires_smallest_positive_eigenvalue"]
    assert not certificate["polynomial_time_compiler"]
    assert row["log2_selected_projector_call_ceiling"] > row["log2_coherent_oracle_matching_search_scale"]
    if n >= 66:
        assert rational(row["polynomial_schedule_null_acceptance_upper_bound"]) < Fraction(1, 1000000)
    json.dumps(row)  # Large exact integers never trigger unsafe decimal conversion.


def test_threshold_copy_count_and_no_free_normalization():
    assert not amplification_contract(720, 9)["constant_bias_certified"]
    assert amplification_contract(720, 10)["constant_bias_certified"]
    assert schedule_null_upper_bound(720, 1) == Fraction(1, 720)
    assert schedule_null_upper_bound(6, 3) == 1
    for args in ((True, 3), (6, True), (0, 3), (6, 0)):
        with pytest.raises(ValueError):
            amplification_contract(*args)


def test_report_has_no_claim_promotion_and_disabled_writes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    report = write_missing_harmonic_report(Path("report.json"), write_registry=False,
                                          finite_specs=((3, 1, 2),), scaling_n_values=(6,), query_specs=((3, 2, 1),))
    assert report["claim_gate"]["gap_free_constant_bias_derivation_checked"]
    for gate in ("speedup_claim_allowed", "polynomial_time_compiler_constructed", "novelty_established", "independently_reviewed", "formally_verified"):
        assert report["claim_gate"][gate] is False
    assert not Path("research/registry").exists()
    assert not build_missing_harmonic_report(finite_specs=(), scaling_n_values=(6,), query_specs=())["claim_gate"]["finite_physical_controls_verified"]


def test_registry_runner_proof_gate_and_idempotent_writes(tmp_path, monkeypatch):
    import experiment_runner
    import proof_tracker
    from research_registry import (initialize_seed_registry, load_experiment_results,
                                   load_negative_results, validate_registry)
    monkeypatch.chdir(tmp_path)
    initialize_seed_registry(overwrite=True)
    assert DEFAULT_EXPERIMENT_ID in experiment_runner.supported_experiment_ids()
    assert "blocked" in proof_tracker._missing_harmonic_detector_lemmas("CODE-COSET-COLLECTIVE")[0].status
    real_writer = write_missing_harmonic_report

    def small_writer(**kwargs):
        return real_writer(finite_specs=((3, 1, 2),), scaling_n_values=(6,), query_specs=((3, 2, 1),), **kwargs)

    monkeypatch.setattr(experiment_runner, "write_missing_harmonic_report", small_writer)
    small_writer()  # Direct command and experiment runner share a result key.
    for _ in range(2):
        outcome = experiment_runner.run_experiment(DEFAULT_EXPERIMENT_ID)
        assert outcome.status == "completed"
    results = [r for r in load_experiment_results() if r["experiment_id"] == DEFAULT_EXPERIMENT_ID]
    assert len(results) == 1
    assert Path(results[0]["artifacts"]["report"]).exists()
    assert any("MISSING-SIGN-GENERIC" in r["id"] for r in load_negative_results())
    from dequantization_checks import build_dequantization_report
    findings = build_dequantization_report()
    assert any(r["id"].endswith("RETAINED-DATA-NORMALIZED-WALK-COST") for r in findings["findings"])
    assert validate_registry()["valid"]
    lemmas = proof_tracker._missing_harmonic_detector_lemmas("CODE-COSET-COLLECTIVE")
    assert lemmas[0].status == "derived-gap-free-detector-review-pending"
    assert lemmas[1].status == "derived-selector-only-query-hybrid-review-pending"
    assert lemmas[2].status.startswith("blocked")
    assert lemmas[3].status == "derived-source-adaptive-missing-sign-hybrid-review-pending"
    report_path = Path(results[0]["artifacts"]["report"])
    report = json.loads(report_path.read_text())
    report["claim_gate"]["source_adaptive_channel_controls_verified"] = False
    report_path.write_text(json.dumps(report))
    assert proof_tracker._missing_harmonic_detector_lemmas("CODE-COSET-COLLECTIVE")[3].status.startswith("blocked")
    assert any(r["id"] == "MISSING-SIGN-SOURCE-ADAPTIVE-QUERY-BOUND" for r in load_negative_results())
    assert any(r["id"].endswith("MISSING-SIGN-SOURCE-ADAPTIVE-QUERY-HYBRID") for r in findings["findings"])
    report["claim_gate"]["gap_free_constant_bias_derivation_checked"] = 1
    report_path.write_text(json.dumps(report))
    assert proof_tracker._missing_harmonic_detector_lemmas("CODE-COSET-COLLECTIVE")[0].status.startswith("blocked")


@pytest.mark.parametrize("spec", ((3, 3, 0), (3, 3, 1), (3, 3, 3), (4, 2, 1)))
def test_selector_only_hybrid_and_forbidden_readout_counterexample(spec):
    row = audit_selector_only_queries(*spec)
    assert row["verified"]
    assert row["maximum_hidden_baseline_residual"] < 1e-9
    assert row["forbidden_free_data_readout_null_acceptance"] > 0.1
    assert row["forbidden_free_data_readout_hidden_acceptance"] < 1e-9
    if spec[-1] == 0:
        assert row["ancilla_trace_distance"] < 1e-9
        assert row["one_sided_ancilla_acceptance"] < 1e-9


@pytest.mark.parametrize("scope_key", SELECTOR_ONLY_SCOPE)
@pytest.mark.parametrize("invalid", (False, 1))
def test_query_bound_rejects_missing_or_merely_truthy_scope(scope_key, invalid):
    scope = {key: True for key in SELECTOR_ONLY_SCOPE}
    scope[scope_key] = invalid
    result = selector_only_query_contract(720, 100, 1, scope=scope)
    assert not result["applicable"]
    assert scope_key in result["scope_issues"]
    assert "output_trace_distance_squared_upper_bound" not in result


def test_query_bound_is_independent_of_copy_count_but_not_a_general_circuit_bound():
    scope = {key: True for key in SELECTOR_ONLY_SCOPE}
    for copies in (1, 100, 100000):
        result = selector_only_query_contract(720, copies, 2, scope=scope)
        assert rational(result["output_trace_distance_squared_upper_bound"]) == Fraction(1, 45)
        assert not result["general_retained_data_circuit_lower_bound"]
        assert not result["arbitrary_program_scope_verified"]
    assert not selector_only_query_contract(720, 2, 1, scope={})["applicable"]
    assert not selector_only_query_contract(720, 2, 1, scope={**scope, "free_data_readout": True})["applicable"]
    assert rational(selector_only_query_contract(720, 2, 0, scope=scope)["one_sided_null_acceptance_upper_bound"]) == 0
