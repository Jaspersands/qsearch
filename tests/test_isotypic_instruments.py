import math
from fractions import Fraction

import numpy as np
import pytest

from isotypic_instruments import (
    finite_isotypic_instrument, isotypic_label_resource_contract,
    subset_incidence_cells, fixed_palette_information_contract,
    regular_algebra_state_lift, source_conditioned_palette_information_contract,
    _sqrt_ratio_dyadic_exponent,
    adaptive_palette_catalogue_information_contract,
)
from representation_obstruction import integer_partitions
from self_dual_wreath_physical_frame_blocks import permutation_representation_matrices


def symmetric_pair_data():
    irreps = {lam: dict(permutation_representation_matrices(lam)) for lam in integer_partitions(3)}
    group = tuple(irreps[(2, 1)])
    actions = [np.kron(irreps[(2, 1)][g], irreps[(2, 1)][g]) for g in group]
    return actions, {lam: [table[g] for g in group] for lam, table in irreps.items()}


def test_full_compute_measure_uncompute_unitary_has_no_dirty_workspace():
    actions, irreps = symmetric_pair_data()
    instrument = finite_isotypic_instrument(actions, irreps)
    order, dimension = len(actions), len(actions[0])
    uniform, origin = np.ones(order) / math.sqrt(order), np.eye(order)[:, 0]
    direction = (origin - uniform) / np.linalg.norm(origin - uniform)
    preparation = np.eye(order) - 2 * np.outer(direction, direction)
    fourier = np.array([math.sqrt(len(table[0]) / order) * np.array([a[i, j].conjugate() for a in table])
                       for table in irreps.values() for i in range(len(table[0])) for j in range(len(table[0]))])
    controlled = sum((np.kron(np.diag(np.eye(order)[index]), action) for index, action in enumerate(actions)),
                     np.zeros((order * dimension, order * dimension), dtype=complex))
    compute = np.kron(fourier, np.eye(dimension)) @ controlled @ np.kron(preparation, np.eye(dimension))
    append_zero = np.kron(origin[:, None], np.eye(dimension))
    assert np.linalg.norm(compute.conj().T @ compute - np.eye(order * dimension)) < 1e-12
    offset = 0
    for label, table in irreps.items():
        width = len(table[0])**2
        mask = np.zeros(order)
        mask[offset:offset + width] = 1
        recovered = compute.conj().T @ np.kron(np.diag(mask), np.eye(dimension)) @ compute @ append_zero
        expected = append_zero @ instrument.projectors[label]
        assert np.linalg.norm(recovered - expected) < 1e-12
        # Operator equality checks every matrix unit and entangled extension,
        # not merely a few diagonal input states.
        offset += width
    assert max(instrument.residuals.values()) < 1e-12


def test_discarded_reference_channel_equals_group_twirl_on_every_matrix_unit():
    actions, irreps = symmetric_pair_data()
    instrument = finite_isotypic_instrument(actions, irreps)
    for row in range(4):
        for column in range(4):
            unit = np.zeros((4, 4), dtype=complex)
            unit[row, column] = 1
            discarded = sum(instrument.discard_reference(label, unit) for label in instrument.labels)
            twirled = sum(action @ unit @ action.conj().T for action in actions) / len(actions)
            assert np.linalg.norm(discarded - twirled) < 1e-12
            for label in instrument.labels:
                assert np.trace(instrument.discard_reference(label, unit)) == pytest.approx(
                    np.trace(instrument.clean_label(label, unit)), abs=1e-12)


def test_naive_discard_erases_carrier_entanglement_even_when_the_label_is_certain():
    _, irreps = symmetric_pair_data()
    actions = [np.kron(action, np.eye(2)) for action in irreps[(2, 1)]]
    instrument = finite_isotypic_instrument(actions, irreps)
    vector = np.array([1, 0, 0, 1]) / math.sqrt(2)
    state = np.outer(vector, vector)
    assert np.linalg.norm(instrument.clean_label((2, 1), state) - state) < 1e-12
    discarded = instrument.discard_reference((2, 1), state)
    assert np.linalg.norm(discarded - np.eye(4) / 4) < 1e-12
    assert np.abs(np.linalg.eigvalsh(discarded - state)).sum() / 2 == pytest.approx(0.75)


