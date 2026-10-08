from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import subprocess

import pytest

from cyclotomic_fiber_receiver import inverse_frequency_coordinates, native_source
from ternary_cyclic_extractor import random_even_source
from ternary_coherent_edge_receiver import (
    NativeEdgeProgram, add, digits, erasure_physical_control, explicit_rows, fiber_structure_control, geometric_control, graph,
    natural_moment_control, negative, offset, orientation_tape,
    physical_control, population_certificate, rank, short_grover_template_bound, source_class_trimming_bound, translation_control, unit_minor_controls,
)
from dcp_coherent_edge_sampling import geometric_kernel
from ternary_least_trit_bootstrap import least_trit_reference


@pytest.mark.parametrize("width", [1, 2, 3])
def test_native_orientation_is_full_basis_reversible_including_padding_and_both_bits(width):
    D = 3**width; P = 1 << (D-2).bit_length(); images = set()
    for x, index, bit in product(range(D), range(P), range(2)):
        word = digits(x, width)
        result = orientation_tape(width, word, index, bit)
        assert orientation_tape(width, *result, inverse=True) == (word, index, bit)
        images.add(result)
        d = offset(width, index)
        if d is None:
            assert result == (word, index, bit)
        elif bit == 0:
            reverse = rank(negative(d))-1
            partner = orientation_tape(width, add(word, d), reverse)
            assert result[:2] == partner[:2] and result[2] != partner[2]
            assert next(t for t in offset(width, result[1]) if t) == 1
    assert len(images) == 2*D*P


def test_binary_involution_assumption_would_be_wrong_on_native_offsets():
    x, d = (0, 1), (1, 2)
    assert add(add(x, d), d) != x
    assert add(add(add(x, d), d), d) == x


@pytest.mark.parametrize("n,r", [(1, 5), (2, 3), (4, 8), (1, 64)])
def test_exact_natural_signal_certificate_charges_exponential_search_not_a_speedup(n, r):
    c = population_certificate(n, r)
    D, G = int(c["native_words"]), int(c["full_frequency_group"])
    assert G == 9*D and c["source_qutrits"] == n*r-2
    assert c["mean_degree"] == Fraction(2*(D-1), G)
    assert c["second_degree_moment"] == c["mean_degree"]**2+c["mean_degree"]*(1-Fraction(2, G))
    assert c["bounded_degree_oriented_mass_lower"] >= Fraction(5, 36)
    assert c["universal_infinite_interference_lower"] == Fraction(1, 30420)
    assert c["raw_trit_advantage_after_charged_abort_lower"] > 0
    h = c["schedule"]["coin_bits"]
    assert c["schedule"]["mean_reversible_predicate_calls_upper"] == 2**(h+1)-1
    assert c["schedule"]["maximum_reversible_predicate_calls"] == 32*2**h-1
    assert not c["polynomial_runtime_proved"] and not c["new_quantum_speedup_proved"]
    assert not c["classical_pair_finder_required"] and not c["bounded_degree_vertices_selected"]
    assert not c["cyclic_DHSP_vector_source_acquisition_supplied"]


def test_insufficient_truncation_and_small_roots_cannot_be_promoted():
    c = population_certificate(1, 5, 4)
    assert not c["positive_advantage_certified"] and c["raw_trit_advantage_after_charged_abort_lower"] < 0
    with pytest.raises(ValueError, match="n.r>=5"):
        population_certificate(1, 4)


@pytest.mark.parametrize("n,r,j", [(1, 5, 0), (2, 3, 0), (2, 3, 1)])
def test_actual_native_oracle_reflections_and_trine_born_score_cover_all_secret_types(n, r, j):
    source = random_even_source(n, 2*r, n*r-2, 98304)
    program = NativeEdgeProgram(source, j)
    for t in (0, 1, 2, 5, 11):
        for secret in ((0,)*n, (3,)*n, (source.modulus-1,)*n):
            c = physical_control(program, t, secret)
            assert max(c[k] for k in ("Born_score_residual", "probability_normalization_residual",
                                     "Grover_row_norm_residual", "marked_amplitude_residual")) < 3e-12
            assert 0 <= c["raw_correct_probability"] <= 1
            assert not c["conditional_normalization_used"] and not c["unknown_secret_used_to_select_edges"]


def test_endpoint_specific_original_offset_tag_erases_signal_not_merely_reduces_success():
    source = random_even_source(1, 10, 3, 98302); program = NativeEdgeProgram(source)
    clean = physical_control(program, 0, (242,)); dirty = physical_control(program, 0, (242,), True)
    assert clean["raw_correct_probability"] > 1/3
    assert abs(dirty["raw_correct_probability"]-1/3) < 1e-12
    assert clean["heralded_probability"] == dirty["heralded_probability"]


