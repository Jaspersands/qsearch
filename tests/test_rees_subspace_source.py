"""Capped finite controls, not physical execution or a new quantum primitive."""
from dataclasses import dataclass
from fractions import Fraction
from itertools import permutations
from math import comb, factorial
import random

import numpy as np
import pytest

from theorems.rees_hsp_reduction import make_rees_cover, _units
from theorems.rees_projective_source import find_moment_design, projective_source_budget
from theorems.rees_subspace_source import (
    SubspacePlan, capped_subspace_stream, subspace_rees_budget,
)
from theorems.right_abelian_induced_source import upper_triangular_lie


def _antisymmetric(d, k):
    # Deliberately tiny test-only enumeration, never a scalable backend.
    assert 1 <= k <= 4 and 1 <= d <= 6 and d**k <= 256
    size = d**k
    tensor_indices = np.arange(size).reshape((d,)*k)
    projector = np.zeros((size, size), dtype=complex)
    for order in permutations(range(k)):
        parity = sum(order[i] > order[j] for i in range(k) for j in range(i+1, k))
        projector[np.arange(size), tensor_indices.transpose(order).ravel()] += (-1)**parity
    return projector/factorial(k)


def _tensor(matrix, k):
    result = np.ones((1, 1), dtype=complex)
    for _ in range(k):
        result = np.kron(result, matrix)
    return result


def _trace_new(joint, d, k):
    return np.trace(joint.reshape(d**k, d, d**k, d), axis1=1, axis2=3)


def _branches(active, fresh, k):
    d = len(fresh)
    projector = _antisymmetric(d, k+1)
    complement = np.eye(len(projector))-projector
    joint = np.kron(active, fresh)
    return (projector @ joint @ projector,
            _trace_new(complement @ joint @ complement, d, k))


def _unitary(d, seed):
    rng = np.random.default_rng(seed)
    return np.linalg.qr(rng.normal(size=(d, d))+1j*rng.normal(size=(d, d)))[0]


def _wedge(frame):
    d, rank = frame.shape
    vector = np.array([1], dtype=complex)
    for column in frame.T:
        vector = np.kron(vector, column)
    return np.sqrt(factorial(rank))*(_antisymmetric(d, rank) @ vector)


@pytest.mark.parametrize("rank,outputs,beta,b", [
    (2, 3, Fraction(3, 16), 5), (3, 5, Fraction(1, 10), 8),
    (2, 1, Fraction(1), 1), (3, 1, Fraction(3, 8), 3),
])
def test_exact_plan_caps_and_whole_stream_union_bound(rank, outputs, beta, b):
    plan = SubspacePlan(rank, outputs, beta)
    assert plan.tail_bits == b
    assert 2**(b-1) < Fraction(rank*outputs)/beta <= 2**b
    assert plan.growth_attempts_per_output == rank*rank*b
    assert plan.growth_attempt_cap == outputs*rank*rank*b
    assert plan.multiplexed_register_swap_cap == 2*(rank-1)*plan.growth_attempt_cap
    assert plan.raw_copy_cap == outputs*(rank*rank*b+1)
    assert plan.preparation_call_cap == plan.raw_copy_cap+plan.growth_attempt_cap
    assert plan.abort_probability_bound == Fraction(rank*outputs, 2**b) <= beta


def test_plan_is_exact_for_large_copy_counts_without_enumerating_outputs():
    plan = SubspacePlan(3, 2**1024, Fraction(1, 2**128))
    assert plan.tail_bits == 1154
    assert plan.raw_copy_cap == 2**1024*(9*1154+1)
    assert plan.abort_probability_bound == Fraction(3, 2**130)


@pytest.mark.parametrize("rank", [2, 3])
def test_small_exact_growth_chain_obeys_the_conservative_abort_bound(rank):
    plan = SubspacePlan(rank, 3, Fraction(1, 16))
    mass = [Fraction(0)]*(rank+1)
    mass[1] = Fraction(1)
    for _ in range(plan.growth_attempts_per_output):
        updated = [Fraction(0)]*(rank+1)
        updated[rank] = mass[rank]
        for k in range(1, rank):
            p = Fraction(rank-k, rank*(k+1))
            updated[k] += mass[k]*(1-p)
            updated[k+1] += mass[k]*p
        mass = updated
    assert sum(mass) == 1
    assert (1-mass[rank])*plan.outputs <= plan.abort_probability_bound


