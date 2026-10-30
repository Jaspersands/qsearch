from fractions import Fraction
import math

import numpy as np
import pytest

from pair_circuit import (Gate, compare_greater, expected_pair, input_state,
                          inverse, pair_circuit, precision_budget,
                          prepare_phi_zero, resources, simulate, uniform_interval)
from transfer_control import repetition_transfer
from sampling_bounds import sampling_bound, sqrt_upper


@pytest.mark.parametrize("q", range(1, 34))
def test_interval_forward_inverse_and_padding(q):
    n = max(1, (q - 1).bit_length()) + 1
    gates = uniform_interval(q, tuple(range(n)))
    zero = np.eye(1, 1 << n, dtype=complex).ravel()
    actual = simulate(gates, zero)
    expected = np.zeros_like(zero)
    expected[:q] = 1 / math.sqrt(q)
    np.testing.assert_allclose(actual, expected, atol=2e-15)
    np.testing.assert_allclose(simulate(inverse(gates), actual), zero, atol=4e-15)
    random = np.random.default_rng(q).normal(size=len(zero)) + 1j * np.random.default_rng(q+1).normal(size=len(zero))
    np.testing.assert_allclose(simulate(inverse(gates), simulate(gates, random)), random, atol=5e-15)


@pytest.mark.parametrize("width", range(1, 5))
def test_reversible_comparator_exhaustive(width):
    a, b = tuple(range(width)), tuple(range(width, 2 * width))
    target = 2 * width
    scratch = tuple(range(target + 1, 3 * width))
    gates = compare_greater(a, b, target, scratch)
    # One distinct amplitude per input also checks no collisions and both target values.
    state = np.zeros(1 << (3 * width), dtype=complex)
    expected = np.zeros_like(state)
    for left in range(1 << width):
        for right in range(1 << width):
            for bit in (0, 1):
                index = left | (right << width) | (bit << target)
                state[index] = index + 1j * (index + 1)
                expected[index ^ ((left > right) << target)] = state[index]
    np.testing.assert_array_equal(simulate(gates, state), expected)
    np.testing.assert_array_equal(simulate(inverse(gates), expected), state)


@pytest.mark.parametrize("q", [2, 3, 4, 5, 7, 8, 9, 13, 17])
def test_every_signed_pair_label_and_clean_flags(q):
    plan = pair_circuit(q)
    for c in range(q):
        start = input_state(plan, c)
        actual = simulate(plan.gates, start)
        expected = expected_pair(plan, c)
        np.testing.assert_allclose(actual, expected, atol=3e-15)
        np.testing.assert_allclose(simulate(inverse(plan.gates), actual), start, atol=6e-15)


@pytest.mark.parametrize("q", [3, 4, 5, 7, 9])
def test_complex_superposition_and_full_unitary_inverse(q):
    plan = pair_circuit(q)
    rng = np.random.default_rng(q)
    v = rng.normal(size=q) + 1j * rng.normal(size=q)
    v -= np.mean(v)
    v /= np.linalg.norm(v)
    start = np.zeros(1 << plan.qubits, dtype=complex)
    start[:q] = v
    expected = np.zeros_like(start)
    for a in range(q):
        for b in range(a + 1, q):
            expected[a | (b << plan.width)] = np.exp(1j * math.pi / 4) * (v[a] - v[b]) / math.sqrt(q)
    np.testing.assert_allclose(simulate(plan.gates, start), expected, atol=3e-15)
    # This includes padding, dirty comparison scratch and both flags. They need
    # not be clean on arbitrary inputs, but the entire plan must be invertible.
    arbitrary = rng.normal(size=len(start)) + 1j * rng.normal(size=len(start))
    arbitrary /= np.linalg.norm(arbitrary)
    np.testing.assert_allclose(simulate(inverse(plan.gates), simulate(plan.gates, arbitrary)), arbitrary, atol=3e-15)


