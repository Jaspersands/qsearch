from itertools import product
import random

import numpy as np
import pytest
from sympy import Matrix, eye

from cyclotomic_rescaling_gate import ideal_chart
from ternary_carry_packets import compile_packet
from ternary_phase_depth import (
    NativePhaseHierarchy, cubic_transfer_countercontrol, cyclic_difference,
    degree_visibility, lifted_quadratic_countercontrol, low_degree_alias_control,
    repeated_identity, run_controls, sharp_degree_control,
)


def derivative_cube(packet, base, directions):
    out = [0]*packet.secret_dimension
    for bits in product(range(2), repeat=len(directions)):
        point = tuple((base[j]+sum(b*d[j] for b, d in zip(bits, directions))) % 3 for j in range(packet.retained))
        sign = (-1)**(len(directions)-sum(bits))
        out = [(a+sign*b) % (packet.phase_modulus//3) for a, b in zip(out, packet.residual(point))]
    return tuple(out)


@pytest.mark.parametrize("order", [1, 2, 3, 4, 5, 8, 13, 20])
def test_cyclic_difference_identity_is_exact_integer_matrix_equality(order):
    S = Matrix([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
    delta = S-eye(3)
    record = repeated_identity(order)
    assert delta**order == record["integer_multiplier"]*S**record["cyclic_shift_power"]*delta**record["remaining_difference_order"]


@pytest.mark.parametrize("level", [3, 5, 7])
def test_factored_native_derivatives_equal_complete_cube_at_all_small_orders(level):
    rng = random.Random(49011)
    a, _, b = ideal_chart(level)[0]
    labels = [[(rng.randrange(a), rng.randrange(b))] for _ in range(3)]
    packet = compile_packet(labels, level)
    hierarchy = NativePhaseHierarchy.from_packet(packet)
    points = list(product(range(3), repeat=packet.retained))
    for order in range(0, 6):
        directions = [points[(order+3*j+1) % len(points)] for j in range(order)]
        for base in points[:3]:
            assert hierarchy.derivative(base, directions) == derivative_cube(packet, base, directions)


@pytest.mark.parametrize("level", [3, 5, 7, 9, 13, 19])
def test_degree_grows_sharply_with_native_phase_depth(level):
    record = sharp_degree_control(level)
    assert record["retained_component_derivative"] == (3**((level-3)//2),)
    assert record["next_derivative"] == (0,)
    assert record["exact_additive_degree_of_this_control"] == level
    assert record["resources"]["unknown_weighted_phase_queries"] == 0


@pytest.mark.parametrize("level", [5, 9, 19])
def test_general_top_tensor_and_universal_next_zero_survive_shifted_base_and_syndrome(level):
    rng = random.Random(49021+level)
    a, _, b = ideal_chart(level)[0]
    labels = [[(rng.randrange(a), rng.randrange(b)) for _ in range(2)] for _ in range(5)]
    raw = compile_packet(labels, level)
    packet = compile_packet(labels, level, tuple(1 for _ in raw.pivots))
    hierarchy = NativePhaseHierarchy.from_packet(packet)
    directions = [tuple(rng.randrange(3) for _ in range(packet.retained)) for _ in range(level)]
    for base in ((0,)*packet.retained, (1,)*packet.retained, (2,)*packet.retained):
        assert hierarchy.derivative(base, directions) == hierarchy.top_derivative(directions)
        assert hierarchy.derivative(base, directions+[(1,)*packet.retained]) == (0,)*packet.secret_dimension


def test_level3_cubic_subspace_does_not_pass_level5_weighted_fifth_gate():
    record = cubic_transfer_countercontrol()
    assert record["all_kernel_and_cubic_weighted_products_zero"]
    assert record["weighted_square_square_linear_product_mod3"] == 2
    assert [c["fifth_derivative"] for c in record["native_level_controls"]] == [(0,), (3,)]
    assert not record["level3_cubic_admission_transfers_to_level5"]
    assert not record["source_cost_or_secret_decoder_supplied"]
    assert not record["full_27_input_quantum_instrument_replayed"]


def test_formal_lifted_quadratic_degree_does_not_mean_additive_degree_two():
    record = lifted_quadratic_countercontrol()
    assert record["formal_lifted_polynomial_degree"] == 2
    assert record["actual_additive_phase_degree"] == 4
    assert record["all_repeated_cyclic_derivative_tables"][4] == (3, 3, 3)
    assert not record["classical_quadratic_F3_transfer_admitted"]


@pytest.mark.parametrize("digits", [2, 4, 8])
def test_constant_additive_degree_aliases_high_secret_digits_exactly(digits):
    record = low_degree_alias_control(digits)
    first, second = (np.array([complex(*z) for z in row]) for row in record["calibration_phase_amplitudes"])
    assert max(abs(first-second)) < 4e-12
    assert record["secret_pair"][1]-record["secret_pair"][0] == 3
    assert record["third_derivative_table"] == (0, 0, 0)
    assert abs(np.vdot(first, second)) == pytest.approx(1)
    ledger = degree_visibility(digits, 2)
    assert ledger["maximum_relative_phase_order"] == "3"
    assert not ledger["all_residual_secret_digits_could_be_retained"]
    assert not ledger["degree_bound_itself_certified_by_this_ledger"]


def test_visibility_degree_requirement_handles_every_growing_phase_digit():
    for digits in range(1, 21):
        assert degree_visibility(digits, 2*digits-1)["all_residual_secret_digits_could_be_retained"]
        assert not degree_visibility(digits, 2*digits-2)["all_residual_secret_digits_could_be_retained"]
        assert degree_visibility(digits, 0)["maximum_relative_phase_order"] == "1"


def test_large_native_derivative_work_is_polynomial_not_cube_or_phase_table_materialization():
    rng = random.Random(49031)
    a, _, b = ideal_chart(19)[0]
    labels = [[(rng.randrange(a), rng.randrange(b)) for _ in range(4)] for _ in range(36)]
    packet = compile_packet(labels, 19)
    hierarchy = NativePhaseHierarchy.from_packet(packet)
    directions = [tuple((j*i+i+1) % 3 for j in range(packet.retained)) for i in range(20)]
    assert hierarchy.derivative((0,)*packet.retained, directions) == (0,)*4
    resources = hierarchy.resources(20)
    assert packet.retained == 32
    assert resources["local_modular_subtractions"] == 8640
    assert resources["derivative_cube_vertices_not_materialized"] == "1048576"
    assert resources["full_phase_table_not_materialized"] == str(3**32)
    assert not resources["coherent_unknown_preparation_or_inverse_supplied"]


def test_invalid_phase_model_and_unbounded_requests_are_rejected():
    with pytest.raises(ValueError, match="odd-level"):
        NativePhaseHierarchy.from_packet(type("Invalid", (), {"level": 4})())
    with pytest.raises(ValueError, match="capped"):
        repeated_identity(513)
    with pytest.raises(ValueError):
        degree_visibility(4, True)
    with pytest.raises(ValueError, match="canonical"):
        cyclic_difference((0, 1, 2), True, 9)


def test_report_is_research_evidence_not_candidate_admission():
    assert not any(run_controls()["claim_gate"].values())
