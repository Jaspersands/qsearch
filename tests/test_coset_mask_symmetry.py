from fractions import Fraction
import math

import numpy as np
import pytest

from coset_mask_symmetry import (audit_selector_mask_symmetry, diagonal_mixture_instrument,
    physical_selector_schur_channel, radialize_mask_probabilities, radial_probabilities,
    schur_mask_distance, search_finite_radial_masks)
from isotypic_instruments import radial_mask_specification, selector_mask_symmetry_contract


FLAGS = dict(source_labelled_schur_channel=True, joint_source_and_selector_permutation_covariance=True,
    mask_fixed_before_source_records=True, natural_source_masses_retained=True, unrestricted_final_measurement=True)


def test_reduction_contract_reduces_parameters_not_objective_or_measurement_cost():
    row = selector_mask_symmetry_contract(10000, **FLAGS)
    assert row["applicable"] and row["canonical_weight_probability_count"] == 10001
    assert row["radial_pure_mask_dominates_every_fixed_mask"]
    assert row["cross_weight_coherence_must_be_retained"]
    for flag in ("source_adaptive_masks_covered", "efficient_objective_evaluation_supplied",
        "efficient_final_measurement_supplied", "all_arbitrary_masks_obstructed", "uniform_mask_is_always_optimal",
        "single_fixed_weight_is_always_optimal", "formal_proof_verification", "novelty_established"):
        assert not row[flag]
    for flag in FLAGS:
        excluded = selector_mask_symmetry_contract(10, **dict(FLAGS, **{flag: False}))
        assert not excluded["applicable"] and excluded["canonical_weight_probability_count"] is None
        with pytest.raises(ValueError):
            selector_mask_symmetry_contract(10, **dict(FLAGS, **{flag: 1}))


@pytest.mark.parametrize("k", (0, -1, True, 1.5))
def test_invalid_copy_counts_are_rejected(k):
    with pytest.raises(ValueError):
        selector_mask_symmetry_contract(k, **FLAGS)


def test_exact_radial_specification_preserves_coherent_weight_superpositions_and_tails():
    row = radial_mask_specification([Fraction(1, 3), 0, Fraction(2, 3), 0])
    assert row["copy_count"] == 3
    assert row["weight_probabilities"] == ["1/3", "0", "2/3", "0"]
    assert row["lower_tail_probability_by_threshold"] == ["0", "1/3", "1/3", "1"]
    assert row["pure_coherent_superposition_over_weight_sectors"] and not row["compiled_preparation_supplied"]
    for values in ([1], [True, 0], [.5, .5], [-1, 2], [0, 0], [1, 1]):
        with pytest.raises(ValueError):
            radial_mask_specification(values)
    weights = [Fraction(0)]*10001
    weights[3000] = Fraction(1)
    large = radial_mask_specification(weights)
    assert large["minimum_occupied_weight"] == 3000
    assert len(large["weight_probabilities"]) == 10001


def test_probability_radialization_is_not_amplitude_averaging():
    p = np.array([.1, .2, .3, .4])
    weights, radial = radialize_mask_probabilities(p)
    assert weights == pytest.approx([.1, .5, .4])
    assert radial == pytest.approx([.1, .25, .25, .4])
    assert radial_probabilities(weights) == pytest.approx(radial)
    assert radial.sum() == pytest.approx(1)
    for bad in ([.2, .3, .5], [1], [-1, 2], [float("nan"), 1], [.1, .1]):
        with pytest.raises(ValueError):
            radialize_mask_probabilities(bad)


def test_diagonal_instrument_is_trace_preserving_even_off_input_support():
    rows = np.array([[0, 1, 0, 0], [0, 0, 1, 0]])
    for weights in ([.25, .75], [0, 1]):
        average, filters = diagonal_mixture_instrument(weights, rows)
        assert (filters**2).sum(axis=0) == pytest.approx(np.ones(4))
        state = np.sqrt(average[:, None]*average[None, :])
        for weight, row, f in zip(weights, rows, filters):
            assert state*np.outer(f, f) == pytest.approx(weight*np.sqrt(row[:, None]*row[None, :]))
    with pytest.raises(ValueError):
        diagonal_mixture_instrument([.5, .5], [[1, 0]])


def test_fidelity_physical_controls_and_new_schur_model_agree():
    from coset_mask_tail_fidelity import _mask, arbitrary_mask_physical_control
    for k in (2, 3):
        model = physical_selector_schur_channel(k)
        assert max(model["residuals"].values()) < 1e-8
        assert model["blocks"].shape == (4, 3**k, 2**k, 2**k)
        for rule in ("complex_full", "high_asymmetric", "low_high_superposition"):
            actual = schur_mask_distance(model["difference_blocks"], np.abs(_mask(k, rule))**2)
            previous = arbitrary_mask_physical_control(k, rule)["physical_decision_trace_distance"]
            assert actual == pytest.approx(previous)


