from fractions import Fraction
import math

import numpy as np
import pytest

from isotypic_instruments import source_selector_quantum_information_contract
from coset_source_selector_quantum import source_selector_quantum_mixture_control, _prepend_tensor


FLAGS = dict(one_common_subset_query=True, common_group_algebra_unitary=True,
    unitary_and_partition_fixed_before_inputs=True, hidden_prior_uniform_on_involution_class=True,
    no_hidden_correlated_preprocessing_or_side_information=True,
    source_records_classical=True,
    only_source_records_and_selector_qubits_retained=True, physical_inputs_discarded=True,
    mask_filter_diagonal_and_fixed_before_input=True, mask_filter_is_a_contraction=True)


def test_quantum_bound_covers_any_selector_readout_but_not_coherent_source_registers():
    full = source_selector_quantum_information_contract(1024, 17528, None, **FLAGS)
    assert full["trace_distance_upper_bound_power_of_two"] == -1662
    assert full["covers_arbitrary_final_selector_povm"]
    assert full["covers_complex_common_central_phases"]
    assert full["covers_noncentral_common_group_algebra_unitaries"]
    assert not full["pointwise_hidden_bound_for_noncentral_unitary"]
    assert not full["raw_copy_bound_applies_to_average_individual_distance"]
    assert not full["covers_coherent_source_or_retained_physical_registers"]
    assert not full["all_copy_counts_obstructed"]
    assert not full["copy_count_is_available_resource_budget"]
    assert not full["novelty_established"]
    assert not full["is_classical_dequantization"]
    intermediate = source_selector_quantum_information_contract(1024, 8764, None, **FLAGS)
    assert intermediate["unpruned_uniform_upper_bound_power_of_two"] == 0
    assert intermediate["trace_distance_upper_bound_power_of_two"] == -544
    for flag in FLAGS:
        row = source_selector_quantum_information_contract(128, 1428, None, **dict(FLAGS, **{flag: False}))
        assert not row["applicable"] and row["trace_distance_upper_bound_power_of_two"] is None
        with pytest.raises(ValueError):
            source_selector_quantum_information_contract(128, 1428, None, **dict(FLAGS, **{flag: 1}))


def test_mask_filter_probability_is_charged_without_weakening_the_raw_copy_bound():
    filtered = source_selector_quantum_information_contract(1024, 17528, None,
        hypothesis_independent_filter_success_lower_bound=Fraction(1, 17529), **FLAGS)
    assert filtered["trace_distance_upper_bound_power_of_two"] == -1647
    assert filtered["filter_information_penalty_charged"] == "17529"
    assert not filtered["comparison_filter_is_required_physical_preparation"]
    small = source_selector_quantum_information_contract(1024, 2191, None,
        hypothesis_independent_filter_success_lower_bound=Fraction(1, 2**2191), **FLAGS)
    assert small["trace_distance_upper_bound_power_of_two"] == -1096
    assert small["filtered_quantum_upper_bound_power_of_two"] == 0
    for bad in (0, -1, True, .5, "1/2", Fraction(3, 2)):
        with pytest.raises(ValueError):
            source_selector_quantum_information_contract(128, 1428, None,
                hypothesis_independent_filter_success_lower_bound=bad, **FLAGS)


def test_quantum_endpoint_and_filter_bounds_round_outward_exactly():
    for n, k in ((16, 80), (64, 588), (128, 1428)):
        p = Fraction(1, k+1)
        row = source_selector_quantum_information_contract(n, k, None,
            hypothesis_independent_filter_success_lower_bound=p, **FLAGS)
        d, m = math.factorial(n), math.prod(range(1, n, 2))
        squared = {
            "mixture": Fraction(4*k*k*2**(n-1), m),
            "bulk_remainder": d*d*Fraction(row["bulk_trace_norm_radius_upper_bound"])**(2*k),
            "endpoint_remainder": 16*d*Fraction(row["endpoint_trace_norm_radius_squared_upper_bound"])**k,
        }
        for term, value in squared.items():
            assert min(1, value) <= Fraction(2)**(2*row["uniform_component_upper_bound_powers_of_two"][term])
        assert min(1, Fraction(2)**row["uniform_quantum_upper_bound_power_of_two"]/p) <= Fraction(2)**row["filtered_quantum_upper_bound_power_of_two"]