def test_complex_characters_use_the_correct_conjugate_label_convention():
    omega = np.exp(2j * np.pi / 3)
    irreps = {frequency: [np.array([[omega**(frequency * g)]]) for g in range(3)] for frequency in range(3)}
    actions = [np.diag([omega**(frequency * g) for frequency in range(3)]) for g in range(3)]
    instrument = finite_isotypic_instrument(actions, irreps)
    for frequency in range(3):
        assert np.linalg.norm(instrument.projectors[frequency] - np.diag(np.eye(3)[frequency])) < 1e-12


def test_incompatible_fourier_or_action_contract_fails_closed():
    actions, irreps = symmetric_pair_data()
    with pytest.raises(ValueError, match="complete irreps"):
        finite_isotypic_instrument(actions, {(2, 1): irreps[(2, 1)]})
    broken = [action.copy().astype(complex) for action in actions]
    broken[1] *= np.exp(0.37j)
    with pytest.raises(ValueError, match="incompatible"):
        finite_isotypic_instrument(broken, irreps)
    broken[0][0, 0] = np.nan
    with pytest.raises(ValueError, match="finite square"):
        finite_isotypic_instrument(broken, irreps)


@pytest.mark.parametrize("args", [(1, 2), (4, 0), (True, 1), (4, 2, -1), (4, 2, 1, float('nan'))])
def test_invalid_resource_contracts_are_rejected(args):
    with pytest.raises(ValueError):
        isotypic_label_resource_contract(*args)


def test_uniform_resource_contract_does_not_hide_postselection_or_multiplicity_resolution():
    contract = isotypic_label_resource_contract(128, 128**2, 128, 1e-6)
    assert contract["group_qft_or_inverse_calls"] == 256
    assert contract["controlled_single_copy_group_action_or_inverse_calls"] == 2 * 128**3
    assert contract["reference_register_qubits"] < 128 * 7
    assert contract["composed_channel_diamond_distance_upper_bound"] == pytest.approx(0.000512)
    assert contract["uniform_reduction_to_known_primitives"]
    assert not contract["postselection_required"]
    assert not contract["multiplicity_basis_transform_supplied"]
    assert not contract["gate_level_sn_qft_backend_supplied_here"]


def test_fixed_subset_palette_counts_effective_cells_not_raw_copies():
    palette = ((0, 1, 4, 5), (2, 3, 4, 5))
    assert subset_incidence_cells(8, palette) == ((0, 1), (2, 3), (4, 5))
    row = fixed_palette_information_contract(105, 8, palette, operations_and_readout_in_palette_algebra=True)
    assert row["effective_cell_count"] == 3
    assert Fraction(row["trace_distance_squared_upper_bound"]) == Fraction(7, 420)
    assert row["exact_output_simulation_by_cell_count_coset_copies"]
    assert not row["is_classical_dequantization"]


def test_individual_source_labels_refine_cells_and_unlisted_readouts_fail_closed():
    palette = (tuple(range(100)),)
    collapsed = fixed_palette_information_contract(105, 100, palette, operations_and_readout_in_palette_algebra=True)
    source_labels = fixed_palette_information_contract(105, 100, palette,
        individual_source_labels=True, operations_and_readout_in_palette_algebra=True)
    assert collapsed["effective_cell_count"] == 1
    assert source_labels["effective_cell_count"] == 100
    assert Fraction(source_labels["trace_distance_squared_upper_bound"]) == 1
    outside = fixed_palette_information_contract(105, 100, palette, operations_and_readout_in_palette_algebra=False)
    assert not outside["applicable"]
    assert outside["trace_distance_squared_upper_bound"] is None
    assert not outside["exact_output_simulation_by_cell_count_coset_copies"]
    with pytest.raises(ValueError):
        fixed_palette_information_contract(105, 100, palette, operations_and_readout_in_palette_algebra="false")


def test_no_subset_access_gives_no_observation_and_duplicate_queries_give_no_new_cells():
    assert subset_incidence_cells(8, ()) == ()
    assert subset_incidence_cells(8, ((0, 1), (0, 1))) == ((0, 1),)
    for count, palette in ((0, ()), (2, ((2,),)), (2, ((0, 0),)), (2, ((True,),))):
        with pytest.raises(ValueError):
            subset_incidence_cells(count, palette)