@pytest.mark.parametrize("rank,outputs,beta", [
    (0, 1, Fraction(1, 10)), (True, 1, Fraction(1, 10)),
    (2, False, Fraction(1, 10)), (2, 0, Fraction(1, 10)),
    (2, 1, 0.1), (2, 1, Fraction(0)), (2, 1, Fraction(2)),
])
def test_invalid_plan_parameters(rank, outputs, beta):
    with pytest.raises(ValueError):
        SubspacePlan(rank, outputs, beta)


@dataclass(frozen=True)
class _Token:
    serial: int
    registers: int
    lineage: frozenset


class _Backend:
    def __init__(self, herald):
        self.herald = herald
        self.live = set()
        self.serial = self.raw = 0
        self.calls, self.delivered, self.discarded, self.rejected_fresh = [], [], [], []

    def token(self, registers, lineage):
        self.serial += 1
        token = _Token(self.serial, registers, frozenset(lineage))
        self.live.add(token)
        return token

    def acquire(self):
        self.raw += 1
        return self.token(1, (self.raw,))

    def grow(self, active, fresh, k):
        assert active.registers == k and fresh.registers == 1
        assert active.lineage.isdisjoint(fresh.lineage)
        assert len(fresh.lineage) == 1
        self.live.remove(active)
        self.live.remove(fresh)
        accepted = self.herald(len(self.calls), k)
        # A new handle on BOTH branches catches silently retaining the old one.
        updated = self.token(k+int(accepted), active.lineage | fresh.lineage)
        self.calls.append((active, fresh, k, accepted, updated))
        if not accepted:
            self.rejected_fresh.append(fresh)
        return accepted, updated

    def consume(self, token):
        self.live.remove(token)
        self.delivered.append(token)

    def discard(self, token):
        self.live.remove(token)
        self.discarded.append(token)

    def run(self, plan, **overrides):
        callbacks = dict(acquire=self.acquire, grow=self.grow,
                         consume=self.consume, discard=self.discard)
        callbacks.update(overrides)
        return capped_subspace_stream(plan, **callbacks)


def test_fresh_lineages_and_updated_failure_tokens_are_preserved():
    backend = _Backend(lambda i, k: i % 3 == 2)
    result = backend.run(SubspacePlan(3, 2, Fraction(1, 8)))
    assert result == {"status": "complete", "raw_copies": 14, "growth_attempts": 12,
                      "delivered_outputs": 2, "peak_live_input_registers": 3}
    assert not backend.live and not backend.discarded
    assert len(backend.rejected_fresh) == 8
    for i, (_, _, k, accepted, updated) in enumerate(backend.calls):
        if k+int(accepted) < 3:
            assert backend.calls[i+1][0] is updated
    first, second = backend.delivered
    assert first.registers == second.registers == 3
    assert first.lineage.isdisjoint(second.lineage)
    assert first.lineage | second.lineage == frozenset(range(1, 15))


def test_first_timeout_aborts_globally_and_discards_latest_active():
    plan = SubspacePlan(2, 3, Fraction(1, 8))
    backend = _Backend(lambda i, k: i == 0)
    result = backend.run(plan)
    assert result["status"] == "abort_per_output_timeout"
    assert result["delivered_outputs"] == 1
    assert result["growth_attempts"] == 1+plan.growth_attempts_per_output
    assert result["raw_copies"] == 3+plan.growth_attempts_per_output < plan.raw_copy_cap
    assert backend.discarded == [backend.calls[-1][-1]]
    assert not backend.live


def test_growth_clock_does_not_reset_on_success_or_failure():
    plan = SubspacePlan(3, 1, Fraction(1, 8))
    backend = _Backend(lambda i, k: i == 0)
    result = backend.run(plan)
    assert result["growth_attempts"] == plan.growth_attempts_per_output
    assert result["raw_copies"] == plan.raw_copy_cap
    assert result["status"] == "abort_per_output_timeout"
    assert backend.discarded[0].registers == 2 and not backend.delivered