@pytest.mark.parametrize("n,k,r", ((4, 2, None), (9, 3, 2), (8, True, 2), (8, 0, 2), (8, 2, False), (8, 2, 0)))
def test_invalid_quantum_contract_inputs_are_rejected(n, k, r):
    with pytest.raises(ValueError):
        source_selector_quantum_information_contract(n, k, r, **FLAGS)


def test_tensor_prepend_uses_the_existing_little_endian_mask_convention():
    first = np.array([[1, 2j], [-2j, 3]])
    second = np.array([[4, 5], [5, 6]])
    tensor = _prepend_tensor(first[None], second[None])[0]
    assert np.array_equal(tensor, np.kron(second, first))
    assert not np.array_equal(tensor, np.kron(first, second))


@pytest.mark.parametrize("n,t,k", ((3, 1, 1), (3, 1, 2), (3, 1, 3), (3, 1, 4), (4, 2, 1), (4, 2, 2), (4, 2, 3)))
@pytest.mark.parametrize("phase", ("negative_character_reflection", "zero_character_reflection", "character_ratio_rotation"))
def test_full_selector_mixture_and_filtered_states_match_the_physical_model(n, t, k, phase):
    row = source_selector_quantum_mixture_control(n, t, k, phase)
    assert row["verified"] and max(row["residuals"].values()) < 1e-9
    assert row["selector_quantum_trace_distance"]+1e-10 >= row["walsh_trace_distance"]
    assert row["ordered_source_blocks_represented"] == (3 if n == 3 else 5)**k
    assert not row["optimal_quantum_povm_is_compiled"]
    assert not row["formal_proof_verification"]
    for filter_row in row["fixed_weight_filter_controls"]:
        m = filter_row["mask_weight"]
        assert Fraction(filter_row["comparison_success_probability"]) == Fraction(math.comb(k, m), 2**k)
        assert filter_row["selector_quantum_trace_distance"] <= filter_row["charged_uniform_distance_upper_bound"]+1e-9


def test_quantum_coherences_and_endpoint_radius_are_not_replaced_by_walsh_statistics():
    row = source_selector_quantum_mixture_control(4, 2, 3, "character_ratio_rotation")
    assert row["selector_quantum_trace_distance"] == pytest.approx(.5182626573525845)
    assert row["walsh_trace_distance"] == pytest.approx(.4435941033289708)
    assert all(not r["walsh_endpoint_half_radius_is_valid_here"] for r in row["kernel_radius_controls"])
    assert all(r["minimum_endpoint_trace_norm_radius"] > .5 for r in row["kernel_radius_controls"])
    assert row["kernel_radius_controls"][1]["maximum_endpoint_trace_norm_radius"] == pytest.approx(1)
    assert any(value > .1 for value in row["remainder_trace_distances"])


def test_zero_source_mass_is_retained_without_dividing_by_zero():
    row = source_selector_quantum_mixture_control(3, 1, 3, "character_ratio_rotation")
    assert row["zero_mass_source_blocks_retained"] > 0
    assert row["residuals"]["natural_source_mass"] < 1e-10


def test_unmeasured_irrep_copy_is_already_classical_only_under_the_stated_input_model():
    from coset_source_selector_quantum import audit_unmeasured_source_labels
    audit = audit_unmeasured_source_labels()
    assert audit["verified"]
    assert not audit["covers_retaining_nontrivial_physical_carrier_registers"]
    for row in audit["controls"]:
        assert row["maximum_standard_input_dephasing_distance"] < 1e-10
        assert row["nonstandard_cross_irrep_pure_input_dephasing_distance"] == pytest.approx(.5)
        assert not row["coherent_label_copy_alone_adds_a_resource"]