@pytest.mark.parametrize("q", [2, 3, 5, 8, 9, 17, 31])
def test_direct_phi_preparation(q):
    plan = pair_circuit(q)
    gates = prepare_phi_zero(q, plan.a, plan.swap_flag)
    zero = np.eye(1, 1 << plan.qubits, dtype=complex).ravel()
    prepared = simulate(gates, zero)
    np.testing.assert_allclose(prepared, input_state(plan, 0), atol=2e-15)
    np.testing.assert_allclose(simulate(inverse(gates), prepared), zero, atol=3e-15)


def test_negative_pair_gram_is_not_unsigned_pair_gram():
    plan = pair_circuit(5)
    a, b = expected_pair(plan, 0), expected_pair(plan, 1)
    assert np.vdot(a, b).real == pytest.approx(-1 / 4)
    assert np.vdot(np.abs(a), np.abs(b)).real == pytest.approx(1 / 4)


def test_missing_uniform_phase_fails():
    plan = pair_circuit(5)
    bad = simulate(plan.prepare + plan.fractional_swap + plan.sort, input_state(plan, 2))
    assert abs(np.vdot(expected_pair(plan, 2), bad)) ** 2 == pytest.approx(1 / 2)


def test_uniform_padded_register_is_wrong():
    plan = pair_circuit(5)
    wrong = uniform_interval(1 << plan.width, plan.b)
    bad = simulate(wrong + plan.fractional_swap + plan.uniform_phase + plan.sort, input_state(plan, 2))
    assert abs(np.vdot(expected_pair(plan, 2), bad)) ** 2 < .9


def test_product_of_bitwise_fractional_swaps_is_wrong():
    plan = pair_circuit(4)
    wrong = ()
    for a, b in zip(plan.a, plan.b):
        spectral = (Gate("h", (plan.swap_flag,)), Gate("swap", (a, b), ((plan.swap_flag, 1),)), Gate("h", (plan.swap_flag,)))
        wrong += spectral + (Gate("phase", controls=((plan.swap_flag, 1),), power=1),) + inverse(spectral)
    bad = simulate(plan.prepare + wrong + plan.uniform_phase + plan.sort, input_state(plan, 0))
    assert abs(np.vdot(expected_pair(plan, 0), bad)) ** 2 < .99


def test_uniform_input_does_not_clean_orientation():
    plan = pair_circuit(5)
    state = np.zeros(1 << plan.qubits, dtype=complex)
    state[:5] = 1 / math.sqrt(5)
    actual = simulate(plan.gates, state)
    index = np.arange(len(actual))
    dirty_mass = np.linalg.norm(actual[((index >> plan.orientation) & 1) == 1]) ** 2
    assert dirty_mass == pytest.approx(1 - 1/(2*plan.q))


@pytest.mark.parametrize("q", [2, 3, 5, 9])
def test_independent_review_sorted_pair_inverse_dirty_work_formula(q):
    plan = pair_circuit(q)
    pair = np.zeros(1 << plan.qubits, dtype=complex)
    pair[1 << plan.width] = 1  # Sorted (0,1), not necessarily in the forward image.
    actual = simulate(inverse(plan.gates), pair)
    index = np.arange(len(actual))
    nonblank_second = ((index >> plan.width) & ((1 << plan.width)-1)) != 0
    assert np.sum(abs(actual[nonblank_second])**2) == pytest.approx(1 - 2/q)


@pytest.mark.parametrize("q", [1019, 65537, 2**127 - 1, 2**256 + 1])
def test_large_symbolic_plan_is_polynomial_not_alphabet_enumeration(q):
    plan = pair_circuit(q)
    ledger = resources(plan)
    n = plan.width
    assert ledger["macro_gates"] <= 3*n*n + 20*n + 10
    assert ledger["max_controls"] <= n
    assert ledger["arbitrary_rotation_elementary_gates_upper"] <= 100*(n+1)*(3*n*n + 20*n + 10)
    assert ledger["structural_qubits"] == 3*n + 1
    assert not ledger["clifford_t_compiled"]
    with pytest.raises(ValueError, match="allocation cap"):
        input_state(plan, 0)


def test_uniform_precision_accounts_for_both_directions_and_other_operations():
    bound = Fraction(9, 10)
    budget = precision_budget(1019, 176, bound)
    assert budget["elementary_call_bound"] == 352 * resources(pair_circuit(1019))["arbitrary_rotation_elementary_gates_upper"]
    assert budget["per_elementary_gate_error"] * budget["elementary_call_bound"] == bound / 4
    assert budget["remaining_other_operations_tv_budget"] == bound / 4
    assert budget["compiled_success_lower_if_all_budgets_met"] == bound / 2


