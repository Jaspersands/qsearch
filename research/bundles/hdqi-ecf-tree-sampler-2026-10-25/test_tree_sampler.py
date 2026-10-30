from fractions import Fraction as Q
from itertools import combinations, product
from random import Random
import sys
from pathlib import Path

import pytest

from tree_controls import direct_native_vector, direct_output_masses, small_ecf_check
from tree_sampler import Decomposition, TreeSampler, arc_decomposition, gaussian, glue_decompositions


def cycle(size):
    edges = [(i, i+1) for i in range(size-1)]+[(0, size-1)]
    bags = [{0, i, i+1} for i in range(1, size-1)]
    return Decomposition(size, edges, bags, [(i, i+1) for i in range(size-3)])


def sun():
    edges = [(0, 1), (0, 2), (1, 2), (0, 3), (1, 4), (2, 5)]
    return Decomposition(6, edges, [{0, 1, 2}, {0, 3}, {1, 4}, {2, 5}], [(0, 1), (0, 2), (0, 3)])


def path(size):
    return Decomposition(size, [(i, i+1) for i in range(size-1)],
                         [{i, i+1} for i in range(size-1)], [(i, i+1) for i in range(size-2)])


def word_bits(word, size):
    return tuple(word >> i & 1 for i in range(size))


@pytest.mark.parametrize("decomposition", [cycle(5), cycle(4), sun(), path(4),
    Decomposition(4, [(0, 1), (2, 3)], [{0, 1}, {2, 3}], [(0, 1)])])
@pytest.mark.parametrize("kind", ["real-Z", "complex-X", "complex-mixed"])
def test_all_native_output_probabilities_match_direct_pauli_actions(decomposition, kind):
    d = decomposition
    couplings = [Q((-1)**i, 1+i % 3) for i in range(d.size)]
    parameters = [Q(1, 3), Q(-2, 7)] if kind == "real-Z" else [(Q(1, 3), Q(2, 5)), (Q(-1, 4), Q(1, 7))]
    bases = ("Z",)*d.size if kind == "real-Z" else (("X",)*d.size if kind == "complex-X"
                                                   else tuple("ZX"[i % 2] for i in range(d.size)))
    sampler = TreeSampler(d, couplings, parameters, bases=bases)
    expected = direct_output_masses(couplings, d.edges, parameters, bases)
    assert sampler.norm_squared == sum(expected)
    for word, mass in enumerate(expected):
        assert sampler.mass(dict(enumerate(word_bits(word, d.size)))) == mass
        assert sampler.probability(word_bits(word, d.size)) == mass/sum(expected)


@pytest.mark.parametrize("bases", [("Z",)*4, ("X",)*4, ("X", "Z", "Z", "X")])
def test_all_partial_marginals_not_only_a_single_sampling_order(bases):
    d = cycle(4)
    couplings, parameters = [1, -1, Q(1, 2), 1], [(Q(1, 3), Q(1, 5)), Q(-2, 7)]
    sampler = TreeSampler(d, couplings, parameters, bases=bases)
    expected = direct_output_masses(couplings, d.edges, parameters, bases)
    for assignment in product((None, 0, 1), repeat=4):
        pins = {v: b for v, b in enumerate(assignment) if b is not None}
        mass = sum(p for word, p in enumerate(expected) if all(word >> v & 1 == b for v, b in pins.items()))
        assert sampler.mass(pins) == mass


def test_three_factors_crossing_orientation():
    d = path(3)
    parameters = [(Q(1, 3), Q(2, 7)), Q(-1, 4), (Q(2, 5), Q(-1, 6))]
    sampler = TreeSampler(d, [1, -1, 1], parameters, bases=("X",)*3)
    expected = direct_output_masses([1, -1, 1], d.edges, parameters, ("X",)*3)
    assert [sampler.mass(dict(enumerate(word_bits(w, 3)))) for w in range(8)] == list(expected)