def test_physical_covariance_concavity_and_phase_invariance_include_strict_radial_gains():
    audit = audit_selector_mask_symmetry()
    assert audit["verified"] and len(audit["controls"]) == 2
    for row in audit["controls"]:
        assert row["permutations_checked"] == math.factorial(row["copy_count"])
        assert row["joint_permutation_covariance_residual"] < 1e-8
        assert len(row["probes"]) == 13
        assert max(r["radial_gain"] for r in row["probes"]) > .02
        for probe in row["probes"]:
            assert probe["phase_distance_residual"] < 1e-8
            assert probe["instrument_residual"] < 1e-8
            assert probe["concavity_gap"] >= -1e-8
            assert probe["radial_gain"] >= -1e-8


def _unitary_channel_difference(diagonal):
    diagonal = np.array(diagonal)
    return (np.outer(diagonal, diagonal.conjugate())-np.ones((len(diagonal), len(diagonal))))[None]


def test_missing_covariance_falsifies_radial_domination():
    # A channel-algebra countercontrol, not an HSP instance or proposed oracle task.
    delta = _unitary_channel_difference([1, -1, 1, 1])
    p = np.array([.5, .5, 0, 0])
    _, radial = radialize_mask_probabilities(p)
    assert schur_mask_distance(delta, p) == pytest.approx(1)
    assert schur_mask_distance(delta, radial) == pytest.approx(math.sqrt(3)/2)


def test_dephasing_weight_sectors_and_restricting_to_single_weights_are_invalid():
    delta = _unitary_channel_difference([1, -1, -1, 1])
    p = radial_probabilities([.5, .5, 0])
    assert schur_mask_distance(delta, p) == pytest.approx(1)
    sectors = np.array([s.bit_count() for s in range(4)])
    dephased_delta = delta*(sectors[:, None] == sectors[None, :])
    assert schur_mask_distance(dephased_delta, p) == 0
    assert all(schur_mask_distance(delta, radial_probabilities(w)) == 0 for w in np.eye(3))


@pytest.mark.parametrize("k", (2, 3))
def test_finite_weight_search_improves_actual_uniform_baseline_without_claiming_a_speedup(k):
    row = search_finite_radial_masks(k)
    weights = row["best_observed_weight_probabilities"]
    assert sum(weights) == pytest.approx(1) and min(weights) >= 0
    assert row["best_observed_radial_distance"] > row["uniform_mask_distance"]+.005
    assert row["best_observed_radial_distance"] > row["best_single_weight_distance"]+.01
    assert row["best_observed_radial_distance"] <= 1
    assert not row["global_optimality_certified"]
    assert not row["speedup_claim_allowed"] and not row["growing_degree_advantage_established"]
    assert row["source_only_baseline_requires_quantum_frontend"]


def test_fidelity_only_evidence_cannot_resolve_the_symmetry_lemma(tmp_path, monkeypatch):
    import json
    from proof_tracker import _binary_carrier_instrument_lemmas
    monkeypatch.chdir(tmp_path)
    path = tmp_path/"research/representation/coset_binary_carrier_instruments.json"
    path.parent.mkdir(parents=True)
    gate = {"finite_complete_channel_evaluation_verified": True, "mask_tail_fidelity_bound_derived": True}
    for required in ("selector_schur_covariance_controls_verified", "selector_mask_diagonal_instrument_verified", "selector_mask_radial_reduction_derived"):
        path.write_text(json.dumps({"claim_gate": gate}))
        assert _binary_carrier_instrument_lemmas("CODE-COSET-COLLECTIVE")[17].status == "blocked-selector-mask-symmetry-evidence-missing"
        gate[required] = True
    path.write_text(json.dumps({"claim_gate": gate}))
    assert _binary_carrier_instrument_lemmas("CODE-COSET-COLLECTIVE")[17].status == "derived-selector-mask-symmetry-review-pending"


def test_failed_optimizer_keeps_only_valid_baseline_witnesses(monkeypatch):
    from types import SimpleNamespace
    import scipy.optimize
    def fail(objective, start, **kwargs):
        assert np.isfinite(objective(np.zeros_like(start)))
        return SimpleNamespace(success=False, x=np.full_like(start, np.nan))
    monkeypatch.setattr(scipy.optimize, "minimize", fail)
    row = search_finite_radial_masks(2)
    assert row["optimizer_reports_converged"] == 0
    assert row["best_observed_radial_distance"] == pytest.approx(max(row["uniform_mask_distance"], row["best_single_weight_distance"]))
    assert not row["global_optimality_certified"]
