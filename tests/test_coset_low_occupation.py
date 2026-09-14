from fractions import Fraction
import json
import math

import numpy as np
import pytest

from coset_mask_symmetry import (audit_low_occupation_support, low_occupation_scaling_controls,
    physical_selector_schur_channel, schur_mask_distance)
from isotypic_instruments import source_selector_low_occupation_contract as contract


FLAGS = dict(one_common_subset_query=True, common_group_algebra_unitary=True,
    unitary_and_partition_fixed_before_inputs=True, hidden_prior_uniform_on_involution_class=True,
    no_hidden_correlated_preprocessing_or_side_information=True, source_records_classical=True,
    source_partition_is_irrep_coarsening=True, only_source_records_and_selector_qubits_retained=True,
    physical_inputs_discarded=True, mask_fixed_before_inputs_and_source_records=True,
    declared_mask_weight_and_support_bounds_hold=True)


def test_entire_physical_blocks_pay_support_rank_after_bounding_all_active_unions():
    report = audit_low_occupation_support()
    assert report["verified"]
    assert sum(r["matrix_entries_checked"] for r in report["controls"]) == 96
    for row in report["controls"]:
        categories = 3 if row["degree"] == 3 else 5
        assert row["source_tuple_count"] == categories**row["copy_count"] and row["hidden_members_checked"] == 3
        assert row["largest_entry_bound_excess"] < 1e-9
        for probe in row["probes"]:
            assert probe["total_distance"] <= probe["rank_charged_trace_distance_upper_bound"]+1e-9
            assert probe["source_weighted_frobenius_squared"] <= probe["largest_active_union_chi_square_bound"]+1e-9
            t, k = probe["maximum_mask_weight"], row["copy_count"]
            assert probe["support_size"] == sum(math.comb(k, i) for i in range(t+1))


def test_s4_physical_extension_checks_a_fixed_point_free_class_and_rejects_undeclared_models():
    model = physical_selector_schur_channel(2, 4)
    assert len(model["sources"]) == 25
    assert model["blocks"].shape == (4, 25, 4, 4)
    assert max(model["residuals"].values()) < 1e-8
    for k, n in ((3, 4), (2, 5), (2, True), (True, 3)):
        with pytest.raises(ValueError):
            physical_selector_schur_channel(k, n)


def test_growing_low_weight_support_is_obstructed_without_claiming_all_masks():
    controls = low_occupation_scaling_controls()
    assert [r["trace_distance_upper_bound_power_of_two"] for r in controls] == [0, -217, -1884]
    for row in controls:
        assert row["selector_rank_factor_charged"]
        assert not row["union_subset_count_used_as_selector_rank"]
        assert not row["full_channel_reduced_to_twice_weight_copies"]
        assert not row["all_arbitrary_masks_obstructed"]
        assert not row["low_high_intersector_coherence_obstructed"]
        assert not row["novelty_established"] and not row["formal_proof_verification"]


def test_exact_dimension_envelope_and_supplied_sparse_support_bound_round_outwards():
    n, k, t = 1024, 1024**2, 256
    m = math.prod(range(1, n, 2))
    rank = sum(math.comb(k, i) for i in range(t+1))
    square = Fraction(rank*(k+2**(2*t)-1), 4*(m-k))
    row = contract(n, k, t, **FLAGS)
    assert row["support_rank_upper_bound_bit_length"] == rank.bit_length()
    assert square <= Fraction(2)**(2*row["trace_distance_upper_bound_power_of_two"])
    sparse = contract(n, k, t, mask_support_size_upper_bound=100, **FLAGS)
    assert sparse["trace_distance_upper_bound_power_of_two"] < row["trace_distance_upper_bound_power_of_two"]
    assert sparse["support_bound_supplied"] and not sparse["mask_support_and_weight_independently_verified"]
    assert len(json.dumps(contract(4096, 4096**2, 1024, **FLAGS))) < 5000


