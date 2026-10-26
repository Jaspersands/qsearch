"""Mixed-input, complete-instrument checks independent of sparse merge code."""
from itertools import product
from fractions import Fraction
from math import prod

import numpy as np
import pytest

from theorems.affine_phase_channel_audit import (
    branch, controls, coset_mixture, coset_vectors, kraus, points, span, translated_phases,
)


@pytest.mark.parametrize("basis", [[], [(1, 2)], [(1, 0), (0, 1)]])
def test_mixture_definition_matches_density_entries(basis):
    p, width = 3, 2
    ambient = points(p, width)
    phases = [(x*x + y) % p for x, y in ambient]
    actual = coset_mixture(p, width, basis, phases)
    subspace = span(p, width, basis)
    expected = np.array([
        [np.exp(2j*np.pi*(phases[i] - phases[j])/p)/len(ambient)
         if tuple((a-b) % p for a, b in zip(x, y)) in subspace else 0
         for j, y in enumerate(ambient)]
        for i, x in enumerate(ambient)])
    assert np.max(abs(actual - expected)) < 1e-12
    assert np.trace(actual) == pytest.approx(1)
    assert np.linalg.eigvalsh(actual).min() > -1e-12


def test_unknown_support_source_does_not_identify_full_polynomial():
    p, width = 5, 2
    ambient = points(p, width)
    phases = [(x**3 + x*y*y) % p for x, y in ambient]
    altered = [(value + y**3) % p for value, (_, y) in zip(phases, ambient)]
    line = [(1, 0)]
    full = [(1, 0), (0, 1)]
    for label in range(p):
        left, right = [[label*value % p for value in table] for table in (phases, altered)]
        assert np.max(abs(coset_mixture(p, width, line, left)
                          - coset_mixture(p, width, line, right))) < 1e-12
        if label:
            assert np.max(abs(coset_mixture(p, width, full, left)
                              - coset_mixture(p, width, full, right))) > 0.01


def test_known_line_measurement_cannot_substitute_for_hpgp_oracle_restriction():
    p, width = 5, 2
    ambient = points(p, width)
    phases = [(x**3 + x*y*y) % p for x, y in ambient]
    source = coset_mixture(p, width, [(1, 0)], phases)
    # The public measured functional y-x has kernel W=span((1,1)).
    averaged = np.zeros_like(source)
    for label in range(p):
        mask = np.array([(y-x) % p == label for x, y in ambient], dtype=float)
        posterior = source * np.outer(mask, mask)
        assert np.trace(posterior).real == pytest.approx(1/p)
        assert np.max(abs(posterior*p - np.diag(mask/p))) < 1e-12
        averaged += posterior
    assert np.max(abs(averaged - np.eye(len(ambient))/len(ambient))) < 1e-12
    assert np.max(abs(source - averaged)) > 0.01


@pytest.mark.parametrize("scales", [(1, 2), (0, 2), (2, 0)])
def test_every_mixed_branch_with_inactive_inputs(scales):
    p, width = 3, 2
    ambient = points(p, width)
    phases = [[(x*y + x) % p for x, y in ambient],
              [(x*x + y*y) % p for x, y in ambient]]
    basis = [(1, 2)]
    source = np.kron(*(coset_mixture(p, width, basis, table) for table in phases))
    for outcomes in product(ambient, repeat=2):
        actual = branch(p, width, scales, outcomes, source)
        probability = np.trace(actual).real
        assert probability == pytest.approx(len(ambient)**-2)
        expected = coset_mixture(p, width, basis,
                                 translated_phases(p, width, scales, outcomes, phases))
        assert np.max(abs(actual / probability - expected)) < 1e-12


def test_sequential_adaptive_branch_invariant_and_telescoping_probability():
    p, width = 3, 1
    ambient = points(p, width)
    basis = [(1,)]
    phases = [[x[0]*x[0] % p for x in ambient], [x[0] for x in ambient]]
    sources = [coset_mixture(p, width, basis, table) for table in phases]
    for first_y in product(ambient, repeat=2):
        first_scales = (1, 2)
        first = branch(p, width, first_scales, first_y, np.kron(*sources))
        first_probability = np.trace(first).real
        first_phases = translated_phases(p, width, first_scales, first_y, phases)
        # A public transcript-dependent choice, including an inactive input.
        second_scales = (1, first_y[0][0])
        for second_y in product(ambient, repeat=2):
            joint = branch(p, width, second_scales, second_y, np.kron(first, sources[0]))
            joint_probability = np.trace(joint).real
            assert joint_probability == pytest.approx(first_probability * p**-2)
            expected_phases = translated_phases(
                p, width, second_scales, second_y, [first_phases, phases[0]])
            expected = coset_mixture(p, width, basis, expected_phases)
            assert np.max(abs(joint / joint_probability - expected)) < 1e-12


def test_exact_phase_cancellation_decouples_classical_transcript():
    p, width = 3, 2
    ambient = points(p, width)
    basis = [(1, 2)]
    phases = [[(x+y) % p for x, y in ambient], [(-x-y) % p for x, y in ambient]]
    source = np.kron(*(coset_mixture(p, width, basis, table) for table in phases))
    expected = coset_mixture(p, width, basis, [0]*len(ambient))
    aggregate = np.zeros_like(expected)
    for outcomes in product(ambient, repeat=2):
        actual = branch(p, width, (1, 1), outcomes, source)
        assert np.max(abs(actual*len(ambient)**2 - expected)) < 1e-12
        aggregate += actual
    assert np.max(abs(aggregate - expected)) < 1e-12
    fourier = np.array([[np.exp(-2j*np.pi*sum(a*b for a, b in zip(x, y))/p)
                         / np.sqrt(len(ambient)) for x in ambient] for y in ambient])
    distribution = np.diag(fourier @ aggregate @ fourier.conj().T).real
    outside = [j for j, y in enumerate(ambient) if sum(a*b for a, b in zip(y, basis[0])) % p]
    assert abs(distribution[outside].sum()) < 1e-12
    classical_distribution = np.diag(fourier @ (np.eye(len(ambient))/len(ambient))
                                     @ fourier.conj().T).real
    assert classical_distribution[outside].sum() == pytest.approx(2/3)


