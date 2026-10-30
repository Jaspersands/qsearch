"""Exact supplied-map/module controls; no elliptic points or quotient backend."""

from itertools import count
from pathlib import Path
import sys

from sympy import Matrix, eye, zeros

from projective_calibration import GroupOperations, calibrate_basis

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "kernel-output-2026-10-23"))
sys.path.insert(0, str(ROOT / "native-membership-baseline-2026-10-25"))
from kernel_output import action, inverse_mod, mod, odd_maximal_order, odd_maximal_split
from controls_membership import conjugate, rational_mod


def vector_operations(prime, dimension):
    return GroupOperations((0,)*dimension,
        lambda a, b: tuple((x+y) % prime for x, y in zip(a, b)),
        lambda k, a: tuple(k*x % prime for x in a))


def vector_control(matrix, prime, masks):
    matrix = mod(matrix, prime)
    if matrix.rows != matrix.cols or matrix.det() % prime == 0:
        raise ValueError("invertible square supplied map required")
    dimension = matrix.rows
    basis = tuple(tuple(int(x) for x in eye(dimension)[:, j]) for j in range(dimension))
    operations = vector_operations(prime, dimension)
    masks = tuple(masks)
    if len(masks) != 2*dimension-1 or any(type(x) is not int or x % prime == 0 for x in masks):
        raise ValueError("one nonzero mask per planned weak call required")
    calls = count()

    def weak(point):
        mask = masks[next(calls)]
        return tuple(int(x) for x in mod(mask*matrix*Matrix(point), prime))

    result = calibrate_basis(prime, basis, weak, operations, operations)
    calibrated = Matrix.hstack(*(Matrix(p) for p in result["images"]))
    assert calibrated == mod(masks[0]*matrix, prime)
    assert next(calls) == 2*dimension-1
    return result


def quaternion_control(prime):
    """phi=1+i and alpha=(1+j)/2 on the known characteristic-11 order."""
    order = odd_maximal_order(11)
    phi, alpha = Matrix([1, 1, 0, 0]), Matrix([0, 0, 1, 0])
    split = odd_maximal_split(11, prime)
    phi_r, alpha_r = (mod(action(x, split), prime) for x in (phi, alpha))
    result = vector_control(phi_r, prime, (1, 2, prime-1))
    raw = Matrix.hstack(*(Matrix(p) for p in result["raw_images"]))
    calibrated = Matrix.hstack(*(Matrix(p) for p in result["images"]))
    correct = rational_mod(action(conjugate(order, phi, alpha), split), prime)
    restored = mod(calibrated*alpha_r*inverse_mod(calibrated, prime), prime)
    assert restored == correct
    naive = mod(raw*alpha_r*inverse_mod(raw, prime), prime)
    doubled = Matrix.diag(calibrated, calibrated)
    assert doubled == mod(Matrix.diag(phi_r, phi_r), prime)
    assert all(x.q == 1 for x in phi)
    return {"prime": prime, "degree": 2,
            "weak_point_calls": result["weak_point_calls"],
            "coordinate_table_entries": result["coordinate_table_entries"],
            "independent_column_masks": [1, 2], "bridge_mask": prime-1,
            "naive_conjugation_wrong": naive != correct,
            "calibrated_conjugation_correct": True,
            "doubled_copy_shares_one_mask": True,
            "supplied_map_control": True, "actual_curve_points_generated": False,
            "unknown_isogeny_recovered": False}


def incomplete_frame_countercontrol():
    """Without a bridge, two genuine linear maps fit the SAME two responses."""
    prime = 5
    first, second = eye(2), Matrix.diag(1, 2)
    responses = eye(2)
    assert mod(first*eye(2), prime) == responses
    assert mod(second*Matrix.diag(1, 3), prime) == responses
    bridge_a, bridge_b = mod(first*Matrix([1, 1]), prime), mod(second*Matrix([1, 1]), prime)
    assert Matrix.hstack(bridge_a, bridge_b).det() % prime != 0
    return {"prime": prime, "basis_responses_identical": True,
            "projective_maps_different": True, "sum_line_responses_separate": True,
            "scope": "finite-module ambiguity, not independently instantiated curve maps"}
