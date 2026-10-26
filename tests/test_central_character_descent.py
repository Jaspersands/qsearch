"""Channel identities and counterexamples, not finite-size speedup evidence."""
from fractions import Fraction
from itertools import product

import numpy as np
import pytest

from theorems.central_character_descent import (
    HeisenbergFixture, all_branch_control, check_moment, controlled_discard,
    exhaustive_scale_fixture, tree_budget,
)


@pytest.mark.parametrize("p", [3, 5])
def test_complete_restored_central_instrument_and_original_source(p):
    group = HeisenbergFixture(p)
    rho = group.coset_density_fixture(group.line_fixture())
    assert np.trace(rho) == pytest.approx(1)
    assert np.linalg.eigvalsh(rho).min() > -1e-12
    projectors = [group.projector(label) for label in range(p)]
    assert np.max(np.abs(sum(projectors)-np.eye(p**3))) < 1e-12
    for label, P in enumerate(projectors):
        assert np.max(np.abs(P-group.restored_fourier_projector(label))) < 1e-12
        assert np.max(np.abs(P-P.conj().T)) < 1e-12
        assert np.max(np.abs(P @ rho-rho @ P)) < 1e-12
        for other, Q in enumerate(projectors):
            assert np.max(np.abs(P @ Q-(P if label == other else 0))) < 1e-12
        mass, normalized = group.branches(rho)[label]
        assert mass == pytest.approx(1/p)
        assert np.max(np.abs(normalized-p*P @ rho)) < 1e-12
        # Contract the entire mixed source and compare every right action.
        hidden = group.line_fixture()
        hz = {group.multiply(h, (0, 0, z)): z for h in hidden for z in range(p)}
        for g in group.elements:
            actual = sum(normalized[np.arange(p**3), group.right_permutation(g)])
            expected = np.exp(2j*np.pi*label*hz[g]/p) if g in hz else 0
            assert actual == pytest.approx(expected, abs=1e-12)


@pytest.mark.parametrize("p", [3, 5])
def test_every_character_tuple_including_zero_labels_and_zero_scales(p):
    report = all_branch_control(p)
    assert report["complete_label_tuples"] == p**3
    assert report["zero_scale_branches"] > 0
    assert report["maximum_entry_error"] < 1e-12
    assert report["maximum_label_mass_error"] < 1e-12


def test_literal_joint_target_trace_agrees_with_independent_factorization():
    group = HeisenbergFixture(3)
    rho = group.coset_density_fixture(group.line_fixture())
    branches = group.branches(rho)
    first, second = branches[1][1], branches[2][1]
    controls = group.controls(1)
    pair_controls = np.array([(a[:, None]*27+a[None, :]).ravel() for a in controls])
    actual = controlled_discard(np.kron(first, second), pair_controls)
    factorized = controlled_discard(first, controls)*controlled_discard(second, controls)*9
    assert np.max(np.abs(actual-factorized)) < 1e-12
    assert np.max(np.abs(actual-group.expected_quotient_fixture(group.line_fixture()))) < 1e-12
    assert np.trace(actual) == pytest.approx(1)
    assert np.linalg.eigvalsh(actual).min() > -1e-12


def test_phase_cancellation_does_not_replace_hidden_subgroup_preservation():
    report = all_branch_control(5, central_slope=1)
    assert report["maximum_label_mass_error"] < 1e-12
    assert report["maximum_entry_error"] > 0.01


def test_dropping_center_requires_twisted_action_not_plain_quotient_translation():
    group = HeisenbergFixture(5)
    rho = group.coset_density_fixture(group.line_fixture())
    p = group.p
    row = np.exp(-2j*np.pi*np.arange(p)/p)/np.sqrt(p)
    compression = np.kron(np.eye(p*p), row[None, :])
    compressed = p*compression @ rho @ compression.conj().T
    coordinates = tuple(product(range(p), repeat=2))
    index = {x: i for i, x in enumerate(coordinates)}
    def wrong_controls(s):
        return np.array([[index[((x-s*a) % p, (y-s*b) % p)] for x, y in coordinates]
                         for a, b in coordinates])
    check_moment(((1,), (1,)), (1, 2), p, 2)
    wrong = controlled_discard(compressed, wrong_controls(1))*controlled_discard(compressed, wrong_controls(2))*p*p
    expected = group.expected_quotient_fixture(group.line_fixture())
    assert np.max(np.abs(wrong-expected)) > 0.01
    assert np.max(np.abs(wrong-np.eye(p*p)/(p*p))) < 1e-12


