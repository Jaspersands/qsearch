from copy import deepcopy
from fractions import Fraction
import hashlib
import json
import random
import subprocess

import pytest

from ternary_covariant_noise import CovariantRecord, simulated_record
from ternary_cyclic_extractor import random_even_source
from ternary_flat_character_certificate import Cyclotomic, ResourceLimit
from ternary_sequential_spectral_extraction import (
    DERIVATION, REPORT, Uncertified, bounded_reference, calibration_payload,
    confidence_ledger, pinching_constant, polynomial_precision_ledger,
    prepare_model, psd_certificate, run_sampling, sequential_draw,
)


@pytest.fixture(scope="module")
def native():
    source = random_even_source(2, 4, 3, 89641)
    rng = random.Random(89642)
    records = tuple(simulated_record(a, c, (1, 3), 9, rng)[0] for a, c in source.frequencies)
    return records


@pytest.fixture(scope="module")
def payload(native):
    return calibration_payload(native, ((0, 0), (1, 3), (8, 8)), perturb=True, reverse=True)


@pytest.fixture(scope="module")
def model(native, payload):
    result, prepared = prepare_model(native, payload)
    assert result["supplied_model_certified"]
    return prepared


@pytest.fixture(scope="module")
def artifact():
    return json.loads(REPORT.read_text())


def record_objects(control):
    return tuple(CovariantRecord(tuple(r["first"]), tuple(r["second"]), tuple(r["outcome"]), r["modulus"])
                 for r in control["records"])


