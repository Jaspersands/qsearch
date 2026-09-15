from fractions import Fraction
import json
import math

import numpy as np
import pytest

from coset_mask_cross_sector import (audit_cross_sector_coherence, audit_overlap_decay_counterexample,
    occupation_band_scaling_controls, _double_character_column)
from coset_mask_symmetry import physical_selector_schur_channel
from coset_mask_tail_fidelity import _regular_selector_model
from isotypic_instruments import source_selector_occupation_band_contract as contract


FLAGS = dict(one_common_subset_query=True, common_group_algebra_unitary=True,
    unitary_and_partition_fixed_before_inputs=True, hidden_prior_uniform_on_involution_class=True,
    no_hidden_correlated_preprocessing_or_side_information=True, source_records_classical=True,
    source_partition_is_irrep_coarsening=True, only_source_records_and_selector_qubits_retained=True,
    physical_inputs_discarded=True, mask_fixed_before_inputs_and_source_records=True)


def test_independent_double_character_kernels_check_every_hidden_member_and_overlap():
    report = audit_cross_sector_coherence()
    assert report["verified"] and not report["novelty_established"]
    assert sum(len(r["rows"]) for r in report["controls"]) == 32
    assert sum(len(r["probes"]) for r in report["controls"]) == 48
    for row in report["controls"]:
        assert row["source_tuple_count"] == (3 if row["degree"] == 3 else 5)**row["copy_count"]
        assert row["hidden_members_checked"] == 3
        assert row["double_character_reconstruction_residual"] < 1e-8
        assert row["high_side_endpoint_identity_residual"] < 1e-8
        for pair in row["rows"]:
            s, t = pair["low_subset"], pair["high_subset"]
            assert pair["high_only_sites"] == (t & ~s).bit_count() >= t.bit_count()-s.bit_count()
            for name, value in pair["component_norms"].items():
                assert value <= pair["component_upper_bounds"][name]+1e-8
        assert any(pair["shared_sites"] > 0 for pair in row["rows"])
        for probe in row["probes"]:
            assert -1e-8 <= probe["intersector_gain"] <= probe["cross_block_trace_norm"]+1e-8
        assert max(p["cross_block_trace_norm"] for p in row["probes"]) > 1e-4
    assert max(p["intersector_gain"] for r in report["controls"] for p in r["probes"]) > 1e-4


def test_swapping_coefficient_conjugation_does_not_reconstruct_physical_cross_columns():
    data, actions, projectors, a, _, _ = _regular_selector_model(2, 3)
    model = physical_selector_schur_channel(2, 3)
    p = np.einsum("jab,gba->jg", projectors, actions).real/len(a)
    wrong = _double_character_column(p, np.array(model["sources"]), 1, 3, a.conjugate(), data[6], data[7]).sum(axis=(1, 2))
    assert np.max(np.abs(wrong-model["blocks"][0, :, 1, 3])) > 1e-4


def test_exact_s6_overlap_counterexample_counts_only_exclusive_positions():
    report = audit_overlap_decay_counterexample()
    assert report["verified"] and len(report["controls"]) == 14
    assert not report["shared_sites_may_be_counted_as_high_only_decay"]
    for row in report["controls"]:
        exclusive = Fraction(row["exclusive_factor_squared_norm"])
        actual = Fraction(row["actual_two_site_squared_norm"])
        false = Fraction(row["incorrect_shared_site_decay_prediction"])
        assert 0 < exclusive <= Fraction(4, 15)
        assert actual == Fraction(16, 15)*exclusive
        assert false == exclusive**2 < actual


def test_hidden_endpoint_average_is_a_correlated_product_not_two_independent_averages():
    data, _, _, a, _, _ = _regular_selector_model(2, 3)
    model = physical_selector_schur_channel(2, 3)
    hidden = [h[0] for h in data[8]]
    low = model["blocks"][1:, :, 1, 0]/a.sum().conjugate()
    actual = (a[hidden].conjugate()[:, None]*low).mean(axis=0)
    incorrect = a[hidden].conjugate().mean()*low.mean(axis=0)
    assert np.max(np.abs(actual-incorrect)) > 1e-4


def test_occupation_band_bounds_charge_coherence_and_do_not_close_the_middle_band():
    rows = occupation_band_scaling_controls()
    assert [r["trace_distance_upper_bound_power_of_two"] for r in rows] == [0, -216, -1883, -1883, 0]
    assert rows[1]["cross_sector_contribution_upper_bound_power_of_two"] == -344
    assert rows[2]["cross_sector_contribution_upper_bound_power_of_two"] == -2395
    for row in rows:
        assert row["low_high_coherence_explicitly_charged"] and row["selector_rank_factor_charged"]
        assert not row["shared_positions_counted_as_high_only"]
        assert not row["intermediate_weight_band_obstructed"] and not row["all_arbitrary_masks_obstructed"]
        assert not row["middle_mass_bound_independently_verified"]
        assert not row["formal_proof_verification"] and not row["independent_review"]