@pytest.mark.parametrize("q", [-1, 0, 1, 2.5])
def test_invalid_alphabet(q):
    with pytest.raises(ValueError):
        pair_circuit(q)


def test_reject_bad_precision_and_gates():
    for copies, bound, fraction in [(0, 1, Fraction(1, 4)), (1, 0, Fraction(1, 4)), (1, 2, Fraction(1, 4)), (1, 1, Fraction(1, 2))]:
        with pytest.raises(ValueError):
            precision_budget(3, copies, bound, fraction)
    with pytest.raises(ValueError):
        simulate((Gate("x", (0,), ((0, 1),)),), [1, 0])


@pytest.mark.parametrize("length", [2, 3])
@pytest.mark.parametrize("syndrome", [0, 1, 2])
def test_transfer_uses_actual_binary_inverse_with_all_work(length, syndrome):
    result = repetition_transfer(length, syndrome)
    assert result["decoder_success"] == pytest.approx(1 - 2**(1-length))
    assert result["joint_fidelity"] == pytest.approx(result["predicted_joint_fidelity"])
    assert result["data_valid_probability"] >= result["joint_fidelity"] - 1e-12
    assert result["raw_verified_probability"] >= result["decoder_success"]**2 / result["gram_eigenvalue"] - 1e-12
    assert not result["quantum_execution"]
    assert result["verified_conditional_tv_from_uniform"] <= result["conditional_fidelity_tv_upper"] + 1e-12


@pytest.mark.parametrize("value", [Fraction(0), Fraction(1, 4), Fraction(1, 3), Fraction(1, 10**100), Fraction(2)])
def test_rational_square_root_upper(value):
    upper = sqrt_upper(value)
    assert upper**2 >= value
    if upper:
        assert (upper - Fraction(1, 2**100))**2 < value


def test_conditioning_tv_bound_exact_small_distributions():
    laws = [(Fraction(a, 8), Fraction(b, 8), Fraction(8-a-b, 8))
            for a in range(9) for b in range(9-a)]
    # First two outcomes valid, third FAILURE; includes changing success mass.
    for mu in laws:
        z = mu[0] + mu[1]
        for nu in laws:
            zz = nu[0] + nu[1]
            delta = sum(abs(x-y) for x, y in zip(mu, nu)) / 2
            if z and zz and delta < z:
                conditional = sum(abs(mu[i]/z - nu[i]/zz) for i in range(2))/2
                assert conditional <= delta/z


def test_sampling_bound_does_not_remove_intrinsic_floor():
    result = sampling_bound(Fraction(9, 10), Fraction(21, 20), Fraction(1, 100))
    assert result["intrinsic_tv_squared_upper"] == Fraction(1, 7)
    assert result["compiled_conditioning_tv_upper"] == Fraction(1, 100) / Fraction(27, 35)
    tighter = sampling_bound(Fraction(9, 10), Fraction(21, 20), 0, failure_bits=200)
    assert tighter["intrinsic_tv_upper"] == result["intrinsic_tv_upper"]
    assert not tighter["arbitrary_requested_precision_at_fixed_input"]
    assert not tighter["exact_uniformity_claimed"]
    assert tighter["fresh_independent_raw_trial_cap"] * tighter["compiled_raw_success_lower"] >= 200


def test_small_failure_family_sampling_bound():
    e, a = Fraction(1, 10**20), Fraction(1, 10**100)
    result = sampling_bound(1-e, 1+a, Fraction(1, 10**15), failure_bits=60)
    assert result["tv_including_abort_upper"] < Fraction(2, 10**10)
    assert not result["premises_verified_by_helper"]


@pytest.mark.parametrize("args", [(0, 1, 0), (1, Fraction(1, 2), 0), (1, 1, 1), (.9, 1, 0)])
def test_bad_sampling_premises(args):
    with pytest.raises(ValueError):
        sampling_bound(*args)