def test_success_on_final_allowed_attempt_is_delivered():
    plan = SubspacePlan(2, 1, Fraction(1, 4))
    backend = _Backend(lambda i, k: i == plan.growth_attempts_per_output-1)
    result = backend.run(plan)
    assert result["status"] == "complete"
    assert result["raw_copies"] == plan.raw_copy_cap
    assert result["growth_attempts"] == plan.growth_attempt_cap
    assert len(backend.delivered) == 1 and not backend.live


def test_all_outputs_can_saturate_both_caps_without_overrun():
    plan = SubspacePlan(2, 3, Fraction(1, 8))
    limit = plan.growth_attempts_per_output
    backend = _Backend(lambda i, k: (i+1) % limit == 0)
    result = backend.run(plan)
    assert result["status"] == "complete"
    assert result["growth_attempts"] == plan.growth_attempt_cap
    assert result["raw_copies"] == backend.raw == plan.raw_copy_cap
    assert result["delivered_outputs"] == plan.outputs
    assert not backend.live


def test_rank_one_passthrough_has_no_growth_no_abort_and_accepts_zero_token():
    plan = SubspacePlan(1, 4, Fraction(1, 100))
    tokens = iter(range(4))
    delivered = []
    def forbidden(*args):
        pytest.fail("rank one must not grow or discard")
    result = capped_subspace_stream(plan, acquire=lambda: next(tokens), grow=forbidden,
                                    consume=delivered.append, discard=forbidden)
    assert plan.tail_bits == plan.growth_attempt_cap == plan.abort_probability_bound == 0
    assert plan.multiplexed_register_swap_cap == 0
    assert plan.raw_copy_cap == plan.preparation_call_cap == 4
    assert result["status"] == "complete" and result["raw_copies"] == 4
    assert result["growth_attempts"] == 0 and result["peak_live_input_registers"] == 1
    assert delivered == list(range(4))


@pytest.mark.parametrize("failure", ["acquire", "grow", "consume", "invalid_herald"])
def test_exception_cleanup_obeys_backend_ownership(failure):
    backend = _Backend(lambda i, k: True)
    def acquire():
        if backend.raw == 1:
            raise RuntimeError("acquire failed")
        return backend.acquire()
    def grow(active, fresh, k):
        backend.discard(active)
        backend.discard(fresh)
        raise RuntimeError("grow failed after ownership transfer")
    def consume(token):
        backend.consume(token)
        raise RuntimeError("consume failed after ownership transfer")
    def invalid_herald(active, fresh, k):
        _, updated = backend.grow(active, fresh, k)
        return 1, updated
    key = "grow" if failure == "invalid_herald" else failure
    callback = {"acquire": acquire, "grow": grow, "consume": consume,
                "invalid_herald": invalid_herald}[failure]
    with pytest.raises(ValueError if failure == "invalid_herald" else RuntimeError):
        backend.run(SubspacePlan(2, 2, Fraction(1, 8)), **{key: callback})
    assert not backend.live


@pytest.mark.parametrize("initial", [True, False])
def test_reserved_acquisition_token_rejected_with_active_cleanup(initial):
    backend = _Backend(lambda i, k: True)
    acquisitions = []
    def acquire():
        acquisitions.append(None)
        if initial or len(acquisitions) == 2:
            return None
        return backend.acquire()
    with pytest.raises(ValueError, match="reserved None"):
        backend.run(SubspacePlan(2, 1, Fraction(1, 8)), acquire=acquire)
    assert len(acquisitions) == (1 if initial else 2)
    assert len(backend.discarded) == (0 if initial else 1)
    assert not backend.live