def test_cross_components_and_composite_sum_round_outwards_exactly():
    n, k, t, s = 1024, 1024**2, 256, 3072
    row = contract(n, k, t, s, middle_mass_upper_bound=0, **FLAGS)
    m, d, l = math.prod(range(1, n, 2)), math.factorial(n), n*(n-1)//2
    rank = sum(math.comb(k, i) for i in range(t+1))
    e = Fraction(m, m-k)
    squares = {"low_column": Fraction(rank*(k+2**t-1), 4*(m-k)),
        "hidden_endpoint": Fraction(rank, 4)*e/m,
        "alternative_off_endpoint": Fraction(rank*d*d, 4)*e*Fraction(4, l)**(s-t),
        "null_off_endpoint": Fraction(rank*d*d, 4)*Fraction(1, l)**(s-t)}
    terms = row["cross_component_upper_bound_powers_of_two"]
    for name, square in squares.items():
        assert square <= Fraction(2)**(2*terms[name])
    cross = Fraction(2)**row["cross_sector_contribution_upper_bound_power_of_two"]
    assert sum(Fraction(2)**value for value in terms.values()) <= cross
    diagonal = Fraction(2)**row["pinched_sector_upper_bound_power_of_two"]
    assert diagonal+cross <= Fraction(2)**row["trace_distance_upper_bound_power_of_two"]


def test_empty_middle_interval_and_extreme_thresholds_are_not_materialized():
    empty = contract(128, 1000, 10, 11, middle_mass_upper_bound=1, **FLAGS)
    assert empty["middle_interval_empty"] and empty["effective_middle_mass_upper_bound"] == "0"
    assert empty["gentle_middle_removal_upper_bound_power_of_two"] is None
    huge = contract(1024, 10**100, 10**99, 10**100, middle_mass_upper_bound=0, **FLAGS)
    assert huge["bound_is_vacuous"] and not huge["numerical_composite_envelope_evaluated"]
    capped = contract(1024, 1024**2, 256, 1024**2, middle_mass_upper_bound=0, **FLAGS)
    assert capped["high_tail_threshold_used"] == 3072
    assert capped["high_only_decay_threshold_used"] == 4096
    assert capped["trace_distance_upper_bound_power_of_two"] < 0


@pytest.mark.parametrize("flag", FLAGS)
def test_scope_assumptions_are_explicit_and_not_silently_relaxed(flag):
    row = contract(128, 1000, 10, 384, middle_mass_upper_bound=0, **dict(FLAGS, **{flag: False}))
    assert not row["applicable"] and row["trace_distance_upper_bound_power_of_two"] is None
    with pytest.raises(ValueError):
        contract(128, 1000, 10, 384, middle_mass_upper_bound=0, **dict(FLAGS, **{flag: 1}))


@pytest.mark.parametrize("n,k,t,s,pi", ((7, 5, 1, 2, 0), (9, 5, 1, 2, 0), (8, True, 0, 1, 0),
    (8, 5, True, 2, 0), (8, 5, 0, True, 0), (8, 5, 2, 2, 0), (8, 5, 3, 2, 0),
    (8, 5, -1, 2, 0), (8, 5, 1, 6, 0), (8, 5, 1, 2, .5), (8, 5, 1, 2, True),
    (8, 5, 1, 2, -1), (8, 5, 1, 2, 2)))
def test_invalid_band_inputs(n, k, t, s, pi):
    with pytest.raises(ValueError):
        contract(n, k, t, s, middle_mass_upper_bound=pi, **FLAGS)


def test_separate_low_high_bounds_do_not_resolve_the_new_cross_sector_lemma(tmp_path, monkeypatch):
    from proof_tracker import _binary_carrier_instrument_lemmas
    monkeypatch.chdir(tmp_path)
    path = tmp_path/"research/representation/coset_binary_carrier_instruments.json"
    path.parent.mkdir(parents=True)
    gate = {"finite_complete_channel_evaluation_verified": True, "low_occupation_support_bound_derived": True,
        "mask_tail_fidelity_bound_derived": True}
    for required in ("source_character_square_bound_verified", "cross_sector_double_character_controls_verified",
                     "cross_sector_high_side_endpoint_verified", "occupation_band_localization_derived"):
        path.write_text(json.dumps({"claim_gate": gate}))
        assert _binary_carrier_instrument_lemmas("CODE-COSET-COLLECTIVE")[20].status == "blocked-occupation-band-evidence-missing"
        gate[required] = True
    path.write_text(json.dumps({"claim_gate": gate}))
    lemmas = _binary_carrier_instrument_lemmas("CODE-COSET-COLLECTIVE")
    assert len({lemma.id for lemma in lemmas}) == len(lemmas)
    assert lemmas[20].status == "derived-occupation-band-bound-review-pending"
    for required in gate:
        path.write_text(json.dumps({"claim_gate": dict(gate, **{required: False})}))
        assert _binary_carrier_instrument_lemmas("CODE-COSET-COLLECTIVE")[20].status == "blocked-occupation-band-evidence-missing"