@pytest.mark.parametrize("seed", [98301, 98302, 98303])
def test_shared_time_exact_kernel_matches_repeated_unitary_dynamics_with_charged_aborts(seed):
    p = NativeEdgeProgram(random_even_source(1, 10, 3, seed)); c = geometric_control(p)
    assert c["infinite_interference_exact"] >= 0
    assert c["tail_error"] <= c["actual_abort_probability"]+2e-12
    assert c["actual_abort_probability"] <= float(c["certified_tail_upper"])
    assert not c["per_label_constant_advantage_claimed"]


def test_prespecified_no_edge_native_source_is_retained_and_returns_chance():
    source = native_source([[(0, 0)]]*3, 10); p = NativeEdgeProgram(source)
    c = physical_control(p, 2, (17,)); g = geometric_control(p)
    assert c["heralded_probability"] == 0 and c["raw_correct_probability"] == 1/3
    assert g["infinite_interference_exact"] == 0 and g["oriented_edges"] == 0


def test_entire_original_native_source_degree_census_matches_pairwise_moments():
    c = natural_moment_control()
    assert c["complete_native_label_pairs"] == 729
    assert c["complete_label_word_assignments"] == 2187
    assert c["mean_degree"] == Fraction(4, 27)
    assert not c["constant_advantage_large_root_bound_applied_here"]


def test_full_native_high_labels_are_legitimate_not_a_low_only_helper():
    # These a labels have identical lower syndrome but distinct target high trits.
    p0 = NativeEdgeProgram(native_source([[inverse_frequency_coordinates(0, 0, 6)]], 6))
    p1 = NativeEdgeProgram(native_source([[inverse_frequency_coordinates(9, 0, 6)]], 6))
    assert not p0.marked((0,), 0) and p1.marked((0,), 0)
    assert p1.marked((1,), 1)


def test_actual_native_fixed_time_can_have_negative_signal_despite_nonzero_heralding():
    p = NativeEdgeProgram(native_source([[inverse_frequency_coordinates(9, 0, 6)]], 6))
    c = physical_control(p, 1, (26,))
    assert abs(c["oriented_interference"]+2/3) < 1e-12
    assert abs(c["raw_correct_probability"]-1/9) < 1e-12
    assert abs(c["heralded_probability"]-2/3) < 1e-12
    assert geometric_control(p)["infinite_interference_exact"] > 0


def test_pointed_native_minor_controls_are_unit_even_over_composite_moduli():
    controls = unit_minor_controls()
    assert len(controls) == 9*8*7
    for c in controls:
        a, b = c["columns"]; u, v = c["rows"]
        determinant = u[a]*v[b]-u[b]*v[a]
        assert determinant == c["integer_determinant"] and abs(determinant) == 1


@pytest.mark.parametrize("n,r,seed,j", [(1,5,98301,0),(1,5,98302,0),(2,3,98304,1)])
def test_actual_tripartite_blocks_reconstruct_graph_but_do_not_grant_access(n,r,seed,j):
    p = NativeEdgeProgram(random_even_source(n,2*r,n*r-2,seed),j)
    c = fiber_structure_control(p); D = p.size
    assert c["native_uniform_source_words_partitioned"] == D
    assert c["compressed_adjacency_reconstruction_residual"] < 2e-12
    assert c["raw_public_Fourier_erasure_success"] == Fraction(c["exact_full_frequency_collision_count"],D*D)
    assert c["mean_erasure_success_over_all_IID_labels"] == Fraction(1,D)+Fraction(D-1,D*p.source.group_size)
    assert c["singleton_class_singular_value_squared"] == Fraction(1,D)
    assert not c["class_counts_or_uniform_basis_given_to_receiver"]
    assert not c["coherent_uniform_class_inverse_preparation_implemented"]
    assert not c["generic_quantum_lower_bound_proved"] and not c["quantum_speedup_proved"]
    rows = tuple(tuple(tuple(row[k] for k in [j,*[i for i in range(n) if i!=j]]) for row in pair)
                 for pair in p.source.frequencies)
    optimum = least_trit_reference(rows,r)["optimal_uniform_secret_least_trit_success"]
    assert abs(c["ideal_class_compressed_raw_trit_success"]-optimum) < 2e-12