def test_unsigned_weights_are_not_a_legal_substitute():
    d, parameters = path(3), [Q(1, 3), Q(2, 5)]
    vector = direct_native_vector([1]*3, d.edges, parameters)
    independent = [mask for mask in range(8) if d.independent(mask)]
    unsigned = [Q(0)]*8
    for a, b in product(independent, repeat=2):
        unsigned[a ^ b] += (-parameters[0])**a.bit_count()*(-parameters[1])**b.bit_count()
    assert vector[7].x > 0 and unsigned[7] < 0
    # Z probabilities can hide some sign errors. X readout exposes interference.
    signed_x = direct_output_masses([1]*3, d.edges, parameters, ("X",)*3)
    unsigned_x = [sum((-1)**((w & y).bit_count())*a for y, a in enumerate(unsigned))**2/8 for w in range(8)]
    assert signed_x != tuple(unsigned_x)


@pytest.mark.parametrize("bases", [("Z",)*5, ("X",)*5, ("Z", "X", "Z", "X", "Z")])
def test_exact_samples_and_sampling_orders(bases):
    sampler = TreeSampler(cycle(5), [1]*5, [(Q(1, 3), Q(2, 5))], bases=bases)
    for order in (range(5), reversed(range(5)), (2, 4, 1, 0, 3)):
        order = tuple(order)
        for seed in range(5):
            assert sampler.probability(sampler.sample(Random(seed), order=order)) > 0


def test_zero_product_rejected_exactly():
    d = Decomposition(2, [(0, 1)], [{0, 1}], [])
    with pytest.raises(ValueError, match="zero transfer"):
        TreeSampler(d, [Q(3, 5), Q(4, 5)], [1, -1])


@pytest.mark.parametrize("bases", [("Z",)*4, ("X",)*4, ("X", "Z", "X", "Z")])
def test_empty_product_is_vacuum_with_normalized_local_measurements(bases):
    sampler = TreeSampler(cycle(4), [1]*4, [], bases=bases)
    assert sampler.norm_squared == 1
    for word in product((0, 1), repeat=4):
        expected = Q(0) if any(b and basis == "Z" for b, basis in zip(word, bases)) else Q(1, 2**bases.count("X"))
        assert sampler.probability(word) == expected


@pytest.mark.parametrize("parameters", [[1.0], [complex(1, 2)], [(Q(1, 2), .1)], [True]])
def test_inexact_parameter_inputs_rejected(parameters):
    with pytest.raises(TypeError):
        TreeSampler(path(3), [1]*3, parameters)


@pytest.mark.parametrize("bags,tree_edges,edges,match", [
    ([{0, 1}, {2}], [], [(0, 1)], "form a tree"),
    ([{0, 1}, {1, 2}], [(0, 1)], [(0, 2)], "not covered"),
    ([{0, 1}, {1, 2}, {0, 2}], [(0, 1), (1, 2)], [(0, 1)], "running intersection"),
    ([{0, 1, 2}], [], [], "independence bound"),
    ([{0, 1}], [], [(0, 1)], "missing"),
    ([{0, 1}, {1, 2}], [(0, 1)], [(0, 0)], "self-loop"),
    ([{0, 1}, {1, 2}], [(0, 1)], [(0, 1), (1, 0)], "repeated edge"),
    ([(0, 0, 1), (1, 2)], [(0, 1)], [(0, 1)], "repeated vertex"),
])
def test_false_decomposition_certificates_rejected(bags, tree_edges, edges, match):
    with pytest.raises(ValueError, match=match):
        Decomposition(3, edges, bags, tree_edges)


def test_budget_charges_two_replicas():
    d = Decomposition(20, list(combinations(range(20), 2)), [set(range(20))], [])
    record = d.resource_record(4)
    assert record["max_bag_pair_states"] == 21**8
    assert record["replicas"] == 8
    assert not record["ecf_recognition_performed"]
    with pytest.raises(ValueError, match="budget"):
        TreeSampler(d, [1]*20, [Q(1, 3)]*4, max_pair_states=100)