@pytest.mark.parametrize("n,k", ((3, 1), (3, 2), (3, 3), (4, 1), (4, 2)))
@pytest.mark.parametrize("rule", ("pointed_involution", "ordered_rotations"))
@pytest.mark.parametrize("retain", (False, True))
def test_noncentral_unitaries_match_every_shared_hidden_physical_channel(n, k, rule, retain):
    from coset_source_selector_quantum import noncentral_group_algebra_control
    row = noncentral_group_algebra_control(n, k, rule, retain)
    assert row["verified"] and max(row["residuals"].values()) < 1e-9
    assert row["noncentrality_commutator_norm"] > .1
    assert row["hidden_members_evaluated"] == 3
    assert row["maximum_class_average_mixed_overlap_violation"] < 1e-10
    assert row["hidden_average_taken_after_tensor_products"]
    assert not row["one_representative_used_without_covariance"]
    assert row["class_average_decision_trace_distance"] <= row["average_individual_trace_distance"]+1e-10
    assert not row["raw_copy_bound_applies_to_average_individual_distance"]
    for control in row["typical_mask_projection_controls"]:
        assert control["verified"]
        assert control["actual_discarded_masses"] == pytest.approx([float(Fraction(control["discarded_uniform_mask_mass"]))]*4)
        assert all(a <= b+1e-10 for a, b in zip(control["projected_remainder_distances"], control["kernel_tail_upper_bounds"]))
    if k == 1:
        assert row["same_hidden_vs_independent_hidden_trace_distance"] < 1e-10


def test_pointed_noncentral_operation_falsifies_representative_and_independent_hidden_shortcuts():
    from coset_source_selector_quantum import noncentral_group_algebra_control
    row = noncentral_group_algebra_control(4, 2, "pointed_involution", False)
    assert row["individual_trace_distances"] == pytest.approx([.75, 0, 0])
    assert row["class_average_decision_trace_distance"] == pytest.approx(.25)
    assert row["maximum_pointwise_mixed_overlap_violation"] == pytest.approx(2/3)
    assert row["independent_hidden_per_copy_decision_distance"] == pytest.approx(7/36)
    assert row["same_hidden_vs_independent_hidden_trace_distance"] == pytest.approx(1/9)


def test_trace_norm_is_not_interchanged_with_hidden_averaging():
    from coset_source_selector_quantum import noncentral_group_algebra_control
    row = noncentral_group_algebra_control(3, 2, "ordered_rotations", True)
    assert row["class_average_decision_trace_distance"] == pytest.approx(.40027632114505074)
    assert row["average_individual_trace_distance"] == pytest.approx(.4368805501457462)


def test_raw_copy_cap_is_falsified_by_individual_inputs_but_bounds_the_averaged_input():
    from coset_binary_carrier_instruments import _source_parity_group_data
    data = _source_parity_group_data(3, 1)
    order = len(data[0])
    actions = np.eye(order)[data[7]]
    null = np.eye(order)/order
    alternatives = [(np.eye(order)+actions[indices[0]])/order for indices in data[8]]
    individual = [np.abs(np.linalg.eigvalsh(state-null)).sum()/2 for state in alternatives]
    decision = np.abs(np.linalg.eigvalsh(np.mean(alternatives, axis=0)-null)).sum()/2
    raw_bound = .5/math.sqrt(len(alternatives))
    assert individual == pytest.approx([.5]*len(alternatives))
    assert np.mean(individual) > raw_bound
    assert decision <= raw_bound
    assert decision == pytest.approx(1/6)


@pytest.mark.parametrize("args", ((3, True, "pointed_involution", True), (4, 3, "ordered_rotations", True),
    (3, 2, "unknown", True), (3, 2, "pointed_involution", 1)))
def test_invalid_noncentral_controls_are_rejected(args):
    from coset_source_selector_quantum import noncentral_group_algebra_control
    with pytest.raises(ValueError):
        noncentral_group_algebra_control(*args)