def test_small_three_class_spectral_block_does_not_remove_erasure_normalization():
    source = native_source([[inverse_frequency_coordinates(9,18,6)]],6)
    c = fiber_structure_control(NativeEdgeProgram(source))
    b = c["complete_nuisance_fibers"][0]
    assert b["class_counts"] == [1,1,1] and b["class_degrees"] == [2,2,2]
    assert b["compressed_adjacency_characteristic"] == ["1","0","-3","-2"]
    assert b["compressed_adjacency_rank"] == 3
    assert b["uniform_class_erasure_singular_values_squared"] == [Fraction(1,3)]*3
    assert abs(c["ideal_class_compressed_raw_trit_success"]-1) < 1e-12
    assert c["raw_public_Fourier_erasure_success"] == Fraction(1,3)


def test_full_root_homomorphism_requires_cycle_wrap_not_only_low_degree_mod_three():
    good = NativeEdgeProgram(native_source([[inverse_frequency_coordinates(9,18,6)]],6))
    bad = NativeEdgeProgram(native_source([[inverse_frequency_coordinates(1,2,6)]],6))
    assert translation_control(good)["native_F_is_group_homomorphism"]
    c = translation_control(bad)
    assert not c["native_F_is_group_homomorphism"]
    assert c["first_exact_cycle_disagreement"]["actual_full_frequency_increment_rows"] == [(1,),(1,),(25,)]
    assert c["IID_probability_of_exact_homomorphism"] == {"base":3,"negative_exponent":5}
    assert not c["rules_out_general_structure_aware_Fourier_transforms"]


def test_empty_informative_graph_does_not_make_nonhomomorphic_native_source_a_character():
    p = NativeEdgeProgram(random_even_source(1,10,3,98301))
    assert physical_control(p,0,(0,))["heralded_probability"] == 0
    assert not translation_control(p)["native_F_is_group_homomorphism"]
    assert not translation_control(p)["native_informative_graph_invariance_inferred_from_nonhomomorphism"]


def test_high_root_translation_obstruction_is_exact_public_arithmetic_not_dense_search():
    p = NativeEdgeProgram(random_even_source(1,128,62,98403))
    c = translation_control(p)
    assert len(c["native_rows"]) == 62 and c["dense_native_words_enumerated"] == 0
    assert c["IID_probability_of_exact_homomorphism"]["negative_exponent"] == 62*127
    assert not c["quantum_algorithm_no_go_proved"]


@pytest.mark.parametrize("n,r,j", [(1,5,0),(2,3,0),(2,3,1)])
def test_actual_source_fourier_erasure_charges_exponential_success_loss(n,r,j):
    p = NativeEdgeProgram(random_even_source(n,2*r,n*r-2,98304),j)
    for secret in ((0,)*n,(3,)*n,(p.source.modulus-1,)*n):
        c = erasure_physical_control(p,secret)
        predicted = fiber_structure_control(p)["raw_public_Fourier_erasure_success"]
        assert c["predicted_raw_erasure_success_exact"] == predicted
        assert abs(c["actual_raw_erasure_success"]-float(predicted)) < 2e-12
        assert c["full_label_output_amplitude_residual"] < 2e-12 and c["whole_unitary_norm_residual"] < 2e-12
        assert abs(c["actual_raw_erasure_success"]+c["charged_rejection_probability"]-1) < 2e-12
        assert not c["unknown_source_inverse_used"] and not c["output_success_renormalized"]
        assert not c["uniform_class_inverse_preparation_implemented"]


