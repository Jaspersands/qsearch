from itertools import product
from pathlib import Path
from random import Random
import sys

import pytest
from sympy import Matrix, eye, zeros

sys.path.insert(0, str(Path(__file__).resolve().parent.parent/"smooth-repolarization-2026-10-23"))
from smooth_repolarization import certificate, evaluate
from prime_square_flags import (
    basis, contained, mod, refine, residual_quotient, scalar_torsion_extension,
    stable_under, symplectic_form,
)


def group_elements(generators, orders, modulus):
    return {tuple(int(v) % modulus for v in generators*Matrix(coefficients))
            for coefficients in product(*(range(order) for order in orders))}


@pytest.mark.parametrize("r", [2, 3, 5])
@pytest.mark.parametrize("free_rank", [0, 1, 2])
def test_all_kernel_types_and_quotient_orders(r, free_rank):
    rng = Random(40+free_rank)
    j, u, n = symplectic_form(2), eye(4), r*r
    for _ in range(5):
        v = Matrix([rng.randrange(n) for _ in range(4)])
        u = mod(u*(eye(4)+v*v.T*j), n)
    diagonal = [entry for i in range(2) for entry in ((0, 1) if i < free_rank else (r, r))]
    matrix = mod(Matrix.diag(*diagonal)*u.inv_mod(n), n)
    flag = refine(matrix, r)
    assert flag.free_rank == free_rank
    assert flag.multiplied_kernel.cols == free_rank
    assert flag.torsion_kernel.cols == 4-free_rank
    assert flag.first_kernel.cols == 2
    full = group_elements(flag.generators, flag.generator_orders, n)
    first = group_elements(r*flag.first_kernel, (r, r), n)
    assert len(full) == r**4 and len(first) == r**2 and first <= full
    assert {tuple(r*x % n for x in point) for point in full} <= first
    representatives = {min(tuple((x+y) % n for x, y in zip(point, h)) for h in first) for point in full}
    assert len(representatives) == r*r
    residual = residual_quotient(flag)
    assert residual["residual_kernel"].cols == 2
    assert abs(int(residual["quotient_matrix"].det())) == r*r
    assert all(stable_under(flag.first_kernel, a*eye(4), r) for a in range(1, r))


@pytest.mark.parametrize("r", [2, 3, 5])
def test_old_rG_shortcut_fails_and_refinement_succeeds(r):
    flag = refine(r*eye(2), r)
    assert flag.multiplied_kernel.cols == 0
    assert flag.torsion_kernel.cols == 2
    assert flag.first_kernel.cols == 1
    assert flag.receipt()["second_quotient_order"] == str(r)


@pytest.mark.parametrize("r", [2, 3, 5])
def test_prior_32_dimensional_repolarization_kernel(r):
    h = ((1, 0, 1, -2), (0, 1, 2, 1), (1, 2, 6, 0), (-2, 1, 0, 6))
    f = Matrix(evaluate(certificate(7, 30)["E"], h))
    flag = refine(f, r)
    assert flag.dimension == 16 and flag.first_kernel.cols == 16
    assert flag.free_rank == {2: 0, 3: 16, 5: 8}[r]
    assert residual_quotient(flag)["residual_kernel"].cols == 16
    assert stable_under(flag.first_kernel, -103*eye(32), r)


@pytest.mark.parametrize("r", [2, 3, 5])
def test_actual_61_isogeny_source_control(r):
    phi = Matrix([[6, -5, 0, 0], [5, 6, 0, 0], [0, 0, 6, 5], [0, 0, -5, 6]])
    sigma = Matrix([[1, 0, 61, 0], [0, 1, 0, 61], [0, 0, 1, 0], [0, 0, 0, 1]])
    h = phi*sigma.T*sigma*phi.T/61
    integer_h = tuple(tuple(int(x) for x in h.row(i)) for i in range(4))
    f = Matrix(evaluate(certificate(3723, 30030)["E"], integer_h))
    flag = refine(f, r)
    assert flag.first_kernel.cols == 16
    assert contained(flag.multiplied_kernel, flag.first_kernel, r)
    assert stable_under(flag.first_kernel, -103*eye(32), r)


def test_without_scalar_frobenius_a_rational_flag_need_not_exist():
    # Characteristic polynomial x^2+1 has no root mod 3. It preserves G=X[3]
    # inside X[9] but preserves no line in X[3]. This is a local countercontrol.
    r, frobenius = 3, Matrix([[0, -1], [1, 0]])
    flag = refine(r*eye(2), r)
    assert not stable_under(flag.first_kernel, frobenius, r)
    lines = [Matrix([1, a]) for a in range(r)]+[Matrix([0, 1])]
    assert all(not stable_under(line, frobenius, r) for line in lines)
    assert all(stable_under(line, frobenius**2, r) for line in lines)


@pytest.mark.parametrize("r", [2, 3, 5, 7, 11, 13, 17])
def test_scalar_frobenius_torsion_degree(r):
    degree = scalar_torsion_extension(-103, r)
    assert degree <= r*(r-1)
    assert pow(-103, degree, r*r) == 1
    assert all(pow(-103, k, r*r) != 1 for k in range(1, degree))


def test_invalid_kernel_promises_rejected():
    with pytest.raises(ValueError, match="order"):
        refine(eye(4), 3)
    with pytest.raises(ValueError, match="isotropic"):
        refine(Matrix.diag(0, 0, 1, 1), 3)
    with pytest.raises(ValueError, match="prime"):
        refine(3*eye(2), 9)
    with pytest.raises(ValueError, match="pairing"):
        refine(3*eye(2), 3, zeros(2))
    with pytest.raises(ValueError, match="coprime"):
        scalar_torsion_extension(3, 3)
