from fractions import Fraction
import itertools
import math

import numpy as np
import pytest

from coset_mask_tail_fidelity import audit_environment_fidelity, arbitrary_mask_physical_control
from isotypic_instruments import source_selector_mask_tail_information_contract as contract


FLAGS = dict(one_common_subset_query=True, common_group_algebra_unitary=True,
    unitary_and_partition_fixed_before_inputs=True, hidden_prior_uniform_on_involution_class=True,
    no_hidden_correlated_preprocessing_or_side_information=True, source_records_classical=True,
    only_source_records_and_selector_qubits_retained=True, physical_inputs_discarded=True,
    mask_fixed_before_inputs_and_source_records=True)


def test_high_occupation_masks_do_not_pay_uniform_overlap_but_low_weights_remain_unresolved():
    high = contract(4096, 4096**2, None, 3*4096, mask_lower_tail_probability_upper_bound=0, **FLAGS)
    assert high["trace_distance_upper_bound_power_of_two"] == -5373
    assert not high["uniform_mask_overlap_penalty_required"]
    assert high["component_upper_bound_powers_of_two"]["discarded_mask"] is None
    assert high["mask_tail_bound_supplied_not_independently_verified"]
    assert not high["all_arbitrary_masks_obstructed"]
    assert not high["formal_proof_verification"] and not high["novelty_established"]
    leaky = contract(4096, 4096**2, None, 3*4096, mask_lower_tail_probability_upper_bound=Fraction(1, 2**4096), **FLAGS)
    assert leaky["trace_distance_upper_bound_power_of_two"] == -2045
    low = contract(4096, 4096**2, None, 0, mask_lower_tail_probability_upper_bound=0, **FLAGS)
    assert low["bound_is_vacuous"]
    full_leak = contract(4096, 4096**2, None, 3*4096, mask_lower_tail_probability_upper_bound=1, **FLAGS)
    assert full_leak["bound_is_vacuous"]


