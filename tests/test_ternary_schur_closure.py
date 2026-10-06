from itertools import combinations_with_replacement, product
import math
import random

import pytest

from ternary_carry_packets import compile_packet
from ternary_phase_depth import NativePhaseHierarchy
from ternary_schur_closure import (
    fixed_frame_probability, frame_columns, native_evaluation_countercontrol,
    native_large_countercontrol, native_refinement_control, native_restriction,
    odd_power_basis, projective_classes, run_controls, schur_admission,
)
from ternary_schur_tensor import combine, rank


@pytest.mark.parametrize("width,degree", [(1, 7), (2, 3), (2, 9), (3, 3), (3, 5), (4, 7)])
def test_iterated_span_equals_explicit_all_mixed_monomials(width, degree):
    rng = random.Random(49181+width)
    while True:
        columns = tuple(tuple(rng.randrange(3) for _ in range(9)) for _ in range(width))
        if rank(columns, 9) == width:
            break
    record = odd_power_basis(columns, degree)
    explicit = [tuple(math.prod(columns[j][i] for j in factors) % 3 for i in range(9))
                for factors in combinations_with_replacement(range(width), degree)]
    basis = [word for word, _ in record["basis"]]
    assert rank(basis, 9) == rank(explicit, 9) == len(basis)
    assert rank(basis+explicit, 9) == len(basis)
    for word, factors in record["basis"]:
        assert len(factors) == degree
        assert word == tuple(math.prod(columns[j][i] for j in factors) % 3 for i in range(9))


@pytest.mark.parametrize("dimension", [1, 2, 3, 4])
def test_odd_saturation_is_complete_projective_signed_block_span(dimension):
    points = tuple(product(range(3), repeat=dimension))
    columns = tuple(tuple(x[j] for x in points) for j in range(dimension))
    geometry = projective_classes(columns)
    assert geometry["projective_length"] == (3**dimension-1)//2
    assert geometry["zero_row_coordinates"] == [0]
    power = odd_power_basis(columns, 2*dimension-1)
    basis = [word for word, _ in power["basis"]]
    blocks = [c["signed_block_word"] for c in geometry["classes"]]
    assert len(basis) == len(blocks)
    assert rank(basis+blocks, len(points)) == len(blocks)
    for j, column in enumerate(columns):
        assert combine(blocks, [c["representative"][j] for c in geometry["classes"]], len(points)) == column


def test_actual_native_level3_admission_fails_after_schur_saturation():
    record = native_evaluation_countercontrol()
    controls = record["level_controls"]
    assert [c["higher_Schur_admission"] for c in controls] == [True, False, False, False]
    assert [c["power_dimension"] for c in controls] == [10, 13, 13, 13]
    assert [c["odd_power_saturated"] for c in controls] == [False, True, True, True]
    assert not any(c["all_odd_powers_admitted"] for c in controls)
    assert controls[0]["disjoint_kernel_refinement"]["certified"] is False
    assert all(any(c["native_top_derivative_of_failure_witness"]) for c in controls[1:])
    assert controls[-1]["evaluated_through_degree"] == 5
    assert len(controls[-1]["mixed_failure_witness"]["basis_factor_indices"]) == 19


def test_overlapping_admitted_frame_has_larger_disjoint_kernel_refinement():
    record = native_refinement_control()["restriction"]
    refinement = record["disjoint_kernel_refinement"]
    assert record["all_odd_powers_admitted"] and refinement["certified"]
    assert refinement["dimension"] == 3 > len(record["physical_frame_columns"])
    assert all(not any(row) for row in record["signed_block_component_images"])
    supports = [set(i for i, x in enumerate(c) if x) for c in refinement["signed_blocks"]]
    assert all(not (a & b) for i, a in enumerate(supports) for b in supports[i+1:])
    assert not refinement["new_source_sampler_or_complete_receiver"]


@pytest.mark.parametrize("dimension,degree", [(1, 3), (2, 3), (2, 5), (3, 7)])
def test_odd_power_spaces_are_nested_by_two_and_reach_disjoint_space(dimension, degree):
    rng = random.Random(49183+dimension)
    while True:
        columns = tuple(tuple(rng.randrange(3) for _ in range(8)) for _ in range(dimension))
        if rank(columns, 8) == dimension:
            break
    first, second = (odd_power_basis(columns, d) for d in (degree, degree+2))
    B, C = ([w for w, _ in p["basis"]] for p in (first, second))
    assert rank(B+C, 8) == len(C)
    assert len(C) == second["projective_geometry"]["projective_length"]