def test_branched_clique_gluing_is_verified_and_not_a_path():
    pieces = [([{0, 1, 2}], []), ([{0, 3}], []), ([{1, 4}], []), ([{2, 5}], [])]
    d = glue_decompositions(6, sun().edges, pieces, [(0, 0, i, 0) for i in (1, 2, 3)])
    assert len(d.children[0]) == 3
    assert small_ecf_check(d.size, d.edges)
    a = TreeSampler(d, [1]*6, [Q(1, 3), Q(1, 7)])
    b = TreeSampler(sun(), [1]*6, [Q(1, 3), Q(1, 7)])
    assert a.mass({1: 1, 4: 0}) == b.mass({1: 1, 4: 0})
    with pytest.raises(ValueError, match="running intersection"):
        glue_decompositions(6, sun().edges, pieces, [(0, 0, 1, 0), (1, 0, 2, 0), (2, 0, 3, 0)])


@pytest.mark.parametrize("universals", [0, 2])
def test_rational_circular_arc_constructor_and_two_clique_bags(universals):
    arcs = [(Q(1, 20), Q(6, 20)), (Q(5, 20), Q(10, 20)),
            (Q(9, 20), Q(14, 20)), (Q(13, 20), Q(18, 20)), (Q(17, 20), Q(2, 20))]
    d = arc_decomposition(arcs, universal_count=universals)
    assert d.bound == 2 and d.size == 5+universals
    assert set(cycle(5).edges) <= set(d.edges)
    assert small_ecf_check(d.size, d.edges)
    sampler = TreeSampler(d, [1]*d.size, [(Q(1, 5), Q(1, 7))], bases=("X",)*d.size)
    expected = direct_output_masses([1]*d.size, d.edges, sampler.parameters, sampler.bases)
    assert sampler.norm_squared == sum(expected)
    assert sampler.mass({0: 1, d.size-1: 0}) == sum(p for w, p in enumerate(expected) if w & 1 and not w >> (d.size-1) & 1)


def test_sampler_does_not_infer_ecf_or_thermal_from_tree_structure():
    d = cycle(4)
    assert not small_ecf_check(4, d.edges)
    sampler = TreeSampler(d, [1]*4, [Q(1, 3)])
    assert not sampler.resources["ecf_recognition_performed"]
    assert not sampler.resources["thermal_approximation_certified"]


@pytest.mark.parametrize("arcs", [[(0, Q(1, 2))], [(Q(1, 2), Q(1, 2))], [(0.1, 0.2)], []])
def test_invalid_arc_input(arcs):
    with pytest.raises((TypeError, ValueError)):
        arc_decomposition(arcs)


def test_real_path_probabilities_match_previous_automaton():
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent/"hdqi-transfer-word-sampler-2026-10-25"))
    from word_sampler import WordSampler
    for basis in ("Z", "X"):
        previous = WordSampler([1, -1, 1, Q(1, 2)], 1, [Q(1, 3), Q(2, 7)], basis=basis)
        new = TreeSampler(path(4), [1, -1, 1, Q(1, 2)], [Q(1, 3), Q(2, 7)], bases=(basis,)*4)
        for word in product((0, 1), repeat=4):
            assert new.probability(word) == previous.probability(word)


def test_gaussian_algebra_is_exact():
    from tree_sampler import conjugate
    z = gaussian((Q(1, 3), Q(2, 5)))
    assert z*conjugate(z) == gaussian(Q(1, 9)+Q(4, 25))


def test_non_line_graph_fixture_remains_in_exact_sampler_scope():
    import networkx as nx
    edges = [(a, b) for a, b in combinations(range(7), 2) if b-a <= 2]
    d = Decomposition(7, edges, [{i, i+1, i+2} for i in range(5)], [(i, i+1) for i in range(4)])
    assert small_ecf_check(7, edges)
    with pytest.raises(nx.NetworkXError):
        nx.inverse_line_graph(nx.Graph(edges))
    sampler = TreeSampler(d, [1]*7, [(Q(1, 3), Q(1, 7)), Q(-1, 5)], bases=("X",)*7)
    expected = direct_output_masses([1]*7, edges, sampler.parameters, sampler.bases)
    assert sampler.norm_squared == sum(expected)
    assert sampler.mass({0: 1, 3: 1, 6: 0}) == sum(p for w, p in enumerate(expected)
                                                  if w & 1 and w >> 3 & 1 and not w >> 6 & 1)