def test_all_zero_scales_are_cptp_but_destroy_the_desired_invariant():
    ambient = points(3, 1)
    completeness = np.zeros((9, 9), dtype=complex)
    for outcomes in product(ambient, repeat=2):
        operator = kraus(3, 1, (0, 0), outcomes)
        completeness += operator.conj().T @ operator
    assert np.max(abs(completeness - np.eye(9))) < 1e-12
    source = np.eye(9)/9
    output = branch(3, 1, (0, 0), ((0,), (0,)), source)*9
    assert np.max(abs(output - np.ones((3, 3))/3)) < 1e-12
    assert np.max(abs(output - np.eye(3)/3)) > 0.3


def test_nonparallel_subspaces_give_intersection_not_an_arbitrary_original_line():
    ambient = points(3, 2)
    zero = [0]*len(ambient)
    source = np.kron(coset_mixture(3, 2, [(1, 0)], zero),
                     coset_mixture(3, 2, [(0, 1)], zero))
    for outcomes in product(ambient, repeat=2):
        posterior = branch(3, 2, (1, 2), outcomes, source)*len(ambient)**2
        assert np.max(abs(posterior - np.eye(len(ambient))/len(ambient))) < 1e-12


def test_pure_coset_and_correlated_coset_probabilities_are_not_mixed_iid_law():
    ambient = points(3, 2)
    kets = coset_vectors(3, 2, [(1, 0)], [0]*len(ambient))
    pure = np.kron(kets[0], kets[0])
    density = np.outer(pure, pure.conj())
    probabilities = [np.trace(branch(3, 2, (1, 1), ys, density)).real
                     for ys in product(ambient, repeat=2)]
    assert sum(probabilities) == pytest.approx(1)
    assert sum(q < 1e-12 for q in probabilities) == 54
    assert max(probabilities) == pytest.approx(1/27)


def test_complete_live_audit_includes_actual_mixed_group_source_and_falsifiers():
    report = controls()
    assert max(report["errors"].values()) < 1e-10
    assert report["source"]["partial_qft_labels_checked"] == 125
    assert report["source"]["constructed_from_mixed_hsp_edges"]
    assert not report["source"]["pure_state_receiver_used"]
    assert report["negative_controls"]["correlated_zero_probability_outcomes"] == 54
    assert not report["scope"]["novelty_established"]
    assert not report["scope"]["general_prime_sde_solver_implemented_here"]


@pytest.mark.parametrize("arities", [(2,), (2, 3), (3, 2, 4), (2, 2, 2, 2)])
def test_depth_first_erasure_schedule_charges_distinct_leaves_and_peak_registers(arities):
    live, peak, leaf_count = 0, 0, 0
    stage_calls = [0]*len(arities)

    def allocate():
        nonlocal live, peak
        live += 1
        peak = max(peak, live)

    def build(stage):
        nonlocal live, leaf_count
        if stage == len(arities):
            allocate()
            leaf_count += 1
            return {leaf_count}
        children = [build(stage+1) for _ in range(arities[stage])]
        assert sum(map(len, children)) == len(set().union(*children))
        stage_calls[stage] += 1
        allocate()  # Fresh uniform target exists before source measurement.
        live -= arities[stage]  # All measured copies, including zero-scale copies.
        return set().union(*children)

    ancestry = build(0)
    assert len(ancestry) == leaf_count == prod(arities)
    assert live == 1
    assert stage_calls == [prod(arities[:j]) for j in range(len(arities))]
    assert sum(stage_calls) <= leaf_count-1
    assert peak == 2 + sum(arity-1 for arity in arities)


def test_small_joint_error_can_be_large_after_rare_acceptance_conditioning():
    accepted, error = Fraction(1, 10**9), Fraction(1, 1000)
    ideal = [accepted, Fraction(0), 1-accepted]  # correct, wrong, abort
    approximate = [accepted, error, 1-accepted-error]
    total_variation = sum(abs(a-b) for a, b in zip(ideal, approximate))/2
    assert total_variation == error
    assert approximate[1] == error  # Unconditional wrong-output probability.
    assert approximate[1]/sum(approximate[:2]) > Fraction(999, 1000)


def test_bounded_retries_charge_abort_and_approximation_without_postselection():
    target = Fraction(1, 1024)
    attempts = 1
    while Fraction(1, 4)**attempts > target/2:
        attempts += 1
    per_attempt_error = target/(2*attempts)
    ideal_abort = Fraction(1, 4)**attempts
    hybrid_error = attempts*per_attempt_error
    assert ideal_abort + hybrid_error <= target
    # An explicit imperfect-attempt model, retaining the ABORT output.
    correct = (1-per_attempt_error)*Fraction(3, 4)
    wrong = per_attempt_error
    abort = (1-per_attempt_error)*Fraction(1, 4)
    total_correct = correct*sum(abort**j for j in range(attempts))
    total_wrong = wrong*sum(abort**j for j in range(attempts))
    total_abort = abort**attempts
    assert total_correct + total_wrong + total_abort == 1
    assert total_wrong <= hybrid_error
    assert total_wrong + total_abort <= target
