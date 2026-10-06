from fractions import Fraction
from itertools import product
import random

import pytest

from cyclotomic_fiber_receiver import inverse_frequency_coordinates, native_source
from ternary_curvature_frontier import (
    apply_gate_word, coordinate_recipe, curvature_certificate,
    exhaustive_scalar_census, iid_retention_ledger, physical_word,
    scalar_witt_dimension, scalar_witt_frame, simultaneous_retention_screen,
    source_control, subspaces,
)
from ternary_cyclic_extractor import curvatures, random_even_source


def source(pairs, level=4):
    return native_source([[inverse_frequency_coordinates(a, c, level) for a, c in row] for row in pairs], level)


@pytest.mark.parametrize("width", [1, 2, 3, 4])
def test_entire_scalar_curvature_space_and_every_subspace_prove_sharp_small_width_bound(width):
    census = exhaustive_scalar_census(width)
    assert census["curvature_arrays"] == 3**width
    assert census["sharp_bound_and_compiler_agree_with_entire_census"]
    if width == 4:
        assert census["all_F3_subspaces"] == 212
        assert census["curvature_subspace_pairs_checked"] == 17172


@pytest.mark.parametrize("width", [8, 32, 128, 512])
def test_polynomial_scaled_scalar_compiler_attains_exact_witt_dimension(width):
    rng = random.Random(55170+width); B = tuple(rng.randrange(3) for _ in range(width))
    frame = scalar_witt_frame(B)
    assert len(frame["columns"]) == scalar_witt_dimension(B)["maximum_totally_isotropic_dimension"]
    assert frame["certificate"]["low_phase_affine_on_every_measured_complement"]
    assert frame["selection_reads_only_curvature"]
    assert not frame["certificate"]["full_root_product_output_certified"]


@pytest.mark.parametrize("B,expected", [((1,), 0), ((0,), 1), ((1, 1), 0), ((1, 2), 1),
                                      ((1, 1, 1), 1), ((1,)*4, 2), ((1,)*6, 2), ((0, 0, 1, 1), 2)])
def test_rank_radical_and_anisotropic_tail_are_all_charged(B, expected):
    assert scalar_witt_dimension(B)["maximum_totally_isotropic_dimension"] == expected
    assert len(scalar_witt_frame(B)["columns"]) == expected


def test_all_three_digit_maps_low_phase_affine_iff_gram_zero_not_merely_individual_isotropy():
    spaces = list(subspaces(3))
    for B in product(range(3), repeat=3):
        for columns in spaces:
            certificate = curvature_certificate([(x,) for x in B], columns)
            def F(z):
                w = tuple(sum(v[i]*x for v, x in zip(columns, z)) % 3 for i in range(3))
                return sum(b for b, x in zip(B, w) if x == 2) % 3
            k = len(columns)
            linear = [F(tuple(int(i == j) for i in range(k))) for j in range(k)]
            affine = all(F(z) == sum(a*x for a, x in zip(linear, z)) % 3 for z in product(range(3), repeat=k))
            assert affine == certificate["low_phase_affine_on_every_measured_complement"]
    # Two individually isotropic but mutually nonorthogonal vectors fail.
    certificate = curvature_certificate([(1,)]*4, ((1, 1, 1, 0), (1, 1, 0, 1)))
    assert certificate["component_Gram_matrices"][0][0][0] == 0
    assert certificate["component_Gram_matrices"][0][1][1] == 0
    assert not certificate["low_phase_affine_on_every_measured_complement"]


@pytest.mark.parametrize("B", [(1,)*4, (0, 1, 2), (0,)*4, (1, 1)])
def test_coordinate_completion_and_explicit_gate_recipe_are_bijections_for_every_original_word(B):
    columns = scalar_witt_frame(B)["columns"]; recipe = coordinate_recipe(columns, len(B))
    seen = set()
    for word in product(range(3), repeat=len(B)):
        logical = apply_gate_word(word, recipe)
        assert logical == tuple(sum(a*x for a, x in zip(row, word)) % 3 for row in recipe["forward_matrix"])
        assert physical_word(recipe, logical) == word
        seen.add(logical)
    assert len(seen) == 3**len(B)
    assert not recipe["unknown_state_preparation_inverse_or_cloning_required"]
    assert recipe["coherent_pointer_unknown_anchor_phases_must_be_retained"]


