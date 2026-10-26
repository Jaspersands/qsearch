from fractions import Fraction
from itertools import product
import random

import networkx as nx
import numpy as np
import pytest

from theorems.ternary_coloring_bpqm import graph_code
from theorems.ternary_graph_reduction import (
    atlas_control, core_edge_witnesses, exact_core_law, path_counts,
    restored_block_control, sample_path, sample_subdivision, series_profile,
    subdivision_budget,
)
from theorems.ternary_tilted_type import relinearize


def rational(record):
    return Fraction(record["numerator"], record["denominator"])


def edges(graph):
    return tuple(sorted(tuple(sorted(e)) for e in graph.edges()))


def test_all_small_connected_graphs_have_the_series_class_square_rank():
    result = atlas_control()
    assert result["connected_simple_graphs_checked"] == 142
    assert result["all_series_square_ranks_match"]
    assert result["census_is_not_a_proof_for_arbitrary_graphs"]


def test_tree_cycle_and_theta_are_scope_controls_not_full_squares():
    tree = series_profile(5, edges(nx.path_graph(5)))
    assert tree["square_dimension"] == 0
    assert len(tree["bridge_edge_indices"]) == 4
    cycle = series_profile(5, edges(nx.cycle_graph(5)))
    assert cycle["square_dimension"] == 1
    assert sorted(cycle["series_classes"][0]) == list(range(5))
    theta = nx.complete_bipartite_graph(2, 3)
    profile = series_profile(5, edges(theta))
    assert profile["square_dimension"] == 3
    assert sorted(len(c) for c in profile["series_classes"]) == [2, 2, 2]


@pytest.mark.parametrize("graph", [nx.complete_graph(4), nx.cubical_graph(),
                                  nx.complete_bipartite_graph(3, 3)])
def test_each_core_edge_has_an_actual_unit_square_witness(graph):
    profile = series_profile(len(graph), edges(graph))
    assert profile["full_square"]
    witnesses = core_edge_witnesses(profile["code"])
    assert len(witnesses) == graph.number_of_edges()
    for witness in witnesses:
        left, right = witness["detours"]
        left_edges = {tuple(sorted(e)) for e in zip(left, left[1:])}
        right_edges = {tuple(sorted(e)) for e in zip(right, right[1:])}
        assert left_edges.isdisjoint(right_edges)
        assert profile["code"]["edges"][witness["edge_index"]] not in left_edges | right_edges


def test_full_core_square_makes_every_codeword_projection_unresolved():
    code = graph_code(4, edges(nx.complete_graph(4)))
    for coefficients in product(range(3), repeat=code["code_dimension"]):
        c = tuple(sum(a*row[i] for a, row in zip(coefficients, code["cycles"])) % 3
                  for i in range(len(code["edges"])))
        outcomes = tuple((a+1) % 3 for a in c)
        result = relinearize(code["cycles"], outcomes)
        assert result["consistent"]
        assert not result["projection_unique"]
        assert result["free_variables"] == code["code_dimension"]


def test_repeated_core_relinearization_matches_forest_criterion_exactly():
    code = graph_code(4, edges(nx.complete_graph(4)))
    repeated = tuple(tuple(a for a in row for _ in range(2)) for row in code["cycles"])
    for coefficients in ((0, 0, 0), (1, 0, 0)):
        c = tuple(sum(a*row[i] for a, row in zip(coefficients, code["cycles"])) % 3
                  for i in range(len(code["edges"])))
        for unknown in product((False, True), repeat=6):
            outcomes = tuple(a for i, value in enumerate(c)
                             for a in ((value+1) % 3, (value+(1 if unknown[i] else 2)) % 3))
            residual = nx.Graph()
            residual.add_nodes_from(range(4))
            residual.add_edges_from(edge for edge, keep in zip(code["edges"], unknown) if keep)
            result = relinearize(repeated, outcomes)
            assert result["projection_unique"] == nx.is_forest(residual)
            assert result["free_variables"] == (
                residual.number_of_edges()-4+nx.number_connected_components(residual))
            if result["projection_unique"]:
                assert result["value"] == coefficients


@pytest.mark.parametrize("length", range(9))
def test_path_count_formula_matches_complete_enumeration(length):
    counts = [0, 0, 0]
    for increments in product((1, 2), repeat=length):
        counts[sum(increments) % 3] += 1
    assert tuple(counts) == path_counts(length)


def test_bridge_sampler_executes_every_path_with_its_exact_uniform_mass():
    class Tickets:
        def __init__(self, values):
            self.values = iter(values)

        def randrange(self, total):
            value = next(self.values)
            assert 0 <= value < total
            return value

    for length in range(1, 7):
        for end in range(3):
            allowed = [p for p in product(range(3), repeat=length-1)
                       if all(a != b for a, b in zip((0, *p, end), (*p, end)))]
            for internal in allowed:
                path = (0, *internal, end)
                probability, tickets = Fraction(1), []
                for j, chosen in enumerate(path[1:], 1):
                    options = [(c, path_counts(length-j)[(end-c) % 3])
                               for c in range(3) if c != path[j-1]]
                    total = sum(w for _, w in options)
                    weight = next(w for c, w in options if c == chosen)
                    tickets.append(sum(w for c, w in options if c < chosen))
                    probability *= Fraction(weight, total)
                assert sample_path(length, 0, end, Tickets(tickets)) == path
                assert probability == Fraction(1, len(allowed))
            assert len(allowed) == path_counts(length)[end]


