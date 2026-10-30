"""Exact public maps and small actual wedge measurements, not a full learner."""
from fractions import Fraction
from itertools import product
from math import factorial
import random

import numpy as np
import pytest

from theorems.exterior_phase_learning import (
    exterior_line_packet, inverse_translation_sum, noisy_copy_envelope,
    report, translated_frame, translation_sum_matrix,
)
from theorems.polynomial_phase_copy_learning import LearningFrame


def _evaluate(frame, coefficients, point):
    return sum(c*np.prod([pow(x, a, frame.p) for x, a in zip(point, alpha)],
                        dtype=object)
               for c, alpha in zip(coefficients, frame.indices)) % frame.p


def _phase(frame, coefficients):
    points = tuple(product(range(frame.p), repeat=frame.width))
    return np.array([np.exp(2j*np.pi*int(_evaluate(frame, coefficients, x))/frame.p)
                     for x in points])/np.sqrt(len(points))


def _components(frame, coefficients, labels):
    points = tuple(product(range(frame.p), repeat=frame.width))
    phase = _phase(frame, coefficients)
    return np.array([phase*np.array([np.exp(2j*np.pi*sum(b*x for b, x in zip(label, point))
                                            /frame.p) for point in points])
                     for label in labels])


def _wedge_branches(frame, coefficients, labels):
    """Construct all original amplitudes, then apply the actual permutation."""
    points = tuple(product(range(frame.p), repeat=frame.width))
    rank, dimension = len(labels), len(points)
    assert dimension**rank <= 20000
    components = _components(frame, coefficients, labels)
    branches = {}
    for indices in product(range(dimension), repeat=rank):
        amplitude = np.linalg.det(components[:, indices].T)/np.sqrt(factorial(rank))
        t = points[indices[-1]]
        offsets = tuple(tuple((x-y) % frame.p for x, y in zip(points[i], t))
                        for i in indices[:-1])
        branches.setdefault(offsets, np.zeros(dimension, dtype=complex))[indices[-1]] = amplitude
    return branches


def _density(frame, coefficients, labels, weights=None):
    components = _components(frame, coefficients, labels)
    if weights is None:
        weights = [1/len(labels)]*len(labels)
    return sum(w*np.outer(state, state.conj()) for w, state in zip(weights, components))


@pytest.mark.parametrize("p,width,degree,labels", [
    (5, 1, 3, ((0,), (1,))),
    (5, 1, 2, ((0,), (1,), (3,))),
    (3, 2, 2, ((0, 0), (1, 2))),
    (3, 2, 2, ((0, 0), (0, 1), (1, 0), (1, 1))),
    (5, 1, 3, ((2,),)),
])
def test_actual_wedge_measurement_produces_publicly_transformed_common_polynomial(
        p, width, degree, labels):
    frame = LearningFrame.initial(p, width, degree)
    coefficients = tuple((i*i+1) % p for i in range(len(frame.known)))
    branches = _wedge_branches(frame, coefficients, labels)
    rank = len(labels)
    linear_shift = tuple(sum(b[j] for b in labels)*pow(rank, -1, p) % p for j in range(width))
    common = tuple((c+sum(linear_shift[j] for j in range(width)
                          if alpha == tuple(int(k == j) for k in range(width)))) % p
                   for alpha, c in zip(frame.indices, coefficients))
    common_frame = LearningFrame(p, width, degree, common, ())
    total_mass = 0
    for offsets, branch in branches.items():
        mass = float(np.vdot(branch, branch).real)
        total_mass += mass
        rows = (*offsets, (0,)*width)
        det = np.linalg.det(np.array([[np.exp(2j*np.pi*sum(b*x for b, x in zip(label, u))/p)
                                       for label in labels] for u in rows]))
        assert mass == pytest.approx(abs(det)**2/(factorial(rank)*p**(width*(rank-1))), abs=1e-12)
        if mass < 1e-14:
            continue
        changed = translated_frame(common_frame, offsets)
        expected = _phase(frame, changed.known)
        assert abs(np.vdot(expected, branch/np.sqrt(mass))) == pytest.approx(1, abs=1e-11)
        assert abs(branch/np.sqrt(mass))**2 == pytest.approx(np.full(p**width, 1/p**width))
    assert total_mass == pytest.approx(1)


