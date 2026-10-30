"""Structural controls; finite split matrices are not unknown native inputs."""

from itertools import product
from pathlib import Path
import sys

import pytest
from sympy import Matrix, Rational, eye

from local_orders import (
    contains, invariant_lines, local_integral, neighbor_frames,
    path_intersection_basis, recover_path_vertex, scalar_order_basis, units,
)

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "classical-symmetry-harvest-2026-10-26"))
from test_harvest import unit_closed_index_seventeen_order
from kernel_output import action, lift_split, mod, odd_maximal_order, odd_maximal_split


@pytest.mark.parametrize("q", [2, 3, 5, 17])
def test_scalar_order_has_center_and_every_neighbor_but_not_distance_two(q):
    basis = scalar_order_basis(q)
    assert abs(Matrix.hstack(*(Matrix(list(x)) for x in basis)).det()) == q**3
    frames = (eye(2),)+neighbor_frames(q)
    assert len(frames) == q+2
    for frame in frames:
        assert all(contains(frame, x, q) for x in basis)
    assert not all(contains(Matrix.diag(1, q*q), x, q) for x in basis)
    # This rejects substituting an arbitrary abstract overorder for End(E).
    assert not contains(neighbor_frames(q)[0], units()[2], q)
    assert not local_integral(Rational(1, q)*units()[1], q)
    assert contains(neighbor_frames(q)[0], Rational(1, q)*units()[1], q)


@pytest.mark.parametrize("q,length", [(2, 3), (3, 2), (17, 1)])
def test_eichler_interval_contains_exactly_the_path_segment(q, length):
    for lo in range(length+1):
        for hi in range(lo, length+1):
            basis = path_intersection_basis(q, lo, hi)
            for target in range(length+2):
                assert all(contains(Matrix.diag(1, q**target), x, q)
                           for x in basis) == (lo <= target <= hi)


@pytest.mark.parametrize("q,length", [(2, 7), (3, 2), (17, 1), (2**61-1, 31)])
def test_bass_path_selection_does_not_enumerate_prime_sized_directions(q, length):
    for target in range(length+1):
        frame = Matrix.diag(1, q**target)
        result = recover_path_vertex(q, length, lambda x: contains(frame, x, q))
        assert result["vertex"] == target
        assert result["membership_calls"] <= 4*length.bit_length()
        assert result["native_recovery_executed"] is False


def test_empty_path_and_unknown_backend():
    def forbidden(_):
        raise AssertionError("length-zero path requires no queries")
    assert recover_path_vertex(3, 0, forbidden)["membership_calls"] == 0
    with pytest.raises(ValueError, match="UNKNOWN"):
        recover_path_vertex(3, 2, lambda _: None)


@pytest.mark.parametrize("q", [2, 3])
def test_complete_small_matrix_incidence_reuses_eigenline_barrier(q):
    frames = neighbor_frames(q)
    for values in product(range(q), repeat=4):
        matrix = Matrix(2, 2, values)
        actual = tuple(i for i, f in enumerate(frames) if contains(f, matrix, q))
        assert actual == invariant_lines(matrix, q)
        scalar = values[1] == values[2] == 0 and values[0] == values[3]
        assert len(actual) == q+1 if scalar else len(actual) <= 2


@pytest.mark.parametrize("q", [2, 3, 5])
def test_nonintegral_neighbor_elements_never_select_two_distinct_leaves(q):
    frames = neighbor_frames(q)
    for frame in frames:
        for x in units():
            moved = frame*x*frame.inv()
            if not local_integral(moved, q):
                assert sum(contains(f, moved, q) for f in frames) == 1


def test_previous_index_seventeen_fixture_is_borel_not_large_branching():
    order = odd_maximal_order(11)
    basis = unit_closed_index_seventeen_order(order)
    split = odd_maximal_split(11, 17)
    images = [action(basis[:, i], split) for i in range(4)]
    common = set(range(18))
    for x in images:
        common.intersection_update(invariant_lines(x, 17))
    # Exactly its center and one neighbor: the native target is already known
    # in this fixture; this checks the local order type, not native discovery.
    assert common == {13}  # (1,13) spans the earlier line (4,1).
    assert basis.det() == 17


def test_previous_index_nine_fixture_has_split_etale_quadratic_core():
    split = odd_maximal_split(11, 3)
    lifted = lift_split(odd_maximal_order(11), split, 3)
    h = lifted[2]
    assert mod(h*h-h+3*eye(2), 9) == Matrix.zeros(2)
    roots = [x for x in range(9) if (x*x-x+3) % 9 == 0]
    assert roots == [3, 7]
    assert all((2*x-1) % 3 for x in roots)
    # Hensel lifting gives a split etale Z_3[h]. R=Z_3[h]+3*M_2(Z_3)
    # is conjugate to diagonal entries arbitrary, off-diagonals divisible by 3,
    # hence an Eichler path of length two, not a branching non-Bass input.
    basis = Matrix.diag(1, 3, 1, 3)
    assert basis.det() == 9
    assert mod(action(basis[:, 1], lifted), 3) == Matrix.zeros(2)
    assert mod(action(basis[:, 3], lifted), 3) == Matrix.zeros(2)


@pytest.mark.parametrize("q", [1, 9, True])
def test_nonprime_levels_rejected(q):
    with pytest.raises(ValueError, match="prime"):
        neighbor_frames(q)


def test_nonrational_or_singular_matrix_rejected():
    with pytest.raises(ValueError, match="exact rational"):
        local_integral(Matrix([[1.0, 0], [0, 1]]), 3)
    with pytest.raises(ValueError, match="nonsingular"):
        contains(Matrix.zeros(2), eye(2), 3)


def test_receipt_does_not_promote_supplied_controls_to_native_execution():
    from replay_scope import receipt
    result = receipt()
    assert result["execution_scope"]["exact_supplied_local_order_controls"] is True
    assert all(value is False for key, value in result["execution_scope"].items()
               if key != "exact_supplied_local_order_controls")
    assert result["source"]["baseline_has_large_prime_value_dependence_in_general"] is True