def test_large_budget_and_large_weight_return_vacuous_not_huge_materialization():
    row = contract(8, 10**100, 10**100, **FLAGS)
    assert row["bound_is_vacuous"] and not row["support_rank_evaluated_exactly"]
    row = contract(1024, 10**100, 10**99, **FLAGS)
    assert row["geometric_envelope_available"] and row["bound_is_vacuous"]
    assert not row["support_rank_evaluated_exactly"]


def test_rank_factor_cannot_be_dropped_even_for_valid_schur_channels():
    # Channel-algebra falsifier, not an oracle problem or algorithm candidate.
    a = np.kron(np.eye(2), [[0, 1], [1, 0]])
    c0, c1 = np.eye(4)+a/2, np.eye(4)-a/2
    assert np.linalg.eigvalsh(c0).min() > 0 and np.linalg.eigvalsh(c1).min() > 0
    p = np.full(4, .25)
    delta = (c1-c0)[None, :, :]
    distance = schur_mask_distance(delta, p)
    frobenius = np.linalg.norm((c1-c0)/4)
    assert distance == pytest.approx(.5)
    assert distance > frobenius/2
    assert distance == pytest.approx(math.sqrt(4)*frobenius/2)


def test_radial_parameter_count_is_not_the_physical_output_rank():
    model = physical_selector_schur_channel(3)
    j = model["sources"].index((1, 1, 1))
    output = model["blocks"][0, j]/8  # Uniform pure mask: only four weight parameters.
    assert np.linalg.matrix_rank(output, tol=1e-10) > 4


def test_two_nonempty_sectors_can_be_useless_separately_but_informative_coherently():
    # Two valid phase channels: neither low/high sector bound controls their cross block.
    phase = np.array([1, -1, 1, 1])
    delta = (np.outer(phase, phase)-np.ones((4, 4)))[None, :, :]
    low, high = np.eye(4)[1], np.eye(4)[3]
    assert schur_mask_distance(delta, low) == 0
    assert schur_mask_distance(delta, high) == 0
    assert schur_mask_distance(delta, (low+high)/2) == pytest.approx(1)


@pytest.mark.parametrize("flag", FLAGS)
def test_scope_and_declared_support_assumptions_are_required(flag):
    row = contract(128, 1000, 10, **dict(FLAGS, **{flag: False}))
    assert not row["applicable"] and row["trace_distance_upper_bound_power_of_two"] is None
    with pytest.raises(ValueError):
        contract(128, 1000, 10, **dict(FLAGS, **{flag: 1}))


@pytest.mark.parametrize("n,k,t,size", ((7, 3, 1, None), (9, 3, 1, None), (8, True, 0, None),
    (8, 0, 0, None), (8, 3, True, None), (8, 3, -1, None), (8, 3, 4, None),
    (8, 3, 1, 0), (8, 3, 1, True), (8, 3, 1, 1.5)))
def test_invalid_support_contract_inputs(n, k, t, size):
    with pytest.raises(ValueError):
        contract(n, k, t, mask_support_size_upper_bound=size, **FLAGS)


def test_vacuum_evidence_does_not_resolve_full_low_occupation_lemma(tmp_path, monkeypatch):
    from proof_tracker import _binary_carrier_instrument_lemmas
    monkeypatch.chdir(tmp_path)
    path = tmp_path/"research/representation/coset_binary_carrier_instruments.json"
    path.parent.mkdir(parents=True)
    gate = {"finite_complete_channel_evaluation_verified": True, "vacuum_coherence_gain_bound_derived": True}
    for required in ("source_character_square_bound_verified", "low_occupation_union_controls_verified",
                     "low_occupation_support_bound_derived"):
        path.write_text(json.dumps({"claim_gate": gate}))
        assert _binary_carrier_instrument_lemmas("CODE-COSET-COLLECTIVE")[19].status == "blocked-low-occupation-support-evidence-missing"
        gate[required] = True
    path.write_text(json.dumps({"claim_gate": gate}))
    assert _binary_carrier_instrument_lemmas("CODE-COSET-COLLECTIVE")[19].status == "derived-low-occupation-support-bound-review-pending"
