import math

import numpy as np
import pytest

from isotypic_instruments import finite_isotypic_instrument, isotypic_label_resource_contract
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
