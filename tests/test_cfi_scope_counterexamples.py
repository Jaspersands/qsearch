"""Independent permutation and normalized-state controls for CFI scope claims.

Only the original graph constructor is imported; no report builders or registry
writers are called.
The enumerated automorphism subgroups are not claimed to be full automorphism groups.
"""

from itertools import combinations, permutations, product

import numpy as np

from theorems.cfi_base_family_search import cfi_parity_graph_from_base


K4_EDGES = tuple(combinations(range(4), 2))
EVEN_CUBIC_MASKS = (0, 3, 5, 6)


def _compose(left, right):
    return tuple(left[right[i]] for i in range(len(left)))


def _inverse(permutation):
    inverse = [0] * len(permutation)
    for source, target in enumerate(permutation):
        inverse[target] = source
    return tuple(inverse)


def _transpositions(size, pairs):
    permutation = list(range(size))
    for left, right in pairs:
        permutation[left], permutation[right] = permutation[right], permutation[left]
    return tuple(permutation)


def _k4_graph():
    base = np.ones((4, 4), dtype=int) - np.eye(4, dtype=int)
    graph = cfi_parity_graph_from_base(base)
    assert graph.shape == (28, 28)
    np.testing.assert_array_equal(graph.sum(axis=1), [3] * 16 + [4] * 12)
    return graph


def _k4_cycle_flips():
    # Pin the original constructor's vertex order, independently of audit helpers.
    labels = [("middle", vertex, mask)
              for vertex in range(4) for mask in EVEN_CUBIC_MASKS]
    labels.extend(("edge", edge, bit) for edge in K4_EDGES for bit in (0, 1))
    index = {label: i for i, label in enumerate(labels)}
    assert index[("edge", (0, 1), 0)] == 16
    assert index[("edge", (0, 1), 1)] == 17
    flips = {}
    for bits in product((0, 1), repeat=len(K4_EDGES)):
        selected = frozenset(edge for edge, bit in zip(K4_EDGES, bits) if bit)
        if any(sum(vertex in edge for edge in selected) % 2 for vertex in range(4)):
            continue
        permutation = []
        for kind, position, value in labels:
            if kind == "middle":
                incident = [edge for edge in K4_EDGES if position in edge]
                shift = sum(1 << i for i, edge in enumerate(incident) if edge in selected)
            else:
                shift = int(position in selected)
            permutation.append(index[(kind, position, value ^ shift)])
        flips[selected] = tuple(permutation)
    return flips


def _assert_automorphism(graph, permutation):
    assert sorted(permutation) == list(range(len(graph)))
    np.testing.assert_array_equal(graph, graph[np.ix_(permutation, permutation)])


def test_k4_eight_cycle_flips_form_a_faithful_automorphism_subgroup():
    graph = _k4_graph()
    flips = _k4_cycle_flips()
    assert len(flips) == len(set(flips.values())) == 8
    identity = tuple(range(28))
    assert flips[frozenset()] == identity
    for permutation in flips.values():
        _assert_automorphism(graph, permutation)
        assert _compose(permutation, permutation) == identity
    for left_edges, left in flips.items():
        for right_edges, right in flips.items():
            assert _compose(left, right) == flips[left_edges ^ right_edges]


def test_k4_uncolored_automorphism_does_not_normalize_cycle_flips():
    graph = _k4_graph()
    flips = _k4_cycle_flips()
    p = _transpositions(28, (
        (1, 12), (2, 8), (3, 4), (5, 9), (6, 13), (10, 14),
        (17, 26), (19, 24), (21, 22),
    ))
    k = flips[frozenset(((0, 1), (0, 2), (1, 2)))]
    assert k == _transpositions(28, (
        (0, 1), (2, 3), (4, 5), (6, 7), (8, 9), (10, 11),
        (16, 17), (18, 19), (22, 23),
    ))
    conjugate = _compose(_compose(p, k), _inverse(p))
    for permutation in (p, k, conjugate):
        _assert_automorphism(graph, permutation)
    assert all(permutation[16] in {16, 17} for permutation in flips.values())
    assert conjugate[16] == 26
    assert conjugate[16] not in {16, 17}
    assert conjugate not in set(flips.values())


def test_two_identical_cfi_components_have_a_verified_128_element_subgroup():
    component = _k4_graph()
    graph = np.zeros((56, 56), dtype=int)
    graph[:28, :28] = component
    graph[28:, 28:] = component
    flips = set(_k4_cycle_flips().values())
    subgroup = set()
    for left, right, swap in product(flips, flips, (False, True)):
        permutation = tuple(
            [target + (28 if swap else 0) for target in left]
            + [target + (0 if swap else 28) for target in right]
        )
        _assert_automorphism(graph, permutation)
        subgroup.add(permutation)
    assert len(subgroup) == 128
    assert tuple(range(56)) in subgroup
    assert sum(permutation[0] < 28 for permutation in subgroup) == 64
    assert sum(permutation[0] >= 28 for permutation in subgroup) == 64
    for left in subgroup:
        assert _inverse(left) in subgroup
        for right in subgroup:
            assert _compose(left, right) in subgroup

    # Even the explicitly exhibited subgroup rules out an order-two hidden group.
    assert len(subgroup) > 2


def _regular_coset_state(group, subgroup):
    index = {permutation: i for i, permutation in enumerate(group)}
    state = np.zeros((len(group), len(group)), dtype=float)
    for representative in group:
        ket = np.zeros(len(group), dtype=float)
        for element in subgroup:
            ket[index[_compose(representative, element)]] = 1 / np.sqrt(len(subgroup))
        state += np.outer(ket, ket) / len(group)
    return state


def test_actual_regular_coset_states_have_intersection_overlaps():
    group = tuple(permutations(range(4)))
    identity = tuple(range(4))
    s = (1, 0, 3, 2)
    t = (2, 3, 0, 1)
    subgroups = (
        frozenset((identity,)),
        frozenset((identity, s)),
        frozenset((identity, t)),
        frozenset((identity, s, t, _compose(s, t))),
    )
    states = []
    for subgroup in subgroups:
        assert all(_compose(a, b) in subgroup for a, b in product(subgroup, repeat=2))
        state = _regular_coset_state(group, subgroup)
        np.testing.assert_allclose(state, state.T, rtol=0, atol=1e-14)
        np.testing.assert_allclose(np.trace(state), 1, rtol=0, atol=1e-14)
        eigenvalues = np.linalg.eigvalsh(state)
        assert eigenvalues.min() >= -1e-14
        rank = len(group) // len(subgroup)
        np.testing.assert_allclose(
            eigenvalues,
            [0] * (len(group) - rank) + [len(subgroup) / len(group)] * rank,
            rtol=0, atol=1e-14,
        )
        states.append(state)
    for i, left in enumerate(subgroups):
        for j, right in enumerate(subgroups):
            np.testing.assert_allclose(
                np.trace(states[i] @ states[j]), len(left & right) / len(group),
                rtol=0, atol=1e-14,
            )

    difference = _compose(_inverse(s), t)
    conjugates = {_compose(_compose(g, difference), _inverse(g)) for g in group}
    assert len(conjugates) == 3
    overlap = np.trace(states[1] @ states[2])
    np.testing.assert_allclose(overlap, 1 / 24, rtol=0, atol=1e-14)
    assert not np.isclose(overlap, 1 / len(conjugates))