def test_regular_lift_keeps_complex_moments_and_rejects_nonpositive_functionals():
    omega = np.exp(2j * np.pi / 3)
    actions = [np.diag([omega**(frequency * g) for frequency in range(3)]) for g in range(3)]
    state = regular_algebra_state_lift([omega**g for g in range(3)], actions)
    assert np.linalg.norm(state - np.diag([0, 1, 0])) < 1e-12
    with pytest.raises(ValueError, match="positive"):
        regular_algebra_state_lift([1, 2, 2], actions)
    with pytest.raises(ValueError, match="orthogonal"):
        regular_algebra_state_lift([1, 1, 1], [np.eye(3)] * 3)
    for values in ([], [1, float("nan"), 1], [[1, 1, 1]]):
        with pytest.raises(ValueError, match="finite"):
            regular_algebra_state_lift(values, actions)


def test_dyadic_rounding_is_outward_at_boundaries_and_never_underflows():
    assert _sqrt_ratio_dyadic_exponent(0, 7) is None
    for exponent in (-10001, -128, -3, -2, -1, 0, 1, 5):
        exact = Fraction(2)**exponent
        for value in (exact, exact * Fraction(1000, 1001), exact * Fraction(1001, 1000)):
            result = _sqrt_ratio_dyadic_exponent(value.numerator, value.denominator)
            assert Fraction(2)**(2 * result) >= min(1, value)
    for numerator in range(1, 48):
        for denominator in range(1, 48):
            b = _sqrt_ratio_dyadic_exponent(numerator, denominator)
            assert Fraction(2)**(2 * b) >= min(1, Fraction(numerator, denominator))
    assert _sqrt_ratio_dyadic_exponent(1, 2**20000) == -10000


def test_source_labels_are_charged_without_claiming_exact_compression():
    row = source_conditioned_palette_information_contract(128, 400, (tuple(range(400)),),
        palette_fixed_before_source_labels=True, operations_and_readout_in_cell_algebra=True)
    assert row["applicable"]
    assert row["effective_cell_count"] == 1
    assert row["source_labels_retained"] == 400
    assert row["trace_distance_upper_bound_power_of_two"] < -100
    assert not row["exact_coset_copy_compression"]
    assert not row["is_classical_dequantization"]
    assert not row["novelty_established"]
    # Empty palettes can still expose the classical source distribution.
    labels_only = source_conditioned_palette_information_contract(128, 400, (),
        palette_fixed_before_source_labels=True, operations_and_readout_in_cell_algebra=True)
    assert labels_only["effective_cell_count"] == 0
    assert labels_only["untouched_copies"] == 400
    assert labels_only["trace_distance_upper_bound_power_of_two"] is not None
    assert labels_only["bound_components"][1]["upper_bound_power_of_two"] is None


def test_source_conditioned_bound_refuses_adaptive_regrouping_and_individual_row_access():
    for fixed, algebra in ((False, True), (True, False), (False, False)):
        row = source_conditioned_palette_information_contract(128, 400, (tuple(range(400)),),
            palette_fixed_before_source_labels=fixed, operations_and_readout_in_cell_algebra=algebra)
        assert not row["applicable"]
        assert row["trace_distance_upper_bound_power_of_two"] is None
        assert row["bound_is_vacuous"] is None
        assert not row["bound_components"]
    for n in (True, 4, 7, 9, 8.0):
        with pytest.raises(ValueError):
            source_conditioned_palette_information_contract(n, 10, (),
                palette_fixed_before_source_labels=True, operations_and_readout_in_cell_algebra=True)
    with pytest.raises(ValueError, match="boolean"):
        source_conditioned_palette_information_contract(128, 400, (),
            palette_fixed_before_source_labels="false", operations_and_readout_in_cell_algebra=True)


def test_dyadic_total_bound_dominates_the_independent_radical_formula():
    n, k, palette = 64, 160, (tuple(range(160)),)
    row = source_conditioned_palette_information_contract(n, k, palette,
        palette_fixed_before_source_labels=True, operations_and_readout_in_cell_algebra=True)
    order = math.factorial(n)
    m = order // (2**(n // 2) * math.factorial(n // 2))
    exact_formula = (math.sqrt(1 / m) / 2 + k / (2 * math.sqrt(m))
                     + math.sqrt((order - 1) / n**k) / 2
                     + math.sqrt(float(Fraction((order - 2) * 9**k, n**k))) / 2)
    assert exact_formula <= 2.0**row["trace_distance_upper_bound_power_of_two"]