def test_source_weighted_large_class_trim_cannot_fix_global_erasure_scale_for_free():
    c = source_class_trimming_bound(1,64); D=int(c["native_words"]); G=9*D
    assert c["minimum_retained_class_size"] == str((D+4095)//4096)
    assert c["exact_mean_source_weighted_excess_class_size"] == Fraction(D-1,G)
    assert c["mean_singleton_source_mass_lower"] > Fraction(8,9)
    assert c["mean_retained_source_mass_upper"] < Fraction(1,10**20)
    assert c["raw_trit_advantage_upper_if_discarded_outputs_guessed_uniform"] == 2*c["mean_retained_source_mass_upper"]/3
    assert not c["lower_bound_against_other_normalizations_or_quantum_receivers"]
    assert not c["large_classes_assumed_physically_filterable"]


def test_trimming_keeps_full_mass_when_no_singleton_is_discarded_and_checks_entire_census():
    c=source_class_trimming_bound(1,3,Fraction(1,3))
    assert c["minimum_retained_class_size"] == "1" and c["mean_retained_source_mass_upper"] == 1
    census=natural_moment_control(); conservative=source_class_trimming_bound(1,3,Fraction(2,3))
    non_singletons=Fraction(census["complete_label_word_assignments"]-census["singleton_native_word_assignments"],census["complete_label_word_assignments"])
    assert non_singletons <= conservative["mean_retained_source_mass_upper"]
    assert Fraction(census["singleton_native_word_assignments"],2187) >= conservative["mean_singleton_source_mass_lower"]
    with pytest.raises(ValueError,match="threshold"):
        source_class_trimming_bound(1,5,0)


def test_polynomial_time_cap_in_unchanged_generic_edge_template_gives_exponentially_weak_bound():
    c=short_grover_template_bound(1,64,64**2)
    assert c["raw_trit_advantage_upper"] < Fraction(1,10**20)
    assert c["label_dependent_shared_time_within_cap_allowed"]
    assert not c["rules_out_general_quantum_measurements_or_modified_oracles"]
    t0=short_grover_template_bound(1,5,0)
    assert t0["raw_trit_advantage_upper"] == t0["native_mean_degree"]/(3*t0["padded_offset_domain"])


def test_actual_native_template_obeys_pointwise_oriented_degree_time_bound():
    p=NativeEdgeProgram(random_even_source(1,10,3,98302)); g=geometric_control(p)
    mean=Fraction(g["oriented_edges"],p.size)
    for t in (0,1,2,5,11):
        signal=physical_control(p,t,(242,))["oriented_interference"]
        assert abs(signal) <= float(mean*(2*t+1)**2/p.padded)+1e-12


def test_positive_shared_kernel_and_bounded_degree_lower_bound_are_exact():
    for P in (8, 32):
        cap = min(8, P//2)
        assert all(geometric_kernel(a, b, P) > 0 for a, b in product(range(1, P+1), repeat=2))
        assert all(geometric_kernel(a, b, P) >= Fraction(1, (1+8*cap)**2)
                   for a, b in product(range(1, cap+1), repeat=2))


def test_whole_diagnostic_preflight_and_native_source_validation_fail_closed():
    p = NativeEdgeProgram(random_even_source(1, 10, 3, 1))
    with pytest.raises(ValueError, match="no partial proof"):
        graph(p, 2)
    with pytest.raises(ValueError, match="underfull"):
        NativeEdgeProgram(random_even_source(1, 10, 2, 1))
    with pytest.raises(ValueError, match="coordinate"):
        NativeEdgeProgram(p.source, True)
    with pytest.raises(ValueError, match="iteration"):
        explicit_rows(p, -1)
    with pytest.raises(ValueError, match="secret"):
        physical_control(p, 1, (-1,))
    with pytest.raises(ValueError, match="index"):
        offset(2, True)


@pytest.mark.parametrize("mutation", ["speedup", "cost", "degree", "frequency", "Born", "negative", "erasure", "fiberbasis", "character", "characterprob", "trimming"])
def test_independent_checker_rejects_corrupted_scopes_costs_and_physical_evidence(tmp_path, mutation):
    root = Path(__file__).resolve().parents[1]
    record = json.loads((root/"research/phase_workbench/ternary_coherent_edge_receiver.json").read_text())
    if mutation == "speedup": record["quantum_speedup_proved"] = True
    elif mutation == "cost": record["population_certificates"][-1]["schedule"]["mean_reversible_predicate_calls_upper"] = 1
    elif mutation == "degree": record["whole_source_degree_census"]["second_degree_moment"] = "1"
    elif mutation == "frequency": record["prespecified_native_physical_cases"][1]["full_frequencies"][0][0][0] = 0
    elif mutation == "Born": record["prespecified_native_physical_cases"][1]["physical_controls"][0]["raw_correct_probability"] = 0.9
    elif mutation == "erasure": record["prespecified_native_physical_cases"][1]["fiber_structure_control"]["raw_public_Fourier_erasure_success"] = "1"
    elif mutation == "fiberbasis": record["prespecified_native_physical_cases"][1]["fiber_structure_control"]["coherent_uniform_class_inverse_preparation_implemented"] = True
    elif mutation == "character": record["scalable_native_translation_controls"][-1]["translation_control"]["native_F_is_group_homomorphism"] = True
    elif mutation == "characterprob": record["scalable_native_translation_controls"][-1]["translation_control"]["IID_probability_of_exact_homomorphism"]["negative_exponent"] = 1
    elif mutation == "trimming": record["source_class_trimming_bounds"][-1]["mean_retained_source_mass_upper"] = "1"
    else: record["fixed_time_cancellation_control"]["physical_control"]["oriented_interference"] = 2/3
    report = tmp_path/"corrupted.json"; report.write_text(json.dumps(record))
    result = subprocess.run(["node", str(root/"research/certificates/ternary_coherent_edge_receiver_crosscheck.js"), str(report)], capture_output=True, text=True)
    assert result.returncode != 0
    assert "Error:" in result.stderr