def test_stale_central_only_evidence_does_not_resolve_the_noncentral_lemma(tmp_path, monkeypatch):
    import json
    from proof_tracker import _binary_carrier_instrument_lemmas
    monkeypatch.chdir(tmp_path)
    path = tmp_path/"research/representation/coset_binary_carrier_instruments.json"
    path.parent.mkdir(parents=True)
    gate = {"finite_complete_channel_evaluation_verified": True,
        "source_selector_quantum_mixtures_verified": True,
        "source_selector_quantum_large_copy_bound_derived": True}
    path.write_text(json.dumps({"claim_gate": gate}))
    lemma = _binary_carrier_instrument_lemmas("CODE-COSET-COLLECTIVE")[15]
    assert lemma.status == "blocked-source-selector-quantum-evidence-missing"
    assert lemma.depends_on == ["PO-INPUT-MODEL", "PO-MEASUREMENT", "PO-SUCCESS"]
    gate["noncentral_group_algebra_controls_verified"] = True
    path.write_text(json.dumps({"claim_gate": gate}))
    lemma = _binary_carrier_instrument_lemmas("CODE-COSET-COLLECTIVE")[15]
    assert lemma.status == "blocked-source-selector-quantum-evidence-missing"
    gate["typical_mask_projection_controls_verified"] = True
    gate["uniform_mask_polynomial_budget_obstruction_derived"] = True
    path.write_text(json.dumps({"claim_gate": gate}))
    lemma = _binary_carrier_instrument_lemmas("CODE-COSET-COLLECTIVE")[15]
    assert lemma.status == "derived-source-selector-quantum-bound-review-pending"
    assert "review-pending" in lemma.status


@pytest.mark.parametrize("orientation", ("bulk", "left_endpoint", "right_endpoint"))
def test_typical_projection_removes_low_support_tensor_terms_on_both_sides(orientation):
    from coset_source_selector_quantum import _typical_mask_tensor_tail
    b = np.array([[.5, 0], [0, 0]])
    e = np.array([[0, .03], [.03, .03]])
    if orientation != "bulk":
        b = np.array([[.5, .5], [0, 0]])
        e = np.array([[0, 0], [.03, .03]])
        if orientation == "right_endpoint":
            b, e = b.T, e.T
    k, t = 6, 3
    full = baseline = np.ones((1, 1))
    for _ in range(k):
        full, baseline = np.kron(b+e, full), np.kron(b, baseline)
    retained = [s for s in range(2**k) if s.bit_count() >= t]
    norm = lambda matrix: np.linalg.svd(matrix, compute_uv=False).sum()
    projected = norm(full[np.ix_(retained, retained)])
    tail = _typical_mask_tensor_tail(norm(b), norm(e), k, t)
    assert projected <= tail+1e-12
    assert tail < .1*norm(full)
    assert norm(baseline[np.ix_(retained, retained)]) == 0
    if orientation == "right_endpoint":
        assert norm(baseline[retained, :]) > 0


def test_physical_kernel_decomposition_has_the_required_zero_pinning_orientation():
    from coset_binary_carrier_instruments import _source_parity_group_data
    from coset_source_selector_quantum import _typical_mask_kernel_decomposition
    data = _source_parity_group_data(3, 1)
    d, products = len(data[0]), data[7]
    actions = np.eye(d)[products]
    projectors = (data[3][:, None]*data[2]/d)[:, products]
    h = data[8][0][0]
    subgroup = np.zeros(d, dtype=bool)
    subgroup[[0, h]] = True
    sigma = projectors @ ((np.eye(d)+actions[h])/d)
    kernels = np.zeros((len(projectors), d*d, 2, 2))
    for u in range(d):
        for v in range(d):
            for j, state in enumerate(sigma):
                kernels[j, u*d+v] = [[np.trace(state), np.trace(state @ actions[u].T)],
                    [np.trace(state @ actions[v]), np.trace(state @ actions[u].T @ actions[v])]]
    kernels /= 2
    base, remainder, radii, epsilons, off = _typical_mask_kernel_decomposition(kernels, subgroup, products)
    assert np.allclose(base+remainder, kernels)
    for index in np.flatnonzero(off):
        u, v = divmod(index, d)
        if subgroup[u]:
            assert np.all(base[:, index, 1, :] == 0)
            assert np.allclose(base[:, index, 0, 0], base[:, index, 0, 1])
        elif subgroup[v]:
            assert np.all(base[:, index, :, 1] == 0)
            assert np.allclose(base[:, index, 0, 0], base[:, index, 1, 0])
        else:
            assert np.count_nonzero(base[:, index, 1, :]) == np.count_nonzero(base[:, index, :, 1]) == 0
        assert radii[index] == pytest.approx(1/math.sqrt(2) if subgroup[u] or subgroup[v] else .5)
        assert epsilons[index] >= 0