def test_relative_outcomes_are_independent_of_phase_but_not_uniform_and_cannot_be_ignored():
    frame = LearningFrame.initial(5, 1, 3)
    labels = ((0,), (1,))
    left = _wedge_branches(frame, (0, 0, 0), labels)
    right = _wedge_branches(frame, (0, 0, 1), labels)
    masses = []
    forgotten = np.zeros((5, 5), dtype=complex)
    for u, branch in right.items():
        mass = np.vdot(branch, branch).real
        assert mass == pytest.approx(np.vdot(left[u], left[u]).real)
        masses.append(mass)
        forgotten += np.outer(branch, branch.conj())
    assert min(masses) == pytest.approx(0)
    assert max(masses)-sorted(masses)[1] > 0.1
    assert np.trace(forgotten@forgotten).real < 0.9


def test_independent_raw_copies_cannot_replace_top_wedge():
    frame = LearningFrame.initial(5, 1, 3)
    rho = _density(frame, (0, 0, 1), ((0,), (1,)))
    u = 1
    # Condition the actual rho tensor rho on x1-x2=u, without antisymmetrizing.
    branch = np.array([[rho[(t+u) % 5, (s+u) % 5]*rho[t, s]
                        for s in range(5)] for t in range(5)])
    assert np.trace(branch).real == pytest.approx(1/5)
    branch /= np.trace(branch)
    assert np.trace(branch@branch).real < 0.9


@pytest.mark.parametrize("p,width,labels", [
    (5, 1, ((0,), (1,), (3,))), (3, 2, ((0, 0), (1, 2))),
])
def test_quadratic_centroid_really_decouples_relative_registers(p, width, labels):
    frame = LearningFrame.initial(p, width, 2)
    coefficients = tuple((i+1) % p for i in range(len(frame.known)))
    rank = len(labels)
    expected_coefficients = tuple(
        (rank*c+sum(sum(label[j] for label in labels)
                    for j in range(width) if alpha == tuple(int(k == j) for k in range(width)))) % p
        for alpha, c in zip(frame.indices, coefficients))
    target = _phase(frame, expected_coefficients)
    points = tuple(product(range(p), repeat=width))
    index = {point: i for i, point in enumerate(points)}
    discarded = np.zeros((p**width, p**width), dtype=complex)
    for offsets, branch in _wedge_branches(frame, coefficients, labels).items():
        mean = tuple(sum(u[j] for u in offsets)*pow(rank, -1, p) % p for j in range(width))
        centered = np.array([branch[index[tuple((v-m) % p for v, m in zip(point, mean))]]
                             for point in points])
        discarded += np.outer(centered, centered.conj())
    assert np.allclose(discarded, np.outer(target, target.conj()), atol=1e-12)


def test_ordinary_bell_measurements_are_uninformative_for_invertible_quadratic():
    p = 5
    frame = LearningFrame.initial(p, 1, 2)
    for quadratic in range(1, p):
        states = _components(frame, (0, quadratic), ((0,), (1,)))
        probabilities = []
        for y, z in product(range(p), repeat=2):
            mass = 0
            for left, right in product(states, repeat=2):
                amplitude = sum(np.exp(-2j*np.pi*z*x/p)*left[x]*right[(x+y) % p]
                                for x in range(p))/np.sqrt(p)
                mass += abs(amplitude)**2/4
            probabilities.append(mass)
        assert probabilities == pytest.approx([1/p**2]*p**2)


