from collections import Counter
from fractions import Fraction
from itertools import product
import math

import numpy as np
import pytest

from ternary_gaussian_drive import (
    block_laplacian_row, default_nullity_cap, dense_calibration_laplacian, gaussian_binomial,
    graph_ledger, incoming, laplacian_row, linear_case_solutions,
    low_blind_measurement_ledger, onehot_fourth_moment, outgoing,
    chirp_exponent, public_chirp, rank_one_component_census, readout_calibration,
    sparse_entry, sparse_entry_spec, sparse_row_locations,
)
from ternary_pointed_triples import low_source, random_native_source


def linear_case(columns, target, domains=None):
    zero = (0,)*len(target)
    return {"corner": 2, "equations_linear_in_coefficients": True,
            "choice_vectors": [(zero, c, tuple(-x % 3 for x in c)) for c in columns],
            "target": target, "coefficient_domains": domains or [(0, 1, 2)]*len(columns)}


def test_affine_kernel_solver_matches_every_small_matrix_target_and_domain():
    for entries in product(range(3), repeat=4):
        columns = (entries[:2], entries[2:])
        for target in product(range(3), repeat=2):
            for domains in (((0, 1, 2),)*2, ((0, 2), (0, 1, 2))):
                case = linear_case(columns, target, domains)
                expected = {w for w in product(*domains)
                            if tuple(sum(c[l]*x for c, x in zip(columns, w)) % 3 for l in range(2)) == target}
                solved = linear_case_solutions(case, 2)
                assert solved["status"] == "complete"
                assert set(solved["solutions"]) == expected
                assert solved["affine_vectors_examined"] <= 9


def test_nullity_exclusion_is_not_misreported_as_no_solution():
    case = linear_case(((0, 0), (0, 0)), (0, 0))
    assert len(linear_case_solutions(case, 2)["solutions"]) == 9
    cut = linear_case_solutions(case, 1)
    assert cut["status"] == "excluded_nullity" and cut["nullity"] == 2
    assert cut["affine_vectors_examined"] == 0
    assert linear_case_solutions(linear_case((), (0,)), 0)["solutions"] == ((),)
    assert linear_case_solutions(linear_case((), (1,)), 0)["solutions"] == ()


@pytest.mark.parametrize("n", [1, 2, 3])
@pytest.mark.parametrize("cap", [0, None])
def test_cut_graph_incoming_is_complete_not_a_candidate_sampler(n, cap):
    source = random_native_source(n, 4, 75100+n)
    frequencies = low_source(source)
    words = tuple(product(range(3), repeat=source.inputs))
    arcs = {word: outgoing(frequencies, word, cap) for word in words}
    vertices = words if n < 3 else words[::11]
    for vertex in vertices:
        expected = {word for word, target in arcs.items() if target == vertex}
        assert set(incoming(frequencies, vertex, cap)) == expected
        neighbors = Counter(expected)
        if arcs[vertex] is not None:
            neighbors[arcs[vertex]] += 1
        row = dict(laplacian_row(frequencies, vertex, cap))
        assert row.get(vertex, 0) == sum(neighbors.values())
        assert all(row[w] == -weight for w, weight in neighbors.items())
        assert sum(row.values()) == 0


def test_gaussian_subspace_union_bound_against_complete_two_by_two_rank_law():
    from flint import nmod_mat
    counts = Counter()
    for entries in product(range(3), repeat=4):
        counts[2-nmod_mat([entries[:2], entries[2:]], 3).rank()] += 1
    for d in (1, 2):
        probability = Fraction(sum(v for nullity, v in counts.items() if nullity >= d), 81)
        assert probability <= Fraction(gaussian_binomial(2, d), 3**(2*d))
    assert gaussian_binomial(2, 1) == 4 and gaussian_binomial(2, 3) == 0


@pytest.mark.parametrize("n", [1, 2, 4, 8, 16, 64, 256])
def test_pointwise_cost_and_source_average_ledgers_are_distinct(n):
    ledger = graph_ledger(n)
    assert 3**(default_nullity_cap(n)-1) < n+2 <= 3**default_nullity_cap(n)
    assert ledger["affine_vectors_per_case_upper"] <= 3*(n+2)
    assert ledger["row_nonzeros_upper"] <= 2+3*(n+2)**2*math.comb(n+2, 2)
    assert 0 <= Fraction(ledger["native_average_retained_directed_arc_fraction_lower"]) <= Fraction(17, 18)
    assert not ledger["spectral_gap_or_secret_decoder_proved"]
    assert not ledger["reversible_gate_level_compilation_supplied"]