def test_thermal_resource_plan_uses_conservative_mode_bound_and_retains_blockers():
    from thermal_scope import conditional_thermal_plan
    d = cycle(5)
    plan = conditional_thermal_plan(d, [1]*5, Q(1, 10), Q(1, 20))
    assert plan["mode_count_upper"] == 5
    assert plan["scalar_approximation"]["requested_error"] == Q(1, 400)
    assert plan["conditional_thermal_squared_vector_error_upper"] <= Q(1, 80)**2
    assert plan["max_pair_states_log2_upper"] >= (d.resource_record(plan["factors_upper"])["max_bag_pair_states"]-1).bit_length()
    assert plan["conditional_on_ecf_transfer_identity"]
    for key in ("ecf_graph_verified", "complex_factors_compiled", "full_thermal_sampler_executed",
                "polynomial_classical_sampler_claim", "quantum_advantage_claim"):
        assert not plan[key]
    non_ecf = conditional_thermal_plan(cycle(4), [1]*4, 1, Q(1, 10))
    assert not non_ecf["ecf_graph_verified"]


@pytest.mark.parametrize("beta,error", [(0, Q(1, 10)), (-1, Q(1, 10)), (1, 0), (1, 2), (.1, Q(1, 10))])
def test_invalid_thermal_plan_inputs(beta, error):
    from thermal_scope import conditional_thermal_plan
    with pytest.raises((ValueError, TypeError)):
        conditional_thermal_plan(cycle(5), [1]*5, beta, error)


def test_bad_measurement_and_sampling_inputs_rejected():
    d = path(3)
    with pytest.raises(ValueError, match="basis"):
        TreeSampler(d, [1]*3, [], bases=("Z", "Y", "Z"))
    sampler = TreeSampler(d, [1]*3, [])
    for pins in ({3: 0}, {0: True}, {0: 2}):
        with pytest.raises(ValueError, match="pins"):
            sampler.mass(pins)
    for order in ((0, 0, 1), (0, 1), (False, 1, 2)):
        with pytest.raises(ValueError, match="permutation"):
            sampler.sample(Random(0), order=order)


@pytest.mark.parametrize("d", [cycle(5), sun()])
def test_full_thermal_vector_bound_on_non_path_geometries(d):
    import numpy as np
    from scipy.linalg import expm
    beta, layers = Q(1, 10), 2
    couplings = [Q((-1)**i, 1+i % 2) for i in range(d.size)]
    dimension = 1 << d.size
    hamiltonian = np.zeros((dimension, dimension))
    for i, coupling in enumerate(couplings):
        earlier = sum(1 << a for a, b in d.edges if b == i)
        for word in range(dimension):
            hamiltonian[word ^ (1 << i), word] += float(coupling)*(-1)**((word & earlier).bit_count())
    exact = expm(-float(beta)*hamiltonian/2)[:, 0]
    exact /= np.linalg.norm(exact)
    product_vector = direct_native_vector(couplings, d.edges, [beta/(2*layers)]*layers)
    approximation = np.array([complex(float(z.x), float(z.y)) for z in product_vector])
    approximation /= np.linalg.norm(approximation)
    mass = sum(j*j for j in couplings)
    bound_squared = beta**6*mass**3/(324*layers**4)
    assert np.linalg.norm(exact-approximation)**2 <= float(bound_squared)+1e-14


def test_even_hole_has_no_scalar_transfer_inversion_identity():
    d = cycle(4)
    vector = direct_native_vector([1]*4, d.edges, [Q(1, 3), Q(-1, 3)])
    assert any(vector[word] for word in range(1, 16))


@pytest.mark.parametrize("d", [cycle(5), sun(), path(5)])
def test_positive_even_factor_norm_bound_exactly(d):
    # p(z)=(1-u*z)(1-conj(u)*z), E(z)=1+|u|^2*z^2 >= E(0).
    u = (Q(1, 5), Q(2, 7))
    sampler = TreeSampler(d, [Q((-1)**i, i+1) for i in range(d.size)], [u, (u[0], -u[1])])
    assert sampler.norm_squared >= 1