def test_four_paid_copy_instrument_has_exact_noisy_regression_law():
    p, hessian, linear = 3, 1, 2
    scales = (2, 0, 2, 2)
    assert sum(scales) % p == sum(a*a for a in scales) % p == 0
    y_counts = [0]*p
    for outcomes in product(range(p), repeat=4):
        y = sum(a*mu for a, mu in zip(scales, outcomes)) % p
        y_counts[y] += 1
        for labels in product((0, 1), repeat=4):
            # Each input and the ancillary t register start with uniform modulus.
            amplitudes = []
            for t in range(p):
                coordinates = [(mu+a*t) % p for mu, a in zip(outcomes, scales)]
                phase = sum((hessian*pow(2, -1, p)*x*x+linear*x+b*x)
                            for x, b in zip(coordinates, labels)) % p
                amplitudes.append(np.exp(2j*np.pi*phase/p)/p**2.5)
            assert sum(abs(x)**2 for x in amplitudes) == pytest.approx(p**-4)
            distribution = abs(np.fft.fft(np.array(amplitudes)*p**2)/np.sqrt(p))**2
            error = sum(a*b for a, b in zip(scales, labels)) % p
            assert distribution[(hessian*y+error) % p] == pytest.approx(1)
    assert y_counts == [p**3]*p


def test_weighted_pauli_overlap_and_nonzero_shift_gap_are_actual_density_identities():
    p, width = 5, 1
    frame = LearningFrame.initial(p, width, 2)
    hessian = 2
    labels = ((0,), (1,), (3,))
    weights = (Fraction(1, 2), Fraction(1, 3), Fraction(1, 6))
    rho = _density(frame, (0, 1), labels, list(map(float, weights)))
    weight = {label[0]: w for label, w in zip(labels, weights)}
    purity = np.trace(rho@rho).real
    for y, z in product(range(p), repeat=2):
        shift = np.roll(np.eye(p), y, axis=0)
        pauli = np.diag(np.exp(2j*np.pi*z*np.arange(p)/p))@shift
        overlap = np.trace(rho@pauli@rho@pauli.conj().T).real
        f = (z-hessian*y) % p
        exact = sum(weight.get(b, 0)*weight.get((b-f) % p, 0) for b in range(p))
        assert overlap == pytest.approx(float(exact))
        if f:
            assert purity-overlap >= float(Fraction(1, 2*len(labels)**3))-1e-12
        else:
            assert overlap == pytest.approx(purity)


def test_flat_symplectic_verifier_needs_no_hidden_hessian_and_separates_wrong_candidates():
    p, rank, hessian = 5, 2, 3
    scales = (3, 4, 1, 2)
    error_counts = [0]*p
    for labels in product(range(rank), repeat=4):
        error_counts[sum(a*b for a, b in zip(scales, labels)) % p] += 1
    validation = [(y, (hessian*y+e) % p, count)
                  for y in range(p) for e, count in enumerate(error_counts) if count]
    for y, z in product(range(p), repeat=2):
        zero_mass = Fraction(sum(count for Y, Z, count in validation if (y*Z-z*Y) % p == 0),
                             p*rank**4)
        deviation = abs(zero_mass-Fraction(1, p))
        if z == hessian*y % p:
            assert deviation >= Fraction(1, 2*rank**7)
        else:
            assert deviation == 0


@pytest.mark.parametrize("weights,expected", [
    ((Fraction(1, 2), Fraction(1, 2)), Fraction(1, 4)),
    ((Fraction(1, 3), Fraction(2, 3)), Fraction(1, 3)),
])
def test_one_sided_and_arbitrary_weight_zero_frequency_extensions_are_false(weights, expected):
    p, scales = 3, (2, 0, 2, 2)
    probability = Fraction(0)
    for labels in product((0, 1), repeat=4):
        if sum(a*b for a, b in zip(scales, labels)) % p == 0:
            mass = Fraction(1)
            for b in labels:
                mass *= weights[b]
            probability += mass
    assert probability == expected
    # A true y=1 candidate need not exceed the wrong-candidate frequency.
    assert probability <= Fraction(1, p)


