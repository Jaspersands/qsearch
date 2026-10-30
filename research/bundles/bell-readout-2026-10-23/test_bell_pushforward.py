from fractions import Fraction

import numpy as np
import pytest

from bell_pushforward import (
    born_law, chain_control, circuit_target_density, exact_chain_evidence,
    map_sample, multiply_commuting_hermitian, polynomial, push_law, tv,
    paired_readout_value,
)


@pytest.mark.parametrize("seed", [10, 11, 12])
def test_actual_partial_trace_equals_pushforward_with_wrong_decoder(seed):
    rng = np.random.default_rng(seed)
    a = rng.normal(size=16) + 1j*rng.normal(size=16)
    a /= np.linalg.norm(a)
    images = [map_sample(u, (1, 2, 3, 1)) for u in range(16)]
    decoder = list(rng.integers(0, 16, size=4))
    phases = np.exp(1j*rng.uniform(-np.pi, np.pi, size=16))
    rho = circuit_target_density(a, images, decoder, phases)
    expected = np.bincount(images, weights=abs(a)**2, minlength=4)
    assert np.diag(rho) == pytest.approx(expected, abs=1e-13)
    assert np.trace(rho) == pytest.approx(1)
    assert np.min(np.linalg.eigvalsh(rho)) >= -1e-12


def test_coherent_collision_sum_is_not_a_classical_pushforward():
    a = np.array([1, 1, 1, 0]) / np.sqrt(3)
    rho = circuit_target_density(a, [0, 1, 0, 1], [0, 1], [1]*4)
    assert np.diag(rho) == pytest.approx([2/3, 1/3])
    wrong = np.array([4/5, 1/5])
    assert 0.5*sum(abs(np.diag(rho)-wrong)) == pytest.approx(2/15)


def test_phase_information_cannot_be_recovered_from_bell_samples():
    a = np.array([1, 1]) / np.sqrt(2)
    plus = circuit_target_density(a, [0, 1], [0, 1], [1, 1])
    minus = circuit_target_density(a, [0, 1], [0, 1], [1, -1])
    assert np.diag(plus) == pytest.approx(np.diag(minus))
    x = np.array([[0, 1], [1, 0]])
    assert np.trace(x @ plus) == pytest.approx(1)
    assert np.trace(x @ minus) == pytest.approx(-1)


def test_noncommuting_interacting_chain_below_relative_distance():
    row = exact_chain_evidence(5, 2)
    assert row["strict_distance_condition"]
    assert row["support_map_injective"]
    assert row["coherent_coefficients_match"]
    assert row["bell_pushforward_tv"] == "0"
    assert row["source_terms"] == 24
    assert not row["hard_instance"]


def test_out_of_window_chain_is_not_declared_dequantized():
    row = exact_chain_evidence(5, 3)
    assert not row["strict_distance_condition"]
    assert not row["support_map_injective"]
    assert row["coherent_coefficients_match"]
    assert Fraction(row["bell_pushforward_tv"]) > 0


def test_exact_pauli_signs_and_nonhermitian_rejection():
    # (X+Z)^2=2I, not 2I+2XZ. This is needed for actual quantum chains.
    h = {(1, 0): 1, (0, 1): 1}
    assert polynomial(h, [0, 0, 1]) == {(0, 0): 2}
    assert multiply_commuting_hermitian({(1, 1): 1}, {(1, 1): 1}) == {(0, 0): 1}
    with pytest.raises(ValueError):
        multiply_commuting_hermitian({(1, 0): 1}, {(0, 1): 1})


def test_classical_forward_map_only_handles_one_long_label():
    columns = tuple(1 << (i % 73) for i in range(1000))
    label = (1 << 999) | (1 << 70) | 1
    assert map_sample(label, columns) == (columns[999] ^ columns[70] ^ columns[0])


def test_pushforward_contractivity_and_invalid_promises():
    p, q = {0: Fraction(1, 4), 1: Fraction(3, 4)}, {0: Fraction(1, 2), 1: Fraction(1, 2)}
    assert tv(push_law(p, lambda _: 0), push_law(q, lambda _: 0)) <= tv(p, q)
    with pytest.raises(ValueError):
        push_law({0: Fraction(2)}, lambda x: x)
    with pytest.raises(ValueError):
        born_law({0: 0})
    with pytest.raises(ValueError):
        map_sample(4, (1, 2))
    with pytest.raises(ValueError):
        chain_control(100)


def test_receipt_keeps_algorithm_and_scope_claims_blocked():
    from replay_bell import evidence
    record = evidence()
    for key in ("speedup_admitted", "novelty_admitted", "general_coherent_simulation_admitted",
                "thermal_mpo_constructor_implemented", "source_mps_sampler_executed"):
        assert record[key] is False
    assert record["requires_valid_target_approximation_promises"]
    assert not record["requires_decoder_for_classical_output"]


@pytest.mark.parametrize("seed", [14, 15, 16])
def test_paired_decoder_readout_matches_actual_target_density(seed):
    rng = np.random.default_rng(seed)
    a = rng.normal(size=16) + 1j*rng.normal(size=16)
    a /= np.linalg.norm(a)
    columns = (1, 2, 3, 1)
    images = [map_sample(u, columns) for u in range(16)]
    decoder = list(rng.integers(0, 16, size=4))
    phases = np.exp(1j*rng.uniform(-np.pi, np.pi, size=16))
    gauge = np.exp(1j*rng.uniform(-np.pi, np.pi, size=4))
    rho = circuit_target_density(a, images, decoder, phases)
    for xmask in range(4):
        for zmask in range(4):
            def nu(t):
                return (1j**((xmask & zmask).bit_count())
                        * (-1)**((zmask & t).bit_count())
                        * gauge[t ^ xmask]/gauge[t])
            observable = np.zeros((4, 4), dtype=complex)
            for t in range(4):
                observable[t ^ xmask, t] = nu(t)
            values = [paired_readout_value(u, a.__getitem__, columns, decoder.__getitem__,
                                           phases.__getitem__, xmask, nu) for u in range(16)]
            actual = sum(abs(a[u])**2*values[u] for u in range(16))
            assert actual == pytest.approx(np.trace(rho @ observable), abs=1e-12)
            assert max(map(abs, values)) <= 1 + 1e-12


def test_absent_partner_image_has_zero_coherent_contribution():
    def forbidden(_):
        raise AssertionError("No amplitude or phase should be requested")
    assert paired_readout_value(0, forbidden, (0,), lambda _: 0, forbidden,
                                1, forbidden) == 0


def test_paired_estimator_uses_phase_and_handles_small_common_scale():
    tiny = lambda u: (1 if u == 0 else 2) * 1e-250
    value = paired_readout_value(0, tiny, (1,), lambda t: t,
                                 lambda u: (-1)**u, 1, lambda _: 1)
    assert value == pytest.approx(-4/5)