@pytest.mark.parametrize("secret_dimension", [1, 2])
def test_fixed_frame_probabilities_match_complete_low_native_source_enumeration(secret_dimension):
    columns = ((2, 1, 0), (2, 0, 1))
    span = odd_power_basis(columns, 3)
    words = [w for w, _ in span["basis"]]
    zero_kernel, zero_power = 0, 0
    for flat in product(range(3), repeat=3*secret_dimension):
        rows = tuple(flat[3*i:3*i+3] for i in range(secret_dimension))
        kernel = all(sum(a*b for a, b in zip(row, c)) % 3 == 0 for row in rows for c in columns)
        power = all(sum(a*b for a, b in zip(row, c)) % 3 == 0 for row in rows for c in words)
        zero_kernel += kernel
        zero_power += power
    ledger = fixed_frame_probability(secret_dimension, 2, 3)
    assert zero_power == 1
    assert 3**(3*secret_dimension)//zero_power == int(ledger["unconditional_admission_probability_denominator"])
    assert zero_kernel//zero_power == int(ledger["conditional_on_AW_zero_probability_denominator"])
    assert ledger["invalid_after_source_adaptive_frame_selection"]


def test_public_low_kernel_selection_does_not_license_fixed_frame_probability():
    packet = compile_packet([[(1, 0)]]*3, 9)
    frame = ((1, 0), (0, 1))
    record = native_restriction(packet, frame)
    assert not record["fixed_frame_probability_applicable_to_this_source_adaptive_kernel_frame"]
    assert not record["higher_Schur_admission"]
    assert not record["secret_decoder_or_generic_no_go"]


def test_native_top_failure_witness_matches_every_affine_syndrome_and_base():
    labels = [[(1, 0)], [(3, 1)], [(5, 2)]]
    for syndrome in ((0,), (1,), (2,)):
        packet = compile_packet(labels, 7, syndrome)
        record = native_restriction(packet, ((1, 0), (0, 1)))
        dirs = [(1, 0) if j == 0 else (0, 1) for j in record["mixed_failure_witness"]["basis_factor_indices"]]
        hierarchy = NativePhaseHierarchy.from_packet(packet)
        assert all(hierarchy.derivative(z, dirs) == record["native_top_derivative_of_failure_witness"]
                   for z in product(range(3), repeat=2))


def test_large_native_width_checks_all_top_terms_without_enumerating_multisets():
    record = native_large_countercontrol()["restriction"]
    resources = record["resources"]
    assert len(record["physical_frame_columns"]) == 21
    assert record["power_dimension"] == 24
    assert record["evaluated_through_degree"] == 3
    assert resources["candidate_products_processed"] <= 21+21*21+24*21
    assert int(resources["full_basis_multisets_not_enumerated"]) > 10**10
    assert resources["unknown_weighted_phase_queries"] == 0
    assert not resources["quantum_instrument_or_decoder_supplied"]


def test_rejects_noncanonical_dependent_nonkernel_and_wrong_degree_inputs():
    for columns in ((), ((True, 0),), ((1, 0), (2, 0)), ((1, 0), (0,)), ((3, 0),)):
        with pytest.raises(ValueError):
            frame_columns(columns)
    for degree in (0, 2, 514, True):
        with pytest.raises(ValueError):
            odd_power_basis(((1, 0),), degree)
    with pytest.raises(ValueError):
        schur_admission(((1, 0),), ((1, 0),), 3)
    with pytest.raises(ValueError):
        fixed_frame_probability(1, 3, 2)
    packet = compile_packet([[(1, 0)]]*3, 3)
    with pytest.raises(ValueError):
        native_restriction(packet, ((1, 0, 0),))


def test_report_cannot_promote_top_admission_to_decoder_or_generic_no_go():
    report = run_controls()
    assert not any(report["claim_gate"].values())
    for control in report["evaluation_code_countercontrol"]["level_controls"]:
        assert control["top_admission_only_not_constant_degree_or_decoder"]
        assert not control["source_acquisition_or_full_instrument_charged"]