def test_native_collective_operator_is_PSD_nonstationary_and_publicly_gaugeable():
    source = random_native_source(2, 4, 319)
    frequencies = low_source(source)
    words, L = dense_calibration_laplacian(source)
    assert np.linalg.eigvalsh(L)[0] > -1e-12
    uniform = np.ones(len(words))/math.sqrt(len(words))
    assert np.max(abs(L @ uniform)) < 1e-12
    secret = (1, 2)
    state = np.array([np.exp(2j*np.pi*(sum(x*s for x, s in zip(source.value(w), secret)) % 9)/9)
                      for w in words])/math.sqrt(len(words))
    edge_energy = sum(abs(state[i]-state[words.index(z)])**2 for i, w in enumerate(words)
                      if (z := outgoing(frequencies, w)) is not None)
    assert edge_energy > .1
    assert abs(np.vdot(state, L @ state).real-edge_energy) < 1e-12
    chirp = public_chirp(source, words)
    gauged = chirp[:, None]*L*chirp.conj()[None, :]
    assert np.max(abs(np.linalg.eigvalsh(gauged)-np.linalg.eigvalsh(L))) < 1e-11
    for i in range(0, len(words), 9):
        for j in range(0, len(words), 7):
            assert abs(sparse_entry(frequencies, words[i], words[j], source=source)-gauged[i, j]) < 1e-11
    assert any(sum(a != b for a, b in zip(w, z)) > 1
               for w in words if (z := outgoing(frequencies, w)) is not None)


def test_fixed_width_sparse_index_program_has_distinct_padding_and_reverse_index():
    source = random_native_source(2, 4, 319)
    frequencies = low_source(source)
    vertex = (0, 1, 2, 0)
    locations = sparse_row_locations(frequencies, vertex)
    assert locations == tuple(sorted(set(locations)))
    assert len(locations) == min(3**source.inputs, graph_ledger(2)["row_nonzeros_upper"])
    assert set(dict(laplacian_row(frequencies, vertex))) <= set(locations)
    for i, w in enumerate(locations):
        assert locations.index(w) == i


@pytest.mark.parametrize("width", [0, 1, 2, 3])
def test_collective_onehot_L4_bound_including_entangled_coefficients(width):
    rng = np.random.default_rng(75300+width)
    coefficients = rng.normal(size=3**width)+1j*rng.normal(size=3**width)
    coefficients /= np.linalg.norm(coefficients)
    assert onehot_fourth_moment(coefficients, width) <= (5/3)**width+1e-10
    balanced = np.ones(3**width)/math.sqrt(3**width)
    assert abs(onehot_fourth_moment(balanced, width)-(5/3)**width) < 1e-10


def test_exact_third_root_average_has_no_alias_in_onehot_fourth_moment():
    coefficients = np.array([1+2j, 2-1j, -3j])/math.sqrt(19)
    average = sum(abs(coefficients[0]+np.exp(2j*np.pi*a/3)*coefficients[1]
                      +np.exp(2j*np.pi*b/3)*coefficients[2])**4 for a, b in product(range(3), repeat=2))/9
    assert abs(average-onehot_fourth_moment(coefficients, 1)) < 1e-11


def test_collective_low_blind_gate_is_not_general_or_per_instance_hardness():
    gate = low_blind_measurement_ledger(8, 16, 64)
    assert Fraction(gate["native_average_decoder_success_squared_upper"]) == Fraction(5, 9)**64/(1-Fraction(1, 3**8))
    assert gate["native_average_decoder_success_upper_approximation"] < 1e-8
    assert gate["native_average_decoder_success_upper"].startswith("sqrt(")
    assert gate["arbitrary_collective_low_controlled_POVM_included"]
    assert gate["unlimited_full_label_classical_postprocessing_included"]
    assert not gate["high_label_quantum_control_included"]
    assert not gate["per_fixed_label_lower_bound_or_general_quantum_lower_bound"]


