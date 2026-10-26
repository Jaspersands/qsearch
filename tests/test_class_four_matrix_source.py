"""Variable-radical and label-selection controls, not a general HSP execution."""
from collections import Counter
from fractions import Fraction
from itertools import product
import random

import numpy as np
import pytest

from theorems.affine_phase_erasure import square_weights
from theorems.class_four_matrix_source import (
    align_variable_jets, factor_alternating, label_coordinates,
    rank_failure_bound, variable_jet_maps,
)
from theorems.ut5_matrix_phase_alignment import _matrix, _rank, symplectic_pair, verify_alignment
from theorems.class_four_scalar_phase_compiler import compile_variable_scalar_packet


def forms3(p):
    result = []
    for i, j in ((0, 1), (0, 2), (1, 2)):
        F = [[0]*3 for _ in range(3)]
        F[i][j], F[j][i] = 1, p-1
        result.append(F)
    return result


def mv(matrix, vector, p):
    return [sum(a*b for a, b in zip(row, vector)) % p for row in matrix]


def blocks(p, z, w, m, seed, count=None):
    rng = random.Random(seed)
    labels, scales, outcomes = [], [], []
    count = 2*w*(m+2)+2 if count is None else count
    for _ in range(count):
        pool = []
        while len(pool) < (z+1)**2:
            label = [rng.randrange(p) for _ in range(z)]
            if any(label):
                pool.append(label)
        beta = square_weights(p, pool, rng)
        multiplier = rng.randrange(1, p)
        scales.extend(multiplier*pow(b, (p+1)//4, p) % p for b in beta)
        labels.extend(pool)
        outcomes.extend([[rng.randrange(p) for _ in range(m)] for _ in pool])
    return labels, scales, outcomes


@pytest.mark.parametrize("p", [5, 7])
def test_every_nonzero_three_dimensional_form_is_singular_but_common_radical_is_zero(p):
    forms = forms3(p)
    assert _rank([row for F in forms for row in F], p) == 3
    radicals = set()
    for label in product(range(p), repeat=3):
        coordinates = label_coordinates(p, forms, label)
        assert coordinates.qudits == int(any(label))
        basis = coordinates.weyl+coordinates.radical
        assert _rank(basis, p) == 3
        F = [[sum(c*A[i][j] for c, A in zip(label, forms)) % p for j in range(3)] for i in range(3)]
        columns = list(zip(*coordinates.weyl)) if coordinates.weyl else [()] * 3
        assert [[symplectic_pair(a, b, p) for b in columns] for a in columns] == F
        if any(label):
            kernel = _matrix(F, p).rref()[0]
            radicals.add(tuple(int(kernel[i, j]) for i in range(3) for j in range(3)))
    assert len(radicals) > p


def test_odd_noncentral_width_occurs_in_a_real_class_four_free_lie_derived_group():
    # Truncated free associative words give a characteristic-zero independent
    # realization. No hand-entered nilpotent bracket table is assumed.
    def bracket(a, b):
        result = Counter()
        for u, x in a.items():
            for v, y in b.items():
                if len(u+v) <= 4:
                    result[u+v] += x*y
                    result[v+u] -= x*y
        return {word: value for word, value in result.items() if value}
    generators = [{(j,): 1} for j in range(3)]
    derived2 = [bracket(generators[i], generators[j]) for i, j in ((0, 1), (0, 2), (1, 2))]
    derived_brackets = [bracket(derived2[i], derived2[j]) for i, j in ((0, 1), (0, 2), (1, 2))]
    words = list(product(range(3), repeat=4))
    assert _rank([[value.get(word, 0) % 7 for word in words] for value in derived_brackets], 7) == 3
    third = bracket(generators[0], derived2[0])
    assert third
    assert all(not bracket(third, a) for a in derived2)
    assert bracket(generators[0], third)
    # Degree >=3 is central inside the derived algebra; its degree-two
    # quotient is the three-dimensional variable-radical space above.


def test_row_space_canonicalization_makes_quartic_selection_equivariant():
    p, z = 7, 2
    rng = random.Random(4)
    labels = []
    while len(labels) < 9:
        label = [rng.randrange(p) for _ in range(z)]
        if any(label):
            labels.append(label)
    beta = square_weights(p, labels, random.Random(9))
    active = next(i for i, b in enumerate(beta) if b)
    counts, biased = Counter(), Counter()
    for entries in product(range(p), repeat=4):
        a, b, c, d = entries
        if (a*d-b*c) % p == 0:
            continue
        transformed = [[(a*x+b*y) % p, (c*x+d*y) % p] for x, y in labels]
        # Verify all 2016 GL_2 transformations, not a random subset.
        assert square_weights(p, transformed, random.Random(9)) == beta
        counts[tuple(transformed[active])] += 1
        chosen = next((v for v in transformed if v[0] == 0), transformed[0])
        biased[tuple(chosen)] += 1
    assert len(counts) == p*p-1
    assert set(counts.values()) == {p*(p-1)}
    assert len(set(biased.values())) > 1


def test_label_dependent_abort_keeps_valid_witnesses_but_biases_selected_label():
    p = 7
    before, after = Counter(), Counter()
    for labels in product(range(1, p), repeat=4):
        gamma = square_weights(p, [[a] for a in labels], random.Random(11))
        beta = [pow(g, (p+1)//4, p) for g in gamma]
        assert any(beta)
        assert sum(a*pow(b, 4, p) for a, b in zip(labels, beta)) % p == 0
        active = next(i for i, b in enumerate(beta) if b)
        selected = labels[active]
        before[selected] += 1
        # This mimics a forbidden label-dependent success/timeout filter.
        if selected == 1:
            after[selected] += 1
    assert set(before.values()) == {(p-1)**3}
    assert set(before) == set(range(1, p))
    assert dict(after) == {1: (p-1)**3}


def test_uniform_block_marginals_do_not_justify_product_rank_bound():
    p, block_count = 5, 4
    labels = [a for a in product(range(p), repeat=2) if any(a)]
    bad = [a for a in labels if not any(mv(
        label_coordinates(p, forms3(p)[:2], a).weyl, [0, 1, 0], p))]
    marginal = Fraction(len(bad), len(labels))
    assert marginal == Fraction(1, p+1)
    # Separate draws give marginal^B. Copying one draw into every block
    # keeps each marginal exactly uniform but the joint failure is marginal.
    independent = marginal**block_count
    shared = marginal
    assert independent <= Fraction(2, p)**block_count < shared
    # Conditioning independent draws on equality produces that same bad law;
    # the acceptance event is global, not a product of local block events.
    equal_pairs = [(a, b) for a in labels for b in labels if a == b]
    assert Counter(a for a, _ in equal_pairs) == Counter(labels)
    assert Fraction(sum(a in bad and b in bad for a, b in equal_pairs),
                    len(equal_pairs)) == marginal


@pytest.mark.parametrize("derivative", [True, False])
def test_single_block_bad_vector_probability_has_the_two_over_p_bound(derivative):
    p = 5
    forms = forms3(p)[:2]
    count = total = 0
    for label in product(range(p), repeat=2):
        if not any(label):
            continue
        D = label_coordinates(p, forms, label).weyl
        for tau in range(1, p):
            for Y in range(p):
                # Derivative case achieves 2/(p+1); the constant case tests
                # the separate independent nonzero block-rescaling argument.
                vector = [0, Y, 0] if derivative else [0, tau, 1]
                total += 1
                count += int(not any(mv(D, vector, p)))
    assert Fraction(count, total) <= Fraction(2, p)
    if derivative:
        assert Fraction(count, total) == Fraction(2, p+1)


@pytest.mark.parametrize("w,m", [(3, 1), (3, 4), (9, 8)])
def test_conservative_block_schedule_has_constant_rank_success(w, m):
    for p in (5, 7, 11, 2**127-1):
        assert rank_failure_bound(p, w, m, 2*w*(m+2)+2) <= Fraction(1, p)


@pytest.mark.parametrize("seed", [11, 18])
def test_alignment_handles_varying_radicals_without_hidden_coefficients(seed):
    p, w, m = 7, 3, 1
    labels, scales, outcomes = blocks(p, 3, w, m, seed)
    alignment = align_variable_jets(p, forms3(p), labels, scales, outcomes)
    assert verify_alignment(alignment)
    assert alignment.maps.noncentral_width == 3
    assert all(c.qudits == 1 for c in alignment.maps.representations)
    R, D = alignment.maps.carrier_width, alignment.maps.jet_width
    L, B, constant = [1, 2, 3], [3, 0, 2], [4, 6, 1]
    def displacement(q):
        raw = [0]*(2*R)
        start = 0
        for i, coordinates in zip(alignment.maps.active_indices, alignment.maps.representations):
            t = (outcomes[i][0]+scales[i]*q) % p
            value = [(c+l*t+pow(2, -1, p)*b*t*t) % p for c, l, b in zip(constant, L, B)]
            v = mv(coordinates.weyl, value, p)
            s = coordinates.qudits
            raw[start:start+s] = v[:s]
            raw[R+start:R+start+s] = v[s:]
            start += s
        return mv(alignment.symplectic, raw, p)
    origin = displacement(0)
    for q in range(p):
        output = [(x-y) % p for x, y in zip(displacement(q), origin)]
        assert output[:D] == [v*q % p for v in L+B]
        assert output[D:R] == [0]*(R-D)


def test_nonzero_labels_with_zero_weyl_rank_are_kept_and_padding_is_accounted():
    p, m = 7, 1
    forms = forms3(p)[:2]+[[[0]*3 for _ in range(3)]]
    labels, scales, outcomes = blocks(p, 3, 3, m, 21, count=8)
    # Add a cancelling pair of one-dimensional representations. Nonzero
    # central labels need NOT have nonzero alternating rank.
    labels += [[0, 0, 1], [0, 0, p-1]]
    scales += [1, 1]
    outcomes += [[0], [1]]
    maps = variable_jet_maps(p, forms, labels, scales, outcomes)
    assert maps.representations[-1].qudits == 0
    assert len(maps.representations[-1].radical) == 3
    assert maps.source_carrier_width == sum(c.qudits for c in maps.representations)
    assert maps.carrier_width >= maps.jet_width+maps.noncentral_width
    assert maps.mixed_padding_qudits == maps.carrier_width-maps.source_carrier_width


def test_common_radical_and_constant_scales_do_not_pass_the_rank_gate():
    p = 7
    labels, scales, outcomes = blocks(p, 1, 3, 1, 11, count=8)
    with pytest.raises(ValueError, match="common radical"):
        variable_jet_maps(p, forms3(p)[:1], labels, scales, outcomes)
    labels = [[1, 0, 0], [p-1, 0, 0]]*12
    outcomes = [[i % p] for i in range(len(labels))]
    with pytest.raises(ValueError, match="rank deficient"):
        variable_jet_maps(p, forms3(p), labels, [1]*len(labels), outcomes)


def test_three_mixed_padding_qudits_make_an_injective_small_design_alignable():
    p = 7
    labels = [[int(j == i)*sign % p for j in range(3)] for i in range(3) for sign in (1, -1)]
    scales = [1, 1, 2, 2, 3, 3]
    outcomes = [[i] for i in range(6)]
    alignment = align_variable_jets(p, forms3(p), labels, scales, outcomes)
    maps = alignment.maps
    assert maps.source_carrier_width == 6
    assert maps.jet_width == 6
    assert maps.carrier_width == 9
    assert maps.mixed_padding_qudits == 3
    assert verify_alignment(alignment)
    for row in list(range(6, 9))+list(range(15, 18)):
        assert not any(maps.quadratic[row]) and not any(maps.linear[row])


def test_variable_radical_qft_fiber_and_radical_character_are_not_optional():
    p = 5
    points = list(product(range(p), repeat=3))
    coordinates = label_coordinates(p, forms3(p), [1, 0, 0])
    omega = np.exp(2j*np.pi/p)
    transform = np.zeros((p**3, p**3), dtype=complex)
    for row, (alpha, i, j) in enumerate(points):
        for col, v in enumerate(points):
            x, z = mv(coordinates.weyl, v, p)
            t, = mv(coordinates.radical, v, p)
            if i == (j+x) % p:
                transform[row, col] = omega**(-(alpha*t+x*z*pow(2, -1, p)+z*j) % p)/p
    np.testing.assert_allclose(transform @ transform.conj().T, np.eye(p**3), atol=1e-13)
    broken = transform.copy()
    # Forgetting alpha makes all radial-character rows duplicates.
    broken[p*p:2*p*p] = broken[:p*p]
    assert np.linalg.norm(broken @ broken.conj().T-np.eye(p**3)) > 1
    for label in product(range(p), repeat=3):
        c = label_coordinates(p, forms3(p), label)
        # Summed irrep dimension squared per central label is exactly p^w.
        assert p**len(c.radical) * p**(2*c.qudits) == p**3


def test_variable_radical_representation_respects_the_actual_class_two_group_law():
    p, label, alpha = 5, [1, 2, 3], [2]
    forms = forms3(p)
    coordinates = label_coordinates(p, forms, label)
    omega, half = np.exp(2j*np.pi/p), pow(2, -1, p)
    def representation(v, center):
        x, z = mv(coordinates.weyl, v, p)
        scalar = sum(a*b for a, b in zip(label, center))+sum(a*b for a, b in zip(alpha, mv(coordinates.radical, v, p)))
        result = np.zeros((p, p), dtype=complex)
        for j in range(p):
            result[(j+x) % p, j] = omega**((scalar+x*z*half+z*j) % p)
        return result
    rng = random.Random(22)
    for _ in range(30):
        v, w, a, b = [[rng.randrange(p) for _ in range(3)] for _ in range(4)]
        bracket = [sum(v[i]*F[i][j]*w[j] for i, j in product(range(3), repeat=2)) % p for F in forms]
        center = [(x+y+half*c) % p for x, y, c in zip(a, b, bracket)]
        np.testing.assert_allclose(representation(v, a) @ representation(w, b),
                                   representation([(x+y) % p for x, y in zip(v, w)], center), atol=1e-13)


def test_radical_character_terms_preserve_cubic_reduction_and_fixed_jets():
    p, w, m = 7, 3, 1
    labels, scales, outcomes = blocks(p, 3, w, m, 11, count=8)
    alignment = align_variable_jets(p, forms3(p), labels, scales, outcomes)
    R = alignment.maps.carrier_width
    # Coefficients by q-degree, independently expanded using the binomial
    # theorem. The generic symbolic compiler is deliberately not assumed.
    noncentral = [[1, 2, 3], [2, 0, 1], [3, 2, 0]]
    central = [[(j+1)*(degree+1) % p for degree in range(5)] for j in range(3)]
    raw = [[0]*3 for _ in range(2*R)]
    psi = [0]*5
    radial = [0]*3
    start = 0
    from math import comb
    for source, c in zip(alignment.maps.active_indices, alignment.maps.representations):
        s, y = scales[source], outcomes[source][0]
        translated = [[sum(coefficient*comb(degree, j)*s**j*y**(degree-j)
                           for degree, coefficient in enumerate(row) if degree >= j) % p
                       for j in range(3)] for row in noncentral]
        for j in range(3):
            value = mv(c.weyl, [row[j] for row in translated], p)
            raw[start][j], raw[R+start][j] = value
            # Nonzero alpha=1 on the one-dimensional radical in every irrep.
            radial[j] += mv(c.radical, [row[j] for row in translated], p)[0]
        for j in range(5):
            psi[j] += sum(label*coefficient*comb(degree, j)*s**j*y**(degree-j)
                          for label, row in zip(labels[source], central)
                          for degree, coefficient in enumerate(row) if degree >= j)
        start += c.qudits
    assert psi[4] % p == 0
    assert any(x % p for x in radial)
    transformed = [mv(alignment.symplectic, [row[j] for row in raw], p) for j in range(3)]
    assert transformed[2][:R] == [0]*R
    # Quadratic Z times at-most-linear X or one retained variable is cubic;
    # the omitted radical phase would change the polynomial, not its degree.
    assert transformed[1][:6] == [row[1] for row in noncentral]+[2*row[2] % p for row in noncentral]
    assert all(transformed[j][6:R] == [0]*(R-6) for j in (1, 2))


def symbolic_transcript(p, variant=0):
    """Finite reference transcripts, NOT a claimed random-sampling schedule."""
    forms = forms3(p)+[[[0]*3 for _ in range(3)]]
    columns = [[1, 0, 0, 2], [0, 1, 0, 3], [0, 0, 1, 4]]
    if variant:
        columns = [[1, 1, 0, 2], [0, 1, 1, 3], [1, 0, 1, 4]]
    columns += [[0, 0, 0, 1]] if not variant else [[1, 1, 1, 1]]*(variant+2)
    labels = [[sign*x % p for x in c] for c in columns for sign in (1, -1)]
    scales = [(j+1) % (p-1)+1 for j in range(len(columns)) for _ in range(2)]
    outcomes = [[(i+variant) % p] for i in range(len(labels))]
    alignment = align_variable_jets(p, forms, labels, scales, outcomes)
    characters = [
        [(j+i+1) % p for j in range(len(label_coordinates(p, forms, label).radical))]
        for i, label in enumerate(labels)]
    spectator = [(j+2) % p for j in range(alignment.maps.carrier_width-alignment.maps.jet_width)]
    return forms, labels, scales, outcomes, alignment, characters, spectator


@pytest.mark.parametrize("p", [7, 2**127-1])
def test_generic_symbolic_compiler_matches_gauges_across_variable_rank_batches(p):
    rng = random.Random(71)
    shared_basis, theta, source_widths = None, None, set()
    for variant in (0, 1, 2):
        forms, labels, scales, outcomes, alignment, alpha, spectator = symbolic_transcript(p, variant)
        packet = compile_variable_scalar_packet(alignment, forms, labels, scales, outcomes, alpha, spectator)
        assert packet.degree == 3
        assert packet.width == 7
        if shared_basis is None:
            shared_basis = packet.parameter_basis
            theta = [rng.randrange(p) for _ in shared_basis]
        else:
            assert packet.parameter_basis == shared_basis
        source_widths.add(alignment.maps.source_carrier_width)
        def Q(q):
            result = [0]*7
            for (coordinate, exponent), coefficient in zip(shared_basis, theta):
                result[coordinate] = (result[coordinate]+coefficient*pow(q, exponent[0], p)) % p
            return result
        R, D = alignment.maps.carrier_width, alignment.maps.jet_width
        for _ in range(12):
            point = [rng.randrange(p) for _ in range(packet.width)]
            raw, psi, start = [0]*(2*R), 0, 0
            for i, c in zip(alignment.maps.active_indices, alignment.maps.representations):
                value = Q((outcomes[i][0]+scales[i]*point[0]) % p)
                displacement = mv(c.weyl, value[:3], p)
                raw[start:start+c.qudits] = displacement[:c.qudits]
                raw[R+start:R+start+c.qudits] = displacement[c.qudits:]
                psi += sum(a*b for a, b in zip(labels[i], value[3:]))
                psi += sum(a*b for a, b in zip(alpha[i], mv(c.radical, value[:3], p)))
                start += c.qudits
            transformed = mv(alignment.symplectic, raw, p)
            A, B = transformed[:R], transformed[R:]
            expected = (-psi-pow(2, -1, p)*sum(a*b for a, b in zip(A, B))-
                        sum(b*t for b, t in zip(B, point[1:]+spectator))) % p
            assert packet.evaluate_fixture(point, theta) == expected
        assert all(len(parameters) <= 2 and sum(exponent) <= 3 for exponent, parameters in packet.terms)
        assert all(max(parameters) < 9 for _, parameters in packet.terms if len(parameters) == 2)
    assert len(source_widths) == 3


def test_zero_weyl_rank_still_contributes_an_observable_radical_phase():
    p = 7
    forms, labels, scales, outcomes, alignment, _, spectator = symbolic_transcript(p)
    alpha = [[0]*len(label_coordinates(p, forms, label).radical) for label in labels]
    base = compile_variable_scalar_packet(alignment, forms, labels, scales, outcomes, alpha, spectator)
    source = next(i for i, label in enumerate(labels) if label_coordinates(p, forms, label).qudits == 0)
    alpha[source][0] = 1
    changed = compile_variable_scalar_packet(alignment, forms, labels, scales, outcomes, alpha, spectator)
    theta = [0]*len(base.parameter_basis)
    theta[base.parameter_basis.index((0, (1,)))] = 1
    differences = [(changed.evaluate_fixture([q]+[0]*6, theta)-base.evaluate_fixture([q]+[0]*6, theta)) % p
                   for q in range(p)]
    assert differences == [(-outcomes[source][0]-scales[source]*q) % p for q in range(p)]
    assert len(set(differences)) == p


@pytest.mark.parametrize("defect", ["radical_width", "spectator_width", "transcript", "relation"])
def test_generic_compiler_rejects_incompatible_public_data(defect):
    p = 7
    forms, labels, scales, outcomes, alignment, alpha, spectator = symbolic_transcript(p)
    if defect == "radical_width":
        alpha[-1] = []
    elif defect == "spectator_width":
        spectator.append(0)
    elif defect == "transcript":
        outcomes[0][0] = (outcomes[0][0]+1) % p
    else:
        scales[0] = 0
    with pytest.raises(ValueError):
        compile_variable_scalar_packet(alignment, forms, labels, scales, outcomes, alpha, spectator)


def test_same_symbolic_basis_does_not_certify_the_same_hidden_instance():
    p = 7
    forms, labels, scales, outcomes, alignment, alpha, spectator = symbolic_transcript(p)
    packet = compile_variable_scalar_packet(alignment, forms, labels, scales, outcomes, alpha, spectator)
    # Identical public coefficient maps P-P cancel formally. Substituting
    # different unknown coefficients into the two copies does NOT cancel.
    rng = random.Random(16)
    theta = [rng.randrange(p) for _ in packet.parameter_basis]
    other = [rng.randrange(p) for _ in packet.parameter_basis]
    differences = []
    for _ in range(20):
        point = [rng.randrange(p) for _ in range(packet.width)]
        differences.append((packet.evaluate_fixture(point, theta)-packet.evaluate_fixture(point, other)) % p)
    assert len(set(differences)) > 1


def test_generic_compiler_never_calls_truth_evaluation(monkeypatch):
    from theorems.ut5_scalar_phase_compiler import SymbolicScalarPacket
    import inspect
    assert "parameters" not in inspect.signature(compile_variable_scalar_packet).parameters
    def forbidden(*args, **kwargs):
        raise AssertionError("hidden truth entered public compilation")
    monkeypatch.setattr(SymbolicScalarPacket, "evaluate_fixture", forbidden)
    forms, labels, scales, outcomes, alignment, alpha, spectator = symbolic_transcript(7)
    assert compile_variable_scalar_packet(alignment, forms, labels, scales, outcomes, alpha, spectator).degree <= 3


def test_generic_compiler_handles_mixed_multivariate_monomials():
    p, m, w = 7, 2, 3
    forms = forms3(p)+[[[0]*3 for _ in range(3)]]
    labels, scales, outcomes = [], [], []
    for j in range(3):
        labels += [[coefficient*int(i == j) % p for i in range(4)] for coefficient in (1, 1, -2)]
        scales += [j+1]*3
        outcomes += [[0, 0], [1, 0], [0, 1]]
    labels += [[0, 0, 0, 1], [0, 0, 0, p-1]]
    scales += [4, 4]
    outcomes += [[0, 0], [1, 1]]
    alignment = align_variable_jets(p, forms, labels, scales, outcomes)
    R, D = alignment.maps.carrier_width, alignment.maps.jet_width
    alpha = [[(j+1) % p for j in range(len(label_coordinates(p, forms, label).radical))] for label in labels]
    spectator = [j % p for j in range(R-D)]
    packet = compile_variable_scalar_packet(alignment, forms, labels, scales, outcomes, alpha, spectator)
    coefficients = [
        {(1, 1): 1, (1, 0): 1}, {(0, 2): 1, (1, 0): -1}, {(2, 0): 1, (0, 1): 1},
        {(2, 2): 1}, {(4, 0): 1, (0, 3): 1}, {(1, 3): 1}, {(3, 1): 1, (0, 1): 1},
    ]
    theta = [coefficients[c].get(exponent, 0) % p for c, exponent in packet.parameter_basis]
    def Q(x, y):
        return [x*y+x, y*y-x, x*x+y, x*x*y*y, x**4+y**3, x*y**3, x**3*y+y]
    rng = random.Random(16)
    for _ in range(15):
        point = [rng.randrange(p) for _ in range(m+D)]
        raw, psi, start = [0]*(2*R), 0, 0
        for i, c in zip(alignment.maps.active_indices, alignment.maps.representations):
            value = Q(*[(y+scales[i]*q) % p for y, q in zip(outcomes[i], point[:m])])
            v = mv(c.weyl, value[:w], p)
            raw[start:start+c.qudits] = v[:c.qudits]
            raw[R+start:R+start+c.qudits] = v[c.qudits:]
            psi += sum(a*b for a, b in zip(labels[i], value[w:]))
            psi += sum(a*b for a, b in zip(alpha[i], mv(c.radical, value[:w], p)))
            start += c.qudits
        transformed = mv(alignment.symplectic, raw, p)
        A, B = transformed[:R], transformed[R:]
        expected = (-psi-pow(2, -1, p)*sum(a*b for a, b in zip(A, B))-
                    sum(b*t for b, t in zip(B, point[m:]+spectator))) % p
        assert packet.evaluate_fixture(point, theta) == expected
    assert packet.degree <= 3
    assert all(max(parameters) < 18 for _, parameters in packet.terms if len(parameters) == 2)


@pytest.mark.parametrize("label", [[1, 2, 3, 4], [0, 0, 0, 1]])
def test_partial_qft_schur_trace_has_the_normalized_matrix_kernel(label):
    # This checks the representation-sector trace, not a general G oracle.
    # Equal central characters cancel, so their sum can be done analytically.
    p, w, z, V = 5, 3, 4, 5
    forms = forms3(p)+[[[0]*w for _ in range(w)]]
    coordinates = label_coordinates(p, forms, label)
    d, order = p**coordinates.qudits, p**(w+z)
    alpha = [(j+1) % p for j in range(len(coordinates.radical))]
    omega, half = np.exp(2j*np.pi/p), pow(2, -1, p)
    def multiply(left, right):
        v, a = left
        u, b = right
        bracket = [sum(v[i]*F[i][j]*u[j] for i, j in product(range(w), repeat=2)) for F in forms]
        return ([(x+y) % p for x, y in zip(v, u)],
                [(x+y+half*c) % p for x, y, c in zip(a, b, bracket)])
    def representation(element):
        v, a = element
        displacement = mv(coordinates.weyl, v, p)
        x, t = displacement if displacement else (0, 0)
        scalar = sum(c*b for c, b in zip(label, a))+sum(c*b for c, b in zip(alpha, mv(coordinates.radical, v, p)))
        result = np.zeros((d, d), dtype=complex)
        for j in range(d):
            result[(j+x) % d, j] = omega**((scalar+half*x*t+t*j) % p)
        return result
    def potential(q):
        return ([q, q*q % p, 2*q % p], [q**4 % p, q**3 % p, q*q % p, q])
    elements = [(list(v), [0]*z) for v in product(range(p), repeat=w)]
    matrices = np.array([representation(n) for n in elements])
    nontrivial_orientation = False
    for q, other in ((0, 0), (1, 1), (1, 3), (2, 4)):
        left, right = potential(q), potential(other)
        inverse = ([-x % p for x in left[0]], [-x % p for x in left[1]])
        increment = multiply(inverse, right)
        translated = np.array([representation(multiply(n, increment)) for n in elements])
        average = np.einsum("aij,akl->ikjl", matrices.conj(), translated)/p**w
        gauge = representation(left).conj().T @ representation(right)
        expected = np.einsum("ik,jl->ikjl", np.eye(d), gauge)/d
        np.testing.assert_allclose(average, expected, atol=1e-13)
        unnormalized = np.einsum("iijl->jl", d*average/(order*V))
        label_probability = d*d/order
        conditional = unnormalized/label_probability
        np.testing.assert_allclose(conditional, gauge/(V*d), atol=1e-13)
        if q == other:
            assert V*np.trace(unnormalized).real == pytest.approx(label_probability)
            assert V*np.trace(conditional).real == pytest.approx(1)
        nontrivial_orientation |= np.linalg.norm(gauge-gauge.conj().T) > 0.1
    assert nontrivial_orientation