def test_nontrivial_central_intersection_has_zero_mass_labels():
    group = HeisenbergFixture(5)
    rho = group.coset_density_fixture([(0, 0, z) for z in range(5)])
    branches = group.branches(rho)
    assert branches[0][0] == pytest.approx(1)
    assert all(abs(mass) < 1e-12 and state is None for mass, state in branches[1:])


def test_correlated_sources_pass_marginals_and_all_label_masses_but_fail_descent():
    # Abelian finite-register counterexample, NOT an oracle candidate.
    # Quotient registers share a Bell pair; central registers are independent.
    p = 3
    states = tuple(product(range(p), repeat=4))
    joint = np.zeros((p**4, p**4), dtype=complex)
    for i, (q, z, r, w) in enumerate(states):
        for j, (Q, Z, R, W) in enumerate(states):
            joint[i, j] = int(q == r and Q == R and z == Z and w == W)/p**3
    tensor = joint.reshape(p*p, p*p, p*p, p*p)
    assert np.max(np.abs(np.einsum("abcb->ac", tensor)-np.eye(p*p)/(p*p))) < 1e-12
    assert np.max(np.abs(np.einsum("abad->bd", tensor)-np.eye(p*p)/(p*p))) < 1e-12
    projected = {}
    for a, b in product(range(p), repeat=2):
        rows = [np.exp(-2j*np.pi*label*np.arange(p)/p)/np.sqrt(p) for label in (a, b)]
        P, Q = [np.kron(np.eye(p), np.outer(row.conj(), row)) for row in rows]
        instrument = np.kron(P, Q)
        branch = instrument @ joint @ instrument.conj().T
        assert np.trace(branch) == pytest.approx(1/(p*p))
        projected[a, b] = branch*p*p
    index = {x: i for i, x in enumerate(states)}
    controls = np.array([[index[((q-g) % p, z, (r-g) % p, w)] for q, z, r, w in states] for g in range(p)])
    check_moment(((1,), (2,)), (1, 1), p, 2)
    actual = controlled_discard(projected[1, 2], controls)
    expected = np.eye(p)/p
    assert np.max(np.abs(actual-np.ones((p, p))/p)) < 1e-12
    distance = sum(abs(np.linalg.eigvalsh(actual-expected)))/2
    assert distance == pytest.approx(Fraction(2, 3))


def test_witness_contract_checks_every_character_coordinate_and_nonempty_support():
    assert check_moment(((1, 2), (4, 3), (2, 1)), (1, 1, 0), 5, 2) == (0, 1)
    with pytest.raises(ValueError, match="all-zero"):
        check_moment(((1,), (1,)), (0, 0), 5, 2)
    with pytest.raises(ValueError, match="character moment"):
        check_moment(((1, 0), (4, 1)), (1, 1), 5, 2)
    with pytest.raises(ValueError, match="canonical"):
        check_moment(((1,), (4,)), (1, 6), 5, 2)
    with pytest.raises(ValueError, match="central rank"):
        check_moment(((1,), (4, 0)), (1, 1), 5, 2)
    with pytest.raises(ValueError, match="cap"):
        exhaustive_scale_fixture(((1,),)*20, 5, 2)
    with pytest.raises(ValueError, match="nonzero scales"):
        HeisenbergFixture(5).controls(0)


def test_action_is_a_complete_channel_without_any_hidden_source_promise():
    group = HeisenbergFixture(3)
    rng = np.random.default_rng(917)
    a = rng.normal(size=(27, 27))+1j*rng.normal(size=(27, 27))
    rho = a @ a.conj().T
    rho /= np.trace(rho)
    out = controlled_discard(rho, group.controls(2))
    assert np.trace(out) == pytest.approx(1)
    assert np.linalg.eigvalsh(out).min() > -1e-12
    with pytest.raises(ValueError, match="permutation"):
        controlled_discard(rho, np.zeros((9, 27), dtype=int))


def test_fresh_tree_counts_and_global_errors_not_rare_branch_errors():
    budget = tree_budget((3, 5, 7), Fraction(1, 1000), (Fraction(1, 1000),)*3)
    assert budget["source_leaves"] == 105
    assert budget["stage_calls"] == (35, 7, 1)
    assert budget["total_instrument_calls"] == 148
    assert budget["trace_distance_bound"] == Fraction(148, 1000)
    assert tree_budget((), Fraction(1, 10))["trace_distance_bound"] == Fraction(1, 10)
    assert tree_budget((100,), Fraction(1, 10))["trace_distance_bound"] == 1
    with pytest.raises(ValueError, match="positive integral"):
        tree_budget((0, 3))
    with pytest.raises(ValueError, match="one nonnegative"):
        tree_budget((3, 5), stage_errors=(Fraction(1, 100),))