@pytest.mark.parametrize("p,width,degree,offsets", [
    (5, 1, 3, ()), (5, 2, 3, ((1, 4),)),
    (3, 2, 2, ((0, 1), (1, 1), (2, 1))),
    (101, 3, 4, ((1, 2, 3), (4, 5, 6))),
    (2**127-1, 2, 3, ((1, 2),)),
])
def test_exact_translation_inverse_and_evaluation_mod_constant(p, width, degree, offsets):
    frame = LearningFrame.initial(p, width, degree)
    rng = random.Random(301026)
    values = tuple(rng.randrange(p) for _ in frame.known)
    changed = translated_frame(LearningFrame(p, width, degree, values, ()), offsets)
    assert inverse_translation_sum(p, width, degree, iter(offsets), changed.known) == values
    for _ in range(8):
        point = tuple(rng.randrange(p) for _ in range(width))
        actual = _evaluate(frame, changed.known, point)
        expected = sum(_evaluate(frame, values, tuple((a+b) % p for a, b in zip(point, u)))
                       - _evaluate(frame, values, u) for u in (*offsets, (0,)*width)) % p
        assert actual == expected


def test_packets_keep_common_unknowns_after_frame_updates_and_different_offsets(monkeypatch):
    frame = LearningFrame.initial(5, 2, 3)
    eta = tuple((i+2) % 5 for i in range(len(frame.basis)))
    relation = (1, 2)+(0,)*(len(eta)-2)
    frame = frame.learn_relation(relation, sum(a*b for a, b in zip(relation, eta)) % 5)
    eta = eta[1:]
    common = tuple((c+sum(a*v[i] for a, v in zip(eta, frame.basis))) % 5
                   for i, c in enumerate(frame.known))
    axis = frame.next_axis()
    for offsets in (((1, 2),), ((3, 4),), ((0, 0),)):
        full = translated_frame(LearningFrame(5, 2, 3, common, ()), offsets)
        for y in range(5):
            correction, packet = exterior_line_packet(frame, offsets, axis, (y,))
            frame.check_coordinate_packet(axis, packet)
            differences = []
            for t in range(5):
                point = (t, y) if axis == 0 else (y, t)
                corrected = (_evaluate(frame, full.known, point)
                             - sum(c*pow(t, r, 5) for r, c in enumerate(correction))) % 5
                differences.append((corrected-packet.evaluate_fixture((t,), eta)) % 5)
            assert len(set(differences)) == 1  # Global phase only.
    # Public preparation does not call the diagnostic hidden-phase evaluator.
    monkeypatch.setattr(type(packet), "evaluate_fixture", lambda *a: pytest.fail("hidden access"))
    exterior_line_packet(frame, ((1, 2),), axis, (3,))


def test_axis_acceptance_lower_bound_survives_all_translation_records():
    initial = LearningFrame.initial(5, 2, 3)
    # An unknown coefficient on x0*(x1-1)*(x1-2), including rejecting slices.
    polynomial = {(1, 2): 1, (1, 1): 2, (1, 0): 2}
    basis = tuple(polynomial.get(alpha, 0) for alpha in initial.indices)
    frame = LearningFrame(5, 2, 3, initial.known, (basis,))
    for offset in product(range(5), repeat=2):
        packets = [exterior_line_packet(frame, (offset,), 0, (y,))[1] for y in range(5)]
        assert sum(bool(packet.degree) for packet in packets) >= 3


def test_rank_divisible_by_characteristic_can_erase_nonlinear_information():
    frame = LearningFrame.initial(3, 2, 2)
    quadratic = tuple(int(alpha == (2, 0)) for alpha in frame.indices)
    labels = ((0, 0), (1, 0), (2, 0))
    assert np.allclose(_density(frame, frame.known, labels), _density(frame, quadratic, labels))
    with pytest.raises(ValueError, match="nonzero modulo"):
        noisy_copy_envelope(3, 2, 2, 3)