def test_all_budget_certificate_covers_variable_participation_without_sweeping_the_budget():
    from isotypic_instruments import source_selector_polynomial_budget_contract as budget
    row = budget(4096, 4096**2, None, **FLAGS)
    assert row["all_participating_counts_through_budget_covered"]
    assert row["raw_copy_prefix_end"] == 20480
    assert row["typical_mask_suffix_start"] == 20481
    assert row["trace_distance_upper_bound_power_of_two"] == -571
    assert not row["covers_exponential_copy_budgets_asymptotically"]
    assert not row["covers_arbitrary_masks"] and not row["formal_proof_verification"]
    masked = budget(8192, 8192**2, None,
        filter_success_lower_bound_uniform_over_copy_counts=Fraction(1, 8192**2+1), **FLAGS)
    assert masked["trace_distance_upper_bound_power_of_two"] == -2530
    assert budget(1024, 1024**2, None, **FLAGS)["bound_is_vacuous"]
    enormous = budget(16, 2**1000, None, **FLAGS)
    assert enormous["raw_copy_prefix_end"] == 80 and enormous["bound_is_vacuous"]
    for flag in FLAGS:
        excluded = budget(16, 100, None, **dict(FLAGS, **{flag: False}))
        assert not excluded["applicable"] and excluded["trace_distance_upper_bound_power_of_two"] is None


def test_typical_mask_integer_envelopes_cover_every_copy_residue():
    from isotypic_instruments import _typical_mask_component_exponents, source_selector_polynomial_budget_contract
    n, start, limit = 16, 81, 120
    d, m, r = math.factorial(n), math.prod(range(1, n, 2)), 2**(n-1)
    root = math.isqrt(n*(n-1)//2)
    row = source_selector_polynomial_budget_contract(n, limit, None, **FLAGS)
    envelope = _typical_mask_component_exponents(d, m, r, root, start, limit)
    for k in range(start, limit+1):
        t = k//4
        squares = {"bulk_remainder": Fraction(d*d*6**(2*t), root**(2*t)),
            "endpoint_remainder": Fraction(16*d*2**k*2**(2*t), root**(2*t)),
            "mixture": Fraction(4*k*k*r, m)}
        for name, value in squares.items():
            assert min(1, value) <= Fraction(2)**(2*envelope[name])
        discard = Fraction(sum(math.comb(k, w) for w in range(t)), 2**k)
        assert min(1, 4*discard) <= Fraction(2)**(2*envelope["discarded_mask"])
    short = source_selector_polynomial_budget_contract(16, 3, None, **FLAGS)
    assert short["typical_mask_suffix_start"] is None
    assert short["trace_distance_upper_bound_power_of_two"] == short["raw_prefix_upper_bound_power_of_two"]
    assert row["suffix_component_upper_bound_powers_of_two"] == envelope


@pytest.mark.parametrize("n,budget,p", ((8, 100, Fraction(1)), (16, True, Fraction(1)),
    (16, 0, Fraction(1)), (16, 10, .5), (16, 10, Fraction(0)), (16, 10, Fraction(2))))
def test_budget_contract_rejects_invalid_degrees_counts_and_filter_bounds(n, budget, p):
    from isotypic_instruments import source_selector_polynomial_budget_contract
    with pytest.raises(ValueError):
        source_selector_polynomial_budget_contract(n, budget, None,
            filter_success_lower_bound_uniform_over_copy_counts=p, **FLAGS)
