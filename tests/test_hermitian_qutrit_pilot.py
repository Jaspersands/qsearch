"""Exact algebra, native readout and independent contraction falsifiers."""

import hashlib
import itertools
import json
from pathlib import Path

import numpy as np
import pytest

from theorems.hermitian_qutrit_pilot import (
    ARTIFACT, OMEGA, bell_mps_from_pilot, bell_prepare, coefficient_vector,
    digits, encode, exact_small_minor, mps_energy, native_control,
    native_hamiltonian, phase_rotate, pilot_mps_reference, power_tables,
    product_expectation, product_pilot_control, ring_multiply, run_controls,
    schmidt_minor, shifted_filter, weyl_matrix,
)


def dense_mps(tensors):
    out = tensors[0][0]
    for tensor in tensors[1:]:
        out = np.tensordot(out, tensor, axes=([-1], [0]))
    return out[..., 0]


def paired_dense_to_matrix(tensor, m):
    out = np.zeros((3 ** m,) * 2, dtype=complex)
    for pairs in itertools.product(range(9), repeat=m):
        a, b = encode([v // 3 for v in pairs]), encode([v % 3 for v in pairs])
        out[a, b] = tensor[pairs]
    return out


def test_eisenstein_ring_uses_exact_integer_pairs():
    for x, y in itertools.product([(1, 0), (0, 1), (-3, 7), (5, -2)], repeat=2):
        a, b = ring_multiply(x, y)
        assert a + b * OMEGA == pytest.approx((x[0] + x[1] * OMEGA) * (y[0] + y[1] * OMEGA))
        for k in range(-3, 4):
            u, v = phase_rotate(x, k)
            assert u + v * OMEGA == pytest.approx((x[0] + x[1] * OMEGA) * OMEGA ** k)


@pytest.mark.parametrize("coefficients", [[2, 3], [1, -2, 3]])
def test_every_exact_power_against_independent_physical_matrices(coefficients):
    m = len(coefficients)
    tables, _ = power_tables(coefficients, 4)
    h = native_hamiltonian(coefficients)
    assert np.linalg.norm(h - h.conj().T) < 1e-12
    basis = []
    for index in range(3 ** m):
        r = digits(index, m)
        basis.append(weyl_matrix(r, [sum(r[j + 1:]) % 3 for j in range(m)]))
    for degree, table in enumerate(tables):
        expected = np.linalg.matrix_power(h, degree)
        coeff = coefficient_vector(table, m)
        reconstructed = sum(value * operator for value, operator in zip(coeff, basis))
        assert np.linalg.norm(reconstructed - expected) / max(1, np.linalg.norm(expected)) < 1e-12
        # Native Hilbert-Schmidt projection independently checks every coefficient.
        projected = [np.trace(operator.conj().T @ expected) / len(h) for operator in basis]
        assert np.linalg.norm(coeff - projected) / max(1, np.linalg.norm(coeff)) < 1e-12
        # The missing pilot is already the filtered seed state, not free data.
        assert np.linalg.norm(coeff - expected[:, 0]) / max(1, np.linalg.norm(coeff)) < 1e-12


def test_minimal_hermitian_rank_minor_is_exact_not_an_svd_threshold():
    table = power_tables([2, 3, 5, 7], 2)[0][2]
    witness = schmidt_minor(table, 4, 2)
    assert witness["schmidt_rank_lower_bound"] == 4 > 2 + 1
    det = exact_small_minor(table, 2, witness)
    assert det == (-4200, -8400)
    p, root = witness["splitting_prime"], witness["omega_image"]
    assert (det[0] + root * det[1]) % p == witness["determinant_mod_prime"] != 0
    assert det[0] ** 2 - det[0] * det[1] + det[1] ** 2 > 0


def test_directional_theorem_does_not_make_the_completed_hamiltonian_easy():
    for hermitian in (False, True):
        tables, _ = power_tables([2, 3, 5, 7], 2, hermitian=hermitian)
        rank = schmidt_minor(tables[2], 4, 2)["schmidt_rank_lower_bound"]
        assert rank == (4 if hermitian else 3)
    a = native_hamiltonian([2, 3], hermitian=False)
    assert np.linalg.norm(a - a.conj().T) > 1
    # Easy powers of A are not the same as powers of its Hermitian completion.
    assert np.linalg.norm(a @ a - (a + a.conj().T) @ (a + a.conj().T)) > 1
    assert power_tables([2, 3, 5, 7], 3, hermitian=False)[0][3] == {0: (503, 0)}


def test_native_normalized_energy_is_independent_of_faithful_realization():
    # X,Z on ONE qutrit have the same independent Weyl commutation data as
    # X_0,Z_0 X_1 on TWO qutrits. Raw dimensions/degeneracies differ.
    x, z = weyl_matrix([1], [0]), weyl_matrix([0], [1])
    h = 2 * (x + x.conj().T) + 3 * (z + z.conj().T)
    p = np.linalg.matrix_power(10 * np.eye(3) - h, 2)
    expected = np.trace(p @ p @ h).real / np.trace(p @ p).real
    record = native_control([2, 3], 2)
    assert record["native_output_energy"] == pytest.approx(expected, abs=1e-11)


def test_inverse_pair_completion_has_no_predecessor_uniform_last_generator():
    generators = list(itertools.product(range(2), (-1, 1)))
    for i, sign in generators:
        phases = {0 if j == i else ((1 if i > j else -1) * sign * other) % 3
                  for j, other in generators if (j, other) != (i, sign)}
        assert len(phases) > 1


def test_public_bell_readout_is_per_qutrit_not_a_cyclic_dimension_nine_dft():
    pilot = np.zeros(9, dtype=complex)
    pilot[encode([0, 1])] = 1
    expected = weyl_matrix([0, 1], [1, 0]) / 3
    assert np.linalg.norm(bell_prepare(pilot, 2) - expected) < 1e-12


@pytest.mark.parametrize("coefficients,degree", [([2, 3], 2), ([2, -3, 5], 3), ([1, 2, 3], 2)])
def test_actual_filter_state_and_classical_energy_not_just_label_law(coefficients, degree):
    record = native_control(coefficients, degree)
    assert record["full_prepared_state_error"] < 1e-12
    assert record["classical_energy_error"] < 1e-11
    assert record["pilot_is_filtered_seed_column_error"] < 1e-12
    assert record["source_output_energy_error"] < 1e-11
    assert record["direct_pilot_mps_energy"] == pytest.approx(record["native_output_energy"], abs=1e-11)
    assert record["native_output_energy"] < 0  # uniform state's mean is zero
    assert record["paired_output_max_bond"] <= 3 * record["pilot_max_bond"]
    assert record["explicit_pilot_preparation_is_exponential"]
    assert not record["efficient_pilot_source_or_ground_gap_proved"]


@pytest.mark.parametrize("m", [1, 2, 3])
def test_three_charge_mps_isometry_for_general_entangled_pilots(m):
    rng = np.random.default_rng(100 + m)
    pilot = rng.normal(size=3 ** m) + 1j * rng.normal(size=3 ** m)
    pilot /= np.linalg.norm(pilot)
    source_mps, lost = pilot_mps_reference(pilot, m)
    assert lost < 1e-24
    assert np.linalg.norm(dense_mps(source_mps).reshape(-1, order="F") - pilot) < 1e-12
    paired = bell_mps_from_pilot(source_mps)
    constructed = paired_dense_to_matrix(dense_mps(paired), m)
    assert np.linalg.norm(constructed - bell_prepare(pilot, m)) < 1e-12
    assert product_expectation(paired, [np.eye(9)] * m).real == pytest.approx(1)
    h = native_hamiltonian([j + 1 for j in range(m)])
    native_mean = np.trace(constructed.conj().T @ h @ constructed).real
    assert mps_energy(paired, list(range(1, m + 1))) == pytest.approx(native_mean, abs=1e-11)
    assert mps_energy(source_mps, list(range(1, m + 1)), paired=False) == pytest.approx(native_mean, abs=1e-11)
    assert np.vdot(pilot, h @ pilot).real == pytest.approx(native_mean, abs=1e-11)


def test_zero_degree_filter_prepares_maximally_mixed_physical_state():
    tables, _ = power_tables([2, 3], 0)
    vector = coefficient_vector(shifted_filter(tables, 10), 2)
    state = bell_prepare(vector, 2)
    assert np.linalg.norm(state @ state.conj().T - np.eye(9) / 9) < 1e-12


def test_scalable_baseline_does_not_call_dense_helpers(monkeypatch):
    import theorems.hermitian_qutrit_pilot as module

    def forbidden(*args, **kwargs):
        raise AssertionError("exponential source/physical matrix used by scalable baseline")

    monkeypatch.setattr(module, "power_tables", forbidden)
    monkeypatch.setattr(module, "bell_prepare", forbidden)
    monkeypatch.setattr(module, "native_hamiltonian", forbidden)
    monkeypatch.setattr(module, "pilot_mps_reference", forbidden)
    record = product_pilot_control(64)
    assert record["paired_output_max_bond"] == 3
    assert record["absolute_error"] < 1e-11
    assert record["intertwiner_energy_error"] < 1e-11
    assert record["final_prefix_character_magnitude"] > 1e-4
    assert not record["exponential_pilot_or_state_table_used"]
    assert not record["is_polynomial_H_filter_pilot"]


@pytest.mark.parametrize("coefficients,degree", [([1] * 9, 2), ([True], 2), ([0.5], 2), ([1], 11), ([], 2)])
def test_caps_and_invalid_sources_do_not_become_hardness_evidence(coefficients, degree):
    with pytest.raises(ValueError):
        power_tables(coefficients, degree)


def test_bad_mps_rejected_before_energy_claim():
    with pytest.raises(ValueError):
        bell_mps_from_pilot([])
    with pytest.raises(ValueError):
        bell_mps_from_pilot([np.full((1, 3, 1), np.nan)])
    with pytest.raises(ValueError):
        mps_energy(bell_mps_from_pilot([np.zeros((1, 3, 1))]), [1])
    with pytest.raises(ValueError, match="no normalized pilot"):
        native_control([0, 0], 2)


def test_artifact_replay_includes_sources_and_no_rank_fit():
    saved = json.loads(ARTIFACT.read_text())
    assert saved == run_controls()
    source = Path(__file__).resolve().parents[1] / "theorems/hermitian_qutrit_pilot.py"
    assert saved["source_sha256"] == hashlib.sha256(source.read_bytes()).hexdigest()
    assert not saved["new_quantum_algorithm_claimed"]
    assert saved["all_native_controls_pass"]
    assert len(saved["rank_controls"]) == 56
    assert all(not c["asymptotic_rank_fit_performed"] for c in saved["rank_controls"])
