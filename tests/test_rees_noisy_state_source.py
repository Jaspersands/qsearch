"""Physical purification controls and scoped composition, not quantum execution."""
from fractions import Fraction

import numpy as np
import pytest

from theorems.rees_noisy_state_source import (
    PurificationPlan, capped_purification_stream, noisy_rees_budget,
)
from tests.test_rees_projective_source import _ut3_source


def _swap_branch(joint, dimension, symmetric):
    swap = np.zeros_like(joint)
    for a in range(dimension):
        for b in range(dimension):
            swap[a*dimension+b, b*dimension+a] = 1
    projector = (np.eye(dimension**2)+(1 if symmetric else -1)*swap)/2
    post = projector @ joint @ projector
    reduced = np.trace(post.reshape(dimension, dimension, dimension, dimension), axis1=1, axis2=3)
    return reduced


def _iterate(rho, levels):
    log_cost = 0.0
    for _ in range(levels):
        square = rho @ rho
        norm = 1+np.trace(square).real
        log_cost += np.log2(4/norm)
        rho = (rho+square)/norm
    return rho, log_cost


def test_physical_swap_branch_is_not_virtual_distillation_and_herald_is_essential():
    rho = np.array([[0.6, 0.13j, 0], [-0.13j, 0.25, 0], [0, 0, 0.15]])
    plus = _swap_branch(np.kron(rho, rho), 3, True)
    minus = _swap_branch(np.kron(rho, rho), 3, False)
    np.testing.assert_allclose(plus, (rho+rho@rho)/2)
    np.testing.assert_allclose(minus, (rho-rho@rho)/2)
    np.testing.assert_allclose(plus+minus, rho)
    probability = np.trace(plus).real
    assert 0.5 <= probability <= 1
    actual = plus/probability
    np.testing.assert_allclose(actual, _iterate(rho, 1)[0])
    assert np.linalg.norm(actual-(rho@rho)/np.trace(rho@rho)) > 0.1


@pytest.mark.parametrize("spectrum", [
    (0.8, 0.15, 0.05), (0.4, 0.3, 0.2, 0.1), (0.21, 0.2, 0.2, 0.2, 0.19),
    (0.9, 0.1),
])
def test_dimension_independent_gap_burn_in_and_expected_cost(spectrum):
    gap = Fraction(str(spectrum[0]))-Fraction(str(spectrum[1]))
    plan = PurificationPlan(gap, Fraction(1, 1000), 3, Fraction(1, 20))
    rho = np.diag(spectrum)
    after_burn, _ = _iterate(rho, plan.burn_in)
    assert 1-after_burn[0, 0] <= 1/8+1e-13
    final, log_cost = _iterate(after_burn, plan.tail_levels)
    assert 1-final[0, 0] <= float(plan.trace_error_bound)+1e-13
    assert log_cost <= plan.tail_levels+1
    assert plan.expected_total_raw_bound/plan.raw_copy_cap <= float(plan.abort_budget)
    assert plan.trace_error_bound <= plan.output_error


def test_exact_low_error_bounds_against_nonuniform_spectrum():
    spectrum = (Fraction(7, 8), Fraction(1, 16), Fraction(1, 24), Fraction(1, 48))
    initial = spectrum
    success_product = Fraction(1)
    for level in range(7):
        error = 1-spectrum[0]
        assert error <= 4*(1-initial[0])/2**level
        assert success_product >= Fraction(5, 8)
        purity = sum(x*x for x in spectrum)
        success_product *= (1+purity)/2
        next_spectrum = tuple(x*(1+x)/(1+purity) for x in spectrum)
        next_error = 1-next_spectrum[0]
        assert next_error <= 2*error/3
        assert next_error <= error/(2*(1-2*error))
        spectrum = next_spectrum


def test_opaque_controller_consumes_rejections_and_keeps_fresh_lineages():
    used, merged, delivered, dropped = [], [], [], []
    def acquire():
        token = frozenset((len(used),))
        used.append(token)
        return token
    def merge(a, b):
        assert a.isdisjoint(b)
        merged.append((a, b))
        if len(merged) == 1:
            dropped.extend((a, b))
            return None
        return a | b
    result = capped_purification_stream(3, 2, 100, acquire=acquire, symmetric_merge=merge,
                                        consume=delivered.append, discard=dropped.append)
    assert result == {"status": "complete", "raw_copies": 18, "swap_tests": 15,
                      "delivered_outputs": 2, "peak_live_input_registers": 4}
    assert all(len(x) == 8 for x in delivered)
    assert delivered[0].isdisjoint(delivered[1])
    assert set().union(*delivered, *dropped) == set(range(18))


