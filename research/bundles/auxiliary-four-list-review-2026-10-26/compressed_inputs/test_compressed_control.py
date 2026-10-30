import pytest
from sympy import Matrix

from control import actions, certify, degree_control, u, v


def test_exact_generator_actions_and_quadratic_ideal():
    assert certify(actions())


@pytest.mark.parametrize("degree", range(8))
def test_true_graded_spaces_without_point_evaluation_quotient(degree):
    assert degree_control(degree)["generated_rank"] == (1 if degree == 0 else 4*degree)


def test_wrong_cubic_action_is_not_accepted_by_dimensions():
    matrices = actions()
    matrices[2][0, 3] += u**3
    with pytest.raises(AssertionError):
        certify(matrices)


def test_affine_evaluation_agrees_with_symbolic_multiplication():
    p = 17
    matrices = actions()
    checked = 0
    for x in range(p):
        for y in range(p):
            if (y*y-x**3-2*x-2) % p:
                continue
            frame = Matrix([[1, x, y, x*y]])
            for operator, value in zip(matrices, (1, x*x, x, y)):
                specialized = operator.subs({u: 1, v: x*x})
                assert all(int(z) % p == 0 for z in frame*specialized-value*frame)
            checked += 1
    assert checked == 18
