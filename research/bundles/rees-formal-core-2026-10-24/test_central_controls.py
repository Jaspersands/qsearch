from itertools import product

import numpy as np
import pytest

import central_controls as c


@pytest.mark.parametrize("family,intersection", [("trivial", 1), ("proper_intersection", 3), ("full_center", 9)])
def test_actual_measurement_and_general_intersection_normalization(family, intersection):
    branches = c.measured_branches(family)
    hidden = c.hidden_elements(family)
    allowed_count = 0
    for label, tau in branches.items():
        allowed = all(abs(c.character(label, z)-1) < 1e-12 for z in c.CENTER if c.embed(z) in hidden)
        expected = np.array([[c.coefficient(family, label, c.mul(c.inv(y), x))
                              for y in c.GROUP] for x in c.GROUP])/(81*9)
        assert np.max(np.abs(tau-expected)) < 1e-12
        assert np.linalg.eigvalsh(tau)[0] > -1e-12
        if allowed:
            allowed_count += 1
            assert abs(np.trace(tau)-intersection/9) < 1e-12
            normalized = tau/(intersection/9)
            assert abs(np.trace(normalized)-1) < 1e-12
            for g in c.GROUP:
                expected_correlation = c.coefficient(family, label, g)/intersection
                assert abs(np.trace(normalized@c.right_regular(g))-expected_correlation) < 1e-12
        else:
            assert np.linalg.norm(tau) < 1e-12
    assert allowed_count == 9//intersection
    assert np.max(np.abs(sum(branches.values())-c.oracle_source(family))) < 1e-12


def test_kraus_completeness_on_arbitrary_target_vectors():
    rng = np.random.default_rng(237)
    v, w = (rng.normal(size=81)+1j*rng.normal(size=81) for _ in range(2))
    actual = sum(np.vdot(c.projector(label)@v, c.projector(label)@w) for label in c.CENTER)
    assert abs(actual-np.vdot(v, w)) < 1e-11
    assert np.max(np.abs(sum(c.projector(label).conj().T@c.projector(label) for label in c.CENTER)-np.eye(81))) < 1e-12


def test_noncentral_measurement_cannot_be_replaced_by_one_sided_product():
    # H=<x>; the measured <y> is not central and its projector need not
    # commute with the source. This checks a necessary theorem premise.
    labels = [g[1:] for g in c.GROUP]
    source = np.array([[a == b for b in labels] for a in labels], dtype=complex)/81
    p = sum(c.right_regular((0, y, 0, 0)) for y in range(3))/3
    assert np.linalg.norm(p@source@p.conj().T-p@source) > .05


def test_incomplete_character_family_is_not_trace_preserving():
    source = c.oracle_source("proper_intersection")
    incomplete = sum(c.projector(label)@source@c.projector(label).conj().T
                     for label in c.CENTER if label != (0, 0))
    assert abs(np.trace(incomplete)-2/3) < 1e-12


@pytest.mark.parametrize("reference", [1, 3, 9])
def test_every_positive_record_and_entangled_reference(reference):
    rng = np.random.default_rng(239)
    factor = rng.normal(size=(9*reference, 4))+1j*rng.normal(size=(9*reference, 4))
    rho = factor@factor.conj().T
    rho /= np.trace(rho)
    target = np.array([[q[1] == r[1] for r in c.ADDRESSES] for q in c.ADDRESSES])
    expected = c.apply_reference(target, rho, reference)
    branches = c.measured_branches("proper_intersection")
    grams = {(label, s): c.discard_gram(branches[label], s, True)
             for label in c.CENTER if label[0] == 0 for s in range(3)}
    actual = np.zeros_like(rho)
    for labels in product([label for label in c.CENTER if label[0] == 0], repeat=3):
        gram = np.prod([grams[label, s] for label, s in zip(labels, c.scales(labels))], axis=0)
        output = c.apply_reference(gram, rho, reference)
        assert np.max(np.abs(output-expected/27)) < 1e-12
        actual += output
    assert np.max(np.abs(actual-expected)) < 1e-12
    assert abs(np.trace(actual)-1) < 1e-12


def test_old_transverse_normalization_loses_two_thirds_of_mass():
    source = c.oracle_source("proper_intersection")
    assumed_mass = sum(1/9 for label in c.CENTER if label[0] == 0)
    assert assumed_mass == 1/3
    assert abs(np.trace(source)-1) < 1e-12


def test_zero_scale_and_bad_moment_do_not_pass():
    branches = c.measured_branches("proper_intersection")
    tau = branches[(0, 1)]*3
    zero = c.discard_gram(tau, 0, True)
    assert np.max(np.abs(zero-1)) < 1e-12
    target = np.array([[q[1] == r[1] for r in c.ADDRESSES] for q in c.ADDRESSES])
    assert np.max(np.abs(zero-target)) > .9
    bad = np.prod([c.discard_gram(branches[label]*3, s, True)
                   for label, s in zip([(0, 1), (0, 1), (0, 0)], (1, 2, 0))], axis=0)
    assert np.max(np.abs(bad-target)) > .9


def test_all_outcomes_receipt_keeps_zero_branches():
    report = c.audit()
    assert report["positive_records"] == 27
    assert report["zero_mass_records"] == 702
    assert abs(report["complete_record_mass"]-1) < 1e-12
    for key in ("maximum_record_entry_error", "complete_channel_entry_error", "kraus_completeness_error",
                "forbidden_branch_norm", "allowed_mass_error"):
        assert report[key] < 1e-12
    assert not report["new_algorithm_or_speedup_claim"] and not report["quantum_execution"]