@pytest.mark.parametrize("case", [(1, 4, 317), (2, 4, 319), (1, 8, 331)])
def test_native_readout_controls_keep_full_root_and_block_speedup_claims(case):
    report = readout_calibration(*case, times=(0., .7))
    assert report["modulus"] == 3**(case[1]//2)
    assert report["unitarity_error"] < 1e-11
    assert not report["speedup_claim_allowed"]
    assert report["dense_cube_and_all_secret_enumeration_are_calibration_only"]
    for row in report["readouts"]:
        assert row["normalization_error"] < 1e-11
        assert row["full_secret_ML_success"] <= report["known_optimal_PGM_reference_full_secret_success"]+1e-11
        assert row["full_secret_ML_success"] <= report["exact_component_preserving_optimal_full_secret_success"]+1e-11
        if row["time"] == 0:
            assert abs(row["full_secret_ML_success"]-1/report["secret_count"]) < 1e-12


def test_block_sum_oracle_and_global_chirp_are_genuinely_cross_block():
    sources = tuple(random_native_source(1, 8, 337+b) for b in range(2))
    vertex = (0, 1, 2, 1, 0, 2)
    row = dict(block_laplacian_row(sources, vertex))
    assert sum(row.values()) == 0
    assert len(row) <= 2*graph_ledger(1)["row_nonzeros_upper"]
    for target, entry in row.items():
        assert dict(block_laplacian_row(sources, target))[vertex] == entry
    report = readout_calibration(1, 8, 337, times=(0., .7), block_count=2)
    assert report["physical_qutrits"] == 6 and report["modulus"] == 81
    assert report["global_chirp_differs_from_product_block_chirps"]
    assert report["unitarity_error"] < 1e-10
    assert all(r["normalization_error"] < 1e-10 for r in report["readouts"])
    assert all(r["full_secret_ML_success"] <= report["known_optimal_PGM_reference_full_secret_success"]+1e-10
               for r in report["readouts"])
    assert not report["speedup_claim_allowed"]


def test_component_conservation_bounds_even_high_label_control_not_just_low_only():
    census = rank_one_component_census()
    histogram = {int(k): v for k, v in census["component_size_square_sum_histogram"].items()}
    assert sum(histogram.values()) == 729
    assert Fraction(sum(k*v for k, v in histogram.items()), 729*27) == Fraction(7357, 729)
    assert census["arbitrary_full_label_control_preserving_product_components_included"]
    assert census["cross_component_quantum_operations_or_more_samples_excluded"]
    report = readout_calibration(1, 4, 317, times=(.7,))
    assert report["exact_component_preserving_optimal_full_secret_success"] < report["known_optimal_PGM_reference_full_secret_success"]


def test_exact_public_phase_program_keeps_native_modulus_not_floating_field_alias():
    source = random_native_source(1, 40, 349)
    frequencies = low_source(source)
    word = (0, 1, 2)
    exponent = chirp_exponent(source, word)
    assert type(exponent) is int and 0 <= exponent < 3**20
    for neighbor, weight in laplacian_row(frequencies, word):
        spec = sparse_entry_spec(frequencies, word, neighbor, source=source)
        assert spec["integer_weight"] == weight and spec["phase_modulus"] == 3**20
        assert spec["phase_numerator"] == (exponent-chirp_exponent(source, neighbor)) % 3**20


def test_source_average_energy_identity_over_every_high_lift_not_a_field_shadow():
    from cyclotomic_fiber_receiver import inverse_frequency_coordinates, native_source
    source = random_native_source(1, 4, 317)
    frequencies = low_source(source)
    words, L = dense_calibration_laplacian(source)
    energy_sum = 0.
    for lifts in product(range(3), repeat=6):
        labels = [[inverse_frequency_coordinates(pair[0][0]+3*lifts[2*i],
                                                 pair[1][0]+3*lifts[2*i+1], 4)]
                  for i, pair in enumerate(frequencies)]
        lifted = native_source(labels, 4)
        state = np.exp(2j*np.pi*np.array([lifted.value(w)[0] for w in words])/9)/math.sqrt(27)
        energy_sum += np.vdot(state, L @ state).real
    arc_count = sum(outgoing(frequencies, w) is not None for w in words)
    assert abs(energy_sum/729-2*arc_count/27) < 1e-11


def test_invalid_inputs_do_not_silently_change_access_or_native_source():
    source = random_native_source(1, 4, 317)
    frequencies = low_source(source)
    with pytest.raises(ValueError):
        incoming(frequencies, (0, 0, 0), cap=True)
    with pytest.raises(ValueError):
        low_blind_measurement_ledger(1, 3, 3)
    with pytest.raises(ValueError):
        linear_case_solutions({**linear_case(((1,),), (0,)), "corner": 1}, 1)
    with pytest.raises(ValueError):
        onehot_fourth_moment(np.ones(3**7), 7)
    with pytest.raises(ValueError):
        readout_calibration(2, 8, 3)
