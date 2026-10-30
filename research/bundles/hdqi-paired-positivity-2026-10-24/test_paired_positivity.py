from fractions import Fraction as F
from itertools import combinations, permutations
import math

import numpy as np
import pytest
from scipy.linalg import expm

import paired_positivity as p


def dense_operators(graph):
    identity, x, z = np.eye(2, dtype=np.int64), np.array([[0, 1], [1, 0]], dtype=np.int64), np.diag([1, -1])
    out = []
    for i in range(graph.vertices):
        matrix = np.ones((1, 1), dtype=np.int64)
        for j in reversed(range(graph.vertices)):
            matrix = np.kron(matrix, x if j == i else z if j < i and (j, i) in graph.edges else identity)
        out.append(matrix)
    return out


def test_explicit_graph_is_connected_and_in_degree_scale_regime():
    graph = p.witness_graph()
    seen = {0}
    while True:
        enlarged = seen | {v for a, b in graph.edges for u, v in ((a, b), (b, a)) if u in seen}
        if enlarged == seen:
            break
        seen = enlarged
    assert seen == set(range(6))
    assert graph.degree == 3
    assert (graph.degree + 1) * F(1, 32)**2 == F(1, 256) < F(1, 64)


def test_exact_multivariate_leading_negative_weight():
    graph = p.witness_graph()
    coefficients = p.leading_paired_coefficients(graph)
    assert coefficients[30] == -F(2, 2025)
    assert p.multivariate_amplitude(graph, (2, 1, 1, 1, 1, 0)) == F(1, 45)
    assert p.multivariate_amplitude(graph, (0, 1, 1, 1, 1, 2)) == -F(1, 45)
    assert sum(coefficients) == 2**12 * p.multivariate_amplitude(graph, (2,) * 6)
    assert sum(coefficients) > 0  # Summing away the output label hides the obstruction.


def test_matrix_powers_independently_match_integer_recurrence():
    graph, label = p.witness_graph(), 30
    operators = dense_operators(graph)
    for active in (63, 62, 31, 30):
        h = sum(op for i, op in enumerate(operators) if active >> i & 1)
        vector = np.zeros(64, dtype=np.int64)
        vector[0] = 1
        direct = []
        for _ in range(15):
            direct.append(int(vector[label]))
            vector = h @ vector
        assert tuple(direct) == p.power_coefficients(graph, active, label, 14)
    assert p.power_coefficients(graph, 31, label, 6)[6] == 16
    assert p.power_coefficients(graph, 62, label, 6)[6] == -16


def test_literal_360_words_prove_path_leading_coefficient():
    graph = p.witness_graph()
    signs = {1: 0, -1: 0}
    for word in set(permutations((0, 0, 1, 2, 3, 4))):
        label, sign = 0, 1
        for generator in reversed(word):
            sign *= (-1)**((graph.lower[generator] & label).bit_count())
            label ^= 1 << generator
        assert label == 30
        signs[sign] += 1
    assert signs == {1: 188, -1: 172}
    assert F(signs[1] - signs[-1], math.factorial(6)) == F(1, 45)


def test_signed_coefficient_symmetry_commutes_with_full_hamiltonian():
    graph, permutation = p.witness_graph(), (5, 3, 2, 1, 4, 0)
    symmetry = np.zeros((64, 64), dtype=np.int64)
    for label in range(64):
        image, sign = p.symmetry_image(graph, permutation, label)
        symmetry[image, label] = sign
    h = sum(dense_operators(graph))
    assert np.array_equal(symmetry.T @ symmetry, np.eye(64, dtype=np.int64))
    assert np.array_equal(symmetry @ h, h @ symmetry)
    assert symmetry[0, 0] == 1
    assert symmetry[30, 30] == -1
    certificate = p.symmetry_zero_certificate(graph, permutation, 30)
    assert certificate["identically_zero_for_unit_couplings"]
    assert not p.symmetry_zero_certificate(graph, permutation, 1)["identically_zero_for_unit_couplings"]


def test_reversal_parity_alone_does_not_explain_this_zero():
    graph, label = p.witness_graph(), 30
    occupied_edges = sum((label >> a & 1) and (label >> b & 1) for a, b in graph.edges)
    assert occupied_edges == 2
    assert p.power_coefficients(graph, graph.full, label, 40) == (0,) * 41


@pytest.mark.parametrize("time", [F(1, 64), F(1, 128), F(1, 1024)])
def test_rational_negative_interval_at_high_temperature(time):
    certificate = p.witness_certificate(time)
    interval = certificate["activity_interval"]
    assert F(interval["lower"]) <= F(interval["upper"]) < 0
    assert F(interval["upper"]) <= F(certificate["analytic_activity_upper"])
    assert certificate["negative_activity_certified"]
    assert not certificate["generic_classical_sampling_ruled_out"]
    assert not certificate["quantum_advantage_established"]