def test_nonuniform_nearly_periodic_support_has_no_rank_only_robustness():
    frame = LearningFrame.initial(3, 2, 2)
    quadratic = tuple(int(alpha == (2, 0)) for alpha in frame.indices)
    labels = ((0, 0), (1, 0), (2, 0), (0, 1))  # Rank 4 is nonzero modulo 3.
    epsilon = 1/256
    weights = [(1-epsilon)/3]*3+[epsilon]
    delta = _density(frame, frame.known, labels, weights)-_density(frame, quadratic, labels, weights)
    distance = sum(abs(np.linalg.eigvalsh(delta)))/2
    assert 0 < distance <= epsilon+1e-14


@pytest.mark.parametrize("rank", [1, 2, 8])
def test_composed_budget_charges_raw_copies_growth_and_all_error_accounts(rank):
    budget = noisy_copy_envelope(101, 2, 3, rank, Fraction(1, 5))
    assert budget["raw_noisy_copy_cap"] == budget["top_wedge_output_cap"]+budget["growth_attempt_cap"]
    assert budget["sde_call_cap"]*budget["required_sde_abort_per_call"] == Fraction(1, 20)
    assert budget["total_error_upper_bound"] <= Fraction(1, 5)
    if rank == 1:
        assert budget["growth_attempt_cap"] == budget["wedge_abort_bound"] == 0
    assert not budget["full_quantum_backend_implemented"]
    assert not budget["source_promise_certified"]
    assert not budget["rees_receiver_required"]


@pytest.mark.parametrize("p,width,degree,offsets", [
    (9, 1, 2, ()), (5, 0, 2, ()), (5, 1, 5, ()),
    (5, 1, 2, ((-1,),)), (5, 1, 2, ((True,),)),
    (5, 2, 2, ((1,),)), (3, 1, 2, ((0,), (1,))),
    (3, 1, 2, ((0,), (1,), (2,))),
])
def test_invalid_public_maps_fail_closed(p, width, degree, offsets):
    with pytest.raises(ValueError):
        translation_sum_matrix(p, width, degree, offsets)


def test_cli_scopes_artifact_does_not_overwrite_pure_baseline_and_binds_sources(tmp_path, capsys):
    import hashlib
    import json
    from pathlib import Path
    import qsearch

    pure = tmp_path/"research/reductions/polynomial_phase_copy_learning.json"
    pure.parent.mkdir(parents=True)
    pure.write_text("prior pure baseline")
    args = qsearch.build_parser().parse_args(["phase-copy-baseline", "--phase-noise", "--write"])
    args.root = tmp_path
    assert args.func(args) == 0
    saved = json.loads((pure.parent/"exterior_phase_learning.json").read_text())
    assert json.loads(capsys.readouterr().out) == saved
    assert pure.read_text() == "prior pure baseline"
    for flag in ("quantum_source_prepared", "quantum_learning_run", "novelty_established",
                 "classical_hardness_established", "standard_lwe_reduction", "rees_receiver_required"):
        assert saved[flag] is False
    root = Path(qsearch.__file__).resolve().parent
    for path, digest in saved["source_sha256"].items():
        assert hashlib.sha256((root/path).read_bytes()).hexdigest() == digest
    assert not (tmp_path/"research/registry/candidates.json").exists()


def test_cli_read_only_without_write_and_original_mode_still_dispatches(tmp_path, capsys, monkeypatch):
    import qsearch
    import theorems.exterior_phase_learning as exterior
    import theorems.polynomial_phase_copy_learning as pure

    monkeypatch.setattr(exterior, "report", lambda: {"mode": "exterior"})
    monkeypatch.setattr(pure, "report", lambda: {"mode": "pure"})
    for arguments, mode in ((["--phase-noise"], "exterior"), ([], "pure")):
        args = qsearch.build_parser().parse_args(["phase-copy-baseline", *arguments])
        args.root = tmp_path
        assert args.func(args) == 0
        assert mode in capsys.readouterr().out
        assert not list(tmp_path.iterdir())