def test_exact_subdivision_law_matches_independent_expanded_graph_census():
    core_edges = edges(nx.cycle_graph(3))
    law = exact_core_law(3, core_edges, 2)
    counts = {tuple(colors): weight for colors, weight in law["rows"]}
    direct = {}
    for tail in product(range(3), repeat=5):
        colors = (0, *tail)
        if all(colors[u] != colors[3+i] != colors[v] for i, (u, v) in enumerate(core_edges)):
            key = colors[:3]
            direct[key] = direct.get(key, 0)+1
    assert counts == direct
    assert sum(direct.values()) == law["normalizer"] == 22
    # Proposal acceptance times bridge mass, divided by total acceptance,
    # is the same rational for every valid expanded coloring.
    acceptance = rational(law["proposal_acceptance"])
    for weight in counts.values():
        probability = Fraction(1, 9)*Fraction(weight, 8)*Fraction(1, weight)/acceptance
        assert probability == Fraction(1, 22)


def test_ordinary_k4_unsatisfiable_target_is_not_solved_by_padding():
    core_edges = edges(nx.complete_graph(4))
    law = exact_core_law(4, core_edges, 2)
    assert law["normalizer"] > 0
    assert rational(law["original_endpoint_constraints_probability"]) == 0
    sample = sample_subdivision(4, core_edges, 8, seed=319, trial_cap=16)
    assert sample["status"] == "EXACT_UNIFORM_SUBDIVISION_COLORING"
    assert sample["every_expanded_edge_verified"]
    assert not sample["core_coloring_is_proper"]


@pytest.mark.parametrize("length", [1, 2, 3, 4, 6, 8])
def test_restored_endpoint_source_has_original_complex_trine_gram(length):
    result = restored_block_control(length)
    expected = np.full((3, 3), -0.5)
    np.fill_diagonal(expected, 1)
    np.testing.assert_allclose(result["gram_real"], expected, atol=2e-12)
    assert result["gram_max_imaginary_residual"] < 2e-12
    assert result["isometry_max_residual"] < 2e-12
    assert not result["extra_logical_discrimination_information"]
    bad = rational(result["invalid_local_pair_probability"])
    assert bad == 0 if length == 1 else bad > 0
    if length == 2:
        assert bad == Fraction(1, 3)


def test_native_padded_law_is_classically_sampled_at_certified_precision():
    graph = nx.random_regular_graph(4, 40, seed=2026102061)
    sample = sample_subdivision(40, edges(graph), 64, seed=2026102062)
    budget = sample["budget"]
    assert sample["status"] == "EXACT_UNIFORM_SUBDIVISION_COLORING"
    assert sample["every_expanded_edge_verified"]
    assert not sample["core_coloring_is_proper"]
    assert budget["expanded_vertices"] == 5080
    assert budget["expanded_edges"] == 5120
    assert rational(budget["classical_trial_acceptance_lower"]) > 1-Fraction(1, 10**16)
    assert rational(budget["classical_abort_probability_upper"]) < Fraction(1, 2**800)
    assert rational(budget["conditional_quantum_output_tv_upper"]) < Fraction(1, 10**15)
    assert not budget["native_quantum_circuit_executed"]


def test_small_padding_does_not_get_a_free_classical_success_bound():
    graph = nx.complete_graph(4)
    budget = subdivision_budget(4, edges(graph), 2)
    assert rational(budget["classical_trial_acceptance_lower"]) == 0
    assert rational(budget["classical_abort_probability_upper"]) == 1
    # Find and retain an actual failed bounded attempt, not resample it away.
    samples = [sample_subdivision(4, edges(graph), 2, seed=s, trial_cap=1) for s in range(10)]
    assert any(s["status"] == "DECLARED_ABORT" for s in samples)


@pytest.mark.parametrize("length", [-1, 1.5, 4097])
def test_path_count_rejects_invalid_or_unbounded_inputs(length):
    with pytest.raises(ValueError):
        path_counts(length)


def test_missing_core_promises_are_not_silently_certified():
    with pytest.raises(ValueError):
        core_edge_witnesses(graph_code(4, edges(nx.cycle_graph(4))))
    with pytest.raises(ValueError):
        sample_subdivision(4, edges(nx.complete_graph(4)), 1, seed=1)
    with pytest.raises(ValueError):
        sample_subdivision(4, edges(nx.complete_graph(4)), 8, seed=1, trial_cap=0)
    with pytest.raises(ValueError):
        sample_path(1, 0, 0, random.Random(1))