@pytest.mark.parametrize("rank", [2, 3])
def test_actual_flat_tensor_projectors_and_both_growth_branches(rank):
    d = rank+1
    frame = _unitary(d, 40+rank)[:, :rank]
    support = frame @ frame.conj().T
    rho = support/rank
    for k in range(1, rank+1):
        projector = _antisymmetric(d, k)
        np.testing.assert_allclose(projector @ projector, projector, atol=2e-14)
        post = projector @ _tensor(rho, k) @ projector
        probability = np.trace(post).real
        np.testing.assert_allclose(probability, comb(rank, k)/rank**k, atol=2e-14)
        active = post/probability
        np.testing.assert_allclose(projector @ active @ projector, active, atol=2e-14)
        np.testing.assert_allclose(_tensor(support, k) @ active, active, atol=2e-14)
        if k == rank:
            wedge = _wedge(frame)
            np.testing.assert_allclose(active, np.outer(wedge, wedge.conj()), atol=2e-14)
            np.testing.assert_allclose(np.trace(active @ active), 1, atol=2e-14)
            continue
        success, failure = _branches(active, rho, k)
        p = Fraction(rank-k, rank*(k+1))
        np.testing.assert_allclose(np.trace(success), float(p), atol=2e-14)
        np.testing.assert_allclose(np.trace(failure), 1-float(p), atol=2e-14)
        np.testing.assert_allclose(projector @ failure @ projector, failure, atol=2e-14)
        np.testing.assert_allclose(failure/(1-float(p)), active, atol=2e-14)
        next_projector = _antisymmetric(d, k+1)
        next_post = next_projector @ _tensor(rho, k+1) @ next_projector
        np.testing.assert_allclose(success/float(p), next_post/np.trace(next_post), atol=2e-14)


@pytest.mark.parametrize("rank,k", [(2, 1), (3, 2)])
def test_failure_partial_trace_can_change_active_even_with_flat_fresh_source(rank, k):
    frame = np.eye(rank)[:, :k]
    wedge = _wedge(frame)
    active = np.outer(wedge, wedge.conj())
    success, failure = _branches(active, np.eye(rank)/rank, k)
    updated = failure/np.trace(failure)
    assert np.linalg.norm(updated-active) > 0.05
    projector = _antisymmetric(rank, k)
    np.testing.assert_allclose(projector @ updated @ projector, updated, atol=1e-14)
    np.testing.assert_allclose(np.trace(success)+np.trace(failure), 1, atol=1e-14)


@pytest.mark.parametrize("pure_prefix", [False, True])
def test_ancilla_lcu_coherent_rejection_requires_recovery_and_not_label_measurement(pure_prefix):
    # k=2, d=3: the ancilla plus three inputs have total dimension only 81.
    d, k = 3, 2
    q, size = k+1, d**(k+1)
    identity = np.eye(size)
    prefix_projector = _antisymmetric(d, k)
    active = prefix_projector/np.trace(prefix_projector)
    if pure_prefix:
        wedge = _wedge(np.eye(d)[:, :k])
        active = np.outer(wedge, wedge.conj())
    joint = np.kron(active, np.eye(d)/d)
    projector = _antisymmetric(d, k+1)
    expected_success = projector @ joint @ projector
    expected_failure = (identity-projector) @ joint @ (identity-projector)

    W = np.exp(2j*np.pi*np.outer(np.arange(q), np.arange(q))/q)/np.sqrt(q)
    U_A = np.zeros((q*size, q*size), dtype=complex)
    U_A[:size, :size] = identity
    indices = np.arange(size).reshape((d,)*(k+1))
    for label in range(1, q):
        order = list(range(k+1))
        order[label-1], order[k] = order[k], order[label-1]
        swap = identity[indices.transpose(order).ravel()]
        U_A[label*size:(label+1)*size, label*size:(label+1)*size] = -swap
    np.testing.assert_allclose(W.conj().T @ W, np.eye(q), atol=1e-14)
    np.testing.assert_allclose(U_A.conj().T @ U_A, np.eye(q*size), atol=1e-14)

    zero = np.diag([1]+[0]*k)
    lcu = np.kron(W.conj().T, identity) @ U_A @ np.kron(W, identity)
    premeasurement = lcu @ np.kron(zero, joint) @ lcu.conj().T
    accept = np.kron(zero, identity)
    reject = np.eye(q*size)-accept
    accepted = accept @ premeasurement @ accept
    rejected = reject @ premeasurement @ reject
    np.testing.assert_allclose(accepted, np.kron(zero, expected_success), atol=1e-14)
    np.testing.assert_allclose(np.trace(accepted)+np.trace(rejected), 1, atol=1e-14)

    recovery = U_A @ np.kron(W, identity)
    recovered = recovery @ rejected @ recovery.conj().T
    uniform = np.outer(W[:, 0], W[:, 0].conj())
    # Check the full unnormalized branch, including ancilla disentanglement.
    np.testing.assert_allclose(recovered, np.kron(uniform, expected_failure), atol=1e-14)

    def trace_ancilla(state):
        return np.trace(state.reshape(q, size, q, size), axis1=0, axis2=2)

    physical_failure = trace_ancilla(recovered)
    np.testing.assert_allclose(physical_failure, expected_failure, atol=1e-14)
    retained = _trace_new(physical_failure, d, k)
    np.testing.assert_allclose(prefix_projector @ retained @ prefix_projector, retained, atol=1e-14)

    # Refining rejection into individual labels destroys coherences which the
    # recovery needs. Forgetting that classical label does not restore them.
    label_measured = np.zeros_like(rejected)
    for label in range(1, q):
        mask = np.zeros((q, q))
        mask[label, label] = 1
        outcome = np.kron(mask, identity)
        label_measured += outcome @ premeasurement @ outcome
    dephased_recovered = recovery @ label_measured @ recovery.conj().T
    for incorrect in (rejected, dephased_recovered):
        failure = trace_ancilla(incorrect)
        np.testing.assert_allclose(np.trace(failure), np.trace(expected_failure), atol=1e-14)
        assert np.linalg.norm(failure-expected_failure) > 0.05
        old = _trace_new(failure, d, k)
        leakage = np.trace((np.eye(d**k)-prefix_projector) @ old).real/np.trace(old).real
        assert leakage > 0.1


