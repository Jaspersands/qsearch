from itertools import product
import numpy as np
import pytest

from physical_channel import Fixture, apply_with_reference, audit, bounded_scales, choi, correlated_bank_control, trace_distance


def setup():
    fixture = Fixture()
    return fixture, fixture.central_branches(fixture.oracle_source(lambda g: g[1:]))


def test_actual_translations_form_right_regular_representation():
    fixture = Fixture()
    rng = np.random.default_rng(991)
    vector = rng.normal(size=27)+1j*rng.normal(size=27)
    for a, b in product(fixture.group, repeat=2):
        assert np.array_equal(fixture.right_translate(fixture.right_translate(vector, b), a),
                              fixture.right_translate(vector, fixture.mul(a, b)))


def test_source_and_complete_projective_mass():
    fixture, branches = setup()
    source = fixture.oracle_source(lambda g: g[1:])
    assert len(source) == 9
    assert abs(sum(w for w, _ in source)-1) < 1e-12
    assert set(branches) == {0, 1, 2}
    for mass, branch in branches.values():
        assert abs(mass-1/3) < 1e-12
        density = sum(w*np.outer(v, v.conj()) for w, v in branch)
        assert abs(np.trace(density)-1) < 1e-12
        assert np.linalg.eigvalsh(density)[0] >= -1e-12


@pytest.mark.parametrize("twisted", [False, True])
def test_every_label_tuple_and_every_address_pair(twisted):
    fixture, branches = setup()
    total = 0
    for labels in product(range(3), repeat=3):
        scales = bounded_scales(labels)
        assert any(scales) and sum(a*b*b for a, b in zip(labels, scales)) % 3 == 0
        mass, gram = fixture.packet_gram(branches, labels, scales, twisted)
        assert np.max(np.abs(gram-fixture.ideal_gram())) < 1e-12
        assert np.max(np.abs(np.diag(gram)-1)) < 1e-12
        assert np.linalg.eigvalsh(gram)[0] >= -1e-12
        total += mass
    assert abs(total-1) < 1e-12


@pytest.mark.parametrize("reference_dimension", [1, 3, 9])
def test_entangled_reference_complete_channel(reference_dimension):
    fixture, branches = setup()
    rng = np.random.default_rng(702)
    dimension = 9*reference_dimension
    matrix = rng.normal(size=(dimension, 4))+1j*rng.normal(size=(dimension, 4))
    density = matrix@matrix.conj().T
    density /= np.trace(density)
    expected = apply_with_reference(fixture.ideal_gram(), density, reference_dimension)
    actual = np.zeros_like(density)
    for labels in product(range(3), repeat=3):
        mass, gram = fixture.packet_gram(branches, labels, bounded_scales(labels))
        output = apply_with_reference(gram, density, reference_dimension)
        assert trace_distance(output, expected) < 1e-12
        actual += mass*output
    assert trace_distance(actual, expected) < 1e-12
    assert abs(np.trace(actual)-1) < 1e-12


def test_target_reuse_is_identity_not_coset_pinching():
    fixture, branches = setup()
    assert sum([1, 1, 1]) % 3 == 0
    reused = fixture.branch_gram(branches[1][1], 1, repetitions=3)
    assert np.max(np.abs(reused-1)) < 1e-12
    assert abs(trace_distance(choi(reused), choi(fixture.ideal_gram()))-2/3) < 1e-12
    _, independent = fixture.packet_gram(branches, (1, 1, 1), (1, 1, 1))
    assert trace_distance(choi(independent), choi(fixture.ideal_gram())) < 1e-12


def test_zero_packet_and_wrong_degree_are_not_valid_replacements():
    fixture, branches = setup()
    _, zero = fixture.packet_gram(branches, (1, 1, 1), (0, 0, 0))
    assert np.max(np.abs(zero-1)) < 1e-12
    labels, weights = (1, 1, 0), (1, 2, 0)
    assert sum(a*b for a, b in zip(labels, weights)) % 3 == 0
    assert sum(a*b*b for a, b in zip(labels, weights)) % 3 != 0
    _, invalid = fixture.packet_gram(branches, labels, weights)
    _, section_changed = fixture.packet_gram(branches, labels, weights, True)
    # This particular untwisted section accidentally suppresses the bad phase.
    assert trace_distance(choi(invalid), choi(fixture.ideal_gram())) < 1e-12
    assert trace_distance(choi(section_changed), choi(fixture.ideal_gram())) > .1
    assert trace_distance(choi(invalid), choi(section_changed)) > .1


def test_nonhomogeneous_h_without_rees_lift_fails_despite_correct_moment():
    fixture = Fixture()
    branches = fixture.central_branches(fixture.oracle_source(lambda g: (g[1], (g[2]-g[0]) % 3)))
    labels, weights = (1, 2, 0), (1, 2, 0)
    assert sum(a*b*b for a, b in zip(labels, weights)) % 3 == 0
    _, actual = fixture.packet_gram(branches, labels, weights)
    assert trace_distance(choi(actual), choi(fixture.ideal_gram())) > .1


def test_correct_raw_and_conditional_marginals_do_not_certify_joint_source():
    report = correlated_bank_control()
    assert report["moment_mod_3"] == 0
    assert abs(report["central_record_mass"]-1/9) < 1e-12
    assert report["raw_single_target_maximum_error"] < 1e-12
    assert report["conditional_single_target_maximum_error"] < 1e-12
    assert report["joint_output_identity_channel_error"] < 1e-12
    assert abs(report["joint_choi_trace_distance_from_required_pinching"]-8/9) < 1e-12
    assert report["independent_bank_choi_trace_distance"] < 1e-12


def test_receipt_preserves_all_records_and_no_speedup_promotion():
    report = audit()
    assert len(report["all_positive_adaptive_label_tuples"]) == 27
    assert abs(report["complete_instrument_mass"]-1) < 1e-12
    assert report["complete_cq_choi_trace_distance"] < 1e-12
    assert not report["scalable_quantum_receiver_implemented"]
    assert not report["quantum_device_executed"] and not report["speedup_claim"]