@pytest.mark.parametrize("q", [3, 9, 27, 81, 243])
def test_pinching_constant_uses_balanced_cyclic_powers(q):
    exact = Fraction(sum(abs(k) for k in range(-(q-1)//2, (q-1)//2+1)), q)
    assert pinching_constant(q) == exact < Fraction(q-1, 2)


@pytest.mark.parametrize("rows,definite,rank", [
    ([[1, 0], [0, 0]], False, 1), ([[2, 1], [1, 2]], True, 2),
    ([[0, 0], [0, 1]], False, 1), ([[1, 1], [1, 1]], False, 1),
])
def test_exact_LDL_handles_positive_and_zero_pivots(rows, definite, rank):
    field = Cyclotomic(9)
    matrix = field.matrix([[field.K.convert(x) for x in row] for row in rows])
    cert = psd_certificate(field, matrix, require_definite=definite)
    assert cert["rank_exact"] == rank
    L = field.matrix([[field.decode(x) for x in row] for row in cert["lower_unit_matrix"]])
    d = [field.decode(x) for x in cert["diagonal"]]
    D = field.matrix([[d[i] if i == j else field.K.zero for j in range(len(d))] for i in range(len(d))])
    assert L*D*field.conjugate_matrix(L).transpose() == matrix


@pytest.mark.parametrize("rows,definite", [
    ([[1, 2], [2, 1]], False), ([[0, 1], [1, 0]], False),
    ([[1, 0], [0, 0]], True), ([[1, 1], [0, 1]], False),
])
def test_indefinite_nonhermitian_and_singular_metrics_fail(rows, definite):
    field = Cyclotomic(9)
    matrix = field.matrix([[field.K.convert(x) for x in row] for row in rows])
    with pytest.raises(Uncertified):
        psd_certificate(field, matrix, require_definite=definite)


def test_noncommuting_q_order_generators_and_metric_are_certified(model):
    U, V = model.operators
    assert U*V != V*U
    identity = U**model.field.q
    assert V**model.field.q == identity
    assert model.certificate["commutator_norm_certificates"]
    assert not model.certificate["classical_model_construction_from_native_input_supplied"]
    assert not model.certificate["all_internal_intermediate_bit_costs_certified"]


def test_order_three_generators_at_root_nine_are_not_called_full_secret_coverage(native):
    p = calibration_payload(native, ((0, 0), (3, 0), (0, 3)))
    result, prepared = prepare_model(native, p)
    assert result["supplied_model_certified"] and prepared is not None
    assert not result["all_generators_primitive_q_order"]
    assert all(period <= 3 for period in result["generator_exact_periods"])
    assert Fraction(result["uniform_secret_coverage_upper_from_generator_periods"]) <= Fraction(1, 9)
    for seed in range(5):
        draw = sequential_draw(prepared, random.Random(seed))
        assert all(s % 3 == 0 for s in draw["secret"])


def test_identity_generators_can_only_extract_zero_secret_not_an_unknown_answer(native):
    p = calibration_payload(native, ((0, 0), (0, 0), (0, 0)))
    result, prepared = prepare_model(native, p)
    assert result["supplied_model_certified"]
    assert result["generator_exact_periods"] == [1, 1]
    assert result["secret_support_size_upper_from_generator_periods"] == "1"
    assert result["uniform_secret_coverage_upper_from_generator_periods"] == "1/81"
    assert sequential_draw(prepared, random.Random(9))["secret"] == (0, 0)


@pytest.mark.parametrize("mutation", [
    "zero_commutator", "zero_representation_error", "missing_difference", "wrong_order",
    "native_access", "indefinite_metric", "unnormalized_state", "nonunitary",
    "float_delta", "float_sigma", "bool_sigma", "noncanonical_sigma", "fake_moments",
])
def test_supplied_premises_are_proved_not_trusted(native, payload, mutation):
    p = deepcopy(payload)
    if mutation == "zero_commutator":
        p["commutator_operator_norm_uppers"] = [["0", "0"], ["0", "0"]]
    elif mutation == "zero_representation_error":
        p["representation_error_uppers"] = [["0"]*3 for _ in native]
    elif mutation == "missing_difference":
        p["original_native_moments"][0].pop()
    elif mutation == "wrong_order":
        p["represented_product_order"].reverse()
    elif mutation == "native_access":
        p["access_model"] = "native_sample_supply"
    elif mutation == "indefinite_metric":
        p["metric"][0][0] = ["-1"]
    elif mutation == "unnormalized_state":
        p["state"][0][0] = ["1"]
    elif mutation == "nonunitary":
        p["operators"][0][0][0] = ["2"]
    elif mutation == "float_delta":
        p["commutator_operator_norm_uppers"][0][1] = 0.01
    elif mutation == "float_sigma":
        p["representation_error_uppers"][0][0] = 0.01
    elif mutation == "bool_sigma":
        p["representation_error_uppers"][0][0] = True
    elif mutation == "noncanonical_sigma":
        p["representation_error_uppers"][0][0] = "2/4"
    else:
        p["original_native_moments"][0] = [["1"]]*3
        p["representation_error_uppers"][0] = ["0"]*3
    result, prepared = prepare_model(native, p)
    assert not result["supplied_model_certified"]
    assert prepared is None and result["issues"]


def test_every_balanced_word_and_nonrational_probability_is_checked(model):
    ref = bounded_reference(model)
    assert len(ref["probabilities"]) == len(ref["all_balanced_word_probes"]) == 81
    assert any(len(p["probability"]) > 1 for p in ref["probabilities"])
    assert all(p["disturbance_certificate"]["status"] in ("ZERO", "POSITIVE") for p in ref["all_balanced_word_probes"])
    assert not ref["reference_is_scalable_sampler"]
    with pytest.raises(ResourceLimit):
        bounded_reference(model, max_outcomes=80)


def test_opposite_measurement_orders_have_different_actual_distributions(native, payload, model):
    forward = deepcopy(payload)
    forward["measurement_order"] = forward["represented_product_order"] = [0, 1]
    result, other = prepare_model(native, forward)
    assert result["supplied_model_certified"]
    assert bounded_reference(other)["probabilities"] != bounded_reference(model)["probabilities"]


def test_single_branch_sampler_does_not_need_reference_grid(model, monkeypatch):
    monkeypatch.setattr("ternary_sequential_spectral_extraction.bounded_reference", lambda *_: pytest.fail("secret table enumerated"))
    draw = sequential_draw(model, random.Random(5))
    assert draw["secret_certified"]
    assert len(draw["dyadic_prefix_transcript"]) == 2
    assert not draw["discarded_then_redrawn"]
    assert not draw["accepted_distribution_conditioned_on_no_abort_is_claimed_unbiased"]


def test_ambiguous_dyadic_prefix_aborts_instead_of_redrawing(native):
    p = calibration_payload(native, ((0, 0), (1, 3), (8, 8)))
    _, prepared = prepare_model(native, p)
    class BoundaryBits:
        calls = 0
        def getrandbits(self, bits):
            self.calls += 1
            return 113  # Bin113/256 straddles the first CDF boundary4/9.
    rng = BoundaryBits()
    result = sequential_draw(prepared, rng, max_random_bits=8)
    assert result["status"].startswith("UNKNOWN_") and rng.calls == 1
    assert not result["secret_certified"] and not result["discarded_then_redrawn"]


def test_sample_budget_is_committed_before_any_random_draw(model):
    class NoBits:
        def getrandbits(self, _):
            pytest.fail("insufficient sample budget nevertheless consumed randomness")
    ledger = confidence_ledger(model.records, Fraction(3, 8), 8)
    assert ledger["required_fixed_independent_draws"] == 392
    assert ledger["bound_controls_bad_and_returned_event_not_abort_conditioned_probability"]
    result = run_sampling(model, Fraction(3, 8), rng=NoBits(), max_draws=391)
    assert not result["conditional_rounding_score_certified"]


def test_seeded_sampling_only_claims_exact_posthoc_score(model):
    result = run_sampling(model, Fraction(3, 8), confidence_bits=1, rng=random.Random(89662))
    assert result["conditional_rounding_score_certified"]
    assert result["completed_draws"] == 49
    assert result["randomness_kind"] == "seeded_calibration"
    assert not result["probabilistic_failure_claim_applies_to_this_seeded_run"]
    assert not result["held_out_native_prediction_verified"]
    assert not result["native_noisy_recovery_proved"]
    assert not result["quantum_speedup_proved"]


@pytest.mark.parametrize("cap", [0, True, 0.5, 53])
def test_projector_caps_never_certify_partial_vocabulary(native, payload, cap):
    result, prepared = prepare_model(native, payload, max_projector_entries=cap)
    assert prepared is None and not result["supplied_model_certified"]


@pytest.mark.parametrize("n,q", [(8, 9), (32, 81), (128, 243)])
def test_precision_ledger_has_polynomial_not_recursive_exponential_requirement(n, q):
    ledger = polynomial_precision_ledger(n, q)
    h = Fraction(q*q-1, 4*q)
    L = h*Fraction((q-1)*n*(n-1), 4)
    assert Fraction(ledger["worst_balanced_word_uniform_commutator_coefficient"]) == L
    assert Fraction(ledger["sufficient_uniform_commutator_bound_at_zero_representation_error"]) == Fraction(1, 30)/L
    assert not ledger["native_source_satisfies_premises"]


def test_live_report_has_prespecified_sources_known_support_and_no_algorithm_claim(artifact):
    assert artifact["derivation_sha256"] == hashlib.sha256(DERIVATION.read_bytes()).hexdigest()
    assert [c["source_seed"] for c in artifact["commuting_native_label_controls"]] == [89513, 89523, 89533]
    for c in artifact["commuting_native_label_controls"]+artifact["noncommuting_native_label_controls"]:
        result, _ = prepare_model(record_objects(c), c["supplied_model"])
        assert json.loads(json.dumps(result)) == c["verification"]
        assert c["supplied_model"]["calibration_operators_encode_known_support"]
        assert not c["supplied_model"]["matrices_were_constructed_from_native_noisy_records"]
        assert c["sampling"]["conditional_rounding_score_certified"]
        if c in artifact["commuting_native_label_controls"]:
            assert result["all_generators_exactly_commute"]
            assert int(result["secret_support_size_upper_from_supplied_model"]) <= 3
    assert not artifact["native_noisy_decoder_supplied"]
    assert not artifact["candidate_record_accepted"]


def test_independent_exact_checker_replays_live_report():
    checker = REPORT.parents[1]/"certificates/ternary_sequential_spectral_extraction_crosscheck.js"
    completed = subprocess.run(["node", str(checker)], check=True, capture_output=True, text=True)
    result = json.loads(completed.stdout)
    assert result["status"] == "PASS"
    assert result["all_balanced_word_probes"] == 162
    assert result["sample_trajectories_checked"] == 1960


@pytest.mark.parametrize("mutation", ["claim_speedup", "claim_native_access", "drop_difference", "wrong_prefix"])
def test_independent_checker_rejects_tampered_evidence(artifact, tmp_path, mutation):
    report = deepcopy(artifact)
    c = report["commuting_native_label_controls"][0]
    if mutation == "claim_speedup":
        report["quantum_speedup_proved"] = True
    elif mutation == "claim_native_access":
        c["supplied_model"]["has_native_quantum_access_to_these_generators"] = True
    elif mutation == "drop_difference":
        c["supplied_model"]["original_native_moments"][0].pop()
    else:
        c["sampling"]["dyadic_prefix_trajectories"][0][0][1] = "99999999"
    path = tmp_path/"tampered.json"
    path.write_text(json.dumps(report))
    checker = REPORT.parents[1]/"certificates/ternary_sequential_spectral_extraction_crosscheck.js"
    result = subprocess.run(["node", str(checker), str(path)], capture_output=True, text=True)
    assert result.returncode != 0 and not result.stdout