def test_global_cap_aborts_and_discards_partial_stack_without_retry_loophole():
    acquired, discarded, outputs = [], [], []
    def acquire():
        acquired.append(len(acquired))
        return acquired[-1]
    result = capped_purification_stream(4, 1, 1, acquire=acquire,
                                        symmetric_merge=lambda a, b: None,
                                        consume=outputs.append, discard=discarded.append)
    assert result["status"] == "abort_raw_copy_cap"
    assert result["raw_copies"] == 1 and result["swap_tests"] == 0
    assert discarded == [0] and not outputs
    result = capped_purification_stream(1, 1, 10, acquire=acquire,
                                        symmetric_merge=lambda a, b: None,
                                        consume=outputs.append, discard=discarded.append)
    assert result["raw_copies"] == 10 and result["swap_tests"] == 5
    assert result["status"] == "abort_raw_copy_cap"


def test_correlated_copies_with_correct_marginals_do_not_purify():
    rho = np.diag((0.75, 0.25))
    correlated = np.diag((0.75, 0, 0, 0.25))
    np.testing.assert_allclose(np.trace(correlated.reshape(2, 2, 2, 2), axis1=1, axis2=3), rho)
    output = _swap_branch(correlated, 2, True)
    np.testing.assert_allclose(output, rho)  # Success probability one, no improvement.
    assert np.linalg.norm(output-_iterate(rho, 1)[0]) > 0.05


def test_degeneracy_and_coherent_rotation_are_not_corrected():
    rho = np.diag((0.5, 0.5, 0.0))
    np.testing.assert_allclose(_iterate(rho, 8)[0], rho)
    theta = 0.2
    phi = np.array([np.cos(theta), np.sin(theta), 0])
    principal = np.outer(phi, phi)
    rotated = 0.8*principal+0.2*np.eye(3)/3
    final, _ = _iterate(rotated, 20)
    np.testing.assert_allclose(final, principal, atol=2e-6)
    original = np.diag((1.0, 0, 0))
    assert np.linalg.norm(final-original) > 0.25
    phase = np.diag(np.exp(2j*np.pi*np.arange(3)/3))
    assert abs(np.trace(original@phase)) == 1
    assert abs(np.trace(final@phase)) < 0.95


def test_noisy_nonabelian_source_is_compared_to_ideal_not_relabelled_exact():
    group, cover, design, H, psi, act, encode, addresses, expected, _ = _ut3_source()
    eta = 0.25
    rho = (1-eta)*np.outer(psi, psi.conj())+eta*np.eye(27)/27
    assert abs(np.trace(rho @ np.eye(27)[np.argsort(group.right_permutation(H[1]))])) < 0.8
    purified, _ = _iterate(rho, 9)
    eta_out = 27*(1-np.vdot(psi, purified@psi).real)/26
    assert 0 < eta_out < eta
    # Finite purification is still full rank: its exact scalar stabilizer did not recover H.
    assert abs(np.trace(purified @ np.eye(27)[np.argsort(group.right_permutation(H[1]))])) < 1-1e-6
    def packet(noise):
        gram = np.ones((81, 81), dtype=complex)
        for s in design.points:
            labels = [encode(cover.evaluate(a, s)) for a in addresses]
            rows = np.array([act(g) for g in labels])
            identity = np.array([[a == b for b in labels] for a in labels])
            gram *= (1-noise)*(rows@rows.conj().T)+noise*identity
        return gram/81
    before = np.linalg.svd(packet(eta)-expected, compute_uv=False).sum()/2
    after = np.linalg.svd(packet(eta_out)-expected, compute_uv=False).sum()/2
    assert 0 < after < before
    assert after <= design.copies_per_block*eta_out*26/27+1e-12
    budget = noisy_rees_budget(cover, design, Fraction(1), Fraction(3, 4), Fraction(1, 10))
    assert budget["total_error_bound"] == sum(budget["failure_terms"].values()) <= Fraction(1, 10)
    assert budget["source_or_swap_instrument_error_per_call"]*2*budget["raw_copy_cap"] == Fraction(1, 80)
    assert budget["swap_test_call_cap"] == budget["raw_copy_cap"]
    assert budget["raw_copy_cap"] > budget["expected_total_raw_copies_bound"] > budget["ideal_target_copies"]
    assert not budget["arbitrary_noise_correction"] and not budget["speedup_claim_allowed"]


def test_promise_validation_and_separate_gap_parameters():
    for gap, error, outputs, abort in ((Fraction(0), Fraction(1, 10), 1, Fraction(1, 10)),
                                       (0.5, Fraction(1, 10), 1, Fraction(1, 10)),
                                       (Fraction(1), Fraction(1, 2), 1, Fraction(1, 10)),
                                       (Fraction(1), Fraction(1, 10), True, Fraction(1, 10)),
                                       (Fraction(1), Fraction(1, 10), 1, Fraction(0))):
        with pytest.raises(ValueError):
            PurificationPlan(gap, error, outputs, abort)
    good = PurificationPlan(Fraction(3, 4), Fraction(1, 100), 10, Fraction(1, 10))
    shrinking = PurificationPlan(Fraction(1, 16), Fraction(1, 100), 10, Fraction(1, 10))
    assert shrinking.burn_in > 20*good.burn_in
    assert shrinking.expected_raw_per_output_bound > 2**100*good.expected_raw_per_output_bound