def test_small_cells_are_charged_as_raw_quantum_inputs_not_as_one_sample():
    n, k = 1024, 4500
    large = tuple(range(30, k))
    palette = (tuple(range(10)) + large, tuple(range(10, 30)) + large)
    kwargs = dict(palette_fixed_before_source_labels=True, operations_and_readout_in_cell_algebra=True)
    naive = source_conditioned_palette_information_contract(n, k, palette, **kwargs)
    assert naive["bound_is_vacuous"]
    retained = source_conditioned_palette_information_contract(n, k, palette, retain_cells_below=21, **kwargs)
    assert retained["effective_cell_count"] == 3
    assert retained["effective_coset_copy_count"] == 31
    assert retained["retained_cell_widths"] == [10, 20]
    assert retained["compressed_cell_widths"] == [4470]
    assert retained["trace_distance_upper_bound_power_of_two"] < -2000
    assert all(row.get("cell_width", 4470) == 4470 for row in retained["bound_components"])
    all_retained = source_conditioned_palette_information_contract(n, k, palette, retain_cells_below=k+1, **kwargs)
    assert all_retained["effective_coset_copy_count"] == k
    assert not all_retained["compressed_cell_widths"]
    assert all_retained["bound_is_vacuous"]
    for threshold in (-1, True, .5):
        with pytest.raises(ValueError, match="threshold"):
            source_conditioned_palette_information_contract(n, k, palette, retain_cells_below=threshold, **kwargs)


def test_adaptive_catalogue_pays_for_all_whole_execution_bounds():
    k = 4500
    first = tuple(tuple(i for i in range(k) if (1 + i % 3) & (1 << bit)) for bit in range(2))
    second = (tuple(range(k)),)
    row = adaptive_palette_catalogue_information_contract(1024, k, (first, second),
        catalogue_fixed_before_input=True, complete_execution_covered=True,
        support_choices_classically_observed=True, operators_and_readout_respect_cover=True)
    assert row["applicable"] and row["source_and_transcript_adaptive_selection_covered"]
    exponents = [item["trace_distance_upper_bound_power_of_two"] for item in row["fixed_palette_bounds"]]
    assert row["trace_distance_upper_bound_power_of_two"] == max(exponents) + 1
    assert row["trace_distance_upper_bound_power_of_two"] < -500
    assert not row["normalized_postselected_branches_used"]
    assert not row["catalogue_size_is_runtime_lower_bound"]
    assert not row["coherent_support_selection_covered"]
    assert not row["novelty_established"]


def test_catalogue_refuses_quantum_selectors_posthoc_catalogues_and_step_only_covers():
    flags = dict(catalogue_fixed_before_input=True, complete_execution_covered=True,
                 support_choices_classically_observed=True, operators_and_readout_respect_cover=True)
    catalogue = ((tuple(range(400)),),)
    for name in flags:
        row = adaptive_palette_catalogue_information_contract(128, 400, catalogue, **(flags | {name: False}))
        assert not row["applicable"]
        assert row["trace_distance_upper_bound_power_of_two"] is None
        assert row["bound_is_vacuous"] is None
        with pytest.raises(ValueError, match="boolean"):
            adaptive_palette_catalogue_information_contract(128, 400, catalogue, **(flags | {name: "false"}))
    with pytest.raises(ValueError, match="nonempty"):
        adaptive_palette_catalogue_information_contract(128, 400, (), **flags)


def test_selected_branch_distance_requires_a_sum_not_the_largest_comparison_bound():
    # Two equally likely initial classical labels, with disjoint informative
    # sectors. Each complete comparison has T=1/2; adaptive selection has T=1.
    zero = np.array([[.5, 0, .5], [0, .5, .5]])
    one = np.array([[0, .5, .5], [.5, 0, .5]])
    comparisons = np.abs(zero - one).sum(axis=1) / 2
    selected = np.abs(zero[:, :2] - one[:, :2]).sum() / 2
    assert selected == 1
    assert selected > comparisons.max()
    assert selected == comparisons.sum()
    # Renormalizing a rare sector would erase the cost paid by the actual run.
    epsilon = 1e-9
    rare0, rare1 = np.array([epsilon, 0, 1 - epsilon]), np.array([0, epsilon, 1 - epsilon])
    assert np.abs(rare0 - rare1).sum() / 2 == pytest.approx(epsilon)
    assert np.abs(rare0[:2] / epsilon - rare1[:2] / epsilon).sum() / 2 == 1