def test_nonvacuous_fidelity_envelopes_round_outward_without_float_underflow():
    n, k, t, pi = 1024, 1024**2, 3072, Fraction(1, 2**1024)
    row = contract(n, k, None, t, mask_lower_tail_probability_upper_bound=pi, **FLAGS)
    d, m = math.factorial(n), math.prod(range(1, n, 2))
    root = math.isqrt(n*(n-1)//2)
    squares = {"mixture": Fraction(4*k*k*2**(n-1), m), "discarded_mask": 4*pi,
        "bulk_remainder": d*d*Fraction(12, root)**t,
        "endpoint_remainder": 16*d*Fraction(2, root)**t}
    for name, square in squares.items():
        exponent = row["component_upper_bound_powers_of_two"][name]
        assert exponent < 0
        assert square <= Fraction(2)**(2*exponent)
    small = contract(n, 4, None, 0, mask_lower_tail_probability_upper_bound=0, **FLAGS)
    assert small["trace_distance_upper_bound_power_of_two"] == small["raw_copy_upper_bound_power_of_two"] < 0


@pytest.mark.parametrize("flag", FLAGS)
def test_mask_tail_gate_does_not_accept_out_of_scope_assumptions(flag):
    row = contract(16, 100, None, 48, mask_lower_tail_probability_upper_bound=0, **dict(FLAGS, **{flag: False}))
    assert not row["applicable"] and row["trace_distance_upper_bound_power_of_two"] is None
    with pytest.raises(ValueError):
        contract(16, 100, None, 48, mask_lower_tail_probability_upper_bound=0, **dict(FLAGS, **{flag: 1}))


@pytest.mark.parametrize("n,k,r,t,pi", ((7, 3, None, 2, 0), (9, 3, None, 2, 0),
    (16, True, None, 1, 0), (16, 3, False, 2, 0), (16, 3, None, True, 0),
    (16, 3, None, 4, 0), (16, 3, None, -1, 0), (16, 3, None, 2, .5),
    (16, 3, None, 2, True), (16, 3, None, 2, Fraction(-1, 3)), (16, 3, None, 2, 2)))
def test_invalid_tail_contract_inputs_rejected(n, k, r, t, pi):
    with pytest.raises(ValueError):
        contract(n, k, r, t, mask_lower_tail_probability_upper_bound=pi, **FLAGS)


def test_fidelity_controls_cover_singular_grams_rare_sources_and_complex_masks():
    report = audit_environment_fidelity()
    assert report["verified"] and len(report["controls"]) == 12
    for row in report["controls"]:
        assert row["root_fidelity_identity_residual"] < 1e-7
        assert row["source_probabilities"] == pytest.approx([.001, .999])
        for tail in row["tails"]:
            assert tail["bulk_cross_norm"] <= tail["bulk_fidelity_upper_bound"]+1e-8
            assert tail["endpoint_cross_norm"] <= tail["endpoint_fidelity_upper_bound"]+1e-8
    orthogonal = next(row for row in report["controls"] if row["family"] == "orthogonal" and row["mask"] == "low_high_superposition")
    assert orthogonal["tails"][0]["bulk_cross_norm"] == pytest.approx(.3)
    assert orthogonal["tails"][1]["bulk_cross_norm"] == pytest.approx(0)
    assert orthogonal["tails"][1]["lower_tail_mass"] == pytest.approx(.3)
    # Dropping the low-weight mass would falsely predict zero for the full state.
    assert orthogonal["source_averaged_failure"] == 0


def test_source_selected_masks_falsify_fixed_mask_jensen_step():
    from coset_mask_tail_fidelity import _span_failure
    e, v, orthogonal = np.eye(3)
    local = [(e, orthogonal, v), (e, v, v)]
    a = sum(_span_failure(x, z, y) for x, y, z in local)/2
    observed = 0.0
    for sources in itertools.product(range(2), repeat=3):
        active = sources.index(1) if 1 in sources else 0
        observed += abs(np.vdot(local[sources[active]][2], local[sources[active]][1]))/8
    assert a == pytest.approx(.5)
    assert observed == pytest.approx(7/8)
    assert observed > math.sqrt(a)


def test_old_typical_mask_evidence_does_not_resolve_the_new_fidelity_lemma(tmp_path, monkeypatch):
    import json
    from proof_tracker import _binary_carrier_instrument_lemmas
    monkeypatch.chdir(tmp_path)
    path = tmp_path/"research/representation/coset_binary_carrier_instruments.json"
    path.parent.mkdir(parents=True)
    gate = {"finite_complete_channel_evaluation_verified": True, "uniform_mask_polynomial_budget_obstruction_derived": True}
    for required in ("source_weighted_environment_fidelity_verified", "arbitrary_mask_positive_comparison_channel_verified", "mask_tail_fidelity_bound_derived"):
        path.write_text(json.dumps({"claim_gate": gate}))
        assert _binary_carrier_instrument_lemmas("CODE-COSET-COLLECTIVE")[16].status == "blocked-mask-tail-fidelity-evidence-missing"
        gate[required] = True
    path.write_text(json.dumps({"claim_gate": gate}))
    assert _binary_carrier_instrument_lemmas("CODE-COSET-COLLECTIVE")[16].status == "derived-mask-tail-fidelity-bound-review-pending"


@pytest.mark.parametrize("copies", (2, 3))
@pytest.mark.parametrize("mask", ("high_asymmetric", "complex_full", "low_high_superposition"))
def test_arbitrary_mask_comparison_is_a_channel_image_but_not_the_actual_output(copies, mask):
    row = arbitrary_mask_physical_control(copies, mask)
    assert row["verified"] and max(row["residuals"].values()) < 1e-8
    assert row["ordered_source_tuples_evaluated"] == 3**copies
    assert row["hidden_members_evaluated"] == 3
    assert not row["source_multiset_compression_used"]
    assert all(a <= b+1e-9 for a, b in zip(row["positive_comparison_trace_distances"], row["walsh_comparison_trace_distances"]))
    assert max(abs(a-b) for a, b in zip(row["individual_trace_distances"], row["positive_comparison_trace_distances"])) > 1e-4