def test_optimal_curvature_cancellation_still_has_exact_full_root_mixed_defect_and_entangled_output():
    native = source([[(0, 1)]]*4); frame = scalar_witt_frame((1,)*4)
    control = source_control(native, frame["columns"], (1,))
    assert len(control["all_measured_pointer_branches"]) == 9
    assert sum(b["probability"] for b in control["all_measured_pointer_branches"]) == pytest.approx(1)
    for branch in control["all_measured_pointer_branches"]:
        assert branch["probability"] == pytest.approx(1/9)
        assert all(all(x % 3 == 0 for x in d["mixed_frequency_defect"]) for d in branch["nonzero_mixed_phase_defects"])
    first = control["all_measured_pointer_branches"][0]
    assert first["original_frequency_table"] == [(0,), (1,), (2,), (0,), (1,), (2,), (3,), (1,), (2,)]
    assert first["nonzero_mixed_phase_defects"] == [
        {"logical_word": (2, 1), "mixed_frequency_defect": (6,)},
        {"logical_word": (2, 2), "mixed_frequency_defect": (6,)}]
    assert first["calibration_first_logical_purity"] == pytest.approx(19/27)
    assert not first["componentwise_separable_for_all_secrets"]
    assert control["maximum_full_root_gate_error"] < 1e-12
    assert not control["calibration_purity_is_an_unknown_secret_estimator"]
    assert not control["identically_labeled_quantum_copies_for_SWAP_test_supplied"]
    # The SAME public table separates at secret0; source-wide certification is stronger.
    constant = source_control(native, frame["columns"], (0,))
    assert constant["all_measured_pointer_branches"][0]["calibration_first_logical_purity"] == pytest.approx(1)
    assert not constant["all_measured_pointer_branches"][0]["componentwise_separable_for_all_secrets"]


def test_zero_curvature_uncoupled_positive_control_is_product_not_declared_hard():
    native = source([[pair] for pair in [(1, 5), (2, 1), (4, 8), (5, 7)]])
    frame = scalar_witt_frame((0,)*4); control = source_control(native, frame["columns"], (1,))
    assert len(frame["columns"]) == 4
    assert len(control["all_measured_pointer_branches"]) == 1
    branch = control["all_measured_pointer_branches"][0]
    assert branch["componentwise_separable_for_all_secrets"]
    assert branch["calibration_first_logical_purity"] == pytest.approx(1)
    assert not control["recursive_source_law_or_speedup_supplied"]


def test_every_secret_component_needs_isotropy_and_pair_direction_screens_are_scoped():
    vectors = [(1, 0), (1, 0), (1, 0), (1, 1)]
    columns = scalar_witt_frame((1,)*4)["columns"]
    assert not curvature_certificate(vectors, columns)["low_phase_affine_on_every_measured_complement"]
    native = source([[(0, a), (0, b)] for a, b in vectors])
    with pytest.raises(ValueError, match="Gram matrices must vanish"):
        source_control(native, columns, (1, 1))
    screen = simultaneous_retention_screen(vectors)
    assert screen["all_projective_directions_enumerated"]
    assert screen["simultaneous_isotropic_dimension_upper_bound"] <= 2
    assert not screen["simultaneous_optimal_frame_constructed"]
    larger = simultaneous_retention_screen([(1, 1, 1)]*4)
    assert not larger["all_projective_directions_enumerated"]


def test_original_higher_root_multicomponent_screen_is_polynomial_and_only_a_necessary_gate():
    native = random_even_source(4, 16, 100, 88794)
    screen = simultaneous_retention_screen(curvatures(native))
    assert len(screen["scalar_direction_screens"]) == 16
    assert screen["public_F3_scalar_multiply_adds"] == 6400
    assert 0 < screen["simultaneous_isotropic_dimension_upper_bound"] < 100
    assert not screen["all_projective_directions_enumerated"]
    assert not screen["simultaneous_optimal_frame_constructed"]
    assert not screen["general_quantum_decoder_lower_bound"]


@pytest.mark.parametrize("width", [1, 2, 3, 4, 5, 6])
def test_expected_optimal_width_formula_matches_entire_iid_curvature_distribution(width):
    expected = Fraction(sum(scalar_witt_dimension(B)["maximum_totally_isotropic_dimension"]
                            for B in product(range(3), repeat=width)), 3**width)
    ledger = iid_retention_ledger(width)
    assert Fraction(ledger["exact_expected_maximum_low_affine_width"]) == expected
    assert expected < Fraction(2*width, 3)
    assert not ledger["applying_the_same_IID_law_after_this_joint_step_certified"]
    assert not ledger["arbitrary_coherent_decoder_lower_bound"]


@pytest.mark.parametrize("columns,width", [(((1, 0), (1, 0)), 2), (((1,),), 2), (((True,),), 1), (((3,),), 1)])
def test_dependent_or_noncanonical_frames_fail_closed(columns, width):
    with pytest.raises(ValueError): coordinate_recipe(columns, width)


def test_dense_budget_and_secret_checks_never_present_unreplayed_instrument():
    with pytest.raises(ValueError, match="width4"): list(subspaces(5))
    native = source([[(0, 1)]]*4); columns = scalar_witt_frame((1,)*4)["columns"]
    with pytest.raises(ValueError, match="integer calibration"): source_control(native, columns, (True,))
    with pytest.raises(ValueError): iid_retention_ledger(0)