@pytest.mark.parametrize("rank", [1, 2, 3])
def test_determinant_overlap_trace_gap_and_support_stabilizer(rank):
    d = rank+1
    frame = _unitary(d, rank)[:, :rank]
    wedge = _wedge(frame)
    rho = frame @ frame.conj().T/rank
    for seed in range(4):
        action = _unitary(d, seed+10)
        overlap = np.vdot(wedge, _tensor(action, rank) @ wedge)
        np.testing.assert_allclose(overlap, np.linalg.det(frame.conj().T @ action @ frame), atol=2e-14)
        td = np.linalg.svd(rho-action @ rho @ action.conj().T, compute_uv=False).sum()/2
        assert 1-abs(overlap) >= td**2/2-2e-14
    basis = _unitary(d, rank)
    action = basis @ np.diag(np.exp(1j*np.arange(d))) @ basis.conj().T
    np.testing.assert_allclose(action @ rho @ action.conj().T, rho, atol=2e-14)
    overlap = np.vdot(wedge, _tensor(action, rank) @ wedge)
    np.testing.assert_allclose(abs(overlap), 1, atol=2e-14)
    if rank >= 2:
        assert abs(overlap-1) > 0.5  # Projective, not necessarily vector invariance.


def test_nonflat_support_stabilizer_is_not_density_conjugation_stabilizer():
    rho = np.diag([0.75, 0.25, 0])
    action = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1]])
    projector = _antisymmetric(3, 2)
    post = projector @ np.kron(rho, rho) @ projector
    wedge = _wedge(np.eye(3)[:, :2])
    np.testing.assert_allclose(post/np.trace(post), np.outer(wedge, wedge.conj()), atol=1e-14)
    np.testing.assert_allclose(np.vdot(wedge, np.kron(action, action) @ wedge), -1, atol=1e-14)
    assert np.linalg.svd(rho-action @ rho @ action.T, compute_uv=False).sum()/2 == 0.5


def test_gap_conversion_with_two_nonzero_unequal_principal_angles():
    angles = np.array([0.2, 1.1])
    frame = np.eye(4)[:, :2]
    cosines, sines = np.diag(np.cos(angles)), np.diag(np.sin(angles))
    action = np.block([[cosines, -sines], [sines, cosines]])
    rho = frame @ frame.T/2
    wedge = _wedge(frame)
    overlap = abs(np.vdot(wedge, np.kron(action, action) @ wedge))
    td = np.linalg.svd(rho-action @ rho @ action.T, compute_uv=False).sum()/2
    gamma = 1-2*np.trace(rho @ action @ rho @ action.T)
    np.testing.assert_allclose(td, np.sin(angles).mean())
    np.testing.assert_allclose(gamma, (np.sin(angles)**2).mean())
    np.testing.assert_allclose(overlap, np.cos(angles).prod())
    assert gamma >= td**2 and overlap <= 1-gamma <= 1-td**2/2


