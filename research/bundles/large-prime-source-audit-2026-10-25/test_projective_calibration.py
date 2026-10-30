from itertools import product
from pathlib import Path
import sys

import pytest
from sympy import Matrix, eye

sys.path.insert(0, str(Path(__file__).resolve().parent))
from projective_calibration import calibrate_basis, coordinate_table
from calibration_controls import (
    incomplete_frame_countercontrol, quaternion_control, vector_control, vector_operations,
)


@pytest.mark.parametrize("prime,dimension", [(3, 2), (5, 2), (3, 4)])
def test_every_mask_assignment_on_a_projective_frame(prime, dimension):
    matrix = eye(dimension)
    matrix[0, 1] = 1
    matrix[1, 0] = 1
    matrix[1, 1] = 2
    for masks in product(range(1, prime), repeat=2*dimension-1):
        result = vector_control(matrix, prime, masks)
        assert result["weak_point_calls"] == 2*dimension-1
        assert result["coordinate_table_entries"] == 2*prime**dimension
        assert not result["global_isogeny_promise_verified"]
        assert not result["common_scalar_known"]


@pytest.mark.parametrize("prime", [3, 5, 7, 13, 17])
def test_supplied_quaternion_map_restores_conjugation(prime):
    record = quaternion_control(prime)
    assert record["calibrated_conjugation_correct"]
    assert record["doubled_copy_shares_one_mask"]
    assert not record["unknown_isogeny_recovered"]
    assert record["naive_conjugation_wrong"]


def test_basis_responses_alone_are_insufficient():
    assert incomplete_frame_countercontrol()["sum_line_responses_separate"]


def test_zero_mask_and_dependent_target_basis_are_rejected():
    operations = vector_operations(5, 2)
    basis = ((1, 0), (0, 1))
    with pytest.raises(ValueError, match="nonzero"):
        calibrate_basis(5, basis, lambda _: (0, 0), operations, operations)
    with pytest.raises(ValueError, match="dependent"):
        calibrate_basis(5, basis, lambda _: (1, 0), operations, operations)


@pytest.mark.parametrize("bridge", [(1, 0), (0, 1), (0, 0)])
def test_degenerate_bridge_is_rejected(bridge):
    operations = vector_operations(5, 2)
    responses = iter(((1, 0), (0, 2), bridge))
    with pytest.raises(ValueError, match="projective-frame"):
        calibrate_basis(5, ((1, 0), (0, 1)), lambda _: next(responses), operations, operations)


def test_bridge_with_extra_coordinate_is_rejected():
    operations = vector_operations(3, 4)
    basis = tuple(tuple(int(x) for x in eye(4)[:, j]) for j in range(4))
    responses = iter(basis+((1, 1, 1, 0),))
    with pytest.raises(ValueError, match="projective-frame"):
        calibrate_basis(3, basis, lambda _: next(responses), operations, operations)


def test_invalid_source_basis_rejected_before_weak_calls():
    operations = vector_operations(5, 2)
    def forbidden(_):
        pytest.fail("invalid source must be rejected before a weak call")
    with pytest.raises(ValueError, match="dependent"):
        calibrate_basis(5, ((1, 0), (2, 0)), forbidden, operations, operations)


def test_large_prime_budget_rejected_before_weak_calls():
    operations = vector_operations(65537, 2)
    def forbidden(_):
        pytest.fail("no huge torsion table may be allocated or queried")
    with pytest.raises(ValueError, match="budget"):
        calibrate_basis(65537, ((1, 0), (0, 1)), forbidden, operations, operations)


@pytest.mark.parametrize("prime", [1, 4, 9])
def test_nonprime_levels_rejected(prime):
    operations = vector_operations(prime, 2)
    with pytest.raises(ValueError, match="prime"):
        coordinate_table(prime, ((1, 0), (0, 1)), operations)


def test_calibration_does_not_certify_unqueried_responses():
    operations = vector_operations(5, 2)
    basis = ((1, 0), (0, 1))
    def inconsistent(point):
        return point if point in basis+((1, 1),) else (1, 0)
    result = calibrate_basis(5, basis, inconsistent, operations, operations)
    assert result["images"] == basis
    assert inconsistent((1, 2)) != (1, 2)
    assert not result["other_weak_responses_verified"]
    assert not result["global_isogeny_promise_verified"]
