from pathlib import Path
import sys

import pytest
from sympy import Matrix, eye, zeros

sys.path.insert(0, str(Path(__file__).resolve().parent))
from elliptic_reduction import annihilator_ideal, line_from_doubled_kernel
from kernel_output import (
    action, coordinate_map, inverse_mod, mod, odd_maximal_order, odd_maximal_split,
)


def doubled(line):
    return Matrix.vstack(Matrix.hstack(line, zeros(2, 1)),
                         Matrix.hstack(zeros(2, 1), line))


@pytest.mark.parametrize("ell", [3, 5, 13])
@pytest.mark.parametrize("vector", [(0, 1), (1, 0), (1, 2)])
def test_doubling_recovers_original_left_ideal(ell, vector):
    order, split = odd_maximal_order(11), odd_maximal_split(11, ell)
    line = Matrix(vector)
    plane = doubled(line)*Matrix([[1, 1], [1, 2]])
    recovered = line_from_doubled_kernel(plane+ell*Matrix.ones(4, 2), ell)
    ideal = annihilator_ideal(order, split, recovered, ell)
    assert ideal == annihilator_ideal(order, split, 2*line, ell)
    assert abs(ideal.det()) == ell**2
    assert all(x.q == 1 for x in ideal.inv()*(ell*eye(4)))
    for i in range(4):
        assert mod(action(ideal[:, i], split)*line, ell) == zeros(2, 1)
        for j in range(4):
            assert all(x.q == 1 for x in
                       ideal.inv()*order.multiply(eye(4)[:, j], ideal[:, i]))


def test_image_constraint_is_not_the_annihilator_ideal():
    ell, order = 5, odd_maximal_order(11)
    split, line = odd_maximal_split(11, ell), Matrix([1, 0])
    ideal = annihilator_ideal(order, split, line, ell)
    e11 = mod(inverse_mod(coordinate_map(split), ell)*Matrix([1, 0, 0, 0]), ell)
    assert mod(action(e11, split)*line, ell) == line
    assert any(x.q != 1 for x in ideal.inv()*e11)
    # E11 has image in L, so an image-constraint implementation would
    # incorrectly accept this element as killing the original kernel.


def test_common_mask_is_required_for_mixing_between_copies():
    r = 7
    phi = Matrix([[2, -1], [1, 2]])
    exact = Matrix.diag(phi, phi)
    sigma = eye(4)
    sigma[:2, 2:] = eye(2)
    s = sigma.T*sigma
    same = 3*exact
    different = Matrix.diag(3*phi, 2*phi)
    target = mod(exact*s*inverse_mod(exact, r), r)
    assert mod(same*s*inverse_mod(same, r), r) == target
    assert mod(different*s*inverse_mod(different, r), r) != target


@pytest.mark.parametrize("kernel", [
    Matrix([[1, 0], [0, 0], [0, 0], [0, 1]]),
    Matrix([[1, 0], [0, 1], [1, 0], [0, -1]]),
    Matrix([[1, 1], [0, 0], [0, 0], [0, 0]]),
])
def test_nondoubled_or_rank_deficient_plane_is_rejected(kernel):
    with pytest.raises(ValueError):
        line_from_doubled_kernel(kernel, 5)


def test_invalid_postprocessing_input():
    order, split = odd_maximal_order(11), odd_maximal_split(11, 5)
    for line, ell in ((Matrix([0, 0]), 5), (Matrix([1, 0]), 9),
                      (Matrix([1, 0, 0]), 5)):
        with pytest.raises(ValueError):
            annihilator_ideal(order, split, line, ell)
    with pytest.raises(ValueError):
        line_from_doubled_kernel(eye(2), 5)
