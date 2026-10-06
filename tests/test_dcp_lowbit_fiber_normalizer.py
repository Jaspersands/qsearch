from fractions import Fraction

import pytest

from dcp_carry_packets import compile_packet
from dcp_physical_phase_noise import read
from dcp_lowbit_fiber_normalizer import (
    _apply_rows, _complete_middle_source_controls, _higher_carry_countercontrol,
    _inverse_rows, compile_normalizer, lowbit_source_certificate,
)


def test_binary_inverse_is_exact_and_rejects_singular_matrices():
    rows = (3, 6, 4)
    inverse = _inverse_rows(rows)
    for value in range(8):
        assert _apply_rows(inverse, _apply_rows(rows, value)) == value
    with pytest.raises(ValueError):
        _inverse_rows((1, 1))


def test_normalizer_is_reversible_without_enumeration_or_rank_assumption():
    for labels in ([[1, 1, 1, 1, 1, 1]], [[3, 5, 1, 11, 9, 7]]):
        normalizer = compile_normalizer(compile_packet(labels, 16))
        outputs = [normalizer.normalize(z) for z in range(32)]
        assert sorted(outputs) == list(range(32))
        for z, output in enumerate(outputs):
            assert normalizer.denormalize(output) == z


def test_successful_backgrounds_normalize_actual_residue_bits():
    normalizer = compile_normalizer(compile_packet([[3, 5, 1, 11, 9, 7]], 16))
    for z in range(32):
        w = normalizer.normalize(z)
        if normalizer.background_plan(w >> normalizer.isotropic_width)["full_residue_bit_rank"]:
            assert w & 1 == normalizer.packet.residual(z)[0] & 1


def test_low_geometry_is_selected_before_middle_and_higher_labels():
    a = compile_normalizer(compile_packet([[1] * 6], 16))
    b = compile_normalizer(compile_packet([[3, 5, 1, 11, 9, 7]], 16))
    assert a.isotropic_directions == b.isotropic_directions
    assert a.basis_columns == b.basis_columns


def test_entire_middle_source_matrix_law_not_only_favorable_cases():
    rows = _complete_middle_source_controls()
    assert [row["all_middle_label_tables"] for row in rows] == [64, 4096]
    for row in rows:
        assert row["whole_permutation_inverse_and_residue_checks"] == row["all_middle_label_tables"] * 2**row["logical_width"]
        assert row["distinct_linear_matrices_per_background"] * row["each_linear_matrix_source_multiplicity"] == row["all_middle_label_tables"]


def test_lattice_first_layer_bound_is_not_a_full_decoder():
    row = lowbit_source_certificate(128, 4 * 128**2 + 16)
    assert read(row["source_mean_bad_background_fraction_upper_bound"]) < Fraction(1, 2**300)
    assert row["both_directions_uniform_polynomial_classical_evaluators"]
    assert not row["logical_assignments_or_fibers_enumerated_by_compiler"]
    assert not row["higher_residue_layer_closed_under_same_quadratic_model"]
    assert not row["unknown_secret_recovered"]


def test_actual_next_bit_can_leave_native_quadratic_model():
    row = _higher_carry_countercontrol()
    assert row["all_backgrounds_full_rank"]
    assert row["higher_quotient_low_bit_degree"] > 2
    assert row["blind_reuse_of_native_quadratic_first_layer_model_falsified"]
    assert not row["all_higher_bit_algorithms_or_other_parameterizations_ruled_out"]


def test_invalid_charts_domains_and_undersized_guarantees_rejected():
    with pytest.raises(ValueError):
        compile_normalizer(compile_packet([[1, 0, 1]], 8, syndrome=1))
    with pytest.raises(ValueError):
        compile_normalizer(compile_packet([[0] * 6], 8))
    with pytest.raises(ValueError):
        lowbit_source_certificate(3, 11)
    normalizer = compile_normalizer(compile_packet([[1] * 6], 8))
    for method in (normalizer.normalize, normalizer.denormalize):
        with pytest.raises(ValueError):
            method(32)
    with pytest.raises(ValueError):
        normalizer.background_plan(1 << (5 - normalizer.isotropic_width))
