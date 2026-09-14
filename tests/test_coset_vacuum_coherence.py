from fractions import Fraction
import json
import math

import pytest

from coset_vacuum_coherence import audit_source_character_squares, audit_vacuum_coherence, vacuum_coherence_scaling_controls
from isotypic_instruments import source_selector_vacuum_coherence_contract as contract


FLAGS = dict(one_common_subset_query=True, common_group_algebra_unitary=True,
    unitary_and_partition_fixed_before_inputs=True, hidden_prior_uniform_on_involution_class=True,
    no_hidden_correlated_preprocessing_or_side_information=True, source_records_classical=True,
    source_partition_is_irrep_coarsening=True, only_source_records_and_selector_qubits_retained=True,
    physical_inputs_discarded=True, mask_fixed_before_inputs_and_source_records=True)


def test_character_square_bound_has_no_category_penalty_and_is_exact_for_full_irreps():
    report = audit_source_character_squares()
    assert report["verified"] and report["exact_arithmetic"] and len(report["controls"]) == 9
    for row in report["controls"]:
        value, bound = Fraction(row["source_chi_square"]), Fraction(row["source_chi_square_upper_bound"])
        assert value <= bound == Fraction(1, row["class_size"])
        assert row["group_elements_checked"] == math.factorial(row["degree"])
        if row["partition_rule"] == "full_irreps":
            assert value == bound
        if row["partition_rule"] == "all_irreps_merged":
            assert value == 0


def test_actual_physical_columns_compression_and_all_four_coefficient_bounds():
    report = audit_vacuum_coherence()
    assert report["verified"] and not report["nonempty_mask_information_obstructed"]
    for row in report["controls"]:
        assert row["source_tuple_count"] == 3**row["copy_count"]
        assert row["hidden_members_checked"] == 3
        assert row["character_reconstruction_residual"] < 1e-8
        assert row["class_invariant_source_mass_residual"] < 1e-8
        assert len(row["rows"]) == 2**row["copy_count"]-1
        for subset in row["rows"]:
            assert subset["weighted_row_squared_norm"] <= subset["compressed_input_chi_square_upper_bound"]+1e-9
            for name, value in subset["coefficient_component_norms"].items():
                assert value <= subset["coefficient_component_upper_bounds"][name]+1e-9
        for probe in row["probes"]:
            assert -1e-9 <= probe["vacuum_coherence_gain"] <= probe["cross_block_half_trace_norm"]+1e-9
            assert probe["cross_block_half_trace_norm"] <= probe["source_weighted_jensen_upper_bound"]+1e-9
        assert max(p["vacuum_coherence_gain"] for p in row["probes"]) > .01
        vacuum = next(p for p in row["probes"] if p["vacuum_probability"] == 1)
        assert vacuum["vacuum_coherence_gain"] == pytest.approx(0)
        assert vacuum["total_distance"] > .3  # A zero GAIN is not a zero total signal.


def test_polynomial_budget_gain_certificates_do_not_assert_total_information_failure():
    controls = vacuum_coherence_scaling_controls()
    assert [r["vacuum_coherence_gain_upper_bound_power_of_two"] for r in controls] == [-3, -115, -1679, -8763]
    for row in controls:
        assert row["low_weight_prefix_end"] == row["degree"]
        assert row["high_weight_suffix_start"] == row["degree"]+1
        assert not row["total_trace_distance_bounded_by_gain"]
        assert not row["nonempty_mask_information_obstructed"]
        assert not row["all_arbitrary_masks_obstructed"]
        assert not row["formal_proof_verification"] and not row["independent_review"]
    # Huge budgets do not enter exponents or require a per-weight sweep.
    huge = contract(1024, 10**100, **FLAGS)
    assert huge["geometric_envelope_available"]
    assert huge["vacuum_coherence_gain_upper_bound_power_of_two"] < 0
    assert len(json.dumps(huge)) < 5000


def test_integer_envelopes_round_outwards_and_split_every_nonempty_weight():
    n, k, w = 128, 128**2, Fraction(1, 3)
    row = contract(n, k, vacuum_probability=w, **FLAGS)
    d, m, l = math.factorial(n), math.prod(range(1, n, 2)), n*(n-1)//2
    e, factor = Fraction(m, m-k), w*(1-w)
    low_square = factor*(e-1+e*Fraction(2**n-1, m))
    assert low_square <= Fraction(2)**(2*row["low_weight_gain_upper_bound_power_of_two"])
    squares = {"source_mass": factor*(e-1), "hidden_endpoint": factor*e/m,
        "alternative_off_subgroup": factor*d*e*Fraction(4, l)**(n+1),
        "null_off_identity": factor*d*Fraction(1, l)**(n+1)}
    for name, square in squares.items():
        exponent = row["high_weight_gain_component_upper_bound_powers_of_two"][name]
        assert exponent < 0 and square <= Fraction(2)**(2*exponent)
    for copies in (1, n-1, n, n+1):
        item = contract(n, copies, **FLAGS)
        assert item["low_weight_prefix_end"] == min(n, copies)
        assert item["high_weight_suffix_start"] == (n+1 if copies > n else None)


def test_vacuous_geometric_envelope_and_zero_coherence_are_distinct():
    assert not contract(8, 105, **FLAGS)["geometric_envelope_available"]
    assert contract(8, 105, **FLAGS)["gain_bound_is_vacuous"]
    for w in (0, 1):
        row = contract(8, 105, vacuum_probability=w, **FLAGS)
        assert row["gain_is_exactly_zero"] and row["vacuum_coherence_gain_upper_bound_power_of_two"] is None
        assert not row["gain_bound_is_vacuous"]


@pytest.mark.parametrize("flag", FLAGS)
def test_out_of_scope_or_implicit_architecture_assumptions_are_not_certified(flag):
    row = contract(128, 1000, **dict(FLAGS, **{flag: False}))
    assert not row["applicable"] and row["vacuum_coherence_gain_upper_bound_power_of_two"] is None
    with pytest.raises(ValueError):
        contract(128, 1000, **dict(FLAGS, **{flag: 1}))


@pytest.mark.parametrize("n,k,w", ((7, 3, None), (9, 3, None), (8, True, None),
    (8, 0, None), (8, 1, .5), (8, 1, True), (8, 1, -1), (8, 1, 2)))
def test_invalid_parameters(n, k, w):
    with pytest.raises(ValueError):
        contract(n, k, vacuum_probability=w, **FLAGS)


def test_symmetry_evidence_alone_does_not_resolve_vacuum_coherence_lemma(tmp_path, monkeypatch):
    from proof_tracker import _binary_carrier_instrument_lemmas
    monkeypatch.chdir(tmp_path)
    path = tmp_path/"research/representation/coset_binary_carrier_instruments.json"
    path.parent.mkdir(parents=True)
    gate = {"finite_complete_channel_evaluation_verified": True, "selector_mask_radial_reduction_derived": True}
    for required in ("source_character_square_bound_verified", "vacuum_coherence_physical_controls_verified",
                     "vacuum_coherence_gain_bound_derived"):
        path.write_text(json.dumps({"claim_gate": gate}))
        assert _binary_carrier_instrument_lemmas("CODE-COSET-COLLECTIVE")[18].status == "blocked-vacuum-coherence-evidence-missing"
        gate[required] = True
    path.write_text(json.dumps({"claim_gate": gate}))
    assert _binary_carrier_instrument_lemmas("CODE-COSET-COLLECTIVE")[18].status == "derived-vacuum-coherence-bound-review-pending"