def test_support_moebius_identity_without_floating_point_subtraction():
    graph, time = p.witness_graph(), F(1, 64)
    total = p.paired_activity_interval(graph, 63, 30, time)
    left = p.amplitude_interval(graph, 31, 30, time).square()
    right = p.amplitude_interval(graph, 62, 30, time).square()
    assert left.lower > 0 and right.lower > 0
    # Exact symmetry proves full and bridge-free amplitudes are zero.
    analytic = p.Interval(-2 * left.upper, -2 * left.lower)
    assert total.lower <= analytic.upper and analytic.lower <= total.upper
    assert left.lower <= right.upper and right.lower <= left.upper


@pytest.mark.parametrize("active", [0, 1, 3, 7])
def test_taylor_interval_against_dense_exponential(active):
    graph = p.Graph.create(3, [(0, 1), (1, 2)])
    h = sum((op for i, op in enumerate(dense_operators(graph)) if active >> i & 1), np.zeros((8, 8)))
    actual = expm(-.125 * h)[:, 0]
    for label in range(8):
        interval = p.amplitude_interval(graph, active, label, F(1, 8), order=6)
        assert float(interval.lower) - 1e-15 <= actual[label] <= float(interval.upper) + 1e-15


@pytest.mark.parametrize("edge_mask", range(8))
def test_all_three_vertex_colored_weights_sum_to_partition_activity(edge_mask):
    pairs = list(combinations(range(3), 2))
    graph = p.Graph.create(3, [e for i, e in enumerate(pairs) if edge_mask >> i & 1])
    coefficients = p.leading_paired_coefficients(graph)
    assert sum(coefficients) == 2**6 * p.multivariate_amplitude(graph, (2, 2, 2))


def test_scalar_edge_weights_do_not_warn_about_six_vertex_failure():
    graph = p.Graph.create(2, [(0, 1)])
    assert all(value >= 0 for value in p.leading_paired_coefficients(graph))
    for label in range(4):
        if label != 3:
            assert p.paired_activity_interval(graph, 3, label, F(1, 64)).lower > 0
    assert p.power_coefficients(graph, 3, 3, 20) == (0,) * 21


@pytest.mark.parametrize("permutation", [(1, 0, 2, 3, 4, 5), (5, 4, 3, 2, 1, 0),
                                         (2, 5, 0, 4, 1, 3)])
def test_negative_leading_weight_survives_vertex_relabeling(permutation):
    graph = p.witness_graph()
    relabeled = p.Graph.create(6, [(permutation[a], permutation[b]) for a, b in graph.edges])
    label = sum(1 << permutation[i] for i in (1, 2, 3, 4))
    assert p.leading_paired_coefficients(relabeled)[label] == -F(2, 2025)


def test_uniform_analytic_interval_is_not_inferred_from_samples():
    ratio = F(45 * 5**8, math.factorial(8) * 64**2) * F(64, 59)
    assert ratio == F(390625, 3383296) < F(1, 8)


@pytest.mark.parametrize("vertices", [6, 7, 128, 1024])
def test_connected_extension_retains_exact_zero_without_density_table(vertices):
    graph, permutation = p.extended_witness(vertices)
    assert graph.degree == 3
    assert tuple(edge for edge in graph.edges if edge[1] < 6) == p.witness_graph().edges
    assert p.symmetry_zero_certificate(graph, permutation, 30)["identically_zero_for_unit_couplings"]
    if vertices > 8:
        with pytest.raises(ValueError):
            p.power_coefficients(graph, graph.full, 30, 12)


def test_missing_symmetry_and_resource_guards_reject():
    graph = p.witness_graph()
    with pytest.raises(ValueError):
        p.symmetry_image(graph, (1, 0, 2, 3, 4, 5), 30)
    with pytest.raises(ValueError):
        p.symmetry_image(graph, (False, 1, 2, 3, 4, 5), 30)
    with pytest.raises(ValueError):
        p.Graph.create(4097, [])
    with pytest.raises(ValueError):
        p.Graph.create(2, [(0, 1), (1, 0)])
    with pytest.raises(ValueError):
        p.multivariate_amplitude(graph, (100,) * 6)
    with pytest.raises(ValueError):
        p.amplitude_interval(graph, 63, 30, 100, order=2)
    with pytest.raises(ValueError):
        p.paired_activity_interval(graph, 1, 30, F(1, 64))
    with pytest.raises(ValueError):
        p.witness_certificate(F(1, 32))
