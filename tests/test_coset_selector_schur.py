from fractions import Fraction
import itertools
import json
import math

import numpy as np
import pytest

from coset_selector_schur import (audit_source_resolved_selector_schur, full_source_collision_audit,
    radial_schur_statistics, selector_schur_storage, selector_spin_sectors, source_resolved_schur_model,
    source_stabilizer_cost, symmetric_power, _compositions)
from representation_obstruction import hook_length_dimension, integer_partitions
from self_dual_wreath_global_collision_free_mass import plancherel_weights
from weak_fourier_signal import character_on_involution


def _dicke_isometry(n):
    w = np.zeros((2**n, n+1))
    for s in range(2**n):
        w[s, s.bit_count()] = 1/math.sqrt(math.comb(n, s.bit_count()))
    return w


@pytest.mark.parametrize("count", range(7))
def test_spin_blocks_match_tensor_action_with_singlets_including_singular_nonnormal_matrices(count):
    rng = np.random.default_rng(90210)
    a = rng.normal(size=(2, 2))+1j*rng.normal(size=(2, 2))
    matrices = (a, a+a.conj().T, np.array([[1, 2j], [0, 0]]), np.zeros((2, 2)), np.eye(2))
    singlet = np.array([0, 1, -1, 0])[:, None]/math.sqrt(2)
    for b in matrices:
        tensor = np.ones((1, 1), dtype=complex)
        for _ in range(count):
            tensor = np.kron(tensor, b)
        for ell, _, _ in selector_spin_sectors(count):
            w = _dicke_isometry(count-2*ell)
            for _ in range(ell):
                w = np.kron(w, singlet)
            predicted = np.linalg.det(b)**ell*symmetric_power(b, count-2*ell)
            assert w.conj().T @ w == pytest.approx(np.eye(w.shape[1]))
            assert tensor @ w == pytest.approx(w @ predicted, abs=1e-8)
    assert sum(d*m for _, d, m in selector_spin_sectors(count)) == 2**count
    assert sum(d*d for _, d, _ in selector_spin_sectors(count)) == math.comb(count+3, 3)


def test_normalized_symmetric_power_is_a_representation_not_a_monomial_basis_similarity():
    a = np.array([[1, 2j], [.3, -.8j]])
    b = np.array([[0, .7], [1j, 2]])
    for n in range(6):
        assert symmetric_power(a @ b, n) == pytest.approx(symmetric_power(a, n) @ symmetric_power(b, n), abs=1e-8)
        assert symmetric_power(np.array([a, b]), n)[0] == pytest.approx(symmetric_power(a, n))


@pytest.mark.parametrize("k,r", itertools.product(range(1, 7), range(1, 5)))
def test_total_storage_formula_keeps_all_histograms_and_spin_blocks(k, r):
    cost = selector_schur_storage(k, r)
    histograms = list(_compositions(k, r))
    assert cost["source_histogram_count"] == len(histograms)
    assert cost["entries_per_hypothesis_all_histograms"] == sum(source_stabilizer_cost(c)["spin_matrix_entries"] for c in histograms)
    assert sum(source_stabilizer_cost(c)["source_orbit_size"] for c in histograms) == r**k
    assert not cost["growing_category_count_polynomial_proved"]


def test_distinct_sources_destroy_this_compression_not_all_possible_efficient_measurements():
    repeated = source_stabilizer_cost([64])
    distinct = source_stabilizer_cost([1]*64)
    assert repeated["largest_spin_block_dimension"] == 65
    assert distinct["stabilizer_order"] == distinct["spin_block_count"] == 1
    assert distinct["largest_spin_block_dimension"] == 2**64
    assert distinct["spin_matrix_entries"] == 4**64
    assert not distinct["dimension_is_a_circuit_lower_bound"]
    assert source_stabilizer_cost([0, 2, 0])["source_orbit_size"] == 1


def test_full_spectra_natural_masses_and_coherence_match_independent_physical_channels():
    report = audit_source_resolved_selector_schur()
    assert report["verified"] and len(report["controls"]) == 3
    for control in report["controls"]:
        assert control["full_spectral_residual"] < 1e-8
        assert control["hidden_members_checked"] == 3
        assert max(p["decision_distance"]-p["incorrect_top_spin_only_distance"] for p in control["probes"]) > .01
        assert max(p["decision_distance"]-p["erased_source_distance"] for p in control["probes"]) > .1
    probes = [p for c in report["controls"] for p in c["probes"]]+report["extended_copy_controls"]
    assert max(p["decision_distance"]-p["incorrect_unit_multiplicity_distance"] for p in probes) > .01
    assert max(p["decision_distance"]-p["weight_pinched_distance"] for p in probes) > .001
    assert max(np.mean(p["individual_hidden_distances"])-p["decision_distance"] for p in probes) > .001
    for flag in ("classical_simulator_for_growing_degree", "intermediate_band_obstructed", "efficient_measurement_compiled",
                 "formal_proof_verification", "independent_review", "novelty_established"):
        assert not report[flag]
    json.dumps(report, allow_nan=False)