def test_wrong_rank_underestimates_output_purity_or_makes_growth_impossible():
    rho = np.eye(3)/3
    post = _antisymmetric(3, 2) @ np.kron(rho, rho) @ _antisymmetric(3, 2)
    undershot = post/np.trace(post)
    np.testing.assert_allclose(np.trace(undershot @ undershot), 1/3, atol=1e-14)
    rho = np.diag([0.5, 0.5, 0])
    wedge = _wedge(np.eye(3)[:, :2])
    success, failure = _branches(np.outer(wedge, wedge.conj()), rho, 2)
    np.testing.assert_allclose(success, 0, atol=1e-14)
    np.testing.assert_allclose(np.trace(failure), 1, atol=1e-14)


def test_correlated_copies_with_flat_marginals_can_never_grow():
    correlated = np.diag([0.5, 0, 0, 0.5])
    rho = np.eye(2)/2
    np.testing.assert_allclose(_trace_new(correlated, 2, 1), rho)
    np.testing.assert_allclose(np.trace(correlated.reshape(2, 2, 2, 2), axis1=0, axis2=2), rho)
    projector = _antisymmetric(2, 2)
    np.testing.assert_allclose(projector @ correlated @ projector, 0)
    iid_success, _ = _branches(rho, rho, 1)
    np.testing.assert_allclose(np.trace(iid_success), 1/4)


@pytest.mark.parametrize("rank", [1, 2, 3])
def test_composed_budget_preserves_source_allocation_and_charges_all_calls(rank):
    algebra, _ = upper_triangular_lie(3, 3)
    cover = make_rees_cover(algebra, _units(3))
    design = find_moment_design(3, 2, rng=random.Random(5))
    error, gap = Fraction(1, 10), Fraction(2, 3)
    ideal = projective_source_budget(cover, design, gap**2/2, error/2)
    budget = subspace_rees_budget(cover, design, gap, error, rank=rank)
    plan = SubspacePlan(rank, ideal["total_fresh_copies"], error/8)
    assert budget["ideal_source_budget"] == ideal
    assert budget["ideal_target_copies"] == plan.outputs
    assert budget["wedge_overlap_gap"] == Fraction(2, 9)
    assert budget["raw_copy_cap"] == plan.raw_copy_cap
    assert budget["growth_attempt_cap"] == plan.growth_attempt_cap
    assert budget["multiplexed_register_swap_cap"] == 2*(rank-1)*plan.growth_attempt_cap
    assert budget["abort_probability_bound"] == plan.abort_probability_bound <= error/8
    assert budget["preparer_live_input_register_cap"] == rank
    assert budget["source_or_growth_instrument_error_per_call"]*plan.preparation_call_cap == error/8
    assert budget["tensor_factor_controlled_action_call_cap"] == rank*ideal["total_controlled_action_calls"]
    assert budget["base_controlled_action_error_per_use"] == ideal["copy_and_action_error_per_use"]/rank
    assert (budget["base_controlled_action_error_per_use"]
            *budget["tensor_factor_controlled_action_call_cap"]
            == ideal["copy_and_action_error_per_use"]*ideal["total_controlled_action_calls"])
    assert len(budget["failure_terms"]) == 3
    assert budget["failure_terms"]["ideal_receiver_and_source_bound"] == ideal["total_error_bound"]
    assert budget["total_error_bound"] == sum(budget["failure_terms"].values()) <= error
    for key in ("exact_flat_source_required", "iid_raw_copies_required",
                "rank_is_supplied_not_certified", "flatness_is_supplied_not_certified",
                "trace_gap_is_supplied_not_certified", "conditional_rees_receiver"):
        assert budget[key]
    for key in ("preparer_quantum_backend_implemented", "quantum_receiver_implemented",
                "novel_antisymmetrization_primitive", "speedup_claim_allowed",
                "nonflat_conjugation_symmetry_covered"):
        assert not budget[key]


@pytest.mark.parametrize("rank,gap,error", [
    (False, Fraction(1), Fraction(1, 3)), (2, 0.5, Fraction(1, 3)),
    (2, Fraction(0), Fraction(1, 3)), (2, Fraction(2), Fraction(1, 3)),
    (2, Fraction(1), 0.1), (2, Fraction(1), Fraction(0)),
])
def test_budget_rejects_invalid_public_promises_before_source_work(rank, gap, error):
    with pytest.raises(ValueError):
        subspace_rees_budget(None, None, gap, error, rank=rank)