def test_more_copies_use_spin_blocks_and_preserve_zero_weight_amplitudes():
    model = source_resolved_schur_model(3, 6)
    assert model["cost"]["entries_per_hypothesis_all_histograms"] == 12376 < 12**6
    assert sum(b["hypothesis_blocks"].shape[-1]**2 for b in model["blocks"]) == 12376
    row = radial_schur_statistics(model, [0, 0, .3, 0, .7, 0, 0])
    assert 0 < row["decision_distance"] < 1 and row["normalization_residual"] < 1e-8
    assert not row["efficient_measurement_supplied"]
    with pytest.raises(ValueError, match="budget"):
        source_resolved_schur_model(3, 100)
    for bad in ([.5, .5], [0]*7, [1, 0, 0, 0, 0, 0, float("nan")]):
        with pytest.raises(ValueError):
            radial_schur_statistics(model, bad)


@pytest.mark.parametrize("copies", (1, 2, 4, 6))
def test_exact_collision_laws_use_actual_alternative_sources_and_charge_the_shared_hidden_model(copies):
    row = full_source_collision_audit(4, copies, exact_distinct=True)
    p = plancherel_weights(4)
    q = tuple(Fraction(hook_length_dimension(lam)*(hook_length_dimension(lam)+character_on_involution(lam, 2)), 24)
        for lam in integer_partitions(4))
    for name, law in (("null", p), ("alternative", q)):
        direct = sum((math.prod(law[i] for i in indices) for indices in itertools.permutations(range(len(law)), copies)), Fraction())
        assert Fraction(row[f"{name}_distinct_probability"]) == direct
        assert 1-direct <= Fraction(row[f"{name}_collision_upper_bound"])
    assert row["alternative_pair_collision_at_most_four_times_null"]
    assert row["source_law_independent_of_hidden_conjugate"] and row["source_law_independent_of_fixed_mask"]
    assert not row["finite_asymptotic_crossover_certified"]


@pytest.mark.parametrize("call", (
    lambda: symmetric_power(np.eye(2), True), lambda: symmetric_power(np.eye(3), 2),
    lambda: symmetric_power(np.full((2, 2), np.nan), 1), lambda: selector_spin_sectors(-1),
    lambda: selector_spin_sectors(True), lambda: source_stabilizer_cost([]),
    lambda: source_stabilizer_cost([0]), lambda: source_stabilizer_cost([True]),
    lambda: selector_schur_storage(True, 2), lambda: selector_schur_storage(2, 0),
    lambda: source_resolved_schur_model(5, 2), lambda: source_resolved_schur_model(3, True),
    lambda: source_resolved_schur_model(3, 2, erase_source_labels=1),
    lambda: full_source_collision_audit(3, 2), lambda: full_source_collision_audit(4, True),
    lambda: full_source_collision_audit(4, 2, exact_distinct=1),
))
def test_invalid_inputs_are_rejected(call):
    with pytest.raises(ValueError):
        call()


def test_proof_gate_requires_both_physical_spectra_and_source_mass_argument(tmp_path, monkeypatch):
    from proof_tracker import _binary_carrier_instrument_lemmas
    monkeypatch.chdir(tmp_path)
    path = tmp_path/"research/representation/coset_binary_carrier_instruments.json"
    path.parent.mkdir(parents=True)
    keys = ("finite_complete_channel_evaluation_verified", "selector_mask_radial_reduction_derived",
        "source_resolved_selector_schur_spectra_verified", "full_source_selector_collision_free_boundary_derived")
    gate = dict.fromkeys(keys, True)
    path.write_text(json.dumps({"claim_gate": gate}))
    lemmas = _binary_carrier_instrument_lemmas("CODE-COSET-COLLECTIVE")
    assert len({row.id for row in lemmas}) == len(lemmas)
    assert lemmas[21].status == "derived-source-resolved-selector-schur-boundary-review-pending"
    for missing in keys:
        path.write_text(json.dumps({"claim_gate": dict(gate, **{missing: False})}))
        assert _binary_carrier_instrument_lemmas("CODE-COSET-COLLECTIVE")[21].status == "blocked-source-resolved-selector-schur-evidence-missing"


def test_cached_calibrations_do_not_bypass_boolean_validation_or_mutate_queries():
    from coset_mask_tail_fidelity import regular_selector_query_control
    source_resolved_schur_model(3, 1)
    with pytest.raises(ValueError):
        source_resolved_schur_model(3, True)
    with pytest.raises(ValueError):
        source_resolved_schur_model(3, 1, erase_source_labels=0)
    _, actions, projectors, a, _ = regular_selector_query_control(3)
    assert not actions.flags.writeable and not projectors.flags.writeable and not a.flags.writeable
